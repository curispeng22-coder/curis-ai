# Curis Desktop Pane Shell Exploration v1

**Status**: SEARCH + PANE SHELL FINAL REVIEW REQUIRED（Shell Header Finalization 五项 + Global Search 已纳入）
**作者**: UI Designer
**日期**: 2026-08-15
**范围**: 仅 XHS Workspace 推进；RD Workspace 暂停，不做任何研发高保真工作。
**不修改**: Product Blueprint、正式前端代码。本探索作为 **Shell Contract Delta-X7 Candidate** 存在，未直接 Frozen。

---

## 0. 被撤销的结构（取代对象）

旧 Shell（Shell Contract §1.1 / §1.2）采用 **Global Topbar（52px）横跨整个 App** + 下方 `Nav(220) + Main + Context/Utility` 的"顶栏 + 侧栏"模型。其问题：

1. 顶部横条同时承载**全局定位 + 状态 + 主题 + 搜索 + 用户**，与 **Workspace 级** 信息（面包屑/业务对象）混在一起，职责不清。
2. Main 的 Workspace Header 概念被顶栏吞掉，导致"Main Header 属于谁"边界模糊。
3. Context / Utility 以"插入列"方式展开时，会把整行向下推，**挤压 Main Header**（用户明确禁止）。

本探索**撤销 Global Topbar 横跨结构**，改为 **Top-aligned Independent Pane**。

---

## 1. 新结构：Top-aligned Independent Pane

```text
窗口顶部（y=0）开始，四 Pane 各自独立成列、顶部齐平：

┌──────────────┬──────────────┬────────────────────────────┬──────────────┐
│ Navigation   │ Context      │ Main                       │ Utility      │
│ Pane Header  │ Pane Header  │ Pane Header                │ Pane Header  │
├──────────────┼──────────────┼────────────────────────────┼──────────────┤
│ Navigation   │ Context      │ Main                       │ Utility      │
│ Pane Content │ Pane Content │ Pane Content               │ Pane Content │
│ (固定)       │ (可选)       │ (必有)                    │ (可选)       │
└──────────────┴──────────────┴────────────────────────────┴──────────────┘
```

### 六条硬规则（来自指令）

1. **Navigation / Context / Main / Utility 是彼此独立的 Pane。**
2. **所有已打开 Pane 从窗口顶部开始并顶部齐平。**
3. **每个 Pane 拥有自己的 Pane Header + Pane Content。**
4. **Main 的 Workspace Header 只能属于 Main Pane，不能横跨 Context / Utility。**
5. **Context / Utility 打开后不能因为 Main Header 被向下挤。**
6. **Context / Utility 都是 Resizable Adaptive Surface**（见 §5）。

### 为什么这能彻底解决"挤压 Main Header"

旧模型里 Context/Utility 是"在 Nav 与 Main 之间/右侧插入的一行"，整行共享同一个顶部，所以插入列会顶动 Main。
新模型里 **每个 Pane 是一根独立列**，列内有自己的 Header（位于该列顶部），列与列**互不嵌套**。Context/Utility 打开 = 增加一根新列，Main 列本身不变、其 Header 仍在 Main 列顶部——**结构上不可能被挤压**。这是本方案相对旧模型的根本优势。

### 结构图（确认用）

