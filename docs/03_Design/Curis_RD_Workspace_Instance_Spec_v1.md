# Curis RD Workspace Instance Specification v1

**Status**: **RD INSTANCE APPROVED**
**Layer**: Layer 4 — Workspace Instance（研发专业实现）
**Current Shared Rule Supersession**: 本文件只保留 RD domain / object anatomy。所有 Shared UI 规则以 `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` 当前 Frozen 内容为准：Runtime State 不驱动展开/收起；唯一初始自动展开是“从 Workspace 外部进入且存在单一当前 working Employee”时的一次性行为，进入后完全由用户控制；Shared Employee UI Status 仅为“空闲 / 工作中·desc / 阻塞·cause”；Composer 消费 Frozen Shell 完整语义槽位。下文旧默认展开/收起、Compact Composer 与旧视觉 token 记录在冲突处均已收窄，不再构成 Current shared rule。
**输入**：
- RD Workspace Visual Baseline v1（Figma 4 图）
- `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（A 阶段 Shell Contract + Shared Patterns · **Frozen**）
- `Curis_RD_Workspace_Design_Brief.md`（Status: Review · READY FOR DESIGN REVIEW）
- `CURIS_VISUAL_STANDARD_V1.md`（Current Frozen Visual Language）；旧 `Curis_Design_System.md` / `_system/tokens.css` 仅保留未被取代的实现 provenance
- `Curis_RD_Workspace_UI_Drift_Audit_v1.md`（A 阶段 Drift Audit + 本轮回写 §G Responsibility Semantics）

**回写记录（本轮回写已应用）**：DP-1~DP-3（§1.1 旧 Global Topbar 图 → Frozen 四独立 Pane）、新增 §1a RD Responsibility Model（多责任共存 + 两类交接区分 + Composer 中性）。
**不修改**：任何代码、任何现有页面、Product Blueprint、Frozen Shell Contract / Shared Patterns（§3.2 Handoff 定义未改）、Frozen 令牌。
**不重新设计**：Figma 骨架与 Frozen Shell Contract 保持不变，本规范只把研发 Workspace **固化**为第一个 Professional Workspace Instance。

---

## 0. 定位与边界（严格三层分离）

| 层 | 来源 | 本规范中的角色 |
|----|------|---------------|
| **Shell Contract** | A 阶段文档（Layer 1–3） | 全局共享，本规范**直接引用，不重定义** |
| **Shared Pattern** | A 阶段 §3（7 个） | 可复用能力，本规范**采用**，不新造 |
| **RD Instance** | 本规范（Layer 4） | 研发专业实现：声明 Main 布局 + 填充 Adaptive Surface + 采用 Pattern |

**Current Frozen Shell 结论**：
> Employee Workstation 允许自由多开。Runtime State 与 UI 展开/收起相互独立；仅当用户从 Workspace 外部进入且存在单一当前 working Employee 时，该 Workstation 初始展开一次。进入 Workspace 后完全尊重用户布局，Runtime 状态变化不得强制改变。

---

## 1. RD Main Workspace 结构参考与当前适用性

**2026-09-15 Current boundary：** 本节旧工位栈、Compact Composer与旧首版工具范围只保留历史实例/对象解剖，不冻结当前专业Main。研发Domain Primary Surface以真实研发工作对象、Version、Build、Test、Review、Blocker为主；Employee Work Area是Shared Work Area，不是整个Workspace主视觉。完整Conversation与复杂研发工作在Main，Code/Diff/Preview等辅助阅读可Utility。Terminal/Git/Preview等目标能力消费[Company OS Shared §16](Curis_Company_OS_Shared_Authority.md)，G5-V未验；不重建RD模型，也不把旧Figma升级当前Final Visual。

### 1.1 布局（Frozen 四独立 Pane · 本轮回写 DP-1~DP-3）

> 旧「Global Topbar（52px）横跨」模型已被 Frozen Shell（Delta-X7）废除，本 § 已回写为四独立 Pane（**DP-1**）。Workspace Header 属于 **Main Pane Content 顶部**，非跨越 Context/Utility 的全局顶栏（**DP-2**）。

```
┌ Navigation Pane ─┬─ Context Pane ─┬─ Main Pane ──────────────┬─ Utility Pane ─┐
│ (Pane Header)    │ (Pane Header) │ (Pane Header)            │ (Pane Header) │
│ 🔍 Search + T1   │ 类型/对象 +T2 │ T1(折叠时) T2 Breadcrumb │ 模式+↗Max +T3 │
│                  │              │ T3 + More                │               │
│ nav items…       │ 当前责任/文件 │ ┌ Workspace Header ────┐ │ Diff/Source/  │
│                  │              │ │ 研发·默认工作空间    │ │ Preview       │
│                  │              │ │ 3员工·2责任·1需CEO   │ │               │
│                  │              │ ├ Decision Banner ───┤ │               │
│                  │              │ │ ⚠ 需CEO决策 [✓][⛔]│ │               │
│                  │              │ ├ R1 陈真 WS ───────┤ │               │
│                  │              │ ├ R2 李翔 WS ───────┤ │               │
│                  │              │ ├ R3 王磊 WS ───────┤ │               │
│                  │              │ └（垂直栈，可滚动）──┘ │               │
└──────────────────┴───────────────┴──────────────────────────┴───────────────┘
```

- **Navigation Pane Header（DP-3）**：Window Controls 预留区 + 🔍 Search + T1（Nav 完全收起/展开）。
- **Main Pane Header（Frozen §1.5）**：T1（Nav 折叠时转最左）+ T2（常驻左）+ Breadcrumb（业务空间 / 研发·默认工作空间 + 当前 Responsibility 定位）+ T3（右）+ More（仅必要动作）。**Main Header 不横跨 Context/Utility**。
- **Context Pane Header**：当前 Context 类型/对象 + 必要 Context Action + T2（不设独立 ✕）。
- **Utility Pane Header**：当前对象/模式（Source / Diff / Preview）+ ↗ Maximize（**DP-3**）+ T3。
- 四 Pane 顶部齐平；Context/Utility 为 Main 左右独立列，结构上不可能挤压 Main Header。
- **Main = 垂直栈的 Employee Workstation**，同一研发目标（Cycle / Workspace）下并列多个责任工作站（每个对应一个 Responsibility，见 §1a）。
- 不存在独立的"底部员工队列 / Footer" Shell 区域（边界修正 1）：底部员工行即 **Collapsed Employee Workstation**，属于同一栈。
- **Workspace Header**（Main Pane Content 顶部）：标题 `研发 · 默认工作空间` + Meta `3名员工 · 2项进行中责任（R1·R2） · 1项需要CEO（R2）` + 状态条（当前态一句话）。
- **Composer** 锚定在**活跃（展开）Workstation 的 Conversation 底部**，随焦点移动，非全局独立条（中性控件见 §1a.3 / §5）。

### 1.2 核心状态（本规范 §10 详列）
`Default` / `Context Open` / `Utility Open` / `Needs CEO` / `Parallel`。

---

## 1a. RD Responsibility Model（多责任共存 · 本轮回写）

> 本模型为 RD Instance（Layer 4）语义，直接采用 Frozen §3.10 三层责任语义（Object Owner ≠ Current Responsibility ≠ Current Executor），不重定义。以下为 RD 的专业实例化与两类交接区分。

### 1a.1 多 Responsibility 共存 + 四概念语义（采用 Frozen §3.10，RD 实例化）

> 直接采用 Frozen §3.10 三层责任语义（Object Owner ≠ Current Responsibility ≠ Current Executor）。RD 在 Employee Workstation 上下文实例化如下四概念，**语义必须严格区分，不得混用**（本回合最终收口确认）。

- **Responsibility（责任单元）**：研发目标下的一个独立责任单元，拥有稳定 **Responsibility ID / Object**（如 `R1 · getUserData API 性能优化`）。是责任归属与执行的载体，不随 Handoff 改变身份。
- **Responsibility Holder（责任归属员工）**：被指派持有该 Responsibility 的 AI 员工（如 R3 持有者 = 王磊·运行AI）。Holder 是稳定的「责任所有者」，跨越责任生命周期存在——**即使当前未在执行，Holder 依然存在**（见 `waiting` 说明）。
- **Current Executor（当前执行者）**：此刻真正在主动执行的员工。**可为 none**——当责任处于 `waiting` / `needs_ceo` / `completed` / `failed` / `idle` 时，没有员工正在主动执行，Current Executor = none；此时不伪装成 System Activity（见 §3.9 / §D）。
- **Status（责任 / Runtime 状态）**：`working` / `waiting` / `needs_ceo` / `completed` / `failed` / `idle`，复用 Frozen §3.1 Runtime State 语义；它不等于 Shared Employee UI Status，也不决定 Workstation 展开/收起。

> **`waiting` 语义铁律（本回合最终确认）**：
> - **Responsibility Holder 可以存在**：`waiting` 的责任仍归属某员工（如 R3 归属王磊），Holder 不因等待而消失。
> - **Current Executor 可以为 none**：`waiting` = 责任已就绪、等待前置条件（如 R1 / R2 完成），此刻没有任何员工在主动执行，Current Executor = none。
> - 因此 `waiting` ≠ `idle` ≠ 无归属：Holder 在、Executor 空，等待恢复条件达成后由 Holder（或受托员工）继续。

- **多 Employee Workstation 共存 ≠ 一个 Responsibility 多个 Current Responsibility**。每个 Workstation 对应一个 Responsibility 的当前执行上下文；多个 Workstation 并列展示多个 Responsibility 的进度，但任一 Responsibility 在任一时刻只有一个 Current Responsibility。
- **每个 Responsibility 独立拥有**：Responsibility ID / Object · **Responsibility Holder** · Current Responsibility（阶段）· **Current Executor（可为 none）** · Status · Result / Evidence · Handoff history。
- **示例**：
  - **R1 · getUserData API 性能优化** → Responsibility Holder：陈真（工程AI）· Current Executor：陈真（执行中）· Current Responsibility：实现批量加载 · Status：`working`
  - **R2 · 用户表数据迁移审核** → Responsibility Holder：李翔（审核AI）· Current Executor：none（等待 CEO 执行权）· Current Responsibility：审核迁移脚本 · Status：`needs_ceo`
  - **R3 · 灰度发布（下一阶段）** → Responsibility Holder：王磊（运行AI）· **Current Executor：none（等待 R1、R2 完成，此刻未执行）** · Current Responsibility：灰度发布 · Status：`waiting`（明确等待 R1、R2 完成，非含糊「等待」）
- **Workspace Header 汇总**：`3 名员工 · 2 项进行中责任（R1·R2） · 1 项需要 CEO（R2）`。不同 Responsibility 不混为一个「当前责任」。

### 1a.2 两类交接（关键区分 · 不修改 Frozen Handoff）
- **Frozen Handoff Event（P5）** = **Current Responsibility 真正转移**（来源员工完成 → 接收员工接管该责任）。仅在此场景使用，轻量呈现（见 §6）。
- **RD Instance Candidate — Artifact Review Request / Review Handoff** = 把 Artifact/Result 送给 Reviewer 检查，**不自动转移 Current Responsibility**。陈真把 R1 实现代码送李翔审核 = Review Handoff；陈真仍持 R1 Current Responsibility，李翔仅做代码审核（不接管 R1 责任）。
- **判定当前示例**：原「陈真→李翔·代码审核交接」属 **Artifact Review Request（责任未转移）**，**不是 Frozen Handoff**。仅当陈真完成 R1 实现、李翔正式接管 R1 审核责任时，才升级为 Frozen Handoff Event。
- **升格处理**：Artifact Review Request 若未来需成为跨 Workspace 通用 Pattern，仅记为 **Shared Pattern Candidate**；本轮回写**不直接升格**，不动 Frozen §3.2。

### 1a.3 Composer（中性 · 与 §5 一致）
- 直接消费 Frozen Shell Composer 语义槽位：**Input / `＋` / 访问权限 / 工作模式 / 已选资源 / Model·Agent / Voice / Send**；运行中可按真实执行状态提供 Stop，不创建 RD 专属 Composer。
- **不固定 Q3 / 默认审批**：模型选项不写死具体模型名；权限是 Frozen 基础槽位，按当前真实权限语义呈现，不做常驻审批工具墙。

---

## 2. RD Context Surface（左 · Adaptive）

**采用 Shell Contract §2.2（Adaptive Surface），RD 声明内容如下：**

| 项 | RD 声明 |
|----|---------|
| 内容 | 当前 Workspace / 当前责任 / 相关文件与目录 / 最近对象（Design Brief §6） |
| 触发 | Main Header 的 T2（Context Toggle），或对话内上下文引用 |
| 展开行为 | 自适应 overlay 或 push（Shell Contract 修正 3：只统一交互契约，具体由窗口/场景决定） |
| 禁止成为 | 第二套员工目录 / Session Manager / Git 仪表盘 / 权限中心 / 交接队列 / 永久工具目录 |

内容示例（Figma）：文件树 `getUserData API 性能优化` → `api/users.ts` / `lib/db/queries.ts` / `types/user.ts`，当前任务高亮。

---

## 3. RD Utility Surface（右 · Adaptive）

**采用 Shell Contract §2.3（Shell 只定义容器，模式由 Instance 声明）。RD 声明模式集：**

| 模式 | 内容 | 触发 |
|------|------|------|
| **Diff / Changes** | 代码差异（红删绿增，语法高亮） | 对话内 Result Reference「查看差异」 |
| **Source / Code** | 源码阅读（文件树 + 代码视图） | 对话内引用或 Context 点文件 |
| **Preview / Result** | 运行结果预览（构建/预览/结果窗） | 对话内「工作结果已就绪」 |

- 每个 utility 必须显示**所属责任** + 提供**返回 Conversation 锚点**；打开 utility 不清除 Conversation、不重置员工、不改 worktree（Design Brief §7）。
- Terminal / Problems / 完整 Test / Git / Branch / Commit / PR / Review / Debug = **Reserved / Later**（Design Brief §3），本实例不实现，不预留装饰按钮。
- 专注模式：比主区更深 1 级背景（`#181a1d` 深 / 对应浅色）。
- 语法高亮令牌：**确有新增**，见 §11 Delta。

