# Curis Workspace Shell Contract & Shared Work Pattern Specification

## 2026-09-15 — F1 / Shared capability authority synchronization

Status: Frozen · Authority Class: CURRENT / SHELL PRODUCT AUTHORITY.

CEO接受F1人工接续：§3.11修正绝对Decision-only旧句。跨业务能力/人工接续/后台/恢复消费[Company OS Shared Authority §10–18](Curis_Company_OS_Shared_Authority.md)；G1-V～G6-V未验，不是实施接受。七区/Four-Pane/Pane-local Header/Shared Composer/Employee三态保持；具体新视觉DESIGN OPEN。

## 2026-09-10 — Product structure research boundary

Authority Class: CURRENT / FROZEN. Disposition: RECORDED / CURRENT — INCLUDED IN CONTROLLED BASELINE PROMOTION.

本 Shell Contract 的空间责任继续消费 [Pre-Design-Research Product Structure Baseline](../01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md)。Navigation、Context、Main、Utility、Reading/Working/Operating、七区与 global CEO Assistant 的结构边界保持；本记录不冻结最终视觉组合，FINAL UI MASTER 仍为 **PAUSED — COMPETITIVE DESIGN RESEARCH REQUIRED**。

## 2026-09-09 CEO Phase A — Current spatial applicability

Authority Class: CURRENT / FROZEN. Disposition: ACCEPTED.
Decision: [Core Product Authority Repair](../reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md) §§5–7。本段明确全局适用范围，不重画UI或修改P1–P7 Runtime语义。

Four-Pane是Navigation/Context/Main/Utility四职责；Nav+Main默认，Context/Utility按需，不能四列常驻或永久留空。沿用Pane-local Header、T1–T3、Resizable和Utility Maximize；Main可独立成立。
Navigation承载七区、canonical Conversation quick access、Company object search、CEO identity/settings。Context限当前domain/work的导航/集合/bounded context，不放完整Employee profile/Conversation/Result正文。Utility默认收起，提供Detail/Editor/Evidence/专业工具/Result检查，可maximize，不是固定结果/员工/Assistant栏。

READING=理解内容资料结果证据；WORKING=与Employee/Work/Meeting持续工作；OPERATING=方向责任状态结果问题及下一判断。Business→Operating Main；Workspace→selected Domain Main；Conversation/Work/Meeting→Working Main；Employee→Main Workstation+Utility detail；Result→Reading Utility/maximized Reading；Evidence→Utility；Knowledge→Reading Main；经营洞察→Operating analysis/Report Reading；Decision→既有P7+Utility Evidence。不冻结Research宽度，不新增状态枚举。

CEO Assistant是独立global floating layer，可拖动/收起/展开，跨七区不销毁，同identity/durable conversation，消费合法context，不占Four-Pane、不预留空间。旧draggable=Vision解释SUPERSEDED；exact width/X/Y/snap/位置记忆/快捷键/drag physics留Final UI Master。CEO Desk是Operating Surface，不是Assistant本体。

Temporary overlay/modal允许start/create/config/select/confirmation；高风险仍需确认，不是每个Modal都审批。Drawer为bounded edit/detail，floating是持续全局层。结果Viewed≠Accepted，隐藏Pane≠停止Runtime。

**Status**: Frozen — S1–S7 APPROVED FOR FREEZE + P1–P7 APPROVED FOR FREEZE（2026-08-15 Final Review 批准回写）+ **Shared Employee Workstation Pattern（Delta-S1/S2/S3）2026-08-16 回写** + **Shared Main Composition（Delta-X9）2026-08-17 回写** + **Shared Employee Work Area + Composer（Delta-X10）2026-08-17 回写** + **Shared Conversation Content Block（Delta-X12）2026-08-17 回写（长内容块 bounded embedded / 内部滚动 / 可进 Utility / 不 Frozen px·字数·样式；不动 Runtime State Schema、不新增 Runtime Primitive）**
**输入**: RD Workspace Visual Baseline v1 (Figma 四张截图)
**泛化自**: `Curis_Design_System_Delta_RD_Workspace.md`（RD 实例 Delta）
**运营视角补充**: `Curis_Workspace_Shell.md`（结果条/责任链/管道槽位参考）
**不修改**: 任何代码、任何现有页面、任何 Frozen 令牌（`_system/tokens.css`）
**设计语言**: 所有色值/字号/间距/圆角一律引用 Frozen `--ui-*`，禁止页面私有令牌

---

## 0. 本规范定位与边界（最高优先级）

本规范定义 **Contract（契约层）+ Pattern（模式层）**，不规定任何 Workspace 的主工作区内部布局。

### 0.1 两个边界修正（来自 CEO 审查）

**边界修正 1 — 不叫"四栏固定"。**
固定的是 **Workspace Shell Contract** 和**空间职责**，不是四栏永久可见。
- **Main 必有**；
- **Context / Utility 都是 Adaptive Surface**，按需出现、展开、收起，默认态不占空间。

> **Professional Workspace / Multi-Surface reconciliation（2026-08-21）**：Four-Pane 是职责模型，不是固定四根物理栏，也不要求四种职责同时可见。Navigation 负责公司级导航；Context 负责 Workspace 的 Domain Navigation 与当前业务上下文；Main 显示当前选中的 Professional Surface 及相关 Shared Work Area；Utility 承载当前对象的 Detail / Editor / Evidence / Tool；CEO Assistant 是 Global Company Employee，不是第五个 Pane。Surface 切换不创建 Team、Employee、Cycle、Result、Session 或 Runtime。

> **Main must stand on its own（2026-08-17 Delta-X9 回写）**：Nav + Main 为默认基础桌面；Context / Utility 全关时，CEO 仍能理解业务整体状态并完成主要工作。Context 仅答按需上下文，**不得承载关闭后导致 Main 无法理解业务的核心信息**。

**边界修正 2 — 不把"决策横幅 + Conversation + Employee Workstation"定义成所有 Workspace 的固定 Main；且不存在独立的 Employee Queue Shell 区域（见修正 1）。**
- **Main 是专业业务主工作面，布局由 Workspace 决定**：
  - 研发 → 以真实研发工作对象 / Version / Build / Test / Review / Blocker为专业核心；Employee Workstation是Shared Work Area，不占据整个专业Main；
  - 小红书 → 以日历 / 内容 / 数据为核心；
  - 短视频 → 以时间轴 / 视频生产为核心；
  - 会议 → 以讨论 / 证据 / Decision 为核心。
- **Employee Workstation、Handoff、Needs CEO、Result Reference、Composer 是 Shared Company Patterns（Available Capability，可用能力），可被不同 Workspace 按需采用，非 Required（强制要求），不等于固定页面布局**。

> **Clarification（Shared Employee Workstation Pattern · 2026-08-16 回写 · Delta-S1）**：Employee Workstation 虽为 Available Capability（非所有 Workspace 默认必备主布局），但**一旦 CEO 进入任意一个具体 AI Employee（不限部门 / 业务），Main Workspace 必须统一呈现该员工的 Conversation-first Employee Workstation**。Workspace 的默认 Main 可保持 **Domain-specific 专业业务界面**（见上：研发多 Workstation / 小红书日历内容 / 短视频时间轴 / 会议讨论），但**任何存在 AI Employee 的 Workspace，都必须支持进入该 Employee 的 Shared Workstation**。基础范式跨所有业务一致，不为不同部门重新设计「员工工作方式」。

> **补强（Shared Main Composition · 2026-08-17 Delta-X9 回写）**：Main 由 **Domain Business Surface（业务展示区，内部架构名，非强制 UI 标题）** + **Shared Work Area（工作区）** 两部分组成。"业务展示区"只规定其职责——让 CEO 在 Context / Utility 全部关闭时也能理解"这个业务现在整体怎么样"；目标 / 状态 / 关键对象 / 进度 / 结果 / Blocker / Needs CEO 等仅为候选维度，具体展示哪些、字段与视觉形式全部由 Domain 决定。Employee Workstation 属于**工作区**，且 **≠ 整个 Main**；钻取进具体员工时，Main 的"工作区"局部呈现其 Conversation-first Workstation，不改变 Main 还含独立的业务展示区。

**2026-09-15能力空间边界：** 完整Conversation、复杂Browser操作、复杂Model设置、持续专业编辑/分析属于Main。Utility仍为辅助Evidence/Result Detail/Reference/Preview/有限详情编辑，可放大阅读但不成为第二Main；Left Context只含当前Domain对象与局部切换，不是全公司树。工具来自当前Work/Workspace或Settings，不增加一级导航；新字段和能力状态消费Company OS Shared §10–18及Master Map。未经既有Interaction Contract接受的具体布局DESIGN OPEN。

### 0.2 抽象的层级关系

```text
Layer 0  Frozen Tokens (_system/tokens.css)        ← 颜色/字号/间距/圆角唯一真源
Layer 1  Workspace Shell Contract (本规范 §1)        ← 空间职责 + 四独立 Pane + Pane-local Header + 三 Toggle + 对象搜索 + 自适应表面
Layer 2  Adaptive Surface Spec (本规范 §2)          ← Context/Utility 按需机制
Layer 3  Shared Company Patterns (本规范 §3)        ← 7 个可复用模式
Layer 4  Workspace Instance (B 阶段: RD 等)         ← 声明主工作区布局 + 填充插槽
```

`Curis_Workspace_Shell.md` 的"5 槽位（结果条/责任链/管道/侧栏/CEO队列）"是 **Layer 4 的一种 Main 变体（运营驱动型）**，不是 Shell Contract 本身。本规范定义的是 Layer 1–3，与运营槽位不冲突、不重复。

---

## 1. Workspace Shell Contract（固定层 · Layer 1）

### 1.1 空间职责表

