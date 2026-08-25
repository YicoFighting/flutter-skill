# 测试规范与提测交付标准（testing）

在 AI 辅助编码的大规模应用背景下，为了防止 AI 产生逻辑幻觉、保证交付质量，并为测试团队提供可追溯的验收依据，本规范定义了 **代码级测试伴生** 与 **提测交付单** 标准。

---

## 1. 核心铁律：测试文件按需触发原则

> ⚠️ **【强制红线】**：
> 1. **事前必问**：在需求调研与方案对齐阶段（阶段一/阶段二），AI **必须主动向用户提问是否需要生成测试文件/用例**；
> 2. **未明确同意严禁生成**：若用户明确表示“不需要”，或者未明确回答需要测试内容，AI **严禁擅自生成任何测试文件**，避免增加项目体积和无谓的维护成本；
> 3. **一旦确认全程伴生**：若用户**主动提及**需要测试文件，或在询问中明确回复“需要”，则在后续**每一次代码新增或修改后，AI 必须强制同步生成/修改对应的测试文件（`test/`）**，并在交付时出具《提测交付单》。

---

## 2. 自动化测试分层与命名规范

在 `packages/feature/feature_xxx/` 或对应 package 下，测试文件必须镜像对应 `lib/src/` 的目录结构：

```text
packages/feature/feature_auth/
├── lib/
│   └── src/
│       ├── model/login_param.dart
│       ├── notifier/contact_us_notifier.dart
│       └── page/contact_us_page.dart
└── test/
    ├── model/login_param_test.dart             # Model 序列化与边界测试
    ├── notifier/contact_us_notifier_test.dart   # 业务逻辑与状态流转单测
    └── page/contact_us_page_test.dart          # 关键 Widget 渲染与事件测试
```

### 分层测试编写标准

| 测试类型 | 适用对象 | 关注重点 |
|---|---|---|
| **单元测试 (Unit Test)** | Notifier、Controller、Service、Utils | 正常业务流、错误分支、空数据/异常边界、状态切换 |
| **模型测试 (Model Test)** | Data Model、Request/Response Param | `fromJson`/`toJson` 解析、空字段容错、默认值 |
| **组件测试 (Widget Test)** | 关键页面、核心表单、复合组件 | 关键文案展示、按钮点击响应、加载中状态、禁用状态 |

---

## 3. 标准测试代码模板

### ① 业务逻辑层测试（Notifier / Riverpod）
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';
import 'package:feature_auth/src/notifier/contact_us_notifier.dart';

void main() {
  group('ContactUsNotifier 业务逻辑测试', () {
    late ContactUsNotifier notifier;

    setUp(() {
      notifier = ContactUsNotifier();
    });

    test('【正常流】初始化时状态应包含默认联系方式', () {
      expect(notifier.state.phoneNumber, isNotEmpty);
      expect(notifier.state.isLoading, isFalse);
    });

    test('【异常/边界值】当号码为空时调用拨打应返回 false 并提示错误', () async {
      final result = await notifier.makePhoneCall('');
      expect(result, isFalse);
    });
  });
}
```

### ② 数据模型解析测试（Model）
```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:feature_auth/src/model/contact_info_model.dart';

void main() {
  group('ContactInfoModel 序列化测试', () {
    test('【正常流】正确解析合法 Json 数据', () {
      final json = {'phone': '400-123-4567', 'service_time': '9:00-18:00'};
      final model = ContactInfoModel.fromJson(json);
      expect(model.phone, '400-123-4567');
    });

    test('【边界容错】缺少字段时应安全降级，不抛出异常', () {
      final json = <String, dynamic>{};
      final model = ContactInfoModel.fromJson(json);
      expect(model.phone, isEmpty);
    });
  });
}
```

---

## 4. 《需求提测交付单》标准模板

当开启测试交付约束后，AI 在交付阶段必须生成 Markdown 格式的提测单，供测试人员快速验收：

```markdown
# 【提测交付单】[需求/Bug 简要名称]

- **关联需求/任务**：[例如：企业登录支持联系我们]
- **开发分支**：feature/xxx
- **交付时间**：YYYY-MM-DD
- **变更文件清单**：
  - `packages/feature/feature_xxx/lib/src/page/xxx_page.dart` (新增/修改)
  - `packages/feature/feature_xxx/lib/src/notifier/xxx_notifier.dart` (新增/修改)

---

## 1. 自动化测试执行结果
- [x] **测试文件**：`packages/feature/feature_xxx/test/...`
- [x] **本地验证命令**：`dart run tool/project.dart test standard` (全量 PASS)

---

## 2. 核心功能与测试用例清单（供测试验收）

| 序号 | 测试场景 / 功能点 | 前置条件 / 输入 | 预期结果 | 自测状态 | 边界/异常说明 |
| :--- | :--- | :--- | :--- | :---: | :--- |
| 1 | [正向主流程] | [如：进入页面点击拨打] | [如：正常调起系统拨号盘] | ✅ PASS | Android / iOS / 鸿蒙三端验证 |
| 2 | [异常/边界值] | [如：网络断开/号码为空] | [如：友好 Toast 提示，不崩溃] | ✅ PASS | 防 Crash 保护 |
| 3 | [多语言/适配] | [如：切换英文/大字体] | [如：文案完整无溢出] | ✅ PASS | 检查 9 语言与小屏机型 |

---

## 3. 关联影响与回归建议
- **潜在风险点**：[例如：调整了登录页底部弹性布局，建议在小屏幕手机上回归键盘弹起遮挡问题]
```
