# UI 切图与静态资源规范（assets）

## 1. 核心红线：严禁擅自使用系统 Icon 脑补

> 🚫 **【严禁行为】** 凡蓝湖设计稿中的图标、插画、装饰图、空状态配图、按钮背景，**严禁私自使用 `Icons.xxx` 或 `CupertinoIcons.xxx` 替代**。
> 
> 原因：商业应用有统一严格的 UI 视觉语言。自带图标库在比例、描边粗细、视觉风格上与设计稿差异巨大，会直接导致 UI 走样和二次返工。

---

## 2. 需求拉扯期：AI 主动索要切图 SOP

当用户提供蓝湖设计稿截图时，AI 在进入编码之前，**必须**按以下模板主动列出切图清单向用户索要：

### 📋 切图索要标准回复模板（AI 必须执行）
```text
已分析 UI 设计稿，检测到以下视觉元素需要切图资源，请在蓝湖中导出并放入对应目录：

1. 【返回图标】：建议命名 `icon_nav_back.png` | 尺寸：1x (24x24px), 2x (48x48px), 3x (72x72px)
2. 【电话客服图标】：建议命名 `icon_phone_contact.png` | 尺寸：1x (20x20px), 2x (40x40px), 3x (60x60px)
3. 【微信图标】：建议命名 `icon_wechat.png` | 尺寸：1x (20x20px), 2x (40x40px), 3x (60x60px)
4. 【空数据插画】：建议命名 `img_empty_records.png` | 尺寸：1x (120x120px), 2x (240x240px), 3x (360x360px)

📁 推荐存放位置：`packages/feature/feature_xxx/assets/images/`
📐 蓝湖导出要求：
   - 切图平台请选择【iOS】或【Web/通用】（切勿选择 Android 的 mipmap，避免产生奇数尺寸与多余倍率）；
   - 勾选 1x、2x、3x 三种倍率导出，分别放入主目录、2.0x/、3.0x/。
```

---

## 3. 资源落位与 Monorepo 目录结构

在 `tuqiang` monorepo 中，资源文件按作用域严格分层：

```text
tuqiang/
├── packages/
│   ├── feature/
│   │   └── feature_auth/                   # 业务模块包
│   │       ├── assets/
│   │       │   └── images/                 # 模块私有图片
│   │       │       ├── icon_phone.png      # 1.0x 基准图（设计稿标注逻辑尺寸，如 20x20）
│   │       │       ├── 2.0x/               # 2 倍图（40x40）
│   │       │       │   └── icon_phone.png
│   │       │       └── 3.0x/               # 3 倍图（60x60）
│   │       │           └── icon_phone.png
│   │       ├── lib/
│   │       │   ├── feature_auth.dart       # 对外 export
│   │       │   └── src/
│   │       │       └── assets/             # 资源常量类
│   │       │           └── feature_auth_assets.dart
│   │       └── pubspec.yaml                # 声明 assets
│   └── assets_common/                      # 跨端/跨模块公共静态资源
│       └── assets/
│           └── images/                     # 全局通用 Logo、隐私协议切图等
```

### 归属判定表
| 资源类型 | 存放位置 | 示例 |
|---|---|---|
| **Feature 专属业务图标/配图** | `packages/feature/feature_xxx/assets/images/` | 登录页背景、功能入口小图标、业务表单切图 |
| **跨模块公共切图** | `packages/assets_common/assets/images/` | 统一返回箭头、公司 Logo、通用弹窗插画 |
| **公共大文件/HTML/协议** | `packages/assets_common/assets/html/` | 隐私协议 HTML、用户协议文档 |

---

## 4. 多倍图（Asset Variants）与蓝湖导出避坑指引

Flutter 通过子目录自动识别屏幕像素密度（DPI/DPR）：

1. **目录层级与倍率关系**：
   ```text
   assets/images/
   ├── icon_service.png          # 1.0x 基准（设计稿 1x 标注逻辑点尺寸，如 24x24）
   ├── 2.0x/
   │   └── icon_service.png      # 2.0x 图（48x48，尺寸为 1x 的 2 倍）
   └── 3.0x/
       └── icon_service.png      # 3.0x 图（72x72，尺寸为 1x 的 3 倍）
   ```

2. **蓝湖切图平台选择（⚠️ 避坑红线）**：
   - **严禁选择 Android 平台**：Android 导出模式会按照 `mdpi/hdpi/xhdpi/xxhdpi/xxxhdpi`（1x/1.5x/2x/3x/4x）导出，不仅会产生 `19x19`、`37x37` 等不可控的奇数/小数像素，而且目录名为 `mipmap-`，与 Flutter 标准不兼容；
   - **正确选择【iOS】或【Web/通用】**：导出的 `@1x`、`@2x`、`@3x` 完美对应 Flutter 的 1.0x、2.0x、3.0x；
   - 将导出的切图分别放入主目录、`2.0x/` 与 `3.0x/`。

