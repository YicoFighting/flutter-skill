# 代码审查高风险清单

只检查会影响正确性、安全性、可维护性、产品边界或三端行为的事项，不把个人格式偏好伪装成项目红线。

## 1. 异常和异步

- `catch` 不得静默吞错；使用项目日志封装并脱敏，状态仍要回到可观察的 error/empty 状态；
- 跨 `await` 更新 Widget 前检查 Widget `mounted`；StateNotifier/Notifier 使用自身生命周期判断；
- 连续请求用 generation、request id 或取消机制防止旧响应覆盖新状态；
- Controller、FocusNode、Subscription、AnimationController 等由当前 owner 创建的资源要释放。

## 2. 类型和数据

- 外部 JSON 在 `TCheck<T>` 或 parser 边界完成类型收窄；
- 不要用 `List<dynamic>` 把脏数据扩散到业务层，也不要为了消灭 `is Map` 而对未经验证的数据强制 cast；
- 请求 DTO 和响应 Model 分开考虑，nullable、required、默认值和显式 null 必须符合接口契约；
- `toJson` 是否过滤 null 取决于后端语义，尤其注意“清空字段”和“省略字段”的区别。

## 3. 路由、平台和资源

- 已确认目标产品、Product Scope 和唯一 owner；老鹰业务没有依赖途强 Feature、资源或运行时配置；
- 已分类 Bug/新需求并满足平台基线：Bug 有 Android+OHOS 修复证据和 iOS 影响/交接；新需求三端都有代码实现；
- 设备列表/详情/更多详情已按 `deviceType`、scene、cameraScene 和最终 route/Page 审查；未确认设备范围时不接受只改当前页面的补丁；
- Tuqiang 地图改动已逐项检查 Android/iOS 各三源与 HarmonyOS Map Kit 的 7 个候选行及实际 map scene，不可达行使用 `无需修改` 并附源码证据；没有把 OHOS factory alias 误当供应商，也没有虚构 `petal` Dart 枚举；
- Laoying 地图改动只按当前 Product Scope、两个宿主 adapter 与实际 scene mapping 检查，没有反向套用 Tuqiang 三供应商矩阵；
- 路由字符串、参数、返回值和栈行为没有无意变化；途强 feature/app 或老鹰 LY registry 不重复提供 builder；
- `url_launcher` 类调用应处理 `launchUrl` 的返回值和异常；不要把 `canLaunchUrl` 当成绝对能力证明，也不要无理由做双重检查；
- 公共 Dart 不出现 OHOS 专属类型或包名；standard-only 能力必须明确隔离；
- asset 路径、大小写、pubspec、owner 常量和 package 参数使用同一种合法写法；
- 设计切图存在时不要用系统图标替代；缺少目标业务图片时先索要，未经授权不使用 Canvas/CustomPainter/TextPainter、文字叠加、系统图标、AI 或程序生成替代；
- 没有对应切图且确属标准语义控件时，才考虑 `Icons.*`。

## 4. 状态和 UI

- Widget 的布尔开关与回调不应形成“可见但不可用”的组合；如果功能是否显示完全由 callback 决定，可直接以 null 判断；
- build 只读取和订阅状态，不同步修改 Provider/Controller；副作用沿目标产品现有事件、初始化或 listener 模式；
- 多语言文本不要在 Widget/State 成员中缓存 `.tr` 结果；
- `.sc` 只用于设计尺寸；系统尺寸、边框、时长和算法参数不要机械转换；
- loading、空态、Toast、AppBar 优先复用实际存在的 `core_ui` 组件，不为单个页面重复造全局组件。

## 5. 最终核对

- [ ] 改动范围没有无关重构、依赖升级或格式化噪音；
- [ ] [覆盖台账](implementation-coverage.md) 没有空白行或无证据的“无需修改”；相关 package、平台、target、地图后端、设备页面、ProductScope、聚焦 architecture/contract tests 和真机验证按规则执行；
- [ ] `standard` analyze 未被当作 iOS 运行证据，iOS 未执行项与同事交接明确；app boundary 已知基线未误归因；
- [ ] 未执行的验证已在交付说明中列出；
- [ ] 没有敏感信息、生产假 URL 或生产假数据进入代码；
- [ ] 使用 `git diff --check` 检查空白和补丁质量。
