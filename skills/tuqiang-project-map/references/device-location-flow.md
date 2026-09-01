# Tuqiang 设备目录 → 选择 → 定位状态 → UI

本页只适用于 Tuqiang，是 Riverpod family、跨 shared package runtime 与混合状态的代表链。Laoying 的 GPS/设备链必须从 `apps/laoying_app/lib/app` 另行追踪。

## 1. 状态不是一份

```text
DeviceListPage
  ├─ Widget setState：分页 loading/筛选 UI
  ├─ shared_device::deviceCatalogProvider：目录、分页、statusesById
  └─ 点击设备
       -> DeviceCoreCommands.setModelFromList
       -> selectedDeviceProvider / deviceIdentityProvider(deviceId)
       -> DeviceCoreRuntime（app 注入外部定位/消息上下文）
       -> selectedLocationDeviceProvider
       -> deviceLocationSnapshotProvider(LocationDeviceRef)
       -> presentation Provider / 页面 watch
       -> UI
```

目录摘要、当前选择、定位快照、模块状态与页面局部值各有 owner，不能合并成“设备全局状态”。

## 2. 目录入口与请求

页面：`apps/tuqiang_app/lib/app/home/device_list_page.dart`

关键 symbol：`DeviceListPage`、`requestDeviceList`、`_loadMoreData`、`pullToRefresh`、`_selectDevice`。首次 build 会触发目录请求；页面 watch `deviceCatalogProvider`，分页 loading 仍由 `setState` 管理。

状态：`packages/shared/shared_device/lib/src/application/providers/device_catalog_provider.dart`

数据边界：

- contract：`packages/shared/shared_device/lib/src/application/device_catalog_repository.dart`
- HTTP 实现：`packages/shared/shared_device/lib/src/data/http_device_catalog_repository.dart`

```text
requestDeviceList
  -> _requestDevicePage(page/filter/requestVersion)
  -> DeviceCatalogRepository.fetchPage
  -> HttpDeviceCatalogRepository
  -> TQHttp（只引用 API 常量名）
  -> model/index state 发布
  -> 页面重建
  ├─ unawaited 批量状态刷新 -> statusesById
  └─ 首次第一页的 T20 尽力唤醒分支
```

requestVersion/mounted 防止旧筛选请求覆盖新结果。T20 唤醒、页面结果和批量状态是不同异步分支，单台唤醒失败不等于目录请求失败。

## 3. 点击设备与路由分支

`DeviceListPage._selectDevice` 先检查升级/兼容，再调用 `ref.read(deviceCoreCommandsProvider).setModelFromList(...)`，然后按设备类型、scene 与服务状态进入 GPS、人员、Pet、Tag、MiFi、行车记录仪或监控等 route。共同状态写入发生在路由分支前；必须按实际 model 继续追最终 route/Page。

## 4. shared_device 写入与 app runtime

文件：

- `packages/shared/shared_device/lib/src/application/device_core_commands.dart`
- `packages/shared/shared_device/lib/src/application/device_core_runtime.dart`
- `packages/shared/shared_device/lib/src/application/device_selection_providers.dart`
- `packages/shared/shared_device/lib/src/application/providers/device_core_providers.dart`
- `packages/shared/shared_device/lib/src/domain/device_core_ref.dart`

`setModelFromList` 清理旧设备 core family，调用注入的 `DeviceCoreRuntime.invalidateExternalContext(model)`，seed identity，发布 selected device，再按能力请求 Wi-Fi/module 等状态。`requestSelectedLocationContext` 通过 `DeviceCoreRuntime.requestExternalContext` 委托 app。

不要再描述成 `DeviceCoreCommands` 直接构造/清理 location family。跨 `shared_device`、`shared_location`、`shared_message` 的组合发生在 `apps/tuqiang_app/lib/app/coordinators/location_container_host.dart` 与 `bootstrap.dart` 的 runtime override。

## 5. 根 Host 激活外部上下文

`LocationContainerHost` watch 目录、当前选择、定位/消息/展示状态，listen 选择和目录变化，并通过 post-frame 激活已选设备：

```text
selectedDeviceProvider 发布
  -> LocationContainerHost listener
  -> addPostFrameCallback + revision/deviceId 校验
  -> DeviceCoreCommands.requestSelectedLocationContext
  -> app runtime 请求 location profile/capabilities/snapshot/message
```

目录批量状态通过 `applyCatalogStatus` 同步给当前定位快照；主动 refresh 是另一条来源。最近核验中 `gpsModuleList` 不在 `FeatureRouterRegistry` 的 location-on-push 刷新集合，首次进入时主要依靠根 Host；回答前仍需实时复查。

## 6. 定位 key、请求与展示

文件：

- `packages/shared/shared_location/lib/src/domain/device/location_device_ref.dart`
- `packages/shared/shared_location/lib/src/application/location_providers.dart`
- `packages/shared/shared_location/lib/src/application/location_dependencies.dart`
- `packages/shared/shared_location/lib/src/application/location_runtime.dart`
- `packages/shared/shared_location/lib/src/data/location_status_repository.dart`
- `packages/shared/shared_location/lib/src/presentation/location_presentation_provider.dart`

`LocationDeviceRef.tryFromDevice` 会判断设备类型/Camera scene；selected device 不一定产生定位 key。key 由 `deviceId + deviceType` 判等。

```text
deviceLocationSnapshotProvider(ref)
  -> DeviceLocationSnapshotNotifier.refresh
  -> pending future 去重 + generation/mounted
  -> LocationStatusRepository.fetchStatus
  -> TQHttp
  -> applyStatus
  -> DeviceLocationSnapshotState
  -> 注入的 LocationRuntime.updatePosition（app 连接旧 Manager）
  -> presentation/page watch -> UI
```

错误会保留旧 status 并记录 error；不要说失败必然清空。页面可能同时 watch identity、profile、snapshot、presentation 或 Manager 镜像值，最终要追到 Text/Image/按钮/地图 marker。

## 7. 清理

- 切设备：`DeviceCoreCommands` 清旧 core family，并由 app runtime 清理目标外部上下文；旧 location key 失去根 Host/页面监听后进入 autoDispose 条件。
- logout：`session_reset_registry.dart` 聚合 device/location/message/app 与 Auth/GPS/Camera/Pet 等 reset participants。
- 语言切换：`language_change_coordinator.dart` 只清部分设备/GPS/广告/逆地理状态，不等于 logout。
- 根 Host 的持续 watch 会让当前 key 活得比单页面更久。

## 8. 实时核验

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "requestDeviceList|_loadMoreData|pullToRefresh|_selectDevice|setModelFromList" apps/tuqiang_app/lib/app/home/device_list_page.dart
rg -n "deviceCatalogProvider|class DeviceCatalogNotifier|_requestDevicePage|requestVersion|T20|fetchStatuses" packages/shared/shared_device/lib
rg -n "class DeviceCoreRuntime|invalidateExternalContext|requestExternalContext|selectedDeviceProvider|deviceIdentityProvider" packages/shared/shared_device/lib
rg -n "class LocationContainerHost|applyCatalogStatus|requestSelectedLocationContext|selectedLocationDeviceProvider" apps/tuqiang_app packages/shared --glob '*.dart'
rg -n "class LocationDeviceRef|class DeviceLocationSnapshotNotifier|fetchStatus|applyStatus|locationPresentationProvider" packages/shared/shared_location/lib
rg -n "<目标状态字段>|<目标展示文案或getter>" apps packages --glob '*.dart'
```
