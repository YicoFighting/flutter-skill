# 双产品上下文：先判产品，再追链路

> 本文件提供当前源码的检索入口，不保存静态行号。每次回答都要在已验证的 `<TUQIANG_ROOT>` 中重新读取目标符号、依赖与测试；仓库现状高于这里的路径索引。

## 1. 产品与 target

先从用户指定 target、目标路径、路由入口或调用方确认产品线：

| 产品线 | 业务 owner | 可执行 shell / target |
|---|---|---|
| Tuqiang | `apps/tuqiang_app` | `apps/standard` / `standard`；`apps/ohos` / `ohos` |
| Laoying | `apps/laoying_app` | `apps/laoying_standard` / `laoying_standard`；`apps/laoying_ohos` / `laoying_ohos` |

`tool/project.dart` 是当前四个 target 的命令事实入口。目标在 `packages/core`、`packages/shared`、`packages/plugins` 等公共目录时，产品线不是由目录名决定的：反查 app/shell 调用方、依赖和 composition root；若两条产品线都消费，分别说明两条接线与平台差异。

## 2. 运行时架构分流

| 关注点 | Tuqiang | Laoying |
|---|---|---|
| 状态入口 | Riverpod Provider/Notifier/family，并混用 Manager、cache、app legacy Model | `LYAppScope extends InheritedNotifier<LYAppProvider>`；`LYAppProvider`、`LYUserSession` 与各 owner Controller 主要是 `ChangeNotifier` |
| UI 订阅 | `ref.watch/select/listen/read`，也可能是 Manager getter、`setState`、`ValueNotifier` | `LYAppScope.of(context)`、`ListenableBuilder` / `AnimatedBuilder`、手动 `addListener` 与局部 `setState` |
| 组合根 | `apps/tuqiang_app/lib/bootstrap.dart` 中 Provider override、Repository override、`*Runtime.configure` / `*ApiPaths.configure` | `apps/laoying_app/lib/bootstrap.dart` 构造 `LYAppProvider`、backend client，并把具体 Repository/adapter 传给 `LYApp` / router / page |
| 网络 | `core_http` / `TQHttp`、`ResultModel`、`TCheck<T>` 与 feature/shared Repository | `LYBackendHttpClient`、`LYHttp*Repository` 和 owner 自己的结果/Model；不能套用 TQHttp 响应模板 |
| 路由 | `MaterialApp.routes` + `onGenerateRoute`，`AppRouters` 与 feature router registry | `LYAppRouter.onGenerateRoute`、`LYAppRouteRegistry`、`LYAuthRouter` 与 `ly_route_contract.dart` |

关键源码入口：

- Tuqiang：`apps/tuqiang_app/lib/app.dart`、`apps/tuqiang_app/lib/bootstrap.dart`、`apps/tuqiang_app/lib/app/router/feature_router_registry.dart`；
- Laoying 状态：`apps/laoying_app/lib/app/session/ly_app_scope.dart`、`apps/laoying_app/lib/app/session/ly_app_provider.dart`，再到各 owner 的 `providers/*controller.dart`；
- Laoying 网络：`apps/laoying_app/lib/app/infrastructure/backend/ly_backend_http_client.dart` 与 `apps/laoying_app/lib/bootstrap.dart`；
- Laoying 路由：`apps/laoying_app/lib/app/router/ly_app_router.dart`、`ly_route_registry.dart`、`apps/laoying_app/lib/app/contracts/ly_route_contract.dart`。

不要因为仓库里能搜索到 Riverpod、TQHttp 或 `AppRouters`，就认定 Laoying 业务链也经过它们；同理，不要把 Laoying 的 app-local Controller 架构泛化给 Tuqiang feature/shared package。

## 3. Laoying 资源与 i18n

Laoying 资源由 `laoying_app` package 自己拥有：

- `apps/laoying_app/lib/app/assets/ly_app_assets.dart` 定义 `LYAssetOwner`、package name 和 owner 目录；
- `apps/laoying_app/pubspec.yaml` 注册 `assets/images/<owner>/` 与 `assets/i18n/`；
- `Image.asset` 的真实调用需核验 `package: LYAppAssets.packageName`，不能默认引用 `assets_common` 或 Tuqiang feature 资源；
- `apps/laoying_app/assets/i18n/manifest.json` 是语言集合与 fallback 的事实入口；当前 manifest 为 `zh_CN`、`en_US`，fallback 为 `en_US`；
- `apps/laoying_app/lib/app/i18n/ly_i18n_initializer.dart` 把 Laoying 翻译安装到 `core_i18n`，不能把 Tuqiang 的资源加载流程当作它的启动链。

解释图片时追完整血缘：资源常量 → `pubspec.yaml` 注册 → package 作用域 → Widget 或原生插件加载。PNG/SVG 等视觉内容本身只能证明文件存在和被使用；没有需求、验收或视觉确认时，不从像素反推产品意图。

## 4. Laoying 测试与验证事实

优先从相关测试反查它们保护的真实边界：

- `apps/laoying_app/test/app/architecture/dependency_boundary_test.dart`：业务 owner 与 app 层不得直接交叉 import；
- `apps/laoying_app/test/app/i18n/ly_i18n_loader_test.dart`：Laoying 翻译通过 `core_i18n` 生效，并与 Tuqiang 资源隔离；
- `apps/laoying_app/test/app/phase5/ly_asset_independence_test.dart`：资源文件、`3.0x` 变体、package AssetBundle 与资源独立性；
- 目标功能目录下的 controller/repository/page 测试：用于证明具体状态、网络和 UI 行为。

`dart run tool/project.dart analyze|test <target>` 只在对应 shell 目录运行 Flutter 命令；它不能自动证明 `apps/laoying_app/test` 全部通过。复盘或讲解验证时记录实际工作目录、命令与覆盖范围，不把 Tuqiang migration test、shell analyze 或“存在测试文件”写成 Laoying app 测试已通过。

## 5. 产品歧义处理

- 路径已经位于某个 app owner 或 shell，且调用链不跨产品：直接判定，不询问可发现事实。
- 公共 package 被两条产品线消费：分别追调用方；用户只问其中一条时裁剪到该产品。
- 用户说“首页”“登录”“GPS 页面”等两条产品线都有的概念，且未给 target/路径：若答案会不同，先问“Tuqiang 还是 Laoying（以及哪个 target）？”。
- 产品可判定，但操作起点、目标页面或希望追到的边界仍有多解：只问会改变结果的最小问题，不自行选择。
