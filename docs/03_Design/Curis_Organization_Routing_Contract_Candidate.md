# Curis · Organization Routing Contract Candidate

> **状态**：APPROVED CANDIDATE（Batch B — Company OS Responsibility & Routing · 经 DELTA B1 修正，未 Frozen）
> **类型**：Company OS Shared（通用路由引擎；Team Lead 为 Employee/Role 实例，非新 primitive）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 7）、`Curis_Organization_Routing_Architecture.md`（§3 Router、§5 Team Lead、DELTA 2）、`Curis_Responsibility_Requirement_Contract_Candidate.md`（契约 ⑥）、`Curis_Shared_Employee_Service_Relation_Contract_Candidate.md`（契约 ⑧）
> **核心判诀**：Router = 确定性、低成本机械调度；Team Lead 仅异常/管理判断介入（DELTA 2）
> **Authority 取代指针（2026-08-16 Frozen）**：本 Candidate 中 `ROUTING_IS_DETERMINISTIC`（「所有路由永远必须同输入同输出」）表述**已被取代，不再冻结**。正式版本见 `Curis_Company_OS_Shared_Authority.md` §3.3 / §3.4：`ROUTING_IS_POLICY_GOVERNED_AND_EXPLAINABLE`（五项冻结原则）。本 Candidate 保留作 **Design Record / Reference**，不删除、不覆盖。

---

## 0. 本契约的目的与边界

固化「**Organization decides WHO**」的求解机制 —— **Organization Routing（Router）** 与 **Team Lead Exception Path**。

**核心纠正（DELTA 2）**：
- 正常任务路由是 **确定性、低成本** 的机械调度（eligibility / capability / availability / queue / capacity / auto-assignment）。**每任务不得调用 Team Lead 决策**。
- **Team Lead 仅在异常 / 管理判断时介入**（Priority Conflict / Blocker / Quality·Acceptance / Exception Handling / Standards·Coaching / Abnormal Workload Intervention）。
- Team Lead 是 **Employee / Role**（运行层管理角色），**不是新的系统 primitive**。
- 普通用户**不配置任何 Routing Rule**（K 节硬约束）；路由在后台求解。

本契约只定义机制语义 / 输入·输出 / 匹配维度 / 异常路径 / 生命周期 / 不变量 / 跨对象引用 / 失败·未知 / 场景验证。**不进入** DB table / SQL / ORM / API / frontend state / 实现类 / migration。

---

## 1. Organization Router（Company OS Shared · 确定性机械调度）

### Object semantics
一个**确定性解析函数**（机制，非必须持久化对象）：输入 Responsibility Requirement + Account Context + 候选 Employee/Team 属性 + Capacity/Availability，输出 Responsibility Holder → Current Executor（即 P1 的 Current Responsibility / Current Executor）。

### Identity（运行期记录，用于可追溯）
- `routing_decision_id`
- `responsibility_requirement_id`（FK → 契约 ⑥）
- `matched_employee_id` / `matched_team_id`（解析结果）
- `match_dimensions_used[]`（实际命中的匹配维度）
- `decision_basis`（如 `CAPABILITY_MATCH + AVAILABILITY + LOAD_TIEBREAK`）

### Composition（Router Spec）
- **输入**：Responsibility Requirement（契约 ⑥）+ Account Context（契约 ② Channel Account 的 `tone_style`/`language`）+ 候选 Employee/Team 属性与 Assignment（契约 ⑧）+ Capacity/Availability。
- **匹配维度**（候选）：`capability` / `specialty` / `platform_experience` / `content_type` / `language` / `style` / `capacity` / `availability`。
- **确定性规则**（有序，低成本、可复现）：
  1. **Eligibility**：候选须经 Responsibility Assignment 覆盖该 responsibility_type（契约 ⑧），且满足 HARD 约束（capability/specialty/...）。
  2. **Capability match**：满足 required_capability / required_specialty 等。
  3. **Availability**：筛除离线 / 过载 Employee。
  4. **Tie-break**：多人均匹配 → 按 `capacity` / `availability` / `load`（current queue depth）确定性择优；**不调用 LLM Team Lead**。
