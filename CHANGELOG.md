# Changelog

本仓库所有重要变更记录于此。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，遵循语义化版本。

## [Unreleased]

## [1.13.0] - 2026-09-01

### Added
- `tuqiang-project-map` 增加双产品识别与事实路由：先区分途强 `standard/ohos/tuqiang_app` 和老鹰在线 `laoying_standard/laoying_ohos/laoying_app`，再选择各自的 App composition、状态体系、路由、网络、资源和测试证据；同步收录 `tool/project.dart` 的四个 target 及边界脚本的 `all/tuqiang/laoying` 产品 scope。
- `tuqiang-dev` 新增需求澄清与决策门 reference：先写清用户可观察行为和可证伪验收标准；完成一次 owner、contract 与 2–4 个同类样本的聚焦调查后仍有多种合理实现，或素材、文案、数据契约、平台范围、公开 API、owner/架构及修改范围需要用户取舍时，必须在写代码前立即请求决策。
- 静态资源规范增加“业务素材保持素材语义”规则：语言、状态或主题变化要求替换图片时使用独立 asset 变体；缺少目标 PNG/SVG 时先向用户或设计方索要，未经明确授权不得用 Canvas、CustomPainter、TextPainter、文字叠加、系统图标、emoji、AI 或其他程序生成方式代替。

### Changed
- 四个 Skill 统一把用户显式路径之后的默认候选改为“当前对话/任务绑定项目的 Git 根目录”；选中、打开、附件或目标文件仅作为项目内定位锚点，不得静默切换到另一个 checkout，冲突时列出候选与失败原因并请求确认。
- 仓库身份验证改用稳定的 App 宿主、`tool/project.dart` 与 package identity；业务 package 清单从当前 pubspec、源码与门禁动态发现，不再把迁移中的单一 shared 聚合包当作永久仓库指纹。
- 依据 2026-09-01 当前源码重建项目事实：原 `shared_business` 已拆为 `shared_account`、`shared_activity`、`shared_advertising`、`shared_command`、`shared_device`、`shared_location`、`shared_media` 与 `shared_message`，遗留 app 能力回到 `apps/tuqiang_app/lib/app/legacy_shared`，设备/定位/媒体与 session contract 的路径、symbol 和依赖边界全部重新索引。
- 启动、路由与状态说明按真实产品线分流：途强继续追 `ProviderScope`、Riverpod family、`AppRouters` 与 Feature contracts；老鹰在线追 `LYAppProvider`、`LYAppScope`、app-local controller/repository、`LYAppRouter/LYAppRouteRegistry`、八个业务 owner 与独立资源 resolver，禁止把两套架构互相套用。
- 网络、国际化、资源、平台与验证规则改为产品感知：途强使用 `TQHttp/ResultModel/TCheck` 和 9 语言 manifest；老鹰在线使用自身 backend client、2 语言 manifest、app-local assets/typed route contract 与独立边界测试；统一命令覆盖 `standard`、`ohos`、`laoying_standard`、`laoying_ohos`。
- `tuqiang-project-map` 升级至 1.2.0，`flutter-to-web` 升级至 1.7.0，`tuqiang-dev` 升级至 1.12.0，`tuqiang-change-retrospective` 升级至 1.1.0，根包升级至 1.13.0；同步根 README 与四个 Skill README。

### Fixed
- 修复最新 checkout 因不存在的 `packages/shared/shared_business/pubspec.yaml` 被四个 Skill 错误判定为“非途强仓库”，继而回退到其他机器历史路径或错误 checkout 的根因。
- 修复开发流程仅在“业务或架构歧义”时才询问的过窄门槛，避免模型自行补全素材、交互、文案、接口 null 语义、平台范围或验收标准；调查无法收敛时不再用扩大搜索或试探性实现代替用户决策。
- 修复图片需求被擅自改写为运行时绘制的问题；例如非中文起点/终点要求 `S/E` 图标但缺少目标 PNG 时，默认动作是索要对应资源并建立语言到 asset 的映射，而不是在原图上绘字。
- 修复把老鹰 `check_app_boundaries.dart` 当作必须全绿门禁的错误；当前检查器仍禁止已被最新 allowlist 和源码正式采用的 `core_ui`，因此规则修复前只记录为已知基线诊断，实际边界由 ProductScope 与聚焦 architecture/contract tests 验证。
- 移除 `AGENTS.md` 全局同步说明中的具体用户名示例，统一使用当前进程的 `$env:USERPROFILE`，避免换电脑后同步到不存在或无权限的用户目录。

