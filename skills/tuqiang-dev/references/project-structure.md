# 目录与归属决策

## 1. 分层和依赖方向

项目总体方向为：

```text
apps/standard, apps/ohos
          ↓
apps/tuqiang_app
          ↓
feature → shared_business / core / plugins / adapter
```

实际依赖以各 package 的 `pubspec.yaml` 为准。feature 可以依赖满足业务所需的稳定插件或 core 能力，但不能依赖 app，也不能为了复用页面反向依赖其他 feature。

| 位置 | 主要职责 | 新代码边界 |
|---|---|---|
| `apps/standard` | Android/iOS 配置、渠道、签名 | 不放共享业务 |
| `apps/ohos` | HarmonyOS 配置、override、DevEco 工程 | 不把 OHOS 专属类型扩散到公共 Dart |
| `apps/tuqiang_app/lib/app` | 启动、路由聚合、session、平台注入、App 壳 | 新业务页面优先下沉 feature；历史代码按迁移计划处理 |
| `packages/feature/feature_xxx` | 某一业务域的页面、状态、模型、路由、资源和回调 | 不 import `package:tuqiang/`，不消费别的 feature 私有 `src` |
| `packages/shared/shared_business` | 两个及以上模块稳定共享的业务模型、Provider、manager | 不放单一 feature 页面和私有状态 |
| `packages/core/core_*` | 网络、i18n、UI、尺寸、权限等基础能力 | 不放具体业务 |
| `packages/plugins/tq_*` / `packages/adapter` | 原生插件和平台适配 | 先复用现有能力，再评估新增通道 |
| `packages/assets_common` | 多模块或 App 壳共享资源 | 单 feature 资源不要继续堆这里 |

## 2. 找 owner 的顺序

1. 找页面当前唯一 builder、route、callback、asset 和 Provider 使用者；
2. 判断能力是单 feature、跨 feature 还是基础设施；
3. 找目标 package 的公开 barrel/API 和已经存在的复用入口；
4. 在同一子域与目标 package 抽样 2–4 个成熟同类实现，再看同层 sibling feature；
5. 检查包外调用方、pubspec、测试、Android/iOS/OHOS 资源；样本冲突时优先当前 owner 中较新且有调用方或测试的模式；
6. 只迁移能证明 owner 已完整转移的内容，避免留下两套事实来源。

feature 内部目录可能是 `pages`、`page`、`controller`、`state`、`router`、`route_effects`、`callbacks` 等不同组合。同一业务域也可能同时存在 `TQ`、`Tq`、无前缀，或 `StateNotifier`、`ChangeNotifier` 等历史模式。目录与命名规范是局部证据，不是要求把所有模块强行重排成同一脚手架；具体采样和复用决策见 [local-style-and-reuse.md](local-style-and-reuse.md)。

## 3. 迁移边界

涉及业务下沉时保持：

- route 字符串、arguments 类型、返回值和栈行为；
- H5/scheme/push/native 入口和 route effect；
- feature-owned 资源的完整倍率/帧/JSON 家族；
- feature → app 的 callback/config/bridge 方向；
- `shared_business` 不反向依赖 feature；
- 新依赖进入实际 owner 的 pubspec，必要时同步受影响 lockfile。

迁移中的目标 feature 和检查范围以 `tool/check_migration_boundaries.ps1` 及
`docs/feature_business_package_split_plan.md` 为准，不要凭本文件的概括扩大检查范围。

## 4. 快速决策

| 想新增的内容 | 优先位置 |
|---|---|
| 只服务宠物页面的 API/Model/Provider/图片 | `feature_pet` |
| GPS、Camera、Pet 等 feature 间的跳转 | feature 提供 callback/config，app 负责组装 |
| 多 feature 都需要的稳定用户/设备模型 | `shared_business`，先确认没有更合适的 core |
| 请求封装、翻译、通用 Toast/AppBar | 对应 `packages/core/core_*` |
| 蓝牙、地图、文件、推送等原生能力 | 现有 `packages/plugins/tq_*` 或 `packages/adapter` |
| 设计图中的业务图片 | 真实消费者所属 feature；共享资源才进 `assets_common` |
