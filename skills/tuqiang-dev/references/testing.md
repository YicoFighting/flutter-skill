# Tuqiang 测试与验证

测试围绕用户可观察行为、账号模式、契约和真实风险，不按文件数机械生成。先写可证伪验收；需求多解时先澄清，不能用测试固化模型自己的方案。

## 风险选择

| 变更 | 最低验证 |
|---|---|
| Model、JSON、参数 | 缺字段、类型异常、nullable、兼容字段、清空/省略语义 |
| 路由/payload/result/effect | owner、builder、参数、返回、栈与副作用 |
| 页面/表单 | loading/empty/error/content、按钮、布局与生命周期 |
| 权限/MethodChannel | 静态契约 + 受影响端行为，必要时真机 |
| 文档/格式 | diff、链接、UTF-8 无 BOM |

账号、平台、地图与设备组合回到 [覆盖门](implementation-coverage.md)，异步竞态/销毁/身份/资源测试回到 [异步生命周期](async-lifecycle.md)，国际化结构与运行验收回到 [i18n](i18n.md)。测试放真实 owner 的 `test/`，包外只经公开 API；fixture/fake 保持真实契约，不把假 URL、延时数据或“永远成功”实现带入生产。

## i18n 入口

先按 [i18n](i18n.md) 运行确定性校验，再执行项目专属测试：

```powershell
Push-Location -LiteralPath (Join-Path $tuqiangRoot 'apps/tuqiang_app')
flutter test test/app/i18n/app_i18n_loader_test.dart
Pop-Location

Push-Location -LiteralPath (Join-Path $tuqiangRoot 'packages/core/core_i18n')
flutter test
Pop-Location
```

## 宿主与边界

从仓库根运行改动 package 测试及：

```powershell
dart run tool/project.dart analyze standard
dart run tool/project.dart analyze ohos
pwsh .\tool\check_migration_boundaries.ps1 -ProductScope tuqiang
```

`dart run tool/project.dart test <target>` 只运行宿主 Flutter tests，不等于业务 package 或全仓测试。`tool/run_migration_tests.ps1` 覆盖哪些目标要以当前清单为准。

boundary 可能因无关历史基线失败；记录完整命令、相关子检查和归属，不能把基线算作本次回归，也不能因子检查通过就宣称整个 gate 全绿。修改 `core/shared/plugin` 公开 API 时搜索全部调用方并运行直接受影响的 contract/tests，这不扩大 Tuqiang 业务范围。

## 证据等级

静态/analyze、单测、build、模拟器/真机、CI、未执行与已交接不得互相冒充；`standard` analyze 不证明 Android/iOS 两端运行。沿 [覆盖台账](implementation-coverage.md) 记录命令、通过、失败、未运行和交接，每个 `无需修改` 有源码证据，不用“其余类似”关闭行。
