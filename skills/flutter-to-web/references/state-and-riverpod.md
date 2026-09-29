# Tuqiang 状态与 Riverpod

先识别目标代码的真实载体：Provider/Notifier、Widget State、Manager、Controller、ValueNotifier、cache 或 plugin callback，不把它们统称为一份 store。

围绕问题核验所需维度：定义、实例身份、依赖、写入、消费、生命周期。只有实例隔离或清理影响结论时，才展开 Container、family key、account/device/session、autoDispose/keepAlive 与 reset；不要求完整状态卡。

## 容易混淆的语义

- family(arg) 用参数身份选择实例，不是给全局 State 临时传参；检查当前参数类型的相等性规则。
- watch 建立响应依赖，read 不持续订阅，select 关注选中的值，listen 用于副作用。以当前依赖版本和调用位置解释具体行为。
- Provider 创建不等于发请求；请求可能来自 build、load、listener、页面事件或 composition callback。
- 状态写入后仍需找到实际 watch/select/listener，才能解释 UI 为什么更新；Manager/cache 还可能有桥接通知。
- autoDispose 不保证离页立即销毁；其他监听和 keepAlive 可能延长寿命。忽略旧状态发布也不等于取消底层请求。

需要解释账号隔离时读取 [账号模式](../../tuqiang-project-map/references/account-mode.md)；生命周期、旧结果和资源释放统一读取 [异步生命周期](../../tuqiang-dev/references/async-lifecycle.md)。不在本文件固化某一 Riverpod 版本的实现细节。

需要建议状态写法时，先核验 [本地风格与复用](../../tuqiang-dev/references/local-style-and-reuse.md)，说明项目已有 owner 与封装；不得仅因熟悉某种状态库而推荐替换。

## Web 心智

| Flutter | Web 近似 |
|---|---|
| Provider.family(key) | keyed composable/store/query |
| Notifier/StateNotifier | store action owner |
| watch(select) | computed/store selector |
| listen | watch/effect/subscription |
| ProviderScope override | provide/Context 组合根 |

类比辅助理解，结论由当前声明、写入与消费证据支持。更复杂的项目拓扑见 [Riverpod 拓扑](../../tuqiang-project-map/references/riverpod-topology.md)。