---

## 4. RD Runtime / Responsibility 状态（采用 Shared Pattern §3.1；不控制 UI 展开）

**自由多开（Frozen Shell）**：多个 Workstation 可同时展开；进入 Workspace 后由用户控制，Runtime 状态变化不得强制改变布局。

| 状态 | RD 真实语义 | Shared UI 投影边界 |
|------|-----------|------------------|
| `working` | Current Executor 正在执行 | 可投影 `工作中 · <desc>`；不自动展开 |
| `waiting` | 等待明确前置条件 / callback | 仅有真实阻塞事实时投影 `阻塞 · <cause>`，否则按当前责任事实表达；不自动收起 |
| `needs_ceo` | 存在真实 CEO Decision Gate | Workspace 注意力由 Decision Banner 表达；Employee UI 状态仍只消费三态投影，不强制展开 |
| `completed` | Work / Result 已完成 | “已完成”属于 Work / Result；Employee 无其他工作时回到 `空闲`，不自动收起 |
| `failed` | 当前执行失败，需真实原因与恢复路径 | 有真实阻塞时投影 `阻塞 · <cause>`；不自动展开 |
| `idle` | 当前无进行中工作 | 投影 `空闲`；不自动收起 |

**Collapsed 形态**（统一密度）：`32px 头像 + 姓名 + 角色 + 状态标签 + 当前工作一句话 + 展开 chevron`。
**Expanded 形态**：Header + 自然 Agent Conversation + 底部锚定 Composer。
展开 Workstation = 打开其**既有** Conversation；除非用户显式开启新责任，否则不新建线程（Design Brief §4）。

