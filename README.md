# flutter-skills

服务途强与老鹰在线双产品 Flutter monorepo 的四个 Agent Skill。它们以当前对话绑定项目为默认 checkout，按实时仓库结构识别产品线、平台 target 和业务 owner，不绑定公司电脑、家庭电脑、盘符或用户目录。

| Skill | 版本 | 职责 | 典型场景 |
|---|---:|---|---|
| [`tuqiang-project-map`](skills/tuqiang-project-map/) | 1.3.0 | 识别当前产品线并提供架构、状态、平台/地图后端、设备页面变体与业务链事实 | “这个逻辑属于哪层”“还有哪些平台或页面分支” |
| [`flutter-to-web`](skills/flutter-to-web/) | 1.7.0 | 从用户操作追踪事件、异步数据、真实状态体系与 UI 更新，并用 Vue3/React 口吻和代码讲解 | “从进入页面/点击开始讲到接口、状态和 UI” |
| [`tuqiang-dev`](skills/tuqiang-dev/) | 1.13.0 | 先处理需求决策点，再用三端、地图实现与设备 route leaf 覆盖矩阵完成修改和验证 | “修复这个 Bug，并确认没有漏端或漏设备类型” |
| [`tuqiang-change-retrospective`](skills/tuqiang-change-retrospective/) | 1.1.0 | 在变更完成后按产品范围追溯 Git 因果、拆解输入输出与事件流，并生成学习复盘 Markdown | “把刚修好的 Bug 或刚完成的需求整理成学习文档” |

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

- `tuqiang-project-map` 是底层项目上下文。它帮助模型确定代码放在哪层、现有能力在哪里、调用链和状态拓扑怎样连接，并把平台/target、地图后端、设备类型与最终页面拆成带可达证据的候选矩阵，但不代替上层 Skill 决定实现方案。
- `flutter-to-web` 重新核验当前源码，以用户操作为顶点，先识别途强 Riverpod/Manager 链或老鹰在线 `LYAppProvider`/controller 链，再分别展开事件、异步数据、状态依赖与 UI 更新，并给出路径、实时行号、最小 Dart 原文及 Vue3/React 端到端代码。
- `tuqiang-dev` 使用地图提供的产品 owner、复用候选和变体矩阵，先把变更类型、用户可观察行为、设备范围与验收说清，再按 Bug/新需求分别关闭 Android/iOS/HarmonyOS、地图后端和页面叶子。
- `tuqiang-change-retrospective` 只在用户手动调用时工作；它结合当前源码、diff、Git 历史和验证证据，把已完成变更整理为 Bug、需求或混合复盘，不修改业务代码。

设备目录 → 选择设备 → 定位状态 → GPS UI 只是代表性主链；真实入口还会按 GPS scene、LBS、Camera scene、Tag、MiFi、服务状态等进入不同详情族。涉及“设备详情/更多详情/更多设置”而范围不明时，开发 Skill 必须先列出当前页面叶子，再询问用户是覆盖全部设备类型还是指定类型。

## 路径无关的仓库识别

四个 Skill 都把 `<TUQIANG_ROOT>` 当作“本次任务已核验的 monorepo 根目录”，不会把占位符或历史绝对路径直接传给 shell。

解析顺序：

1. 用户在当前请求中明确给出的项目路径；
2. 当前对话/任务绑定项目或 workspace 的 Git 根目录；
3. 当前对话未绑定项目时，才复用本次任务已校验的根目录或从用户明确指向的外部文件发现仓库；
4. 无法唯一确认，或外部文件属于另一有效 checkout 时，列出候选与失败原因并询问用户，不静默切换、不扫描整个磁盘。

候选根目录通过稳定的 App 宿主、`tool/project.dart`、Git tracked 状态及 `pubspec.yaml` package identity 校验；feature/shared package 清单从当前源码动态发现，不把迁移中的单一业务包设成永久指纹。最终路径和行号均从当前 checkout 实时生成，因此公司与家庭目录不同不会影响使用。

## 为什么拆成四个

- 项目事实集中维护，避免教学和开发 Skill 各保存一份静态架构并逐渐冲突；
- 教学可以详细，但不会把解释模板混入实际代码决策；
- 开发可以保持最小改动和局部团队风格，同时用强制覆盖台账区分 Bug/新需求、三端、地图后端与设备页面，不会把途强与老鹰在线两套架构混用；
- 复盘独立处理 Git 历史、证据置信度和 Markdown 写入，不会在普通开发时自动创建学习文件；
- references 按问题渐进加载，完整业务链、Riverpod、网络或风格规则只在相关任务中读取。

兄弟 Skill 不可用时，`flutter-to-web`、`tuqiang-dev` 和 `tuqiang-change-retrospective` 都保留按同一仓库身份协议直接检索当前源码的降级能力。

## 仓库结构

