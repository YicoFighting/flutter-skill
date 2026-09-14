# Tuqiang 架构总览

## 分层与依赖方向

```text
apps/standard ─┐
               ├─> apps/tuqiang_app ─> packages/feature/* ─┐
apps/ohos ─────┘                    └> packages/shared/* ──┼─> packages/core/*
                                                         └─> packages/plugins/* / adapter / assets_common
```

图表示组合与依赖方向，不是运行时调用顺序。具体结论仍需读取相关 `pubspec.yaml`、import、barrel、composition override 和调用者。

| 层 | 当前职责 | 关键入口 |
|---|---|---|
| 宿主 | 标准端与 HarmonyOS 平台初始化 | `apps/standard/lib/main.dart::main`、`apps/ohos/lib/main.dart::main` |
| 启动协调 | 首屏前环境/用户/i18n/HTTP/缓存任务与首帧后任务 | `apps/tuqiang_app/lib/app/coordinators/app_startup_data_coordinator.dart::AppStartupDataCoordinator` |
| Composition root | 根 `ProviderScope` overrides、跨 feature/runtime callback、平台能力注入 | `apps/tuqiang_app/lib/bootstrap.dart::getApp` |
| App 壳 | 首屏、生命周期、尺寸、locale、`MaterialApp` | `apps/tuqiang_app/lib/app.dart::StrongApp` |
| Dart 路由 | app alias、自有页面、checked feature routes、动态参数 | `apps/tuqiang_app/lib/app/router/app_router.dart::AppRouters` |
| 路由元数据 | native routes、screen secure、route effects、刷新分类 | `apps/tuqiang_app/lib/app/router/feature_router_registry.dart::FeatureRouterRegistry` |
| 业务 owner | 独立用户流程与跨 feature 领域状态 | `packages/feature/*`、`packages/shared/shared_*` |
| App-local 边界 | 尚未下沉或只由 App 组合的 manager/model/viewmodel/tools | `apps/tuqiang_app/lib/app` |

当前正式 shared 领域包为 `shared_account`、`shared_activity`、`shared_advertising`、`shared_command`、`shared_device`、`shared_location`、`shared_media`、`shared_message`。回答前仍应以 tracked pubspec 为准。

## 关键组合事实

- `bootstrap.dart::getApp` 是跨包注入证据。feature/shared 只看到 contract provider 或 runtime callback 时，继续追根 override 到最终 Page、Manager、Repository 或 plugin。
- `AppRouters.getRouters` 负责 Dart route map 与 checked feature route 合并；`FeatureRouterRegistry` 负责 native route 和 effect/security/refresh 元数据。
- `shared_device::DeviceCoreRuntime` 通过 app composition 注入定位/消息外部上下文，避免 shared 包反向依赖。
- `core_ui` 除 Widget 外还导出 navigation contracts、checked registry、route effect 和 `SessionResetParticipant`；owner 不能仅由包名推断。
- `core_*` 不应依赖 shared、feature 或 app。修改公共 API 时反查当前仓库全部调用者。

## 混合状态体系

```text
Widget setState / Controller
        ├─ Riverpod Provider / Notifier / family cache
        │       └─ Repository ─> TQHttp / plugin
        ├─ Manager / singleton
        └─ SharedPreferences / 文件 / 数据库
```

具体页面可能同时经过多种机制。只有实际经过 Provider 的链路才能称为 Riverpod；`read`、`watch`、`listen`、`select` 和 Manager setter 要分别说明。

个人/企业是运行时账号模式，不属于上述层级或宿主 target。涉及 session、请求、缓存或可见性时读取 [account-mode.md](account-mode.md)。

## 当前事实与迁移资料

优先核验 `AGENTS.md`、当前源码、各 `pubspec.yaml`/lockfile、`tool/project.dart`、门禁脚本和相关测试。`docs/` 中的迁移方案只能解释背景；目标结构不等于当前运行结构，大型方案中的历史基线也不能覆盖源码。

## 实时核验

用 tool/project.dart、宿主入口、startup/ProviderScope/StrongApp、AppRouters/FeatureRouterRegistry 和目标 import 重查当前分层；reference 路径不能替代实时证据。
