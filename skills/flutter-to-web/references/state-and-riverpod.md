# Riverpod 状态管理 · 前端深度对照表

> 主文档见 [../SKILL.md](../SKILL.md)。本文件是 §1 映射表中「全局状态」部分的展开版，
> 遇到复杂状态代码看不懂时按需查阅。所有类比以 Vue3 / Pinia 为主、React 为辅。

## 1. Provider 全家桶对照表

| Riverpod | Vue3 世界 | React 世界 | 一句话本质 |
|---|---|---|---|
| `Provider<T>` | 注入一个同步计算值 / 工具实例 | Context 里放个单例 | 「往仓库放一个现成的东西」（如 dio 实例） |
| `FutureProvider<T>` | Pinia 的 async action | React Query 的 `useQuery` | 「声明一次接口调用，loading/error/data 全帮你管好」 |
| `StreamProvider<T>` | `watch` 一个持续推送的数据流 | RxJS 订阅 + `useSyncExternalStore` | WebSocket、倒计时、定位轨迹这类"源源不断"的数据 |
| `StateProvider<T>` | 一个 `ref()` 裸响应式变量 | `useState` | 最简单的可写状态（开关、选中 tab） |
| `StateNotifierProvider<S, T>` | 整个 Pinia store（state + actions） | useReducer + Context | 正经业务模块的标配，改状态的方法全在 Notifier 里 |
| `ConsumerWidget` | setup() 里用了 store 的组件 | 用了 useSelector 的组件 | 「这个组件订阅了仓库」 |
| `ConsumerStatefulWidget` | 有本地状态且还要连仓库的组件 | useState + useSelector | 既要 TextEditingController 又要 watch 全局数据 |

## 2. ref 三件套：read / watch / listen

```dart
ref.read(userProvider)              // 查字典：拿一次就走，不订阅（事件回调里用）
ref.watch(userProvider)             // computed / useSelector：数据变 → UI 自动重渲染（build 里用）
ref.listen(userProvider, (prev, next) { ... })  // watch(回调版)：变化时执行副作用（弹 toast、跳路由）
```

**铁律级口诀**：`build` 里只准 `watch`；按钮回调里只准 `read`；要弹窗/跳转就用 `listen`。
翻译成 Vue：`computed` 里不会去 `store.dispatch`，一个道理。

## 3. 典型样板翻译示例

### StateNotifier 三板斧（= 一个 Pinia store）

```dart
class LoginState {                    // = Pinia 的 state（字段全 final，不可变）
  final bool loading;
  const LoginState({this.loading = false});
}

class LoginController extends StateNotifier<LoginState> {   // = store 的 actions 部分
  LoginController(this.api) : super(const LoginState());
  final HttpApi api;

  Future<void> submit(String pwd) async {
    state = const LoginState(loading: true);      // 整体替换 state，不是改字段
    await api.login(pwd);
    state = const LoginState(loading: false);
  }
}

final loginProvider =
    StateNotifierProvider<LoginController, LoginState>((ref) => LoginController(ref.watch(httpProvider)));
```

大白话：**「写了一个登录 store：state 只有 loading 字段，submit 就是个 action。
Dart 不允许偷偷改字段，所以每次都 new 一个新 state 整体换上去——相当于你写
`state = { ...state, loading: true }`，仅此而已。」**

### 页面接线（= 组件里用 store）

```dart
class LoginPage extends ConsumerWidget {
  build(context, ref) {
    final s = ref.watch(loginProvider);            // computed：自动跟随
    return ElevatedButton(
      onPressed: () => ref.read(loginProvider.notifier).submit('123'),   // dispatch action
      child: Text(s.loading ? '登录中...' : '登录'),
    );
  }
}
```

### session 重置（= 退出登录清空所有 store）

`ref.invalidate(loginProvider)` ≈ Pinia 的 `$reset()` / 把 store 恢复出厂设置。
项目里通常在登出时把用户相关 provider 全部 invalidate 一遍。

## 4. 常见疑问速查

| 你可能会问 | 大白话答案 |
|---|---|
| 为什么不直接用一个全局变量？ | 能跑，但没响应式：改了变量页面不会刷新。Provider 就是给你加了"变了自动通知 UI"的 buff |
| `autoDispose` 是干嘛的 | 页面没人看了就自动销毁状态，≈ 组件卸载时清空对应 store 分片 |
| `family` 是干嘛的 | 同一个 provider 按参数缓存多份，≈ `useQuery(['user', id], ...)` 按 key 缓存 |
| 状态类为什么要 `copyWith` | Dart 没有 spread 更新对象的习惯用法，`copyWith(loading: false)` ≈ `{...state, loading:false}` |
