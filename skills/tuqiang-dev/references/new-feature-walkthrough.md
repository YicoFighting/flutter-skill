# 新需求实施清单

## 1. 先澄清

写明目标产品、用户可观察行为和可证伪验收。新需求默认必须实现 Android+iOS+HarmonyOS；平台能力缺失导致可见降级、素材、文案、API、Product Scope、owner 或范围会改变结果且不唯一时，按 [requirement-clarification.md](requirement-clarification.md) 先问用户。

若入口属于设备列表、设备首页/详情、“更多详情/设备详情/更多设置”或离线/未激活状态卡片，先枚举所有当前 route leaf。用户未明确全部或指定设备类型时，必须先问，确认前不写代码。

老鹰需求先核对当前 `docs/laoying` Product Scope 与 API/route/resource/native contract；设计稿或途强现有功能不等于老鹰范围批准。

## 2. 找 owner 与样本

- 途强单业务放对应 `feature_*`；跨 Feature 稳定能力落到职责匹配的拆分 `shared_*`；
- 老鹰业务放 `apps/laoying_app/lib/app/auth|gps|pet|mine|overview|message|device_share|device_management`；
- 找公开入口、调用方、route、状态、Repository、asset、测试和宿主注入；
- 在同产品同 owner 采样 2–4 个成熟实现；老鹰不拿途强 Feature 页面当模板；
- 建立 [跨端、地图实现与设备页面覆盖台账](implementation-coverage.md)，每个当前可达页面/平台都有代码与验证状态；
- 一次聚焦调查后仍多解，停止实现并询问。

## 3. 数据、状态与页面

- 接口来自真实 contract；未就绪时不编造 URL/字段/成功数据，使用可注入 fake/unavailable；
- 途强沿用当前 Riverpod/Manager 模式并核对 family key、写入源、消费者和 reset；
- 老鹰沿用 `LYAppProvider`/`LYAppScope`、app-local ChangeNotifier Controller 和 Repository；
- 异步覆盖 loading/success/empty/error、generation、mounted/dispose；
- UI 沿同产品视觉体系；业务图片缺失先索要，不用 Canvas、叠字、系统图标或生成素材替代；
- i18n 按目标产品 manifest：途强当前九语言，老鹰当前 `zh_CN/en_US`。

## 4. 路由与平台

- 途强保持 Feature Router、`AppRouters`、arguments/result 和 route effect；
- 老鹰使用 `LYAppRouteRegistry`、`LYBusinessRouter` 与 typed LY payload/result；
- Android/iOS/HarmonyOS 都要有实现；Windows 上不能运行 iOS 时仍完成代码与可行静态检查，并列出 build/模拟器/真机交接；
- Tuqiang 地图需求在当前 scene 下按 Android/iOS 各三源与 HarmonyOS 华为 Map Kit 建立 7 个候选行；用户所称“花瓣地图”只作为 Map Kit 后端的业务称谓，不新增虚假的 `TQMapSourceType.petal`；某行不可达时记录 `无需修改` 与源码证据，某后端无法实现同一语义时先询问降级；
- 三端基线只作用于已确认产品；core/shared/plugin 的改动经调用证据确认同时影响两产品或公共 contract 时才扩到四 target，不能只凭文件目录扩大产品范围；产品配置、凭据、channel 和资源保持隔离。

## 5. 验证

```powershell
# 途强
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope tuqiang

# 老鹰
dart run tool/project.dart analyze laoying_standard
dart run tool/project.dart analyze laoying_ohos
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope laoying
```

老鹰业务还需在 `apps/laoying_app` 运行 analyze/test 与聚焦 architecture/contract tests；app boundary 检查器仅在与当前 allowlist 一致时作为门禁，已知基线见 [testing.md](testing.md)。core/shared/plugin 改动先枚举两产品消费者，同时影响两产品调用或公共 contract 时才使用 `-ProductScope all` 并检查四 target。每个平台、地图实现和设备页面行分别说明代码、静态/构建/运行验证；未执行的 iOS、签名、联调和真机项逐项交接。
