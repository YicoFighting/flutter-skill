# Tuqiang 代码审查高风险清单

只报告影响正确性、安全、账号隔离、维护性或三端行为的问题；每项给触发条件、用户影响、路径/行号和修复方向。详细规则回到对应唯一事实源。

| Diff 风险 | 必查 |
|---|---|
| 登录/session/请求/cache/UI 分支 | accountMode 来源是 isEnterprise；personal/enterprise 的请求、identity/cache、UI、切换/退出与测试均闭合 |
| 可见文本或语言切换 | 当前 manifest 全 locale、非空值、占位符、动态翻译；Auth/Mine、Arabic RTL；运行 i18n validator |
| await/Timer/listener/plugin | owner、新鲜度、account/device/key/session 身份、资源释放；success/catch/finally/whenComplete 全出口 |
| Riverpod | WidgetRef mounted；Notifier 每轮 epoch；StateNotifier super.dispose；onDispose 不冒充 await barrier；autoDispose 命令有监听/keepAlive |
| JSON/网络 | DTO/parser 收窄动态类型；nullable/default/清空语义、错误和脱敏正确 |
| State/route | family key、route/action 参数和 State 字段不混；arguments/result/栈与 route effect 不意外变化 |
| owner/公共 API | 位于真实 app/feature/shared/core/plugin；跨包只用公开 API；全部现有调用契约已查 |
| 平台/地图/设备 | Bug Android+OHOS 与 iOS 影响；新需求三端；地图七行；确认范围内的 route leaf |
| asset/布局/权限 | pubspec/package/语言状态正确；无假切图；.sc、SafeArea、权限用途与真机流程合理 |
| 原生依赖/推送/广告/打包 | 核对 flavor、Walle channel、实际 module/factory、Manifest 和 ABI；参考项目地图构建上下文 |
| 验证/diff | 覆盖台账、聚焦 tests、standard/ohos、boundary、build/真机与未执行项如实；无无关重构、敏感值、BOM 或 diff whitespace |

不要把一次 mounted、一次 .tr、一次 standard analyze 或“公共实现”当作整类风险已关闭。
