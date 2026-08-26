# 路由规范

途强当前主要使用 Flutter 原生命名字符串路由：`Navigator.pushNamed`、
`MaterialApp.routes` 和 `onGenerateRoute`。app 通过 `AppRouters` 聚合 feature router，
不要因通用教程推荐 go_router 而主动迁移。

## 1. 新增路由

feature 定义自己的常量和 owner：

```dart
abstract final class FeaturePetRouter {
  static const bathList = 'pet_bath_list';
  static const routeNames = <String>{bathList};
}
```

app 层只做聚合和必要的兼容 alias；builder 应由唯一 owner 提供。跳转时沿用项目当前
`arguments` 约定：

```dart
final result = await Navigator.of(context).pushNamed(
  FeaturePetRouter.bathList,
  arguments: params,
);
```

接收端使用现有参数类型和安全解析方式。新代码可以使用明确的 argument wrapper 或
`TCheck`，但迁移旧路由时不能擅自把 model、Map、String 等历史参数改型。

## 2. 路由兼容契约

修改或迁移路由前记录并保持：

- 路由字符串，包括历史拼写；
- arguments 类型、必填字段和默认行为；
- `Navigator.pop` 返回值和调用方等待逻辑；
- push/replace/removeUntil 等栈行为；
- H5、scheme、push、native 入口；
- 定位刷新、退出清理、防截屏、全屏/系统栏等 route effect。

检查 feature router、`AppRouters` alias、`nativeRouters`、`FeatureRouterRegistry`
和对应 route effect 集合，禁止 feature/app 同时保留两个 builder。

## 3. 登录和跨 feature 跳转

feature 不直接 import app 私有路由或其他 feature 私有 `src/**`。登录成功、打开首页、
跨业务导航等宿主行为通过 callback/config 注入，app 负责组装；公共 barrel 只导出稳定 API。

## 4. 验证

- 普通新增路由：对应 package/app analyze，手动验证进入、带参、返回和重复进入；
- 修改既有路由：补 route contract test，检查常量、owner、builder、参数和返回值；
- 涉及 native/route effect：运行 boundary，必要时做 standard/OHOS 真机或 CI 行为验证；
- 启动出现 duplicate route 时，优先搜索所有 router、alias 和 registry，而不是删除任意一处注册。
