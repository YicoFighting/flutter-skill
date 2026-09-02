# 跨端、地图实现与设备页面覆盖门

本文件把“受影响端”展开成可执行矩阵。任何 Bug 修复、新需求、混合变更或相关代码评审，在写代码前先分类并建立矩阵；事实候选来自项目地图的 [平台、地图后端与设备页面变体调查](../../tuqiang-project-map/references/variant-surface.md) 与当前源码。

## 1. 先分类，不混用完成标准

```text
变更类型：Bug 修复 | 新需求 | 混合变更 | 只读评审
目标产品：tuqiang | laoying | cross-product | 待确认
用户可观察行为：...
设备范围：不涉及 | 全部 | 已明确的 deviceType/scene/cameraScene | 待确认
地图场景：不涉及 | 填写实时 TQMapUseSceneType enum symbol 集合（如 location、lineTrace、smartTrace、pointTrace、fence）
```

混合变更分别套用规则：修复部分按 Bug 标准，新行为按新需求标准。产品范围是独立维度；同名功能同时存在于 Tuqiang 与 Laoying 时，不因代码相似自动扩大或缩小产品范围。

产品无法从用户描述与当前入口唯一确定时，先返回候选 Product Scope 请求确认。只有任务命中第 4 节列出的设备入口时才展开设备 route leaf；与这些入口无关的普通页面改动记为“不涉及”，不得仅因文件位于 GPS module 就强制询问设备范围。地图同理：未命中地图 Widget/protocol/adapter、地图相关页面行为或独立地图能力时记为“不涉及”，不得生成供应商候选行。

## 2. 平台最低交付基线

本节是仓库的组织最低基线：除非用户明确变更这条规则，或当前源码/Product Scope 证明能力在某平台不可达，否则不能因复现设备、当前打开文件或本机工具限制缩小平台代码范围。平台专属问题不得伪造其他端修改：用源码证据把无关平台记为 `无需修改`；若问题只存在于 iOS 原生层，则按团队约束列出同事实施与验证交接。所有实际受影响且由本机负责的平台仍须完成代码修复，可运行性与验收状态另行记录。

| 变更类型 | Android | HarmonyOS | iOS |
|---|---|---|---|
| Bug 修复 | 必须修复并完成可行验证 | 必须修复并完成可行验证 | 检查共享代码和 iOS 专属影响；本机不声称已运行或已验收，列出交接给同事的文件、场景与验证项 |
| 新需求 | 必须实现并验证 | 必须实现并验证 | 必须完成代码实现与可行静态验证；本机无法运行的 build/模拟器/真机项明确交接 |
| 只读评审 | 检查实现和验证证据 | 检查实现和验证证据 | 检查实现；缺少运行证据时作为明确剩余风险 |

“Bug 的 iOS 交接”不等于机械阻止共享 Dart 修复：共享实现自然覆盖 iOS 代码路径时，记录“代码路径已覆盖，iOS 未运行/未验收”；只有 iOS 原生专属问题留给同事实施。不得把 `standard` analyze、Android 真机结果或共享代码编译通过写成 iOS 已修复。

如果现有能力在某端不存在，新需求不能静默跳过该端。先查 adapter/plugin/宿主注入；仍需隐藏、禁用、提示或替代流程时，这是用户可见产品决策，实施前询问用户。

## 3. 地图变更的候选矩阵

Tuqiang 地图任务至少按以下 7 个平台 × 后端候选单元逐项分类，而不是把四个后端家族名称压成四行，更不能当成一个 switch 的四个枚举值：

| 候选行 | 平台/target | 必查实现 |
|---|---|---|
| 1 | Android（`standard`） | 百度 Android 原生实现 |
| 2 | Android（`standard`） | 高德 Android 原生实现 |
| 3 | Android（`standard`） | Google Flutter/Android 实现 |
| 4 | iOS（`standard`） | 百度 iOS 原生实现 |
| 5 | iOS（`standard`） | 高德 iOS 原生实现 |
| 6 | iOS（`standard`） | Google Flutter/iOS 实现 |
| 7 | HarmonyOS（`ohos`） | 华为 Map Kit；对应用户所称“花瓣地图”，但不是源码 SDK 名；同时核对 BMap/AMap 兼容 factory id 到 OHOS View 的映射 |

支持三源的主地图 scene 默认保留这 7 行。共享 Dart 实现或同一测试证据可以在多行引用，但每行仍要单独说明平台原生差异；某 scene 不可达某行时，保留该行，以 `无需修改` 为代码状态并附 source、factory、route 或配置证据。

地图 Bug：

1. 在 7 个候选行中逐项排查是否可复现、是否共享错误逻辑、是否不可达，不能因 Android 与 iOS 使用同一逻辑 source 而合并两端；
2. Android 与 HarmonyOS 的适用分支必须修复并验证；共享 Dart 修复可以同时覆盖多个实现，但仍要逐项证明；
3. iOS 记录共享代码覆盖情况，并把 iOS 原生差异、构建与真机验证交接；
4. “当前默认地图源没有问题”不能代替其他源排查。

