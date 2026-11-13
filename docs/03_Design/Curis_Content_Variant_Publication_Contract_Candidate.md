# Curis · Content Variant / Publication Contract Candidate

> **状态**：**APPROVED CANDIDATE**（Batch C — Content Production × Channel Ops 落点；仍不 Frozen）
> **修订**：已应用 **DELTA C1 — Publication 必须服从 Distribution Execution Policy**（区分 FACT CONSISTENCY 与 FUTURE EXECUTION POLICY；Policy 引用契约 ④，本契约不重定义第二套）
> **FROZEN 指针（2026-08-16）**：⑤ Content Variant / Publication 语义已正式冻结于 `Curis_Content_Growth_Domain_Authority.md` §1.5。本 Candidate 保留作 **Design Record / Reference**，不删除、不覆盖。
> **类型**：Content Growth Domain（Variant / Publication 记录）；Publication 实际执行 → Capability·Connector（仅引用）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 5）、`Curis_Target_Account_Contract_Candidate.md`（契约 ④，production_requirements 来源）、`Curis_Content_Intent_Contract_Candidate.md`（契约 ③）、`Curis_Channel_Account_Contract_Candidate.md`（契约 ②，账号作用域 + authorization_state）、`Curis_Organization_Routing_Architecture.md`（H/I 节 Variant/Publication 为 per-Account 真相源）

---

## 0. 本契约的目的与边界

固化「**Variant 归属具体 Account（可每账号多份）+ Publication 为 per-Account 真相源**」—— 即 Batch A 的 Target Account Set 向下游的**落点**。

**核心纠正（继承前序）**：
- 一个 Content Intent → **N 个 Content Variant**，每个 Variant **绑定且仅绑定一个 Channel Account**（账号级）。
- **Publication 是 per-Account 真相源**：某账号是否发布、回执、时间、状态，独立记录在该账号的 Publication 上。
- **DELTA C1 — 事实一致性 ≠ 后续执行策略**：「一个账号失败不回滚其他账号」**仅**表示「**已经发生的** Publication 事实不被篡改/回滚」；它**不**表示「无论业务意图如何，其他账号永远继续发布」。**尚未执行**的部分是否继续，由契约 ④ 的 **Distribution Execution Policy**（`BEST_EFFORT` / `ALL_REQUIRED`）决定。本契约**只引用**该 Policy，**不重新定义第二套策略**。
- 发布执行（真实发布调用、回执产生）由 **Capability·Connector** 承担，本契约**只引用**其回执，不定义其内部（纪律：不开发 Connector）。
- 定时发布 `scheduled_at` **按平台条件化**（YouTube `publishAt` ✅ / 抖音官方 API ❌ 未知）—— **POLICY VERIFICATION REQUIRED**，不写死「每次必须人工点击」也不假设「总能定时」。

本契约只定义对象语义 / 关系 / 归属 / 生命周期 / 必填·可选 / 不变量 / 跨对象引用 / 失败·未知 / 场景验证。**不进入** DB table / SQL / ORM / API / frontend state / 实现类 / migration。

---

## 1. Content Variant（Content Growth Domain · 账号级变体）

### Object semantics
一个 Content Intent 在**某个具体 Channel Account** 上的**账号级适配产物**——实际要发布的素材规格（ratio/时长/文案/封面/标签/音乐/披露 等）。每个 Variant 严格绑定一个账号。

### Identity
- `variant_id`
- `content_intent_id`（FK → 契约 ③ Content Intent）
- `channel_account_id`（FK → 契约 ② Channel Account，**账号作用域**）

### Composition（核心字段）
- `ratio` / `duration` / `edit_variant`（账号级适配：画幅/时长/剪辑版本）
- `caption` / `title` / `cover` / `hashtag` / `music`（账号级文案与素材）
- `disclosure`（AI 披露，按平台政策字典生成）
- `platform_policy_result`（该平台政策校验结果：PASS / WARN / BLOCK）
- `production_config`（如何生产：来源 Capability Provider 引用，不定义内部）
- `reuse_mode`：`HIGH_REUSE`（共享推理、仅改 metadata）/ `FULL_DIVERGENCE`（同 Intent 不同形态，完全重新生产）
  - 由 Intent 的共享/分歧原则决定（继承 Operating Model G 节「Shared reasoning once, divergent production when necessary」）

