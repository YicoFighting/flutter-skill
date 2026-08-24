# 目录规范与「加东西动哪个包」

## 1. 分层规则

依赖方向必须单向：`apps → feature → shared_business / core`，`core 包之间不互相依赖业务包`。

| 层 | 位置 | 放什么 | 不放什么 |
|---|---|---|---|
| App 入口 | `apps/standard`、`apps/ohos` | 平台配置、签名、渠道、pubspec 差异、dependency_overrides | 业务代码 |
| 公共 App | `apps/tuqiang_app/lib/app/**` | 路由总表 `app_router.dart`、启动编排 `bootstrap.dart`、i18n 资产加载、HTTP delegate、session 协调器 | 可复用的业务页面（该下沉到 feature） |
| 业务模块 | `packages/feature/feature_xxx` | 该业务域的 pages / controller / state / model / router / widgets / assets / callbacks | 其他模块的私有实现 |
| 共享业务 | `packages/shared/shared_business/lib` | 跨模块模型、全局 Provider、manager、device/location 等领域层 | 单个 feature 私有的东西 |
| 基础库 | `packages/core/core_*` | 网络(core_http)、国际化(core_i18n)、UI 组件(core_ui)、工具与权限(core_base)、尺寸适配、webview、分享、地区 core_region | 任何具体业务 |
| 平台插件 | `packages/plugins/tq_*` | 需要原生能力的自研插件（推送、地图、日志、文件、蓝牙、信号、P2P…），内含 android/ios/(ohos) 原生代码 | 纯 Dart 业务 |
| 适配包 | `packages/adapter/*` | 三方库的 ohos 替代实现与封装 | — |

## 2. 「我想加 X，动哪里」决策表

| 你要加的东西 | 动哪里 | 参考范例 |
|---|---|---|
| 某业务的普通页面+状态 | 对应 feature 包的 `src/pages` + `src/state` + `src/controller` | `feature_pet` 的我的信标页四件套 |
| 新接口地址 | 新做法：feature 内建 `src/api/xxx_api_endpoints.dart`；存量做法：`shared_business/lib/common/address.dart` 的 `TQAddress` 加 getter | `feature_auth/src/api/auth_api_endpoints.dart` |
| 接口请求方法 | feature 内 `src/repository/xxx_repository.dart`，返回 `ResultModel` | `auth_repository.dart` |
| 可复用 UI 组件 | `packages/core/core_ui/lib/` 根目录一个文件，命名 `tq_xxx.dart` | `tq_appbar.dart`、`tq_no_data_widget.dart` |
| 字符串/数字/日期工具 | `core_base/lib/xxx_extension.dart` 或 `tq_xxx_util.dart`；日期相关放 `core_union` | `num_extension.dart`、`string_extension.dart` |
| 图片/静态资源 | 对应 feature 的 `lib/src/assets/` 目录 + `feature_xxx_assets.dart` 注册路径；跨端公共静态资源放 `packages/assets_common/` | `feature_pet_assets.dart` |
| 全局单例 manager（登录态等） | `shared_business/lib/manager/`（存量 `lib/common/manager/` 仍有 TQInfoManager 等，跟随现状） | `TQGlobalModel`、`TQInfoManager` |
| 新原生能力 | 先查 `plugins/` 有没有 tq_* 插件；没有→新建插件或走 adapter 替代 | `tq_push_plugin` |
| 三方库 ohos 版替换 | `packages/adapter/` + `apps/ohos/pubspec.yaml` dependency_overrides | `share_plus_ohos` |
| 多语言文案 | `apps/tuqiang_app/assets/i18n/*.json`（9 个语言文件 + manifest） | 见 i18n.md |

## 3. feature 包的标准内部结构（照此组织）

```text
packages/feature/feature_xxx/
├── lib/
│   ├── feature_xxx.dart            # 对外出口：所有需要暴露的类逐个 export
│   └── src/
│       ├── api/                    # XxxApiEndpoints：接口地址
│       ├── assets/                 # 资源路径注册
│       ├── callbacks/              # 反向回调导航（宿主注入跳转）
│       ├── config/                 # 依赖注入（XxxDependencies.setup 模式）
│       ├── controller/             # XxxController extends StateNotifier<XxxState>
│       ├── model/                  # 数据模型（fromJson/toJson + TCheck 安全取值）
│       ├── pages/                  # 页面 Widget
│       ├── repository/             # 接口请求封装（可选，接口多时拆出）
│       ├── route_effects/          # 路由副作用监听（可选）
│       ├── router/                 # XxxRouter：路由名常量 + routeNames + nativeRouters
│       ├── session/                # 登录态重置 participants
│       ├── state/                  # Provider 定义
│       └── widgets/                # 本模块私有组件
├── pubspec.yaml                    # 只依赖 core_* 与 shared_business，禁止依赖其他 feature
└── test/                           # 有逻辑的 model/controller 尽量配测试
```

硬性要求：

- **对外只经 `feature_xxx.dart` export**。别的包不许 `import 'package:feature_xxx/src/...'` 深路径。
- feature 包之间**禁止互相 import**；确需联动时通过 shared_business 或 callbacks/config 注入解耦（参考 `AuthDependencies`、`SharedWebviewBridge`）。
- 文件命名：类名 `TQ` 前缀（存量惯例），文件名小写下划线。

## 4. pubspec 注意事项

- 各 package 的 pubspec 用 path 依赖仓库内包；版本号只对 pub.dev 三方库声明。
- `apps/standard/pubspec.yaml` 有 `fluwx:` 配置段（微信 app_id/universal_link），别误删。
- `apps/ohos/pubspec.yaml` 靠大段 `dependency_overrides` 把三方库换成 ohos 版；改标准端依赖后必须检查鸿蒙端是否也要同步 override。
- 提交不得包含 `pubspec.lock` 的意外变更；CI 会校验 lock 未被改写。

## 5. 验证方式

```powershell
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
.\tool\check_migration_boundaries.ps1
```

三者全绿 = 结构合规。新增 export 后若他包编译报「找不到类」，优先怀疑忘了在 `feature_xxx.dart` 里 export。
