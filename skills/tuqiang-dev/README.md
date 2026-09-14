# tuqiang-dev

版本 2.1.0。只开发、修复、测试和评审 Tuqiang；强制检查 accountMode、可见文本和异步结果发布，平台/地图/设备矩阵按需展开。

入口见 [SKILL.md](SKILL.md)。核心事实源：

- [实施覆盖](references/implementation-coverage.md)
- [国际化](references/i18n.md)
- [异步生命周期](references/async-lifecycle.md)
- [测试与验证](references/testing.md)：SDK 选择、owner 测试、边界命令与副作用范围
- [构建与运行上下文](../tuqiang-project-map/references/build-runtime-context.md)：Android flavor、Walle channel 与原生依赖

其余 owner、状态、网络、路由、资源、权限和兼容专题均由 SKILL.md 按任务路由。

国际化确定性检查：

    python -X utf8 scripts/validate_tuqiang_i18n.py --root <TUQIANG_ROOT> --key '<source key>'

脚本不是 Flutter 运行依赖；它检查 locale JSON、变更 key、literal 翻译调用和占位符。语义、可见硬编码、RTL 与布局仍需源码和运行审查。

版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
