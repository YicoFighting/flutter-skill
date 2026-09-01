---
name: tuqiang-project-map
description: 为途强 Flutter monorepo 的 Tuqiang 与 Laoying 两条产品线提供可核验的仓库事实、模块 owner、状态/数据拓扑和源码索引；当架构、路由、状态、跨模块依赖或业务链需要先按产品线定位时使用。负责证据与归属依据，不承担 Vue3/React 教学、实现方案决策或代码修改。
license: Apache-2.0
metadata:
  version: "1.2.0"
---

# 途强 Flutter 项目地图

本 skill 是项目的事实与架构索引层。它先确认当前仓库与产品线，再回答“系统由什么组成”“逻辑实际经过哪些文件、状态和数据边界”“当前 owner 与组合入口在哪里”。它不绑定绝对路径，不把 Tuqiang 的 Riverpod/AppRouters 事实套到 Laoying，也不把 Laoying 的 app-local/ChangeNotifier 结构套到 Tuqiang。

它为其他 skill 提供项目上下文，但不代替它们的交付职责：

- `flutter-to-web` 使用本 skill 的调用链、状态拓扑、源码证据和生命周期事实，再负责 Vue3/React 类比。
- `tuqiang-dev` 使用本 skill 的 owner、依赖方向、现有抽象、同层样本和影响面事实，再负责方案取舍、代码修改与验证。
- `tuqiang-change-retrospective` 使用本 skill 的当前事实，再结合 Git 历史生成复盘文档。
- 本 skill 不输出教学实现，不决定 API/资源生成方式，不修改代码，也不执行提交。

## 1. 先识别仓库与产品线

首先按 [references/project-root-discovery.md](references/project-root-discovery.md) 确定并校验 `<TUQIANG_ROOT>`，保存为 PowerShell 变量 `$tuqiangRoot`。用户明确路径优先；未明确时，当前 Codex 对话所附项目/工作区就是第一隐式候选。校验失败或候选冲突时询问用户，不扫描整个磁盘。

随后必须给当前问题标注产品线：

- `tuqiang`：锚点位于 `apps/standard`、`apps/ohos`、`apps/tuqiang_app`，或调用 Tuqiang 的 `feature_*`、`shared_*`、`StrongApp`、`AppRouters`。
- `laoying`：锚点位于 `apps/laoying_standard`、`apps/laoying_ohos`、`apps/laoying_app`，或调用 `LYApp`、`LYAppProvider`、`LYAppRouter`、`LYAppRouteRegistry`。
- `cross-product`：问题明确涉及两条产品线、core/plugin 公共能力或差异比较；分别建立证据链，不能把其中一条当作另一条的实现。

产品线不能由用户描述、目标文件或调用方唯一确定，且不同选择会改变 owner、状态或路由结论时，先向用户确认；在确认前只报告已核验候选，不继续补全一条猜测链路。

references 保存相对路径和 symbol，不把历史行号当成永久事实。每次回答前必须在 `$tuqiangRoot` 对要引用的文件和 symbol 执行 `rg -n`，再使用本次行号展示证据。

事实冲突时按以下顺序判断：

1. `<TUQIANG_ROOT>/AGENTS.md`、当前源码、当前 `pubspec.yaml` 与 lockfile；
2. `tool/`、`ci/` 中实际执行的门禁和脚本；
3. 对应测试；
4. `docs/` 中明确描述当前状态的段落；
5. 本 skill 的 references。

迁移方案里的目标结构不等于当前运行结构。无法从当前源码确认的分支必须标为“未核验”，不得用文档目标补全。

## 2. 事实调查边界

- 用户给出的代码只是锚点。调用/数据流需向上追到产品入口、路由或用户事件，向下追到状态写入、Repository/Manager/HTTP/插件、状态消费与 UI。
- 分开描述同步调用、异步数据流和响应式依赖。`ref.watch` 重建、`notifyListeners`、Future 完成和 post-frame 不是同一条同步调用栈。
- Tuqiang 是 Riverpod、Manager/单例、Widget `setState`、Controller、缓存与直接 HTTP 并存的混合架构；Laoying 当前 App 根状态由 `LYAppProvider extends ChangeNotifier` 协调，并有 app-local controller/repository。只有实际经过 Provider 的链路才能称为 Riverpod。
- 不把 `read`、`watch`、`listen`、`select` 或 `notifyListeners` 当成风格标签；说明调用点订阅、读取、发布或触发了什么。
- 代码归属不能只看目录名；核对产品线、package 依赖、barrel/router/composition 入口、同类实现、调用者与测试。
- “已有抽象”必须落到具体 symbol 与当前调用证据。仅名称相似而语义、生命周期或依赖方向不一致时，只能列为候选。
- 不复制 endpoint 值、Token、Key、证书、签名配置或生产参数。接口只引用常量名、Repository 方法与请求语义。

