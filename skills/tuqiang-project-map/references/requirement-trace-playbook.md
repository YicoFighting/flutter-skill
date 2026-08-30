# 完整需求追踪 Playbook

目标：从一次可观察操作出发，恢复真实的同步调用、异步数据流、状态拓扑与 UI 消费，并用当前路径、行号和源码证据回答。用户选中的代码是搜索锚点，不是分析边界。

## 1. 先定义问题

把用户问题改写成一句可验证的问题：

```text
当 <用户/系统事件> 发生时，<输入或设备> 如何经过 <路由/状态/数据层>，
最终让 <页面字段/组件> 呈现 <结果>，失败、切换或退出时如何处理？
```

先确认：

- 起点：启动、进入页、点击、刷新、输入、推送、scheme、原生 callback、Timer 或 session 事件；
- 终点：具体 Widget、route、插件调用、本地写入或可观察副作用；
- 标识：route 常量、Page 类、方法、Provider、State 字段、DTO/model 字段；
- 分支：设备类型、账号类型、平台、权限、缓存命中、登录态。

如果用户只给一段代码，先识别其中最有辨识度的 symbol，再向上搜调用方、向下搜消费者。

## 2. 七段追踪法

### A. 用户操作或生命周期入口

找 `onTap`/`onPressed`/`onRefresh`、`initState`、首次 build gate、route/native handler 或 observer。记录 Widget 参数和当时可用的设备/账号/route 数据。

### B. 页面与路由装配

追 route 常量、Navigator 调用、`AppRouters`、`FeatureRouterRegistry`、feature router、`onGenerateRoute` 和最终 Page builder。若调用的是 Navigator/Composition contract，回到 `bootstrap.dart::getApp` 查 Provider override。

### C. 状态拓扑

对每个 Provider 建立一行：

| Provider 实例 | 声明/State/Notifier | key 来源 | 写入者 | watch/listen/read 消费者 | 生命周期/reset |
|---|---|---|---|---|---|

普通 Provider、全局选择、family keyed state 和 presentation 派生值必须分开。

### D. 数据边界

继续追 Notifier/Controller 方法到 Repository、Manager、插件或直接 `TQHttp`。写出参数从 UI/route/key 到请求 DTO 的变换，并写出响应从 `ResultModel.data`、`TCheck<T>`、`fromJson` 到 state 的变换。

只引用 API 常量名，不打开或复制 endpoint 具体值；不输出 Token、Key、证书、签名或生产配置。

### E. 状态发布与异步时序

标出 loading、成功、空数据、错误，以及：

- `await`/`unawaited` 的分叉；
- requestVersion/generation/mounted；
- pending future 去重；
- 直接写入：`state =`、Notifier 的 `apply/seed/update`、Manager setter、缓存回写；
- 触发入口：页面/Timer/listener/RouteObserver 调用的 `refresh/load/request`，与直接写入者分开列；
- `ref.listen` 的副作用或 post-frame 调度。

### F. UI 消费

从 Provider/State 字段反向搜索消费者。最终落到实际 Widget 属性或插件调用，说明 `watch`/`select` 的字段怎样触发重建。若 presentation mapper 中间转换了字段，把映射也放进链路。

### G. 失效与恢复

查页面离开、切换 family key、`autoDispose`、`keepAlive`、`onDispose`、`invalidate`、语言切换和 logout/session reset。说明下一次进入是复用、重建、磁盘恢复还是重新请求。

## 3. 同步栈、异步流与依赖图要分开

错误表达：

```text
onTap -> network -> UI
```

推荐表达：

```text
同步调用：onTap -> _selectDevice -> setModelFromList -> selectedDeviceNotifier.select

状态/调度：selectedDevice state 发布
  -> LocationContainerHost 的 ref.listen 收到变化
  -> addPostFrameCallback
  -> requestSelectedLocationContext

异步数据：snapshotNotifier.refresh
  -> repository.fetchStatus
  -> await TQHttp
  -> applyStatus
  -> state 发布

响应式依赖：Page ref.watch(snapshotProvider(key).select(...))
  -> 所选字段变化
  -> Widget rebuild
  -> Text/地图/按钮更新
```

`ref.listen`、post-frame、Future 和 rebuild 是跨时间阶段，不要称为同一条同步函数栈。

## 4. family 专项追踪

遇到 `someProvider(arg)`，必须依次回答：

1. Provider 是哪种 `.family`，声明在哪里？
2. `arg` 是 String、record 还是 value object？
3. 它从 route 参数、Widget 参数还是另一个 Provider 派生？
4. key 的 `==`/`hashCode` 是什么；哪些字段决定实例身份？
5. 同一 Container 内相同 key 是否复用，切 key 后旧实例如何处理？
6. `autoDispose` 是否被根 Host/其他页面的 watch 延长，是否调用 `keepAlive`？
7. 状态写入哪个 Notifier 的 `state`，谁读取同一个 key？
8. session reset 是 invalidate 指定实例还是整个 family？

