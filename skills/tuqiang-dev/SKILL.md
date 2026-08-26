---
name: tuqiang-dev
version: 1.9.0
description: 为 D:/Code/tuqiang Flutter monorepo 提供项目事实、三端边界、包归属、命令入口和风险分级验证规范；适用于在该仓库解释、修改、测试或评审代码。
---

# 途强 Flutter 项目开发规范

本 skill 只服务 D:/Code/tuqiang。目标是让 AI 在真实项目结构中做最小、可验证、三端可控的修改，不把迁移目标、通用 Flutter 教程或一次性个人偏好当成绝对规则。

## 1. 事实来源与项目边界

遇到冲突时按以下顺序判断：

1. D:/Code/tuqiang/AGENTS.md、当前源码、各 package 的 pubspec.yaml；
2. tool/project.dart、tool/check_migration_boundaries.ps1、tool/run_migration_tests.ps1 和 CI；
3. docs/ 中与当前迁移批次对应的文档；
4. 本 skill 的 references；
5. 通用 Flutter 最佳实践。

如果“当前代码”和“迁移目标”不一致，先按当前 owner 和相邻成熟模块实现；只有用户明确要求迁移时，才执行迁移目标的清理规则。apps/tuqiang_app 中尚未迁出的历史业务代码不应被伪装成新代码模板。

## 2. 项目事实速查

```text
apps/standard       Android + iOS 入口，Flutter 3.35.7
apps/ohos           HarmonyOS 入口，custom_3.35.7_ohos
apps/tuqiang_app    共享业务 App 包，pubspec name: tuqiang
packages/core       core_base / core_http / core_i18n / core_ui 等基础包
packages/feature    feature_auth / feature_pet / feature_gps / ... 业务包
packages/shared     shared_business 跨模块业务层
packages/plugins    tq_* 自研插件及原生实现
packages/adapter    部分三方库的平台适配封装
packages/assets_common 公共静态资源
```

依赖方向原则为 apps → feature → shared/core/plugins/adapter；shared_business 不反向依赖 feature。新代码应放在真正的业务 owner 包中，不能因为调用方便就放回 app 或 shared。

## 3. 命令入口

App 的 pub get、analyze、run、build 必须走统一入口，避免选错 SDK、渠道或 HarmonyOS 配置：

```powershell
dart run tool/project.dart pub-get standard --enforce-lockfile
dart run tool/project.dart analyze standard
dart run tool/project.dart pub-get ohos --enforce-lockfile
dart run tool/project.dart analyze ohos
dart run tool/project.dart run standard
dart run tool/project.dart build standard apk --debug
dart run tool/project.dart build ohos hap --debug
```

`dart run tool/project.dart test <target>` 只是对对应 app 目录执行 Flutter test，不是完整迁移测试。完整迁移测试使用：

```powershell
pwsh .\tool\run_migration_tests.ps1 -FlutterExecutable <对应端 Flutter 可执行文件>
```

`tool/check_migration_boundaries.ps1` 是架构红线检查；本地优先使用 PowerShell 7（pwsh）。如果 Windows PowerShell 5.1 因无 BOM UTF-8 解析失败，必须把边界检查标记为未执行，不能用 analyze 结果冒充通过。

## 4. 不可突破的三端边界

