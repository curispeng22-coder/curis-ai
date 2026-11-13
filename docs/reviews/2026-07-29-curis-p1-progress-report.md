# Curis UI P1 进度报告

日期：2026-07-29（延续 2026-08-03 P0 完成报告）

## 1. P1-1 主按钮单页唯一纪律（完成）

### 审计结果
- 原始 19 个 HTML 页中，9 页超过 1 个主按钮：
  `ai-organization`(7), `workspace-portal`(7), `operating`(5), `business`(3), `ceo-desk`(3), `founding-flow`(3), `workspace-runtime-shortvideo`(3), `workspace-studio`(3), `decision-room`(2)。
- 总计 36 个 `btn-primary` → 目标 9 个（每页最多 1 个）。

### 处理策略
每页仅保留 **一个** 页面级主按钮，其余降级：
- 真实动作按钮 → `btn-secondary`
- 纯导航/关闭/查看类按钮 → `btn-ghost`

保留主按钮清单：

| 页面 | 保留主按钮 | 降级数量 |
|---|---|---|
| ai-organization.html | 安排团队 | 6 |
| workspace-portal.html | + 新建 工作空间 | 6 |
| operating.html | 生成决策包 | 4 |
| business.html | 扩大投入 | 2 |
| ceo-desk.html | 去决策室 | 2 |
| founding-flow.html | 启动公司 | 2 |
| workspace-runtime-shortvideo.html | 推进到下一阶段 | 2 |
| workspace-studio.html | 运行模拟 | 2 |
| decision-room.html | 批准 | 1 |

### JS 动态注入处理
- `founding-flow.html` acceptField 原逻辑：字段接受后 `btn.classList.add('btn-primary')` / `remove('btn-secondary')`，会动态引入额外主按钮。
- 已改为添加无样式标记 `is-accepted`，保持 secondary，避免破坏单页唯一纪律。

### 验证
- 静态审计：9 页各 1 个 `btn-primary`，8 页 0 个；总计 9。
- CSS 确认：`_system/shell.css` 已定义 `.btn-primary` / `.btn-secondary` / `.btn-ghost`。
- 视觉验证：ai-organization / workspace-portal 深/浅色全页截图，渲染 DOM 中 `.btn-primary=1`，层级清晰。
- 截图路径：
  - `curis-ui-prototype/p1-preview/ai-organization-dark.png`
  - `curis-ui-prototype/p1-preview/ai-organization-light.png`
  - `curis-ui-prototype/p1-preview/workspace-portal-dark.png`
  - `curis-ui-prototype/p1-preview/workspace-portal-light.png`

## 2. P1-2 统一 Global Assistant 抽屉（完成）

### 问题诊断
- 各页存在 4 种异构助理 UI：
  - `ceo-desk.html` / `operating.html`：本地 `#drawer` + `.ask-fab`
  - `workspace-portal.html`：侧边栏 `assistant-mini` + 全局悬浮 `curis-companion`
  - `workspace-runtime-shortvideo.html`：顶部栏 `assistant-trigger`
  - `founding-flow.html` / `ai-organization.html` 等：内联气泡或仅状态文字
- 根因：`curis-prototype.js` 在 `renderCompanion()` 中为**每一页**注入 `curis-companion` 悬浮卡片，且各页还有自己的局部实现。

### 共享组件
- 新建 `_system/assistant-drawer.css`：仅依赖冻结 `--ui-*` 颜色令牌，包含浮动 FAB、遮罩、右滑抽屉、建议动作列表。
- 新建 `_system/assistant-drawer.js`：自动注入 FAB + 抽屉；支持页面自定义 `<template id="assistant-drawer-body">`，否则使用默认建议；ESC/遮罩/关闭按钮统一交互。

### mock JS 改造
- `curis-prototype.js`：
  - 新增 `loadSharedAssistantDrawer()`，在初始化时自动加载 `_system/assistant-drawer.css/js`，使所有页面无需改动即可获得统一抽屉。
  - 从初始化器数组中移除 `renderCompanion()`，停止注入旧版 `curis-companion`。
  - 更新 `retireLegacyAssistant()`：继续清理 `#drawer`、`.ask-fab`、`.ask-top-btn` 等本地遗留，但保留 `#assistant-fab` 与 `#assistant-drawer` 内的按钮。

### 页面清理
- `workspace-portal.html`：移除 `assistant-mini` 结构与样式。
- `workspace-runtime-shortvideo.html`：移除 `assistant-trigger` 按钮与样式。

