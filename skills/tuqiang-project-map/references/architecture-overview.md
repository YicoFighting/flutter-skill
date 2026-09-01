# 架构总览

## 1. 先选择产品线

当前 monorepo 同时承载 Tuqiang 与 Laoying。两者共享部分 core/plugin 与仓库工具，但 App、状态与路由组合不同：

```text
Tuqiang
apps/standard ─┐
               ├─> apps/tuqiang_app ─> feature_* ─┐
apps/ohos ─────┘                    └> shared_* ──> core_* / plugins / adapter / assets_common

Laoying
apps/laoying_standard ─┐
                       ├─> apps/laoying_app ─> app-local auth/gps/pet/mine/... ─> core_* / tq_map_plugin
apps/laoying_ohos ─────┘
```

图表示组合与依赖方向，不是运行时调用顺序。具体问题仍要读取目标 `pubspec.yaml`、import 与调用方。

| 识别结果 | 应使用的根事实 | 不得默认套用 |
|---|---|---|
| Tuqiang | `StrongApp`、根 `ProviderScope`、`AppRouters`、`FeatureRouterRegistry`、`feature_*` 与 8 个 `shared_*` | Laoying 的 `LYAppProvider`、LY 路由与 app-local owner |
| Laoying | `LYApp`、`LYAppProvider`、`LYAppRouter`、`LYAppRouteRegistry`、`apps/laoying_app/lib/app/<domain>` | Tuqiang 的 Riverpod family、AppRouters、feature package owner |
| Cross-product | 分别追两条链，再在 core/plugin/adapter 交点比较 | 用一条产品链替代另一条 |

锚点不足且产品选择会改变结论时，必须先问用户。

## 2. Tuqiang 分层

| 层 | 当前职责 | 关键入口 |
|---|---|---|
| 宿主 | 标准端与 OHOS 平台初始化 | `apps/standard/lib/main.dart::main`、`apps/ohos/lib/main.dart::main` |
| 启动协调 | 首屏前环境/用户/i18n/HTTP/缓存任务与首帧后任务 | `apps/tuqiang_app/lib/app/coordinators/app_startup_data_coordinator.dart::AppStartupDataCoordinator` |
| Composition root | 根 `ProviderScope` overrides、跨 feature/runtime callback、平台能力注入 | `apps/tuqiang_app/lib/bootstrap.dart::getApp` |
| App 壳 | 首屏、生命周期、尺寸、locale、`MaterialApp` | `apps/tuqiang_app/lib/app.dart::StrongApp` |
| Dart 路由 | app alias、自有页面、checked 合并 feature routes、动态参数 | `apps/tuqiang_app/lib/app/router/app_router.dart::AppRouters` |
| 路由元数据 | native routes、screen secure、route effects、刷新分类 | `apps/tuqiang_app/lib/app/router/feature_router_registry.dart::FeatureRouterRegistry` |
| 业务 owner | 独立用户流程与跨 feature 领域状态 | `packages/feature/*`、`packages/shared/shared_*` |
| App 遗留边界 | 尚未下沉或产品专属的历史 manager/model/viewmodel/tools | `apps/tuqiang_app/lib/app/legacy_shared` |

Tuqiang 当前 8 个正式 shared 领域包是 `shared_account`、`shared_activity`、`shared_advertising`、`shared_command`、`shared_device`、`shared_location`、`shared_media`、`shared_message`。`shared_business` 已从 tracked package 拆除，不应出现在当前 owner 或根校验结论中。

## 3. Laoying 分层

| 层 | 当前职责 | 关键入口 |
|---|---|---|
| 宿主 | 标准端/OHOS 平台 adapter 与运行入口 | `apps/laoying_standard/lib/main.dart`、`apps/laoying_ohos/lib/main.dart` |
| Bootstrap | i18n、skin、平台能力、repository/controller 组合与 App provider 创建 | `apps/laoying_app/lib/bootstrap.dart` |
| App 壳 | `LYAppScope`、`MaterialApp`、locale/theme/route | `apps/laoying_app/lib/app.dart::LYApp` |
| 根状态 | session、reset participant、refresh bus 与 `notifyListeners` | `apps/laoying_app/lib/app/session/ly_app_provider.dart::LYAppProvider` |
| 路由 | 解析 route/arguments 与 checked 合并 app-local business routers | `ly_app_router.dart::LYAppRouter`、`ly_route_registry.dart::LYAppRouteRegistry` |
| 业务 owner | auth、gps、pet、mine、overview、message、device_share、device_management 等 app-local 目录 | `apps/laoying_app/lib/app/<domain>` |
| 资源 | 产品级 i18n/images 与各领域 asset 常量 | `apps/laoying_app/assets`、`apps/laoying_app/lib/app/**/ly_*_assets.dart` |

