# 从零实现一个需求的完整步骤（复制即用模板）

以「在 feature_pet 里新增宠物洗澡记录页（列表 + 新增）」为例。任何普通页面需求都按这 10 步走。

> 给人类操作者：把本文件连同需求描述一起发给 AI 助手，让它逐步执行；每步完成跑一次对应验证命令。

## Step 0：明确四件事再动手

1. 页面属于哪个 feature 包？（新业务域才需要建包，见 project-structure.md）
2. 接口地址和字段（找后端要接口文档）
3. 设计稿（确认是 375 宽基准标注）
4. 是否要新权限/新原生能力？（要→先读 permissions.md / compatibility.md）

## Step 1：接口地址

```dart
// packages/feature/feature_pet/lib/src/api/pet_api_endpoints.dart
import 'package:shared_business/app_config.dart';

class PetApiEndpoints {
  const PetApiEndpoints();
  String get petBathList => '${AppConfig.iotHost}/pet/bath/list';
  String get petBathAdd  => '${AppConfig.iotHost}/pet/bath/add';
}
```

## Step 2：数据模型

```dart
// lib/src/model/pet/tq_pet_bath_model.dart
import 'package:core_base/safe_utils.dart';

class TqPetBathModel {
  TqPetBathModel({this.id, this.petName, this.bathTime});

  final String? id;
  final String? petName;
  final String? bathTime;

  factory TqPetBathModel.fromJson(Map<String, dynamic> json) {
    return TqPetBathModel(
      id: TCheck<String>(json['id']),
      petName: TCheck<String>(json['petName']),
      bathTime: TCheck<String>(json['bathTime']),
    );
  }

  Map<String, dynamic> toJson() => {'id': id, 'petName': petName, 'bathTime': bathTime};
}
```

要点：字段可空、`TCheck` 包裹、必须能 toJson（路由传参用）。

## Step 3：State + Controller

```dart
// lib/src/controller/pet/tq_pet_bath_controller.dart
import 'package:flutter/material.dart';
import 'package:riverpod/riverpod.dart';
import 'package:core_http/core_http.dart';
import 'package:core_base/safe_utils.dart';
import '../api/pet_api_endpoints.dart';
import '../model/pet/tq_pet_bath_model.dart';

@immutable
class PetBathState {
  PetBathState({List<TqPetBathModel> baths = const <TqPetBathModel>[]})
    : baths = List<TqPetBathModel>.unmodifiable(baths);

  final List<TqPetBathModel> baths;
}

class TQPetBathController extends StateNotifier<PetBathState> {
  TQPetBathController({PetApiEndpoints? endpoints})
    : _endpoints = endpoints ?? const PetApiEndpoints(),
      super(PetBathState());

  final PetApiEndpoints _endpoints;
  int _generation = 0;

  /// 请求洗澡记录列表
  Future<void> requestBathList({bool showLoading = true}) async {
    final generation = ++_generation;
    var result = await TQHttp.postWithConfig(
      _endpoints.petBathList,
      params: {},
      showLoading: showLoading,
      showErrorToast: true,
    );
    if (!mounted || generation != _generation) return;   // 防销毁/竞态
    if (result.success) {
      final list = TCheck<List>(result.data) ?? [];
      state = PetBathState(
        baths: list.map((e) => TqPetBathModel.fromJson(TCheck<Map<String, dynamic>>(e) ?? {})).toList(),
      );
    }
  }

  /// 新增记录后刷新
  Future<bool> addBathRecord(Map<String, dynamic> params) async {
    var result = await TQHttp.postWithLoadingAndErrTip(_endpoints.petBathAdd, params: params);
    if (!mounted) return false;
    if (result.success) await requestBathList();
    return result.success;
  }
}

// lib/src/state/pet_bath_provider.dart
import 'package:riverpod/riverpod.dart';

final petBathProvider =
    StateNotifierProvider.autoDispose<TQPetBathController, PetBathState>(
      (ref) => TQPetBathController(),
    );
```

页面级状态用 autoDispose；若是全局共享状态，记得注册 session 重置（state-management.md §3）。

## Step 4：路由名

```dart
// src/router/feature_pet_router.dart 追加：
static const petBathList = 'pet_bath_list';
// 并把 petBathList 加进 routeNames 集合。
```

## Step 5：页面

```dart
// lib/src/pages/pet/pet_bath_list_page.dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:core_base/num_extension.dart';
import 'package:core_base/safe_utils.dart';
import 'package:core_i18n/core_i18n.dart';
import 'package:core_ui/tq_appbar.dart';
import 'package:core_ui/tq_no_data_widget.dart';
import '../../model/pet/tq_pet_bath_model.dart';
import '../../router/feature_pet_router.dart';
import '../../state/pet_bath_provider.dart';

/// 宠物洗澡记录页
class PetBathListPage extends ConsumerWidget {
  const PetBathListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return _PetBathListView(
      state: ref.watch(petBathProvider),
      controller: ref.read(petBathProvider.notifier),
    );
  }
}

class _PetBathListView extends StatelessWidget {
  const _PetBathListView({required this.state, required this.controller});

  final PetBathState state;
  final TQPetBathController controller;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: TQAppBar(title: '洗澡记录'.tr),
      body: state.baths.isEmpty
          ? TQNoDataWidget()
          : ListView.separated(
              padding: EdgeInsets.symmetric(horizontal: 15.sc, vertical: 12.sc),
              itemCount: state.baths.length,
              itemBuilder: (_, index) => _buildItem(context, state.baths[index]),
              separatorBuilder: (_, __) => SizedBox(height: 8.sc),
            ),
    );
  }

  Widget _buildItem(BuildContext context, TqPetBathModel item) {
    return ListTile(
      title: Text((item.petName ?? '').tr),
      subtitle: Text(item.bathTime ?? ''),
      onTap: () {}, // 详情跳转按 routing.md 补
    );
  }
}
```

