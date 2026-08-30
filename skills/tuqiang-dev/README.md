# tuqiang-dev

当前版本：1.11.0

途强三端 Flutter monorepo 的专属开发、修复、测试与评审 Skill。它通过 `tuqiang-project-map` 的动态 `<TUQIANG_ROOT>` 协议核验当前 checkout，再按当前源码、目标 package 的局部风格、边界测试、统一工具和 CI 做最小可验证修改。

## 这次强化了什么

- 不再绑定任何机器路径；`<TUQIANG_ROOT>` 只代表本次任务已核验的仓库根目录；
- 项目地图提供架构事实和源码索引，`tuqiang-dev` 独立负责 owner、复用、实现和验证决策；
- 动手前先定位正确层级、公开 barrel/API 与已有复用入口；
- 在目标 package 内抽样 2–4 个成熟同类实现，分别沿用 Provider、Model、Repository、Widget 的局部主流写法；
- 样本冲突时优先当前 owner 中较新且有调用方或测试的模式，并记录依据；不借需求统一存量命名、目录或状态架构；
- 复用语义一致的现有能力，但不为复用制造透传 wrapper、mode flag 或投机性公共抽象；
- 以高内聚、低耦合和最小影响面约束实现，并通过 diff、调用方、测试和边界门禁验证；
- 修改 Riverpod 前必须追完整影响链，不再只看选中 Provider 或 Widget；
- 明确 family 参数是 Provider 实例 key，检查参数来源、不可变性、`==/hashCode` 和状态隔离；
- 全仓核验全部写入源与 `watch/select/read/listen` 消费端；
- 检查根 Host 对 autoDispose family 的实际保活、`keepAlive/onDispose`、切设备和 session reset；
- 把 Manager/单例、Notifier 可变字段、`setState`、`ValueNotifier`、Timer、插件回调纳入状态图；
- 跟踪 ProviderScope override 的 contract 声明、App 注入与 Feature 调用，保持跨 Feature 依赖方向；
- 国际化基础能力留在 `core_i18n`，各 Feature/shared owner 暴露自身缓存清理入口，App 的 `LanguageChangeCoordinator` 只做跨 Feature 聚合与顺序编排；
- 项目架构、模块和真实业务流从 [`tuqiang-project-map`](../tuqiang-project-map/) 按需读取，避免在开发规范里重复一整套静态事实。

## 三个 skill 的分工

- `tuqiang-project-map`：提供动态根目录解析、架构、模块职责、源码索引和端到端业务事实；
- `flutter-to-web`：用金字塔结构、实时源码和 Vue3/React 代码解释业务链；
- `tuqiang-dev`：决定改哪里、怎么改、三端风险和如何验证。

兄弟项目地图未安装时，本 skill 仍按同一协议从用户路径、选中/目标文件或当前 workspace 的 Git 根目录解析并校验 `<TUQIANG_ROOT>`；无法唯一确认时先请求确认，不扫描磁盘或猜测 checkout。

## 内容索引

| 文件 | 内容 |
|---|---|
| `SKILL.md` | 事实优先级、架构边界、修改前影响链、三端规则、统一命令与验证矩阵 |
| `references/project-structure.md` | owner、依赖方向与迁移边界 |
| `references/local-style-and-reuse.md` | 局部风格采样、复用/抽象/内联决策与可验证检查 |
| `references/state-management.md` | Riverpod 类型、family、完整读写图、生命周期与 session reset |
| `references/networking.md` | TQHttp、ResultModel、TCheck、Model/Repository 边界和 fake 注入 |
| `references/routing.md` | 命名路由、Feature owner、native route 与 route effect |
| `references/i18n.md` | `.tr/keyTr/multiKeyTr`、9 语言 JSON 与切换清理 |
| `references/sizing-ui.md` | `.sc`、SafeArea、core_ui 与布局 |
| `references/assets-guide.md` | 设计源、资源 owner、package asset 与倍率目录 |
| `references/testing.md` | 单测、Widget/contract test 与 migration runner |
| `references/permissions.md` | 权限与永久拒绝处理 |
| `references/compatibility.md` | Android/iOS/OHOS 边界与插件选择 |
| `references/code-review-checklist.md` | 异常、异步、类型、平台、资源、路由和状态风险 |
| `references/new-feature-walkthrough.md` | 从需求、owner 到验证的最小实施清单 |

## 使用

```text
@tuqiang-dev
修复切换设备后 GPS 页面短暂展示上一台设备状态的问题。先追 family key、
全部状态写入源、根 Host 保活和 session/reset，再做最小修改并运行相关验证。
```

## 统一命令示例

```powershell
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
pwsh .\tool\check_migration_boundaries.ps1
```

完整构建/测试范围按修改风险选择；未执行的真机、签名、CI 或 OHOS 步骤必须如实说明。

## 安装

推荐安装整个仓库：

```bash
/plugin marketplace add tuqiang/flutter-skill
```

或单独复制：

```bash
cp -r skills/tuqiang-dev ~/.codex/skills/
```

## 适用边界

本 Skill 与途强 monorepo 强绑定，但不绑定机器路径。`<TUQIANG_ROOT>` 必须先按项目地图的根目录发现协议解析并核验；换一个 Flutter 项目不要直接套用其中的 package、命令、路由或平台约定。

未经用户明确要求，不执行 `git commit` 或 `git push`。

## 许可证

Apache 2.0 © tuqiang
