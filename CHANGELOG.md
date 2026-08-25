# Changelog

本仓库所有重要变更记录于此。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，遵循语义化版本。

## [Unreleased]

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
