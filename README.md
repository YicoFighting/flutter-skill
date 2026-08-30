# flutter-skills

服务途强三端 Flutter monorepo 的四个 Agent Skill。它们按仓库结构动态识别当前 checkout，不绑定公司电脑、家庭电脑、盘符或用户目录。

| Skill | 版本 | 职责 | 典型场景 |
|---|---:|---|---|
| [`tuqiang-project-map`](skills/tuqiang-project-map/) | 1.1.1 | 提供架构分层、模块 owner、状态/数据拓扑、公共封装、复用入口与业务链的可核验事实索引 | “这个逻辑属于哪层”“状态实际经过哪些文件” |
| [`flutter-to-web`](skills/flutter-to-web/) | 1.6.1 | 从用户操作追踪事件、异步数据、Riverpod 状态与 UI 重建，并用 Vue3/React 口吻和代码讲解 | “从进入页面/点击开始讲到接口、状态和 UI” |
| [`tuqiang-dev`](skills/tuqiang-dev/) | 1.11.1 | 依据项目分层、现有复用入口和目标 package 的局部主流风格完成修改与风险验证 | “按同事现有写法修复这个 Bug” |
| [`tuqiang-change-retrospective`](skills/tuqiang-change-retrospective/) | 1.0.0 | 在变更完成后追溯 Git 因果、拆解输入输出与事件流，并生成学习复盘 Markdown | “把刚修好的 Bug 或刚完成的需求整理成学习文档” |

## 四个 Skill 如何协作

```text
当前 checkout 的源码、pubspec、测试与门禁
                    │
                    ▼
          tuqiang-project-map
       项目事实、架构、owner、拓扑
             ┌──────┴──────┐
             ▼             ▼
      flutter-to-web    tuqiang-dev
      理解与教学        实现与验证
             └──────┬──────┘
                    ▼
     tuqiang-change-retrospective
       Git 因果、学习复盘与 MD
```

- `tuqiang-project-map` 是底层项目上下文。它帮助模型确定代码放在哪层、现有能力在哪里、调用链和状态拓扑怎样连接，但不代替上层 Skill 输出教学代码或决定实现方案。
- `flutter-to-web` 重新核验当前源码，以用户操作为顶点，分别展开事件/同步调用、异步数据、状态依赖/UI 重建，并给出路径、实时行号、最小 Dart 原文及 Vue3/React 端到端代码。
- `tuqiang-dev` 使用地图提供的 owner 和复用候选，再在目标子域/package 抽样 2–4 个成熟同类实现，做局部风格、复用、内聚/解耦和验证决策。
- `tuqiang-change-retrospective` 只在用户手动调用时工作；它结合当前源码、diff、Git 历史和验证证据，把已完成变更整理为 Bug、需求或混合复盘，不修改业务代码。

设备目录 → 选择设备 → 定位状态 → GPS UI 只是地图中已整理的一条代表性业务链。项目地图的主职责是整个项目的事实、分层与索引，不是只讲设备或定位。

## 路径无关的仓库识别

四个 Skill 都把 `<TUQIANG_ROOT>` 当作“本次任务已核验的途强仓库根目录”，不会把占位符或历史绝对路径直接传给 shell。

解析顺序：

1. 用户明确给出的项目路径；
2. 当前选中/目标文件所在 Git 仓库；
3. 当前 workspace 的 Git 根目录；
4. 无法唯一确认时询问用户，不扫描整个磁盘。

候选根目录还要通过三端宿主、共享业务包、项目工具及 `pubspec.yaml` package identity 校验。最终回答中的文件路径和行号均从当前 checkout 实时生成，因此公司与家庭目录不同不会影响使用。

## 为什么拆成四个

- 项目事实集中维护，避免教学和开发 Skill 各保存一份静态架构并逐渐冲突；
- 教学可以详细，但不会把解释模板混入实际代码决策；
- 开发可以保持最小改动、局部团队风格和三端验证，不会被通用教程带偏；
- 复盘独立处理 Git 历史、证据置信度和 Markdown 写入，不会在普通开发时自动创建学习文件；
- references 按问题渐进加载，完整业务链、Riverpod、网络或风格规则只在相关任务中读取。

