# 局部风格与复用

目标是在真实 Tuqiang owner 中选择成熟样本和最小抽象，不用模型偏好的统一架构覆盖存量。

## 采样

1. 沿入口、route、Provider/Controller/Manager、Repository、asset 和测试确定 owner。
2. 检查公开 barrel/API 与真实调用方；包外不 import 其他 package 的私有 src。
3. 在同 owner 选 2–4 个同类样本，优先相同操作、生命周期、accountMode 和平台边界；不足再看相邻 owner，最后才看公开 core/shared/plugin。
4. Model、Repository、State、Widget 和测试可分别参考不同样本，不复制整套脚手架。

对样本至少核对：账号来源/两侧调用，family key/写入/reset，DTO null/清空语义，Repository failure/注入，Widget i18n/订阅/清理，route/asset owner，以及最小可证伪测试。

## 复用阶梯

1. 职责、账号、错误语义和生命周期一致：直接复用。
2. owner 内有稳定共同概念：小幅扩展，使用明确业务参数。
3. 只有一个消费者或局部实现更清楚：保持局部。
4. 至少两个现存消费者、共同语义稳定、依赖方向正确且 contract 可测试：新增共享抽象。
5. 只能通过 Feature 横向私有依赖、app 反向承载或 shared 依赖 Feature 才能复用：重新选 owner。

不新增纯转发 wrapper、大量 nullable callback/互斥 boolean、假想未来 base/service、泄露私有 Model/route/Provider 的 API，也不恢复已拆除的 shared_business。

记录 accountMode、owner、复用 symbol、2–4 个样本、选择理由、最小范围和未决策项。完成后确认公开 API/调用者一致，且无无关迁移、改名或状态库替换；多解按 [澄清门](requirement-clarification.md) 停止。
