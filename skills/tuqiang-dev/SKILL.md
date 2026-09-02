---
name: tuqiang-dev
description: 为途强智能与老鹰在线共仓的 Flutter monorepo 提供开发、修复、测试与代码评审规范；适用于澄清用户可观察需求，确定产品与 owner，按当前源码修改状态、页面、路由、地图或平台能力，并用强制覆盖矩阵防止遗漏 Android/iOS/HarmonyOS、地图后端及设备类型/详情页变体。架构事实从 tuqiang-project-map 与当前源码核验，本 skill 负责实现与复用决策。
metadata:
  version: "1.13.0"
---

# 途强 Flutter 项目开发规范

本 skill 只服务当前途强 Flutter monorepo。仓库同时承载途强智能与老鹰在线两个产品、Android/iOS/HarmonyOS 三个平台和四个构建 target。目标是先锁定产品与 owner，沿用该产品当前实现方式，保持跨产品、跨 package 和平台边界，并完成最小、可验证的修改。`tuqiang-project-map` 负责“项目现在是什么、入口在哪里”的事实与架构上下文；本 skill 负责“应该改哪里、复用什么、怎样实现和验证”的开发决策。用户在完成后显式要求学习复盘时，由 `tuqiang-change-retrospective` 调查 Git 因果并生成 Markdown，本 skill 不在普通开发中自动产出复盘。

## 1. 解析仓库与事实优先级

`<TUQIANG_ROOT>` 是“本次任务已核验的仓库根目录”占位符，不是固定路径，也不能原样传给 shell。开工前必须按公共 [项目根目录发现协议](../tuqiang-project-map/references/project-root-discovery.md) 解析，不在本 Skill 复制一份容易过期的仓库 identity。用户明确路径优先；否则默认使用当前对话/任务绑定的项目或 workspace Git 根目录。选中、打开、附件或目标文件只作为该项目内的定位锚点，不得据此静默切换到另一份 checkout；仅在当前对话没有绑定项目或用户明确要求处理 workspace 外文件时，才从目标文件发现仓库。读取适用的 `AGENTS.md`，校验失败或无法唯一确认时停止写入并说明失败原因，不扫描整个磁盘或任意父目录，不硬编码历史路径。

先按 [需求澄清与用户决策门](references/requirement-clarification.md) 写清变更类型、用户可观察行为和可证伪验收标准，再按作为唯一规范源的 [跨端、地图实现与设备页面覆盖门](references/implementation-coverage.md) 建立候选矩阵。缺失信息会改变素材、文案、API、平台行为、owner/架构、公开契约或修改范围时，先询问用户，不得以模型偏好补全。

事实判断按维度进行：

1. 用户当前请求、项目 `AGENTS.md` 和明确验收结论决定本次授权、产品范围与业务范围；平台最低基线以 [implementation-coverage.md](references/implementation-coverage.md) 为唯一规范源，除非用户明确变更该组织规则或源码/Product Scope 证明某平台不适用；
2. 当前源码、各 package 的 `pubspec.yaml`/lockfile、测试、`tool/project.dart` 和 CI 决定实际运行结构；
3. 老鹰在线的产品范围、阻塞项和契约分别以 `docs/laoying/product_scope_matrix.md`、`route_contract.md`、`api_contract.md`、`resource_inventory.md`、`native_capability_matrix.md` 的当前状态为准；代码存在不代表产品已批准，设计图也不能覆盖 Product Scope；
4. `tool/check_migration_boundaries.ps1 -ProductScope <tuqiang|laoying|all>`、产品契约与当前有效测试决定依赖和资源边界；产品专属检查器先与当前 allowlist/源码交叉核验，已知基线误报不得冒充新改动失败；
5. [tuqiang-project-map](../tuqiang-project-map/SKILL.md) 中经当前源码复核的架构事实与 symbol 索引；
6. 本 skill 的 references；
7. 通用 Flutter 最佳实践。

