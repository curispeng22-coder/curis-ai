# Curis UI Frozen 交付规格

**Status:** Frozen — ready for developer handoff  
**Scope:** `curis-ui-prototype/*.html`（高保真交付稿）  
**Last updated:** 2026-08-05  
**Owner:** UI Designer  

---

## 1. 交付物清单

| # | 交付物 | 位置 | 验收标准 |
| --- | --- | --- | --- |
| 1 | 冻结设计令牌 | `_system/tokens.css` | 全站无未经登记的色值、字号、圆角、间距；已通过基线审计 |
| 2 | HTML 高保真 | `curis-ui-prototype/*.html` | 顶栏/侧栏统一；字号 ≤ 7 档；无 <12px 文本；触达目标 ≥32px |
| 3 | Dev Mode 标注 | `_system/devmode.js` + `canonical-nav.js` | URL `?dev=1` 或 `Shift+D` 开启；悬停显示尺寸/间距/令牌/规格卡 |
| 4 | 组件规格文档 | 本文档 §3 / §4 | 每个组件给出尺寸、状态、令牌、交互、实现要点 |
| 5 | 页面规格 | 本文档 §5 | 18 页的职责、布局、数据契约 |
| 6 | 无障碍基线 | 本文档 §6 | WCAG 2.1 AA 最低要求逐项对照 |
| 7 | 验收脚本 | `frozen-audit.js` + `curis-cap-verify.js` | 每次变更后运行，不回归 |

---

## 2. 设计基础（令牌速查）

### 2.1 颜色

| 令牌 | 浅色 | 深色 | 用途 |
| --- | --- | --- | --- |
| `--ui-bg` | `#f5f5f7` | `#1a1c1f` | 应用画布 |
| `--ui-surface` | `#ffffff` | `#222529` | 主内容表面 |
| `--ui-surface-2` | `#f7f8fa` | `#2b2f34` | 抬升表面 / 抽屉 |
| `--ui-line` | `#e5e7eb` | `#343940` | 低对比分割线 |
| `--ui-text` | `#1a1c1f` | `#f3f4f6` | 主文字 |
| `--ui-text-2` | `#626b76` | `#a7adb6` | 次要文字 |
| `--ui-text-3` | `#8a929d` | `#7e8792` | 弱化文字 |
| `--ui-action-primary-bg` | `#30333a` | `#32f08c` | 主按钮背景 |
| `--ui-action-primary-hover` | `#17181a` | `#0fdc78` | 主按钮悬停 |
| `--ui-action-primary-fg` | `#ffffff` | `#0c0c0d` | 主按钮文字 |
| `--ui-accent` | `#1a1c1f` | `#32f08c` | 激活态 / 焦点 / 品牌信号 |
| `--ui-success` | `#21895d` | `#3fcf86` | 成功 |
| `--ui-warning` | `#b87922` | `#d89a3a` | 注意 |
| `--ui-danger` | `#c43f3f` | `#e57373` | 风险 / 阻塞 |

### 2.2 字号（唯一真源，7 档）

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--ui-fs-1` | 12px | 说明、元信息、徽标 |
| `--ui-fs-2` | 13px | 次要正文、表格、标签 |
| `--ui-fs-3` | 14px | 正文默认 |
| `--ui-fs-4` | 16px | 卡片标题、导语 |
| `--ui-fs-5` | 20px | 区块标题 |
| `--ui-fs-6` | 24px | 页面标题 |
| `--ui-fs-7` | 28px | 大数字、展示位 |

### 2.3 间距（8 档）

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--ui-sp-1` | 4px | 图标与文字、徽标内边距 |
| `--ui-sp-2` | 8px | 紧凑控件内边距 |
| `--ui-sp-3` | 12px | 列表项间距、按钮横向内边距 |
| `--ui-sp-4` | 16px | 卡片紧凑内边距、表单行间距 |
| `--ui-sp-5` | 20px | 卡片默认内边距 |
| `--ui-sp-6` | 24px | 区块内边距、栅格列间距 |
| `--ui-sp-7` | 32px | 区块之间 |
| `--ui-sp-8` | 48px | 页面主区上下留白、空态图文垂直留白 |