| 区域 | 是否固定 | 职责 | 备注 |
|------|---------|------|------|
| **Navigation Pane** | 固定（可完全收起） | 窗口控制（macOS traffic lights，桌面 App 原生）+ 全局对象搜索入口 + Navigation Toggle(T1) + 七区导航 + 用户/主题/设置 | 顶部齐平；自带 Pane Header；收起时 `width:0`（完全隐藏） |
| **Context Pane**（左） | **Adaptive** | Workspace Domain Navigation + 当前业务上下文 / 决策支撑 | 默认收起；由 T2 开合；Resizable；具体菜单由 Package / Instance 声明 |
| **Main Workspace Pane** | 固定（必有） | 当前选中的 Professional Surface + 相关 Shared Work Area；Surface 的专业业务展示由 Domain 决定 | 顶部齐平；自带 Pane Header；**布局由 Workspace 决定**（见 0.1 边界修正 2），Shell 不规定内部；Context / Utility 全关时 Main 自成立 |
| **Utility Pane**（右） | **Adaptive** | 当前对象的 Detail / Editor / Evidence / Tool + Utility Maximize | 默认收起；由 T3 开合；Resizable |

> **注（边界修正 1）**：不存在第二套员工队列 Shell 区域。员工在任何位置（主工作区底部、列表、侧栏）均以 **Collapsed Employee Workstation** 呈现，统一使用 §3.1 状态模型。Shell 不单独定义 Employee Queue / Footer。四 Pane 彼此独立、顶部齐平、各自 Pane Header + Pane Content（取代旧 Global Topbar 横跨结构，见 §1.5）。

### 1.2 Desktop 参考组合（Top-aligned Independent Pane · 可见时）

当四种职责在 Desktop 同时以 Pane 呈现时，各 Pane 为独立列，均从窗口顶部开始、顶部齐平；每列内有自己的 Pane Header（位于列顶）与 Pane Content。该组合是参考实现，不把 Four-Pane 职责冻结成四根永久物理栏。**不采用 Global Topbar 横跨整个 App**。

```css
/* 默认态：Navigation 固定列 + Main 弹性满宽；Context/Utility 默认不占空间 */
.workspace-shell {
  display: grid;
  grid-template-columns: var(--ui-sidebar-w) minmax(0, 1fr); /* Nav 固定列 + Main 弹性 */
}
/* Context Surface 展开：左插一列（Resizable，拖拽边界调宽） */
.workspace-shell.with-context {
  grid-template-columns: var(--ui-sidebar-w) var(--ctx-w) minmax(0, 1fr);
}
/* Utility Surface 展开：右插一列（Resizable，拖拽边界调宽） */
.workspace-shell.with-utility {
  grid-template-columns: var(--ui-sidebar-w) minmax(0, 1fr) var(--util-w);
}
```

- `--ui-sidebar-w` 来自 Frozen tokens（原 `--ui-sidebar-w: 220px`，仅为建议默认）。
- `--ctx-w` / `--util-w` 为 Adaptive Surface **推荐默认**展开宽度（Context 260px / Utility 360px），**仅为建议默认，非固定宽度**（Delta-X5 已批准）：用户可拖拽边界覆盖、记忆上次宽度；设 min/max 与 Main minimum usable width；空间不足自动转 Overlay/Focus；无显式放大/缩小按钮。
- **Navigation Pane 采用 T1 Toggle 完全收起/展开（非 Resizable）**：收起时 `width:0`（完全隐藏），T1 自动转移到 Main Header 左侧作为稳定 reopen 入口。
- Main 永远 `minmax(0, 1fr)`，保证自适应面板展开时主区弹性收缩而非溢出；每 Pane 为独立列，Context/Utility 打开在结构上不可能挤压 Main Header。

### 1.3 导航七区（来自 Current Product Truth，引用 UI Blueprint）

固定顺序，不增不减：

1. CEO 工作台
2. 业务空间
3. 组织中心
4. 人才与能力
5. 经营洞察
6. 资料库
7. 会议

底部固定：设置 / 帮助与反馈（移入左下角用户头像菜单）。

### 1.4 主题与令牌纪律

- 主题三态（dark/light/system）由 `_system/theme.js` 统一接管，禁止页面自带主题逻辑。
- 所有视觉令牌只能来自 Frozen `_system/tokens.css`；禁止页面私有 accent（历史违规 `#387bff`、私有 `--radius-*`）。
- mock 数据必须带 `.mock-badge`「示例数据」徽标。

---

## 1.5 Pane Header 定义与 Shell 交互契约（S2 / S3 / S5 / S6 / S7）

> 本节将 XHS Visual v4（2026-08-15）经 Final Review 批准的 Shell Delta **S1–S7** 正式回写为 Shell Contract。
> **Prototype 实现不冻结**：Prototype 的 JS / CSS 具体实现（`querySelectorAll` / `classList` / `.app` 作用域 / 纯 CSS 显隐 / 当前 HTML 事件绑定方式）**不进入本 Contract**，仅作 Reference（见 `Curis_Desktop_Pane_Shell_Exploration_v1.md` §9.7，标 `PROTOTYPE REFERENCE ONLY`）。本 Contract 只冻结**行为**与**位置语义**。

### 1.5.1 Pane-local Header（S2）

四 Pane 各自拥有独立的 Pane Header + Pane Content，顶部齐平，**不采用 Global Topbar 横跨整个 App**。

- **Navigation Pane Header**：单行（`flex row, space-between`）——左：macOS traffic lights（桌面 App 原生窗口控制）；右：🔍 Search icon + T1 Navigation Toggle。
- **Context Pane Header**：Context 类型 / 名称 + 切换 + 对象动作（由 Instance 声明；T2 控制开合，本 Header 不重复开合、不设独立 ✕）。
- **Main Pane Header**：Breadcrumb + T2（当前Main有合法Context能力/内容时固定在左侧）/ T3（条件右）+ More。（T1 在 Nav 折叠时条件显示于最左。）
- **Utility Pane Header**：模式名 / 子标题 + 模式切换 + ↗ Maximize + T3（展开后从 Main Header 转移至此；本 Header 不重复开合、不设独立 ✕）。

### 1.5.2 三个 Toggle 位置（S3，跨 Workspace 一致）

| Toggle | 固定位置 | 语义 |
|--------|---------|------|
| **T1 Navigation Toggle** | 展开：Nav Header 右侧；折叠后转移到 Main Header 最左 | 控制 Navigation 完全收起/展开 |
| **T2 Context Toggle** | 当前Main有合法Context能力/内容时，固定显示于Main Pane Header左侧 | 双向控制Context展开/收起；无合法Context内容时隐藏，不显示disabled占位 |
| **T3 Utility Toggle** | 折叠：Main Header 右侧；展开后转移到 Utility Header 右侧（与 T1 对称） | 控制 Utility Surface 开合 |

位置在所有 Workspace 实例中完全一致；视觉风格（方形/圆形/图标密度）由 Frozen Design Tokens 决定，不在此冻结。

**FDI-01 · CEO Decision（2026-09-15）：** T2的“常驻”仅指有合法Context场景中的位置与控制稳定性，不是永久可见。无合法Context内容时T2隐藏，不显示disabled占位、不预留Context空面板，Main Header正常使用该空间；与§2.2一致。本消歧不改变T1/T3、Four-Pane或其他Shell行为。

### 1.5.3 Toggle 行为契约（S7 · 冻结行为，不冻结实现）

1. **双向 Toggle，不区分 open/close 按钮**：T1/T2/T3 均为双向操作（点击展开，再点折叠）；禁止为 Context/Utility 提供独立 ✕ 关闭按钮。
2. **展开/收起后控制入口持续可达**：位置转移始终落在活跃 Header 内（Nav 折叠→T1 转 Main Header；Utility 展开→T3 转 Utility Header），不悬浮、不消失。
3. **Pane 状态变化后 Toggle 仍可操作**：当前可见的那个 Toggle 实例必须已绑定事件；状态切换后操作不失效。
4. **Workspace / Pane 实例状态隔离**：每个 Workspace 根容器作用域独立，Pane 状态变化只影响自身实例，不串扰其他 Workspace 实例。

> **实现不冻结（PROTOTYPE REFERENCE ONLY）**：Prototype 采用的 `querySelectorAll` 全实例绑定 / `classList.toggle` / 以 `.app` 为作用域 / 纯 CSS 位置转移显隐 / 当前 HTML 具体事件绑定方式，仅作为实现参考；正式 React / Tauri 实现自行决定技术方案，只要满足上述 4 条行为契约即可。

### 1.5.4 Company-wide Object Search（S5）

- **入口**：Navigation Pane Header 右侧轻量 🔍 Search icon（**非** Navigation Content 常驻大搜索框）；点击展开独立 Search Surface，再次点击 / 点遮罩 / ✕ / `Esc` 收起。
- **产品语义 = Company-wide Object Search（Object-first, Task-capable）**：Curis 是 Company OS，Search 检索公司级对象——Business / Workspace / Employee·Role / Business Object(Note·Video·Project·商品) / Knowledge·Document·Asset / Result·Artifact / Meeting / Decision / Capability(Expert·Skill·Connector) / Task——**不是** WorkBuddy/Codex 的 Task 历史搜索。
- **Surface 信息结构（展开态）**：顶部统一输入框；空查询→Recent；有查询→按对象类型分组结果（图标 + 标题 + 组织/业务上下文 + 类型标签），点击直达对象/Workspace；底部操作提示 + 范围声明。
- **v1 明确不做（RESERVED）**：复杂 NL 关系查询、AI 问答、Command Palette、高级过滤器、搜索语法。
- Navigation 折叠（`width:0`）时 Nav Header 整体隐藏，Search icon 随之不可见（首版不跨 Header 转移，与 T1 行为不同：T1 转移是为了恢复导航，Search 在折叠态下非必需）。

### 1.5.5 Utility Maximize（S6）

- **内置浏览器**：Utility Pane 可承载 Instance 声明的内置预览浏览器（多文件标签切换 / 内置渲染），用于查看文件、文档、HTML、图片等。
- **Maximize**：Utility Header 含 ↗ 最大化按钮，点击后 Utility 以全屏 Overlay 覆盖整个页面（含 Main），其他 Pane 暂时隐藏；退出通过 ✕ / `Esc` / 点遮罩。
- 具体浏览器引擎与渲染实现由 Instance / Platform 决定，Shell 只定义「最大化 Overlay」这一交互能力。

---

## 2. Adaptive Surface Specification（自适应表面 · Layer 2）

### 2.1 定义

**Adaptive Surface** = 不保证永久可见、由用户操作或事件触发出现的专业工作面。
Context Surface（左）与 Utility Surface（右）都属于此类，**不是主工作区的一部分**。

