# Riverpod 状态拓扑与 family 语义

## 1. 版本与现实边界

当前项目在 `apps/tuqiang_app/pubspec.yaml` 声明 Flutter Riverpod 约束，解析版本记录在对应 lockfile。回答具体 API 行为前先核对两处；本 reference 的扫描基线观察到 2.6.x，不把它当成永久版本。

项目主要使用 `StateNotifierProvider`，同时存在普通 `Provider`、`FutureProvider.autoDispose.family` 和 Riverpod 2 的 `NotifierProvider.autoDispose.family`。没有搜到某种 Provider 不代表项目永远不用它，结论必须限定为“本次当前源码扫描”。

## 2. Provider 不是一种状态

| 形态 | 当前项目例子 | 状态在哪里 | 参数/依赖在哪里进入 |
|---|---|---|---|
| `Provider<T>` | `deviceCoreCommandsProvider`、`activeDeviceCorePresentationProvider` | 通常是无可变状态的服务或派生值，由 ProviderContainer 缓存 | builder 内通过 `ref` 读取/订阅依赖 |
| `StateNotifierProvider<N,S>` | `deviceCatalogProvider`、`selectedDeviceProvider` | `StateNotifier.state`；实例归当前 ProviderContainer | Provider builder 构造 Notifier |
| `StateNotifierProvider.autoDispose.family<N,S,K>` | `deviceIdentityProvider(deviceId)`、`deviceLocationSnapshotProvider(deviceRef)` | 每个 family key 对应一个独立 Notifier/state 实例 | family builder 的 `deviceId`/`deviceRef` 参数 |
| `FutureProvider.autoDispose.family<S,K>` | `monitorDeviceInfoProvider(videoRef)` | 每个 key 对应独立 `AsyncValue<S>`/异步缓存 | async builder 的 `key` |
| `NotifierProvider.autoDispose.family<N,S,K>` | `mediaDownloadQueueProvider(sessionKey)`、`cameraProvisioningFlowProvider(deviceId)` | Notifier 的 `state`，每个 key 一份 | `build(K arg)` 收到 key |

不要只说“这个 Provider 存数据”。必须指出：Provider 声明、Notifier/State 类型、Container 作用域、family key、写方法、消费者与销毁/reset。

## 3. family 参数为什么能传

以 `deviceLocationSnapshotProvider(deviceRef)` 为例：

```text
deviceLocationSnapshotProvider                    family 定义
  + LocationDeviceRef(deviceId, deviceType)       family key
  = 一个具体 Provider 实例                       keyed instance
  -> DeviceLocationSnapshotNotifier               该 key 的 Notifier
  -> DeviceLocationSnapshotState                  该 key 的状态
```

`provider(arg)` 不是把普通函数参数塞进“一份全局状态”。`.family` 根据参数选择或创建一个 keyed Provider 实例；在同一 ProviderContainer 内，相等 key 复用同一实例，不同 key 隔离状态。

项目里的复合 key：

- `packages/shared/shared_business/lib/device/domain/device_core_ref.dart::DeviceCoreRef`
- `packages/shared/shared_business/lib/location/domain/device/location_device_ref.dart::LocationDeviceRef`
- `packages/shared/shared_business/lib/video/domain/device/video_device_ref.dart::VideoDeviceRef`

这些不可变对象实现 `operator ==` 与 `hashCode`，因此“字段值相等的新对象”可以命中同一 family 实例。解释 family 时必须展示 key 类的相等性代码；若 key 是 `String deviceId`，也要说明它按字符串值区分实例。

## 4. 参数从哪里来

典型设备链：

```text
TQDeviceInfoModel
  -> DeviceCoreCommands.setModelFromList
  -> selectedDeviceProvider（当前选中设备）
  -> selectedLocationDeviceProvider（派生并校验是否支持定位）
  -> LocationDeviceRef(deviceId, deviceType)
  -> deviceLocationSnapshotProvider(deviceRef)
```

另一个典型链：

```text
selectedDeviceProvider.deviceId + deviceType
  -> DeviceCoreRef
  -> deviceModuleProvider(deviceRef)
```

不能从某个消费端的 `provider(key)` 就断言 key 来源。继续向上查局部变量、Widget 参数、route arguments、选中 Provider 或 composition callback，直到找到用户动作或生命周期入口。

## 5. read / watch / listen / select 的实际语义

| API | 当前链路中应检查什么 |
|---|---|
| `ref.watch(provider)` | 建立响应式依赖；Widget 可能重建，Provider builder 可能重新计算。查被 watch 的具体实例，family key 不能省略。 |
| `ref.read(provider)` | 读取当下值或获取命令对象/Notifier，不建立持续订阅。它可出现在 build 中，但后续变化不会因这次 read 自动触发重建。 |
| `ref.listen(provider, callback)` | 状态变化时执行副作用/桥接；查 previous/next 条件、首轮是否触发、回调是否异步调度。 |
| `.select((state) => field)` | 只订阅选中的派生字段；说明哪个字段变化会触发消费者。 |
| `ProviderScope.containerOf(context, listen: ...)` | 在非 Consumer API、路由 builder 或 callback 中访问同一个根 Container；查 `listen` 参数和作用域。 |
| `ref.invalidate(provider)` | 丢弃指定实例；family 可失效一个 key，也可失效整个 family。查重新被读/看后如何重建。 |

