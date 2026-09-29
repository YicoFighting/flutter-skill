# Tuqiang 完整需求追踪

用于用户要求端到端说明，或局部证据不足以解释故障时。普通 owner、取值或路由问题在关键证据明确后结束，不套用完整报告。

先明确本次操作和可观察结果，再沿实际经过的阶段调查：

| 阶段 | 需要找到的证据 |
|---|---|
| 入口与页面 | 用户事件/生命周期/原生回调、route 参数、最终 builder；分栏时区分 master 与 detail |
| 状态身份 | 实际 Provider/Manager/Controller，key/account scope，写入与消费 |
| 数据边界 | Repository/HTTP/cache/plugin、请求输入与响应映射 |
| 异步发布 | loading/success/empty/error、旧结果判断、pending 与缓存回写 |
| 可观察终点 | 展示字段、可见性、按钮或地图/原生参数及其 mapper |
| 清理与恢复 | 页面退出、切 key、dispose、账号切换或语言切换中与问题有关的清理 |

有异步时分清“同步事件 → 调度 → 异步返回 → 响应式消费”，不能把 `onTap → network → UI` 当作完整证据；mounted 不能证明结果仍属于当前账号或设备。

## 控制调查范围

- 账号差异读 [账号模式](account-mode.md)；只在结论依赖模式时展开两侧与切换。
- 设备/地图差异读 [变体](variant-surface.md)；追问题可达的 route leaf，公共分派改动才反查全部调用者。
- 展示值与 fallback 读 [国际化与展示取值](../../tuqiang-dev/references/i18n.md)；复用入口与纯函数边界读 [本地封装](../../tuqiang-dev/references/local-style-and-reuse.md)。
- `rg -n` 优先限定已知 owner、route 或 symbol；只有当前链确实跨包时扩大搜索。

输出按因果顺序解释关键跳，并引用当前路径、行号、symbol。表格或时间线只在能解释问题时使用；无需逐项输出“不涉及”。当入口、行为原因和终点已由证据连接，且影响结论的分支已查明，就停止。未能确认的事实如实标注，不用迁移目标或默认模式补空白。
