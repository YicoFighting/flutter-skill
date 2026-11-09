# Tuqiang 代码审查清单

只报告影响正确性、安全、账号隔离、维护性或三端行为的问题；每项给触发条件、用户影响、`path:line` 与修复方向。按实际 diff 触发，不逐行审计无关功能；规则细节回到对应 reference。

| Diff 风险 | 必查 |
|---|---|
| 项目规范 | 违反业务仓库 `AGENTS.md`、`.codex/skills`（`.sc`、`.tr`、分层、切图倍率、文件职责）或 `DESIGN.md` 已确认约定 |
| 登录/session/请求/cache/UI 分支 | 本次改变的账号行为核验 isEnterprise 与两侧分支；身份/隔离变化再追请求、cache、切换/退出 |
| 可见文本、语言切换 | key/已译文本/业务值不混；无重复翻译、页面 fallback 或逐层兼容；全 locale 与占位符 |
| await/Timer/listener/plugin | 存活、新鲜度、身份、资源四防线；success/catch/finally/whenComplete 全出口 |
| Riverpod | 复用已有状态身份与订阅；Widget 生命周期不同步写 Provider；命令型 autoDispose 保活合理 |
| JSON/网络 | DTO/parser 收窄动态类型；nullable/default/清空语义、错误与脱敏 |
| State/route | family key、route/action 参数、State 字段不混；arguments/result/栈/route effect 不意外变化 |
| 复用/新增计算 | 已有状态/函数/组件优先；新计算显式输入、无全局读取/副作用/输入修改 |
| owner/公共 API | 位于真实 app/feature/shared/core/plugin；跨包只用公开 API；现有调用契约已查 |
| 平台/地图/设备 | 受影响端的共享/专属实现；鸿蒙百度专属逻辑以 `usesOhosBaiduMap` 隔离；确认范围内的 route leaf |
| asset/布局/权限 | 倍率目录与 pubspec 正确，无假切图；pane 尺寸不用整窗；权限状态与用途文案 |
| 原生/打包 | flavor、Walle 渠道、实际 module/factory、Manifest、ABI |
| 验证/diff | 按 [验证](testing.md) 分级；已执行与未执行如实；无无关重构、敏感值、BOM 或 whitespace 问题 |

一次 mounted、一次 `.tr`、一次 standard analyze 或"公共实现"都不能关闭整类风险。
