# 目录与归属决策

## 1. 先确定产品，再确定 owner

当前仓库是两个产品、四个宿主 target：

```text
apps/standard ─┐                         apps/laoying_standard ─┐
               ├─> apps/tuqiang_app                            ├─> apps/laoying_app
apps/ohos ─────┘        ↓                apps/laoying_ohos ─────┘        ↓
                 feature_* → shared_*                    LY app-local business
                         \      /                              ↓
                       core / plugins / adapter / public shared_*
```

实际依赖以当前 `pubspec.yaml`、Product Scope 和边界测试为准。不要因为两个产品有相似页面，就把途强 Feature 的业务实现、路由、资源或运行时配置带入老鹰在线。

| 位置 | 主要职责 | 新代码边界 |
|---|---|---|
| `apps/standard` / `apps/ohos` | 途强智能 Android/iOS 与 HarmonyOS 宿主、渠道和平台配置 | 不放共享业务 |
| `apps/tuqiang_app/lib/app` | 途强启动、ProviderScope、路由聚合、session、平台注入与 App 壳 | 新业务优先回到真实 Feature owner |
| `packages/feature/feature_*` | 途强单一业务域的页面、状态、Model、Repository、路由与资源 | 不依赖 app 或其他 Feature 私有 `src/**` |
| `packages/shared/shared_account` | 用户会话与偏好 | 不承载无关设备或页面状态 |
| `packages/shared/shared_device` | 设备身份、目录、能力与选择 | 不承载定位、命令或媒体的私有实现 |
| `packages/shared/shared_location` | 定位、地址、逆地理编码与相关状态 | 不反向依赖 Feature |
| `packages/shared/shared_command` | 设备命令、远程设置与历史 | 保持公开契约稳定 |
| `packages/shared/shared_message` | 消息、告警、摘要与已读状态 | 不放单页面 UI |
| `packages/shared/shared_media` | 播放、进度、文件与下载 | 平台实现仍经 plugin/adapter |
| `packages/shared/shared_advertising` | 广告共享能力 | 不泄漏产品品牌资源 |
| `packages/shared/shared_activity` | 活动统计、图表、Controller 与 API paths | 不承载应用壳编排 |
| `apps/laoying_standard` / `apps/laoying_ohos` | 老鹰在线标准端与 HarmonyOS 宿主 | 产品标识、签名、权限与渠道独立 |
| `apps/laoying_app/lib/app` | 老鹰应用、会话、Router、Repository、i18n、资源与业务 owner | 不新增 `feature_laoying*`，不 import 途强 Feature 或 `package:tuqiang/` 业务入口 |
| `packages/core/core_*` | 网络、i18n、UI、尺寸等公共基础能力 | 不放具体产品业务 |
| `packages/plugins/tq_*` / `packages/adapter` | 原生插件和平台适配 | 先复用公开能力，再评估新通道 |
| `packages/assets_common` | 途强共享资源 | 老鹰页面不得运行时引用 |

旧 `packages/shared/shared_business` 已冻结拆分：不把它当成仓库身份标记，也不新增文件、依赖或 import。新增跨 Feature 能力必须落到职责匹配的八个 `shared_*` 之一；没有稳定共同语义时留在原 owner。

## 2. 两类业务 owner

### 途强智能

单一业务域由对应 `feature_*` owner。跨 Feature 导航由 Feature 暴露 callback/config/contract，`apps/tuqiang_app` 负责装配；不要为跳转形成 Feature 横向私有依赖。

### 老鹰在线

业务 owner 固定在 `apps/laoying_app/lib/app/<owner>/`：

```text
auth  gps  pet  mine  overview  message  device_share  device_management
```

业务目录不互相直接 import，通过应用级 Router、Coordinator 或 contract 协作。`session`、`router`、`contracts`、`coordinators`、`i18n`、`infrastructure`、`assets` 和 `skin` 是应用级 owner；`home` 属于 App 壳，不等于第九个可任意承载业务的目录。

老鹰能按公开 API 复用 core/shared/plugin/adapter 的底层能力，但不能复用途强 Feature 页面、业务 Controller、品牌资源、凭据或运行时配置。是否允许某项能力，先看 `docs/laoying/product_scope_matrix.md` 及对应 route/API/resource/native contract；源码存在或设计图出现都不代表范围已批准。

## 3. 找 owner 的顺序

1. 写明目标产品、用户可观察行为和可证伪验收；不唯一时按 [requirement-clarification.md](requirement-clarification.md) 询问；
2. 找当前唯一 builder、route、Controller/Provider、Repository、asset 和测试；
3. 对老鹰核对 Product Scope 与相应 contract；对途强核对 Feature split/迁移边界；
4. 找目标 owner 的公开入口和已有复用能力；
5. 在同一产品、同一 owner 抽样 2–4 个成熟同类实现，再看同产品相邻 owner；
6. 检查包外调用方、pubspec、测试、宿主注入和受影响平台；
7. 只有 owner 已完整转移且契约有测试保护时才迁移，避免两套事实来源。

目录和命名是局部证据，不是全仓统一任务。途强可以同时存在 `TQ`/`Tq`/无前缀及多种 Riverpod/Manager 模式；老鹰当前以 `LY` app-local 类型、`LYAppProvider` 和 ChangeNotifier Controller 为主。不得为了“一致”跨产品套脚手架。

## 4. 边界与门禁

- 途强业务下沉需保持路由字符串、arguments、返回值、H5/scheme/push/native 入口和 route effect；
- 途强 Feature 资源整体归 owner，共享资源仅在确有多模块消费者时进入 `assets_common`；
- 老鹰可见资源必须复制为产品独立 asset，并由 `LYAppAssets`/业务 Resolver 访问；
- 老鹰八个业务目录不得互相直接 import，不能依赖 `feature_*` 或途强 app；
- 新依赖进入实际 owner 的 pubspec；只有受影响 target 的 lockfile 可以变化；
- `tool/check_migration_boundaries.ps1 -ProductScope tuqiang` 检查只影响途强的改动，`-ProductScope laoying` 检查只影响老鹰的改动；core/shared/plugin 改动先枚举两产品消费者，同时影响两产品调用或公共 contract 时才使用 `-ProductScope all`。

迁移范围以当前脚本、`docs/feature_business_package_split_plan.md` 和老鹰 Product Scope 文档为准，不凭本文件概括扩大范围。

## 5. 快速决策

| 想新增的内容 | 优先位置 |
|---|---|
| 途强宠物页面的 API/Model/Provider/图片 | `packages/feature/feature_pet` |
| 途强多 Feature 稳定共享的用户、设备、定位等能力 | 职责匹配的 `shared_account/device/location/...` |
| 老鹰 GPS 页面、Controller、Repository、路由或图片 | `apps/laoying_app/lib/app/gps` 及 `assets/images/gps` |
| 老鹰应用会话、全局刷新或业务 reset 编排 | `apps/laoying_app/lib/app/session` / `coordinators` |
| 请求、翻译、通用无业务 UI | 对应 `packages/core/core_*`；产品运行时配置仍留 app |
| 蓝牙、地图、文件、推送等原生能力 | 现有 plugin/adapter；老鹰先确认 Product Scope/native contract |
| 缺失的品牌或业务图片 | 先索要素材，不用 Canvas、系统图标或生成图片替代 |