<svg viewBox="0 0 680 484" width="100%" xmlns="http://www.w3.org/2000/svg" role="img">
  <title>Curis Desktop Pane Shell — Top-aligned Independent Pane</title>
  <desc>Four independent panes — Navigation, optional Context, Main, optional Utility — all starting at the window top, each with its own header. No global top bar spans the app.</desc>
  <rect x="20" y="20" width="640" height="400" rx="16" fill="#1a1c1f" stroke="#343940" stroke-width="0.5"/>
  <rect x="20" y="20" width="150" height="400" fill="#222529" stroke="#343940" stroke-width="0.5"/>
  <rect x="20" y="20" width="150" height="44" fill="#2b2f34"/>
  <!-- macOS Traffic Lights（桌面 App 窗口控制按钮，固定在 Nav Header 最左侧） -->
  <circle cx="34" cy="42" r="5" fill="#ff5f57"/>
  <circle cx="48" cy="42" r="5" fill="#febc2e"/>
  <circle cx="62" cy="42" r="5" fill="#28c840"/>
  <!-- 品牌 logo 已移出顶栏：下移到 Navigation Content 顶部（.nav-brand，顶栏以下第一行） -->
  <text x="34" y="80" font-family="Inter, system-ui, sans-serif" font-size="14" font-weight="600" fill="#f3f4f6">Curis</text>
  <!-- T1: 面板折叠图标（▤，与 WorkBuddy/Codex 同款） -->
  <rect x="134" y="30" width="28" height="24" rx="6" fill="#1a1c1f" stroke="#343940" stroke-width="0.5"/>
  <text x="148" y="47" font-family="Inter, system-ui, sans-serif" font-size="13" fill="#a7adb6" text-anchor="middle">▤</text>
  <rect x="34" y="86" width="120" height="10" rx="3" fill="#2b2f34"/>
  <rect x="34" y="110" width="100" height="10" rx="3" fill="#2b2f34"/>
  <rect x="34" y="134" width="112" height="10" rx="3" fill="#2b2f34"/>
  <rect x="34" y="158" width="90" height="10" rx="3" fill="#2b2f34"/>
  <rect x="34" y="182" width="108" height="10" rx="3" fill="#2b2f34"/>
  <rect x="34" y="206" width="96" height="10" rx="3" fill="#2b2f34"/>
  <text x="34" y="380" font-family="Inter, system-ui, sans-serif" font-size="11" fill="#a7adb6">global: 搜索 · 主题 · 账户</text>
  <rect x="170" y="20" width="160" height="400" fill="#222529" stroke="#343940" stroke-width="0.5"/>
  <rect x="170" y="20" width="160" height="44" fill="#2b2f34"/>
  <text x="184" y="47" font-family="Inter, system-ui, sans-serif" font-size="13" font-weight="500" fill="#f3f4f6">选题库 · 信号</text>
  <rect x="298" y="30" width="22" height="22" rx="6" fill="#1a1c1f" stroke="#343940" stroke-width="0.5"/>
  <text x="309" y="45" font-family="Inter, system-ui, sans-serif" font-size="12" fill="#a7adb6" text-anchor="middle">✕</text>
  <rect x="184" y="86" width="130" height="36" rx="6" fill="#2b2f34"/>
  <rect x="184" y="130" width="130" height="36" rx="6" fill="#2b2f34"/>
  <rect x="184" y="174" width="130" height="36" rx="6" fill="#2b2f34"/>
  <text x="184" y="388" font-family="Inter, system-ui, sans-serif" font-size="11" fill="#a7adb6">Resizable · 默认 260 · 可拖拽</text>
  <rect x="330" y="20" width="230" height="400" fill="#222529" stroke="#343940" stroke-width="0.5"/>
  <rect x="330" y="20" width="230" height="44" fill="#2b2f34"/>
  <rect x="338" y="30" width="26" height="24" rx="6" fill="#1a1c1f" stroke="#343940" stroke-width="0.5"/>
  <text x="351" y="47" font-family="Inter, system-ui, sans-serif" font-size="13" fill="#a7adb6" text-anchor="middle">☰</text>
  <text x="374" y="47" font-family="Inter, system-ui, sans-serif" font-size="13" fill="#f3f4f6">业务空间 / 小红书 / Note</text>
  <rect x="528" y="30" width="26" height="24" rx="6" fill="#1a1c1f" stroke="#343940" stroke-width="0.5"/>
  <text x="541" y="47" font-family="Inter, system-ui, sans-serif" font-size="13" fill="#a7adb6" text-anchor="middle">▦</text>
  <rect x="346" y="86" width="198" height="60" rx="8" fill="#2b2f34"/>
  <rect x="346" y="158" width="198" height="120" rx="8" fill="#2b2f34"/>
  <rect x="346" y="290" width="198" height="40" rx="8" fill="#2b2f34"/>
  <text x="346" y="380" font-family="Inter, system-ui, sans-serif" font-size="11" fill="#a7adb6">Main Header 仅属 Main Pane</text>
  <rect x="560" y="20" width="100" height="400" fill="#222529" stroke="#343940" stroke-width="0.5"/>
  <rect x="560" y="20" width="100" height="44" fill="#2b2f34"/>
  <text x="572" y="47" font-family="Inter, system-ui, sans-serif" font-size="12" font-weight="500" fill="#f3f4f6">图文预览</text>
  <rect x="640" y="30" width="16" height="22" rx="5" fill="#1a1c1f" stroke="#343940" stroke-width="0.5"/>
  <text x="648" y="45" font-family="Inter, system-ui, sans-serif" font-size="12" fill="#a7adb6" text-anchor="middle">✕</text>
  <rect x="572" y="86" width="76" height="120" rx="8" fill="#2b2f34"/>
  <rect x="572" y="218" width="76" height="60" rx="8" fill="#2b2f34"/>
  <text x="572" y="380" font-family="Inter, system-ui, sans-serif" font-size="11" fill="#a7adb6">Resizable · 默认 360</text>
  <circle cx="148" cy="42" r="10" fill="#32f08c"/>
  <text x="148" y="46" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="700" fill="#0c0c0d" text-anchor="middle">T1</text>
  <circle cx="351" cy="42" r="10" fill="#32f08c"/>
  <text x="351" y="46" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="700" fill="#0c0c0d" text-anchor="middle">T2</text>
  <circle cx="541" cy="42" r="10" fill="#32f08c"/>
  <text x="541" y="46" font-family="Inter, system-ui, sans-serif" font-size="11" font-weight="700" fill="#0c0c0d" text-anchor="middle">T3</text>
  <text x="20" y="446" font-family="Inter, system-ui, sans-serif" font-size="12" fill="#a7adb6">T1 → Navigation 顶栏右／折叠后 Main 左　｜　T2 → Main 左　｜　T3 → Main 右／展开后 Utility 右（与 T1 对称）</text>
  <text x="20" y="468" font-family="Inter, system-ui, sans-serif" font-size="12" fill="#a7adb6">所有 Pane 顶部齐平 · 各自独立 Pane Header + Pane Content · Main Header 不横跨 · Context/Utility 打开不挤压 Main Header</text>