## [1.12.0] - 2026-08-30

### Added
- 新增 `tuqiang-change-retrospective` 1.0.0 变更复盘 Skill，支持 Bug、需求与混合三种完成后复盘模式；只在用户显式调用时运行，只创建学习 Markdown，不修改业务源码或 Git 历史。
- 新增 `references/git-causality.md`：以修复前错误版本为调查基线，使用 status/diff/log `-S/-G`/blame/show 等只读证据，区分缺陷引入、问题暴露、修复改动与防线缺失，并按“已确认/高度可能/候选/无法确定”标注置信度。
- 新增 `references/bug-retrospective.md` 与 `references/feature-retrospective.md`：分别提供 Bug 因果栈、排查/解决/预防剧本，以及需求价值金字塔、owner/取舍、输入输出血缘和事件/异步/状态/UI 三泳道复盘；混合模式可在一份需求文档中嵌入 Bug 卡。
- 新增 `references/report-contract.md`：约束完整 Markdown 的模式化结构、默认 `docs/learning/` 路径、无覆盖命名、仓库相对源码证据、UTF-8 无 BOM、验证状态和初学者复习问题。
- 新增 `agents/openai.yaml`，设置 `allow_implicit_invocation: false`，确保普通开发、解释或评审不会自动写入复盘文件。

### Changed
- 根包升级至 1.12.0，增加第 4 个 Skill 的 package 元数据、检索关键词、四 Skill 协作图、安装说明、显式调用模板、复盘验收清单与 FAQ。
- `tuqiang-project-map` 升级至 1.1.1，明确向变更复盘提供当前 owner、调用链和状态拓扑事实；`flutter-to-web` 升级至 1.6.1，明确向复盘提供 Dart/Vue3/React 对照而不负责 Git 归因；`tuqiang-dev` 升级至 1.11.1，明确普通开发不自动生成复盘。
- 新 Skill 默认把文章组织为“结论/价值 → 行为与规则 → 模块、状态与数据 → 源码、提交、测试证据”的金字塔；同步函数使用调用栈，异步请求与响应式 UI 更新改用独立时间泳道。
- 根据 Bug 与需求双场景前向测试收敛输出契约：完整性以证据链闭环为准，同一事实和源码只展开一次，其他章节通过步骤号或小节引用，避免初学者复盘因模板重复而失控增长。

### Fixed
- 防止把 `git blame`、最近提交、作者、首次报错时间或“当前已经修好”直接写成历史 Bug 根因；引入/暴露/修复分别标注置信度，未提交改动明确记录为“当前工作区改动，尚无对应提交”，历史不足时保留未知边界。
- 防止把 `await` 返回、Provider 通知和 Widget 重建错误描述为一条连续同步调用栈，并要求 Dart、Vue3、React 对照使用同一业务字段和步骤。
- 防止复盘覆盖已有学习文档、写入机器专属绝对路径、复制整文件源码或泄露 endpoint、Token、证书与生产配置。

## [1.11.0] - 2026-08-30

### Added
- `tuqiang-project-map` 新增 `references/project-root-discovery.md`：按用户路径、选中文件仓库和当前 workspace 解析 `<TUQIANG_ROOT>`，再用三端宿主、共享业务包、项目工具及四个 pubspec package identity 校验仓库；失败或多候选时请求确认，不扫描磁盘。
- `flutter-to-web` 新增 `references/project-root-resolution.md`：优先复用项目地图的根目录结果，并保留兄弟 Skill 不可用时的独立源码定位能力；所有最终路径和行号均来自当前 checkout。
- `tuqiang-dev` 新增 `references/local-style-and-reuse.md`：建立目标 package 的 2–4 个成熟同类样本、局部风格证据优先级、复用决策阶梯、反过度抽象规则及可执行 diff/重复入口检查。

