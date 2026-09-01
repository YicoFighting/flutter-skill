# 启动、Composition Root 与路由

本页同时索引两条产品线，但一次追踪必须先选择 Tuqiang 或 Laoying。两者只有平台宿主的形态相似，根状态和路由不是同一套。

## 1. Tuqiang 启动主链

标准端与 HarmonyOS 都先进入各自 runner，再完成首屏前准备。runner 的调用形态因平台和环境而异：非生产分支直接 `runApp(getApp())`，生产分支把 `getApp(...)` 返回给 APM runner。不要把某一分支的调用顺序泛化为全部环境。

```text
apps/standard/lib/main.dart::main
  -> runStandardApp
  -> bootstrap::_runApp
  -> AppStartupDataCoordinator.prepareBeforeRunApp
  -> 非生产：runApp(getApp())
     或生产：APM appRunner 返回 getApp(...)
  -> AppStartupDataCoordinator.scheduleAfterFirstFrame（注册首帧后任务）
```

HarmonyOS：

```text
apps/ohos/lib/main.dart::main
  -> OHOS recorder/auth/map/vsdk binding 配置
  -> runOhosApp
  -> bootstrap::_runOhosApp
  -> 与标准端相同的 startup coordinator 与 getApp；生产/非生产同样由不同 runner 挂载
```

`scheduleAfterFirstFrame` 的调用点在非生产分支位于 `runApp` 之后，在生产 APM 分支位于 `return getApp(...)` 之前；它的语义是注册首帧后任务，不表示 Widget 树已经按文字顺序构建。根 Widget 组成应单独写为：

```text
getApp(...)
  -> ProviderScope(overrides)
  -> LocationContainerHost
  -> StrongApp
```

首屏前数据入口仍应实时追 `AppStartupDataCoordinator.prepareBeforeRunApp`，而不是已删除的旧 helper。

| 文件 | 关键 symbol | 追踪重点 |
|---|---|---|
| `apps/tuqiang_app/lib/app/coordinators/app_startup_data_coordinator.dart` | `prepareBeforeRunApp`、`scheduleAfterFirstFrame`、`_initializeI18n` | 环境、用户、i18n、HTTP、缓存任务；首帧前/后边界 |
| `apps/tuqiang_app/lib/bootstrap.dart` | `runStandardApp`、`runOhosApp`、`getApp` | 平台分支、根 overrides、runtime/callback |
| `apps/tuqiang_app/lib/app/coordinators/location_container_host.dart` | `LocationContainerHost` | 根 Riverpod 监听和设备外部上下文激活 |
| `apps/tuqiang_app/lib/app.dart` | `StrongApp`、`getHomePage` | 首屏、`ApplicationStartupCoordinator`、尺寸、locale、MaterialApp |

## 2. Tuqiang composition root

`bootstrap.dart::getApp` 不是样板。根 `ProviderScope(overrides: ...)` 当前会注入：

- 各 feature 的导航、composition builder 与 app callback；
- `shared_device` 的 repository/runtime，外部上下文由 app 连接定位与消息；
- `shared_location` 的 repository/runtime，坐标副作用在 app 层连接旧 Manager；
- `shared_message` repository、`shared_media` session、`shared_advertising` repository/login state；
- route observer、screen secure、平台插件和 AppTarget 配置。

feature/shared 中只看到 contract provider 或 runtime callback 时，必须回到 `getApp` 查 override，再追闭包的最终 page、manager、repository 或 plugin。

```powershell
rg -n "ProviderScope|overrides:|overrideWith|overrideWithValue|deviceCoreRuntimeProvider|locationRuntimeProvider|getApp\(" apps/tuqiang_app/lib/bootstrap.dart
rg -n "Provider<.*Navigator|Provider<.*Composition|Provider<.*Runtime|Provider<.*Callback" packages/feature packages/shared --glob '*.dart'
```

## 3. Tuqiang App 壳与路由

`apps/tuqiang_app/lib/app.dart::StrongApp` 需要分开追：

- `getHomePage` 根据 `AppRuntimeState` 等当前状态选择入口；
- `initState` 启动 `ApplicationStartupCoordinator`；
- `build` 初始化尺寸并创建 `MaterialApp`；
- `routes: AppRouters.getRouters()`；
- `onGenerateRoute: AppRouters.generateRoute`；
- locale/supportedLocales 连接 i18n manifest；
- builder 固定 text scaler 并叠加 App 级 UI。

