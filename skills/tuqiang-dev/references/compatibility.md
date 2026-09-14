# Tuqiang 三端兼容

Android/iOS 使用 `standard` 宿主，HarmonyOS 使用 `ohos`；`standard` 不是两端运行证明。最低交付、iOS 交接与地图七行统一见 [实施覆盖](implementation-coverage.md)。

## 公共代码边界

- Android/iOS 沿当前 owner 使用 `Platform.isAndroid/isIOS`；OHOS 使用 bootstrap 配置的 `AppTargetConfig.isOhos`，不存在 `Platform.isOhos`。
- OHOS-only 类型、View、package 或 SDK 只出现在宿主、专属 plugin/adapter 或注入实现；公共 Dart 通过 callback、Provider override 或 bridge 依赖平台实现。
- standard-only 能力必须在 owner、pubspec 和调用路径中隔离，不能默认为三端支持。
- 修改 `core/shared/plugin` 公开 API 时搜索全部现有调用方并保持必要 contract 兼容，但不扩大本次 Tuqiang 业务行为。

依赖选择顺序：现有 core/plugin/adapter → 已验证纯 Dart 库 → OHOS override → 新 plugin/channel。新增依赖前核对两个 target 的 pubspec/lockfile、原生实现、权限和打包；只修改真实受影响文件。

## 能力决策与验证

拨号、短信、商店、蓝牙、地图、推送、相机、文件和后台定位等能力逐端确认可达性、运行证据、权限/文案以及不支持时的用户行为；多种降级都合理时先询问。地图场景与后端覆盖回到 [实施覆盖](implementation-coverage.md)。

`canLaunchUrl`、依赖 override 或 analyze 通过不能证明真机能力。命令、build/真机/CI 与未执行证据统一见 [测试规范](testing.md)。
