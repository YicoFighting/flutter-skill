# 权限申请规范

统一入口：`core_base` 的 **`TQPermissionManager`**（`TQPermissionManager.util` 实例），配合 `core_union` 的 **`TQPermissionAlert`** 做拒绝后的引导弹窗。**禁止**业务代码直接 import `permission_handler` 自己申请。

## 1. 可申请的权限

| 方法 | 权限 |
|---|---|
| `checkLocationPermission(apply:, never:)` | 定位（含后台场景按需） |
| `checkBluePermission(...)` | 蓝牙扫描/连接 |
| `checkCameraPermission(...)` | 相机 |
| `checkPhotoAlbumPermission(...)` | 相册/媒体 |
| `checkMicroPhonePermission(...)` | 麦克风 |
| `checkNotificationPermission(apply:)` | 通知 |
| `checkPhonePermission(...)` | 电话状态 |
| `checkSystemLocationService()` | 系统定位服务开关（非权限） |
| `checkNotificationStatus()` | 通知开关状态 |
| `checkReadPasteBoardStatus()` | 剪贴板 |

返回统一枚举：

```dart
enum TQPermissionEnum { granted, denied, never, limited }
```

## 2. 标准调用模板（页面里）

```dart
import 'package:core_base/tq_permission_manager.dart';
import 'package:core_union/permission/tq_permission_alert.dart';

final _permissionAlert = TQPermissionAlert();

Future<void> _startScan() async {
  final status = await TQPermissionManager.util.checkBluePermission(
    apply: true,                                   // true = 没授权就弹系统授权框
    never: () => _permissionAlert.showBluePermissionAlert(context), // 永久拒绝引导
  );
  if (status.isgranted) {
    // 继续业务
  } else {
    TQToast.show('需要蓝牙权限才能搜索设备'.tr);
  }
}
```

规则：

- **首次进入功能页申请**，不要 App 启动时一把全申请（iOS 审核会拒）；
- `never:` 回调里必须接对应的 `TQPermissionAlert.showXxxPermission(context)`（内部弹「去设置」并跳系统设置页）；
- `denied`（用户这次拒绝）只 toast 说明用途，不反复弹系统框骚扰；
- 定位类功能先查 `checkSystemLocationService()`，服务关了引导开服务，和权限是两回事。

## 3. 平台差异集中管理

特殊平台逻辑写在 `TQPermissionManager` 内部，页面无感知，例如：

- Android 13+ 且 firebase 渠道：`shouldSkipMediaReadPermission()` 跳过媒体读权限；
- 鸿蒙端差异由 `AppTargetConfig.isOhos` 分支处理（见 compatibility.md，**不是** `Platform.isOhos`）。

若你的需求涉及新权限的平台差异：改 `TQPermissionManager`，不要在页面里写 `Platform.isAndroid` 判断权限逻辑。

## 4. 原生侧配套【新权限必查】

Dart 申请之外，原生清单也要声明，否则真机永远 denied：

- Android：`apps/standard/android/app/src/main/AndroidManifest.xml` 加 `<uses-permission>`；
- iOS：`apps/standard/ios/Runner/Info.plist` 加 `NSxxxUsageDescription`（**必须写多语言用途说明**，缺失直接闪退）；
- 鸿蒙：`apps/ohos/ohos/entry/src/main/module.json5` 的 `requestPermissions`。

三端清单同步改，漏一端就是「这端永远申请不下来」。

## 5. 验证方式

- 真机分别测试：首次申请 → 拒绝 → 再进 → 永久拒绝（设置里关）→ 引导弹窗跳设置；
- `dart run tool/project.dart analyze standard` 通过。
