---
name: tuqiang-dev
version: 1.7.0
description: 途强（tuqiang）三端 Flutter 项目专属开发技能。面向不会写代码或只会 Vue3 前端的人员，配合 AI 编码助手完整实现 Android / iOS / 鸿蒙三端需求。包含项目铁律、目录规范、dio 网络请求、Riverpod 全局状态、权限申请、sc 尺寸适配、tr 国际化、路由注册、三端兼容等全部规范，以及从零实现一个需求的完整步骤模板。凡在本仓库内开发新功能、改 Bug、加页面、加接口，一律先读本技能。
---

# 途强三端开发规范（tuqiang-dev）

你正在 **D:\Code\tuqiang** 这个 Flutter monorepo 里工作。它同时产出 Android、iOS、HarmonyOS（鸿蒙）三个端的应用。

本技能的读者可能是：① AI 编码助手；② 不会写 Dart/Flutter、只会 Vue3 甚至完全不懂代码的人。
因此规则分两类：

- **【铁律】** 违反会导致编译失败、CI 挂掉或线上事故，任何情况下不得违反；
- **【规范】** 保证代码可迭代、三端兼容的固定套路，照抄模板即可，不需要理解原理。

> 给人的话：你不需要"学会 Flutter"，你只需要**找一个同类旧页面 → 照着模板替换内容 → 跑验证命令**。给 AI 的话：所有代码必须符合本文与 references/ 内的模板，不确定时先读对应参考文件再动手。

---

## 1. 三条铁律（先背下来）

### 铁律一：命令只走统一入口

本仓库有两个 Flutter App 工程、两套 SDK，**永远不要直接执行 `flutter run` / `flutter build` / `flutter pub get`**。统一入口 `tool/project.dart` 会按端自动选择正确的 Flutter SDK（读取各 app 的 `.fvmrc`，标准端 `3.35.7`，鸿蒙端 `custom_3.35.7_ohos`）。

```powershell
# 标准端 = Android + iOS（SDK 3.35.7）
dart run tool/project.dart pub-get standard --enforce-lockfile
dart run tool/project.dart analyze standard
dart run tool/project.dart run standard
dart run tool/project.dart build standard apk --debug
dart run tool/project.dart test standard          # 跑迁移契约测试

# 鸿蒙端 = HarmonyOS（SDK custom_3.35.7_ohos，入口自动切换定制 SDK）
dart run tool/project.dart pub-get ohos --enforce-lockfile
dart run tool/project.dart analyze ohos
dart run tool/project.dart test ohos
dart run tool/project.dart build ohos hap --debug
```

> ⚠️ 本机是 Windows PowerShell 5.1 时，直接运行 `.\tool\check_migration_boundaries.ps1` 可能因编码解析报错（脚本是无 BOM UTF-8）。CI 用的是 PowerShell 7（`pwsh`），以 CI 结果为准；本地跑不动时改用 `dart run tool/project.dart analyze` 双端全绿兜底。

