---
name: tuqiang-dev
description: 为途强三端 Flutter monorepo 提供开发、修复、测试与代码评审规范；适用于确定 feature/shared/core owner，按目标 package 的局部主流风格修改 Riverpod、Model、Repository、Widget、路由、网络、i18n、尺寸或平台能力，并按 Android、iOS、HarmonyOS 风险验证。架构事实从 tuqiang-project-map 与当前源码核验，本 skill 负责实现与复用决策。
metadata:
  version: "1.11.0"
---

# 途强 Flutter 项目开发规范

本 skill 只服务当前途强 Flutter monorepo。目标是让修改落在正确 owner，沿用目标 package 的真实写法，保持三端边界，并完成最小、可验证的实现。`tuqiang-project-map` 负责“项目现在是什么、入口在哪里”的事实与架构上下文；本 skill 负责“应该改哪里、复用什么、怎样实现和验证”的开发决策。

## 1. 解析仓库与事实优先级

`<TUQIANG_ROOT>` 是“本次任务已核验的仓库根目录”占位符，不是固定路径，也不能原样传给 shell。开工前按 [项目根目录发现协议](../tuqiang-project-map/references/project-root-discovery.md) 解析：用户明确路径优先，其次复用本次任务已完整校验的根目录，再使用选中/目标文件所在 Git 仓库，最后使用当前 workspace 的 Git 根目录；随后核验三端宿主、共享业务包、`tool/project.dart` 和 package identity，并读取适用的 `AGENTS.md`。校验失败或无法唯一确认时停止写入并请求用户确认，不扫描整个磁盘或任意父目录。不得把解析结果写回 Skill，也不得硬编码另一份 checkout。

冲突时按以下顺序判断：

1. 项目 `AGENTS.md`、当前源码、各 package 的 `pubspec.yaml` 与 lockfile；
2. 测试、`tool/check_migration_boundaries.ps1`、`tool/run_migration_tests.ps1`、`tool/project.dart` 与 CI；
3. [tuqiang-project-map](../tuqiang-project-map/SKILL.md) 中经当前源码复核的架构事实与 symbol 索引；
4. `docs/` 中明确描述当前批次或已完成状态的内容；
5. 本 skill 的 references；
6. 通用 Flutter 最佳实践。

项目地图未安装时，独立降级也必须使用同一组完整身份条件，不能缩减成几个宽泛目录：

| 必须存在的文件 | `pubspec.yaml` 必须声明的 `name` |
|---|---|
| `apps/standard/pubspec.yaml` | `tuqiang_standard` |
| `apps/ohos/pubspec.yaml` | `tuqiang_ohos` |
| `apps/tuqiang_app/pubspec.yaml` | `tuqiang` |
| `packages/shared/shared_business/pubspec.yaml` | `shared_business` |
| `tool/project.dart` | 不适用 |

任一标志缺失、identity 不匹配或存在多个通过校验的候选时停止写入并请求用户确认。兄弟 Skill 缺失不应阻塞已唯一确认仓库中的开发；地图记录的是事实上下文、symbol 与相对路径，不是永久行号、实现模板或修改授权，实施前必须在当前 checkout 重新检索。

迁移文档可能同时包含历史基线、目标设计和已完成记录。如果当前代码与目标不一致，按当前 owner 与相邻成熟实现工作；只有用户明确要求迁移时，才执行目标态清理。

## 2. 架构边界速查

```text
apps/standard ─┐
               ├─> apps/tuqiang_app（composition root / App 壳）
apps/ohos ─────┘             ↓
                    feature_* → shared_business → core/plugins/adapter
```

- `apps/standard`：Android/iOS 平台入口与配置；
- `apps/ohos`：HarmonyOS 入口、平台实现与 dependency overrides；
- `apps/tuqiang_app`：启动、ProviderScope、跨 Feature 注入、路由聚合、session、首页与生命周期；
- `packages/feature/feature_*`：单一业务域的页面、状态、Repository、路由和资源；
- `packages/shared/shared_business`：跨 Feature 稳定复用的设备、定位、消息、账号、视频等业务能力；
- `packages/core/core_*`：HTTP、i18n、UI、尺寸、蓝牙、WebView 等无具体业务基础能力；
- `packages/plugins` / `packages/adapter`：原生能力与平台/三方适配；
- `packages/assets_common`：真正跨模块的公共资源。

