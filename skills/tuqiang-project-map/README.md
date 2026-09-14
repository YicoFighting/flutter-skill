# tuqiang-project-map

版本 2.1.1。只读核验 Tuqiang 当前 checkout 的根目录、accountMode、owner、业务链、状态和变体事实；不修改代码或输出 Web 教学。

入口见 [SKILL.md](SKILL.md)。专题按需读取：

- [根目录](references/project-root-discovery.md)、[账号模式](references/account-mode.md)、[架构](references/architecture-overview.md)、[模块 owner](references/module-catalog.md)
- [启动与路由](references/startup-routing.md)、[Riverpod](references/riverpod-topology.md)、[设备定位](references/device-location-flow.md)
- [平台/地图/设备变体](references/variant-surface.md)、[基础设施](references/infrastructure-and-cross-cutting.md)、[完整追踪](references/requirement-trace-playbook.md)

新增 [构建与运行上下文](references/build-runtime-context.md)，区分 flavor、分发渠道与账号；[只读根校验脚本](scripts/validate_project_root.py) 使用当前任务动态发现的路径，支持子目录和 worktree；项目移动或改名后无需修改 Skill。

所有路径、symbol 和行号必须从本次源码重查。产品固定为 Tuqiang；公共 API 只调查技术调用契约，不扩大业务范围。

版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
