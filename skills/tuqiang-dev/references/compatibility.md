# 双产品三端兼容规范

仓库有两个产品、三个平台、四个宿主 target：

| 产品 | Android/iOS | HarmonyOS |
|---|---|---|
| 途强智能 | `standard` → `apps/standard` | `ohos` → `apps/ohos` |
| 老鹰在线 | `laoying_standard` → `apps/laoying_standard` | `laoying_ohos` → `apps/laoying_ohos` |

## 1. 变更类型决定平台基线

| 类型 | 最低平台范围 |
|---|---|
| Bug 修复 | Android 与 HarmonyOS 必须修复/验证；iOS 检查共享代码与专属差异，记录未运行项并交接同事 |
| 新需求 | Android、iOS、HarmonyOS 都必须实现；本机不能运行 iOS 时完成可行静态检查并交接 build/真机验证 |
| 混合变更 | 修复部分按 Bug，新行为按新需求分别关闭矩阵 |

先确定产品范围，再在该产品内执行三端基线；“三端”不等于自动同时修改 Tuqiang 与 Laoying。`standard`/`laoying_standard` 各自同时承载 Android+iOS，一次 target analyze 不能证明两个平台运行时都通过。详细状态与交接格式见 [implementation-coverage.md](implementation-coverage.md)。

## 2. 公共代码边界

- Android/iOS 判断可沿当前 owner 使用 `Platform.isAndroid/isIOS`；
- Tuqiang app/feature 路径可沿用 bootstrap 已配置的 `AppTargetConfig.isOhos`；不存在 `Platform.isOhos`；
- Laoying 不读取 Tuqiang 的 `AppTargetConfig`，由 `laoying_standard` / `laoying_ohos` 壳把地图、扫码等平台 adapter 注入 `laoying_app`；
- OHOS-only 类型、View、package 或定制 SDK 类型只能在宿主、专属插件/adapter 或注入实现内；
- 公共 Dart 依赖抽象，端实现由对应产品宿主注入，不把任一产品的 target flag 下沉成公共判断；
- standard-only 能力要在 owner、pubspec 和调用路径明确隔离，不能默认声称三端支持。

途强沿用 Feature callback/config、Provider override 和 bridge 注册。老鹰沿用 `LY` app-local contracts、Router/Coordinator 和 infrastructure adapter；不能把途强 app composition 或品牌配置复制过去。

## 3. 依赖与产品隔离

依赖选择顺序：现有公共 core/plugin/adapter → 已验证的纯 Dart 库 → 对应 OHOS override → 新 plugin/通道。新增依赖前确认能力是否属于 Product Scope、是否进入公共路径，并用真实消费者判断一个还是两个产品受影响；只有同时影响两产品调用或公共 contract 时才展开四个 target 的 pubspec/lockfile/原生实现检查。

两个产品的 application id、签名/凭据、URL scheme、channel/authority、后端运行时配置、品牌文案和资源必须独立。老鹰的当前范围还需以 `docs/laoying/product_scope_matrix.md`、`native_capability_matrix.md` 和 dependency allowlist 为准：地图供应商固定项、延期项和永久排除项不能因途强已有实现而越过。

## 4. 原生目录

| target | 原生工程 |
|---|---|
| `standard` | `apps/standard/android`、`apps/standard/ios` |
| `ohos` | `apps/ohos/ohos` |
| `laoying_standard` | `apps/laoying_standard/android`、`apps/laoying_standard/ios` |
| `laoying_ohos` | `apps/laoying_ohos/ohos` |

只更新已确认的产品，不把同名业务自动扩到另一产品；该产品内的平台范围按 Bug/新需求基线执行。涉及跨产品公共 core/shared/plugin 时再扩到四 target。签名和本机配置文件只核对职责，不读取或复制敏感值。

## 5. 平台能力决策门

拨号、邮件、短信、商店、蓝牙面板、地图、推送、相机和后台定位等能力必须逐端确认：

- 对应 Bug/新需求基线要求在哪些平台闭环，哪些仅能静态检查或交接；
- 现有 plugin/override 是仅可编译，还是已有真机行为证据；
- 不支持时是隐藏、禁用、提示还是替代流程；
- 老鹰 Product Scope 是否批准，供应商/凭据是否就绪。

存在多种用户可见降级方式时立即询问。`canLaunchUrl` 或 package override 不能当作真机支持证明。

## 6. 地图实现边界

Tuqiang 的可达地图实现按平台拆分：

- Android/iOS 标准端：百度、高德、Google；
- HarmonyOS：宿主把兼容 factory id 映射到华为 Map Kit；用户所称“花瓣地图”是业务称谓映射，不是源码 SDK 名，也不是第四个 `TQMapSourceType`；
- 修改时还要从当前枚举标注 `location`、`lineTrace`、`smartTrace`、`pointTrace`、`overview`、`fence` 等实际 map scene，公共 protocol 或 callback 变更需反查其他 scene。

Tuqiang 地图 Bug 按 Android/iOS 各自的三源与 HarmonyOS Map Kit 建立 7 个候选行后再修复适用分支；地图新需求必须让每个当前可达行具备该能力。Laoying 的供应商范围仍由 Product Scope 和两个宿主 adapter 决定，不能因为 Tuqiang 有高德/Google 就擅自接入。

## 7. 验证

```powershell
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
dart run tool/project.dart analyze laoying_standard
dart run tool/project.dart analyze laoying_ohos
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope all
```

按消费者证据选择范围：只影响途强时用两个途强 target 与 `tuqiang` scope；只影响老鹰时用两个老鹰 target、聚焦 architecture/contract tests 与 `laoying` scope，app boundary 检查器按 [testing.md](testing.md) 排除已知基线；同时影响两产品调用或公共 contract 时才跑四 target/`all`。平台行为仍按变更类型逐项记录；系统交互、签名、推送、地图和 MethodChannel 还需对应端真机或 CI，iOS 与其他未执行项如实交接。
