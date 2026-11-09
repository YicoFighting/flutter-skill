# Tuqiang 架构与模块 owner

目录与表格只是定位入口；owner 结论由 tracked pubspec、barrel/import、router、composition 与真实调用方证明。

## 分层与依赖方向

```text
apps/standard ─┐
               ├─> apps/tuqiang_app ─> feature_* ─> shared_* ─> plugin/adapter ─> core_*
apps/ohos ─────┘
```

只允许高层依赖低层。层级细则（core_base/core_log → 普通 core → core_ui/core_webview → core_union → plugin/adapter → shared → feature → app）、禁止的聚合包与新建/移动 package 的联动要求，以业务仓库 `.codex/skills/tuqiang-flutter-architecture` 和 `tool/check_dependency_architecture.ps1` 为准。跨包只用公开 barrel，不引用他包 `src`。

| 层 | 职责 | 关键入口 |
|---|---|---|
| 宿主 | Android/iOS 与 HarmonyOS 平台初始化、原生注入 | `apps/standard/lib/main.dart`、`apps/ohos/lib/main.dart` |
| 启动协调 | 首屏前环境/用户/i18n/HTTP/缓存与首帧后任务 | `app/coordinators/app_startup_data_coordinator.dart::AppStartupDataCoordinator` |
| Composition root | 根 `ProviderScope` overrides、跨 feature callback、平台能力注入 | `apps/tuqiang_app/lib/bootstrap.dart::getApp` |
| App 壳 | 首屏、生命周期、分栏尺寸、locale、`MaterialApp` | `apps/tuqiang_app/lib/app.dart::StrongApp` |
| 路由 | Dart route map/自适应路由；native route 与 effect 元数据 | `app/router/app_router.dart::AppRouters`、`feature_router_registry.dart::FeatureRouterRegistry` |
| App-local | 尚未下沉的 manager/model/viewmodel/tools，及设备列表等组合页面 | `apps/tuqiang_app/lib/app`（含 `legacy_shared`） |

当前位置是事实，不代表目标设计；`docs/` 下的迁移方案只解释背景。

## Core

| Package | 职责 |
|---|---|
| `core_base` | 基础类型、安全转换、尺寸（`TQSizeFit`/`.sc`/`Screen`）、颜色常量 `TQColors`、权限工具 |
| `core_blue` / `core_blue_ohos` | 标准端 / HarmonyOS 蓝牙 |
| `core_color` | 无产品语义的色彩原语 |
| `core_http` | `TQHttp`、delegate、`ResultModel` |
| `core_i18n` | `TQI18nManager`、`TQLanguageType`、`String.tr`；字典与 manifest 归 App 资源层 |
| `core_log` / `core_region` / `core_share` | 日志、地区检测、分享 |
| `core_ui` | 公共组件、navigation contracts、checked registry、route effect、`SessionResetParticipant`、`adaptive_layout.dart` 分栏能力、`src/neutral` 中性组件 |
| `core_union` / `core_webview` | 跨 core 公共能力 / WebView 页面与 scheme 页面 |

## Shared 领域包

公共 barrel 位于 `packages/shared/<package>/lib/<package>.dart`；`shared_business` 已拆除。

| Package | 能力 | 检索入口 |
|---|---|---|
| `shared_account` | 用户模型、session、账号偏好持久化 | `tq_user_model.dart`、`account_local_repository.dart` |
| `shared_activity` | Pet/ID Card 活动统计、图表与 API contract | barrel、`src/application` |
| `shared_advertising` | 广告 model/state/repository、曝光与点击 | barrel、根 override |
| `shared_command` | 跨设备指令、远程设置、指令历史 | barrel、调用方 |
| `shared_device` | 设备 identity、目录、能力、选择、外部 runtime contract | `device_catalog_provider.dart`、`device_core_commands.dart`、`device_core_runtime.dart` |
| `shared_location` | 定位状态、逆地理、展示派生、地图面板 | `location_providers.dart`、`location_display_utils.dart`、`widgets/map_panel_layout.dart` |
| `shared_media` | 播放、进度、文件、下载、视频设备 key | `media_download_queue_provider.dart`、`src/data` |
| `shared_message` | 消息、告警、设备摘要、已读 | barrel、根 override |

`shared_device` 通过 `DeviceCoreRuntime` 把定位/消息外部上下文交给 app composition，不反向 import 其他 shared。

## Feature

| Package | 主要流程 |
|---|---|
| `feature_ai` | 小途 AI（图片/视频/确认） |
| `feature_auth` | 登录、认证、语言选择入口 |
| `feature_camera` | 行车/监控/移动摄像头、回放、相册、P2P、配网 |
| `feature_device_management` / `feature_device_share` | 添加/搜索/解绑设备；设备分享 |
| `feature_gps` | 地图、定位、轨迹、围栏、远程设置、指令历史、通讯录 |
| `feature_id_card` / `feature_pet` / `feature_tag` | 学生证；宠物/信标（含 D38Max、常去地点）；Tag 与跨 GPS 导航入口 |
| `feature_message` / `feature_mine` / `feature_overview` | 消息；我的与设置；设备总览 |
| `feature_mifi` / `feature_value_added` | Wi-Fi/MiFi；增值服务、套餐、SIM 用量 |

跨 feature 通过 contract、route 或 app composition 连接；运行时能跳转不等于存在直接 Dart 依赖。

## Plugin、adapter 与资源

- `packages/plugins`：`tq_map_plugin`（地图）、`tq_push_plugin`（推送，含 Android 原生 Gradle module）、`tq_p2p_plugin`、`tq_vsdk_plugin`（视频）、`tq_filemanage_plugin`、`tq_log_plugin`、`tq_signal_plugin`、`flutter_lame_update`（MP3 编码）、`adscope_sdk_ohos`。
- `packages/adapter`：OHOS 兼容实现（share/webview/umeng）与 `adscope_sdk_adapter`、`app_settings`。平台差异还可能在宿主目录。
- 公共资源 `packages/assets_common`；feature 私有资源在 `packages/feature/<owner>/assets`，经 asset 常量暴露。
- 推送/广告/地图原生依赖由宿主构建变体选择，见 [变体与构建](variants.md)。

## 混合状态

```text
Widget setState / Controller
   ├─ Riverpod Provider / Notifier / family
   │     └─ Repository ─> TQHttp / plugin
   ├─ Manager / singleton
   └─ SharedPreferences / 文件 / 数据库
```

同一页面可能同时经过多种机制；只有实际经过 Provider 的链路才称为 Riverpod。个人/企业是运行时账号模式，不属于任何层，见 [账号模式](account-mode.md)。

## Owner 定位顺序

Page/route/asset 常量 → 定义与调用者 → 跨包 contract 追 feature router 与 `getApp` override → 业务共用查 `shared_*`、基础设施查 `core_*` → 原生能力追 plugin/adapter/宿主。归属明确即停止。修改公共 API 时反查当前仓库全部调用者。