地图新需求：

1. 百度、高德、Google 与 HarmonyOS Map Kit 的可达实现都必须落地；
2. 同时标注当前 `TQMapUseSceneType`（定位、轨迹、围栏等），公共 protocol/option/callback 变化要反查其他 scene；
3. 坐标系、marker/polyline、回调、生命周期、资源与地图切换都属于实现面；只改 Flutter 覆盖层时也要证明各后端渲染/事件行为一致；
4. 某后端不支持需求语义时，先询问降级结果，不能留空或默认“不做”。

POI 搜索、街景、外部导航等独立地图能力按自己的 channel/宿主实现再建子矩阵，不能用主地图 Widget 已覆盖替代。

Laoying 不自动获得 Tuqiang 的三种标准端供应商。先服从当前 Product Scope 和宿主 adapter；仍要对目标 map scene 核对 Dart view id → Laoying OHOS resolver → 插件已注册 factory 的闭环，不能用 `location` 已接通推断 `overview`、`lineTrace`、`smartTrace`、`pointTrace`、`fence` 已接通。Laoying 新需求仍按 Android、iOS、HarmonyOS 三个平台分别建行；`laoying_standard` 只是一份共享宿主，不能合并 Android/iOS 的运行证据，供应商范围则只按 Product Scope。若需求要求扩大供应商范围而与契约冲突，必须请求用户决策。

## 4. 设备列表、详情与“更多详情”的强制提问

以下任一入口被需求命中时，先从当前源码枚举 route leaf：

- 设备列表点击设备；
- 设备搜索、绑定或其他会重新选择设备的入口；
- 设备首页/module page、设备详情、定位卡片；
- “更多详情”“设备详情”“更多设置”；
- 在线/离线/未激活、客服卡片、服务到期、分享设备等在详情族页面展示的状态。

枚举至少包含 `deviceType`、scene/category、cameraScene、服务/模式条件、route、最终 Page 和目标 Widget；同时核对父子 Gesture/InkWell 的真实点击区域，不能用“更多详情”文案或方法名推断下一跳。若实时枚举存在两个以上相互独立的 route/Page 或页面消费叶子，而用户没有明确“所有设备类型”或点名具体类型/场景，**在写代码前必须询问**，不能从共享组件、当前文件、截图、Bug 复现设备或第一个搜索命中推断范围。用户已明确唯一 route/Page 及设备场景，或源码只有一个叶子时，不重复提问。

推荐问题：

```text
当前源码中这个入口会分到 <列出已核验的设备类型/场景与页面族>。
本次需要覆盖所有设备类型/场景，还是只改指定类型？
如果只改单一类型，请确认 deviceType/scene/cameraScene（以及服务或激活状态）。
```

用户选择“全部”后，每个当前可达叶子都要进入覆盖表；选择单一类型后，只实现该业务分支，但仍检查共享组件、Provider、route 或 plugin 的修改是否会回归其他设备类型。

## 5. 覆盖台账

实施前创建简短台账，实施中更新，不要求写入仓库文件：

| 产品 | 变更类型 | 平台/target | 设备/场景 | route/Page | 地图 scene/实现 | 代码状态 | 验证状态/证据 |
|---|---|---|---|---|---|---|---|

代码状态只使用有明确含义的值：

- `已实现/已修复`；
- `共享实现覆盖`（给出共同 symbol 与各调用方）；
- `无需修改`（给出不可达或行为不受影响证据）；
- `待用户决定`；
- `iOS 专属实现待同事`（仅限 Bug 的 iOS 原生专属问题；新需求不得用此状态跳过代码实现）。

验证状态分开记录 `静态已验证`、`构建已验证`、`运行时已验证`、`未执行`、`已交接`。不得用 analyze 冒充 build/真机，也不得写“其余类似”关闭剩余行。

新需求的 iOS 行必须先达到 `已实现` 或有证据的 `共享实现覆盖`；可交接的是 Windows 本机无法完成的 iOS build、模拟器、真机和验收，不是代码实现本身。

## 6. 实施与评审完成条件

- [ ] 已分类 Bug/新需求/混合，并按对应三端基线工作；
- [ ] `standard` target 没有被当成 Android+iOS 两端运行时证明；
- [ ] Tuqiang 地图变更已关闭 Android/iOS 各三源与 HarmonyOS Map Kit 的 7 个候选行，不可达行使用 `无需修改` 并附源码证据；Laoying 地图变更只按当前 Product Scope、两个宿主 adapter 与实际 scene mapping 关闭；
- [ ] 设备详情族已先枚举 route leaf；范围不明确时已询问“全部还是指定类型”，确认前未写代码；
- [ ] 每个矩阵行都有代码状态和验证证据，`无需修改` 有源码依据；
- [ ] iOS 的共享代码覆盖、专属差异、未运行项和同事交接内容已分开说明。
