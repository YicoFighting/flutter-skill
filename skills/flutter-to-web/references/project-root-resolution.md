# 途强项目动态根目录协议

> 每次需要读取项目源码时执行。目标是得到经验证的 `<TUQIANG_ROOT>`，而不是记住某台电脑上的绝对路径。

## 1. 解析顺序

按以下优先级选择候选目录：

1. 用户在当前请求中明确给出的项目根目录；
2. `tuqiang-project-map` 已在本次任务中解析并验证的根目录；
3. 当前选中文件、打开文件或目标源码所在目录向上找到的 Git 根目录；
4. 当前工作区各根目录或当前目录向上找到的 Git 根目录。

不要把 Skill 仓库误当成 Flutter 项目。不要扫描整块磁盘，也不要依赖公司/家庭电脑的盘符、用户名或历史路径。多个候选同时通过验证时，根据当前选中文件属于哪个候选来选择；仍有歧义再向用户确认。

## 2. 仓库身份验证

候选目录必须通过与 `tuqiang-project-map` 完全相同的五个结构标志：

```text
apps/standard/pubspec.yaml
apps/ohos/pubspec.yaml
apps/tuqiang_app/pubspec.yaml
packages/shared/shared_business/pubspec.yaml
tool/project.dart
```

随后校验四个 package identity：

| pubspec | 必须声明的 `name` |
|---|---|
| `apps/standard/pubspec.yaml` | `tuqiang_standard` |
| `apps/ohos/pubspec.yaml` | `tuqiang_ohos` |
| `apps/tuqiang_app/pubspec.yaml` | `tuqiang` |
| `packages/shared/shared_business/pubspec.yaml` | `shared_business` |

任何标志缺失或 identity 不匹配，都不能仅凭目录名、历史路径或目标 symbol 猜测它是途强项目。读取根 `AGENTS.md` 并确认目标 symbol 属于该 checkout；项目结构将来变化但无法同时通过上述身份校验时，停止检索并让用户确认，而不是自行放宽条件。

## 3. PowerShell 示例

从当前源码目录解析 Git 根目录：

```powershell
$tuqiangRoot = (git -C '<SOURCE_OR_WORKSPACE_PATH>' rev-parse --show-toplevel).Trim()
```

验证结构标志和 package identity：

```powershell
$requiredMarkers = @(
  'apps/standard/pubspec.yaml',
  'apps/ohos/pubspec.yaml',
  'apps/tuqiang_app/pubspec.yaml',
  'packages/shared/shared_business/pubspec.yaml',
  'tool/project.dart'
)
$missingMarkers = $requiredMarkers | Where-Object {
  -not (Test-Path -LiteralPath (Join-Path $tuqiangRoot $_))
}

$expectedPackages = @{
  'apps/standard/pubspec.yaml' = 'tuqiang_standard'
  'apps/ohos/pubspec.yaml' = 'tuqiang_ohos'
  'apps/tuqiang_app/pubspec.yaml' = 'tuqiang'
  'packages/shared/shared_business/pubspec.yaml' = 'shared_business'
}
$identityMismatch = @(
  foreach ($pubspec in $expectedPackages.GetEnumerator()) {
    $match = Select-String -LiteralPath (Join-Path $tuqiangRoot $pubspec.Key) `
      -Pattern '^name:\s*(\S+)\s*$'
    $actual = if ($match) { $match.Matches.Groups[1].Value } else { '<missing>' }
    if ($actual -ne $pubspec.Value) {
      "$($pubspec.Key): expected=$($pubspec.Value), actual=$actual"
    }
  }
)

$isTuqiangRepo = $missingMarkers.Count -eq 0 -and $identityMismatch.Count -eq 0
```

这只是可选实现示例。用户明确给出的非 Git 目录仍可直接做完整身份校验；从选中文件或 workspace 自动发现时若 Git 根目录不可得，则询问用户路径。不得改成向任意父目录或整块磁盘逐级试探。

## 4. 后续使用约定

- 文档与命令统一写 `<TUQIANG_ROOT>`；真正回答用户时输出解析后的当前绝对路径。
- 所有搜索限制在已验证根目录内，例如：

```powershell
rg -n '目标Widget|目标方法|目标Provider' '<TUQIANG_ROOT>'
rg -n '目标Provider\(' '<TUQIANG_ROOT>/apps' '<TUQIANG_ROOT>/packages'
```

- 行号必须来自本次搜索或逐行读取，不能沿用项目地图中的历史行号。
- 如果兄弟 Skill 不可用，根目录解析、源码检索和完整链路讲解仍必须独立完成。
