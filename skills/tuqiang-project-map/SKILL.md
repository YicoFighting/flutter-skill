---
name: tuqiang-project-map
description: 为途强三端 Flutter monorepo 提供可核验的项目事实与源码索引；当用户询问仓库架构、模块 owner、状态/数据拓扑、通用封装或业务链路，或 flutter-to-web、tuqiang-dev 需要这些项目上下文时使用。负责提供证据与归属依据，不承担 Vue3/React 教学、实现方案决策或代码修改。
license: Apache-2.0
metadata:
  version: "1.1.0"
---

# 途强 Flutter 项目地图

本 skill 是途强项目的“事实与架构索引层”，负责回答“系统由什么组成”、“这段逻辑实际经过哪些文件、状态与数据边界”以及“新逻辑应归属哪层、现有复用入口在哪里”。它不绑定某台电脑的绝对路径，也不把任何一条业务链当成项目全貌。

它为其他 skill 提供项目上下文，但不代替它们的交付职责：

- `flutter-to-web` 消费本 skill 提供的调用链、状态拓扑、源码证据和生命周期事实，再负责用 Vue3/React 口吻与代码类比讲解。
- `tuqiang-dev` 消费本 skill 提供的 owner、依赖方向、现有抽象、同层风格样本和影响面事实，再负责做实现取舍、修改与验证。
- 本 skill 不输出 Vue3/React 教学，不自行决定 API 形状或修改代码，不提供提交流程。

## 1. 先识别仓库，再核验事实

首先按 [references/project-root-discovery.md](references/project-root-discovery.md) 确定并校验 `<TUQIANG_ROOT>`，将其保存为 PowerShell 变量 `$tuqiangRoot`。用户明确给出的路径优先；否则从当前选中文件或工作区向上确定 Git 根目录并校验仓库特征。无法唯一确认时询问用户，不猜测路径，不扫描整个磁盘。

references 保存的是架构地图、相对路径和 symbol，不把扫描时的行号当成永久事实。每次回答前必须在 `$tuqiangRoot` 对将要引用的文件和 symbol 执行 `rg -n`，再用当前行号展示源码证据。

事实冲突时按以下顺序判断：

1. `<TUQIANG_ROOT>/AGENTS.md`、当前源码、当前 `pubspec.yaml` 与 lockfile；
2. `tool/`、`ci/` 中实际执行的门禁和脚本；
3. 对应测试；
4. `docs/` 中明确描述当前状态的段落；
5. 本 skill 的 references。

迁移方案里的“目标结构”不等于当前运行结构。无法从当前源码确认的分支必须标为“未核验”，不得用文档目标补全调用链。

## 2. 事实调查边界

- 调查调用/数据流时，用户给出的选中代码只是锚点，不是分析边界。向上追到页面入口、路由或用户事件，向下追到状态写入、Repository/Manager/TQHttp、状态消费与 UI 展示。
- 分开描述“同步调用栈”“异步数据流”和“状态依赖图”。`ref.watch` 引发的重建不是普通函数调用，异步请求完成后的状态发布也不是连续同步栈。
- 项目是混合状态架构：Riverpod 与 `Manager`/单例、Widget `setState`、Controller、缓存以及直接 `TQHttp` 调用并存。只有实际经过 Provider 的部分才能称为 Riverpod 链路。
- 不把 `read`、`watch`、`listen`、`select` 当成风格标签；必须说明它们在该调用点订阅什么、读取什么、触发什么。
- 调查代码归属时，不只根据目录名称下结论；核对 package 依赖方向、barrel/router/composition 入口、同类实现、调用者与测试。
- “项目已有抽象”必须落到具体 symbol 和当前调用证据；只有相似命名而语义、生命周期或依赖方向不一致时，只能标为候选。
- 不复制或输出 endpoint 的具体值、Token、Key、证书、签名配置或生产环境参数。接口只引用常量名、Repository 方法和请求语义。

