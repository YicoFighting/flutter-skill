# Tuqiang 设计源与静态资源

## 设计源

- 有可访问的设计稿或正式切图时，按其尺寸、颜色、字体、状态和交互还原。
- 没有设计稿时，沿目标 Feature 的相邻成熟页面、`core_ui` 与现有视觉 token。
- 设计稿有业务/品牌切图时使用真实资源；只有标准语义控件且无指定切图时才考虑 `Icons.*`。

## 缺素材时停止

PNG/SVG/动画帧中的文字、语言、状态、主题和业务含义都是产品输入。需求要求替换或新增业务图片而仓库没有目标素材时，先索要文件并确认选择条件。未经明确授权不得使用：

- `Canvas/CustomPainter/TextPainter` 或运行时叠字；
- 系统图标、emoji、字体图标或临时占位图；
- AI/程序生成、动态 SVG 或近似重绘；
- 不存在的文件名或生产路径中的 fake。

例如起终点图片需要非中文 `S/E` 版本时，应取得对应资源并按语言选择，而不是在旧图上绘字。用户允许先做接线时，也要明确未完成状态，不能让 placeholder 看起来像最终交付。

## Owner 与引用

- 单 Feature 图片、JSON、动画与帧序列放 `packages/feature/feature_xxx/assets`。
- 至少两个稳定消费者或 App 壳共同使用的 Tuqiang 资源，才考虑 `packages/assets_common`。
- 迁移资源时搜索 Dart、pubspec、Android、iOS、OHOS 引用；根图、倍率目录、帧序列和 JSON 整组迁移，避免两份事实来源。
- 路径通过目标 owner 已有常量/Resolver 暴露；`Image.asset` 的 `package` 参数、大小写和 pubspec 声明沿相邻成熟实现，不在页面散落字符串。
- 新增 dependency 或 asset 目录只改真实受影响的 pubspec/target，不顺手触碰 lockfile。

## 语言、账号与状态变体

语言素材遵循当前 manifest，并与 [国际化流程](i18n.md) 一起验证；状态和主题变体必须有明确选择条件。若个人/企业显示不同资源，将 `accountMode` 纳入覆盖台账并验证切账号后不会沿用旧缓存。

## 验证

- 路径、大小写、文件存在性、pubspec、package 参数和倍率配对；
- 每种语言/状态/accountMode 实际选中目标文件；
- 按 [测试规范](testing.md) 选择必要的资源/contract 检查；改变打包或依赖边界才增加宿主/构建/架构检查；
- 新页面按风险检查小屏、宽屏/折叠态和三端；
- `git diff --check`，并确认没有临时或生成占位资源。
