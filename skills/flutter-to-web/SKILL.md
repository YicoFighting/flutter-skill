---
name: flutter-to-web
description: 面向 Vue3/React 前端开发者解释途强 Flutter monorepo 中 Tuqiang 与 Laoying 产品线的真实业务链路；当问题涉及页面入口、交互事件、异步请求、Riverpod/ChangeNotifier 状态、跨模块依赖或 UI 展示时，从当前仓库动态定位源码，输出可核验的端到端事件流、数据流、路径行号、最小 Dart 证据以及 Vue3 与 React 等价实现。只负责理解与讲解，不代替开发 Skill 修改代码。
license: Apache 2.0
metadata:
  version: "1.7.0"
---

# Flutter 业务链路讲解（Vue3 / React 视角）

服务对象是熟悉 Vue3、React、正在接手当前 Flutter monorepo 的前端开发者。不要停留在 Dart 语法翻译；默认从一个用户可感知的操作开始，把事件如何触发、数据如何获取、状态如何保存、依赖如何通知、UI 如何重建讲成可核验的完整闭环。

## 1. 项目根目录与事实来源

先按 [动态项目根目录协议](references/project-root-resolution.md) 得到并验证 `<TUQIANG_ROOT>`，后续命令、路径和证据都基于它。用户明确路径优先；否则当前对话绑定的项目/workspace 就是首选候选。不得假定项目位于某个盘符、用户目录或固定绝对路径，也不得继续沿用其他对话或其他机器的历史路径。

事实优先级：

1. `<TUQIANG_ROOT>` 中的 `AGENTS.md`、当前源码、`pubspec.yaml`、lockfile、测试、CI 与 `tool/`；
2. 同仓库 [tuqiang-project-map](../tuqiang-project-map/SKILL.md) 提供的架构分层、模块 owner、状态拓扑和业务链路索引；
3. 实际依赖版本对应的官方文档；
4. 本 Skill 的 Vue3 / React 心智映射。

`tuqiang-project-map` 是帮助理解源码的项目事实层，不是当前答案的替代品。它不可用、内容过期或链接不可读时，按根目录协议直接检索真实源码继续完成讲解。静态地图只用于缩小范围；文件、符号、依赖版本和行号必须在本次回答前重新核验。

本 Skill 只负责理解与讲解。用户要求修改、测试、构建或评审代码时，讲解规则仍可使用，但开发决策、代码风格与验证交给 `tuqiang-dev`。Bug 或需求完成后的 Git 因果、学习编排与 Markdown 落盘由 `tuqiang-change-retrospective` 负责，本 Skill 只向它提供 Flutter、Vue3、React 的链路解释能力。

## 2. 讲解模式

开始追踪前先读 [双产品上下文](references/product-context.md)，从目标路径、入口、target 或调用方判定本次属于：

- **Tuqiang**：`standard` / `ohos` shell 与 `apps/tuqiang_app`，常见 Riverpod + Manager/cache，`TQHttp`，`AppRouters` / feature router；
- **Laoying**：`laoying_standard` / `laoying_ohos` shell 与 `apps/laoying_app`，常见 `LYAppProvider` + `ChangeNotifier` / `InheritedNotifier`，`LYBackendHttpClient`，`LYAppRouter`；
- **共享层或双产品**：继续反查真实调用方，分别说明两条产品接线，不能拿一条产品线的状态、网络、路由或资源规则套另一条。

产品线能由源码唯一确定时直接继续，不把可检索事实丢给用户。若“用户操作起点”“目标页面/功能”或“讲解终点（例如只到 Repository、继续到原生插件，或回到哪个 UI）”存在两个以上合理解释，且会改变追踪链或结论，先用一个简短具体的问题请用户选择；未澄清前不要自行选一条展开。若歧义只发生在仓库外部且不影响仓库内已证事实，可追到边界并标为未知。

### 完整链路模式（默认）

以下情况都应展开完整链路，即使用户只选中几行代码：

- 解释需求、业务逻辑、数据流、事件流或调用栈；
- 从进入页面、点击、刷新、切换或回调开始发生了什么；
- 状态在哪里定义、为什么能传参数、在哪里写入和消费；
- 请求的数据怎样最终出现在 UI；
- 问题明显跨越 Widget、Provider、Repository、路由或插件。

选中代码只是检索锚点，不是解释边界。只有用户明确说“只解释这几行/这个语法”时才使用局部模式；局部解释仍要点明决定其语义的项目封装和关键上游。

## 3. 金字塔追踪：从操作顶点到实现底座，再回到 UI

复杂链路先读 [完整业务链追踪](references/full-flow-tracing.md)；涉及状态时再读 [状态与 Riverpod / ChangeNotifier](references/state-and-riverpod.md)。按当前问题裁剪范围，但必须闭环：