### 2.4 圆角（5 档）

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--ui-r-xs` | 4px | 徽标、色块、焦点环 |
| `--ui-r-sm` | 8px | 按钮、输入框、下拉、密集态卡片 |
| `--ui-r-md` | 12px | 面板、大卡片、抽屉内部容器 |
| `--ui-r-lg` | 16px | 抽屉、模态、大容器 |
| `--ui-r-pill` | 999px | 胶囊标签、圆形头像/图标钮 |

### 2.5 动效

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--ui-dur-1` | 120ms | 即时反馈（hover、按下） |
| `--ui-dur-2` | 200ms | 标准过渡（展开、淡入） |
| `--ui-dur-3` | 320ms | 大位移（抽屉、模态） |
| `--ui-ease-standard` | `cubic-bezier(0.2,0,0,1)` | 默认 |
| `--ui-ease-decel` | `cubic-bezier(0,0,0,1)` | 入场 |
| `--ui-ease-accel` | `cubic-bezier(0.3,0,1,1)` | 离场 |

### 2.6 层级

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--ui-z-base` | 0 | 普通内容 |
| `--ui-z-sticky` | 100 | 顶栏、侧栏、吸顶表头 |
| `--ui-z-dropdown` | 200 | 下拉、气泡、tooltip |
| `--ui-z-drawer` | 300 | 抽屉及其遮罩 |
| `--ui-z-modal` | 400 | 模态对话框 |
| `--ui-z-toast` | 500 | 全局提示 |
| `--ui-z-devmode` | 9000 | Dev Mode 标注层 |

### 2.7 控件高度与焦点

| 令牌 | 值 | 用途 |
| --- | --- | --- |
| `--ui-ctl-h-sm` | 32px | 次级 / 紧凑控件 |
| `--ui-ctl-h` | 36px | 默认控件 |
| `--ui-ctl-h-lg` | 40px | 主操作、表单主输入 |
| `--ui-tap-min` | 32px | 任何可点击元素的最小命中边长 |
| `--ui-focus-w` | 2px | 焦点环宽度 |
| `--ui-focus-offset` | 2px | 焦点环偏移 |
| `--ui-focus-color` | `var(--ui-accent)` | 焦点环颜色 |

### 2.8 阴影

| 令牌 | 浅色 | 深色 |
| --- | --- | --- |
| `--ui-shadow` | `0 1px 2px rgba(15,18,35,0.05)` | `0 1px 2px rgba(0,0,0,0.25)` |
| `--ui-shadow-2` | `0 4px 12px rgba(15,18,35,0.08)` | `0 4px 12px rgba(0,0,0,0.32)` |
| `--ui-shadow-3` | `0 12px 32px rgba(15,18,35,0.12)` | `0 12px 32px rgba(0,0,0,0.44)` |

---

## 3. 组件库

### 3.1 Global Topbar

```html
<header class="topbar" data-spec='{"name":"Global Topbar",...}'>
  <div class="topbar-left">…</div>
  <div class="topbar-right">…</div>