</svg>

---

## 2. Pane 结构表

| Pane | 是否固定 | 默认宽度 | 默认态 | Pane Header 职责 | Pane Content 职责 |
|------|---------|---------|--------|------------------|-------------------|
| **Navigation** | 固定（可完全收起） | 220px（展开）；收起时 `width:0; opacity:0`（**完全隐藏，非细轨**） | 默认展开 | 顶栏：`🔴🟡🟢 + 🔍 Search + T1(▤)`（单行）；内容区顶部：`.nav-brand` 品牌 + 六区导航 + 用户/主题/设置菜单（Search 改为顶栏 icon → Search Surface，见 §9.8） |
| **Context** | **Adaptive（可选）** | 260px（建议值） | 默认收起 | Context 名/类型 + 切换 + 关闭 | 由 Instance 声明（XHS=选题库） |
| **Main** | 固定（必有） | 弹性 `minmax(0,1fr)` | 永远在 | 面包屑 + Context/Utility Toggle + More | 专业业务主工作面（布局由 Instance 决定） |
| **Utility** | **Adaptive（可选）** | 360px（建议值） | 默认收起 | 模式名 + 模式切换 + 关闭 | 由 Instance 声明模式（XHS=预览/数据/审核） |

> Main 永远 `minmax(0,1fr)`：Context/Utility 展开时主区弹性收缩而非溢出；其最小可用宽度由 Resizable 规则守护（§5）。

---

## 3. 四个 Pane Header 逐项定义

原则：**Low Surface Complexity, High Functional Density**。成熟产品功能可隐藏在 More / Popover / 对象动作中，不铺工具墙。逐项判断"这个动作到底属于哪一层"。

### 3.1 Navigation Pane Header

**结构**：单行顶栏（顶栏就两样东西）—— `flex-direction:row; justify-content:space-between`：
- **左侧**：macOS Traffic Lights 🔴🟡🟢（桌面 App 原生窗口控制）
- **右侧**：🔍 Search icon + T1 Navigation Toggle（▤ 面板+竖线图标）。Search icon 点击展开 Company-wide Object Search Surface（§9.8），不常驻。
- **Curis 品牌 logo 不在顶栏内**，下移到 Navigation Content 顶部固定显示（`.nav-brand`，顶栏以下第一行），与导航搜索 / 六区导航同属导航内容区。

| 候选能力 | 是否在 Header | 判定 |
|---------|:---:|------|
| **macOS Window Controls（Traffic Lights 🔴🟡🟢）** | ✅ | **存在，顶栏最左侧固定**。桌面 App（Tauri）原生窗口控制按钮；红=关闭、黄=最小化、绿=最大化。独占顶栏左半，不与品牌同行。 |
| **Navigation Toggle（T1 · 面板+竖线图标）** | ✅ | **存在，顶栏最右侧**。WorkBuddy / Codex 同款面板折叠图标（圆角矩形 + 内竖线）。**位置转移行为**：展开时在 Nav 顶栏右；折叠后自动转移到 Main Header 左侧（T2 前）。始终在活跃 Header 区域内，不悬浮独立。 |
| Curis identity（logo + 名） | ➡️ 移出 Header | **不在顶栏**。下移到 Navigation Content 顶部（`.nav-brand`），作为导航内容区的固定第一行。原因：顶栏只承载「窗口控制 + 面板开合」两件事，品牌属于内容区身份锚点。 |
| **全局 Search（🔍 icon）** | ✅ | **Nav Header 右侧轻量 Search icon**（与 T1 同组 `.nav-head-right`）。点击展开 Company-wide Object Search Surface（§9.8）。**不常驻** Navigation Content（已移除常驻 `.nav-search` 大搜索框）。 |
| 主题 / 账户 / 设置 / 帮助 | ⚠️ 放 Navigation Footer（用户菜单） | 全局动作，稳定归属 Navigation Pane 底部用户区。 |

**结论**：Navigation 顶栏 = `🔴🟡🟢（左） + 🔍 Search + ▤ T1（右）` 一行；Curis 品牌在顶栏以下的导航内容区顶部固定显示。Search 为轻量 icon，点击展开 Search Surface（§9.8），Navigation Content 不再常驻搜索框。

### 3.2 Main Pane Header

