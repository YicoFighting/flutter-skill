# 本地封装优先与纯函数

## 先找已有能力

从目标 owner 和一个直接调用方开始，按业务语义查已有 **状态/selector → 函数/extension/formatter → 组件/路由/服务**，再查职责匹配的 shared/core/plugin 公开入口。有明确匹配就停止扩搜；不要只搜同名函数，也不要先写实现再找复用。

复用前确认输入、返回语义、账号/平台、语言与生命周期。例如 `displayName` 可能已翻译，状态 provider 可能已有当前设备身份；不能再 `.tr`、复制一份 State 或在页面重新计算。没有匹配时，简记缺口与新增位置即可，不要求采样报告。

| 当前检索锚点（使用前重查） | 能力与注意事项 |
|---|---|
| `packages/shared/shared_device/lib/shared_device.dart` | 公开的 `deviceCatalogProvider`、`selectedDeviceProvider`、`deviceIdentityProvider` 及设备状态/展示 API；沿已有订阅和写入路径 |
| `packages/shared/shared_device/lib/src/presentation/device_display_utils.dart` | `TQDeviceDisplayUtils` 已有类型、图标、信号展示；部分方法内部 `.tr`，不能当纯计算照搬或二次翻译 |
| `packages/core/core_base/lib/safe_utils.dart`、`tq_validation_util.dart`、`tq_time_util.dart` | `TCheck<T>`、`TQValidationUtil`、`TQTimeUtil`、`DurationParts`；逐方法核对空值、格式与隐式 locale，名称不证明纯度 |
| `packages/core/core_ui/lib/` | `TQAppBar`、`TQToast`、`TQConfirmButtonWidget` 与 `CoreEmptyState`；按已有公开库入口使用，不假设全部由 `core_ui.dart` 导出 |
| `packages/core/core_ui/lib/adaptive_layout.dart` | `CoreAdaptiveLayout`、`CoreAdaptiveSections`、`CorePaneViewport`、`CoreAdaptiveMaster`、`CoreAdaptivePageRoute`；分栏与路由复用这些契约，详见 [UI](sizing-ui.md) / [路由](routing.md) |

## 新增函数的边界

没有可复用能力时，新增业务判断、映射、筛选、排序、格式化与派生状态必须是纯函数：**相同显式输入得到相同输出，不改变输入或外部状态**。

- 传入所需值/不可变快照；不要把 `BuildContext`、`WidgetRef`、可变 Manager 或任意 callback 当作隐藏依赖容器。
- 不在计算中读 provider/单例、缓存、平台、当前时间、随机数或当前语言；由已有调用边界读取并传入 `now`、locale、单位、账号/设备快照等实际需要的值，不为假想需求加参数。
- 不发请求、写文件/缓存、发布 State、导航、Toast 或注册监听；不原地 sort/remove 输入集合或改 Model。内部局部变量可以变化，输出应是值或新的集合。
- 文案计算优先返回语义 code/key 与参数，由响应式展示边界按 [国际化](i18n.md) 翻译一次；不要在新纯函数内部 `.tr`，也不要长期缓存译文。
- 例如剩余时长计算传入 `expiresAt` 和 `now`，不要内部调用 `DateTime.now()`；格式化若依赖 locale/时区也需显式输入，不能仅把旧全局调用包进新函数。

请求、订阅、Widget 生命周期和状态发布本身有副作用：优先复用现有 Repository/Notifier/Controller/组件；需求确需新增接线时，仅在这些 owner 中保留必要副作用，计算部分仍抽为纯函数。不要用“纯函数”名义另造服务层、迁移存量或把 IO 包装器称为纯函数。复用已存在的有状态 API 不要求重写整个 API。

## 取值和抽象只保留一处

数据兼容、字段优先级、空值与默认值按 [i18n 的展示边界](i18n.md) 集中到负责它的 parser/Model 或 presentation 函数；标准化后下游消费明确类型，不在 Model、formatter、Widget 逐层重复 `??`、空串检测、别名尝试或异常兜底。只有当前契约/真实数据有证据才添加兼容，不猜测历史版本。上游对象本身为空等独立缺失状态仍需处理；不要把所有 `??` 都判为重复。

同语义直接复用；现有能力缺少一个必要参数时在 owner 内小幅扩展；只有局部消费者就保持局部。至少两个现存消费者、共同语义稳定且依赖方向正确时才提共享抽象。跨包只用公开 API，禁止 Feature 私有横向依赖、app 反向承载、空转发 wrapper 与假想未来 base/service。

## 验证

业务计算用有意义的边界用例验证结果，并检查相同输入重复调用一致、输入集合/对象未变、依赖环境变化时只有显式参数改变才影响结果。优先已有测试，不为简单转发和可逆样式造测试；状态与组件复用核对其真实调用契约。验证范围见 [测试规范](testing.md)。
