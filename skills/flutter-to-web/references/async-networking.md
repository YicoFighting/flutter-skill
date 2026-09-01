# 异步与网络：按产品识别真实协议栈

> 先按 [动态项目根目录协议](project-root-resolution.md) 验证 `<TUQIANG_ROOT>`，再按 [双产品上下文](product-context.md) 判定 Tuqiang / Laoying。不要从仓库里“能搜到某个 client”推断本次调用就经过它。

## 1. Tuqiang：TQHttp 与 shared/feature Repository

Tuqiang 业务请求优先追当前源码实际采用的 `core_http`、`TQHttp`、`ResultModel`、`TCheck<T>`、`TQAddress` 和 feature/shared Repository。shared 拆分后，具体 Repository、API path resolver 或 runtime 可能由 `apps/tuqiang_app/lib/bootstrap.dart` 通过 Provider override、构造参数、`*Runtime.configure` / `*ApiPaths.configure` 注入；不能只在 feature 内找 endpoint。

```text
Widget / RouteObserver / 根 Host
  → Notifier/Command/Manager
  → injected Repository / TQHttp
  → ResultModel
  → TCheck<T> / fromJson
  → Riverpod State、Manager/cache 或局部状态
  → watch/listen/Widget
```

只有源码真的直接调用 `dio`、`http` 或其他 client 时，才按裸 client 解释。不要把所有 Tuqiang 请求强行画成完全相同的 Repository + Riverpod：真实值可能在 Manager/cache，Provider 只携带 revision，也可能由插件或 Timer 回填。

## 2. Laoying：LYBackendHttpClient 与 owner Repository

Laoying 不使用 TQHttp 作为默认业务链。当前检索入口：

- `apps/laoying_app/lib/app/infrastructure/backend/ly_backend_http_client.dart`：配置、签名、transport、session、timeout 与错误边界；
- `apps/laoying_app/lib/bootstrap.dart`：创建 backend client，并把它注入 `LYHttpAuthRepository`、`LYHttpGpsRepository`、`LYHttpOverviewRepository` 等 owner Repository；
- `apps/laoying_app/lib/app/<owner>/repositories/`：接口、HTTP adapter、结果与 Model 的真实边界；
- `apps/laoying_app/lib/app/<owner>/providers/*controller.dart`：把结果写入 `ChangeNotifier` 字段并通知 UI。

```text
Widget / route builder
  → owner Controller
  → owner Repository interface
  → LYHttp*Repository
  → LYBackendHttpClient
  → owner result / Model
  → Controller 字段 + notifyListeners()
  → ListenableBuilder / AnimatedBuilder / listener
```

讲解时展示 bootstrap 的具体实现注入，但省略环境地址、签名值、Token 和生产配置。不要把 Laoying 的结果对象改称 `ResultModel`，也不要用 `TCheck<T>` 模板替代其 owner-specific 解析；类型、错误和空值以目标 Repository 当前实现为准。

## 3. Web 心智映射

| Dart/Flutter | Web 近似 | 解释重点 |
|---|---|---|
| `Future<T>` | `Promise<T>` | 最终完成一次，不是响应式状态本身 |
| `Stream<T>` | RxJS Observable | 持续推送，需要订阅和释放 |
| `TQHttp` | Tuqiang 的统一 axios/fetch 封装 | 请求、会话、错误、日志等项目语义以源码为准 |
| `LYBackendHttpClient` | Laoying 的独立 API client | 由 bootstrap 配置并注入 owner Repository |
| Repository interface + HTTP adapter | service interface + concrete client adapter | UI/Controller 不应被 backend 字段污染 |
| `fromJson` / owner parser | TypeScript schema/mapper | 把动态响应收窄为业务类型 |

类比只帮助理解；两条产品协议栈的响应 envelope、错误类型、身份字段和注入方式不能互换。

## 4. 序列化与字段血缘

`fromJson` 类似把后端 JSON 映射成有类型的 TypeScript 对象。是否过滤 null、使用 `TCheck<T>`、owner mapper 或自定义 result 都取决于当前接口契约。

对用户关心的字段追齐：请求参数来源 → HTTP adapter 使用的 backend 字段 → Model/DTO 映射 → State/Controller 字段 → 最终 Widget。引用 endpoint 时只展示常量名与职责，不复制实际值。

## 5. 生命周期、错误与竞态

- `await` 前后页面可能已离开：Widget 检查 `mounted`，Notifier/Controller 检查自己的 operation/generation 与生命周期；
- 多次请求可能乱序，必须找目标实现是否丢弃旧响应、取消任务或以稳定 key 隔离；
- `catch` 不能被解释成“请求失败页面自然不变”，要追 error/empty/loading 字段或诊断记录；
- Tuqiang 检查 Provider/Manager/cache 的清理，Laoying 检查 controller listener、`dispose()` 与 session reset participant；
- `Future.delayed` 只表示延时，不等于真实网络；先判定是测试 fake、轮询还是生产逻辑。

一句话总结：先判产品协议栈，再把“触发请求、响应收窄、状态写入、响应式消费”闭环；不要用一条产品线的 client、响应模板或状态术语解释另一条。
