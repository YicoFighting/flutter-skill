---
name: tuqiang-change-retrospective
description: 仅在用户明确要求复盘或学习文档时，依据当前源码、Git 与验证证据复盘已完成的 Tuqiang Bug、需求或混合改动，生成 Markdown；不修改业务代码或 Git。
license: Apache-2.0
metadata:
  version: "2.4.0"
---

# Tuqiang 变更复盘

仅在用户显式要求复盘或学习文档时使用。围绕已完成的目标改动解释结果、原因与验证，不扩展到其他产品或无关工作区改动。

## 边界

- 按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 确认 checkout 并读取项目 `AGENTS.md`。
- 只读源码、Git history/diff 与已有验证结果；唯一写入是一份新的复盘 Markdown。不改业务、测试、配置或 Git，不执行 checkout/reset/pull/fetch/bisect/commit/push，不顺手修复问题，不为复盘运行项目禁止的测试或依赖安装。
- 从用户指定的 commit/range/diff/file 或当前任务上下文确定范围；只有范围歧义会改变主要结论时才澄清。

## 流程

1. 从业务结果或已修复症状入手，用当前源码与目标 diff 解释关键变化。
2. 简单改动只写目标/症状、原因或实现、前后证据、验证与未知；跨文件或时序问题再展开数据/状态/UI 链，异步不画成同步栈。
3. 历史因果属于问题时按 [Git 因果](references/git-causality.md) 调查，不为普通需求强找根因。
4. 按 [输出约定](references/report-contract.md) 生成与问题规模相称的 UTF-8 无 BOM 文档，核验路径、行号、SHA 与敏感信息。

关键结论分为已证实事实、推断与未知。blame 只证明最后修改某行；用户确认修好不证明引入提交；未提交修改写为工作区改动；已有测试通过不自动等于完整验收。

## 按需核验

只展开与改动有因果关系的项：owner 或业务链 → [项目地图](../tuqiang-project-map/SKILL.md)；账号 → [账号模式](../tuqiang-project-map/references/account-mode.md)；文案/fallback/展示值 → [国际化](../tuqiang-dev/references/i18n.md)；复用与计算/IO 边界 → [本地复用](../tuqiang-dev/references/local-style-and-reuse.md)；生命周期、竞态、清理 → [状态与异步](../tuqiang-dev/references/state-async.md)；平台/地图/渠道 → [变体与构建](../tuqiang-project-map/references/variants.md)；用户要求 Web 对照 → [flutter-to-web](../flutter-to-web/SKILL.md)。

最终回复给出文档的绝对可点击路径、复盘范围与影响结论的未验证项，不在聊天中复制整份报告。