| 候选能力 | 是否在 Header | 判定 |
|---------|:---:|------|
| **Navigation Toggle（T1 · 条件显示）** | ✅ **条件** | Navigation 折叠时，T1 自动转移到 Main Header **最左侧**（T2 Context Toggle 之前）。展开时 T1 回到 Nav Header，此处隐藏。 |
| 当前 Workspace / 业务对象 / Breadcrumb | ✅ | **存在**，Header 中部。表达"我现在在哪、在处理哪篇 Note"。 |
| Context Toggle（T2） | ✅ | **存在，Header 左侧**（紧邻 Main 内容区左缘，Context 是 Main 左邻）。 |
| Utility Toggle（T3） | ✅ | **对称于 T1**：Utility 折叠时在 Main Header 右侧；Utility 展开时自动转移到 Utility Header 右侧（与 T1 镜像）。始终在活跃 Header 区域内。 |
| 全局 Search | ❌ | 已在 Navigation（§3.1），不在 Main。 |
| Share | ⚠️ 进 More（popover） | Workspace 动作，藏入 More。 |
| More（⋯） | ✅ | **存在，Header 最右**。承载 Workspace 级次要动作。 |

**结论**：Main Header = `▤ T1(条件·Nav 折叠时)` + `☰ T2` + `面包屑/业务对象` + `▦ T3(条件·Utility 折叠时)` + `⋯ More`。T1 仅在 Nav 折叠时出现于最左；T3 仅在 Utility 折叠时出现于最右，Utility 展开后 T3 转移到 Utility Header 右侧。

### 3.3 Context Pane Header

| 候选能力 | 是否在 Header | 判定 |
|---------|:---:|------|
| 当前 Context 类型 / 名称 | ✅ | **存在**（如「选题库 · 信号」）。 |
| 切换 Context | ⚠️ 仅实例有多 Context 时需要 | 下拉/分段切换（XHS 若有"信号 / 素材 / 草稿"多 Context 才出现）。 |
| Close / Collapse（✕） | ❌ **已移除** | T2/T3 Toggle 本身就是双向按钮（点击展开，再点折叠），**不需要独立关闭按钮**。Toggle 已承担开合职责。 |
| 必要对象动作 | ⚠️ 实例决定 | 如"新建选题"等，由 Instance 声明，可放 Header 右侧或 Content 顶部。 |

**注意**：Context 的**开合**由 Main Header 的 T2 控制（双向 Toggle，点击展开/再点折叠）；Context Pane 自身 Header 只做 **切换 / 对象动作**，不重复开合控制，也不需要独立关闭按钮。

### 3.4 Utility Pane Header

| 候选能力 | 是否在 Header | 判定 |
|---------|:---:|------|
| 当前专业对象 / 模式 | ✅ | **存在**（如「图文预览」「数据看板」「审核」）。 |
| 模式切换（Diff/Preview/Analytics） | ⚠️ 仅实例需要时 | 分段控件（XHS 声明 预览/数据/审核 多模式才出现）。 |
| Close / Collapse（✕） | ❌ **已移除** | T2/T3 Toggle 本身就是双向按钮（点击展开，再点折叠），**不需要独立关闭按钮**。Toggle 已承担开合职责。 |
| 必要对象动作 | ⚠️ 实例决定 | 如"复制预览链接"，由 Instance 声明。 |

**注意**：Utility 的**开合**由 T3 控制（双向 Toggle，折叠时在 Main Header 右、展开后在 Utility Header 右）；Utility Pane 自身 Header 只做 **模式切换 / 对象动作**，不重复开合控制，也不需要独立关闭按钮。

---

## 4. 三个 Toggle（Shell Header Finalization：位置语义冻结，视觉不冻结）

> 硬性约束：**不允许任何 Workspace 自行发明 toggle 位置或语义**。三个控制的位置与语义由 Shell 统一固定。视觉风格（方形/圆形/图标密度）由 Design System Token 决定，不在此冻结。

### 视觉原则（Shell Header Finalization #2）

- **默认为低视觉重量 icon control**：无边框、无背景、纯图标 + `currentColor`
- **Hover / Active 才显示背景/边界**（subtle surface bg）
- 参考 WorkBuddy / Codex 的 Pane Toggle 密度（28×28px tap target，16×16px 图标）
- 不冻结"方形按钮"具体实现——未来可能演变为圆形或其他

| Toggle | 固定位置 | 语义 | 视觉（默认态） |
|--------|---------|------|:---:|
| **T1 Navigation Toggle** | **展开时**：Nav Header Row2 右侧；**折叠后**：Main Header 最左侧（T2 前） | 控制 Navigation 完全收起/展开。折叠后自动转移位置，始终在活跃 Header 内。 | 面板+竖线 SVG icon（**展开态=竖线左** `x1=5.5` 向左折叠 / **折叠态=竖线右** `x1=10.5` 向右展开），无 bg/border |
| **T2 Context Toggle** | Main Pane Header 左侧（T1 条件显示的右侧） | 控制 Context Surface 开合 | 面板+竖线 SVG icon（**竖线左**，与 T1 展开态同向 — 都控制 Main 左侧面板），无 bg/border |
| **T3 Utility Toggle** | **折叠时**：Main Header 右侧；**展开后**：Utility Header 右侧（与 T1 对称） | 控制 Utility Surface 开合 | 面板+竖线 SVG icon（**竖线右** `x1=10.5` 向右折叠 — 控制 Main 右侧面板），无 bg/border |

