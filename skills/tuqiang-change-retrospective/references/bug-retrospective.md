# Bug 复盘剧本

用于已完成的 Tuqiang Bug 或 hybrid 中的 Bug 卡。先确定被破坏的不变量，再追传播链、Git 角色和缺失防线。

## 问题卡

| 字段 | 内容 |
|---|---|
| accountMode / target | personal/enterprise/both/unknown；standard/ohos/both/unknown；附依据 |
| 症状与触发 | 用户所见；入口、参数、时序、设备、账号或生命周期条件 |
| 期望 / 实际 / 不变量 | 正确规则、偏离结果、任何时序和模式都必须成立的约束 |
| 验证 | 用户确认、测试、静态、真机/集成分别记录 |

期望若来自推测就标推断。账号相关结论读 [账号模式事实](../../tuqiang-project-map/references/account-mode.md)，不从 accountType 或目录猜。

## 因果与三条流

    根因/防线缺失 → 错误身份/参数/时序/资源
    → Repository/Provider/Manager 错误写入 → UI/副作用 → 症状

再拆成同步事件、异步数据、状态/UI 三条泳道，标出 await、loading/error/empty、重复操作、旧响应和身份切换；不得画成同步栈。

针对范围判断：账号来源、请求/DTO、缓存/Provider identity、UI 与 reset；可见文本的硬编码、缺 key、占位符和翻译缓存；异步的 owner、新鲜度、account/device/key/session 身份和资源释放。详细定义回到 [账号模式](../../tuqiang-project-map/references/account-mode.md)、[国际化](../../tuqiang-dev/references/i18n.md) 与 [异步生命周期](../../tuqiang-dev/references/async-lifecycle.md)，纯 Repository 不机械要求 mounted。

## 修复证据

| 步骤 | 修复前 | 修复后 | 恢复的不变量 |
|---|---|---|---|
| 模式/参数 |  |  |  |
| 异步/数据 |  |  |  |
| 状态/UI/清理 |  |  |  |

最小证据覆盖入口、错误条件、修复点、最终消费者和回归测试。历史代码写 path@sha，当前代码写 path:line；不伪造旧行号。

## Git 与预防

按 [Git 因果](git-causality.md) 分开缺陷引入、问题暴露、修复与防线缺失，每个角色独立给证据和置信度。本次实际排查只写发生过的步骤，推荐流程另列。

预防措施必须对应本根因：代码门禁、修复前失败/修复后通过的测试、2–4 个评审问题、脱敏可观测字段，以及相关账号/target/语言/key/前后台回归。最终结构与检查统一按 [输出契约](report-contract.md)。