兄弟 Skill 不可用时，`flutter-to-web`、`tuqiang-dev` 和 `tuqiang-change-retrospective` 都保留按同一仓库身份协议直接检索当前源码的降级能力。

## 仓库结构

```text
flutter-skills/
├── package.json                         # 仓库版本 v1.12.0 与四个 Skill 元数据
├── AGENTS.md                            # 四联动维护、同步和提交规范
├── CHANGELOG.md                         # Keep a Changelog 增量记录
├── README.md
└── skills/
    ├── tuqiang-project-map/             # 项目事实与架构索引 v1.1.1
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── project-root-discovery.md
    │   │   ├── architecture-overview.md
    │   │   ├── module-catalog.md
    │   │   ├── startup-routing.md
    │   │   ├── riverpod-topology.md
    │   │   ├── device-location-flow.md
    │   │   ├── infrastructure-and-cross-cutting.md
    │   │   └── requirement-trace-playbook.md
    │   ├── README.md
    │   └── LICENSE.txt
    ├── flutter-to-web/                  # Vue3/React 完整链路教学 v1.6.1
    │   ├── SKILL.md
    │   ├── references/                  # 动态根目录、完整追踪、Riverpod 与前端对照
    │   ├── README.md
    │   └── LICENSE.txt
    ├── tuqiang-dev/                     # 项目开发规范 v1.11.1
    │   ├── SKILL.md
    │   ├── references/                  # owner、局部风格、复用、状态、网络、三端和测试
    │   ├── README.md
    │   └── LICENSE.txt
    └── tuqiang-change-retrospective/    # 变更学习复盘 v1.0.0
        ├── SKILL.md
        ├── agents/openai.yaml           # 仅允许显式调用
        ├── references/                  # Git 因果、Bug/需求剧本与 Markdown 契约
        ├── README.md
        └── LICENSE.txt
```

每个 Skill 使用 `SKILL.md` frontmatter 和按需读取的 `references/`；版本放在 `metadata.version`，并与 `package.json` 同步。

## 安装与启用

### 推荐：四个 Skill 一起安装

推荐把四个完整目录并排安装，确保 `SKILL.md`、`references/` 和兄弟 Skill 引用都可用：

```text
<SKILLS_HOME>/
├── tuqiang-project-map/
├── flutter-to-web/
├── tuqiang-dev/
└── tuqiang-change-retrospective/
```

当前仓库是 Skill 源码包，尚未包含可验证的 marketplace/plugin manifest，因此安装时直接复制完整目录。支持 `.agents/skills` 的项目级目录与 Codex 全局目录示例：

```bash
# 项目级安装（适用于支持 .agents/skills 的客户端）
mkdir -p .agents/skills
cp -r skills/* .agents/skills/

# Codex 全局安装
mkdir -p ~/.codex/skills
cp -r skills/* ~/.codex/skills/
```

Windows PowerShell 全局安装示例：

```powershell
$codexSkillsDir = Join-Path $env:USERPROFILE '.codex\skills'
New-Item -ItemType Directory -Force -Path $codexSkillsDir | Out-Null
Copy-Item -Recurse -Force -Path '.\skills\*' -Destination $codexSkillsDir
```

单独安装任务 Skill 也能降级工作：它们会自行解析项目根目录并检索实时源码；但复盘 Skill 缺少 `flutter-to-web` 时，Dart/Vue3/React 对照通常不如四个 Skill 并装完整。

### 必须安装完整目录

不要只复制或引用一个 `SKILL.md`。例如：

```text
@[flutter-to-web](C:\path\to\flutter-to-web\SKILL.md)
```

