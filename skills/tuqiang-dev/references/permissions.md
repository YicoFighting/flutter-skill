# Tuqiang 权限

先确认平台、账号模式和用户可见拒绝/降级行为。首次申请、普通拒绝、永久拒绝、系统服务关闭和“去设置”是不同状态；需求未明确且会改变交互时先询问。

优先使用 `core_base` 的 `TQPermissionManager` 与 `core_union` 的 `TQPermissionAlert`，不在 Feature 直接 import `permission_handler`。具体方法和枚举以当前源码为准：

- 在用户进入相关功能时按需申请，不在 App 启动时一次申请全部；
- 永久拒绝沿现有提示引导系统设置；普通拒绝不循环弹系统框；
- 定位权限与系统定位服务开关分别判断；
- 平台差异集中在 manager/plugin/adapter，不散落页面；
- 权限文案属于用户可见文本，必须按 [国际化规范](i18n.md) 覆盖当前所有 locale；
- 个人/企业流程若入口或能力不同，分别验证；没有差异时任务卡标记 `both`。

原生声明在 `apps/standard/android`、`apps/standard/ios`、`apps/ohos/ohos`。按 [平台覆盖门](implementation-coverage.md) 逐端检查权限项、用途文案、channel/authority 与 Dart 行为：Bug 闭环 Android+OHOS 并列 iOS 影响；新需求三端代码完整。某端无需修改必须有已有声明或不可达证据。

真机行为按风险覆盖：

```text
未询问 → 首次申请 → 普通拒绝 → 再次进入
→ 永久拒绝 → 设置引导 → 系统服务关闭/恢复
```

运行受影响 package/target analyze、`-ProductScope tuqiang` 与 contract 测试。没有真机结果时写“未执行/交接”，不能从编译通过推断授权流程通过。
