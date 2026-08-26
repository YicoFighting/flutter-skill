# 布局与 UI 组件 · 前端深度对照表

> 主文档见 [../SKILL.md](../SKILL.md)。本文件展开 §1 的「UI 与布局」部分。
> Flutter 没有 CSS，所有样式都是"套 Widget"，但布局心智模型就是 Flexbox + Grid + 绝对定位。

## 1. 布局组件对照表

| CSS / Web | Flutter | 备注 |
|---|---|---|
| `display: flex; flex-direction: column` | `Column` | 纵向排一列 |
| `flex-direction: row` | `Row` | 横向排一行 |
| `flex: 1` | `Expanded` | 瓜分剩余空间 |
| `flex: 1; flex-shrink: 0`（按内容收缩） | `Flexible` | 子项可以比分配额小 |
| 主轴对齐 `justify-content` | `mainAxisAlignment` | `center / spaceBetween ...` |
| 交叉轴对齐 `align-items` | `crossAxisAlignment` | `center / stretch ...` |
| `gap`（flex 间距） | `SizedBox(width:, height:)`，或按当前 Flutter SDK 使用 Flex 的 `spacing` | 途强现有代码以 SizedBox 和项目组件为准，不要假设所有 SDK 都支持同一 API |
| `padding` | `Padding` 或 `Container(padding:)` | |
| `margin` | 外面再套一层 `Container(margin:)` | Flutter 只有 padding，margin 是"外面的 padding" |
| `position: relative + absolute` | `Stack` + `Positioned` | 图层堆叠（角标、浮层按钮） |
| `overflow: auto`（纵向） | `SingleChildScrollView` | 单屏内容可滚动 |
| `v-for` + 虚拟滚动 | `ListView.builder` | 只渲染可视区，itemCount = 数据条数 |
| `display: grid` | `GridView.count/crossAxisCount` | crossAxisCount ≈ grid-template-columns 的份数 |
| `width/height: %` | `FractionallySizedBox` / `Expanded` | 百分比要靠弹性或分数盒 |

## 2. 「容器三兄弟」怎么选

```dart
Container(...)   // 万能 div：颜色、宽高、内外边距、圆角、装饰一把梭
SizedBox(...)    // 空 div：只占位（最常用作间距）
DecoratedBox(...)  // 只管装饰不管布局
```

大白话：**「随手写个 `div` 就是 Container；只想留白就 SizedBox；别嵌太深，十层嵌套的
Widget Hell 谁看谁晕。」**

## 3. 一个典型页面骨架翻译

```dart
Scaffold(                                  // 页面 Layout：顶栏 + 内容区
  appBar: AppBar(title: const Text('宠物详情')),
  body: Column(                            // flex-direction: column
    children: [
      Expanded(child: ListView.builder(...)),   // flex:1 的滚动列表
      SafeArea(child: submitButton),            // 底部安全区，≈ env(safe-area-inset-bottom)
    ],
  ),
)
```

一句话总结：**「一个标准页面 = Layout 壳 + 一列布局 + 弹性撑满的滚动区，跟你在 Vue 里
Layout 组件包 `<router-view>` 加 flex 布局完全同构。」**

## 4. 主题与样式变量

| Web | Flutter |
|---|---|
| `:root { --primary }` CSS 变量 | `ThemeData(colorScheme:)` 全局主题 |
| Tailwind class | 官方组件自带样式 + `style:` 参数 |
| `@media (prefers-color-scheme)` | `ThemeMode.system` 深色模式跟随系统 |

## 5. 常见坑速查

| 报错现象 | 大白话解释 |
|---|---|
| `RenderFlex overflowed by N pixels` | flex 子项内容超出容器还不想被裁剪——加 `Expanded` / `Flexible` / 外层套滚动 |
| Column 里塞 ListView 不显示 | 「无界高度」冲突：无限高的爹没法给列表量高度，给 Expanded 或固定高 |
| 图片不显示 | 忘了在 pubspec 注册 assets，≈ webpack 没配 loader |