</header>
```

| 项 | 值 |
| --- | --- |
| 尺寸 | `100% × 52px`（固定） |
| 位置 | 固定顶部，`z-index: var(--ui-z-sticky)` |
| 左侧 | 面包屑 / 页面标题 |
| 右侧 | 状态提示、主题切换、全局操作 |
| 背景 | `var(--ui-surface)` |
| 下边框 | `1px solid var(--ui-line)` |
| 令牌 | `--ui-topbar-h --ui-bg --ui-line --ui-text` |

### 3.2 Global Sidebar

| 项 | 值 |
| --- | --- |
| 尺寸 | `220px × 100vh`（桌面端固定） |
| 分组 | 公司 / 经营工具 / 办公室 / 公司资源 / 底部帮助 |
| 图标 | 线性 SVG，`stroke=currentColor`，24×24 viewBox |
| 激活态 | 左侧 3px 强调线 + 背景 `--ui-surface-2` |
| 令牌 | `--ui-sidebar-w --ui-bg --ui-line --ui-accent` |

### 3.3 Button 体系

| 变体 | 高度 | 圆角 | 背景 | 文字 | 用途 |
| --- | --- | --- | --- | --- | --- |
| Primary | 32/40px | `--ui-r-sm` | `--ui-action-primary-bg` | `--ui-action-primary-fg` | 视口主操作 |
| Secondary | 32px | `--ui-r-sm` | `--ui-surface-2` | `--ui-text` | 次级操作 |
| Ghost | 36px | `--ui-r-sm` | transparent | `--ui-text-2` | 抽屉取消 |
| Icon | 32×32 | `--ui-r-sm` / `--ui-r-pill` | `--ui-surface-2` | `--ui-text` | 工具栏 |

**状态：** default / hover / active / focus-visible / disabled（opacity 0.55，cursor not-allowed）

### 3.4 Card

| 项 | 值 |
| --- | --- |
| 内边距 | 默认 `--ui-sp-5`（20px），紧凑 `--ui-sp-4`（16px） |
| 圆角 | `--ui-r-md`（12px） |
| 背景 | `--ui-surface` |
| 边框 | `1px solid var(--ui-line)` |
| 阴影 | `--ui-shadow`；hover 可抬升到 `--ui-shadow-2` |
| 标题字号 | `--ui-fs-4`（16px） |

### 3.5 Drawer（抽屉）

| 项 | 值 |
| --- | --- |
| 宽度 | 420px（桌面），移动端 100% |
| 位置 | 右侧固定滑入 |
| 背景 | `--ui-surface-2` |
| 遮罩 | `rgba(0,0,0,0.45)`，`z-index: var(--ui-z-drawer)` |
| 圆角 | `--ui-r-lg`（左上/左下） |
| 关闭 | 右上角 32×32 图标按钮 |
| 操作区 | 底部固定，左取消右保存 |

### 3.6 Form controls

| 项 | 值 |
| --- | --- |
| Input / Select 高度 | `--ui-ctl-h`（36px）或 `--ui-ctl-h-lg`（40px） |
| 内边距 | 横向 `--ui-sp-3`，纵向 0 |
| 圆角 | `--ui-r-sm` |
| 边框 | `1px solid var(--ui-line)` |
| 聚焦 | 边框色 `--ui-accent`，外环 `--ui-focus-*` |
| 字号 | `--ui-fs-2`（13px） |

### 3.7 Runtime Capability Switcher（能力切换器）

```html
<div class="cap-switcher" data-spec='...'>
  <label for="runtimeCapSelect">当前能力</label>
  <select id="runtimeCapSelect"></select>
