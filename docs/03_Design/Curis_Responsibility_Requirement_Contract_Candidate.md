# Curis · Responsibility Requirement Contract Candidate

> **状态**：APPROVED CANDIDATE（Batch B — Company OS Responsibility & Routing · 经 DELTA B1 修正，未 Frozen）
> **类型**：Company OS Shared（扩展 Frozen P1；责任词汇属 Content Growth Domain，机制属 OS Shared）
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7（仅扩展 P1）/ 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：`CONTENT_GROWTH_SHARED_CONTRACT_PLAN.md`（契约 6）、`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（P1 三层责任语义，Frozen）、`Curis_Organization_Routing_Architecture.md`（§2 Responsibility Requirement）
> **核心判诀**：Process asks WHAT / Organization decides WHO / Capability determines HOW
> **FROZEN 指针（2026-08-16）**：⑥ Responsibility Requirement 语义已正式冻结于 `Curis_Company_OS_Shared_Authority.md` §1.1。本 Candidate 保留作 **Design Record / Reference**，不删除、不覆盖。

---

## 0. 本契约的目的与边界

固化「**流程只声明责任需求，不绑固定 Employee**」的载体 —— **Responsibility Requirement**。

**核心纠正（继承 DELTA 1/2 与 Frozen P1）**：
- Process 的每个节点声明的是 **WHAT（需要什么责任能力 + 约束）**，**绝不写死 WHO（哪个 Employee）**。
- 本契约 **扩展** Frozen P1 的三层责任语义（Object Owner ≠ Current Responsibility ≠ Current Executor），**不修改**它：Responsibility Requirement 是 P1「Current Responsibility」的**上游声明层**，运行期由 Organization Routing 解析为 Responsibility Holder → Current Executor（即 P1 的 Current Responsibility / Current Executor）。
- 禁止固定 DAG：「字幕永远由员工 X 做」这种硬编码不在本契约表达；路由是运行期按上下文求解。

本契约只定义对象语义 / 关系 / 归属 / 生命周期 / 必填·可选 / 不变量 / 跨对象引用 / 失败·未知 / 场景验证。**不进入** DB table / SQL / ORM / API / frontend state / 实现类 / migration。

## 0.1 Leadership Assignment 适用语义（消费 Current Product Truth）

Department Leader、Business Leader、Workspace Leader / Operating Owner 都是普通 Employee 的 Leadership Role。流程节点、Leader Workstation 与结果回收不得只携带 Employee ID；必须能解析到 `Employee × Role × Scope` Responsibility Assignment。一个 Employee 可承担多个普通或 Leadership Assignment，具体 Conversation 以当前 Assignment Scope 隔离。

---

## 1. Responsibility Requirement（Company OS Shared · 扩展 P1）

### Object semantics
附加在**流程节点**上的**声明式规格**：说明「这一步需要某类责任（responsibility_type）+ 一组匹配约束」，但**不指名具体执行人**。它是设计期/模板期产物，运行期被 Organization Routing 解析为 Holder/Executor。

### Identity
- `responsibility_requirement_id`
- `process_node_id`（声明该需求的流程/任务图节点；运行层概念，本契约只引用其身份）
- `responsibility_type`（责任族枚举，见下）

### Composition（核心字段 —— 均为约束，非执行人）
- `responsibility_type`（责任族，候选）：
  - `TOPIC_RESEARCH`（选题研究）
  - `SCRIPT_WRITING`（脚本）
  - `VIDEO_PRODUCTION`（视频生产）
  - `SUBTITLE_PRODUCTION`（字幕）
  - `CONTENT_REVIEW`（内容审核）
  - `CHANNEL_ADAPTATION`（渠道适配）
  - `ENGAGEMENT_HANDLING`（互动处理）
  - `ANALYTICS_SYNTHESIS`（数据复盘）
- `required_capability`（需要的能力，如「字幕生成」）
- `required_specialty`（专业，如「中文视频字幕」）
- `required_content_type`（VIDEO / NOTE / IMAGE_SET）
- `required_platform_experience`（DOUYIN / XHS / BILIBILI / ...）
- `required_language`（zh-CN / en / ...）
- `account_context`（该责任发生在哪个 Channel Account 的上下文，引用契约 ② 的 Channel Account，用于风格匹配）
- `constraint_severity`（约束严格度：`HARD` 必须满足 / `SOFT` 偏好，路由时作 tie-break）

### Required / Optional information
**必填**：`process_node_id`、`responsibility_type`
**可选**：`required_capability` / `required_specialty` / `required_content_type` / `required_platform_experience` / `required_language` / `account_context` / `constraint_severity` / `override_reason`

### Relationships
- `Responsibility Requirement *—1 Process Node`（由某流程节点声明）
- `Responsibility Requirement → Responsibility Holder (runtime)`（经 Organization Routing 解析，成为 P1 的 Current Responsibility）
- `Responsibility Requirement → Employee/Team 属性`（经 Routing 匹配，契约 ⑧）
- `Responsibility Requirement → Channel Account`（`account_context` 引用，契约 ②；用于 `tone_style` / `language` 风格匹配）

### Ownership
- 属于**流程定义**（Company OS Shared）。它是声明式规格，不是指派、不归属任何 Office 或 Employee。
- 责任**词汇**（responsibility_type 枚举）属 Content Growth Domain；**匹配机制**属 Company OS Shared（供所有 Workspace 复用）。

### Lifecycle
Responsibility Requirement **不是独立 Workflow**，不制造小状态机；其「生命周期」随所附着节点的解析推进：
- **DECLARED**：在流程/模板节点上定义（设计期）。
- **ACTIVE**：流程实例到达该节点，需求生效、待解析。
- **RESOLVED**：Organization Routing 已将其绑定到 Responsibility Holder（→ P1 Current Responsibility / Current Executor）。
- （节点完成后需求随之 FULFILLED，属流程层状态，本契约不单独建模。）
- **Automation by default 保持不变**：声明即生效，解析自动发生，不要求用户逐节点确认。

### Invariants（硬约束）
1. **Requirement ≠ Executor**：Responsibility Requirement **绝不指名具体 Employee**；只声明 capability / specialty / context 等约束。（「Process asks WHAT，not WHO」）
2. **扩展 P1，不修改 P1**：本契约是 P1「Current Responsibility」的**上游声明层**；运行期解析结果写入 P1 的 Current Responsibility / Current Executor。P1 三层语义（Object Owner ≠ Current Responsibility ≠ Current Executor）**完全不变**。
3. **解析是动态的**：绑定到 Holder/Executor 发生在运行期（经 Organization Routing，契约 ⑦），**不在声明期**硬编码。
4. **无固定 DAG**：流程不得编码「字幕永远由员工 X 做」。Requirement 只声明「需要字幕生成」；WHO 每实例由 Routing 求解。
5. **同责任族跨 Office/Account 复用**：一个 responsibility_type（如 SUBTITLE_PRODUCTION）通过 `account_context` 等约束服务多个 Office/Account，**不复制**为「Douyin 字幕责任 / XHS 字幕责任」。
6. **account_context 是匹配键，不是所有权**：它把需求链接到某 Channel Account 的 `tone_style` / `language` 做风格匹配，但不使需求「属于」该账号。
7. **需求解析须触发上下文作用域（DELTA B1）**：Responsibility Requirement 被解析时，其 `process_node_id` / `account_context` 等应作为**任务作用域键**，驱动装配 **task-scoped Context Package**（当前 Office/Account/Object + 仅所需 Knowledge），**而非**全量加载公司资料。需求本身不持有、不预载任何 Office/账号上下文。
8. **需求 ≠ 上下文所有权（DELTA B1）**：Requirement 只声明 WHAT（责任 + 约束 + 作用域键）；它**不**把所服务 Office 的 Knowledge/历史/策略变成 Employee 的永久上下文（见契约 ⑧ §2b Context Isolation）。

### Cross-object references
- → **P1（Frozen）**：运行期解析为 Current Responsibility / Current Executor（扩展，非修改）。
- → **契约 ⑦ Organization Routing**（消费本需求 + Employee 属性，求解 Holder）。
- → **契约 ⑧ Shared Employee Service Relation**（Employee 属性被匹配）。
- → **契约 ② Channel Account**（`account_context` / `tone_style` 风格匹配来源）。
- → **流程 / 任务图**（声明该需求的节点；运行层概念，本契约只引用身份）。

### Failure / Unknown semantics
- **无匹配 Employee（UNFILLED）**：Router 找不到满足 HARD 约束的 Employee（如 required_specialty=「韩语字幕」但无人具备）→ 需求保持 ACTIVE/UNRESOLVED → 升级至 Team Lead 异常路径（契约 ⑦）或 CEO Decision Gate（P7）。**不静默丢弃工作**。
- **歧义匹配（多候选）**：多人均满足 → Router 用确定性 tie-break（capacity / availability / load），**不调用 LLM Team Lead**（DELTA 2）。
- **约束未知**：如 required_platform_experience 对应平台能力为 UNKNOWN → 需求标记缺口；路由可仅按 capability 匹配并附警告，或升级，不静默继续。

### Example scenarios
- **CASE B1（Process 声明 WHAT 非 WHO）**：Content Production 流程在某节点声明 `SUBTITLE_PRODUCTION (required_capability=subtitle_generation, required_language=zh-CN)`。未指名任何人；运行期 Router 选当时空闲的字幕 Employee。
- **CASE B2（同责任族服务多 Office）**：仅一个 `SUBTITLE_PRODUCTION` 责任族，`account_context` 分别 = Douyin Office / XHS Office / Bilibili Office 的账号；**同一字幕 Employee** 经约束匹配服务三者 —— 无需造「Douyin 字幕员工 / XHS 字幕员工」。
- **CASE B3（无固定 DAG）**：字幕 Employee A 不可用时，Router 改派同样具备字幕能力的 Employee B 或标记 Team Lead —— 流程**不**写死「字幕=员工 A」。
- **CASE B4（无匹配→升级）**：`required_specialty=韩语字幕` 但无具备者 → 需求 UNFILLED → Team Lead 异常 / CEO 决策「增加该能力」。

---

## 2. 与 Frozen P1 的衔接（扩展而非修改）

```
Process Node
  → Responsibility Requirement   （本契约：WHAT，声明约束，不指名 WHO）   [新增声明层]
      → Organization Routing      （契约 ⑦：动态求解 WHO）
          → Responsibility Holder → Current Executor   （P1 的 Current Responsibility / Current Executor · Frozen）
