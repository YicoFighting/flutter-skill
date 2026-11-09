# Flutter ↔ Web 对照

类比只辅助理解，结论仍由当前 Dart 声明、写入与消费证据支持。

## 状态

| Flutter / Riverpod | Vue3 | React |
|---|---|---|
| `Provider.family(key)` | keyed composable/store | keyed store / query key |
| Notifier / StateNotifier | Pinia action owner | reducer/store action |
| `ref.watch(provider.select(...))` | computed / store getter | selector hook |
| `ref.listen` | `watch` / effect | `useEffect` 订阅 |
| `ProviderScope` override | `provide/inject` 组合根 | Context Provider |
| AsyncValue / FutureProvider | 异步 composable 状态 | query 状态（loading/error/data） |

易混点：family(arg) 按参数相等性选实例，不是给全局 State 传参；Provider 创建不等于发请求（可能来自 build、load、listener、页面事件或 composition callback）；写入后要找到实际 watch/select/listener 才能解释 UI 更新，Manager/cache 还可能有桥接通知；autoDispose 不保证离页立即销毁，忽略旧发布也不等于取消底层请求。不要因熟悉某种状态库推荐替换项目现有 owner。

## 路由

| Flutter | Web |
|---|---|
| route name + arguments | router path/params、location state |
| builder → Page | 路由组件 + props |
| `Navigator.pop(result)` / await push | 回调或导航后的状态回传 |
| `CoreAdaptivePageRoute` 分栏 | 主从布局 + 嵌套路由 |

解释去向时追到实际 builder/Page；route string、barrel 或 contract 不足以确认行为。设备页面受 deviceType/scene/cameraScene 分流，不用第一个 route 代表所有设备。

## 异步与网络

Future ≈ Promise，Repository ≈ API client/queryFn。说明当前代码实际存在的保护与缺口：owner 存活、结果新鲜度、身份匹配、资源释放是四件事，`mounted` 只回答第一件。只引用接口 symbol 与语义，不展示 endpoint、Token 或配置。

## 布局

| Flutter | Web |
|---|---|
| Row/Column + Expanded/Flexible | flex grow/shrink |
| Stack/Positioned | position relative/absolute |
| ListView/CustomScrollView | 滚动容器 / 虚拟列表 |
| LayoutBuilder / MediaQuery | container / viewport query |
| SafeArea | safe-area inset |
| `.sc` | 以 375 设计宽缩放的 rem 类单位（上限 1.2） |

约束父传子、尺寸子传父，更像显式 layout protocol 而非文档流。溢出或点击问题查父约束、轴向、scroll owner、inset 与最终 hit target（嵌套 Gesture/InkWell）。

## Widget 生命周期

| Flutter | Web |
|---|---|
| initState | 首次挂载（`onMounted` / `useEffect(..., [])`） |
| didChangeDependencies | 注入依赖变化 |
| didUpdateWidget | props 变化或外部 owner 替换 |
| build | 可多次执行的渲染求值 |
| dispose | 卸载清理（`onUnmounted` / effect cleanup） |

资源问题说明谁创建、何时绑定、重绑与释放；build 可能多次执行，不放副作用。
