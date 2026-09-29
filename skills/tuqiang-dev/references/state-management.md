# Tuqiang 状态管理

Tuqiang 当前是 Riverpod、Manager/单例、Widget State、Controller、缓存与插件状态并存的混合架构。先核对当前 pubspec/lockfile；最近审计基线为 Riverpod 2.6.1。先复用已有状态与 selector，沿目标 owner 的现有订阅/写入模式修改，不另建重复状态。新增派生计算遵守 [纯函数规则](local-style-and-reuse.md)，状态发布仍由原 owner 负责。

## 状态身份图

```text
声明/完整泛型 → family key → State/Notifier → Repository/请求触发
→ state/seed/apply/Manager/cache 写入 → watch/select/read/listen
→ 最终 UI/副作用 → dispose/invalidate/session reset
```

- route 参数把上下文带到页面；family key 决定 Provider 实例；方法参数控制一次 operation；State 字段保存结果。不得混用。
- family 对象 key 必须不可变并有稳定 `==/hashCode`。修改 key 时搜索所有构造点、override、缓存和测试。
- 个人/企业模式影响数据身份时，family/cache/session scope 必须包含或验证 `accountMode`，防止切模式后复用旧数据。读取 [账号模式事实](../../tuqiang-project-map/references/account-mode.md)。
- 查全 `state =`、seed/apply/update、Manager/cache/database/plugin 写入和 `watch/select/read/listen` 消费，不假设所有状态都经过 Riverpod。

## Provider override 与 owner

跨 Feature contract 常见方向：

```text
Feature 定义 Provider<Contract>
← apps/tuqiang_app 的 ProviderScope override 注入
← Feature 只调用公开 contract
```

修改 contract 同时检查声明、composition root、`standard`/`ohos`、route/result 与 session reset。Feature 不直接 import app 或其他 Feature 私有实现。

## 生命周期

`autoDispose`、命令保活、Widget/Notifier/StateNotifier/FutureProvider、监听 owner、竞态、身份快照和资源释放统一读取 [异步生命周期](async-lifecycle.md)，这里不复制判断表。

## reset 与验证

切设备、切 family key、切语言、登出和切账号模式分别检查 invalidate/reset；聚焦测试与真实命令见 [测试规范](testing.md)。
