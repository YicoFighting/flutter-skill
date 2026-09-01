# 完整需求追踪 Playbook

目标：从可观察操作恢复当前产品的同步调用、异步数据流、状态拓扑与 UI/插件消费，并用实时路径、行号和最小源码证据回答。用户选中代码只是锚点。

## 1. 产品与问题前置

先填：

```text
项目根：<已校验 Git root>
产品：tuqiang | laoying | cross-product
平台：Android/iOS | HarmonyOS | 全平台
事件：<启动/进入/点击/刷新/推送/native callback/session>
终点：<具体 Page/Widget/route/资源/插件/本地写入>
```

产品证据优先取 app 路径、入口调用方和路由 owner。仅凭需求中的业务名不能区分产品。产品、平台、账号/设备类型、目标资源或验收结果缺失，且会改变 owner/实现链时，停止并向用户提一个最小决策问题。

将问题改写为：

```text
当 <事件> 发生时，<输入> 如何经过 <当前产品的路由/状态/数据层>，
最终让 <可观察终点> 呈现 <结果>；失败、切换或退出时怎样处理？
```

## 2. 七段追踪

### A. 入口

找 `onTap/onPressed/onRefresh`、`initState`、首次 build gate、route/native handler、observer、Timer 或 session 事件，记录当时的 route、设备、账号、平台和资源参数。

### B. 页面与路由装配

- Tuqiang：Navigator/contract → `bootstrap.dart::getApp` override（若有）→ `AppRouters`/feature router → `AppRouters.generateRoute`/Page。
- Laoying：Navigator/LY contract → `LYAppRouter.onGenerateRoute` → `LYAppRouteRegistry`/app-local business router → Page。

查 route 常量、arguments 产生/转换/fallback、导航类型、observer/effect/security 与最终 builder。

### C. 状态拓扑

| 状态/对象实例 | 声明与类型 | key/实例来源 | 谁写 | 谁订阅/读取 | 生命周期/reset |
|---|---|---|---|---|---|

Tuqiang 分开普通 Provider、全局选择、family state、presentation、Manager/setState。Laoying分开 `LYAppProvider`、domain controller、Widget state 与 repository，不把 `notifyListeners` 写成 Riverpod rebuild。

### D. 数据与资源边界

状态/Controller → Repository/Manager/plugin/直接 HTTP；写清 UI/route/key 到请求 DTO、响应到 model/state 的转换。

资源需求还要追：实际文件 → pubspec 声明 → asset 常量/参数 → Flutter Widget 或原生插件消费。目标资源不存在时标记缺失并询问来源，不发明 Canvas、临时文件或默认替代。

只引用 API 常量名，不展示 endpoint、Token、Key、证书、签名或生产配置。

### E. 异步发布

标出 loading/success/empty/error，以及 `await/unawaited`、requestVersion/generation/mounted、pending 去重、post-frame/listener、`state =`、seed/apply/update、`notifyListeners`、Manager setter 与缓存回写。

触发 refresh 的入口与最终写状态的方法必须分开。

### F. UI/插件消费

从字段反向搜到实际 Text/Image/颜色/可见性/按钮、地图 marker、相机画面、原生参数或 loading/error/empty 分支。中间有 presentation mapper/asset selector 时一并列出。

### G. 失效与恢复

查页面离开、切 family key、controller dispose、autoDispose/keepAlive/onDispose、invalidate、语言切换与 logout/session reset。说明下次进入是复用、重建、磁盘恢复还是重请求。

## 3. 时间阶段分开

```text
同步调用：用户事件 -> 方法 -> 状态/命令入口

状态/调度：状态发布 -> listener/notifyListeners -> post-frame/刷新事件

异步数据：repository -> await HTTP/plugin -> 映射 -> 新状态

响应式消费：watch/select/ChangeNotifier/controller listener -> rebuild -> UI/插件变化
```

这些阶段不能压成“onTap -> network -> UI”的虚假同步栈。

## 4. Tuqiang family 专项

遇到 `someProvider(arg)` 必须回答：

1. provider 类型和声明；
2. arg 类型与业务来源；
3. value object 的 `==/hashCode`；
4. 同 Container 相同/不同 key 的实例隔离；
5. autoDispose、根 Host watch、keepAlive；
6. Notifier/state 的写入者与同 key 消费者；
7. invalidate 指定 key 还是整个 family；
8. 跨 shared runtime callback 是否参与。

Laoying 目标未实际使用 Riverpod 时跳过本节，改查 controller/ChangeNotifier 实例的创建、注入、监听与 dispose。

## 5. 搜索协议

```powershell
Set-Location -LiteralPath $tuqiangRoot

# 产品入口与锚点
rg -n "<方法>|<类>|<字段>|<资源常量>" <已确认产品目录> packages --glob '*.dart'

# 路由和最终 builder
rg -n "<route>|<Page>|generateRoute|onGenerateRoute|routes\(" <已确认产品目录> packages --glob '*.dart'

# Tuqiang Provider/State 或 Laoying provider/controller
rg -n "final <Provider>|<Provider>\(|<Provider>\.notifier|invalidate\(<Provider>|class LYAppProvider|class .*Controller|notifyListeners" <相关目录> --glob '*.dart'

# 数据、资源与消费
rg -n "<Repository>|TQHttp\.|ResultModel|TCheck|fromJson|<状态字段>|<资源文件名>" <相关目录> --glob '*.dart' --glob 'pubspec.yaml'

# 生命周期
rg -n "autoDispose|keepAlive|onDispose|dispose\(|invalidate\(|SessionReset|resetSession|clearForLogout" <相关目录> --glob '*.dart'
```

symbol 常见时组合目录、类型与方法，不用一次全仓宽搜替代证据链。

## 6. 证据规则

最终引用格式：

```text
<TUQIANG_ROOT>/<相对路径>:<当前行>  <symbol>
```

每个关键阶段给足以证明结论的 3–20 行片段。行号来自本次 `rg -n`/当前文件；跨文件逐个引用；不能拼接不连续代码制造调用。命名推断必须标为推断并说明缺失证据。缩小上下文以避开敏感值。

## 7. 输出结构

1. 一句话结论：产品、触发者、状态/owner、可观察终点。
2. 操作时间线：标注同步、listener/post-frame、await、rebuild。
3. 状态/对象拓扑表：定义、实例/key、写入、消费、清理。
4. 参数/资源与生命周期：family 或 controller 实例、资源来源、跨层 callback。
5. 按调用顺序的源码证据。
6. 实际涉及的产品/平台/设备/账号/loading/error 分支。
7. 已核验边界与需要用户决策/运行时/后端/原生证据的部分。

## 8. 歧义停止

出现以下情况不继续替用户推断：

- Tuqiang/Laoying 或平台选择会改变链路；
- route/owner/资源有多个合理候选；
- 验收描述与仓库现有资产/contract 不一致；
- 持续搜索仍没有唯一入口或终点，缺的是业务场景而不是 symbol。

先报告已核验事实和候选差异，再问能排除分支的最小问题。不要以“先做一个能跑的版本”为理由修改事实或默认用户选择。

## 9. 完成条件

- 根、产品、平台与可观察起终点明确；
- 关键状态/对象有定义、写入、读取、实例/key 与生命周期；
- 数据有参数来源、Repository/网络/插件边界和响应映射；
- 资源有实际文件、声明、常量与消费端，或明确标为缺失；
- 异步边界没有被压成同步栈；
- 非 Riverpod 状态按实际链路列出；
- 关键结论有当前路径、行号和源码；
- 未决策项与敏感信息边界明确。