核心契约：
- 默认态两者均收起，主区满宽；
- 可单开、可双开、可全关；
- 收起后主区回到弹性满宽，无残留占位；
- 展开/收起动效统一：`--ui-dur-3` (320ms) + `--ui-ease-standard`。

### 2.2 Context Surface（左 · 按需）

| 项 | 规格 |
|----|------|
| 触发 | 顶栏控件，或对话内上下文引用 |
| 展开方式 | 统一交互契约（触发 / 开合 / 动效）；具体 overlay 或 push 由窗口尺寸与场景自适应决定，不强制全产品单一实现 |
| 内容 | 由 Workspace 声明：Domain Navigation、当前 Professional Surface、相关对象 / 历史 / 目录等业务上下文；具体菜单和信息架构不由 Shell 冻结 |
| 空态 | 无上下文时不显示入口，不预留空面板 |
| 令牌 | 容器 `--ui-surface-2`；标题 `--ui-text-2`；当前项高亮 `--ui-accent` |
| 宽度（Resizable · Delta-X5） | 默认 260px（建议值，非固定）；用户可拖拽边界调整；记忆上次宽度；min/max 与 Main minimum usable width 约束；空间不足自动 Overlay/Focus；无显式放大/缩小按钮。 |

### 2.3 Utility Surface（右 · 按需）

| 项 | 规格 |
|----|------|
| 触发 | 对话内轻量引用（Result Reference / Diff 链接 / 数据链接） |
| 模式容器 | Shell 只定义专业 Utility 容器与开合机制；**模式的数量与内容完全由 Workspace Instance 声明**（研发可声明 Diff / Source / Preview，其他域声明自己的模式集） |
| 专注模式 | 比主区更深 1 级的背景色（`#181a1d` 深 / 对应浅色），创造"沉浸工具"感 |
| 操作栏 | 底部固定操作（如"提交变更 / 请求协审"），由当前模式决定 |
| 令牌 | 容器更深背景；语法高亮色需补充到令牌体系（新增 `--ui-syntax-*` 子令牌，B 阶段定） |
| 宽度（Resizable · Delta-X5） | 默认 360px（建议值，非固定）；用户可拖拽边界调整；记忆上次宽度；min/max 与 Main minimum usable width 约束；空间不足自动 Overlay/Focus；无显式放大/缩小按钮。 |

### 2.4 共同规则

- 两者互不依赖：可只开 Context、只开 Utility、或双开。
- 同一引用可同时触发两侧（如点文件引用 → 左开文件树定位、右开 Diff）。
- 移动端（<640px）：Adaptive Surface 转为全屏 overlay，不并排。
- **Resizable（Delta-X5）**：Context / Utility 均为可拖拽调宽的 Resizable Adaptive Surface；默认宽度仅为建议值，用户拖边界覆盖并记忆；设 min/max 与 Main 最小可用宽度，空间不足自动 Overlay/Focus；无显式放大/缩小按钮。

---

## 3. Shared Company Patterns（固化 · Layer 3）

> 以下 Pattern 从 RD Workspace Visual Baseline v1 提取，泛化为 Company 级 **Shared Company Patterns（Available Capability）**。
> 研发是第一个使用者，但模式本身不绑定研发语义，任何 Workspace **按需采用**，非强制要求。

### 3.1 Employee Workstation（Collapsed / Expanded）

> **Current适用范围（CEO 2026-09-23）**：专业对象内员工交互优先消费下方§3.1A。以下历史解剖中的全员工列表、单一working默认展开、常驻Idle文字不再适用于该场景；独立员工Conversation-first与canonical状态语义保留。不得跳过§3.1A单独按旧句实施。

**定义**：在对话流或责任视图中，呈现单个 AI 员工工作状态的可折叠单元。

> **Global Shared Rule（2026-08-16 回写 · Delta-S1）**：本 Pattern 是**全公司所有 AI Employee 的统一基础工作范式**，跨研发 / 内容增长 / 空间工程 / 销售 / 客服 / 未来业务一致。CEO 进入任意一个具体 Employee 后，Main 统一呈现其 **Conversation-first Employee Workstation**（自然 Conversation + 工作状态 + Tool/Action 状态 + Result/Artifact 引用 + Composer），**不为不同业务重新设计**。Domain-specific 的是 Workspace 自身的专业业务界面（日历 / 代码 / 工单队列等），不是本基础范式。

> **Main 组合澄清（2026-08-17 Delta-X9）**：Employee Workstation ∈ Main.WorkArea（工作区）；Main = Domain Business Surface（业务展示区）+ Shared Work Area（工作区）。钻取进具体员工时，Main 的"工作区"局部呈现其 Workstation，不改变 Main 还含独立的业务展示区。本澄清不新开 P 编号、不修改 P1–P7、不重定义 Workstation。

**Anatomy（普通列表行，不做 Card · 2026-08-17 Delta-X10 精化）**：
- **Row（始终可见，可点击）**，两行结构：
  - `32px` 角色色头像（**占两行**；色仅作区分，必须配合文字/图标非颜色指示，满足色盲可达性）
  - 第二列第一行：**员工名 + �岗位（堆叠）**
  - 第二列第二行：**当前职责简述**（轻量一行）
  - 右侧：**Employee Runtime Status（经 UI Projection，见下方「Shared Employee UI Status」）**
  - 最右：**展开箭头 `▸`（Conversation 收起）/ `▾`（展开）**
- **交互**：
  - 点击**头像或姓名** → Utility 打开 **Shared Employee Detail（§3.14，六字段，无 Conversation）**；**不设独立「详情」按钮**（详情动作即「点头像/姓名」）。
  - 点击箭头（或行其余空白区）→ 展开/收起该 Employee 的 Conversation-first Workstation。
- **Body（仅展开时可见）**：
  - 自然 Agent Conversation（居中 / Bounded·Responsive / 用户可拖拽调高，见下方「Conversation Surface Shared Rules」）
  - 底部输入消费Shared Composer Shell完整语义槽位（见§3.5）；Compact仅描述历史紧凑展示，不构成缩减功能的第二合同

> **三层概念边界（防误导 · 2026-08-17 Stale-Rule Cleanup）**：① **Runtime State Schema**（下表 `working`/`waiting`/`needs_ceo`/`completed`/`failed`/`idle`）= 员工真实运行状态真源，本轮不改动；② **Employee UI Status Projection**（上方「Shared Employee UI Status」blockquote）= 三态用户侧投影，源自真实 Runtime/Responsibility 事实，≠ Runtime State Schema；③ **Conversation 展开状态** = 纯 UI 偏好，由用户控制，不随 Runtime 状态自动改变。三者相互独立，不得混用或相互推导。

**States**：
| 状态 | 表现 |
|------|------|
| `working` | 状态标签品牌绿 + 脉冲点 |
| `waiting` | 中性标签 |
| `needs_ceo` | 员工责任状态之一：warning 标签 + danger 标签，带注意力；是否展开不固定，由 Workspace / 场景决定；与 Workspace 级 Needs CEO / Decision Pattern（§3.3）分离 |
| `completed` | success 标签 |
| `failed` | 显著呈现失败阶段 / 责任人 / 恢复动作 / 重试边界 |
| `idle` | 保留可恢复摘要 |

> **Runtime State ≠ UI Expand/Collapse State（2026-08-18 stale-rule cleanup）**：上表只表达 Runtime State Schema 的真实语义，不包含展开/收起建议。进入 Workspace 后，展开/收起完全由用户控制；Runtime 状态变化不得自动强制改变 UI 展开状态。唯一允许的初始自动展开规则见下方“工作区编排约定”。

> **状态模型扩展（Delta-1，B 阶段 RD Instance 批准后并入）**：`failed` / `idle` 两态来自 RD Design Brief §4，已批准为 Shared Employee Workstation 状态模型的正式成员，所有采用此 Pattern 的 Workspace 均可使用。

> **Shared Employee UI Status = Runtime Truth 的用户侧投影（2026-08-17 Delta-X10）**：上表 **Runtime State Schema（`working`/`waiting`/`needs_ceo`/`completed`/`failed`/`idle`）是员工真实运行状态的真源，本轮不删、不改语义、不迁移、不新增 Runtime Primitive（含 `blocked`/`offline`/`unavailable`）**。用户侧只呈现下列**三态投影**，投影必须来自真实 Runtime / Responsibility 事实：
> - `空闲`：Runtime 无进行中工作（如 `idle`）。
> - `工作中 · <简短实时工作描述>`：来自 Runtime `working` + 真实运行时短句（由 Runtime 提供，非编造）。
> - `阻塞 · <简短问题原因>`：**仅当真实 Runtime / Responsibility 事实能证明阻塞时投影**；若 Current Runtime 无独立 blocked 真值，UI 不得伪造状态、不得新增 Runtime Primitive。
> - **禁止把 已完成 / 待审核 / 已验收 / 待命 当 Employee UI Status**（属 Work/Result/Responsibility 事实；员工完成无其他工作投影回 `空闲`）。
> - Runtime State 模型是否需清理，留给后续独立技术 / Authority 审计，不在本 UI 层处理。

> **Conversation Surface Shared Rules（2026-08-17 Delta-X10，只 Frozen 语义不 Frozen px）**：展开 Employee Row 后直接出现统一 Conversation-first Workstation（不做 Card、不做 AI 状态 Dashboard、不重复显示 Employee Holder/当前步骤/下一步）。对话 = 自然消息流 + Runtime 真实过程（仅真实发生时作轻量状态行）+ Result/Artifact 轻量引用 + Composer。规则：① **居中**（Main 可用宽度内始终居中）；② **Bounded·Responsive**（随 Desktop/Pane 宽度自适应，有合理 minimum/preferred/maximum readable width，不写死 px）；③ **默认舒适高度**；④ **用户可拖拽调整高度**（右下角手柄，仅本地 UI 偏好，不回写 Runtime）；⑤ **展开/收起只改 UI 不改 Runtime**（收起后员工继续工作，再展开可见最新输出）。

