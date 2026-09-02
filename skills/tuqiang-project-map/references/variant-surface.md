# 平台、地图后端与设备页面变体调查

本文件用于在开发、修复或评审前恢复真实影响面。它只提供当前源码中的分支事实与检索方法，不替 `tuqiang-dev` 决定交付范围。

## 1. 先拆开五个维度

不要把“产品、平台、宿主 target、地图实现、设备类型”压成一个模糊的“受影响端”。至少分别记录：

| 维度 | 需要确认的事实 |
|---|---|
| 产品 | `tuqiang`、`laoying` 或两者 |
| 平台 | Android、iOS、HarmonyOS |
| 宿主 target | `standard`、`ohos`、`laoying_standard`、`laoying_ohos` |
| 运行时实现 | 地图后端、plugin/adapter、原生 View/Channel |
| 业务变体 | `deviceType`、`scene/category`、`cameraScene`、服务/激活/分享状态、最终 route/Page |

一个 target 可以承载多个平台，多个兼容入口也可能落到同一个平台后端。因此输出使用“候选矩阵”：设备与普通业务变体只列源码可达组合，不机械生成笛卡尔积；Tuqiang 主地图按第 3 节保留 7 个平台 × 后端候选行，不可达行统一记为 `无需修改` 并附 route、配置或实现证据。

## 2. 平台宿主事实

| 产品 | target | 平台 | 当前宿主 |
|---|---|---|---|
| Tuqiang | `standard` | Android、iOS | `apps/standard` |
| Tuqiang | `ohos` | HarmonyOS | `apps/ohos` |
| Laoying | `laoying_standard` | Android、iOS | `apps/laoying_standard` |
| Laoying | `laoying_ohos` | HarmonyOS | `apps/laoying_ohos` |

`standard` analyze/build 结果不能自动证明 Android 与 iOS 的运行时行为相同。遇到 platform channel、PlatformView、权限、资源或原生 SDK 时，继续追 Android、iOS、OHOS 各自目录。

## 3. Tuqiang 地图实现面

当前公共 Dart 选择层位于 `packages/plugins/tq_map_plugin`：

- `tq_map_enum.dart::TQMapSourceType` 当前只有 `baidu`、`google`、`gaode`；
- `TQBaseMapWidgetState.buildMapView` 分派百度、Google、高德三条 Dart 分支；
- `TQMapUseSceneType` 当前包含 location、lineTrace、smartTrace、pointTrace、overview、follow、fence、report、addDevice；一个地图需求只需覆盖实际可达 scene，但改公共 protocol/adapter 时要反查所有 scene 调用者；
- Android/iOS 的百度、高德走各自 PlatformView/native factory，Google 走 `google_maps_flutter` 控制器；
- `apps/ohos/lib/main.dart` 调用 `configureOhosMapPlatformView`，`apps/ohos/lib/map_ohos_view_host.dart` 把 BMap/AMap factory id 映射到 OHOS factory，插件 ArkTS 实现引用 `@kit.MapKit`。

POI 搜索、街景、外部地图导航等可能使用独立 channel、页面或供应商能力；主地图 Widget 的 source/backend 矩阵不能自动证明这些能力已覆盖，需求命中时另行追踪真实入口与平台实现。

因此用户所说的“花瓣地图”应在调查表中记为 **HarmonyOS 的华为 Map Kit 平台后端**。这是业务称谓到当前实现的映射，不是源码 SDK 名，也不是“已接入 Petal Maps 产品/SDK”的证明；不得凭空给 `TQMapSourceType` 增加第四个枚举值。OHOS 中仍出现 BMap/AMap factory id 是兼容分发入口，不代表运行了百度或高德原生 SDK。回答前必须实时核对这些映射是否变化。

对于支持三源的 Tuqiang 主地图 scene，默认候选台账是 7 个平台 × 后端单元：Android 百度/高德/Google、iOS 百度/高德/Google、HarmonyOS Map Kit。它们可以共享同一段 Dart 修复或测试证据，但不能因此合并平台行；某 scene 确实不可达某单元时，保留该行并给出 source、factory、route 或配置证据，代码状态记为 `无需修改`。

地图影响链至少追到：

```text
业务 Page/Widget
→ TQMapUseSceneType 与 map options/protocol
→ MapSourceManager / TQMapSourceType（标准端）
→ TQBaseMapWidgetState 分派
→ 百度/高德 native adapter 或 Google controller
→ OHOS viewType resolver / OhosView / @kit.MapKit（鸿蒙）
→ 坐标系、marker/polyline、回调、生命周期与资源消费
```

Laoying 地图必须另查当前 Product Scope、两个宿主注入和 app-local adapter。对每个实际使用的 `TQMapUseSceneType`，逐项对照 Dart 生成的 standard view id、Laoying OHOS `viewTypeResolver` 和插件真正注册的 factory；`location` 能映射不代表 `overview`、`lineTrace`、`smartTrace`、`pointTrace`、`fence` 等 scene 也已接通。代码中存在 Tuqiang 的高德/Google 实现，不等于 Laoying 已批准这些供应商。

## 4. 设备列表到详情不是一条路由

Tuqiang 当前入口 `apps/tuqiang_app/lib/app/home/device_list_page.dart::DeviceListPage._selectDevice` 在共同选择状态写入后，至少按以下条件分流；路径和 symbol 每次都要重新检索：

