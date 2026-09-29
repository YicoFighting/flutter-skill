# Widget 生命周期与异步完成

围绕当前 owner 解释生命周期，不机械套 Web hook。

| Flutter | Web 近似 |
|---|---|
| initState | 首次挂载初始化 |
| didChangeDependencies | inherited 依赖变化 |
| didUpdateWidget | 父级配置或外部 owner 替换 |
| build | 可多次执行的渲染求值 |
| dispose | 本 owner 的资源释放 |

资源问题说明谁创建、何时绑定、何时重绑和释放；异步问题说明结果在哪发布，以及 owner 存活、结果新鲜度和身份是否仍成立。不要仅凭 mounted 或 dispose 判断所有问题都已解决。

项目的 Widget/Provider 使用约束和 owner-specific 检查统一读取 [异步生命周期](../../tuqiang-dev/references/async-lifecycle.md)，并对照当前依赖版本；本文件不重复维护实现门禁。只解释影响用户问题的生命周期节点，不为简单 build 问题展开全部清理流程。
