# tuqiang-dev

版本 2.4.0。用于 Tuqiang 开发、修复和评审：项目规则优先 → 明确可验证行为 → 复用本地能力 → 最小实现 → 按风险验证。

入口见 [SKILL.md](SKILL.md)，专题按需读取：

- [本地复用与纯函数](references/local-style-and-reuse.md)、[国际化与展示取值](references/i18n.md)
- [状态、网络与异步](references/state-async.md)、[UI、路由与资源](references/ui-routing-assets.md)
- [平台/账号/地图/设备/权限覆盖](references/coverage.md)、[验证](references/testing.md)、[评审清单](references/code-review-checklist.md)

业务仓库 `.codex/skills/tuqiang-flutter-conventions` 默认禁止 `flutter test` 与安装依赖，因此默认验证为静态分析、确定性脚本与 diff。国际化确定性检查（只读，在本 Skill 目录执行）：

    python -X utf8 scripts/validate_tuqiang_i18n.py --root <TUQIANG_ROOT> --key '<source key>'

版本记录见 [CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