```text
flutter-skills/
├── package.json                         # 仓库版本 v1.14.0 与四个 Skill 元数据
├── AGENTS.md                            # 四联动维护、同步和提交规范
├── CHANGELOG.md                         # Keep a Changelog 增量记录
├── README.md
└── skills/
    ├── tuqiang-project-map/             # 双产品项目事实与变体索引 v1.3.0
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── project-root-discovery.md
    │   │   ├── architecture-overview.md
    │   │   ├── module-catalog.md
    │   │   ├── startup-routing.md
    │   │   ├── riverpod-topology.md
    │   │   ├── device-location-flow.md
    │   │   ├── variant-surface.md       # 平台、地图后端与设备 route leaf
    │   │   ├── infrastructure-and-cross-cutting.md
    │   │   └── requirement-trace-playbook.md
    │   ├── README.md
    │   └── LICENSE.txt
    ├── flutter-to-web/                  # Vue3/React 完整链路教学 v1.7.0
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── project-root-resolution.md
    │   │   ├── product-context.md       # Tuqiang / Laoying 状态、路由、网络与资源分流
    │   │   └── ...                      # 完整追踪、生命周期与前端对照
    │   ├── README.md
    │   └── LICENSE.txt
    ├── tuqiang-dev/                     # 项目开发与覆盖规范 v1.13.0
    │   ├── SKILL.md
    │   ├── references/
    │   │   ├── requirement-clarification.md # 需求、素材、契约与范围决策门
    │   │   ├── implementation-coverage.md # 三端、地图与设备页面覆盖台账
    │   │   ├── assets-guide.md          # 产品资源 owner 与缺素材禁代画规则
    │   │   └── ...                      # 局部风格、状态、网络、产品/平台和测试
    │   ├── README.md
    │   └── LICENSE.txt
    └── tuqiang-change-retrospective/    # 变更学习复盘 v1.1.0
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
| 项目位置 | 通常不必重复；仅在切换 checkout 时覆盖当前对话项目 | `项目根目录是 <目标 checkout>` |
| 产品与 target | 防止把两套 app 架构或平台范围混用 | `途强 standard`、`老鹰在线 laoying_ohos` |
| 变更类型 | 决定 Bug 与新需求的三端完成标准 | `Bug 修复`、`新需求`、`混合变更` |
| 操作起点 | 决定调用链从哪里开始 | `从进入设备列表并点击设备开始` |
| 设备范围 | 防止只改某一详情实现 | `所有设备类型`、`仅 GPS-person scene` |
| 地图场景 | 决定需核查的 source/backend 与 use scene | `定位页，百度/高德/Google/鸿蒙 Map Kit` |
| 目标终点 | 防止只解释选中代码 | `一直追到 GPS 地图和状态文本更新` |
| 源码锚点 | 帮助快速定位，不作为讲解边界 | 当前文件、Widget、Provider 或方法名 |
| 重点疑问 | 决定需要展开的机制 | family 参数、缓存、竞态、生命周期 |
| 任务边界 | 控制是否允许修改 | `先解释，不修改代码` |
| 验收结果 | 让开发结果可验证 | 切换设备不串状态，受影响产品和平台行为不回退 |
| 复盘范围 | 防止混入无关提交或工作区改动 | `当前 diff`、`abc123^..def456` |
| 输出位置 | 指定学习文档目录 | `输出到 docs/learning` |

不需要把这些信息机械地全部填写。当前对话绑定项目就是默认项目；能从 workspace、目标文件和需求中唯一确定的内容，应由 Skill 自己检索和核验。若缺失信息会改变用户可见行为、素材、数据契约、平台范围或修改边界，Skill 应先给出已确认事实和待决项，请用户决定后再写代码。

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

开发 Skill 默认应先调查再修改，但不会为了“复用”强行新增 wrapper、base class、mode flag，也不会借当前需求统一重构整个模块。Bug 至少闭环 Android+HarmonyOS，并把 iOS 共享覆盖、专属差异和未运行项交接；新需求必须有 Android+iOS+HarmonyOS 代码实现。完成一次 owner、contract 与 2–4 个同类样本的聚焦调查后仍有两种以上合理实现，或无法写出唯一验收标准时，应立即停止扩大搜索并请求用户决策。

设备详情族可用下面的提示检查强制范围门：

```text
$tuqiang-dev

修复设备离线时详情页的客服卡片。请先从设备列表和设备搜索入口枚举
deviceType/scene/cameraScene、最终 route/Page 以及“更多详情”下一跳。
如果我没有说明设备范围，先问我是要覆盖全部设备类型还是指定类型，确认前不要修改。
```

### 5. 开发一个新需求

```text
$tuqiang-dev

在轨迹设置页增加“恢复默认值”操作：只恢复页面暂存值，用户点击“确定”后才保存。
请先定位页面 owner、默认值来源、现有保存链路、国际化 key、缩放规范和同类按钮布局；
参考目标 package 内 2–4 个成熟实现，尽量复用现有 Controller、常量和提交逻辑。

