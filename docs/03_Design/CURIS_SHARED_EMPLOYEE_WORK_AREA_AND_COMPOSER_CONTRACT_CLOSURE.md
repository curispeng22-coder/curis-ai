# CURIS Shared Employee Work Area + Composer Contract Closure

> **Status**：APPROVED · 修正后已回写 Frozen（Delta-X10 · 2026-08-17）· 高保真最后一轮已据本 Closure 重制
> **日期**：2026-08-17
> **范围**：把所有 Business Workspace 共用的「工作区（Shared Employee Work Area）」与「Composer Shared Shell」固定下来，供未来新办公室复用——新办公室原则上只设计 Main 上部的 Domain Business Surface，不再重复设计员工工作区。
> **非目标（本轮严守）**：
> - **不创建新 P Pattern**；不修改 §3.1 现有 **Runtime State Schema**（`working`/`waiting`/`needs_ceo`/`completed`/`failed`/`idle` 一律不删、不改语义、不迁移）；**不新增 Runtime Primitive**。
> - 仅引用既有 Capability / Provider 能力真值（Permission `requested≠configured≠effective`、Model/Agent 本质、真实支持的模式/权限集），不发明新原语。
> - Workspace Engineering 高保真修改为独立执行轮次（已据本 Closure 最后一轮重制），不重做 Main / 四栏 / 资料台结构、不写正式产品代码。

---

## 0. 背景与目标

现有 Frozen 已覆盖：
- §3.1 Employee Workstation（含 Delta-X9 工作区编排约定）
- §3.5 Composer（极简骨架）
- §3.8 Employee Presence（P2）
- §3.14 Employee Detail（Utility，六字段，无 Conversation）
- P6 Result Reference（轻量引用 → Utility）
- Shared Authority §1.2 / §5.1（Employee 服务关系 / Context Isolation Truth）

但仍有三处缺口，导致新办公室每次都要「重复设计」员工工作区：
1. **Employee Row 结构未统一为两行+无详情按钮**；
2. **Employee Runtime Status 与 Work/Responsibility/Result 状态混在同张 States 表里**，易把「已完成/待审核」误写成员工状态；
3. **Composer Shared Shell 过薄**，无统一 Add / Access / Work Mode / Execution Selector / Provider Adaptation 约定，新办公室会各写一套。

本 Closure 一次性把这三处固定为 **Shared（可复用、Available Capability）**，并显式区分 Shared 固定项 与 Provider 决定项。

---

## 1. 现有 Frozen Authority 盘点（不重复定义，仅引用）

| 现有真源 | 已覆盖 | 本轮需补强 |
|---|---|---|
| §3.1 Employee Workstation + Delta-X9 工作区编排 | Workstation = Conversation-first；工作区 = Employee Workstation List；Runtime ≠ UI 折叠；外部进入单一 working 员工默认展开 | Employee Row 两行结构、Runtime Status 与 Work/Result 状态分离、Conversation Surface 居中/自适应/可拖拽语义 |
| §3.5 Composer | 多行 textarea + 紧凑工具条（左 +添加/执行/模型；右 权限/模式/发送） | 升级为 Shared Composer Shell（固定槽位 + Provider Adaptation） |
| §3.8 Employee Presence（P2） | 谁在这里 / 谁当前负责（员工入口），贴在业务对象上 | 其 Status 需与 §3.1 Employee Runtime Status 对齐口径（见 §5.4） |
| §3.14 Employee Detail（Utility） | 六字段，无 Conversation，点击「详情/是谁」触发 | 触发器改为「点击头像/姓名」（与 Employee Row 一致，去掉独立详情按钮） |
| P6 Result Reference（§3.4） | 对话内轻量引用 → 点击 Utility 全文 | **已覆盖，本轮不新增**（见 §4） |
| Shared Authority §1.2 / §5.1 | Employee ∈ Organization；Context Isolation Truth | 引用其 Permission/Capability 真值，不新增 primitive |

---

## 2. Shared Employee Work Area（固定结构）

### 2.1 Employee Row — 最终 Shared 结构

固定为**普通列表行（不做 Card）**。每行：

```
[头像（占两行）] [ 姓名 + 岗位          ] [ Employee Runtime Status ]
                [ 当前职责简述          ]                    [ ▸ / ▾ ]
```