**图标方向语义**：
- **竖线在左** = "向左折叠"（T1 展开态 + T2）：点击后收起左侧面板
- **竖线在右** = "向右折叠"（T1 折叠态 + T3）：点击后收起右侧面板 / 展开左侧内容
- T1 是唯一一个**状态双向图标**的 Toggle（展开/折叠显示不同方向）

**发现性保证**：
- T2 常驻 Main Header 左侧；T3 常驻但位置随状态转移：Utility 折叠时在 Main Header 右侧，展开后"搬家"到 Utility Header 右侧
- T1 始终可见：展开时在 Nav 顶栏右，折叠后"搬家"到 Main Header 左
- 三者位置在所有 Workspace 实例中**完全一致**

---

## 5. Resizable 规则（Shell Header Finalization #4：规则框架冻结，数值待验证）

Context / Utility 均为 **Resizable Adaptive Surface**（继承 Delta-X5）：

### Contract 冻结的规则框架

1. **边界直接拖动**调整宽度（Pane 内边界手柄，非显式放大/缩小按钮）。
2. **默认宽度为建议值**（非固定约束），具体数值由后续 Prototype 验证后确定。
3. **记忆上次宽度**（per Workspace 持久化）。
4. 设 **min / max** 边界（具体数值待验证），以及 **Main minimum usable width**（主区低于该值不再压缩）。
5. **空间不足自动转 Overlay / Focus**（不强行并排挤压主区）。
6. 不增加显式"放大/缩小"按钮。

### 不进入 Contract 的内容

- **180px / 520px**：仅 v4 Prototype demo 拖拽边界，非最终 min/max
- **260px / 360px**：仅默认建议值，Instance 可覆盖
- 具体档位阈值（如"≥ 480px 后转 Overlay"）：待多分辨率验证

> Navigation Pane 采用 **T1 Toggle 完全收起/展开**（非 Resizable）。收起时 `width:0; opacity:0`（完全隐藏）；T1 自动转移到 Main Header 左侧作为稳定 reopen 入口。**已撤销"必须折叠为 ~64px Compact Rail"的旧假设**（见 §9.3）。

---

## 6. Shell 固定能力 vs Workspace Instance 决定

| 能力 | 归属 |
|------|------|
| Pane 结构（四独立 Pane：Nav / Context / Main / Utility） | **Shell 固定** |
| 所有 Pane 顶部齐平 + 各自 Pane Header + Pane Content | **Shell 固定** |
| T1 / T2 / T3 三个 Toggle 的存在与位置 | **Shell 固定**（跨 Workspace 一致） |
| Resizable 机制（拖拽 / 默认建议值 / 记忆 / min-max / Overlay 兜底） | **Shell 固定** |
| 全局搜索 / 主题 / 账户 位置（Navigation Pane） | **Shell 固定** |
| Breadcrumb 位置（Main Pane Header） | **Shell 固定** |
| Main 内部布局（Calendar / Split / 列表…） | **Workspace Instance** |
| Context 内容 + 是否多 Context + 切换 UI | **Workspace Instance 决定** |
| Utility 模式集 + 默认模式 + 模式切换 UI | **Workspace Instance 决定** |
| Pane 内对象动作（新建选题 / 复制预览链接…） | **Workspace Instance 决定** |
| More 中的 Workspace 动作集合（Share / 视图…） | **Workspace Instance 决定** |
| 导航子项 child 渲染细节（缩进/图标/active/owner 头像） | **Shell Navigation Detail Pending（不冻结）** |

---

## 7. 与 Shell Contract 的关系

- 本探索 = **Shell Contract Delta-X7 Candidate（Top-aligned Independent Pane）**，已在 `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` §7 登记，**未直接 Frozen**。
- 待 XHS v4 Final Review 批准后，再将 Delta-X7 回写为 Shell Contract §1（取代旧 Global Topbar 模型），并相应更新 §1.2 网格、§3/§4 中"Main Header 横跨"相关措辞。
- 不修改 Product Blueprint，不修改正式前端代码。

---

## 8. 已解决 / 更新