---

## 5. Conversation + Composer（采用 Shared Pattern §3.5）

- **Conversation**：provider-native Agent Conversation，嵌入展开态 Workstation Body；自然解释 + 轻量 Result Reference（不内嵌完整 Diff/代码/源码，见 §8）。
- **Composer**（锚定活跃 Workstation Conversation 底部）：
  - 自然语言输入（placeholder 显示继承的 Workspace + 责任上下文）
  - Frozen Shell 基础槽位：Input / `+` / 访问权限 / 工作模式 / 已选资源 / Model·Agent / Voice / Send
  - RD 只提供合法的 domain-specific mode / resource options，不改变基础 Composer；运行中可按真实执行状态提供 Stop
- Composer 视觉可保持安静紧凑，但不得因此隐藏或删除 Frozen Shell 的当前语义槽位。

---

## 6. Handoff Event（采用 Shared Pattern §3.2）

研发中的责任交接，在对话流轻量呈现。

**默认轻量形态（禁止大卡）**：仅显示 `来源员工 → 完成/交接摘要 → 接收员工 → 时间`。

**展开详情后**才显示：被转移的责任 + 上下文包 / 验收状态 / 待决问题 / 预期结果 / 返回·升级路径。

行为（Design Brief §8）：交接被接受后可提供发送方 / 接收方焦点入口，但不得由 Runtime 状态强制收起或展开 Workstation；若接收方拒绝或缺少上下文，回到发送方或升级为 Needs CEO。呈现责任链，**不暴露 DAG**。

