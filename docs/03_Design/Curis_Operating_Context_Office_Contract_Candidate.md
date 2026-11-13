# Curis · Office / Operating Context Contract Candidate

> **状态**：APPROVED CANDIDATE（Batch A — Operating Foundation · 经 DELTA A3 修正，未 Frozen）
> **类型**：Content Growth Domain（见 §归属层）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7 / 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 1）、上一轮 `Curis_Content_Growth_Operating_Model.md`（DELTA 1 已落地）
> **本轮修正**：DELTA A3（Operating Context 不升 OS Shared Primitive；Office 直接挂 Company；Operating Context → RESERVED/DEFERRED CANDIDATE）
> **FROZEN 指针（2026-08-16）**：① Office 语义已正式冻结于 `Curis_Content_Growth_Domain_Authority.md` §1.1。本 Candidate 保留作 **Design Record / Reference**，不删除、不覆盖。

---

## 0. 本契约的目的与边界

固化「经营什么」的载体 —— **Office（经营单元 / Operating·Business Context）**。

**核心纠正（DELTA 1 + DELTA A3）**：Office 与 Organization（Department / Team / Employee）**正交**。

- ❌ 禁止表达：`Company → Office → Employee`（组织隶属）。
- ✅ 正确表达（DELTA A3 收敛后）：
  - `Company → Office`（经营层：为谁经营 / 讲什么）
  - `Company → Organization → (Department / Team / Role / Employee)`（组织层：谁在 / 谁承担）
  - `Employee *—* Office`（经 **Responsibility Assignment** 服务关系，非组织隶属 —— 由契约 8 在后续 Batch 固化）
- **Operating Context 不进入本轮契约**（DELTA A3）：原计划的「上层业务容器」属**可能的过早抽象**（为 ECOMMERCE / CONSULTING / GENERAL 等预留），本轮**降为 RESERVED / DEFERRED CANDIDATE**，**不 Frozen 为 Company OS Shared**。若未来真实出现「一个上层 Business Context 需管理多个 Office」，再从真实需求抽象；届时优先检查 Product Blueprint 已有的 **Business / 业务空间（Workspace）** 概念能否承担该上层容器角色，避免重复造概念。

本契约只定义对象语义、关系、归属、生命周期、必填/可选、不变量、跨对象引用、失败/未知语义、场景验证。**不进入** DB table / SQL / ORM / API / frontend state / 实现类 / migration。

---

## 1. Operating Context（RESERVED / DEFERRED CANDIDATE · 本轮不固化）

> **状态：RESERVED / DEFERRED CANDIDATE（不 Frozen、不升 OS Shared Primitive）。** 仅作占位记录，供未来真实需求触发时再设计。

### Object semantics（候选，未批准）
通用**业务线容器**，承载 Company 下的多个 Office。动机：未来非 Content Growth 业务线（电商 / 咨询 / 通用）可能需要一个上层容器。

### 当前处置（DELTA A3）
- **不上升为 Company OS Shared Primitive**。
- Office 本轮**直接挂 Company**（`company_id`），不需要 Operating Context 该层。
- 若未来需要上层容器，优先复用 / 对齐 Product Blueprint 的 **Business / 业务空间** 概念，而非新造 Operating Context。
- 本候选对象**不在 Batch A 任何契约中持久化**；本节约为设计追溯，不进入权威契约。

---

## 2. Office（Content Growth Domain · 经营单元）

### Object semantics
**经营单元** = 一套共同的：
- 经营目标（business_goals）
- 定位（positioning）
- 受众（audience）
- 内容策略（content_strategy）
- Knowledge（knowledge_refs）
- Growth Context（历史表现 / 复盘知识 / 反馈沉淀）
- Account Pool（经 OfficeAccountBinding 绑定的账号集合）

它是「**经营什么**」的载体。

**明确不等于**：
- ❌ 不等于 Platform（不是「抖音 Office」）
- ❌ 不等于 Account（不是「账号 Office」）
- ❌ 不等于 Content Type（不是「视频 Office」）
- ❌ 不等于 Department / Team（不是组织节点；DELTA A3 重申：删除 Operating Context 后，Office 仍是经营单元，**绝不重新变成 Department**）

### Identity
- `id`（全局唯一）
- `company_id`（FK → Company，直接父容器；DELTA A3）
- `name`
- `operating_context_ref?`（**RESERVED**，仅当未来 Operating Context 候选被真实需求触发时才使用；本轮为空）

### Relationships
- `Office *—1 Company`（直接归属 Company；DELTA A3）
- `Office *—* Channel Account`（经 **OfficeAccountBinding**，见契约 2）
- `Office 1—1 default_target_account_set`（引用其 Account Pool 的子集，见契约 4）
- `Office *—* Content Intent`（**弱服务关系**：Intent 可为 Office 服务，但不被 Office 独占拥有；见契约 3）
- `Office *—* Employee`（经 **Responsibility Assignment** 服务关系 —— 由契约 8 在后续 Batch 固化，本契约仅声明该关系存在、不在此定义其结构）