- **第一列**：头像（占两行），色仅作区分，须配文字/图标满足色盲可达性。
- **第二列（第一行）**：姓名 + 岗位（堆叠）。
- **第二列（第二行）**：当前职责简述（轻量一行）。
- **第三列（右侧）**：Employee Runtime Status（见 §2.2）。
- **最右列**：展开箭头 `▸`（Conversation 收起）/ `▾`（Conversation 展开）。
- **交互**：
  - 点击**头像或姓名** → Utility 打开 **Shared Employee Detail（§3.14，六字段，无 Conversation）**。
  - **不设独立「详情」按钮**（详情动作即「点头像/姓名」）。
  - 点击箭头（或行其余空白区）→ 展开/收起该 Employee 的 Conversation-first Workstation。
- **Employee Row 是普通列表行**：用分隔线/行结构区隔，不套大型 Card。

> 与 Delta-X9「工作区编排约定」一致：每 Employee 固定轻量展示（头像+姓名+岗位+当前职责+当前状态+展开/收起）；本轮仅把布局精确为「两行 + 头像跨两行 + 去详情按钮 + 点击头像/姓名进 Utility」。

### 2.2 Employee UI Status（用户侧投影）— 与 Runtime State Schema 分离

> **关键边界（Review 修正 1）**：本节固定的 **Shared Employee UI Status 是 Runtime Truth 的用户侧投影（projection），不是 Runtime State Schema 本身。**
>
> - **现有 §3.1 Runtime State Schema（`working` / `waiting` / `needs_ceo` / `completed` / `failed` / `idle`）本轮一律不删、不改语义、不迁移。** 它们是员工真实运行状态的真源，仍由 Runtime / 责任视图表达 Work/Result 生命周期与责任状态。
> - 本轮**不重构**该 States 表，也**不新增**任何 Runtime Primitive（含 `blocked`、`offline`、`unavailable`）。
> - Runtime State 模型是否需要清理，留给后续**独立的**技术 / Authority 审计，不在本 UI Closure 内处理。

**Shared Employee UI Status = Runtime Truth 的用户侧投影（三态）**：用户侧只看到下列三种「这个员工当前能不能接活 / 在干什么」的简化表达，投影来自真实 Runtime / Responsibility 事实。

| UI Status | 投影来源（必须来自真实事实） | 表现 |
|---|---|---|
| `空闲` | Runtime 无进行中工作（如 `idle`） | 中性标签 |
| `工作中 · <简短实时工作描述>` | Runtime `working` + 真实运行时短句（如「撰写发布稿」） | 品牌绿 + 脉冲点；`<描述>` 由 Runtime 提供，非编造 |
| `阻塞 · <简短问题原因>` | **仅当真实 Runtime / Responsibility 事实能证明阻塞时投影**（如「等待 API 凭证」）；`<原因>` 须来自真实事实 | warning 标签 |

**投影纪律（不可违反）**：
- UI Status **不得**凭 UI 需要自行发明状态；`阻塞` 只有在真实 Runtime/Responsibility 事实能证明其阻塞时才投影，且**不因此新增 Runtime Primitive**（若 Current Runtime 没有独立的 blocked 真值，UI 不得伪造）。
- **禁止把以下当 Employee UI Status**：`已完成` / `待审核` / `已验收`（= Work/Result/Responsibility 审批事实，由对应对象表达；员工完成后若无他务投影回 `空闲`）；`待命`（语义模糊，不构成员工运行时态）。
- 工作完成后若员工无其他工作 → UI 投影回 `空闲`；完成事实由 Work / Responsibility / Result 表达，不由员工 UI Status 表达。
- **不新增** Offline / Unavailable：现有 Runtime / Shared Authority 均无此真实状态依据，本轮不凭空创造。

### 2.3 Conversation Surface — Shared 规则

展开 Employee Row 后，直接出现统一的 **Conversation-first Workstation**，不做 Card、不做 AI 状态 Dashboard、不重复显示 Employee Holder / 当前步骤 / 下一步（这些由 Work/Responsibility/Result 表达或对话内轻量状态行承载）。

Shared 规则（只 Frozen 语义，不 Frozen 具体 px）：
- **居中**：Conversation 在 Main 可用宽度内**始终居中**。
- **Bounded / Responsive**：随 Desktop / Pane 宽度变化自适应；有合理 **minimum / preferred / maximum readable width**（建议以可读行为准，不写死 px）。
- **默认舒适高度**：展开后有默认舒适高度。
- **用户可拖拽调整高度**：右下角拖拽手柄，用户可改变高度；该高度仅为本地 UI 偏好，不回写 Runtime。
- **展开/收起只改 UI，不改 Runtime**：收起后员工继续工作；列表状态持续更新；再展开可见最新输出（与 Delta-X9「Runtime ≠ UI 折叠」一致）。

