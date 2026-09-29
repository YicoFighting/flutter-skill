# flutter-to-web

版本 2.2.0。面向 Vue3/React 开发者，从当前 Tuqiang 源码解释目标功能、状态与 UI；只讲解，不修改代码。

入口见 [SKILL.md](SKILL.md)。简单问题使用最短证据链，完整业务链按需展开，不强制上下文卡或全状态表。用户指定 Vue3 或 React 时只输出对应框架；未指定时给简短 Web 心智模型。

- [完整业务链](references/full-flow-tracing.md)、[状态与 Riverpod](references/state-and-riverpod.md)
- [路由](references/routing.md)、[异步网络](references/async-networking.md)
- [布局 UI](references/layout-ui.md)、[Widget 生命周期](references/widget-lifecycle.md)
- [国际化与展示边界](../tuqiang-dev/references/i18n.md)：fallback 与展示值的单一处理边界
- [本地风格与复用](../tuqiang-dev/references/local-style-and-reuse.md)：已有封装优先，新增计算保持纯函数

账号或构建差异影响结论时，分别读取 [账号模式](../tuqiang-project-map/references/account-mode.md) 与 [构建上下文](../tuqiang-project-map/references/build-runtime-context.md)。共享 references 随四个技能一同安装。

版本变化见 [根 CHANGELOG](../../CHANGELOG.md)。许可证：Apache 2.0。
