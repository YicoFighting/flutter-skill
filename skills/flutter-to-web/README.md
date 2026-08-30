# flutter-to-web

当前版本：1.6.1

面向 Vue3 / React 开发者解释途强 Flutter 项目的教学 Skill。它会动态识别并验证当前 `<TUQIANG_ROOT>`，从用户操作或页面入口向下追到数据源和状态写入，再沿响应式依赖回到最终 UI；不依赖某台电脑的固定盘符或目录。

## 核心能力

- 用户只选中一段代码时，默认把它作为检索锚点，而不是讲解边界；
- 分开解释事件/同步调用、异步数据流、Riverpod 状态依赖和 UI 重建，再按时间拼成闭环；
- 对每个关键状态说明定义、family 参数来源与实例身份、依赖、写入、读取、最终消费和生命周期；
- 覆盖 Riverpod 之外的 Manager/cache、`setState`、`ValueNotifier` 和插件状态；
- 每个关键跳提供本次核验的真实路径、行号和最小必要 Dart 原文；
- 术语首次出现就用 Vue3/React 心智解释，同时保留准确的 Flutter/Riverpod 语义；
- 同时提供与实际 Dart 链路一一对应的 Vue3、React 端到端实现，而不是只翻译一行代码；
- 明确 loading/error/empty、缓存、竞态、销毁/清理和外部未知边界。

## 默认讲解结构

```text
一句话业务结论
→ 用户操作与页面/路由入口
→ 事件/同步调用链
→ 异步数据链
→ Riverpod/其他状态依赖与 UI 重建链
→ 状态身份、family key、写入与消费
→ 每一跳的 Dart 源码证据
→ 字段落到最终 Widget
→ Vue3 端到端等价实现
→ React 端到端等价实现
→ 生命周期、分支与未知边界
```

详细规则：

- [动态项目根目录协议](references/project-root-resolution.md)
- [完整业务链追踪](references/full-flow-tracing.md)
- [Riverpod 参数、状态与生命周期](references/state-and-riverpod.md)
- [异步与网络](references/async-networking.md)
- [路由](references/routing.md)
- [布局与 UI](references/layout-ui.md)
- [Widget 生命周期](references/widget-lifecycle.md)
- [官方来源](references/official-sources.md)

## 与另外三个 Skill 的分工

- `tuqiang-project-map`：提供架构分层、模块 owner、公共能力、状态拓扑和业务链路索引，帮助模型快速组织源码上下文；
- `flutter-to-web`：重新核验实时源码，用 Vue3/React 心智讲清事件、数据、状态与 UI 闭环；
- `tuqiang-dev`：根据项目主流风格实施修改、复用现有抽象并完成验证。
- `tuqiang-change-retrospective`：在变更完成后复用本 Skill 的对照讲解，结合 Git 因果生成学习复盘 Markdown。

`tuqiang-project-map` 不可用时，本 Skill 会按动态根目录协议直接检索源码继续工作。设备选择、定位/GPS 只是地图中的一个领域案例，不是本 Skill 的固定职责。

## 安装

推荐安装整个仓库，使四个 Skill 可以协同：

```bash
/plugin marketplace add tuqiang/flutter-skill
```

也可手动复制本目录到对应 Skill 目录。单独安装时仍可独立解析项目根目录和追踪源码，只是没有兄弟项目地图帮助预先缩小检索范围。

## 使用示例

```text
@flutter-to-web
从进入列表页并点击某条记录开始，解释路由参数怎样变成 Riverpod family key、
请求由谁触发、状态在哪里定义和写入、哪些 watch/listen 消费它、最终哪个 Widget 展示。
每一跳给实时路径、行号和最小 Dart 原文，并给完整的 Vue3 与 React 对照实现。
```

只解释局部语法时请明确说：

```text
@flutter-to-web 只解释我选中的这几行 Dart 语法，不展开完整业务链。
```

## 许可证

Apache 2.0 © tuqiang
