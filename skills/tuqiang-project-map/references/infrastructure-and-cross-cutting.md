# 网络、持久化、Session、国际化、缩放与 UI

本页记录跨业务能力的真实入口。解释具体需求时只读取相关小节，并继续追实际调用方；不要把横切基础设施堆成与需求无关的清单。

## 1. 网络链路

### 初始化与 delegate

```text
apps/tuqiang_app/lib/bootstrap.dart::prepareAppStartupData
  -> TQHttp.initHttp(AppHttpDelegate())
  -> packages/core/core_http/lib/src/tq_http.dart::TQHttp
  -> apps/tuqiang_app/lib/app/tools/http/app_http_delegate.dart::AppHttpDelegate
```

- `core_http::TQHttp` 提供 get/post/put/delete、loading/error tip 和 config 变体。
- `HttpBaseDelegate` 定义 app 需要提供的请求前后、响应解析和错误处理边界。
- `AppHttpDelegate` 连接用户/session 信息、请求头、业务 `ResultModel`、失效会话处理和 UI 提示。
- 业务层既有 Repository 包装，也有遗留的直接 `TQHttp.*` 调用。是否经过 Repository 必须按当前链路说明。

### 业务数据收窄

代表文件：

- `packages/core/core_http/lib/src/model/result_model.dart::ResultModel`
- `packages/core/core_base/lib/safe_utils.dart::TCheck`
- `packages/shared/shared_business/lib/device/data/device_catalog_repository.dart`
- `packages/shared/shared_business/lib/device/data/device_core_repository.dart`
- `packages/shared/shared_business/lib/location/data/location_status_repository.dart`
- `packages/shared/shared_business/lib/location/data/location_attribute_repository.dart`
- `packages/shared/shared_business/lib/location/data/location_capabilities_repository.dart`

典型链：

```text
Provider/Controller
  -> Repository 方法
  -> TQHttp.<method>(TQAddress/TVAddress 常量, params)
  -> ResultModel.success / data
  -> TCheck<T> 做运行时类型收窄
  -> Model.fromJson
  -> state / callback / Manager
```

回答只能展示 API 常量名和参数语义，不展开 `address.dart`、`tv_address.dart` 中的实际 endpoint 值；也不得复制 Token、Key、证书、签名或生产配置。

### 并发与错误

网络层统一提示不代表状态层自动正确。继续检查：

- Notifier 的 `mounted`、generation/requestVersion；
- 重复请求是否复用 pending future；
- catch 后保留旧数据还是写 error；
- loading 是 `AsyncValue`、State 字段、全局 loading 还是 Widget `setState`；
- session 失效由 delegate、guard、路由还是 coordinator 处理。

## 2. 持久化与缓存

项目存在多种本地存储，不能都叫“缓存”：

| 类型 | 代表文件/Symbol | 常见用途 |
|---|---|---|
| SharedPreferences repository | `packages/shared/shared_business/lib/manager/tq_global_local_repository.dart::TQGlobalLocalRepository` | 用户、本地配置、启动所需状态 |
| SharedPreferences helper | `packages/shared/shared_business/lib/tools/utils/tq_sp_utils.dart` | list/map/string/bool 等遗留便捷访问 |
| App config repository | `packages/shared/shared_business/lib/manager/tq_app_config_repository.dart` | App 配置持久化 |
| Debug config | `packages/shared/shared_business/lib/manager/tq_debug_config.dart` | 本机 debug 选择 |
| 文件/图片缓存 | `packages/shared/shared_business/lib/common/manager/tq_cache_manager.dart::TQCacheManager` | 设备图标、地图头像等下载缓存 |
| 逆地理缓存 | `tq_regeo_cache_manager.dart`、`common/database/re_geo_code_database_helper.dart` | 坐标到地址的内存/数据库缓存 |
| 下载记录 | `video/data/download/media_download_task_store.dart`、`download_record_cache_manager.dart` | 按 session 保存媒体下载任务 |

追踪“数据从哪里来”时按顺序找：内存 Provider/Manager → 启动 restore → 本地 repository/cache → 网络刷新 → 回写路径。若只看到 Manager getter，应继续找它的 restore/set/clear 调用。

## 3. Session 与状态清理

### 主协调链

文件：

- `apps/tuqiang_app/lib/app/session/session_state_coordinator.dart::SessionStateCoordinator`
- `apps/tuqiang_app/lib/app/session/session_reset_registry.dart::defaultSessionResetParticipants`
- `packages/shared/shared_business/lib/contracts/session/session_reset_participant.dart::SessionResetParticipant`

```text
logout/session clear
  -> SessionStateCoordinator.clearForLogout
  -> 清理当前 VideoDownloadSessionKey 的下载队列并 invalidate
  -> 遍历 defaultSessionResetParticipants
  -> participant.reset(ProviderContainer)
  -> invalidate shared/app Provider 或执行 feature reset action
```

Registry 当前覆盖消息、设备目录/选择、设备 family、定位 family、总览/App 状态等组。Camera、GPS、Pet 等 feature 通过自己的 `Feature*SessionResetters` 暴露参与者，app 负责聚合。

