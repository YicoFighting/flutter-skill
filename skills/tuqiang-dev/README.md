# tuqiang-dev

版本 2.3.0。用于 Tuqiang 开发、修复、测试和评审。入口只保留最小工作流：明确可验证行为 → 复用本地能力 → 最小实现 → 按风险验证。

入口见 [SKILL.md](SKILL.md)。核心规则按需读取：

- [本地复用与纯函数](references/local-style-and-reuse.md)：已有状态、函数和组件优先；缺少的计算显式输入、确定输出、无副作用。
- [国际化与展示取值](references/i18n.md)：区分 key、已译文本和业务值；统一 fallback、单次翻译、单一取值边界；manifest 与可选语言列表分开。
- [UI 适配](references/sizing-ui.md) / [路由](references/routing.md)：复用当前分栏封装，区分整窗与 pane，保持路由和状态身份。
- [异步生命周期](references/async-lifecycle.md) / [实施覆盖](references/implementation-coverage.md)：只检查本次触发的生命周期、账号和平台风险。
- [测试与验证](references/testing.md)：按风险分级选择检查，通过后停止，不重复全平台分析和构建。

国际化确定性检查（在本 Skill 目录执行）：

    python -X utf8 scripts/validate_tuqiang_i18n.py --root <TUQIANG_ROOT> --key '<source key>'

脚本检查 locale JSON、变更 key、literal 调用和占位符；翻译语义、动态 key、重复 fallback 与实际布局仍需相关源码/运行证据。其余专题由 SKILL.md 路由。

版本记录见 [CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
