# flutter-skills

一个仓库收录两个 Agent Skill：

| Skill | 一句话简介 | 适合谁 |
|---|---|---|
| [`flutter-to-web`](skills/flutter-to-web/) | 把 Flutter/Dart 代码用前端大白话（Vue/React）翻译出来讲解的**教学技能** | 有 Web 前端经验、正在学/读 Flutter 的开发者 |
| [`tuqiang-dev`](skills/tuqiang-dev/) | 途强（`D:\Code\tuqiang`）三端 Flutter 项目专属的**开发规范技能** | 在该仓库干活的 AI 编码助手 + 会 Vue3 的同学 |

两个 skill 均遵循 [Agent Skills](https://github.com/anthropics/skills) 的标准结构：
`SKILL.md`（主文档，含 frontmatter）+ `references/`（按需深读的参考文件）+ `README.md`（安装与使用说明）+ `LICENSE.txt`。

## 仓库结构

```
flutter-skills/
├── package.json               # 仓库元数据与统一版本号（v1.7.0）
├── AGENTS.md                  # 仓库维护规范、四联动变更铁律与提交约定
├── README.md                  # 本文件：双 skill 导航与安装说明
├── CHANGELOG.md               # 变更记录（Keep a Changelog 规范）
└── skills/
    ├── flutter-to-web/        # 教学技能 (v1.3.0)
    │   ├── SKILL.md           # 映射表 + 讲解套路 + 官方出处
    │   ├── references/        # 状态/路由/布局/异步/生命周期深度对照表
    │   ├── README.md
    │   └── LICENSE.txt
    └── tuqiang-dev/           # 途强项目规范技能 (v1.8.0)
        ├── SKILL.md           # 铁律 + 目录规范 + 五步开发闭环
        ├── references/        # 切图资源/测试/网络/状态/i18n/适配/权限/路由/三端兼容/Code Review 12 篇模板
        ├── README.md
        └── LICENSE.txt
```

## 安装

### Claude Code 插件市场

```bash
/plugin marketplace add tuqiang/flutter-skill
```

安装后 `/plugin` 里会同时出现 `flutter-to-web` 与 `tuqiang-dev` 两个技能。

### 手动复制到项目

```bash
# 只要教学技能
mkdir -p .agents/skills && cp -r skills/flutter-to-web .agents/skills/

# 只要途强项目规范（仅限 D:\Code\tuqiang 仓库使用）
mkdir -p .agents/skills && cp -r skills/tuqiang-dev .agents/skills/

# 全都要
cp -r skills/* .agents/skills/
```

### 复制到全局 skills 目录

```bash
cp -r skills/* ~/.codex/skills/
```

## 使用

在对话中通过 `@` 引用即可激活对应技能：

```
@flutter-to-web   帮我解释这段 Riverpod 代码
@tuqiang-dev      在设置页加一个"清除缓存"入口
```

Claude Code 中也可以用斜杠命令 `/flutter-to-web`、`/tuqiang-dev`。

## 选哪个？

- **看不懂别人的 Flutter 代码 / 在学前端转 Flutter** → `flutter-to-web`
- **要在途强三端 monorepo 里真正改代码、加功能** → `tuqiang-dev`
- 两者可以同时启用：先用 `flutter-to-web` 看懂代码，再按 `tuqiang-dev` 的规范动手。

## 许可证

两个 skill 均以 Apache 2.0 发布（见各自目录内的 LICENSE.txt）。© tuqiang