兄弟 Skill 缺失不应阻塞已由公共协议唯一确认的仓库开发；不得自行恢复旧版 identity，更不得把已经冻结拆分的 `shared_business` 当作必需 package。地图记录的是事实上下文、symbol 与相对路径，不是永久行号、实现模板或修改授权，实施前必须在当前 checkout 重新检索。

迁移文档可能同时包含历史基线、目标设计和已完成记录。如果当前代码与目标不一致，按当前 owner 与相邻成熟实现工作；只有用户明确要求迁移时，才执行目标态清理。

## 2. 架构边界速查

```text
apps/standard ─┐                         apps/laoying_standard ─┐
               ├─> apps/tuqiang_app                            ├─> apps/laoying_app
apps/ohos ─────┘        ↓                apps/laoying_ohos ─────┘        ↓
                 feature_* → shared_*                    LY app-local business
                         \      /                              ↓
                       core / plugins / adapter / public shared_*
```

- `apps/standard`、`apps/ohos`：途强智能 Android/iOS 与 HarmonyOS 宿主；
- `apps/tuqiang_app`：途强智能启动、ProviderScope、跨 Feature 注入、路由聚合、session、首页与生命周期；
- `packages/feature/feature_*`：途强智能单一业务域的页面、状态、Repository、路由和资源；
- `packages/shared/shared_account|device|location|command|message|media|advertising|activity`：拆分后的稳定共享业务域；旧 `shared_business` 已冻结，不新增文件、依赖或 import；
- `apps/laoying_standard`、`apps/laoying_ohos`：老鹰在线标准端与 HarmonyOS 宿主；
- `apps/laoying_app/lib/app`：老鹰在线应用层。`auth/gps/pet/mine/overview/message/device_share/device_management` 是八个 app-local 业务 owner，`LYAppProvider`/`LYAppScope`、LY Router、Repository、资源与品牌配置也留在该产品；不新增 `feature_laoying*`，不 import 既有 `feature_*` 或 `package:tuqiang/` 业务入口；
- `packages/core/core_*`、`packages/plugins`、`packages/adapter`：两个产品可按公开 API 复用的基础和原生能力，产品身份、凭据、品牌资源及运行时配置仍隔离；
- `packages/assets_common`：途强智能共享资源；老鹰在线页面可见图片放 `apps/laoying_app/assets` 并经 `LYAppAssets`/业务 Resolver 使用，不能运行时引用途强 Feature 或 `assets_common` 图片。

依赖方向以 pubspec、当前 Product Scope 和边界测试为准：途强 `feature` 不依赖 app 或其他 feature 私有实现，拆分后的 `shared_*` 不反向依赖 feature；老鹰八个业务 owner 不互相直接 import，通过应用 Router、Coordinator 或 contract 协作。老鹰可复用 core/shared/plugin 的公开能力，不因 `TQ` 命名重复造底层实现，但不得泄漏途强 Feature、品牌资源或运行时配置。

完整层级、模块职责与源码入口按需读取：

- [项目根目录发现协议](../tuqiang-project-map/references/project-root-discovery.md)
- [架构总览](../tuqiang-project-map/references/architecture-overview.md)
- [模块目录](../tuqiang-project-map/references/module-catalog.md)
- [启动、ProviderScope 与路由](../tuqiang-project-map/references/startup-routing.md)
- [基础设施与横切能力](../tuqiang-project-map/references/infrastructure-and-cross-cutting.md)

## 3. 修改前先建立影响链

先确认目标产品，再对跨文件业务、状态、设备、路由或异步 Bug 建立最小影响图。用户选中的代码只是检索锚点；途强智能按 [需求追踪剧本](../tuqiang-project-map/references/requirement-trace-playbook.md) 追 Riverpod/Manager 链，老鹰在线则从 `LYAppProvider`/业务 ChangeNotifier、Router、Repository 与应用级 Coordinator 追踪：

```text
用户入口/路由/生命周期
→ Widget 事件或根 Coordinator
→ Command/Notifier/Manager/LY Controller
→ Repository/TQHttp/LYBackendHttpClient/缓存/插件
→ Riverpod State/LYAppProvider/ChangeNotifier/局部状态写入
→ derived Provider/listener/InheritedNotifier 通知
→ 最终 Widget 与副作用
→ invalidate/dispose/session reset
```

