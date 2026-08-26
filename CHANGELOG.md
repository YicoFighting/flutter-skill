# Changelog

本仓库所有重要变更记录于此。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，遵循语义化版本。

## [Unreleased]

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
  - 在【参考文件索引】中更新 ssets-guide.md 说明。

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
