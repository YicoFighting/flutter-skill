# 平台、账号模式、地图与设备覆盖门

只为本次改动影响的可达维度建表；简单共享改动可用一句证据说明，无需展开表格。不生成平台 × 账号 × 地图 × 设备的机械笛卡尔积。候选事实来自项目地图的 [变体调查](../../tuqiang-project-map/references/variant-surface.md)、[账号模式](../../tuqiang-project-map/references/account-mode.md) 与当前源码。以 SKILL 的验收行为和已确定范围为准；影响行为或契约的未知按 [澄清规则](requirement-clarification.md) 处理。

## 平台实现与验证分开

用户指定的平台范围优先；未指定的通用需求先核对 Android、iOS、HarmonyOS 的可达性。Bug 修复覆盖实际受影响实现，新需求覆盖范围内可达实现，不能仅因本机无法运行某端就省略其代码。共享 Dart 一次实现可覆盖多端；某端不可达时用 source、adapter、route 或配置说明。

| 当前证据 | 代码处理 | 验证选择 |
|---|---|---|
| 三端共用同一 Dart 路径，未改变平台边界 | 修改共享 owner，引用共同入口与消费者证据 | 一组相关模块分析/测试；不重复做三份相同检查 |
| 某端存在独立实现或条件分支 | 检查本次变化影响到的专属代码 | 增补该端相关静态/契约检查，构建与运行按风险选择 |
| 原生、SDK、权限、打包或渠道影响行为 | 完成受影响宿主/plugin/adapter 的修改 | 受影响端构建；运行时能力风险需对应运行验证 |
| 只读评审 | 评估实际影响和已有证据 | 默认只读调查；关键结论确需复现时选聚焦检查 |

`共享实现覆盖` 只说明代码覆盖；`standard` analyze 不证明 Android/iOS 运行。Windows 上确需 iOS 构建或真机而无法执行时明确交接，不用其他平台成功代替。无需构建的低风险任务不因此变成待交接任务。具体命令的触发条件见 [测试规范](testing.md)。

## 账号模式覆盖

本次改动影响 [账号模式事实](../../tuqiang-project-map/references/account-mode.md) 的请求、数据、权限、缓存或行为分支时，分别核对 personal/enterprise。路径和行为确实相同可合并说明；有差异才展开下表，不因页面属于设备/我的模块就重查整条账号链：

| 账号模式 | 判定/入口 | 请求与数据 | 状态/缓存身份 | UI/副作用 | reset | 测试 |
|---|---|---|---|---|---|---|
| personal | 当前源码证据 |  |  |  |  |  |
| enterprise | 当前源码证据 |  |  |  |  |  |

代码确实共用可写 `共享实现覆盖`，但须给共同 symbol 和两种模式的调用证据。禁止从 `accountType`、target 或 flavor 推断，也不能因 personal 是默认分支省略 enterprise。

## Tuqiang 地图候选

改变地图协议、adapter、坐标、marker、轨迹、后端选择或地图生命周期时，按当前 scene 检查以下候选；这些是影响面，不是七次构建/真机的固定清单。仅改地图页普通文案、间距或颜色且不触及地图逻辑时，不展开：

| 行 | 平台/target | 后端 |
|---|---|---|
| 1 | Android `standard` | 百度 Android |
| 2 | Android `standard` | 高德 Android |
| 3 | Android `standard` | Google Flutter/Android |
| 4 | iOS `standard` | 百度 iOS |
| 5 | iOS `standard` | 高德 iOS |
| 6 | iOS `standard` | Google Flutter/iOS |
| 7 | HarmonyOS `ohos` | 华为 Map Kit，并核对兼容 factory id 的宿主映射 |

“花瓣地图”只是 Map Kit 的业务称谓，不新增 SDK 或 `TQMapSourceType`。共享 Dart 证据可跨行引用，但平台差异与验证状态分开；不可达行附 `无需修改` 证据。POI、街景、外部导航等独立 channel 另建子表。

## Android 构建变体（条件触发）

原生依赖、推送、广告、ABI、Manifest 或渠道差异按 [构建上下文](../../tuqiang-project-map/references/build-runtime-context.md) 增补 flavor/channel。`combined` 母包与写入渠道后的产物分开验证；默认 `allvendor` 结果不证明其他包可用。地图七行是平台/后端候选，若该改动还受 flavor 影响，则在对应行补充实际可达组合；无关任务不扩表。

## 设备页面范围

改变设备分流、共享详情行为或服务状态规则时，枚举 `deviceType`、scene/category、cameraScene、服务/账号/分享状态、route、最终 Page、目标 Widget 和真实点击区域。只有不同叶子会改变实现且用户/源码都不能确定范围时，暂停依赖该选择的改动；单一叶子仍检查共享组件、Provider、route 或 plugin 对其他叶子的回归。

## 覆盖台账

| 变更类型 | 账号模式 | 平台/target（相关时附 flavor/channel） | 设备/route leaf | 地图 scene/后端 | 代码状态 | 验证状态/证据 |
|---|---|---|---|---|---|---|

代码状态：`已实现/已修复`、`共享实现覆盖`、`无需修改`、`待用户决定`、`受阻`；范围内代码仍需完成，实际限制要说明，不能以缺少本机设备为由省略实现。验证等级统一见 [测试规范](testing.md)。

完成时关闭本次受影响的实际可达行；个人/企业、平台、地图及 route leaf 按触发条件检查；每个共享实现或无需修改都有当前源码证据，代码状态与验证证据不混写。
