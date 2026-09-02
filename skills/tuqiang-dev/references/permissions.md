# 权限申请规范（双产品）

先确认目标产品、平台和用户可见拒绝/降级行为。首次申请、拒绝、永久拒绝、系统服务关闭和“去设置”是不同状态；需求未明确且会改变交互时先询问。

## 1. 途强智能

途强业务优先使用 `core_base` 的 `TQPermissionManager` 与 `core_union` 的 `TQPermissionAlert`，不在 Feature 直接 import `permission_handler`。定位、蓝牙、相机、相册、麦克风、通知、电话、剪贴板等具体方法和枚举必须从当前源码核验，不把本文件当永久 API 清单。

- 在用户进入相关功能时按需申请，不在 App 启动时一次申请全部；
- 永久拒绝沿现有 `TQPermissionAlert` 引导设置；普通拒绝不循环弹系统框；
- 定位权限与系统定位服务开关分别检查；
- 平台差异集中在 manager/plugin/adapter，不散落于页面。

原生声明位于 `apps/standard/android`、`apps/standard/ios`、`apps/ohos/ohos`。按 [implementation-coverage.md](implementation-coverage.md) 逐端分类：Bug 至少修复 Android+OHOS 并列出 iOS 影响/交接，新需求三端均实现；某端声明无需修改时给出已有权限或不可达证据，并验证用途文案与 Dart 行为一致。

## 2. 老鹰在线

老鹰优先沿用当前 app-local `LY` permission/system/scan adapter；Product Scope 明确允许且公开契约一致时，可复用 core/plugin 的底层能力。不要直接复制途强页面的 `TQPermissionAlert` 流程、品牌文案或宿主配置。

先核对：

- `docs/laoying/native_capability_matrix.md` 和 Product Scope 是否批准；
- owner 是业务目录、`infrastructure` 还是宿主原生工程；
- `laoying_standard` 与 `laoying_ohos` 的权限声明、channel 和降级策略；
- fake/unavailable adapter 是否 fail closed，不能伪装授权成功。

原生声明分别位于 `apps/laoying_standard/android`、`apps/laoying_standard/ios`、`apps/laoying_ohos/ohos`。应用标识、用途文案、authority、channel 与凭据保持产品独立。

## 3. 验证

真机按已确认产品和 Bug/新需求平台基线覆盖：未询问 → 首次申请 → 普通拒绝 → 再次进入 → 永久拒绝 → 设置引导 → 系统服务关闭/恢复。并运行对应 target analyze、ProductScope boundary 与聚焦 contract/architecture tests；老鹰 app boundary 检查器的已知基线按 [testing.md](testing.md) 处理。没有真机结果时明确写“未执行/交接”，不能从编译通过推断授权流程通过。
