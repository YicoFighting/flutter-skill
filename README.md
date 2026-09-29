# flutter-skill

版本 2.3.0。四个 Skill 只服务 Tuqiang，通过用户当前指定或绑定的业务项目定位 checkout，不绑定盘符和目录名。源码变更后重新核验目标 symbol，references 作为检索入口，不作为永久事实。

| Skill | 版本 | 职责 |
|---|---|---|
| [tuqiang-project-map](skills/tuqiang-project-map/SKILL.md) | 2.2.0 | 按问题定位 owner、账号、状态、平台与变体证据 |
| [flutter-to-web](skills/flutter-to-web/SKILL.md) | 2.2.0 | 用最短证据链解释行为，按需提供 Vue3/React 对照 |
| [tuqiang-dev](skills/tuqiang-dev/SKILL.md) | 2.3.0 | 本地复用优先，最小实现，按风险验证 |
| [tuqiang-change-retrospective](skills/tuqiang-change-retrospective/SKILL.md) | 2.2.0 | 显式要求后按改动规模生成学习 Markdown |

本版精简四个入口和重复模板：简单任务不再强制上下文卡、完整链路、全量矩阵或长报告；只加载影响当前问题的规则。

- [本地复用与纯函数](skills/tuqiang-dev/references/local-style-and-reuse.md)：优先使用已有状态、函数、组件；缺少的业务计算显式输入、确定输出、无副作用。IO/状态发布保留在既有 owner，不迁移存量。
- [国际化与展示取值](skills/tuqiang-dev/references/i18n.md)：区分 source key、已译 label 和业务值；翻译一次，统一 fallback，字段兼容在一个边界处理。manifest 与语言选择列表分开核验。
- [当前 UI 与分栏](skills/tuqiang-dev/references/sizing-ui.md)：复用已有自适应布局/路由，区分 pane 与整窗；[项目地图](skills/tuqiang-project-map/references/infrastructure-and-cross-cutting.md) 提供当前封装入口。
- [按风险验证](skills/tuqiang-dev/references/testing.md)：局部改动聚焦相关检查，必要验证通过后停止。账号、异步、平台和构建专题仍由各入口按需路由。

完整变更见 [CHANGELOG.md](CHANGELOG.md)。

## 结构

    skills/
    ├─ tuqiang-project-map/
    │  └─ scripts/validate_project_root.py
    ├─ flutter-to-web/
    ├─ tuqiang-dev/
    │  └─ scripts/validate_tuqiang_i18n.py
    └─ tuqiang-change-retrospective/

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