不要回答成“Riverpod 支持传参数所以可以”。参数的业务来源、实例隔离和生命周期才是重点。

## 5. 搜索步骤

在项目根执行，优先缩小目录：

```powershell
Set-Location -LiteralPath $tuqiangRoot

# 1. 锚点定义与调用方
rg -n "<方法名>|<类名>|<字段名>" apps packages --glob '*.dart'

# 2. 路由与最终 builder
rg -n "<路由常量>|<路由字符串>|<Page类>|onGenerateRoute|routes\(" apps packages --glob '*.dart'

# 3. Provider 声明和所有实例化/读写
rg -n "final <Provider名>|<Provider名>\(|<Provider名>\.notifier|invalidate\(<Provider名>" apps packages --glob '*.dart'

# 4. State 与写入点
rg -n "class <State名>|state\s*=|copyWith\(|seed\(|select\(|refresh\(" <相关目录> --glob '*.dart'

# 5. 数据层与响应映射
rg -n "<Repository名>|TQHttp\.|ResultModel|TCheck|fromJson|toJson" <相关目录> --glob '*.dart'

# 6. 最终消费者和非 Riverpod 状态
rg -n "<状态字段>|ref\.(watch|listen|read)|\.select\(|setState\(|Manager|Controller" <相关目录> --glob '*.dart'

# 7. 生命周期与 reset
rg -n "autoDispose|keepAlive|onDispose|dispose\(|invalidate\(|SessionReset|clearForLogout" apps packages --glob '*.dart'
```

如果 symbol 名很常见，组合“文件目录 + 类型名 + 方法名”，不要依赖一次全仓宽泛搜索得出结论。

## 6. 行号与源码证据

references 不保存易漂移行号，最终回答必须保存本次搜索结果的当前行号。每个关键阶段采用：

```text
<TUQIANG_ROOT>/<相对路径>:<起始行>  <symbol>
```

随后给 3–20 行足以证明结论的 Dart 源码片段。单个片段要小，但总证据不能因为“代码应短”而跳过入口、Provider 定义、family key、写入、Repository 和消费端。

路径与行号的要求：

- 行号必须来自本次 `rg -n`/当前文件，而不是 reference 中的旧数字；
- 同一结论跨文件时逐个给路径，不能只给目录；
- 标注片段省略了什么，不能用不连续代码制造一条不存在的调用；
- 若只通过命名或邻近代码推断，明确写“推断”，并说明还缺哪份运行时证据；
- 不展示 endpoint/token/key/cert 等敏感值，即使它们恰好在上下文行中；缩小片段或脱敏字段值。

## 7. 金字塔输出模板

### 第一层：一句话结论

用业务语言回答“谁触发、状态存哪、谁展示”。

### 第二层：操作时间线

```text
进入/点击
  -> 同步方法
  -> 状态发布
  -> listener/异步请求
  -> 新状态
  -> UI 重建/副作用
```

为异步边界标注 `await`、`unawaited`、post-frame、listener、rebuild。

### 第三层：状态拓扑表

| 状态 | 定义 | 实例/key | 谁写 | 谁读/展示 |
|---|---|---|---|---|

至少覆盖用户问到的状态，以及决定它 key/生命周期的上游状态。

### 第四层：参数与生命周期

专门解释 family 参数来源、相等性、缓存隔离、autoDispose/keepAlive、invalidate/session reset。非 family 也说明作用域。

### 第五层：源码证据

按调用顺序展示当前文件路径、行号、symbol 与最小源码片段，不按文件名随意排序。

### 第六层：分支与异常

列出这次需求真正涉及的设备/账号/平台/权限/缓存分支，以及 loading、error、旧请求和页面退出处理。

### 第七层：核验边界

明确哪些已由源码确认，哪些需要运行时日志、后端契约、原生实现或产品规则才能确认。

## 8. 质量反例

- 只解释用户选中代码的“自上而下”，没找上游入口和下游消费者。
- 把 Provider 声明叫“全局变量”，不说明 ProviderContainer 和 family key。
- 说“参数传给 Provider”，但不展示参数从路由/设备选择何处产生。
- 找到 `state =` 就结束，没有找谁 watch/select 以及哪个 Widget 展示。
- 把 `setState`、Manager、缓存或直接 TQHttp 隐藏掉，伪装成纯 Riverpod 架构。
- 把 `ref.listen`、Future 完成和 Widget rebuild 写成连续同步调用栈。
- 用迁移文档目标代替当前 route/owner。
- 给旧行号、只给目录、只贴概念示例或输出敏感配置。

## 9. 停止条件

只有同时满足以下条件才算追踪完成：

- 有明确操作入口与最终可观察终点；
- 每个关键状态有定义、写入、读取、key 与生命周期；
- 数据请求有参数来源、Repository/直接网络边界、响应映射；
- 异步边界与分支没有被压成虚假的同步栈；
- Riverpod 之外的 Manager/setState/Controller/缓存已按实际链路列出；
- 关键结论均有当前路径、行号与源码证据；
- 未确认项和敏感信息边界已明确。