### Changed
- `tuqiang-project-map` 升级至 1.1.0，明确定位为供教学与开发 Skill 使用的“项目事实与架构索引层”，输出分层、owner、状态/数据拓扑、公共封装、复用候选、同层样本与业务链证据；设备/定位仅作为按需读取的代表性链路。
- `flutter-to-web` 升级至 1.6.0，默认从用户操作或页面入口开始，分别恢复事件/同步调用、异步数据、状态依赖/UI 重建三条链；每个关键状态必须说明定义、route/family/action 参数、key 身份、依赖、全部写入、读取消费与生命周期，并提供逐跳 Dart 证据及 Vue3/React 端到端代码。
- `tuqiang-dev` 升级至 1.11.0，将“项目主流风格”收敛为同一子域/目标 package 的局部证据：优先真实调用方、测试和公开 API，不借需求统一 `TQ`/`Tq`/无前缀、状态架构或历史目录；实现遵循正确 owner、复用优先但不强行抽象、高内聚低耦合和最小影响面。
- 根包升级至 1.11.0，并同步三个 Skill README、根 README、目录索引、职责图和 package 元数据。

### Fixed
- 移除三个 Skill、README、命令和输出示例中的机器绝对路径依赖，并统一独立降级时的候选优先级、五个结构标志、四个 package identity 与歧义停止条件，修复公司与家庭 checkout 不同或兄弟 Skill 缺失时的误检索风险。
- 修复项目地图容易被误解为设备/GPS 专用 Skill 的职责偏差，明确它服务整个 monorepo 的架构分层、代码归属、通用能力、状态拓扑和业务索引。
- 修复完整需求讲解仍可能围绕选中代码局部展开的问题，强制追到真实操作入口、数据边界、状态写入、响应式消费者和最终 Widget，并区分同步栈、异步流与重建链。
- 修复“全仓统一代码风格”会带来的无关重构与协作噪音，改为按 owner 局部采样并拒绝纯转发 wrapper、模式开关胶水和无真实消费者的投机性公共抽象。
- 修复国际化清理 owner 的歧义：`core_i18n` 只承载语言基础设施，Feature/shared owner 暴露自身缓存清理 primitive，App `LanguageChangeCoordinator` 负责跨 Feature 聚合与执行顺序。

## [1.10.0] - 2026-08-30

### Added
- 新增 `tuqiang-project-map` 1.0.0 项目事实 Skill，按渐进披露拆分架构与依赖、模块职责、启动与路由、Riverpod 拓扑、设备/定位完整链路、基础设施与横切能力、需求追踪剧本。
- `flutter-to-web` 新增 `references/full-flow-tracing.md`，建立“用户操作 → 调用链 → 数据源 → 状态写入 → 消费端 → 最终 UI”的金字塔输出契约，并强制给出实时绝对路径、行号、Dart 源码及 Vue3/React 端到端对照。
- 两个原有 Skill 增加 `tuqiang-project-map` 的按需引用与源码直查降级能力，形成“项目事实层 → 教学解释层 / 开发执行层”的单向协同。

### Changed
- `flutter-to-web` 升级至 1.5.0：完整需求默认把选中代码当作检索锚点，分别追踪同步/异步调用链与状态重建链，展开 ProviderScope override、family key、全部写入源、全部消费者、生命周期和非 Riverpod 旁路。
- `tuqiang-dev` 升级至 1.10.0：修改 Riverpod、路由、设备或异步逻辑前必须建立跨文件影响图，检查 family 相等性、根 Host 保活、并发保护、切设备、切语言与 session reset。
- 依据 `D:/Code/Flutter` 当前源码重新整理三端壳、App composition root、Feature/Shared/Core/Plugin owner、命名路由、设备目录与定位状态、TQHttp、持久化、国际化和 `.sc` 缩放事实。
- 三个 Skill 的 frontmatter 版本统一迁移到标准兼容的 `metadata.version`，同步更新根包至 1.10.0、三个 README、AGENTS 维护说明与 package 元数据。

