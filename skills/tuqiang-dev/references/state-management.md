# 状态管理规范（Riverpod 2.x）

项目状态管理统一用 **flutter_riverpod 2.6.1**（`StateNotifier` 风格，不是 hooks、不是新 API）。Vue3 类比：Provider ≈ Pinia store；`ref.watch` ≈ computed 响应式绑定。

## 1. 三板斧模板（State + Controller + Provider）

### 第一步：不可变 State

```dart
// controller/beacon/tq_my_beacon_controller.dart
import 'package:flutter/material.dart';

@immutable
class MyBeaconState {
  MyBeaconState({
    this.bluetoothUpperLimit = 0,
    List<TqBeaconItemModel> beacons = const <TqBeaconItemModel>[],
  }) : beacons = List<TqBeaconItemModel>.unmodifiable(
         beacons.map((item) => TqBeaconItemModel.fromJson(item.toJson())),
       );

  final int bluetoothUpperLimit;
  final List<TqBeaconItemModel> beacons;
}
```

规则：

- 字段全 `final`，类加 `@immutable`；
- 列表字段必须 `List.unmodifiable(...)` 包一层，防止外部改内部数据；
- 需要「部分更新」时在 State 上加 `copyWith`（存量部分页面靠重建对象，跟随所在模块现状即可）。

### 第二步：Controller

```dart
class TQMyBeaconController extends StateNotifier<MyBeaconState> {
  TQMyBeaconController() : super(MyBeaconState());

  /// 请求信标列表数据，并刷新UI
  Future<void> requestBeaconList({bool showLoading = false}) async {
    final generation = ++_beaconListGeneration;      // 竞态保护
    var result = await TQHttp.postWithConfig(
      TQAddress.getMyBeacons, params: {...},
      showLoading: showLoading, showErrorToast: true,
    );
    if (!mounted || generation != _beaconListGeneration) return;  // 销毁或过期直接丢弃
    if (result.success) {
      final list = TCheck<List>(result.data) ?? [];
      _beaconList = list.map((e) => TqBeaconItemModel.fromJson(e)).toList();
      _publish();                                    // 组装新 State 并 update
    }
  }

  void _publish() {
    state = MyBeaconState(
      bluetoothUpperLimit: _bluetoothUpperLimit,
      beacons: _beaconList,
    );
  }
}
```

规则：

- 改状态的唯一方式是给 `state` 赋一个**新的** State 对象；
- 异步回调里第一件事检查 `if (!mounted) return;`；
- 连续触发同一请求的场景用 generation 计数防旧响应覆盖新响应；
- UI 事件方法可以带 `BuildContext`（如弹窗跳转），但网络逻辑不要依赖 context。

### 第三步：Provider 注册

```dart
// state/beacon/my_beacon_provider.dart
import 'package:riverpod/riverpod.dart';
import '../../controller/beacon/tq_my_beacon_controller.dart';

final myBeaconProvider =
    StateNotifierProvider.autoDispose<TQMyBeaconController, MyBeaconState>(
      (ref) => TQMyBeaconController(),
    );
```

- 页面级状态：`autoDispose`（离开页面自动释放）。
- 全局/跨页共享状态（如设备目录 `deviceCatalogProvider`）：不加 autoDispose，由 session 重置统一清理。
- 文件放 feature 包 `src/state/` 下，一个 provider 一个文件或按域合并均可，跟随模块现状。

## 2. 页面接线模式【标准写法】

外层薄壳 ConsumerWidget + 内层纯展示 View（范例 `tq_my_beacon.dart`）：

```dart
class TQMyBeacon extends ConsumerWidget {
  const TQMyBeacon({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return _TQMyBeaconView(
      state: ref.watch(myBeaconProvider),                    // 订阅 → 自动刷新
      controller: ref.read(myBeaconProvider.notifier),       // 取实例调方法
    );
  }
}

class _TQMyBeaconView extends StatelessWidget {
  const _TQMyBeaconView({required this.state, required this.controller});

  final MyBeaconState state;
  final TQMyBeaconController controller;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: TQAppBar(title: '我的信标'.tr),
      body: ListView.builder(
        itemCount: state.beacons.length,
        itemBuilder: (_, i) => TQBeaconItemWidget(
          item: state.beacons[i],
          onTap: () => controller.onBeaconTap(context, state.beacons[i]),
        ),
      ),
    );
  }
}
```

要点：

- **watch 只出现在最外层壳**，内层 View 是普通 StatelessWidget，便于复用和测试；
- **局部精细监听（Riverpod 性能优化）**：若页面或子组件只关心 State 中的某一个字段，使用 `select` 避免无关字段变化触发整页重绘：
  ```dart
  // 只有 upperLimit 改变时才触发此组件 build
  final limit = ref.watch(myBeaconProvider.select((s) => s.bluetoothUpperLimit));
  ```
- 需要局部监听副作用（toast/跳转）时用 `ref.listen(provider, (prev, next) {...})`；
- **资源成对释放规范（防内存泄露）**：
  若页面使用 `ConsumerStatefulWidget`，所有在 `initState` 或属性中创建的资源必须在 `dispose` 中显式释放：
  ```dart
  @override
  void dispose() {
    _textController.dispose();
    _focusNode.dispose();
    _tabController.dispose();
    _streamSubscription?.cancel();
    super.dispose();
  }
  ```
- 读一次不订阅用 `ref.read`；禁止在 build 里用 read 订阅数据。

## 3. 状态分发与穷尽匹配（Pattern Matching）

处理复杂请求状态（加载中/成功/失败/空数据）或业务状态分支时，推荐用 Dart 3 Switch 表达式保证**穷尽匹配**，杜绝漏写状态导致界面卡死。空态用现成的 `TQNoDataWidget`（注意 `tipStr` 是必填参数）：

```dart
Widget _buildBody(BuildContext context) {
  return switch (status) {
    PageStatus.loading => const EightRectLoading(),          // core_ui 加载动画
    PageStatus.empty   => const TQNoDataWidget(tipStr: ''),  // core_ui 空态
    PageStatus.error   => TQNoDataWidget(tipStr: '加载失败，请重试'.tr),
    PageStatus.success => _buildContent(context),
  };
}
```

## 4. 登录态重置【容易漏，必做】

换账号/退出登录时所有全局缓存必须清空。机制：`apps/tuqiang_app/lib/app/session/session_reset_registry.dart` 汇总各 feature 的 participants。

feature 包内提供：

```dart
// src/session/feature_xxx_session_resetters.dart
class FeatureXxxSessionResetters {
  static final participants = <SessionResetParticipant>[
    SessionResetParticipant(
      name: 'xxx',
      actions: [
        (container) => container.invalidate(myXxxGlobalProvider),
      ],
    ),
  ];
}
```

然后在 app 的 `defaultSessionResetParticipants` 里追加 `...FeatureXxxSessionResetters.participants`。
**新增任何非 autoDispose 的全局 provider 都必须注册**，否则会出现 A 用户数据泄露给 B 用户的事故。

## 5. 全局单例并存说明

项目仍有少量静态单例（`TQGlobalModel.shared`、`TQI18nManager` 等）与新 Riverpod 并存。规则：

- 新代码一律走 Riverpod；
- 不要在 Provider 外部随手读全局单例再缓存到变量；
- 语言切换等会引发大面积缓存的动作已有 `LanguageChangeCoordinator.clearCache` 统一处理，别自己另写一套。

## 6. 验证方式

```powershell
dart run tool/project.dart analyze standard
```

涉及全局 provider 的改动，额外自测：登录 → 操作 → 退出 → 换账号登录，确认无残留数据。