这份图不要求交付成长文，但必须足以回答：修改哪一个 owner、会影响哪些写入/消费端、哪个平台和生命周期需要验证。若追到后端、外部 SDK 或原生未知边界，明确停止点，不编造行为。

### 变更覆盖矩阵

影响链建立后、写代码前，必须按 [implementation-coverage.md](references/implementation-coverage.md) 分类并逐项关闭矩阵：

- Bug 修复的最低闭环是 Android + HarmonyOS；iOS 需要检查共享路径和专属差异，明确未运行/未验收及同事交接，不能用 Android 或 `standard` analyze 冒充；
- 新需求必须实现 Android + iOS + HarmonyOS；本机无法运行 iOS 只影响运行验证，不允许省略 iOS 代码或宿主差异；
- Tuqiang 地图 Bug 必须把 Android/iOS 各自的百度、高德、Google 与 HarmonyOS 华为 Map Kit 拆成 7 个平台 × 后端候选行；地图新需求在所有当前可达行落地。共享 Dart 证据可以复用，但不得合并掉平台行；用户所称“花瓣地图”只映射到当前 Map Kit 后端，不是源码 SDK 名，不虚构第四个 `TQMapSourceType`；
- 设备列表、设备首页/详情及“更多详情/更多设置”命中多个 device/scene/route leaf 时，用户未明确范围就必须先问“所有设备类型还是指定类型”，确认前不写代码。

覆盖表不机械生成平台 × 地图源 × 设备类型的笛卡尔积；设备与业务页面只列当前源码可达组合，Tuqiang 主地图则保留 7 个候选行。任何 `无需修改` 都必须给出 route、Product Scope、adapter 或调用证据，不能写“其余类似”。项目事实枚举见 [平台、地图后端与设备页面变体](../tuqiang-project-map/references/variant-surface.md)。

### 状态变更预检

途强智能最近扫描基线为 Riverpod 2.6.1；修改前先核对当前 `pubspec.yaml` 与 lockfile。它采用 Riverpod、Manager/单例、`setState`、`ValueNotifier`、直接 `TQHttp` 与插件状态并存的混合架构。老鹰在线当前业务代码不使用 Riverpod：应用会话与刷新由 `LYAppProvider`、`LYAppScope`、`LYUserSession` 和 `LYSessionResetCoordinator` 组织，各业务以 app-local ChangeNotifier Controller、Repository 和局部 Widget State 为主。不得把任一产品的状态模板套到另一个产品。

修改途强 Provider 或消费者前必须检查：

1. Provider 完整类型、State、Notifier、依赖和实际请求触发点；
2. family key 的来源、业务字段、不可变性、`==/hashCode`，以及同 key 复用/不同 key 隔离；
3. 路由参数、family 参数、Notifier 方法参数、State 字段是否被混淆；
4. 所有 `state =/seed/apply/update`、Manager/cache/局部状态写入源；
5. 所有 `watch/select/read/listen`、`ProviderContainer` 与最终 UI 消费端；
6. `autoDispose` 是否仍被根 Host 订阅，是否有 `keepAlive/onDispose`；
7. 切设备/切 key、`invalidate`、切语言和登出 session reset 是否覆盖；
8. `mounted`、generation/operation、Timer/Subscription/Controller 与并发旧响应保护；
9. ProviderScope override 的声明、app 注入与 Feature 调用是否成对。

修改老鹰状态时对应检查 Controller 的创建/持有者、`addListener/removeListener`、异步 generation、Repository 注入、`LYAppProvider.resetSession()` participant、`LYRefreshBus` 发布/订阅与 Widget dispose。详细规则见 [references/state-management.md](references/state-management.md)；途强真实拓扑与设备流另见 [Riverpod 拓扑](../tuqiang-project-map/references/riverpod-topology.md) 和 [设备/定位链路](../tuqiang-project-map/references/device-location-flow.md)。