依赖方向以 pubspec 和边界测试为准：上层可以依赖下层，`feature` 不依赖 app，`shared_business` 不依赖 feature，Camera/GPS 等 Feature 不应直接形成横向依赖。跨 Feature 导航与组合通过 contract/callback/provider，由 app composition root 注入。

完整层级、模块职责与源码入口按需读取：

- [项目根目录发现协议](../tuqiang-project-map/references/project-root-discovery.md)
- [架构总览](../tuqiang-project-map/references/architecture-overview.md)
- [模块目录](../tuqiang-project-map/references/module-catalog.md)
- [启动、ProviderScope 与路由](../tuqiang-project-map/references/startup-routing.md)
- [基础设施与横切能力](../tuqiang-project-map/references/infrastructure-and-cross-cutting.md)

## 3. 修改前先建立影响链

对跨文件业务、Riverpod、设备、路由或异步 Bug，用户选中的代码只是检索锚点。修改前按 [需求追踪剧本](../tuqiang-project-map/references/requirement-trace-playbook.md) 建立最小影响图：

```text
用户入口/路由/生命周期
→ Widget 事件或根 Coordinator
→ Command/Notifier/Manager
→ Repository/TQHttp/缓存/插件
→ State/Manager/局部状态写入
→ derived Provider / listener
→ 最终 Widget 与副作用
→ invalidate/dispose/session reset
```

这份图不要求交付成长文，但必须足以回答：修改哪一个 owner、会影响哪些写入/消费端、哪个平台和生命周期需要验证。若追到后端、外部 SDK 或原生未知边界，明确停止点，不编造行为。

### Riverpod 变更预检

最近扫描基线为 Riverpod 2.6.1；修改前先核对当前 `pubspec.yaml` 与 lockfile。项目采用混合架构，主要是手写 `Provider`、`StateNotifierProvider`、family/autoDispose，少量 `NotifierProvider`、`FutureProvider`；同时存在 Manager/单例、`setState`、`ValueNotifier`、直接 `TQHttp` 与插件状态。

修改任何 Provider 或消费者前必须检查：

1. Provider 完整类型、State、Notifier、依赖和实际请求触发点；
2. family key 的来源、业务字段、不可变性、`==/hashCode`，以及同 key 复用/不同 key 隔离；
3. 路由参数、family 参数、Notifier 方法参数、State 字段是否被混淆；
4. 所有 `state =/seed/apply/update`、Manager/cache/局部状态写入源；
5. 所有 `watch/select/read/listen`、`ProviderContainer` 与最终 UI 消费端；
6. `autoDispose` 是否仍被根 Host 订阅，是否有 `keepAlive/onDispose`；
7. 切设备/切 key、`invalidate`、切语言和登出 session reset 是否覆盖；
8. `mounted`、generation/operation、Timer/Subscription/Controller 与并发旧响应保护；
9. ProviderScope override 的声明、app 注入与 Feature 调用是否成对。

项目真实拓扑与设备流见 [Riverpod 拓扑](../tuqiang-project-map/references/riverpod-topology.md) 和 [设备/定位链路](../tuqiang-project-map/references/device-location-flow.md)。具体编码规则见 [references/state-management.md](references/state-management.md)。

## 4. “加东西放哪里”

- 页面、State、Controller/Notifier、Model、Repository、路由、私有组件与资源：放真实业务 owner 的 `feature_*`；
- 跨两个及以上 Feature、语义稳定的实体、Provider、Manager 或 contract：才考虑 `shared_business`；
- 网络、语言字典/locale/`.tr`、尺寸、无业务 UI、权限工具：优先复用对应 `core_*`；
- 由具体业务数据产生的多语言缓存仍由该 Feature 或 `shared_business` owner 提供清理 primitive/participant；`apps/tuqiang_app` 的 `LanguageChangeCoordinator` 只负责跨 Feature 聚合与执行顺序，不能把业务缓存实现塞进 `core_i18n`；
- 地图、视频、P2P、推送、文件、信号、蓝牙等原生能力：先找现有 plugin/adapter/core；
- `apps/tuqiang_app/lib/app` 只承接 App 装配、路由聚合、session、平台注入和共享 App 壳；历史业务可以暂留，新可复用业务不要继续堆入 app；
- Feature 目录并不完全统一，先看当前 owner 的公开 barrel、相邻成熟模块和测试，不做无关脚手架重排。

