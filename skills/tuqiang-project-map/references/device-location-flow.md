# 设备目录 → 选择 → 定位状态 → UI 完整链路

这是项目中一条适合解释 Riverpod family、跨文件状态和混合架构的代表性业务链，不是 `tuqiang-project-map` 的主职责或默认入口。只有问题涉及设备目录、设备选择、定位状态或 GPS UI 时才读取本页。以下保存路径和 symbol；引用时必须用 `rg -n` 更新当前行号，并根据用户实际入口裁剪分支。

## 1. 总览：不是一份“设备状态”

```text
设备列表页
  ├─ 页面局部状态：setState（分页 loading、筛选 UI、输入等）
  ├─ 目录状态：deviceCatalogProvider
  │    ├─ devicesById / 列表 / 页码
  │    └─ statusesById（批量设备状态）
  └─ 点击设备
       -> deviceCoreCommandsProvider.setModelFromList
       -> selectedDeviceProvider（一份当前选择）
       -> deviceIdentityProvider(deviceId)（按设备身份）
       -> selectedLocationDeviceProvider（派生 LocationDeviceRef）
       -> deviceLocationSnapshotProvider(deviceRef)（按设备定位快照）
       -> locationDeviceProfileProvider(deviceId)（按设备属性）
       -> presentation Provider / 页面 watch
       -> UI 重建与展示
```

同一设备的“列表摘要状态”“当前选择”“定位详情快照”“模块列表”“页面局部 loading”各有 owner。回答时必须逐份区分。

## 2. 进入设备列表与获取目录

### 页面入口

文件：`apps/tuqiang_app/lib/app/home/device_list_page.dart`

关键 symbol：

- `DeviceListPage`、`_DeviceListPageState`
- `_firstVMBuild`：首次构建触发列表请求的入口之一
- `requestDeviceList`：把页面筛选同步给 Notifier，再发起请求
- `_buildBody`：`watch(deviceCatalogProvider)` 订阅目录变化，并取得 notifier 读取展示字段/命令
- `_loadMoreData`：使用 Widget `setState` 管理页面级分页 loading
- `pullToRefresh`：下拉刷新入口

### 目录 Provider

文件：`packages/shared/shared_business/lib/device/application/providers/device_catalog_provider.dart`

关键 symbol：

- `DeviceCatalogState`：目录视图、设备/状态索引等对外状态
- `DeviceCatalogFilterState` / `deviceCatalogFilterProvider`
- `SelectedDepartmentState` / `selectedDepartmentProvider`
- `DeviceCatalogViewPreferenceState` / `deviceCatalogViewPreferenceProvider`
- `deviceCatalogRepositoryProvider`
- `deviceCatalogProvider`
- `DeviceCatalogNotifier.requestDeviceList`
- `DeviceCatalogNotifier._requestDevicePage`
- `DeviceCatalogNotifier._refreshDeviceStatusesSafely` / `_refreshDeviceStatuses`
- `DeviceCatalogNotifier._emit`

Provider builder 用 `ref.listen` 监听筛选、部门和视图偏好，将外部状态变化合入目录展示；这不是 Widget 的监听。

### Repository 与网络

文件：`packages/shared/shared_business/lib/device/data/device_catalog_repository.dart`

```text
DeviceCatalogNotifier.requestDeviceList
  -> DeviceCatalogQuery（个人/企业、状态、产品类型、部门、关键字）
  -> _requestDevicePage（pageIndex、requestVersion）
  -> DeviceCatalogRepository.fetchPage
  -> HttpDeviceCatalogRepository.fetchPage
  -> DeviceCatalogRequestMapper.address/params
  -> TQHttp（只引用 API 常量名，不展示实际地址值）
  -> ResultModel.success + TCheck 类型收窄
  -> TQDeviceInfoTotalModel
  -> Notifier 更新 infoModel / devicesById 并 _emit
  -> 页面 watch 导致重建
  -> 异步批量 fetchStatuses 更新 statusesById
```

`_requestDevicePage` 使用 request version 和 `mounted` 防止旧请求覆盖新筛选结果。批量状态刷新是后续异步分支，不能伪装成 `await fetchPage` 的同步返回字段。

## 3. 点击某台设备

文件：`apps/tuqiang_app/lib/app/home/device_list_page.dart`

`_selectDevice` 的关键顺序：

1. 用当前 presentation 数据处理同设备复用；
2. 检查强制升级与设备类型兼容；
3. 调用 `ref.read(deviceCoreCommandsProvider).setModelFromList(...)`；
4. 再根据设备类型、scene/cameraScene、服务状态选择不同 route。

因此“点击设备”的共同状态写入发生在路由分支之前。随后可能进入 GPS、人员、Pet、Tag、MiFi、行车记录仪、监控等不同页面；必须按实际 model 分支继续追 route，不能把某一页面当作所有设备的统一终点。

