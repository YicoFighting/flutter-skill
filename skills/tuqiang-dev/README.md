# tuqiang-dev

版本 2.2.0。只开发、修复、测试和评审 Tuqiang；按实际改动触发 accountMode、国际化与异步检查，按风险选择模块测试、宿主分析或构建；三端影响检查不等于三端重复运行。

入口见 [SKILL.md](SKILL.md)。核心事实源：

- [实施覆盖](references/implementation-coverage.md)
- [国际化](references/i18n.md)
- [异步生命周期](references/async-lifecycle.md)
- [测试与验证](references/testing.md)：四级风险、验证升级/停止条件、SDK 选择与命令范围
- [构建与运行上下文](../tuqiang-project-map/references/build-runtime-context.md)：Android flavor、Walle channel 与原生依赖

其余 owner、状态、网络、路由、资源、权限和兼容专题均由 SKILL.md 按任务路由。

国际化确定性检查：

    python -X utf8 scripts/validate_tuqiang_i18n.py --root <TUQIANG_ROOT> --key '<source key>'

脚本不是 Flutter 运行依赖；它检查 locale JSON、变更 key、literal 翻译调用和占位符。语义、可见硬编码、RTL 与布局仍需源码和运行审查。

版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
