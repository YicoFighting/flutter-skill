# Tuqiang 布局与 UI 的 Web 对照

Flutter 约束由父向子传，尺寸由子向父回传，ParentData 决定位置；它更接近显式 layout protocol，而不是浏览器普通文档流。

| Flutter | Web 心智 |
|---|---|
| Row/Column + Expanded/Flexible | flex 与 grow/shrink |
| Stack/Positioned | position relative/absolute |
| ListView/CustomScrollView | 滚动容器/虚拟列表 |
| LayoutBuilder/MediaQuery | container/viewport query |
| SafeArea | safe-area inset |

只追影响目标字段或布局的父约束、轴向、scroll owner、inset 和状态分支。Tuqiang 的 .sc、core_ui 组件和尺寸初始化以当前源码为准，不用通用 CSS 教程替代解释。

字段展示沿“Model/State → mapper/条件 → Widget 属性”追到消费点；fallback 和兼容规则参考 [国际化与展示边界](../../tuqiang-dev/references/i18n.md)。涉及组件选择时核验 [本地风格与复用](../../tuqiang-dev/references/local-style-and-reuse.md)，先指出项目已有封装。

多语言、loading/error/empty、RTL、账号 visibility 仅在影响本题时展开。溢出或点击问题检查最终 hit target、嵌套 Gesture/InkWell 和滚动约束。
