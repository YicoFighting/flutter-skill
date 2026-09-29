# Tuqiang 启动、Composition Root 与路由

## 启动主链

标准端与 HarmonyOS 先进入各自 runner，再完成首屏前准备；APM runner 可能因环境不同，不把单一分支的文字顺序泛化。

    apps/standard/lib/main.dart::main
    → runStandardApp → bootstrap::_runApp

    apps/ohos/lib/main.dart::main
    → runOhosApp(callback) → bootstrap::_runApp → _runOhosApp
    → _prepareOhosFlutterStartup → _initializeOhosPlatformBindings
    → callback 配置 recorder/auth/map/vsdk binding

    两端 → AppStartupDataCoordinator.prepareBeforeRunApp
      非生产：runApp(getApp()) → scheduleAfterFirstFrame
      生产 APM：scheduleAfterFirstFrame → appRunner 返回 getApp(...)

`scheduleAfterFirstFrame` 只是注册首帧后任务，不证明 Widget 树按源码文字顺序完成。根组合固定为：

    getApp → ProviderScope(overrides) → LocationContainerHost → StrongApp

| 文件 | 关键 symbol | 追踪重点 |
|---|---|---|
| `apps/tuqiang_app/lib/app/coordinators/app_startup_data_coordinator.dart` | `prepareBeforeRunApp`、`scheduleAfterFirstFrame`、`_initializeI18n` | 环境、用户、i18n、HTTP、缓存与首帧边界 |
| `apps/tuqiang_app/lib/bootstrap.dart` | `runStandardApp`、`runOhosApp`、`getApp` | 平台分支、root overrides、runtime/callback |
| `apps/tuqiang_app/lib/app/coordinators/location_container_host.dart` | `LocationContainerHost` | 根 Riverpod 监听与设备外部上下文激活 |
| `apps/tuqiang_app/lib/app.dart` | `StrongApp`、`getHomePage` | 首屏、生命周期、尺寸、locale 与 MaterialApp |

启动/恢复用户后把 `accountMode` 追到首笔请求；判定链见 [账号模式](account-mode.md)。

## Composition root

`bootstrap.dart::getApp` 注入：

- feature 导航/composition builder/app callback，以及 route observer、screen secure、平台插件和 AppTarget；
- `shared_device` repository/runtime 与定位/消息外部上下文；`shared_location` repository/runtime 与 app-local Manager 副作用；
- `shared_message` repository、`shared_media` session、`shared_advertising` repository/login state，以及账号模式 callback、请求 path/cache scope。

feature/shared 只看到 contract provider 或 callback 时，回到 `getApp` 查 override，再追闭包最终调用的 Page、Manager、Repository 或 plugin。

## App 壳与路由

`apps/tuqiang_app/lib/app.dart::StrongApp` 分开追：

- `getHomePage` 根据 `AppRuntimeState` 等当前状态选择入口；
- `initState` 启动 `ApplicationStartupCoordinator`；
- `build` 按当前 route 与 pane 宽度更新 `TQSizeFit` 并创建 `MaterialApp`；
- 当前只配置 `onGenerateRoute: AppRouters.generateRoute`，不能把仍存在的 `getRouters()` 当成 `MaterialApp.routes` 的实际接入；
- locale 来自 `TQI18nManager.curLang`，`supportedLocales` 当前显式列 zh/en；它不是 manifest 的全部资源列表。builder 叠加 App 级 UI。

`AppRouters` 负责 app route/兼容 alias、静态 map、checked feature routes 与动态参数；`FeatureRouterRegistry` 负责 native routes、screen secure、route effects 和刷新分类，不能合并归属。

## 分栏与方向

2026-09-29 核验的检索入口：

- `AppRouters._paneRoutes/generateRoute`：可分栏页面使用 `CoreAdaptivePageRoute`；摄像头、视频及其余页面保留 `MaterialPageRoute`，scheme 入口可显式 `allowPane: false`。
- `core_ui/lib/adaptive_layout.dart`：`CoreAdaptiveMaster` 注册主页面，`CoreAdaptivePageRoute` 连接详情路由，`CorePaneViewport` 给子树提供 pane 尺寸；页面布局另有 `CoreAdaptiveSections`。
- `HomePage` 使用 `CoreAdaptiveMaster`；设备选择等入口可调用 `closeDetails`。保留 master 的分栏路由与整页覆盖的可见性不同，涉及返回刷新时检查实际 observer/listener。
- `StrongApp._topPageUsesPane/_updateSizeFit` 按路由和屏幕决定缩放宽度；standard 的 `AppOrientationObserver` 管理普通页面方向，特殊页面可保留自身策略。

只定位路由时给出当前 builder、参数和 route 类型即可；生命周期、权限或首笔请求影响问题时再追。完整方法见 [端到端调查](requirement-trace-playbook.md)，现有封装用法见 [本地封装与复用](../../tuqiang-dev/references/local-style-and-reuse.md)。