- **输出**：Responsibility Holder → Current Executor（写入 P1 的 Current Responsibility / Current Executor）。

### Required / Optional information
**必填输入**：Responsibility Requirement + 候选 Employee/Team 池（含 Assignment 与属性）
**可选**：SOFT 约束偏好（作 tie-break 权重，非硬门槛）

### Relationships
- `Router → Responsibility Requirement`（消费，契约 ⑥）
- `Router → Employee/Team 属性 + Assignment`（消费，契约 ⑧）
- `Router → Responsibility Holder → Current Executor`（产出，P1 运行期）
- `Router → Team Lead Exception`（确定性路径失败 / 异常时触发）
- `Team Lead = Employee/Role 实例`（非新 primitive；本身可被 Router 在异常时路由）

### Ownership
- Router 是 Company OS Shared 机制（跨 Workspace 复用）。
- `Routing Decision` 是运行期记录（可追溯；性质上接近 System Activity 的派生记录，P3 范畴，不重定义）。
- Team Lead 属 Organization（Employee/Role）。

### Lifecycle（Routing Decision 记录）
- **PENDING**：需求待解析。
- **RESOLVED**：已绑定 Holder（→ P1 Current Responsibility/Executor）。
- **EXECUTED**：Executor 工作中。
- **ESCALATED**：确定性路径失败 / 异常 → 转 Team Lead / CEO。
- 路由本身是**即时确定性计算**；Decision 记录仅用于可追溯，不制造独立 Workflow。

### Invariants（硬约束）
1. **确定性、低成本**：正常路由是机械调度（eligibility/capability/availability/queue/capacity/auto-assignment），**每任务不调用 LLM Team Lead**（DELTA 2）。
2. **Router ≠ Team Lead**：Team Lead **仅**在异常/管理判断介入（见 §2）；常规 Assignment / Load balancing / auto-assignment 属 Router，Team Lead 不介入每任务。
3. **用户不配置路由**：路由后台求解；普通用户永远不看到/设置 Routing Rule（K 节硬约束）。用户仅见 Office / AI Employee / Current Work / Needs CEO。
4. **无固定 DAG**：路由逐实例动态求解，不写死「Employee X 永远做 Y」。
5. **扩展 P1，不修改**：路由产出 P1 的 Current Responsibility/Current Executor，不改三层语义。
6. **升级而非静默丢弃**：无匹配 → 升级 Team Lead / CEO，需求保持 UNRESOLVED；**不静默丢弃**工作。
7. **路由解析须同步确定上下文作用域（DELTA B1）**：Router 求解 Holder/Executor 时，应**同时解析**当前 Office / Account / Object 作用域，产出 **task-scoped Context Package 引用**（供执行期按需装配），**而非**把 Employee 所服务 Office 的全部上下文加载进 Executor。路由只负责 WHO + 作用域键，不负责全量上下文预载。
8. **路由不造成上下文串线（DELTA B1）**：因 Employee 共享多 Office 而路由分派时，Router 必须按当前实例的作用域键隔离上下文；禁止将 Office A 的 Knowledge/风格混入 Office B 的执行（对应契约 ⑧ §2b Context Isolation）。

---

## 2. Team Lead Exception Path（仅异常 / 管理判断）

### Object semantics
Team Lead 是 **Employee / Role**（运行层管理角色），**不是新 primitive**。正常机械调度由 Router 完成；Team Lead **仅**在以下异常 / 管理判断场景介入：

| 触发（exception trigger） | 含义 |
|---|---|
| `PRIORITY_CONFLICT` | 优先级冲突裁决 |
| `BLOCKER` | 阻塞处理 / 升级 |
| `QUALITY_ACCEPTANCE` | 验收与质量把关 |
| `EXCEPTION_HANDLING` | 异常处置 |
| `STANDARDS_COACHING` | 标准制定与辅导 |
| `ABNORMAL_WORKLOAD` | 异常负载干预（如突发积压） |

