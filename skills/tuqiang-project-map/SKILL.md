---
name: tuqiang-project-map
description: 为 Tuqiang Flutter monorepo 从当前源码定位仓库事实、个人/企业账号模式、模块 owner、状态/数据拓扑及平台、地图和设备页面变体；用于架构、路由、依赖、业务链或影响面调查。只提供证据，不修改代码或输出 Web 教学。
license: Apache-2.0
metadata:
  version: "2.1.0"
---

# Tuqiang 项目地图

只调查 Tuqiang。不要搜索、比较或汇报其他产品线的业务；公共 core/shared/plugin API 只反查技术调用契约。本 Skill 不修改代码或决定实现。

## 入口

1. 按 [根目录发现](references/project-root-discovery.md) 校验 Tuqiang Git 根并读取项目 AGENTS.md；用户路径优先，不扫描磁盘。
2. 建立上下文卡：

       product: tuqiang
       accountMode: personal | enterprise | both | unknown
       platform: Android | iOS | HarmonyOS | multiple | unknown
       owner: <symbol/package | unknown>
       entry: <event | unknown>
       observableEnd: <UI/state/storage/plugin | unknown>
       buildVariant: <涉及构建/原生差异时填写 flavor/channel/SDK>
       deviceOrMapScope: <相关时填写>

3. 登录/session、请求/DTO、设备目录、消息、权限、缓存、页面可见性、账号切换或退出一律读取 [账号模式](references/account-mode.md)。账号模式来自当前 isEnterprise 传播链，不是 accountType、target 或 flavor；证据不足写 unknown。
4. 只读命中专题，从可观察入口追到 owner、数据边界、状态发布、UI/插件终点与 reset/dispose。

## 调查与证据

- 在当前 checkout 用 rg -n 重查路径、symbol 和 1-based 行号。优先级：AGENTS.md 与当前源码/pubspec/lockfile → 实际 tool/CI → 测试 → 当前状态文档 → references。
- 用户文件只是锚点；向上追入口、路由与 composition，向下追 Repository/Manager/HTTP/缓存/插件，向旁追写入者、消费者和清理。
- 分开同步事件、异步返回和响应式重建。只描述实际使用的 Riverpod、Manager、setState、Controller 或缓存机制。
- owner 由 import、router/barrel、composition override、调用者和测试共同证明；contract provider、callback 或 route registry 必须追到最终实现。
- 平台、地图后端、设备 scene 与 route/Page 是独立维度，只在相关任务展开；无需修改也要有证据。
- 只引用接口 symbol 与语义，不输出 endpoint、Token、Key、证书或生产配置值。

## Reference 路由

| 读取条件 | Reference |
|---|---|
| 首次定位或 checkout 不明 | [project-root-discovery.md](references/project-root-discovery.md) |
| 构建、推送、广告、ABI 或安装包差异 | [build-runtime-context.md](references/build-runtime-context.md) |
| 账号敏感行为（强制） | [account-mode.md](references/account-mode.md) |
| 分层、依赖与状态体系 | [architecture-overview.md](references/architecture-overview.md) |
| app/feature/shared/core/plugin owner | [module-catalog.md](references/module-catalog.md) |
| main、bootstrap、composition 与路由 | [startup-routing.md](references/startup-routing.md) |
| Provider/family、key、订阅与失效 | [riverpod-topology.md](references/riverpod-topology.md) |
| 设备目录、选择与定位 | [device-location-flow.md](references/device-location-flow.md) |
| 平台、地图或设备页面变体 | [variant-surface.md](references/variant-surface.md) |
| 网络、session、i18n、尺寸或资源 | [infrastructure-and-cross-cutting.md](references/infrastructure-and-cross-cutting.md) |
| 完整端到端调查 | [requirement-trace-playbook.md](references/requirement-trace-playbook.md) |

## 停止与完成

会改变 owner、账号分支、route、设备范围或外部契约且源码不能唯一确认时，报告候选和证据后只问一个必要问题；不得用默认模式、自创资源或迁移目标补空白。

完成时必须证明：根目录有效；accountMode 已标注；关键跳有当前路径、行号、symbol 和最小证据；链路覆盖身份/key、写入、消费、异步、UI 与 reset/dispose；相关变体已关闭，未知与敏感信息处理正确。
