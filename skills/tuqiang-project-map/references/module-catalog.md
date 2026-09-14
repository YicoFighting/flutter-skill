# Tuqiang 模块目录与职责

本目录用于定位当前 owner，不代替源码核验。先确认账号模式与运行入口，再由 import、barrel/router、composition、调用者和测试证明归属。

## Apps 与宿主

| 路径 | pubspec name | 当前职责 |
|---|---|---|
| `apps/standard` | `tuqiang_standard` | Android/iOS 宿主，`main` 调用 `runStandardApp` |
| `apps/ohos` | `tuqiang_ohos` | HarmonyOS 宿主，`main` 调用 `runOhosApp` 并注入平台 binding/backend |
| `apps/tuqiang_app` | `tuqiang` | App 壳、启动、Provider composition、路由、session、coordinator 与 app-local 代码 |

`tool/project.dart::AppTarget` 只是 target 候选索引。支持结论还需核对对应 app 被 Git 跟踪、pubspec identity 与实际入口，不能只信枚举或目录存在。

## Core packages

| Package | 主要职责/边界 |
|---|---|
| `core_base` | 基础类型、安全转换、尺寸、屏幕与权限工具 |
| `core_blue` / `core_blue_ohos` | 标准端与 HarmonyOS 蓝牙实现；后者提供兼容 package name |
| `core_color` | 不带产品主题语义的中性色彩原语 |
| `core_http` | `TQHttp`、delegate、结果模型与网络基础设施 |
| `core_i18n` | 翻译查找、语言类型和 String 扩展；Tuqiang 字典与 manifest 由 App 资源层拥有 |
| `core_log` | Dart/native 统一日志能力 |
| `core_region` | 地区检测 |
| `core_share` | 跨平台分享 |
| `core_ui` | 公共 UI、navigation contracts、checked registry、route effect、session reset contract |
| `core_union` | 跨 core 公共能力 |
| `core_webview` | WebView 工具与页面基础设施 |

读取目标包 `pubspec.yaml` 与公共 barrel；不能仅由 package 名推断完整职责。core 不应依赖 shared、feature 或 app。

## Shared 领域包

`shared_business` 已拆除。当前公共 barrel 位于 `packages/shared/<package>/lib/<package>.dart`：

| Package | 当前跨 feature 能力 | 高价值索引 |
|---|---|---|
| `shared_account` | 用户模型、session、账号偏好持久化 | `tq_user_model.dart`、`account_local_repository.dart` |
| `shared_activity` | Pet/ID Card 共用活动统计、图表与 API contract | package barrel、`src/application` |
| `shared_advertising` | 广告 model/state/repository、曝光与点击 | package barrel、根 Provider override |
| `shared_command` | 跨设备指令、远程设置与指令历史 | package barrel、调用方 |
| `shared_device` | 设备 identity、目录、能力、选择与外部 runtime contract | `device_catalog_provider.dart`、`device_core_commands.dart`、`device_core_runtime.dart` |
| `shared_location` | 定位状态、属性、能力、逆地理编码与展示派生 | `location_providers.dart`、`src/data`、`src/presentation` |
| `shared_media` | 播放、进度、文件、下载与视频设备 key | `media_download_queue_provider.dart`、`src/data` |
| `shared_message` | 消息、告警、设备摘要与已读状态 | package barrel、根 Provider override |

`shared_device` 通过 `DeviceCoreRuntime` 把定位/消息外部上下文交给 app composition，不直接反向 import 其他 shared 包。

## Feature packages

| Package | 当前主要流程 |
|---|---|
| `feature_ai` | AI 业务 |
| `feature_auth` | 登录、认证与账号入口 |
| `feature_camera` | 行车记录仪/监控、相册、P2P、摄像头配网 |
| `feature_device_management` | 添加、搜索、解绑等设备管理 |
| `feature_device_share` | 设备分享 |
| `feature_gps` | 地图、定位、轨迹、围栏、远程设置与指令历史 |
| `feature_id_card` | 学生证与运动统计 |
| `feature_message` | 消息列表、筛选与设置 |
| `feature_mifi` | Wi-Fi/MiFi、实名、套餐与网络控制 |
| `feature_mine` | 我的、账号资料与入口 |
| `feature_overview` | 设备总览 |
| `feature_pet` | 宠物/信标 |
| `feature_tag` | Tag 与跨 GPS 导航入口 |
| `feature_value_added` | 增值服务、套餐与 SIM 用量 |

跨 feature 页面通过 contract、route 或 app composition 连接；运行时能跳转不等于存在直接 Dart 依赖。

## App-local、plugin 与资源

- 尚未下沉的 manager/model/viewmodel/tools 位于 `apps/tuqiang_app/lib/app/legacy_shared`；设备列表等组合页面也可位于 App 层。当前位置是事实，不代表最终设计归属。
- 自研插件位于 `packages/plugins`，覆盖文件、日志、地图、P2P、推送、信号和视频原生能力；平台差异还可能位于 `packages/adapter` 与宿主目录。
- 公共资源位于 `packages/assets_common`；feature 私有资源位于 `packages/feature/<owner>/assets` 并由 asset 常量暴露。
- 个人/企业账号相关 owner 先按 [account-mode.md](account-mode.md) 追 session、composition、Repository 与缓存，不以“公共包”推断 `both`。

## Owner 定位顺序

1. 确认 `accountMode`、平台和可观察入口。
2. 从 Page/route/asset 常量查定义、barrel 与最终 builder。
3. 查 feature router/contract、shared 领域包和 `bootstrap.dart` override。
4. 多业务共用且带业务语义时核对 `shared_*`；无业务语义基础设施再核对 `core_*`。
5. 涉及原生能力时查 plugin、adapter、宿主 override 与目标平台实现。
6. 多个 owner 都合理且需求不足以排除时，列证据并请求最小澄清。

## 实时核验

用 tracked pubspec/name、barrel/import、Router/Composition/Runtime、真实调用方和资源声明重查 owner；目录列表本身不是证据。