- 公共 Dart 代码不得出现 Platform.isOhos、OhosView、*_ohos 专属包名或定制 SDK 独有类型。
- HarmonyOS 差异通过 AppTargetConfig.isOhos、adapter、公共抽象、callback、bridge 或 app 启动注入隔离。
- 新增依赖先检查 apps/ohos/pubspec.yaml 的 override、packages/adapter、packages/core/*_ohos、packages/plugins 和已有 core 能力。
- 标准端和 OHOS 端可以有不同 lockfile。依赖变更时按实际影响更新对应 lockfile，并检查 diff，禁止无关漂移。
- standard-only 插件不自动意味着必须补 OHOS 实现；先查插件清单和调用场景。若公共能力确实需要 OHOS，才补原生实现和行为验证。

## 5. “加东西放哪里”决策

- 页面、Controller、State、Model、Repository、路由、业务资源：放所属 packages/feature/feature_xxx。
- 跨两个及以上 feature 且语义稳定的模型、Provider、manager：才考虑 packages/shared/shared_business。
- 网络、i18n、尺寸、通用 UI、权限工具：优先复用 packages/core/core_*。
- 原生通道或平台能力：优先现有 packages/plugins/tq_* / packages/adapter。
- apps/tuqiang_app/lib/app/** 负责启动编排、路由聚合、session、平台注入和共享 App 壳。已有历史页面可以暂留，但新建可复用业务页面不要继续堆入 app。
- feature 内部目录不是固定脚手架。先看同一 feature 的 owner、barrel、router、state 和测试，再沿用相邻成熟模块结构。

详细归属规则见 [references/project-structure.md](references/project-structure.md)。

## 6. 变更工作流：按风险验证

1. 搜索同类实现、调用方、pubspec、测试、路由 owner 和平台注入点。
2. 写出最小变更范围和可证伪验收标准；只有存在业务歧义、架构选择或高风险外部影响时才向用户确认。
3. 设计稿可用时按设计稿和实际 core_ui 对齐；没有设计稿时沿用同类页面，不因设计工具不可用阻塞普通功能。
4. 动态接口未提供时不得编造 URL 或生产假数据；需要 UI 预览或单测时使用可注入 fake repository。
5. 行为变化和实现一起补验证；不要求每改一个文件就机械配一个测试文件。
6. 只修改直接相关文件，保留用户已有改动，不做 drive-by 重构、无关格式化或未经要求的依赖升级。

## 7. 验证矩阵

| 变更范围 | 最低验证 |
|---|---|
| 文档/注释/纯格式 | git diff --check，确认无误改编码 |
| 单个 feature 的 Dart 逻辑 | 对应 package analyze + 相关单测 |
| route / asset / package 边界 / i18n manifest | boundary script + 对应 contract/解析测试 |
| core、shared、公共插件或依赖 | analyze standard + analyze ohos + boundary；必要时 migration tests |
| 权限、原生通道、OHOS override、系统能力 | 上述静态验证 + 受影响端行为/真机验证 |
| App 构建、渠道、签名、DevEco 配置 | 走 tool/project.dart，并记录未执行的 CI/签名步骤 |

本地环境不适合执行完整构建或迁移测试时，完成静态检查并如实报告“未执行”，不要用 analyze 结果代替行为验证。

## 8. 交付前检查

- [ ] 新代码的 package、route、asset、Provider 和平台能力 owner 唯一且方向正确。
- [ ] 路由字符串、参数、返回值、栈行为、H5/scheme/push/native 语义没有无意变化。
- [ ] 资源路径与 pubspec.yaml、常量、大小写和倍率目录一致。
- [ ] 网络响应在 ResultModel/TCheck<T> 边界完成类型收窄；请求 DTO 与响应 DTO 的 null 语义符合接口契约。
- [ ] .tr、.sc、TQAppBar、TQNoDataWidget 等项目约定按实际 API 使用。
- [ ] 异步回调、Widget/Notifier 生命周期、Controller/FocusNode/Subscription 释放正确。
- [ ] 受影响端和实际运行过的检查命令已记录。
- [ ] 不自动执行 git commit 或 git push，等待用户明确指示。

## 9. 参考文件索引（按需阅读）

| 文件 | 什么时候读 |
|---|---|
| [references/project-structure.md](references/project-structure.md) | 判断 feature/core/shared/app/plugin 归属和迁移边界 |
| [references/assets-guide.md](references/assets-guide.md) | 新增/迁移图片、JSON、公共资源或设计稿 |
| [references/testing.md](references/testing.md) | 选择单测、Widget/契约测试和 CI runner |
| [references/networking.md](references/networking.md) | TQHttp、ResultModel、TCheck、Model 和 Repository |
| [references/state-management.md](references/state-management.md) | StateNotifier/Notifier、Provider 作用域、异步和 session reset |
| [references/i18n.md](references/i18n.md) | .tr、9 个语言文件和动态切换 |
| [references/sizing-ui.md](references/sizing-ui.md) | .sc、SafeArea、core_ui 和布局防溢出 |
| [references/permissions.md](references/permissions.md) | 权限申请、永久拒绝和 manifest |
| [references/routing.md](references/routing.md) | 命名路由、feature owner、nativeRouters 和 route effect |
| [references/compatibility.md](references/compatibility.md) | Android/iOS/OHOS 差异与插件选型 |
| [references/code-review-checklist.md](references/code-review-checklist.md) | 交付前排查真实高风险缺陷 |
| [references/new-feature-walkthrough.md](references/new-feature-walkthrough.md) | 需要从需求到验证的最小实施清单 |
