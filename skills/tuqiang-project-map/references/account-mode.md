# 个人/企业账号模式

调查或修改登录/session、账号相关请求、权限、缓存或页面可见性时读取；纯展示、尺寸或包依赖问题不必展开。

| 值 | 证据 |
|---|---|
| personal | 有效 session 明确 `isEnterprise != true`，或只进入个人实现 |
| enterprise | 链路明确 `isEnterprise == true`，或只进入企业实现 |
| both | 需求覆盖两种模式，且两侧分别核验 |
| unknown | 证据不足；会改变行为时停止推断并最小澄清 |

这是同一 Tuqiang App 的运行时维度，独立于 AppTarget、flavor 和平台。

## 判定链（回答前用 `rg -n` 重查）

| 阶段 | 当前 symbol | 证明内容 |
|---|---|---|
| 用户与身份 | `shared_account/lib/src/domain/tq_user_model.dart`：`TQUserModel.isEnterprise` / `identifier` | 模式与账号标识的承载 |
| 企业登录 | `feature_auth/lib/src/page/ent_login_page.dart` | 成功结果如何写 isEnterprise |
| 登录落地 | `apps/tuqiang_app/lib/app/common/manager/login_utils.dart`：`onLoginSuccess` | 用户持久化、全局值与 token |
| 运行时权威值 | `apps/tuqiang_app/lib/app/legacy_shared/manager/tq_global_model.dart`：`TQGlobalModel.isEnterprise` | 未显式传参时的来源 |
| App 适配 | `apps/tuqiang_app/lib/app/state/app_runtime_state.dart`：`AppRuntimeState` | callback 如何向下暴露 |
| Composition | `apps/tuqiang_app/lib/bootstrap.dart`：`getApp` | Repository、path、query 或两套实现如何注入 |
| 显式领域值 | `shared_device/lib/src/domain/device_catalog_query.dart`：`DeviceAccountMode` | 设备查询如何携带模式 |

`TQGlobalModel.isEnterprise` 在用户未恢复时也可能为 false，必须同时证明有效 session/identifier。模式经 callback、构造参数、query 或 cache scope 改名后继续追到终点。

## 按问题核验

只选会影响结论的维度；查单个接口时先确认它的模式输入与实现，不自动展开整个登录流程。

- 入口：个人/企业登录、自动登录、恢复、切换。
- identity：isEnterprise 与 identifier 的写入、持久化、恢复。
- token/header：`onLoginSuccess` 与 `AppHttpDelegate` 如何更新/读取（不展示值）。
- path/contract：Repository 选择的 API symbol、method、请求/响应 DTO。
- 状态与缓存：family/cache/disk scope 是否含模式与账号身份。
- 权限与 UI：route、列表、空态、详情或操作在哪里分流。
- reset 与并发：切换/退出/session 失效清理哪些 Provider、Manager、pending、缓存；await 后是否仍匹配发起时的 mode/identifier/session。

## 红线

- `accountType` 通常是手机号/邮箱等登录类型，不能替代 isEnterprise。
- 未登录时的 false 不证明 personal；公共 package 也不证明两种模式都适用。
- 没有显式 if 不证明无差异：path、Repository、DTO、query 或 callback 可能已分流。
- 缺失模式写 unknown，不默认个人；mounted 只证明 owner 存活，不证明结果属于当前账号。
- 结论涉及账号时写明模式与判定来源；只查一侧就说明范围，不能笼统写"已兼容个人/企业"。