### Fixed
- 修复所有生效文档仍指向不存在的旧项目路径 `D:/Code/tuqiang`，改为先解析并验证当前 monorepo，默认候选为 `D:/Code/Flutter`。
- 修复全局同步规则硬编码不存在且无权限的 `C:/Users/admin`，改为当前操作系统用户的 `%USERPROFILE%/.gemini/config/skills`。
- 移除“ProviderScope/main/路由等胶水直接跳过”“整份解释限制 5–15 行”和强制吐槽等会截断真实业务链的规则。
- 修复 Riverpod “build 里只准 watch”绝对口诀，补全 family 参数作为实例缓存键、对象相等性、多写入源、autoDispose/keepAlive/invalidate 与实际根订阅语义；明确切设备时显式清理的是旧设备 core family 与目标设备残留 location context。
- 修复 `keyTr` 示例错误：该 API 只替换 `{key}`，自定义命名占位符应使用 `multiKeyTr`；拆分资源字典 key、Flutter Locale 与后端 languageCode 三套语言标识；同时清理历史 CHANGELOG 中的异常控制字符。

## [1.9.0] - 2026-08-26

### Added
- `flutter-to-web` 增加 D:/Code/tuqiang 项目事实层：以实际的 Riverpod 2.6.1、命名路由、TQHttp、core_i18n、.sc 和 core_ui 为解释上下文。
- 两个 skill 增加事实来源优先级和协同边界：`tuqiang-dev` 负责项目技术决策，`flutter-to-web` 负责 Vue/React 视角的概念解释。

### Changed
- `skills/tuqiang-dev/SKILL.md`：将固定审批式流程改为按风险执行，补充当前/迁移目标区分、实际命令入口、lockfile 处理和验证矩阵。
- `skills/tuqiang-dev/references/assets-guide.md`：修正 `TQAppBar`、package asset 路径写法、资源 owner 和 3.0x 现状，取消无依据的 2.0x 强制要求。
- `skills/tuqiang-dev/references/testing.md`：改为按行为选择测试，补充 `run_migration_tests.ps1` 与 boundary runner 的真实职责。
- `skills/tuqiang-dev/references/networking.md`：区分请求/响应 Model 的 null 语义，禁止生产假数据，改为 fake 注入和 TQHttp 边界说明。
- `skills/tuqiang-dev/references/state-management.md`：反映 StateNotifier、NotifierProvider、FutureProvider 共存现状，细化 mounted、初始化和 session reset 规则。
- `skills/tuqiang-dev/references/project-structure.md`、`routing.md`、`i18n.md`、`sizing-ui.md`、`compatibility.md`：按当前 feature owner、命名路由、9 语言、尺寸和三端边界校准。
- `skills/tuqiang-dev/references/code-review-checklist.md`：删除低价值的导入/换行伪红线，保留异常、异步、类型、平台、资源和路由等高风险检查。
- `skills/tuqiang-dev/references/new-feature-walkthrough.md`：改为最小实施清单，修正 i18n key 示例、测试入口和接口未就绪处理。
- `skills/flutter-to-web/references/async-networking.md`、`state-and-riverpod.md`、`routing.md`、`layout-ui.md`：将通用类比改为兼容途强项目实际依赖和命名路由的解释。
- 同步更新根 README、两个 skill README 和 package 元数据版本。

### Fixed
- 修正原先把 `dart run tool/project.dart test standard` 描述为完整迁移测试的问题。
- 修正 `CommonAppBar`、英文 i18n key、生产 `Future.delayed` Mock、Riverpod “只允许 StateNotifier”以及 go_router 与途强命名路由的误导。

## [1.8.0] - 2026-08-25

