# 异步与网络 · Web 深度对照

## 1. 先识别项目封装

在按 [动态项目根目录协议](project-root-resolution.md) 验证的 `<TUQIANG_ROOT>` 中，业务请求优先看当前源码实际采用的 `core_http`、`TQHttp`、`ResultModel`、
`TCheck<T>`、`TQAddress` 和 feature 内的 endpoint/repository。只有源码真的直接调用
`dio`、`http` 或其他 client 时，才按裸 client 解释。

| Dart/Flutter | Web 近似 | 解释重点 |
|---|---|---|
| `Future<T>` | `Promise<T>` | 最终完成一次，不是响应式状态本身 |
| `async/await` | `async/await` | 语法相近，但仍要处理 Dart 类型和异常 |
| `Stream<T>` | RxJS Observable | 可以持续推送多个值，需要订阅和释放 |
| `TQHttp` | 项目统一 axios/fetch 封装 | 除请求外还承接 token、loading、错误和日志 |
| `ResultModel` | 统一响应对象 | 先判断 `success`，再读取 `desc/data` |
| `TCheck<T>` | 运行时 schema 收窄 | 把动态响应安全转换成业务类型 |

## 2. 请求到页面的链路

```text
Widget / RouteObserver / 根 Host 触发
  → Controller/Notifier
  → Repository 或 TQHttp
  → ResultModel
  → TCheck<T> / fromJson
  → State 更新
  → ref.watch 的 Widget 重建
```

解释时不要把“请求完成”直接等同于“页面更新”：中间还可能有 Provider 缓存、并发丢弃、
错误状态和 Widget/Notifier 已销毁等情况。项目也存在 Manager/缓存单例、Notifier 公开可变字段、
`setState` 和直接 `TQHttp` 等旁路；应追到真正的数据载体，不能强行画成纯 Repository + Riverpod。

## 3. 序列化

`fromJson` 类似把后端 JSON 映射成有类型的 TypeScript 对象，但 Dart 通常需要手写工厂：

```dart
factory User.fromJson(Map<String, dynamic> json) {
  return User(name: TCheck<String>(json['name']));
}
```

`toJson` 是反方向映射。是否过滤 null 取决于接口契约；不要解释成所有请求都必须
“删掉 null”。

## 4. 生命周期和错误

- `await` 前后可能页面已经离开，Widget 判断自己的 `mounted`，Notifier 判断自己的生命周期；
- 多次请求可能乱序，项目常用 generation/request id 丢弃旧结果；
- 相同 in-flight 请求可能被合并，远程指令也可能通过 Timer 轮询后再回填同一 State；
- `catch` 不能静默吞错；页面通常需要回到可观察的 error/empty 状态；
- `Future.delayed` 只表示人为延时，不等于真实网络请求。若代码出现它，先判断是测试/预览 fake 还是生产逻辑。

引用源码时可以展示 endpoint 常量名与请求职责，但不得复制 endpoint、Token、密钥、证书、签名或生产配置的具体值。

一句话总结：这条链路就是“事件触发请求，把不可信 JSON 收窄成类型化数据，再写进
Riverpod 状态让页面响应式更新”。
