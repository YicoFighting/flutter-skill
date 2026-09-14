# 个人/企业账号模式

这是 accountMode 的唯一事实源。登录/session、请求/DTO、设备目录、消息、权限、缓存、页面可见性、切换或退出账号必须读取。

| 值 | 证据 |
|---|---|
| personal | 有效 session 明确 isEnterprise != true，或只进入个人实现 |
| enterprise | 链路明确 isEnterprise == true，或只进入企业实现 |
| both | 需求覆盖两种模式，且两侧分别核验 |
| unknown | 证据不足；若会改变行为，停止推断并最小澄清 |

这是同一 Tuqiang App 的运行时维度，不是 AppTarget、flavor、平台或独立构建。standard/ohos 与 accountMode 必须分栏记录。

## 判定链

回答前用 rg -n 重查：

| 阶段 | 当前 symbol | 证明内容 |
|---|---|---|
| 用户与身份 | `packages/shared/shared_account/lib/src/domain/tq_user_model.dart`：`TQUserModel.isEnterprise` / `identifier` | 模式和账号标识如何承载 |
| 企业登录 | `packages/feature/feature_auth/lib/src/page/ent_login_page.dart` | 成功结果如何写 isEnterprise |
| 登录落地 | `apps/tuqiang_app/lib/app/common/manager/login_utils.dart`：`onLoginSuccess` | 用户持久化、全局值和 token 更新 |
| 运行时权威值 | `apps/tuqiang_app/lib/app/legacy_shared/manager/tq_global_model.dart`：`TQGlobalModel.isEnterprise` | 未显式传参时的模式来源 |
| App 适配 | `apps/tuqiang_app/lib/app/state/app_runtime_state.dart`：`AppRuntimeState` | callback 如何向下暴露模式 |
| Composition | `apps/tuqiang_app/lib/bootstrap.dart`：`getApp` | Repository、path、query 或两套实现如何注入 |
| 显式领域值 | `packages/shared/shared_device/lib/src/domain/device_catalog_query.dart`：`DeviceAccountMode` | 设备查询如何携带模式 |

TQGlobalModel.isEnterprise 在用户尚未恢复时也可能返回 false；必须同时证明有效 session/identifier。模式经 callback、构造参数、query 或 cache scope 改名后，继续追到终点。

## 必查维度

| 维度 | 要回答 |
|---|---|
| 入口 | 个人/企业登录、自动登录、恢复或切换从哪里进入 |
| identity | isEnterprise 与 identifier 如何写入、持久化和恢复 |
| token/header | onLoginSuccess 与 AppHttpDelegate 如何更新/读取；不展示值 |
| path/contract | Repository 选择的 API symbol、method、请求/响应 DTO |
| 状态与缓存 | family/cache/disk scope 是否包含模式和账号身份 |
| 权限与 UI | route、列表、空态、详情或操作在哪里分流 |
| reset | 切换、退出、session 失效如何清 Provider、Manager、pending 和缓存 |
| 并发 | await 后是否仍匹配发起时的 mode/identifier/session |
| 测试 | 个人、企业、切换、退出和恢复覆盖哪些受影响分支 |

不相关项写“不涉及 + 证据”。both 可共用实现，但必须有共同 symbol 和两侧入口证据。

## 红线

- accountType 通常表示手机号/邮箱等登录类型，不能替代 isEnterprise。
- 未登录时的 false 不证明 personal；公共 package 也不证明同时适用两种模式。
- 没有显式 if 不证明无差异；path、Repository、DTO、query 或 callback 可能已分流。
- 缺失模式字段写 unknown，不能默认为个人。
- mounted 只证明 owner 存活，不能证明结果仍属于当前账号。

最终结论必须写 accountMode、判定来源、上表各项结果和未核验的一侧；不能只写“已兼容个人/企业”。
