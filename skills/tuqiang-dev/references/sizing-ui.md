# 尺寸适配与 UI

`core_base` 的 `TQSizeFit` 以当前项目约定的 375 宽设计稿为基准，最大缩放约 1.2。`.sc` 主要用于设计稿布局尺寸、间距、圆角和字号：

```dart
Padding(padding: EdgeInsets.all(15.sc))
SizedBox(height: 8.sc)
Text('标题'.tr, style: TextStyle(fontSize: 16.sc))
```

系统栏高度、边框宽度、动画时长、算法参数、比例、flex、约束和 API 数值不机械套 `.sc`。`horizontalSpace/verticalSpace` 也只表达设计间距。

## 安全区与公共 UI

- 底部按钮、BottomSheet、输入区使用 `SafeArea` 或 `Screen.bottomSafeHeight`；
- 不手算刘海、手势条和系统栏，优先用现有 `Screen` 封装；
- 新页面先查 `packages/core/core_ui/lib`，优先实际存在的 `TQAppBar`、Toast、loading、空态和按钮；
- 单业务组件放 Feature，稳定无业务 UI 才进入 `core_ui`；
- build 只读取/订阅状态，副作用沿现有事件、初始化或 listener；
- 高频更新区域可拆子 Widget 或用 Riverpod `select`，不要把 `const` 解释为永不 rebuild。

## 多语言布局

任何可见文本先执行 [i18n 流程](i18n.md)。为德语等长文本检查换行、`maxLines/overflow` 和按钮宽度；Arabic 检查 RTL、方向图标、对齐与数字/单位。不要用固定高度掩盖翻译溢出。

## 资源与验证

设计稿有切图时使用真实 owner asset；缺业务图片按 [资源规范](assets-guide.md) 索要，不以 Canvas、叠字、系统图标或生成图替代。影响 UI 时运行对应 package analyze/Widget 测试，并按风险检查小屏、宽屏/折叠态、大字体、Android/iOS/HarmonyOS 和个人/企业模式。
