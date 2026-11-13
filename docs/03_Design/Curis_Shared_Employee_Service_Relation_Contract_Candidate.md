# Curis · Shared Employee Service Relation Contract Candidate

> **状态**：APPROVED CANDIDATE（Batch B — Company OS Responsibility & Routing · 经 DELTA B1 修正，未 Frozen）
> **类型**：Company OS Shared（Employee 实体属 Organization；新增「服务关系」跨轴链接 Office）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 8）、`Curis_Organization_Routing_Architecture.md`（§1 DELTA 1、§4 Employee）、`Curis_Content_Growth_Company_Evolution_Model.md`（§1/§2 两正交轴）、`Curis_Operating_Context_Office_Contract_Candidate.md`（契约 ①，Office 直接挂 Company）
> **核心判诀**：Employee 属 Organization 轴，经 Responsibility Assignment 服务 N 个 Office，不产生固定 DAG / 复杂用户配置
> **FROZEN 指针（2026-08-16）**：⑧ Shared Employee Service Relation 语义已正式冻结于 `Curis_Company_OS_Shared_Authority.md` §1.2。本 Candidate 保留作 **Design Record / Reference**，不删除、不覆盖。

---

## 0. 本契约的目的与边界

固化「**Employee 如何安全地跨多个 Office 服务，而不产生固定 DAG 或复杂用户配置**」的载体 —— **Responsibility Assignment（服务关系）**。

**核心纠正（DELTA 1 正交）**：
- `Employee / Team` 属 Company 的 **Organization** 轴（Company → Organization → Department/Team/Role/Employee）。
- `Office` 属 **Business 轴**（Company → Office，DELTA A3 后直接挂 Company）。
- 二者**正交**：Employee **经 Responsibility Assignment 服务 Office，不隶属于 Office**。Office **不是** Department/Team 节点。
- 一个 Employee **可同时服务 N 个 Office**（如字幕 Employee 服务 Douyin/XHS/Bilibili Office），**不复制**为「Douyin 字幕员工 / XHS 字幕员工」。

本契约只定义对象语义 / 关系 / 归属 / 生命周期 / 必填·可选 / 不变量 / 跨对象引用 / 失败·未知 / 场景验证。**不进入** DB table / SQL / ORM / API / frontend state / 实现类 / migration。

---

## 1. Employee（Company OS Shared · Organization 轴）

### Object semantics
Employee = **动态调用能力的岗位**（Curis 四原则之一），**非固定 Agent**。它是可参与路由匹配的实体，其属性作为 Responsibility Requirement 的匹配键。

### Identity
- `employee_id`（FK → Organization Employee 实体；本契约为引用，不重定义 Employee 实体本身）
- 匹配属性（供 Routing 使用）：
  - `capability`（拥有的能力，如字幕生成）
  - `specialty`（专业，如中文视频字幕）
  - `platform_experience`（DOUYIN / XHS / BILIBILI / ...）
  - `content_type`（VIDEO / NOTE / IMAGE_SET）
  - `language`（zh-CN / en / ...）
  - `style`（风格，可与 Channel Account 的 `tone_style` 匹配）
  - `capacity`（容量：可并行 / 单位时间处理量）
  - `availability`（可用性：在线 / 负载）
  - `organization_membership`（Department/Team，属 Organization 轴，Frozen Organization 管理）

### Composition
- 上述匹配属性为 Employee 的**描述性属性**，由 Organization / 能力层维护；本契约只引用并声明其用于路由匹配。

### Required / Optional information
**必填**：`employee_id` + `organization_membership` + 至少一项 `capability`
**可选**：`specialty` / `platform_experience` / `content_type` / `language` / `style` / `capacity` / `availability`

### Relationships
- `Employee *—1 Organization (Department/Team)`（组织隶属，Frozen Organization 管理，本契约不重定义）
- `Employee *—* Office`（**经 Responsibility Assignment**，非组织隶属 —— DELTA 1 核心）
- `Employee → Responsibility Requirement`（经 Routing 匹配，契约 ⑥）
- `Employee → Capability Provider`（HOW：Agent/Skill/Tool/Connector；Employee 声明能力，不拥有能力，能力层可替换）

---

## 2. Responsibility Assignment（服务关系 · 本契约新增核心）

### Object semantics
一个**轻量跨轴链接**：声明「某 Employee 以哪些 responsibility_types 服务某 Office，分配多少容量」。它是**服务能力/资格声明**，不是组织隶属，也**不是硬路由规则**（WHO 仍由运行期 Routing 逐实例求解）。

### Identity
- `assignment_id`
- `employee_id`（FK → Employee）
- `office_id`（FK → Office，契约 ① CG Domain）
- `responsibility_types[]`（该 Employee 为此 Office 承担的责任族，如 `[SUBTITLE_PRODUCTION, VIDEO_PRODUCTION]`）
- `capacity_share`（分配给此 Office 的容量比例/额度；首版可简化为整段可用性）

