# tuqiang-change-retrospective

当前版本：1.0.0

途强三端 Flutter monorepo 的开发后复盘 Skill。它只在手动调用时工作：读取当前源码、Git diff/history、测试与已有任务上下文，把已修复 Bug、已完成需求或混合改动整理成一份可长期学习的 Markdown。

## 为什么单独做成第 4 个 Skill

- `tuqiang-project-map` 负责当前项目事实、owner 与调用链；
- `flutter-to-web` 负责 Flutter、Vue3、React 的业务链教学；
- `tuqiang-dev` 负责实现、修复和验证；
- `tuqiang-change-retrospective` 负责完成后的 Git 因果追溯、初学者复盘编排和 Markdown 落盘。

复盘不会自动介入普通开发，也不会修改业务源码或执行提交推送。

## 三种模式

| 模式 | 内容 |
|---|---|
| Bug | 原因、引入/暴露/修复改动、排查路径、解决方式与预防 |
| 需求 | 业务动机、实现金字塔、输入输出、事件/数据/状态/UI 流转 |
| 混合 | 以需求为主线，嵌入开发过程中引入、暴露或修复的 Bug 卡 |

## 默认产物

用户未指定路径且项目没有其他文档约定时，输出到：

```text
<TUQIANG_ROOT>/docs/learning/
```

文件名按 `YYYY-MM-DD-bug-<slug>.md`、`YYYY-MM-DD-feature-<slug>.md` 或 `YYYY-MM-DD-hybrid-<slug>.md` 生成。同名文件不会被覆盖。

每份文档包含可核验的仓库相对路径、行号、commit/diff 证据、最小 Dart 源码、Vue3/React 对照、纯文本金字塔或因果栈，以及已验证/未验证边界。

## 使用示例

```text
@tuqiang-change-retrospective

复盘刚刚修复的“切换设备后短暂显示旧状态”问题。
请说明根因、引入/暴露/修复改动、排查过程、如何避免，
并用 Dart + Vue3 + React 对照解释，生成完整学习 Markdown。
```

```text
@tuqiang-change-retrospective

复盘刚完成的“轨迹设置恢复默认值”需求。
请按金字塔解释为什么这样设计、具体输入输出从哪里来、
事件/异步/状态/UI 怎样流转，并生成完整学习 Markdown。
```

Codex 中使用 `$tuqiang-change-retrospective`；ChatGPT 中使用 `@tuqiang-change-retrospective`。

## 文件结构

```text
tuqiang-change-retrospective/
├── SKILL.md
├── agents/
│   └── openai.yaml
├── references/
│   ├── git-causality.md
│   ├── bug-retrospective.md
│   ├── feature-retrospective.md
│   └── report-contract.md
├── README.md
└── LICENSE.txt
```

## 许可证

Apache 2.0 © tuqiang
