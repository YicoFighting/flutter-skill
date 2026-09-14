# 仓库根目录发现与校验

Tuqiang 根目录不是固定盘符。按以下顺序取候选：

1. 用户在本任务明确给出的目录；
2. 当前任务绑定项目/workspace 的 Git 根；
3. 本任务已校验且 checkout 未变化的根；
4. 无 workspace 时，目标源码所属 Git 根。

候选缺失、冲突或校验失败时询问用户；不扫描整块磁盘、用户目录，也不复用其他任务的绝对路径。

## 校验

先运行 git -C <candidate> rev-parse --show-toplevel。结果必须与用户候选一致，且不能是本 Skill 仓库。

以下文件必须存在并由 Git 跟踪：

| 路径 | pubspec name |
|---|---|
| apps/standard/pubspec.yaml | tuqiang_standard |
| apps/ohos/pubspec.yaml | tuqiang_ohos |
| apps/tuqiang_app/pubspec.yaml | tuqiang |
| tool/project.dart | 不适用 |

逐项用 Test-Path、git ls-files -- <path> 与 pubspec 的顶层 name 验证；任一缺失或 identity 不符就停止。不要仅凭目录名、tool 枚举、忽略文件或迁移残留认定项目。

确认 package 时同样检查 tracked pubspec、name 和公共 barrel。packages/shared/shared_business 已不是 tracked package，不能作为根标记或 owner。

## 使用规则

- 将校验后的路径保存为本任务的 tuqiangRoot，并在该目录搜索。
- reference 和报告保存相对路径、当前行号与 symbol；只有用户界面需要可点击链接时才组合本机绝对路径。
- 切换项目、worktree、branch 或 checkout 后重新校验。
- Git 失败、根为空或出现多个合法 checkout 时不猜测。