## 4. “加东西放哪里”

- 途强智能页面、State、Controller/Notifier、Model、Repository、路由、私有组件与资源：放真实业务 owner 的 `feature_*`；
- 途强跨两个及以上 Feature、语义稳定的能力：放职责对应的 `shared_account/device/location/command/message/media/advertising/activity`，不得向冻结的 `shared_business` 新增代码或依赖；
- 老鹰在线八个业务域的页面、LY Model、Repository/Adapter、Controller、路由和资源：放 `apps/laoying_app/lib/app/<owner>/`；应用级 session、router、contracts、coordinators、i18n、infrastructure 和 skin 留在相应 app-local 目录；
- 网络、语言字典/locale/`.tr`、尺寸、无业务 UI、权限工具：优先复用对应 `core_*`；
- 由具体业务数据产生的多语言缓存由真实 Feature、拆分后的 `shared_*` 或 LY app-local owner 清理；途强由 `LanguageChangeCoordinator` 聚合，老鹰沿 `LYAppProvider`/业务 Controller 与自身偏好链处理，不能把业务缓存实现塞进 `core_i18n`；
- 地图、视频、P2P、推送、文件、信号、蓝牙等原生能力：先找现有 plugin/adapter/core；
- `apps/tuqiang_app/lib/app` 只承接 App 装配、路由聚合、session、平台注入和共享 App 壳；历史业务可以暂留，新可复用业务不要继续堆入 app；
- Feature 目录并不完全统一，先看当前 owner 的公开 barrel、相邻成熟模块和测试，不做无关脚手架重排。

详细归属见 [references/project-structure.md](references/project-structure.md)，局部风格采样与复用取舍见 [references/local-style-and-reuse.md](references/local-style-and-reuse.md)。

## 5. 双产品与三端边界

- 公共 Dart 代码不得泄漏 `Platform.isOhos`、`OhosView`、OHOS-only 包或定制 SDK 独有类型；
- HarmonyOS 差异按产品隔离：Tuqiang 可使用 bootstrap 已配置的 `AppTargetConfig.isOhos`，Laoying 由两个产品壳注入平台 adapter；公共层依赖抽象、callback/bridge，不读取某一产品的 target flag；
- 新增依赖先检查 OHOS override、现有 adapter、`core_*_ohos`、plugins 与锁文件；
- `standard`/`ohos` 与 `laoying_standard`/`laoying_ohos` 各有独立 pubspec、lockfile 和平台配置；同时记住一个 standard target 承载 Android+iOS，单次 analyze 不能替代两端运行时证据；
- 平台交付范围按变更类型执行：Bug 至少闭环 Android+HarmonyOS 并记录 iOS 影响/交接；新需求实现 Android+iOS+HarmonyOS。standard-only 能力若进入新需求公共路径，必须补 OHOS adapter 或请求用户决定可见降级，不能静默跳过；
- 途强与老鹰产品范围分别核对，不把“三端”扩大成“两产品全做”。变更途强 Feature contract、Provider override、route effect 或插件时检查 `standard` 与 `ohos`；变更老鹰 app-local contract、LY Router、原生 channel 或插件时检查 `laoying_standard` 与 `laoying_ohos`；改 core/shared/plugin 时先枚举两产品真实消费者，只有改动触及两产品调用或公共 contract 才检查四 target，否则验证已确认产品并给出另一产品不受影响证据；
- Tuqiang 地图标准端有百度/高德/Google 分支，OHOS 通过宿主映射使用华为 Map Kit；地图改动按当前 scene 和可达后端逐项核查，不把 OHOS 兼容 factory id 当成百度/高德原生实现；
- 老鹰的应用标识、签名/凭据、URL scheme/channel/authority、后端配置、品牌文案和图片必须独立。产品范围明确永久排除或延期的能力不得因途强已有实现而接入。

## 6. 实施工作流

