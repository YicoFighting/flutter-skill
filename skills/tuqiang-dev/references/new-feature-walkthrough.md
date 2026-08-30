# 新需求实施清单（项目版）

本清单用于在途强项目新增页面、接口或跨端能力。它是决策顺序，不要求所有需求机械复制同一套目录。

## 1. 先确认 owner 和现状

- 找到所属 feature；新业务域才考虑新包；
- 先找公开 barrel/API 和已有复用入口，再搜索相邻页面、route、Provider、asset、Repository、测试和 app 注入；
- 在目标 package 内选 2–4 个成熟同类实现；命名、目录、Provider、Model、Repository、Widget 分别按 [local-style-and-reuse.md](local-style-and-reuse.md) 记录依据；
- 确认是新增、修复还是迁移，区分当前实现和迁移目标；
- 涉及路由时记录旧字符串、arguments、返回值、栈行为和 native/route effect；
- 涉及三端时记录 standard/OHOS 的依赖、override、原生能力和验证端。

## 2. 确认数据和设计来源

- 接口文档存在：按真实字段创建 endpoint、Repository、request/response Model；
- 接口未就绪：不编造 URL、字段或生产假数据；先完成抽象，UI 预览和单测使用可注入 fake；
- 有设计稿：按设计稿和现有 `core_ui` 对齐；
- 无设计稿：参考同类页面，使用实际存在的 `TQAppBar`、按钮、空态和 loading 组件；
- 新图片按 [assets-guide.md](assets-guide.md) 判断 owner、路径、倍率和 pubspec。

## 3. 按真实模块结构实现

优先沿用目标 feature 当前结构，常见组成包括 `api`、`repository`、`model`、
`state`/`controller`、`pages`/`page`、`router`、`callbacks`、`assets`。

不要为了套模板把成熟模块改成另一种目录；包外只消费公开 barrel/API，不能 import 其他 feature 的私有 `src/**`。

## 4. Model 和网络边界

```dart
factory XxxResponse.fromJson(Map<String, dynamic> json) {
  return XxxResponse(
    id: TCheck<String>(json['id']),
    count: TCheck<int>(json['count']),
  );
}
```

响应字段的 null 性和 `toJson` 是否过滤 null 由接口契约决定。请求 DTO 可以用
`required` 表达调用方必须提供的字段；不要用“所有字段可空”或“所有 null 都过滤”替代接口设计。

## 5. 状态和页面

- 沿用所在模块的 `StateNotifierProvider`、`NotifierProvider` 或其他实际模式；
- 异步操作处理 loading、success、empty、error、并发和销毁后的回调；
- UI 用 `watch` 订阅数据、`read` 调 controller、`listen` 处理副作用；
- 不在 `build` 中同步修改 Provider；Widget 创建的 Controller、FocusNode、Subscription 要释放；
- 页面尺寸遵循设计尺寸的 `.sc`，不把系统尺寸和动画参数机械转换。

## 6. 路由接入

```dart
abstract final class FeaturePetRouter {
  static const bathList = 'pet_bath_list';
  static const routeNames = <String>{bathList};
}
```

在 feature router 定义 owner，在 app 的 `AppRouters` 聚合；保持命名路由的兼容契约，
按 [routing.md](routing.md) 检查 arguments、返回值、重复 builder、nativeRouters 和 route effect。

## 7. 国际化和资源

```dart
Text('洗澡记录'.tr)
```

在 9 个语言 JSON 中使用相同中文 key：

```json
// zh_CN.json
"洗澡记录": "洗澡记录"
// en_US.json
"洗澡记录": "Bath Records"
```

不要在 Widget/State 成员里缓存会随语言变化的 `.tr` 结果。

## 8. 测试与验证

按 [testing.md](testing.md) 选择行为测试，不按文件数量机械生成。通常需要：

- Model/Repository：解析、错误和 null 语义；
- State/Notifier：成功、失败、空数据、并发和销毁；
- 路由：字符串、owner、builder、参数和返回值；
- 关键页面：用户可观察的 loading/empty/error/content 和按钮行为。

根据影响范围执行：

```powershell
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
pwsh .\tool\check_migration_boundaries.ps1
pwsh .\tool\run_migration_tests.ps1 -FlutterExecutable <path>
```

不适用或未执行的命令要在交付说明中写明。
