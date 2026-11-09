# Tuqiang 状态拓扑与设备链

Riverpod 版本以 lockfile 为准（当前 2.6.1）。项目混用 Provider、StateNotifierProvider、FutureProvider/NotifierProvider autoDispose family，以及 Widget state、Manager、Controller 与缓存；只描述目标链实际经过的机制。

## Provider 形态

| 形态 | 当前代表 | 调查重点 |
|---|---|---|
| Provider | `deviceCoreCommandsProvider`、`activeDeviceCorePresentationProvider` | 服务、派生值与 Container |
| StateNotifierProvider | `deviceCatalogProvider`、`selectedDeviceProvider` | 单份 Notifier/state 与 reset |
| StateNotifierProvider.autoDispose.family | `deviceIdentityProvider`、`deviceLocationSnapshotProvider` | 每个相等 key 一份实例 |
| FutureProvider.autoDispose.family | `monitorDeviceInfoProvider` | keyed AsyncValue 与底层 Future |
| NotifierProvider.autoDispose.family | `mediaDownloadQueueProvider`、`cameraProvisioningFlowProvider` | build(key)、state 与 lifecycle epoch |

- `provider(arg)` 选择 keyed 实例，不是给全局 State 传参；说明 key 字段与 `==/hashCode`（代表 value object：`DeviceCoreRef`、`LocationDeviceRef`、`VideoDeviceRef`）。数据受账号影响时还要证明 key、上游 cache scope 或 reset 隔离了账号。
- watch 持续依赖；read 一次读取；select 订阅字段；listen 说明 owner、previous/next 与副作用（Widget 只在 build listen，其他生命周期用 `listenManual`，外部 `ProviderContainer.listen` 由外部 owner close）。
- `invalidate(provider(key))` 与 `invalidate(family)` 范围不同；主动 session reset 与 autoDispose 是两套机制。
- autoDispose 只表示无人监听后可释放，根 Host、其他 watch 或 keepAlive 会延长寿命；onDispose 不等待 Future；FutureProvider 忽略旧实例发布但不终止底层请求。判断与修复规则见 [异步与状态](../../tuqiang-dev/references/state-async.md)。

## 设备目录

`apps/tuqiang_app/lib/app/home/device_list_page.dart::DeviceListPage` 同时持有分页/筛选 `setState` 与 `deviceCatalogProvider`；目录、当前选择、定位快照、presentation 和页面局部值各有 owner，不是一份"设备全局状态"。

```text
requestDeviceList（accountMode/filter/department/page + request scope）
→ _requestDevicePage → DeviceCatalogRepository.fetchPage
→ HttpDeviceCatalogRepository → TQHttp → devices/index/page/statusesById → 页面重建
```

数据边界在 `shared_device/lib/src/`：`application/providers/device_catalog_provider.dart`、`application/device_catalog_repository.dart`、`data/http_device_catalog_repository.dart`、`domain/device_catalog_query.dart::DeviceAccountMode`。主目录请求、批量 `statusesById` 与首页尽力唤醒是三个独立异步分支，分别核验 requestVersion、owner 存活与账号 scope。

## 选择 → runtime → 定位

```text
_selectDevice → DeviceCoreCommands.setModelFromList
→ deviceIdentityProvider(deviceId).seed → selectedDeviceProvider
→ LocationContainerHost listener
  → post-frame 检查 context.mounted + expectedDeviceId + expectedRevision
  → requestDeviceCoreExternalContext
  → 再比较 expectedDeviceId 与 selectedLocationDeviceProvider.deviceRef
→ app runtime 请求 profile/capabilities/snapshot/message
→ LocationDeviceRef.tryFromDevice → deviceLocationSnapshotProvider(ref) → presentation → UI
```

- 设备变化时 `setModelFromList` 清旧 core family，并经 `DeviceCoreRuntime.invalidateExternalContext` 委托 app 清外部上下文；同一设备仍会 seed identity、发布选择并按能力请求状态。`invalidateExternalContext/requestExternalContext` 只是 contract，必须追到 `getApp` 的实现。
- 页面族分流见 [变体与构建](variants.md)。
- 定位边界在 `shared_location/lib/src/`：`domain/device/location_device_ref.dart`、`application/location_providers.dart`、`application/location_runtime.dart`、`data/location_status_repository.dart`、`presentation/location_presentation_provider.dart`。`tryFromDevice` 可能不生成定位 key；snapshot 需核验 pending 去重、generation/scope、错误时旧状态策略，以及 `LocationRuntime.updatePosition` 如何连接 app-local Manager。

## 清理

切设备看 core family 与 external context；切账号看目录、选择、定位、消息、pending 与 cache（[账号模式](account-mode.md)）；logout 由 `session_reset_registry.dart` 聚合 reset participants，语言切换清理范围更窄。根 Host 持续 watch 会延长当前 key 的生命周期。

只回答本题经过的关键跳；完整状态调查才展开"定义 → key/实例 → 写入 → 消费 → 清理"。
