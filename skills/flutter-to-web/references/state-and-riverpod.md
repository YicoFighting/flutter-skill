# Tuqiang 状态与 Riverpod

先识别真实载体：Provider/StateNotifier/Notifier、Widget setState、Manager/单例、Controller、ValueNotifier、cache 或 plugin callback。不要把它们统称为一份 store。

## 状态身份卡

| 问题 | 必须说明 |
|---|---|
| 定义 | Provider、State、Notifier/Controller 的完整类型 |
| 身份 | Container、family key、账号/device/session scope 与 ==/hashCode |
| 依赖 | read/watch/listen/select 的具体对象 |
| 写入 | 初值、请求、Manager/cache 旁路及全部相关 setter |
| 消费 | Widget/listener 使用的字段和重建条件 |
| 生命周期 | autoDispose/keepAlive、invalidate/reset、资源清理与旧结果淘汰 |

family(arg) 以相等 arg 选择实例，不是给全局 State 临时传参。route 参数、family key、action 参数、State 字段和 accountMode 分开讲。

## 依赖语义

- watch 建立响应依赖；read 是快照或命令入口，不持续订阅。
- select 只在选中字段变化时通知；必须说清字段。
- listen 触发副作用而非渲染。Widget listen 只在 build，其他生命周期用 listenManual；外部 ProviderContainer.listen 由外部 owner 关闭。
- Provider 实例创建不等于发请求；请求可能来自 build、显式 load、listener、页面事件或 composition callback。
- invalidate 一个 family 实例与整个 family 的范围不同；结合监听、autoDispose 和 Notifier 类型解释重算/释放。

## 发布与 UI

从 state 写入继续追 copyWith/setter、notify、派生 Provider/presentation mapper、watch/select 和最终字段。说明 loading/error/empty、重复值是否通知、Manager/cache 如何桥接，以及一次 UI 刷新究竟由谁触发。

账号模式改变数据时，family/cache identity 或 reset 必须隔离 personal/enterprise。只有 deviceId 的 key 未必够；读取 [账号模式事实](../../tuqiang-project-map/references/account-mode.md) 核验。

## 生命周期边界

- autoDispose 不是“页面退出必销毁”；其他监听或 KeepAliveLink 会延长寿命。
- Riverpod 2.6.1 Notifier 可能跨重算复用，每轮 build/onDispose 需要新的 lifecycle epoch；一次 _disposed=true 不能永久沿用。
- FutureProvider 会忽略已销毁实例的状态发布，但不会取消底层 Future/HTTP。
- read(autoDispose.notifier).load() 不保活。
- WidgetRef 在 unmount 后不可用；Widget 生命周期不得同步写 Provider。

更完整的项目拓扑读项目地图的 [Riverpod 拓扑](../../tuqiang-project-map/references/riverpod-topology.md)；实现门禁读 tuqiang-dev 的 [异步生命周期](../../tuqiang-dev/references/async-lifecycle.md)。

## Web 心智

| Flutter | Web 近似 |
|---|---|
| Provider.family(key) | keyed composable/store/query |
| StateNotifier/Notifier | reducer/store action owner |
| watch(select) | computed/store selector |
| listen | watch/effect/subscription |
| ProviderScope override | provide/Context 组合根 |
| autoDispose/keepAlive | subscription 生命周期/cache retention |

类比只辅助理解；最终以当前 Dart 声明、写入、消费和清理证据为准。
