# Curis · Lightweight Queue / Bottleneck Candidate Contract Candidate

> **状态**：**APPROVED CANDIDATE**（Batch C — Runtime Observation；仍不 Frozen）
> **修订**：已应用 **DELTA C2 — Bottleneck ≠ 一定缺员工**（`possible_cause` 可为 UNKNOWN；`suggested_action` 收敛为 4 个最小候选；禁止 AI 编造原因；CEO 侧不暴露工程指标）
> **类型**：Company OS Shared（运行层观测；跨域，不限于 Content Growth）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 9）、`Curis_Responsibility_Requirement_Contract_Candidate.md`（契约 ⑥，观测对象）、`Curis_Shared_Employee_Service_Relation_Contract_Candidate.md`（契约 ⑧，availability 来源）、`Curis_Content_Growth_Company_Evolution_Model.md`（§5 Runtime Facts → Bottleneck Candidate → 一键增员）、`Curis_Organization_Routing_Architecture.md`（§6 DELTA 3 降复杂度）
> **核心判诀**：首版只采集 Runtime Facts → Bottleneck Candidate（DELTA 3：降复杂度，不做复杂推断）

---

## 0. 本契约的目的与边界

固化「**首版只观测、不推断**」的运行层机制 —— **Runtime Fact（运行事实）** + **Bottleneck Candidate（瓶颈候选）**。

**核心纠正（DELTA 3 降复杂度）**：
- 首版**只采集观测事实**（queue_depth / oldest_wait / active_count / employee_availability），**不产生** throughput 预测 / capacity score / 智能负载算法 / 企业级 scheduler。
- Bottleneck Candidate 仅是「某 Runtime Fact 越过静态阈值 → 提出一个**候选动作**」的**简单派生**，不是复杂推断引擎、**也不是诊断引擎**。
- 用户**永远只做二选一**（[按建议处理] / [其他方案]），**不设计组织 / 拓扑**。

**核心纠正（DELTA C2 — Bottleneck ≠ 一定缺员工）**：
- Runtime Facts → Bottleneck Candidate 只能证明「**这里可能出现持续阻塞**」，**不能**直接证明「**这里缺员工**」。
- 阻塞的可能来源至少包括：Employee 容量不足 / 短期任务峰值 / Tool·Capability 不可用 / External dependency / Priority conflict / 当前任务异常复杂 / Responsibility 无法获得合适 Executor / **UNKNOWN**。
- 因此 `suggested_action` **不再是唯一的 `ADD_EMPLOYEE`**，而是 4 个最小候选：`WAIT_AND_OBSERVE` / `REBALANCE_EXISTING` / `ADD_EMPLOYEE` / `ESCALATE_FOR_DIAGNOSIS`。
- **事实不足时**：`possible_cause = UNKNOWN`，`suggested_action = ESCALATE_FOR_DIAGNOSIS` 或 `WAIT_AND_OBSERVE`。**禁止让 AI 编造原因**。
- **不建设复杂诊断引擎**；仅保留「可能原因 / 未知」这一语义位。

本契约只定义对象语义 / 关系 / 归属 / 生命周期 / 必填·可选 / 不变量 / 跨对象引用 / 失败·未知 / 场景验证。**不进入** DB table / SQL / ORM / API / frontend state / 实现类 / migration / **不开发 Runtime 观测系统本身**（仅定义其产出对象的语义）。

---

## 1. Runtime Fact（Company OS Shared · 仅观测）

### Object semantics
对**某个 Responsibility** 在某一时刻的**原始运行观测值**（point-in-time snapshot）。它**是事实，不是推断**；不携带结论。

### Identity
- `fact_id`
- `responsibility_id`（FK → 契约 ⑥ Responsibility Requirement）
- `observed_at`（观测时刻）
- `office_id?`（可选作用域；责任跨 Office 时可聚合，不强制 per-Office 隔离 —— 见 Invariant #3）

