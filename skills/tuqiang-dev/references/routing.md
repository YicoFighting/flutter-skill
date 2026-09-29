# Tuqiang 路由

沿用当前命名路由，不主动迁移 `go_router`。Feature 定义路由和 builder，`apps/tuqiang_app/lib/app/router/app_router.dart` 的 `AppRouters` 与 `FeatureRouterRegistry` 装配公开入口。

当前 `StrongApp` 通过 `onGenerateRoute` 进入 `AppRouters.generateRoute`；它按 `_paneRoutes` 选择 `CoreAdaptivePageRoute`，摄像头/视频等仍使用 `MaterialPageRoute`。新增页面或修改导航先查现有注册、分栏白名单及全屏例外，不自行换 route 类型或加第二个 Navigator。分栏细节见 [UI 适配](sizing-ui.md)。

只检查本次改变的契约：

- route 字符串、唯一 builder、arguments 类型及默认值；
- `Navigator.pop` result、等待方与 push/replace/removeUntil 栈行为；
- 相关 H5/scheme/push/native 入口与定位刷新、session、系统栏等 route effect；
- 分栏可见性、返回/切设备时详情关闭、主页面刷新与状态保持。

影响账号分支时读 [账号模式](../../tuqiang-project-map/references/account-mode.md)；改变设备分流时沿实际条件追到最终 Page 和点击控件，范围选择按 [实施覆盖](implementation-coverage.md)，局部改动不枚举无关叶子。

按 [测试规范](testing.md) 验证改变的参数、返回、栈和 effect；装配/边界变化才增加相关宿主分析或架构检查，native/scheme 的运行风险再补对应宿主证据。
