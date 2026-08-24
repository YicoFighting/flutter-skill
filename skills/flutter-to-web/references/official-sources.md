# 官方权威来源索引（深挖原理时用）

> 主文档见 [../SKILL.md](../SKILL.md)。当用户对某个概念想**深挖原理或最佳实践**时，
> 不要自己瞎编，按这张表引用 Flutter 官方 Agent Skills 仓库（`flutter/agent-plugins`）作为权威来源。

## 引用规范（先翻译再给出处）

1. **先用大白话给用户讲清楚"它是在干嘛"**（遵守主文档 §1 的映射规则）；
2. 再补一句："官方推荐的写法是 XXX（来源：`flutter/agent-plugins` 的 `flutter-xxx` skill）"；
3. **不要**直接把官方 skill 的英文原文整段甩给用户。

## 场景 → 官方 Skill 对照表

| 用户追问的场景 | 引用的官方 Skill |
|---|---|
| "Flutter 项目应该怎么组织目录/分层？" | `flutter-apply-architecture-best-practices`（UI/Logic/Data 分层、MVVM、Repository 模式） |
| "响应式布局怎么做？手机和平板怎么适配？" | `flutter-build-responsive-layout`（LayoutBuilder/MediaQuery/Expanded 的正确用法） |
| "路由和深链（deep link）怎么配？" | `flutter-setup-declarative-routing`（go_router、嵌套导航、URL 策略） |
| "列表/表单溢出报错怎么办？" | `flutter-fix-layout-issues`（RenderFlex overflow、约束问题排查） |
| "JSON 序列化怎么写才对？" | `flutter-implement-json-serialization`（fromJson/toJson 最佳实践） |
| "HTTP 请求用什么包？" | `flutter-use-http-package`（http 包 GET/POST/PUT/DELETE） |
| "测试怎么写？" | `flutter-add-widget-test` / `dart-test-fundamentals` / `dart-add-unit-test` |
| "本地化/多语言怎么配？" | `flutter-setup-localization`（flutter_localizations + intl + l10n.yaml） |

## 补充的官方一手资料

| 主题 | 官方入口 |
|---|---|
| 布局约束（理解了它就懂 90% 的布局报错） | docs.flutter.dev 的 "Understanding constraints" |
| Dart 语言速成（会 JS 的话半小时够用） | dart.dev/language 的 Dart cheatsheet codelab |
| Riverpod 文档 | riverpod.dev（有最佳实践的官方示例） |
| go_router 文档 | pub.dev/packages/go_router |
