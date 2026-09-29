# 尺寸适配与 UI

## 先复用当前分栏封装

当前大屏链路由 `apps/tuqiang_app/lib/app.dart` 使用 `CoreAdaptiveLayout.sizingWidth` 更新 `TQSizeFit`；`core_ui/adaptive_layout.dart` 负责分栏判定、铰链、pane 尺寸和自适应路由。不要在页面另写“宽度大于某值”或固定半屏逻辑。

- `CoreAdaptiveLayout.canSplit/panes`：当前窗口与安全区决定分栏；断点使用逻辑像素，不乘 `.sc`。
- `CoreAdaptiveSections`：同一页面分区重排；`CoreAdaptiveMaster` / `CoreAdaptivePageRoute`：主从路由分栏。按当前 owner 已有模式复用。
- `CorePaneViewport`：为子页面提供 pane 内的 `MediaQuery`。页面宽高和安全区优先取局部 `LayoutBuilder` / `MediaQuery.of(context)` / `SafeArea`；`Screen` 读取整窗，不能作为 pane 尺寸替代。
- 地图面板先查 `packages/shared/shared_location/lib/src/presentation/widgets/map_panel_layout.dart` 的 `MapPanelLayout` / `MapDeviceHomeLayout` 与 `map_scrollable_bottom_card.dart`；路径以当前 checkout 为准。

分栏后主页面可能仍可见，不能用 `route.isCurrent` 单独推断可见性；沿 `CoreAdaptiveMaster.isVisible` 与现有 owner 的监听刷新契约。不要增加第二个 Navigator 或通过换 key 重建状态规避尺寸变化。

## 设计尺寸与组件

`core_base/tq_size_fit.dart` 的 `TQSizeFit` 当前以 375 设计宽和 1.2 最大比例缩放。`.sc` 用于设计间距、布局尺寸、圆角和字号；系统 inset、约束、比例、flex、动画时长和算法值不机械缩放，也不在页面重复初始化全局比例。

公共 AppBar、Toast、按钮、空态和 Sheet 先按 [本地复用](local-style-and-reuse.md) 核对已有组件和公开入口。build 只读/订阅状态，副作用留在事件/初始化/listener；保持原有组件身份和资源 owner。

## 文案与验证

可见文本按 [国际化](i18n.md) 处理，布局按当前可达语言检查长文本、换行、按钮宽度与大字体；仅当本次范围可达 RTL locale 时检查方向，不固定要求已从选择列表移除的语言。业务资源见 [资源规范](assets-guide.md)。

按 [测试规范](testing.md) 选择相关 analyze、既有 Widget 测试或视觉检查；折叠/分栏改动重点看切换前后的状态保持、局部尺寸、安全区、滚动和点击区域。公共自适应封装的现有测试锚点为 `packages/core/core_ui/test/adaptive_layout_test.dart`，不因页面样式变化自动跑全平台构建。
