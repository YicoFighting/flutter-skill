---
name: tuqiang-change-retrospective
description: 仅在用户明确要求时，复盘已经完成的 Tuqiang Flutter Bug、需求或混合改动；基于当前源码、Git 与验证证据生成学习 Markdown，覆盖账号模式、国际化、异步生命周期和业务链。只读调查，不修改业务代码或 Git。
license: Apache-2.0
metadata:
  version: "2.1.0"
---

# Tuqiang 变更复盘

仅在用户显式要求复盘或学习文档时使用。产品固定为 Tuqiang，不调查或汇报其他产品线业务。

## 边界与范围

- 只读源码、Git history/diff、测试结果和任务上下文；默认唯一写入是新的复盘 Markdown。
- 不修改业务代码、测试或配置，不执行 checkout/reset/pull/fetch/bisect/commit/push，不顺手修复新问题。
- 无关工作区改动不纳入；证据不足标记未知或未验证。
- 按 [根目录协议](../tuqiang-project-map/references/project-root-discovery.md) 校验 Git 根并读取项目 AGENTS.md。

开始前记录：

    mode: Bug | feature | hybrid
    product: Tuqiang
    accountMode: personal | enterprise | both | unknown
    target: standard | ohos | both | unknown
    buildVariant: <构建/原生差异相关时的 flavor/channel/SDK>
    scope: <commit/range/diff/file/symbol>
    acceptance: <症状或目标、期望、验证状态>
    output: <用户路径、项目约定或 docs/learning>

账号敏感改动必须读取 [账号模式事实](../tuqiang-project-map/references/account-mode.md) 并核验 isEnterprise；不能从 accountType、目录或 target 猜测。会改变主结论的范围歧义只问一个必要问题。

## 按需读取

| 场景 | Reference |
|---|---|
| Bug 或 hybrid 的 Bug 卡 | [bug-retrospective.md](references/bug-retrospective.md) |
| feature 或 hybrid 的需求主线 | [feature-retrospective.md](references/feature-retrospective.md) |
| 引入、暴露、修复与防线缺失 | [git-causality.md](references/git-causality.md) |
| 每次最终文档 | [report-contract.md](references/report-contract.md) |
| owner 或业务链不清 | [项目地图](../tuqiang-project-map/SKILL.md) |
| 构建/渠道/原生依赖影响结论 | [构建上下文](../tuqiang-project-map/references/build-runtime-context.md) |
| 可见文本或语言切换 | [国际化](../tuqiang-dev/references/i18n.md) |
| 实现约束需要核验 | [开发规范](../tuqiang-dev/SKILL.md) 的对应 reference |
| 用户要求 Web 对照 | [flutter-to-web](../flutter-to-web/SKILL.md) |

只加载当前模式需要的内容；源码、Git、测试和项目规则高于 reference。

## 工作流

1. 记录分支、HEAD、相关 staged/unstaged diff、提交范围和验证状态，不改工作树。
2. 建证据账本，将关键结论分成已证实事实、高可信推断和未知边界。
3. 从用户操作或生命周期入口，分开还原同步事件、异步数据、状态发布/UI 重建和清理。
4. 若相关，分别记录：
   - accountMode 来源、请求/DTO、cache/provider identity、UI 与切换/退出清理；
   - 可见文本 key、当前 manifest 全 locale、占位符、回退与翻译缓存；
   - owner 存活、结果新鲜度、device/key/session/account 身份、资源释放。
5. 按模式还原问题/目标、实现取舍、验证和预防；用 Git 证据区分引入、暴露、修复与防线缺失。
6. 按输出契约生成 UTF-8 无 BOM 文档，不覆盖同名文件，并检查链接、行号、SHA 与敏感信息。

异步 owner-specific 规则读 [异步生命周期](../tuqiang-dev/references/async-lifecycle.md)。纯 Repository 不机械要求 mounted；一次 mounted 也不能证明新鲜度、身份和释放。

## Git 与输出底线

- blame 只证明某行最后修改；只有 diff、真实传播链和复现/测试闭环才能确认因果。
- 未提交改动写“当前工作区改动，尚无对应提交”；用户确认修好不自动证明历史引入提交。
- 无法访问父版本、后端、SDK 或运行环境时写明证据停止点。
- 只摘录最小源码，使用仓库相对路径和 1-based 行号，不输出 endpoint、Token、Key、证书或生产配置。
- 默认文件名为 YYYY-MM-DD-{bug|feature|hybrid}-<slug>.md；最终回复给出绝对可点击路径及范围、accountMode、置信度和未验证项。

完成时，范围卡、三条流、账号/i18n/异步结论、Git 四类角色、事实等级和实际验证状态必须齐全；文档未覆盖旧文件，除该 Markdown 外无任何写入。
