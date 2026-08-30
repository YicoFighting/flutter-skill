# 完整业务链追踪与讲解模板

> 主入口见 [../SKILL.md](../SKILL.md)。先按 [动态项目根目录协议](project-root-resolution.md) 解析 `<TUQIANG_ROOT>`。本文件把“选中代码”扩展成可核验的端到端业务链，适合完整需求、Riverpod 状态来源/去向、页面进入或点击事件分析。

## 1. 先画三条链，不要伪造一条连续调用栈

Flutter + Riverpod 的异步流程通常分为：

```text
事件/同步调用链
用户操作 → Widget 回调 → Command/Notifier → Repository/Plugin 调用

异步数据链
请求发出 → await 返回 → DTO/Model 转换 → State/缓存写入

状态依赖/重建链
Provider 通知 → derived Provider 重算 → Widget/ref.listen → 重建或副作用 → 字段展示
```

`await` 之后以及 Provider 通知阶段不等于仍处于最初点击回调的同步栈帧。回答中分别列出三条链，再用时间顺序把它们拼成业务闭环。术语第一次出现时立即补上 Vue3/React 心智，例如把 `ref.listen` 先解释为类似 `watch`/effect 的副作用订阅，再说明 Riverpod 的真实语义。

## 2. 从锚点向四个方向搜索

### 向上：谁让这段代码运行

- 路由常量、builder owner、`Navigator.pushNamed`；
- `onTap/onPressed/onChanged`；
- `initState/didChangeDependencies/didPush/didPopNext`；
- `ProviderScope` override 与 app composition callback；
- Timer、推送、原生/插件回调。

### 向下：数据最终来自哪里

- Provider 的 builder/build；
- Notifier/Command 方法；
- Repository/Service；
- `TQHttp`、数据库、缓存、Manager 或插件边界；
- Model/DTO 的解析和字段映射。

### 向旁：还有谁写同一份数据

全仓搜索 Provider 名、Notifier 类型、State 字段和更新方法，重点看：

```text
state =
copyWith(
.notifier).
seed / apply / update / refresh
ref.invalidate
setState / ValueNotifier
Manager / cache 写入
```

先区分两类命中：

- **直接写入者**：真正执行 `state =`、`apply/seed/update`、Manager/cache setter 或局部状态赋值；
- **触发入口**：页面、Timer、listener、RouteObserver 等只调用 `refresh/load/request`，最终仍汇合到直接写入者。

同一状态可能同时由页面首次加载、手动刷新、轮询、推送或其他命令回填；只讲一条会让因果关系失真。触发入口只展开与当前用户操作相关的部分，其余按来源分类列索引，避免把几十个重复 `.refresh()` 调用混成几十个状态 owner。设备/GPS 是这种多写入源的一个领域案例，不是默认讲解对象。

### 向外：谁消费并展示

分类记录：

- `ref.watch`：响应式订阅；
- `ref.watch(provider.select(...))`：字段级订阅；
- `ref.listen` / `ProviderContainer.listen`：副作用；
- `ref.read` / `ProviderContainer.read`：一次性快照或命令；
- Manager/cache getter：非 Riverpod 真正数据源；
- `Text/Image/Switch/Map` 等最终 Widget。

## 3. 检索顺序

默认用 `rg`，先符号后路径：

```powershell
rg -n "目标Widget|目标方法|目标Provider" "<TUQIANG_ROOT>"
rg -n "目标Provider\(" "<TUQIANG_ROOT>/apps" "<TUQIANG_ROOT>/packages"
rg -n "state\s*=|copyWith\(|seed\(|apply[A-Z]|invalidate\(" <相关目录>
rg -n "watch\(|read\(|listen\(|select\(" <相关目录>
```

随后逐行读取命中位置上下文。不要用静态 reference 的旧行号直接回答；不要优先展开生成文件。本项目当前未使用 Riverpod codegen，若未来出现 `.g.dart`，先展示手写声明或注解，只有生成层本身影响问题时才下钻。

## 4. Provider 身份卡

每个关键 Provider 至少输出：