详细归属见 [references/project-structure.md](references/project-structure.md)，局部风格采样与复用取舍见 [references/local-style-and-reuse.md](references/local-style-and-reuse.md)。

## 5. 三端边界

- 公共 Dart 代码不得泄漏 `Platform.isOhos`、`OhosView`、OHOS-only 包或定制 SDK 独有类型；
- HarmonyOS 差异通过 `AppTargetConfig.isOhos`、adapter、公共抽象、callback/bridge 或 app 启动注入隔离；
- 新增依赖先检查 OHOS override、现有 adapter、`core_*_ohos`、plugins 与锁文件；
- Standard 与 OHOS 可有不同 lockfile。只更新受影响端，检查无关依赖漂移；
- standard-only 插件不自动要求补 OHOS 实现；先判断能力是否进入公共路径，再决定适配范围；
- 变更跨 Feature contract、Provider override、route effect 或插件时，Standard 与 OHOS 的 composition root 都要检查。

## 6. 实施工作流

1. 解析 `<TUQIANG_ROOT>`，读取适用的 `AGENTS.md`；用项目地图建立 owner 候选、模块边界与调用上下文，再用当前源码复核；
2. 先确定正确 owner、层级、公开 barrel/API 与现有复用入口；同时核对调用方、Provider 图、路由、pubspec、资源、测试和平台注入点；
3. 在目标 package 内抽样 2–4 个成熟同类实现和相邻文件，分别记录命名、文件组织、Provider、Model、Repository、Widget 与测试写法；
4. 以“同一子域/目标 package 的成熟同类实现 > 同层 sibling feature > 全局通用”为证据优先级。样本冲突时沿当前 owner 中较新且有真实调用方或测试的模式，并记录选择依据；
5. 先复用语义一致的公开能力；只有多个真实消费者且职责稳定时才抽公共抽象。单点逻辑或抽象会引入 mode flag、透传 callback、转发 wrapper 时，保留 owner 内的小而直接实现；
6. 写出 owner、复用结论、采样依据、最小文件范围和可证伪验收标准；只有业务歧义或会改变产品/架构方向时再向用户确认；
7. UI 有设计源时按设计与现有 core_ui 对齐；无设计源时沿用同类页面，不凭空创建另一套视觉体系；
8. 动态接口未提供时不得编造 URL 或生产假数据；预览/测试使用可注入 fake Repository；
9. 保持既有路由字符串、arguments、返回值、栈行为、H5/scheme/push/native 语义；
10. 让业务规则、状态和数据访问留在真实 owner，跨包只暴露必要 contract；只做直接相关的最小改动，不为统一命名、目录或架构顺手重排存量；
11. 行为变化与适当验证一起完成，不机械要求每个文件一份测试，并用 diff 证明没有冗长胶水、重复入口或无关扩散。

“项目主流风格”不是全仓投票结果。Provider、Model、Repository、Widget 可以分别沿用当前 owner 内不同的成熟模式；不得为了表面统一，把 `TQ`/`Tq`/无前缀、`StateNotifier`/`ChangeNotifier` 或旧/新目录一次性改成一套。完整采样和决策表见 [references/local-style-and-reuse.md](references/local-style-and-reuse.md)。

所有新写文本必须为 UTF-8 无 BOM。任何 endpoint、Token、密钥、证书、签名或生产配置只描述职责，不复制到 Skill、测试日志或回复。

## 7. 统一命令

App 的 pub get、analyze、run、build 统一走工具入口：

```powershell
dart run tool/project.dart pub-get standard --enforce-lockfile
dart run tool/project.dart analyze standard
dart run tool/project.dart pub-get ohos --enforce-lockfile
dart run tool/project.dart analyze ohos
dart run tool/project.dart run standard
dart run tool/project.dart build standard apk --debug
dart run tool/project.dart build ohos hap --debug
```

`dart run tool/project.dart test <target>` 只在对应 app 目录运行 Flutter test，不等于完整迁移测试。完整迁移测试：