1. **操作顶点**：确定 App 启动、路由进入、生命周期、点击、输入、下拉刷新、Timer、推送或插件回调中的真实起点。
2. **入口接线**：找到 Widget 回调、route builder、Host/Coordinator、`ProviderScope` override、`LYAppScope`、构造注入、`*Runtime.configure` / `*ApiPaths.configure` 及跨模块 contract；只保留会改变当前链路的接线。
3. **同步事件/调用链**：追踪当前函数直接调用谁，标出普通调用、路由跳转、回调注册和命令分发。
4. **异步数据链**：追踪 `await` 前后、Repository/Service、HTTP/缓存/数据库/插件、DTO/Model 映射、loading/error/empty 与竞态处理。
5. **状态依赖链**：找到 State、Notifier/Controller、Provider/family key、`ChangeNotifier` / `InheritedNotifier`、派生状态、override 和其他真实状态载体。
6. **写入与通知**：列出真正改变目标数据的全部可发现写入源，并说明哪次写入触发哪些 Provider 重算或订阅回调。
7. **读取与 UI**：反查 `watch/select/listen/read`、Manager getter、`setState/ValueNotifier` 与最终 Widget 字段，说明哪些变化会重建，哪些只读一次，哪些只产生副作用。
8. **生命周期闭环**：说明创建、复用、切 key、离开页面、`autoDispose/keepAlive/invalidate/onDispose`、登出/reset 和异步取消。
9. **证明边界**：追到后端、原生插件、外部 SDK 或缺失实现时停止，标明“源码只能证明到这里”。

Flutter 的异步与响应式流程通常不是一条始终存在的同步栈。回答必须明确分开并最终按时间拼合：

```text
事件/同步调用链：用户操作 → Widget 回调 → Command/Notifier → Repository 调用
异步数据链：     请求发出 → await 返回 → DTO/Model → State/缓存写入
响应式重建链：   Provider/ChangeNotifier 通知 → 派生状态重算 → Widget build → 字段展示
```

设备选择、定位和 GPS 只是可选的领域案例；不得把任何单条业务链误写成整个项目或本 Skill 的中心模型。

## 4. 每个关键状态的身份卡

每个影响答案的 Riverpod Provider、ChangeNotifier/Controller 或其他状态载体都必须回答：

1. **定义**：声明、完整泛型、State、Notifier/Controller 在哪里；
2. **参数**：route、family、action 参数各从哪里产生，各自控制什么；
3. **实例身份**：Riverpod 要解释 `.family` key；Laoying Controller 要解释由哪个页面/route 参数创建、谁持有实例；对象 key 的不可变性及 `==/hashCode` 是否可靠；
4. **依赖**：builder/build 中 `watch/read` 了什么，或 `LYAppScope.of`、`addListener`、`ListenableBuilder/AnimatedBuilder` 订阅了什么；具体实现从哪里注入；
5. **写入**：初始值和 `state =`、`copyWith`、seed/apply/update、Manager/cache setter、`setState/ValueNotifier` 等所有相关写入；
6. **读取与消费**：`watch/select/listen/read`、`LYAppScope.of`、`ListenableBuilder/AnimatedBuilder` 或 getter 分别在哪里，最终哪个 Widget 使用哪个字段；
7. **生命周期**：何时创建、复用、销毁、重建、清理，以及旧异步结果如何避免覆盖新状态。

必须区分：

```text
路由参数    = 把页面上下文带到入口
family key  = 决定选择哪一个 Provider 实例/状态分区
action 参数 = 控制某一次命令
State 字段  = 请求或计算后留存并供消费者使用的数据
```

`.family` 应解释成“以参数为身份键创建/选择 Provider 实例的工厂”，不是向单份全局 State 临时传参。`autoDispose` 是无人监听后具备释放条件，不等于某个页面一退出就必定销毁；必须检查根 Host、listener 和 `keepAlive`。

## 5. 源码证据要求

每个关键跳转都要同时给出：

- 基于当前 `<TUQIANG_ROOT>` 的真实文件路径和本次核验的 1-based 行号；
- 能证明“入口、调用、参数、写入或消费”的最小必要 Dart 原文；
- 这一跳在事件流、数据流或状态依赖中的作用。

优先使用 `rg -n` 搜索符号，再逐行读取上下文。不要复制静态 reference 中的旧行号，不要用长源码堆砌代替解释，也不要为了短而漏掉入口、Provider 声明、写入、数据源和 UI 消费。

```text
<TUQIANG_ROOT>/packages/.../some_provider.dart:42
```

不得展示 endpoint、Token、密钥、证书、签名或生产配置值；只保留脱敏后的调用职责。

## 6. Vue3 / React 讲解与等价代码

术语首次出现时先用前端开发者熟悉的语言解释，再保留准确的 Flutter/Riverpod 名称，方便继续搜索源码。例如先说明 `ProviderScope override` 类似 Vue `app.provide` 或 React Context 组合根，再解释它在 Riverpod 中的真实注入语义。类比用于建立心智模型，不能冒充等价事实。