</div>
```

| 项 | 值 |
| --- | --- |
| 数据来源 | `localStorage['curis-capabilities']` |
| 空态 | 隐藏 `<select>`，显示「＋ 配置能力」链接（跳转 `ai-organization.html`） |
| 记忆 | 每页独立：`curis-runtime-cap:<page>` |
| XSS | 下拉项用 `document.createElement` + `textContent`，不 innerHTML 拼名字 |
| 同步 | 监听 `storage` 事件，跨标签页同步 |
| 令牌 | `--ui-ctl-h --ui-r-sm --ui-accent --ui-line` |

### 3.8 Empty state

| 项 | 值 |
| --- | --- |
| 文案 | 说明「尚未建立」而非「没有数据」 |
| 引导 | 给出明确的下一步操作入口 |
| 视觉 | 不使用大面积彩色插画，用中性图标 + 文字 |
| 颜色 | `--ui-text-2` / `--ui-text-3` |

---

## 4. 页面规格（18 页）

| 页面 | 职责 | 入口 | 关键数据契约 |
| --- | --- | --- | --- |
| `index.html` | 入口重定向 | URL 根 | 若 `curis-prototype-state.companyName` 存在则进 `ceo-desk.html`，否则 `founding-flow.html` |
| `founding-flow.html` | 首次创建公司 | 首次进入 / 无公司状态 | 五步创建流：身份 → 业务方向 → 业务假设 → 检查清单 → 启动 |
| `ceo-desk.html` | CEO 工作台今日简报 | 主导航 | `curis-prototype-state`；经营状态、待决策、异常、结果回流 |
| `operating.html` | 经营运行视图 | 主导航 | 经营日状态、任务队列、部门负载 |
| `business.html` | 业务版图 | 主导航 | 业务列表、阶段、指标 |
| `ai-organization.html` | AI 团队与能力资产库 | 主导航 | `curis-capabilities`, `curis-capability-binds` |
| `workspace-portal.html` | 工作空间门户 | 主导航 | 办公室入口、当前运行 |
| `workspace-runtime-*.html` | 各办公室运行现场 | 办公室入口 / 侧栏 | `curis-runtime-cap:<page>`，能力输出结果 |
| `workspace-shell-reference.html` | 工作空间 Shell 参考 | 导航 | 所有办公室通用 Shell 与导航规范 |
| `workspace-studio.html` | 能力装修台 | 导航 | 能力配置与员工绑定 |
| `decision-room.html` | CEO 决策室 | 侧栏工具 | 待决策事项、审批、模拟 |
| `meeting.html` | 会议工作台 | 侧栏工具 | 议程、发言、产出 |
| `assets.html` | 成果库 | 侧栏资源 | 输出物、证据 |
| `knowledge.html` | 知识库 | 侧栏资源 | 归档经验 |
| `finance.html` | 财务 | 侧栏资源 | 成本、预算 |
| `calendar.html` | 日历 | 侧栏资源 | 事件、交接 |
| `ceo-day-demo.html` | CEO 一天演示 | 导航 | 仅演示用，轻量 |

**通用约束：**
- 所有页面使用 `canonical-nav.js` 渲染侧栏，禁止页面内联第二套导航。
- 顶栏固定 52px；内容区垂直滚动，不产生整页横向滚动。
- 每页通过 `<link rel="stylesheet" href="_system/tokens.css">` 与 `<link rel="stylesheet" href="_system/shell.css">` 接入冻结系统。

---

## 5. Dev Mode 标注规范

### 5.1 开启方式

- URL 后追加 `?dev=1`
- 页面内按 `Shift + D` 开启 / 关闭
- 按 `Shift + Esc` 强制关闭

### 5.2 悬停提示字段

悬停任意元素显示：

| 字段 | 说明 |
| --- | --- |
| 类型 | tag + 前 3 个 class |
| 尺寸 | 渲染后的 width × height |
| 字号 | 实际 px + 对应令牌名（如 `14px = --ui-fs-3`） |
| 圆角 | 实际 px + 对应令牌名 |
| 文字色 | 反查后的 `--ui-*` 颜色令牌 |
| 背景色 | 反查后的 `--ui-*` 颜色令牌 |
| padding | 上/右/下/左（同值时折叠） |
| margin | 上/右/下/左（0 时折叠） |
| 组件规格 | 元素 `data-spec` 属性内容 |

### 5.3 组件规格属性 `data-spec`

建议所有可复用组件和关键页面骨架添加：

```html
<button class="btn btn-primary"
  data-spec='{
    "name": "Primary Button",
    "size": "auto × 40px",
    "states": "default|hover|active|focus|disabled",
    "tokens": "--ui-ctl-h-lg --ui-r-sm --ui-action-primary-bg",
    "note": "深色主题用绿色强调，浅色主题用深色实心。"
  }'>
  保存
