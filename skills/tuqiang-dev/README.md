# tuqiang-dev

当前版本：1.12.0

途强 Flutter monorepo 的开发、修复、测试与评审 Skill，覆盖途强智能与老鹰在线、Android/iOS/HarmonyOS 及 `standard`、`ohos`、`laoying_standard`、`laoying_ohos` 四个 target。

## 1.12.0 重点

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
| `references/project-structure.md` | 双产品 owner、拆分 shared、老鹰 app-local 边界与 Product Scope |
| `references/local-style-and-reuse.md` | 同产品同 owner 采样及复用/抽象决策 |
| `references/state-management.md` | 途强 Riverpod 与老鹰 LYAppProvider/ChangeNotifier |
| `references/networking.md` | TQHttp 与 LYBackendHttpClient、契约和 fail-closed |
| `references/routing.md` | 途强 Feature Router 与老鹰 LY checked registry/typed payload |
| `references/i18n.md` | 途强九语言与老鹰当前双语言独立加载 |
| `references/sizing-ui.md` | 尺寸、安全区、公共 UI 与产品视觉边界 |
| `references/assets-guide.md` | 双产品资源 owner、package asset 与缺素材禁代画规则 |
| `references/testing.md` | 四 target、ProductScope、app boundary 已知基线与 migration runner 覆盖 |
| `references/permissions.md` | 双产品权限 owner、原生声明和真机验证 |
| `references/compatibility.md` | 双产品三端、宿主隔离与平台能力决策门 |
| `references/code-review-checklist.md` | 异步、类型、产品、平台、路由和资源风险 |
| `references/new-feature-walkthrough.md` | 从澄清、Product Scope、owner 到验证的实施清单 |

## 使用

```text
@tuqiang-dev
非中文地图起终点需要显示 S/E。先检查是否已有目标 PNG 和语言选择契约；
若素材缺失，请列出所需文件并等我提供，不要用 Canvas 或文字叠加替代。
```

## 四 target 命令示例

```powershell
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
dart run tool/project.dart analyze laoying_standard
dart run tool/project.dart analyze laoying_ohos
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope all
```

完整范围按风险选择。`tool/run_migration_tests.ps1` 当前不覆盖 `apps/laoying_app` 自身测试；未执行的构建、签名、真机或 CI 必须如实说明。

## 适用边界

本 Skill 与当前途强 monorepo 强绑定，但不绑定机器路径。换项目不能套用其中的 package、产品范围、路由或平台约定。未经用户明确要求，不执行 `git commit` 或 `git push`。

## 许可证

Apache 2.0 © tuqiang