### Required / Optional information
**必填**：`content_intent_id`、`channel_account_id`、（至少一项适配字段）
**可选**：`reuse_mode` / `platform_policy_result` / `production_config` / `disclosure` / 其余适配字段

### Relationships
- `Content Variant *—1 Content Intent`（父意图，契约 ③）
- `Content Variant *—1 Channel Account`（账号作用域，契约 ②）
- `Content Variant ← Target Account Set 的 production_requirements`（由 ④ 推导的账号级生产要求驱动）
- `Content Variant 1—* Publication`（每个 Variant 可对应多次 Publication）

### Ownership
- 属 Content Growth Domain 业务对象层；**per-Account**（每个 Variant 绑定单一账号）。
- Variant 的**实际生产**由 Capability Provider 完成（能力层），本契约只持有产物质规格与引用。

### Lifecycle
Variant **不是 Workflow**，是产物规格；其「生命周期」随生产推进：
- **DRAFT**：待生产 / 生产中
- **READY**：账号级适配产物就绪，可被 Publication 消费
- （可选 REVISED：基于反馈修订；属生产层，本契约不强制状态机）

### Invariants（硬约束）
1. **Variant 严格账号级**：每个 Variant 绑定**且仅绑定一个** Channel Account。一个 Intent → N 个 Variant（每选中账号一份）。
2. **reuse_mode 来自 Intent 分歧原则**：HIGH_REUSE（轻量 metadata 适配）vs FULL_DIVERGENCE（完全重新生产）；Variant 只承载**账号专属适配**，不重复存储 Intent 的共享推理。
3. **无跨账号串线（DELTA B1）**：为 Account A 生产的 Variant **不得**携带 Account B 的 `tone_style` / 策略 / Knowledge；Variant 在 task-scoped Context Package 内生产（见契约 ⑧ §2b），上下文隔离。
4. **Publication 执行在 Connector，不在本契约**：本契约记录 Publication 记录（状态/回执/时间）；真实发布调用由 Capability·Connector 执行，仅引用 `publish_receipt`。
5. **scheduling 按平台条件化（POLICY VERIFICATION REQUIRED）**：`scheduled_at` 仅在该平台官方支持时有效；不支持的平台（如抖音官方 API 未知）`scheduled_at` 置空/标记不支持，**不写死强规则**。
6. **Variant 可多次 Publication**：一个 Variant **可对应多次 Publication**（重发 / 多版本）；每次 Publication 仍 per-Account 独立真相追踪（见 §2）。

### Cross-object references
- → **契约 ③ Content Intent**（父）
- → **契约 ④ Target Account Set**（production_requirements 来源；生产按选中账号逐账号发生）
- → **契约 ② Channel Account**（账号作用域；`authorization_state` 决定发布期 Eligibility）
- → **Capability·Connector**（实际生产 / 发布执行；`production_config` / `publish_receipt` 引用，不定义内部）
- → **契约 ⑨ Bottleneck Candidate**（间接：生产队列观测，后续 Batch）

### Failure / Unknown semantics
- **账号 OAuth 过期（发布期，链接 ④ DELTA A2）**：该账号 Publication → FAILED / BLOCKED；**其他账号 Publication 不受影响**（per-Account 真相）。
- **平台政策未知**（如抖音 scheduling）：`scheduled_at` 置空 / 不支持标记；Publication 走即时发布或标记，不静默假设。
- **某账号 Variant 生产失败**：仅该账号 Variant/Publication 受影响，其余账号继续。
- **platform_policy_result = BLOCK**：该 Variant 在该平台被阻，不发布；不影响其他平台 Variant。

### Example scenarios
- **CASE C1（同 Intent → N 账号级 Variant）**：Intent #101 选中 `{Douyin, XHS, Bilibili}` → 3 个 Variant，各绑定单一账号；Douyin 取 `HIGH_REUSE`（快口播改 metadata），Bilibili 取 `FULL_DIVERGENCE`（深度教程重生产）。
- **CASE C2（Publication per-Account 真相）**：Douyin=PUBLISHED、XHS=PUBLISHED、Bilibili=FAILED(OAuth) —— 各自独立真相追踪；Bilibili 失败**不回滚** Douyin/XHS。
- **CASE C3（scheduling 条件化）**：YouTube Variant `scheduled_at` 可设（支持 ✅）；Douyin Variant `scheduled_at` 不支持（官方 API ❌ 未知）→ 置空、走即时发布 / 标记；POLICY VERIFICATION REQUIRED，不硬编码。
- **CASE C5（reuse/divergence）**：`reuse_mode=HIGH_REUSE` → Variant 克隆母版仅改 metadata；`FULL_DIVERGENCE` → 按账号完全重产。