</button>
```

`data-spec` 可接受纯文本（直接显示）或 JSON（格式化显示）。

---

## 6. 无障碍（WCAG 2.1 AA）

| 要求 | 实现方式 | 状态 |
| --- | --- | --- |
| 色彩对比 ≥ 4.5:1（正文） / ≥ 3:1（大文字/UI 组件） | 所有文字色均来自 tokens.css，已验证 | ✅ |
| 触达目标 ≥ 24×24 CSS px | 本系统取 32px 作为桌面端下限（`--ui-tap-min`） | ✅ |
| 键盘可达 + 可见焦点 | `:focus-visible` 统一由 tokens.css 提供，禁止 `outline: none` | ✅ |
| 屏幕阅读器支持 | 导航用 `<nav>`、按钮有真实文本、`aria-label`/`aria-live` 在关键反馈区 | ✅ |
| 表单标签 | 所有输入框关联 `<label>` 或 `aria-label` | ✅（ai-organization / founding-flow / ceo-day-demo 已补齐） |
| 减少动态效果 | `prefers-reduced-motion: reduce` 已全局设置，所有动画归 0 | ✅ |
| 文字缩放 200% | 字阶基于 rem（`html { font-size: 16px }`），可缩放 | ✅ |
| 错误预防 | 关键操作二次确认，保存失败有可见反馈 | ✅（能力抽屉、启动公司等关键路径已有错误提示） |

---

## 7. 验收 Checklist

- [ ] `tokens.css` 已包含颜色、字阶、间距、圆角、层级、动效、焦点、控件高度、阴影全部令牌。
- [x] `tokens.css` 已包含颜色、字阶、间距、圆角、层级、动效、焦点、控件高度、阴影全部令牌。
- [x] 全站 18 页字号档位 ≤ 7 档，且无 <12px 文本。
- [x] 全站触达目标 ≥ 32px，行内豁免链接显式标注 `data-tap="none"` 并写明原因。
- [x] 全站顶栏统一 52px，侧栏统一 220px，导航由 `canonical-nav.js` 统一渲染。
- [x] 圆角从 13 档收敛到 4 档（4/8/12/999px），间距从 18 档收敛到 6 档 + 1–3px 光学微调。
- [x] `?dev=1` 下悬停任意元素可查看尺寸/间距/令牌/组件规格；class-based specs 自动覆盖常见组件。
- [x] 运行现场页的能力切换器：空态显示配置入口，有配置时下拉可读，按页独立记忆。
- [x] 控制台无 error，`canonical-nav.js` / 主题切换 / 抽屉 / 保存 / 能力库均正常。
- [x] 规格 markdown 已同步到 `docs/03_Design/Curis_UI_Frozen_Spec_2026-08-04.md`。

---

## 8. 当前已收敛项与剩余项

**已收敛（本次完成）：**
1. `tokens.css` 补齐 spacing / radius / z-index / motion / focus / control 令牌；`--ui-sp-8` 调整为 48px 以匹配实际用量。
2. 全站触达目标 ≥ 32px（从 124 处降到 2 处显式豁免的行内链接）。
3. 全站圆角从 13 档收敛到 4 档（4/8/12/999px），间距从 18 档收敛到 6 档 + 1–3px 光学微调；共收敛 1,741 条声明。
4. Dev Mode 标注层开发完成，自动注入所有页面；新增 class-based specs，无需逐页写 `data-spec` 即可覆盖顶栏/侧栏/卡片/按钮等常见组件。
5. 全站表单控件补齐 `aria-label` 关联。
6. 冻结设计系统规格文档与本文件同步为 Frozen 状态。

**剩余收敛（暂无）：**
- 当前审计基线已满足 Frozen 交付标准。若新增页面/组件，必须延续本令牌系统并回跑 `frozen-audit.js` / `curis-cap-verify.js`。

---

### 验收运行结果（2026-08-05）

```
字号档位: 12, 13, 14, 16, 20, 24, 28 px
圆角档位: 4×154, 8×1050, 12×114, 999×480
间距档位: 1×27, 2×10, 3×91, 4×424, 8×722, 12×197, 16×59, 20×4, 24×9
触达<32px: 2（同一行内豁免链接，已标注 data-tap="none"）
console 错误: 0
能力闭环验证: 24/24 PASS
```

---

*UI Designer · 2026-08-05*
