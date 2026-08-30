# Riverpod：从参数身份到最终 UI 的前端对照

> 主入口见 [../SKILL.md](../SKILL.md)。项目事实地图可按需读取 `tuqiang-project-map` 的 Riverpod 拓扑；只有当前问题属于设备/定位领域时才读取对应业务链 reference。兄弟 Skill 不可用时直接在已验证的 `<TUQIANG_ROOT>` 中检索。依赖版本、符号和行号始终以本次源码为准。

## 1. 先识别当前项目的真实状态形态

先核对当前 `pubspec.yaml` 与 lockfile 中的 Riverpod 版本，再搜索实际声明；不要把历史扫描结果或通用教程当成当前事实。常见类型的前端心智近似如下：

| Riverpod 类型 | 常见职责 | Vue3 / React 近似 |
|---|---|---|
| `Provider<T>` | Repository/服务注入、派生状态、跨 Feature contract | `provide/inject`、computed、Context |
| `Provider.autoDispose.family` | 每个业务 key 一份只读组合值或 Controller | keyed computed / keyed selector |
| `StateNotifierProvider` | 显式 state + actions | Pinia/Zustand store |
| `StateNotifierProvider.family` | 每个 key 一份隔离的业务状态 | store factory / keyed store |
| `StateNotifierProvider.autoDispose.family` | 每个实体/查询 key 一份可释放状态 | keyed store + 自动释放策略 |
| `NotifierProvider.autoDispose.family` | Riverpod 2 Notifier 的 keyed store | keyed store factory |
| `FutureProvider.autoDispose.family` | 按 key 暴露一次异步结果 | keyed query / React Query |

表中只是帮助前端开发者入门的近似。最终答案要展示项目实际使用的 Provider 类型、完整泛型和版本，不能声称当前源码中不存在的类型或代码生成方式已经采用。

项目也可能混用 Manager/cache、全局 Model、Notifier 的公开可变字段、页面 `setState/ValueNotifier` 或插件状态。看到 Provider 后仍要继续找真正存储值与触发 UI 的载体。

## 2. `family(arg)` 为什么能传参数

第一次解释时可把 `.family` 类比为“以 key 保存多份 store/query 的 Map”：

```ts
Map<FamilyArgument, ProviderInstance>
```

Riverpod 的真实语义是：声明中的最后一个泛型（或 Notifier 的 `build(arg)`）定义参数类型；调用 `provider(arg)` 时，`arg` 被传给 builder/build，同时参与 Provider 实例的身份与缓存选择。

```dart
final detailProvider = StateNotifierProvider.autoDispose.family<
  DetailNotifier, // ref.read(provider(key).notifier) 的命令对象类型
  DetailState,    // ref.watch(provider(key)) 得到的响应式状态类型
  EntityRef       // family key 类型：决定选择哪一份实例
>((ref, key) => DetailNotifier(ref, key));
```

```dart
final key = EntityRef(id: entityId, category: category);
final state = ref.watch(detailProvider(key));
ref.read(detailProvider(key).notifier).refresh(force: true);
```

必须把四类参数拆开追踪：

| 参数 | 来源与作用 |
|---|---|
| 路由 `arguments` / Widget 属性 | 把页面上下文带到入口，不自动成为状态 key |
| family `key` | 决定 Provider 实例身份、状态隔离和缓存命中 |
| `refresh(force: true)` 等 action 参数 | 只控制这一次命令 |
| `DetailState.result` 等 State 字段 | 请求/计算后留存并供消费者读取的数据 |

### 相同 key 与不同 key

- 同一个 `ProviderContainer` 中，相等 key 通常选择同一实例；
- 不同 key 拥有互相隔离的 State/Notifier；
- 字符串、数字等按值参与相等判断；
- 复合实体引用、筛选条件、分页查询等对象 key 必须检查不可变性与 `==/hashCode`；
- 不稳定或每次都不相等的 key 可能造成实例抖动、重复请求或状态无法复用。

