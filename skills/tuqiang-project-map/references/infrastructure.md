# Tuqiang 网络、持久化、Session、国际化、尺寸与资源

只读命中小节；账号相关基础设施同时读 [账号模式](account-mode.md)。

## 网络

```text
AppStartupDataCoordinator.prepareBeforeRunApp → TQHttp.initHttp(AppHttpDelegate())
→ core_http::TQHttp → apps/tuqiang_app/lib/app/tools/http/app_http_delegate.dart::AppHttpDelegate
```

Repository 与遗留直接 `TQHttp` 并存。代表 owner：`shared_device` 的 `DeviceCatalogRepository/HttpDeviceCatalogRepository`，`shared_location/lib/src/data/location_*_repository.dart`，`shared_message/lib/src/data`，`shared_media/lib/src/data`；结果模型 `core_http::ResultModel` 与 `core_base::TCheck`。只引用 API 常量、Repository symbol 与参数语义。

## 持久化与缓存

| 类型 | owner |
|---|---|
| 账号持久化 contract | `shared_account/lib/src/application/account_local_repository.dart` |
| App 全局本地 repository / config | `app/legacy_shared/manager/tq_global_local_repository.dart`、`tq_app_config_repository.dart`、`tq_debug_config.dart` |
| SharedPreferences helper | `app/legacy_shared/tools/utils/tq_sp_utils.dart` |
| 文件/图片 cache | `app/legacy_shared/common/manager/tq_cache_manager.dart` |
| 逆地理 cache/database；媒体下载记录 | `shared_location` regeo cache；`shared_media` task store/record cache |

追 getter 时继续找 restore/set/clear 与消费者。

## Session 与清理

contract `core_ui/lib/session_reset_participant.dart::SessionResetParticipant`；聚合 `app/session/session_reset_registry.dart::defaultSessionResetParticipants`；协调 `session_state_coordinator.dart::SessionStateCoordinator`；语言切换 `language_change_coordinator.dart::LanguageChangeCoordinator`。`clearForLogout` 先处理当前媒体下载 session，再执行 message/device/location/app 与 feature 的 participants；语言切换清理更窄，不等于 logout。

## 国际化链

```text
AppStartupDataCoordinator._initializeI18n → TQI18nManager.initLanguage
→ AppI18nRepository.installStartupTranslations → AppI18nLoader.loadManifest/loadLocales
→ TQI18nManager.installTranslations → StrongApp locale + tr/keyTr/multiKeyTr
按需：ensureLanguageLoaded → loadLocales → mergeTranslations
```

`core_i18n` 只提供查找；产品字典是 `apps/tuqiang_app/assets/i18n` 的 manifest（当前 9 个 locale）与 JSON。`TQI18nManager.supportLangList`、`StrongApp.supportedLocales` 只列 zh/en，但 `TQLanguageType` 与 manifest 仍保留多语言，`initLanguage/fromString` 可能恢复旧语言：设置入口、系统 locale、资源清单与实际加载集合是不同事实。取值与 fallback 规则见 [国际化](../../tuqiang-dev/references/i18n.md)。

## 尺寸与 UI 封装

`core_base/lib/tq_size_fit.dart::TQSizeFit`（375 设计宽、`maxScale` 1.2）、`num_extension.dart::.sc`、`tq_screen.dart::Screen`（整窗）。`StrongApp` 按分栏后的可用宽度初始化缩放；逻辑缩放、`devicePixelRatio`、`Screen.scale` 与 TextScaler 分开。分栏与方向见 [启动与路由](startup-routing.md)。

可复用的组件、展示函数与地图面板入口统一列在 [本地复用](../../tuqiang-dev/references/local-style-and-reuse.md)；入口不代表 helper 是纯函数，部分展示方法读取当前语言或注入偏好。

## 资源

资源链追"实际文件 → pubspec 目录声明 → Dart asset 常量/参数 → Flutter 或三端原生消费者"。地图标记等图标可能只在 Android/iOS/鸿蒙原生资源中（Google 适配器读取原生资源生成图片），不能只搜 Flutter assets。目标资源缺失时报告并询问来源，不虚构替代。
