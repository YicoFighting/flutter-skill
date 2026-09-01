# UI 设计源与静态资源规范

## 1. 设计源按可用性处理

- 用户提供了可访问的设计稿或切图时，按设计稿尺寸、颜色、字体和资源还原；只有需要精确读取设计稿时才使用对应设计工具。
- 没有设计稿时，先找相邻页面，复用 `core_ui` 和项目视觉语言；不因没有蓝湖连接而阻塞普通功能开发。
- 资源确实存在时优先使用设计切图。没有对应切图、且是标准语义控件时才使用 `Icons.*`；不要用系统图标冒充明确的品牌/业务切图。

### 业务图片缺失时必须停下

现有 UI 以 PNG/SVG/package asset 表达的品牌或业务图标，其语言、状态、主题和产品变体仍属于产品素材。需求要求替换图片、但仓库没有目标素材时，先向用户或设计索要并确认选择条件；不得把素材缺失转换成自己的视觉方案。

例如地图起点/终点当前是“起/终”PNG，非中文需要 `S/E` 时，应请求对应的 `S/E` PNG，并在语言变化时切换 asset。未经用户明确授权，禁止使用以下方式替代缺失的业务图片：

- `Canvas`、`CustomPainter`、`TextPainter` 或在原图上运行时叠字；
- `Icons.*`、emoji、字体图标或临时占位图；
- AI 生成、程序生成、动态 SVG 或其他近似重绘；
- 继续引用不存在的文件名，或把 fake/placeholder 带入生产路径。

只有标准语义控件，或需求明确要求动态绘制且视觉、交互和验收标准已经确认时，才可使用程序绘制。若用户允许先完成不依赖素材的接线，修改范围和未完成状态也要先确认，不能让占位实现看起来像最终交付。

## 2. 资源 owner

途强智能单 feature 使用的图片、JSON、动画帧和目录放在：

```text
packages/feature/feature_xxx/assets/
```

途强智能跨两个及以上模块、app 壳或全局协议使用的资源才放 `packages/assets_common/`。判断归属时搜索 Dart、pubspec、Android、iOS 和 OHOS 引用；同一组根图/`3.0x`/帧序列/JSON 应整体迁移，避免两份事实来源。

迁移中的 feature 由 `tool/check_migration_boundaries.ps1` 校验具体资源路径和 owner。当前项目常见的是根目录资源加 `3.0x/`，不要无依据强制创建 `2.0x/`。

老鹰在线页面可见资源必须位于 `apps/laoying_app/assets/images/<owner>/`，业务 owner 为 `auth/gps/pet/mine/overview/message/device_share/device_management`，应用公共图片放 `common`。允许从途强资源复制并登记为老鹰独立副本，但运行时不得引用 `assets_common`、既有 `feature_*` 图片或途强 app 资源。

## 3. 途强 Feature package 资源路径

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

## 4. 老鹰在线资源路径

老鹰资源由应用级 Resolver 和业务 Resolver 组合：

```dart
final path = LYGpsAssets.traceStart; // gps_trace_start.png

Image.asset(
  path,
  package: LYGpsAssets.packageName,
);
```

- 应用级入口是 `apps/laoying_app/lib/app/assets/ly_app_assets.dart::LYAppAssets`；GPS 等页面优先使用当前 owner 已有的 `LYGpsAssets.traceStart` 这类业务常量，不在页面重新拼文件名；
- 每个业务使用自己的 `LY*Assets`，例如 `LYGpsAssets`，页面不散落硬编码目录；
- `apps/laoying_app/pubspec.yaml` 声明业务资源目录；根图与项目实际要求的 `3.0x` 变体保持配对；
- `Image.asset` 显式使用当前业务 Resolver 暴露的 `packageName`（如 `LYGpsAssets.packageName`，最终来自 `LYAppAssets.packageName`），确保两个宿主都从 `laoying_app` package 加载；
- 产品资源独立不等于底层组件必须重写：`core_ui` 可以复用，但品牌色、文案和图片由老鹰传入或覆盖。

## 5. UI 组件和尺寸

- 先查 `packages/core/core_ui/lib/`；统一顶栏使用实际存在的 `TQAppBar`，空态、Toast、loading 和按钮优先复用对应 `TQ*` 组件。
- 设计稿中的布局尺寸、间距、圆角和字号按项目规则使用 `.sc`；系统尺寸、边框宽度、动画时长、算法参数不要机械套 `.sc`。
- 底部按钮和 BottomSheet 通过 `SafeArea` 或 `Screen.bottomSafeHeight` 处理手势区。

## 6. 验证

- 检查资源路径、大小写、pubspec 声明和引用方式；
- 途强 feature 运行对应资源/contract 测试与 `-ProductScope tuqiang` boundary；
- 老鹰运行相关 `LY*Assets` 测试、`ly_asset_independence_test.dart` 与 `-ProductScope laoying` boundary；app boundary 检查器按 [testing.md](testing.md) 先排除当前 allowlist 冲突；
- 语言/状态变体逐一验证选择条件，确认缺失素材没有被 Canvas、文字叠加、系统图标或生成图片替代；
- 新页面至少检查小屏和一个宽屏/折叠态；资源迁移涉及行为时补对应测试；
- 用 `git diff --check` 检查格式，不为换行细节编写一次性脚本修改大量语言文件。
