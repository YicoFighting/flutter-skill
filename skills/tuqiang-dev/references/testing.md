# 测试与验证规范

测试围绕用户可观察行为、契约和风险，不按文件数量机械生成。先写可证伪验收；需求仍多解时先澄清，不能用测试把模型自己的方案固化成“需求”。

## 1. 默认层级

| 变更 | 默认验证 |
|---|---|
| Model、JSON、参数解析 | 单测缺字段、类型异常、null/清空语义 |
| Controller/Notifier/Repository | 成功、失败、空数据、重复请求、竞态与销毁 |
| 路由/payload/result/route effect | contract test：字符串、owner、builder、参数、返回和副作用 |
| 关键页面/表单 | Widget test：loading/empty/error/content 和按钮行为 |
| asset/i18n manifest | 路径、package、key/fallback、语言/状态选择与独立性测试 |
| 权限/MethodChannel/OHOS override | 静态边界 + 受影响端行为，必要时真机 |
| 文档/注释/纯格式 | diff、链接与编码检查 |

测试放在实际 owner 的 `test/`，包外只经公开 API。fixture/fake 保持契约结构，不把假 URL、延时假数据或“总是成功”实现放入生产。

## 2. 四个 target 与产品门禁

`tool/project.dart` 支持：

```text
standard  ohos  laoying_standard  laoying_ohos
```

`dart run tool/project.dart test <target>` 只运行对应宿主目录的 Flutter tests，不等于业务 package 或全仓测试。

边界脚本按产品：

```powershell
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope tuqiang
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope laoying
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope all
```

- 途强业务：目标 Feature/shared 的 analyze/test，`standard`/`ohos` 按影响运行；
- 老鹰业务：在 `apps/laoying_app` 运行 `flutter analyze`、`flutter test` 和目标 architecture/contract tests，再检查 `laoying_standard`/`laoying_ohos`；
- core/shared/plugin 公共变化：四 target analyze，加 `-ProductScope all` 与两产品受影响测试。

## 3. 老鹰 app boundary 检查器的已知基线

每次先对照 `docs/laoying/dependency_allowlist.md`、当前合法 import 和 `apps/laoying_app/tool/check_app_boundaries.dart` 的规则。最新 checkout 中，allowlist 已允许 `core_ui` 公开 API，App 也在合法使用；但该检查器的 `_forbiddenImports` 仍禁止 `package:core_ui/`，因此会产生与当前产品规则冲突的基线误报。

- 规则修复前，`dart run tool/check_app_boundaries.dart` 只能作为诊断输出，不能要求全绿或作为验收成功标准；
- 不能把既有 `core_ui` 报告归因于本次改动，也不能为了让旧脚本通过而删除合法复用；
- owner 互相 import 的真实边界使用 `test/app/architecture/dependency_boundary_test.dart` 等聚焦测试，并结合 `-ProductScope laoying`、目标 route/asset/i18n contract tests；
- 若当前 checkout 已修复检查器并与 allowlist 一致，再恢复为正式门禁，并记录实际命令与结果。

## 4. migration runner 的真实覆盖

`tool/run_migration_tests.ps1` 当前遍历途强 app 与 packages，不覆盖 `apps/laoying_app` 自身测试。它通过不代表老鹰业务通过；老鹰测试必须显式单独运行。

```powershell
pwsh .\tool\run_migration_tests.ps1 -FlutterExecutable <对应端 Flutter 可执行文件>
```

完整构建、签名与真机由 CI/专用环境执行时，交付中逐项写明已执行、失败和未执行，不能用 analyze 冒充 build 或真机通过。

## 5. 内容要求

- 异步测试等待明确状态/future，不用固定 sleep；
- 途强 Provider 测试使用实际 Provider 类型和 `ProviderContainer`/override；
- 老鹰使用实际 `LYAppProvider`、ChangeNotifier Controller、Repository fake 和 reset/listener；
- Widget 测试断言用户能看到或操作的结果，不绑定 Flutter 内部实现；
- asset 变体测试断言语言/状态选中了真实目标文件，不接受 Canvas/叠字/placeholder；
- 只有用户或仓库流程要求时才生成提测单，执行结果不能预填 PASS。
