---
name: tuqiang-change-retrospective
description: 仅在用户明确要求复盘或学习文档时，依据当前源码、Git 与验证证据复盘已完成的 Tuqiang Bug、需求或混合改动，生成 Markdown；不修改业务代码或 Git。
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Tuqiang 变更复盘

仅在用户显式要求复盘或学习文档时使用。围绕已完成的目标改动解释结果、原因和验证，不扩展到其他产品线或无关工作区改动。

## 范围与边界

- 按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 确认 checkout 并读取项目 AGENTS.md。
- 只读源码、Git history/diff 和已有验证结果；默认唯一写入是新的复盘 Markdown。不修改业务、测试、配置或 Git，不执行 checkout/reset/pull/fetch/bisect/commit/push，不顺手修复问题。
- 从用户指定 commit/range/diff/file 或当前任务上下文确定范围，记录相关基线和验证状态。只有范围歧义会改变主要结论且无法从上下文排除时才澄清。
- 账号、平台、国际化、异步和构建信息只在影响改动结论时展开；不输出强制全字段范围卡。

## 按改动规模复盘

1. 从业务结果或已修复症状入手，用当前源码和目标 diff 解释关键变化。
2. 简单修复只保留问题/目标、原因或实现、前后证据、验证与仍未知的部分。跨文件或时序问题再展开数据/状态/UI 链；异步完成和响应式重建不能画成同步栈。
3. 历史因果属于问题时，再调查引入、暴露、修复和防线缺失；不为普通需求强行寻找历史根因。
4. 按 [输出约定](references/report-contract.md) 生成与问题规模相称的 UTF-8 无 BOM 文档，核验路径、行号、SHA 与敏感信息。

关键结论分为已证实事实、推断与未知。blame 只证明最后修改某行，用户确认修好不证明历史引入提交；未提交修改如实写为工作区改动，已有测试通过也不自动证明完整验收。

## 按需读取

| 场景 | Reference |
|---|---|
| Bug 原因、修复有效性与预防 | [Bug 复盘](references/bug-retrospective.md) |
| 需求结果、实现取舍与验收 | [需求复盘](references/feature-retrospective.md) |
| 需要历史归因 | [Git 因果](references/git-causality.md) |
| 文档路径、结构和证据格式 | [输出约定](references/report-contract.md) |
| owner 或业务链不清 | [项目地图](../tuqiang-project-map/SKILL.md) |
| 账号分流或隔离 | [账号模式](../tuqiang-project-map/references/account-mode.md) |
| 翻译 fallback、默认文案和展示取值 | [国际化与展示边界](../tuqiang-dev/references/i18n.md) |
| 本地复用与新增计算/IO 边界 | [本地风格与复用](../tuqiang-dev/references/local-style-and-reuse.md) |
| 生命周期、竞态或清理 | [异步生命周期](../tuqiang-dev/references/async-lifecycle.md) |
| 构建、渠道或原生依赖 | [构建上下文](../tuqiang-project-map/references/build-runtime-context.md) |
| 用户要求 Web 对照 | [flutter-to-web](../flutter-to-web/SKILL.md) |

只加载相关资料，当前源码、Git、验证证据和项目规则优先。最终回复给出文档的绝对可点击路径、复盘范围及影响结论的未验证项，不重复整份报告。
