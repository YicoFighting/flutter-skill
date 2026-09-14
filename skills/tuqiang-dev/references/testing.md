# Tuqiang 测试与验证

测试围绕用户可观察行为、账号模式、契约和真实风险，不按文件数机械生成。先写可证伪验收；需求多解时先澄清，不能用测试固化模型自己的方案。

## 风险分级与默认验证范围

按行为、契约与平台影响选择，不能只按文件数或扩展名；一行 session/key 修改也可能是高风险。用户明确要求及当前项目实际适用的强制检查优先，普通本地任务不因 CI 存在全量流程就自动执行整条流水线。

| 等级/改动 | 默认验证 | 扩大范围的条件 |
|---|---|---|
| L0 局部展示：文案、颜色、间距、注释、文档；不改变业务逻辑或生命周期 | diff；修改 Dart 时做相关文件静态分析；文案按 i18n 校验 key/locale，布局用现有预览或可行视觉检查。无需为可逆样式新增镜像测试 | 实际改变交互、订阅、可见性、资源加载或平台行为时重新分级 |
| L1 模块业务：局部计算、DTO、校验、单页状态/交互 | owner 的相关文件或 package analyze，加覆盖变化行为的现有/必要回归测试；不重复运行等价的文件与整包分析 | 发现跨包消费者、身份/竞态风险或宿主装配变化时升级 |
| L2 跨包或关键状态：公开 API、路由契约、session/账号隔离、缓存身份、异步资源/竞态 | 受影响 owner 与直接消费者分析及契约/生命周期测试；改变 import/依赖边界时加对应 architecture/boundary 检查 | 影响宿主装配或 SDK 解析时加相关宿主分析；影响广泛且聚焦检查不能覆盖风险时加范围匹配的回归集 |
| L3 平台/打包：原生实现、MethodChannel、插件注册、SDK/原生依赖、权限配置、Gradle/Manifest、ABI、渠道或原生资源打包 | 受影响端的静态/契约检查与必要构建；选择能验证该变化的 artifact/flavor。推送、权限、地图回调等运行时风险还需对应运行验证 | 三端/多渠道均受影响才扩展相应构建；只构建可达且影响不同的组合 |

Model/JSON 关注 null、类型、兼容与清空语义；路由关注参数/返回/栈/effect；页面状态关注本次改变的 loading/error/empty/content。检查覆盖真实风险，不为完成模板测试未改动的全套状态。Bug 的回归验证应能区分修复前后；已有测试充分时不添加重复用例。

## 升级与停止条件

- 执行前用一句话明确本次等级、受影响范围和准备运行的检查，不要求用户审批普通验证。
- 只有新的依赖/消费者证据、尚未解决的风险、相关检查失败，或用户/项目明确要求，才扩大到宿主分析、构建或全量回归；具体说明新增检查要证明什么。
- 纯共享 Dart 变更默认不构建三端；但诊断表明问题只能在编译、链接或运行中验证时，仍执行相应必要检查，不以分级为由跳过。
- 本次验收已覆盖、必要检查通过且无未决风险后立即交付。不因“再保险”继续跑其他平台、渠道、全量测试，或再次执行输入未变化的已通过命令。
- 改动之后只重跑受新 diff 影响的检查；同一任务中源码、依赖、配置、SDK 和参数未变的通过结果可以复用。切换 checkout/SDK 或出现新风险时不能沿用失效证据。
- 缺少 SDK/设备或遇到无关历史失败时，完成其他可行检查并记录证据缺口；不反复重试相同失败，不通过修改无关依赖/配置让检查变绿，也不能把必要但未完成的验证写成通过。
- 不默认安装工具、切换全局 SDK、运行 `flutter clean`、重新 pub get 或生成完整学习报告；仅在任务需要或证据表明确有环境问题时处理。可先用现有失败结果定位原因，避免重跑长命令只为重新获取同一日志。

交付简述改动、已运行检查及必要但未运行的项目；“按风险无需运行”和“需要但未运行”分开。普通任务不用逐一罗列所有未触发的三端/地图/渠道组合。

账号、平台、地图与设备组合回到 [覆盖门](implementation-coverage.md)，异步竞态/销毁/身份/资源测试回到 [异步生命周期](async-lifecycle.md)，国际化结构与运行验收回到 [i18n](i18n.md)。测试放真实 owner 的 `test/`，包外只经公开 API；fixture/fake 保持真实契约，不把假 URL、延时数据或“永远成功”实现带入生产。

