# 当前对话项目的动态根目录协议

> 每次需要读取业务源码时执行。目标是得到经验证的 `<TUQIANG_ROOT>`，而不是记住某台电脑上的绝对路径。这里的名字表示 monorepo 根目录，不等于本次一定属于 Tuqiang 产品线。

## 1. 解析顺序

按以下优先级选择候选目录：

1. 用户在当前请求中明确给出的项目根目录；
2. Codex 当前对话绑定的项目或 active workspace root；
3. 本任务中已按同一协议验证、且 project/checkout 未变化的根目录；
4. 仅在当前对话没有项目上下文，或用户明确要求处理项目外文件时，才从选中、打开或目标源码文件向上找 Git 根目录；
5. 仅在当前对话没有项目上下文时，才从当前工作目录向上找 Git 根目录。

显式路径与当前对话项目均高于兄弟 Skill 的缓存结论。二者只要存在但身份校验失败，就说明候选与失败原因并请用户确认，不得静默降级到缓存根、目标文件或当前目录；只有更高优先级来源本来就不存在时，才看下一项。不要因为当前目录恰好是 Skill 仓库就把它当成业务仓库，也不要沿用其他对话、其他电脑或上一次任务的路径。不要扫描整块磁盘。

当前对话项目存在时，选中/打开/附件文件只作为该项目内的检索锚点，不能静默把任务切换到另一份 checkout。目标文件属于另一合法仓库，或多个候选会产生不同答案时，列出当前项目、外部候选与冲突原因并请用户确认。

## 2. 稳定仓库身份验证

基础仓库身份使用稳定的 Tuqiang 三个 App 与项目命令入口，不再依赖已经拆分的 `packages/shared/shared_business`：

| 必须存在的文件 | `pubspec.yaml` 中的 `name` |
|---|---|
| `apps/standard/pubspec.yaml` | `tuqiang_standard` |
| `apps/ohos/pubspec.yaml` | `tuqiang_ohos` |
| `apps/tuqiang_app/pubspec.yaml` | `tuqiang` |
| `tool/project.dart` | 不适用 |

同时确认候选目录是目标 Git checkout，并读取其根 `AGENTS.md`。不得仅凭目录名、盘符或一个同名 symbol 判定。

`packages/shared/*` 已按领域拆分，某个具体 shared package 只能用于 owner/依赖判断，不能再作为整个仓库的必需身份标志。若候选中出现 `apps/laoying_standard`、`apps/laoying_ohos`、`apps/laoying_app` 任一项，则继续校验 Laoying trio 必须完整、被 Git 跟踪，且 package identity 分别为 `laoying_standard`、`laoying_ohos`、`laoying_app`。证据冲突且会影响答案时请用户确认，不能退回历史固定路径。

## 3. 产品线与 target 验证

仓库验证通过后，再按目标路径、用户入口或 `tool/project.dart` 的当前 `AppTarget` 判定产品：

| target | shell | package identity | 产品/平台 |
|---|---|---|---|
| `standard` | `apps/standard` | `tuqiang_standard` | Tuqiang Android / iOS |
| `ohos` | `apps/ohos` | `tuqiang_ohos` | Tuqiang HarmonyOS |
| `laoying_standard` | `apps/laoying_standard` | `laoying_standard` | Laoying Android / iOS |
| `laoying_ohos` | `apps/laoying_ohos` | `laoying_ohos` | Laoying HarmonyOS |

只验证本次涉及的 target，不要把某个未涉及 shell 的平台差异自动扩展进答案。目标位于 `packages/core`、`packages/shared`、`packages/plugins` 或其他公共层时，继续反查调用方：只有 Tuqiang 调用就按 Tuqiang，只有 Laoying 调用就按 Laoying，两边都调用则标“共享/双产品”并分别追接线。

## 4. PowerShell 示例

从当前对话项目或目标文件目录解析 Git 根目录：

```powershell
$projectRoot = (git -C '<CURRENT_PROJECT_OR_SOURCE_PATH>' rev-parse --show-toplevel).Trim()
```

验证稳定结构和 package identity：

```powershell
$requiredMarkers = @(
  'apps/standard/pubspec.yaml',
  'apps/ohos/pubspec.yaml',
  'apps/tuqiang_app/pubspec.yaml',
  'tool/project.dart'
)
$missingMarkers = $requiredMarkers | Where-Object {
  -not (Test-Path -LiteralPath (Join-Path $projectRoot $_)) -or
  [string]::IsNullOrWhiteSpace((& git -C $projectRoot ls-files -- $_).Trim())
}

$expectedPackages = @{
  'apps/standard/pubspec.yaml' = 'tuqiang_standard'
  'apps/ohos/pubspec.yaml' = 'tuqiang_ohos'
  'apps/tuqiang_app/pubspec.yaml' = 'tuqiang'
}
$identityMismatch = @(
  foreach ($pubspec in $expectedPackages.GetEnumerator()) {
    $match = Select-String -LiteralPath (Join-Path $projectRoot $pubspec.Key) `
      -Pattern '^name:\s*(\S+)\s*$'
    $actual = if ($match) { $match.Matches.Groups[1].Value } else { '<missing>' }
    if ($actual -ne $pubspec.Value) {
      "$($pubspec.Key): expected=$($pubspec.Value), actual=$actual"
    }
  }
)

$isTargetRepo = $missingMarkers.Count -eq 0 -and $identityMismatch.Count -eq 0
```

这是基础身份的可选实现示例；Laoying trio 的完整性与 identity 继续按上节校验，或直接复用 `tuqiang-project-map` 的公共协议。用户明确给出的非 Git 目录仍可直接做完整身份校验；自动发现时若 Git 根目录不可得，则请求用户路径。不得改成向任意父目录或整块磁盘盲目试探。

## 5. 后续使用约定

- 文档与命令统一写 `<TUQIANG_ROOT>`；真正回答用户时输出本次解析后的绝对路径。
- 所有搜索限制在已验证根目录内，例如：

```powershell
rg -n '目标Widget|目标方法|目标状态' '<TUQIANG_ROOT>'
rg -n '目标符号\(' '<TUQIANG_ROOT>/apps' '<TUQIANG_ROOT>/packages'
```

- 行号必须来自本次搜索或逐行读取，不能沿用项目地图中的历史行号。
- 如果兄弟 Skill 不可用，根目录解析、产品判定、源码检索和完整链路讲解仍必须独立完成。