Vue keyed store 或 React query key 能辅助理解“按 key 分区”，但 Riverpod 还受 `ProviderScope`、依赖图、override 和 autoDispose 控制，不能把类比冒充完全等价。

## 3. `read/watch/listen/select` 看的是依赖关系

术语首次出现时先给前端心智，再说明真实语义：

```dart
final state = ref.watch(detailProvider(key));
final title = ref.watch(detailProvider(key).select((s) => s.title));
final notifier = ref.read(detailProvider(key).notifier);
ref.listen(detailProvider(key), (previous, next) { /* side effect */ });
```

| 写法 | Vue3 / React 心智 | Riverpod 真实语义 |
|---|---|---|
| `watch(provider)` | `computed` / `useSelector` | 建立响应式依赖，值变使当前 Widget/Provider 重算 |
| `watch(provider.select(...))` | selector | 只订阅投影结果；结果相等时减少无关重算 |
| `read(provider)` | 事件中读取 store 快照 | 取当前值，不建立后续响应式依赖 |
| `read(provider.notifier)` | 取 store actions/dispatch | 获取命令对象，本身不是订阅 State |
| `listen(provider)` | Vue `watch` / effect | 状态变化时执行导航、Toast、同步等副作用 |
| `invalidate(provider)` | 清除 keyed store/query 实例 | 丢弃准确 Provider 实例，并允许后续读取重新创建 |

不要套用“build 里只能 watch、按钮里只能 read”之类绝对口诀。应解释当前调用为什么需要订阅、快照、命令对象或副作用。

还要区分 Riverpod 的 `provider.select((state) => field)` 与项目 Notifier 中可能同名的 `select(model)` 业务 action。

## 4. Provider 被读取不等于自动发请求

检查构造函数或 `build(arg)` 是否真正触发 I/O。许多 Notifier 只保存 key，需要由 Host、RouteObserver、页面首次加载、listener 或按钮显式调用 `.refresh()`。

```text
provider(key) 被 watch/read
  ≠ 一定发请求

某个真实触发点
  → provider(key).notifier.refresh()
  → Repository/HTTP/缓存/插件
  → state = ...
  → 订阅者更新
```

讲解时必须把“实例创建”和“业务请求触发”分成两跳，并分别给出调用处源码。

## 5. 状态定义、全部写入源与字段血缘

对影响最终 UI 的每个字段建立身份卡：

| 字段 | 初始值 | 谁写 | 写入条件 | 谁读 | UI 含义 |
|---|---|---|---|---|---|
| `isRefreshing` | `false` | Notifier | 请求开始/结束 | loading 组件 | 后台刷新中 |
| `result` | `null` | 请求、缓存回填、推送/轮询 | 新结果到达 | Presentation Provider | 当前业务数据 |

全仓搜索全部相关写入源，尤其注意：

- 同一状态可能由首次加载、批量请求、当前实体请求、手动刷新、推送或轮询共同写入；
- 真实值可能写在 Manager/cache，Riverpod State 只增加 `revision` 触发重算；
- 页面可能 watch State，却从 Notifier 的公开可变字段取列表；
- `setState` 与 `ValueNotifier` 只影响页面局部 UI，不会自动写入 Provider。

设备/GPS 是多 key、多写入源的一种领域案例。只有当前需求属于该领域时才展开它，不能把其 Provider、Host 或生命周期结论泛化到其他模块。

## 6. 派生 Provider 与最终展示

一个通用拓扑可能是：

```text
selectedEntityProvider
  + entityIdentityProvider(entityId)
  → selectedDomainEntityProvider
  → domainSnapshotProvider(EntityRef)
  + profile/capabilities
  → activePresentationDataProvider
  → Feature 页面 ref.watch/select
  → Text / Switch / List / Map
```