### Composition
- `responsibility_types[]`：本 Assignment 覆盖的责任族（引用契约 ⑥ 的 responsibility_type 枚举）。
- `capacity_share`：首版可为简单值（如 `FULL` / 比例），复杂 capacity score 留契约 ⑨ / DELTA 3 范围。

### Required / Optional information
**必填**：`employee_id` + `office_id` + `responsibility_types[]`
**可选**：`capacity_share`

### Relationships
- `Responsibility Assignment *—1 Employee`
- `Responsibility Assignment *—1 Office`
- `Responsibility Assignment → Responsibility Requirement`（声明其可 fulfill 的责任族，供 Routing 匹配）
- 一个 Employee 可拥有 **多个** Responsibility Assignment（分别指向不同 Office）—— 这是「一 Employee 服务多 Office」的载体。

### Ownership
- Employee 属 Organization（Company OS Shared）。
- Responsibility Assignment 是**关系**，不单独「拥有」；其两端分别归属 Organization（Employee）与 Content Growth Domain（Office）。
- Office 本身不被 Assignment 改变结构。

### Lifecycle
- **PROPOSED**：由系统 / Team Lead 建议建立服务关系。
- **ACTIVE**：生效中，Employee 可经此 Assignment 服务该 Office。
- **PAUSED**：临时停止服务（如容量再分配），不删除。
- **REVOKED**：不再服务该 Office（如业务线调整）。
- 首版可仅用 `ACTIVE` / `REVOKED` 两态；关键是**同一 Employee 可同时持有多个 ACTIVE Assignment**（跨多 Office）。

### Invariants（硬约束）
1. **服务关系 ≠ 组织隶属**：Assignment 把 Employee 链接到 Office 提供服务；**不使** Employee 成为 Office 的部门/成员。Employee 始终在 Organization 轴。
2. **一 Employee，多 Office**：单个 Employee **可经 N 个 Assignment 同时服务 N 个 Office**（如字幕 Employee 服务 Douyin/XHS/Bilibili Office）。**禁止**为每 Office 复制 Employee。
3. **无固定 DAG**：Assignment 表达「能服务」，不是「必须永远服务 X 做 Y」。实际 WHO 由运行期 Routing（契约 ⑦）逐实例决定；Assignment 是容量/资格，不是硬编码路由规则。
4. **Office 不被 Assignment 改变**：增删 Assignment 不改动 Office 结构，也不改动 Organization 树。
5. **Employee 能力是声明非拥有**：Employee 引用 capability（Agent/Skill/Tool/Connector）但不拥有；能力层可替换（Curis 四原则）。
6. **org_membership 与 office 服务并存且独立**：Employee 的 Department/Team（组织轴）与其 Office 服务 Assignment（业务轴）是**两正交轴**，可同屏展示但**不得混淆**。
7. **服务关系 ≠ 上下文所有权（DELTA B1）**：Employee 服务 Office A/B/C，**不代表** A/B/C 的全部 Knowledge、历史 Conversation、账号策略**永久进入** Employee 上下文。Assignment 是容量/资格声明，**不是**永久 Context 绑定。
8. **执行期上下文隔离（DELTA B1）**：每次执行只装配 **task-scoped Context Package**（当前 Responsibility + 当前 Office/Account/Object + 当前 Task Inputs + 仅所需 Knowledge/Evidence）。**禁止**全量加载所有服务 Office 的资料、所有账号历史，或因 Employee 共享导致 Office Context 串线。

### Cross-object references
- → **契约 ① Office**（CG Domain，`office_id` 引用；DELTA A3 后 Office 直接挂 Company）
- → **契约 ⑥ Responsibility Requirement**（匹配；`responsibility_types` 引用其枚举）
- → **契约 ⑦ Organization Routing**（消费 Assignment + Employee 属性做匹配）
- → **Frozen Organization**（Employee 实体、Department/Team；本契约不重定义）
- → **能力层**（capability 引用；可替换，不拥有）
- → **Context Assembly**（Future Company OS Shared Candidate；按任务作用域检索 + 装配 task-scoped Context Package；**本轮仅记录候选，不建第 10 契约**，见 Batch B Review）

### Failure / Unknown semantics
- **Employee 不可用**（availability=offline / overloaded）：Assignment 仍 ACTIVE，但 Routing 当前实例跳过该 Employee；**不删除** Assignment。
- **Assignment 指向不存在的 Office**：拒绝建立（`office_id` 必须引用有效 Office）。
- **容量冲突**（Employee 跨 Office 过度分配）：首版 = 简化整段可用性；Bottleneck Candidate（契约 ⑨）可建议再平衡或增员；**不做**自动复杂再分配（DELTA 3）。
- **责任族无对应能力**：Assignment 声明的 `responsibility_types` 须有 Employee 属性支撑，否则 Assignment 建立时被拒或标记缺口。

