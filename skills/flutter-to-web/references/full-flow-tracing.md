# 跨文件业务链追踪

用于用户要求完整流程，或必须跨文件才能解释的行为。单个字段、函数或组件问题无需展开所有维度。

从用户给定的入口或 symbol 开始，围绕问题沿上下游取证：谁触发、参数从哪来、实际实现是谁、数据在哪转换/写入、最终谁消费。只有并发写入、账号/设备切换或退出影响结论时，再追旁路和清理。

涉及异步或响应式更新时，区分：

    事件：操作/生命周期 → Widget callback → command
    数据：输入 → HTTP/cache/plugin → Model/错误 → State
    更新：状态通知/派生 → build/listener → UI/副作用

这些是分析维度，不是每次必交的三个图。await、listener、post-frame 与 rebuild 要说明触发关系，不能连成同步栈。

## 关键证据

- route、contract provider、callback 或 barrel 不能替代实际 builder/override/实现。
- 状态身份仅追影响当前行为的 family key、account/device/session 和 reset；路由参数、action 参数与持久 State 分开讲。
- 字段问题沿“来源 → Model/mapper → 消费者”追一次。fallback、空值和展示兼容统一参考 [国际化与展示边界](../../tuqiang-dev/references/i18n.md)，指出当前由谁负责，避免建议在多层重复处理。
- 要解释“为什么采用这种实现”时，先核验现有 owner 和封装，参考 [本地风格与复用](../../tuqiang-dev/references/local-style-and-reuse.md)。
- 账号模式确实改变此链时才展开分流，依据 [账号模式事实](../../tuqiang-project-map/references/account-mode.md)；声称两种账号都成立必须有两侧证据。

检索优先从相关 owner 目录的精确 symbol 与引用开始，必要时扩大到 route、数据边界和最终消费。用当前路径与行号支持关键因果，未知的后端或插件内部行为写清停止点。

输出先给业务结论，再解释必要的链和证据。Web 对照按用户指定框架给出；完整示例才需要逐段对应操作、参数、请求、状态、UI 和清理。
