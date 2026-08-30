---
name: tuqiang-change-retrospective
description: 在途强 Flutter Bug 已修复或需求已完成后，基于当前源码、Git diff/history 与验证证据生成可长期学习的 Markdown 复盘；适用于追溯缺陷引入、暴露与修复改动，拆解需求动机、输入输出、事件/异步/状态流，并按需借助 flutter-to-web 给出 Dart、Vue3、React 对照。仅在用户明确要求复盘或生成学习文档时使用，不负责修改业务代码、重新实现需求或提交推送。
license: Apache-2.0
metadata:
  version: "1.0.0"
---

# 途强 Flutter 变更复盘

本 Skill 是开发完成后的“证据复盘与学习文档层”。它把已经修复的 Bug、已经完成的需求，或二者交织的改动，还原成一份可追溯、适合初学者反复阅读的 Markdown。

## 1. 手动触发与职责边界

仅在用户显式调用本 Skill，并表达“复盘、整理原因、生成学习文档”等意图时工作。普通开发、修复、解释或评审过程中不要自动生成文档。

- 只读调查源码、Git 历史、diff、测试结果和已有任务上下文；
- 唯一默认写入是最终复盘 Markdown，不修改业务源码、测试、配置或 Git 历史；
- 不执行 `checkout`、`reset`、`pull`、`fetch`、`bisect`、`commit` 或 `push`；即使用户需要二分调查，也应另开隔离任务并单独授权，不在本复盘流程切换工作树；
- 不把“用户说已完成”扩展成重新实现或顺手修复；证据不足时在文档中标记未验证；
- 若工作区存在无关改动，只纳入与本次复盘范围有直接证据关系的文件和 hunk。

## 2. 三种复盘模式

根据用户描述、当前对话、diff 和提交范围选择：

| 模式 | 适用情况 | 主问题 |
|---|---|---|
| Bug | 已完成缺陷修复 | 为什么出现、何时引入/暴露、如何排查和避免 |
| 需求 | 已完成需求开发 | 为什么这样做、如何实现、输入输出和事件怎样流转 |
| 混合 | 需求开发中引入、暴露或顺带修复 Bug | 需求主链与 Bug 因果如何相互影响 |

能可靠判断时直接选择。只有模式或范围歧义会实质改变 Git 归因和文档内容时，才请求用户补充。混合模式默认生成一份主文档，在需求主线中嵌入 Bug 复盘卡；用户明确要求时再拆成多个文件。

## 3. 项目事实与兄弟 Skill 协作

先按 [项目根目录发现协议](../tuqiang-project-map/references/project-root-discovery.md) 确定并验证 `<TUQIANG_ROOT>`，读取目标仓库中适用的 `AGENTS.md`。兄弟 Skill 不可用时，使用同一仓库身份条件直接核验当前源码；无法唯一确定目标项目时停止写入并请求确认。

项目地图不可用时，候选根目录至少同时满足：

| 必须存在的文件 | `pubspec.yaml` 中的 `name` |
|---|---|
| `apps/standard/pubspec.yaml` | `tuqiang_standard` |
| `apps/ohos/pubspec.yaml` | `tuqiang_ohos` |
| `apps/tuqiang_app/pubspec.yaml` | `tuqiang` |
| `packages/shared/shared_business/pubspec.yaml` | `shared_business` |
| `tool/project.dart` | 不适用 |

用户路径优先，其次使用目标文件所在 Git 仓库和当前 workspace 的 Git 根目录；不为寻找项目扫描整个磁盘。

按需复用，不一次加载全部内容：

- [tuqiang-project-map](../tuqiang-project-map/SKILL.md)：提供 owner、依赖边界、调用链和状态拓扑的事实索引；跨文件需求链再读其 [需求追踪剧本](../tuqiang-project-map/references/requirement-trace-playbook.md)；
- [flutter-to-web](../flutter-to-web/SKILL.md)：涉及 Flutter 事件、Riverpod、异步请求、UI 重建或前端类比时，读取其入口及当前问题所需的 reference；跨文件链优先读 [完整业务链追踪](../flutter-to-web/references/full-flow-tracing.md)，涉及 Provider 身份/生命周期时再读 [状态与 Riverpod](../flutter-to-web/references/state-and-riverpod.md)；
- [tuqiang-dev](../tuqiang-dev/SKILL.md)：只有解释“为什么沿用该实现方式、验证范围或项目约束”时才读取；局部风格或复用取舍读 [局部风格与复用](../tuqiang-dev/references/local-style-and-reuse.md)，不要为普通复盘加载整套开发规范。

当前源码、当前 Git 历史、测试和目标仓库规则始终高于 reference。Vue3/React 代码是心智映射，不是项目事实，也不能替代 Dart 证据。

## 4. 标准工作流