解释“退出后为什么还看到旧设备”时，要同时检查：

- 目标 Provider 是否在 registry；
- 是失效整个 family 还是某个 key；
- Manager/SharedPreferences/Controller 是否另有清理；
- keepAlive 的下载队列是否先执行了业务清理；
- 新 session 首次 watch 是否从磁盘重新 restore。

### 语言切换不是完整 logout reset

`apps/tuqiang_app/lib/app/session/language_change_coordinator.dart::LanguageChangeCoordinator.clearCache` 会清当前设备和相关 identity/module/wifi/sim family、部分 GPS 指令/广告/逆地理缓存。它与 logout registry 的范围不同，不能混为一个 reset 流程。

## 4. 国际化

### 数据与初始化

```text
apps/tuqiang_app/assets/i18n/manifest.json
  -> apps/tuqiang_app/lib/app/i18n/app_i18n_loader.dart::AppI18nLoader
  -> bootstrap.dart::initialI18nData
  -> core_i18n::TQI18nManager.installTranslations/initLanguage
  -> app.dart::MaterialApp.locale + supportedLocales
  -> String.tr / keyTr / multiKeyTr
```

当前 manifest 使用 `en_US` fallback，并列出 `zh_CN`、`en_US`、`ar`、`de`、`es`、`fr`、`id`、`it`、`vi` 九种 JSON。回答前重新读取 manifest，不能假设语言数量固定。

中文/英文存在三套不可混用的标识：资源 manifest/字典使用 `zh_CN/en_US`，`TQLanguageType.name` 与 `MaterialApp Locale` 使用 `zh/en`，`TQLanguageType.languageCode`、本地语言持久化及后端历史协议使用 `zh-CN/en-US`；其余语言当前三处均使用两字母代码。

String 扩展位于 `packages/core/core_i18n/lib/src/string_extension.dart`：

- `'文案键'.tr`：按当前语言查字典；
- `'包含{key}占位符的键'.keyTr(value)`：只替换字面量 `{key}`；
- `'含{name}和{count}的键'.multiKeyTr({'name': ..., 'count': ...})`：替换多个命名占位符。

`.tr` 是运行时 getter。若把翻译结果缓存进不会随语言变化重建的 final/单例字段，UI 可能不更新；解释动态语言链时要查字符串计算时机及 Widget 的重建来源。

## 5. 缩放、屏幕与文字

关键文件：

- `packages/core/core_base/lib/tq_size_fit.dart::TQSizeFit`
- `packages/core/core_base/lib/num_extension.dart::NumExtension.sc`
- `packages/core/core_base/lib/tq_screen.dart::Screen`
- `apps/tuqiang_app/lib/app.dart::_StrongAppState.build`

当前计算：

```text
StrongApp build 中取当前约束最小宽/高
  -> TQSizeFit.initialize(standardW)
  -> scale = min(standardW / 375, 1.2)
  -> 设计尺寸 num.sc = TQSizeFit.setPt(num)
```

- `TQSizeFit` 会在首次或宽度明显变化时重算，适配折叠屏等变化。
- `.sc` 是基于当前逻辑短边（`min(width, height)`）的设计尺寸缩放，不是 devicePixelRatio。
- `Screen.scale` 是 devicePixelRatio；`Screen.width/height/safeHeight` 来自 MediaQuery。不要混用两种 scale。
- `MaterialApp.builder` 当前用 `TextScaler.linear(1.0)` 覆盖文本缩放；这是项目现状，解释可访问性或字号问题时必须指出该全局入口。

## 6. UI 复用与展示定位

- 通用组件优先查 `packages/core/core_ui/lib` 的 barrel 和具体 Widget。
- 带设备/地图业务语义的展示 mapper/helper 常在 `shared_business/lib/device/presentation` 或 `location/presentation`。
- feature 私有组件在 `packages/feature/<owner>/lib/**/widgets`、`pages` 或 `presentation`。
- App 级 loading、route observer、screen secure 和 SafeArea 组合可能在 `apps/tuqiang_app/lib/app`。
- 公共资源通过 `packages/assets_common`，feature 私有资源通过对应 package 的 asset 常量和 pubspec。

从状态追到 UI 时至少找到实际 Widget 属性：`Text` 内容、图片/图标、颜色、可见性、enable 状态、地图 marker/相机画面或 loading/error/empty 分支。停在 presentation mapper 不算“找到展示位置”。

## 7. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "TQHttp\.initHttp|class TQHttp|class AppHttpDelegate|ResultModel|TCheck" apps packages --glob '*.dart'
rg -n "SharedPreferences|TQGlobalLocalRepository|TQCacheManager|DatabaseAbstract|loadFromDisk|restore" <相关目录> --glob '*.dart'
rg -n "SessionStateCoordinator|defaultSessionResetParticipants|SessionResetParticipant|Feature.*SessionResetters|invalidate\(" apps packages --glob '*.dart'
rg -n "initialI18nData|AppI18nLoader|TQI18nManager|\.tr\b|keyTr|multiKeyTr" <相关目录> --glob '*.dart'
rg -n "TQSizeFit|\.sc\b|Screen\.|textScaler" <相关目录> --glob '*.dart'
```