| 项目 | 必答问题 |
|---|---|
| 声明 | 绝对路径、实时行号、完整泛型 |
| 实例身份 | 普通 Provider 还是 family；family key 是什么、从哪来 |
| 相等性 | 对象 key 是否不可变，`==/hashCode` 是否按业务值实现 |
| State | 初始值、关键字段、loading/error/data 表达 |
| 写入者 | Notifier/Command/回调/其他旁路 |
| 依赖 | builder 中 watch/read 哪些 Provider/Repository |
| 消费者 | watch/select/listen/read 各自在哪 |
| 生命周期 | autoDispose、根 Host 订阅、keepAlive、onDispose |
| 清理 | 切 key、显式 invalidate、切语言、登出 reset |

必须区分：

```text
路由参数       只传导航上下文
family 参数    决定 Provider 实例/缓存身份
方法参数       控制某一次 action
State 字段     请求后留存并供消费者读取的数据
```

## 5. 字段血缘表

不要只说“接口数据进了 Provider”。对用户关心的 UI 字段逐列追踪：

| 最终 UI | Presentation/getter | State/缓存字段 | Model/DTO | Repository/外部来源 |
|---|---|---|---|---|
| 例：列表数量 | `visibleCount` | `catalog.items` | 列表响应 | Repository/缓存回填 |

若 Presentation State 只存 revision、真实值在 Manager/cache，必须在表里写出这条旁路，不得误称数据存于 Provider。

## 6. 源码证据规格

完整链路至少给出六类证据，并让每个关键跳都能由相邻证据连接：

1. 页面/路由/事件入口；
2. Provider 声明与 family key；
3. Notifier/Command 的核心写入；
4. Repository、缓存或插件边界；
5. derived/presentation Provider；
6. 最终 UI 消费。

格式示例：

```text
<TUQIANG_ROOT>/packages/.../some_provider.dart:42
```

```dart
// 只摘录能证明本次跳转或写入的必要上下文
```

单段源码保持短小，但不能用一个总行数上限删掉关键阶段。长方法可拆成多个命名片段，中间用文字说明未展示的低价值分支。路径与行号来自本次检索；最终回答应使用解析后的绝对路径，也可在统一声明 `<TUQIANG_ROOT>` 后用该占位符缩写。

## 7. Vue3 对照必须覆盖整条链

```ts
// keyed Map ≈ family：每个 entityId 一份状态
const details = reactive(new Map<string, DetailState>())

async function refresh(entityId: string) {
  const previous = details.get(entityId)
  details.set(entityId, { ...previous, refreshing: true })
  const result = await repository.fetchDetail(entityId)
  details.set(entityId, { result, refreshing: false })
}

const active = computed(() =>
  selectedId.value ? details.get(selectedId.value) : undefined,
)
```

要继续补上真实事件入口、route/props 参数来源、`watch` 副作用、模板消费和卸载/切 key 清理；名称、字段及 loading/error/empty 分支与本次 Dart 源码对应，不能只写一个 `computed` 就结束。

## 8. React 对照必须覆盖整条链

```tsx
function DetailPanel({ entityId }: { entityId: string }) {
  const detail = useEntityStore(s => s.byId[entityId])

  useEffect(() => {
    const controller = new AbortController()
    void refreshEntity(entityId, controller.signal)
    return () => controller.abort()
  }, [entityId])

  return <span>{detail?.title}</span>
}
```

要补上真实事件入口、route/props 参数来源、状态写入、selector/effect 和最终组件消费。说明 query key/store key 与 Riverpod family key 的近似关系，以及 React cleanup、AbortController 与 Riverpod `autoDispose/onDispose/generation` 的差异。

## 9. 输出骨架

```markdown
## 一句话结论

## 1. 用户操作与入口

## 2. 事件/同步调用链

## 3. 异步数据链

## 4. 状态依赖与 UI 重建链

## 5. Provider/状态身份与参数

## 6. 逐跳源码证据

## 7. 字段如何落到 UI

## 8. Vue3 端到端等价实现

## 9. React 端到端等价实现

## 10. 生命周期、并发与清理

## 11. 已证实、推断与未知边界
```

## 10. 完成条件

- 起点是用户可感知操作，而非任意被选代码；
- 一端追到 UI，另一端追到 API、缓存、数据库或插件；
- family 参数来源、相等性、状态隔离和生命周期说清；
- 同一状态的所有可发现写入源均列出；
- 明确哪些读取会重建、哪些只是快照、哪些是副作用；
- 真实 Dart、Vue3、React 三套代码覆盖同一条完整业务链并能逐段对照；
- 每个关键事实有实时路径/行号，未知部分不猜；
- endpoint、Token、密钥、证书与生产配置已脱敏。
