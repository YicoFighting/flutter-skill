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
- Toast、loading、空态、确认按钮等优先复用当前产品已经采用的公共组件；
- 途强单业务组件放 Feature；老鹰业务组件放对应 LY app-local owner；稳定无业务 UI 才进入 `core_ui`；
- 途强可沿用现有 TQ 品牌 token；老鹰品牌色、文案和图片由自身 skin/asset owner 提供，不能因复用 `core_ui` 泄漏途强视觉。

## 3. 布局防御

- `Column` 中的可滚动内容需要明确高度约束，通常使用 `Expanded`/`Flexible`；
- 文字受多语言影响时设置合适的 `maxLines`、`overflow` 或允许换行；
- 高频更新区域拆成子 Widget，或用 Riverpod `select` 缩小重建范围；
- `const` 用于确实不依赖运行时状态的对象；不要把它解释成“整棵树不会 rebuild”；
- 平板、折叠屏和大字体只在布局确实受影响时验证，不要求每个小改动都做完整设备矩阵。

## 4. 图标和资源

设计稿有对应切图时使用目标产品 owner asset 常量。缺少目标业务图片时先索要，不得用
Canvas、文字叠加、系统图标或生成图片替代；只有标准语义控件才考虑 `Icons.*`。资源路径、
package 参数和倍率目录遵循 [assets-guide.md](assets-guide.md)。

## 5. 验证

影响 UI 的行为改动：对应 package analyze 和必要的 Widget/页面验证；
影响公共 UI、尺寸工具或平台安全区：检查受影响产品的两个 target；公共能力检查四 target，
并按 ProductScope 运行 boundary，必要时补真机检查。