> **本轮回写补充（不修改 Frozen §3.2）**：Frozen Handoff 仅用于 **Current Responsibility 真正转移**。RD 中「作者把产物送他人 Review、但作者仍负实现责任」属 **Artifact Review Request（Review Handoff，见 §1a.2）**，是 RD Instance Candidate，**不是** Frozen Handoff，不自动转移责任。二者在对话流中视觉区分（Frozen Handoff 用 `⇄ 责任交接` 轻量行；Review Handoff 用虚线 `🔍 送审请求`）。

---

## 7. Needs CEO / Decision（采用 Frozen §3.3 + §3.13 CEO Decision Package · P7 · Workspace 级）

**RD 采用确认（2026-08-15 最终收口）**：本节逐项对齐 Frozen §3.13 P7 冻结 10 项（①8 要素语义 ②非固定 8 块 UI ③三层信息层级 ④Complexity-aware 动作 ⑤高风险/不可逆禁止 Layer0 直批 ⑥Provenance 标记 ⑦禁止编造 ⑧决策后 AI 自动继续 ⑨CEO Decision ≠ Handoff ⑩专业证据进 Layer2），RD 已全部采用，无偏离。

**本 Pattern 是 Workspace 级阻断性决策面，出现在 Main 顶部 Decision Banner（非员工卡内部）。**