## 3. 歧义停止规则

遇到下列任一情况，停止替用户作决定，说明缺失信息、已核验候选及各自影响，并提出最小问题：

- 根目录校验失败、出现多个合法候选，或对话项目与目标文件属于不同仓库；
- Tuqiang/Laoying 产品线不明确，而两者的状态、路由或 owner 不同；
- 当前源码存在多个合理 owner/复用入口，需求语义不足以排除其中任何一个；
- 需求要求替换图片、文案、接口或平台能力，但仓库没有目标资源/契约，且继续需要产品、设计或调用方决策；
- 搜索范围持续扩大仍无法建立唯一入口或终点，实质原因是需求缺少场景、平台、账号/设备类型或验收结果。

不得用 Canvas 动态绘制、临时资源、兼容 alias、默认文案或自创 contract 填补缺失决策。本 skill 只确认“现有资源是否存在、由谁拥有、哪些调用方受影响”，最终方案交给用户与开发 skill。

## 4. 标准工作流

1. 校验 `$tuqiangRoot`，确认当前产品线与平台；需要跨产品比较时分别建链。
2. 读取最少的 reference：架构/归属先读总览与模块目录；状态或业务链再读对应专题。
3. 从可观察入口开始，用 `rg -n` 查调用方、路由、状态声明/key、写入者、Repository、消费者和 reset/invalidate。
4. 调查开发归属时，确认当前 owner 和依赖方向，再查接口、基类、helper、Provider/ChangeNotifier、Repository、组件、同层实现和测试。
5. 遇到 app composition callback、route registry、runtime callback 或 controller 时，继续追到最终 builder/owner；不要在 contract 停止。
6. 向教学任务返回调用/数据/状态证据；向开发任务额外返回 owner、现有复用入口、同层样本、依赖边界、资源边界与影响面。本 skill 不做最终实现决策。

完整搜索、产品分流与输出协议见 [references/requirement-trace-playbook.md](references/requirement-trace-playbook.md)。

## 5. Reference 路由

| Reference | 何时读取 |
|---|---|
| [references/project-root-discovery.md](references/project-root-discovery.md) | 首次使用、路径变化或当前对话项目不明时，发现并校验根目录 |
| [references/architecture-overview.md](references/architecture-overview.md) | 确认双产品拓扑、层级、状态体系与事实来源 |
| [references/module-catalog.md](references/module-catalog.md) | 找 Tuqiang/Laoying 的 app、feature/shared/core/plugin owner |
| [references/startup-routing.md](references/startup-routing.md) | 追两条产品线的 main、bootstrap、根状态、路由与页面装配 |
| [references/riverpod-topology.md](references/riverpod-topology.md) | 解释 Tuqiang Riverpod family、状态保存、订阅与生命周期；同时识别 Laoying 非 Riverpod 边界 |
| [references/device-location-flow.md](references/device-location-flow.md) | 仅当 Tuqiang 问题涉及设备目录、选择设备、定位状态或 GPS UI 时读取 |
| [references/infrastructure-and-cross-cutting.md](references/infrastructure-and-cross-cutting.md) | 查两产品线的网络、持久化、session、i18n、尺寸与资源边界 |
| [references/requirement-trace-playbook.md](references/requirement-trace-playbook.md) | 输出完整需求链、当前路径/行号、证据与未决策项 |

## 6. 回答完成条件

- [ ] 已校验 `$tuqiangRoot`，未固定盘符，也未把同名或忽略目录当成 package 事实。
- [ ] 已明确 `tuqiang`、`laoying` 或 `cross-product`，没有混用状态与路由体系。
- [ ] 每个关键结论都有当前文件路径、实时行号、symbol 和最小源码证据。
- [ ] 没有把迁移目标、猜测、缺失资源或敏感配置写成当前事实。
- [ ] 存在会改变结论的歧义时，已停止并请求用户决策。

调用/数据流还必须覆盖入口、状态定义与写入/读取、key 或实例作用域、异步边界、网络/缓存/Manager/controller、UI 终点及清理。开发归属调查还必须给出当前 owner、依赖方向、可复用 symbol、同层样本、调用者、测试与资源边界，把最终实现取舍留给 `tuqiang-dev`。