### Composition（观测维度 · 仅采集）
- `queue_depth`（该责任当前排队深度）
- `waiting_since` / `oldest_wait`（最旧任务等待起始 / 持续时长）
- `active_count`（在制数量）
- `employee_availability`（相关 Employee 可用性，引用契约 ⑧）

### Required / Optional information
**必填**：`responsibility_id` + `observed_at` + 至少一项观测值
**可选**：`office_id` / 其余观测维度

### Relationships
- `Runtime Fact *—1 Responsibility Requirement`（观测对象，契约 ⑥）
- `Runtime Fact → Employee availability`（引用契约 ⑧ 的 availability）
- `Runtime Fact → Bottleneck Candidate`（越过阈值时派生）

### Ownership
- 属 Company OS Shared（运行层观测）；**跨域**，不限于 Content Growth。

### Lifecycle
- **OBSERVED**（快照）→（瞬时，可被再次观测）。Fact 是点观测，不持持久 Workflow 状态。

### Invariants（硬约束）
1. **Fact 是事实非推断**：仅原始观测值，不含预测/评分/建议。
2. **不强制 per-Office 隔离**：Fact 按 Responsibility 聚合（某责任跨多 Office 服务时，可跨 Office 聚合观测），与 DELTA B1（观测负载而非加载上下文）一致。

---

## 2. Bottleneck Candidate（Company OS Shared · 简单派生）

### Object semantics
当某 Runtime Fact **越过静态阈值**时派生的**瓶颈候选** —— 它只主张「**这个责任环节可能出现持续阻塞**」，**不主张原因**、**不主张一定缺员工**（DELTA C2）。它是观察的下游，**不是调度决策，也不是诊断结论**。

### Identity
- `candidate_id`
- `affected_responsibility`（= `responsibility_id`，FK → 契约 ⑥；**唯一受影响主体**）
- `signal`（哪个 Fact 越界，如 `oldest_wait`）

### Composition（DELTA C2 最小字段集）
- `signal`（触发信号：哪个 Runtime Fact 越界）
- `observed_since`（该信号**持续**越界的起始时刻 —— 用于区分「短期峰值」与「持续阻塞」）
- `affected_responsibility`（受影响责任）
- `possible_cause`：`EMPLOYEE_CAPACITY` / `SHORT_TERM_SPIKE` / `TOOL_OR_CAPABILITY_UNAVAILABLE` / `EXTERNAL_DEPENDENCY` / `PRIORITY_CONFLICT` / `TASK_COMPLEXITY` / `NO_ELIGIBLE_EXECUTOR` / **`UNKNOWN`**
  - **UNKNOWN 是合法且默认的取值**；事实不足时**必须**取 UNKNOWN，**禁止编造**（Invariant #7）
- `suggested_action`（**首版仅 4 个候选**）：
  | 动作 | 含义 | 典型触发 |
  |------|------|----------|
  | `WAIT_AND_OBSERVE` | 先观察一段时间，不动组织 | 信号刚越界 / 疑似短期峰值 / 原因 UNKNOWN |
  | `REBALANCE_EXISTING` | 在**现有** Employee 之间重新分派 | 有可用同责任 Employee 且未满负荷 |
  | `ADD_EMPLOYEE` | 增加一名承担该责任的 Employee | 证据充分：持续积压 + 现有 Employee 长期满负荷 |
  | `ESCALATE_FOR_DIAGNOSIS` | 升级人工/CEO 判断，不自行归因 | 原因 UNKNOWN 且持续越界 / Tool·外部依赖疑似 |
- `threshold_breach`（是否越界 / 简单严重度；静态规则）
- （可选）`office_id?` 作用域提示

### Required / Optional information
**必填**：`affected_responsibility` + `signal` + `observed_since` + `possible_cause`（可为 UNKNOWN） + `suggested_action`
**可选**：`office_id` / `threshold_breach` 细节

