# 架构总览

## 1. 这是什么仓库

`<TUQIANG_ROOT>` 表示当前已通过仓库特征校验的途强 Flutter monorepo 根目录。该仓库用同一套共享业务支撑三端：

```text
apps/standard ─┐
               ├─> apps/tuqiang_app ─> feature_* ─┐
apps/ohos ─────┘                    ├> shared_business ─> core_*
                                   └> plugins / adapter / assets_common
```

图表示“上层组合并依赖下层”，不是运行时调用顺序。实际 `pubspec.yaml` 可能包含更多直接依赖，回答具体问题时要检查相关 package 的当前依赖。

- `apps/standard`：Android/iOS 宿主入口。
- `apps/ohos`：HarmonyOS 宿主入口，包含平台初始化和依赖 override。
- `apps/tuqiang_app`：共享 App 壳、启动编排、路由聚合、feature composition、session 协调，以及尚未下沉的历史业务页面。
- `packages/feature/*`：具有独立用户流程的业务 owner。
- `packages/shared/shared_business`：多个 feature 共用的设备、定位、视频基础契约、消息摘要、账号和通用业务能力。
- `packages/core/*`：不带单一业务语义的基础设施。
- `packages/plugins/*` 与 `packages/adapter/*`：原生能力和平台/三方适配。
- `packages/assets_common`：跨模块公共资源。

## 2. 运行时分层

| 层 | 真实职责 | 关键入口 |
|---|---|---|
| 宿主入口 | 选择平台环境并接入原生初始化 | `apps/standard/lib/main.dart` 的 `main`；`apps/ohos/lib/main.dart` 的 `main` |
| Bootstrap | 初始化环境、缓存、i18n、HTTP、插件并创建根作用域 | `apps/tuqiang_app/lib/bootstrap.dart` 的 `runStandardApp`、`runOhosApp`、`prepareAppStartupData`、`getApp` |
| App composition | 用 Provider overrides/callback 将 feature 与 app 能力组装 | `bootstrap.dart` 的 `getApp` 与 `ProviderScope` |
| App 壳 | 首屏选择、MaterialApp、路由、locale、尺寸初始化 | `apps/tuqiang_app/lib/app.dart` 的 `StrongApp`、`_StrongAppState` |
| 路由聚合 | 合并 feature route，保留兼容 alias，执行 route effect | `app/router/app_router.dart`、`app/router/feature_router_registry.dart` |
| 业务状态 | feature 私有状态与 shared 跨 feature 状态 | 各 `providers.dart`、Notifier/State、Manager/Controller |
| 数据边界 | Repository、TQHttp、SharedPreferences、缓存、插件 | `packages/**/data`、`packages/core/core_http`、各 Manager |
| 展示 | ConsumerWidget/ConsumerStatefulWidget、派生 presentation Provider、普通 StatefulWidget | `apps/tuqiang_app/lib/app/**`、`packages/feature/**/pages` |

## 3. 依赖与组合的关键事实

- feature 之间的页面跳转或页面嵌入常通过 contract、Navigator callback 或 app 侧 composition builder 连接，不能只沿 Dart import 判断完整运行链。
- `bootstrap.dart` 的根 `ProviderScope(overrides: ...)` 是依赖注入和跨 feature 组合的重要证据；解释需求时不能把它当作无关样板跳过。
- `FeatureRouterRegistry` 聚合各 feature 的 checked routes/native routes/route effects，`AppRouters` 仍承担兼容路由名和 app 自有页面。
- `shared_business` 是跨 feature 业务层，不等同于无业务语义的 core；设备身份、设备目录、定位快照等共享状态位于此处。
- `apps/tuqiang_app` 仍有历史业务代码。迁移文档中的目标 owner 与当前文件位置可能不同，必须查当前源码与 route builder。

## 4. 混合状态架构

项目不是“所有数据都在 Riverpod”这种单一结构。常见链路会同时包含：

```text
Widget setState / Controller
        │
        ├─ Riverpod Provider / Notifier / family cache
        │       └─ Repository ─> TQHttp / plugin
        │
        ├─ Manager / singleton（全局模型、地图、屏幕安全等）
        └─ SharedPreferences / 文件缓存 / 数据库
```

例如设备列表分页中的 `_isLoading` 由 Widget `setState` 管理，目录数据由 `deviceCatalogProvider` 管理；定位状态进入 `deviceLocationSnapshotProvider(deviceRef)`，同时 `DeviceLocationSnapshotNotifier.applyStatus` 会同步坐标给 `TQInfoManager`。解释时要分别标注每一份状态的 owner，不能把它们合并成一个“全局 Provider”。

## 5. 当前事实与迁移目标

优先用于确认当前事实：

- `AGENTS.md`
- `README.md`
- 当前源码、`pubspec.yaml`、lockfile
- `tool/check_migration_boundaries.ps1`
- `tool/run_migration_tests.ps1`
- 相关测试

架构背景与迁移上下文：

- `docs/feature_business_package_split_plan.md`
- `docs/shared_business_and_tuqiang_app_restructure_plan.md`
- `docs/三端分支统一合并实施方案.md`
- `docs/ohos_migration_inventory.md`

阅读 docs 时必须识别“已完成/当前状态”和“目标/计划/候选”措辞。只有在源码或门禁中能对应到的内容，才可作为运行时结论。

## 6. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "runStandardApp|runOhosApp|ProviderScope|class StrongApp" apps --glob '*.dart'
rg -n "class AppRouters|class FeatureRouterRegistry|routes\(|nativeRoutes|routeEffects" apps packages --glob '*.dart'
rg -n "package:tuqiang/|package:feature_" packages --glob '*.dart'
rg -n "StateNotifierProvider|NotifierProvider|FutureProvider|Provider<|setState\(|Manager\.shared|TQHttp\." apps packages --glob '*.dart'
```

不要把这些命令的历史结果写成永远成立的事实；每次回答只报告本次实际命中。
