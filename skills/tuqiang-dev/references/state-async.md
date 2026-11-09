# 状态、网络与异步生命周期

Tuqiang 是 Riverpod（lockfile 当前 2.6.1）、Manager/单例、Widget State、Controller、缓存与插件状态并存的混合架构。先复用已有状态与 selector，沿目标 owner 的订阅/写入方式修改，不另建重复状态；拓扑与当前代表 Provider 见 [状态与设备链](../../tuqiang-project-map/references/state-device-flow.md)。

## 状态身份

- route 参数带页面上下文；family key 决定 Provider 实例；方法参数控制一次 operation；State 字段保存结果——不得混用。
- family 对象 key 不可变并有稳定 `==/hashCode`；修改 key 时搜索全部构造点、override、缓存与测试。
- 数据受账号影响时，family/cache/session scope 必须包含或验证 accountMode，见 [账号模式](../../tuqiang-project-map/references/account-mode.md)。
- 跨 feature contract：feature 定义 `Provider<Contract>`，`apps/tuqiang_app` 的 `ProviderScope` override 注入；改 contract 时同时检查声明、`getApp`、standard/ohos、route/result 与 session reset。
- 切设备、切 family key、切语言、登出、切账号分别检查 invalidate/reset。

## 网络与数据边界

- 不得凭需求编造 URL、字段、成功响应或 null 语义；不输出 endpoint、Token、header 密钥、签名或完整个人信息。
- 沿用 `core_http::TQHttp` 与 owner 现有 loading/error/timeout 处理，不另建 Dio。`ResultModel` 以 `success` 判成功、`desc` 为错误文案；`data` 在 Repository/parser 边界用 `TCheck<T>` 或明确 parser 收窄，不把 `List<dynamic>`/未校验 JSON 扩散到业务层。
- 请求 DTO 与响应 Model 分开；required、nullable、默认值、兼容字段与"省略/显式清空"来自接口契约，兼容只在 parser/Model 边界处理一次；Model 不承载 UI 文案。
- endpoint、DTO、Repository 放真实 feature 或职责匹配的 `shared_*`，不因 app 提供网络能力就把业务实现放进 app。长生命周期 owner 不在构造时固化 `isEnterprise`，沿现有 closure/provider/session snapshot 保持动态身份。
- 日志脱敏；异常不静默吞掉，按 owner 映射为可观察的 error/empty/提示。

## 异步：四道独立防线

不是每个 `await` 都要加 `mounted`。只有 async gap 之后访问生命周期 owner、发布 UI/状态/副作用或持有可释放资源时才按 owner 选择保护：

1. **存活**：发布目标还在吗？（`mounted` / `_disposed`）
2. **新鲜度**：仍是最新 operation 吗？（generation / requestVersion）
3. **身份**：仍属于当前 device/key/session/accountMode 吗？（参数与 session 快照）
4. **资源**：谁取消 Timer、Stream、listener、plugin handler 或请求？

四者不能互相替代。保护要覆盖全部出口：`try/catch/finally`、`.then/.catchError/.whenComplete`、post-frame、Timer、Stream、MethodChannel、listener；每个新的 async gap 都可能让之前的 mounted 结论失效。

| owner | 存活门 | 新鲜度与身份 | 资源 |
|---|---|---|---|
| 纯 Repository/解析 | 无 | 调用方负责 | 只取消真实可取消的资源 |
| `StatefulWidget` / `ConsumerState` | 每个 gap 后检查 `mounted`/`context.mounted`；销毁后不 `ref.read/invalidate` | 可重复或参数可切换时加 operation token 与参数快照 | `dispose` 释放自建资源；外部 controller 在 `didUpdateWidget` 重绑 |
| `StateNotifier` | `mounted` | requestVersion + device/key/session/accountMode 快照 | override `dispose` 先失效 token、取消资源，最后 `super.dispose()` |
| `Notifier/AutoDisposeNotifier`（2.6.1） | 无 `ref.mounted`；每轮 `build` 恢复 active 并注册 `ref.onDispose` 使该轮 epoch 失效 | 操作捕获 epoch，发布前比较最新值 | onDispose 只做同步取消；需顺序保证的清理用显式可 `await` 的 shutdown/clear |
| `FutureProvider.autoDispose` | Riverpod 忽略旧实例发布 | family key 隔离；有外部副作用时另加 token | 底层 Future/HTTP 不会自动终止 |
| `ChangeNotifier`/Controller | `_isDisposed` 后不 `notifyListeners` | generation + 身份快照 | override `dispose` 成对释放 |
| Timer/Stream/plugin/listener | 回调触碰 owner 前检查存活 | restart 时使旧 token 失效 | `cancel/removeListener/setMethodCallHandler(null)`，不用不可移除的匿名 listener |

## Riverpod 2.6.1 要点

- Widget 的 `build/initState/dispose/didUpdateWidget/didChangeDependencies` 不得同步写 Provider；首次命令放 Provider 初始化或用户事件，确需 Widget 发起时安排到首帧后并先检查 `mounted`。
- Widget `ref.listen` 只在 build；其他生命周期用 `listenManual`；外部 `ProviderContainer.listen` 的 subscription 由外部 owner 关闭。
- 仅 `read(autoDisposeProvider(key).notifier).load()` 不保活；命令型 owner 需要真实 watch/listen 或有业务依据的 `keepAlive`，不要无条件保活。
- Notifier 实例可能跨重算复用而上一轮 `onDispose` 已触发：每轮 build 恢复 active、推进 epoch；dispose 闭包捕获本轮资源，避免误关新一轮资源。

## 发布边界

复用 owner 已有的 requestVersion、身份与存活判断。没有现成防线时：请求前捕获 version/key/session，返回后先查存活，再读取**此时最新**的值比较，通过才发布。计数与发布留在 owner；确需提取比较函数时显式传入捕获值与当前值（见 [纯函数](local-style-and-reuse.md)），不新建隐式读取实例字段或 Provider 的 helper。`async void` 难以等待与测试，事件回调用 `unawaited(worker())` 并让异常可观察。

成熟样本（使用前 `rg -n` 重查，不保存行号）：`device_catalog_provider.dart` 的 requestVersion + scope、`media_download_queue_provider.dart` 每轮 build 恢复 active 与 lifecycleVersion，测试 `feature_gps/test/trace/trace_provider_lifecycle_test.dart`、`feature_camera/test/alarm/video_alarm_notifier_lifecycle_test.dart`。

## 验证场景

按本次改变的异步行为选择，用可控 `Completer`/fake，不用真实网络与固定 sleep：销毁后完成不发布；A/B 乱序只保留最新；请求中切 device/key/session/accountMode 不写入新身份；dispose 后 Timer/subscription/handler 已解绑；success/catch/finally 均不在已销毁 owner 上发布。是否运行测试按 [验证](testing.md) 与项目规则决定；评审只复查本次改变的发布点与资源生命周期，不因文件已有 `await` 审计整页。
