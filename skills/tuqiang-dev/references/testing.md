# Tuqiang 测试与验证

测试围绕用户可观察行为、账号模式、契约和真实风险，不按文件数机械生成。先写可证伪验收；需求多解时先澄清，不能用测试固化模型自己的方案。

## 风险选择

| 变更 | 最低验证 |
|---|---|
| Model、JSON、参数 | 缺字段、类型异常、nullable、兼容字段、清空/省略语义 |
| 路由/payload/result/effect | owner、builder、参数、返回、栈与副作用 |
| 页面/表单 | loading/empty/error/content、按钮、布局与生命周期 |
| 权限/MethodChannel | 静态契约 + 受影响端行为，必要时真机 |
| 文档/格式 | diff、链接、UTF-8 无 BOM |

账号、平台、地图与设备组合回到 [覆盖门](implementation-coverage.md)，异步竞态/销毁/身份/资源测试回到 [异步生命周期](async-lifecycle.md)，国际化结构与运行验收回到 [i18n](i18n.md)。测试放真实 owner 的 `test/`，包外只经公开 API；fixture/fake 保持真实契约，不把假 URL、延时数据或“永远成功”实现带入生产。

## SDK 与解析状态

先按 [构建上下文](../../tuqiang-project-map/references/build-runtime-context.md) 核验目标 SDK、宿主 `.fvmrc` 和 `tool/project.dart` 的当前选择逻辑。owner 包测试应使用已确认的标准 SDK 可执行文件（下例 `$standardFlutter`），不要假定 PATH 中 `flutter` 就是它；OHOS 验证使用工具封装选择的 OHOS SDK。

执行前记录相关 Git status/diff 和依赖解析是否就绪。已就绪的聚焦测试使用 `--no-pub`；缺少解析配置时，用目标 SDK 在对应 package 执行必要的 pub get，tracked lockfile 可用当前 SDK 支持的 `--enforce-lockfile` 保持约束。失败时报告缺少 SDK/依赖或锁约束，不擅自升级依赖、删除锁文件或伪称已测试。

同一 checkout 中会写同一 package 解析/生成状态的命令串行执行；OHOS 配置快照不保护所有生成文件。完成后比较相关 diff，识别工具新产生的改动，保留用户原有工作。

## Owner 包与 i18n 入口

先按 [i18n](i18n.md) 运行确定性校验，再执行项目专属测试：

```powershell
# $standardFlutter 是按当前项目解析出的标准 SDK 可执行文件。
Push-Location -LiteralPath (Join-Path $tuqiangRoot 'apps/tuqiang_app')
try {
    & $standardFlutter test --no-pub test/app/i18n/app_i18n_loader_test.dart
    if ($LASTEXITCODE -ne 0) { throw 'App i18n 测试失败' }
} finally { Pop-Location }

Push-Location -LiteralPath (Join-Path $tuqiangRoot 'packages/core/core_i18n')
try {
    & $standardFlutter test --no-pub
    if ($LASTEXITCODE -ne 0) { throw 'core_i18n 测试失败' }
} finally { Pop-Location }
```

其他业务测试同样切换到真实 owner 包并指定相关 test 文件；不要将 package 相对测试路径直接传给宿主 `project.dart test standard`。

## 宿主与边界

在 `$tuqiangRoot` 按改动影响选用以下命令；每条检查退出码，记录各自结果。`--no-pub` 的前提同上：

```powershell
dart run tool/project.dart analyze standard --no-pub
dart run tool/project.dart analyze ohos --no-pub
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope tuqiang
pwsh .\tool\check_dependency_architecture.ps1
```

- `project.dart analyze/test <target>` 在宿主目录调用 Flutter，不保证覆盖 App/feature/shared 包的全部源码或测试；先完成本次 owner 的 analyze/test。
- `check_migration_boundaries.ps1` 支持 `-ProductScope tuqiang`；`check_dependency_architecture.ps1` 是独立的全仓技术依赖检查，没有 ProductScope 参数。依赖/import/public API 改动时运行后者，不把两个检查视为互相替代，也不把全仓技术诊断扩为其他产品业务任务。
- `tool/run_migration_tests.ps1 -FlutterExecutable <已核验标准SDK可执行文件>` 当前枚举 `apps/tuqiang_app` 与 packages 中有测试的包，排除 example、构建目录和 `_ohos` 包。它逐包执行 `pub get`（tracked lockfile 时附 `--enforce-lockfile`）再 `test --no-pub`，会改解析状态；既不是只读扫描，也不是全部宿主/原生平台测试。仅在影响面确需全量回归时运行，执行前重查脚本筛选条件。

具体测试入口可从当前 tracked `*_test.dart` 查找：设备目录的 cache/request mapper/filter、App invalid-token/session reset、GPS trace lifecycle、camera alarm/P2P、地图 helper 等。名称相近不代表覆盖当前行为，先读断言再选用。

boundary 可能因无关历史基线失败；记录完整命令、相关子检查和归属，不能把基线算作本次回归，也不能因子检查通过就宣称整个 gate 全绿。修改 `core/shared/plugin` 公开 API 时搜索全部调用方并运行直接受影响的 contract/tests，这不扩大 Tuqiang 业务范围。

## 证据等级

静态/analyze、单测、build、模拟器/真机、CI、未执行与已交接不得互相冒充；`standard` analyze 不证明 Android/iOS 两端运行。沿 [覆盖台账](implementation-coverage.md) 记录命令、通过、失败、未运行和交接，每个 `无需修改` 有源码证据，不用“其余类似”关闭行。