1. 解析 `<TUQIANG_ROOT>`，读取适用的 `AGENTS.md`，按 [需求澄清与用户决策门](references/requirement-clarification.md) 确认变更类型、产品、用户可观察行为、验收标准和待决项；
2. 用项目地图和当前源码建立 [实施覆盖台账](references/implementation-coverage.md)：平台/target 是基线，地图实现和设备 route leaf 只在任务实际命中对应入口时展开，否则明确记为“不涉及”；设备详情族范围未明确时先询问，确认前不写代码；
3. 用当前 Product Scope、项目地图和源码确定正确 owner、层级、公开 API 与复用入口；同时核对调用方、状态图、路由、pubspec、资源、测试和平台注入点；
4. 在同一产品、同一 owner 内抽样 2–4 个成熟同类实现和相邻文件，分别记录命名、文件组织、状态、Model、Repository、Widget 与测试写法；老鹰不以途强 Feature 页面作为实现模板；
5. 以“同产品同 owner 的成熟实现 > 同产品相邻 owner > 允许复用的公开 core/shared/plugin 能力 > 全局通用”为证据优先级。样本冲突时沿当前 owner 中有真实调用方、测试和产品契约支持的模式，并记录选择依据；
6. 先复用语义一致的公开能力；只有多个真实消费者且职责稳定时才抽公共抽象。单点逻辑或抽象会引入 mode flag、透传 callback、转发 wrapper 时，保留 owner 内的小而直接实现；
7. 写出产品/owner、复用结论、采样依据、最小文件范围和可证伪验收标准；完成一次聚焦调查后仍有多种会改变用户可见结果或契约的合理方案时，立即询问用户，不继续扩大搜索或试探实现；
8. UI 有设计源时按设计与当前产品视觉体系对齐；无设计源时沿用同产品同类页面。业务图片缺失时按 [assets-guide.md](references/assets-guide.md) 请求素材，不擅自程序绘制或生成替代；
9. 动态接口未提供时不得编造 URL、字段或生产假数据；只有产品契约允许时才用当前个人端实现提取准确契约，预览/测试使用可注入 fake/unavailable Repository；
10. 保持既有路由字符串、arguments、返回值、栈行为、H5/scheme/push/native 语义；
11. 让业务规则、状态和数据访问留在真实 owner，跨包只暴露必要 contract；只做直接相关的最小改动，不为统一命名、目录或架构顺手重排存量；
12. 行为变化与适当验证一起完成，逐行更新覆盖台账；用 diff 证明没有漏改可达变体、冗长胶水、重复入口或无关扩散，不机械要求每个文件一份测试。

“项目主流风格”不是全仓投票结果。Provider、Model、Repository、Widget 可以分别沿用当前 owner 内不同的成熟模式；不得为了表面统一，把 `TQ`/`Tq`/无前缀、`StateNotifier`/`ChangeNotifier` 或旧/新目录一次性改成一套。完整采样和决策表见 [references/local-style-and-reuse.md](references/local-style-and-reuse.md)。

所有新写文本必须为 UTF-8 无 BOM。任何 endpoint、Token、密钥、证书、签名或生产配置只描述职责，不复制到 Skill、测试日志或回复。

## 7. 统一命令

四个宿主 target 的 pub get、analyze、test、run、build 统一走工具入口：

```powershell
dart run tool/project.dart pub-get standard --enforce-lockfile
dart run tool/project.dart analyze standard
dart run tool/project.dart pub-get ohos --enforce-lockfile
dart run tool/project.dart analyze ohos
dart run tool/project.dart pub-get laoying_standard --enforce-lockfile
dart run tool/project.dart analyze laoying_standard
dart run tool/project.dart pub-get laoying_ohos --enforce-lockfile
dart run tool/project.dart analyze laoying_ohos
dart run tool/project.dart run standard
dart run tool/project.dart run laoying_standard
dart run tool/project.dart build standard apk --debug
dart run tool/project.dart build ohos hap --debug
dart run tool/project.dart build laoying_standard apk --debug
dart run tool/project.dart build laoying_ohos hap --debug
```

