# Tuqiang 设备目录 → 选择 → 定位状态 → UI

本页保留设备链特有事实；Provider 通用语义见 [Riverpod 拓扑](riverpod-topology.md)，设备目录和消息的个人/企业分流先读 [账号模式](account-mode.md)。

## 状态与目录请求

`DeviceListPage` 同时持有分页/筛选 `setState` 与 `deviceCatalogProvider`。目录摘要、当前选择、定位快照、presentation 和页面局部值各有 owner，不是一份“设备全局状态”。

    DeviceListPage
    → deviceCatalogProvider（目录、分页、statusesById）
    → DeviceCoreCommands.setModelFromList
    → selectedDeviceProvider / deviceIdentityProvider(deviceId)
    → DeviceCoreRuntime → selectedLocationDeviceProvider
    → deviceLocationSnapshotProvider → presentation → UI

页面：`apps/tuqiang_app/lib/app/home/device_list_page.dart`；关键 symbol：`DeviceListPage`、`requestDeviceList`、`_loadMoreData`、`pullToRefresh`、`_selectDevice`。数据边界：

- `packages/shared/shared_device/lib/src/application/providers/device_catalog_provider.dart`
- `packages/shared/shared_device/lib/src/application/device_catalog_repository.dart`
- `packages/shared/shared_device/lib/src/data/http_device_catalog_repository.dart`
- `packages/shared/shared_device/lib/src/domain/device_catalog_query.dart::DeviceAccountMode`

    requestDeviceList
    → accountMode/filter/department/page + request scope
    → _requestDevicePage → DeviceCatalogRepository.fetchPage
    → HttpDeviceCatalogRepository → TQHttp
    → model/index state → 页面重建

主目录请求、批量 `statusesById` 和首次页尽力唤醒是三个独立异步分支。核验 requestVersion、owner liveness 与账号 scope；一条辅助支路失败不等于主请求失败。

## 选择、runtime 与页面分支

`_selectDevice` 先写共同选择状态，再按设备类型与状态进入页面族；可达叶子和范围门见 [变体事实](variant-surface.md) 与开发 Skill 的 [实施覆盖](../../tuqiang-dev/references/implementation-coverage.md)。

shared_device 关键文件：`device_core_commands.dart`、`device_core_runtime.dart`、`device_selection_providers.dart`、`providers/device_core_providers.dart`、`domain/device_core_ref.dart`。

设备变化时，`setModelFromList` 清旧 core family，并经 `DeviceCoreRuntime.invalidateExternalContext` 委托 app 清外部上下文；同一设备仍会 seed identity、发布 selected device，再按能力请求状态。`shared_device`、`shared_location` 与 `shared_message` 在 `LocationContainerHost` 和 `bootstrap.dart` 的 runtime override 组合。

## 根 Host 与定位

`LocationContainerHost` watch 目录、当前选择、定位/消息/presentation，listen 变化并激活当前设备：

    selectedDeviceProvider
    → LocationContainerHost listener
    → post-frame 检查 context.mounted + expectedDeviceId + expectedRevision
    → requestDeviceCoreExternalContext
    → 再比较 expectedDeviceId 与 selectedLocationDeviceProvider.deviceRef
    → app runtime 请求 profile/capabilities/snapshot/message

定位边界：

- `packages/shared/shared_location/lib/src/domain/device/location_device_ref.dart`
- `packages/shared/shared_location/lib/src/application/location_providers.dart`
- `packages/shared/shared_location/lib/src/application/location_runtime.dart`
- `packages/shared/shared_location/lib/src/data/location_status_repository.dart`
- `packages/shared/shared_location/lib/src/presentation/location_presentation_provider.dart`

`LocationDeviceRef.tryFromDevice` 可能不为 selected device 生成定位 key。snapshot 需核验 pending 去重、generation/liveness/scope、错误时旧状态策略，以及 `LocationRuntime.updatePosition` 如何连接 app-local Manager。

## 清理

切设备的 core/external-context 清理与 autoDispose 条件见 [Riverpod 拓扑](riverpod-topology.md)；切账号的目录、选择、定位、消息、pending 与 cache 见 [账号模式](account-mode.md)。logout 由 `session_reset_registry.dart` 聚合 reset participants，语言切换的清理范围更窄；根 Host 持续 watch 会延长当前 key 生命周期。

实时定位以上事实时，以 `requestDeviceList/_selectDevice`、`DeviceAccountMode/scopeAtRequest`、`DeviceCoreRuntime`、`LocationContainerHost`、`LocationDeviceRef` 与 `locationPresentationProvider` 为检索 seed。