## 3. 标准工作流

1. 确定并校验 `$tuqiangRoot`，所有路径以它为基准。
2. 根据问题读取最少的 reference：架构/归属问题优先总览与模块目录；数据流问题再读状态拓扑、追踪 Playbook 和相关业务专题。
3. 解释调用/数据流时，从 App 启动、进入页面、点击、刷新、路由回调或 session 事件等可观察操作确定起点；用 `rg -n` 查入口、调用方、Provider 声明、family key、Notifier 方法、Repository、消费者和 reset/invalidate。
4. 调查开发归属时，先确认当前 owner 与依赖方向，再搜现有接口/基类/helper/Provider/Repository/组件、同层近似实现、已有调用者和测试。
5. 沿与当前问题相关的可发现真实分支建立证据链；其他分支只列入口索引。遇到 app composition callback 或 route registry 时继续追到最终 builder/owner。
6. 向教学任务返回调用/数据/状态证据；向开发任务额外返回 owner、现有复用入口、同层实现样本、依赖边界和影响面。不在本 skill 中代替上层 skill 生成教学代码或决定实现方案。

完整搜索与输出协议见 [references/requirement-trace-playbook.md](references/requirement-trace-playbook.md)。

## 4. Reference 路由

| Reference | 何时读取 |
|---|---|
| [references/project-root-discovery.md](references/project-root-discovery.md) | 首次使用、仓库路径变化或当前工作区不明时，确定并校验 `<TUQIANG_ROOT>` |
| [references/architecture-overview.md](references/architecture-overview.md) | 第一次理解仓库、判断层级与事实来源 |
| [references/module-catalog.md](references/module-catalog.md) | 找业务 owner、feature/core/shared/plugin/app 模块 |
| [references/startup-routing.md](references/startup-routing.md) | 追 main、bootstrap、ProviderScope override、路由和页面装配 |
| [references/riverpod-topology.md](references/riverpod-topology.md) | 解释 Provider、family 参数、状态保存位置、订阅和生命周期 |
| [references/device-location-flow.md](references/device-location-flow.md) | 仅当问题涉及设备目录、选择设备、定位状态或 GPS UI 时读取；这是一条代表性业务链，不是本 skill 的主职责 |
| [references/infrastructure-and-cross-cutting.md](references/infrastructure-and-cross-cutting.md) | 查网络、持久化、session、i18n、缩放和 UI 基础设施 |
| [references/requirement-trace-playbook.md](references/requirement-trace-playbook.md) | 输出完整需求链、源码路径/行号和证据片段 |

## 5. 回答完成条件

- [ ] 已校验 `$tuqiangRoot` 的仓库特征，没有把当前目录或某台电脑的路径当成项目事实。
- [ ] 每个关键结论都有当前文件路径、实时行号、symbol 和最小源码片段。
- [ ] 没有把迁移目标、猜测或敏感配置写成当前事实。

若任务是调用/数据流解释，还必须满足：

- [ ] 起点是用户操作或生命周期事件，而不是孤立代码片段。
- [ ] 已说明状态定义、写入者、读取者、family 参数来源与 key 相等性。
- [ ] 已说明网络/缓存/Manager/setState 中实际参与的部分。
- [ ] 已区分上游选择状态、按 key 隔离状态和展示派生状态（若链路涉及）。
- [ ] 已覆盖 loading/error、并发防旧请求覆盖、autoDispose/keepAlive、invalidate/session reset（若链路涉及）。

若任务是开发归属或复用调查，还必须满足：

- [ ] 已给出当前 owner、允许的依赖方向和组合边界证据。
- [ ] 已给出可复用 symbol、同层主流实现样本、调用者与相关测试；不适合复用时说明语义或生命周期差异。
- [ ] 只提供组织代码所需的项目事实与候选依据，把最终实现决策留给 `tuqiang-dev`。
