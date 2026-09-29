# Tuqiang 代码审查高风险清单

只报告影响正确性、安全、账号隔离、维护性或三端行为的问题；每项给触发条件、用户影响、路径/行号和修复方向。按实际 diff 和行为变化触发以下清单，不逐行审计无关功能；详细规则回到对应唯一事实源。

| Diff 风险 | 必查 |
|---|---|
| 登录/session/请求/cache/UI 分支 | 按本次改变的账号行为核验 isEnterprise 与相关两侧分支；身份/隔离变化再追请求、cache、UI 和切换/退出，不因已有分支审计整条会话 |
| 可见文本或语言切换 | 按 [国际化](i18n.md) 区分 key/已译文本/业务值；无重复翻译、fallback 或逐层兼容；相关 key 全 locale/占位符校验，切语言与 RTL 按可达范围验证 |
| await/Timer/listener/plugin | owner、新鲜度、account/device/key/session 身份、资源释放；success/catch/finally/whenComplete 全出口 |
| Riverpod | 复用已有状态身份与订阅；本次改变异步发布、重算/销毁或命令保活时才按 [异步规则](async-lifecycle.md) 检查对应 owner，不为同步 Provider 新增 epoch |
| JSON/网络 | DTO/parser 收窄动态类型；nullable/default/清空语义、错误和脱敏正确 |
| State/route | family key、route/action 参数和 State 字段不混；arguments/result/栈与 route effect 不意外变化 |
| 复用/新增计算 | 按 [复用与纯函数](local-style-and-reuse.md) 复用已有状态/函数/组件；新计算显式输入、无全局读取/副作用/输入修改 |
| owner/公共 API | 位于真实 app/feature/shared/core/plugin；跨包只用公开 API；全部现有调用契约已查 |
| 平台/地图/设备 | 受影响端的共享/专属实现；真实地图行为变化才检查七候选；确认范围内受影响的 route leaf |
| asset/布局/权限 | pubspec/package/语言状态正确；无假切图；.sc、SafeArea、权限用途与真机流程合理 |
| 原生依赖/推送/广告/打包 | 核对 flavor、Walle channel、实际 module/factory、Manifest 和 ABI；参考项目地图构建上下文 |
| 验证/diff | 按 testing.md 分级选择聚焦检查；扩大验证有触发依据，通过后停止；已执行与必要但未执行项如实；无无关重构、敏感值、BOM 或 diff whitespace |

不要把一次 mounted、一次 .tr、一次 standard analyze 或“公共实现”当作整类风险已关闭。
