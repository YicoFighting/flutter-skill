# Tuqiang 异步与网络链

只解释当前代码实际经过的 Repository、TQHttp、cache、database 或 plugin；不要套统一分层模板，也不要展示 endpoint、Token、Key、证书或生产配置。

## 请求链

逐跳说明：

    UI/route/family key
    → Command/Notifier/Manager
    → Repository 或直接 TQHttp/plugin
    → path/method/header/DTO symbol
    → ResultModel/TCheck/fromJson
    → State/cache
    → Widget/listener

记录参数来源、默认值、序列化、响应字段映射和 loading/success/empty/error。字段血缘必须落到最终 Widget 使用的属性。

## 账号身份

请求可能通过 isEnterprise、DeviceAccountMode、personal/enterprise Repository/path、identifier 或 callback 分流。发起时记录 accountMode/session/device/query scope；await 后发布前验证仍是同一身份。cache、pending Future 和 family key 也必须隔离，否则 owner 仍 mounted 也会串数据。

完整判定读项目地图的 [账号模式事实](../../tuqiang-project-map/references/account-mode.md)，不用 accountType、target 或调用目录猜模式。

## 异步边界

区分四件事：

| 问题 | 常见证据 |
|---|---|
| owner 存活 | mounted、StateNotifier mounted、active/lifecycle epoch |
| 结果新鲜 | generation/requestVersion |
| 身份匹配 | account/device/family key/session 快照 |
| 资源释放 | cancel/close/removeListener/unregister |

检查 success、catch、finally、whenComplete、Timer/Stream 和 plugin callback。FutureProvider dispose 后会忽略旧状态发布，但不会自动取消底层请求或外部副作用。具体实现规则统一读取 tuqiang-dev 的 [异步生命周期](../../tuqiang-dev/references/async-lifecycle.md)。

## Web 心智

Future ≈ Promise，Repository ≈ API client/queryFn，AsyncValue ≈ query 状态。generation 类似 request id，family key 类似 query key，accountMode/session 必须进入身份。类比不能省略当前 Dart 的请求、映射、发布和清理证据。
