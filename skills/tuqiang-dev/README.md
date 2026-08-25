# tuqiang-dev

途强（tuqiang）三端 Flutter 项目（`D:\Code\tuqiang`）的**专属开发规范 Skill**。

面向不会写代码或只会 Vue3 的同学 + AI 编码助手，把「Android / iOS / 鸿蒙」三端开发的
铁律、目录规范、dio 网络请求、Riverpod 状态、权限、sc 适配、国际化、路由注册等全部固化成
「照抄模板就能干活」的套路。

> 凡是在 `D:\Code\tuqiang` 仓库内开发新功能、改 Bug、加页面、加接口，一律先读本 Skill。

## Skill 内容一览

- `SKILL.md`：三条铁律、仓库一分钟速览、Vue3 头脑映射表、五步开发闭环（对齐方案 → 审批 → 编码 → 验证 → 审查）、参考文件索引
- `references/`：按需深读的模板与细则

| 文件 | 内容 |
|---|---|
| `project-structure.md` | 目录地图、「加东西动哪个包」决策表 |
| `assets-guide.md` | **UI 切图与静态资源规范**：杜绝 Icons 脑补、蓝湖导出避坑、2x/3x 倍图、命名与常量注册 |
| `testing.md` | **测试规范与提测交付标准**：按需生成必问原则、Unit/Widget 测试模板、提测交付单 Markdown |
| `networking.md` | dio/TQHttp 封装、ResultModel、TCheck 安全取值、Model 四大铁律与代码模板、动态接口暂缺异步 Mock |
| `state-management.md` | Riverpod State+Controller+Provider 三板斧、生命周期防修改红线 |
| `i18n.md` | tr/keyTr/multiKeyTr、9 语言 JSON 维护、禁止 `final` 成员变量缓存 `.tr` |
| `sizing-ui.md` | sc 尺寸适配原理、安全区与 core_ui 清单 |
| `permissions.md` | TQPermissionManager 权限申请、永久拒绝引导 |
| `routing.md` | 字符串路由注册四步、传参约定 |
| `compatibility.md` | 三端兼容铁律细则、平台差异三种注入模式 |
| `new-feature-walkthrough.md` | 从零实现一个完整页面的分步模板 |

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

- 在途强三端 Flutter monorepo 里实现任何需求之前，让 AI 先读规范再动手
- 只会 Vue3 的同学照着映射表和模板参与 Flutter 三端开发
- AI 编码助手需要统一的项目铁律（统一构建入口、鸿蒙边界检查、依赖选型）

> 注意：本 Skill 与业务仓库强绑定（命令入口、包名、路径均以 `D:\Code\tuqiang` 为准），
> 换一个项目请勿直接复用。

## 许可证

Apache 2.0 © tuqiang