要点：文案 `.tr`、尺寸 `.sc`、外层壳 watch/read 分离、空态用现成组件。

## Step 6：export 对外暴露

`packages/feature/feature_pet/lib/feature_pet.dart` 追加：

```dart
export 'src/api/pet_api_endpoints.dart';            // 若外部要用
export 'src/controller/pet/tq_pet_bath_controller.dart';
export 'src/model/pet/tq_pet_bath_model.dart';
export 'src/pages/pet/pet_bath_list_page.dart';
export 'src/state/pet_bath_provider.dart';
```

## Step 7：app 层注册路由

```dart
// apps/tuqiang_app/lib/app/router/app_router.dart
static const String petBathList = FeaturePetRouter.petBathList;
// 并在 routes 注册处映射：
// FeaturePetRouter.petBathList: (_) => const PetBathListPage(),
```

## Step 8：多语言文案（9 个文件）

页面里出现的每个中文串，去 `apps/tuqiang_app/assets/i18n/` 在 **zh_CN / en_US / ar / de / es / fr / id / it / vi** 九个 JSON 各加一条：

```json
"洗澡记录": "洗澡记录",        // zh_CN（值=原文）
"Bath Records": "Bath Records" // en_US；其余 7 个语言给对应翻译
```

## Step 9：入口接线（谁打开这个页面）

- 列表卡片点击进入：找到宿主 widget 的 onTap，加 `Navigator.pushNamed(context, FeaturePetRouter.petBathList)`；
- 需要登录态数据：确认 provider 是 autoDispose 或已注册 session reset；
- 涉及原生跳转：补 nativeRouters（routing.md §3）。

## Step 10：防御性自检与验证提交

### 1. 交付前自检清单（Pre-delivery Checklist）
在执行验证命令与交付 Review 前，AI 必须完成以下逐项自检：
- [ ] **改动范围控制**：是否做到了外科手术式精准修改，没有误改或顺手格式化无关文件？
- [ ] **异步与生命周期安全**：所有异步网络请求后是否都有 `if (!mounted) return;` 保护？
- [ ] **资源释放**：StatefulWidget 中的 Controller、FocusNode、Subscription 是否在 `dispose()` 中成对释放？
- [ ] **UI 与适配**：所有尺寸间距字号是否都使用了 `.sc`？底部按钮/面板是否适配了 `Screen.bottomSafeHeight`？
- [ ] **多语言覆盖**：新增的页面文案是否都加了 `.tr`，并且在 9 个 JSON 文件中补齐了对应词条？
- [ ] **状态管理与重置**：全局非 autoDispose 的 Provider 是否已向 `SessionResetRegistry` 注册？
- [ ] **三端与鸿蒙红线**：公共代码中是否杜绝了 `Platform.isOhos` / `OhosView` 等非法符号？

### 2. 本地全量验证命令
```powershell
dart run tool/project.dart pub-get standard --enforce-lockfile   # 改了依赖才需要
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos        # 动了公共包必跑
.\tool\check_migration_boundaries.ps1          # 动了依赖/平台相关必跑
dart run tool/project.dart run standard        # 真机自检三语言切换
```

### 3. 交付审查与提交规范
- ⚠️ **验证全绿后，不要擅自自动执行 `git commit`**，保持工作区干净并等待用户或其他模型进行 Code Review 确认。
- Code Review 确认无误后，提交 message 使用 **Angular 规范（简短中文）**：

| 前缀 | 场景 | 示例 |
|---|---|---|
| `feat:` | 新功能 | `feat: 新增宠物洗澡记录页` |
| `fix:` | 修复 Bug | `fix: 修复信标列表越界崩溃` |
| `refactor:` | 重构 | `refactor: 提取设备卡片公共组件` |
| `docs:` | 文档/说明 | `docs: 补充接口文档` |
| `style:` | 样式/UI 调整 | `style: 解绑按钮上下居中` |
| `chore:` | 构建/工具/配置 | `chore: 升级依赖版本` |
| `perf:` | 性能优化 | `perf: 优化地图渲染流畅度` |
| `test:` | 测试 | `test: 补充信标数据解析单测` |

## 附：常见需求 → 差异点速查

| 需求类型 | 与模板的差异 |
|---|---|
| 表单提交页 | Step 3 controller 加表单校验方法；输入框用 TextEditingController（dispose 别忘）；提交按钮防抖（easy_debounce） |
| 含定位/地图 | 先读 permissions.md 定位部分；地图用 tq_map_plugin，参考 feature_gps |
| 含蓝牙设备 | checkBluePermission；蓝牙统一走 core_blue（鸿蒙端由 core_blue_ohos 提供，公共代码不直接 import 它） |
| 含扫码 | mobile_scanner + core_ui/TQScannerOverlay，参考搜索信标页 |
| 含图片上传 | image_picker 选图 → `TQHttp.uploadImage`，参考 core_union 的 image_picker 封装 |
| WebView 页 | 跳 H5 用 core_webview 的 TQWebviewPage，桥接能力见 SharedWebviewBridge |
