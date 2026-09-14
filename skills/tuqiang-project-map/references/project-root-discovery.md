# 仓库根目录发现与校验

本技能库服务 Tuqiang 项目身份，不绑定盘符、目录名或开发者机器。根目录按以下顺序发现：

1. 当前任务中用户明确指定或已确认的业务路径；支持仓库根、子目录或源码文件。
2. 当前任务绑定的业务项目/workspace/worktree 的 Git 根；不得把技能库 cwd 当作业务根。
3. 本任务已校验且项目上下文未变化的业务根。
4. 未绑定业务 workspace 时，当前目标源码文件所属的 Git 根。

取最高优先级的明确候选并执行下面的身份校验。没有可用候选、候选指向不同业务 checkout 且当前任务无法确定目标，或权威候选校验失败时，只询问当前业务路径；不扫描磁盘，不静默回退到其他 checkout，不将历史聊天中的绝对路径写成默认值。

显式业务路径优先于技能库 cwd，两者不同是正常的“技能源 / 被服务源码”关系，不必重复询问。项目移动、改名或换机器后，以当前任务的新路径重新校验；只要仓库标记和 package identity 满足条件，就无需修改或重新安装 Skill。

## 确定性校验

从当前 Skill 目录执行（Python 3.10+、Git）：

```powershell
# $tuqiangCandidate 来自上面的当前任务候选发现，不能取技能库目录。
$rootJson = python -X utf8 .\scripts\validate_project_root.py --root $tuqiangCandidate
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