> 对话内容本身 = 自然消息流 + Runtime 真实过程（仅真实发生时作为轻量状态行出现，不做 Dashboard）+ Result/Artifact 轻量引用 + Composer。

---

## 3. Shared Composer Shell

> 基于 WorkBuddy / Codex / 豆包 / Coze / EvoFlow 参考**提炼统一骨架**，不照抄任何产品。Curis 面向普通用户，**默认不把重要能力全部藏进 `+`**。

### 3.1 固定槽位（Shared 语义固定；Desktop 推荐布局，非所有尺寸冻结）

```
┌─────────────────────────────────────────────────────────────┐
│  输入区（多行，placeholder 随 Employee/场景变化）              │
├──────────────────────────────────────┬──────────────────────┤
│ 底部左侧：                              │ 底部右侧：              │
│  + 功能 | 访问权限 ▾ | 工作模式 ▾        │ 执行选择(Model/Agent)▾ │
│  [已选择的功能/资源 chip…]               │ | Voice(支持时) | Send  │
└──────────────────────────────────────┴──────────────────────┘
```

- **输入区**：多行文本输入。
- **+（统一 Add 入口，语义冻结，文案不冻结）**：根据当前 Employee **真实支持的能力**提供（Review 修正 3）：
  - 文件 / 图片 / 资料·Knowledge / Skill / Connector / 其他当前 Employee 真实支持的功能。
  - 选择后仅在 Composer 中显示对应 **chip / reference**；未选择不占空间。
  - 用户侧避免要求理解 Tool / MCP / Skill / Connector 等内部技术区别（统一为「功能/资源」）。
  - **Add 入口语义冻结为「统一附加能力入口」；但按钮文案不冻结**——Frozen 只锁语义，不锁标签；当前原型可使用 `+`，展开后按真实能力列出文件/图片/资料/Skill/Connector 等；**不强制按钮必须叫「功能」**。
- **访问权限（固定显性入口）**：必须消费**真实 Computer Access / Provider 权限能力**（其 `requested ≠ configured ≠ effective` 真值由 Provider Capability 提供）；不支持的权限不得伪造为可选。
- **工作模式（固定显性入口）**：面向普通用户表达工作意图（如 目标 / 计划 等）；具体模式必须来自**真实 Runtime 能力**，本轮不凭 UI 自创完整模式体系。
- **执行选择（Execution Selector，必须显性，但区分 Model / Agent）**：见 §3.3。
- **Voice（可选）**：仅当 Provider 支持时显示。
- **Send**：发送。

### 3.2 Provider Adaptation（Shared 固定 vs Provider 决定）

| 维度 | Shared 固定（Core 规则） | Provider 决定（Adapter 暴露） |
|---|---|---|
| **语义槽位**（Input / Add / Access / Work Mode / Selected / Execution / Voice / Send） | ✅ 槽位语义固定 | — |
| **布局** | Desktop 推荐「输入区在上、底部左右分组」的当前布局；但**不 Frozen 为所有尺寸/平台固定排列**（Review 修正 2） | 响应式 / overflow / mobile 等场景允许重新布局（槽位不丢，顺序/排列可变） |
| 支持哪些**权限** | 入口固定，消费真值 | Provider 决定实际可选权限集 |
| 支持哪些**工作模式** | 入口固定 | Provider 决定实际模式集 |
| **Model 还是 Agent** | 必须显性区分二者 | Provider 暴露其本质（模型型 / Agent 型） |
| 是否允许**切换模型** | 入口存在 | Provider 决定是否可切换 |
| Agent 有哪些**原生执行设置** | 不制造第二套 | Agent 经 Adapter 暴露其真实支持项 |

**不把 Codex / Claude Code / ChatGPT 等 Provider 写死进 Core 规则**——它们是 Provider 实例，经 Adapter 被 Shared Shell 消费。

### 3.3 Model-backed / Agent-backed 如何适配

- **Model-backed Employee** → Execution Selector 展示 **Model / Auto 选择**（如 `Auto` / `GPT` / `Claude` …）。
- **Agent-backed Employee** → Execution Selector 展示**真实 Agent**（如 `Codex` / `Claude Code` / 其他 Provider Agent）。
  - **不得把 Agent 错误降级成「一个模型」**（这是 Capability Truth 边界：Agent ≠ Model）。
  - 若 Agent **自身管理** Model / Permission / Mode，由 **Provider Adapter 暴露其真实支持项**；Curis 不得制造第二套虚假 Model Truth。

