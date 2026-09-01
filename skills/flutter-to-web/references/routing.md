# 路由导航：Tuqiang 与 Laoying 分流

> 主文档见 [../SKILL.md](../SKILL.md)。先按 [双产品上下文](product-context.md) 确认产品与 target，再解释当前源码实际使用的命名路由；只有代码确实出现 `go_router` 时才按 go_router 展开。

## 1. 先找当前产品的路由 owner

| 产品线 | App 接线 | 聚合/注册 | 参数契约 |
|---|---|---|---|
| Tuqiang | `apps/tuqiang_app/lib/app.dart` 的 `MaterialApp.routes` / `onGenerateRoute` | `AppRouters`、`apps/tuqiang_app/lib/app/router/feature_router_registry.dart` 与各 feature router | route 常量、arguments、返回值与 route effect |
| Laoying | `apps/laoying_app/lib/app.dart` 的 `LYAppRouter.onGenerateRoute` | `apps/laoying_app/lib/app/router/ly_app_router.dart`、`ly_route_registry.dart`、`LYAuthRouter` | `apps/laoying_app/lib/app/contracts/ly_route_contract.dart` 中的稳定引用、查询与 mutation result |

同名“首页、登录、GPS、设备详情”在两条产品线都有可能存在。若用户未给路径或 target，且两条路由会产生不同答案，先确认产品线和目标页面；不要默认选择熟悉的一条。

## 2. Tuqiang 命名路由

```dart
Navigator.pushNamed(context, routeName, arguments: routeArguments);
```

Tuqiang 大量使用字符串命名路由：先在 `MaterialApp.routes` / `onGenerateRoute` 注册，再由 `AppRouters` 聚合 feature router。追踪时找齐：

```text
用户入口
  → Navigator.pushNamed / AppRouters helper
  → route 常量与 arguments
  → feature router / app registry 的唯一 builder
  → ProviderScope override、route effect 或页面 Host
  → 目标 Widget
```

还要检查 `nativeRouters`、route effect、定位刷新、防截屏集合及兼容 alias 是否参与当前 route。路由字符串、参数类型、返回值和栈行为是兼容契约，不能用通用教程中的 go_router 模型覆盖真实实现。

## 3. Laoying 路由

Laoying 使用独立的 `LYAppRouter.onGenerateRoute`。它先通过 registry 判定 path，再把 bootstrap 注入的 Repository、adapter、skin controller 和 home tab coordinator 传给目标页面。

```text
用户入口 / LYBusinessRouter
  → Navigator.pushNamed + LY route path
  → LYAppRouteRegistry / LYAuthRouter
  → LYAppRouter.onGenerateRoute
  → 根据 arguments 构造页面并注入 Repository/adapter
  → 页面创建 owner Controller
```

重点核验 `ly_route_contract.dart`：当前多条业务路由刻意传稳定服务端 ID、不可变 query 或轻量 result，而不是跨路由传完整业务 Model。解释时分别说明：

- route path 的 owner；
- arguments 的准确类型及产生位置；
- 为什么目标页仍需 Repository 拉取或刷新展示数据；
- pop 返回的 mutation/navigation result 如何让上一页刷新；
- 页面/Controller 的创建与释放边界。

不得把 `LYAppRouter` 说成 `AppRouters` 的另一份 feature registry，也不得把 Tuqiang 的 route effect 集合自动套给 Laoying。

## 4. Web 心智映射

| Flutter 当前项目 | Vue Router / React Router 近似 | 非等价点 |
|---|---|---|
| route registry / route name | routes 配置中的 name/path | Flutter named route 不等于浏览器 URL |
| `Navigator.pushNamed` | `router.push` / navigate | arguments 是内存对象，不是自动序列化的 URL params |
| `RouteSettings.arguments` | route params/state | 真实类型由项目 contract 约束 |
| `Navigator.pop(result)` | 返回后由调用方处理结果 | Web router 通常没有同样的 typed pop result |
| app router 构造注入 | route element 外层 provider | Laoying 可直接把 Repository/adapter 传入页面 |

如果源码真的使用 go_router，再解释 path parameters、query parameters、redirect 和 nested routes；不要为了类比而虚构 URL、deep link 或 guard。

## 5. 路由解释检查

- [ ] 产品线、target、操作起点与目标页面已唯一确定；
- [ ] route 名/常量、发起调用、arguments、唯一 builder 与目标 Widget 已闭环；
- [ ] Tuqiang 的 AppRouters/feature registry 或 Laoying 的 LYAppRouter/contract 没有混用；
- [ ] 参数只传稳定 ID/query 还是传 Model，已由当前 contract 证明；
- [ ] 返回值、刷新、副作用、页面/Controller 生命周期已说明；
- [ ] 外部 deep link 或原生入口无法从仓库确认时已标未知。