### Relationships
- `Bottleneck Candidate *—1 Responsibility Requirement`（契约 ⑥）
- `Bottleneck Candidate → CEO Assistant 白话建议`（→ P7 CEO Decision Package；用户二选一 [按建议处理] / [其他方案]）
- `Bottleneck Candidate → Routing Pool / Capacity 更新`（**仅当** `suggested_action = ADD_EMPLOYEE` 且用户接受：Employee 创建 + 入池 + Capacity 更新 + Responsibility 指派）
- `Bottleneck Candidate → 契约 ⑧ Responsibility Assignment`（**仅当** `REBALANCE_EXISTING` 且用户接受：在现有 Employee 间调整分派，**不新建 Employee**）
- `Bottleneck Candidate → 契约 ⑦ Organization Routing`（仅感知；Routing 逻辑不被 Bottleneck 改变）

### Ownership
- 属 Company OS Shared（运行层观测派生）；跨域。

### Lifecycle
- **DETECTED**（阈值越界）→ **SUGGESTED**（CEO Assistant 白话 + 二选一）→ **ACCEPTED**（按 `suggested_action` 执行）/ **DISMISSED**（用户选其他方案）
- `WAIT_AND_OBSERVE` 被接受时：候选进入 **OBSERVING**（继续观察，不动组织）；越界缓解则自然关闭，持续则可再次 SUGGESTED（可能升级动作）。
- 若 DISMISSED：候选关闭；系统**不破坏式降级**，可后续再次 DETECTED。
- **无独立复杂状态机**：以上仅表达「发现 → 建议 → 处理/搁置」，不构成调度 Workflow。

### Invariants（硬约束 · DELTA 3 + DELTA C2 最小集）
1. **观测非推断引擎**：Runtime Fact 是原始指标；Bottleneck Candidate 是**简单阈值越界**，不是 throughput 预测 / capacity score / 智能负载 / 企业级 scheduler。
2. **DELTA C2 — Bottleneck ≠ 缺员工**：Candidate 只能主张「**可能出现持续阻塞**」，**不得**默认归因为「缺员工」。`ADD_EMPLOYEE` 仅是 4 个候选动作之一，**不是默认值**。
3. **不改动路由**：检测是观测/建议；Organization Routing（契约 ⑦）仍确定性运行，Bottleneck 只触发建议，不改变路由逻辑。
4. **用户决策是二选一，非组织设计**：CEO Assistant 白话 + [按建议处理] / [其他方案]；用户**永不设计组织/拓扑**。
5. **拒绝即非破坏（non-destructive）**：用户选 [其他方案] → 候选关闭；**不自动降级生产 / 不破坏式丢弃队列**；若越界持续可再次检测。
6. **多瓶颈独立处理**：多个责任同时越界 → 各自独立 Candidate；无跨 Candidate 编排（DELTA 3）。
7. **DELTA C2 — 禁止编造原因**：`possible_cause` 只能取枚举内值；**事实不足必须取 `UNKNOWN`**，并配 `ESCALATE_FOR_DIAGNOSIS` 或 `WAIT_AND_OBSERVE`。**禁止** AI 生成自由文本归因、禁止把猜测写成结论。
8. **DELTA C2 — 不建诊断引擎**：`possible_cause` 只是一个语义位，由**简单事实规则**填充（如「Tool 调用连续失败 → TOOL_OR_CAPABILITY_UNAVAILABLE」）；**不实现**根因分析 / 依赖图推理 / 归因模型。
9. **DELTA C2 — CEO 侧不暴露工程信息**：`queue_depth` / `oldest_wait` / `capacity` / `routing` / `bottleneck score` / `possible_cause` 枚举 / `suggested_action` 枚举等**内部语义禁止直接呈现给 CEO**。对外只允许 **Frozen P7** 语义的白话叙述 + 二选一（见 §2b）。
10. **DELTA C2 — 观测不加载业务上下文（承 DELTA B1）**：Fact/Candidate 只看负载与可用性，**不加载** Office 资料 / 账号历史 / 业务全文。