---

## 4. Result / Artifact（已覆盖，仅重申）

Conversation 中只 Frozen：**轻量 Result/Artifact Reference → 点击 Utility 完整查看**。不 Frozen 具体视觉形式。未来允许 Provider / Capability 根据真实结果类型呈现文件、图片、Diff、代码、Preview 等。

> 此条已由 **P6 Result Reference（§3.4，Frozen）** 覆盖，本轮不新增。

---

## 5. 最小 Delta 提案（等待 Review，本轮不回写）

> 以下为**提案**，Review 通过后才回写 Frozen。本轮仅记录。

### 5.1 Frozen Shell Contract §3.1 Employee Workstation
- **Anatomy 精化**：Employee Row 改为两行（头像跨两行；行1 姓名+岗位；行2 当前职责）；去掉独立「详情」按钮，改为「点击头像/姓名 → Utility Employee Detail」。
- **新增子节「Shared Employee UI Status（用户侧投影）」**（替换原本「重构 States 表」的写法，Review 修正 1）：
  - **不动现有 Runtime State Schema**（`working`/`waiting`/`needs_ceo`/`completed`/`failed`/`idle` 一律保留、不改语义、不迁移）。
  - 固定 **Shared Employee UI Status = Runtime Truth 的用户侧投影（三态）**：`空闲` / `工作中·<实时描述>` / `阻塞·<原因>`。
  - 投影纪律：UI 不得凭 UI 需要自造状态；`阻塞` 仅当真实 Runtime/Responsibility 事实能证实时投影，**不因此新增 Runtime Primitive**；完成事实由 Work/Result 表达，员工无其他工作投影回 `空闲`；不新增 Offline/Unavailable。
  - Runtime State 模型清理留给后续独立技术 / Authority 审计。
- **新增子节「Conversation Surface Shared Rules」**：居中 / Bounded·Responsive（min·preferred·max readable width，不写死 px）/ 默认舒适高度 / 用户可拖拽调整高度 / 展开收起只改 UI 不改 Runtime。

### 5.2 Frozen Shell Contract §3.5 Composer
- 由极简骨架**升级为 Shared Composer Shell**：固定**语义槽位**（Input / +（Add 入口，语义冻结、文案不冻结）/ 访问权限 / 工作模式 / 已选功能资源 / 执行选择 / Voice 可选 / Send）+ Provider Adaptation 表 + Model-backed/Agent-backed 适配规则（Agent 不得降级为模型；Provider Adapter 暴露真实项）。
- **布局仅 Desktop 推荐**（输入区在上、底部左右分组），**不 Frozen 为所有尺寸/平台固定排列**；响应式/overflow/mobile 可重新布局（Review 修正 2）。
- 引用真实 Provider Permission 真值（`requested ≠ configured ≠ effective`），不伪造不支持的权限。

### 5.3 Frozen Shell Contract §3.14 Employee Detail
- 触发器由「详情/是谁 按钮」改为「点击头像/姓名」（与 §2.1 Employee Row 一致）。

### 5.4 Shared Authority（仅引用，不新增 primitive）
- §3.8 Employee Presence 的 Status 口径应与 §3.1 Shared Employee UI Status 对齐（Presence 表达「谁在/做什么」，其 Status 不混入 Work/Result 生命周期态）。
- Provider Permission 真值（`requested ≠ configured ≠ effective`）如尚未 Frozen，归属 Provider Capability Authority（Candidate），本 Closure 仅**消费**该真值，不新造 Runtime Primitive。

---

## 6. 八问直接回答