### Identity（异常记录）
- `exception_id`
- `trigger_reason`（上表枚举）
- `handled_by`（Team Lead 的 employee_id）
- `resolution`（处置结果）

### Lifecycle
- **TRIGGERED** → **HANDLING** → **RESOLVED**（或再升级至 CEO Decision Package，P7）。

### Invariants（附加于 §1）
7. **Team Lead 不介入常规调度**：上述 6 类之外的常规 Queue/Assignment/Load balancing 一律由 Router 确定性完成。
8. **Team Lead 可经 Router 在异常时路由**：Lead 本身是 Employee/Role，异常处置任务也可被 Router 派给具备 Lead 角色的 Employee，不须固定指派。

---

## 3. 归属层

| 对象 | 归属层 |
|------|--------|
| Organization Router（机制） | Company OS Shared（通用路由引擎） |
| Routing Decision（记录） | Company OS Shared（运行期，P3 派生） |
| Team Lead Exception / Team Lead 角色 | Company OS Shared（Employee/Role 实例） |

---

## 4. 与现有权威文档的关系

- **P1–P7**：不冲突、不修改。路由产出 P1 的 Current Responsibility/Current Executor；Team Lead 介入属 P5 Handoff / P7 CEO Decision 的异常延伸，不改既定义。
- **DELTA 2（Router/Team Lead 分离）**：本契约是 DELTA 2 的契约落地 —— Router 确定性机械调度，Team Lead 仅异常/管理判断。
- **P4 Automation by default**：路由自动发生，不要求用户逐任务确认；仅 Decision Gate（升级）需人介入。
- **Blueprint / XHS / RD Instance**：不冲突、不改、不变。
- **契约依赖**：消费 ⑥ Responsibility Requirement 与 ⑧ Employee/Assignment；产出写入 P1；异常可升级至 P7 CEO Decision Package；Runtime Facts 来自 ⑨ Bottleneck Candidate（后续 Batch）。
- **本 Batch 纪律**：不 Frozen、不 UI / Runtime / Connector、不做 ⑤⑨（⑨ 仅作为后续依赖被引用）。

---

## 5. 场景验证（Batch B 目标）

| 场景 | 验证的契约 | 结论 |
|------|-----------|------|
| CASE B1 确定性指派 | ⑥ + ⑦ + ⑧ | 字幕需求(zh-CN) → Router 选空闲字幕 Employee A → 指派，无 Team Lead ✅ |
| CASE B2 同责任服务多 Office | ⑧ + ⑥ | 一个 SUBTITLE_PRODUCTION 责任族 + `account_context` 多 Office → 同一 Employee 服务三者，无复制 ✅ |
| CASE B3 无固定 DAG | ⑦ + ⑧ | A 过载 → Router 改派 B / 标记 Lead，不写死「字幕=A」 ✅ |
| CASE B4 无匹配→升级 | ⑥ + ⑦ | 韩语字幕无具备者 → 需求 UNFILLED → Team Lead/CEO 决策增能力 ✅ |
| CASE B6 Team Lead 仅异常 | ⑦ + ⑨(后续) | 3 字幕任务积压(Abnormal Workload) → Team Lead 干预再平衡/建议增员，非每任务 ✅ |

**Batch B 目标校验**：
- 「Process asks WHAT / Organization decides WHO / Capability determines HOW」—— 由 ⑥(WHAT) + ⑦(WHO) + 能力层(HOW) 三段契约稳定表达 ✅
- 「Employee 安全跨多 Office 服务而不产生固定 DAG / 复杂用户配置」—— 由 ⑧(服务关系) + ⑦(动态路由) 稳定表达，用户零路由配置 ✅

---

*本文件为 Contract Candidate，经 Batch B Review 批准为 **APPROVED CANDIDATE**，未 Frozen。以后续 Batch / Frozen 裁定为准。*

---

*CONTENT GROWTH CONTRACT BATCH B — APPROVED CANDIDATE*
