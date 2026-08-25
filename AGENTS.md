# flutter-skills 仓库维护规范（AGENTS.md）

你正在维护 `flutter-skills` 技能库仓库（收录 `flutter-to-web` 与 `tuqiang-dev` 两个专属 Agent Skill）。

---

## 1. 核心维护铁律（修改 Skill 必须四联动）

凡涉及修改 `skills/` 下的任何技能内容、补充规范、新增参考文件或修复 Bug，**必须在同一次交付中联动完成以下 4 项工作**：

1. **版本号递增（SemVer）**：
   - 更新对应 `skills/<skill-name>/SKILL.md` frontmatter 中的 `version`（小改动升 patch，新功能/规范增补升 minor）。
   - 同步更新根目录 `package.json` 的顶层 `version` 以及 `skills` 列表中对应项的 `version`。
2. **详细更新 CHANGELOG.md**：
   - 严格遵循 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/) 格式。
   - 在对应版本号（如 `## [1.2.0] - YYYY-MM-DD`）下，按 `### Added`、`### Changed`、`### Fixed` 详细分类记录变更条目。
3. **同步更新 README.md**：
   - 若涉及版本号、目录结构、特性概览或新增 reference 文件索引，必须同步更新根目录 `README.md` 以及对应 skill 的 `README.md`。
4. **全局自动同步（Sync to Global）**：
   - 每次在工作区内完成 skill 修改后，必须自动将变更递归同步复制到系统全局配置目录 `C:\Users\admin\.gemini\config\skills\<skill-name>\`，确保全局生效。

---

## 2. Git 提交与 Commit Message 规范

1. **严禁未经授权自动提交**：
   - 验证完成后保持工作区文件修改状态，日常任务中**严禁擅自自动执行 `git commit` 或 `git push`**。
   - 提交操作必须且只能由用户明确发起或指示。
2. **Commit & Push 执行规则（用户指示提交时触发）**：
   - 当用户明确提及“编写 commit msg 并提交”或要求提交推送时，必须：
     1. **必须使用中文**编写 Commit Message，**内容描述越详细越好**，禁止一两句话敷衍带过；
     2. 采用 **Angular 中文规范** 作为标题，并在正文中详细罗列改动背景、关键规则与具体文件；
     3. 编写完成后，**自动执行 `git commit` 命令与 `git push` 命令**完成代码提交与远端推送。

```text
<前缀>: <中文简要概述>

### 变更背景与原因
- 详细说明为什么进行本次修改或补充

### 详细变更内容
- [模块/文件] 详细说明新增或调整的规则内容
- [模块/文件] 说明关联影响与注意事项

### 涉及文件
- 详细列出修改与新增的文件清单
```

---

## 3. 安全操作底线

- 所有脚本与文件读写必须显式强制 UTF-8 编码（无 BOM）；
- 严禁篡改未经要求的系统配置、依赖锁文件；
- 严禁在代码、日志、终端或回复中暴露密码、Token、私钥或生产配置等敏感信息。
