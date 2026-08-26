# 网络请求规范（dio / TQHttp）

业务代码优先使用 `core_http` 的 `TQHttp`，不要在 feature 内自行创建 Dio。先查看同类模块实际使用的 loading、错误提示和超时配置。

## 1. 方法选择

| 场景 | 常用方法 |
|---|---|
| 页面自行处理结果 | `get` / `post` / 对应 HTTP 动词 |
| 自动 loading | `getWithLoading` / `postWithLoading` |
| 自动错误提示 | `getWithErrTip` / `postWithErrTip` |
| 两者都要 | `getWithLoadingAndErrTip` / `postWithLoadingAndErrTip` |
| 需要精细配置 | `xxxWithConfig` |
| 上传图片 | `uploadImage` |

## 2. 响应边界

`TQHttp` 返回 `ResultModel`。成功判断使用 `result.success`，不要在业务层重复解析 code；错误文案优先使用 `result.desc`。因为 `result.data` 是动态值，进入业务模型前使用 `TCheck<T>` 或明确 parser 收窄：

```dart
final result = await TQHttp.get(TQAddress.beaconBindNumber);
if (!mounted) return; // StateNotifier 的生命周期判断；Widget 要判断自己的 mounted

if (result.success) {
  final map = TCheck<Map<String, dynamic>>(result.data);
  if (map != null) {
    final item = TqBeaconUpperLimitNum.fromJson(map);
    // 发布到新的 State
  }
} else {
  TQToast.show(result.desc?.isNotEmpty == true
      ? result.desc!
      : '网络异常，请稍后重试'.tr);
}
```

列表也要在边界处检查元素类型，再交给 `fromJson`；不要把不可信的 `List<dynamic>` 直接传入业务层。

## 3. Model 规则

- Model 只表达接口业务数据，不放页面标题、按钮文案等 UI 内容；
- 响应 Model 是否可空由接口契约决定，不能为了套模板把必填字段全部改成 nullable；请求 DTO 可以使用 required/default 表达调用方约束；
- `fromJson` 负责处理缺失字段、类型转换和兼容字段，优先使用 `TCheck<T>`；
- `toJson` 是否省略 null 由接口契约决定。部分更新接口需要省略 null，清空字段的接口可能需要显式发送 null，不能一刀切；
- 集合和嵌套结构要保持明确类型，必要时提供独立 parser。

```dart
factory XxxResponse.fromJson(Map<String, dynamic> json) {
  return XxxResponse(
    id: TCheck<String>(json['id']),
    count: TCheck<int>(json['count']),
  );
}

Map<String, dynamic> toJson() => {
  if (id != null) 'id': id,
  if (count != null) 'count': count,
};
```

上面的 null 过滤只是“接口允许省略时”的例子；新增接口前先确认后端的 null 语义。

## 4. Endpoint 与 Repository

新 feature 的 endpoint、Repository 和 Model 放在真实 owner 包内。接口地址来自需求、后端文档或现有 `TQAddress`，禁止凭空编造 URL 和字段。

```dart
class XxxRepository {
  XxxRepository({XxxApiEndpoints? endpoints})
      : endpoints = endpoints ?? const XxxApiEndpoints();

  final XxxApiEndpoints endpoints;

  Future<ResultModel> fetchItems(Map<String, dynamic> params) {
    return TQHttp.postWithLoadingAndErrTip(
      endpoints.items,
      params: params,
    );
  }
}
```

Repository 只有在存在明确的接口边界、注入需求或多个 API 时才需要额外抽象，不要为一个简单请求堆空壳层。

## 5. 接口未就绪时

- 不编造真实 URL、字段或“成功”响应；
- 可以先完成 Model/Repository 接口和明确 TODO；
- UI 预览或单测需要数据时，把 fake repository 通过构造函数或 Provider override 注入测试/预览环境；
- 不把 `Future.delayed` 假数据作为默认生产实现；
- 真实接口接入后仍需验证 loading、错误、重试、重复请求和页面销毁后的回调。

## 6. 生命周期和安全

- 跨 `await` 更新 Widget 前判断 Widget `mounted`；Notifier 使用自身的 `mounted`，不要混淆；
- 高频请求用 generation、请求 id 或取消机制防止旧响应覆盖新状态；
- 统一复用项目 token、header、401 和日志拦截器，不在业务代码手工塞 token；
- 日志使用项目日志封装并脱敏，不记录密码、token、完整手机号或生产配置。

## 7. 验证

- 改 feature 网络代码：对应 package analyze + 聚焦测试；
- 改 `core_http`、shared 或公共 Model：standard/OHOS analyze，并按影响运行 migration tests；
- 新增接口参数或响应契约：补 Model/Repository 测试，必要时做真实端联调；
- 命令和未执行项目按 [testing.md](testing.md) 的验证矩阵如实记录。