常见 route symbol 包括 `AppRouters.gpsModuleList`、`personModuleList`、`petModuleList`、`beaconsModuleList`、`jankHomePage`、`drivingModuleList`、`monitorModuleList`、`tagLocation`、`wifiModuleList`。回答前核对这些常量当前映射的 feature owner 和 builder。

## 4. 设备选择写到哪里

文件：`packages/shared/shared_business/lib/device/application/device_core_commands.dart`

`DeviceCoreCommands.setModelFromList`：

```text
列表 TQDeviceInfoModel
  -> 计算 previous DeviceCoreRef 与 LocationDeviceRef.tryFromDevice(model)
  -> 切换设备时 invalidate 旧设备的 core family
  -> invalidate 目标设备可能残留的 location family
  -> deviceIdentityProvider(deviceId).notifier.seed(model)
  -> selectedDeviceProvider.notifier.select(model, source)
  -> 可选同步 TQScreenSecureManager
  -> Wi-Fi 分支请求 detail
  -> requestModuleList -> deviceModuleProvider(DeviceCoreRef).notifier.refresh
```

相关声明在：

- `packages/shared/shared_business/lib/device/application/providers/device_core_providers.dart`
- `packages/shared/shared_business/lib/device/application/providers/device_core_states.dart`
- `packages/shared/shared_business/lib/device/domain/device_core_ref.dart`

状态位置：

| 状态 | 实例数量 | key |
|---|---|---|
| `selectedDeviceProvider` | 当前 ProviderContainer 一份 | 无 family key |
| `deviceIdentityProvider(deviceId)` | 每个设备 ID 一份 | `String` |
| `deviceModuleProvider(deviceRef)` | 每个设备 ID + 类型一份 | `DeviceCoreRef` |
| Wi-Fi/SIM/base settings | 每个设备 ID 一份 | `String` |

`DeviceCoreRef` 实现值相等和 `hashCode`，相同 `deviceId + deviceType` 会命中同一 family 实例。

## 5. 根 Host 如何激活定位上下文

文件：`apps/tuqiang_app/lib/app/coordinators/location_container_host.dart`

`LocationContainerHost.build` 在根部：

- watch `deviceCatalogProvider`；
- listen 目录变化，把选中设备的最新 model/status 同步到 identity/定位快照；
- listen `selectedDeviceProvider`，在选择变化后通过 post-frame 调度激活；
- watch `selectedLocationDeviceProvider`；
- key 有效时 watch 定位快照、profile、capabilities、消息摘要、presentation、prompt，并 listen command 状态。

`_scheduleSelectedDeviceActivation` 会验证 deviceId/revision，先同步目录已有状态，再在选择来源符合条件时调用：

```text
DeviceCoreCommands.requestSelectedLocationContext
  -> deviceLocationSnapshotProvider(locationRef).notifier.refresh
  -> locationDeviceProfileProvider(deviceId).notifier.refresh
  -> locationCapabilitiesProvider(deviceId).notifier.refreshLocationTypes
  -> messageDeviceSummaryProvider(deviceId).notifier.refresh
```

这里同时存在两个定位状态来源：

1. 目录批量状态已有值时，`_syncSelectedStatusFromCatalog` 直接 `applyStatus`；
2. 选择后 `requestSelectedLocationContext` 主动发起单设备刷新。

两条路径通过 generation/request state 防止旧请求覆盖新值。解释时要展示实际入口触发了哪一条或两条。

最近扫描基线中，`gpsModuleList` 不在 `FeatureRouterRegistry` 的定位 route-refresh 集合里，因此从设备列表首次进入该页时，snapshot 首次请求来自根 Host 的“选中设备激活”，不是 `LocationRouteObserver`。页面自身的倒计时、下拉刷新和子页返回仍可能再次刷新；回答前重新核对 registry 与页面当前代码。

## 6. 如何从选择派生 family key

文件：

- `packages/shared/shared_business/lib/location/domain/device/location_device_ref.dart`
- `packages/shared/shared_business/lib/location/application/providers/location_providers.dart`

```text
selectedDeviceProvider
  -> deviceId
  -> deviceIdentityProvider(deviceId).device
  -> LocationDeviceRef.tryFromDevice(device)
  -> selectedLocationDeviceProvider.deviceRef
```

`LocationDeviceRef.tryFromDevice` 还会判断设备类型/Camera scene 是否支持定位，所以 selected device 不一定产生 location key。`LocationDeviceRef` 的相等性由 `deviceId + deviceType` 决定。

## 7. 单设备定位状态请求

文件：

- `packages/shared/shared_business/lib/location/application/providers/location_providers.dart`
- `packages/shared/shared_business/lib/location/application/providers/location_dependencies.dart`
- `packages/shared/shared_business/lib/location/data/location_status_repository.dart`
- `packages/shared/shared_business/lib/location/application/providers/location_states.dart`

