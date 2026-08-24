# 异步、网络与序列化 · 前端深度对照表

> 主文档见 [../SKILL.md](../SKILL.md)。本文件展开 §1 的「异步与网络」部分。

## 1. 异步模型对照表

| JS / TS | Dart | 大白话 |
|---|---|---|
| `Promise<T>` | `Future<T>` | 一个"未来才有结果"的盒子 |
| `async / await` | `async / await` | 写法几乎逐字符相同 |
| `Promise.all([...])` | `Future.wait([...])` | 并发跑多个，全好了再继续 |
| `.catch(e => ...)` | `try { } on Exception catch (e) { }` | Dart 用 try/on/catch，不用 .then 链 |
| 微任务队列 | 事件循环（单线程 isolate） | 同样是单线程 + 消息队列，没有多线程心智负担 |
| Web Worker | `Isolate` | 真·多线程，但一般业务碰不到 |

结论：**「你会 JS 的 async/await 就会 Dart 的，连关键字都懒得换。」**

## 2. 网络请求对照表

| JS | Dart | 说明 |
|---|---|---|
| `axios` | `dio` | 拦截器、超时、取消 token 全都有，企业项目标配 |
| `fetch` | `http` 包 | 官方轻量版，够用但裸 |
| `axios.create({ baseURL, timeout })` | `Dio(BaseOptions(baseUrl:, connectTimeout:))` | |
| 拦截器 `interceptors.request` | `dio.interceptors.add(InterceptorsWrapper(...))` | 塞 token、统一报错都在这 |
| 取消请求 AbortController | `CancelToken` | |

```dart
final dio = Dio(BaseOptions(baseUrl: 'https://api.example.com', connectTimeout: 10.s));
dio.interceptors.add(InterceptorsWrapper(
  onRequest: (opt, handler) {
    opt.headers['token'] = getToken();     // ≈ axios 拦截器塞 token
    handler.next(opt);
  },
));
final res = await dio.get('/users');        // res.data 直接就是解析好的 JSON
```

## 3. JSON 序列化：最大的心智差异

JS 对象天生就是字典，Dart 类型严格，所以**必须手写（或生成）转换函数**：

```dart
class User {
  final String name;
  const User({required this.name});

  factory User.fromJson(Map<String, dynamic> j) => User(name: j['name']);  // ≈ JSON.parse 后的整形
  Map<String, dynamic> toJson() => {'name': name};                          // ≈ JSON.stringify 前的定制
}
```

大白话：**「fromJson/toJson 就是手动版 `JSON.parse/stringify`。嫌手写烦就上
`json_serializable` 自动生成，≈ 写个 TS interface 让工具帮你造转换函数。」**

安全取值习惯：后端可能给 null 时用 `j['name'] as String?` 接住，
等价于 TS 可选链的心智——「别信接口，先判空」。

## 4. Stream：会持续推送的 Promise

| 场景 | Future | Stream |
|---|---|---|
| 心智模型 | `Promise`（一次性） | RxJS `Observable`（多次推送） |
| 典型用途 | 一次 HTTP 请求 | WebSocket、倒计时、定位轨迹、下载进度 |

```dart
Stream<int> countdown() async* {          // async* ≈ 生成器函数 function*
  for (var i = 3; i > 0; i--) {
    yield i;                               // 推一个值 ≈ observer.next(i)
    await Future.delayed(const Duration(seconds: 1));
  }
}
```

消费端三选一：
- `await for (final v in stream)` ≈ for-await-of；
- `.listen((v) {...})` ≈ subscribe；
- UI 里直接 `StreamBuilder` ≈ 订阅 + 模板渲染二合一。

## 5. 常见坑速查

| 现象 | 大白话解释 |
|---|---|
| `type 'Null' is not a subtype...` | 接口字段是 null 但你按非空接了；用可空类型 + 默认值兜底 |
| `setState after dispose` | 组件已销毁还敢刷 UI；异步回来先判 `mounted`（≈ 清理过的 effect 别再 setState） |
| await 卡死不返回 | 忘了 await 或者请求没走拦截器的 mock 分支，看 Network/日志确认 |
