# tuqiang-project-map

`tuqiang-project-map` 是途强三端 Flutter monorepo 的项目事实、架构分层与跨文件索引 skill，版本 `1.1.1`。它按仓库身份动态发现 `<TUQIANG_ROOT>`，不绑定某台电脑的安装路径。

它解决四类问题：

- 从三端入口、App composition root 和路由 registry 定位页面如何装配；
- 从用户操作追到 Riverpod 状态、family key、Repository、网络/缓存、session reset 和 UI 消费；
- 快速确认 feature、shared、core、plugin、adapter 与 app 壳的 owner、依赖方向和复用入口；
- 为 `flutter-to-web` 提供教学事实，为 `tuqiang-dev` 提供代码归属与复用索引，为 `tuqiang-change-retrospective` 提供变更后复盘所需的当前链路证据。

## 使用边界

本 skill 不做 Vue3/React 教学，也不自行决定实现方案或修改代码。需要前端类比时由 `flutter-to-web` 消费本 skill 的证据，需要开发、修复和验证时由 `tuqiang-dev` 做最终取舍；变更完成后的 Git 因果与学习文档由 `tuqiang-change-retrospective` 负责。

reference 不固定源码行号。使用时必须先校验 `<TUQIANG_ROOT>`，再通过 `rg -n` 重新确认 symbol 的当前行号，并以当前源码为准。设备/GPS 只是已收录的一条代表性业务链，不是该 skill 的主职责。

## 文件结构

```text
tuqiang-project-map/
├── SKILL.md
├── README.md
├── LICENSE.txt
└── references/
    ├── architecture-overview.md
    ├── project-root-discovery.md
    ├── module-catalog.md
    ├── startup-routing.md
    ├── riverpod-topology.md
    ├── device-location-flow.md
    ├── infrastructure-and-cross-cutting.md
    └── requirement-trace-playbook.md
```

## 典型触发语句

- “解释这个页面从进入到数据展示的完整链路。”
- “这个 Provider 为什么能传设备参数，状态到底存在哪里？”
- “点击设备后如何选中、请求定位状态并更新 UI？”
- “这个需求应该经过哪些 package、route 和 composition callback？”
- “这段共享逻辑应该放在 feature、shared_business 还是 core，项目里有没有可复用入口？”