---

## 2. Publication（Content Growth Domain · per-Account 真相源）

### Object semantics
某 Variant 在**某个 Channel Account** 上的**一次发布事件/记录**——是该账号「是否发布、回执、时间、状态」的**唯一真相源**。

### Identity
- `publication_id`
- `variant_id`（FK → §1 Content Variant）
- `channel_account_id`（FK → 契约 ②，per-Account）

### Composition（核心字段）
- `publish_status`：`DRAFT` / `SCHEDULED` / `PUBLISHING` / `PUBLISHED` / `FAILED` / `BLOCKED`（per-Account）
- `publish_receipt`（→ Connector 回执引用；成功时由 Connector 回填）
- `scheduled_at?`（条件化，见 §1 Invariant #5）
- `published_at`（实际发布时间，成功时回填）
- `applied_execution_policy_ref?`（**只读引用快照**：本次执行时生效的 ④ `distribution_execution_policy` 取值，仅供事后追溯；**语义与默认值不在本契约定义** —— DELTA C1）

### Required / Optional information
**必填**：`variant_id`、`channel_account_id`、`publish_status`
**可选**：`publish_receipt` / `scheduled_at` / `published_at` / `failure_reason`

### Relationships
- `Publication *—1 Content Variant`（父变体）
- `Publication *—1 Channel Account`（per-Account）
- `Publication → Capability·Connector`（执行引用；回执由 Connector 产生，本契约不定义发布逻辑）

### Ownership
- 属 Content Growth Domain 记录层；**per-Account 真相**。
- 发布**执行**归属 Connector（能力层），本契约只持有记录。

### Lifecycle（per-Account 独立状态机）
- `DRAFT` → `SCHEDULED`（若 `scheduled_at` 且平台支持）→ `PUBLISHING` → `PUBLISHED` / `FAILED`
- 或 `DRAFT` → `PUBLISHING` → `PUBLISHED` / `FAILED`（即时）
- `BLOCKED`：账号 Eligibility 不足（如 OAuth 过期，链接 ④ DELTA A2）；可按 Distribution Execution Policy 重试/跳过
- **每个账号的 Publication 独立推进**；一个账号的终态不影响其他账号

### Invariants（硬约束 · 承接 §1）
1. **per-Account 真相源（FACT CONSISTENCY）**：发布状态/回执/时间**逐账号独立记录**；某账号 FAILED/BLOCKED **不得篡改、不得回滚**其他账号**已经发生**的 Publication 事实。
2. **Publication ≠ Variant 一对一**：一个 Variant 可对应多次 Publication（重发/多版本）；每次 Publication 仍 per-Account 独立真相。
3. **回执来自 Connector**：`publish_receipt` 由 Capability·Connector 回填，本契约不生成发布证据。
4. **状态机仅 per-Account**：无跨账号「整体发布状态」概念；整体进度由 Aggregate View（非本契约对象）派生。
5. **DELTA C1 — 后续执行服从 Distribution Execution Policy（FUTURE EXECUTION POLICY）**：某账号不可执行/失败后，**尚未执行**的其余 Target Account 是否继续，**必须**按契约 ④ 的 `distribution_execution_policy` 判定：
   - `BEST_EFFORT` → 其余可用 Target 继续执行；
   - `ALL_REQUIRED` → 任一 Required Target 不可执行时，**本次 Distribution 中尚未执行的部分暂停**（已发生事实不回滚）。
   **禁止**把 Invariant #1（事实不回滚）解释为「其他账号无条件继续发布」。
6. **DELTA C1 — 不重定义第二套 Policy**：本契约**不**定义任何自有的分发/中止策略枚举或默认值；`distribution_execution_policy` 的语义、默认值与覆盖规则**唯一归属契约 ④**（Office 有默认、任务可覆盖）。本契约仅**读取并服从**。

### Cross-object references
- → §1 Content Variant（父）
- → 契约 ② Channel Account（per-Account；`authorization_state` 影响 `BLOCKED`）
- → Capability·Connector（执行 + 回执）
- → 契约 ④ Target Account Set（发布执行状态**归属此处**，不在 Target Account Set —— DELTA A1 已分离）
- → **契约 ④ `distribution_execution_policy`（唯一定义方）**：本契约**读取并服从**，用于判定「某账号不可执行后，尚未执行部分是否继续」；**不重定义**（DELTA C1）
- → **契约 ④ Account Eligibility**（DELTA A2）：Eligibility 决定「能不能发」→ 映射为 Publication 的 `BLOCKED`；Target 本身不因此被删除