### Added
- `skills/tuqiang-dev/references/code-review-checklist.md`：新增【代码审查高频缺陷对照清单】参考文档，收录 8 项真实代码审查中反复出现的缺陷模式：
  - **静默 catch（🔴 吞异常）**：`catch (_) {}` 必须改为 debugPrint + HTTP 层 showErrorToast；
  - **双重非空断言 `!.`（🔴 运行时崩溃）**：连续 `!.` 必须改为先 `?? ''` 取值再判断；
  - **`canLaunchUrl` + `launchUrl` 双检查（TOCTOU）**：移除预检查，直接 `launchUrl` + catch 兜底；
  - **宽类型参数 + 运行时 `is` 判断**：`List<dynamic>` 改为具体泛型 `List<Map<String, dynamic>>`；
  - **Widget 布尔参数与回调耦合**：`showCopy` + `onCopy` 两态合一，用 `onCopy != null` 推断；
  - **为单个函数导入整个库**：`dart:math` 的 `max` 用三元表达式替代；
  - **i18n JSON 文件末尾缺换行**：`tail -c 1` 检查并补 `0a`；
  - **State getter 死代码**：未使用的便捷 getter 按 YAGNI 删除或统一使用；
  - **💡 页面 loading 闪烁**：手动 `TQLoading.show()` 推荐改用 State 内嵌 loading。
- `skills/tuqiang-dev/SKILL.md`：
  - 在【阶段五：交付与审查】防御性自检清单中新增「代码审查高频缺陷」自检项；
  - 在【参考文件索引】中新增 `code-review-checklist.md` 条目。

### Changed
- `skills/tuqiang-dev` 版本升级至 `1.8.0`；
- 根目录 `package.json` 版本升级至 `1.8.0`；
- 更新 `skills/tuqiang-dev/README.md` 与根目录 `README.md` 中的 references 索引。

## [1.7.0] - 2026-08-25

### Added
- `skills/tuqiang-dev/references/state-management.md`：新增【生命周期防修改红线（极其重要，违者必崩）】规范与标准代码：
  - **生命周期防修改红线**：严禁在 `initState` 或 `build` 阶段直接同步触发修改 Provider 状态的方法（例如在 `initState` 里直接调 `controller.fetchData()` 且方法内同步执行了 `state = state.copyWith(...)`），杜绝 Flutter 运行时 `Tried to modify a provider while the widget tree was building.` 严重崩溃；
  - **标准解法与代码示例**：明确唯一正确写法为必须包裹在 `WidgetsBinding.instance.addPostFrameCallback((_) { ... })` 中，将修改推迟至首帧渲染挂载完成之后；
- `skills/flutter-to-web/references/state-and-riverpod.md`：在常见疑问答疑中新增【为什么在 `initState` 里调请求会报 `Tried to modify a provider...` 崩溃？】大白话解答（类比 Web 挂载计算首帧 DOM 时的生命周期死锁与 `nextTick` 解决机制）；
- `skills/tuqiang-dev/SKILL.md`：
  - 在【阶段五：交付与审查】Checklist 中新增「生命周期与 Provider 赋值红线」自检项；
  - 在【参考文件索引】中更新 `state-management.md` 描述。

### Changed
- `skills/tuqiang-dev` 版本升级至 `1.7.0`；
- `skills/flutter-to-web` 版本升级至 `1.3.0`；
- 根目录 `package.json` 版本升级至 `1.7.0`；
- 更新根目录 `README.md` 与 `skills/tuqiang-dev/README.md` 中的版本与文档说明。

## [1.6.0] - 2026-08-25

### Added
- skills/tuqiang-dev/references/assets-guide.md：升级为 UI 设计源决策、蓝湖 MCP 接入与静态资源切图全景规范：
  - **UI-First SOP 决策闭环**：新页面/UI 功能开工前，强制主动询问用户是否有蓝湖设计稿链接；
  - **分支 A（有蓝湖链接）**：检查并调用 lanhu-mcp（lanhu_get_designs ➔ lanhu_get_ai_analyze_design_result 提取精准 HTML/CSS 样式与参数 ➔ lanhu_get_design_slices 提取多倍切图），严禁擅自使用系统 Icon 替代，严格执行像素级还原；
  - **分支 B（无蓝湖链接）**：遵循项目现有整体 UI 风格（#F5F6F8 灰底、白色圆角卡片、.sc 间距规范、core_ui 公共组件如 CommonAppBar / 统一按钮 / 空状态），向用户简述 UI 骨架确认后再编码；
- skills/tuqiang-dev/SKILL.md：
  - 在【阶段一：需求调研与反向拉扯】中新增「UI 设计源决策与蓝湖 MCP 接入【强制卡点】」；
  - 在【阶段五：交付与审查】Checklist 中增加 UI 设计源与切图自检卡点；
  - 在【参考文件索引】中更新 assets-guide.md 说明。

