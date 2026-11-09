# tuqiang-change-retrospective

版本 2.4.0。仅在用户明确要求时，只读复盘已完成的 Tuqiang Bug、需求或混合改动，生成一份新的学习 Markdown；不修改业务代码或 Git。

入口见 [SKILL.md](SKILL.md)。报告随改动规模展开，关键结论区分事实、推断与未知：

- [输出约定](references/report-contract.md)：Bug/需求/混合改动的内容要点、文件命名与证据格式
- [Git 因果](references/git-causality.md)：仅在历史归因相关时加载

显式调用策略见 [agents/openai.yaml](agents/openai.yaml)。版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