Laoying 当前不是 Tuqiang feature/shared 拆包的镜像。看到相同业务名也要追 Laoying 自己的 router/controller/repository，而不是跳到 `packages/feature`。

## 4. 组合与依赖的关键事实

- Tuqiang 的 `bootstrap.dart::getApp` 是跨包依赖注入证据；feature 只调用 contract 时，要追根 `ProviderScope` override 或 runtime callback 到最终实现。
- `AppRouters.getRouters` 负责 Tuqiang Dart route map 与 checked feature route 合并；`FeatureRouterRegistry` 不再承担 Dart map 合并，它负责 native route 与 route effect/security/refresh 元数据。
- 设备与定位跨 shared 包不应相互反向 import。`shared_device::DeviceCoreRuntime` 暴露外部上下文 callback，由 app composition 注入定位/消息失效和请求。
- `core_ui` 除 UI 组件外还导出 navigation contracts、checked registry、route effect 与 `SessionResetParticipant`；owner 判断要读取其 barrel，不可仅凭包名断言“纯 Widget”。
- `core_color` 提供中性色彩原语，`core_log` 提供统一日志能力；core 不应依赖 shared/feature/app。
- Laoying 的业务 owner 当前主要在 `apps/laoying_app/lib/app`。是否下沉为公共包属于设计决策，项目地图只能报告现状和依赖证据。

## 5. 状态体系不是一套

Tuqiang：

```text
Widget setState / Controller
        ├─ Riverpod Provider / Notifier / family cache
        │       └─ Repository ─> TQHttp / plugin
        ├─ Manager / singleton
        └─ SharedPreferences / 文件 / 数据库
```

Laoying：

```text
LYAppProvider(ChangeNotifier) / LYAppScope
        ├─ app-local controller + repository
        ├─ session reset participants + refresh bus
        └─ infrastructure adapter / preferences / HTTP / plugin
```

具体页面仍可能有 `StatefulWidget`、controller 或其他监听机制。只描述本次源码实际经过的状态，不把产品级模式扩张为“全部状态”。

## 6. 当前事实与迁移资料

优先核验：`AGENTS.md`、当前源码、各 `pubspec.yaml`/lockfile、`tool/project.dart`、`tool/check_dependency_architecture.ps1`、`tool/check_migration_boundaries.ps1`、相关测试。

用于理解迁移背景但不能替代源码：

- `docs/shared_business_domain_split_migration_plan.md`
- `docs/feature_business_package_split_plan.md`
- `docs/laoying_app_implementation_plan.md`
- `docs/三端分支统一合并实施方案.md`
- `docs/ohos_migration_inventory.md`

大型迁移文档可能同时保留历史基线与最新验收段落；必须依据段落状态与当前源码交叉核验。

## 7. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "enum AppTarget|laoyingStandard|laoyingOhos" tool/project.dart
rg -n "runStandardApp|runOhosApp|AppStartupDataCoordinator|ProviderScope|class StrongApp" apps/standard apps/ohos apps/tuqiang_app --glob '*.dart'
rg -n "runLaoyingStandardApp|runLaoyingOhosApp|class LYApp|class LYAppProvider|class LYAppRouter|class LYAppRouteRegistry" apps/laoying_* --glob '*.dart'
rg -n "class AppRouters|class FeatureRouterRegistry|nativeRouters|routeEffects|generateRoute" apps/tuqiang_app packages/feature --glob '*.dart'
rg -n "package:feature_|package:shared_|package:core_" <已确认的产品目录> --glob '*.dart'
```

每次只报告本次命中；不要把 reference 中的路径当作无需验证的永久事实。
