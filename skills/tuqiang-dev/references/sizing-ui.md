# 尺寸适配与 UI 组件规范（sc）

## 1. sc 是什么

`core_base` 的 `TQSizeFit` 按 **375 宽设计稿**做等比缩放（类似 Vue 里的 postcss-px-to-viewport）：

```dart
scale = min(屏幕宽 / 375, 1.2)   // 大屏最多放大 1.2 倍，防平板/折叠屏失控
```

用法：任何设计稿标注的数值后面直接加 `.sc`：

```dart
import 'package:core_base/num_extension.dart';

Padding(padding: EdgeInsets.all(15.sc))
SizedBox(height: 8.sc)
Text('x', style: TextStyle(fontSize: 16.sc))
```

## 2. 规则

- 【必须】布局尺寸、间距、圆角、字号一律 `.sc`，禁止裸写 `15.0`；
- 专用快捷属性：
  ```dart
  23.verticalSpace      // SizedBox(height: 23.sc)
  8.horizontalSpace     // SizedBox(width: 8.sc)
  ```
- 安全区/系统栏高度不要手算，用现成封装：
  ```dart
  import 'package:core_base/tq_screen.dart';
  Screen.topSafeHeight       // 状态栏高度 (刘海/挖孔高度，相当于 env(safe-area-inset-top))
  Screen.bottomSafeHeight    // 底部安全区高度 (全面屏手势条，无手势条时贴心保底给 10.sc)
  Screen.navigationBarHeight // 状态栏 + AppBar 组合总高度
  ```
- **底部吸底按钮 / 弹窗安全区适配【高频踩坑】**：
  底部操作按钮或 BottomSheet 必须适配底部安全区（防止被 iPhone / 鸿蒙底部手势条遮挡），常用两种方式：
  ```dart
  // 方式 A：Padding 配合 Screen.bottomSafeHeight (最常用)
  Padding(
    padding: EdgeInsets.fromLTRB(16.sc, 8.sc, 16.sc, Screen.bottomSafeHeight),
    child: TQConfirmButtonWidget(text: '确定', onTap: () {}),   // core_ui 主按钮组件
  )

  // 方式 B：外层包裹 SafeArea (指定只保护底部)
  SafeArea(
    top: false,
    child: Padding(
      padding: EdgeInsets.all(16.sc),
      child: TQConfirmButtonWidget(text: '确定', onTap: () {}),
    ),
  )
  ```
- 字体缩放保护：如需屏蔽系统大字体的页面，可用 `Screen.fixedFontSize(16)`，但仅限确实会被顶爆的紧凑 UI；
- **图标与切图规范【严禁脑补】**：
  - 严禁私自使用 `Icons.xxx` 代替蓝湖设计稿切图；
  - 切图标注宽高一律加 `.sc`（如 `width: 24.sc, height: 24.sc`），跨 package 引用必须带 `package: 'feature_xxx'` 参数；
  - 切图索要 SOP、2x/3x 多倍图、命名与常量注册详见 [assets-guide.md](assets-guide.md)；
- **折叠屏/平板特殊场景**：仅在开发**视频播放器/监控摄像头全屏旋转**等场景才需判断折叠屏（参考 `bootstrap.dart` 的 `_isWideFoldable` 600.sc 阈值，大屏展开态不强制转横屏）；普通业务页面直接使用 `.sc` 即可（已内建 1.2 倍缩放上限保护，无需手动判断）。

## 3. UI 性能与布局防御规范（Flutter 官方最佳实践）

### ① 最大化利用 `const` 构造函数
- 不依赖变量的 Widget、Padding、SizedBox 等尽量加上 `const`；
- `const` Widget 在父组件 rebuild 时会被 Flutter 引擎直接复用，避免不必要的重新实例化和 GC 压力。

### ② Widget 粒度拆分（防过度 Rebuild）
- **不要把整个大页面的 UI 逻辑写在一个巨型 `build()` 方法里**；
- 频繁更新的部分（如倒计时、输入框、勾选框、高频动画）必须独立抽成单独的子 Widget 类（或配合 Riverpod `select` 局部监听），隔离刷新范围，避免导致整页或外层列表重复 build。

### ③ 布局约束与防溢出（Overflow Prevention）
- **无限高度/宽度冲突（Unbounded Constraints）**：在 `Column` 或 `ListView` 中直接嵌套另一个可滚动列表或自适应内容时，必须用 `Expanded`、`Flexible` 或明确高度的 `SizedBox` 包裹；
- **文字撑爆防护**：单行标题/描述必须设置 `maxLines` 和 `overflow: TextOverflow.ellipsis`，防止多语言翻译后文案变长引发 RenderFlex 溢出（黄黑斑马线）。

---

## 4. 先查 core_ui 再自己写组件

`packages/core/core_ui/lib/` 下已有大量成品，新页面前先翻一遍：

| 组件 | 用途 |
|---|---|
| `TQAppBar` | 统一标题栏 |
| `TQToast.show('xxx')` | 全局 toast |
| `TQAlert.*` | 十几种弹窗：showAlert / showEnsureAlert / showCustomContentDialog / showVersionUpgradeAlert… |
| `TQLoading` | 全局 loading（show/dismiss） |
| `EightRectLoading` | 加载动画 Widget |
| `TQNoDataWidget` | 空数据占位（`tipStr` 必填） |
| `TQConfirmButtonWidget` | 主操作按钮（自带防抖/进度） |
| `TQWarningAlert` | 警告弹窗 |
| `TQSheet` | 底部弹出面板 |
| `TQTabBar` | 标签栏 |
| `TQCalendarWidget` / `TQTimePickerWidget` | 日历/时间选择 |
| `TQScannerOverlay` | 扫码取景框 |
| `AgreementTextWidget` | 协议富文本 |

规则：

- 新通用组件进 `core_ui`（命名 `tq_xxx.dart`、类名 TQ 前缀）；只属于一个 feature 的组件放该 feature 的 `src/widgets/`；
- core_ui 没有统一 barrel 文件，import 具体组件文件即可，如 `import 'package:core_ui/tq_appbar.dart';`
- 颜色用 `core_base/tq_colors.dart` 的品牌色常量，不要散落 `Color(0xFF...)`。

## 5. 验证方式

- `dart run tool/project.dart analyze standard` 通过；
- 真机自检：小屏机型 + 平板/折叠屏展开态各看一遍，重点确认列表不被裁切、弹窗不溢出（overflow 黄黑条）。