### Cross-object references
- → **契约 ⑥ Responsibility Requirement**（观测/派生对象）
- → **契约 ⑧ Employee / Assignment**（availability 来源；增员目标）
- → **契约 ⑦ Organization Routing**（感知，不改逻辑）
- → **P7 CEO Decision Package**（建议投递；用户二选一）
- → **Batch B Context Assembly（Future Company OS Shared Candidate）**：无关（上下文装配是另一候选能力，不在此契约）
- → **Runtime / Connector**：本契约**不定义**观测系统实现（仅定义其产出对象语义）

### Failure / Unknown semantics
- **阈值未校准 / 未知**：首版用**静态规则**（简单常量）；自适应基线留未来。未校准时不做推断，仅记录 Fact。
- **原因无法判断（DELTA C2 主路径）**：`possible_cause = UNKNOWN` + `suggested_action = ESCALATE_FOR_DIAGNOSIS`（持续越界）或 `WAIT_AND_OBSERVE`（刚越界/疑似峰值）。**不编造原因**，CEO 侧白话须显式表达不确定（例：「也可能是近期任务集中造成的」）。
- **用户选择「其他方案」**：Candidate DISMISSED；队列保持现状；无破坏式动作；越界持续则再检测。
- **多 Candidate 并发**：各独立处理，无跨 Candidate 协同（DELTA 3）。
- **处理后仍未缓解**：新 Fact 可能再次触发 Candidate（可能给出不同 `suggested_action`）；系统**不循环自动增员**（每次仍需用户二选一）。
- **Tool·Capability 不可用导致阻塞**：`possible_cause = TOOL_OR_CAPABILITY_UNAVAILABLE` + `ESCALATE_FOR_DIAGNOSIS`；**不得**建议 `ADD_EMPLOYEE`（加人不解决能力不可用）。

### Example scenarios
- **CASE C4（DELTA C2 修正 — 证据不足先观察）**：Subtitle 责任 `oldest_wait` 刚越阈值，`observed_since` 仅 1 天，现有字幕 Employee 并非长期满负荷 → `possible_cause = UNKNOWN`、`suggested_action = WAIT_AND_OBSERVE` → CEO Assistant 白话：
  > 「最近有多条视频长时间卡在字幕环节。目前看起来字幕处理能力可能不足，但也可能是近期任务集中造成的。建议先观察一段时间。」
  > [按建议处理] [其他方案]
- **CASE C4b（证据充分 → 增员）**：`observed_since` 已持续一周、现有字幕 Employee `employee_availability` 长期满负荷 → `possible_cause = EMPLOYEE_CAPACITY`、`suggested_action = ADD_EMPLOYEE` → CEO Assistant 白话：
  > 「最近一周字幕任务持续积压，现有字幕员工长期满负荷。建议增加一名字幕员工。」
  > [按建议处理] [其他方案]
- **CASE C4c（能力不可用 → 升级诊断）**：字幕 Tool 连续调用失败 → `possible_cause = TOOL_OR_CAPABILITY_UNAVAILABLE`、`suggested_action = ESCALATE_FOR_DIAGNOSIS`；白话「字幕处理最近多次失败，可能是所用工具出了问题，需要先排查」，**不建议加人**。
- **CASE C4d（现有人力可再平衡）**：同责任另有未满负荷 Employee → `possible_cause = PRIORITY_CONFLICT`、`suggested_action = REBALANCE_EXISTING`；接受后仅调整 ⑧ Assignment 分派，**不新建 Employee**。
- **CASE C5（拒绝非破坏）**：用户 [其他方案] → Candidate DISMISSED；队列保持；无自动暂停；若仍越界，再次 DETECTED 并再建议。
- **CASE C6（per-Responsibility 跨 Office 聚合）**：Subtitle 责任服务 3 Office；Fact 跨 Office 聚合；瓶颈**对责任整体建议一次**，而非每 Office 各一次（与共享 Employee 模型一致，契约 ⑧）。

---

## 2b. 用户侧表达边界（DELTA C2 · Frozen P7 语义）

内部可以有 `possible_cause` / `suggested_action` 等动作语义，但**用户侧必须保持简单**。

