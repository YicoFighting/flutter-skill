---
name: flutter-to-web
description: 面向 Vue3/React 开发者，从当前 Tuqiang 源码解释目标功能、状态、路由与 UI，并按需给出 Web 对照。只讲解，不修改代码。
license: Apache-2.0
metadata:
  version: "2.4.0"
---

# Tuqiang Flutter 讲解

围绕用户的问题解释当前 Tuqiang 实现：先给结论，再用最短的源码因果链说明为什么；不逐句翻译 Dart，不扩展到其他产品。需要改代码时转 tuqiang-dev。

## 边界

按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 确认 checkout 并读取项目 `AGENTS.md`；路径、symbol、行号与依赖版本以当前源码为准。owner 不明时用 [项目地图](../tuqiang-project-map/SKILL.md) 定位。

单个字段、组件或状态只追足以解释它的入口、转换与消费；用户要求完整流程或局部证据解释不了时才跨文件展开。账号、平台、构建差异只在改变结论时核验，账号以实际 `isEnterprise` 来源为准（[账号模式](../tuqiang-project-map/references/account-mode.md)），不从目录、accountType 或 target 猜测。

## 解释规则

- 关键结论给当前路径、1-based 行号与最小源码；区分事实、推断与证据停止点。
- 接口、barrel、route registry 或 Provider override 要追到影响本题的实际实现（多数在 `bootstrap.dart::getApp`）。
- 异步区分三个维度：事件（操作/生命周期 → callback → command）、数据（输入 → HTTP/cache/plugin → Model/错误 → State）、更新（通知/派生 → build/listener → UI）。await、listener、post-frame 与 rebuild 说明触发关系，不画成同步栈。
- 讲状态时区分 route 参数、family key、accountMode、单次 action 参数与 State 字段；只解释影响结论的身份、错误/空态、竞态与清理。
- 字段问题沿"来源 → Model/mapper → 消费者"追一次，指出 fallback/兼容由谁负责（[国际化与展示取值](../tuqiang-dev/references/i18n.md)），不建议多层重复处理。
- 当前实现有问题时指出证据，不把它当推荐模式，也不顺手修改。

## Web 对照

用户指定 Vue3 或 React 时只用该框架；未指定时给一两句心智模型。只有用户要求时才展开完整代码或双框架比较，并标明类比与真实 Flutter 行为的差别。对照表与易混语义见 [Web 对照](references/web-analogies.md)。

## 按需读取

| 问题 | Reference |
|---|---|
| Provider/混合状态、生命周期、竞态与资源释放 | [状态拓扑](../tuqiang-project-map/references/state-device-flow.md)、[状态与异步](../tuqiang-dev/references/state-async.md) |
| 启动、路由、分栏 | [启动与路由](../tuqiang-project-map/references/startup-routing.md) |
| 布局、尺寸、组件封装 | [UI 与路由](../tuqiang-dev/references/ui-routing-assets.md)、[本地复用](../tuqiang-dev/references/local-style-and-reuse.md) |
| 平台、地图、设备页面、渠道或原生 SDK | [变体与构建](../tuqiang-project-map/references/variants.md) |

回答长度跟随问题规模：一段结论加两处证据能讲清就到此为止；复杂流程再用链图或表格，不固定输出三条链、全状态卡或全量风险检查。
