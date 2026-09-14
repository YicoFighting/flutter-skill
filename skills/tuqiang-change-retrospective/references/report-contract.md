# Markdown 输出契约

每次只生成一份无需聊天上下文即可阅读的 Markdown；不授权修改业务代码、测试、配置或 Git。

## 文件

路径优先级：用户文件 → 用户目录 → 项目规范 → docs/learning。默认名：

    YYYY-MM-DD-{bug|feature|hybrid}-<safe-kebab-slug>.md

不覆盖已有文件，依次加 -2、-3；只有用户明确要求更新原文时才编辑。使用 UTF-8 无 BOM，末尾换行。

## 元信息

标题后记录：

| 字段 | 内容 |
|---|---|
| 模式/product/accountMode/target | Bug、需求或混合；Tuqiang；personal/enterprise/both/unknown；standard/ohos/both/unknown |
| 构建上下文（相关时） | platform、flavor、distributionChannel、SDK；区分母包、分渠道产物及各自验证证据 |
| 范围与基线 | commit/range/diff/file/symbol；分支、short HEAD、相关未提交状态 |
| 日期与验证 | 本地日期；用户确认、test、analyze、真机/集成分别记录 |
| Git 置信度 | 引入、暴露、修复分别为已确认/高度可能/候选/无法确定/不适用 |

both 必须有个人与企业证据；unknown 写证据停止点和影响。detached HEAD 如实记录，不输出含凭据的 remote URL。

## 模式结构

Bug：

    30 秒结论；范围/accountMode/验证；现象与不变量；因果金字塔；
    引入/暴露/修复/防线缺失；三条流；修复前后证据；
    修复有效性；排查路径；防复发矩阵；证据账本；学习总结。

需求：

    30 秒业务结果；范围/accountMode/验证；目标与验收；实现金字塔；
    owner 与取舍；三条流；输入输出血缘；真实证据；
    账号/i18n/异步防线；实现与验证；证据账本；学习总结。

混合模式以需求为主线，在对应步骤后放 Bug 卡，记录其关系、Git 四类角色、因果/修复和回归；复杂 Bug 可展开，但仍只输出一个文件。没有证据的标题可以合并或标“不适用”，不得填充猜测。

## 防复发矩阵

| 类别 | 检查项 | 结论 | 证据/缺口 | 防线 |
|---|---|---|---|---|
| accountMode | 来源、请求/DTO、缓存身份、UI、切换/退出 |  |  |  |
| i18n | 硬编码、全 locale/占位符/空值、翻译缓存 |  |  |  |
| async | owner、新鲜度、account/device/key/session 身份、资源释放 |  |  |  |

只展开相关项；不适用写理由。这张表回答为何未更早发现及如何防复发，不复制正文因果。

## 证据格式

- 至少一份纯文本金字塔或因果栈；同步事件、异步数据、状态/UI 分泳道。
- 输入输出用血缘表；Git 使用“角色—改动—因果—证据—置信度”。
- 当前代码写仓库相对路径和实时 1-based 行号；历史代码写 path@short-sha。
- 仅摘录证明一跳所需源码，并解释输入、输出和下一跳。
- endpoint、Token、Key、证书、签名和生产配置省略或脱敏。
- Web 对照仅在用户要求时给指定框架，并标明是教学映射。

## 完成条件

product、accountMode、target、范围和验证齐全；事实/推断/未知及 Git 角色不混淆；事件、异步和响应式更新未画成伪同步栈；防复发矩阵闭合；链接、行号、SHA 可核验；文档未覆盖旧文件且无敏感信息。最终回复提供绝对可点击路径。
