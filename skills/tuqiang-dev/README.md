# tuqiang-dev

当前版本：1.9.0

途强（tuqiang）三端 Flutter 项目（`D:\Code\tuqiang`）的**专属开发规范 Skill**。

面向不会写代码或只会 Vue3 的同学 + AI 编码助手，把「Android / iOS / 鸿蒙」三端开发的
边界、目录归属、TQHttp 网络请求、Riverpod 状态、权限、sc 适配、国际化、命名路由和验证矩阵
固化成可执行的项目规范。它优先遵循当前源码、CI、边界脚本和迁移文档，不把所有模块强行套成同一模板。

> 凡是在 `D:\Code\tuqiang` 仓库内开发新功能、改 Bug、加页面、加接口，一律先读本 Skill。

## Skill 内容一览

- `SKILL.md`：事实来源、项目速查、统一命令、三端边界、包归属、风险分级工作流、验证矩阵和参考文件索引
- `references/`：按需深读的模板与细则

| 文件 | 内容 |
|---|---|
| `project-structure.md` | 目录地图、「加东西动哪个包」决策表 |
| `assets-guide.md` | 设计源、资源 owner、package asset 路径、倍率目录和实际 `core_ui` 组件 |
| `testing.md` | 按行为风险选择单测、Widget/契约测试，以及项目 migration runner |
| `networking.md` | TQHttp、ResultModel、TCheck、Model/Repository 边界和 fake 注入 |
| `state-management.md` | Riverpod 2.6.1 的 StateNotifier/Notifier 选择、生命周期和 session reset |
| `i18n.md` | tr/keyTr/multiKeyTr、9 语言 JSON 维护、禁止 `final` 成员变量缓存 `.tr` |
| `sizing-ui.md` | sc 尺寸适配原理、安全区与 core_ui 清单 |
| `permissions.md` | TQPermissionManager 权限申请、永久拒绝引导 |
| `routing.md` | 字符串路由注册四步、传参约定 |
| `compatibility.md` | 三端兼容铁律细则、平台差异三种注入模式 |
| `code-review-checklist.md` | 真实高风险审查项：异常、异步、类型、平台、资源、路由和状态 |
| `new-feature-walkthrough.md` | 从 owner、接口、页面到验证的最小实施清单 |

## 安装

### Claude Code

```bash
# 方式一：从本插件市场安装（含两个 skill）
/plugin marketplace add tuqiang/flutter-skill

# 方式二：直接复制到项目
mkdir -p .agents/skills/tuqiang-dev
# 将 SKILL.md 与 references/ 整个目录复制进去
```

### 手动安装到全局 skills 目录

```bash
cp -r skills/tuqiang-dev ~/.codex/skills/
```

## 使用

在对话中通过 `@` 引用即可激活：

```
@tuqiang-dev 帮我在设置页加一个"清除缓存"入口
```

或在 Claude Code 中使用斜杠命令：

```
/tuqiang-dev
```

## 适用场景

- 在途强三端 Flutter monorepo 里实现、测试、构建或评审需求
- 只会 Vue3 的同学照着映射表和模板参与 Flutter 三端开发
- AI 编码助手需要统一的项目铁律（统一构建入口、鸿蒙边界检查、依赖选型）

> 注意：本 Skill 与业务仓库强绑定（命令入口、包名、路径均以 `D:/Code/tuqiang` 为准），
> 换一个项目请勿直接复用。

## 许可证

Apache 2.0 © tuqiang
