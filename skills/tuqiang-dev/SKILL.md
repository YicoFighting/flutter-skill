---
name: tuqiang-dev
description: 开发、修复、测试或评审 Tuqiang Flutter；优先复用本地状态、函数和组件，新增计算用纯函数，统一国际化与展示取值，并按改动风险验证。
metadata:
  version: "2.3.0"
---

# Tuqiang Flutter 开发

只实现 Tuqiang。Android/iOS 使用 `apps/standard`，HarmonyOS 使用 `apps/ohos`，应用装配在 `apps/tuqiang_app`。个人/企业是运行时账号模式，不是 target/flavor。公共 API 改动检查现有调用契约，不扩大到其他产品业务。

## 最小工作流

1. 按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 校验当前 checkout，读取项目 AGENTS.md。当前源码、调用方和测试高于 references；本任务已确认且未变化的信息直接复用。
2. 用一句可验证的行为明确需求：什么条件下，用户做什么，看到什么结果。只确认影响实现的 owner、账号、平台或设备范围，不填无关上下文卡；源码与已有授权不能确定的产品选择按 [澄清规则](references/requirement-clarification.md) 处理。
3. 按 [本地复用与纯函数](references/local-style-and-reuse.md) 找到已有状态、函数、组件和调用方。能复用就直接复用；缺少的计算写为显式输入、确定输出、无副作用的纯函数。IO 与状态发布留在现有 owner，不复制状态或另建通用 helper 层。
4. 在最小相关文件内实现验收行为，沿下表加载命中专题。局部修改只追到能解释该行为与消费者的边界，不强制审计整页或追完登录到退出。
5. 按 [测试规范](references/testing.md) 选择最小必要检查；有新证据或相关失败才扩大，通过后停止。交付改动结果、实际验证和必要但未验证项；检查 diff，不自动 commit/push。

## 按改动触发

触发条件是本次改变的行为，不是目标文件中已有 `.tr`、`await` 或账号分支。没有触发就不加载、不输出空表。

| 本次涉及 | 读取与要点 |
|---|---|
| 本地封装、新增函数或展示计算 | [复用与纯函数](references/local-style-and-reuse.md)：同语义优先复用；新计算显式传值；标准化只在一个边界 |
| 可见文案、字段展示、翻译或语言切换 | [国际化](references/i18n.md)：区分 key/已译文本/业务值；只翻译一次；不叠加页面 fallback |
| 登录/session、请求/DTO、缓存、权限或 UI 的账号差异 | [账号模式](../tuqiang-project-map/references/account-mode.md)：核验 isEnterprise、身份隔离与相关两侧行为 |
| 异步后发布状态/UI/副作用 | [异步生命周期](references/async-lifecycle.md)：owner、新鲜度、身份和释放分别判断 |
| Provider/family、订阅或 reset | [状态](references/state-management.md) |
| HTTP、DTO 或数据兼容 | [网络](references/networking.md) |
| 路由、参数/返回、分栏或 route effect | [路由](references/routing.md) |
| 尺寸、安全区、折叠屏与布局 | [UI 适配](references/sizing-ui.md) |
| 设计稿或资源 | [资源](references/assets-guide.md) |
| 平台/地图/设备分流与覆盖 | [实施覆盖](references/implementation-coverage.md)，平台能力再读 [兼容](references/compatibility.md) |
| 权限流程 | [权限](references/permissions.md) |
| 原生/打包、推送、广告、渠道或 SDK | [构建上下文](../tuqiang-project-map/references/build-runtime-context.md) |
| 只读评审 | [评审清单](references/code-review-checklist.md) |

## 完成标准

验收行为成立；沿用正确 owner 和本地契约；展示没有重复取值/回退，新计算没有隐式环境依赖；命中的账号、异步和平台风险有证据。通用需求核对实际可达端，共享 Dart 可一次实现和聚焦验证，不机械构造平台 × 地图 × 设备 × 账号矩阵。analyze、测试、build 与真机结果分别陈述，敏感值不进入输出。
