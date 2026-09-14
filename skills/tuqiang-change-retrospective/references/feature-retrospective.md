# 需求复盘剧本

用于已完成的 Tuqiang 需求或 hybrid 的需求主线。按“用户价值 → 可验收行为 → 规则 → 数据/状态 → 实现 → 证据”下钻，不按文件清单叙述。产品理由只有用户、工单或明确说明可证明时才写事实。

## 范围与取舍

记录 accountMode、target、用户入口、正常/loading/empty/error/权限/取消分支、不在范围内行为，以及代码存在、测试通过、用户确认、真机未验证等不同状态。both 必须有两侧证据。

| 决策 | 证据 |
|---|---|
| owner 与复用 | route、barrel、调用方、测试、pubspec；复用的现有 symbol/contract |
| 状态与数据 | Widget State、Provider family/Notifier、Manager/cache；Repository/HTTP/plugin/storage |
| 平台与账号 | standard/ohos adapter/override；模式来源、请求/DTO、cache、UI、reset |

“为了可维护性”不是证据；说明为何选择现有 owner 和契约。

## 输入输出与三条流

| 输入/来源 | accountMode/身份 | 转换/校验 | 状态写入 | 输出/消费者 | 证据 |
|---|---|---|---|---|---|

输入可来自操作、route/deep link/push/native callback、family key、session、API/cache/plugin 或 bootstrap。若个人/企业任一列不同，分两行。

    同步事件：操作 → Widget callback → command → 发起数据操作
    异步数据：输入/身份 → await → Model/错误 → 接受或丢弃
    状态/UI：状态写入 → 派生/通知 → Widget 或副作用

说明 accountMode 和参数如何产生、数据在哪转换、State 按何种 key/session 隔离、谁消费，以及离开页面、切账号/设备、重复操作和旧响应如何处理。

## 防线与证据

只对相关项记录账号入口/请求/cache/UI/reset，i18n 的复用 key/全 locale/占位符/动态翻译，以及异步 owner/新鲜度/身份/释放。详细规则回到 [账号模式](../../tuqiang-project-map/references/account-mode.md)、[国际化](../../tuqiang-dev/references/i18n.md) 和 [异步生命周期](../../tuqiang-dev/references/async-lifecycle.md) 事实源。

最小源码覆盖入口、状态 owner、数据边界、账号分支、写入、最终 UI/副作用和测试。按解决问题的逻辑顺序讲实现；Git 无法证明实际开发顺序时标“按最终 diff 教学重组”。

hybrid 中每个 Bug 卡说明它是新引入、暴露旧问题还是独立修复，影响主链哪一步和哪种 accountMode，并给 Git 四类角色与回归；复杂项读取 [Bug 剧本](bug-retrospective.md)。最终结构按 [输出契约](report-contract.md)。
