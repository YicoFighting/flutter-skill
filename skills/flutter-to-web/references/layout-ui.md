# Tuqiang 布局与 UI 的 Web 对照

Flutter 约束由父向子传，尺寸由子向父回传，ParentData 决定位置；它更接近显式 layout protocol，而不是浏览器普通文档流。

| Flutter | Web 心智 |
|---|---|
| Row/Column + Expanded/Flexible | flex 与 grow/shrink |
| Stack/Positioned | position relative/absolute |
| ListView/CustomScrollView | 滚动容器/虚拟列表 |
| LayoutBuilder/MediaQuery | container/viewport query |
| SafeArea | safe-area inset |

解释实际页面时只追影响目标字段的约束：父约束、主/交叉轴、scroll owner、SafeArea、keyboard inset、文本换行/ellipsis 和状态分支。不要用通用 CSS 教程代替源码。

Tuqiang 的 .sc、core_ui 组件和宿主尺寸初始化必须从当前代码核验。多语言 UI 同时检查长文本、Arabic RTL、方向性图标、数字/单位和语义标签；账号模式可能改变 visibility、权限和空态。

最终说明“State/Model 字段 → mapper/条件 → Widget 属性 → 布局结果”，并分别覆盖 loading/error/empty。溢出或点击问题还要确认最终 hit target、嵌套 Gesture/InkWell 与滚动约束。