### Changed
- skills/tuqiang-dev 版本升至 1.6.0；
- 根目录 package.json 版本升至 1.6.0；
- 更新根目录 README.md 与 skills/tuqiang-dev/README.md 中的文档说明。

## [1.5.0] - 2026-08-25

### Added
- `skills/tuqiang-dev/references/networking.md`：新增【业务数据模型（Model）标准范式与四大铁律】章节及标准代码模板：
  - **纯粹性铁律**：Model 字段必须只包含后端业务数据，严禁将客户端 UI 结构文案（页面标题、副标题、按钮文字等）塞进 Model，UI 文案统一由 Widget 内 `.tr` 动态求值；
  - **全可空铁律**：网络字段全部使用可空类型（`final String? phone;` 等），构造函数使用命名参数，严禁硬编码默认值/假数据；
  - **TCheck 防崩铁律**：`fromJson` 统一使用 `TCheck<T>(json['xxx'])` 进行类型安全提取，缺失或类型不符时安全返回 `null`；
  - **Collection If 规范**：`toJson()` 统一使用 Dart 集合 if（`if (field != null) 'field': field`）过滤 `null` 字段，避免向后端发送脏数据；
  - **标准实体 Model 模板**：提供开箱即用的标准不可变 Model 实体类代码模板；
- `skills/flutter-to-web/references/async-networking.md`：新增【Dart 请求参数组装语法糖（前端大白话）】章节：
  - **集合内部 if（Collection If）**：对照讲解 JS 展开运算符 + 三元表达式（`...(phone ? { phone } : {})`）；
  - **Switch 表达式（Dart 3 模式匹配）**：对照讲解按渠道/类型构建入参的表达式化写法；
- `skills/tuqiang-dev/SKILL.md`：在【阶段五：交付与审查】Checklist 中新增 Model 四大铁律自检项。

### Changed
- `skills/tuqiang-dev` 版本升级至 `1.5.0`；
- `skills/flutter-to-web` 版本升级至 `1.2.0`；
- 根目录 `package.json` 版本升级至 `1.5.0`；
- 更新根目录 `README.md`、`skills/tuqiang-dev/README.md` 与两个 skill 的 `SKILL.md` 索引。

## [1.4.0] - 2026-08-25

### Added
- `skills/tuqiang-dev/references/testing.md`：新增【测试规范与提测交付标准】独立参考文档：
  - **测试按需触发铁律**：明确在需求调研期必须主动询问用户是否需要测试文件，未确认严禁擅自生成，一旦确认则每次代码变动强制同步伴生生成/修改 `test/` 测试文件；
  - **自动化测试分层规范**：标准化业务层（Notifier）、数据层（Model）与组件层（Widget）的测试目录结构与代码模板；
  - **《需求提测交付单》Markdown 模板**：提供包含用例清单、三端验证结果、边界异常与回归建议的标准提测验收单；
- `skills/tuqiang-dev/references/assets-guide.md`：
  - **蓝湖切图平台避坑指引**：明确禁止导出 Android mipmap 格式（避免产生 1.5x/2.5x 及 19x19 奇数尺寸），指定选择 iOS/Web 平台导出标准 1x/2x/3x 偶数多倍图；
  - **尺寸规整与透明外框**：规范 1x 切图必须为偶数像素，要求 UI 导出时保留统一透明外框（Bounding Box）以杜绝排版抖动；
  - **切图索要模板升级**：AI 索要切图时必须明确列出推荐命名、包路径以及具体的 1x/2x/3x 像素尺寸；
- `skills/tuqiang-dev/SKILL.md`：
  - 在【阶段一：需求调研与反向拉扯】中新增【测试文件需求事前必问】强制卡点，并升级【UI 切图预检与尺寸索要】卡点；
  - 在【阶段三：分步编码】中新增测试文件同步伴生规则；
  - 在【阶段四：本地全量验证】与【阶段五：交付与审查】Checklist 中新增测试与提测单自检项。

