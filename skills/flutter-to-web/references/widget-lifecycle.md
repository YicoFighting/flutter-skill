# 组件生命周期与状态 · 前端深度对照表

> 主文档见 [../SKILL.md](../SKILL.md)。本文件展开「StatefulWidget 生命周期」部分。

## 1. 生命周期对照表

| Vue3 | React Hooks | Flutter (StatefulWidget) | 干什么用 |
|---|---|---|---|
| `setup()` | 函数体 / render | `createState()` → `initState()` | 初始化：创建 TextEditingController、挂监听 |
| `onMounted` | `useEffect(fn, [])` | `initState()` | 只跑一次的初始化 |
| `watch` 首次触发 | `useEffect(fn, [dep])` | `didChangeDependencies()` | 依赖的上游配置变了 |
| props 变化 | — | `didUpdateWidget(old)` | 父组件传了新参数 |
| `onUnmounted` | useEffect 的清理函数 | `dispose()` | **必须**释放 controller / focusNode / 订阅 |
| template + setup | render | `build()` | 描述 UI，状态一变就重跑 |

```dart
class SearchBox extends StatefulWidget { const SearchBox({super.key}); }

class _SearchBoxState extends State<SearchBox> {
  final controller = TextEditingController();      // ≈ useState('')

  @override
  void initState() {                               // ≈ onMounted
    super.initState();
    controller.addListener(() => setState(() {})); // 挂监听
  }

  @override
  void dispose() {                                 // ≈ onUnmounted，有借有还
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {             // ≈ render/template
    return TextField(controller: controller);      // v-model 的本体
  }
}
```

一句话总结：**「一个带状态的组件 = useState(initState 里建) + onMounted(挂监听) +
onUnmounted(dispose 释放) + render(build)。生命周期心智完全平移。」**

## 2. setState：最朴素的刷新

- `setState(() { count++ })` ≈ 触发 re-render。回调里只写"改数据"，别写耗时逻辑。
- 忘了包 `setState` 直接改字段 → 数据改了但页面不刷，≈ 改了个非响应式变量。
- 跨页面或业务状态交给当前产品已采用的状态 owner：Tuqiang 常见 Riverpod，Laoying 常见 ChangeNotifier Controller（见 [state-and-riverpod.md](state-and-riverpod.md)）；不要仅为套教程引入另一套状态框架。

## 3. Key 是什么

`ValueKey(item.id)` ≈ React/Vue 列表的 `:key`——告诉框架"这是同一个元素，
别整个销毁重建"。列表顺序会变、会增删时一定要给稳定 key。

## 4. context："往上找爹"的身份证

- `BuildContext` = 组件在树里的位置句柄。
- `Theme.of(context)` / `MediaQuery.of(context)` / `ModalRoute.of(context)` 全是
  "顺着组件树往上找最近的祖先拿配置" ≈ `useContext()` / inject。
- 坑：异步回调里缓存了旧 context 再用会炸；跨层级取东西优先用 provider，少靠爬树。

## 5. 自检清单（写完组件过一遍）

- [ ] 每个 `TextEditingController` / `FocusNode` / 订阅是否都在 `dispose` 成对释放？
- [ ] 异步回调回来是否判了 `mounted` 再 `setState`？
- [ ] 列表是否给了稳定的 `key`？
- [ ] build 里是否只做"数据 → UI"映射、没有副作用？
