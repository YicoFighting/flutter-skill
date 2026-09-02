# 网络请求规范（双产品）

先确认产品和真实 API 契约。不得把途强的 endpoint、token/header、运行时配置或错误语义直接复制到老鹰在线，也不得凭需求描述编造 URL、字段、成功响应或生产假数据。

## 1. 途强智能：`TQHttp` / `ResultModel`

途强业务沿用 `core_http` 的 `TQHttp` 和同 owner 已有的 loading/错误/超时方法，不在 Feature 内自行创建 Dio。`ResultModel` 以 `result.success` 判断成功，错误文案按现有约定使用 `result.desc`；`result.data` 在 Repository/parser 边界用 `TCheck<T>` 或明确 parser 收窄。

Model 规则：

- 请求 DTO 与响应 Model 分开；required、nullable、默认值来自接口契约；
- `fromJson` 处理缺失、类型变化和兼容字段，不把 `List<dynamic>` 扩散到业务层；
- `toJson` 是否过滤 null 取决于“省略”与“显式清空”的后端语义；
- Model 不承载页面标题、按钮等 UI 文案；
- endpoint、Model、Repository 留在真实 Feature 或职责匹配的拆分 `shared_*` owner。

是否额外建立 Repository 抽象取决于已有边界、注入和测试需求，不为单个简单调用堆空壳。

## 2. 老鹰在线：`LYBackendHttpClient`

老鹰使用 app-local `LYBackendHttpClient`、`LYBackendConfig` 和各业务 `LY*Repository`/adapter。运行时 base URL、签名、凭据和产品 header 由老鹰宿主独立注入；不得复用途强 app 的运行时配置或业务 Repository。

- API 范围与字段先看 `docs/laoying/api_contract.md` 和当前 Product Scope；
- 只有 contract 明确允许时，才从个人端现有实现提取准确接口契约；这不授权复制 Feature、配置、凭据或副作用；
- API 未就绪时使用可注入 fake 或 unavailable/fail-closed 实现，不能默认“成功”或把 placeholder 带入生产；
- 业务 Repository 留在 `apps/laoying_app/lib/app/<owner>/`，跨 owner 通过应用 contract/coordinator，不互相 import 私有实现；
- 未配置或未批准的真实写操作必须失败可见，不能静默降级为成功。

## 3. 生命周期与安全

- 连续请求用 generation/request id/取消机制防旧响应覆盖；
- 页面/Controller 销毁后不发布状态；
- 401、token、header、日志和重试沿目标产品现有 client；
- 日志脱敏，不记录密码、Token、完整手机号、endpoint 密钥或生产配置；
- 真实写操作、权限和平台差异不明确时进入 [requirement-clarification.md](requirement-clarification.md)。

## 4. 验证

- 途强 Feature/shared：Model/Repository 测试、受影响 package analyze、`-ProductScope tuqiang`；
- 老鹰：业务 Repository/fake/failure 测试、`apps/laoying_app` analyze/test、聚焦 architecture tests、`-ProductScope laoying`；app boundary 已知基线按 [testing.md](testing.md) 处理；
- 修改 core/shared HTTP/parser：先枚举两产品消费者；同时影响两产品调用或公共 contract 时做四 target analyze、`-ProductScope all` 与两产品测试，否则验证已确认产品并记录另一产品不受影响证据；
- 联调未执行或环境未配置时明确记录，不能用 fake 测试声称真实接口通过。