| 条件 | 当前分支方向 |
|---|---|
| 服务过期/设备状态异常 | 先显示续费或状态提示，可能不进入详情 |
| GPS + 基础服务未购买 | base location 页面 |
| GPS + novice mode | novice location 页面 |
| GPS + normal/person/keys/pet scene category | GPS module、人员 module、场景 module、Pet module 四类入口 |
| LBS | beacon module |
| Camera + jank/driving/parking/monitor camera scene | 独立摄像头首页或行车记录仪、停车监控、监控入口 |
| Tag | Tag location |
| 其他设备类型 | Wi-Fi/MiFi module |

入口页之后也不是统一的“更多详情”：

- `gps_module_list_page.dart::jumpToMoreDetailPage` 虽进入 GPS device detail，但可见“更多详情”可能位于另一个外层点击区域并实际进入 location；`person_module_list_page.dart` 的“更多详情”和编辑入口也指向不同页面。必须核对父子 Gesture/InkWell 的真实 hit target，不能靠方法名或文案猜 route；
- base/novice location 页、Pet callback 可能以不同参数进入 GPS 详情，MiFi、Beacon、Camera、Tag 则有自己的页面族；
- `DeviceListPage._openDeviceMoreSettings` 还会按 `cameraScene` 分到 monitor setting、GPS remote setting、driving record setting，其他类型才走通用 more settings；
- `feature_device_management` 的设备搜索/选择入口也存在同类设备分流，并经 app bootstrap 注入最终导航；修改设备列表入口时必须反查其他选择入口，不能只改 `_selectDevice`；
- 离线客服卡片当前分别出现在 GPS、person、scene、Pet、Wi-Fi/MiFi 页面，说明“相同 UI 需求”可能由多个页面 owner 独立消费同一组件。

所以页面名、用户文案或当前打开文件只能作为锚点。必须从设备列表点击开始，沿每个可达 route 追到实际 Page，再从“更多详情/设备详情/更多设置”等事件继续追一层，不能在第一个命中页面停止。

## 5. 调查步骤

1. 从真实入口枚举 `deviceType`、scene/category、cameraScene、服务/激活/分享状态分支。
2. 对每个候选查 route 常量、arguments、composition callback、最终 builder 与 Page。
3. 在最终 Page 搜目标 Widget、文案、状态字段、公共组件和同语义实现，不只搜用户当前给出的文件。
4. 地图任务再给每个 Page 标注 map scene；Tuqiang 默认展开 Android/iOS 各三源与 OHOS Map Kit 的 7 个候选单元，Laoying 按当前 Product Scope 与宿主 adapter 展开。
5. 对每个候选标为“可达”“不可达（证据）”“待用户确认”；把会改变修改范围的设备类型歧义交给 `tuqiang-dev` 决策门。

推荐输出：

| 产品 | 平台/target | 设备/scene | 入口 → 最终 Page | 地图 scene/后端 | 可达证据 | 待决项 |
|---|---|---|---|---|---|---|

## 6. 实时核验命令

```powershell
Set-Location -LiteralPath $tuqiangRoot

# 设备入口、详情与二级详情
rg -n "_selectDevice|_openDeviceMoreSettings|deviceType|cameraScene|sceneCategory" apps/tuqiang_app/lib/app/home/device_list_page.dart
rg -n "selectAction|DeviceSearchPage|setModelFromList" packages/feature/feature_device_management apps/tuqiang_app/lib/bootstrap.dart --glob '*.dart'
rg -n "更多详情|设备详情|更多设置|jumpToMoreDetail|openDeviceDetail|DeviceDetail" apps packages --glob '*.dart'
rg -n "TQOfflineCustomerServiceCard|isCustomerServiceAvailableProvider" apps packages --glob '*.dart'

# 地图 source、scene、宿主和平台后端
rg -n "enum TQMapSourceType|enum TQMapUseSceneType|buildMapView|MapSourceManager" packages/plugins/tq_map_plugin/lib --glob '*.dart'
rg -n "TQMapUseSceneType\.|TQMapViewFactoryId|configureOhosMapPlatformView|resolveOhosMapViewType" apps packages --glob '*.dart'
rg -n "@kit.MapKit|MapComponent" packages/plugins/tq_map_plugin/ohos apps/ohos --glob '*.ets' --glob '*.ts'

# 每个最终 route/Page 的真实 builder 和消费者
rg -n "<route>|<Page>|<Widget>|<状态字段>" <已确认产品目录> packages --glob '*.dart'
```

## 7. 完成条件

- 平台与 target 已拆开，未用一次 `standard` 检查代表 Android+iOS 运行时；
- Tuqiang 地图任务已按 Android/iOS 各三源与 HarmonyOS Map Kit 展开 7 个候选单元，不可达行使用 `无需修改` 并附源码证据；已标明实际 map scene；Laoying 未被套用 Tuqiang 供应商矩阵；
- 设备任务已列出所有当前可达叶子或给出不可达证据，未把一个详情页当作全部设备实现；
- 命中设备选择/详情族且存在两个以上 route/Page 或页面消费叶子时，若设备范围未明确，已把候选矩阵返回给开发 Skill 请求用户决定；没有用共享组件或当前页面替代范围确认。