完整链路回答必须同时给出两份真正端到端的等价实现：

- **Vue3**：使用与源码对应的操作入口、route/props、keyed composable 或 Pinia、异步请求、状态写入、`computed/watch`、模板消费和卸载/切 key 清理；
- **React**：使用与源码对应的操作入口、route/props、keyed store/query、异步请求、selector/effect、组件消费和 cleanup/取消；
- 名称、关键字段、分支和数据阶段应与本次 Dart 链路一一对应，不能只把一行 `ref.watch` 翻译成 `computed` 或 selector；
- 明确指出非等价处，例如 Riverpod family 的 key 相等性、`ProviderScope`、依赖图和 `autoDispose` 与 Pinia/Zustand/React Query 生命周期的差异。

常用近似：

| Flutter / Riverpod | Vue3 近似 | React 近似 |
|---|---|---|
| `Widget.build` | template/setup 的响应式求值 | 函数组件 render |
| `StatefulWidget + setState` | 组件内 `ref/reactive` | `useState` |
| `StateNotifierProvider.family(key)` | keyed Pinia/composable store | keyed Zustand store / query |
| `ref.watch(...select(...))` | `computed`/selector | store selector |
| `ref.listen` | `watch` 副作用 | `useEffect`/store subscribe |
| `ProviderScope overrides` | `app.provide` 组合根 | Context Provider 组合根 |
| `InheritedNotifier<ChangeNotifier>` | `provide/inject + reactive` | Context + external store subscription |
| `ListenableBuilder/AnimatedBuilder` | `watchEffect` 驱动局部模板 | store subscription 驱动 render |
| `Future<T>` | `Promise<T>` | `Promise<T>` |

## 7. 默认输出契约

完整链路回答依次输出：

1. 一句话业务结论及产品线/target；
2. 用户操作与页面/路由入口；
3. 事件/同步调用链；
4. 异步数据链；
5. Riverpod/ChangeNotifier/其他状态依赖与 UI 重建链；
6. 关键状态身份卡；
7. 每一跳的路径、行号与最小 Dart 原文；
8. 关键字段从外部数据到最终 Widget 的血缘；
9. Vue3 端到端等价实现；
10. React 端到端等价实现；
11. loading/error/empty、竞态、缓存、生命周期与清理；
12. 已证实事实、合理推断与未知边界。

## 8. 按需读取的参考文件

| 文件 | 什么时候读 |
|---|---|
| [references/project-root-resolution.md](references/project-root-resolution.md) | 每次需要定位途强项目源码时 |
| [references/product-context.md](references/product-context.md) | 每次先判 Tuqiang、Laoying、共享层与 target；涉及产品资源或测试时 |
| [references/full-flow-tracing.md](references/full-flow-tracing.md) | 完整需求、跨文件业务链、状态来源/去向 |
| [references/state-and-riverpod.md](references/state-and-riverpod.md) | Riverpod family 或 Laoying ChangeNotifier 的身份、读写、通知和生命周期 |
| [references/routing.md](references/routing.md) | 路由入口、参数、builder owner、route effect |
| [references/async-networking.md](references/async-networking.md) | Future、Repository/HTTP、序列化、竞态与错误 |
| [references/layout-ui.md](references/layout-ui.md) | Flutter 约束、布局和最终 UI 映射 |
| [references/widget-lifecycle.md](references/widget-lifecycle.md) | Widget 生命周期、context、Controller 清理 |
| [references/official-sources.md](references/official-sources.md) | 用户追问原理或官方依据 |

需要项目分层、模块 owner、基础设施或已整理业务链时，从 `tuqiang-project-map` 只读取相关 reference；不要一次加载整张地图。设备/定位 reference 仅在问题确实属于该领域时读取。

## 9. 回答前自检

- [ ] 是否已动态解析并验证 `<TUQIANG_ROOT>`，且没有假定固定机器路径？
- [ ] 是否已判定 Tuqiang / Laoying / 共享层及具体 target，并使用对应的状态、网络、路由与资源链？
- [ ] 起点、目标页或解释终点若存在会改变结论的多解，是否已先请用户选择？
- [ ] 是否从用户操作/页面入口开始，而不是把选中代码当作边界？
- [ ] 是否分开事件调用、异步数据、状态依赖与 UI 重建，再拼成时间闭环？
- [ ] 每个关键状态的定义、参数身份、依赖、写入、读取、消费和清理是否齐全？
- [ ] 是否覆盖 Manager/cache、`ChangeNotifier`、`setState`、`ValueNotifier` 和插件等真实旁路？
- [ ] 每个关键跳是否有刚核验的路径、行号和最小 Dart 证据？
- [ ] Vue3 与 React 代码是否都覆盖整个实际链路，并说明非等价点？
- [ ] 是否标明外部边界并脱敏敏感配置？
