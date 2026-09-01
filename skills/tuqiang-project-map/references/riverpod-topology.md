# Riverpod 状态拓扑与 family 语义

## 1. 产品边界与版本

本页的 Riverpod 拓扑属于 Tuqiang。Laoying 根状态当前是 `LYAppProvider extends ChangeNotifier` 加 app-local controller/repository；除非目标 Laoying 文件确实导入并使用 Riverpod，不得套用本页。

Tuqiang 在 `apps/tuqiang_app/pubspec.yaml` 声明 `flutter_riverpod`/`riverpod`，实际版本以对应 lockfile 为准；最近核验为 2.6.1，但回答 API 行为前必须重新读取。项目同时使用 `StateNotifierProvider`、普通 `Provider`、`FutureProvider.autoDispose.family` 与 `NotifierProvider.autoDispose.family`。

## 2. Provider 不是一种状态

| 形态 | 当前例子 | 状态与 key |
|---|---|---|
| `Provider<T>` | `deviceCoreCommandsProvider`、`activeDeviceCorePresentationProvider` | 服务或派生值，由当前 ProviderContainer 缓存 |
| `StateNotifierProvider<N,S>` | `deviceCatalogProvider`、`selectedDeviceProvider` | Container 内一份 Notifier/state |
| `StateNotifierProvider.autoDispose.family<N,S,K>` | `deviceIdentityProvider(deviceId)`、`deviceLocationSnapshotProvider(deviceRef)` | 每个相等 key 一份 Notifier/state |
| `FutureProvider.autoDispose.family<S,K>` | `monitorDeviceInfoProvider(videoRef)` | 每个 key 一份 `AsyncValue`/异步缓存 |
| `NotifierProvider.autoDispose.family<N,S,K>` | `mediaDownloadQueueProvider(sessionKey)`、`cameraProvisioningFlowProvider(deviceId)` | `build(K)` 收 key，每个 key 一份 state |

必须指出声明、Notifier/State、Container 作用域、family key 来源、写入者、消费者和销毁/reset，不能只说“Provider 存数据”。

## 3. family key 与当前 owner

`provider(arg)` 根据参数选择/创建 keyed Provider 实例，不是把参数塞进一份全局状态。当前复合 key：

- `packages/shared/shared_device/lib/src/domain/device_core_ref.dart::DeviceCoreRef`
- `packages/shared/shared_location/lib/src/domain/device/location_device_ref.dart::LocationDeviceRef`
- `packages/shared/shared_media/lib/src/domain/device/video_device_ref.dart::VideoDeviceRef`

这些 value object 实现 `operator ==` 与 `hashCode`；解释 family 时展示决定身份的字段。String key 也要说明按字符串值隔离。

## 4. 当前设备到定位 key

```text
TQDeviceInfoModel
  -> DeviceCoreCommands.setModelFromList
  -> deviceIdentityProvider(deviceId).seed
  -> selectedDeviceProvider.select
  -> selectedLocationDeviceProvider
  -> LocationDeviceRef.tryFromDevice(device)
  -> deviceLocationSnapshotProvider(deviceRef)
```

`DeviceCoreCommands` 现在属于 `shared_device`。跨定位/消息上下文的失效和请求不由它直接 import 其他 shared 包，而是调用 `DeviceCoreRuntime.invalidateExternalContext/requestExternalContext`；app 在 `bootstrap.dart`/coordinator 中注入实现。追参数来源时必须继续经过这层 runtime callback。

## 5. read/watch/listen/select

| API | 要核验的实际语义 |
|---|---|
| `ref.watch(provider)` | 订阅哪个具体实例；变化会让 Widget 重建或 Provider 重算 |
| `ref.read(provider)` | 一次性读取值或命令/Notifier，不建立持续订阅 |
| `ref.listen(provider, callback)` | 状态变化触发副作用/桥接；查 previous/next、首轮和异步调度 |
| `.select((state) => field)` | 只订阅哪个字段，何种变化触发消费者 |
| `ProviderScope.containerOf(context, listen: ...)` | 非 Consumer 或路由/composition 如何访问同一根 Container |
| `ref.invalidate(provider)` | 丢弃某个 family key 还是整个 family，何时重新构建 |

不要使用“build 只能 watch”“按钮只能 read”之类绝对规则。

## 6. autoDispose、keepAlive 与并发

- `autoDispose` 实例失去监听且满足生命周期条件后可释放；根 Host 或其他页面的 watch 会延长寿命。
- `ref.onDispose` 用于 Timer、Controller、网络/下载或持久化尾部清理。
- `mediaDownloadQueueProvider(sessionKey)` 虽为 autoDispose，但显式持有 `KeepAliveLink`，页面退出不等于立即清空。
- generation/requestVersion/mounted/pending future 是业务并发控制，不等于 Riverpod 自动取消请求。
- session reset 的主动 `ProviderContainer.invalidate` 与 autoDispose 是两套机制。