| 原问题 | 状态 | 解决方案 |
|--------|:---:|----------|
| Navigation 折叠细轨 ~64px | **已撤销** | 改为 Full Hide（`width:0; opacity:0`）+ T1 转移到 Main Header。见 §9.3 |
| T1 图标 Unicode 回退不可识别 | **已解决** | 改用 SVG 内联图标（面板+竖线），展开/收起竖线位置不同 |
| T1 折叠后消失 | **已解决** | T1 位置转移：展开在 Nav Header，折叠后自动转移到 Main Header 左侧 |
| Logo 与 Traffic Lights 同行 / 顶栏过复杂 | **已解决** | 顶栏改为单行：左=Traffic Lights，右=T1；Curis 品牌 logo 移出顶栏，下移到 Navigation Content 顶部（`.nav-brand`）固定显示。顶栏只承载「窗口控制 + 面板开合」两件事。 |
| 产品文案含设计解释 | **已解决** | 删除"无需手动提交"等面向用户的解释，改用自然业务语言。见 §9.5 |
| Context/Utility 独立 ✕ 关闭按钮多余 | **已解决** | 移除所有 `.ctx-close` / `.util-close` 按钮。T2/T3 Toggle 本身为双向（展开/折叠），已承担关闭职责，不需要冗余关闭按钮。 |
| 常驻 Navigation 大搜索框 vs Nav Header 轻量 Search icon | **已解决** | 移除 Navigation Content 常驻 `.nav-search`；改为 Nav Header 右侧 🔍 Search icon → 独立 Search Surface（Company-wide Object Search，见 §9.1 / §9.8）。 |

---

## 9. Shell Header Finalization 五项

### 9.1 Global Search — 形态冻结（选中方案 A）

**归属确认**：Global Search 属于 Navigation Pane（跨 Workspace 全局检索：业务空间/组织/员工/资料）。

**最终决策（v4 Finalization 选定）**：采用 **方案 A — Navigation Header 轻量 Search icon → Search Surface**。
- 删除 Navigation Content 常驻大搜索框（v4 已移除 `.nav-search`）。
- Navigation Header 右侧新增轻量 🔍 Search icon（复用 `.pane-toggle` 基类），与 T1 同组（`.nav-head-right`）；点击 → 展开独立 Search Surface。
- 交互范式对齐 WorkBuddy / Codex / VSCode 的 Command Palette：默认不占空间，按需展开。

**产品语义（Company-wide Object Search，非 Task Search）**：Curis 是 Company OS（Company / Organization / Business / Employee / Workspace 关系），Search 定义为**公司级对象搜索**，不是 WorkBuddy / Codex 的 Task 历史搜索。
- 原则：**Object-first, Task-capable**——Task 可搜到，但不是 Search 第一产品心智。
- 搜索对象类型：Business / Workspace / Employee·Role / Business Object（Note·Video·Project·商品）/ Knowledge·Document·Asset / Result·Artifact / Meeting / Decision / Capability（Expert·Skill·Connector）/ Task。
- 每条结果显示必要的组织 / 业务上下文（如「小红书运营办公室 · Note」），点击直接进入对应对象 / Workspace。

**v1 范围（RESERVED，不做）**：复杂自然语言关系查询、AI 问答、完整 Command Palette、高级过滤器、搜索语法。首版只做基础对象搜索（输入 → 按对象类型分组结果 + Recent）。

**信息结构与交互细节见 §9.8。**

### 9.2 T1/T2/T3 视觉重量

**冻结**：位置和语义（§4）。
**不冻结**：具体视觉样式（方形/圆形/尺寸/是否带边框）。

**默认方向**：
- 轻量 icon control（28×28px tap target, 16×16px 图标）
- 默认无背景、无边框
- Hover → subtle surface background
- Active → slightly deeper background
- Focus-visible → outline ring（WCAG AA）

参考基准：WorkBuddy / Codex 的 Pane Toggle 密度。

### 9.3 Navigation Collapse 方案比较

**已撤销旧冻结**："必须折叠为 ~64px Compact Rail" 不再成立。

| 方案 | 描述 | 优点 | 缺点 | 推荐 |
|------|------|------|------|:---:|
| **A. Full Hide + 稳定 reopen control** | 完全收起（`width:0; opacity:0`）；T1 自动转移到 Main Header 左侧作为 reopen 入口 | 最大工作区空间；行为与 WorkBuddy 一致；无需维护 Compact Rail 内容子集 | 收起后完全看不到导航内容 | ✅ **推荐** |
| **B. Compact Rail (~64px)** | 折叠到窄轨；仅显示图标+展开按钮 | 导航入口始终可见 | 占用水平空间；需定义 Rail 内容子集；增加复杂度 | 备选 |

**推荐 A 的理由**：
1. v4 Prototype 已验证可行：T1 位置转移机制稳定
2. 与 WorkBuddy / Codex 行为一致（用户已有心智模型）
3. Low Surface Complexity：收起=完全隐藏，不保留残影
4. Desktop App 场景下空间宝贵（尤其小屏笔记本）
5. 用户需要导航时，T1 在 Main Header 左侧触手可及

**B 可能适用的场景**：未来若用户反馈"频繁切换导航太麻烦"，可考虑引入 Compact Rail 作为可选模式（非默认）。

### 9.4 Resizable 数值边界