### Failure / Unknown semantics
- **发布调用失败（网络/平台拒绝）**：该 Publication → `FAILED` + `failure_reason`；其他账号**已发生**的 Publication 事实不变；**尚未执行**的按 ④ Policy 判定（见 Invariant #5）。
- **账号 BLOCKED（OAuth 过期）**：Publication → `BLOCKED`（账号仍是 Target，仅不可执行 —— ④ DELTA A2）；后续执行按 ④ `distribution_execution_policy`：`BEST_EFFORT` 跳过继续 / `ALL_REQUIRED` 暂停尚未执行部分。
- **回执缺失**：`publish_receipt` 为空但 `publish_status=PUBLISHED` 视为不完整记录，标记待核对，不静默视为成功。
- **Policy 未知/缺失**：`distribution_execution_policy` 未解析到时 → **不猜测**，按契约 ④ 的 Office 默认；仍无法解析则暂停并升级（不默认全量继续发布）。

### Example scenarios
- **CASE C2（BEST_EFFORT）**：3 账号发布，Office Policy = `BEST_EFFORT`；Douyin/XHS 成功、Bilibili `BLOCKED`（OAuth）→ 各自 Publication 独立真相，其余继续；CEO 可见「B站授权已过期，抖音和小红书仍可继续发布」（白话，链接 ④ DELTA A2）。
- **CASE C7（ALL_REQUIRED，DELTA C1 新增）**：某次品牌同步发布，任务覆盖 Policy = `ALL_REQUIRED`（三平台必须同步）。执行顺序中 Douyin 已 `PUBLISHED`，随后 Bilibili `BLOCKED`（OAuth）→
  - **已发生事实不回滚**：Douyin 的 Publication 保持 `PUBLISHED`（Invariant #1）。
  - **尚未执行部分暂停**：XHS 的 Publication 不进入 `PUBLISHING`，保持待执行/暂停并升级（Invariant #5）。
  - CEO 白话：「B站授权已过期，这次要求三个平台同步发布，已暂停后续发布。抖音已发出。」
- **CASE C6（重发）**：Variant #101-Douyin 首次 PUBLISHED；两周后二次 Publication（重发）→ 两个独立 Publication 记录，均 per-Account 追踪。

---

## 3. 归属层

| 对象 | 归属层 |
|------|--------|
| Content Variant | Content Growth Domain |
| Publication（记录） | Content Growth Domain（per-Account 真相源） |
| Publication 实际执行 | Capability·Connector（仅引用，不定义） |

---

## 4. 与现有权威文档的关系

- **P1–P7**：不冲突、不修改。Publication 是业务对象记录；其发布/回执不引入新责任语义。
- **DELTA A1（Target/Publication 分离）**：发布执行/成功状态**归属 Publication（本契约）**，不在 Target Account Set（契约 ④）—— 已落实。
- **DELTA A2 / DELTA C1（Eligibility 与 Policy）**：Eligibility（能不能发）→ Publication `BLOCKED`；`distribution_execution_policy`（后续是否继续）**唯一定义在契约 ④**，本契约只引用服从。事实一致性（不回滚已发生）与后续执行策略（是否继续）**严格分离**。
- **DELTA B1（上下文隔离）**：Variant 在 task-scoped Context Package 内按账号生产，无跨账号串线（Invariant #3）。
- **Blueprint / XHS / RD Instance**：不冲突、不改、不变（当前 XHS 单账号实例退化为单 Variant/单 Publication；新模型支持其未来多账号扩展）。
- **契约依赖**：消费 ③ Intent / ④ Target Account（production_requirements）/ ② Channel Account；执行经 Capability·Connector；被 ⑨ Bottleneck Candidate 间接观测。
- **本 Batch 纪律**：不 Frozen、不 UI / Runtime / Connector。

---

*本文件为 APPROVED CANDIDATE（已应用 DELTA C1），**仍未 Frozen**。Frozen 需待 Authority Consolidation Review。*

---

*CONTENT GROWTH CONTRACT BATCH C — APPROVED CANDIDATE*
