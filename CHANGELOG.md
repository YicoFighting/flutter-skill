# Changelog

本仓库所有重要变更记录于此。
格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，遵循语义化版本。

## [Unreleased]

### Changed
- 仓库重组为多 skill 结构：原有 `flutter-to-web` 移入 `skills/flutter-to-web/`，
  新增 `tuqiang-dev`（SKILL.md + references/）至 `skills/tuqiang-dev/`。

### Added
- `skills/flutter-to-web/references/`：新增 5 篇深度对照表
  （`state-and-riverpod.md`、`routing.md`、`layout-ui.md`、`async-networking.md`、
  `widget-lifecycle.md`、`official-sources.md`），并在 SKILL.md 增加按需阅读索引；
- `skills/tuqiang-dev/`：途强三端开发规范技能（含 9 篇 references 模板）；
- 两个 skill 各自的 `README.md` 与 `LICENSE.txt`；
- 仓库级 `README.md`（双 skill 导航与安装说明）与本 `CHANGELOG.md`。

## [1.0.0] - 2025-08-21

### Added
- 首个 skill `flutter-to-web`：面向 Web 前端（Vue/React）开发者的 Flutter
  大白话讲解指南（SKILL.md + Apache 2.0 LICENSE）。
