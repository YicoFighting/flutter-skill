---
name: flutter-to-web
description: 面向 Vue3/React 开发者解释 Tuqiang Flutter monorepo 的真实业务链；从当前源码核验个人/企业账号、用户事件、异步数据、Riverpod/混合状态与 UI，并按需给出 Web 对照。只讲解，不修改代码。
license: Apache 2.0
metadata:
  version: "2.0.1"
---

# Tuqiang Flutter 业务链讲解

只解释 Tuqiang，不搜索、比较或汇报其他产品线业务。目标不是逐句翻译 Dart，而是从用户可感知操作讲清数据如何取得、状态如何发布、UI 为什么变化。代码修改与验证交给 tuqiang-dev。

## 上下文

按 [项目根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 校验当前 checkout，并先标注：

    product: Tuqiang
    accountMode: personal | enterprise | both | unknown
    platform/target: Android/iOS standard | HarmonyOS ohos | multiple | unknown
    entry: <操作、路由或生命周期>
    end: <UI、Repository、缓存或插件边界>

登录/session、HTTP/DTO、设备目录、消息、权限、缓存、页面可见性、首页/Mine、切换或退出账号时，必须读取 [账号模式事实](../tuqiang-project-map/references/account-mode.md) 并核验 isEnterprise 传播链。unknown 不得静默当成公共行为；多个解释会改变结论且源码无法排除时，只问一个必要问题。

事实优先级：项目 AGENTS.md 与当前源码/pubspec/lockfile/测试/tool/CI → 本次核验后的 [项目地图](../tuqiang-project-map/SKILL.md) → 当前依赖版本的一手官方文档 → Web 类比。路径、symbol、版本和行号每次重查。

## 追踪闭环

跨文件问题读取 [完整追踪](references/full-flow-tracing.md)，状态问题再读 [状态与 Riverpod](references/state-and-riverpod.md)。始终分开：

    事件：用户操作 → Widget 回调 → Command/Notifier → Repository
    数据：请求 → await → DTO/Model → State/缓存
    更新：状态通知 → 派生重算 → build/listener → 字段展示

按问题裁剪，但不可漏掉真实入口与 route builder、Provider override/composition、请求或插件边界、loading/error/empty、状态写入与最终消费、key/session/accountMode 身份，以及 dispose/invalidate/reset。不要把异步完成和响应式重建画成同步调用栈。

每个关键状态说明六项：定义、实例身份/family key、依赖 read/watch/listen/select、写入源、UI 消费、生命周期与旧结果淘汰。路由参数、family key、账号模式、单次 action 参数和 State 字段不能混为一类。

## 证据与 Web 对照

每个关键跳提供当前仓库相对路径、1-based 行号、最小 Dart 证据及其因果作用；优先 rg -n 搜 symbol。只展示接口名和语义，不泄露 endpoint、Token、Key、证书或生产配置。

- 用户指定 Vue3 或 React：只给该框架。
- 未指定：给简洁 Web 心智模型。
- 只有明确要求迁移、完整实现或双框架比较时才展开代码；操作、route/props、accountMode、keyed store/query、请求、状态、UI 和 cleanup 必须与 Dart 链逐段对应。

常用近似：Widget.build ≈ render/template；StatefulWidget ≈ 组件局部状态；Provider.family ≈ keyed store/query；watch(select) ≈ selector/computed；ProviderScope override ≈ Context/provide 组合根。类比不能替代框架事实。

## 按需读取

| 场景 | Reference |
|---|---|
| 完整跨文件链路与字段血缘 | [full-flow-tracing.md](references/full-flow-tracing.md) |
| Riverpod family、混合状态与生命周期 | [state-and-riverpod.md](references/state-and-riverpod.md) |
| route、arguments/result 与 effect | [routing.md](references/routing.md) |
| Future、HTTP、账号身份与竞态 | [async-networking.md](references/async-networking.md) |
| 约束、尺寸、多语言布局与字段展示 | [layout-ui.md](references/layout-ui.md) |
| Widget context、监听与资源释放 | [widget-lifecycle.md](references/widget-lifecycle.md) |

设备、地图或定位问题再从项目地图读取对应专题；不要一次加载全部 reference。

## 完成条件

回答必须包含上下文卡、三条链、关键状态身份、账号分支、实时证据、外部边界和按用户需要选择的 Web 对照；明确 loading/error/empty、竞态、缓存与清理，并区分已证实事实、推断和未知。