### Example scenarios
- **CASE B2（共享 Employee）**：Subtitle Employee A 持有分别指向 Office Douyin / Office XHS / Office Bilibili 的 3 个 Assignment —— 一个 Employee，三个 Office，**无复制**。
- **CASE B3（无固定 DAG）**：Employee A 过载时，Router 把字幕工作改派同样持字幕 Assignment 的 Employee B，或标记 Team Lead；Assignment「A 服务 XHS」**不**把 XHS 字幕强制绑死到 A。
- **CASE B5（组织 vs 服务正交）**：Employee A 在 Organization 属「Production Department / Subtitle Team」（`organization_membership`），同时经 Assignment 服务 Office Douyin/XHS。撤销一个 Assignment **不**把 A 移出 Subtitle Team。
- **CASE B6（容量再平衡）**：A 同时服务 3 Office 且持续超载 → Bottleneck Candidate 触发 → CEO Assistant 白话建议「增加一名字幕员工」→ 用户二选一，不要求用户设计组织。

---

## 2b. Context Isolation（DELTA B1 — Shared Employee ≠ Shared Context）

**边界铁律（语义层，本轮只定义，不设计实现）**：Employee 可跨多个 Office 服务，但**不得因此永久加载这些 Office 的全部上下文**。

### 两类上下文（明确区分）

**Employee Persistent Context（持久上下文 · 稳定、长期）**
- `Role`（岗位）
- `Specialty`（专业）
- `Stable Skills`（稳定技能）
- `Stable Company-level rules`（稳定公司级规则）
- `Stable Tool / Capability bindings`（稳定工具/能力绑定）

**Responsibility Execution Context（执行期上下文 · 瞬时、任务作用域）**
- `Current Responsibility`（当前责任，来自契约 ⑥）
- `Current Office Context`（当前 Office，来自契约 ①）
- `Current Channel Account Context`（当前账号，来自契约 ②）
- `Current Business Object`（当前业务对象，如 Content Intent / Variant / Publication）
- `Current Task Inputs`（当前任务输入）
- `Required Knowledge / Evidence only`（**仅**任务所需的 Knowledge/Evidence）

### 核心原则

> **Employee Service Relation ≠ Context Ownership**
>
> Employee 服务 Office A/B/C，**不代表** A/B/C 的全部 Knowledge、历史 Conversation、账号策略**永久进入** Employee 上下文。

### 每次执行流（语义约束）

```
Responsibility（契约⑥）
  → resolve current Office / Account / Object   （解析当前作用域）
    → retrieve only relevant Knowledge            （仅检索相关 Knowledge）
      → assemble task-scoped Context Package      （装配任务级上下文包）
        → execute                                 （执行）
```

### 禁止（硬约束 · 对应 Invariant #7/#8）
- ❌ 全量加载所有服务 Office 的资料
- ❌ 全量加载所有账号历史
- ❌ 因 Employee 共享导致 Office Context 串线（如把 Office A 的口播风格混入 Office B 的干货清单）
- ❌ 将 Organization Membership 当成 Knowledge Access（组织隶属 ≠ 知识访问权）
- ❌ 将 Responsibility Assignment 当成永久 Context 绑定

### 目标
1. 降低 Token 消耗
2. 降低上下文污染
3. 防止不同 Office 风格串线
4. 保持账号 / 业务隔离
5. 让成本更多取决于「当前任务复杂度」，而非「公司总资料量」

### Cross-object boundary
- **Context Assembly（上下文装配） = Future Company OS Shared Candidate**：本概念（按任务作用域检索 + 装配 task-scoped Context Package）是 Company OS Shared 的候选能力，但**本轮不新建第 10 个正式 Contract**，仅在 Batch B Review 记录其候选归属。
- 不设计 Context Engine / RAG / Embedding / Vector DB / Runtime（用户明确禁止本轮实现）。

---

## 3. 归属层

| 对象 | 归属层 |
|------|--------|
| Employee（引用 Organization 实体） | Company OS Shared（Organization 轴） |
| Responsibility Assignment（服务关系） | Company OS Shared（跨轴链接；Office 引用来自 CG Domain） |

---

## 4. 与现有权威文档的关系

- **P1–P7**：不冲突、不修改。Employee Presence（P2）/ Handoff（P5）等语义不变；本契约只新增跨轴服务关系。
- **DELTA 1（Office/Org 正交）**：本契约是 DELTA 1 的契约落地 —— Employee 经 Assignment 服务 Office，非隶属。
- **Blueprint**：不冲突、不改 Blueprint（Office 直接挂 Company，与 Organization 树正交）。
- **XHS / RD Instance**：不变。
- **契约依赖**：引用 ① Office；被 ⑦ Routing 消费；与 ⑥ Responsibility Requirement 的 `responsibility_type` 对齐。
- **本 Batch 纪律**：不 Frozen、不 UI / Runtime / Connector、不做 ⑤⑨。

---

*本文件为 Contract Candidate，经 Batch B Review 批准为 **APPROVED CANDIDATE**，未 Frozen。以后续 Batch / Frozen 裁定为准。*

---

*CONTENT GROWTH CONTRACT BATCH B — APPROVED CANDIDATE*
