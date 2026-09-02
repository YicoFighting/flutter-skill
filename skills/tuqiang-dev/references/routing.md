# 路由规范（双产品）

两个产品都保留当前原生命名路由体系，不因通用教程主动迁移 go_router，但 owner、registry 和 payload 类型彼此独立。

## 1. 途强智能

途强由 Feature 定义路由常量和唯一 builder，`apps/tuqiang_app` 的 `AppRouters`/`FeatureRouterRegistry` 聚合并保留必要 alias。Feature 不直接 import app 私有路由或其他 Feature 私有 `src/**`；登录、首页和跨业务导航通过 callback/config/contract 注入。

迁移既有路由必须保持：

- 历史路由字符串；
- arguments 类型、必填字段和默认行为；
- `Navigator.pop` 返回值及调用方等待逻辑；
- push/replace/removeUntil 栈行为；
- H5、scheme、push、native 入口；
- 定位刷新、session 清理、防截屏、系统栏等 route effect。

检查 Feature router、`AppRouters` alias、`nativeRouters`、registry 与 route effect；不能 Feature/app 同时保留两个 builder。

设备列表到详情必须额外枚举 `deviceType`、scene/category、cameraScene、服务/激活状态和最终 builder；再从各首页/详情的“更多详情/设备详情/更多设置”继续追一层，并核对父子 `GestureDetector`/`InkWell` 的实际 hit target，不能用文案或方法名猜 route。若发现多个 route leaf 而用户未说明全部或指定设备类型，按 [implementation-coverage.md](implementation-coverage.md) 先询问，不能把当前打开的 Page 当作全部范围。

## 2. 老鹰在线

老鹰使用 app-local `LYAppRouteRegistry` 聚合八个 `LYBusinessRouter`。registry 的 checked merge 会检查重复 owner、重复 path、缺 owner/path；新增或改路由不能绕过它。

- 路由、payload、result 使用 `LY*` typed contract，不把途强 Map/Model/`AppRouters` 类型带入；
- 页面和业务 Router 留在 `apps/laoying_app/lib/app/<owner>/`；
- `LYAppRouter` 负责应用级导航与 Repository 注入；
- 八个业务目录不互相直接 import，通过 Router/Coordinator/contract 协作；
- route 范围、阶段和返回契约以 `docs/laoying/route_contract.md` 与 Product Scope 为准；
- 设计稿出现入口不代表 route 已批准，阻塞/延期项先询问用户。

## 3. 验证

- 新增/修改均验证进入、参数、返回、重复进入和栈行为；设备详情族按已确认的每个 route leaf 分别记录；
- 途强运行 route contract、受影响 package/app analyze 与 `-ProductScope tuqiang`；
- 老鹰运行 registry/typed payload-result/owner contract tests 与 `-ProductScope laoying`；app boundary 检查器按 [testing.md](testing.md) 先排除当前 allowlist 冲突；
- 涉及 native/scheme/route effect 时验证对应宿主和真机；duplicate route 先全量搜索 registry/alias，不随意删除注册。
