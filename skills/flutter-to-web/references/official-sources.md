# 官方权威来源索引（深挖原理时用）

> 主文档见 [../SKILL.md](../SKILL.md)。当用户对某个概念想深挖原理或最佳实践时，
> 先查 Flutter/Dart 或实际依赖的官方文档。解释动态解析出的 `<TUQIANG_ROOT>` 时，项目当前源码和锁定依赖版本优先于通用推荐。

## 引用规范（先翻译再给出处）

1. **先用大白话给用户讲清楚它在做什么**（遵守主文档的映射规则）；
2. 再补充官方文档链接，并说明它与途强当前实现是否一致；
3. **不要**直接把官方文档原文整段贴给用户。

## 场景 → 一手来源对照表

| 用户追问的场景 | 优先查阅 |
|---|---|
| "Flutter 项目应该怎么组织目录/分层？" | 先看途强的 project-structure、CI 和实际 package 依赖 |
| "响应式布局怎么做？手机和平板怎么适配？" | Flutter 官方 constraints、LayoutBuilder、MediaQuery 文档 |
| "路由和深链（deep link）怎么配？" | 先看途强 routing；只有代码使用 go_router 才查 go_router 文档 |
| "列表/表单溢出报错怎么办？" | Flutter 官方 constraints 和 RenderFlex 文档 |
| "JSON 序列化怎么写才对？" | Dart JSON 文档，再结合途强的 TCheck/Model 约定 |
| "HTTP 请求用什么包？" | 先判产品：Tuqiang 看 TQHttp/core_http，Laoying 看 LYBackendHttpClient；不要用通用 http 示例替换当前实现 |
| "测试怎么写？" | 先看途强 testing.md，再查 Flutter/Dart 测试文档 |
| "本地化/多语言怎么配？" | 先判产品并读当前 manifest/loader；Laoying 与 Tuqiang 拥有独立资源，不能互套 |

## 补充的官方一手资料

| 主题 | 官方入口 |
|---|---|
| 布局约束（理解了它就懂 90% 的布局报错） | docs.flutter.dev 的 "Understanding constraints" |
| Dart 语言速成（会 JS 的话半小时够用） | dart.dev/language 的 Dart cheatsheet codelab |
| Riverpod 文档 | riverpod.dev（解释 Provider API 时使用） |
| go_router 文档 | pub.dev/packages/go_router |