## SDK 与解析状态

仅在将要执行相关 Flutter 命令时，按 [构建上下文](../../tuqiang-project-map/references/build-runtime-context.md) 核验所需 SDK、宿主 `.fvmrc` 和 `tool/project.dart` 的当前选择逻辑；本任务已确认且未变化的工具信息直接复用。owner 包测试应使用已确认的标准 SDK 可执行文件（下例 `$standardFlutter`），不要假定 PATH 中 `flutter` 就是它；OHOS 验证使用工具封装选择的 OHOS SDK。

执行前记录相关 Git status/diff 和依赖解析是否就绪。已就绪的聚焦测试使用 `--no-pub`；缺少解析配置时，用目标 SDK 在对应 package 执行必要的 pub get，tracked lockfile 可用当前 SDK 支持的 `--enforce-lockfile` 保持约束。失败时报告缺少 SDK/依赖或锁约束，不擅自升级依赖、删除锁文件或伪称已测试。

同一 checkout 中会写同一 package 解析/生成状态的命令串行执行；OHOS 配置快照不保护所有生成文件。完成后比较相关 diff，识别工具新产生的改动，保留用户原有工作。

## Owner 包与 i18n 入口

仅改文案 key/值时先按 [i18n](i18n.md) 运行确定性校验；不自动执行两个包的全部测试。改变 App loader/manifest 加载、语言切换或 core_i18n 行为时，分别选对应测试，例如：

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

以下是触发后使用的命令索引，不是每次任务顺序执行的清单。宿主入口、composition override、插件注册、目标 SDK/依赖解析或平台 import 改变时，选择受影响 target 的 analyze；架构/迁移边界改变时选择相应 gate。每条检查退出码并记录结果；在 `$tuqiangRoot` 执行，`--no-pub` 的前提同上：

```powershell
dart run tool/project.dart analyze standard --no-pub
dart run tool/project.dart analyze ohos --no-pub
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope tuqiang
pwsh .\tool\check_dependency_architecture.ps1
```

- `project.dart analyze/test <target>` 在宿主目录调用 Flutter，不保证覆盖 App/feature/shared 包的全部源码或测试；按上面的等级先完成本次必要的 owner 检查。
- `check_migration_boundaries.ps1` 支持 `-ProductScope tuqiang`；`check_dependency_architecture.ps1` 是独立的全仓技术依赖检查，没有 ProductScope 参数。依赖/import/public API 改动时运行后者，不把两个检查视为互相替代，也不把全仓技术诊断扩为其他产品业务任务。
- `tool/run_migration_tests.ps1 -FlutterExecutable <已核验标准SDK可执行文件>` 当前枚举 `apps/tuqiang_app` 与 packages 中有测试的包，排除 example、构建目录和 `_ohos` 包。它逐包执行 `pub get`（tracked lockfile 时附 `--enforce-lockfile`）再 `test --no-pub`，会改解析状态；既不是只读扫描，也不是全部宿主/原生平台测试。仅在广泛依赖/公共契约变化且聚焦检查不足、用户明确要求或适用项目门禁要求时运行；单个页面/普通业务改动不默认运行，执行前重查脚本筛选条件。

具体测试入口可从当前 tracked `*_test.dart` 查找：设备目录的 cache/request mapper/filter、App invalid-token/session reset、GPS trace lifecycle、camera alarm/P2P、地图 helper 等。名称相近不代表覆盖当前行为，先读断言再选用。

boundary 可能因无关历史基线失败；记录完整命令、相关子检查和归属，不能把基线算作本次回归，也不能因子检查通过就宣称整个 gate 全绿。修改 `core/shared/plugin` 公开 API 时搜索全部调用方并运行直接受影响的 contract/tests，这不扩大 Tuqiang 业务范围。

## 证据等级

静态/analyze、单测、build、模拟器/真机、CI、未执行与已交接不得互相冒充；`standard` analyze 不证明 Android/iOS 两端运行。沿 [覆盖台账](implementation-coverage.md) 记录命令、通过、失败、未运行和交接，每个 `无需修改` 有源码证据，不用“其余类似”关闭行。
