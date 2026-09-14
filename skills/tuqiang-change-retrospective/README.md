# tuqiang-change-retrospective

版本 2.1.0。仅在用户明确要求时，只读复盘已经完成的 Tuqiang Bug、需求或混合改动，并生成新的学习 Markdown；不修改业务代码或 Git。

入口见 [SKILL.md](SKILL.md)。按模式读取：

- [Bug 复盘](references/bug-retrospective.md)
- [需求复盘](references/feature-retrospective.md)
- [Git 因果](references/git-causality.md)
- [输出契约](references/report-contract.md)

复盘必须区分事实、推断和未知，并分别记录 accountMode、国际化、异步四防线以及实际验证状态。显式调用策略见 [agents/openai.yaml](agents/openai.yaml)。

构建或原生差异相关复盘补充 flavor、分发渠道、SDK 和对应产物验证，事实统一读取 [构建上下文](../tuqiang-project-map/references/build-runtime-context.md)。

版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
