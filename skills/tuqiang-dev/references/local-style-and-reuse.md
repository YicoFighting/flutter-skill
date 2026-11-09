# 本地封装优先与纯函数

## 先找已有能力

从目标 owner 和一个直接调用方开始，按业务语义查 **状态/selector → 函数/extension/formatter → 组件/路由/服务**，再查职责匹配的 shared/core/plugin 公开入口。有明确匹配即停止扩搜；不要只搜同名函数，也不要先写实现再找复用。

复用前确认输入、返回语义、账号/平台、语言与生命周期：`displayName` 可能已翻译，状态 provider 可能已含当前设备身份，不能再 `.tr`、复制一份 State 或在页面重算。没有匹配时简记缺口与新增位置即可。

| 检索锚点（使用前重查） | 能力与注意 |
|---|---|
| `shared_device/lib/shared_device.dart` | `deviceCatalogProvider`、`selectedDeviceProvider`、`deviceIdentityProvider` 及设备状态/展示 API |
| `shared_device/.../presentation/device_display_utils.dart`、`device_core_presentation.dart` | `TQDeviceDisplayUtils` 类型/图标/信号展示；部分方法内部 `.tr`，不能当纯计算或二次翻译 |
| `shared_location/.../presentation/location_presentation_mapper.dart`、`location_display_utils.dart` | 定位展示、日期/距离偏好 |
| `shared_location/.../widgets/map_panel_layout.dart`、`map_scrollable_bottom_card.dart` | `MapPanelLayout`/`MapDeviceHomeLayout`、地图底部卡片 |
| `core_base/lib/`：`safe_utils.dart`、`tq_validation_util.dart`、`tq_time_util.dart`、`tq_measurement_util.dart`、`tq_colors.dart` | `TCheck<T>`、校验、时间/`DurationParts`、单位、`TQColors`；逐方法核对空值与隐式 locale |
| `core_ui/lib/` 独立库：`tq_appbar`、`toast/tq_toast`、`tq_alert`、`tq_loading`、`tq_sheet`、`tq_confirm_button_widget`、`tq_no_data_widget`、`tq_mobile_scanner` | AppBar、Toast、弹窗、加载、Sheet、按钮、空态、通用扫码；按各自文件 import，不假设都由 `core_ui.dart` 导出 |
| `core_ui/lib/core_ui.dart` → `src/neutral` | `CoreAlert`、`CoreSheet`、`CoreEmptyState`、`CoreToast` 等中性组件与 `core_ui_theme` |
| `core_ui/lib/adaptive_layout.dart` | 分栏与自适应路由，见 [UI、路由与资源](ui-routing-assets.md) |
| feature 内组件 | 如 `feature_camera` 的 `TQVideoBottomSheet`、横屏控件；只在所属 feature 内复用 |

## 新增函数的边界

没有可复用能力时，新增的业务判断、映射、筛选、排序、格式化与派生状态写成纯函数：**相同显式输入得到相同输出，不改变输入或外部状态**。

- 传入所需值/不可变快照；不把 `BuildContext`、`WidgetRef`、可变 Manager 或任意 callback 当隐藏依赖容器。
- 不在计算中读 provider/单例、缓存、平台、当前时间、随机数或当前语言；由调用边界读取并传入 `now`、locale、单位、账号/设备快照等实际需要的值，不为假想需求加参数。
- 不发请求、写文件/缓存、发布 State、导航、Toast 或注册监听；不原地 sort/remove 输入集合或改 Model，输出值或新集合。
- 文案计算优先返回 code/key 与参数，由展示边界按 [国际化](i18n.md) 翻译一次；不在纯函数内部 `.tr`，不长期缓存译文。

例：剩余时长计算传入 `expiresAt` 与 `now`，不在内部调 `DateTime.now()`。请求、订阅、Widget 生命周期与状态发布本身有副作用：复用现有 Repository/Notifier/Controller/组件，只把计算部分抽为纯函数。不要借"纯函数"另造服务层、迁移存量或重写已有有状态 API。

## 取值与抽象只保留一处

数据兼容、字段优先级、空值与默认值集中到负责它的 parser/Model 或 presentation 函数；下游消费明确类型，不在 Model、formatter、Widget 逐层重复 `??`、空串判断、别名尝试或异常兜底。只有当前契约/真实数据有证据才加兼容，不猜历史版本；上游对象本身为空等独立缺失状态仍需处理。

同语义直接复用；缺一个必要参数时在 owner 内小幅扩展；只有局部消费者就保持局部（页面专属、无独立生命周期的子组件优先写成私有构建方法）。至少两个现存消费者、语义稳定且依赖方向正确才提共享抽象；禁止跨 feature 私有依赖、app 反向承载、空转发 wrapper 与假想的 base/service。

## 验证

业务计算用有意义的边界用例核对结果、重复调用一致、输入未被修改、只有显式参数变化才影响结果。状态与组件复用核对真实调用契约；不为简单转发和可逆样式造测试。范围见 [验证](testing.md)。