### Changed
- `skills/tuqiang-dev` 版本升级至 `1.4.0`；
- 根目录 `package.json` 版本升级至 `1.4.0`；
- 更新 `skills/tuqiang-dev/README.md` 与根目录 `README.md` 中的 references 索引。

## [1.3.0] - 2026-08-25

### Added
- `skills/tuqiang-dev/references/networking.md`：新增【动态接口 vs 静态数据与 Mock 规范】章节：
  - **静态数据判定原则**：明确本地配置场景，AI 必须向用户陈述理由并确认，确认后收敛在常量配置中，杜绝散落硬编码；
  - **动态接口暂缺处理范式**：严禁暗箱脑补假 URL，必须采用标准架构预留（Model / Repository）+ 结构化异步 Mock 数据（`Future.delayed` 模拟延迟并返回符合规范的 `ResultModel`），实现后续提供真实接口时上层 UI 与 Controller 零改动无缝平替；
- `skills/tuqiang-dev/SKILL.md`：
  - 在【阶段一：需求调研与反向拉扯】中将【数据源动静判定与接口对齐】升格为强制卡点（与 UI 切图预检并列）；
  - 在【阶段五：交付与审查】Checklist 中新增接口与数据源规范自检项。

### Changed
- `skills/tuqiang-dev` 版本升级至 `1.3.0`；
- 根目录 `package.json` 版本升级至 `1.3.0`。

## [1.2.0] - 2026-08-25

### Added
- 根目录新增 `AGENTS.md`：建立仓库级多技能维护规范、四联动变更铁律（Skill / package.json / CHANGELOG / README / 全局同步）与中文详尽 Commit Message 提交规范；
- `skills/tuqiang-dev/references/i18n.md`：新增【国际化禁止 `final` 成员变量缓存】规则与正反代码示例（解决在 Widget/State 成员属性中定义 `final title = 'xxx'.tr` 导致语言切换不刷新的高频暗坑）；
- `skills/tuqiang-dev/references/project-structure.md`：新增【所有文件强制使用 UTF-8（无 BOM）】规范与 Python/Dart/Node 读写标准代码，新增【敏感信息零泄露防线】；
- `skills/tuqiang-dev/SKILL.md`：在阶段三编码基线与阶段五交付审查 Checklist 中增加 UTF-8、敏感信息脱敏与 `final` 国际化缓存的自检项。

### Changed
- `skills/tuqiang-dev` 版本升级至 `1.2.0`；
- 根目录 `package.json` 版本升级至 `1.2.0`。

## [1.1.0] - 2026-08-25

### Added
- 根目录新增 `package.json`：建立仓库级统一元数据与语义化版本（SemVer）管理体系；
- `skills/flutter-to-web/SKILL.md` 与 `skills/tuqiang-dev/SKILL.md`：在 YAML frontmatter 中显式声明 `version: 1.1.0`；
- `skills/tuqiang-dev/references/assets-guide.md`：新增 UI 切图与静态资源规范（严禁私自使用系统 Icons 脑补、阶段一/二主动索要切图 SOP、2.0x/3.0x 多倍图与蓝湖导出设置、小写下划线命名规范、常量注册与 `package:` 跨包引用）；
- `skills/flutter-to-web/references/`：新增 5 篇深度对照表
  （`state-and-riverpod.md`、`routing.md`、`layout-ui.md`、`async-networking.md`、
  `widget-lifecycle.md`、`official-sources.md`），并在 SKILL.md 增加按需阅读索引；
- `skills/tuqiang-dev/`：途强三端开发规范技能（含 10 篇 references 模板与人机协同闭环）；
- 两个 skill 各自的 `README.md` 与 `LICENSE.txt`；
- 仓库级 `README.md`（双 skill 导航与安装说明）与本 `CHANGELOG.md`。

### Changed
- 仓库重组为 multi-skill 架构：原有 `flutter-to-web` 移入 `skills/flutter-to-web/`，
  新增 `tuqiang-dev`（SKILL.md + references/）至 `skills/tuqiang-dev/`。

## [1.0.0] - 2025-08-21

### Added
- 首个 skill `flutter-to-web`：面向 Web 前端（Vue/React）开发者的 Flutter
  大白话讲解指南（SKILL.md + Apache 2.0 LICENSE）。
