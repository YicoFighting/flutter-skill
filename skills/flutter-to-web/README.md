# flutter-to-web

当前版本：1.4.0

专门为 Web 前端开发者（React/Vue 技术栈）**讲人话**地解释
`D:/Code/tuqiang` Flutter 代码的 Skill。

它会结合该项目真实的 Riverpod 2.6.1、命名路由、`TQHttp`、`core_i18n`、
`.sc` 和 `core_ui` 约定，用 Web 概念解释代码；类比只用于理解，不会覆盖项目实际实现。

## 安装

### Claude Code（推荐）

```bash
/plugin marketplace add tuqiang/flutter-skill
```

或直接复制到项目：

```bash
mkdir -p .agents/skills/flutter-to-web
# 将 SKILL.md 和 LICENSE.txt 复制到该目录
```

### 手动安装

将 `flutter-to-web` 目录复制到全局 skills 目录：

```bash
cp -r flutter-to-web ~/.codex/skills/
```

## 使用

在对话中通过 `@` 引用即可激活：

```
@flutter-to-web 帮我解释这段 Flutter 代码
```

或在 Claude Code 中使用斜杠命令：

```
/flutter-to-web
```

## 适用场景

- 从 Web 前端（Vue/React）转 Flutter 的开发者
- 需要向前端团队解释 Flutter 代码
- 阅读 `D:/Code/tuqiang` 项目代码时希望快速理解

## 与 tuqiang-dev 一起使用

- 只解释代码：使用本 skill；
- 要修改、测试、构建或评审 `D:/Code/tuqiang`：使用 `tuqiang-dev`；
- 两者同时启用时，`tuqiang-dev` 负责项目事实和技术决策，本 skill 只负责把实现翻译成 Vue/React 开发者容易理解的语言。

## 许可证

Apache 2.0 © tuqiang
