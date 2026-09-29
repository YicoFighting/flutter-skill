# Tuqiang 平台、地图后端与设备页面变体

本页只保存当前源码的候选变体事实。账号模式、平台/target、runtime backend、device scene 与最终 route/Page 分栏记录，不生成机械笛卡尔积；账号规则见 [account-mode.md](account-mode.md)，开发关闭矩阵见 [实施覆盖](../../tuqiang-dev/references/implementation-coverage.md)。

## 平台宿主

`standard → Android/iOS`，`ohos → HarmonyOS`。target 需由 tracked app、pubspec identity 与入口共同证明；命中 channel、PlatformView、权限、资源或原生 SDK 时继续追各平台目录。一次 `standard` analyze/build 不能证明 Android 与 iOS 运行行为相同。

涉及推送、广告、ABI、原生地图依赖或安装包差异时，再按 [构建与运行上下文](build-runtime-context.md) 区分 Android flavor 与分发渠道；不要用默认 allvendor 包的结果关闭其他变体。

## 地图实现面

公共选择层位于 `packages/plugins/tq_map_plugin`：

- `tq_map_enum.dart::TQMapSourceType` 当前候选为 `baidu/google/gaode`，回答前重查；
- `TQBaseMapWidgetState.buildMapView` 分派三条 Dart 分支；
- `TQMapUseSceneType` 标识 location、lineTrace、smartTrace、pointTrace、overview、follow、fence、report、addDevice 等 scene；修改 protocol/adapter 时反查全部调用者；
- Android/iOS 的百度、高德使用各自 PlatformView/native factory，Google 使用 `google_maps_flutter`；
- `apps/ohos/lib/main.dart` 注入 map host，插件 ArkTS 侧连接华为 Map Kit。

“花瓣地图”映射为 HarmonyOS 的华为 Map Kit 平台后端，不是第四个 Dart source；兼容 BMap/AMap factory id 也不证明运行了对应 SDK。支持三源的主地图候选集合为 Android/iOS × 百度/高德/Google，加 HarmonyOS Map Kit 共 7 行；逐行交付状态见 [实施覆盖](../../tuqiang-dev/references/implementation-coverage.md)。POI、街景或外部导航的独立 channel 不由主地图矩阵自动覆盖。

    Page/Widget
    → TQMapUseSceneType + options/protocol
    → MapSourceManager / TQMapSourceType（标准端）
    → TQBaseMapWidgetState dispatch
    → native adapter / Google controller / OHOS resolver
    → 坐标、marker/polyline、回调、生命周期与资源

## 设备列表到详情

`DeviceListPage._selectDevice` 写入共同选择状态后，当前至少检查：

| 条件 | 分支方向 |
|---|---|
| 服务过期/状态异常 | 续费或状态提示，可能不进详情 |
| GPS + 基础服务/新手状态 | base 或 novice location 页面 |
| GPS + normal/person/keys/pet scene | GPS、人员、场景、Pet 页面族 |
| LBS | beacon 页面族 |
| Camera + cameraScene | 摄像头、行车、停车或监控页面族 |
| Tag | Tag location |
| 其他设备类型 | Wi-Fi/MiFi 页面族 |

从问题可达的 route 追到最终 Page；仅当需求涉及“更多详情/设备详情/更多设置”或公共入口时继续追对应事件与其他调用者。多个叶子不自动触发提问：先由用户给定页面、设备和源码收窄，仍有会改变结论的范围歧义才澄清。

实时定位以上事实时，以设备类型/scene、最终 Page、`TQMapSourceType/TQMapUseSceneType`、平台 factory id、OHOS `MapComponent` 和目标 Widget 为检索 seed。