这类写法可能只是把一个文件附加到当前对话，不能保证客户端把同目录的 `references/` 和兄弟 Skill 当作完整技能包加载。要获得完整行为，应安装整个 Skill 目录，再使用客户端提供的 Skill 选择或显式调用能力。

### 不同客户端的调用语法

| 客户端 | 显式调用示例 |
|---|---|
| Codex | `$flutter-to-web` |
| ChatGPT | `@flutter-to-web` |
| 其他支持 Agent Skill 的客户端 | 使用客户端的 Skill 菜单、补全语法或自动匹配 |

OpenAI 官方约定中，ChatGPT 使用 `@skill-name`，Codex 使用 `$skill-name`；Skill 的名称与描述也可以让模型在请求匹配时自动加载。详见 [OpenAI Build skills](https://developers.openai.com/plugins/build/skills) 和 [OpenAI Skills concepts](https://developers.openai.com/plugins/concepts/skills)。

本文后续示例统一使用 Codex 的 `$skill-name`。在 ChatGPT 中使用时，只需把调用行的 `$` 换成 `@`，提示词正文保持不变。

### 安装后检查

至少确认下面四个入口和各自的 `references/` 都存在：

```text
<SKILLS_HOME>/tuqiang-project-map/SKILL.md
<SKILLS_HOME>/flutter-to-web/SKILL.md
<SKILLS_HOME>/tuqiang-dev/SKILL.md
<SKILLS_HOME>/tuqiang-change-retrospective/SKILL.md
```

如果安装后没有立即出现在 Skill 列表中，重新打开客户端或新建会话，再通过客户端的 Skill 列表确认，不要用文件附件代替安装验证。

## 使用原则

### 四个都安装，按任务显式调用

日常不需要每次把四个 Skill 全部写上。`tuqiang-project-map` 是底层项目上下文；复盘 Skill 只在变更完成并由用户显式调用时运行。

| 当前目标 | 默认显式调用 | 是否需要同时写 `tuqiang-project-map` |
|---|---|---|
| 理解页面、需求、Riverpod、事件流和数据流 | `$flutter-to-web` | 通常不需要 |
| 实现需求、修复 Bug、重构或评审 | `$tuqiang-dev` | 通常不需要 |
| Bug/需求完成后生成学习复盘 Markdown | `$tuqiang-change-retrospective` | 通常不需要 |
| 专门梳理架构、模块 owner、Provider 拓扑或复用入口 | `$tuqiang-project-map` | 它就是主 Skill |
| 先理解现状，再直接实现 | `$flutter-to-web $tuqiang-dev` | 通常不需要 |

以下情况可以额外显式启用 `tuqiang-project-map`：

- 当前交付物本身就包含一份架构图、模块地图或 owner 清单；
- 模型曾遗漏跨 package、App composition root、Provider override 或公共封装；
- 当前客户端不会自动读取兄弟 Skill；
- 你希望模型先输出项目事实，再进行教学或开发决策。

### 一次提供哪些上下文

高质量提示词最好说明以下信息；不确定的部分可以省略，让 Skill 从源码核验：

| 信息 | 作用 | 示例 |
|---|---|---|
| 项目位置 | 多 checkout 时消除歧义 | `项目根目录是 E:\work\tuqiang_flutter` |
| 操作起点 | 决定调用链从哪里开始 | `从进入设备列表并点击设备开始` |
| 目标终点 | 防止只解释选中代码 | `一直追到 GPS 地图和状态文本更新` |
| 源码锚点 | 帮助快速定位，不作为讲解边界 | 当前文件、Widget、Provider 或方法名 |
| 重点疑问 | 决定需要展开的机制 | family 参数、缓存、竞态、生命周期 |
| 任务边界 | 控制是否允许修改 | `先解释，不修改代码` |
| 验收结果 | 让开发结果可验证 | 切换设备不串状态，三端行为不回退 |
| 复盘范围 | 防止混入无关提交或工作区改动 | `当前 diff`、`abc123^..def456` |
| 输出位置 | 指定学习文档目录 | `输出到 docs/learning` |

不需要把这些信息机械地全部填写。能从当前 workspace、选中文件和需求中确定的内容，应由 Skill 自己检索和核验。

## 快速开始

### 1. 专门了解项目架构

适合刚接触一个模块、还不知道页面和状态分别属于哪个 package 时使用：

```text
$tuqiang-project-map

梳理“设备列表进入 GPS 首页”涉及的架构分层、模块 owner、路由装配、
Provider 拓扑、网络/缓存入口、公共组件和推荐复用入口。
请给出当前 checkout 的真实文件路径与实时行号，并区分项目事实和你的推断。
```

期望得到的是“项目地图和证据索引”，不是 Vue3/React 教程，也不是直接修改代码。

### 2. 从 Vue3/React 视角理解完整链路

```text
$flutter-to-web

从“用户进入页面并点击设备”开始，解释这段需求的完整链路：
事件触发、路由参数、请求入口、Riverpod 状态定义、family 参数来源、
数据写入、状态消费、Widget 重建和最终 UI 展示。

不要把我选中的代码当作讲解边界。请分别列出同步事件链、异步数据链、
响应式/UI 重建链；每一跳提供真实文件路径、实时行号和最小必要 Dart 源码，
最后给出与真实链路一一对应的 Vue3 和 React 完整代码。
```

如果只想理解局部 Dart 语法，要明确收窄范围：

```text
$flutter-to-web
只解释我选中的几行 Dart 语法和对应的 Vue3/React 写法，不展开跨文件业务链。
```

### 3. 深挖 Riverpod family 和状态去向

当你最困惑的是“为什么 Provider 可以传参数、数据究竟存在哪里”时，可以直接使用这个模板：

```text
$flutter-to-web

围绕 deviceLocationSnapshotProvider(deviceRef) 解释完整状态闭环：
1. Provider 的完整类型和定义位置；
2. deviceRef 从哪个用户操作、路由或上游状态得到；
3. family 参数如何决定 Provider 实例身份和缓存隔离；
4. 所有写入源，以及每次写入发生在 await 前还是 await 后；
5. 所有 watch/select/read/listen 消费端；
6. 哪些 Widget 因此重建，最终展示哪些字段；
7. autoDispose、保活、切设备、退出登录和竞态处理。

请给真实路径、实时行号、Dart 原文，并用 Vue3 keyed store/computed/watch
和 React keyed store/selector/effect 写出端到端对照，不要只做术语翻译。
```

Provider 名只是锚点。Skill 仍应向上追到用户操作，向下追到请求与写入，再回到 UI 消费。

### 4. 按项目风格实现需求或修复 Bug

```text
$tuqiang-dev

修复“切换设备后 GPS 页面短暂展示上一台设备状态”的问题。
先确认功能 owner、现有复用入口、family key、全部状态写入源、根 Host 保活和
session reset；再从目标 package 选取 2–4 个成熟同类实现作为风格证据。

保持现有分层和团队主流写法，优先复用语义一致的能力，做高内聚、低耦合的
最小修改。完成后检查调用方、diff 和受影响测试，并说明已验证与未验证项。
```

开发 Skill 默认应先调查再修改，但不会为了“复用”强行新增 wrapper、base class、mode flag，也不会借当前需求统一重构整个模块。

### 5. 开发一个新需求

```text
$tuqiang-dev

在轨迹设置页增加“恢复默认值”操作：只恢复页面暂存值，用户点击“确定”后才保存。
请先定位页面 owner、默认值来源、现有保存链路、国际化 key、缩放规范和同类按钮布局；
参考目标 package 内 2–4 个成熟实现，尽量复用现有 Controller、常量和提交逻辑。

不要改动无关架构。完成代码、必要测试和静态检查，并列出真实修改文件及验证结果。
```

这里描述的是期望行为，不需要提前替模型指定 Provider、Repository 或组件抽象；具体放置位置应由项目事实和局部主流风格决定。

### 6. 只读评审代码，不进行修改

```text
$tuqiang-dev

只读评审当前改动，不修改文件。请结合目标 package 的局部主流写法，检查 owner、
复用边界、Riverpod 状态隔离、异步竞态、生命周期、i18n、缩放和三端影响。
问题按严重程度排序，给出真实文件路径、实时行号、触发条件和修复方向；
如果没有阻断问题，也要明确说明剩余风险和尚未执行的验证。
```

“解释”或“评审”本身不授权修改代码。需要 Skill 实施修复时，再明确提出“修复这些问题并验证”。

### 7. 先理解，再开发

需要在一次任务中直接完成时：

```text
$flutter-to-web $tuqiang-dev

先从用户操作开始，用 Vue3/React 方式解释现有事件流、异步数据流、
Riverpod 状态和 UI 重建；再根据已经核验的 owner、复用入口和局部主流风格
实现需求，保持最小改动并完成受影响范围验证。
```

如果你想先审核方案、确认后再改代码，建议拆成两轮：

```text
# 第一轮
$flutter-to-web
解释当前完整链路，并指出最可能的修改 owner 和风险；只读分析，不修改代码。

# 第二轮（确认理解后）
$tuqiang-dev
根据上一轮已经核验的链路实现需求，保持局部主流风格并完成验证。
```

这样能明确区分“建立心智模型”和“授权修改代码”，尤其适合第一次接触的复杂模块。

### 8. 变更完成后生成学习复盘

Bug 已修复时：

```text
$tuqiang-change-retrospective

复盘刚刚修复的“切换设备后短暂展示旧状态”问题。
范围：当前工作区。
请说明根因、缺陷引入/问题暴露/修复改动、实际排查过程、下次排查路径和预防方式；
用修复前后 Dart 源码以及 Vue3、React 对照逐层解释，并生成完整学习 Markdown。
```

需求已完成时：

```text
$tuqiang-change-retrospective

复盘刚完成的“轨迹设置恢复默认值”需求。
请按“用户价值 → 可验收行为 → 状态与数据 → 源码证据”的金字塔拆解，
说明输入从哪里来、怎样转换和保存、输出被谁消费，以及同步事件、异步数据、
状态通知和 UI 重建怎样流转。生成完整学习 Markdown。
```

该 Skill 还支持“混合模式”：需求开发中引入、暴露或顺带修复的 Bug 会作为 Bug 卡嵌入同一份需求复盘。它默认输出到目标项目的 `docs/learning/`，不覆盖已有文件。

## 项目路径与多 checkout

Skill 不固定使用 `D:\Code\Flutter`。公司电脑、家庭电脑、Codex worktree 或其他 checkout 都可以使用同一套 Skill。

通常在 Flutter 仓库 workspace 中打开任务即可；Skill 会从用户给出的路径、选中文件或当前 Git workspace 解析 `<TUQIANG_ROOT>`。如果同时打开了多个仓库，建议在提示词第一行明确本次目标：

```text
项目根目录：E:\company\flutter-app
请先核验它是目标途强 monorepo，再开始追踪源码。
```

路径只是本次任务的候选值，不会被写回 Skill。候选目录校验失败或存在多个有效 checkout 时，Skill 应停止猜测并请用户确认；它不会为了寻找项目而扫描整个磁盘。

## 输出验收清单

### 解释类结果

- 是否以用户操作或页面入口为顶点，而不是从选中代码直接开始；
- 是否拆清同步事件、异步请求和响应式 UI 重建，避免把它们伪装成一条同步调用栈；
- 是否说明状态定义、family 参数来源、实例身份、写入源、消费端和生命周期；
- 是否把字段落到最终 Widget、文本、地图或交互状态；
- 是否提供当前 checkout 的真实路径、实时行号和最小必要 Dart 原文；
- Vue3/React 代码是否覆盖同一条完整链路，而不是只给一行语法类比；
- 是否标出条件分支、缓存、loading/error/empty、竞态与尚未核验的外部边界。

### 开发类结果

- 是否先确认功能 owner、依赖方向、公开 API 和现有复用入口；
- 是否参考目标 package 中 2–4 个成熟同类样本，而不是套用模型偏好的通用架构；
- 是否优先最小修改，并避免无收益的 wrapper、公共抽象和顺手重构；
- 是否检查 Riverpod/Manager/本地状态的完整读写与清理链；
- 是否覆盖受影响调用方、标准版/OHOS/其他端边界、i18n、资源和缩放；
- 是否报告真实修改文件、测试命令、验证结果和未执行项。

### 复盘类结果

- 是否区分缺陷引入、问题暴露、修复改动与防线缺失，而不是把 `git blame` 当根因；
- 是否用纯文本金字塔或因果栈逐层解释，并把同步、异步、响应式更新分开；
- 是否说明输入来源、转换、状态写入、输出和最终消费者；
- 是否提供修复前后或需求关键 Dart 源码，以及同一业务链的 Vue3/React 对照；
- 是否把已证实事实、高可信推断、未知边界和实际验证状态分开；
- 是否生成 UTF-8 无 BOM 的完整 Markdown，使用仓库相对路径且不覆盖旧文档。

## 常见问题

### 每次都要显式调用 `tuqiang-project-map` 吗？

不用。它默认作为底层事实索引供另外三个任务 Skill 按需读取。只有要单独产出架构地图，或当前客户端不能读取兄弟 Skill 时，才需要额外显式调用。

### 同时启用四个 Skill 会不会效果更好？

不一定。与当前目标无关的 Skill 会增加上下文和职责冲突。开发时调用 `tuqiang-dev`，理解时调用 `flutter-to-web`；只有变更已经完成且要落学习文档时，才调用 `tuqiang-change-retrospective`。

### 复盘 Skill 会自动创建 Markdown 吗？

不会。`tuqiang-change-retrospective` 配置为仅显式调用；只有使用 `$tuqiang-change-retrospective`（ChatGPT 中为 `@tuqiang-change-retrospective`）时才生成文档。它只写复盘文件，不修改业务源码或 Git 历史。

### 只把 `SKILL.md` 拖进对话可以吗？

可以临时阅读，但不要把它等同于完整安装。单文件附件可能无法按设计读取 `references/`，也无法可靠发现兄弟项目地图。

### 模型为什么还是只解释了选中的代码？

明确写出操作起点、UI 终点，并要求“选中代码只作为检索锚点”。同时检查安装的是完整 `flutter-to-web` 目录而不是单个文件。

### reference 中的路径或行号与当前项目不同怎么办？

当前源码永远优先。reference 只提供检索方向，Skill 必须在本次 checkout 中重新定位 symbol 并生成实时路径与行号；不要手工把历史绝对路径改成另一台电脑的路径。

### 换成其他 Flutter 项目能直接用吗？

`flutter-to-web` 的部分教学思路可以参考，但四个 Skill 中的 package、路由、统一命令和平台约定是为途强 monorepo 维护的。`tuqiang-project-map`、`tuqiang-dev` 与 `tuqiang-change-retrospective` 不应直接套用于无关项目。

### `tuqiang-dev` 会自动提交或推送代码吗？

不会。默认只完成工作区修改与验证；只有用户明确要求提交或推送时，才会执行对应 Git 操作。

## 维护要求

修改任何 Skill 时必须在同一次交付中：

1. 递增该 Skill 与根包版本；
2. 在 `Unreleased` 后增量插入 CHANGELOG，保留所有历史版本标题；
3. 同步根 README 与对应 Skill README；
4. 递归同步到 `AGENTS.md` 规定的全局 Skill 目录；
5. 检查 UTF-8 无 BOM、链接、frontmatter、版本联动和 diff；
6. 未经用户明确要求，不执行 commit 或 push。

## 许可证

四个 Skill 均以 Apache 2.0 发布（见各自目录的 `LICENSE.txt`）。© tuqiang
