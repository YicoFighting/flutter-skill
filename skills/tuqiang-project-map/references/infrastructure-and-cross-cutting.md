# Tuqiang 网络、持久化、Session、国际化、尺寸与资源

只读取命中小节。账号相关基础设施同时读取 [账号模式](account-mode.md)。

## 网络

    AppStartupDataCoordinator.prepareBeforeRunApp
    → TQHttp.initHttp(AppHttpDelegate())
    → core_http::TQHttp
    → apps/tuqiang_app/lib/app/tools/http/app_http_delegate.dart::AppHttpDelegate

Repository 与遗留直接 `TQHttp` 并存。代表 owner：设备 `shared_device` 的 `DeviceCatalogRepository/HttpDeviceCatalogRepository`，定位 `shared_location/lib/src/data/location_*_repository.dart`，消息 `shared_message/lib/src/data`，媒体 `shared_media/lib/src/data`；通用结果为 `core_http::ResultModel` 与 `core_base::TCheck`。

只引用 API 常量、Repository symbol 和参数语义，不展示 endpoint、Token、Key、证书或签名。个人/企业 path、DTO、header/token、cache 与旧请求发布条件回到 [账号模式](account-mode.md)。

## 持久化与缓存

| 类型 | 当前 owner |
|---|---|
| 账号持久化 contract | `packages/shared/shared_account/lib/src/application/account_local_repository.dart` |
| App 全局本地 repository | `apps/tuqiang_app/lib/app/legacy_shared/manager/tq_global_local_repository.dart` |
| App config/debug config | `tq_app_config_repository.dart`、`tq_debug_config.dart` |
| SharedPreferences helper | `apps/tuqiang_app/lib/app/legacy_shared/tools/utils/tq_sp_utils.dart` |
| 文件/图片 cache | `apps/tuqiang_app/lib/app/legacy_shared/common/manager/tq_cache_manager.dart` |
| 逆地理 cache/database | `shared_location` 的 regeo cache manager/database helper |
| 媒体下载记录 | `shared_media` 的 task store/download record cache manager |

追 getter 时继续找 restore/set/clear 和消费者；账号相关 cache scope 与切换清理以 [账号模式](account-mode.md) 为准。

## Session 与清理

- contract：`packages/core/core_ui/lib/session_reset_participant.dart::SessionResetParticipant`
- 聚合：`apps/tuqiang_app/lib/app/session/session_reset_registry.dart::defaultSessionResetParticipants`
- 协调：`session_state_coordinator.dart::SessionStateCoordinator`
- 语言切换：`language_change_coordinator.dart::LanguageChangeCoordinator`

`clearForLogout` 先处理当前媒体下载 session，再执行包含 message/device/location/app 与 feature 的 reset participants。语言切换清理更窄，不等于 logout。

## 国际化事实

`core_i18n` 提供 `TQI18nManager/TQLanguageType/String.tr` 等查找能力；`apps/tuqiang_app/assets/i18n` 的 manifest 与 locale JSON 才是产品字典。

    AppStartupDataCoordinator._initializeI18n
    → TQI18nManager.initLanguage
    → AppI18nRepository.installStartupTranslations
    → AppI18nLoader.loadManifest/loadLocales
    → TQI18nManager.installTranslations
    → StrongApp locale/supportedLocales + tr/keyTr/multiKeyTr

后续按需加载经 `ensureLanguageLoaded → loadLocales → mergeTranslations`。本页只报告 owner 与运行链；manifest、缺 key、翻译缓存和修改门禁见开发 Skill 的 [国际化规范](../../tuqiang-dev/references/i18n.md)。

## 尺寸、UI 与资源

- `core_base/lib/tq_size_fit.dart::TQSizeFit`
- `core_base/lib/num_extension.dart::NumExtension.sc`
- `core_base/lib/tq_screen.dart::Screen`
- `apps/tuqiang_app/lib/app.dart::StrongApp`

逻辑缩放与 `devicePixelRatio` 不同；`.sc`、`Screen.scale` 和 `StrongApp.TextScaler` 按当前实现解释。公共 UI/导航 contract 在 `packages/core/core_ui/lib`，展示 mapper 在 `shared_device/shared_location` 的 presentation，公共资源在 `packages/assets_common`，Feature 资源在 `packages/feature/<owner>/assets`。

资源链追“实际文件 → pubspec → Dart asset 常量/参数 → Flutter 或三端原生消费者”。目标资源缺失时报告并询问来源，不虚构 Canvas、临时资源或默认替代。