不要使用“build 只能 watch”“按钮只能 read”这类绝对规则。判断依据是调用点需要响应式订阅、一次性读取还是副作用监听。

## 6. autoDispose、keepAlive 与清理

- `autoDispose`：当某个 keyed 实例没有监听者并满足 Riverpod 生命周期条件时，可被释放；再次读取/监听会创建新实例。
- `ref.onDispose`：项目用它取消 Timer、Controller、网络/下载资源或持久化尾部状态。
- `ref.keepAlive()`：可以延长 autoDispose 实例寿命。`mediaDownloadQueueProvider(sessionKey)` 明确持有 KeepAliveLink，因此不能只看到 `autoDispose` 就说页面退出后立即清空。
- Notifier 内还常用 generation/requestVersion/mounted 防止旧异步结果覆盖新状态；这是业务并发控制，不等同于 Riverpod 自动取消网络请求。
- session reset 通过 `ProviderContainer.invalidate` 主动清除跨账号状态，和 autoDispose 是两套机制。

## 7. 项目代表拓扑

### 设备目录（单实例）

文件：`packages/shared/shared_business/lib/device/application/providers/device_catalog_provider.dart`

```text
deviceCatalogFilterProvider ─┐
selectedDepartmentProvider ──┼─ ref.listen -> DeviceCatalogNotifier._emit/刷新视图
viewPreferenceProvider ──────┘
deviceCatalogRepositoryProvider -> DeviceCatalogNotifier -> DeviceCatalogState
                                                     ├> devicesById
                                                     └> statusesById
```

### 当前设备与按设备状态

文件：`packages/shared/shared_business/lib/device/application/providers/device_core_providers.dart`

```text
selectedDeviceProvider                         一份当前选中状态
deviceIdentityProvider(deviceId)               每个 deviceId 一份
deviceModuleProvider(DeviceCoreRef)            每个 deviceId + deviceType 一份
deviceWifiDetailProvider(deviceId)             每个 deviceId 一份
deviceSimAuthProvider(deviceId)                每个 deviceId 一份
```

`packages/shared/shared_business/lib/device/presentation/device_core_presentation.dart::activeDeviceCorePresentationProvider` watch 上述状态并合成 UI 友好的只读数据。

### 定位状态

文件：`packages/shared/shared_business/lib/location/application/providers/location_providers.dart`

```text
selectedDeviceProvider + deviceIdentityProvider
  -> selectedLocationDeviceProvider
  -> LocationDeviceRef?
       ├> deviceLocationSnapshotProvider(ref)
       ├> locationDeviceProfileProvider(deviceId)
       ├> locationCapabilitiesProvider(deviceId)
       ├> locationPresentationProvider(ref)
       ├> locationCommandProvider(ref)
       └> locationPromptProvider(ref)
```

展示聚合见 `packages/shared/shared_business/lib/location/presentation/location_presentation_provider.dart::activeLocationPresentationDataProvider`。

## 8. 混合状态不得遗漏

完整追踪还要搜索：

- Widget `setState`：分页 loading、tab、输入、动画等页面局部状态；
- `TQGlobalModel`、`TQInfoManager`、`MapSourceManager`、`TQScreenSecureManager` 等 Manager/单例；
- Controller、Timer、StreamSubscription 和插件 callback；
- Repository 之外的直接 `TQHttp.*`；
- SharedPreferences、文件缓存或数据库。

如果一条链同时写 Riverpod 和 Manager，要分别列出写入原因及消费者，不要声称 Manager 数据“也自动在 Provider 中”。

## 9. 实时拓扑扫描

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "final <provider名>|class <Notifier名>|class <State名>" apps packages --glob '*.dart'
rg -n "<provider名>\(|<provider名>\.notifier|invalidate\(<provider名>|refresh\(" apps packages --glob '*.dart'
rg -n "ref\.(read|watch|listen)|\.select\(" <相关文件> --glob '*.dart'
rg -n "operator ==|hashCode" <family-key文件>
rg -n "autoDispose|keepAlive|onDispose|dispose\(|requestVersion|generation|mounted" <Provider及Notifier文件>
rg -n "setState\(|Manager|Controller|TQHttp\." <同一需求目录> --glob '*.dart'
```

最终答案应把命中结果整理成“定义 → 参数来源 → 写入 → 保存 → 订阅/读取 → UI → 清理”，而不是粘贴搜索列表。
