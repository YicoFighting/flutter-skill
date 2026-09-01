# 仓库根目录发现与校验

`<TUQIANG_ROOT>` 是当前对话要处理的 Flutter monorepo 根目录，不是固定盘符。公司电脑、个人电脑、worktree 与其他检出目录都应使用同一套协议。

## 1. 发现顺序

按以下优先级确定候选：

1. 用户在当前任务中明确给出的项目目录。
2. 当前 Codex 对话所附项目/工作区的 Git 根目录；未显式指定路径时，它就是用户指定项目的第一隐式含义。
3. 本任务内已经完成本文全部校验、且对话项目/checkout 未变化的 `$tuqiangRoot`。
4. 当前打开、选中或目标源码文件所属的 Git 根目录，但仅在没有对话项目上下文时作为候选。
5. 上下文缺失、校验失败、对话项目与目标文件属于不同仓库，或存在多个合法候选时，询问用户。

不递归扫描整个磁盘或用户目录，不复用过去任务的绝对路径。用户已经给出路径时，不再用当前工作区覆盖它。

## 2. 获取 Git 根目录

用户明确给出路径：

```powershell
$tuqiangCandidate = (Resolve-Path -LiteralPath '<用户给出的项目目录>').Path
$tuqiangRoot = (& git -C $tuqiangCandidate rev-parse --show-toplevel).Trim()
```

从当前对话项目/工作区发现：

```powershell
$projectContextPath = '<当前 Codex 对话所附项目或工作区路径>'
$tuqiangRoot = (& git -C $projectContextPath rev-parse --show-toplevel).Trim()
```

Git 失败、返回空值、返回了 Skill 仓库，或与用户给出的候选不一致时，不猜测；进入身份校验，失败后询问用户。

## 3. 稳定仓库身份

根校验只依赖稳定的 app/tool 身份，不依赖迁移中的某个 shared package。基础 Tuqiang trio 与项目工具必须同时存在且被 Git 跟踪：

```powershell
$tuqiangStableIdentity = @{
  'apps/standard/pubspec.yaml' = 'tuqiang_standard'
  'apps/ohos/pubspec.yaml' = 'tuqiang_ohos'
  'apps/tuqiang_app/pubspec.yaml' = 'tuqiang'
}

$tuqiangStableMarkers = @(
  $tuqiangStableIdentity.Keys
  'tool/project.dart'
)

$tuqiangMissingMarkers = @(
  foreach ($relativePath in $tuqiangStableMarkers) {
    $absolutePath = Join-Path $tuqiangRoot $relativePath
    $trackedPath = (& git -C $tuqiangRoot ls-files -- $relativePath).Trim()
    if (-not (Test-Path -LiteralPath $absolutePath) -or [string]::IsNullOrWhiteSpace($trackedPath)) {
      $relativePath
    }
  }
)

if ($tuqiangMissingMarkers.Count -gt 0) {
  throw "候选目录不是当前途强 Flutter monorepo；缺少稳定 tracked 特征: $($tuqiangMissingMarkers -join ', ')"
}
```

再核对 package identity：

```powershell
function Test-PubspecIdentity([string]$root, [hashtable]$expected) {
  @(
    foreach ($entry in $expected.GetEnumerator()) {
      $pubspecPath = Join-Path $root $entry.Key
      $match = Select-String -LiteralPath $pubspecPath -Pattern '^name:\s*(\S+)\s*$'
      $actual = $match.Matches.Groups[1].Value
      if ($actual -ne $entry.Value) {
        "$($entry.Key): expected=$($entry.Value), actual=$actual"
      }
    }
  )
}

$tuqiangIdentityMismatch = Test-PubspecIdentity $tuqiangRoot $tuqiangStableIdentity
if ($tuqiangIdentityMismatch.Count -gt 0) {
  throw "Tuqiang package identity 不匹配: $($tuqiangIdentityMismatch -join '; ')"
}
```

## 4. 可选 Laoying trio 校验

最新仓库还包含 Laoying 三个 app。为兼容缺少该产品线的较早 checkout，它们不是基础根标记；但只要出现任意一个，就必须三者齐全、被 Git 跟踪且 identity 匹配：

```powershell
$laoyingIdentity = @{
  'apps/laoying_standard/pubspec.yaml' = 'laoying_standard'
  'apps/laoying_ohos/pubspec.yaml' = 'laoying_ohos'
  'apps/laoying_app/pubspec.yaml' = 'laoying_app'
}

$laoyingPresent = @(
  $laoyingIdentity.Keys | Where-Object {
    Test-Path -LiteralPath (Join-Path $tuqiangRoot $_)
  }
)

if (($laoyingPresent.Count -ne 0) -and ($laoyingPresent.Count -ne $laoyingIdentity.Count)) {
  throw 'Laoying app trio 仅部分存在；请确认 checkout 或迁移状态。'
}

if ($laoyingPresent.Count -eq $laoyingIdentity.Count) {
  $untrackedLaoying = @(
    $laoyingIdentity.Keys | Where-Object {
      [string]::IsNullOrWhiteSpace((& git -C $tuqiangRoot ls-files -- $_).Trim())
    }
  )
  if ($untrackedLaoying.Count -gt 0) {
    throw "Laoying app identity 文件未被 Git 跟踪: $($untrackedLaoying -join ', ')"
  }

  $laoyingIdentityMismatch = Test-PubspecIdentity $tuqiangRoot $laoyingIdentity
  if ($laoyingIdentityMismatch.Count -gt 0) {
    throw "Laoying package identity 不匹配: $($laoyingIdentityMismatch -join '; ')"
  }
}
```

校验通过后：

```powershell
Set-Location -LiteralPath $tuqiangRoot
```

## 5. 不要用目录外观判断 package

- 当前迁移可能留下被忽略的 `.dart_tool` 或生成文件；只有 tracked `pubspec.yaml` 及其 `name:` 才能证明 package 存在。
- 需要确认 package 时使用 `git ls-files 'packages/<group>/<name>/**'`、读取 `pubspec.yaml`，再检查公共 barrel；不要因 `Test-Path` 为真就认定它仍是生产 package。
- `packages/shared/shared_business` 已不是当前 tracked package，不能再用它校验根目录或作为默认 owner。

## 6. 路径与证据规则

- reference 只保存相对 `$tuqiangRoot` 的路径，不固定盘符或用户名。
- 搜索在 `$tuqiangRoot` 下执行，结果保留相对路径、当前行号与 symbol。
- 交付可点击链接时，再用 `$tuqiangRoot` 组成当前机器的绝对路径。
- 任务中切换项目、worktree、branch 或 checkout 后，重新执行全部校验。
