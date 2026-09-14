---
name: tuqiang-dev
description: 开发、修复、测试或评审 Tuqiang Flutter monorepo；修改账号、请求、缓存、页面、状态、路由、国际化或异步逻辑时，强制区分个人/企业模式，并按需覆盖 Android、iOS、HarmonyOS、地图和设备页面变体。
metadata:
  version: "2.1.0"
---

# Tuqiang Flutter 开发

只实现 Tuqiang：apps/standard 承载 Android/iOS，apps/ohos 承载 HarmonyOS，apps/tuqiang_app 负责应用装配。个人/企业是同一 App 的运行时账号模式，不是 target 或 flavor。

不要调查或交付其他产品线业务。修改公共 core/shared/plugin API 时仍检查全部现有调用契约，但不扩大业务实现。仓库事实与 owner 由 [项目地图](../tuqiang-project-map/SKILL.md) 提供。

## 开工卡

按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 校验 Git 根并读取项目 AGENTS.md。修改前填写：

    变更类型：Bug | 新需求 | 混合 | 只读评审
    用户行为与验收：<条件、操作、可观察结果>
    accountMode：personal | enterprise | both | unknown
    平台/target：Android/iOS standard | HarmonyOS ohos | multiple | unknown
    构建变体：<仅涉及原生/打包差异时填写 flavor/channel/SDK>
    owner：<app/feature/shared/core/plugin>
    用户可见文本：是 | 否
    异步后发布 UI/状态/副作用：是 | 否
    设备范围：不涉及 | 全部 | 指定叶子 | unknown
    地图场景：不涉及 | <当前 symbol>

源码能确定的字段直接填写。unknown 若会改变请求、缓存、UI、reset、范围或验收，按 [澄清门](references/requirement-clarification.md) 展示证据并只问一个必要问题。

## 三个强制门

- **账号模式**：登录/session、HTTP/DTO、设备目录、消息、权限、缓存、页面可见性、账号切换或退出必须读取 [账号模式事实](../tuqiang-project-map/references/account-mode.md)。只认当前 isEnterprise 链；both 要分别验证两侧，unknown 不得当公共逻辑。
- **国际化**：任何标题、按钮、Toast、Dialog、空态、错误、权限提示、tooltip 或语义标签都读取 [i18n](references/i18n.md)。调用 .tr 不等于 key 存在；禁止缓存长生命周期翻译结果。
- **异步发布**：await/then/whenComplete、Timer、Stream、listener 或 plugin callback 后发布状态/UI/副作用时读取 [异步生命周期](references/async-lifecycle.md)，分别证明 owner 存活、结果新鲜、device/key/session/accountMode 身份匹配和资源释放；mounted 只覆盖第一项。

## 实施

1. 从用户入口追到 Widget/Coordinator → Notifier/Manager/Controller → Repository/HTTP/缓存/插件 → 状态写入 → UI/副作用 → dispose/invalidate/session reset；分开同步事件、异步结果和响应式重建。
2. 在真实 owner 内找 2–4 个成熟同类样本，确认公开 API、调用方和最小文件范围。owner 索引读 [模块目录](../tuqiang-project-map/references/module-catalog.md)，复用边界读 [局部风格](references/local-style-and-reuse.md)。
3. 保持既有路由参数/返回/栈与错误语义；素材缺失按 [资源规范](references/assets-guide.md) 停止，不造业务切图。
4. 只做需求直接需要的修改，不顺手迁移状态库、重排目录或新增无真实消费者的抽象。

Provider/family、网络和路由分别读取 [状态](references/state-management.md)、[网络](references/networking.md)、[路由](references/routing.md)；不要在入口重复维护实现细节。

## 条件覆盖

[实施覆盖](references/implementation-coverage.md) 是平台、账号、地图和设备矩阵的唯一来源。仅在相关时展开：

- Bug 至少闭环 Android 与 HarmonyOS，并检查 iOS 共享路径/专属差异；新需求完成三端代码。
- 主地图核对 Android/iOS 各百度、高德、Google，加 HarmonyOS Map Kit 七个候选。
- 多个设备 route/Page 可达且范围不明时，确认全部或指定叶子后再写代码。

不要生成平台 × 地图 × 设备 × 账号的笛卡尔积；只列当前源码可达且会改变行为的组合，每个无需修改都附证据。

## 验证与交付

按风险运行 owner 的 analyze/test、Widget/contract/lifecycle 测试、宿主检查、build、真机或 CI；命令和证据等级只在 [测试规范](references/testing.md) 维护。analyze 不能冒充 build/真机，standard 不能证明 Android 与 iOS 都已运行。检查 diff，分别记录通过、失败、未运行和交接项。

完成前确认：任务卡闭合；个人/企业相关入口、请求、缓存、UI/reset 有证据；可见文本通过当前 manifest；异步四防线有测试或理由；owner/依赖/路由/资源正确；条件矩阵逐行关闭；无敏感值、格式噪声或 BOM。未经明确要求不得 commit/push。

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
