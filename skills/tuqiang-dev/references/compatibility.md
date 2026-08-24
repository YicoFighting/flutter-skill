# 三端兼容规范（Android / iOS / HarmonyOS）

本仓库最大的坑就在这一章。目标：**同一套 Dart 业务代码，三端编译运行**。

## 1. 平台判断【红线】

| 场景 | 允许 | 禁止 |
|---|---|---|
| 判断 Android/iOS | `Platform.isAndroid` / `Platform.isIOS`（`dart:io`） | — |
| 判断鸿蒙 | `AppTargetConfig.isOhos`（`core_base/app_target.dart`） | `Platform.isOhos` ❌（官方 SDK 无此符号，边界检查直接挂 CI） |
| 鸿蒙专属 Widget/包（OhosView、xxx_ohos 包） | 只能出现在 app 启动注入层或 ohos 专属工程/插件内 | 出现在 `packages/**/lib`、`apps/tuqiang_app/lib` 任何公共文件 ❌ |

```dart
import 'package:core_base/app_target.dart';

if (AppTargetConfig.isOhos) {
  // 鸿蒙差异行为（这个开关本身是安全的，可以进公共代码）
}
```

CI 红线由 `tool/check_migration_boundaries.ps1` 把守，本地提交前可自行运行确认。

## 2. 平台差异的三种正解（全部来自仓库真实代码）

原则：**公共代码只依赖抽象，端实现由 app 层启动时注入。**

### 模式 A：视图构建器注入（鸿蒙专属 UI）

公共包定义抽象 + 注册点；ohos 入口工程在 main 里注册真实实现：

```dart
// feature_auth/src/platform/harmony_auth_platform.dart （公共包内，安全）
typedef HarmonyAuthViewBuilder = Widget Function({required ValueChanged<String> onAuthCode});

class HarmonyAuthPlatform {
  static HarmonyAuthViewBuilder? _viewBuilder;
  static bool get isAvailable => _viewBuilder != null;
  static void configureViewBuilder(HarmonyAuthViewBuilder builder) => _viewBuilder = builder;

  static Widget buildView({required ValueChanged<String> onAuthCode}) {
    final builder = _viewBuilder;
    if (builder == null) return const SizedBox.shrink();  // 未注册=该端不支持
    return builder(onAuthCode: onAuthCode);
  }
}

// 页面里直接用，无需关心平台：
HarmonyAuthPlatform.buildView(onAuthCode: (code) => ...);
```

### 模式 B：依赖注入回调（行为差异）

```dart
// feature_auth/src/config/auth_dependencies.dart
class AuthDependencies {
  final AuthUserAction onLoginSuccess;   // 登录成功后干什么
  final AuthContextAction jumpToHome;    // 跳主页怎么跳
  // ...
  static void setup(AuthDependencies d) => _current = d;
}

// apps/tuqiang_app/lib/app.dart 启动时装配：
void setupAuthDependencies() {
  AuthDependencies.setup(AuthDependencies(
    onLoginSuccess: (context, user) => LoginUtils.onLoginSuccess(user),
    jumpToHome: (context) =>
        Navigator.of(context).pushNamedAndRemoveUntil(AppRouters.home, (_) => false),
    ...
  ));
}
```

feature 包不 import app 层、不 import 其他 feature，全部通过这类 config/callback 解耦。新 feature 需要「宿主能力」时照抄此模式。

### 模式 C：桥接注册（服务能力）

```dart
// core_webview/webview/bridge/webview_bridge.dart
abstract class WebviewBridge { String? getToken(); Future<bool> saveImageToGallery(String url); ... }

class SharedWebviewBridge {
  static WebviewBridge? _bridge;
  static void register(WebviewBridge bridge) => _bridge = bridge;
  static WebviewBridge get shared => _bridge ?? const _EmptyWebviewBridge(); // 空实现兜底
}

// apps/tuqiang_app/lib/app/webview/app_webview_bridge.dart 提供真实现并注册。
```

