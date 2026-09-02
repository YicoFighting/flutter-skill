# tuqiang-dev

当前版本：1.13.0

途强 Flutter monorepo 的开发、修复、测试与评审 Skill，覆盖途强智能与老鹰在线、Android/iOS/HarmonyOS 及 `standard`、`ohos`、`laoying_standard`、`laoying_ohos` 四个 target。

## 1.13.0 重点

- 新增强制覆盖台账，分开记录变更类型、产品、Android/iOS/HarmonyOS、宿主 target、地图实现、设备 route leaf、代码状态和验证状态；
- Bug 至少闭环 Android+HarmonyOS；iOS 共享路径与专属差异必须核查并交接，不能把 `standard` analyze 或 Android 结果写成 iOS 已验收；
- 新需求必须实现 Android+iOS+HarmonyOS；Windows 无法运行 iOS 只影响运行验证，不允许省略 iOS 代码；
- Tuqiang 地图 Bug 按 Android/iOS 各自的百度、高德、Google 与 HarmonyOS 华为 Map Kit 建立 7 个平台 × 后端候选行，地图新需求覆盖全部当前可达单元；用户所称“花瓣地图”只是 Map Kit 的业务称谓映射，不是新的 SDK 或 `TQMapSourceType` 枚举；
- 设备列表 → 详情/首页 → “更多详情/更多设置”存在多种设备页面时，用户未说明全部或指定类型就必须先枚举并询问，不能只改当前页面；
- core/shared/plugin 目录不自动代表跨产品；先查两产品真实消费者，只有同时影响两产品调用或公共 contract 时才扩到四 target 与 `ProductScope all`；
- 未显式给路径时，优先使用当前对话/任务绑定的项目或 workspace Git 根目录；统一调用 `tuqiang-project-map` 的公共 project-root-discovery，不复制固定路径或过期 identity；
- 动手前写清用户可观察行为和可证伪验收；素材、文案、API、平台、Product Scope、owner 或范围有多解时先询问；
- 一次聚焦调查后仍无法唯一实现，立即给出已确认事实、待决定问题和方案差异，不继续长时间搜索或试探性改代码；
- 途强跨 Feature 业务使用拆分后的 `shared_account/device/location/command/message/media/advertising/activity`；冻结的 `shared_business` 不再作为必需 package 或新代码 owner；
- 老鹰业务留在 `apps/laoying_app` 八个 app-local owner，沿用 `LYAppProvider`、LY Router、Repository、i18n 与资源体系，不套用途强 Feature/Riverpod 模板；
- 老鹰 Product Scope、API/route/resource/native contract 是功能范围门；设计或代码存在不等于批准；
- 缺少 S/E 等目标业务 PNG 时先索要素材，未经授权禁止 Canvas/CustomPainter/TextPainter、叠字、系统图标或生成图片替代；
- 测试、兼容性和权限按双产品、四 target 与 `-ProductScope tuqiang|laoying|all` 分流。
- 老鹰 app boundary 检查器当前仍与允许 `core_ui` 复用的最新 allowlist 冲突；修复前只作基线诊断，不作为必须全绿的验收门禁。

## 四个 Skill 分工

- `tuqiang-project-map`：根目录发现、架构事实、模块归属和源码索引；
- `flutter-to-web`：从实时源码解释事件流/数据流及 Vue3/React 等价实现；
- `tuqiang-dev`：决定产品/owner、实现、复用、风险和验证；
- `tuqiang-change-retrospective`：用户显式要求后追溯 Git 因果并生成复盘。

## 内容索引

| 文件 | 内容 |
|---|---|
| `SKILL.md` | 根目录、事实优先级、双产品架构、实施流程、四 target 与验证矩阵 |
| `references/requirement-clarification.md` | 用户可观察行为、可证伪验收、一次聚焦调查和决策门 |
| `references/implementation-coverage.md` | Bug/新需求三端基线、地图后端、设备详情强制提问、覆盖台账与 iOS 交接 |
| `references/project-structure.md` | 双产品 owner、拆分 shared、老鹰 app-local 边界与 Product Scope |
| `references/local-style-and-reuse.md` | 同产品同 owner 采样及复用/抽象决策 |
| `references/state-management.md` | 途强 Riverpod 与老鹰 LYAppProvider/ChangeNotifier |
| `references/networking.md` | TQHttp 与 LYBackendHttpClient、契约和 fail-closed |
| `references/routing.md` | 途强 Feature Router 与老鹰 LY checked registry/typed payload |
| `references/i18n.md` | 途强九语言与老鹰当前双语言独立加载 |
| `references/sizing-ui.md` | 尺寸、安全区、公共 UI 与产品视觉边界 |
| `references/assets-guide.md` | 双产品资源 owner、package asset 与缺素材禁代画规则 |
| `references/testing.md` | 按消费者证据选择 target/ProductScope、app boundary 已知基线与 migration runner 覆盖 |
| `references/permissions.md` | 双产品权限 owner、原生声明和真机验证 |
| `references/compatibility.md` | 双产品三端、宿主隔离与平台能力决策门 |
| `references/code-review-checklist.md` | 异步、类型、产品、平台、路由和资源风险 |
| `references/new-feature-walkthrough.md` | 从澄清、Product Scope、owner 到验证的实施清单 |

## 使用

```text
@tuqiang-dev
修复设备离线时详情页的客服卡片。先从设备列表入口枚举所有
deviceType/scene/cameraScene 和“更多详情”最终页面；如果我没有说明范围，
先问我是要覆盖所有设备类型还是指定类型，不要直接只改当前页面。

若涉及 Tuqiang 地图，按 Android/iOS 各三源与 HarmonyOS Map Kit 逐项关闭 7 个候选行，不可达行使用 `无需修改` 并附源码证据；Laoying 则按当前 Product Scope、宿主 adapter 与实际 scene mapping 建表；
Bug 闭环 Android+OHOS 并列出 iOS 交接，新需求则完成三端代码实现。
```

## 四 target 命令示例

```powershell
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
dart run tool/project.dart analyze laoying_standard
dart run tool/project.dart analyze laoying_ohos
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope all
```

产品范围按事实选择，平台范围按 Bug/新需求基线执行。`standard` analyze 不能证明 Android+iOS 运行时都通过；`tool/run_migration_tests.ps1` 当前不覆盖 `apps/laoying_app` 自身测试。未执行的 iOS、构建、签名、真机或 CI 必须如实说明并交接。

## 适用边界

本 Skill 与当前途强 monorepo 强绑定，但不绑定机器路径。换项目不能套用其中的 package、产品范围、路由或平台约定。未经用户明确要求，不执行 `git commit` 或 `git push`。

## 许可证

Apache 2.0 © tuqiang
