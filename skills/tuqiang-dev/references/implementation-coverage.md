# 平台、账号模式、地图与设备覆盖门

只为当前任务可达维度建表，不生成平台 × 账号 × 地图 × 设备的机械笛卡尔积。候选事实来自项目地图的 [变体调查](../../tuqiang-project-map/references/variant-surface.md)、[账号模式](../../tuqiang-project-map/references/account-mode.md) 与当前源码。继承 SKILL 开工卡；混合变更分别套标准，影响行为或契约的 `unknown` 必须先澄清。

## 平台最低基线

| 变更类型 | Android | HarmonyOS | iOS |
|---|---|---|---|
| Bug | 修复并完成可行验证 | 修复并完成可行验证 | 检查共享路径与专属差异；未运行/未验收项明确交接 |
| 新需求 | 实现并验证 | 实现并验证 | 完成代码与可行静态验证；Windows 无法完成的 build/真机项交接 |
| 只读评审 | 检查实现与验证证据 | 检查实现与验证证据 | 检查实现并标出缺少的运行证据 |

`standard` 同时承载 Android/iOS，但一次 analyze 不是两端运行证明。某端不可达时以 source、adapter、route 或配置标记 `无需修改`；新需求需要用户可见降级且多解时先询问。

## 账号模式覆盖

命中 [账号模式事实](../../tuqiang-project-map/references/account-mode.md) 的任一分支面时，至少建立 personal/enterprise 两行：

| 账号模式 | 判定/入口 | 请求与数据 | 状态/缓存身份 | UI/副作用 | reset | 测试 |
|---|---|---|---|---|---|---|
| personal | 当前源码证据 |  |  |  |  |  |
| enterprise | 当前源码证据 |  |  |  |  |  |

代码确实共用可写 `共享实现覆盖`，但须给共同 symbol 和两种模式的调用证据。禁止从 `accountType`、target 或 flavor 推断，也不能因 personal 是默认分支省略 enterprise。

## Tuqiang 地图候选

命中主地图 Widget/protocol/adapter 或可见行为时，按当前 scene 逐项关闭：

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

## 设备页面范围

命中设备列表/搜索、首页/详情、“更多详情/设置”或服务状态卡片时，枚举 `deviceType`、scene/category、cameraScene、服务/账号/分享状态、route、最终 Page、目标 Widget 和真实点击区域。多个独立叶子且范围不明时，确认前不写代码；单一叶子仍检查共享组件、Provider、route 或 plugin 对其他叶子的回归。

## 覆盖台账

| 变更类型 | 账号模式 | 平台/target | 设备/route leaf | 地图 scene/后端 | 代码状态 | 验证状态/证据 |
|---|---|---|---|---|---|---|

代码状态：`已实现/已修复`、`共享实现覆盖`、`无需修改`、`待用户决定`、`iOS 专属实现待同事`；最后一项只允许 Bug 的 iOS 原生专属问题，新需求不得用它跳过代码。验证等级统一见 [测试规范](testing.md)。

完成时关闭全部实际可达行；个人/企业、三端、地图七行和已确认 route leaf 符合对应最低标准；每个共享实现或无需修改都有当前源码证据，代码状态与验证证据不混写。
