# Tuqiang 路由

沿用当前命名路由体系，不因通用教程主动迁移 `go_router`。Feature 定义路由常量和唯一 builder，`apps/tuqiang_app` 的 `AppRouters`/`FeatureRouterRegistry` 聚合并保留必要 alias；跨 Feature 导航通过公开 callback/config/contract 装配。

修改路由必须保持并验证：

- 历史 route 字符串与唯一 builder；
- arguments 类型、必填字段和默认行为；
- `Navigator.pop` result 与等待它的调用方；
- push/replace/removeUntil 栈行为；
- H5、scheme、push、native 入口；
- 定位刷新、session 清理、防截屏、系统栏等 route effect；
- 个人/企业模式进入的页面、参数、首页/Mine/消息分支。

涉及登录或账号页面时读取 [账号模式事实](../../tuqiang-project-map/references/account-mode.md)。个人登录与企业登录属于同一 Tuqiang 应用的两个入口，不能做成 target/flavor，也不能用 `accountType` 判断。

设备列表到详情需额外枚举 `deviceType`、scene/category、cameraScene、服务/激活/分享/账号状态和最终 builder；再从各首页/详情的“更多详情/设置”追一层并核对真实 hit target。存在多个 route leaf 而范围未明确时，按 [覆盖门](implementation-coverage.md) 先询问。

验证进入、参数、返回、重复进入、栈行为和 route effect；运行受影响 package/app contract tests、`standard/ohos` analyze 与 `-ProductScope tuqiang`。涉及 native/scheme 时补对应宿主与真机证据。
