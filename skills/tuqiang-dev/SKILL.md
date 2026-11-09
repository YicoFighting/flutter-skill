---
name: tuqiang-dev
description: 开发、修复或评审 Tuqiang Flutter（Android/iOS/HarmonyOS）；遵守业务仓库自带规范，优先复用本地状态、函数和组件，新增计算用纯函数，统一国际化与展示取值，并按改动风险验证。
license: Apache-2.0
metadata:
  version: "2.4.0"
---

# Tuqiang Flutter 开发

只实现 Tuqiang：Android/iOS 宿主 `apps/standard`，HarmonyOS 宿主 `apps/ohos`，应用装配 `apps/tuqiang_app`。个人/企业是运行时账号模式，不是 target/flavor。公共 API 改动只检查现有调用契约，不扩大到老鹰等其他产品。

## 项目规则优先

按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 校验 checkout 后读取业务仓库 `AGENTS.md`；改 UI 时读 `DESIGN.md` 中的命中条目，并按需读取 `.codex/skills`：

- `tuqiang-flutter-conventions`：UTF-8、`.sc`、`.tr`、修改边界；**默认禁止执行 `flutter test`、安装依赖或改无关 lockfile**，禁止自动 commit/push/发布。
- `tuqiang-flutter-architecture`：包分层、依赖方向，新建/移动 package 的联动要求。
- `tuqiang-lanhu-image-assets`、`tuqiang-figma-flutter-development`：切图倍率、目录与设计还原。部分条目引用的 symbol 来自其他仓库，使用前核对当前仓库存在。

项目规则与本技能冲突时以项目规则为准；本技能补充账号、异步、i18n、覆盖与验证判断。

## 工作流

1. 用一句可验证的行为明确需求：什么条件下，用户做什么，看到什么。只确认影响实现的 owner、账号、平台或设备范围。
2. 按 [本地复用与纯函数](references/local-style-and-reuse.md) 找已有状态、函数、组件和调用方；缺少的计算写成显式输入、确定输出、无副作用的纯函数，IO 与状态发布留在现有 owner。
3. 在最小相关文件内实现，按下表加载命中专题；局部修改只追到能解释该行为与消费者的边界。
4. 按 [验证](references/testing.md) 选最小必要检查，通过即停。交付改动、实际验证和必要但未验证项；检查 diff，不 commit/push。

**澄清**：只有剩余未知会改变用户可见结果、外部契约或范围才问——账号/设备叶子改变请求/缓存/UI，API 的 null/清空/写操作语义未定义，指定业务素材缺失，平台不支持时的产品行为未定，或多种交互默认值都有依据。给出已确认事实、一个问题与方案差异，只暂停依赖答案的改动。不用默认个人模式、第一处搜索结果、自创接口、假素材或推测兼容填空白，也不反复确认用户已定的选择。

## 按改动触发

触发条件是本次改变的行为，不是目标文件里已有的 `.tr`、`await` 或账号分支。未触发不加载、不输出空表。

| 本次涉及 | 读取 |
|---|---|
| 复用已有能力、新增函数或展示计算 | [本地复用与纯函数](references/local-style-and-reuse.md) |
| 可见文案、字段展示、翻译或语言切换 | [国际化与展示取值](references/i18n.md) |
| 登录/session、请求/DTO、缓存、权限或 UI 的账号差异 | [账号模式](../tuqiang-project-map/references/account-mode.md) |
| Provider/family、HTTP/DTO、await 后发布、Timer/Stream/plugin | [状态、网络与异步](references/state-async.md) |
| 布局/尺寸/分栏、路由、设计稿或资源 | [UI、路由与资源](references/ui-routing-assets.md) |
| 平台/地图/设备分流、三端能力、权限 | [实施覆盖](references/coverage.md) |
| 原生/打包、推送、广告、渠道或 SDK | [变体与构建](../tuqiang-project-map/references/variants.md) |
| 只读评审 | [评审清单](references/code-review-checklist.md) |

## 完成标准

验收行为成立；沿用正确 owner 与本地契约；展示没有重复取值/回退，新计算没有隐式环境依赖；命中的账号、异步、平台风险有证据。共享 Dart 一次实现、聚焦验证，不机械构造平台 × 地图 × 设备 × 账号矩阵。analyze、脚本、测试、build 与真机结果分开陈述，敏感值不进入输出。
