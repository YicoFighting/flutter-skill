# Widget 生命周期与异步完成

生命周期解释围绕当前 owner，不机械套 Web hook。

| Flutter | Web 近似 |
|---|---|
| initState | 首次挂载初始化 |
| didChangeDependencies | inherited/provider 依赖变化 |
| didUpdateWidget | 父级配置或外部 owner 替换 |
| build | 纯渲染求值，可多次运行 |
| dispose | 清 Timer、Controller、subscription、listener |

## Widget 专属规则

- await 后使用 setState、context、Navigator、Toast/Dialog 或 WidgetRef 前，每个 async gap 都重新检查 mounted/context.mounted。
- mounted 只证明 Widget 还在树中；乱序结果用 generation，device/key/session/accountMode 切换用身份快照。
- build/initState/dispose/didUpdateWidget/didChangeDependencies 不得同步写 Provider。确需 Widget 首次发命令时放到首帧后，并再次检查 mounted。
- Widget ref.listen 只在 build；其他生命周期用 listenManual。ProviderContainer.listen 属于外部 owner，subscription 必须显式 close。
- didUpdateWidget 比较旧/新外部 Controller 或 key，先解绑旧 listener 再绑定新值。
- dispose 成对释放本 owner 创建的 Controller、FocusNode、Timer、StreamSubscription、observer 和 plugin handler；不要销毁外部传入对象。

## 解释顺序

指出资源由谁创建、何时绑定、什么变化触发重绑、异步完成在哪个 owner 发布、dispose 如何清理。随后分开说明 owner 存活、结果新鲜、身份和资源；完整实现门禁读 tuqiang-dev 的 [异步生命周期](../../tuqiang-dev/references/async-lifecycle.md)。
