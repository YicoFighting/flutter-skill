# Tuqiang 网络请求

先确认真实 API 契约和 `accountMode`。不得凭需求描述编造 URL、字段、成功响应、null 语义或生产假数据，也不得输出 endpoint、Token、header 密钥、签名或完整个人信息。

## TQHttp 与数据边界

- 沿用 `core_http` 的 `TQHttp` 和当前 owner 的 loading/error/timeout 处理，不在 Feature 内另建 Dio。
- `ResultModel` 以 `result.success` 判断成功，错误文案沿当前约定使用 `result.desc`；`result.data` 在 Repository/parser 边界通过 `TCheck<T>` 或明确 parser 收窄。
- 请求 DTO 与响应 Model 分开；required、nullable、默认值、兼容字段和“省略/显式清空”来自接口契约。
- 不把 `List<dynamic>` 或未校验 JSON 扩散到业务层；Model 不承载页面标题、按钮等 UI 文案。
- endpoint、DTO/Model 和 Repository 放真实 Feature 或职责匹配的 `shared_*` owner。是否抽 Repository 接口取决于已有边界、注入和测试需求，不堆单点空壳。

## 账号、异步与安全

账号、设备、消息、首页/Mine、session 或缓存请求必须读取 [账号模式事实](../../tuqiang-project-map/references/account-mode.md)。不能把不同 endpoint/DTO 压成无模式公共实现，也不能在长生命周期 owner 构造时固化 `isEnterprise`；沿现有 closure/provider/session snapshot 保持动态身份。

请求返回后发布 Widget/Notifier/Controller 时读取 [异步生命周期](async-lifecycle.md)。真实写操作授权、权限或平台降级不明确时进入 [需求决策门](requirement-clarification.md)。

日志必须脱敏，不记录密码、Token、完整手机号、签名材料或生产配置。异常不能静默吞掉；按当前 owner 将 failure 映射为可观察的 error/empty/提示。

## 验证

覆盖 DTO/parser 边界、personal/enterprise 契约、成功/失败/超时及相关并发；命令和证据等级统一见 [测试规范](testing.md)。fake 通过不等于后端联调通过。