```

- P1 的 `Object Owner` / `Current Responsibility` / `Current Executor` 三层语义**原样保留**。
- 本契约仅在 P1 之前插入「声明层」，使「WHO」由运行期求解而非设计期写死 —— 这正是 P4（Automation by default）与 Curis 四原则（员工=动态调用能力的岗位）的体现。

---

## 3. 归属层

| 对象 | 归属层 |
|------|--------|
| Responsibility Requirement | Company OS Shared（扩展 P1；责任词汇属 Content Growth Domain） |

---

## 4. 与现有权威文档的关系

- **P1–P7**：**扩展 P1，不修改任何 Frozen Shared Pattern**。P1 三层语义原样保留；本契约为其上游声明层。
- **Blueprint**：不冲突、不改 Blueprint。
- **XHS / RD Instance**：不变。
- **契约依赖**：被 ⑦ Organization Routing 消费；匹配 ⑧ Employee 属性；`account_context` 引用 ② Channel Account；运行期写入 P1 的 Current Responsibility/Executor。
- **本 Batch 纪律**：不 Frozen、不改 P1–P7、不 UI / Runtime / Connector。

---

*本文件为 Contract Candidate，经 Batch B Review 批准为 **APPROVED CANDIDATE**，未 Frozen。以后续 Batch / Frozen 裁定为准。*

---

*CONTENT GROWTH CONTRACT BATCH B — APPROVED CANDIDATE*