**内容结构（采用 Frozen §3.13 CEO Decision Package Pattern · P7）**：每次 Needs CEO 必须语义覆盖 8 要素（发生了什么 / 为何 AI 不能自决 / 可选方案 / 每方案影响·风险·代价 / Employee 推荐 / 推荐理由 / CEO 只需做的选择 / 选择后 AI 如何自动继续），主界面只讲 CEO 语言，专业证据走 Layer 2（P6 Result Reference）。**8 要素是语义，不等于 UI 固定 8 块**；按复杂度压缩表达（Low Surface Complexity, High Functional Density）。

**Layer 0 / 1 / 2 信息层级**：
- Layer 0 Decision Banner：极简「发生了什么」+ 复杂度感知动作；**不可逆 / 高风险 Decision 只 `[查看方案] [暂缓]`，禁止 Layer 0 一句话直接批准**。
- Layer 1 Plain Package：8 要素紧凑组合，CEO 看完方案 / 影响 / 推荐后再选择。
- Layer 2 Professional Evidence：技术脚本 / Diff / Test 按需查看（P6 + Utility）。

**Provenance（来源可追溯）**：Impact / Risk / Cost / Recommendation / Recommendation Reason 须带 `FACT` / `POLICY` / `EVIDENCE` / `EST` / `UNK` 标记；禁止编造，未知显式 `(UNK) 尚未验证`。

员工卡上的 `needs_ceo` 只是该员工的**责任状态指示**；真正的 Decision 交互由本 Pattern 承载（修正 2）。CEO 决策后，同一 Workstation 与 session 在安全检查后继续，责任未变不新建对话（CEO Decision ≠ Handoff，§3.12）。员工 Conversation 只做白话汇报 + Decision Reference，指向同一 Decision Packet，**不复制完整 8 要素、不把 SQL/CLI 原文扔给 CEO、不产生新 Handoff**。