3. **切图尺寸规整与透明外框规范**：
   - **尺寸必须为偶数**：1x 基础切图尺寸必须为偶数（如 `16x16`、`20x20`、`24x24`、`32x32` 等），保证 2x、3x 能被整除，避免边缘抗锯齿发虚；
   - **统一透明外框（Bounding Box）**：若同一列表内图标图形本身长宽不一，UI 切图必须带上统一尺寸的透明外框（如统一 `24x24` 框），杜绝在 Flutter 页面中因图形微小尺寸差异导致排版抖动与偏移。

---

## 5. 命名规范（必须遵守）

- **全部小写字母 + 下划线（`snake_case`）**，**严禁使用中文、空格或大写驼峰**（避免 iOS/Android/鸿蒙跨端构建时文件名大小写敏感冲突）；
- **前缀语义化分类**：

| 前缀 | 用途 | 命名示例 |
|---|---|---|
| `icon_` 或 `ic_` | 小图标、操作入口图标 | `icon_phone_contact.png`、`ic_arrow_right.png` |
| `img_` | 插画、大配图、占位图 | `img_empty_search.png`、`img_banner_default.png` |
| `bg_` | 背景图、卡片底图 | `bg_login_header.png`、`bg_card_gradient.png` |
| `btn_` | 按钮切图、点选状态 | `btn_radio_checked.png`、`btn_radio_normal.png` |

---

## 6. 代码注册与调用标准模板

### ① 在 `pubspec.yaml` 声明资源路径
```yaml
# packages/feature/feature_auth/pubspec.yaml
flutter:
  assets:
    - assets/images/
    - assets/images/2.0x/
    - assets/images/3.0x/
```

### ② 在 `src/assets/feature_xxx_assets.dart` 定义常量
禁止在 Widget 代码中硬编码字符串路径！

```dart
// packages/feature/feature_auth/lib/src/assets/feature_auth_assets.dart
class FeatureAuthAssets {
  FeatureAuthAssets._();

  static const String package = 'feature_auth';

  /// 电话联系图标
  static const String iconPhoneContact = 'assets/images/icon_phone_contact.png';

  /// 微信客服图标
  static const String iconWechat = 'assets/images/icon_wechat.png';

  /// 快捷构建 Image Widget（可选）
  static Image image(
    String name, {
    double? width,
    double? height,
    BoxFit? fit,
  }) {
    return Image.asset(
      name,
      package: package,
      width: width,
      height: height,
      fit: fit,
    );
  }
}
```

### ③ 在 `feature_xxx.dart` 中 export
```dart
// packages/feature/feature_auth/lib/feature_auth.dart
export 'src/assets/feature_auth_assets.dart';
```

### ④ 在 Widget 中调用
```dart
import 'package:flutter/material.dart';
import 'package:core_base/num_extension.dart';
import '../assets/feature_auth_assets.dart';

// 方式 A：直接使用 Image.asset（必须带 package 参数）
Image.asset(
  FeatureAuthAssets.iconPhoneContact,
  package: FeatureAuthAssets.package,
  width: 24.sc,
  height: 24.sc,
  fit: BoxFit.contain,
)

// 方式 B：使用常量类封装的快捷方法
FeatureAuthAssets.image(
  FeatureAuthAssets.iconPhoneContact,
  width: 24.sc,
  height: 24.sc,
)
```

> ⚠️ **高频踩坑注意**：
> 在多 package 架构下，`Image.asset` 若不传 `package: 'feature_xxx'`，Flutter 默认会去主入口 `apps/tuqiang_app` 查找资源，导致 **`Unable to load asset` 运行时图片丢失报错**！

---

## 7. 交付前切图自检 Checklist

- [ ] UI 中的所有图标/配图均已使用切图，没有私自残留 `Icons.xxx`；
- [ ] 所有图片文件名使用英文小写下划线（`snake_case`）；
- [ ] 图片资源已放入 `assets/images/`（及 `2.0x/`、`3.0x/`）；
- [ ] 对应 package 的 `pubspec.yaml` 中已包含该 assets 路径；
- [ ] 已在 `feature_xxx_assets.dart` 定义常量并在 `feature_xxx.dart` 中 export；
- [ ] 调用处已显式指定 `package: 'feature_xxx'` 参数，且尺寸加上了 `.sc`。
