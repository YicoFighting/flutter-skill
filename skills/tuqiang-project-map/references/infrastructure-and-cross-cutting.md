# 网络、持久化、Session、国际化、尺寸与资源

只读取与当前产品/需求有关的小节。相同底层 core/plugin 不代表两产品有相同 app delegate、session 或资源 owner。

## 1. 网络

Tuqiang：

```text
AppStartupDataCoordinator.prepareBeforeRunApp
  -> TQHttp.initHttp(AppHttpDelegate())
  -> core_http::TQHttp
  -> app/tools/http/app_http_delegate.dart::AppHttpDelegate
```

业务可能经 Repository，也可能遗留直接调用 `TQHttp`。代表边界：

- 设备：`packages/shared/shared_device/lib/src/application/device_catalog_repository.dart` 与 `packages/shared/shared_device/lib/src/data/http_device_catalog_repository.dart`
- 定位：`packages/shared/shared_location/lib/src/data/location_*_repository.dart`
- 媒体：`packages/shared/shared_media/lib/src/data`
- 通用结果：`packages/core/core_http/lib/src/model/result_model.dart::ResultModel`、`packages/core/core_base/lib/safe_utils.dart::TCheck`

Laoying 网络组合从 `apps/laoying_app/lib/app/infrastructure/backend` 的 backend config/runtime/http client 开始，各 app-local 领域在 `repositories/adapters/ly_http_*_repository.dart` 接入。不要默认经过 `AppHttpDelegate`。

只引用 API 常量/Repository 方法与参数语义，不展示 endpoint、Token、Key、证书、签名或生产配置。继续核验 requestVersion/generation/mounted、pending 去重、旧数据保留、loading/error 与 session 失效入口。

## 2. 持久化与缓存 owner

Tuqiang 当前路径：

| 类型 | 当前 owner |
|---|---|
| 账号持久化 contract | `packages/shared/shared_account/lib/src/application/account_local_repository.dart` |
| App 全局本地 repository | `apps/tuqiang_app/lib/app/legacy_shared/manager/tq_global_local_repository.dart` |
| App config/debug config | `apps/tuqiang_app/lib/app/legacy_shared/manager/tq_app_config_repository.dart`、`tq_debug_config.dart` |
| SharedPreferences helper | `apps/tuqiang_app/lib/app/legacy_shared/tools/utils/tq_sp_utils.dart` |
| 文件/图片 cache | `apps/tuqiang_app/lib/app/legacy_shared/common/manager/tq_cache_manager.dart` |
| 逆地理 cache/database | `packages/shared/shared_location/lib/src/data/tq_regeo_cache_manager.dart`、`src/data/cache/re_geo_code_database_helper.dart` |
| 媒体下载记录 | `packages/shared/shared_media/lib/src/data/media_download_task_store.dart`、`download_record_cache_manager.dart` |

Laoying 产品持久化 adapter 位于 `apps/laoying_app/lib/app/infrastructure`，例如 mine preferences、skin storage、terminal id provider 的 SharedPreferences 实现。追 getter 时继续找 restore/set/clear 和具体消费者。

## 3. Session 与清理

Tuqiang：

- contract：`packages/core/core_ui/lib/session_reset_participant.dart::SessionResetParticipant`
- 聚合：`apps/tuqiang_app/lib/app/session/session_reset_registry.dart::defaultSessionResetParticipants`
- 协调：`session_state_coordinator.dart::SessionStateCoordinator`
- 语言切换：`language_change_coordinator.dart::LanguageChangeCoordinator`

`clearForLogout` 先处理当前媒体下载 session，再执行 reset participants。Registry 当前包括 message/device/location/app 组及 Auth/GPS/Camera/Pet 等 feature participant。语言切换清理范围更窄，不得当成 logout。

Laoying：`apps/laoying_app/lib/app/session/ly_app_provider.dart` 中 `resetSession` 重置 user session、执行 session reset coordinator、通过 refresh bus 发布事件并 `notifyListeners`。查每个 app-local controller/repository 是否注册 participant；不要套用 Tuqiang registry。

## 4. 国际化

Tuqiang：

```text
启动安装：AppStartupDataCoordinator._initializeI18n
  -> TQI18nManager.initLanguage
  -> AppI18nRepository.installStartupTranslations
  -> AppI18nLoader.loadManifest/loadLocales
  -> TQI18nManager.installTranslations

后续按需：AppI18nRepository.ensureLanguageLoaded
  -> AppI18nLoader.loadLocales
  -> TQI18nManager.mergeTranslations

消费：StrongApp locale/supportedLocales + String.tr
```

