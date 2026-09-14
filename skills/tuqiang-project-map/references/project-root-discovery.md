# 仓库根目录发现与校验

本技能库当前服务 `D:\Code\tuqiang` 的 Tuqiang 产品；这是用户指定的工作副本，不是所有机器必须存在的盘符。根目录选择顺序：

1. 当前任务中用户明确指定或已确认的 Tuqiang checkout；
2. 当前任务绑定的 Tuqiang 项目/worktree；
3. 在本技能库维护任务或无业务 workspace 时，以 `D:\Code\tuqiang` 为已约定候选。

显式业务路径优先于技能库 cwd，两者不同是正常的“技能源 / 被服务源码”关系，不必重复询问。合法的新 checkout/worktree 可以替代约定路径；路径不存在或身份校验失败时报告原因并询问，不扫描磁盘，也不静默改用其他任务的 checkout。

## 确定性校验

从当前 Skill 目录执行（Python 3.10+、Git）：

```powershell
$rootJson = python -X utf8 .\scripts\validate_project_root.py --root 'D:\Code\tuqiang'
if ($LASTEXITCODE -ne 0) { throw 'Tuqiang 根目录校验失败' }
$tuqiangRoot = ($rootJson | ConvertFrom-Json).root
```

也可使用脚本绝对路径；`--root` 支持仓库根、子目录、目标源码文件及 Git worktree。脚本只读，输出规范化 Git 根、product、HEAD 与校验标记，不读取 remote/凭据、不执行 pub get、不修改业务文件。得到的 HEAD 只用于标记本次基线，不代表工作树干净；继续按任务范围读取 Git status/diff。

脚本检查以下文件实际存在、由 Git 跟踪、位于 checkout 内，并核对 pubspec 顶层 name：

| 路径 | pubspec name |
|---|---|
| apps/standard/pubspec.yaml | tuqiang_standard |
| apps/ohos/pubspec.yaml | tuqiang_ohos |
| apps/tuqiang_app/pubspec.yaml | tuqiang |
| tool/project.dart | 不适用 |

没有 Python 时按相同条件使用 `git rev-parse --show-toplevel`、`git ls-files`、`Test-Path` 和 UTF-8 读取手工校验。子目录应规范化到 Git 根，不要求原输入字符串与根完全相等；不能仅凭同名目录、tool target 枚举或忽略文件认定项目。

## 使用规则

- 校验后读取业务仓库的 AGENTS.md；只在 `$tuqiangRoot` 搜业务源码，技能修改仍在技能库进行。
- 确认 owner 时另查 tracked pubspec、name、barrel、import 和 composition；旧 shared_business 不能作为永久根标记。
- 首次校验后复用结果；切换项目、worktree、branch 或 checkout 后重查，不在每个搜索步骤重复校验。
- references 与学习报告保存相对路径和 symbol；用户界面需要可点击链接时组合本机绝对路径。