| 层 | 允许内容 |
|----|----------|
| **内部（系统/契约）** | `queue_depth` / `oldest_wait` / `active_count` / `employee_availability` / `threshold_breach` / `possible_cause` / `suggested_action` |
| **CEO 可见（P7 白话）** | 一段自然语言叙述（现象 + 可能原因 + 不确定性 + 一个建议）+ **两个按钮** `[按建议处理]` `[其他方案]` |

**禁止呈现给 CEO**：`queue_depth`、`oldest_wait`、`capacity`、`routing`、`bottleneck score`、任何枚举名或分数。

**白话表达要求**：
1. 先说现象（「多条视频长时间卡在字幕环节」）。
2. 再说可能原因，且**证据不足时必须表达不确定**（「也可能是近期任务集中造成的」）。
3. 最后给**一个**建议（对应内部 `suggested_action`，但不暴露枚举名）。
4. 始终二选一，**不让用户理解内部枚举、不让用户设计组织**。

> 语义归属：本节表达形式遵循 **Frozen P7 — CEO Decision Package**，本契约**不新增**决策模式、**不修改** P7。

---

## 3. 归属层

| 对象 | 归属层 |
|------|--------|
| Runtime Fact | Company OS Shared（运行层观测，跨域） |
| Bottleneck Candidate | Company OS Shared（运行层派生，跨域） |

---

## 4. 与现有权威文档的关系

- **P1–P7**：不冲突、不修改。Bottleneck 触发的是 P7 CEO Decision Package 风格的二选一建议，不改责任/员工语义；§2b 的白话表达**沿用** P7，不新增决策模式。
- **DELTA 3（首版降复杂度）**：本契约是 DELTA 3 的契约落地 —— 仅 Runtime Facts + Bottleneck Candidate，不做 throughput/capacity score/智能负载/企业级 scheduler。
- **DELTA C2（Bottleneck ≠ 缺员工）**：`possible_cause` 允许 UNKNOWN，`suggested_action` 收敛为 4 个最小候选（WAIT_AND_OBSERVE / REBALANCE_EXISTING / ADD_EMPLOYEE / ESCALATE_FOR_DIAGNOSIS）；禁止编造原因；不建诊断引擎；CEO 侧不暴露工程指标。
- **DELTA B1**：Fact 观测的是**负载**（queue_depth/availability），**不加载** Office/账号上下文（与契约 ⑧ §2b 一致）。
- **Blueprint / XHS / RD Instance**：不冲突、不改、不变。
- **契约依赖**：观测 ⑥ Responsibility、引用 ⑧ Employee availability；感知 ⑦ Routing（不改）；建议投递 P7。
- **本 Batch 纪律**：不 Frozen、不 UI / Runtime / Connector（仅定义产出对象语义，不实现观测系统）。

---

## 5. 明确不做（DELTA 3 边界）

- ❌ 完整 throughput 预测
- ❌ 复杂 capacity score
- ❌ 智能负载算法
- ❌ 企业级 scheduler
- ❌ 自动再平衡 / 自动暂停 / 自动缩容（`REBALANCE_EXISTING` 是**建议**，须用户接受，非自动执行）
- ❌ 跨 Candidate 编排
- ❌ 自适应阈值基线（留未来；首版静态规则）
- ❌ **复杂诊断引擎 / 根因分析 / 依赖图推理 / 归因模型**（DELTA C2）
- ❌ **AI 自由文本归因**（`possible_cause` 仅枚举 + UNKNOWN，DELTA C2）
- ❌ **向 CEO 暴露工程指标**（queue_depth / oldest_wait / capacity / routing / bottleneck score，DELTA C2）

> 以上均**留待规模增长后演化**，不预设、不在首版建设。

---

*本文件为 APPROVED CANDIDATE（已应用 DELTA C2），**仍未 Frozen**。Frozen 需待 Authority Consolidation Review。*

---

*CONTENT GROWTH CONTRACT BATCH C — APPROVED CANDIDATE*
