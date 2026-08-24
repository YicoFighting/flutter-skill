# 网络请求规范（dio / TQHttp）

项目统一用 `core_http` 封装好的 **`TQHttp`** 静态方法发请求（底层 dio，含超时、请求头、token 失效检测、日志、证书校验）。业务代码**直接调 `TQHttp`，不要自己 new Dio**。

## 1. 方法选择表

所有方法返回 `Future<ResultModel>`。按「要不要 loading / 要不要错误 toast」选：

| 场景 | 用哪个 |
|---|---|
| 普通查询，页面自己处理失败 | `TQHttp.get(url)` / `TQHttp.post(url, params: {...})` |
| 要转圈但不自动报错 | `getWithLoading` / `postWithLoading` |
| 不要转圈但失败弹 toast | `getWithErrTip` / `postWithErrTip` |
| 都要（提交类操作常用） | `getWithLoadingAndErrTip` / `postWithLoadingAndErrTip` |
| 上传图片 | `TQHttp.uploadImage(url, formData)` |
| 全自定义 | `xxxWithConfig(url, showLoading:, showErrorToast:, connectTimeout:...)` |

HTTP 动词对应：`get/post/put/delete...` 各成一套，如 `putWithLoadingAndErrTip`。

## 2. 标准调用模板（controller 里）

```dart
import 'package:core_http/core_http.dart';
import 'package:core_base/safe_utils.dart';   // 提供 TCheck

// 简单 GET
var result = await TQHttp.get(TQAddress.beaconBindNumber);
if (!mounted) return;                    // StateNotifier 里防销毁后 setState
if (result.success) {
  final map = TCheck<Map<String, dynamic>>(result.data) ?? {};
  final config = TqBeaconUpperLimitNum.fromJson(map);
  // ... 写入 state 后 _publish();
}

// 带 loading + 错误提示的 POST
var result = await TQHttp.postWithConfig(
  TQAddress.getMyBeacons,
  params: {"deviceIds": deviceIds, "macs": macs},
  showLoading: showLoading,
  showErrorToast: showErrorToast,
);
if (!mounted || generation != _beaconListGeneration) return;  // 防竞态
if (result.success) {
  final list = TCheck<List>(result.data) ?? [];
  _beaconList = list.map((e) => TqBeaconItemModel.fromJson(e)).toList();
}
```

## 3. ResultModel 与安全取值【必须遵守】

```dart
class ResultModel {
  final String? code;   // '0' 表示成功
  final String? desc;
  final dynamic data;
  bool get success => code == '0';
}
```

- 成功判断**只认 `result.success`**，不要自己解析 code。
- `data` 是 dynamic，取值一律走 `TCheck<T>(...)` 并给默认值：
  - `TCheck<String>(json['name'])`、`TCheck<int>(json['age'])`
  - 它会自动处理 int/double 互转，类型不符返回 null 而不是抛异常——这是本项目防线上崩溃的核心手段。
- 列表：`final list = TCheck<List>(result.data) ?? [];` 再 map 成 model。
- model 必须提供 `fromJson` / `toJson`；字段可空 + 默认值，参考 `tq_beacon_item_model.dart`。
- 需要错误信息时读 `result.desc`（后端文案，一般已是多语言）。

### 现代 Dart 3 模式匹配（Pattern Matching）解构响应
在复杂业务返回或多字段结构化数据中，推荐使用 Dart 3 的模式匹配解构与校验：

```dart
// 模式匹配安全解构 Map
if (result.success && result.data case Map<String, dynamic> data) {
  final count = TCheck<int>(data['totalCount']) ?? 0;
  final items = TCheck<List>(data['items']) ?? [];
  // 处理数据...
}
```

## 4. 接口地址写法

新代码优先在 feature 包内建 Endpoints 类（可测试、可注入）：

```dart
// feature_xxx/src/api/xxx_api_endpoints.dart
import 'package:shared_business/app_config.dart';

class XxxApiEndpoints {
  const XxxApiEndpoints();
  String get petBathList => '${AppConfig.iotHost}/pet/bath/list';
}
```

- 个人版接口 host 用 `AppConfig.iotHost`，企业版 `entHost`，聚合 `mergeHost`，H5 页面 `iotH5Host`。
- 存量代码里还有 `shared_business/lib/common/address.dart` 的 `TQAddress` getter 写法，改旧功能时跟随原文件风格即可。

## 5. Repository 层（接口 ≥3 个建议拆）

```dart
// feature_xxx/src/repository/xxx_repository.dart
class XxxRepository {
  XxxRepository({XxxApiEndpoints? endpoints})
    : endpoints = endpoints ?? const XxxApiEndpoints();

  final XxxApiEndpoints endpoints;

  Future<ResultModel> fetchBathList(Map<String, dynamic> params) {
    return TQHttp.postWithLoadingAndErrTip(endpoints.petBathList, params: params);
  }
}
```

## 6. 你不需要管的事（框架已处理）

- 请求头（Version/System/screctMethod、企业版 saas-ent-token 等）：`AppHttpDelegate.staticHeaders` 统一加。
- token 失效跳登录：拦截器回调 `checkInvalidToken` 自动处理。
- 日志上报：talker_dio_logger 拦截器统一记录。
- 证书校验、抓包代理开关：delegate 配置。

**禁止**在业务代码里手工塞 token 到 header 或自己处理 401。

## 7. 验证方式

- 新增接口后跑 `dart run tool/project.dart analyze standard`；
- 真机联调看 Talker 日志页确认请求/响应；
- 若改了 `core_http` 本体，standard 和 ohos 两端都要 analyze。
