# tuqiang-project-map

版本 2.4.0。只读核验 Tuqiang 当前源码的模块归属、路由、状态/数据链、账号与变体影响范围；从具体问题开始，证据足够即停止。

入口见 [SKILL.md](SKILL.md)，按问题读取：

- [根目录发现](references/project-root-discovery.md)：候选顺序、[只读校验脚本](scripts/validate_project_root.py)、业务仓库 `AGENTS.md`/`DESIGN.md`/`.codex/skills` 读取规则
- [架构与模块](references/architecture.md)、[启动与路由](references/startup-routing.md)、[状态与设备链](references/state-device-flow.md)
- [账号模式](references/account-mode.md)、[变体与构建](references/variants.md)（含鸿蒙百度地图与设备页面族）、[基础设施](references/infrastructure.md)
- 跨技能共用：[国际化](../tuqiang-dev/references/i18n.md)、[本地复用](../tuqiang-dev/references/local-style-and-reuse.md)

路径与 symbol 是检索入口，结论以任务时的源码为准。版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
