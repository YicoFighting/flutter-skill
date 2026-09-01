# 模块目录与职责

本目录用于定位当前 owner，不代替源码核验。第一步永远是确认产品线；相同业务名在 Tuqiang 与 Laoying 中可能属于完全不同的目录和状态体系。

## 1. Apps 与产品入口

| 产品 | 路径 | pubspec name | 当前职责 |
|---|---|---|---|
| Tuqiang | `apps/standard` | `tuqiang_standard` | Android/iOS 宿主，`main` 调用 `runStandardApp` |
| Tuqiang | `apps/ohos` | `tuqiang_ohos` | HarmonyOS 宿主，`main` 调用 `runOhosApp` 并注入平台 binding/backend |
| Tuqiang | `apps/tuqiang_app` | `tuqiang` | App 壳、启动、Provider composition、路由、session、coordinator 与 app-local 遗留代码 |
| Laoying | `apps/laoying_standard` | `laoying_standard` | 标准端宿主，`main` 调用 `runLaoyingStandardApp` |
| Laoying | `apps/laoying_ohos` | `laoying_ohos` | OHOS 宿主，`main` 调用 `runLaoyingOhosApp` |
| Laoying | `apps/laoying_app` | `laoying_app` | LY App 壳、ChangeNotifier session、LY 路由、app-local 业务与产品资源 |

`tool/project.dart::AppTarget` 是可执行 target 的当前索引；回答支持哪些 target 前先实时核验它。

## 2. Core packages

| Package | 主要职责/边界 |
|---|---|
| `core_base` | 基础类型、安全转换、尺寸、屏幕与权限工具 |
| `core_blue` | 标准端蓝牙能力 |
| `core_blue_ohos` | 以 package name `core_blue` 提供 OHOS 替代实现 |
| `core_color` | 不带产品主题语义的中性色彩原语 |
| `core_http` | `TQHttp`、delegate、结果模型与网络基础设施 |
| `core_i18n` | 翻译字典、语言类型与 String 扩展 |
| `core_log` | Dart/native 统一日志能力；不得依赖 shared/feature/app |
| `core_region` | 地区检测 |
| `core_share` | 跨平台分享 |
| `core_ui` | 公共 UI，以及 navigation contracts、checked registry、route effect、`SessionResetParticipant` |
| `core_union` | 跨 core 公共能力 |
| `core_webview` | WebView 工具与页面基础设施 |

读取每个包的 `pubspec.yaml` 与 `lib/<package>.dart`；不能仅由 package 名推断完整职责。

## 3. Tuqiang shared 领域包

`shared_business` 已拆分并从 tracked package 中删除。当前公共 barrel 均为 `packages/shared/<package>/lib/<package>.dart`：

| Package | 当前跨 feature 能力 | 高价值索引 |
|---|---|---|
| `shared_account` | 账号、session、账号偏好持久化 | `src/application/account_local_repository.dart` |
| `shared_activity` | Pet/ID Card 共用活动统计、图表、Controller 与 API paths | package barrel、`src/application`、model 与 Widget 调用方 |
| `shared_advertising` | 广告 model/state/repository、曝光与点击 | package barrel、根 Provider override |
| `shared_command` | 跨设备指令、远程设置与指令历史 | package barrel、调用方 |
| `shared_device` | 设备 identity、目录、能力、选择与外部 runtime contract | `device_catalog_provider.dart`、`device_core_commands.dart`、`device_core_runtime.dart` |
| `shared_location` | 定位状态、属性、能力、逆地理编码与展示派生 | `src/application/location_providers.dart`、`src/data`、`src/presentation` |
| `shared_media` | 播放/进度/文件/下载与视频设备 key | `media_download_queue_provider.dart`、`src/data` |
| `shared_message` | 消息、告警、设备摘要与已读状态 | package barrel、根 Provider override |

`shared_device` 不直接实现定位/消息上下文；它通过 `DeviceCoreRuntime` callback 交给 app composition，避免 shared 包反向依赖。

## 4. Tuqiang feature packages