RD 示例（不可逆类 · Layer 0 只提醒）：`⚠ 用户数据搬家最后一步需要你拍板（会改动线上结构、不可直接回退）` + `[查看方案] [暂缓]`；展开 Layer 1 后显示紧凑 Decision Package（3 个方案 + 影响/风险/代价 + 推荐 + 理由），技术脚本 `migration/users_2026.sql` / Diff / 测试进 Layer 2。

---

## 8. Result Reference（采用 Shared Pattern §3.4）

对话内**只放轻量引用**，点击开对应 Utility Surface；对话内不铺完整 Diff / 源码 / 数据。

| 引用 | 打开 |
|------|------|
| `api/users.ts · 34-93 · 查看差异 ▸` | Utility · Diff |
| `✅ 工作结果已就绪 ▸` | Utility · Preview / Result |
| `📊 测试通过 127/127 ▸` | Utility · Preview（Test Result 仅需要时） |

视觉：`emoji + 文字 + ▸箭头`，`--ui-accent` 色。

---

## 9. Parallel Working（自由多开 · CEO 冻结）

- 同一研发目标下，多个责任 Workstation 并列；每个有独立状态 / Owner / 连续 session / 源码范围 / 结果。
- 用户切换焦点**不丢失**其他责任，也**不暴露 Session Manager**。
- 禁止：顶部 tab、无差别群聊、节点图 / DAG（Design Brief §9）。
- 表现形式就是 §1.1 的垂直栈中多个 Workstation 可同时展开；初始展开与后续用户控制遵循 Frozen Shell，不按 working 状态持续驱动。

---

## 10. 核心状态矩阵

| 状态 | Header | Decision Banner | Workstation 栈 | Context | Utility | Composer |
|------|--------|----------------|----------------|---------|---------|----------|
| **Default** | 正常 | 无（无待决策） | 保持用户布局；仅“从 Workspace 外部进入 + 单一当前 working Employee”时初始展开一次 | 收起 | 收起 | 锚定活跃 WS |
| **Context Open** | 正常 | 无 | 保持 | **展开** | 收起 | 锚定活跃 WS |
| **Utility Open** | 正常 | 无 | 保持 | 收起（或同开） | **展开** | 锚定活跃 WS |
| **Needs CEO** | 正常 + 待决策徽标 | **显示** | needs_ceo 卡保留状态（展开/收起尊重用户布局）+ 顶部注意力项 | 收起 | 收起（点击引用可开） | 锚定活跃 WS |
| **Parallel** | 正常 | 按是否有待决策 | 多个 working 同时展开 | 收起 | 收起 | 锚定当前焦点 WS |

注：Context / Utility 可单开、双开、全关（Shell Contract §2.4）；所有状态均尊重用户手动布局调整（CEO 冻结）。

---

## 11. Design System Delta（方向已批准，具体值待验证）

以下 Delta **方向已获批准**；**具体令牌值暂不回写 Frozen**，待 Dark / Light / Contrast 验证后再 Frozen。

### Delta-1：Runtime State 记录 — **Historical decision, current UI projection superseded**
`failed` / `idle` 作为 Runtime State Schema 语义继续保留；Shared Employee UI Status 只消费 Frozen Shell 的“空闲 / 工作中·desc / 阻塞·cause”，不得把 Runtime 枚举直接变成额外 UI 状态或展开规则。

### Delta-2：Utility Surface 语法高亮令牌 — **批准方向，色值待定**
Frozen 确无代码/Diff 高亮令牌，Utility Surface 需要 `--ui-syntax-*` 系列令牌这一**方向已批准**。
**具体色值（深 / 浅 / 对比度）暂不批准**，须经过 Dark / Light / Contrast 验证后再 Frozen。
以下仅为待验证的候选示意，**未写入 `tokens.css`**：

```css
/* 候选示意 — 未批准，待 Contrast 验证 */
--ui-syntax-add-fg / --ui-syntax-del-fg / --ui-syntax-add-bg / --ui-syntax-del-bg
--ui-syntax-keyword / --ui-syntax-string / --ui-syntax-comment / --ui-syntax-code-bg
```

