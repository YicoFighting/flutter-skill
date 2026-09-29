# Tuqiang Riverpod 状态拓扑

版本以当前 lockfile 为准。项目混用 Provider、StateNotifierProvider、FutureProvider/NotifierProvider autoDispose family，以及 Widget state、Manager、Controller 和缓存；只描述目标链实际经过的机制。

## 身份与依赖

| 形态 | 当前代表 | 调查重点 |
|---|---|---|
| Provider | deviceCoreCommandsProvider、activeDeviceCorePresentationProvider | 服务、派生值与 Container |
| StateNotifierProvider | deviceCatalogProvider、selectedDeviceProvider | 一份 Notifier/state 与 reset |
| StateNotifierProvider.autoDispose.family | deviceIdentityProvider、deviceLocationSnapshotProvider | 每个相等 key 一份实例 |
| FutureProvider.autoDispose.family | monitorDeviceInfoProvider | keyed AsyncValue 与底层 Future |
| NotifierProvider.autoDispose.family | mediaDownloadQueueProvider、cameraProvisioningFlowProvider | build(key)、state 与 lifecycle epoch |

先查问题对应的声明、key、写入或消费；生命周期/跨账号问题再展开 Container、销毁/reset 与账号 scope，不把整张拓扑当作每次回答的前置条件。

provider(arg) 选择 keyed 实例，不是给全局 State 临时传参。展示 key 字段和 ==/hashCode；数据受账号模式影响时，还要证明 key、上游 cache scope 或 reset 隔离了账号。代表 value object：DeviceCoreRef、LocationDeviceRef、VideoDeviceRef。

- watch：持续依赖并触发 Widget 重建或 Provider 重算；read：一次读取，不建立监听。
- listen：说明 owner、previous/next、调度和副作用。Widget listen 只在 build，其他 Widget 生命周期用 listenManual；外部 ProviderContainer.listen 的 subscription 由外部 owner close。
- select：说明订阅字段；invalidate(provider(key)) 与 invalidate(family) 要区分实例范围和有无监听时的重算/释放。

## 当前设备链

    TQDeviceInfoModel
    → DeviceCoreCommands.setModelFromList
    → deviceIdentityProvider(deviceId).seed
    → selectedDeviceProvider
    → app 注入 DeviceCoreRuntime
    → selectedLocationDeviceProvider
    → LocationDeviceRef.tryFromDevice
    → deviceLocationSnapshotProvider(deviceRef)

invalidateExternalContext/requestExternalContext 只是 contract callback，必须追到 app composition 的实现。

设备目录由 filter、department、view preference 等 Provider 通过 listen 驱动 DeviceCatalogNotifier，repository 产出 devices/index/page/statusesById；个人/企业链继续追 DeviceAccountMode、request scope 与 repository。

## 生命周期事实

- autoDispose 只表示无人监听并满足条件后可释放；根 Host、其他 watch 或 KeepAliveLink 会延长寿命。
- Riverpod 2.6.1 Notifier 可能跨重算复用，而上一轮 onDispose 会触发；每轮 build 恢复 active 并注册同步失效该轮 epoch。
- onDispose 不等待 Future。要求顺序的异步 teardown 使用显式可 await 的 shutdown/clear。
- 仅 read(autoDispose.notifier).load() 不保活；需要真实 watch/listen 或有业务依据的 keepAlive。
- FutureProvider 会忽略已 dispose/recompute 实例的状态发布，但不会自动终止底层 Future/HTTP 或其外部副作用。
- generation、owner liveness、account/device/session scope 与资源释放是独立防线；详见 [异步生命周期](../../tuqiang-dev/references/async-lifecycle.md)。
- Widget 的 build/initState/dispose/didUpdateWidget/didChangeDependencies 不得同步写 Provider；首次命令应由 Provider 初始化、用户事件或首帧后且 mounted 的回调触发。
- 主动 session invalidate/reset 与 autoDispose 是两套机制。

## 调查输出

沿当前链实际经过的 setState、Manager、Controller、Timer/Stream、plugin callback、HTTP 或持久化补足证据，不为凑全状态类型扩大搜索。输出能解释问题的关键跳与当前行号；只有完整状态调查才展开“定义 → key/实例 → 写入 → 保存 → 消费 → 清理”。
