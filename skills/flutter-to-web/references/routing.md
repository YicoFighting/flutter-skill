# Tuqiang 路由导航

解释页面去向或传参时，追到实际 builder/Page；仅有 route string、barrel 或 contract 不足以确认行为：

    用户/系统入口 → 导航封装与 arguments → registry/builder → Page

返回刷新、副作用或栈行为属于问题时，再追 pop result、observer、pushReplacement/popUntil 等调用。无需为简单页面入口枚举全部导航 effect。

区分 route 参数（页面上下文）、family key（Provider 实例）、accountMode（账号分支）、action 参数（一次命令）和 State 字段（留存结果）。只展开当前入口经过的类型、默认值和转换。

Web 可近似为 router params/location state → component props → keyed store/query；仍以当前 Dart builder 和 Provider override 为证据。设备页面若受 deviceType/scene/cameraScene 分流影响，继续追到对应 Page 与点击区域，不用第一个 route 代表所有设备。
