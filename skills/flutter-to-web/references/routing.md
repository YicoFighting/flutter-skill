# Tuqiang 路由导航

路由链必须追齐：

    用户/系统入口 → route 常量 → Navigator/封装 → arguments
    → app/feature registry → builder → Page
    → pop result / observer / refresh / analytics 等 effect

不能停在 route string、barrel 或 contract。核验 push/pushReplacement/popUntil 等栈语义、arguments 的类型/默认值/null 处理、最终 Page 以及返回后谁消费 result。

分开五类身份：

| 值 | 作用 |
|---|---|
| route 参数 | 把页面上下文送到入口 |
| family key | 选择 Provider 实例 |
| accountMode | 决定账号身份与可能的请求/UI 分支 |
| action 参数 | 控制一次命令 |
| State 字段 | 留存请求或计算结果 |

Web 中可近似为 router params/location state → component props → keyed store/query → navigation effect，但最终以当前 Dart builder、Provider override 和副作用证据为准。

设备详情任务必须继续追 deviceType/scene/cameraScene 到最终 Page 和点击区域，不能用第一个 route 代表所有设备。
