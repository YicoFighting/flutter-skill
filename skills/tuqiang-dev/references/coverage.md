# 平台、账号、地图、设备与权限覆盖

只为本次改动影响的可达维度建表；简单共享改动用一句证据说明即可，不生成平台 × 账号 × 地图 × 设备笛卡尔积。候选事实见项目地图 [变体与构建](../../tuqiang-project-map/references/variants.md) 与 [账号模式](../../tuqiang-project-map/references/account-mode.md)。

## 平台

用户指定的平台范围优先；未指定的通用需求核对 Android、iOS、HarmonyOS 可达性。Bug 覆盖实际受影响实现，新需求覆盖范围内可达实现，不能因本机无法运行某端就省略其代码。

| 当前证据 | 代码 | 验证 |
|---|---|---|
| 三端共用同一 Dart 路径，未改平台边界 | 改共享 owner，给共同入口证据 | 一组相关静态检查，不做三份 |
| 某端有独立实现或条件分支 | 检查受影响的专属代码 | 补该端静态/契约检查 |
| 原生、SDK、权限、打包或渠道影响行为 | 完成受影响宿主/plugin/adapter 修改 | 受影响端构建；运行时风险需对应运行验证 |

- Android/iOS 用 `Platform.isAndroid/isIOS`，OHOS 用 `AppTargetConfig.isOhos`。OHOS-only 类型、View、package 或 SDK 只在宿主、专属 plugin/adapter 或注入实现中出现；公共 Dart 通过 callback、override 或 bridge 依赖平台实现。
- 依赖选择：现有 core/plugin/adapter → 已验证纯 Dart 库 → OHOS override → 新 plugin/channel；新增依赖前核对两个 target 的 pubspec、原生实现、权限与打包。
- 拨号、短信、商店、蓝牙、地图、推送、相机、文件、后台定位等能力逐端确认可达性与不支持时的用户行为；`canLaunchUrl`、override 或 analyze 通过不证明真机能力。
- `standard` analyze 不证明 Android/iOS 运行；Windows 上必需的 iOS 构建/真机无法执行时明确交接。

## 账号模式

改动影响请求、数据、权限、缓存或行为分支时，分别核对 personal/enterprise（判定入口、请求与数据、状态/缓存身份、UI/副作用、reset）。代码确实共用可写"共享实现覆盖"，但要给共同 symbol 与两种模式的调用证据；不从 `accountType`、target、flavor 推断，不因 personal 是默认分支省略 enterprise。

## 地图

改变地图协议、adapter、坐标、marker、轨迹、后端选择或地图生命周期时按当前 scene 检查以下候选（影响面，不是 7 次构建清单）；只改地图页普通文案、间距或颜色不展开：

| 行 | 平台 | 后端 |
|---|---|---|
| 1–3 | Android `standard` | 百度 / 高德 / Google |
| 4–6 | iOS `standard` | 百度 / 高德 / Google |
| 7 | HarmonyOS `ohos` | 百度 ArkTS（`TQBMap*`；高德 ID 也解析到百度） |

- 鸿蒙百度问题优先在 `tq_map_plugin/ohos/**/BMap/` 原生实现修复；确需改 Dart 时只以 `TQMapViewHost.usesOhosBaiduMap(mapType, scene)` 为启用条件，其他地图与系统保持原路径，详见业务仓库 `docs/ohos_baidu_map_integration_spec.md`。
- 华为 Map Kit（花瓣）factory 只服务老鹰宿主，不属于 Tuqiang 行。POI、街景、外部导航等独立 channel 另建子表。共享 Dart 证据可跨行引用，平台差异与验证状态分开。
- 原生依赖、推送、广告、ABI、Manifest 或渠道差异再按 flavor/channel 补行；`combined` 母包与写入渠道后的产物分开验证。

## 设备页面

改变设备分流、共享详情行为或服务状态规则时，枚举 deviceType、scene/category、cameraScene、服务/账号/分享状态、route、最终 Page、目标 Widget 与真实点击区域。只有不同叶子会改变实现且用户与源码都不能确定范围时，才暂停依赖该选择的改动；单一叶子仍检查共享组件、Provider、route 或 plugin 对其他叶子的回归。

## 权限

优先 `core_base::TQPermissionManager` 与 `core_union::TQPermissionAlert`，feature 不直接 import `permission_handler`。按需在进入功能时申请；首次、普通拒绝、永久拒绝（引导设置）、系统服务关闭是不同状态，需求未定且会改变交互时先问。权限文案按 [国际化](i18n.md) 覆盖全部 locale；原生声明在 `apps/standard/android`、`apps/standard/ios`、`apps/ohos/ohos`，只改受影响端。没有真机结果写"未执行/交接"。

## 台账

需要时用一行一条记录：变更类型 | 账号 | 平台/target（相关时附 flavor） | 设备/route leaf | 地图 scene/后端 | 代码状态 | 验证证据。代码状态：`已实现/已修复`、`共享实现覆盖`、`无需修改`（附源码证据）、`待用户决定`、`受阻`；代码状态与验证证据不混写，不用"其余类似"关闭行。