`apps/tuqiang_app/lib/app/router/app_router.dart::AppRouters` 负责 app route/兼容 alias、静态 route map、checked 合并 feature routes 与动态参数。`FeatureRouterRegistry` 当前负责：

- `nativeRouters()`；
- `screenSecureRoutes`；
- `routeEffects()`；
- 定位/相机刷新与路由退出分类。

不要再把 feature Dart route map 合并归给 `FeatureRouterRegistry`。具体 route owner 仍要追 feature router、Page builder 和 `getApp` callback。

## 4. Laoying 启动主链

标准端：

```text
apps/laoying_standard/lib/main.dart::main
  -> runLaoyingStandardApp(platform adapters)
  -> apps/laoying_app/lib/bootstrap.dart::_runLaoyingApp
  -> WidgetsFlutterBinding.ensureInitialized
  -> LYI18nInitializer.initialize
  -> _createSkinController
  -> LYAppProvider
  -> backend/repository/controller 组合
  -> runApp(LYApp(...))
```

OHOS 从 `apps/laoying_ohos/lib/main.dart::main` 调用 `runLaoyingOhosApp`，注入 OHOS 地图/平台能力，再进入相同 `_runLaoyingApp`。回答平台差异时必须对比两个宿主传入的 adapter，不能只看共享 App。

`apps/laoying_app/lib/app.dart::LYApp` 在 build 中通过 `LYAppScope` 暴露 `LYAppProvider`，创建 `MaterialApp`，并把未命中路由交给 `LYAppRouter.onGenerateRoute`。

## 5. Laoying 状态与路由

- `apps/laoying_app/lib/app/session/ly_app_provider.dart::LYAppProvider extends ChangeNotifier` 是根 session 协调对象；查 `resetSession`、reset coordinator、refresh bus 与每个 `notifyListeners` 的条件。
- `apps/laoying_app/lib/app/router/ly_route_registry.dart::LYAppRouteRegistry` checked 合并 app shell、auth、gps、pet、mine、overview、message、device share、device management routers，并检查重复 route/owner。
- `apps/laoying_app/lib/app/router/ly_app_router.dart::LYAppRouter.onGenerateRoute` 解析 route 与 arguments 并构建最终页面。
- 目标业务 owner 位于 `apps/laoying_app/lib/app/<domain>`；继续追 `ly_*_router.dart`、controller、repository、Page 与 asset 常量。

不要在 Laoying 链路中虚构 `ProviderScope` 或 Tuqiang feature router。若一个公共 core/plugin 同时被两产品使用，分别找各自的 composition 接入。

## 6. 路由追踪模板

```text
用户动作 / 外部事件
  -> 产品内 Widget callback、scheme/push/native handler
  -> 产品路由 contract/Navigator
  -> composition 绑定（若有）
  -> AppRouters + feature router（Tuqiang）
     或 LYAppRouter + LYAppRouteRegistry + app-local router（Laoying）
  -> arguments 转换与最终 Page
  -> initState/build/controller
  -> 状态/Repository/插件
```

必须回答 route owner、参数来源与 fallback、导航类型、observer/effect/security、目标页首笔数据触发点。若 route 字符串在两产品都出现，按入口和最终 builder 分别核验。

## 7. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "runStandardApp|runOhosApp|AppStartupDataCoordinator|prepareBeforeRunApp|scheduleAfterFirstFrame|getApp" apps/standard apps/ohos apps/tuqiang_app --glob '*.dart'
rg -n "ProviderScope|LocationContainerHost|StrongApp|MaterialApp|AppRouters\.getRouters|AppRouters\.generateRoute" apps/tuqiang_app/lib --glob '*.dart'
rg -n "runLaoyingStandardApp|runLaoyingOhosApp|_runLaoyingApp|LYI18nInitializer|LYAppProvider|class LYApp" apps/laoying_* --glob '*.dart'
rg -n "class LYAppRouter|class LYAppRouteRegistry|onGenerateRoute|LYBusinessRouter" apps/laoying_app/lib/app --glob '*.dart'
rg -n "<路由常量>|<路由字符串>|class <目标页面>" <已确认产品目录> --glob '*.dart'
```
