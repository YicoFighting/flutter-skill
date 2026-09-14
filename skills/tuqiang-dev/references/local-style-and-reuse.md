# 局部风格与复用

目标是在真实 Tuqiang owner 中选择成熟样本和最小抽象，不用模型偏好的统一架构覆盖存量。

## 采样

1. 沿入口、route、Provider/Controller/Manager、Repository、asset 和测试确定 owner。
2. 检查公开 barrel/API 与真实调用方；包外不 import 其他 package 的私有 src。
3. 局部修改优先延续当前实现；需要新模式时先选一个操作、生命周期、accountMode 和平台边界直接可比的同 owner 样本。确有差异再扩大到相邻样本或公开 core/shared/plugin，不设固定样本数量。
4. Model、Repository、State、Widget 和测试可分别参考不同样本，不复制整套脚手架。

只核对与本次改动相关的样本维度：账号来源/两侧调用，family key/写入/reset，DTO null/清空语义，Repository failure/注入，Widget i18n/订阅/清理，route/asset owner，以及最小可证伪测试。

## 复用阶梯

1. 职责、账号、错误语义和生命周期一致：直接复用。
2. owner 内有稳定共同概念：小幅扩展，使用明确业务参数。
3. 只有一个消费者或局部实现更清楚：保持局部。
4. 至少两个现存消费者、共同语义稳定、依赖方向正确且 contract 可测试：新增共享抽象。
5. 只能通过 Feature 横向私有依赖、app 反向承载或 shared 依赖 Feature 才能复用：重新选 owner。

不新增纯转发 wrapper、大量 nullable callback/互斥 boolean、假想未来 base/service、泄露私有 Model/route/Provider 的 API，也不恢复已拆除的 shared_business。

按需记录 owner、复用 symbol、实际比较的样本与选择理由；简单修改无需另写采样报告。完成后确认公开 API/调用者一致，且无无关迁移、改名或状态库替换；多解按 [澄清门](requirement-clarification.md) 停止。
