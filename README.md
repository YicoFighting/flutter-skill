# flutter-skill

版本 2.4.0。四个 Skill 只服务 Tuqiang，通过用户当前指定或绑定的业务项目定位 checkout，不绑定盘符和目录名。业务仓库自带的 `AGENTS.md`、`DESIGN.md` 与 `.codex/skills` 优先于本技能；references 是检索入口，不是永久事实。

| Skill | 版本 | 职责 |
|---|---|---|
| [tuqiang-project-map](skills/tuqiang-project-map/SKILL.md) | 2.4.0 | 按问题定位 owner、账号、状态、平台/地图/设备变体证据 |
| [flutter-to-web](skills/flutter-to-web/SKILL.md) | 2.4.0 | 用最短证据链解释行为，按需提供 Vue3/React 对照 |
| [tuqiang-dev](skills/tuqiang-dev/SKILL.md) | 2.4.0 | 项目规则优先，本地复用，最小实现，按风险验证 |
| [tuqiang-change-retrospective](skills/tuqiang-change-retrospective/SKILL.md) | 2.4.0 | 显式要求后按改动规模生成学习 Markdown |

本版按 2026-11-09 的 Tuqiang 源码更新事实（鸿蒙地图统一走百度 ArkTS、设备页面族新分支、新增公共组件、项目自带规范），并把 references 由 35 份合并为 17 份。

- [变体与构建](skills/tuqiang-project-map/references/variants.md)：平台、地图 7 行候选、设备列表分流、flavor/渠道/SDK。
- [本地复用与纯函数](skills/tuqiang-dev/references/local-style-and-reuse.md)、[国际化与展示取值](skills/tuqiang-dev/references/i18n.md)：已有能力优先，翻译一次，兼容只在一个边界。
- [验证](skills/tuqiang-dev/references/testing.md)：遵守业务仓库"默认不执行 `flutter test`、不装依赖"，默认静态分析 + 确定性脚本 + diff。

完整变更见 [CHANGELOG.md](CHANGELOG.md)。

## 结构

    skills/
    ├─ tuqiang-project-map/        # 7 references + scripts/validate_project_root.py
    ├─ flutter-to-web/             # references/web-analogies.md
    ├─ tuqiang-dev/                # 7 references + scripts/validate_tuqiang_i18n.py
    └─ tuqiang-change-retrospective/  # report-contract.md、git-causality.md

四个 Skill 通过相对路径共享事实源，必须将四个完整目录安装到同一个 skills 根，不能只复制 SKILL.md 或单独安装其中一个。

## Windows 安装或升级

升级时精确替换四个目录，避免已删除 reference 残留：

    $sourceRoot = (Resolve-Path -LiteralPath '.\skills').Path
    $skillNames = @(
      'tuqiang-project-map',
      'flutter-to-web',
      'tuqiang-dev',
      'tuqiang-change-retrospective'
    )
    $destinationRoots = @(
      (Join-Path $env:USERPROFILE '.codex\skills'),
      (Join-Path $env:USERPROFILE '.gemini\config\skills')
    )

    foreach ($destinationRootInput in $destinationRoots) {
      $destinationRoot = [IO.Path]::GetFullPath($destinationRootInput)
      New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null
      foreach ($skillName in $skillNames) {
        $source = Join-Path $sourceRoot $skillName
        $destination = [IO.Path]::GetFullPath((Join-Path $destinationRoot $skillName))
        if ([IO.Path]::GetDirectoryName($destination) -ne $destinationRoot -or
            [IO.Path]::GetFileName($destination) -ne $skillName) {
          throw "拒绝非预期目标：$destination"
        }
        if (Test-Path -LiteralPath $destination) {
          Remove-Item -LiteralPath $destination -Recurse -Force
        }
        Copy-Item -LiteralPath $source -Destination $destinationRoot -Recurse -Force
      }
    }

## macOS/Linux 安装或升级

    mkdir -p ~/.codex/skills
    for skill in tuqiang-project-map flutter-to-web tuqiang-dev tuqiang-change-retrospective; do
      rm -rf -- "$HOME/.codex/skills/$skill"
      cp -R -- "skills/$skill" "$HOME/.codex/skills/$skill"
    done

Codex 可用 $skill-name 显式调用；除复盘 Skill 保持显式调用外，其余也可由客户端自动匹配。

## 验证与维护

- 修改 Skill 时同步版本、根 package.json、CHANGELOG、根 README 与对应 Skill README。
- 运行 skill-creator 的 quick_validate.py，并验证脚本、链接、UTF-8 无 BOM 与 diff。
- 完成后递归同步当前用户的 Gemini 全局目录并校验文件集合与 SHA-256；安装到其他客户端时使用对应目的目录，不写死用户名。
- 未经用户明确要求，不执行 git commit 或 git push。

许可证：Apache 2.0。
