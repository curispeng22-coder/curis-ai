# Curis RD Workspace — UI Drift Audit v1

**状态**：RD DESIGN REVIEW RECORD · Reference Only
**阶段**：RD Workspace 正式设计重构 · A 阶段（Authority / Drift Audit + Pane Header 固定 + Delta Proposal）
**日期**：2026-08-15
**UI Designer**：UiDesigner

**权威真源（本次只读，不修改）**：
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` — **Frozen**（S1–S7 + P1–P6）
- `Curis_XHS_Workspace_UI_Authority_Map.md` — **APPROVED**（Shell / Shared 边界）
- `Curis_RD_Workspace_Instance_Spec_v1.md` — **APPROVED CANDIDATE**（Layer 4 输入）
- `Curis_RD_Workspace_Design_Brief.md` / `Curis_RD_Workspace_Reference_Synthesis.md` — 研发语义与视觉母版描述
- `Curis_Design_System_Delta_RD_Workspace.md` — RD 视觉基线 v1（Figma 描述）
- `Curis_Design_System.md` / `_system/tokens.css` — **Frozen**

**关键事实**：
- RD 原 Figma 4 张 Visual Baseline 截图**不在本机**（Instance Spec 标注其为输入，但本地无 PNG）。本次以 `Curis_Design_System_Delta_RD_Workspace.md` + Design Brief + Reference Synthesis 作为「视觉母版描述」来源。
- **RD 原 Figma / RD Delta / RD Instance Spec §1.1 仍采用「Global Topbar（52px）横跨 + 220 Nav + Main」旧模型**。该模型已被 Frozen Shell 的 **Top-aligned Independent Pane** 取代（Delta-X7）。
- **冲突裁定（用户规则）**：旧 Figma Shell 与 Frozen Shell 冲突时，**以当前 Frozen Shell 为准**。因此旧 Topbar 模型整体 REINTERPRET 为四独立 Pane。

---

## A. Drift Audit（旧 Figma / RD Delta / RD Instance Spec → Frozen Pane Shell）

> 判定词：**KEEP**（保留旧方案，已符合 Frozen）/ **MIGRATE**（旧有但需按 Frozen 迁移位置或机制）/ **REMOVE**（旧模型被 Frozen 明确废除）/ **REINTERPRET**（语义保留但需换壳重构）。

### 1. 旧 Global Topbar / Header 层级
- **旧**：52px Global Topbar 横跨全 App（含全局定位+状态+主题+搜索+用户），下方 Nav(220)+Main；Context「从 topbar 控件」开合。
- **Frozen**：无 Global Topbar。Navigation / Context / Main / Utility 四独立 Pane，各自顶部齐平、各有 Pane Header；Main Header 只属 Main。
- **判定**：**REMOVE + REINTERPRET**。废除 Global Topbar；原「topbar 控件」拆为 Nav Header（🔍 + T1）、Main Header（T2/T3/Breadcrumb/More）、Context/Utility 各自 Header。Workspace 标题/状态条移入 Main Pane 内容区（非全局顶栏）。
- **RD Instance Spec §1.1 现状**：仍画 `┌ Topbar（52px · 全局固定）──┐` + `Primary Nav（220px）│ Main`。**属 Drift，见 §F.3 Delta Proposal**。

### 2. Navigation / Context / Main / Utility 是否符合 Top-aligned Independent Pane
- **旧**：Nav 固定 220 + Main 弹性；Context/Utility 按需，但表述为「topbar 控件开」、位置含糊（overlay 倾向）。
- **Frozen**：4 列独立网格，均从窗口顶开始、顶部齐平；Nav 可 `width:0` 完全收起；Context 在 Main 左、Utility 在 Main 右。
- **判定**：**REINTERPRET**。采用 4 列网格（`nav | ctx | main | util`）。Nav 是独立 Pane（非顶栏一部分）；Context 与 Utility 是 Main 左右的独立列，不再是「悬浮于 topbar」的抽象控件。

### 3. T1 / T2 / T3 位置
- **旧 Figma**：仅一个含糊的「topbar 控件」开 Context；无显式 T1（Nav 折叠）/ T3（Utility）。
- **Frozen**：T1=Nav Header 右（折叠后转 Main Header 最左）/ T2=Main Header 左（常驻）/ T3=Main Header 右（展开后转 Utility Header 右）；禁止独立 ✕。
- **判定**：**MIGRATE**。严格采用 Frozen T1/T2/T3 位置；三 Workspace（RD/XHS/未来）完全一致，RD 不另创。

### 4. Context / Utility Resizable
- **旧**：未声明可拖拽调宽（固定或 overlay）。
- **Frozen（Delta-X5）**：Resizable Adaptive Surface，默认 260/360px 仅为建议值；可拖边界覆盖、记忆宽度、min/max、空间不足转 Overlay；无放大/缩小按钮。
- **判定**：**MIGRATE**。Context/Utility 实现为可拖拽调宽列，遵循 Delta-X5 全部规则。

### 5. Utility Maximize
- **旧 Figma**：无 maximize 概念。
- **Frozen（S6）**：Utility Header 含 ↗ 最大化，点击后全屏 Overlay 覆盖整页（含 Main），✕ / Esc / 点遮罩退出。
- **判定**：**MIGRATE**。Utility Header 增加 ↗ Maximize（RD Diff/Source/Preview 适用）。

### 6. Company-wide Object Search
- **旧 Figma**：隐含于全局 Topbar 的大搜索框。
- **Frozen（S5）**：Nav Pane Header 轻量 🔍 icon → 独立 Search Surface；语义 = Company-wide Object Search（Object-first, Task-capable）；无常驻大搜索框。
- **判定**：**MIGRATE**。搜索入口落在 Nav Pane Header（🔍），展开 Search Surface；删除任何常驻大搜索框。RD 搜索覆盖 Business/Workspace/Employee/Code Object/Result/Meeting/Decision/Capability 等公司级对象。

### 7. Employee Presence / Workstation 关系
- **旧 Figma / RD Delta**：Workstation 即存在层，无独立 Presence 组件。
- **Frozen**：P2 Employee Presence（业务对象上轻量责任存在）+ P1 Workstation 为两个**不同** Pattern。
- **判定**：**REINTERPRET（RD 专属，见 §D）**。RD 以 Workstation 为主存在层；当 Workstation 已展开时，Presence 融入 Workstation Header（不新增独立 Presence 卡）。仅在「对象级轻量责任」场景（如 PR 负责人 chip、任务卡头像）使用 Presence 内联。禁止把 Presence 做成常驻员工列表 / Sidebar 目录。

### 8. Handoff Event
- **旧 Figma / RD Delta**：对话流内 Handoff 呈现。
- **Frozen（P5）**：轻量形态（来源→摘要→接收→时间），可展开详情；不与 DAG 等同。
- **判定**：**KEEP**。RD Handoff 默认轻量行（禁止大卡），与 Frozen §3.2 一致；详情展开后才是 Context Package/Acceptance/Questions/Expected/Escalation。
- **本轮回写新增区分（见 §G.2）**：Frozen Handoff = **Current Responsibility 真正转移**；RD 中「陈真把代码结果送李翔 Review、但陈真仍负实现责任」**不是** Frozen Handoff，定义为 **RD Instance Candidate — Artifact Review Request / Review Handoff**（责任不转移）。原 HF 示例「陈真→李翔·代码审核交接」已归为后者并重新标注。不修改 Frozen §3.2 定义。

### 9. Needs CEO / Decision Gate
- **旧 Figma**：Needs CEO 仅作 Workstation `needs_ceo` 状态。
- **Frozen（P3 §3.3）**：Workspace 级 **Decision Banner**（顶部，阻断性决策面），与单个员工 `needs_ceo` 状态**分离**；CEO Decision ≠ Handoff。
- **判定**：**REINTERPRET**。保留员工卡 `needs_ceo` 状态标签；**新增** Main 顶部 Decision Banner 承载真实决策交互（批准/驳回/暂缓/提供指示）。员工仍持 Current Responsibility，决策后 AI 自动继续。

### 10. Result Reference
- **旧 Figma**：`api/users.ts · 34-93 · 查看差异` 引用行。
- **Frozen（P6）**：`emoji + 文字 + ▸`，`--ui-accent` 色，点击开对应 Utility Surface；对话内不铺完整 Diff/代码。
- **判定**：**KEEP**。RD 引用格式（如 `📎 api/users.ts · 34-93 · 查看差异 ▸`）与 Frozen §3.4 完全一致。

### 11. Automation by default
- **旧 Figma / RD Delta**：自动 Handoff、自动继续。
- **Frozen（P4）**：Automation by default；Human action only at Decision Gates。
- **判定**：**KEEP**。RD 重申：员工完成自动 Handoff；CEO 只在 Decision Gate 操作；不充当「下一步」按钮。

### 12. System Activity 是否需要在 RD 出现
- **Frozen（P3 §3.9）**：非员工 Runtime（Analytics/Monitor/自动流水线），Current Executor=none 时启用；不得伪装员工。
- **RD 判定**：**OPTIONAL / RESERVED（不在 5 个 DESIGN NOW 核心状态强制出现）**。RD 未来可有后台 Build/Test（无员工）运行时 → 适用 System Activity；但 Test/Terminal/Git 等属 E 段 RESERVED，**当前 5 状态不渲染 System Activity**。当出现非员工 Runtime 时，必须显 System Activity 组件（无头像、无工作过程入口），**绝不伪装成员工**。

---

## B. 固定 RD Pane Header（严格继承 Frozen Shell，不重新发明）

> 全部位置/行为来自 Frozen §1.5。RD 不重写、不另创。以下仅为「RD 在每个 Header 里填什么」的实例声明。

### Navigation Pane Header
- **左**：Window Controls reserved area（macOS traffic lights 占位；桌面 App 原生接管）。
- **右**：🔍 Search icon（开 Search Surface）+ **T1**（Navigation Toggle，控制 Nav 完全收起/展开）。
- 收起时整列 `width:0`，Header 随之隐藏；T1 转移到 Main Header 最左（见下）。

### Main Pane Header
- 从左到右：`[T1 仅 Nav 折叠时]` · **T2（Context Toggle，常驻左）** · **Breadcrumb**（业务空间 / 研发·默认办公室）+ 当前 Responsibility/Object 定位 · `（弹性间隔）` · **T3（Utility Toggle，右）** · **More**（仅必要动作：如「新建责任」「设置」）。
- **Main Header 不横跨 Context / Utility**；只属 Main Pane 列顶。

### Context Pane Header
- **左**：当前 Context 类型 / 对象（如「上下文 · getUserData 性能优化」或「文件树」）。
- **右**：必要 Context Action（如「定位当前文件」）+ **T2**（控制本 Pane 开合；不设独立 ✕）。
- **不增加工具墙**：Context 只承载 Workspace/Responsibility/Files/Recent，不变成员工目录 / Session Manager / Git 仪表盘。

### Utility Pane Header
- **左**：当前对象 / 模式名（如「Diff · api/users.ts」）。
- **中/右**：RD 专业模式切换（**Source / Diff / Preview**）+ **↗ Maximize** + **T3**（展开后从 Main Header 转移至此；不设独立 ✕）。
- 模式数量/内容由 RD 声明，Shell 只定义容器与开合机制。

### 四 Pane 顶部齐平
所有已开 Pane 从窗口顶开始、各自列顶有 Pane Header；Context/Utility 打开为左右独立列，**结构上不可能挤压 Main Header**。

---

## D. RD 专属语义（Conversation / Presence / System Activity）

### Conversation
- **只负责解释、决策、沟通**。完整产物（Code / Diff / Source / Preview / Test Result）**不塞满 Conversation**。
- Conversation 内仅保留：**Result Reference**（轻量引用，点开 Utility）、**Handoff**（轻量行）、**简短摘要**。
- 代码引用示例：`📎 api/users.ts · 34-93 · 查看差异 ▸` → 开 Utility · Diff。

### Employee Presence
- RD 以 **Employee Workstation** 为主存在层（垂直栈，可多开）。
- **当 Workstation 已展开**：Presence 融入 Workstation Header（头像+角色+状态+当前工作），**不重复增加一条独立 Presence 卡**。
- 仅在「对象级轻量责任」处使用 Presence 内联（如 PR 负责人 chip、任务卡头像）。
- 禁止：Presence 常驻列表、Sidebar 员工目录、把 Presence 当员工队列。

### System Activity
- **仅当 Current Executor = none、Runtime / Test / Build / Background Automation 独立运行时**使用。
- 无员工头像、无「工作过程」入口；**不伪装成员工**、不造伪岗位。
- 当前 5 个 DESIGN NOW 状态不强制渲染（Test/Terminal/Git 属 RESERVED）；未来出现非员工 Runtime 时再启用。

---

## E. 当前范围

**DESIGN NOW**：
- Frozen Pane Shell 适配（四独立 Pane / T1–T3 / Resizable / Search / Maximize）
- Employee Workstation（多开、状态模型）
- Conversation + Composer
- Context（文件树/责任/相关文件/最近对象）
- Utility（Source / Diff / Preview）
- Handoff
- Needs CEO（Decision Banner）
- Result Reference
- Resizable / Maximize

**RESERVED / LATER**（不因 Codex / Cursor / WorkBuddy 有就往 RD 塞）：
- 完整 Git / PR / Worktree
- Terminal
- Debug / Problems
- Scheduled Work
- Autopilot
- Voice
- 高级 IDE 克隆（DAG / 多 utility 同屏 / Session Manager / 员工 Tab / 工具墙）

**DO NOT COPY**（来自 Design Brief §14）：员工 Top Tab、Context 内放员工、DAG 普通视图、常驻工具墙、一次展开所有能力、Session Manager 首屏、为专业感加按钮、完整 Codex/Cursor/VS Code 克隆。

---

## G. RD Responsibility Semantics（本轮回写 · Layer 4 Candidate）

> 本回合在「大方向通过」基础上，仅做 Responsibility / Handoff 语义收口，不重画结构、不新增 IDE 功能、不修改 Frozen Shell / Shared Patterns。

### G.1 多 Responsibility 共存模型

- Workspace 可同时存在**多个 Responsibility**（同一研发目标下的不同责任单元）。每个 Responsibility 独立拥有：
  - **Responsibility ID / Object**（如 `R1 · getUserData API 性能优化`）
  - **Current Responsibility**（当前责任阶段）
  - **Current Executor**（此刻执行员工，可为 none）
  - **Status**（`working` / `waiting` / `needs_ceo` / `completed` / `failed` / `idle`）
  - **Result / Evidence**
  - **Handoff history**
- **多 Employee Workstation 共存 ≠ 一个 Responsibility 多个 Current Responsibility**。多个 Workstation 并列展示多个 Responsibility 的进度；任一 Responsibility 在任一时刻只有一个 Current Responsibility。
- **示例（本 HF 已落地）**：
  - **R1 · getUserData API 性能优化** → 陈真（工程AI）· Current Responsibility：实现批量加载 · Status：`working`
  - **R2 · 用户表数据迁移审核** → 李翔（审核AI）· Current Responsibility：审核迁移脚本 · Status：`needs_ceo`（等待 CEO 执行权）
  - **R3 · 灰度发布（下一阶段）** → 王磊（运行AI）· Current Responsibility：灰度发布 · Status：`waiting`（明确等待 R1、R2 完成，非含糊「等待」）
- **Workspace Header 汇总**（与 Frozen 一致，不混淆责任）：`3 名员工 · 2 项进行中责任（R1·R2） · 1 项需要 CEO（R2）`。不同 Responsibility 不混为一个「当前责任」。

### G.2 两类交接（关键区分 · 不修改 Frozen Handoff）

| 维度 | Frozen Handoff Event（P5） | RD Instance Candidate — Artifact Review Request |
|------|---------------------------|-----------------------------------------------|
| 定义 | **Current Responsibility 真正转移**（来源完成 → 接收接管该责任） | Artifact/Result 送 Reviewer 检查，**不自动转移 Current Responsibility** |
| 触发 | 责任完成、责任链推进 | 代码/产物需他人审阅，但作者仍持责任 |
| 视觉 | Frozen §3.2 轻量行（`⇄ 来源 → 接收 · 责任交接`） | 本 HF 用虚线 `🔍 送审请求` 标记（责任未转移） |
| 升格 | 已 Frozen，跨 Workspace 通用 | **仅记 Candidate，本轮回写不直接升格 Shared Pattern** |

- **判定当前示例**：原 HF「陈真→李翔·代码审核交接」属 **Artifact Review Request（责任未转移）**，**不是 Frozen Handoff**。陈真仍持 R1 Current Responsibility，李翔仅做代码审核（不接管 R1 责任）。
- **仅当真正转移**才用 Frozen Handoff：陈真完成 R1 实现 → 李翔正式接管 R1 审核责任时，才升级为 Frozen Handoff Event。
- **纪律**：不修改 Frozen §3.2 定义；Artifact Review Request 若未来需跨 Workspace 通用，仅记为 Shared Pattern Candidate，不动 Frozen。

### G.3 Composer 中性（与 §5 一致 · 修正 HF 旧实现）

- 可见控件：`＋`（添加上下文） / **Mode**（Provider-supported execution modes） / **Model**（仅 Provider 支持切换时显示） / **Send** / **Stop**。
- **移除旧 HF 错误**：固定 `Q3` 模型名、常驻 `默认审批` 权限按钮 —— 二者均违反「模型不写死、权限按需非常驻工具墙」。
- 权限/审批属于按需能力，不在 Composer 常驻；`needs_ceo` 由 Decision Banner（§3.3）承载，不进 Composer。

### G.4 升格处理

- Artifact Review Request 仅为 **RD Instance Candidate（Layer 4）**；是否升格为 Shared Pattern 由后续 Review 决定，**本轮回写不直接升格**，不动 Frozen §3.2。

---

## F. 交付与 Delta Proposal

### F.1 交付物
1. `Curis_RD_Workspace_UI_Drift_Audit_v1.md`（本文件）
2. `Curis_RD_Workspace_High_Fidelity_v1.html`（5 状态高保真）
3. Delta Proposal（见下，仅建议，不修改 Frozen Contract）

### F.2 不修改声明
- 未修改 Product Blueprint、Frozen Shell Contract、XHS Instance、XHS Visual、正式前端代码。
- Prototype JS/CSS（本 HTML 内）标 `PROTOTYPE REFERENCE ONLY`，不进入权威 Contract。
- 所有视觉令牌仅用 Frozen `--ui-*`（含 `--ui-success`/`--ui-danger` 作 Diff 增删色）；语法高亮 `--ui-syntax-*` 待 Contrast 验证，本 mock 内不写死、不回写 `tokens.css`。

### F.3 Delta Proposal（RD Instance Spec ↔ Frozen Shell 小型一致性修正）

> 仅建议；**不改 Frozen Contract**。RD Instance Spec 为 Layer 4 候选文档，其 §1.1 图示目前与 Frozen 冲突，建议在该 Spec 后续定稿时同步修正（本 High-Fidelity 已按正确模型实现）。

**DP-1：RD Instance Spec §1.1 布局图改为四独立 Pane** — **✅ 本轮已应用**
- 现状：`┌ Topbar（52px · 全局固定）──┐` + `Primary Nav（220px）│ Main Workspace` 旧两区模型。
- 已改：替换为 Frozen §1.2 四列网格（Nav 固定列 / Context 左 Adaptive / Main 弹性 / Utility 右 Adaptive），并标注 T1（Nav Header）→ T2（Main Header 左）/ T3（Main Header 右）位置。
- 理由：Delta-X7 已 Frozen 取代 Global Topbar；RD Instance Spec 作为首个 Professional Instance 不应保留被废除的旧模型图示。

**DP-2：RD Instance Spec §1.1「Workspace Header」定位澄清** — **✅ 本轮已应用**
- 现状：Workspace Header 画在 Main 顶部、似全局。
- 已改：明确 Workspace Header（标题 `研发·默认办公室` + Meta `N名AI员工 · <责任> · <注意>` + 状态条）属于 **Main Pane Content 顶部**，非跨越 Context/Utility 的全局顶栏；四 Pane 各自 Pane Header 独立。

**DP-3：RD Instance Spec 补 T1 / Utility Maximize 声明** — **✅ 本轮已应用**
- 已改：在 §1.1 补 Navigation Pane Header（🔍 + T1）、Utility Pane Header（模式切换 + ↗ Maximize + T3），与 Frozen §1.5 对齐。

> 上述 DP 均**只动 RD Instance Spec（Layer 4 候选），不动 Frozen Shell Contract（Layer 1–3）**。本轮回写已批准并应用，同时新增 §1a RD Responsibility Model（见 G 章）。

---

**最终状态**：RD DESIGN REVIEW RECORD · Reference Only（本文件为 RD 设计重构过程审计稿，最终权威以 RD Instance Spec v1（RD INSTANCE APPROVED）为准）