| Package | 当前主要流程 |
|---|---|
| `feature_ai` | AI 业务 |
| `feature_auth` | 登录、认证、账号入口 |
| `feature_camera` | 行车记录仪/监控、相册、P2P、摄像头配网 |
| `feature_device_management` | 添加、搜索、解绑等设备管理 |
| `feature_device_share` | 设备分享 |
| `feature_gps` | 地图、定位、轨迹、围栏、远程设置与指令历史 |
| `feature_id_card` | 学生证与运动统计 |
| `feature_message` | 消息列表、筛选、设置 |
| `feature_mifi` | Wi-Fi/MiFi、实名、套餐、网络控制 |
| `feature_mine` | 我的、账号资料与入口 |
| `feature_overview` | 设备总览 |
| `feature_pet` | 宠物/信标 |
| `feature_tag` | Tag 与跨 GPS 导航入口 |
| `feature_value_added` | 增值服务、套餐、SIM 用量 |

跨 feature 页面通过 contract、route 或 app composition 连接；不要因运行时能跳转就断言 feature 存在直接 Dart 依赖。

## 5. 产品 App-local owner

Tuqiang 尚未下沉的历史代码位于 `apps/tuqiang_app/lib/app/legacy_shared/{common,manager,model,tools,viewmodel}`，设备列表等页面仍可位于 `apps/tuqiang_app/lib/app/home`。文件当前位于 app 是事实，不代表最终设计归属。

Laoying 当前业务主要直接由 `apps/laoying_app/lib/app` 拥有：

- `auth`、`gps`、`pet`、`mine`、`overview`、`message`、`device_management`、`device_share`；
- 每个领域优先检查 `ly_*_router.dart`、`providers/*controller.dart`、`repositories`、`pages` 与 `ly_*_assets.dart`；
- 公共组合入口在 `session`、`router`、`contracts`、`coordinators`、`infrastructure`、`skin`、`i18n`。

同名 Tuqiang feature 不自动成为 Laoying owner；是否抽取共用包需要用户/开发决策。

## 6. Plugins、adapter 与资源

| 分组 | 当前目录 | 作用 |
|---|---|---|
| 自研插件 | `packages/plugins/tq_filemanage_plugin`、`tq_log_plugin`、`tq_map_plugin`、`tq_p2p_plugin`、`tq_push_plugin`、`tq_signal_plugin`、`tq_vsdk_plugin` | 文件、日志、地图、P2P、推送、信号、视频原生能力 |
| OHOS 广告 | `packages/plugins/adscope_sdk_ohos` | OHOS 广告插件 |
| Adapter | `packages/adapter/*` | 三方库或平台差异适配 |
| Tuqiang 公共资源 | `packages/assets_common` | 跨 package 资源 |
| Tuqiang feature 资源 | `packages/feature/<owner>/assets` 与 asset 常量 | 领域私有图片/静态资源 |
| Laoying 资源 | `apps/laoying_app/assets/{i18n,images}` 与 `ly_*_assets.dart` | Laoying 产品级/领域资源 |

资源需求必须查实际文件、pubspec 声明、asset 常量和各平台消费端。目标图片不存在时应报告缺失并询问来源，不能把“可以动态画”当成既定实现。

## 7. Owner 定位顺序

1. 确认产品线和平台。
2. 从 Page/route/asset 常量查定义、barrel 与最终 builder。
3. Tuqiang 查 feature router/contract、shared 领域包及 `bootstrap.dart` override；Laoying 查 app-local router/controller/repository 与 `_runLaoyingApp` 组合。
4. 多业务共用且带业务语义时核对对应 `shared_*`；无业务语义基础设施再核对 `core_*`。
5. 涉及原生能力时查 plugin、adapter、宿主 override 和所有目标平台。
6. 多个 owner 都合理且需求不足以排除时，列证据并让用户决策。

## 8. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "^name:|^description:" apps packages --glob 'pubspec.yaml'
Get-ChildItem packages/shared,packages/feature,packages/core -Directory
rg -n "class .*Router|routes\(|onGenerateRoute|Navigator|Composition|Runtime" <产品相关目录> --glob '*.dart'
rg -n "package:feature_|package:shared_|package:core_" <相关目录> --glob '*.dart'
rg -n "<资源常量>|<文件名>" apps packages --glob '*.dart' --glob 'pubspec.yaml'
```
