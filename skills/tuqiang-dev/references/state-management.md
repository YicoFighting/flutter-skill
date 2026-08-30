# 状态管理规范（Riverpod 2.6.1）

最近扫描基线使用 `flutter_riverpod` / `riverpod` 2.6.1；每次修改前先核对当前 `pubspec.yaml` 与 lockfile。基线源码以手写 `Provider`、`StateNotifierProvider`、family/autoDispose 为主，少量使用 `NotifierProvider.autoDispose.family` 与 `FutureProvider.autoDispose.family`；未发现 Riverpod codegen。新增或修改代码先沿用 owner 模块的成熟模式，不做无关 API 迁移。

项目不是纯 Riverpod：Manager/单例、Notifier 公开可变字段、页面 `setState`、`ValueNotifier`、Timer、`ProviderContainer`、直接 `TQHttp` 和插件状态仍然存在。诊断或修改时必须沿真实数据载体追踪。

项目级 Provider 图与设备示例见：

- [Riverpod 拓扑](../../tuqiang-project-map/references/riverpod-topology.md)
- [设备目录、选择与定位状态链](../../tuqiang-project-map/references/device-location-flow.md)

## 1. 修改前画 Provider 影响图

对每个相关 Provider 记录：

```text
声明与完整泛型
→ family key 来源与值相等性
→ State / Notifier 初始状态
→ 依赖的 Provider / Repository
→ 真正的请求或命令触发点
→ 所有 state/seed/apply/cache 写入源
→ watch/select/read/listen 消费端
→ derived/presentation Provider
→ 最终 UI/副作用
→ autoDispose/keepAlive/invalidate/session reset
```

选中的文件只是入口。改 State 字段、family key、生命周期或 Repository 前要全仓搜索声明、实例化、`.notifier` 调用、状态写入、`ProviderContainer` 访问和 reset participant。

## 2. 选择 Provider 类型

| 类型 | 当前项目用途 | 变更原则 |
|---|---|---|
| `Provider<T>` | Repository/服务 DI、派生状态、Navigator/Composition contract | 不要把所有 Provider 当成 store |
| `Provider.autoDispose.family` | 每个设备一份只读值或 Controller | 关注 key 与资源释放 |
| `StateNotifierProvider` | 设备目录、当前设备、消息等显式 state/actions | 存量模块优先沿用 |
| `StateNotifierProvider.family` | 按 key 隔离的长期业务状态 | 检查会话清理 |
| `StateNotifierProvider.autoDispose.family` | 设备详情、定位、轨迹、视频等 | 检查真实监听者，不假定页面退出即销毁 |
| `NotifierProvider.autoDispose.family` | 少量新 Notifier，如配网/下载队列 | 沿用所在模块，不为统一改写存量 |
| `FutureProvider.autoDispose.family` | 少量无复杂命令的一次查询 | UI 直接处理 `AsyncValue` |

当前扫描未发现 `StateProvider`、`StreamProvider`、`AsyncNotifierProvider`、`ChangeNotifierProvider` 或 `@riverpod`。新需求只有在数据模型确实匹配、所在 owner 接受且三端依赖可用时才引入，不以“Riverpod 有这个 API”为理由增加模式。

## 3. family 是状态实例身份

```dart
final snapshotProvider = StateNotifierProvider.autoDispose.family<
  SnapshotNotifier,
  SnapshotState,
  LocationDeviceRef
>((ref, key) => SnapshotNotifier(ref, key));
```

三项泛型分别是 Notifier、`ref.watch` 返回的 State、Provider 实例 key。`snapshotProvider(key)` 不是给一份全局状态临时传参，而是按 key 选择/创建实例：

- 同一个 `ProviderContainer` 中，相等 key 复用同一实例；
- 不同 key 的 State/Notifier 隔离；
- 对象 key 应不可变并按业务字段实现稳定 `==/hashCode`；
- key 字段变化可能创建全新状态，修改 key 结构是行为变更；
- Provider 构造不一定发请求，必须找到显式 `.refresh/load/request` 触发点。

必须区分：

| 参数 | 含义 |
|---|---|
| route arguments | 页面导航上下文 |
| family key | Provider 实例/缓存身份 |
| Notifier 方法参数 | 单次 action 的选项，如 `force` |
| State 字段 | 持久到下一次状态替换的 UI/业务数据 |

修改 `DeviceCoreRef`、`LocationDeviceRef`、`VideoDeviceRef`、`TraceQuery` 等 key 前，检查所有构造点、测试和 key 相等性；不得把可变 List/Model 直接塞进 key 而不稳定冻结或比较。

## 4. StateNotifier 存量模式

```dart
@immutable
class BeaconState {
  const BeaconState({
    this.loading = false,
    this.items = const <TqBeaconItemModel>[],
  });

  final bool loading;
  final List<TqBeaconItemModel> items;
}

class BeaconController extends StateNotifier<BeaconState> {
  BeaconController(this.repository) : super(const BeaconState());

  final BeaconRepository repository;
  int _generation = 0;

  Future<void> load() async {
    final generation = ++_generation;
    state = BeaconState(loading: true, items: state.items);
    final result = await repository.fetch();
    if (!mounted || generation != _generation) return;
    state = BeaconState(loading: false, items: result);
  }
}
```

State 应保持不可变，集合对外避免被静默修改；是否需要 `copyWith`、深拷贝或 freezed 服从模块现状。不要用 `toJson/fromJson` 反复深拷贝可变 Model，这可能丢字段、类型或对象身份。

异步必须评估：