> **Conversation Content Block（长内容块）Shared Rule（2026-08-17 Delta-X12，只 Frozen 语义不 Frozen px/字数/样式）**：Conversation 本身**不 Card 化**；普通短消息走**自然消息流**，不强制结构化。当且仅当出现 **长文本 / Tool / Terminal / Code / Diff / Structured Result** 等内容时，允许使用 **bounded embedded content block（有界内嵌内容块）** 承载：① 长内容块**内部可滚动**，避免单次输出无限撑高多人共享工作区；② 点击块内「完整查看」或来源引用可进入 **Utility 专业视图**看全文（Utility 不受此有界限制）；③ 块的可有界尺寸、字数/行数阈值与具体视觉样式**不 Frozen**，由实现按内容类型与可用宽度自适应决定。本规则只规范「长内容如何有界呈现」，**不新增任何 Runtime Primitive、不改变 Runtime State Schema、不定义具体 px**。

**Correction（来自 Delta §3）**：员工标题栏**不常驻专业工具按钮**（如"查看差异""源代码"）。工具从 Conversation 内的轻量引用进入，不从员工标题进入。

**复用（按需）**：Employee Workstation 是呈现员工的可用模式；Workspace 若在主工作面展示员工，统一采用此状态模型（collapsed 为默认密度）。小红书员工以"内容生产中"呈现，会议员工以"发言/纪要中"呈现。非所有 Workspace 必须展示员工。

**工作区（Shared Work Area）编排约定（2026-08-17 Delta-X9 回写）**：
- **工作区本质 = Employee Workstation List**：同一业务下所有真实 AI Employee 以列表呈现，统一命名"工作区"。（对长期 Business Workspace + 真实 AI Operating Team，Shared Work Area 是 Main 的统一组成部分，非 Domain 可选项；不沿用"Domain 可自行决定是否采用员工工作区"旧措辞。）
- **每个 Employee 固定轻量行（普通列表行，不做 Card）**：头像（跨两行）+ 行1 姓名+岗位 + 行2 当前职责 + 当前状态（UI Projection，见上方「Shared Employee UI Status」）+ 展开/收起（chevron）；**点击头像/姓名 → Utility Employee Detail（不设独立「详情」按钮）**。
- **展开后统一显示 Frozen Conversation-first Workstation**：Conversation + 工作过程 + Result / Artifact 轻量引用 + Composer。
- **Runtime 状态 ≠ UI 折叠状态**：`working` / `waiting` / `completed` / `idle` 等是员工真实运行状态，不强制绑定展开/收起。CEO 进入 Workspace 后可自由展开/收起任一 Employee Workstation；Runtime 状态变化不得自动强制改变 UI 展开状态。
- **收起不暂停、不停止、不改变真实工作状态**：员工继续运行，列表状态持续更新；再次展开可见最新工作过程。已完成 / 等待员工同样允许 CEO 展开其 Conversation 并继续讨论。
- **唯一默认展开行为**：当用户从 Workspace 外部进入、且存在**单一当前正在工作的 Employee** 时，该 Employee Workstation 默认展开，让 CEO 直接感知员工正在持续工作。进入 Workspace 后的展开/收起状态由用户自行控制，不因 Runtime 状态自动强制改变。
- **多 Employee 并行工作的默认展开策略本轮不额外定义**：无真实"主焦点员工"语义时，不自行创造；交由各 Workspace 实例按真实协作拓扑决定。

### 3.1A V1 Shared Employee Interaction（2026-09-23 CEO Accepted · Frozen）

