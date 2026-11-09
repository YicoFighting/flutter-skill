# Tuqiang 启动、Composition Root 与路由

## 启动主链

```text
apps/standard/lib/main.dart::main → runStandardApp → bootstrap::_runApp
apps/ohos/lib/main.dart::main → runOhosApp(callback) → _runApp → _runOhosApp
  → _prepareOhosFlutterStartup → _initializeOhosPlatformBindings
  → callback 配置 recorder/auth/map(configureOhosMapPlatformView)/vsdk binding

两端 → AppStartupDataCoordinator.prepareBeforeRunApp
  非 APM：runApp(getApp()) → scheduleAfterFirstFrame
  APM：UmengApmSdk.init(appRunner: … scheduleAfterFirstFrame … getApp)
根组合：getApp → ProviderScope(overrides) → LocationContainerHost → StrongApp
```

`scheduleAfterFirstFrame` 只注册首帧后任务，不证明 Widget 树按源码文字顺序完成；APM 分支两端略有差异，不把单一分支泛化。

| 文件 | 关键 symbol | 追踪重点 |
|---|---|---|
| `app/coordinators/app_startup_data_coordinator.dart` | `prepareBeforeRunApp`、`scheduleAfterFirstFrame`、`_initializeI18n` | 环境、用户、i18n、HTTP、缓存与首帧边界 |
| `bootstrap.dart` | `runStandardApp`、`runOhosApp`、`getApp` | 平台分支、root overrides、runtime/callback |
| `app/coordinators/location_container_host.dart` | `LocationContainerHost` | 根 Riverpod 监听与设备外部上下文激活 |
| `app.dart` | `StrongApp`、`getHomePage` | 首屏、生命周期、尺寸、locale |

启动/恢复用户后把 accountMode 追到首笔请求，见 [账号模式](account-mode.md)。

## Composition root

`getApp` 注入 feature 导航/composition builder/app callback、route observer、screen secure、平台插件与 AppTarget；`shared_device`/`shared_location` 的 repository、runtime 与外部上下文；`shared_message` repository、`shared_media` session、`shared_advertising` repository/登录态，以及账号模式 callback、请求 path/cache scope。feature/shared 只看到 contract 或 callback 时，回到 `getApp` 查 override，再追闭包最终调用的 Page、Manager、Repository 或 plugin。

## App 壳与路由

- `StrongApp.getHomePage` 按 `AppRuntimeState` 等状态选首屏；`initState` 启动 `ApplicationStartupCoordinator`。
- `build` 由 `_topPageUsesPane/_updateSizeFit` 按路由与 `CoreAdaptiveLayout.canSplit` 更新 `TQSizeFit`，再创建 `MaterialApp`。
- 只配置 `onGenerateRoute: AppRouters.generateRoute`；仍存在的 `getRouters()` 返回副本，不是 `MaterialApp.routes` 的实际接入。
- locale 来自 `TQI18nManager.curLang`；`supportedLocales` 只列 zh/en，不等于 manifest 资源列表。
- `AppRouters` 负责 app route、兼容 alias、checked feature routes 与动态参数；`FeatureRouterRegistry` 负责 native routes、screen secure、route effects 与刷新分类，二者不合并归属。

## 分栏与方向

- `AppRouters._paneRoutes/generateRoute`：白名单页面用 `CoreAdaptivePageRoute`，摄像头/视频等用 `MaterialPageRoute`；scheme 入口可显式 `allowPane: false`。
- `core_ui/lib/adaptive_layout.dart`：`CoreAdaptiveMaster` 注册主页面，`CoreAdaptivePageRoute` 连接详情，`CorePaneViewport` 提供 pane 内 `MediaQuery`，`CoreAdaptiveSections` 做页内分区重排。
- `HomePage` 使用 `CoreAdaptiveMaster`，设备选择等入口可 `closeDetails`。保留 master 的分栏与整页覆盖可见性不同，返回刷新要查实际 observer/listener。
- standard 的 `AppOrientationObserver` 管普通页面方向，特殊页面（如横屏播放）保留自身策略。

只定位路由时给出 builder、参数和 route 类型即可；生命周期、权限或首笔请求影响结论时再追。
