# tuqiang-project-map

`tuqiang-project-map` 是途强 Flutter monorepo 的项目事实、架构分层与跨文件索引 skill，版本 `1.3.0`。它按仓库身份动态发现 `<TUQIANG_ROOT>`，先识别 Tuqiang/Laoying 产品线，再恢复状态、路由、owner，以及平台、地图后端和设备页面变体。

它解决五类问题：

- 从六个宿主/共享 App 入口定位两条产品线的启动与页面装配；
- 对 Tuqiang 追踪 Riverpod family、Repository、session reset 与 UI，对 Laoying 追踪 `LYAppProvider`、app-local controller/repository 与 LY 路由；
- 确认 feature、8 个 `shared_*` 领域包、core、plugin、adapter 与 app-local 代码的当前 owner 和依赖方向；
- 把 Android/iOS/HarmonyOS、宿主 target、百度/高德/Google/Map Kit、设备类型/scene 与最终 route/Page 拆成带可达证据的候选矩阵，避免用一个页面或一个 target 代表全部实现；
- 为 `flutter-to-web`、`tuqiang-dev`、`tuqiang-change-retrospective` 提供可实时核验的项目事实。

## 使用边界

本 skill 不做 Vue3/React 教学，不自行决定实现方案或修改代码。产品线、owner、资源来源或验收语义存在会改变结论的歧义时，它只列已核验候选并询问用户，不用临时绘制、默认文案或自创 contract 填补决策。

reference 不固定源码行号。使用时先校验当前对话所附项目/工作区；用户明确路径时以用户路径为准。然后用 `rg -n` 重新确认 symbol 的当前行号，并以当前源码为准。物理存在但没有 tracked `pubspec.yaml` 的目录不能视为有效 package。

设备/GPS 专题只覆盖 Tuqiang 的代表性业务链，不代表 Laoying 采用相同实现。设备列表后的 GPS、LBS、Camera、Tag、MiFi 等页面叶子必须实时枚举；用户所称“花瓣地图”映射为 HarmonyOS 的华为 Map Kit 平台后端，不把它写成源码 SDK 名，也不虚构第四个 `TQMapSourceType`。

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
    ├── variant-surface.md
    ├── infrastructure-and-cross-cutting.md
    └── requirement-trace-playbook.md
```

## 典型触发语句

- “这个文件属于 Tuqiang 还是 Laoying，启动后怎么进入该页面？”
- “这个 Provider 为什么能传设备参数，状态到底存在哪里？”
- “Laoying 登录态由谁发布，LY 路由如何找到最终页面？”
- “这个需求应该经过哪个 package、route 和 composition/runtime callback？”
- “设备列表点进去和再点更多详情，当前到底有多少种设备页面分支？”
- “这个地图改动在百度、高德、Google 和鸿蒙 Map Kit 分别落到哪里？”
- “这段共享逻辑应放在 feature、某个 `shared_*`、core，还是产品 app-local 层？”
