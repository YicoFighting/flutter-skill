# Tuqiang 完整需求追踪

从可观察操作恢复事件、异步数据、状态拓扑与 UI/插件消费。上下文卡沿用 SKILL.md；账号证据读 [account-mode.md](account-mode.md)，平台/地图/设备读 [variant-surface.md](variant-surface.md)。

把问题写成：“当某 accountMode 用户触发事件时，输入如何经过路由、状态和数据层到达可观察终点；失败、切换、退出或旧结果返回时怎样处理？”

## 七段链

| 段 | 必查事实 |
|---|---|
| 入口 | onTap/onPressed/onRefresh、initState/build gate、route/native handler、observer、Timer 或 session 事件；记录账号、用户/device、平台和参数 |
| 页面装配 | route 常量、arguments 来源/fallback、Navigator、bootstrap override、feature router、最终 builder 与 effect |
| 状态身份 | Provider/Manager/Controller/setState 的定义、family key/account scope、写入者、订阅者、生命周期/reset |
| 数据/资源 | Repository/HTTP/cache/plugin、请求 DTO、模式选择、响应映射；asset 文件 → pubspec → 常量 → 消费端 |
| 异步发布 | loading/success/empty/error、await、generation、owner、account/device 身份、pending 去重和缓存回写 |
| UI/插件 | 状态字段到 Text/Image/可见性/按钮/marker/相机/原生参数的最终消费及中间 mapper/gate |
| 失效恢复 | 页面离开、切 key、dispose、autoDispose/keepAlive、invalidate、语言/账号切换与 logout；下次复用、恢复或重请求 |

设备入口还要枚举 deviceType、scene/category、cameraScene、服务/激活/分享状态，并追到“更多详情/设置”后的最终 Page。资源不存在就报告缺失，不能造替代品。

## 时间与变体

分开四条时间线：

    同步事件：用户操作 → 方法 → 命令/状态入口
    调度：状态发布 → listener → post-frame/刷新
    异步数据：Repository → HTTP/plugin → 映射 → 新状态
    响应式消费：watch/select/listener → rebuild → UI/插件

不要压成“onTap → network → UI”。mounted 不证明结果仍属于当前账号或设备。

- 账号相关：personal/enterprise 分别核验，或给出单侧不涉及证据。
- 设备相关：列当前可达 route leaf，不用第一个页面代表全部。
- 主地图相关：标注 TQMapUseSceneType，并保留 Android/iOS 各三源与 HarmonyOS Map Kit 七个候选。
- 普通局部业务不展开无关矩阵。

## 搜索与证据

优先在 apps/tuqiang_app 与 packages 用 rg -n 组合搜索入口 symbol、route/Page、Provider/Controller、isEnterprise/identity、Repository/TQHttp/DTO、状态字段、dispose/invalidate 和资源名；常见 symbol 加目录与类型约束，避免无界宽搜。

每个关键阶段引用“相对路径:当前 1-based 行号 + symbol + 最小连续源码”，并解释它证明的输入、输出与下一跳。API 只写常量名和语义，不展示 endpoint、Token、Key、证书或签名。

## 输出

1. 一句话说明 accountMode、入口、owner、状态和终点。
2. 四条时间线与状态身份表。
3. 请求/资源、生命周期和按顺序排列的源码证据。
4. 实际涉及的账号、平台、设备与 loading/error 分支。
5. 未核验项；需用户决策时只提一个最小问题。

完成时，根目录和起终点明确；状态定义/key/写入/消费/reset、数据参数/边界/映射、资源声明/消费、旧结果处理和相关变体都有实时证据。
