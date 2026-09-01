# 本地风格采样与复用决策

本文件回答“在这个产品和 owner 里应该照谁写、复用什么、是否需要抽象”。最终实现以当前仓库、当前 Product Scope 和目标 owner 的局部证据为准。

## 1. 先定产品和 owner，再采样

1. 沿页面入口、route、Controller/Provider、Repository、asset 和测试确认产品与唯一 owner；
2. 老鹰先核对 Product Scope、API/route/resource/native contract；途强核对 Feature/public barrel 与迁移边界；
3. 查看目标 owner 的公开入口、真实调用方和复用点，禁止跨包 import 私有 `src/**`；
4. 在同一产品、同一 owner 选 2–4 个成熟同类实现，优先同一操作、生命周期和平台边界；
5. 同类不足时再看同产品相邻 owner，最后才参考允许复用的公共 core/shared/plugin；
6. 核对测试、当前 export 和实际调用，不能只凭文件名、时间或代码看起来“更新”判断。

证据优先级：

```text
同产品同 owner 的成熟实现
> 同产品相邻 owner
> 当前 Product Scope 允许的公共 core/shared/plugin
> 通用 Flutter 写法
```

老鹰不能把途强 Feature 页面当 sibling 模板。可以复用的是语义一致的公开底层能力，不是途强的业务 Router、Controller、资源或运行时配置。

## 2. 最小采样表

| 维度 | 必查证据 | 需要确定 |
|---|---|---|
| 产品/范围 | target、Product Scope、需求验收 | 允许做什么、哪些平台、哪些阻塞项 |
| 命名与文件组织 | 同 owner symbol、相邻文件、公开入口 | `TQ/Tq/LY` 前缀、目录和公开/私有边界 |
| 状态 | 声明、身份 key、消费者、dispose/reset | 途强 Provider/Manager 或老鹰 LY Controller/Scope 的实际模式 |
| Model | 同接口响应、parser、测试 | null、不可变性、转换与 copy |
| Repository | 同域实现、HTTP client、错误分支、fake | 返回类型、failure 边界和注入 |
| Widget | 同产品页面、core_ui、i18n、尺寸、释放逻辑 | 拆分、订阅、副作用和品牌覆盖 |
| 路由/资源 | registry、contract、resolver、pubspec | 唯一 owner、参数/返回值、package asset |
| 测试 | 同类行为、fixture/fake、contract test | 最小可证伪场景 |

这些维度可以分别沿用不同成熟样本，不为表面一致复制一整套脚手架。

## 3. 复用决策阶梯

1. **直接复用公开能力**：职责、产品范围、错误语义和生命周期一致；
2. **小幅扩展 owner 内能力**：新增参数不会变成产品/mode 开关；
3. **保留局部直接实现**：只有一个真实消费者，或少量重复更清楚；
4. **新增共享抽象**：至少两个现存消费者、稳定共同语义、正确依赖方向和可验证 contract；
5. **停止并重新选 owner**：只能靠跨产品业务 import、Feature 横向私有依赖、app 反向承载或 shared 依赖 Feature 才能复用。

以下通常不抽象：

- 只转发参数/返回值的 wrapper；
- 依赖大量 nullable callback 或 boolean/mode flag；
- 为未来假想消费者建立 base/service/global util；
- 会暴露业务 Model、路由、Provider/Controller 私有细节；
- 会扩大 package、lockfile、平台或 session reset 影响面；
- 需要从冻结的 `shared_business` 恢复入口。

## 4. 实施前决策记录

```text
产品/Product Scope：<tuqiang 或 laoying；允许范围与平台>
Owner/层级：<package/目录；为什么归它>
现有复用入口：<symbol；复用、扩展或不复用的原因>
局部样本：<2–4 个同产品文件/symbol；各证明什么>
选择的写法：<状态/Model/Repository/Widget/route/asset>
最小范围与验收：<改什么、不改什么、可证伪行为>
待用户决定：<没有则写无；有则停止相关实现>
```

完成一次聚焦调查后仍有多解时，按 [requirement-clarification.md](requirement-clarification.md) 立即询问，不继续扩大搜索。实现中发现 owner 或复用判断错误，先更新决策，再考虑扩大范围。

## 5. 可验证检查

先按公共协议得到 `$tuqiangRoot`，再替换真实相对路径和 symbol：

```powershell
$targetRelative = '<目标 owner 相对路径>'
$targetPath = Join-Path $tuqiangRoot $targetRelative
$candidate = '<候选 symbol>'

rg -n 'export |Provider|Repository|Controller|class ' (Join-Path $targetPath 'lib') (Join-Path $targetPath 'test')
rg -n $candidate (Join-Path $tuqiangRoot 'apps') (Join-Path $tuqiangRoot 'packages')
git -C $tuqiangRoot diff -- $targetRelative
```

交付前确认：

- [ ] 样本来自同一产品、同一 owner；降级采样有理由；
- [ ] 老鹰范围有 Product Scope/contract 证据，未把设计存在当授权；
- [ ] 复用入口是当前公开 API，未依赖另一产品业务或私有 `src/**`；
- [ ] 没有为统一存量而改名、搬目录、替换状态库或重排脚手架；
- [ ] 没有纯转发 wrapper、mode flag、投机基类或无消费者共享层；
- [ ] 没有向冻结的 `shared_business` 写入或产生产品资源/配置泄漏；
- [ ] diff 只覆盖必要 owner，验证与未执行项均已记录。