`dart run tool/project.dart test <target>` 只在对应宿主目录运行 Flutter test。顶层 `run_migration_tests.ps1` 当前覆盖途强 app 与 packages，不覆盖 `apps/laoying_app` 自身测试；老鹰业务改动必须在该目录单独运行 analyze/test 和聚焦 architecture/contract tests。

当前 `apps/laoying_app/tool/check_app_boundaries.dart` 仍把 `package:core_ui/` 列为禁止项，但最新 `docs/laoying/dependency_allowlist.md` 已允许 core 公开 API，当前 App 也有合法 `core_ui` 调用。因此它只能作为已知基线诊断，修复规则前不得要求全绿，也不得把该误报归因给当前改动；每次仍应重新核验检查器与 allowlist 是否已对齐。详见 [references/testing.md](references/testing.md)。途强迁移测试：

```powershell
pwsh .\tool\run_migration_tests.ps1 -FlutterExecutable <对应端 Flutter 可执行文件>
```

`tool/check_migration_boundaries.ps1` 是支持 Product Scope 的架构门禁：只影响途强的改动用 `-ProductScope tuqiang`，只影响老鹰的改动用 `-ProductScope laoying`；当前消费者证据表明同时影响两产品或公共 contract 时才用 `-ProductScope all`，不能只凭文件位于 core/shared/plugin 选择 `all`。优先用 PowerShell 7；未运行时如实报告，不能用 analyze 冒充通过。

## 8. 风险分级验证

| 变更范围 | 最低验证 |
|---|---|
| 文档/注释/纯格式 | `git diff --check`，检查 UTF-8 与无误改 |
| 单个 Feature 的 Dart 逻辑 | 对应 package analyze + 相关单测 |
| 老鹰 app-local 业务逻辑 | `apps/laoying_app` analyze + 聚焦/全量 test + architecture/contract tests；检查对应 LY Controller/Repository/session |
| Provider family key/生命周期/状态写入 | 相关 Provider/Repository 测试 + 消费页面验证；检查切 key 和 reset |
| 设备列表/详情/更多详情 | 按已确认设备范围逐个验证 route leaf、最终 Page、状态分支与公共组件；范围不明时先询问，不进入实现 |
| Tuqiang 地图 | 当前 scene 下逐项验证 Android/iOS 各自的百度、高德、Google 与 HarmonyOS Map Kit；Bug 记录 7 个候选行的排查结论，新需求记录各当前可达行的实现证据 |
| Laoying 地图 | 服从当前 Product Scope，把 `laoying_standard` 再拆为 Android/iOS 平台行并加 HarmonyOS 行，逐项验证宿主注入、目标 scene 的 view id → resolver → 已注册 factory，不套用 Tuqiang 三供应商矩阵 |
| route/asset/package 边界/i18n manifest | ProductScope boundary + 对应 contract/解析测试；app-local 检查器仅在当前规则与 allowlist 一致时作为门禁 |
| core/shared/公共插件/依赖 | 先枚举两产品消费者；同时影响两产品调用或公共 contract 时跑四 target + `-ProductScope all`，否则验证已确认产品并记录另一产品不受影响证据 |
| 权限、MethodChannel、OHOS override、系统能力 | 静态验证 + 受影响端行为/真机验证 |
| App 构建、渠道、签名、DevEco | 走 `tool/project.dart`，记录未执行的 CI/签名步骤 |

本地无法执行完整构建或真机检查时，完成可行静态验证并明确“未执行”，不夸大结论。

## 9. 交付检查

