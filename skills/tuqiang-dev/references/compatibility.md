# 双产品三端兼容规范

仓库有两个产品、三个平台、四个宿主 target：

| 产品 | Android/iOS | HarmonyOS |
|---|---|---|
| 途强智能 | `standard` → `apps/standard` | `ohos` → `apps/ohos` |
| 老鹰在线 | `laoying_standard` → `apps/laoying_standard` | `laoying_ohos` → `apps/laoying_ohos` |

## 1. 公共代码边界

- Android/iOS 判断可沿当前 owner 使用 `Platform.isAndroid/isIOS`；
- Tuqiang app/feature 路径可沿用 bootstrap 已配置的 `AppTargetConfig.isOhos`；不存在 `Platform.isOhos`；
- Laoying 不读取 Tuqiang 的 `AppTargetConfig`，由 `laoying_standard` / `laoying_ohos` 壳把地图、扫码等平台 adapter 注入 `laoying_app`；
- OHOS-only 类型、View、package 或定制 SDK 类型只能在宿主、专属插件/adapter 或注入实现内；
- 公共 Dart 依赖抽象，端实现由对应产品宿主注入，不把任一产品的 target flag 下沉成公共判断；
- standard-only 能力要在 owner、pubspec 和调用路径明确隔离，不能默认声称三端支持。

途强沿用 Feature callback/config、Provider override 和 bridge 注册。老鹰沿用 `LY` app-local contracts、Router/Coordinator 和 infrastructure adapter；不能把途强 app composition 或品牌配置复制过去。

## 2. 依赖与产品隔离

依赖选择顺序：现有公共 core/plugin/adapter → 已验证的纯 Dart 库 → 对应 OHOS override → 新 plugin/通道。新增依赖前确认能力是否属于 Product Scope、是否进入公共路径、两个产品是否都需要，以及四个 target 的 pubspec/lockfile/原生实现影响。

两个产品的 application id、签名/凭据、URL scheme、channel/authority、后端运行时配置、品牌文案和资源必须独立。老鹰的当前范围还需以 `docs/laoying/product_scope_matrix.md`、`native_capability_matrix.md` 和 dependency allowlist 为准：地图供应商固定项、延期项和永久排除项不能因途强已有实现而越过。

## 3. 原生目录

| target | 原生工程 |
|---|---|
| `standard` | `apps/standard/android`、`apps/standard/ios` |
| `ohos` | `apps/ohos/ohos` |
| `laoying_standard` | `apps/laoying_standard/android`、`apps/laoying_standard/ios` |
| `laoying_ohos` | `apps/laoying_ohos/ohos` |

只更新需求明确影响的产品与平台；涉及公共能力时再扩到四 target。签名和本机配置文件只核对职责，不读取或复制敏感值。

## 4. 平台能力决策门

拨号、邮件、短信、商店、蓝牙面板、地图、推送、相机和后台定位等能力必须逐端确认：

- 需求是否要求 Android/iOS/HarmonyOS 同行为；
- 现有 plugin/override 是仅可编译，还是已有真机行为证据；
- 不支持时是隐藏、禁用、提示还是替代流程；
- 老鹰 Product Scope 是否批准，供应商/凭据是否就绪。

存在多种用户可见降级方式时立即询问。`canLaunchUrl` 或 package override 不能当作真机支持证明。

## 5. 验证

```powershell
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
dart run tool/project.dart analyze laoying_standard
dart run tool/project.dart analyze laoying_ohos
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope all
```

按影响缩小范围：途强用两个途强 target 与 `tuqiang` scope；老鹰用两个老鹰 target、聚焦 architecture/contract tests 与 `laoying` scope，app boundary 检查器按 [testing.md](testing.md) 排除已知基线；公共能力才跑四 target/`all`。系统交互、签名、推送、地图和 MethodChannel 还需受影响端真机或 CI，未执行项如实记录。
