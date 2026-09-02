# 状态管理规范（双产品）

先确认产品。途强智能当前是 Riverpod、Manager/单例、局部 State 和插件状态并存；老鹰在线业务当前不使用 Riverpod，而由 `LYAppProvider`/`LYAppScope`、app-local ChangeNotifier Controller、Repository 和 Widget State 组成。不得跨产品套状态模板。

## 1. 途强 Riverpod 基线

最近扫描基线为 `flutter_riverpod` / `riverpod` 2.6.1，修改前仍需核对当前 pubspec/lockfile。主要模式是手写 `Provider`、`StateNotifierProvider`、family/autoDispose，少量 `NotifierProvider.autoDispose.family` 和 `FutureProvider.autoDispose.family`；不为统一 API 改写存量。

修改前画完整图：

```text
声明与完整泛型 → family key → State/Notifier → Repository/请求触发
→ 所有 state/seed/apply/Manager/cache 写入 → watch/select/read/listen
→ 最终 UI/副作用 → autoDispose/keepAlive/invalidate/session reset
```

family 是实例身份，不是临时方法参数。同一 `ProviderContainer` 中相等 key 复用实例，不同 key 隔离；对象 key 必须不可变并有稳定 `==/hashCode`。区分 route arguments、family key、Notifier 方法参数和 State 字段，修改 key 时搜索全部构造点与测试。

`autoDispose` 只表示无人监听后允许销毁。检查根 Host/Coordinator、`ProviderContainer` listener、`keepAlive`、`onDispose`、切设备和登出 reset；离开页面不等于实例必然释放。

跨 Feature contract 的方向：

```text
Feature 定义 Provider<Contract>
← apps/tuqiang_app 的 ProviderScope override 注入
← Feature 内通过公开 contract 调用
```

修改 contract 必须同步检查声明、composition root、`standard`/`ohos`、route/返回值与 session reset registry。Feature 不直接 import app 或另一个 Feature 私有实现。

## 2. 老鹰在线状态基线

应用级入口：

- `LYAppProvider extends ChangeNotifier`：持有用户 session、reset coordinator 和 refresh bus；
- `LYAppScope extends InheritedNotifier<LYAppProvider>`：把应用状态暴露给 Widget 树；
- `LYUserSession`：产品独立的用户会话；
- `LYSessionResetCoordinator`：登出/切用户的有序清理；
- `LYRefreshBus`：跨 owner 的刷新事件，不等于共享可变 store。

业务状态放八个 app-local owner 的 ChangeNotifier Controller、Repository 或局部 Widget State。修改时检查：

1. Controller 的创建者、持有者与唯一事实源；
2. `addListener/removeListener` 是否成对，Widget/Controller 是否 dispose；
3. Repository 是否通过构造函数或应用装配注入；
4. 连续异步请求是否用 generation/operation 防旧响应覆盖；
5. 需要跨会话清理的对象是否注册到 `LYAppProvider.resetSession()` 链；
6. `LYRefreshBus` 的发布/订阅是否有明确 owner、事件含义和解绑；
7. 业务目录是否因共享状态而产生相互直接 import。

不要给老鹰引入 Riverpod 只为模仿途强；若需求确实要改变状态框架，这是架构与范围决策，必须先询问用户。

## 3. 两边都适用

- State/集合对外避免静默可变；nullable、copyWith、深拷贝服从当前 owner 与契约；
- 跨 `await` 更新 Widget 前检查 Widget `mounted`；Notifier/Controller 使用各自生命周期信号；
- Timer、Subscription、FocusNode、AnimationController 和插件 listener 由创建者释放；
- loading、success、empty、error 必须可观察，异常不能静默吞掉；
- 明确 Manager/cache/database/插件与 UI State 的同步方向，不借修复做大规模状态迁移；
- build 只读状态并绑定事件，不同步写 Provider/Controller；
- 多语言派生值和用户/设备数据要进入对应产品的语言/session reset。

## 4. 验证

途强重点测 family 等值/隔离、切 key、并发、autoDispose/保活、override 和 session reset；按范围跑 Feature/package tests、`standard`/`ohos` 与 `-ProductScope tuqiang`。

老鹰重点测 Controller 初始/成功/失败/空态/并发/dispose、listener、Repository fake、`LYAppProvider.resetSession()` 和 refresh bus；在 `apps/laoying_app` 运行 analyze/test、聚焦 architecture tests，并跑 `-ProductScope laoying`。app boundary 检查器仅在其规则与当前 allowlist 一致时作为门禁，已知基线见 [testing.md](testing.md)。

core/shared/plugin 状态变化先枚举两产品消费者；同时影响两产品调用或公共 contract 时检查四 target 和 `-ProductScope all`，否则验证已确认产品并记录另一产品不受影响证据。未执行真机或 CI 项必须明确记录。
