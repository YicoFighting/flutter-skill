# 测试与验证规范

测试围绕行为和风险编写，不按“每改一个文件就配一个测试文件”机械生成，也不把未询问用户当成禁止测试的理由。

## 1. 选择测试层级

| 变更 | 默认验证 |
|---|---|
| Model、JSON、参数解析 | Model 单测，覆盖缺字段、类型异常和 null 语义 |
| Controller、Notifier、Repository | 单测，覆盖成功、失败、空数据、重复请求和销毁后的回调 |
| 路由、参数、返回值、route effect | route contract test，检查字符串、owner、builder 和关键副作用 |
| 关键页面、表单、加载/空态/错误态 | Widget test；只测用户可观察行为 |
| 权限、MethodChannel、OHOS override、系统能力 | 静态边界检查 + 受影响端行为验证，必要时真机测试 |
| 文档、注释、纯格式或无行为重命名 | 不强制新增测试，执行 diff 和编码检查即可 |

测试应放在实际 package 的 `test/` 下，并通过公开 barrel/API 访问被测包；包外不要 import 另一个 feature 的私有 `src/**`。测试 fixture 和 fake 应保持与真实接口结构一致，不要把假 URL 或延时假数据放进生产 Repository。

## 2. 途强项目的测试入口

`dart run tool/project.dart test <standard|ohos>` 只是对对应 app 目录调用 Flutter test。它不等于完整迁移测试。

完整迁移测试由 `tool/run_migration_tests.ps1` 遍历 app、core、feature 和 shared package，并按 tracked lockfile 决定是否使用 `--enforce-lockfile`：

```powershell
pwsh .\tool\run_migration_tests.ps1 -FlutterExecutable <对应端 Flutter 可执行文件>
```

如果只改一个 package，可以先在该 package 运行针对性测试；如果改了公共包、路由、资源、i18n manifest 或迁移边界，再运行：

```powershell
pwsh .\tool\check_migration_boundaries.ps1
```

Standard/OHOS 的完整测试和构建由 CI 负责时，本地可以只跑项目规定的静态检查，但交付说明必须写清楚哪些测试、构建或真机验证未执行。

## 3. 测试内容要求

- 不只测 happy path：至少考虑空响应、类型异常、网络失败、重复操作、页面离开和语言切换；
- 测试异步逻辑时等待明确状态或 future，不使用无意义的固定 sleep；
- Provider 测试使用项目实际 Provider 类型和 `ProviderContainer`/override，不能把 StateNotifier 模板套到 Notifier；
- Widget 测试优先验证文案、可见状态、按钮行为和导航结果，不测试 Flutter 内部实现细节；
- 只有当用户或仓库流程要求提测单时才生成提测单，并据实记录执行结果，不能预填 PASS。