- 旧响应是否会覆盖新 key/新筛选条件；
- 相同 in-flight 请求是否需要合并；
- Notifier 销毁后回调是否检查 `mounted`；
- Timer/Subscription/Controller 是否在 dispose 取消；
- generation/operation/request id 是否在 invalidate 或切设备时失效；
- error/empty/loading 是否回到可观察状态，不能永久卡 loading。

## 5. Widget 与 Provider 接线

```dart
class BeaconPage extends ConsumerWidget {
  const BeaconPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(beaconProvider);
    final controller = ref.read(beaconProvider.notifier);
    return BeaconView(state: state, onReload: controller.load);
  }
}
```

- `watch`：渲染或派生状态的响应式依赖；
- `watch(provider.select(...))`：只订阅投影字段，避免无关重建；
- `read`：一次性快照或获取 Notifier；在 `build` 中只读取稳定 Notifier 并绑定事件可以合理；
- `listen`：Toast、导航、loading overlay、缓存同步等副作用；
- `invalidate`：丢弃实例并让后续读取重建，不只是普通 refetch；
- `ProviderContainer.read/listen`：常见于 RouteObserver/Coordinator，要纳入调用链与清理检查。

禁止在 `build` 中直接执行会同步写 Provider 的命令。`initState` 是否需要 post-frame 取决于动作是否在 Widget 树建立阶段同步修改被监听 Provider；可以使用 provider 自身初始化、`ref.listen`、`addPostFrameCallback` 或幂等首次加载，不能机械给所有请求包 post-frame。

## 6. 多写入源与混合状态

改一个 State 前不要只搜 `state =`。还要检查：

```text
.notifier).方法
seed / apply / update / refresh
ProviderScope override callback
Manager/cache/database 写入
setState / ValueNotifier
RouteObserver / Timer / plugin callback
Notifier 公开可变字段
```

代表性风险：

- 设备定位 snapshot 可由目录批量状态、当前设备定向刷新、远程命令轮询共同回填；
- 地址可能实际存入 `TQReGeoCacheManager`，Provider State 只用 revision 通知重建；
- 设备目录 UI 可能订阅 `DeviceCatalogState`，但列表仍读 Notifier 的 `infoModel`；
- 修改 Riverpod State 不代表 Manager、插件或页面局部副本自动同步。

如果不得不维持混合写法，应明确唯一 source of truth、同步方向和退出清理；不要顺手做大规模状态迁移。

## 7. autoDispose、保活与销毁

`autoDispose` 只表示无人监听后允许释放。判断实际生命周期时检查：

1. 根 Host/Coordinator 是否在 App 生命周期内持续 watch 当前 key；
2. RouteObserver 是否通过 `ProviderContainer` 继续持有或触发；
3. 是否调用 `ref.keepAlive()`，何时关闭 link；
4. `ref.onDispose` 是否释放 Timer、P2P/视频 Controller、Subscription；
5. 切 key 时旧 family 是否失去订阅或被显式 invalidate；
6. 非 autoDispose 或 keepAlive 状态是否进入 session reset。

定位链由根 `LocationContainerHost` 持续订阅当前设备的 snapshot/profile/capabilities/presentation/command 等 family，所以离开 GPS 页面并不必然销毁。切设备、显式 invalidate 或登出才是关键清理点。明确使用 `ref.keepAlive` 的代表是下载队列，不要假设所有 autoDispose 状态都被 keepAlive。

## 8. ProviderScope override 与跨 Feature 边界

跨 Feature contract 的正确方向：

```text
Feature 定义 Provider<Contract>
  ← apps/tuqiang_app bootstrap 通过 override 注入实现
  ← Feature 内 ref.read(contractProvider) 调用
```

修改时同时检查：

- contract 声明与默认行为；
- `ProviderScope(overrides: ...)` 的装配；
- Standard/OHOS 是否走同一 composition root；
- callback 是否捕获过期 context/state；
- 被调用 Feature 的 route、返回值、screen secure 与 route effect。

Feature 不应为了调用方便直接 import 另一个 Feature 的私有实现。

## 9. Session reset

新增非 autoDispose、用户级、设备级或 keepAlive 状态时，检查：

```text
apps/tuqiang_app/lib/app/session/session_reset_registry.dart
apps/tuqiang_app/lib/app/session/session_state_coordinator.dart
```

Feature 可以公开 reset participant，由 app 聚合；不得反向依赖 app。全局单例、下载队列、数据库/缓存与 Riverpod 可能需要不同顺序清理，先沿现有 coordinator 扩展。

最低行为用例：用户 A 产生状态 → 退出 → 用户 B 登录 → 不出现 A 的设备、消息、地址、下载或筛选缓存。

切语言也可能清理设备/GPS/广告等带翻译的缓存；相关逻辑检查 language change coordinator，避免只重建 Widget 却保留旧语言派生值。

## 10. 测试与验证

- family：相等 key 共享、不同 key 隔离、key 切换、构造是否自动请求；
- Notifier：初始、成功、失败、空数据、并发、旧响应丢弃、销毁后回调；
- autoDispose：无监听释放、根 Host 保活、keepAlive 关闭、onDispose 清理；
- 多写入源：目录回填、定向请求、轮询/推送的优先级与竞态；
- override：fake Repository/Contract 注入，Standard/OHOS composition 不缺失；
- session：用户切换与切语言无陈旧数据；
- Widget：loading/empty/error/content、字段级重建、按钮、导航和副作用；
- 公共状态改动：相关测试 + standard/OHOS analyze + boundary，必要时 migration tests。