1. **锁定范围**：记录用户给出的标题、问题/需求、提交范围、文件、符号、验收结果和输出路径；未给出时从当前对话与目标相关 diff 推导。
2. **记录基线**：读取当前分支、`HEAD`、工作区状态、未暂存/已暂存改动和相关提交；区分用户确认、实际测试通过与未执行验证。
3. **建立证据账本**：所有关键结论标为“已证实事实”“高可信推断”或“未知边界”，不从源码反推不存在的产品意图。
4. **还原业务闭环**：从用户操作或生命周期入口，分别追同步事件链、异步数据链、状态依赖/UI 重建链；异步和响应式通知不能伪装成一条连续调用栈。
5. **执行模式分析**：Bug 读取 [Bug 复盘剧本](references/bug-retrospective.md)；需求读取 [需求复盘剧本](references/feature-retrospective.md)；混合模式两者都读。
6. **调查 Git 因果**：需要回答“哪次提交或改动造成”时读取 [Git 因果取证](references/git-causality.md)，区分缺陷引入、问题暴露、修复改动和防线缺失。
7. **生成教学对照**：摘录修复前/后或关键需求 Dart 源码，用相同字段和步骤给出 Vue3、React 对照，并明确非等价处。
8. **写入并自检**：按 [Markdown 输出契约](references/report-contract.md) 生成一份完整文档，检查路径、行号、提交号、敏感信息、链接和 UTF-8 无 BOM。

## 5. 金字塔、栈与时间流的正确用法

文档至少保留一份纯文本图，保证离线 Markdown 也能阅读：

```text
金字塔：结论/用户价值
        ↓
      行为与规则
        ↓
    模块、状态与数据
        ↓
  源码、提交、测试证据
```

- **金字塔**用于从“为什么”逐层下钻到证据；
- **因果栈**用于 Bug 的“根因 → 错误状态 → 用户症状”和反向修复过程；
- **调用栈**只描述同一时刻的同步函数调用；
- **三泳道时间流**分别描述事件/同步调用、异步数据、状态通知/UI 重建。

不因用户说“用栈讲解”就把 `await` 返回、Provider 通知和 Widget 重建画成一条同步栈。

## 6. 证据与归因底线

- `git blame` 只能证明某行最后由哪个提交修改，不能单独证明根因；
- 必须区分“引入缺陷的改动”“让潜伏缺陷可达的暴露改动”“恢复不变量的修复改动”；
- 当前未提交改动写作“当前工作区改动，尚无对应提交”，不得虚构 commit；
- 若只有 blame/搜索线索，写“候选提交”；若 diff、调用链与复现/测试闭环，才写“已确认”；
- 无法访问完整历史、父版本、后端、原生 SDK 或运行环境时，明确说明证据停止点；
- 不输出 endpoint、Token、Key、证书、签名或生产配置值。

## 7. Markdown 落盘规则

路径优先级：

1. 用户明确指定的文件或目录；
2. 目标仓库 `AGENTS.md` 或现有文档约定；
3. `<TUQIANG_ROOT>/docs/learning/`。

默认文件名：

```text
YYYY-MM-DD-bug-<slug>.md
YYYY-MM-DD-feature-<slug>.md
YYYY-MM-DD-hybrid-<slug>.md
```

- 不覆盖同名文件；新建时追加 `-2`、`-3`、……直到找到首个不存在的名称，并在写入前再次检查；只有用户明确要求更新已有复盘时才编辑原文件；
- 文档内部使用仓库相对路径与 1-based 行号，便于换电脑继续阅读；
- 历史代码标记 commit，当前代码标记当前分支/`HEAD` 或工作区；
- 源码只摘录证明入口、错误、修复、写入和消费的最小片段；
- “完整”指证据链闭环，不指篇幅最大化；同一事实和代码只在一个主章节完整解释，其他章节用步骤号或小节链接引用；
- 最终回复给出生成文件的绝对可点击路径，并简述模式、范围、引入/暴露/修复各角色的置信度摘要和未验证边界；不得用修复角色的高置信度掩盖历史归因仍属候选或未知。

## 8. Reference 路由

| 文件 | 什么时候读 |
|---|---|
| [references/git-causality.md](references/git-causality.md) | 追溯引入/暴露/修复提交，或解释当前未提交改动 |
| [references/bug-retrospective.md](references/bug-retrospective.md) | Bug 模式；混合模式中的 Bug 卡 |
| [references/feature-retrospective.md](references/feature-retrospective.md) | 需求模式；混合模式中的需求主线 |
| [references/report-contract.md](references/report-contract.md) | 每次生成最终 Markdown 时 |

## 9. 完成条件

- [ ] 目标仓库、复盘范围、模式和输出路径已确定；
- [ ] 事实、推断与未知边界已分开；
- [ ] Git 归因没有把 blame、提交时间或作者等同于根因；
- [ ] 已分别展示同步事件、异步数据、状态/UI 重建；
- [ ] Bug 包含原因、引入/暴露/修复证据、排查、解决和预防；需求包含动机、实现、输入输出与事件流；
- [ ] Dart、Vue3、React 使用同一业务链，且类比未冒充等价事实；
- [ ] 已生成完整 Markdown，未覆盖已有文件，文本为 UTF-8 无 BOM；
- [ ] 没有修改业务源码、Git 历史或泄露敏感信息。
