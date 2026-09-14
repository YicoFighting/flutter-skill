# Tuqiang 构建与运行上下文

仅在构建、CI、推送、广告、地图原生依赖、ABI 或“同一页面不同安装包表现不同”时读取。以下索引于 2026-09-14 从目标源码核验；使用前重查 symbol 与实际依赖，不把注释和历史清单当永久事实。

## 分开六个维度

记录 `product / platform / target / flavor / distributionChannel / accountMode`。本技能业务固定 Tuqiang；主宿主为 `standard`、`ohos`。其他 tool target 或同仓 app 目录不自动纳入业务范围。账号由 [isEnterprise](account-mode.md) 决定；flavor 是构建选择，分发渠道可在构建后写入，二者均不能推断个人/企业账号。

## Android flavor 与分发渠道

| flavor | 当前实际依赖/分派 | 需要核验的差异 |
|---|---|---|
| `allvendor` | `jpush_push`、极光厂商插件、`ad_sdk` | 默认内部包，不能代表其他安装包 |
| `combined` | 五家厂商 push module、Walle、`ad_sdk` | 母包经渠道写入后，运行时选择厂商；不能仅验证未写 channel 的母包 |
| `firebase` | `firebase_push`、`ad_sdk_noop`、Google Play 高德本地依赖 | 广告空实现、推送、Manifest、arm64-v8a 与原生库差异 |

源码入口：

- `apps/standard/android/app/build.gradle`：`productFlavors`、`*Implementation`、ABI 及打包规则。`combined` 声明上方仍有“依赖与 allvendor 相同”的旧注释，应以实际依赖块和工厂为准。
- `apps/standard/android/app/src/{main,combined,firebase,firebaseRelease}/AndroidManifest.xml`：按当前构建变体检查合并覆盖，不能只读 main。
- `packages/plugins/tq_push_plugin/android/src/main/java/com/tuqiang/smart/push/TQPushPlugin.java::resolveVendor`：推送 vendor 与 Walle channel 的解析。
- `packages/plugins/tq_push_plugin/android/push_core/src/main/java/com/tuqiang/smart/push/core/TQPushFactory.java`：vendor 到实际实现；缺模块/未知渠道的当前行为继续追源码。
- `apps/standard/android/app/src/main/java/com/tuqiang/smart/MainActivity.java`：`BuildConfig.FLAVOR`、渠道读取和上报；不要假定它与 push resolver 的 fallback 完全相同。
- `tool/apk_unpack/split_channels.mjs`、`split_channels.test.mjs`：渠道产物与测试；只有任务涉及打包/分发时才读取。

推送、广告、原生地图依赖或 ABI 改动按可达 flavor 增加覆盖行；纯共享 Dart 文案改动无需构建所有渠道。`firebase` 不表示只有 Google 地图，地图 source 与二进制依赖分别核验。

## SDK 与命令封装

`tool/project.dart::_flutterExecutableFor/_sdkRootFromFvm` 决定 SDK：

- standard：`TUQIANG_FLUTTER_STANDARD / FLUTTER_HOME` → target `.fvmrc` 与已安装 FVM SDK → `flutter`。
- ohos：`TUQIANG_FLUTTER_OHOS / OHOS_FLUTTER_HOME` → target `.fvmrc` 与已安装 FVM SDK → `flutter_ohos` 环境变量 → `ohos-flutter`。

`_childEnvironmentFor` 给 OHOS 子进程配置 SDK/工具路径。不要全局改 PATH 或拿标准 Flutter 代替 OHOS SDK。诊断只展示需要的工具路径/版本，禁止输出整份环境、签名或生产配置。

`_withDefaultStandardAndroidFlavor` 会给 standard 的 `run`、`build apk/appbundle` 补默认 `allvendor`；显式 `--flavor` 保留。当前 `run` 判断不检查设备平台，所以 iOS 运行需核对实际参数与 scheme，不能把这条默认行为理解为正确的 iOS 方案。

`OhosSharedConfigSnapshot.capture/restore` 只恢复列出的四份 OHOS 配置，不覆盖 lockfile、`.dart_tool/package_config.json` 等所有构建产物。同一 checkout 上会改同一 package 解析状态的标准/OHOS 命令应串行；只读搜索可以并行。验证前后比较相关 Git diff，保留用户原有改动，不以整仓 reset/clean 收尾。

具体命令、测试范围和证据等级见 [测试规范](../../tuqiang-dev/references/testing.md)。