1. **Employee Row 最终 Shared 结构**：普通列表行（不做 Card）= `[头像跨两行] [行1 姓名+岗位] [行2 当前职责] [Employee Runtime Status] [▸/▾]`；点头像/姓名 → Utility Employee Detail；无独立详情按钮。
2. **Employee UI Status 最终候选（用户侧投影，非 Schema）**：`空闲` / `工作中·<实时描述>` / `阻塞·<原因>` 三态；禁止把 已完成/待命/待审核/已验收 当员工状态；**不重构现有 Runtime State Schema**（working/waiting/needs_ceo/completed/failed/idle 一律保留），不新增 Runtime Primitive；`阻塞` 仅当真实事实证实时投影，Offline/Unavailable 不新增。
3. **Conversation Surface Shared 规则**：居中、Bounded·Responsive（min/preferred/max readable width，不写死 px）、默认舒适高度、用户可拖拽调高、展开收起只改 UI 不改 Runtime。
4. **Composer 固定语义槽位（布局不冻结）**：输入区 + 底部左（`+` Add 入口 / `访问权限▾` / `工作模式▾` / 已选功能资源 chip）+ 底部右（`执行选择(Model/Agent)▾` / `Voice 可选` / `Send`）。Desktop 推荐当前左右分组布局，但不 Frozen 为所有尺寸/平台固定排列；响应式/mobile 可重排。Add 入口**语义冻结、文案不冻结**（可用 `+`，不必叫「功能」）。
5. **Model-backed / Agent-backed 适配**：Model 型 → 展示 Model/Auto 选择；Agent 型 → 展示真实 Agent；Agent 不得降级为模型；Agent 自管项由 Provider Adapter 暴露真实支持集，Curis 不造第二套 Model Truth。
6. **Shared vs Provider**：Shared 固定**语义槽位**/显性区分 Model·Agent/Voice 可选；**布局** Desktop 推荐、响应式可重排；Provider 决定支持哪些权限/模式、Model 还是 Agent、能否切模型、Agent 原生执行设置；不写死具体 Provider 进 Core。
7. **Frozen Shell / Shared Authority 最小 Delta**：§3.1（两行 Row + 新增 Shared Employee UI Status **投影**子节【不动现有 Runtime State Schema】+ Conversation Surface 规则）、§3.5（升级 Shared Composer Shell：固定语义槽位+Provider Adaptation，布局仅 Desktop 推荐）、§3.14（触发器改点头像/姓名）、Shared Authority（仅引用 Permission 真值，不新增 primitive；§3.8 口径对齐）。
8. **Workspace Engineering 当前高保真最后需改什么**（下一轮，本轮不动）：① Employee Row 改两行 + 去详情按钮 + 点头像/姓名接 Utility；② Runtime Status 对齐三态（去 已完成/待审核 类）；③ Conversation 居中 + 自适应最大宽 + 右下角拖拽调高；④ Composer 扩为 Shared Shell 槽位（接真实 Capability/Provider）；⑤ 其余 §0.1「Main must stand on its own」/ 四栏 / 无伪装 Topbar / §3.12·§3.14 禁止项保持。

---

## 7. 高保真待改清单（下一轮，本轮不执行）

| # | 改动 | 来源 |
|---|---|---|
| H1 | Employee Row：单行 → 两行（头像跨两行，行1 姓名+岗位，行2 职责）；移除详情按钮；点头像/姓名 → Utility Employee Detail | §2.1 / §5.3 |
| H2 | UI Status 投影：员工行状态改为 UI Projection 三态 `空闲/工作中·<desc>/阻塞·<cause>`；现有 Runtime State 不删不改；不投影 已完成/待审核 类 | §2.2 / §5.1 |
| H3 | Conversation Surface：居中 + 自适应 max readable width + 默认舒适高 + 右下角拖拽调高 | §2.3 / §5.1 |
| H4 | Composer：扩为 Shared Shell（Input / `+` Add（语义冻结文案不冻结）/ 访问权限▾ / 工作模式▾ / 已选 chip / 执行选择 Model·Agent▾ / Voice / Send），接真实 Capability/Provider；Desktop 推荐布局，响应式可重排 | §3 / §5.2 |
| H5 | 保持：Main must stand on its own / 四栏 / 无伪装 Topbar / §3.12·§3.14 禁止项 | 不变 |

---

## 8. 停止态

```text
SHARED EMPLOYEE WORK AREA + COMPOSER CONTRACT CLOSURE — APPROVED · 修正3点 · 已回写 Frozen (Delta-X10)
→ 输入：现有 Frozen §3.1 / §3.5 / §3.8 / §3.14 / P6 + Shared Authority §1.2·§5.1
→ 交付：本 Closure（APPROVED）+ Frozen 最小 Delta 回写（Delta-X10）+ 高保真最后一轮重制
→ 固定：Employee Row 两行结构 / Shared Employee UI Status(投影,非Schema) 三态 / Conversation Surface 居中·自适应·可拖拽 / Composer Shared 语义槽位 + Provider Adaptation
→ 修正：① UI Status=Runtime Truth 投影,不动 Runtime State Schema,不新增 Primitive ② Composer Frozen 语义槽位非布局 ③ +入口文案不冻结
→ 纪律：未建新 P Pattern / 未改 Runtime State Schema / 未新增 Runtime Primitive / 未重做 Main·四栏·资料台 / 未写产品代码
→ 停止 Review（STOP FOR REVIEW）
```