**Contract 只保留规则框架**（§5），不冻结具体数值：

| 参数 | 当前状态 | 说明 |
|------|---------|------|
| Context 默认宽度 | 建议值 ~260px | Instance 可覆盖 |
| Utility 默认宽度 | 建议值 ~360px | Instance 可覆盖 |
| Min width | 待验证 | Prototype 用 180px |
| Max width | 待验证 | Prototype 用 520px |
| Main minimum usable | 待验证 | 建议 ≥ 480px 后转 Overlay |

后续步骤：多分辨率测试 + 真实内容填充后确定最终数值。

### 9.5 产品文案原则

**删除面向用户的设计解释**。Automation 通过状态/Handoff 自然表达，不加"设计说明"。

| ❌ 不要写 | ✅ 改为 |
|-----------|--------|
| "无需手动提交" | "已交接王芳审核" |
| "无需再次点击推进" | "等待你的决定" |
| "CEO 不负责点击下一步" | （不出现，行为自明） |
| "工作流已完成，无需人工推进" | "✅ 已发布" |
| "不存在人工按钮" | （不出现） |

**原则**：界面文案只告诉用户**当前状态**和**下一步是什么**，不解释"为什么没有某个按钮"或"系统自动做了什么"。自动化是隐式体验，不是显式说明。

---

**UI Designer**: UI Designer
**阶段**: Pane Shell Exploration v1（Shell Header Finalization 完成）
**状态**: SEARCH + PANE SHELL FINAL REVIEW REQUIRED
**配套**: `Curis_XHS_Workspace_Visual_v4.html`（同步更新）
**下一步**: 用户 Final Review 批准后回写 Shell Contract Delta-X7 + 起前端实现 Issue

### 9.6 Utility 内置浏览器 + 最大化（Round 2 新增）

**背景**：Utility 面板不仅是空面板——它是 **内置预览浏览器**，用于查看文件、文档、HTML、图片等。类似 WorkBuddy 的预览面板。

#### 能力定义

| 能力 | 描述 | 状态 |
|------|------|:---:|
| **多文件标签切换** | Utility 内置 tab 栏，可同时打开多个文件/预览快速切换 | ✅ v4 已实现框架 |
| **内置渲染引擎** | 在 Utility 视口内直接渲染 HTML / 图片 / 文档预览 | 框架已搭建 |
| **最大化按钮** | Utility Header 新增 `↗` 最大化按钮（轻量 icon，与 Toggle 同级） | ✅ v4 已实现 |
| **全屏 Overlay** | 点击最大化后，Utility 覆盖**整个页面**（含 Main），其他 Pane 暂时隐藏；Esc 或 ✕ 退出 | ✅ v4 已实现动画 |

#### Header 布局更新

Utility Header = `模式名 + 子标题` + `模式切换` + `↗ 最大化` + `▤ T3 折叠`（T3 展开后从 Main Header 转移到此处；Toggle 双向，无需独立 ✕ 关闭按钮）

#### 最大化行为

- **触发**：点击 `↗` 按钮
- **效果**：`position:fixed; inset:0; z-index:9999` 全屏 overlay
- **退出**：点击 overlay 内 `✕` 或按 `Esc`
- **动画**：200ms ease scale(0.98→1) + fade in
- **Context 不需要此功能**：Context 保持轻量（选题库等），不需要内置浏览器

### 9.7 Toggle 交互逻辑实现规范（冻结 · 跨 Workspace 强制一致）

> **本规范是 Shell Header Finalization #2（T1/T2/T3）的实现层收口，所有 Workspace 页面 MUST 遵守，不允许各页面自创。**

#### 问题溯源（v4 初版 bug）

v4 初版用 `querySelector('.mh-util')` 只绑定了 DOM 中**第一个** T3（Main Header 内）。而 T3 有「对称位置转移」：Utility 展开后 Main Header 的 T3 被 CSS 隐藏、Utility Header 的 T3 才显示。**展开后用户看到的那个 T3 从未绑定事件 → 只能展开、不能折叠**。已修复为 `querySelectorAll` 绑定所有同类 Toggle。

#### 冻结规则（五条，跨页面强制）

1. **双向 Toggle，不区分 open / close 按钮**：T1/T2/T3 均为 `classList.toggle(...)` 双向操作——点击展开，再点折叠。**禁止**为 Context / Utility 提供独立 ✕ 关闭按钮（v4 已移除 `.ctx-close` / `.util-close`）。
2. **位置转移 = 纯 CSS 显示规则，不靠 JS 移动 DOM**：
   - T1：Nav 展开 → Nav Header 内显示、Main Header 内 T1 `display:none`；Nav 折叠 → 反之。
   - T3：Utility 折叠 → Main Header 内显示、Utility Header 内 T3 `display:none`；Utility 展开 → 反之。
   - 互斥模板（同一时刻仅一个 T3 可见）：
     ```css
     .panes:not(.util-open) .util-head .mh-util { display:none; }
     .panes.util-open      .main-head .mh-util { display:none; }
     ```
