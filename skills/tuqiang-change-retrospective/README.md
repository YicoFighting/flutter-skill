# tuqiang-change-retrospective

版本 2.2.0。仅在用户明确要求时，只读复盘已完成的 Tuqiang Bug、需求或混合改动，并生成新的学习 Markdown；不修改业务代码或 Git。

入口见 [SKILL.md](SKILL.md)。报告随改动规模展开，简单修复无需全字段卡、固定长模板或全量风险矩阵。关键结论仍需证据，事实、推断和未知分别表述。

- [Bug 复盘](references/bug-retrospective.md)、[需求复盘](references/feature-retrospective.md)
- [Git 因果](references/git-causality.md)：仅在历史归因相关时加载
- [输出约定](references/report-contract.md)：文件路径、精简结构与证据
- [国际化与展示边界](../tuqiang-dev/references/i18n.md)：fallback 和展示兼容单点处理
- [本地风格与复用](../tuqiang-dev/references/local-style-and-reuse.md)：已有封装优先，新增计算保持纯函数

账号、异步和构建差异只在影响结论时调查。共享 references 随四个技能一同安装；显式调用策略保留于 [agents/openai.yaml](agents/openai.yaml)。

版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
