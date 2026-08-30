# 途强仓库根目录发现与校验

`<TUQIANG_ROOT>` 是“当前这份途强 Flutter monorepo 的根目录”，不是某台电脑的固定路径。同一 skill 应可在公司、家中、worktree 或其他检出目录中使用。

## 1. 发现顺序

按以下优先级确定唯一候选根目录：

1. 用户在当前任务中明确给出的项目目录。
2. 本次任务中已经按本文完成全部校验的 `<TUQIANG_ROOT>`。
3. 用户选中的 Dart 文件、打开文件或目标文件所在 Git 仓库的根目录。
4. 当前 Codex 项目/工作区的 Git 根目录。
5. 若以上上下文缺失、校验失败或出现多个候选，询问用户的当前项目路径。

不递归扫描整个磁盘、用户目录或任意父目录，不因为过去在某个路径找到过项目就默认继续使用。

## 2. 获取候选根目录

用户已给出路径时：

```powershell
$tuqiangRoot = (Resolve-Path -LiteralPath '<TUQIANG_ROOT>').Path
```

从选中文件或工作区发现时，将占位符替换为已知的文件所在目录或工作区目录：

```powershell
$tuqiangRoot = (& git -C '<选中文件所在目录或工作区>' rev-parse --show-toplevel).Trim()
```

Git 命令失败、返回空值或返回了当前 Skill 仓库时，不继续猜测；先执行下节校验，不通过就询问用户。

## 3. 仓库身份校验

候选目录必须同时具有三端宿主、共享业务包和项目工具特征。以下检查为通过条件，而不是用来在磁盘上搜索仓库：

```powershell
$tuqiangMarkers = @(
  'apps/standard/pubspec.yaml'
  'apps/ohos/pubspec.yaml'
  'apps/tuqiang_app/pubspec.yaml'
  'packages/shared/shared_business/pubspec.yaml'
  'tool/project.dart'
)

$tuqiangMissingMarkers = @(
  $tuqiangMarkers | Where-Object {
    -not (Test-Path -LiteralPath (Join-Path $tuqiangRoot $_))
  }
)

if ($tuqiangMissingMarkers.Count -gt 0) {
  throw "当前候选目录不是已知的途强 Flutter monorepo；缺少特征: $($tuqiangMissingMarkers -join ', ')"
}
```

目录结构通过后还要核对四个 `pubspec.yaml` 的 package identity，避免把结构相似的仓库当成途强项目：

```powershell
$tuqiangPubspecIdentity = @{
  'apps/standard/pubspec.yaml' = 'tuqiang_standard'
  'apps/ohos/pubspec.yaml' = 'tuqiang_ohos'
  'apps/tuqiang_app/pubspec.yaml' = 'tuqiang'
  'packages/shared/shared_business/pubspec.yaml' = 'shared_business'
}

$tuqiangIdentityMismatch = @(
  foreach ($tuqiangPubspec in $tuqiangPubspecIdentity.GetEnumerator()) {
    $tuqiangPubspecPath = Join-Path $tuqiangRoot $tuqiangPubspec.Key
    $tuqiangDeclaredName = (
      Select-String -LiteralPath $tuqiangPubspecPath -Pattern '^name:\s*(\S+)\s*$'
    ).Matches.Groups[1].Value
    if ($tuqiangDeclaredName -ne $tuqiangPubspec.Value) {
      "$($tuqiangPubspec.Key): expected=$($tuqiangPubspec.Value), actual=$tuqiangDeclaredName"
    }
  }
)

if ($tuqiangIdentityMismatch.Count -gt 0) {
  throw "当前候选目录的 package identity 不匹配: $($tuqiangIdentityMismatch -join '; ')"
}
```

校验通过后，后续 reference 中的命令统一使用：

```powershell
Set-Location -LiteralPath $tuqiangRoot
```

## 4. 路径与证据规则

- reference 只保存相对于 `$tuqiangRoot` 的路径；不在说明、示例或输出模板中固定盘符或用户目录。
- 搜索命令在 `$tuqiangRoot` 下执行，搜索结果保留“相对路径 + 当前行号 + symbol”。
- 向用户交付可点击文件链接时，再用 `$tuqiangRoot` 将相对路径组成当前机器的绝对路径。
- 仓库在任务期间切换到其他 worktree 或 checkout 时，重新发现与校验，不复用旧的 `$tuqiangRoot`。
