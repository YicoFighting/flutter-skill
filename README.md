# flutter-skill

版本 2.0.1。四个 Skill 只服务 Tuqiang Flutter monorepo：

| Skill | 职责 |
|---|---|
| [tuqiang-project-map](skills/tuqiang-project-map/SKILL.md) | 从当前 checkout 核验根目录、账号模式、owner、链路和变体事实 |
| [flutter-to-web](skills/flutter-to-web/SKILL.md) | 向 Vue3/React 开发者解释事件、异步数据、状态与 UI |
| [tuqiang-dev](skills/tuqiang-dev/SKILL.md) | 开发、修复、测试与评审 |
| [tuqiang-change-retrospective](skills/tuqiang-change-retrospective/SKILL.md) | 用户显式要求后，只读复盘并生成学习 Markdown |

2.0.1 在 Tuqiang-only 范围内继续瘦身，并把重复规则集中到五个事实源：

- [账号模式](skills/tuqiang-project-map/references/account-mode.md)：personal / enterprise / both / unknown 与 isEnterprise 传播链。
- [国际化](skills/tuqiang-dev/references/i18n.md)：当前 manifest、全 locale、占位符、缺 key 回显和语言切换。
- [异步生命周期](skills/tuqiang-dev/references/async-lifecycle.md)：owner、新鲜度、身份与资源四道防线。
- [实施覆盖](skills/tuqiang-dev/references/implementation-coverage.md)：三端、地图和设备 route leaf 的条件矩阵。
- [复盘输出](skills/tuqiang-change-retrospective/references/report-contract.md)：Bug、需求与混合模式的 Markdown 契约。

其他入口和 reference 只说明触发条件并链接事实源。详细版本记录见 [CHANGELOG.md](CHANGELOG.md)。

## 结构

    skills/
    ├─ tuqiang-project-map/
    ├─ flutter-to-web/
    ├─ tuqiang-dev/
    │  └─ scripts/validate_tuqiang_i18n.py
    └─ tuqiang-change-retrospective/

必须复制完整 Skill 目录，不能只复制 SKILL.md。

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
- 完成后精确同步当前用户的 Gemini 全局目录。
- 未经用户明确要求，不执行 git commit 或 git push。

许可证：Apache 2.0。
