---
name: tuqiang-project-map
description: 从 Tuqiang 当前源码定位模块归属、路由、状态/数据链和影响范围；用于架构或业务调查。只读，不修改代码或输出 Web 教学。
license: Apache-2.0
metadata:
  version: "2.2.0"
---

# Tuqiang 项目地图

只调查 Tuqiang；公共 core/shared/plugin API 只反查技术契约，不扩展到其他产品线。

## 调查方式

1. 按 [根目录发现](references/project-root-discovery.md) 校验用户指定的 Git 根并读取项目 AGENTS.md；同一 checkout 复用结果，不扫描磁盘。
2. 从用户问题、文件或可观察事件出发，用 `rg -n` 查当前实现。先回答最小问题，再展开会改变结论的上下游。
3. 由调用方、import、router 或 composition 证明 owner；遇到 contract provider/callback 时追到实际注入实现。只有涉及状态、异步或切换时，才追写入、消费和清理。
4. 登录/session、账号相关请求、权限、缓存或可见性按 [账号模式](references/account-mode.md) 区分 personal/enterprise；平台、地图和设备变体只核验问题可达的分支。

当前源码、pubspec 与实际工具优先于本技能索引和迁移文档。不要因为文件位于 shared 就认定它适用于全部账号，也不要因为出现 Provider 就把整条链称为 Riverpod。

## 按问题读取

| 问题 | Reference |
|---|---|
| 分层、依赖、模块归属 | [架构](references/architecture-overview.md)、[模块 owner](references/module-catalog.md) |
| 启动、路由、分栏页面装配 | [启动与路由](references/startup-routing.md) |
| Provider/key/订阅与失效 | [状态拓扑](references/riverpod-topology.md) |
| 设备目录、选择与定位 | [设备定位](references/device-location-flow.md) |
| 账号、平台、地图、设备页面差异 | [账号模式](references/account-mode.md)、[变体](references/variant-surface.md) |
| 构建、推送、广告、ABI 或安装包 | [构建上下文](references/build-runtime-context.md) |
| 网络、session、国际化、尺寸与资源 owner | [基础设施](references/infrastructure-and-cross-cutting.md) |
| 展示值来源、缺 key、fallback 或重复兼容 | [国际化与展示取值](../tuqiang-dev/references/i18n.md) |
| 本地状态/函数/组件入口、纯函数边界 | [本地封装与复用](../tuqiang-dev/references/local-style-and-reuse.md) |
| 用户要求完整端到端链路 | [完整追踪](references/requirement-trace-playbook.md) |

## 完成标准

直接给出结论和关键路径、symbol、当前行号；必要时附最小源码片段。仅报告影响答案的账号/平台限制、未核验项或冲突，不输出必填上下文卡、空检查项或固定全链报告。

当问题已被当前证据解释时停止追踪。只有源码不能消除、且会改变答案的歧义才向用户澄清。API 只引用 symbol 和语义，不输出 endpoint、Token、Key、证书或生产配置。