```powershell
pwsh .\tool\run_migration_tests.ps1 -FlutterExecutable <对应端 Flutter 可执行文件>
```

`tool/check_migration_boundaries.ps1` 是架构门禁；优先用 PowerShell 7。若环境/编码导致未运行，必须如实报告，不能用 analyze 冒充通过。

## 8. 风险分级验证

| 变更范围 | 最低验证 |
|---|---|
| 文档/注释/纯格式 | `git diff --check`，检查 UTF-8 与无误改 |
| 单个 Feature 的 Dart 逻辑 | 对应 package analyze + 相关单测 |
| Provider family key/生命周期/状态写入 | 相关 Provider/Repository 测试 + 消费页面验证；检查切 key 和 reset |
| route/asset/package 边界/i18n manifest | boundary script + 对应 contract/解析测试 |
| core/shared/公共插件/依赖 | standard + OHOS analyze + boundary；必要时 migration tests |
| 权限、MethodChannel、OHOS override、系统能力 | 静态验证 + 受影响端行为/真机验证 |
| App 构建、渠道、签名、DevEco | 走 `tool/project.dart`，记录未执行的 CI/签名步骤 |

本地无法执行完整构建或真机检查时，完成可行静态验证并明确“未执行”，不夸大结论。

## 9. 交付检查

- [ ] owner、依赖方向、Provider/route/asset 唯一来源正确；
- [ ] 已找到现有公开复用入口，并用目标 package 的 2–4 个成熟同类样本说明命名、目录及 Provider/Model/Repository/Widget 选择；
- [ ] 样本冲突的取舍有调用方、测试或当前 owner 证据，没有借需求顺手统一存量；
- [ ] 入口到数据源再到 UI 的影响链已核验，没有漏掉 Manager/cache/Timer/插件旁路；
- [ ] family key、所有写入源、所有消费者、autoDispose/keepAlive/invalidate/reset 已检查；
- [ ] 请求 DTO、响应 DTO、`ResultModel/TCheck<T>` 与 null 语义符合真实接口；
- [ ] `.tr/keyTr/multiKeyTr`、`.sc` 与 core_ui 按实际 import/API 使用；
- [ ] 异步竞态、mounted/generation、Controller/Timer/Subscription 释放正确；
- [ ] route、返回值、screen secure、route effect 与跨 Feature callback 无意外变化；
- [ ] 受影响平台和实际执行的命令已记录；
- [ ] diff 只覆盖必要 owner，没有纯转发 wrapper、模式开关胶水、投机性公共抽象或无关重排；
- [ ] 未泄露敏感值，文本为 UTF-8 无 BOM；
- [ ] 未经用户明确要求，不执行 `git commit` 或 `git push`。

## 10. 参考文件索引

| 文件 | 什么时候读 |
|---|---|
| [references/project-structure.md](references/project-structure.md) | feature/core/shared/app/plugin owner 与迁移边界 |
| [references/local-style-and-reuse.md](references/local-style-and-reuse.md) | 目标 package 局部风格采样、复用/抽象/内联决策与可验证检查 |
| [references/state-management.md](references/state-management.md) | Provider 选择、family key、生命周期、并发与 session reset |
| [references/networking.md](references/networking.md) | TQHttp、ResultModel、TCheck、Model 与 Repository |
| [references/routing.md](references/routing.md) | 命名路由、Feature owner、native route 与 route effect |
| [references/i18n.md](references/i18n.md) | `.tr/keyTr/multiKeyTr`、9 语言与切换清理 |
| [references/sizing-ui.md](references/sizing-ui.md) | `.sc`、SafeArea、core_ui 与布局 |
| [references/assets-guide.md](references/assets-guide.md) | 设计源、资源 owner、package asset 与倍率目录 |
| [references/testing.md](references/testing.md) | 单测、Widget/contract test 与 migration runner |
| [references/permissions.md](references/permissions.md) | 权限申请、永久拒绝与 manifest |
| [references/compatibility.md](references/compatibility.md) | Android/iOS/OHOS 差异与插件选择 |
| [references/code-review-checklist.md](references/code-review-checklist.md) | 高风险缺陷审查 |
| [references/new-feature-walkthrough.md](references/new-feature-walkthrough.md) | 从需求、owner 到验证的最小实施清单 |
