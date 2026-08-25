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
  final String? code;   // 可解析为 int 且等于 0 表示成功（'0'、'00' 均可）
  final String? desc;   // 错误信息（已自动兼容后端 desc / msg 字段）
  final dynamic data;   // 业务数据
  bool get success => /* code 安全解析为整数后 == 0 */ true;  // 实现见 core_http/result_model.dart
}
```

- 成功判断**只认 `result.success`**，不要自己解析 code；
- 失败信息优先读 `result.desc`，兼容后端 `msg` / `errorCode` 字段（fromJson 已处理）；
- `data` 是 dynamic，取值一律走 `TCheck<T>(...)` 并给默认值：
  - `TCheck<String>(json['name'])`、`TCheck<int>(json['age'])`
  - 它会自动处理 int/double 互转，类型不符返回 null 而不是抛异常——这是本项目防线上崩溃的核心手段；
- 列表：`final list = TCheck<List>(result.data) ?? [];` 再 map 成 model；
- model 必须提供 `fromJson` / `toJson`；字段可空 + 默认值，参考 `tq_beacon_item_model.dart`；
- 需要错误信息时读 `result.desc`（后端文案，一般已是多语言）。

### 响应解构范式

#### 1. 业务层标准写法（推荐）
```dart
if (result.success) {
  final data = TCheck<Map<String, dynamic>>(result.data) ?? {};
  final total = TCheck<int>(data['total']) ?? 0;
  final records = TCheck<List>(data['records']) ?? [];
  // 处理数据...
} else {
  // 失败提示兜底
  final errMsg = result.desc?.isNotEmpty == true ? result.desc! : "网络异常，请稍后重试~".tr;
  TQToast.show(errMsg);
}
```

#### 2. Dart 3 模式匹配（Pattern Matching）写法
若使用 Dart 3 模式匹配，请使用 `when` 守卫条件（避免在 `if` 括号内直接用 `&&` 混连 `case` 造成语法错误）：

```dart
// 模式匹配安全解构 Map（使用 when 守卫判断 success）
if (result.data case Map data when result.success) {
  final total = TCheck<int>(data['total']) ?? 0;
  final records = TCheck<List>(data['records']) ?? [];
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

## 6. 动态接口 vs 静态数据与 Mock 规范【必须遵守】

### ① 数据源动静判定原则
- **静态数据（Static Data）**：
  - 适用场景：纯客户端本地配置（如“关于我们”固定菜单、帮助中心固定 QA、本地协议入口、固定功能枚举）；
  - **AI 协同铁律**：AI 判定为静态数据时，**必须向用户陈述理由并请求确认**（如：*“该关于我们列表属于纯客户端固定入口，无需后端接口下发，建议作为本地静态数据内置，是否确认？”*）；确认后收敛在对应 feature 的 `src/common/` 或常量配置中，禁止零散写死在 Widget 内部。
- **动态接口（Dynamic API）**：
  - 适用场景：设备状态、用户资产、列表分页、业务表单提交等随服务端变化的数据；
  - **【严禁私自脑补假 URL】**：AI 严禁暗箱猜测或编造未提供的后端 URL 路径及入参字段。

### ② 动态接口暂缺时的标准 Mock 范式（解耦与 0 改动无缝切换）
若功能属于动态数据，但用户/后端**暂未提供真实接口**时，不得阻塞开发，必须采用 **「标准架构预留 + Repository 异步 Mock」**：

```dart
// feature_xxx/src/repository/xxx_repository.dart
class XxxRepository {
  XxxRepository({XxxApiEndpoints? endpoints})
    : endpoints = endpoints ?? const XxxApiEndpoints();

  final XxxApiEndpoints endpoints;

  /// 获取洗澡记录列表
  /// [待接入真实接口] 目前为 Mock 数据，接口就绪后替换为 TQHttp.post
  Future<ResultModel> fetchBathList(Map<String, dynamic> params) async {
    // 1. 模拟真实网络延时（500ms）
    await Future.delayed(const Duration(milliseconds: 500));
    
    // 2. 构造符合 ResultModel 规范的 Mock 字典（结构严格与 Model 一致）
    final mockMap = {
      "code": "0",
      "desc": "success",
      "data": {
        "total": 2,
        "records": [
          {"id": "1001", "petName": "旺财", "bathDate": "2026-08-25", "price": 88.0},
          {"id": "1002", "petName": "咪咪", "bathDate": "2026-08-20", "price": 66.0}
        ]
      }
    };
    
    // 3. 返回 ResultModel（UI 和 Controller 零感知）
    return ResultModel.fromJson(mockMap);
    
    /* 真实接口就绪后直接换成以下一行即可，上层 UI 与 Controller 零改动：
    return TQHttp.postWithLoadingAndErrTip(endpoints.petBathList, params: params);
    */
  }
}
```

## 7. 你不需要管的事（框架已处理）

- 请求头（Version/System/screctMethod、企业版 saas-ent-token 等）：`AppHttpDelegate.staticHeaders` 统一加。
- token 失效跳登录：拦截器回调 `checkInvalidToken` 自动处理。
- 日志上报：talker_dio_logger 拦截器统一记录。
- 证书校验、抓包代理开关：delegate 配置。

**禁止**在业务代码里手工塞 token 到 header 或自己处理 401。

## 8. 验证方式

- 新增接口后跑 `dart run tool/project.dart analyze standard`；
- 真机联调看 Talker 日志页确认请求/响应；
- 若改了 `core_http` 本体，standard 和 ohos 两端都要 analyze。
