# UI 设计源与静态资源规范

## 1. 设计源按可用性处理

- 用户提供了可访问的设计稿或切图时，按设计稿尺寸、颜色、字体和资源还原；只有需要精确读取设计稿时才使用对应设计工具。
- 没有设计稿时，先找相邻页面，复用 `core_ui` 和项目视觉语言；不因没有蓝湖连接而阻塞普通功能开发。
- 资源确实存在时优先使用设计切图。没有对应切图、且是标准语义控件时才使用 `Icons.*`；不要用系统图标冒充明确的品牌/业务切图。

## 2. 资源 owner

单 feature 使用的图片、JSON、动画帧和目录放在：

```text
packages/feature/feature_xxx/assets/
```

跨两个及以上模块、app 壳或全局协议使用的资源放在 `packages/assets_common/`。判断归属时搜索 Dart、pubspec、Android、iOS 和 OHOS 引用；同一组 1x/3.0x/帧序列/JSON 应整体迁移，避免两份事实来源。

迁移中的 feature 由 `tool/check_migration_boundaries.ps1` 校验具体资源路径和 owner。当前项目常见的是根目录资源加 `3.0x/`，不要无依据强制创建 `2.0x/`。

## 3. Flutter package 资源路径

本项目优先沿用 owner 常量返回完整 package asset key：

```dart
abstract final class FeaturePetAssets {
  static const imageDirectory = 'packages/feature_pet/assets/images';
  static String pet(String filename) => '$imageDirectory/pet/$filename';
}

Image.asset(FeaturePetAssets.pet('empty.png'));
```

另一种合法写法是相对路径加 `package:`：

```dart
Image.asset(
  'assets/images/empty.png',
  package: 'feature_pet',
);
```

两种写法只能选一种，不能把 `packages/feature_pet/...` 再配合 `package: 'feature_pet'` 使用。新增资源必须同时更新 package 的 `pubspec.yaml` 和 owner 常量/公开 API，并保持大小写完全一致。

## 4. UI 组件和尺寸

- 先查 `packages/core/core_ui/lib/`；统一顶栏使用实际存在的 `TQAppBar`，空态、Toast、loading 和按钮优先复用对应 `TQ*` 组件。
- 设计稿中的布局尺寸、间距、圆角和字号按项目规则使用 `.sc`；系统尺寸、边框宽度、动画时长、算法参数不要机械套 `.sc`。
- 底部按钮和 BottomSheet 通过 `SafeArea` 或 `Screen.bottomSafeHeight` 处理手势区。

## 5. 验证

- 检查资源路径、大小写、pubspec 声明和引用方式；
- 迁移 feature 运行 boundary script；
- 新页面至少检查小屏和一个宽屏/折叠态；资源迁移涉及行为时补对应测试；
- 用 `git diff --check` 检查格式，不为换行细节编写一次性脚本修改大量语言文件。