主链：

```text
deviceLocationSnapshotProvider(LocationDeviceRef)
  -> DeviceLocationSnapshotNotifier
  -> refresh / _refresh
  -> LocationStatusRepository.fetchStatus(deviceId)
  -> TQHttp.postWithConfig(API 常量名, deviceIds: [deviceId])
  -> ResultModel + TCheck + TQDeviceStatusModel.fromJson
  -> applyStatus
  -> DeviceLocationSnapshotState.statusModel
  -> 同步 TQInfoManager.setPosition（混合状态副作用）
```

`refresh` 会复用未完成的 future（除非 force），`_generation`、`mounted` 和 `invalidatePendingRequest` 用于抑制过期结果。错误时状态保留旧 `statusModel` 并写入 error；不要简单描述为“失败就清空页面”。

## 8. 哪里读取并展示

共享展示聚合：

- `packages/shared/shared_business/lib/device/presentation/device_core_presentation.dart::activeDeviceCorePresentationProvider`
- `packages/shared/shared_business/lib/location/presentation/location_presentation_provider.dart::activeLocationPresentationDataProvider`
- `packages/shared/shared_business/lib/location/application/providers/location_providers.dart::locationPresentationProvider`

页面可以：

1. watch 聚合 presentation；
2. watch 某个 family state；
3. 用 `.select` 只订阅字段；
4. 使用 Manager/Controller 的镜像值；
5. 使用 `setState` 管理纯页面状态。

代表页面 `packages/feature/feature_camera/lib/src/jank/jank_home_page.dart` 会从当前设备构造 location key，并分别 watch identity、profile 和 snapshot 的选定字段；`requestDeviceState` 可手动调用 snapshot notifier 的 `refresh`。这能说明同一页面可能同时消费多个 keyed state，而不是只 watch 一个“大状态”。

定位/GPS 页面还有各自的 presentation mapper、地图插件和页面 Controller。回答某个具体字段“在哪里展示”时，从字段名或 getter 继续 `rg -n` 到 Text/Image/地图 marker 等实际 Widget，不能停在 presentation Provider。

## 9. 清理与账号隔离

- 切换设备：`DeviceCoreCommands._invalidate(previous)` 显式清理旧设备的 identity/module/wifi/sim core family；`_invalidateLocationContext(nextLocationRef)` 清理目标设备可能残留的 location/message family，再发布新选择。
- 旧设备的 location family 并非在 `setModelFromList` 中由 `_invalidateLocationContext` 显式清除；根 Host 改为订阅新 key 后，旧 key 通常因失去监听进入 autoDispose 条件，登出时还会由 session reset 兜底。
- 退出账号/session 变化：`apps/tuqiang_app/lib/app/session/session_reset_registry.dart` invalidate 目录、选择、设备 family、定位 family 等。
- feature 私有状态：由 feature 提供 session reset participant，例如 Camera 的 resetter。
- autoDispose：页面/根 Host 不再监听时可释放 keyed 实例；根 Host 持续 watch 的实例寿命可能长于单页。

## 10. 一次解释必须回答的问题

- 列表什么时候请求？筛选/部门/分页参数从哪里来？
- 网络返回后写的是目录 model、目录 status，还是定位详情 status？
- 点击后哪一行先发布 selected device，哪一行才导航？
- `deviceId`/`DeviceCoreRef`/`LocationDeviceRef` 分别来自哪里，如何判等？
- 哪个 Notifier 保存状态，哪个 Provider 只是派生展示？
- 根 Host 和目标页面各 watch/listen 什么？
- 状态最终用于哪个 Widget 字段、地图 marker、文本或可用性判断？
- 切设备、页面离开、语言切换和退出账号时怎样失效？
- 哪些局部值在 `setState`，哪些副作用进入 Manager/插件？

## 11. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "class DeviceListPage|_firstVMBuild|requestDeviceList|_selectDevice|setModelFromList" apps/tuqiang_app/lib/app/home/device_list_page.dart
rg -n "deviceCatalogProvider|class DeviceCatalogNotifier|_requestDevicePage|fetchPage|fetchStatuses|_emit" packages/shared/shared_business/lib/device
rg -n "selectedDeviceProvider|deviceIdentityProvider|deviceModuleProvider|class DeviceCoreRef" packages/shared/shared_business/lib/device
rg -n "class LocationContainerHost|selectedLocationDeviceProvider|deviceLocationSnapshotProvider|requestSelectedLocationContext" apps packages --glob '*.dart'
rg -n "class LocationDeviceRef|class DeviceLocationSnapshotNotifier|fetchStatus|applyStatus|activeLocationPresentationDataProvider" packages/shared/shared_business/lib/location
rg -n "<目标状态字段>|<目标展示文案或getter>" apps packages --glob '*.dart'
```