- 在 `apps/ohos` 目录裸跑 `flutter` 会用错 SDK、污染仓库签名配置——禁止。
- 提交前必须保证 `analyze standard` 与 `analyze ohos` 都零 error（warning 尽量清零）。
- 改了公共包（packages/**）之后，两端都要 analyze。

### 铁律二：鸿蒙专属 API 永远不进公共 Dart 代码

以下符号出现在 `apps/tuqiang_app/lib`、`packages/core/*/lib`、`packages/shared/**/lib`、`packages/feature/*/lib` 等公共代码里**一律禁止**（官方 Flutter 编译器无法解析，就算用 if 包住也会分析整个文件；仓库红线脚本与 CI 也会拦截架构违规）：

```text
Platform.isOhos   OhosView   flutter_blue_plus_ohos   screen_protector_ohos
任意 xxx_ohos 包名   鸿蒙定制 Flutter SDK 独有类
```

原因：官方 Flutter 编译器无法解析这些符号，就算用 if 包住也会分析整个文件。
正确做法见 [references/compatibility.md](references/compatibility.md)——三种注入模式（视图构建器 / 依赖注入回调 / 桥接注册），全部来自本仓库真实代码。

### 铁律三：新依赖先查有没有鸿蒙替代品

添加任何三方库之前，按顺序检查：

1. `apps/ohos/pubspec.yaml` 的 `dependency_overrides` 里是否已有 ohos 适配版（如 `share_plus_ohos`、`umeng_common_sdk_ohos`、git 源的 `openharmony-tpc` 包）；
2. `packages/adapter/` 下是否已有本项目封装的适配包（优先引适配包而不是原生包）;
3. `packages/plugins/` 下是否已有 tq_* 自研插件覆盖该能力（推送、地图、日志、文件、蓝牙等都有）。

加依赖要同时评估两端：标准端版本写进 `apps/standard/pubspec.yaml` 或对应 package 的 pubspec；鸿蒙端在 `apps/ohos/pubspec.yaml` 用 override 指到 ohos 版。**提交时两个 `pubspec.lock` 都不能被意外改写**（CI 会检查）。

---

## 2. 一分钟看懂这个仓库

```text
tuqiang/
├── apps/
│   ├── standard/        # Android + iOS 入口工程（官方 Flutter 3.35.7）
│   ├── ohos/            # HarmonyOS 入口工程（定制 SDK custom_3.35.7_ohos）
│   └── tuqiang_app/     # 公共业务 App 包（name: tuqiang），三端共享
├── packages/
│   ├── core/            # 基础库：网络 core_http、国际化 core_i18n、UI core_ui、
│   │                    #   工具 core_base、尺寸适配、权限管理、webview、分享…
│   ├── feature/         # 业务模块包：feature_auth / feature_pet / feature_gps /
│   │                    #   feature_camera / feature_mine / feature_message …
│   ├── shared/          # shared_business：跨模块共享的业务层、模型、Provider
│   ├── plugins/         # 自研平台插件 tq_*（含各自的原生 Android/iOS/ohos 实现）
│   ├── adapter/         # 三方库的 ohos 替代适配包
│   └── assets_common/   # 跨端公共静态资源（隐私协议 HTML 等）
├── tool/project.dart    # 统一构建入口（铁律一）
├── tool/check_migration_boundaries.ps1  # 迁移架构红线检查脚本（CI 执行）
└── docs/                # 架构与迁移方案文档
```

一句话分工：**页面和业务写在 feature 包；跨模块复用的状态和模型放 shared_business；纯工具和 UI 组件放 core；只有碰原生能力才动 plugins / adapter。**

详细「我想加 X 应该动哪个包」决策表 → [references/project-structure.md](references/project-structure.md)

---

## 3. Vue3 头脑映射表（看懂代码用）

只会 Vue3 的人按这张表翻译概念，AI 解释代码时也必须用这套大白话：

| Vue3 | 这个项目 | 说明 |
|---|---|---|
| 组件 `.vue` 文件 | `Widget` 类 | 页面就是一个 Widget 类 |
| Pinia store | Riverpod `StateNotifierProvider` | 全局/模块状态仓库 |
| store 的 state | 不可变 `XxxState` 类 | 字段全 final，改动靠整体替换 |
| store 的 actions | `XxxController extends StateNotifier<XxxState>` 的方法 | 请求接口、改状态都写这里 |
| `computed` / 响应式绑定 | `ref.watch(xxxProvider)` | 数据变了 UI 自动刷新 |
| 方法里取一次值 | `ref.read(xxxProvider.notifier)` | 拿 controller 调方法，不订阅 |
| `$t('key')` | `'中文原文'.tr` | key 直接写中文，详见 i18n 规范 |
| `<style>` 里的 px | 数值后加 `.sc` | `15.sc`，设计稿宽 375 基准 |
| `v-model` | `TextEditingController` | `controller.text` 取输入值 |
| `onMounted` | `initState()` | 页面加载跑一次 |
| `onUnmounted` | `dispose()` | 释放 controller/focusnode |
| `props` + emit 回调 | 构造参数传函数 `onTap: () {}` | |
| `router.push` | `Navigator.pushNamed(context, 名字)` | 字符串路由，需先注册 |

深入版映射与示例 → 各 references 文件。

---

## 4. 标准开发闭环（人机协同 SOP）

为了防止 AI 盲目猜测修改代码导致返工，所有需求必须严格执行 **「先对齐方案 ➔ 审批后编码 ➔ 动态同步 ➔ 全绿交付」** 的五步闭环：

### 阶段一：需求调研与反向拉扯（AI 严禁立即写码）
1. **AI 预检与调研**：AI 检索代码库相似功能与 `references/` 规范（尤其是三端兼容预检表）。
2. **主动质疑与对齐（Karpathy Think Before Coding）**：
   - 严禁暗箱假设与脑补业务逻辑，凡有模糊或多解处，必须主动列出选项向用户提问；
   - **UI 设计源决策与蓝湖 MCP 接入【强制卡点】**：
     - **新页面事前必问**：AI **必须在开工前主动询问用户是否有该页面的蓝湖设计稿链接**；
     - **分支 A（有蓝湖链接）**：检查并调用 `lanhu-mcp`（`lanhu_get_designs` ➔ `lanhu_get_ai_analyze_design_result` 提取精确 HTML/CSS 样式与参数 ➔ `lanhu_get_design_slices` 提取多倍切图），**严禁私自使用 `Icons.xxx` 或 `CupertinoIcons.xxx` 代替切图**，严格执行像素级还原；
     - **分支 B（无蓝湖链接）**：必须遵循项目现有整体 UI 风格（`#F5F6F8` 灰底、白色圆角卡片、`.sc` 间距规范、`core_ui` 公共组件如 `CommonAppBar` / 统一按钮 / 空状态），向用户简述 UI 骨架确认后再编码（详见 [references/assets-guide.md](references/assets-guide.md)）；
   - **测试文件需求事前必问【强制卡点】**：
     - AI **必须主动向用户询问本次需求是否需要生成对应的测试文件/测试用例**；
     - **用户不同意或未明确回答需要**：严禁擅自生成任何测试代码，保持交付精简高效；
     - **用户明确同意或主动提及需要**：后续每一次代码编写/变更后，AI **必须强制同步生成或更新对应的测试文件（`test/`）**，并在交付时出具《提测交付单》（详见 [references/testing.md](references/testing.md)）；
   - **数据源动静判定与接口对齐【强制卡点】**：
     - **静态数据**：AI 判定为纯客户端本地配置时，必须向用户陈述理由并确认（如说明为什么无需服务端动态下发），确认后收敛在常量配置中，禁止零散写死在 Widget 内部；
     - **动态接口**：若用户已提供接口文档，按规范编写 Endpoints/Repository/Model；**若用户暂未提供接口，严禁私自编造假 URL**！必须预留标准方法并使用 `Future.delayed` 结构化异步 Mock 数据，保证后续接入真实接口时 UI 与 Controller 零改动（详见 [references/networking.md](references/networking.md)）；
   - 主动评估三端兼容风险（如蓝牙/权限/原生调用/鸿蒙差异）。
3. **来回拉扯确认**：双方沟通直至业务逻辑、技术边界、静态切图资产、数据源接口方案与**可证伪验证标准**（如何证明功能正确）100% 清晰。

### 阶段二：出具实施方案 + 任务 Checklist
AI 输出完整的 **实施方案文档与任务分解清单（Checklist）**，包含：
- 涉及改动的包与文件列表（按 Model / Controller / Page / Assets / i18n / Router 拆解）；
- 涉及的三端兼容处理与平台差异方案；
- **极简优先（Simplicity First）**：方案必须是解决问题的最小代码量，严禁加入未经要求的“未来扩展性”和多余抽象；
- 可执行的任务 Checklist（包含每一步的明确验证标准）。
> ⚠️ **强制卡点：方案必须获得用户的明确同意（Approval）后，AI 才允许开始编写代码！**

### 阶段三：分步编码与 Checklist 实时同步
1. **外科手术式精准修改（Surgical Changes）**：
   - 严格限定改动范围（Blast Radius），只修改与当前任务直接相关的代码行；
   - 严禁借修 Bug 之名“顺手重构”周边无关代码或大面积重格式化文件（No drive-by refactoring）。
2. **安全操作与编码基线（Safe Operation & UTF-8）**：
   - 所有文件读写与配置脚本必须显式强制 UTF-8 编码（无 BOM），杜绝 Windows 下的 GBK/ANSI 编码损坏；
   - 严禁擅自篡改依赖版本与锁文件，严禁擅自启动未经授权的外部长期后台进程；
   - 严格防范敏感信息泄漏，严禁在代码、日志、终端或回复中暴露未脱敏的 Token、密码、私钥或生产环境配置。
3. **测试代码同步伴生（若开启测试要求）**：
   - 若阶段一已确认需要测试文件，每完成或修改一个业务文件（Model / Notifier / Page），必须**同步创建或修改 `test/` 目录下对应的测试文件**。
4. **分步实现与实时打勾**：严格按 Checklist 逐步实现各子模块，每完成一项**实时更新任务 Checklist 状态**（如 `- [x]`），让用户随时掌握进展。
5. **遇阻即问**：编码过程中若发现未预期的问题、接口变动或设计冲突，**立即暂停并主动向用户提问**，根据讨论结果同步更新方案与 Checklist。

### 阶段四：本地全量验证（三道护身符）
```powershell
dart run tool/project.dart pub-get standard --enforce-lockfile   # 改依赖时
dart run tool/project.dart analyze standard                    # 标准端类型语法检查
dart run tool/project.dart analyze ohos                        # 鸿蒙端类型语法检查
dart run tool/project.dart test standard                       # 运行单测（若生成了测试文件）
.\tool\check_migration_boundaries.ps1                          # 架构红线检查（需 pwsh 7；CI 必跑）
```

### 阶段五：交付与审查（Code Review）
- **交付前防御性自检**：
  - [ ] 是否触碰了与需求无关的文件？（保持变动最小化）
  - [ ] **UI 与切图规范**：是否已事前询问蓝湖链接？有蓝湖稿是否通过 `lanhu-mcp` 像素级还原？无蓝湖稿是否严格贴合项目设计规范？是否杜绝了擅自使用 `Icons.xxx`？切图是否按 1x/2x/3x 放入对应目录并在常量类声明？
  - [ ] **测试文件与提测单**：是否严格遵守按需触发原则（未确认不生成，已确认则全量伴生）？已开启测试时是否所有测试均通过并附带《提测交付单》？
  - [ ] **接口与数据源规范**：是否杜绝了私自脑补假 URL？静态数据是否已陈述理由并确认收敛？动态接口暂缺时是否已按标准 Repository 异步 Mock？
  - [ ] **Model 规范**：是否严格遵守四大铁律（纯业务数据无 UI 文案、字段全可空、`TCheck` 防崩、`toJson` 集合 if 过滤 null）？
  - [ ] **i18n 规范与防坑**：是否所有中文字符串都在 9 语言 JSON 文件中补齐了翻译？**是否杜绝了在 Widget/State 成员属性中使用 `final` 缓存 `.tr` 国际化文本？**
  - [ ] **编码与安全防线**：所有文件读写是否显式使用 UTF-8（无 BOM）？是否存在任何 Token、密码、私钥等敏感信息泄露风险？
  - [ ] 是否所有异步操作都做了 `if (!mounted) return;` 保护？
  - [ ] **生命周期与 Provider 赋值红线**：是否杜绝了在 `initState` / `build` 中直接同步修改 Provider 状态？（`initState` 中触发拉取必须包在 `WidgetsBinding.instance.addPostFrameCallback` 内）
  - [ ] 是否所有 Controller / FocusNode / 订阅都在 `dispose` 中成对释放？
  - [ ] 鸿蒙端是否有未隔离的独有符号或缺失 ohos 适配的三方库？
- ⚠️ **验证全绿后，严禁擅自自动执行 `git commit`**，保持工作区干净，交付给用户或其他大模型进行 Code Review 审查。
- 审查通过后，由用户或由用户指示使用 **Angular 中文规范** 提交：

| 前缀 | 场景 | 示例 |
|---|---|---|
| `feat:` | 新功能 | `feat: 新增宠物洗澡记录页` |
| `fix:` | 修复 Bug | `fix: 修复信标列表越界崩溃` |
| `refactor:` | 重构 | `refactor: 提取设备卡片公共组件` |
| `docs:` | 文档/说明 | `docs: 补充接口文档` |
| `style:` | 样式/UI 调整 | `style: 解绑按钮上下居中` |
| `chore:` | 构建/工具/配置 | `chore: 升级依赖版本` |
| `perf:` | 性能优化 | `perf: 优化地图渲染流畅度` |
| `test:` | 测试 | `test: 补充信标数据解析单测` |

---

## 5. 参考文件索引（按需阅读）

| 文件 | 内容 |
|---|---|
| [references/project-structure.md](references/project-structure.md) | 目录地图、「加东西动哪个包」决策表、pubspec 注意事项 |
| [references/assets-guide.md](references/assets-guide.md) | **UI 设计源决策、蓝湖 MCP 接入与静态资源切图全景规范**：事前必问蓝湖链接、lanhu-mcp 自动化读取、无设计稿自适应规范、杜绝 Icons 脑补、2x/3x 倍图、命名与常量注册 |
| [references/testing.md](references/testing.md) | **测试规范与提测交付标准**：按需生成必问原则、Unit/Widget 测试模板、提测交付单 Markdown |
| [references/networking.md](references/networking.md) | dio/TQHttp 封装、ResultModel、TCheck 安全取值、Model 四大铁律与代码模板、动态接口暂缺异步 Mock |
| [references/state-management.md](references/state-management.md) | Riverpod State+Controller+Provider 三板斧、Consumer 接线、生命周期防修改红线、session 重置 |
| [references/i18n.md](references/i18n.md) | tr/keyTr/multiKeyTr、9 语言 JSON 维护、禁止 `final` 成员变量缓存 `.tr` |
| [references/sizing-ui.md](references/sizing-ui.md) | sc 适配原理与限制、verticalSpace/horizontalSpace、安全区与 core_ui 清单 |
| [references/permissions.md](references/permissions.md) | TQPermissionManager 全量权限申请、定位双关检查、永久拒绝引导 |
| [references/routing.md](references/routing.md) | 字符串路由注册四步、传参约定、nativeRouters |
| [references/compatibility.md](references/compatibility.md) | 三端兼容铁律细则、平台差异三种注入模式、插件选型路径 |
| [references/new-feature-walkthrough.md](references/new-feature-walkthrough.md) | 从零实现一个完整页面的分步模板（复制即用） |

---

## 6. 给人类操作者的协同心法

1. **需求拉扯期**：把需求告诉 AI ➔ 认真回答 AI 提出的边界与疑点（包括是否需要测试文件） ➔ 审阅方案文档与任务 Checklist。
2. **方案审批点**：确认方案可行后再回复“同意/开始执行”，牢牢把握架构控制权。
3. **编码观察期**：观察 AI 实时打勾更新的 Checklist 进度，遇到 AI 提问时及时对齐决策。
4. **验证与审查**：督促 AI 跑通 §4 的验证命令全绿 ➔ 使用其他模型或人工进行 Code Review ➔ 确认无误后按规范提交。
