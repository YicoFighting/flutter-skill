# 本地风格采样与复用决策

本文件用于回答“在这个 owner 里应该照谁写、复用什么、是否需要抽象”。项目地图只提供 owner 候选、架构边界和 symbol 索引；最终实现必须以当前 `<TUQIANG_ROOT>` 中目标 package 的局部证据为准。

## 1. 先定 owner，再采样

按以下顺序执行，不能先写代码再为已有方案找证据：

1. 沿页面入口、route、Provider、Repository、asset 和测试确认唯一 owner 与所属层级；
2. 查看目标 package 的公开 barrel/API、现有调用方和可复用入口，禁止跨包 import 私有 `src/**`；
3. 在同一子域、目标 package 选 2–4 个成熟同类实现，优先同一用户操作、同一生命周期和同一平台边界；
4. 同类不足时再看同层 sibling feature，最后才参考全局通用写法；
5. 对每个候选核对真实调用方、测试、当前 public export 和最近仍在维护的 owner，不能只凭文件名、更新时间或代码更“新潮”判断。

证据优先级固定为：

```text
同一子域/目标 package 的成熟同类实现
> 同层 sibling feature
> 全局通用写法
```

项目不是全局一致的：同一业务域可能同时存在 `TQ`、`Tq`、无前缀，`StateNotifier`、`ChangeNotifier`，以及旧/新目录。样本冲突时沿当前 owner 中较新且有真实调用方或测试的模式，并在实施说明中记录取舍；不得借当前需求顺手统一存量命名、目录或状态架构。

## 2. 最小采样表

动手前至少记录与本次修改有关的行；不相关维度不必凑数。

| 维度 | 必查证据 | 需要确定的选择 |
|---|---|---|
| 命名与文件组织 | 同类 symbol、相邻文件、barrel export | 前缀、文件名、公开/私有边界、目录位置 |
| Provider | 声明、family key、Notifier、消费者、dispose/reset | Provider 类型、State 形态、参数和生命周期 |
| Model | 同接口响应、`fromJson/toJson`、`TCheck`、测试 | null 语义、不可变性、转换和 `copyWith` |
| Repository | 同域 Repository、TQHttp 调用、错误分支、fake | 方法返回类型、异常/Result 边界、依赖注入 |
| Widget | 同类页面/组件、core_ui、`.tr`、`.sc`、释放逻辑 | Widget 类型、拆分粒度、订阅和副作用位置 |
| 测试 | 同类行为测试、fixture/fake、contract test | 最小可证伪场景与断言层级 |

Provider、Model、Repository、Widget 可以分别沿用当前 owner 内不同的成熟模式；不要为了“一致”强迫它们复制同一个 sibling feature 的整套脚手架。

## 3. 复用决策阶梯

从上到下选择第一个满足语义和依赖方向的方案：

1. **直接复用公开能力**：现有 API、Provider、Repository、core_ui 或 adapter 的职责与生命周期完全一致；
2. **小幅扩展 owner 内能力**：语义一致，新增参数不会把单一职责变成模式开关；
3. **保留局部直接实现**：只有一个真实消费者，或少量重复比抽象更清楚；
4. **新增共享抽象**：至少有两个已存在的真实消费者、稳定共同语义、正确依赖方向和可验证 contract；
5. **停止并重新选 owner**：只能通过 feature 横向依赖、app 反向承载业务或 shared 依赖 feature 才能复用。

以下情况通常不要抽象：

- wrapper 只转发参数或返回值，没有收敛平台、错误或生命周期差异；
- 需要大量可空 callback、boolean/mode flag 才能服务不同业务；
- 为尚未出现的消费者建立 base class、通用 service 或全局 util；
- 共享后反而暴露业务 Model、路由或 Provider 私有细节；
- 抽象会扩大 package、lockfile、平台实现或 session reset 的影响面。

目标是高内聚、低耦合：业务规则、状态和数据访问留在真实 owner，跨 package 只暴露必要 contract。复用优先不等于抽象优先。

## 4. 实施前决策记录

开始修改前，用短句写清：

```text
Owner/层级：<package 与目录，为什么归它>
现有复用入口：<symbol；复用、扩展或不复用及原因>
局部样本：<2–4 个文件/symbol；各自证明什么>
选择的写法：<Provider/Model/Repository/Widget 中与需求相关的约定>
最小范围与验收：<要改的文件、不会改的边界、可证伪行为>
```

样本冲突时必须补一行“选择依据”，指向当前 owner 的调用方、测试或公开 export。实现中若发现 owner 或复用判断错误，先更新这份决策，再扩大修改范围。

## 5. 可验证检查

先按项目地图协议得到 `$tuqiangRoot`，再把目标 package 的仓库相对路径和 symbol 占位符替换为真实值：

```powershell
$targetPackageRelative = '<目标 package 相对路径>'
$targetPackage = Join-Path $tuqiangRoot $targetPackageRelative
$candidateSymbol = '<候选 symbol>'
$newOrEquivalentSymbol = '<新增或已有同义 symbol 的 rg pattern>'

# 公开入口、同类实现和调用方
rg -n 'export |Provider|Repository|class ' (Join-Path $targetPackage 'lib') (Join-Path $targetPackage 'test')
rg -n $candidateSymbol (Join-Path $tuqiangRoot 'apps') (Join-Path $tuqiangRoot 'packages')

# 修改后检查影响面和是否产生重复入口
git -C $tuqiangRoot diff -- $targetPackageRelative
rg -n $newOrEquivalentSymbol (Join-Path $targetPackage 'lib') (Join-Path $targetPackage 'test')
```

交付前逐项确认：

- [ ] 2–4 个样本来自同一子域/目标 package；不足时已说明为何降级到 sibling/global；
- [ ] 复用入口有当前 public export 和真实调用方证据，不依赖其他 package 的私有 `src/**`；
- [ ] Provider、Model、Repository、Widget 只采纳与本次需求相关的局部约定；
- [ ] 样本冲突的选择有测试、调用方或当前 owner 证据；
- [ ] 没有为统一存量而改名、搬目录、替换状态库或重排脚手架；
- [ ] 没有纯转发 wrapper、模式开关胶水、投机性基类或无真实消费者的共享层；
- [ ] `git diff` 只覆盖必要 owner，并已运行该范围对应的 analyze、测试与边界检查；未执行项如实记录。
