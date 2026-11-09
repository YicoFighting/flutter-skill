# 仓库根目录发现与校验

技能服务的是 Tuqiang 项目身份，不绑定盘符、目录名或机器。

## 候选顺序

1. 当前任务中用户明确指定或已确认的业务路径（仓库根、子目录或源码文件均可）。
2. 当前任务绑定的业务 workspace/worktree 的 Git 根；技能库 cwd 不是业务根。
3. 本任务已校验且上下文未变化的业务根。
4. 未绑定业务 workspace 时，目标源码文件所属的 Git 根。

取最高优先级候选校验。没有候选、多个 checkout 无法确定目标，或权威候选校验失败时，只询问当前业务路径；不扫描磁盘，不静默切换 checkout，不把历史聊天里的绝对路径当默认值。技能库 cwd 与业务根不同是正常情况，无需重复询问。

## 确定性校验

在本 Skill 目录执行（Python 3.10+、Git）：

```powershell
# $tuqiangCandidate 来自上面的候选，不能取技能库目录
$rootJson = python -X utf8 .\scripts\validate_project_root.py --root $tuqiangCandidate
if ($LASTEXITCODE -ne 0) { throw 'Tuqiang 根目录校验失败' }
$tuqiangRoot = ($rootJson | ConvertFrom-Json).root
```

脚本只读：规范化到 Git 根，要求以下标记存在、被 Git 跟踪且位于 checkout 内，输出 root/product/HEAD；不读 remote/凭据，不 pub get。HEAD 只标记基线，不代表工作树干净。

| 标记 | pubspec 顶层 name |
|---|---|
| `apps/standard/pubspec.yaml` | `tuqiang_standard` |
| `apps/ohos/pubspec.yaml` | `tuqiang_ohos` |
| `apps/tuqiang_app/pubspec.yaml` | `tuqiang` |
| `tool/project.dart` | — |

无 Python 时用 `git rev-parse --show-toplevel`、`git ls-files` 与 UTF-8 读取按同样条件手工校验；同名目录或 target 枚举不能单独证明项目身份。

## 使用规则

- 校验后读取业务仓库 `AGENTS.md`；涉及 UI/设计稿时读 `DESIGN.md`，涉及规范、分层或切图时读对应 `.codex/skills/*/SKILL.md`。只在 `$tuqiangRoot` 搜业务源码，技能修改仍在技能库。
- `apps/laoying_*` 与 `tool/project.dart::AppTarget` 中的 overseas/laoying target 不属于 Tuqiang 范围。
- 切换项目、worktree、branch 或 checkout 后重新校验，不在每次搜索前重复。
- references 与报告保存仓库相对路径和 symbol；需要可点击链接时再拼接本机绝对路径。
