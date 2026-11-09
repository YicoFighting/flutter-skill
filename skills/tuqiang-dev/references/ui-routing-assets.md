# UI 适配、路由与资源

## 分栏与尺寸

`apps/tuqiang_app/lib/app.dart` 用 `CoreAdaptiveLayout.sizingWidth` 更新 `TQSizeFit`；`core_ui/lib/adaptive_layout.dart` 负责分栏判定、铰链、pane 尺寸和自适应路由。不要在页面另写"宽度大于某值"或固定半屏逻辑。

- `CoreAdaptiveLayout.canSplit/panes`：窗口与安全区决定分栏，断点是逻辑像素，不乘 `.sc`。
- `CoreAdaptiveSections`：同页分区重排；`CoreAdaptiveMaster` / `CoreAdaptivePageRoute`：主从路由分栏。
- `CorePaneViewport` 为子页面提供 pane 内 `MediaQuery`；页面尺寸与安全区取局部 `LayoutBuilder` / `MediaQuery.of(context)` / `SafeArea`，`Screen` 是整窗，不能代替 pane 尺寸。
- 分栏后主页面可能仍可见，不能只用 `route.isCurrent` 推断可见性，沿 `CoreAdaptiveMaster.isVisible` 与 owner 的刷新契约；不加第二个 Navigator，不靠换 key 重建规避尺寸变化。
- 地图面板先查 `MapPanelLayout` / `MapDeviceHomeLayout` 与 `map_scrollable_bottom_card.dart`。

`TQSizeFit` 以 375 设计宽、最大 1.2 倍缩放。按项目规范，设计尺寸（字号、宽高、间距、圆角、定位、图标）用 `.sc`；系统 inset、约束、比例、flex、动画时长与算法值不机械缩放。可选尺寸参数用 null 默认值、在使用处 `.sc`，不重复缩放调用方已缩放的值。颜色用 `TQColors`/主题语义变量，不散落色值。

build 只读/订阅状态，副作用放事件、初始化或 listener；保持组件身份与资源 owner。公共 AppBar、Toast、弹窗、Sheet、空态、扫码先按 [本地复用](local-style-and-reuse.md) 选已有封装。

## 路由

沿用命名路由，不迁移 `go_router`。Feature 定义路由和 builder，`AppRouters` 与 `FeatureRouterRegistry` 装配。`StrongApp` 通过 `onGenerateRoute → AppRouters.generateRoute`，按 `_paneRoutes` 选 `CoreAdaptivePageRoute`，摄像头/视频等保留 `MaterialPageRoute`；新增页面先查注册、分栏白名单与全屏例外，不自行换 route 类型。

只检查本次改变的契约：route 字符串与唯一 builder、arguments 类型与默认值；`pop` result、等待方与 push/replace/removeUntil 栈行为；H5/scheme/push/native 入口与 route effect（定位刷新、session、系统栏、方向）；分栏可见性、返回/切设备时关闭详情与主页面刷新。改设备分流时追到最终 Page 与真实点击区域，范围按 [实施覆盖](coverage.md)。

## 设计源与资源

- 有设计稿/切图按其尺寸、颜色、字体、状态还原（Figma/蓝湖规则见业务仓库 `.codex/skills`，`DESIGN.md` 记录已确认的页面约定）；无设计稿时沿目标 feature 相邻成熟页面与 `core_ui`。
- 切图倍率与目录按 `tuqiang-lanhu-image-assets`：父目录放 iOS @2x、同级 `3.0x/` 放同名 @3x，不建 `2.0x/`，pubspec 只声明父目录；文件名不带 `@2x/@3x` 后缀。
- 缺少业务素材时先索要并确认选择条件；未经授权不用 Canvas/运行时叠字、系统图标/emoji、生成或近似重绘、占位图冒充最终交付。
- 单 feature 资源放 `packages/feature/<owner>/assets`，两个以上稳定消费者才考虑 `packages/assets_common`；路径经 owner 已有常量/Resolver 暴露。迁移资源时搜 Dart、pubspec、Android、iOS、OHOS 引用，整组迁移。地图标记等原生图标在三端原生资源中维护。
- 语言/状态/账号变体需要明确选择条件；个人/企业资源不同时验证切账号不沿用旧缓存。

## 验证

长文案、换行、按钮宽度、大字体按当前可达语言检查；折叠/分栏改动看切换前后的状态保持、局部尺寸、安全区、滚动与点击区域（公共封装测试锚点 `core_ui/test/adaptive_layout_test.dart`）。资源核对路径、大小写、pubspec、倍率配对与每种变体实际选中的文件。路由/资源改变装配或依赖边界时才加宿主分析或架构检查，见 [验证](testing.md)。