## 3. 三方库与插件选型顺序

1. **纯 Dart 库**（无平台通道）：两端通用，正常引入；
2. 有官方/社区 ohos 适配版的库：标准端引原版，`apps/ohos/pubspec.yaml` 用 `dependency_overrides` 覆盖为 ohos 版（git 源如 `openharmony-tpc/flutter_packages.git` 或 `packages/adapter/` 内封装）；
3. 项目自研 tq_* 插件：优先用（tq_push/tq_map/tq_log/tq_filemanage/core_blue…），它们内部已含多端原生实现；
4. 都没有：需求方评估 → 新建 plugin 并按现有 tq_* 插件结构补 android/ios/(ohos) 三份原生代码。

**改依赖后必做**：standard 与 ohos 两端分别 `pub-get --enforce-lockfile` + analyze + 跑边界检查脚本。

## 4. 原生目录速查

| 端 | 工程位置 |
|---|---|
| Android | `apps/standard/android/` |
| iOS | `apps/standard/ios/` |
| 鸿蒙 | `apps/ohos/ohos/`（DevEco 工程，签名读被忽略的 `build-profile.local.json5` 或 OHOS_* 环境变量） |

权限清单三端同步规则见 [permissions.md](permissions.md) §4。

## 5. 常见翻车清单

- ❌ 在公共包写 `Platform.isOhos` → CI 边界挂；
- ❌ 只跑 standard analyze 就提交 → ohos 端编译红；
- ❌ 加依赖忘了鸿蒙 override → ohos pub get 失败或运行时 MissingPluginException；
- ❌ MethodChannel 新通道只在 Android/iOS 实现 → 鸿蒙调用无响应（新通道需在 apps/ohos 对应插件里补实现）；
- ❌ 以为「包在 override 里 = 该能力三端已验证」→ override 只保证能编译注册，**具体 scheme/行为仍需真机验证**。例：`url_launcher` 鸿蒙版（`url_launcher_ohos.har`）对 `tel:` 拨号、`mailto:` 的支持与 Android/iOS 不保证一致，仓库内此前无 `tel:` 先例，首次使用必须鸿蒙真机实测；
- ✅ 不确定时先看同类功能怎么做的（搜仓库里 `AppTargetConfig.isOhos` 的现有用法），再动手。

## 6. 平台 API 能力验证清单【新交互形态必做】

凡是「拉起系统能力」的调用（拨号 tel: / 发邮件 mailto: / 短信 sms: / 应用商店 / 蓝牙配对系统面板等），按端逐一确认：

| 能力 | Android | iOS | 鸿蒙 |
|---|---|---|---|
| `tel:` 拨号 | ✅ 直接可用 | ✅ 可用（可在 Info.plist 加 LSApplicationQueriesSchemes 处理 canLaunch） | ⚠️ 依赖 url_launcher_ohos 实现，**真机实测** |
| 外部浏览器 http(s) | ✅ | ✅ | ✅ 仓库已有先例（tq_page_utils） |
| 剪贴板 Clipboard.setData | ✅ | ✅ | ✅ 引擎层实现 |

规则：表中「⚠️」的能力，编码完成只是第一步，必须列入真机自检；`canLaunchUrl` 在鸿蒙端的返回值也不可与标准端划等号，兜底逻辑（如复制号码）要保留但不能当作「鸿蒙不支持」的结论依据。

## 7. 验证方式

```powershell
.\tool\check_migration_boundaries.ps1
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
```

三条全绿才允许提交涉及平台差异的改动。

## 8. 验证方式（能力类改动附加）

涉及 §6 表格中「⚠️」能力的改动，除上述三条命令外，还需：

- 鸿蒙真机实测该交互（模拟器无法验证拨号盘/邮件客户端拉起）；
- 在 PR 描述里注明「已实测端」与「待验证端」。