不要改动无关架构。完成代码、必要测试和静态检查，并列出真实修改文件及验证结果。
```

这里描述的是期望行为，不需要提前替模型指定 Provider、Repository 或组件抽象；具体放置位置应由项目事实和局部主流风格决定。

地图新需求还会按当前可达组合覆盖 Android/iOS 各自的百度、高德、Google 与 HarmonyOS 华为 Map Kit；用户所称“花瓣地图”只是 Map Kit 后端的业务称谓映射，不是源码 SDK 名。支持三源的 Tuqiang 主地图场景默认建 7 个平台 × 后端候选行，而不是把同名供应商合并后只改当前默认地图源。`standard` target 同时承载 Android/iOS，但 analyze 结果不等于两端运行时都通过；Windows 上不能运行的 iOS 验证会作为交接项单独列出。

如果需求指定的是品牌/业务图片替换，素材本身也是产品输入。例如“非中文起终点改用 S/E 图片”但没有提供目标 PNG 时，Skill 应先给出建议文件名、owner、倍率和需要补齐的资源清单，请用户或设计提供；未经明确授权，不得在旧图片上画字，也不得用 Canvas、CustomPainter、TextPainter、系统图标、emoji 或 AI 生成图替代。

### 6. 只读评审代码，不进行修改

```text
$tuqiang-dev

只读评审当前改动，不修改文件。请结合目标 package 的局部主流写法，检查 owner、
复用边界、真实状态隔离、异步竞态、生命周期、i18n、缩放和受影响产品/平台。
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

Skill 不固定任何机器绝对路径。公司电脑、家庭电脑、Codex worktree 或其他 checkout 都可以使用同一套 Skill。

通常在 Flutter 仓库项目中打开任务即可；当前对话/任务绑定项目就是默认 `<TUQIANG_ROOT>` 候选，选中文件只在该项目内帮助定位。只有需要覆盖当前项目或同时打开多个有效 checkout 时，才在提示词第一行明确目标：

```text
项目根目录：<目标 checkout 的完整路径>
请先核验它是目标途强 monorepo，再开始追踪源码。
```

路径只是本次任务的候选值，不会被写回 Skill。目标文件位于另一 checkout、候选目录校验失败或存在多个有效 checkout 时，Skill 应停止猜测并请用户确认；它不会静默换项目，也不会为了寻找项目而扫描整个磁盘。

## 输出验收清单

### 解释类结果

- 是否以用户操作或页面入口为顶点，而不是从选中代码直接开始；
- 是否拆清同步事件、异步请求和响应式 UI 重建，避免把它们伪装成一条同步调用栈；
- 是否先识别产品线与真实状态体系，再说明状态定义、参数身份、写入源、消费端和生命周期；
- 是否把字段落到最终 Widget、文本、地图或交互状态；
- 是否提供当前 checkout 的真实路径、实时行号和最小必要 Dart 原文；
- Vue3/React 代码是否覆盖同一条完整链路，而不是只给一行语法类比；
- 是否标出条件分支、缓存、loading/error/empty、竞态与尚未核验的外部边界。

### 开发类结果

- 是否先确认功能 owner、依赖方向、公开 API 和现有复用入口；
- 是否先写清用户可观察行为、可证伪验收与必须由用户决定的素材/API/平台/范围问题；
- 是否先分类 Bug/新需求：Bug 闭环 Android+OHOS 并交接 iOS，新需求三端均实现；
- 设备详情族是否先枚举每个 route leaf，范围不明时是否先问“全部还是指定设备类型”；
- Tuqiang 地图变更是否按 Android/iOS 各三源与 HarmonyOS Map Kit 逐项关闭 7 个候选行，并为不可达行记录 `无需修改` 与源码证据；是否标出实际 map scene；Laoying 是否只按当前 Product Scope 和宿主 adapter 验证；
- 是否参考目标 package 中 2–4 个成熟同类样本，而不是套用模型偏好的通用架构；
- 是否优先最小修改，并避免无收益的 wrapper、公共抽象和顺手重构；
- 是否检查 Riverpod/Manager 或 `LYAppProvider`/controller/本地状态的完整读写与清理链；
- 是否覆盖受影响调用方、产品 scope、`standard`/`ohos`/`laoying_standard`/`laoying_ohos` 中实际受影响的 target、i18n、资源和缩放；
- 图片变体缺失时是否暂停并索要产品素材，而不是自行绘制或生成替代图；
- 是否按矩阵报告真实修改文件、共享覆盖/无需修改证据、测试命令、静态/构建/运行结果和 iOS/其他未执行交接项。

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

`flutter-to-web` 的部分教学思路可以参考，但四个 Skill 中的 package、路由、统一命令和平台约定是为当前途强/老鹰在线 monorepo 维护的。`tuqiang-project-map`、`tuqiang-dev` 与 `tuqiang-change-retrospective` 不应直接套用于无关项目。

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