3. **事件绑定 MUST 用 `querySelectorAll` 绑定所有同类实例**（根因修复规则）：绝不能 `querySelector('.mh-util')` 只绑第一个——位置转移后可见的那个 Toggle 会没有监听。每个 workspace 根容器内对所有 `.nh-toggle` / `.mh-ctx` / `.mh-util` 遍历绑定，回调统一 `panes.classList.toggle('<state>')`。
4. **同页面多 Workspace 实例隔离**：以每个 workspace 根容器（`.app`）为作用域，`app.querySelector('.panes')` 取自身 state，toggle 只影响自身容器，不串扰其他实例。
5. **Icon 方向语义**（见 §4）：竖线左=向左折叠，竖线右=向右折叠；T1 展开/折叠显示不同方向（状态双向图标），T2/T3 固定方向。

#### 规范参考实现（JS 模板 · 所有页面复制此片段）

```js
(function(){
  document.querySelectorAll('.app').forEach(function(app){
    var panes = app.querySelector('.panes');
    var nav   = app.querySelector('.pane-nav');
    var t1s = app.querySelectorAll('.nh-toggle');
    var t2s = app.querySelectorAll('.mh-ctx');
    var t3s = app.querySelectorAll('.mh-util');
    function toggleNav(){ if(nav) nav.classList.toggle('collapsed'); }
    t1s.forEach(function(t){ if(t) t.addEventListener('click', toggleNav); });
    t2s.forEach(function(t){ if(t && panes) t.addEventListener('click', function(){ panes.classList.toggle('ctx-open'); }); });
    t3s.forEach(function(t){ if(t && panes) t.addEventListener('click', function(){ panes.classList.toggle('util-open'); }); });
  });
})();
```

> **强制范围**：XHS Workspace、RD Workspace、以及未来任何新增的 Workspace 页面，无论 UI 高保真还是真实前端实现，**必须**采用上述同一套 Toggle 交互逻辑。禁止各页面自创 open/close 双按钮、禁止单实例绑定、禁止 JS 移动 Toggle DOM。本规范随 Shell Contract Delta-X7 一同 Frozen 后具备强制约束力。

### 9.8 Company-wide Object Search Surface（v1 基础对象搜索）

> **本规范是 Shell Header Finalization #1（Global Search）的实现层收口。所有 Workspace 页面 MUST 复用同一套 Search Surface 交互与信息结构。**

#### 入口（统一）
- Navigation Header 右侧轻量 🔍 Search icon（`.nav-search-trigger`，复用 `.pane-toggle` 基类）；与 T1 Navigation Toggle 同组（`.nav-head-right`）。
- 点击 → 展开 Search Surface；再次点击 / 点击遮罩 / ✕ / `Esc` → 收起。
- Navigation Pane 折叠时（宽度 0）Nav Header 整体隐藏，Search icon 随之不可见——首版不跨 Header 转移（与 T1 行为不同：T1 转移是为了恢复导航，Search 在折叠态下非必需）。

#### Surface 信息结构（展开态）
1. **顶部统一输入框**：placeholder 提示覆盖的对象类型（业务空间 / 员工 / 笔记 / 知识 / 结果 / 会议…）。
2. **空查询态**：显示 **Recent**（最近访问的对象），不显示分组结果。
3. **有查询态**：按**对象类型分组**结果——
   - 分组标题（如 业务空间 · Business / 员工 · Employee / 笔记 · Note / 知识 · Knowledge / 结果 · Result / 会议 · Meeting / 决策 · Decision / 能力 · Capability）。
   - 每条结果：`图标 + 标题 + 组织/业务上下文 + 类型标签`。
   - 点击结果 → 直接跳转到对应对象 / Workspace（非搜索结果页、非文件浏览器）。
4. **底部提示条**：操作说明（↵ 进入对象 · Esc 关闭）+ 范围声明（仅对象搜索 v1）。

#### 对象类型清单（Object-first）
| 类型 | 说明 |
|------|------|
| Business / Workspace | 业务空间、工作区 |
| Employee / Role | 员工、岗位角色 |
| Business Object | Note / Video / Project / 商品 等业务对象 |
| Knowledge / Document / Asset | 知识、文档、资产 |
| Result / Artifact | 结果、制品 |
| Meeting | 会议 |
| Decision | 决策 |
| Capability | Expert / Skill / Connector |
| Task | 任务（可搜到，但非第一心智） |

#### v1 明确不做（RESERVED）
- 复杂自然语言关系查询
- AI 问答
- 高级过滤器 / Facet
- 搜索语法
- 完整 Command Palette（命令模式）

#### 强制范围
XHS Workspace、RD Workspace、未来任何新增 Workspace 页面，**必须**复用同一套 Search Surface（入口 icon + 分组结果结构 + 对象类型语义），禁止各页面自创独立搜索框或文件浏览器式搜索。

