# 模块目录与职责

本目录用于定位 owner，不代替当前源码核验。feature 成熟度和迁移进度不一致；确定页面、Provider 或 route 的实际 owner 时，继续检查该包的 barrel、router、pubspec 和调用方。

## 1. Apps

| 路径 | pubspec name | 职责与关键 symbol |
|---|---|---|
| `apps/standard` | `tuqiang_standard` | Android/iOS 入口；`lib/main.dart::main` 调用 `runStandardApp` |
| `apps/ohos` | `tuqiang_ohos` | HarmonyOS 入口；`lib/main.dart::main` 调用 `runOhosApp` 并注入平台 binding/backend |
| `apps/tuqiang_app` | `tuqiang` | 共享 App；`bootstrap.dart`、`app.dart`、`app/router`、`app/session`、`app/coordinators` 是组合层 |

`apps/tuqiang_app/lib/app/home` 仍包含设备列表等历史 app 页面；“位于 app”是当前事实，不自动代表最终设计归属。

## 2. Core packages

| Package | 主要职责 | 典型入口 |
|---|---|---|
| `core_base` | 通用值转换、尺寸、屏幕、安全工具、权限与基础类型 | `tq_size_fit.dart`、`tq_screen.dart`、`num_extension.dart`、`tq_permission_manager.dart` |
| `core_http` | HTTP 初始化、delegate、client 配置、网络线路和结果模型 | `src/tq_http.dart`、`src/http_base_delegate.dart`、`src/model/result_model.dart` |
| `core_i18n` | 翻译字典管理、语言状态、String 扩展 | `src/tq_i18n_manager.dart`、`src/string_extension.dart` |
| `core_ui` | AppBar、空态、Toast、Dialog 等公共 UI | 先查 `lib/` 的 barrel 与具体组件调用方 |
| `core_blue` | 标准端蓝牙抽象/实现 | `pubspec.yaml` 与 `lib/` |
| `core_blue_ohos` | 以相同 package name `core_blue` 提供 OHOS 替代实现 | `apps/ohos/pubspec.yaml` 的 override |
| `core_region` | 地区检测能力 | package barrel 与调用方 |
| `core_share` | 跨平台分享能力 | package barrel 与平台接入 |
| `core_union` | 跨 core 共享能力 | package barrel 与 pubspec |
| `core_webview` | WebView 工具与页面基础设施 | package barrel 与调用方 |

## 3. Shared business

`packages/shared/shared_business` 是多个 feature 共用的业务层。高价值入口：

| 子域 | 路径 | 代表能力 |
|---|---|---|
| 设备目录 | `lib/device/application/providers/device_catalog_provider.dart` | 列表、筛选、部门、分页、批量状态 |
| 设备核心 | `lib/device/application/providers/device_core_providers.dart` | 当前选中设备、按设备 identity/module/wifi/sim 状态 |
| 设备命令 | `lib/device/application/device_core_commands.dart` | 选择/清空设备、刷新模块及定位上下文 |
| 设备数据 | `lib/device/data/` | catalog/core/avatar Repository |
| 设备展示 | `lib/device/presentation/` | active presentation 和展示映射 |
| 定位 | `lib/location/application/providers/` | 快照、属性、能力、展示、命令、提示 |
| 定位数据 | `lib/location/data/` | 状态、属性、能力、指令、逆地理编码 Repository |
| 视频共享契约 | `lib/video/` | 设备 key、下载队列、共享 gateway/capability |
| 消息摘要 | `lib/message/application/providers/` | 按设备的消息摘要 |
| Session contract | `lib/contracts/session/` | feature reset participant 协议 |
| 路由 contract | `lib/contracts/navigation/` | checked registry、route effect、导航服务 |
| 遗留/横切状态 | `lib/manager/`、`lib/common/manager/`、`lib/tools/utils/` | 全局模型、缓存、屏幕安全、请求工具等混合状态 |

## 4. Feature packages

| Package | 用户流程/领域 |
|---|---|
| `feature_ai` | AI 相关业务 |
| `feature_auth` | 登录、认证与账号入口 |
| `feature_camera` | 行车记录仪/监控视频、相册、P2P、摄像头配网和 Camera route |
| `feature_device_management` | 添加、搜索、解绑等设备管理 |
| `feature_device_share` | 设备分享流程 |
| `feature_gps` | GPS 位置、地图、轨迹、围栏、远程设置和指令历史 |
| `feature_id_card` | 学生证/运动统计相关流程 |
| `feature_message` | 消息列表、筛选、设置和设备消息状态 |
| `feature_mifi` | Wi-Fi/MiFi 设备、实名、套餐和网络控制 |
| `feature_mine` | 我的、账号资料与相关入口 |
| `feature_overview` | 设备总览 |
| `feature_pet` | 宠物/信标业务 |
| `feature_tag` | Tag 设备业务与跨 GPS 导航入口 |
| `feature_value_added` | 增值服务、套餐与 SIM 用量 |

这些职责来自当前目录、barrel、路由和项目文档，但一次具体需求仍可能跨多个 owner。例如 Camera 页面可通过 app 注入的 composition builder 嵌入 GPS 模块，不能据此断言 feature 包之间存在直接依赖。

## 5. Plugins、adapter 与资源

| 分组 | 当前目录 | 作用 |
|---|---|---|
| 自研插件 | `packages/plugins/tq_filemanage_plugin`、`tq_log_plugin`、`tq_map_plugin`、`tq_p2p_plugin`、`tq_push_plugin`、`tq_signal_plugin`、`tq_vsdk_plugin` | 文件、日志、地图、P2P、推送、信号、视频原生能力 |
| OHOS/广告插件 | `packages/plugins/adscope_sdk_ohos` | OHOS 广告插件实现 |
| Adapter | `packages/adapter/*` | 三方库或平台差异适配，如分享、WebView、友盟、设置、广告 |
| 公共资源 | `packages/assets_common` | 跨模块图片与静态资源 |

## 6. Owner 定位顺序

1. 从页面/route 常量查定义及导出 barrel。
2. 查 feature 自己的 router、composition/navigator contract、provider 和 repository。
3. 查 `FeatureRouterRegistry` 与 `bootstrap.dart` 的 override/callback，确认最终装配。
4. 若能力被多个 feature 使用，再查 `shared_business`；无业务语义基础设施再查 `core_*`。
5. 若涉及原生通道，查 plugin、adapter 和 OHOS override。

## 7. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot
Get-ChildItem -LiteralPath '.\packages\feature' -Directory
rg -n "^name:|^description:" apps packages --glob 'pubspec.yaml'
rg -n "class .*Router|static .*routes|Navigator|Composition|Navigator" packages/feature apps/tuqiang_app/lib/app --glob '*.dart'
rg -n "package:feature_|package:shared_business|package:core_" <相关目录> --glob '*.dart'
```

将 `<相关目录>` 替换成明确目录，不对整个磁盘做宽泛扫描。