> 两项 Delta 均未自行写入 Frozen；Delta-1 的 Runtime State 语义保留，但旧 UI projection 已由 Frozen Shell supersede；Delta-2 待 Contrast 验证后回写。

---

## 12. 与现有文档关系 / 不修改声明

| 文档 | 关系 |
|------|------|
| `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` | 本实例的 Layer 1–3 基础，直接引用 |
| `Curis_RD_Workspace_Design_Brief.md` | 研发语义与禁止项错误来源，本规范固化其结论 |
| `Curis_Design_System_Delta_RD_Workspace.md` | RD 实例级视觉基线（前两阶段），本规范在其实例化结论上收敛 |
| `_system/tokens.css` / `Curis_Design_System.md` | Frozen 令牌与组件，只引用不修改（Delta 见 §11） |
| `Curis_Workspace_Shell.md` | 运营槽位（Layer 4 另一 Main 变体），本规范不冲突 |

**未修改**：任何代码、现有页面、`curis-ui-prototype/*`、Product Blueprint 或 Runtime Schema；Delta-1 的 UI projection 只消费 Frozen Shell，Delta-2 方向批准但色值待 Contrast 验证，未回写。

---

## 13. RD INSTANCE APPROVED

本规范将 RD Workspace 固化为 Professional Workspace Instance，依据 RD Figma structure reference + Frozen Shell Contract + RD Design Brief；当前视觉语言统一消费 Frozen Visual Standard，旧 Design System 不再定义品牌视觉。

**上一轮 Review 结论（4 点修正已落地）**：
1. `needs_ceo` 不强制收起：Decision Banner 负责 Workspace 级注意力，对应 Employee Workstation 保留 `needs_ceo` 状态并尊重用户展开/收起布局（可保持展开查看上下文）。
2. RD 不固定 plan/run 或具体模型；Composer 当前完整基础槽位与可见性语义统一由 Frozen Shell 决定。
3. Handoff Event 默认必须轻量：仅 `来源 → 摘要 → 接收 → 时间`，详情展开后才显示 Context Package / Acceptance / Questions / Expected / Escalation，禁止默认大卡。
4. Syntax Token：批准 `--ui-syntax-*` Delta 方向；**暂不批准具体色值**，待 Dark/Light/Contrast 验证后 Frozen。`failed` / `idle` 只保留为 Runtime State 语义，Shared Employee UI Status 仍只消费 Frozen Shell 三态投影。

**本轮回写已应用（Responsibility / Handoff Semantics 收口 + 最终确认）**：
- DP-1~DP-3 已应用：§1.1 旧 Global Topbar 图 → Frozen 四独立 Pane；Workspace Header 定位为 Main Pane Content；补 T1 / Utility Maximize。
- 新增 §1a RD Responsibility Model：多 Responsibility 共存（R1/R2/R3 各自拥有 ID/Object/Responsibility Holder/Current Executor/Status/Result/Handoff history）；**四概念语义严格区分，并确认 `waiting` 时 Responsibility Holder 存在、Current Executor 可为 none**。
- 两类交接区分：Frozen Handoff（责任真正转移）vs RD Instance Candidate — Artifact Review Request（责任未转移）；原「陈真→李翔·代码审核交接」归为后者。不修改 Frozen §3.2。
- Composer 中性：移除固定 `Q3` / 常驻 `默认审批`；当前直接消费 Frozen Shell 的 Input / `＋` / 访问权限 / 工作模式 / 已选资源 / Model·Agent / Voice / Send 语义槽位。
- §7 确认 RD 完全采用 Frozen §3.13 P7 冻结 10 项，无偏离。

**状态：RD INSTANCE APPROVED · READY FOR IMPLEMENTATION PLANNING**。不修改 Frozen Shell / Shared Patterns P1–P7 / Product Blueprint / 正式代码 / XHS；Artifact Review Request 保持 RD Instance Candidate，不升格 Shared Pattern。

---

**UI Designer**: UI Designer
**规范日期**: 2026-08-15
**状态**: RD INSTANCE APPROVED
