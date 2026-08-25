# 代码审查高频缺陷对照清单（Code Review Checklist）

交付前给 AI 做防御性自检、给人/大模型做 Code Review 时对照本清单。
每一项都来自本仓库真实代码审查中反复出现的高频缺陷，**先看反面示例，再抄正面写法**。

严重度标注：🔴 必须修（可能崩溃 / 功能错误）；🟡 应该修（体验或健壮性）；🟢 有余力再修（整洁度）。

---

## 1. 🔴 静默 catch（吞异常）

**反面示例**（`catch (_) {}` 什么都不做，用户看到空白页完全不知道发生了什么）：

```dart
try {
  final result = await repo.getXxx();
} catch (_) {
  // 保持当前状态 —— ❌ 吞掉了所有异常
}
```

**正确写法**（两件事，参考 `feature_auth` 的 `EnterpriseContactNotifier`）：
1. **网络错误提示交给 HTTP 层**：Repository 里用带 `ErrTip` 的请求方法（`getWithErrTip` / `postWithConfig(showErrorToast: true)`），失败时封装层自动弹错误 Toast；
2. **catch 兜底必须打日志**：`debugPrint('xxx error: $e')`，至少保证线上能查日志：

```dart
} catch (e) {
  debugPrint('EnterpriseContactNotifier.fetchContactInfo error: $e');
  if (mounted && gen == _generation) {
    state = state.copyWith(isLoading: false);
  }
}
```

> 大白话：可以不出错误弹窗，但绝对不能"静默失败"。用户看得见的错误交给统一封装层，自己 catch 的异常至少要留日志。

---

## 2. 🔴 双重非空断言 `!.`（改字段为 null 时直接崩溃）

**反面示例**（`contactInfo` 或 `qrcodeImgUrl` 为 null 时，`!.` 直接抛 `NoSuchMethodError`）：

```dart
if (contactInfo?.qrcodeImgUrl != null &&
    contactInfo!.qrcodeImgUrl!.trim().isNotEmpty) {   // ❌ 双重 !
```

**正确写法**（先取出到局部变量再判空，天然安全）：

```dart
final qrUrl = contactInfo?.qrcodeImgUrl ?? '';
if (qrUrl.trim().isNotEmpty) { ... }
```

**规则**：一个对象上连续出现两个 `!.` 就是高危信号。能先 `?? ''` 兜底的字段一律先取值再判断。

---

## 3. 🟡 `canLaunchUrl` + `launchUrl` 双检查（TOCTOU）

**反面示例**（先检查再启动，检查到启动之间设备状态可能变化，纯属多余）：

```dart
if (await canLaunchUrl(uri)) {
  await launchUrl(uri);      // ❌ 这里仍可能抛异常
} else {
  _copyText(phone, tip);
}
```

**正确写法**（直接启动，`catch` 统一兜底失败场景）：

```dart
try {
  await launchUrl(uri);
} catch (_) {
  _copyText(phone, tip);
}
```

> `url_launcher` 的 `launchUrl` 失败本身就会抛异常，`canLaunchUrl` 的预检查既不能保证成功，还多一次平台调用。

---

## 4. 🟡 宽类型 + 运行时类型检查（`List<dynamic>` / `item is Map`）

**反面示例**（参数声明成 `List<dynamic>`，循环里 `item is Map` 再强取字段——类型不符时静默丢数据，排查困难）：

```dart
factory XxxModel.fromDictList(List<dynamic> list) {
  for (final item in list) {
    if (item is Map) {                       // ❌ 运行时猜测类型
      final label = item['dictLabel'];       // ❌ 可能返回 null 被静默丢弃
    }
  }
}
```

**正确写法**（把类型声明直接收窄，编译期就挡住脏数据）：

```dart
factory EntContactInfoModel.fromDictList(List<Map<String, dynamic>> list) {
  final map = <String, dynamic>{};
  for (final item in list) {
    final label = item['dictLabel']?.toString().trim();
    final value = item['dictValue']?.toString().trim();
    if (label != null && value != null) {
      map[label] = value;
    }
  }
  ...
}
```

**规则**：能用具体泛型（`List<Map<String, dynamic>>`、`List<String>`）就不用 `List<dynamic>`；能用编译期类型就不用 `is` 运行时判断。调用处 `as` 转换同步改成具体类型。

---

## 5. 🟡 Widget 参数里"布尔开关"与"回调"耦合

**反面示例**（`showCopy` 和 `onCopy` 分开传，`showCopy: true` 但 `onCopy: null` 时出现"看得见点不动"的幽灵按钮）：

```dart
Widget _buildContactItem({
  bool showCopy = false,   // ❌ 与 onCopy 状态可能不一致
  VoidCallback? onCopy,
})
```

**正确写法**（用 `onCopy != null` 直接推断是否显示，删掉布尔开关）：

```dart
Widget _buildContactItem({
  VoidCallback? onTap,
  VoidCallback? onCopy,    // null 时不显示复制图标
})

// 内部：
if (onCopy != null) {
  GestureDetector(onTap: onCopy, child: ...iconCopy...);
}
```

**规则**：传了回调 = 功能可用，没传 = 不渲染，两态合一，杜绝错位。

---

## 6. 🟢 为单个函数导入整个库

**反面示例**：只为了 `max(a, b)` 就 `import 'dart:math';`。

**正确写法**：一个三元表达式搞定：

```dart
// ❌ import 'dart:math';
final bottomSafe = Screen.bottomSafeHeight > 16.sc
    ? Screen.bottomSafeHeight
    : 16.sc;
```

---

## 7. 🟢 i18n JSON 文件末尾必须换行

**高频细节**：9 个语言文件（`apps/tuqiang_app/assets/i18n/*.json`）末尾都以 `}` 结尾，**没有换行符**。提交前逐个检查 `tail -c 1`，不是 `0a` 就补一个空行，避免后续 diff 噪音。

```bash
for f in apps/tuqiang_app/assets/i18n/*.json; do
  [ "$(tail -c 1 "$f" | xxd -p)" != "0a" ] && echo "" >> "$f"
done
```

---

## 8. 🟢 State / 模型里定义了 getter 却没人用

**反面示例**：State 里写了一排便捷 getter（`String? get telephone => contactInfo?.telephone;`），页面却还是 `contactInfo?.telephone` 直接取。

**正确写法**：二选一——
- **页面统一走 State getter**（`contactState.telephone`），getter 有值；
- 或者按 YAGNI 原则**删掉没用的 getter**，别留死代码。

---

## 9. 💡 补充：页面 loading 不要用手动全局 TQLoading

页面首次加载用**手动 `TQLoading.show()` / `TQLoading.dismiss()`** 时，如果请求秒回会有闪烁，pop 页面时还可能和 `dispose` 里的 `dismiss` 打架。
**推荐**：改用 State 的 `isLoading` 字段驱动页面内嵌 loading（`switch (state.isLoading) { ... }`），数据到达自动消失，无需成对 dismiss。

---

## 提交前速查

- [ ] 所有 `catch` 都至少打了日志，没有 `catch (_) {}` 空块
- [ ] 全文件搜索 `!.`，连续 `!.` 已消除
- [ ] uri 启动类操作没有 `canLaunchUrl` + `launchUrl` 双检查
- [ ] Model / 方法的集合参数用了具体泛型，没有运行时 `is` 猜类型
- [ ] Widget 布尔开关与回调两态合一
- [ ] i18n 9 语言文件末尾都有换行
- [ ] 没用的 getter / 导入已清理