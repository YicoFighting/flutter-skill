# Tuqiang 平台、地图、设备页面与构建变体

记录候选变体事实，不生成机械笛卡尔积。维度分开：`platform / target / mapBackend / device leaf / flavor / distributionChannel / accountMode`。账号由 [isEnterprise](account-mode.md) 决定，flavor 与渠道都不能推断账号。开发侧逐行交付见 [实施覆盖](../../tuqiang-dev/references/coverage.md)。

## 平台宿主

`standard → Android/iOS`，`ohos → HarmonyOS`。一次 standard analyze/build 不能证明 Android 与 iOS 运行一致；命中 channel、PlatformView、权限、资源或原生 SDK 时追各平台目录。OHOS 判断用 bootstrap 配置的 `AppTargetConfig.isOhos`（不存在 `Platform.isOhos`）。

## 地图实现面

公共选择层 `packages/plugins/tq_map_plugin`：

- `map_source/tq_map_enum.dart`：`TQMapSourceType` = baidu/google/gaode；`TQMapUseSceneType` = location、lineTrace、smartTrace、pointTrace、overview、follow、fence、report、addDevice、markers。
- `TQBaseMapWidgetState.buildMapView` 分派 Dart 分支；`TQMapViewFactoryId.resolve(mapType, scene)` 给百度/高德 PlatformView ID，Google 走 `google_maps_flutter`，不用 factory id。
- Android/iOS 的百度、高德是各自原生 PlatformView。
- **HarmonyOS（Tuqiang 宿主）统一走百度 ArkTS**：`apps/ohos/lib/map_ohos_view_host.dart` 把 bMap/aMap 两组 ID 都解析为 `TQBMap*ViewFactory`，经 `PreparedBaiduMaps` 预建底图；`configureOhosMapPlatformView` 注入 `ohosBaiduView`。插件中仍注册的华为 Map Kit（花瓣）factory 只由 `apps/laoying_ohos` 使用，不在 Tuqiang 范围。设置页"地图偏好"只对个人账号且非 OHOS 显示；OHOS 的 POI 搜索 PlatformView 返回空 Widget。
- 鸿蒙百度专属 Dart 逻辑只能以 `TQMapViewHost.usesOhosBaiduMap(mapType, scene)` 为启用条件；不能用 `Platform.operatingSystem`、`TQMapViewHost.isConfigured`、`usesWgs84Coordinates` 或界面选择的"百度"推断。完整约束见业务仓库 `docs/ohos_baidu_map_integration_spec.md`。

```text
Page/Widget → TQMapUseSceneType + options
→ MapSourceManager / TQMapSourceType → TQBaseMapWidgetState
→ factory id（OHOS 再经 resolveOhosMapViewType）→ native adapter / Google controller
→ 坐标、marker/polyline、回调、生命周期与资源
```

主地图候选共 7 行：Android/iOS × 百度/高德/Google，加 HarmonyOS 百度 ArkTS。POI、街景、外部导航等独立 channel 不由主地图行自动覆盖。

## 设备列表 → 页面族

`DeviceListPage._selectDevice` 在写入共同选择后当前分流（使用前重查）：

| 条件 | 去向 |
|---|---|
| 强制升级 / 服务过期（`deviceStatus == -1`） | 更新提示或续费页，不进详情 |
| GPS + D38Max 狗（`TQSceneEnum.isD38MaxDog`） | `petModuleList` |
| GPS + 基础服务 / 新手状态 | `baseDeviceLocation` / `noviceDeviceLocation` |
| GPS + scene category normal/person/keys/pet/tag | `gps/person/scene/pet/tagModuleList` |
| LBS | `beaconsModuleList` |
| Camera：`isJankCameraRouteDevice` | `jankHomePage` |
| Camera driving：停车监控 / 高帧（移动）/ 其他 | `parking/moving/drivingModuleList` |
| Camera monitor | `monitorModuleList` |
| Tag | `tagLocation` |
| 其他 | `wifiModuleList` |

从问题可达的 route 追到最终 Page 与真实点击区域；只有需求涉及"更多详情/设备详情/更多设置"或公共入口时才追其他调用者。多个叶子本身不触发提问，先由用户给定页面、设备和源码收窄。

## Android 构建变体

仅在构建、CI、推送、广告、原生地图依赖、ABI 或"不同安装包表现不同"时读取。

| flavor | 实际依赖 | 需核验 |
|---|---|---|
| `allvendor`（工具默认） | `jpush_push` + 极光厂商插件、`ad_sdk`、高德 Maven 依赖 | 默认内部包不代表其他包 |
| `combined` | 五家厂商 push module、Walle、`ad_sdk`、高德 Maven 依赖 | 母包写入渠道后运行时选厂商，不能只验未写渠道母包 |
| `firebase` | `firebase_push`、`ad_sdk_noop`、Google Play 高德本地依赖、arm64-v8a | 广告空实现、推送、Manifest、ABI |

- `apps/standard/android/app/build.gradle`：以实际 `*Implementation` 块为准（`combined` 上方旧注释不可信）。Manifest 按变体检查 `src/{main,combined,firebase,firebaseRelease,debug,profile}`。
- 推送：`tq_push_plugin/android/.../TQPushPlugin.java::resolveVendor`、`push_core/.../TQPushFactory.java`；`MainActivity.java` 的渠道读取与 resolver fallback 不一定相同。打包/分发才读 `tool/apk_unpack/split_channels.mjs`。
- `firebase` 不表示只有 Google 地图；地图 source 与二进制依赖分别核验。纯共享 Dart 改动无需构建所有渠道。

## SDK 与命令封装

- `tool/project.dart::_flutterExecutableFor/_sdkRootFromFvm`：standard 依次取 `TUQIANG_FLUTTER_STANDARD`/`FLUTTER_HOME` → target `.fvmrc` 的 FVM SDK → `flutter`；ohos 取 `TUQIANG_FLUTTER_OHOS`/`OHOS_FLUTTER_HOME` → `.fvmrc` → `flutter_ohos` 环境 → `ohos-flutter`。不要全局改 PATH 或用标准 SDK 代替 OHOS SDK。
- `_withDefaultStandardAndroidFlavor` 给 standard 的 `run`、`build apk/appbundle` 补 `--flavor allvendor`，`run` 不判断设备平台，iOS 运行需核对参数与 scheme。
- `OhosSharedConfigSnapshot.capture/restore` 只恢复列出的 OHOS 配置，不覆盖 lockfile 与 `.dart_tool`。会改同一 package 解析状态的命令串行执行；验证前后比较相关 diff，不以整仓 reset/clean 收尾。

诊断只展示需要的工具路径/版本，不输出整份环境、签名、AK 或生产配置。