启动只安装当前语言及必要的 zh/en/fallback 集合；之后的按需分支是 `AppI18nRepository.ensureLanguageLoaded → AppI18nLoader.loadLocales → TQI18nManager.mergeTranslations`。不要再回退到旧 bootstrap i18n helper。manifest 当前 fallback 为 `en_US`，列出九种 locale，但每次回答都应重新读取。

`TQLanguageType.translationLocale`、`name`/MaterialApp Locale 与 `languageCode` 可能使用不同格式；从 `core_i18n/lib/src/tq_language_type.dart` 实时核验。翻译 getter 若被缓存进不随语言重建的 final/单例，UI 可能不更新。

Laoying 从 `apps/laoying_app/assets/i18n`、`ly_i18n_loader.dart` 与 `ly_i18n_initializer.dart` 初始化；它是独立产品资源边界，不能默认复用 Tuqiang manifest。

## 5. 尺寸与文字

Tuqiang 关键入口：

- `core_base/lib/tq_size_fit.dart::TQSizeFit`
- `core_base/lib/num_extension.dart::NumExtension.sc`
- `core_base/lib/tq_screen.dart::Screen`
- `apps/tuqiang_app/lib/app.dart::StrongApp`

`TQSizeFit` 以逻辑短边相对 375 缩放并封顶 1.2；`.sc` 不是 devicePixelRatio。`Screen.scale` 才是 devicePixelRatio。`StrongApp` 的 MaterialApp builder 当前固定 `TextScaler.linear(1.0)`。

Laoying 的入口在 `apps/laoying_app/lib/app/infrastructure/ly_screen_scale_initializer.dart` 和 `LYApp`；不要直接套用 StrongApp 结论。

## 6. UI 与资源证据

- Tuqiang 通用 UI/导航 contract：`packages/core/core_ui/lib`。
- Tuqiang 设备/定位展示 mapper：`packages/shared/shared_device/lib/src/presentation`、`packages/shared/shared_location/lib/src/presentation`。
- Tuqiang 公共资源：`packages/assets_common`；feature 私有资源：`packages/feature/<owner>/assets`。
- Laoying 资源：`apps/laoying_app/assets/{i18n,images}` 及各领域 `ly_*_assets.dart`。

资源变更先建立四段证据：实际文件 → pubspec asset 声明 → Dart asset 常量/参数 → Android/iOS/OHOS 原生消费端（若插件接收路径）。例如 Tuqiang 轨迹起终点国际图当前由 `feature_gps/lib/src/presentation/trace_type_ui.dart` 选择 `FeatureGpsAssets.traceStartInternational/traceEndInternational`，Flutter 将路径传给地图插件，再由各平台加载图片。

如果验收要求另一张 PNG，而目标资源在仓库中不存在，项目地图应明确“缺少目标资产”并询问用户提供或指定来源；不能推断为 Canvas 绘制，也不能把现有中文图动态覆字当作已确认方案。

从状态/资源追到 UI 时必须落到实际 Text/Image/颜色/可见性/按钮/地图 marker/相机画面或 loading/error/empty 分支。

## 7. 实时核验

```powershell
Set-Location -LiteralPath $tuqiangRoot
rg -n "TQHttp\.initHttp|class TQHttp|class AppHttpDelegate|class LYBackendHttpClient|ResultModel|TCheck" apps packages --glob '*.dart'
rg -n "SharedPreferences|TQGlobalLocalRepository|TQCacheManager|loadFromDisk|restore|Storage" <产品相关目录> --glob '*.dart'
rg -n "SessionStateCoordinator|defaultSessionResetParticipants|SessionResetParticipant|resetSession|notifyListeners|invalidate\(" apps packages --glob '*.dart'
rg -n "AppI18nRepository|AppI18nLoader|LYI18nLoader|LYI18nInitializer|TQI18nManager|\.tr\b" <产品相关目录> --glob '*.dart'
rg -n "TQSizeFit|\.sc\b|Screen\.|textScaler|LYScreenScale" <产品相关目录> --glob '*.dart'
rg -n "<资源常量>|<资源文件名>" apps packages --glob '*.dart' --glob 'pubspec.yaml'
```
