# tuqiang-project-map

版本 2.2.0。只读核验 Tuqiang 当前源码的模块归属、路由、状态/数据链和影响范围；从具体问题开始，证据足够即停止，不要求每次建立上下文卡或展开完整链路。

入口见 [SKILL.md](SKILL.md)。按问题读取：

- [根目录](references/project-root-discovery.md)、[账号模式](references/account-mode.md)、[架构](references/architecture-overview.md)、[模块 owner](references/module-catalog.md)
- [启动与路由](references/startup-routing.md)、[Riverpod](references/riverpod-topology.md)、[设备定位](references/device-location-flow.md)
- [平台/地图/设备变体](references/variant-surface.md)、[基础设施](references/infrastructure-and-cross-cutting.md)、[构建上下文](references/build-runtime-context.md)、[完整追踪](references/requirement-trace-playbook.md)
- 跨技能共用：[国际化与展示取值](../tuqiang-dev/references/i18n.md)、[本地封装与纯函数边界](../tuqiang-dev/references/local-style-and-reuse.md)

本版核对了语言选择与资源清单的差异、自适应路由和分栏/地图面板封装。路径与 symbol 是检索入口，结论仍以任务时的源码为准。账号和平台保持独立维度，产品范围固定 Tuqiang。

[只读根校验脚本](scripts/validate_project_root.py) 支持用户指定的仓库根、子目录、源码文件和 worktree；项目移动或改名后无需重新配置。版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
