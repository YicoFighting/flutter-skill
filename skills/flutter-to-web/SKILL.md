---
name: flutter-to-web
description: 面向 Vue3/React 开发者，从当前 Tuqiang 源码解释目标功能、状态与 UI，并按需给出 Web 对照。只讲解，不修改代码。
license: Apache 2.0
metadata:
  version: "2.2.0"
---

# Tuqiang Flutter 讲解

围绕用户的问题解释当前 Tuqiang 实现。先讲结论，再用最短的源码因果链说明为什么；不逐句翻译 Dart，不扩展到其他产品线。需要修改业务代码时使用 tuqiang-dev。

## 先确定问题边界

按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 确认 checkout 并读取项目 AGENTS.md。已有有效上下文可复用；路径、symbol、行号和依赖版本以当前源码为准。

单个字段、组件或状态问题，只追足以解释它的入口、转换和消费；用户要求完整流程或局部证据无法解释行为时，才展开跨文件链。账号、平台、构建差异只在会改变结论时核验并说明，不要求输出固定上下文卡。

账号敏感逻辑读取 [账号模式事实](../tuqiang-project-map/references/account-mode.md)，沿实际 `isEnterprise` 来源核验；不能从目录、accountType 或 target 猜测，也不能将 unknown 当成共享行为。

## 解释规则

- 关键结论提供当前路径、1-based 行号和必要的最小源码；区分事实、推断与证据停止点，不复制旧 reference 的行号。
- 遇到接口、barrel、route registry 或 Provider override，追到影响本题的实际实现；无需遍历无关入口和分支。
- 异步和重建相关问题区分“事件发起、数据完成、状态通知/UI 消费”，不要画成同步调用栈。只解释影响结论的身份、错误/空态、竞态与清理。
- 讲状态时按需说明定义、实例 key、写入和消费；不要把 route 参数、family key、单次 action 参数和 State 字段混为一类。
- 用户指定 Vue3 或 React 时只用该框架；未指定时给简短心智模型。只有用户要求时才展开完整代码或双框架比较，且标明类比与真实 Flutter 行为的差别。
- 解释现有封装和数据来源；若当前实现有问题，应指出证据，不把它作为推荐模式，也不顺手修改代码。

## 按需读取

| 问题 | Reference |
|---|---|
| 完整流程或跨文件字段血缘 | [完整追踪](references/full-flow-tracing.md) |
| Provider、混合状态、实例身份 | [状态与 Riverpod](references/state-and-riverpod.md) |
| 页面入口、传参和返回值 | [路由](references/routing.md) |
| 请求、异步结果和竞态 | [异步网络](references/async-networking.md) |
| 约束、布局和字段展示 | [布局 UI](references/layout-ui.md) |
| Widget 生命周期或资源释放 | [Widget 生命周期](references/widget-lifecycle.md) |
| 翻译 fallback、默认文案或展示取值 | [国际化与展示边界](../tuqiang-dev/references/i18n.md) |
| 本地状态/函数/组件复用、新增计算的纯函数边界 | [本地风格与复用](../tuqiang-dev/references/local-style-and-reuse.md) |
| 平台、渠道或原生 SDK 差异 | [构建上下文](../tuqiang-project-map/references/build-runtime-context.md) |

项目规则和当前源码优先于 references；只读取当前问题需要的资料。设备、地图、定位等 owner 不明时，从 [项目地图](../tuqiang-project-map/SKILL.md) 定位。

回答长度跟随问题规模：能用一段结论和两处证据讲清就到此为止；复杂流程再用链图或表格，不固定输出三条链、全状态卡或全量风险检查。