- [ ] 目标产品、Product Scope、owner、依赖方向、state/route/asset 唯一来源正确；
- [ ] 变更已分类为 Bug/新需求/混合；用户可观察行为、可证伪验收与需用户决策项已明确；
- [ ] 已按规则覆盖 Android/iOS/HarmonyOS：Bug 的 Android+OHOS 闭环与 iOS 影响/交接清楚，新需求三端均有代码实现；
- [ ] 设备详情族已枚举 route leaf；用户未说明全部或指定设备类型时已先询问，未从单一页面擅自推断；
- [ ] Tuqiang 地图变更已逐项关闭 Android/iOS 各三源与 HarmonyOS Map Kit 的 7 个候选行，不可达行使用 `无需修改` 并附源码证据；Laoying 地图变更已按当前 Product Scope、两个宿主 adapter 与实际 scene mapping 关闭；两者均区分代码覆盖、静态/运行验证、无需修改与 iOS 交接；
- [ ] 缺素材或产品/API/平台口径时没有擅自补全；
- [ ] 已找到现有公开复用入口，并用目标 package 的 2–4 个成熟同类样本说明命名、目录及 Provider/Model/Repository/Widget 选择；
- [ ] 样本冲突的取舍有调用方、测试或当前 owner 证据，没有借需求顺手统一存量；
- [ ] 入口到数据源再到 UI 的影响链已核验，没有漏掉 Manager/cache/Timer/插件旁路；
- [ ] 途强 family key、写入源、消费者、autoDispose/invalidate/reset，或老鹰 `LYAppProvider`/Controller/listener/session reset 已按目标产品检查；
- [ ] 请求 DTO、响应 DTO、目标产品的 Result/failure/parser 与 null 语义符合真实接口；
- [ ] 目标产品的 i18n manifest、`.tr/keyTr/multiKeyTr`、`.sc`、core_ui 与资源 Resolver 按实际 API 使用；
- [ ] 异步竞态、mounted/generation、Controller/Timer/Subscription 释放正确；
- [ ] 途强 route/screen secure/route effect/跨 Feature callback，或老鹰 LY typed payload/result/checked registry 无意外变化；
- [ ] 覆盖台账每行都有可达证据、代码状态和验证状态；实际执行命令与未执行/交接项已记录；
- [ ] diff 只覆盖必要 owner，没有纯转发 wrapper、模式开关胶水、投机性公共抽象或无关重排；
- [ ] 未泄露敏感值，文本为 UTF-8 无 BOM；
- [ ] 未经用户明确要求，不执行 `git commit` 或 `git push`。

## 10. 参考文件索引

| 文件 | 什么时候读 |
|---|---|
| [references/requirement-clarification.md](references/requirement-clarification.md) | 修改前验收、需求多解、缺素材/契约和用户决策门 |
| [references/implementation-coverage.md](references/implementation-coverage.md) | Bug/新需求三端基线、Tuqiang 七个平台 × 地图后端候选单元、Laoying 产品边界、设备详情强制提问与覆盖台账 |
| [references/project-structure.md](references/project-structure.md) | 双产品 app/feature/shared/core/plugin owner 与迁移边界 |
| [references/local-style-and-reuse.md](references/local-style-and-reuse.md) | 目标 package 局部风格采样、复用/抽象/内联决策与可验证检查 |
| [references/state-management.md](references/state-management.md) | 途强 Riverpod 与老鹰 LYAppProvider/ChangeNotifier、生命周期、并发和 session reset |
| [references/networking.md](references/networking.md) | 途强 TQHttp 与老鹰 LYBackendHttpClient、Model、Repository 和配置隔离 |
| [references/routing.md](references/routing.md) | 途强 Feature route 与老鹰 LY checked registry/typed payload |
| [references/i18n.md](references/i18n.md) | 途强 9 语言与老鹰独立 zh/en bundle、切换清理 |
| [references/sizing-ui.md](references/sizing-ui.md) | `.sc`、SafeArea、core_ui 与布局 |
| [references/assets-guide.md](references/assets-guide.md) | 设计源、资源 owner、package asset 与倍率目录 |
| [references/testing.md](references/testing.md) | 按消费者证据选择 target/ProductScope、老鹰 app boundary 已知基线、单测与 migration runner |
| [references/permissions.md](references/permissions.md) | 权限申请、永久拒绝与 manifest |
| [references/compatibility.md](references/compatibility.md) | Android/iOS/OHOS 差异与插件选择 |
| [references/code-review-checklist.md](references/code-review-checklist.md) | 高风险缺陷审查 |
| [references/new-feature-walkthrough.md](references/new-feature-walkthrough.md) | 从需求、owner 到验证的最小实施清单 |
