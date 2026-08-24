# 路由规范

项目用 **Flutter 原生命名字符串路由**（`Navigator.pushNamed`），不是 go_router。每个 feature 包自带路由常量表，app 层统一注册。

## 1. 新增页面的路由注册四步【必须全做】

以 feature_pet 新增「宠物洗澡记录」页为例：

### ① feature 包定义路由名

```dart
// src/router/feature_xxx_router.dart
abstract final class FeatureXxxRouter {
  static const petBathList = 'pet_bath_list';

  static const routeNames = <String>{
    petBathList,
    // ...原有项
  };
}
```

- 路由名小写下划线，全局唯一（建议带模块前缀防撞）；
- `routeNames` 集合要包含所有路由名（安全屏幕、位置刷新等观察者按名单工作）。

### ② app 层总表登记别名

```dart
// apps/tuqiang_app/lib/app/router/app_router.dart
class AppRouters {
  static const petBathList = FeaturePetRouter.petBathList;
  // ...
}
```

并在该文件 `MaterialApp.routes` / onGenerateRoute 的注册处把路由名映射到页面 Widget。

### ③ 跳转

```dart
Navigator.of(context).pushNamed(
  FeaturePetRouter.petBathList,
  arguments: item.toJson(),          // 传参：model.toJson()
);
```

### ④ 接收参数

```dart
final args = ModalRoute.of(context)?.settings.arguments;
final model = TqBeaconItemModel.fromJson(TCheck<Map<String, dynamic>>(args) ?? {});
```

## 2. 传参约定

- 参数一律 `Map<String, dynamic>`（model.toJson()）或简单类型；接收端 `TCheck` 安全还原；
- 返回值用 `await Navigator.pushNamed(...)` 接 `Navigator.pop(context, result)`；
- 复杂对象不要直接塞 arguments（跨路由序列化易踩坑），传 id 后在目标页查 provider/重新请求。

## 3. nativeRouters（原生容器跳转）

feature Router 类里若有 `static Map<String, String> nativeRouters`（flutter→原生页映射），新增涉及原生的路由要在其中补条目；app 层 `FeatureRouterRegistry.nativeRouters()` 会 `addEntriesChecked` 汇总各 feature——重复路由名会在启动时报错，这就是为什么路由名必须全局唯一。

## 4. 特殊路由副作用

- 需要「进入刷新位置/退出停止定位」等行为的路由，登记到 `feature_router_registry.dart` 对应集合（`_locationRefreshRoutes`、`_locationRouteExitRoutes` 等）；
- 需要防截屏的页面加进 `_screenSecureRoutes` 风格集合或 `apps/tuqiang_app/lib/app/config/app_screen_secure_config.dart`；
- 全屏视频类路由参考 `bootstrap.dart` 的 `_isFullScreenVideoRoute` 处理 SystemUi。

## 5. 登录拦截

未登录跳登录页走 `AuthRoutes.*`（feature_auth 提供）；登录成功后的跳转由 app 层 `AuthDependencies.setup(jumpToHome: ...)` 注入——feature 包内**禁止**直接 push AppRouters.home 这类 app 私有路由，反向依赖用 callbacks/config 模式（见 compatibility.md）。

## 6. 验证方式

- `dart run tool/project.dart analyze standard`；
- 真机把新页面进/出/带参/返回值四条链路各点一遍；若启动报「duplicate route」，检查路由名是否与别的模块撞名。
