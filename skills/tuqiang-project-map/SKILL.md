---
name: tuqiang-project-map
description: 从 Tuqiang 当前源码定位模块归属、路由、状态/数据链、账号与平台/地图/设备变体及影响范围；用于架构或业务调查。只读，不修改代码，不输出 Web 教学。
license: Apache-2.0
metadata:
  version: "2.4.0"
---

# Tuqiang 项目地图

只调查 Tuqiang；core/shared/plugin 公开 API 只反查技术契约，不扩展到同仓老鹰等其他产品。

## 调查方式

1. 按 [根目录发现](references/project-root-discovery.md) 校验 checkout，读取业务仓库 `AGENTS.md`，命中时再读 `DESIGN.md` 与相关 `.codex/skills/*`；同一 checkout 复用结果。
2. 从用户问题、文件或可观察事件出发，用 `rg -n` 限定 owner/symbol 查当前实现；先答最小问题，只展开会改变结论的上下游。
3. 用调用方、import、router 或 composition 证明 owner；contract provider/callback 追到 `bootstrap.dart::getApp` 的实际注入。
4. 账号、平台、地图、设备变体只核验问题可达的分支。

当前源码、pubspec/lockfile 与工具脚本优先于本技能索引和 `docs/` 迁移方案；reference 中的路径和 symbol 只是检索 seed。

## 按问题读取

| 问题 | Reference |
|---|---|
| 分层、依赖、模块 owner | [架构与模块](references/architecture.md) |
| 启动、composition、路由、分栏 | [启动与路由](references/startup-routing.md) |
| Provider/key/订阅，设备目录 → 选择 → 定位 | [状态与设备链](references/state-device-flow.md) |
| 登录/session、账号相关请求、缓存、可见性 | [账号模式](references/account-mode.md) |
| 平台、地图后端、设备页面族、flavor/渠道/SDK | [变体与构建](references/variants.md) |
| 网络、持久化、session reset、i18n 链、尺寸、资源 | [基础设施](references/infrastructure.md) |
| 展示取值/fallback，可复用的状态、函数、组件 | [国际化](../tuqiang-dev/references/i18n.md)、[本地复用](../tuqiang-dev/references/local-style-and-reuse.md) |

## 完整链路

仅在用户要求端到端说明或局部证据解释不了时展开，沿实际经过的阶段取证：

1. 入口：用户事件/生命周期/原生回调、route 参数、最终 builder；分栏区分 master 与 detail。
2. 状态身份：实际 Provider/Manager/Controller、key 与账号 scope、写入与消费。
3. 数据边界：Repository/HTTP/cache/plugin 的输入与映射。
4. 异步发布：loading/error/empty、旧结果判断、pending 与回写。
5. 可观察终点：展示字段、可见性、按钮或地图/原生参数。
6. 与问题相关的清理：退出页面、切 key/设备/账号/语言。

异步链区分"事件 → 调度 → 返回 → 响应式消费"，不能画成同步栈；mounted 不能证明结果仍属于当前账号或设备。

## 完成标准

先给结论，再给关键路径、symbol 和当前 1-based 行号，必要时附最小片段；只报告影响答案的账号/平台限制、未核验项与冲突，不输出空检查项。证据足以解释问题即停止；源码无法消除且会改变答案的歧义才澄清。API 只引用 symbol 与语义，不输出 endpoint、Token、Key、证书或生产配置。