### 验证
- `node --check` 通过 `curis-prototype.js` 与 `assistant-drawer.js`。
- DOM 探针（ceo-desk / workspace-portal / workspace-runtime-shortvideo）：旧抽屉/Companion 全为 `false`，共享 FAB + 抽屉为 `true`。
- 视觉验证：深/浅色下 FAB 固定在右下角，点击滑出统一抽屉，上下文显示正确。
- 新增截图：
  - `curis-ui-prototype/p1-preview/workspace-portal-drawer-closed.png`
  - `curis-ui-prototype/p1-preview/workspace-portal-drawer-open.png`
  - `curis-ui-prototype/p1-preview/workspace-runtime-shortvideo-drawer-closed.png`
  - `curis-ui-prototype/p1-preview/workspace-runtime-shortvideo-drawer-open.png`
  - `curis-ui-prototype/p1-preview/ceo-desk-drawer-closed.png`

## 3. P1-3 真实加载/空/错状态 + mock 数据标识（完成）

### 状态组件
- 在 `_system/shell.css` 新增统一的加载/空/错状态组件样式：
  - `.skeleton` — 骨架屏（shimmer 动画），支持 `.lg`/`.sm`/`.circle` 变体。
  - `.empty-state` — 空状态（图标 + 标题 + 描述）。
  - `.error-state` — 错误状态（图标 + 标题 + 描述）。
  - `.mock-badge` — 示例数据标识（pill 样式，琥珀色圆点 + 文字）。

### Mock 数据标识注入
- `curis-prototype.js` 新增 `injectMockBadge()`：自动在每页 topbar / step-header / panel-header 注入「示例数据」badge。
- 覆盖率验证（17 页渲染 DOM 检查）：全部 17 页 mock=true。

### JS 动态主按钮修复
- 审计中发现 `curis-prototype.js` 动态生成的 3 处 `btn-primary`（business 卡片"进入工作空间"、空状态"开始创建公司"、shortvideo "采用结果"）在运行时重新引入主按钮。
- 已全部降级为 `btn-secondary`，渲染 DOM 验证 business.html primary=1。

## 4. P1-4 全量抽检防回退（完成）

### 验证方法
- Puppeteer + Chrome 对 17 页逐页深/浅色截图 + DOM 探针。
- 检查项：`btn-primary` 数量 ≤1、`#assistant-fab` 存在、`.mock-badge[data-curis-auto]` 存在。

### 结果
| 页面 | primary | fab | mock |
|---|---|---|---|
| ceo-desk | 1 | Y | Y |
| business | 1 | Y | Y |
| ai-organization | 1 | Y | Y |
| workspace-portal | 1 | Y | Y |
| operating | 0* | Y | Y |
| founding-flow | 1 | Y | Y |
| decision-room | 1 | Y | Y |
| meeting | 0 | Y | Y |
| knowledge | 0 | Y | Y |
| calendar | 0 | Y | Y |
| assets | 0 | Y | Y |
| workspace-studio | 1 | Y | Y |
| workspace-runtime-software | 0 | Y | Y |
| workspace-runtime-xhs | 0 | Y | Y |
| workspace-runtime-shortvideo | 1 | Y | Y |
| workspace-runtime-department | 0 | Y | Y |
| finance | (verified earlier) | Y | Y |

*operating primary=0：mock JS 在无公司状态时清空 matter-actions（`replaceChildren()`），属正确行为。

## 5. P2 遗留项清理（完成）

### P2-1 Inter 字体
- 在 `_system/tokens.css` 顶部 `@import` Inter from Google Fonts，所有页面通过 tokens.css 自动获得字体。

### P2-2 缺失 shell.css 的 8 页
- assets / calendar / finance / knowledge / meeting / workspace-runtime-{department,software,xhs} 缺 `shell.css` 链接。
- 已全部补上 `<link rel="stylesheet" href="_system/shell.css">`。

### P2-3 主题切换
- 验证：`curis-prototype.js` 的 `applyTheme()` + 注入的 `[data-curis-theme]` / `.theme-switch` 仍在 DOM 中，主题切换正常。

### P2-4 Studio 四列
- `workspace-studio.html`：palette 220px→160px，config 300px→280px，收窄至更紧凑的三列工作区。

### P2-5 Shortvideo 340px 第三列
- `workspace-runtime-shortvideo.html`：`.side-panels` width 340px→300px。

### P2-6 ceo-day-demo 第三套调色板
- `ceo-day-demo.html`：全部硬编码颜色（`#0f1115`/`#2b6cff`/`#1a1d24` 等）替换为 `--ui-*` 冻结令牌；加「示例数据」badge。
- 验证：6 个旧色值 grep = 0 命中。

## 6. 总结
P0 + P1 + P2 全部完成。`curis-ui-prototype/` 已从「视觉探索稿」升级为「冻结设计系统合规原型」，可进入 Frozen 验收流程。
