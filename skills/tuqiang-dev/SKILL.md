---
name: tuqiang-dev
description: 开发、修复、测试或评审 Tuqiang Flutter monorepo；按实际改动检查账号分支、国际化、异步与平台影响，按风险选择模块分析、测试和必要构建，避免小改动触发全量验证。
metadata:
  version: "2.2.0"
---

# Tuqiang Flutter 开发

只实现 Tuqiang：apps/standard 承载 Android/iOS，apps/ohos 承载 HarmonyOS，apps/tuqiang_app 负责应用装配。个人/企业是同一 App 的运行时账号模式，不是 target 或 flavor。

不要调查或交付其他产品线业务。修改公共 core/shared/plugin API 时仍检查全部现有调用契约，但不扩大业务实现。仓库事实与 owner 按需查 [项目地图](../tuqiang-project-map/SKILL.md) 的相关 reference；局部改动不把完整业务链讲解或架构调查作为前置任务。

## 开工卡

按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 校验 Git 根并读取项目 AGENTS.md。修改前明确以下相关信息；简单任务可在内部简记，无需逐项输出空表：

    变更类型：Bug | 新需求 | 混合 | 只读评审
    用户行为与验收：<条件、操作、可观察结果>
    accountMode：personal | enterprise | both | unknown
    平台/target：Android/iOS standard | HarmonyOS ohos | multiple | unknown
    构建变体：<仅涉及原生/打包差异时填写 flavor/channel/SDK>
    验证范围：<按 testing.md 分级；准备运行的最小检查>
    owner：<app/feature/shared/core/plugin>
    用户可见文本：是 | 否
    异步后发布 UI/状态/副作用：是 | 否
    设备范围：不涉及 | 全部 | 指定叶子 | unknown
    地图场景：不涉及 | <当前 symbol>

源码能确定的字段直接填写。unknown 若会改变请求、缓存、UI、reset、范围或验收，按 [澄清门](references/requirement-clarification.md) 展示证据并只问一个必要问题。

## 三个条件触发的强制门

按本次行为变化与实际 diff 判断触发条件，不因文件中已有账号分支、翻译或 await 就审计整页；命中风险后，下列防线仍必须检查。

- **账号模式**：登录/session、HTTP/DTO、设备目录、消息、权限、缓存、页面可见性、账号切换或退出必须读取 [账号模式事实](../tuqiang-project-map/references/account-mode.md)。只认当前 isEnterprise 链；both 要分别验证两侧，unknown 不得当公共逻辑。
- **国际化**：任何标题、按钮、Toast、Dialog、空态、错误、权限提示、tooltip 或语义标签都读取 [i18n](references/i18n.md)。调用 .tr 不等于 key 存在；禁止缓存长生命周期翻译结果。
- **异步发布**：await/then/whenComplete、Timer、Stream、listener 或 plugin callback 后发布状态/UI/副作用时读取 [异步生命周期](references/async-lifecycle.md)，分别证明 owner 存活、结果新鲜、device/key/session/accountMode 身份匹配和资源释放；mounted 只覆盖第一项。

## 实施

1. 从用户入口追到足以解释本次行为和受影响消费者的边界。逻辑变更串起 Widget/Coordinator → 状态 owner → Repository/HTTP/缓存/插件 → UI/副作用；身份或生命周期变化再追 reset/dispose。局部样式不追无关网络/session 链。
2. 优先沿用目标 owner 的现有实现；需要新增模式时先找一个直接可比的成熟样本，有差异或歧义再扩大比较，不为凑数量继续搜索。确认公开 API、调用方和最小文件范围。owner 索引读 [模块目录](../tuqiang-project-map/references/module-catalog.md)，复用边界读 [局部风格](references/local-style-and-reuse.md)。
3. 保持既有路由参数/返回/栈与错误语义；素材缺失按 [资源规范](references/assets-guide.md) 停止，不造业务切图。
4. 只做需求直接需要的修改，不顺手迁移状态库、重排目录或新增无真实消费者的抽象。

Provider/family、网络和路由分别读取 [状态](references/state-management.md)、[网络](references/networking.md)、[路由](references/routing.md)；不要在入口重复维护实现细节。

## 条件覆盖

[实施覆盖](references/implementation-coverage.md) 是平台、账号、地图和设备矩阵的唯一来源。仅在相关时展开：

- 三端先检查可达性与共享/专属实现；用户已指定平台时遵循范围，并核对共享改动的回归。通用需求在可达端完成实现，共享 Dart 可一次覆盖多端；这不要求逐端重复 analyze、test 或 build。
- 地图协议、adapter 或真实地图行为变化才核对七个候选；普通地图页标题、按钮样式不自动触发七后端验证。
- 改变设备分流或共享详情行为且不同 route/Page 范围会改变实现时，确认全部或指定叶子；用户明确的局部控件修改无需追加全设备询问。

不要生成平台 × 地图 × 设备 × 账号的笛卡尔积；只列当前源码可达且会改变行为的组合，每个无需修改都附证据。

## 验证与交付

按 [测试规范](references/testing.md) 的风险分级先选最小验证集；只有新证据、失败或明确要求才扩大到宿主、构建或全量回归。无新改动且必要检查已通过时停止，不为补齐三端表格重复执行。命令、升级条件和证据等级由该 reference 统一维护。analyze 不能冒充 build/真机，standard 不能证明 Android 与 iOS 都已运行。检查 diff，分别记录通过、失败、未运行和交接项。

完成前只核对本次触发项：验收与验证范围闭合；相关个人/企业入口、请求、缓存、UI/reset 有证据；文案变更通过当前 manifest；异步变化的四防线有测试或理由；owner/依赖/路由/资源正确；受影响组合有实现与验证结论；无敏感值、格式噪声或 BOM。未经明确要求不得 commit/push。

## Reference 路由

| 场景 | Reference |
|---|---|
| 验收、账号、素材/API 或范围多解 | [requirement-clarification.md](references/requirement-clarification.md) |
| 平台、账号、地图或设备覆盖 | [implementation-coverage.md](references/implementation-coverage.md) |
| 局部样本、复用与抽象 | [local-style-and-reuse.md](references/local-style-and-reuse.md) |
| Provider/family、订阅与 reset | [state-management.md](references/state-management.md) |
| 异步发布与资源 owner | [async-lifecycle.md](references/async-lifecycle.md) |
| TQHttp、DTO 与请求分支 | [networking.md](references/networking.md) |
| Feature route 与 effect | [routing.md](references/routing.md) |
| 可见文本、语言切换与 RTL | [i18n.md](references/i18n.md) |
| 尺寸、安全区与多语言布局 | [sizing-ui.md](references/sizing-ui.md) |
| 设计源和 package asset | [assets-guide.md](references/assets-guide.md) |
| 构建、推送、广告、渠道与 SDK 选择 | [构建上下文](../tuqiang-project-map/references/build-runtime-context.md) |
| 测试命令和验证证据 | [testing.md](references/testing.md) |
| 权限流程 | [permissions.md](references/permissions.md) |
| 平台插件与降级 | [compatibility.md](references/compatibility.md) |
| 只读评审或最终风险复查 | [code-review-checklist.md](references/code-review-checklist.md) |
