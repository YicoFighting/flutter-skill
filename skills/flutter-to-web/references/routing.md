# 路由导航 · 前端深度对照表

> 主文档见 [../SKILL.md](../SKILL.md)。本文件展开 §1 的「路由导航」部分。
> Flutter 世界里 `go_router` 就是 Vue Router / React Router 的亲兄弟，配置思路一模一样。

## 1. 概念对照表

| Vue Router / React Router | go_router | 大白话 |
|---|---|---|
| `createRouter({ routes })` | `GoRouter(routes: [...])` | 建一份"URL → 页面"映射表 |
| `<RouterView />` | 壳 Widget 里的嵌套内容 | 子页面渲染的占位口 |
| `path: '/detail/:id'` | `path: '/detail/:id'` | 动态段写法完全一致 |
| `route.params.id` | `state.pathParameters['id']` | 取 URL 参数 |
| `route.query.keyword` | `state.uri.queryParameters['keyword']` | 取查询串 |
| `router.push('/x')` | `context.push('/x')` | 压栈跳转（可以返回） |
| `router.replace('/x')` | `context.replace('/x')` | 替换当前页（不能返回到它） |
| `router.back()` | `context.pop()` | 返回上一页 |
| 重定向守卫 `beforeEach` | `redirect: (ctx, state) => ...` | 登录拦截：没 token 一律踢回 `/login` |
| 嵌套路由 `children` | `routes: [GoRoute(routes: [...])]` | 父子页面层级 |
| `meta.requiresAuth` | 通常直接在 redirect 里判断 | 标记哪些路由要登录 |

## 2. 完整路由表翻译示例

```dart
final router = GoRouter(
  initialLocation: '/login',                       // = 首次进入的默认页
  redirect: (context, state) {
    final loggedIn = ref.read(authProvider).loggedIn;
    if (!loggedIn && state.matchedLocation != '/login') return '/login';  // 全局守卫
    return null;                                   // null = 放行
  },
  routes: [
    GoRoute(path: '/', builder: (_, __) => const HomeScreen()),
    GoRoute(
      path: '/pet/:id',
      builder: (_, state) => PetDetailScreen(id: state.pathParameters['id']!),
    ),
  ],
);
```

大白话总结：**「这就是一份带登录守卫的路由表：`/` 到首页，`/pet/:id` 到详情页并把 URL 上的
id 传给组件。跟你在 Vue Router 写 `routes + beforeEach` 没有任何本质区别。」**

## 3. 命名路由（老项目常见）

```dart
Navigator.pushNamed(context, '/detail', arguments: pet.id);   // ≈ router.push，参数塞 arguments 里
```

老项目大量用字符串命名路由：先在 `MaterialApp.routes` / `onGenerateRoute` 注册名字，
再按名字跳转——相当于「先在路由表登记 path，才能 `push`」。新项目官方推荐 go_router。

## 4. 深链与 Web URL

go_router 天然支持浏览器地址栏和 App 冷启动直达某页（deep link），
≈ Web 里的「直接访问 /history 刷新后还能还原页面」+ App 版的分享落地页。

## 5. 常见坑速查

| 现象 | 大白话解释 |
|---|---|
| pop 之后页面数据没刷新 | 上个页面没重新 watch；回来自动刷新要用 `await context.push()` 后手动 invalidate |
| 弹窗里的 context 跳转失败 | Dialog 是另一棵子树，拿不到路由上下文；用全局 navigatorKey（= router 实例提到模块顶层） |
| Web 地址栏出现 `#/` | 默认 hash 路由策略，≈ Vue Router 的 `createWebHashHistory` |
