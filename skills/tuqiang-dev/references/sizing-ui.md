# 尺寸适配与 UI 组件规范（sc）

## 1. 设计尺寸

`core_base` 的 `TQSizeFit` 以 375 宽设计稿为基准，最大缩放约为 1.2：

```dart
Padding(padding: EdgeInsets.all(15.sc))
SizedBox(height: 8.sc)
Text('标题', style: TextStyle(fontSize: 16.sc))
```

`.sc` 主要用于设计稿中的布局尺寸、间距、圆角和字号。系统栏高度、边框宽度、动画时长、
算法参数、比例、flex、约束和 API 数值不应机械套 `.sc`。使用 `horizontalSpace`、
`verticalSpace` 时也先确认它表达的是设计间距。

## 2. 安全区和公共 UI

- 底部按钮、BottomSheet 和输入区域用 `SafeArea` 或 `Screen.bottomSafeHeight`；
- 不手算刘海、手势条和系统栏高度，优先使用 `Screen` 封装；
- 新页面先查 `packages/core/core_ui/lib/`，统一顶栏用实际存在的 `TQAppBar`；
- Toast、loading、空态、确认按钮等优先复用 `TQ*` 组件；
- 只属于一个 feature 的组件放 feature；跨 feature 且稳定的组件才进入 `core_ui`；
- 品牌色优先使用 `core_base/tq_colors.dart`。

## 3. 布局防御

- `Column` 中的可滚动内容需要明确高度约束，通常使用 `Expanded`/`Flexible`；
- 文字受多语言影响时设置合适的 `maxLines`、`overflow` 或允许换行；
- 高频更新区域拆成子 Widget，或用 Riverpod `select` 缩小重建范围；
- `const` 用于确实不依赖运行时状态的对象；不要把它解释成“整棵树不会 rebuild”；
- 平板、折叠屏和大字体只在布局确实受影响时验证，不要求每个小改动都做完整设备矩阵。

## 4. 图标和资源

设计稿有对应切图时使用 owner asset 常量；没有对应切图且是标准语义控件时才使用
`Icons.*`。资源路径、package 参数和倍率目录遵循 [assets-guide.md](assets-guide.md)，不要假定
所有 feature 都有完全相同的 2x/3x 目录。

## 5. 验证

影响 UI 的行为改动：对应 package analyze 和必要的 Widget/页面验证；
影响公共 UI、尺寸工具或平台安全区：standard/OHOS analyze，必要时补 boundary/真机检查。
