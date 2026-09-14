# 完整业务链追踪

从用户可感知入口解释 Tuqiang 事件、数据、状态和 UI。上下文卡沿用 SKILL.md；账号敏感链先读项目地图的 [账号模式事实](../../tuqiang-project-map/references/account-mode.md)。

## 三条链

    事件：操作/生命周期 → Widget → Command/Notifier/Controller → Repository
    数据：route/key/input → HTTP/cache/plugin → DTO/Model → State
    更新：state/Manager/cache → notify/derive → build/listener → UI/副作用

按时间拼合，但不要伪装成同步栈。每个 await、listener、post-frame 和 rebuild 都标出触发者。

## 从锚点向外追

| 方向 | 问题 |
|---|---|
| 向上 | 谁创建 Widget/Provider/Controller；哪个 route、builder、override、用户事件或 callback 让代码运行 |
| 向下 | 参数如何进入 Repository/HTTP/cache/plugin；DTO 如何映射；loading/error/empty 在哪发布 |
| 向旁 | 谁还写同一 State/Manager/cache；refresh、push、Timer、session reset 是否竞争 |
| 向外 | 哪个 watch/select/listener/mapper 消费哪个字段，最终哪个 Widget 或插件变化 |

遇到 contract provider、runtime callback、route registry 或 barrel 继续追到实际实现，不能停在接口。账号模式逐段记录分流、共享与汇合；both 必须有个人和企业两条证据。

## 状态与字段

对关键状态记录：

| 定义/类型 | family key 与 account scope | 依赖 | 写入 | 消费 | dispose/reset |
|---|---|---|---|---|---|

路由参数、family key、单次 action 参数、State 字段和 accountMode 分开解释。字段血缘写成“外部字段 → DTO/Model → State/mapper → Widget 字段”，并覆盖 null/default、错误和空态。

## 检索顺序

1. 精确 symbol 与引用；
2. route 常量、arguments 和最终 builder；
3. Provider/Notifier/Manager/Controller 声明与读写；
4. Repository/TQHttp/cache/plugin 与 DTO；
5. Widget 字段、visibility、loading/error/empty；
6. dispose/invalidate/reset、账号或 key 切换。

优先在相关 owner 目录用 rg -n，常见名加类型和路径约束。只引用当前行号和最小连续源码，不复制旧 reference 行号或敏感配置。

## Web 对照

先说明 Flutter/Riverpod 事实，再映射用户指定框架。完整实现必须逐段对应 operation、route/props、accountMode、keyed store/query、异步请求、状态写入、selector/effect、UI 和 cleanup；未要求时不展开两套代码。

## 完成

输出一句业务结论、上下文卡、三条链、状态身份表、字段血缘、逐跳证据、生命周期/竞态与未知边界。设备、地图和平台矩阵只在影响结论时从项目地图加载。
