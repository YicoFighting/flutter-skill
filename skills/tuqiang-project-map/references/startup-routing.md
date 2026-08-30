# 启动、Composition Root 与路由

## 1. 三端启动主链

标准端：

```text
apps/standard/lib/main.dart::main
  -> 平台 recorder/plugin 配置
  -> apps/tuqiang_app/lib/bootstrap.dart::runStandardApp
  -> _runApp
  -> prepareAppStartupData + initialI18nData
  -> getApp
  -> ProviderScope(overrides)
  -> LocationContainerHost
  -> StrongApp
```

HarmonyOS：

```text
apps/ohos/lib/main.dart::main
  -> OHOS native backend/binding 配置
  -> apps/tuqiang_app/lib/bootstrap.dart::runOhosApp
  -> _runOhosApp
  -> prepareAppStartupData + initialI18nData
  -> getApp
  -> 与共享 App 相同的根组合链
```

关键文件与 symbol：

| 文件 | Symbol | 追踪重点 |
|---|---|---|
| `apps/standard/lib/main.dart` | `main` | 标准端在进入共享 bootstrap 前做什么 |
| `apps/ohos/lib/main.dart` | `main` | OHOS 特有 backend/binding 如何注入 |
| `apps/tuqiang_app/lib/bootstrap.dart` | `runStandardApp`、`runOhosApp`、`_runApp`、`_runOhosApp` | 首帧延迟、初始化并发与异常分支 |
| 同上 | `prepareAppStartupData` | 环境、用户、配置、缓存、地图、网络等启动数据 |
| 同上 | `getApp` | composition callback、Provider override、根 Widget |
| `apps/tuqiang_app/lib/app/coordinators/location_container_host.dart` | `LocationContainerHost` | 根级 Riverpod 监听和设备/定位状态激活 |
| `apps/tuqiang_app/lib/app.dart` | `StrongApp`、`_StrongAppState` | 启动 coordinator、尺寸、MaterialApp、locale、home |

## 2. 为什么 `getApp` 不能跳过

`getApp` 不只是 `runApp` 前的样板。它通过根 `ProviderScope(overrides: ...)` 把 app 层实现注入各 feature 暴露的 contract，例如：

- feature 导航 callback；
- GPS/Camera/Pet 等跨 feature 页面 builder；
- 设备管理、分享、增值服务、Mine、MiFi 等入口；
- route observer、screen secure 或清理 callback；
- 平台插件和 AppTarget 配置。

当 feature 中只看到 `ref.read(<contractProvider>)` 或某个 Navigator/Composition 对象时，必须回到 `bootstrap.dart::getApp` 查它是否被 override，再追 override 的闭包最终打开的 route/page。仅解释 feature 文件会丢失真正的实现绑定。

实时定位：

```powershell
rg -n "ProviderScope|overrides:|overrideWith|overrideWithValue|getApp\(" apps/tuqiang_app/lib/bootstrap.dart
rg -n "Provider<.*Navigator|Provider<.*Composition|Provider<.*Callback" packages/feature packages/shared --glob '*.dart'
```

## 3. App 壳与首屏

`apps/tuqiang_app/lib/app.dart` 需要分开追：

- `_home`/相关 builder：依据本地用户、登录和首次启动状态选择启动页；
- `_StrongAppState.initState`：启动 `ApplicationStartupCoordinator` 等生命周期编排；
- `build`：初始化 `TQSizeFit`，创建 `MaterialApp`；
- `routes`：来自 `AppRouters.getRouters`；
- `onGenerateRoute`：处理未在静态 map 中命中的路由；
- locale/supportedLocales：连接 `TQI18nManager` 与 manifest 数据；
- builder：固定 text scaler，并叠加 EasyLoading 等 App 级 UI。

解释“进入某页”时还要检查该页是首屏、静态 named route、`onGenerateRoute`、native route，还是 composition builder 直接创建。

## 4. 路由聚合

### AppRouters

文件：`apps/tuqiang_app/lib/app/router/app_router.dart`

重点 symbol：

- `AppRouters`：app route 常量和兼容 alias；
- `getRouters`：静态 route map 聚合；
- `onGenerateRoute`：动态参数/兼容分支；
- 具体 route builder：确认构造参数、ProviderContainer 读取和最终页面。

### FeatureRouterRegistry

文件：`apps/tuqiang_app/lib/app/router/feature_router_registry.dart`

重点 symbol：

- `FeatureRouterRegistry`；
- feature checked route registries；
- native routes；
- screen-secure/route effects；
- registry 合并和冲突检查。

feature 自己的 route owner 通常位于：

```text
packages/feature/<feature>/lib/**/router*.dart
packages/feature/<feature>/lib/**/routes*.dart
packages/feature/<feature>/lib/<feature>.dart   # barrel
```

不要只搜路由字符串。还要搜：路由常量名、目标 Page 类、`Navigator.push*`、feature Navigator contract，以及 `bootstrap.dart` 中注入的 callback。

## 5. 一次路由追踪模板

```text
用户动作 / 外部事件
  -> Widget callback 或 native/scheme/push handler
  -> Navigator / feature navigator contract
  -> app composition override（若有）
  -> AppRouters / FeatureRouterRegistry / onGenerateRoute
  -> route builder 与参数解析
  -> 目标 Page 构造
  -> Page 首次 build/initState/useEffect
  -> Provider/Controller 请求与 UI
```

必须回答：

1. 路由名由谁拥有，谁只是兼容 alias？
2. 参数从哪里产生，传递途中有没有转换、fallback 或从 ProviderContainer 补值？
3. 是 push、replacement、popUntil 还是嵌入式 builder？
4. route effect、screen secure、observer 是否参与？
5. 目标页何时发起第一笔数据请求？

## 6. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "runStandardApp|runOhosApp|_runApp|_runOhosApp|prepareAppStartupData|initialI18nData|getApp" apps --glob '*.dart'
rg -n "ProviderScope|LocationContainerHost|StrongApp|MaterialApp|onGenerateRoute|getRouters" apps/tuqiang_app/lib --glob '*.dart'
rg -n "<路由常量>|<路由字符串>|class <目标页面>" apps packages --glob '*.dart'
rg -n "Navigator\.(of\([^)]*\)\.)?(push|pushNamed|pop)|open[A-Z]|PageBuilder" <相关目录> --glob '*.dart'
```

输出时将占位符替换为实际 symbol，并引用本次命中的当前行号。
