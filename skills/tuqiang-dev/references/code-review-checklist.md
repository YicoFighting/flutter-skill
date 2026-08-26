# 代码审查高风险清单

只检查会影响正确性、安全性、可维护性或三端行为的事项，不把个人格式偏好伪装成项目红线。

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

- 路由字符串、参数、返回值和栈行为没有无意变化；feature/app 不重复提供 builder；
- `url_launcher` 类调用应处理 `launchUrl` 的返回值和异常；不要把 `canLaunchUrl` 当成绝对能力证明，也不要无理由做双重检查；
- 公共 Dart 不出现 OHOS 专属类型或包名；standard-only 能力必须明确隔离；
- asset 路径、大小写、pubspec、owner 常量和 package 参数使用同一种合法写法；
- 设计切图存在时不要用系统图标替代；没有对应切图的标准语义控件才考虑 `Icons.*`。

## 4. 状态和 UI

- Widget 的布尔开关与回调不应形成“可见但不可用”的组合；如果功能是否显示完全由 callback 决定，可直接以 null 判断；
- build 只读取和订阅状态，不同步修改 Provider；副作用使用事件、初始化阶段或 `ref.listen`；
- 多语言文本不要在 Widget/State 成员中缓存 `.tr` 结果；
- `.sc` 只用于设计尺寸；系统尺寸、边框、时长和算法参数不要机械转换；
- loading、空态、Toast、AppBar 优先复用实际存在的 `core_ui` 组件，不为单个页面重复造全局组件。

## 5. 最终核对

- [ ] 改动范围没有无关重构、依赖升级或格式化噪音；
- [ ] 相关 package、standard/OHOS、boundary、测试和真机验证按影响范围执行；
- [ ] 未执行的验证已在交付说明中列出；
- [ ] 没有敏感信息、生产假 URL 或生产假数据进入代码；
- [ ] 使用 `git diff --check` 检查空白和补丁质量。