### Ownership
- **经营层**（Business），直接属于 Company，不属于 Organization 层。
- Office 是 Channel Account 的**绑定方**（经 Binding），不是 Account 的「组织所有者」。

### Lifecycle
- `created`（如「AI工具 Office」建立）
- `active`
- `archived`（业务线终止：释放 Account Binding、保留历史内容/Publication；不删除账号）

### Required / Optional information
**必填**：
- `name`
- `company_id`（DELTA A3：直接挂 Company，不再经 Operating Context）
- `business_goals`（或 `positioning`，至少其一表达「经营什么」）

**可选**（长期复用业务语义）：
- `positioning`（定位描述）
- `audience`（受众假设）
- `content_strategy`（内容策略）
- `knowledge_refs[]`（绑定 Knowledge / Brand 文档引用）
- `growth_context`（跨账号/跨平台回流的 Growth Knowledge 摘要）
- `default_target_account_set[]`（默认目标账号集，引用 Account Pool 子集）

### Invariants（硬约束 · DELTA 1 + DELTA A3）
1. **Office ≠ Department / Team**。Office 不在 Organization 层级内；DELTA A3 删除 Operating Context 后，Office **仍不得重新变成 Department**。
2. **Employee 不隶属于 Office**。Employee 经 Responsibility Assignment **服务** N 个 Office（服务/责任关系，非组织归属）。Office 对象中**不持有 employee 列表**。
3. **Office 不通过外键独占 Channel Account**。账号经 `OfficeAccountBinding` 关联（支持首版 1:1、结构允许 N:N）。
4. Office 可绑定 **1..N** 个 Channel Account（CASE 2 验证）。
5. 同平台不同定位的账号 → **可拆为不同 Office**（CASE 1 验证）；多平台同定位 → **同一 Office 绑 N 账号**（CASE 2 验证）。

### Cross-object references
- → Company（直接父容器；DELTA A3）
- → OfficeAccountBinding（契约 2）
- → default_target_account_set / Target Account Set（契约 4）
- → Content Intent（弱服务链接，契约 3）
- → Responsibility Assignment（Employee 服务，契约 8 后续）

### Failure / Unknown semantics
- **全部绑定账号 OAuth 失效**：Office 仍存在，标记 `at_risk`；内容生产暂停（无法发布），但**历史内容/Publication 保留**。不删除 Office。
- **Office archived**：释放 Binding，账号与历史保留。

### Example scenarios
- **CASE 1（同平台不同定位）**：
  - `Office A · AI科普` 绑定 `Douyin · AI科普号`
  - `Office B · 个人IP` 绑定 `Douyin · 个人IP号`
  - 两个 Office 各自独立经营、各自 Account Pool、各自 Growth Context；非「一个抖音 Office 管两个号」。
- **CASE 2（多平台同定位）**：
  - `Office · Curis AI` 绑定 `Douyin · Curis AI`、`XHS · Curis AI`、`Bilibili · Curis AI`、`TikTok · Curis AI`（1 Office，N 账号，统一定位）。

---

## 3. 归属层

| 对象 | 归属层 |
|------|--------|
| Office | Content Growth Domain（直接属 Company 经营层） |
| Operating Context | **RESERVED / DEFERRED CANDIDATE**（不 Frozen、不升 OS Shared；未来若触发，优先对齐 Blueprint Business / 业务空间） |

> Office 是 Content Growth 业务经营对象，不被 Shell / Shared Pattern / Organization 层拥有；直接挂靠 Company。

---

## 4. 与现有权威文档的关系

- **P1–P7（Frozen Shell/Shared）**：不冲突。P1 三层责任语义（Object Owner ≠ Responsibility ≠ Executor）描述的是**责任归属**，Office 是**业务经营对象**；Office 可成为某内容对象的 Object Owner 候选（与 P1 兼容，不修改 P1）。
- **XHS Instance（APPROVED）**：当前 XHS 实例以「小红书运营办公室」为 Workspace + Object Owner，是**单 Office·单 XHS 账号**的退化形态。新模型是其**超集**：未来 XHS Channel Operations Workspace 可服务多个 Office（各绑 XHS 账号）。**当前实例不变**，仅未来纳入方式说明（见 Batch A Review）。
- **Product Blueprint**：Office 是业务经营层概念，直接挂 Company；与 Blueprint「公司 → 部门 → 项目 → 员工」组织层及「业务空间 / Workspace」层级**正交**，不改 Blueprint。若未来需上层容器，优先对齐 Blueprint 的 Business / 业务空间，而非新造 Operating Context（DELTA A3）。

---

*本文件为 Contract Candidate，经 Batch A Review 批准为 **APPROVED CANDIDATE**，未 Frozen。以后续 Batch / Frozen 裁定为准。*

---

*CONTENT GROWTH CONTRACT BATCH A — APPROVED CANDIDATE*
