# Changelog

本仓库所有重要变更记录于此。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，遵循语义化版本。

## [Unreleased]

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
