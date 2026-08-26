# 状态管理规范（Riverpod 2.6.1）

途强使用 `flutter_riverpod` / `riverpod` 2.6.1。存量业务以 `StateNotifierProvider` 为主，但已有 `NotifierProvider`、`FutureProvider` 等实现。新增或修改代码先沿用所在模块的模式，不为追求统一而做无关迁移。

## 1. 选择 Provider 类型

- 页面级、需要显式 Controller 的存量功能：沿用 `StateNotifierProvider`；
- 新增简单的读写状态：可评估 Riverpod 2 `NotifierProvider`；
- 只读同步依赖或配置：`Provider`；
- 单一异步查询且不需要复杂命令：`FutureProvider`；
- 持续数据流：`StreamProvider`；
- 页面离开即失效：通常使用 `autoDispose`；
- 跨页面且属于用户会话的数据：由 session reset 机制清理。

不要在同一功能内无理由混用两套状态模型，也不要因为类型名称像 Pinia store 就忽略 Provider 的作用域和销毁时机。

## 2. StateNotifier 存量模式

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

  Future<void> load() async {
    state = BeaconState(loading: true, items: state.items);
    final result = await repository.fetch();
    if (!mounted) return;
    state = BeaconState(loading: false, items: result);
  }
}
```

State 应保持不可变、字段通常为 `final`，集合对外暴露不可修改视图；是否需要 `copyWith`、深拷贝或 freezed 由模块现有风格决定。不要为了“不可变”反复 `toJson/fromJson` 深拷贝可变模型，这可能丢失字段、类型或对象身份。

异步请求可能并发时，用 generation、请求 id 或取消机制防止旧响应覆盖新响应：

```dart
final generation = ++_generation;
final result = await repository.fetch();
if (!mounted || generation != _generation) return;
state = state.copyWith(data: result);
```

## 3. Widget 接线

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

- `watch` 用于需要响应变化的 UI；
- `read` 用于事件回调、读取 controller 或一次性依赖；在 build 中 read controller 本身是合理的，不能把它误说成“build 禁止 read”；
- `select` 用于只订阅 State 的一个字段；
- `listen` 用于 toast、跳转等副作用，不代替 UI 渲染。

## 4. 生命周期

- Widget 跨 `await` 更新 UI 或使用 context 前检查 Widget 自身的 `mounted`；
- StateNotifier/Notifier 回调检查的是 provider 实例自身的生命周期；
- 不在 `build` 中同步修改 Provider；
- `initState` 是否需要 post-frame 取决于初始化动作。若会同步修改当前 build 中正在监听的 Provider，使用 post-frame、provider 初始化或 `ref.listen`，并避免重复请求；不是所有初始化都必须机械包一层 `addPostFrameCallback`；
- Controller、TextEditingController、FocusNode、TabController、StreamSubscription 等由 Widget 创建的资源在 `dispose` 释放。

## 5. 登录态重置

新增非 `autoDispose`、包含用户数据或会话缓存的 Provider 时，检查
`apps/tuqiang_app/lib/app/session/session_reset_registry.dart`。feature 可提供自己的 participants，由 app 聚合；不要把 feature 直接反向依赖 app。

退出登录后的验证至少覆盖：用户 A 产生数据 → 退出 → 用户 B 登录 → 不应看到 A 的缓存。全局单例与 Riverpod 并存时，先确认已有 coordinator 的清理路径，避免重复实现。

## 6. 测试与验证

- StateNotifier/Notifier：成功、失败、空数据、并发、销毁后回调；
- Provider：作用域、autoDispose、override 和 session reset；
- Widget：用户可观察的 loading/empty/error/content、按钮和导航；
- 公共状态或 session 变化：standard/OHOS analyze，并按 [testing.md](testing.md) 选择 migration/contract test。
