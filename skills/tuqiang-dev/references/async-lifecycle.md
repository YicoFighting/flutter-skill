# 异步生命周期与结果发布

不是每个 `await` 都要加 `mounted`。只有异步间隙之后要访问生命周期 owner、发布 UI/状态/副作用，或持有可释放资源时，才按 owner 选择保护。

## 四个独立问题

```text
1. 存活：发布目标还存在吗？
2. 新鲜度：结果仍属于最新 operation 吗？
3. 身份：结果仍属于当前 device/key/session/accountMode 吗？
4. 资源：谁取消 Timer、Stream、listener、plugin handler 或请求？
```

`mounted/_disposed` 只回答存活；generation/requestVersion 只回答新鲜度；参数与 session 快照回答身份；`cancel/removeListener/unregister` 回答资源释放。四者不能互相替代。

## Owner 决策表

| await 后的 owner/动作 | 存活门 | 新鲜度与身份门 | 资源门 |
|---|---|---|---|
| 纯 Repository/解析，只返回值 | 无 Widget 生命周期门 | 由调用方负责 | 只取消真实可取消资源 |
| `StatefulWidget` / `ConsumerState` 后续 `setState`、导航、Toast/Dialog、读取 `context` 或使用 `WidgetRef` | 每个 async gap 后检查 `mounted` 或目标 `context.mounted`；已销毁后也不得 `ref.read/invalidate` | 可重复操作或参数可切换时加 operation token 与参数快照 | `dispose` 释放自建资源；外部 controller 在 `didUpdateWidget` 重绑 |
| `StateNotifier` 后续读写 `state` | `mounted` | generation/requestVersion + device/key/session/accountMode 快照 | override `dispose` 先失效 token、取消资源，最后必须 `super.dispose()`，使 mounted=false 并释放内部监听 |
| Riverpod 2.6.1 `Notifier/AutoDisposeNotifier` | 不写不存在的 `ref.mounted`；每轮 `build` 恢复 active 状态并注册 `ref.onDispose`，dispose/recompute 时使该轮 lifecycleVersion 失效 | 每次异步操作捕获当前 lifecycleVersion，并由统一 `_isCurrent(version, key, session)` 校验 | `ref.onDispose` 只做同步取消/解绑或启动无需等待的兜底清理；需要顺序保证的异步清理由显式可 `await` 的 shutdown/clear 完成 |
| `FutureProvider.autoDispose` 仅返回 `AsyncValue` | 无手写 mounted；dispose/recompute 后 Riverpod 忽略旧实例的状态发布 | family key 隔离实例；Future 内有外部副作用时另加 token | 底层 Future/HTTP 不会自动终止；支持取消时在同步 `onDispose` 发起取消 |
| `ChangeNotifier`/普通 Controller | `_isDisposed`，销毁后不 `notifyListeners` | generation/operation + 身份快照 | override `dispose` 成对释放 |
| Timer/Stream/plugin/外部 listener | 回调触碰 owner 前检查存活 | restart/replacement 时使旧 token 失效 | `cancel/removeListener/setMethodCallHandler(null)`；外部 owner 禁用不可移除的匿名 listener |

## 检查所有异步出口

保护不能只写在 success 分支。逐一检查 `try/catch/finally`、`.then/.catchError/.whenComplete`、post-frame callback、Timer、Stream、MethodChannel 和 listener。每经过一个新的异步间隙，之前的 mounted 结论都可能失效。

非框架要求的 `async void` 难以等待和测试。事件回调可用同步闭包显式启动 `unawaited(worker())`，worker 返回 `Future<void>`/`Future<T>` 并让异常有可观察处理。

Flutter Riverpod 2.6.1 的 Widget `build/initState/dispose/didUpdateWidget/didChangeDependencies` 不得同步修改 Provider。页面首次命令若会立即写 state，优先放进 Provider 初始化或用户事件；确需 Widget 发起时安排到首帧后，并在回调中先检查 `mounted` 再用 `ref`。Widget `ref.listen` 只在 `build`，build 外生命周期用 `listenManual`；Widget 外 `ProviderContainer.listen` 的 subscription 由外部 owner 显式关闭。

仅 `read(autoDisposeProvider(key).notifier).load()` 不建立监听，不能保证异步 operation 期间实例存活。需要命令型 autoDispose owner 持续工作时，必须有真实 `watch/listen`，或由 Provider 按业务显式 `keepAlive`；不要为掩盖 owner 错误无条件保活。

## StateNotifier 推荐结构

```dart
Future<void> load(DeviceKey key) async {
  final version = ++_requestVersion;
  final session = _sessionSnapshot();
  final result = await repository.load(key);
  if (!_isCurrent(version, key, session)) return;
  state = state.withResult(result);
}

bool _isCurrent(int version, DeviceKey key, SessionSnapshot session) {
  return mounted &&
      version == _requestVersion &&
      key == _currentKey &&
      session == _sessionSnapshot();
}
```

示例表达的是四类门，不要求每个 owner 使用相同字段名。Riverpod `Notifier` 的实例可能跨依赖重算复用，而上一轮 `ref.onDispose` 会在重算时触发。因此不能只做一次 `_disposed = true`：每轮 `build` 都要恢复 active 状态、为该轮注册同步 dispose 回调并推进/失效 epoch；异步操作捕获 epoch，发布前同时校验 active、epoch 与身份。资源字段若会在下一轮 `build` 被覆盖，dispose 闭包应捕获本轮资源，不能误关新一轮资源。

`ref.onDispose` 是同步通知，不会等待 `Future`。可以同步 `cancel/removeListener/close`，或用 `unawaited` 启动无需顺序保证的兜底清理；logout、切账号、销毁下载任务等必须等待完成的流程，应提供显式 `Future<void> shutdown/clear`，由调用方先 `await`，再 invalidate/dispose。

## 测试配方

使用可控 `Completer` 或 fake，不使用真实网络和固定 sleep：

1. **销毁**：启动 → unmount/dispose/container.dispose → 完成 Future → 不抛异常、不发布状态或导航。
2. **乱序**：A 启动、B 启动，按相反顺序完成 → 只保留最新 operation。
3. **身份切换**：请求中切 device/family key/session/accountMode → 旧结果不写入新身份。
4. **资源释放**：dispose 后 Timer 不再触发，subscription/listener/plugin handler 已解绑；替换外部 Controller 后旧 listener 不回调。
5. **错误出口**：success/catch/finally/whenComplete 均不在已销毁 owner 上发布。

项目内可检索的成熟证据包括 `device_catalog_provider.dart` 的 requestVersion + scope、`media_download_queue_provider.dart` 在每轮 `build` 恢复 active 并由 `ref.onDispose` 推进 lifecycleVersion 的做法，以及 `trace_provider_lifecycle_test.dart`、`video_alarm_notifier_lifecycle_test.dart` 的可控异步测试。样本只证明对应机制，不代表可整段照搬；引用前必须用 `rg -n` 在当前 checkout 重新定位，不保存历史行号。

## 异步台账

diff 新增或修改 `await/then/unawaited/Timer/listen/addListener/setMethodCallHandler/state=/setState/notifyListeners` 时，评审至少记录：

```text
入口 | owner | 发布点 | 存活门 | 新鲜度/身份门 | 清理点 | 测试
```