## 7. 当前代表拓扑

### 设备目录

文件：`packages/shared/shared_device/lib/src/application/providers/device_catalog_provider.dart`

```text
deviceCatalogFilterProvider ─┐
selectedDepartmentProvider ──┼─ ref.listen -> DeviceCatalogNotifier
viewPreferenceProvider ──────┘
deviceCatalogRepositoryProvider -> DeviceCatalogState
                                   ├─ devices/index/page
                                   └─ statusesById
```

`_requestDevicePage` 使用 requestVersion/mounted 防旧请求覆盖。首次第一页还有 T20 尽力唤醒的异步分支；它与列表结果和批量状态刷新不是一条同步返回。

### 当前设备与按设备状态

定义文件：

- `packages/shared/shared_device/lib/src/application/device_selection_providers.dart`：`selectedDeviceProvider`、`deviceIdentityProvider`；
- `packages/shared/shared_device/lib/src/application/providers/device_core_providers.dart`：module、Wi-Fi、SIM 等按设备状态。

```text
selectedDeviceProvider                      当前选择一份
deviceIdentityProvider(deviceId)            每个 deviceId
deviceModuleProvider(DeviceCoreRef)         每个 deviceId + deviceType
deviceWifiDetailProvider(deviceId)          每个 deviceId
deviceSimAuthProvider(deviceId)             每个 deviceId
```

展示聚合见 `packages/shared/shared_device/lib/src/presentation/device_core_presentation.dart::activeDeviceCorePresentationProvider`。

### 定位

文件：`packages/shared/shared_location/lib/src/application/location_providers.dart`

```text
selectedDeviceProvider + deviceIdentityProvider
  -> selectedLocationDeviceProvider
  -> LocationDeviceRef?
       ├─ deviceLocationSnapshotProvider(ref)
       ├─ locationDeviceProfileProvider(deviceId)
       ├─ locationCapabilitiesProvider(deviceId)
       ├─ locationPresentationProvider(ref)
       ├─ locationCommandProvider(ref)
       └─ locationPromptProvider(ref)
```

展示聚合见 `packages/shared/shared_location/lib/src/presentation/location_presentation_provider.dart`。snapshot 的坐标同步通过注入的 location runtime callback 进入 app 旧 Manager，不应描述为 shared_location 直接拥有该 Manager。

### 媒体与 Camera

- `packages/shared/shared_media/lib/src/application/media_download_queue_provider.dart::mediaDownloadQueueProvider`
- `packages/feature/feature_camera/lib/src/video/providers/video_read_providers.dart::monitorDeviceInfoProvider`
- `packages/feature/feature_camera/lib/src/pages/set_net/application/camera_provisioning_notifier.dart::cameraProvisioningFlowProvider`

不要因视频 key 在 shared_media 就把 Camera 私有流程归给 shared。

## 8. Laoying 状态边界

Laoying 先追：

```text
LYAppProvider(ChangeNotifier)
  -> session/user/reset coordinator/refresh bus
  -> notifyListeners
  -> LYAppScope 消费者

app-local page
  -> domain controller
  -> domain repository/adapters
  -> controller/Widget 发布与展示
```

关键入口为 `apps/laoying_app/lib/app/session/ly_app_provider.dart` 与各领域 `providers/*controller.dart`。必须按实际 controller 基类和监听方式说明；不能把 `notifyListeners` 改写成 `ref.watch`。

## 9. 混合状态扫描

完整链路还要搜索 Widget `setState`、Manager/单例、controller、Timer/Stream、插件 callback、直接 HTTP、SharedPreferences/文件/数据库。若同一链写 Riverpod 与 Manager，要分别列写入原因和消费者。

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "final <provider名>|class <Notifier名>|class <State名>" apps packages --glob '*.dart'
rg -n "<provider名>\(|<provider名>\.notifier|invalidate\(<provider名>|refresh\(" apps packages --glob '*.dart'
rg -n "ref\.(read|watch|listen)|\.select\(" <Tuqiang相关文件> --glob '*.dart'
rg -n "operator ==|hashCode" <family-key文件>
rg -n "autoDispose|keepAlive|onDispose|requestVersion|generation|mounted" <Provider及Notifier文件>
rg -n "class LYAppProvider|notifyListeners|resetSession|class .*Controller" apps/laoying_app/lib/app --glob '*.dart'
```

最终整理成“产品 → 定义 → 参数/实例来源 → 写入 → 保存 → 订阅/读取 → UI → 清理”，不要粘贴搜索列表。
