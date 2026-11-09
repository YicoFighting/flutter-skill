# Tuqiang 验证

围绕用户可观察行为、账号模式、契约与真实风险选择检查，不按文件数机械生成。

## 项目约束

业务仓库 `.codex/skills/tuqiang-flutter-conventions` **禁止执行 `flutter test`、安装依赖（pub get）或修改无关 lockfile**。因此默认只做静态分析、确定性脚本与 diff 审查；只有用户明确要求时才运行测试或解析依赖，并在交付中写明是按用户要求执行。需要但未运行的测试写为"未执行（项目规则）"，不能写成通过。

## 风险分级

| 等级 | 范围 | 默认检查 | 升级条件 |
|---|---|---|---|
| L0 | 文案、颜色、间距、注释 | diff；改 Dart 时相关文件静态分析；文案跑 i18n 脚本 | 实际改变交互、订阅、可见性、资源加载或平台行为 |
| L1 | 局部计算、DTO、校验、单页状态/交互 | owner 包或相关文件 analyze；说明覆盖行为的现有测试 | 发现跨包消费者、身份/竞态风险或装配变化 |
| L2 | 公开 API、路由契约、session/账号隔离、缓存身份、异步资源 | 受影响 owner 与直接消费者 analyze；改 import/依赖边界时加架构脚本 | 影响宿主装配或 SDK 解析时加宿主 analyze |
| L3 | 原生、MethodChannel、插件注册、原生依赖、权限配置、Gradle/Manifest、ABI、渠道 | 受影响端静态/契约检查与必要构建 | 多端/多渠道都受影响才扩展；运行时风险需真机 |

一行 session/key 修改也可能是 L2。执行前用一句话说明等级、范围与准备运行的检查；有新消费者证据、未决风险、相关失败或用户/项目要求才扩大。必要检查通过且无未决风险即交付，不为"再保险"重复跑其他平台、渠道或已通过且输入未变的命令；改动后只重跑受影响检查。

## 命令索引（触发后选用，不是固定清单）

在 `$tuqiangRoot` 执行，检查退出码：

```powershell
dart run tool/project.dart analyze standard --no-pub
dart run tool/project.dart analyze ohos --no-pub
pwsh .\tool\check_dependency_architecture.ps1                 # 依赖/import/public API/package 变化
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope tuqiang
python -X utf8 <TUQIANG_DEV_SKILL>/scripts/validate_tuqiang_i18n.py --root $tuqiangRoot --key '<source key>'
git diff --check
```

- `project.dart analyze <target>` 在宿主目录运行，不保证覆盖 App/feature/shared 全部源码；局部改动优先对 owner 包或文件做分析。SDK 选择见 [变体与构建](../../tuqiang-project-map/references/variants.md)，OHOS 用工具封装选择的 OHOS SDK。
- 两个架构脚本互不替代；boundary 可能因无关历史基线失败，记录相关子检查与归属，不把基线算作本次回归，也不因子检查通过宣称整个 gate 全绿。
- `tool/run_migration_tests.ps1` 会逐包 pub get 再测试，属于项目禁止的默认操作，只在用户明确要求时运行。
- 用户要求运行测试时：在真实 owner 包执行 `<已确认标准SDK> test --no-pub <相关 test 文件>`，先读断言确认覆盖当前行为；会写同一解析状态的命令串行执行，完成后比较相关 diff，保留用户原有改动。

不默认安装工具、切换全局 SDK、`flutter clean`、pub get 或升级依赖。缺 SDK/设备或遇无关历史失败时完成其他可行检查并记录缺口，不反复重试，不改无关配置让检查变绿。

## 证据等级

静态分析、确定性脚本、单测、build、模拟器/真机、CI、未执行与已交接互不冒充；`standard` analyze 不证明 Android/iOS 运行。交付简述改动、已运行检查，以及"按风险无需运行"与"需要但未运行"两类，分开写；普通任务不罗列未触发的三端/地图/渠道组合。专题验证要点分别见 [状态与异步](state-async.md)、[国际化](i18n.md)、[覆盖](coverage.md)。
