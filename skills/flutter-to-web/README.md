# flutter-to-web

专门为 Web 前端开发者（React/Vue 技术栈）**讲人话**的 Flutter 教学 Skill。

当你在 Claude Code 中贴出 Flutter/Dart 代码时，它会自动用你最熟悉的 Web 概念（v-model、Pinia、useEffect、Flexbox……）翻译给你听，而不是扔 Flutter 学术术语。

## 安装

### Claude Code（推荐）

```bash
/plugin marketplace add tuqiang/flutter-to-web
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
- 阅读 Flutter 项目代码时希望快速理解

## 许可证

Apache 2.0 © tuqiang