Authority Class: CURRENT / FROZEN SHARED PRODUCT CONTRACT。上位依据：[Product Blueprint — Shared Employee Interaction](../01_Product/Curis_Product_Blueprint.html#shared-employee-interaction-20260923)。这是既有Employee / Responsibility / Conversation / Result的交互收口，不新增对象、Runtime状态或Workflow。适用于专业对象内协作；独立Full Main Conversation、Meeting多人语义不被改造成专业对象页面。

- **默认空间**：Professional Object标题/状态 → Lightweight Employee Bar → Professional Main。Employee持续在场，Conversation默认完全隐藏、不占空间；不因单一员工working自动展开。
- **Employee Bar**：头像、姓名、Current Responsibility、必要的一句有意义工作状态、一起讨论。只突出当前Responsible Employee；不是大卡片、团队头像墙、Agent Manager，也不常驻Provider/Model/Tool状态。无重要状态时只显示责任，不持续显示“空闲 / 无进行中执行”。头像/姓名仍进入既有Employee Detail。
- **按需展开**：一起讨论 / 讨论这段 / 要求修改 → Bar下方、专业Main上方的Main.WorkArea Conversation＋既有Shared Composer。收起讨论完整隐藏该区域，保留history、draft input、selection、current object和target Employee；不暂停执行、不改变责任或Result。不是永久右Drawer或floating Employee Chat。
- **Composer**：沿用§3.5；Text、Current Context、Selection、Reference、Attachment、Target Employee、Send是交互职责，不是新配置表或Prompt Builder。只呈现真实可用能力；不支持的Attachment/Model/Agent/Tool/Access隐藏或明确不可用，不做假按钮。发送仍校验合法scope与执行权限。
- **Selection**：明确Object、Version、专业Locator、Short Excerpt/Description、Return Anchor；可定位、移除、更换。CG可用Script Paragraph/Shot/Artifact Region；Writing用Chapter/Paragraph/Text Range；Music用Candidate/Time Range/Lyrics Section。Base改变即stale，保留原输入与历史引用，要求重新选择/比较，禁止静默映射latest。Selection不是授权扩张，也不证明Provider理解或精确编辑能力。
- **Conversation = Communication；Professional Main = Work**：交流承载意图、解释、追问、澄清、进度和Result Reference；Artifact/Revision/Candidate/Manuscript/Audio/Script/Finding回Main进行Preview/Compare/Review/Audition与Human Choice，不能只存聊天气泡。结果回来后可以收起讨论。
- **P6兼容**：引用仍可打开Utility辅助查看同一Result的Evidence/Provenance，再返回同对象/版本/anchor的Main做专业处理；不建第二Result。长消息有界块不替代专业Artifact真源。
- **Human Choice**：Viewed ≠ Accepted。Accept/Reject/Revise绑定Object＋Version＋Effect，不新增全业务统一ACCEPTED状态。CG采纳脚本≠视频核验/发布；Writing Revision→Draft→Review→Author Confirmation→Formal Manuscript；Music Candidate→Selected Candidate→Explicit Master Confirmation，均不等于Published。
- **责任与状态**：Object Owner ≠ Responsibility Holder ≠ Current Executor。执行结束不删除责任；Review不自动Handoff，普通创作选择不自动P7。Reviewer/Supporting Employee在实际Result/Review贡献处出现。沿用canonical事实，不新增Idle/Working/Waiting/Blocked/Result Ready五态；“正在处理”“等你确认”“有结果可查看”是有来源的工作描述，非新的Employee枚举，无证据不得制造working。
- **CEO Assistant**：保持全局轻量悬浮Company-level Coordinator，与专业Employee及其Conversation身份独立。Employee讨论展开时降低其视觉权重，不同时摆两个同等级Full Composer；不删除或用Assistant替员工回复。
- **Four-Pane不变**：Navigation / Context / Main / Utility职责不变；Employee Conversation在Main.WorkArea，Employee Detail/Evidence/Provenance可进Utility，专业Result处理在Main。共享语法不要求业务Surface相同，不冻结尺寸、配色或完整业务版式。

**旧句适用范围裁定**：§3.1旧“全部Employee Workstation List”“单一working默认展开”和常驻Idle文字，在专业对象内由本节替代；独立员工会话的Conversation-first仍成立。既有三态投影保留为事实解释，不强制每态常驻展示；Work的待确认/结果就绪不升级为Employee状态。此处是CEO明确产品展示修订，不是Architecture conflict或Runtime迁移。

Decision Evidence：[Accepted Candidate](../research/shared-employee-interaction-2026-09-23/CURIS_V1_SHARED_EMPLOYEE_INTERACTION_CANDIDATE.md)及其Writing三态。证据不作为第二Authority；HTML通过不等于Runtime已实现。

### 3.2 Handoff Event（责任交接 · P5 · Frozen）

**定义**：员工之间的责任交接事件，在对话流中轻量呈现，不阻断主流程。

**视觉**：
- Handoff 标记（如 `⇄` 或「交接」徽标）
- 来源员工 → 目标员工
- 交接原因 + 下一检查点

**交互**：点击展开交接详情（在 Utility Surface 或 Drawer 中）。

**复用**：研发（工程→QA）、小红书（创作→审核）、会议（提案→决策）均通用。

### 3.3 Needs CEO / Decision（阻断性决策）

**定义**：需 CEO 批准/驳回/替代的阻断性请求。**不绑定特定 Workspace**。

> **与员工 `needs_ceo` 状态分离（边界修正 2）**：本 Pattern 是 **Workspace 级**阻断性决策面（可出现在顶部 Decision Banner），与单个 Employee 的 `needs_ceo` 责任状态（§3.1）**分开定义**。员工卡上的 `needs_ceo` 只是该员工的责任状态指示；真正的 Decision 交互由本 Pattern 承载，Decision 可在顶部出现而员工仍保留其责任状态。

**视觉**：
- 橙色 Decision Banner（warning 色系 `--ui-warning`）
- 图标 + 标题「需要 CEO 决策」+ 描述 + 元信息（影响范围/风险评估，可折叠）
- 三按钮：主操作（✓ 执行，品牌绿）+ 次操作（⛔ 驳回）+ 第三操作（「暂缓」/「替代」）

**States**：`waiting_ceo` / `approved` / `returned`。

**复用矩阵**：
- 研发：DB 变更 / 发布上线
- 小红书：品牌/敏感表达确认
- 抖音：投放预算确认
- 会议：方向/Decision 确认

**Correction**：Delta Open Question 中的「选择返回」语义不清 → 建议改为「暂缓」或「搁置」，更符合 CEO 心智。

### 3.4 Result Reference（轻量结果引用 · P6 · Frozen）

**定义**：对话中对工作结果的轻量引用，点击后打开对应 Utility Surface。**对话内不铺完整 Diff/数据/视频**。

**视觉**：`emoji + 文字 + ▸箭头`，使用 `--ui-accent` 色。

**示例**：
- 研发：`📎 查看差异 (+34/-93) ▸` / `✅ 工作结果已就绪 ▸`
- 小红书：`📊 数据看板 ▸` / `✅ 笔记已发布 ▸`
- 抖音：`🎬 视频预览 ▸` / `📊 完播数据 ▸`
- 会议：`📝 纪要预览 ▸` / `✅ Decision 已记录 ▸`

**规则**（来自 Delta §4 Conversation/Diff Separation）：
- 对话内仅放引用行，不放完整代码块/数据表/视频帧；
- 单击引用 → 开右侧 Utility Surface 对应模式；
- 代码引用示例格式：`api/users.ts · 34-93 · 查看差异`。

### 3.5 Composer（指令输入 · Shared Composer Shell · 2026-08-17 Delta-X10 升级）

**定义**：锚定在活跃 Workstation Conversation 底部的统一输入面。**Shared 固定语义槽位，不 Frozen 具体布局**（Desktop 推荐「输入区在上、底部左右分组」，响应式/overflow/mobile 可重排，槽位不丢）。基于 WorkBuddy / Codex / 豆包 / Coze / EvoFlow 参考**提炼统一骨架**，不照抄任何产品；Curis 面向普通用户，默认不把重要能力全部藏进 `+`。

**语义槽位（Shared 固定，所有 Employee 通用）**：
- **输入区**：多行文本输入，placeholder 随 Employee/场景变化。
- **`+`（统一 Add 入口，语义冻结、文案不冻结）**：根据当前 Employee **真实支持的能力**提供（文件 / 图片 / 资料·Knowledge / Skill / Connector / 其他真实支持的功能）；选择后仅在 Composer 显示对应 chip/reference，未选择不占空间；用户侧避免要求理解 Tool/MCP/Skill/Connector 内部区别（统一为「功能/资源」）。**按钮文案不强制（可用 `+`，不必叫「功能」）**。
- **访问权限（固定显性入口）**：必须消费真实 Computer Access / Provider 权限能力（其 `requested ≠ configured ≠ effective` 真值由 Provider Capability 提供）；不支持的权限不得伪造为可选。
- **工作模式（固定显性入口）**：面向普通用户表达工作意图（如 目标 / 计划）；具体模式须来自真实 Runtime 能力，不凭 UI 自创完整模式体系。
- **执行选择（Execution Selector，必须显性区分 Model / Agent）**：见下方适配规则。
- **Voice（可选）**：仅当 Provider 支持时显示。
- **Send**：发送。

**Provider Adaptation（Shared 固定 vs Provider 决定）**：

| 维度 | Shared 固定（Core） | Provider 决定（Adapter 暴露） |
|---|---|---|
| 语义槽位（Input/Add/Access/Work Mode/Selected/Execution/Voice/Send） | ✅ 槽位语义固定 | — |
| 布局 | Desktop 推荐左右分组；**不 Frozen 为所有尺寸/平台固定排列** | 响应式/mobile 可重排 |
| 支持哪些**权限** | 入口固定，消费真值 | Provider 决定实际可选权限集 |
| 支持哪些**工作模式** | 入口固定 | Provider 决定实际模式集 |
| **Model 还是 Agent** | 必须显性区分二者 | Provider 暴露其本质（模型型 / Agent 型） |
| 是否允许**切换模型** | 入口存在 | Provider 决定是否可切换 |
| Agent 原生执行设置 | 不制造第二套 | Agent 经 Adapter 暴露真实支持项 |

- **Model-backed Employee** → Execution Selector 展示 **Model / Auto 选择**（如 `Auto` / `GPT` / `Claude` …）。
- **Agent-backed Employee** → Execution Selector 展示**真实 Agent**（如 `Codex` / `Claude Code` / 其他 Provider Agent）；**不得把 Agent 错误降级成「一个模型」**（Agent ≠ Model，Capability Truth 边界）；若 Agent 自身管理 Model/Permission/Mode，由 **Provider Adapter 暴露真实项**，Curis 不造第二套虚假 Model Truth。
- **不把 Codex / Claude Code / ChatGPT 等 Provider 写死进 Core 规则**——它们是 Provider 实例，经 Adapter 被 Shared Shell 消费。

**Rationale**：只显示改变当前运行契约的控件（UI Blueprint 规则）；Shared 固定槽位保证跨 Workspace 一致，Provider 差异经 Adapter 注入。

### 3.6 Context Surface（作为 Adaptive Surface 的一种）

见 §2.2。此处强调它作为 Shared Pattern 的复用性：每个 Workspace 声明自己的 Context 内容，Shell 不预设。

### 3.7 Utility Surface（作为 Adaptive Surface 的一种）

见 §2.3。此处强调它作为 Shared Pattern 的复用性：每个 Workspace 声明自己的 Utility 模式集与操作栏，Shell 只提供容器与展开机制。

> 见 §3.8 Employee Presence（已 Frozen，P2）。

---

### 3.8 Employee Presence（轻量员工责任存在 · P2 · Frozen）

**定义**：业务对象上的轻量员工责任存在，持续可感知（贴在业务对象上：Note 卡头像 / Split 顶部 Presence 条），包含 Identity / Role / Current Responsibility / Current Activity / Status / 可选 Handoff Origin + Open Workstation 入口。

**与 Employee Workstation（§3.1）区分**：Presence 持续可感知、不做常驻列表、也不完全隐藏；Workstation / Conversation 按需展开。

**关键边界（P2 ↔ P3）**：Employee Presence 只表达 **Current Responsibility / Current Executor**（有真实员工在场）。不是 Object Owner；不是「最后处理过的人」；无员工时不用。

**Multi-Surface 边界（2026-08-21）**：只投影与当前 Surface / Object 真实相关的 Holder、Executor、Consult、Review、Handoff 或异常责任；不得因 Employee 可跨 Surface 工作而建设常驻在线员工墙。进入同一 Employee 时复用 Company OS 的 Conversation-first Workstation，并保持 Assignment scope 与 context isolation。

**复用（按需）**：研发（任务卡头像 + PR 负责人 Presence）、小红书（Note 卡作者头像 + 创作/审核 Presence）、会议（议题负责人 Presence）。

### 3.9 System Activity（非员工 Runtime · P3 · Frozen）

**定义**：表达非员工 Runtime / Automation 状态（Analytics / Monitoring / 自动流水线），在 **Current Executor = none** 时启用。

**硬边界（≠ Employee Presence）**：
- 无员工头像、无「工作过程」入口；
- 不伪装成员工、不造伪岗位；
- 与 Employee Presence **不得混用**（同一业务对象同一时刻要么显员工 Presence，要么显 System Activity，不叠加冒充）。

**复用**：发布后自动 Analytics / Content Reuse Loop、监控流水线、自动 Handoff 执行等系统运行时状态。

### 3.10 三层责任语义（Object Owner ≠ Current Responsibility ≠ Current Executor · P1 · Frozen）

- **Object Owner**：对象稳定归属（如「AI 科技 Workspace」），不随 Handoff 改变，不进入 Presence。
- **Current Responsibility**：当前责任阶段，随 Handoff 转移。
- **Current Executor**：此刻真正执行者；员工完成 / 系统接管时可为 none（此时启用 System Activity，见 §3.9）。

> Employee Presence（§3.8）只表达 Current Responsibility / Current Executor；Object Owner 仅在对象元信息 / 历史中呈现，不占 Presence。

### 3.11 Automation by default / Necessary Human Handoff（P4 · Frozen · CEO Accepted 2026-09-15）

- AI自治默认；员工之间按原责任/结果合同交接，不要求CEO手动点击每个“下一步”。发布后的数据采集只在合法能力可用时继续，不承诺所有平台已接通。
- 登录、MFA、手机确认、身份/现实动作、材料补充及当前AI/Provider不能代理的必要动作，可以在原Work进入 **User Required / Human Handoff**。旧“Human action only at Decision Gates”绝对规则正式SUPERSEDED。
- 必须解释AI已完成什么、为何需要用户、用户做什么、去哪里、完成判据、之后Curis继续什么，保留原Work/责任/Scope与回程。
- 用户点击“已完成”只是报告；有可核验的外部事实时先核验再继续。沉默/离开/等待不等成功；人工控制期间AI不并发争用，恢复重验目标、权限和动作版本。
- 人工接续≠P7 Decision，也不自动触发§3.2 P5责任转移；真正经营决定仍P7，真正责任转移仍P5。完整产品合同见Company OS Shared §11/15。
- 无新增HumanWork/Runtime enum/Console。正常授权后在原Work继续，不能借恢复重放未知外部副作用。

### 3.12 边界澄清（Frozen）

| 边界 | 规则 |
|------|------|
| **Employee Presence ≠ System Activity** | 员工责任存在 与 非员工运行时 不得混用；System Activity 无员工头像、无工作过程入口、不伪装员工 |
| **CEO Decision ≠ Responsibility Handoff ≠ Human Handoff** | §3.3/P7为经营决定；§3.2/P5为真实责任转移；§3.11人工接续可保持原责任等待必要用户动作，三者不互相伪装 |
| **System Runtime ≠ Employee** | 系统自动采集/监测等活动不是员工；经营分析与Review由真实Analyst责任承担，不能被采集器替代。系统活动，不占用 Employee Workstation / Presence，不造伪岗位 |
| **Employee Workstation / Conversation ≠ Context Pane** | 员工工位与对话只在 **Main**；Context 只答「这次工作是什么上下文」，含团队 Presence 简要（P2），**不含完整员工详情、不含员工 Conversation**（2026-08-16 回写 · Delta-S3） |
| **Employee Workstation / Conversation ≠ Employee Detail / Utility Pane** | Utility 的 Employee 视图永远只是 **Detail（§3.14）**，不承载 Conversation；Conversation 一旦出现必属 Main 的 Workstation（2026-08-16 回写 · Delta-S3） |

> **Shared Pattern 索引（P1–P7，均已 APPROVED FOR FREEZE）**：P1 = §3.10 三层责任语义；P2 = §3.8 Employee Presence；P3 = §3.9 System Activity；P4 = §3.11 Automation by default；P5 = §3.2 Handoff Event（此前已 Frozen）；P6 = §3.4 Result Reference（此前已 Frozen）；**P7 = §3.13 CEO Decision Package Pattern（DP-CEO-1 FINAL REVIEW APPROVED 回写）**。本次正式补齐 P1 / P2 / P3 / P4 并固化 §3.12 边界。

---

### 3.13 CEO Decision Package Pattern（决策内容结构 · P7 · Frozen）

**定义**：建立在 §3.3（Needs CEO / Decision）之上的「决策内容结构」层——解决「决策界面讲什么语言」。Status: **Frozen**（2026-08-15 DP-CEO-1 FINAL REVIEW APPROVED 回写）。

**冻结 10 项**：

1. **Decision Packet 8 要素语义**：每次 Needs CEO 必须语义覆盖 —— ①发生了什么 ②为何 AI 不能自决 ③可选方案 ④每方案影响/风险/代价 ⑤Employee 推荐 ⑥推荐理由 ⑦CEO 只需做的选择 ⑧选择后 AI 如何自动继续。
2. **8 要素 ≠ 固定 8 块 UI**：8 要素是 Decision Packet 的必备语义，**不等于** UI 固定展示 8 张卡 / 8 个标题。UI 须按复杂度压缩表达（**Low Surface Complexity, High Functional Density**）；Layer 1 优先自然紧凑组合 8 要素。
3. **三层信息层级**：Layer 0 Decision Banner（注意力 + 复杂度感知动作）/ Layer 1 Plain Decision Package（8 要素紧凑组合，CEO 语言）/ Layer 2 Professional Evidence（P6 Result Reference 按需）。CEO 默认只接触 Layer 0 + Layer 1。
4. **Complexity-aware Decision Actions**：简单·低歧义·影响明确 → Banner 直接 `[按建议处理] [其他方案] [暂缓]`；有业务取舍 / 高风险 / 不可逆 → Banner 只 `[查看方案] [暂缓]`。
5. **高风险 / 不可逆禁止 Layer 0 直接批准**：不可逆对外变更、涉及资金 / 合规的 Decision，禁止仅凭 Layer 0 一句话批准；必须进 Layer 1 看清方案 / 影响 / 推荐后才执行具体 Choice。
6. **Provenance（来源可追溯）**：Impact / Risk、Cost / Recommendation / Recommendation Reason 必须带来源标记 —— `FACT`（已验证事实）/ `POLICY`（平台·公司规则）/ `EVIDENCE`（具体可查，指向 Layer 2）/ `EST`（Employee Estimate，须明示为员工判断、非事实）/ `UNK`（尚未验证）。
7. **禁止编造**：不得为「让决策看起来完整」编造时间 / 成本 / 风险概率 / 业务影响 / 流量变化；不知道显式 `(UNK) 尚未验证`，`(EST)` 不得伪装成 FACT。
8. **CEO Decision 后 AI 自动继续**：决策后 AI 按要素 8 自动恢复（P4 Automation）；Decision 不产生新对话、不新建 Handoff。
9. **CEO Decision ≠ Handoff**：重申 §3.12 —— 升级 CEO 是 Decision Gate，责任未转移，AI 自动继续原责任流。
10. **Professional Evidence 通过 Result Reference / Utility 按需查看**：技术脚本 / Diff / Test / Logs 只进 Layer 2（P6 + RD Utility），不要求 CEO 默认阅读。

**跨 Workspace 通用**：RD（数据迁移·不可逆类）、XHS（合规审核·简单类）、抖音（投放预算）、会议（方向确认）复用同一结构与 Provenance 规则，仅领域内容不同。

**不修改**：§3.3 定义、§3.12 边界、P4 / P6 内容；本 Pattern 只在其上补充「内容结构 + 分层证据 + Provenance」。

---

### 3.14 Employee Detail（Shared · Utility · 2026-08-16 回写 · Delta-S2）

**定义**：回答「**这个员工是谁 / 组织关系 / 岗位 / 能力 / 长期责任 / 当前 Responsibility / 工作方式 / 最近结果**」的共享视图。位于 **Utility Pane**，由**点击员工头像 / 姓名**触发（与 §3.1 Employee Row 一致；**不设独立「详情」按钮**）；**不含 Conversation**（Conversation 只属 Main Workstation）。

**与 Employee Presence（§3.8）/ Employee Workstation（§3.1）构成三概念统一（Frozen）**：

| 概念 | 回答的问题 | 所在 Pane | 含 Conversation |
|---|---|---|---|
| **Employee Presence**（P2 · §3.8） | 谁在这里工作 / 谁当前负责（**员工入口**） | 贴在业务对象上，持续可感知 | 否（仅「▸ 工作过程」入口） |
| **Employee Workstation**（§3.1） | 这个员工现在怎么和 CEO 一起工作 | **Main**（进入具体员工时） | **是** |
| **Employee Detail**（本条目） | 这个员工是谁 / 组织关系 / 负责什么 | **Utility**（点击头像/姓名时） | 否 |

**内容字段（引用既有 Shared Employee Authority / T5，不重复定义）**：个人信息 · Organization-Department-Team-Leader 关系 · 长期责任 · 当前 Responsibility · 能力 / 工作方式 · 最近结果。语义来源：`Curis_Company_OS_Shared_Authority.md` §1.2（已冻结）+ `Curis_Shared_Employee_Service_Relation_Contract_Candidate.md`（Design Record）。

**铁律**：Utility 里的 Employee 视图**永远只是 Detail**，绝不承载 Conversation；Conversation 一旦出现，必属 Main 的 Workstation。

> 本条目为 Layer 3 Shared Pattern（**非 P 编号，P1–P7 语义不动**）；经 2026-08-16 Shared Employee Workstation Pattern Closure 批准回写（Delta-S2）。

---

## 4. Pattern 采用矩阵（Available Capability，非 Required）

> **图例**：✅ = 典型采用　⚪ = 可选采用（按需）　— = 通常不采用
> **原则**：Shared Pattern 是 Available Capability，由各 Workspace 按需采用，非所有 Workspace Required。尤其 **Composer / Employee Workstation** 不要求所有 Workspace 必备。<br>**编目 ≠ 可省略（2026-08-17 Stale-Rule Cleanup）**：本矩阵为 Shared Pattern **编目**（记录各 Workspace 类型使用了哪些共享能力），<strong>不授予 Business Workspace 省略 Shared Work Area 的自由</strong>——对长期 Business Workspace + 真实 AI Operating Team，Shared Work Area 是 Main 的统一组成部分（见上方工作区编排约定）。

| Pattern | 研发 | 小红书 | 抖音 | 会议 | 说明 |
|---------|:----:|:------:|:----:|:----:|------|
| Employee Workstation | ✅ | ⚪ | ⚪ | ⚪ | 呈现员工的可用模式；非所有 Workspace 必须展示员工 |
| Handoff Event | ✅ | ⚪ | ⚪ | ⚪ | 责任交接通用，按需采用 |
| Needs CEO / Decision | ✅ | ✅ | ✅ | ✅ | 决策通用，内容因域而异 |
| Result Reference | ✅(Diff) | ✅(数据) | ✅(视频) | ✅(纪要) | 引用内容因域而异 |
| Composer | ✅ | ⚪ | ⚪ | ⚪ | 指令输入，按需采用 |
| Context Surface | 文件树 | 选题库（信号 / 素材） | 脚本库 | 议程 | 内容由 Instance 声明 |
| Utility Surface | Diff/Source | 图文预览 / 数据看板 / 审核 | 视频预览 | 纪要预览 | 模式完全由 Instance 声明 |
| Employee Presence（P2） | ⚪ | ✅（创作/审核 Presence） | ⚪ | ⚪ | 业务对象上的轻量责任存在，持续可感知；按需 |
| System Activity（P3） | ⚪ | ✅（发布后自动 Analytics） | ⚪ | ⚪ | 非员工 Runtime；Current Executor=none 时启用，≠ Employee Presence |
| CEO Decision Package（P7） | ✅ | ✅ | ✅ | ✅ | 决策内容结构（8要素语义+分层+Provenance）；随 Needs CEO 采用，内容因域而异 |
| Employee Detail（§3.14） | ⚪ | ⚪ | ⚪ | ⚪ | 点击员工**头像/姓名** → Utility 共享视图（六字段，不含 Conversation）；内容引用 Shared Employee Authority / T5 |

> **2026-08-15 XHS Research Review 补注（Delta-X2 采纳）**：小红书（XHS）于本日 Review 正式补为**第二个 Context / Utility 实例示例**，与 RD 并列，证明 Adaptive Surface 的 Context/Utility 不为研发所独占——任何 Workspace 均按自身语义声明内容（XHS = 选题库（信号/素材）/ 图文预览·数据看板·审核）。X1 / X3 / X4 经裁决不采纳，Contract 其余不变。

**关键原则**：Pattern 是"能力"，不是"布局"。同一 Pattern 在不同 Workspace 的呈现位置、密度、伴随组件均可不同。

---

## 5. 与现有文档关系（避免平行/冲突）

| 文档 | 层级 | 关系 |
|------|------|------|
| `_system/tokens.css` | Layer 0 | 令牌唯一真源，本规范只引用 |
| `Curis_Design_System_Delta_RD_Workspace.md` | Layer 3–4 (RD 实例) | 本规范泛化其 Pattern 定义；RD 实例细节在 B 阶段回归此文档 |
| `Curis_Workspace_Shell.md` | Layer 4 (运营槽位) | 其"5 槽位"是 Main 的一种变体（运营驱动型），与本规范 Layer 1–3 不冲突 |
| `Curis_UI_Frozen_Spec_2026-08-04.md` | Layer 0–3 组件 | 基础组件库，本规范 Pattern 复用其基类 |

本规范**不修改**上述任何文件，仅在其上建立更高层 Contract + Pattern 抽象。

---

## 6. 待 B 阶段确认（Open Questions，提升自 Delta §Open Questions）

> 以下问题中，#2、#3 已由 A 阶段审查修正解决（见对应边界修正），#4 模式数量已由修正 4 解决。

1. Workstation 展开是否互斥（单开）还是自由（多开）？
2. ~~`needs_ceo` 员工卡默认展开还是折叠 + 顶部注意力项？~~ **已解决（修正 2）**：`needs_ceo` 不固定折叠，且与 Workspace 级 Needs CEO / Decision Pattern 分离；Decision 可在顶部，员工保留责任状态。
3. ~~Context Surface 展开用 overlay 还是 push 主区？（需全产品一致）~~ **已解决（修正 3）**：Shell 只统一交互契约；overlay / push 由窗口与场景自适应，不强制全产品一致。
4. 角色色映射是否满足色盲可达性？是否需要非颜色指示（图标/纹理）？
5. Diff 引用显示文件数+行数，还是单文件引用？
6. Utility Surface 的 `--ui-syntax-*` 子令牌具体档位？（B 阶段 RD 定稿；模式数量已由修正 4 解决：Shell 不固定模式数）
7. **Shell Navigation Detail Pending（导航细节待定，不冻结）**：业务空间子项（如 XHS「AI 科技」Workspace）在 Primary Nav 中的具体渲染方式（缩进层级 / 图标 / active 态 / 是否显示 owner 头像等）**暂不冻结为 Shell 导航规则**。当前各 Workspace 实例（RD / XHS）在 nav 中的 child 呈现仅为示例，待更多 Workspace 实例验证后再定稿导航细节规范。本项与 §0.1 边界修正 2 一致：Main 布局由 Instance 决定，导航子项细节同样留待收敛。

---

## 7. Delta 回写记录（Delta-X5 已于 2026-08-15 批准并回写 §1.2 / §2.2 / §2.3 / §2.4）

> 以下 Delta 经 XHS Interaction Exploration（Round 2）提出，原登记为待回写 Candidate；**已于 2026-08-15 经 Review 批准并正式回写**至 §1.2（默认宽度说明）、§2.2 / §2.3（Resizable 行）、§2.4（Resizable 共同规则）。保留原文作追溯。

### Delta-X5: Resizable Adaptive Surface（Context / Utility 可拖拽调宽）

**问题**：§1.2 / §2.2 / §2.3 当前将 `--ctx-w` / `--util-w` 表述为"建议 260px / 360px（B 阶段 RD 实例定稿）"，易被误读为固定宽度档位，且未声明用户可调。

**决议（用户 2026-08-15）**：
1. Context Surface 与 Utility Surface 均为 **Resizable Adaptive Surface**；
2. `260px` / `360px` 仅是**当前建议默认展开宽度**，不是固定宽度；
3. 用户可**直接拖动边界**调整展开宽度（**不增加**显式放大/缩小按钮）；
4. **记忆用户上次宽度**（per Workspace 持久化）；
5. 设 **min / max** 边界，以及 **Main minimum usable width**（主区低于该值不再压缩，转 Overlay / Focus）；
6. **空间不足时自适应**：窗口窄 / 主区过小时，Adaptive Surface 自动转为 Overlay 或 Focus 模式，不强行并排挤压主区。

**回写落点（待批准）**：
- §2.2 / §2.3 增加 "Resizable" 说明与 min/max/记忆宽度规则；
- §1.2 的 `--ctx-w` / `--util-w` 改为"建议默认，可拖拽覆盖"；
- 新增一条 Adaptive Surface 共同规则：无显式 zoom 按钮，拖拽即调，记忆上次宽度。

---

### Delta-X6: Employee Presence（业务对象上的轻量员工责任存在 · Pending Candidate）

> **状态：APPROVED FOR FREEZE — 已回写为 §3.8 Employee Presence（P2）+ §4 矩阵行（2026-08-15 Final Review 批准）。** 由 XHS Visual Round 3 暴露的产品模型修正提出（2026-08-15）：原「Employee Workstation 节点浮现非常驻」弱于真实需求，修正为 **Employee Presence 持续可感知 + Workstation / Conversation 按需展开**。

**定义**：业务对象上的轻量员工责任存在，包含：
- **Identity**：员工身份（名 / 头像）
- **Role**：角色（如 内容创作 / 内容审核）
- **Current Responsibility**：当前责任项（正在负责的这篇 Note）
- **Current Activity**：当前活动（如「正在为你制作：封面生成中…」）
- **Status**：责任状态（制作中 / 审核中 / 已发布 / needs_ceo 等，复用 §3.1 状态语义）
- **可选 Handoff Origin**：来源交接（⇄ 从 策划·李翔 交接至 内容创作·陈真）
- **Open Workstation 入口**：提供「▸ 工作过程」等入口，按需展开完整 Employee Workstation / Conversation

**关键区分（Employee Presence ≠ Employee Workstation）**：
- **Presence 持续可感知**：贴在业务对象上（如 Note 卡片头像、Split Working 顶部 Presence 条），无需展开即知「谁在负责 / 在做什么 / 状态」。
- **Workstation / Conversation 按需展开**：完整工作单元（对话流 + Composer + 责任明细）仅在用户主动查看过程 / 指导 / 处理阻塞时展开，不做成常驻员工列表，也不完全隐藏。

**复用（按需）**：研发（任务卡头像 + PR 负责人 Presence）、小红书（Note 卡作者头像 + 创作/审核 Presence）、会议（议题负责人 Presence）均通用；Workspace 声明在哪些业务对象上呈现 Presence、呈现哪些字段。

**回写落点（已回写 2026-08-15）**：
- §3 新增 §3.8 Employee Presence（定义 + Anatomy + 与 §3.1 区分）；
- §4 矩阵增加 Employee Presence 行（研发 ⚪ / 小红书 ✅ / 抖音 ⚪ / 会议 ⚪）；
- 不修改 Frozen tokens.css（Presence 复用现有 `--ui-*` 与 §3.1 状态色）。

---

### Delta-X7: Top-aligned Independent Pane Shell（取代 Global Topbar 横跨结构 · Pending Candidate）

> **状态：APPROVED FOR FREEZE — 已回写为 §1.1 / §1.2 / §1.5（S1 Top-aligned Independent Pane + S2 Pane-local Header + S3 T1/T2/T3 + S5 对象搜索 + S6 Utility Maximize + S7 Toggle 行为契约）（2026-08-15 Final Review 批准）。** 由 XHS Visual v4（2026-08-15）提出并首次实例化。已取代旧 Global Topbar 横跨结构。

**问题**：§1.1 / §1.2 当前采用 **Global Topbar（52px）横跨整个 App** + 下方 `Nav(220) + Main + Context/Utility` 的"顶栏 + 侧栏"模型。其问题：
1. 顶部横条同时承载全局定位 + 状态 + 主题 + 搜索 + 用户，与 Workspace 级信息混在一起，职责不清；
2. Main 的 Workspace Header 概念被吞，边界模糊；
3. Context / Utility 以"插入列"展开时会把整行向下推，**挤压 Main Header**。

**决议（用户 2026-08-15）**：撤销 Global Topbar 横跨结构，改为 **Top-aligned Independent Pane**：
1. **Navigation / Context / Main / Utility 彼此独立 Pane**；
2. **所有已打开 Pane 从窗口顶部开始并顶部齐平**；
3. **每个 Pane 拥有自己的 Pane Header + Pane Content**；
4. **Main 的 Workspace Header 只能属于 Main Pane，不横跨 Context / Utility**；
5. **Context / Utility 打开后不挤压 Main Header**（每 Pane 是独立列，列内各自 Header 在列顶，互不嵌套，结构上不可能挤压）；
6. **Context / Utility 仍为 Resizable Adaptive Surface**（继承 Delta-X5）。

**三个 Toggle 位置固定（跨 Workspace 一致，各 Workspace 不得自创）**：
- **T1 Navigation Toggle** → Navigation Pane Header 右侧（控制折叠/展开，即使折叠为细轨也保留展开入口）；
- **T2 Context Toggle** → Main Pane Header 左侧（Main 永远存在，Context 是 Main 左邻）；
- **T3 Utility Toggle** → Main Pane Header 右侧（Main 永远存在，Utility 是 Main 右邻）。

**能力归属**：全局动作（搜索 / 主题 / 账户）归属 Navigation Pane；Breadcrumb 归属 Main Pane Header；Pane 内对象动作由 Workspace Instance 决定；四 Pane 结构 / 顶部齐平 / 各自 Header / T1–T3 位置 / Resizable 机制 = **Shell 固定**。

**回写落点（已回写 2026-08-15）**：
- §1.1 空间职责表：删除"Topbar（全局定位+状态+主题+搜索+用户 52px）"一行，改为 Navigation/Context/Main/Utility 各自 Pane Header 职责；
- §1.2 网格：删除全局 Topbar 行与"插入列"模型，改为四独立 Pane 列（Nav 固定 / Context·Utility Adaptive / Main 弹性）；
- 新增 §1.5（Pane Header 定义 + T1/T2/T3 位置 + Toggle 行为契约 + 对象搜索 + Utility Maximize）；
- 同步更新 §3/§4 中"Main Header 横跨"相关措辞为"Main Header 仅属 Main Pane"。

---

### Delta-X8: Shared Employee Workstation Pattern（Conversation-first 全局统一 · 2026-08-16 回写）

> **状态：APPROVED — 已回写（经 2026-08-16 Shared Employee Workstation Pattern Closure Review 批准）**。由该 Closure 提出，本 Contract 落实为 Layer 3 最小补强；**不创建 P8，不修改 P1–P7 既有语义**。

**问题**：现有 Contract 已定义 Employee Workstation（§3.1）与 Employee Presence（P2 · §3.8），但（1）「进入任意具体员工 → Main 统一 Conversation-first」的全局约束未单条显式；（2）**Employee Detail（Utility）不在本 Contract**，只活于 Content Growth T5 Candidate；（3）「Conversation 不得越界」未升为 Shared 显式禁止。

**决议（用户 2026-08-16）**：
1. **Delta-S1（§0.1 边界修正 2 澄清 + §3.1 Global Shared Rule）**：CEO 进入任意具体 AI Employee 后，Main 统一 Conversation-first Employee Workstation；Workspace 默认 Main 可保持 Domain-specific 专业业务界面，但任何存在 AI Employee 的 Workspace 都必须支持进入该 Employee 的 Shared Workstation。
2. **Delta-S2（新增 §3.14 Employee Detail · Shared · Utility）**：正式收编 Employee Detail 为 Shared Utility Pattern，引用 `Curis_Company_OS_Shared_Authority.md` §1.2 + T5，不重复定义；与 P2(Presence) / §3.1(Workstation) 构成三概念统一。
3. **Delta-S3（§3.12 边界澄清新增两行）**：Employee Workstation / Conversation 禁止进入 Context Pane；禁止进入 Employee Detail / Utility Pane。
4. Result / Artifact 在 Conversation 中使用轻量引用（P6），点击后进入 Utility 专业预览（已有，重申）。

**回写落点（已回写 2026-08-16）**：
- §0.1 边界修正 2：新增 Clarification blockquote（Delta-S1）；
- §3.1：新增 Global Shared Rule note（Delta-S1）；
- 新增 §3.14 Employee Detail（Shared · Utility，Delta-S2）；
- §3.12：边界澄清表新增两行（Delta-S3）；
- §4 Pattern 采用矩阵：新增 Employee Detail（§3.14）行；
- Status 头 + 本 Delta 记录同步。

---

### Delta-X9: Shared Main Composition（Main = Domain Business Surface + 工作区 · 2026-08-17 回写）

> **状态：APPROVED — 已回写（经 2026-08-17 Shared Main Composition Closure 批准）**。由该 Closure 提出，本 Contract 落实为 Layer 1–3 最小补强；**不创建 P8，不修改 P1–P7 既有语义，不重定义 Employee Workstation**。

**决议（用户 2026-08-17）**：
1. **Main 组合规则**：含 AI Employee 的长期 Business Workspace，Main = Domain Business Surface（业务展示区，内部架构名，非强制 UI 标题）+ Shared Work Area（工作区）；Employee Workstation belongs to 工作区 ≠ 整个 Main。无 AI Employee 的 Workspace 其 Main 可仅含业务展示区（与 §0.1 Workstation = Available Capability 非 Required 一致）。
2. **Domain Business Surface 职责（Shared 仅规定职责）**：让 CEO 在 Context / Utility 全部关闭时也能理解"这个业务现在整体怎么样"；目标/状态/关键对象/进度/结果/Blocker/Needs CEO 仅为候选维度，具体展示哪些、字段与视觉形式全部由 Domain 决定。
3. **工作区（Shared 统一名"工作区"）**：复用 Frozen Conversation-first Employee Workstation；Domain 只决定员工组成/当前·完成·等待/顺序·并行/Responsibility/Tool/Result 类型/折叠-展开编排。
4. **四栏**：Nav + Main 默认基础桌面；Context + Utility = Adaptive On-demand 默认收起；新增"Main must stand on its own"——Context/Utility 全关时 CEO 仍能理解业务整体状态并完成主要工作；Context 不得承载关闭后导致 Main 无法理解业务的核心信息。
5. **S1 歧义澄清**：将易误读的"Employee Workstation = Main"精确为"Employee Workstation ∈ Main.WorkArea"；Main = Domain Business Surface + Shared Work Area。不创建 P8、不改 P1–P7、不重定义 Employee Workstation。
6. **工作区编排不与 Runtime 绑定**：工作区 = Employee Workstation List；每 Employee 固定轻量展示（头像+姓名+岗位+当前职责+当前状态+展开/收起），展开统一显示 Frozen Conversation-first Workstation；Runtime 状态 ≠ UI 折叠状态；CEO 自由展开/收起，收起不暂停员工真实工作；唯一默认展开行为 = 从 Workspace 外部进入且存在单一 working Employee 时该 Employee 默认展开；多 Employee 并行默认展开策略本轮不额外定义。

**回写落点（已回写 2026-08-17）**：
- §0.1 边界修正 1：新增"Main must stand on its own"原则；
- §0.1 边界修正 2 Clarification：追加 Main 组合补强 blockquote（业务展示区内部架构名 / Employee Workstation ∈ 工作区 ≠ 整个 Main）；
- §1.1 空间职责表 Main 行：注明 Main = Domain Business Surface + 工作区（业务展示区非强制 UI 标题）；
- §2.1：引用 §0.1 的 Main 自成立原则；
- §3.1 Global Shared Rule：追加 Main 组合澄清（Workstation ∈ Main.WorkArea）；
- §3.1：新增"工作区编排约定"（工作区 = Employee Workstation List + 轻量展示 + 展开 Workstation + Runtime 状态 ≠ UI 折叠 + 唯一默认展开行为）；
- §3.1 States 表："默认态"标注为建议呈现、非状态绑定；
- Status 头 + 本 Delta 记录同步。

### Delta-X10: Shared Employee Work Area + Composer（Employee Row / UI Status 投影 / Conversation Surface / Shared Composer Shell · 2026-08-17 回写）

> **状态：APPROVED — 已回写（经 2026-08-17 Shared Employee Work Area + Composer Contract Closure 批准，修正 3 点）**。由该 Closure 提出，本 Contract 落实为最小补强；**不创建新 P Pattern，不修改 §3.1 现有 Runtime State Schema（`working`/`waiting`/`needs_ceo`/`completed`/`failed`/`idle` 一律不删不改不迁移），不新增 Runtime Primitive（含 `blocked`/`offline`/`unavailable`）**。

**决议（用户 2026-08-17，含 3 点修正）**：
1. **Employee Row 两行结构**：普通列表行（不做 Card）= 头像（跨两行）+ 行1 姓名+岗位 + 行2 当前职责 + 当前状态（UI Projection）+ 展开/收起；点击头像/姓名 → Utility Employee Detail，**不设独立「详情」按钮**。与 Delta-X9「工作区编排约定」一致。
2. **Shared Employee UI Status = Runtime Truth 的用户侧投影（非 Schema）**：固定三态 `空闲` / `工作中·<实时描述>` / `阻塞·<原因>`；投影必须来自真实 Runtime/Responsibility 事实；`阻塞` 仅当真实事实证实时投影，不因此新增 Runtime Primitive；禁止把 已完成/待审核/已验收/待命 当员工 UI Status；**现有 Runtime State Schema 不动**；Runtime State 模型清理留给后续独立技术/Authority 审计。
3. **Conversation Surface Shared Rules**：居中 / Bounded·Responsive（min/preferred/max readable width，不写死 px）/ 默认舒适高度 / 用户可拖拽调整高度 / 展开收起只改 UI 不改 Runtime；对话 = 自然消息流 + 真实过程轻量状态行 + Result/Artifact 轻量引用 + Composer，不做 Card / 不做 AI 状态 Dashboard。
4. **Shared Composer Shell**：固定**语义槽位**（Input / `+` Add（语义冻结、文案不冻结）/ 访问权限▾ / 工作模式▾ / 已选功能资源 / 执行选择 Model·Agent▾ / Voice 可选 / Send）+ Provider Adaptation（Shared 固定槽位+显性区分 Model·Agent，Provider 决定权限/模式/能否切模型/Agent 原生设置，不写死具体 Provider）；**布局仅 Desktop 推荐（输入区在上、底部左右分组），不 Frozen 为所有尺寸/平台固定排列**，响应式/mobile 可重排。
5. **§3.14 Employee Detail 触发器**：由「详情/是谁 按钮」改为「点击头像/姓名」（与 §3.1 Row 一致）。

**回写落点（已回写 2026-08-17）**：
- §3.1 Anatomy：精化为两行 Row（头像跨两行 + 行1 姓名岗位 + 行2 职责 + 状态 + 展开箭头）+ 交互（点头像/姓名 → Utility，无详情按钮）+ Body 引用 Conversation Surface / Shared Composer Shell；
- §3.1：新增「Shared Employee UI Status = Runtime Truth 的用户侧投影」blockquote（三态 + 投影纪律 + 不动 Runtime State Schema + 不新增 Primitive）+ 新增「Conversation Surface Shared Rules」blockquote；
- §3.1 工作区编排约定：每 Employee 行结构对齐两行 + 点头像/姓名 → Utility；
- §3.5 Composer：由极简骨架升级为 Shared Composer Shell（语义槽位 + Provider Adaptation + Model/Agent 适配 + 布局仅 Desktop 推荐）；
- §3.14 Employee Detail：触发器改为点击头像/姓名；
- §3.14 三概念表 / §4 Pattern 采用矩阵：同步「点击头像/姓名」；
- Status 头 + 本 Delta 记录 + 规范日期同步。

### Delta-X12: Shared Conversation Content Block（长内容块 · 2026-08-17 回写）

> **状态：APPROVED — 已回写（用户 2026-08-17 设计权威收敛轮，作为最后一条 Shared Conversation Delta）**。由本轮「DESIGN AUTHORITY RECONCILIATION」提出，本 Contract 落实为最小补强；**不创建新 P Pattern，不修改 Runtime State Schema，不新增 Runtime Primitive，不 Frozen 具体 px / 字数 / 视觉样式**。

**决议（用户 2026-08-17）**：
1. **Conversation 不 Card 化**：对话表面本身不做 Card 包裹。
2. **普通短消息自然流**：短消息走自然消息流，不强制结构化。
3. **长内容用 bounded embedded content block**：当且仅当出现 长文本 / Tool / Terminal / Code / Diff / Structured Result 时，允许有界内嵌内容块承载。
4. **长块内部滚动**：长内容块内部可滚动，避免单次输出无限撑高多人共享工作区。
5. **可进 Utility 完整查看**：点击块内「完整查看」或来源引用 → Utility 专业视图看全文（Utility 不受有界限制）。
6. **不 Frozen px / 字数 / 样式**：块的有界尺寸、字数/行数阈值与具体视觉样式不 Frozen，由实现按内容类型与可用宽度自适应。

**回写落点（已回写 2026-08-17）**：
- §3.1：新增「Conversation Content Block（长内容块）Shared Rule」blockquote（接在 Conversation Surface Shared Rules 之后）；
- Status 头追加 Delta-X12；
- 规范日期同步（见文末）。

---

**UI Designer**: UI Designer
**规范日期**: 2026-08-15（2026-08-16 追加 Delta-X8 回写；2026-08-17 追加 Delta-X9 回写；2026-08-17 追加 Delta-X10 回写；2026-08-17 追加 Delta-X12 回写）
**阶段**: A（Shell Contract + Adaptive Surface + Shared Patterns）— **S1–S7 + P1–P7 已 Frozen（APPROVED FOR FREEZE）** + **Shared Employee Workstation Pattern（Delta-S1/S2/S3）2026-08-16 回写**；B 阶段 RD Instance 固化与抖音 Instance 待后续轮次（未启动，不属本轮范围）
