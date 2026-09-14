# flutter-to-web

版本 2.1.0。面向 Vue3/React 开发者，从当前 Tuqiang 源码解释用户事件、异步数据、状态通知和最终 UI；不修改代码。

入口见 [SKILL.md](SKILL.md)。按需读取：

- [完整业务链](references/full-flow-tracing.md)
- [状态与 Riverpod](references/state-and-riverpod.md)
- [路由](references/routing.md)、[异步网络](references/async-networking.md)
- [布局 UI](references/layout-ui.md)、[Widget 生命周期](references/widget-lifecycle.md)

账号敏感问题统一读取项目地图的 [account-mode.md](../tuqiang-project-map/references/account-mode.md)。用户指定 Vue3 或 React 时只输出对应框架；未指定时给简洁 Web 心智模型。

安装包行为不同时，读取 [构建上下文](../tuqiang-project-map/references/build-runtime-context.md)，沿 flavor/channel 追到实际原生实现。

版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