对每个派生 Provider 列出它 `watch` 的上游、输出的 ViewModel/展示字段，以及哪个 Widget 消费哪个字段。仅说“Provider 自动刷新页面”不够；必须说明是哪一次 State 写入导致哪个依赖重新计算，并区分 `ref.listen` 副作用与 Widget 重建。

## 7. `autoDispose`、长期订阅与清理

`autoDispose` 的准确含义是“实例无人监听后具备被释放的条件”，不是“页面 pop 就必定清空”。检查：

1. 页面之外是否有根 Host/Coordinator 仍在 watch/listen 当前 key；
2. 是否调用 `ref.keepAlive()`；
3. 是否注册 `ref.onDispose` 清理 Timer、Controller、subscription 或插件；
4. 切 key 后旧实例是否失去订阅或被显式 invalidate；
5. 登出/session reset 是否集中 invalidate；
6. 异步返回前是否检查 `mounted`、generation/operation，避免旧结果覆盖新状态。

某些常驻 App Host 可能持续订阅当前 key 的多组 `autoDispose.family`，使页面离开后状态仍然存活。必须由当前源码证明该长期订阅，不得复用其他业务链的结论。

## 8. `ProviderScope` override 是跨 Feature 接线

第一次出现时可类比 Vue `app.provide` 或 React 根 Context Provider；Riverpod 的真实链路仍要找齐三处：

```text
Feature 声明 Provider<Contract>
  → App composition root 用 overrideWithValue 注入实现
  → Feature 内 ref.read(contractProvider).openXxx()
```

如果缺少其中任何一处，用户仍无法理解“抽象从哪里获得具体实现”。

## 9. Vue3 端到端等价实现要求

```ts
type State = { refreshing: boolean; result?: EntityDetail }
const stores = new Map<string, ReturnType<typeof createEntityStore>>()

function useEntityStore(entityId: string) {
  if (!stores.has(entityId)) {
    const state = reactive<State>({ refreshing: false })
    const refresh = async () => {
      state.refreshing = true
      try { state.result = await repository.fetchDetail(entityId) }
      finally { state.refreshing = false }
    }
    stores.set(entityId, { state, refresh })
  }
  return stores.get(entityId)!
}

const activeDetail = computed(() =>
  selectedId.value ? useEntityStore(selectedId.value).state.result : undefined,
)
```

这是心智示例，不是可直接粘贴的固定答案。真实讲解要替换成当前 Dart 链路中的 route/props、family key、Repository、State 字段和 UI 名称，并补齐用户事件、loading/error/empty、`watch` 副作用、模板消费以及卸载/切 key 清理。

## 10. React 端到端等价实现要求

```tsx
function DetailPanel({ entityId }: { entityId: string }) {
  const query = useQuery({
    queryKey: ['entity-detail', entityId],
    queryFn: ({ signal }) => repository.fetchDetail(entityId, signal),
  })

  if (query.isLoading) return <Spinner />
  return <span>{query.data?.title}</span>
}
```

`queryKey` 能辅助理解 family 身份，但 StateNotifier family 还可能包含 actions、多写入源和显式 State，不应一概翻译成 React Query。真实讲解必须补齐当前业务的操作入口、route/props、状态写入、selector/effect、最终组件及 cleanup/取消。

## 11. 回答检查单

- [ ] 当前 Riverpod 版本和真实 Provider 类型是否已从源码核验？
- [ ] 完整泛型每一项是否解释？
- [ ] family key 从哪里得到、为何包含这些字段、相等性在哪里？
- [ ] Provider 构造是否真的发请求，真正触发点是谁？
- [ ] route/family/action 参数和 State 字段是否区分？
- [ ] 全部相关写入源和最终消费者是否列出？
- [ ] `watch/read/listen/select` 是否按当前语义解释？
- [ ] `autoDispose` 是否检查长期订阅、keepAlive、invalidate、cleanup 与 reset？
- [ ] 是否追到 Manager/cache/setState/ValueNotifier 等旁路？
- [ ] Vue3/React 代码是否覆盖当前完整业务链，而不是复用通用片段？
