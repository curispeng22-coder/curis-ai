# Batch B — Contract Review（Company OS Responsibility & Routing）

> **状态**：APPROVED CANDIDATE（Batch B — 经 DELTA B1 修正，未 Frozen）
> **范围**：契约 ⑥ Responsibility Requirement · ⑧ Shared Employee Service Relation · ⑦ Organization Routing
> **纪律**：不 Frozen / 不改 Product Blueprint / 不改 P1–P7（仅扩展 P1）/ 不改 XHS·RD Instance / 不开发 Runtime / 不开发 Connector / 不画 UI
> **前置**：Batch A（① Office / ② Channel·Account / ③ Intent / ④ Target Account，均 APPROVED CANDIDATE）、`Curis_Organization_Routing_Architecture.md`（DELTA 1/2/3 已应用）、`Curis_Content_Growth_Company_Evolution_Model.md`、`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（P1 Frozen）
> **本轮修正**：DELTA B1（Shared Employee ≠ Shared Context：服务关系 ≠ 上下文所有权；执行期 task-scoped Context Package 隔离；Context Assembly = Future Company OS Shared Candidate，不建第 10 契约）

---

## 0. 本轮交付清单

| 文件 | 契约 | 归属层 |
|------|------|--------|
| `Curis_Responsibility_Requirement_Contract_Candidate.md` | ⑥ Responsibility Requirement | Company OS Shared（扩展 P1；责任词汇属 CG Domain） |
| `Curis_Shared_Employee_Service_Relation_Contract_Candidate.md` | ⑧ Shared Employee Service Relation | Company OS Shared（Employee 属 Organization；新增服务关系跨轴链 Office） |
| `Curis_Organization_Routing_Contract_Candidate.md` | ⑦ Organization Routing | Company OS Shared（Router 机制 + Team Lead 异常路径） |
| （本文件） | Batch B Review | — |

---

## 1. 三个契约之间的关系

```
Process Node
  → Responsibility Requirement ⑥   （WHAT：声明责任需求 + 约束，不指名 WHO）
       → Organization Routing ⑦     （WHO：确定性机械调度，求解 Holder）
            → Responsibility Holder → Current Executor   （写入 P1 的 Current Responsibility / Current Executor · Frozen）
                 → Employee / Team  （HOW 由能力层决定；Employee 经 ⑧ 服务 Office）
                      → Capability Provider（Agent/Skill/Tool/Connector，可替换）

Employee（Organization 轴）
  └─ Responsibility Assignment ⑧   （服务关系：employee_id × office_id × responsibility_types[]）
        └─ Office（CG Domain，直接挂 Company · DELTA A3）   ← Employee 经 Assignment 服务，非隶属（DELTA 1）

Team Lead = Employee/Role 实例（非新 primitive）
  └─ Team Lead Exception Path ⑦§2  （仅 Priority Conflict/Blocker/Quality/Exception/Standards/Abnormal Workload）
```

**依赖顺序**（本 Batch 内部）：
- ⑥ Responsibility Requirement 是声明层（WHAT），是基础输入。
- ⑧ Shared Employee Service Relation 定义 Employee 跨 Office 的服务资格（Capacity/Eligibility），提供 Router 的候选池。
- ⑦ Organization Routing 消费 ⑥ + ⑧，确定性求解 WHO，并定义 Team Lead 仅异常的边界。

**三者共同稳定 Batch B 的两大目标**：
1. **Process asks WHAT / Organization decides WHO / Capability determines HOW**（⑥ = WHAT，⑦ = WHO，能力层 = HOW）。
2. **Employee 安全跨多 Office 服务而不产生固定 DAG / 复杂用户配置**（⑧ 服务关系 + ⑦ 动态路由；用户零路由配置）。

---

## 2. Unresolved Questions（待 Review 裁定）

1. **Router 实现形态（规则引擎 vs 轻量 LLM）**
   - 设计定：确定性、低成本、可复现；**每任务不调用 LLM Team Lead**（DELTA 2）。
   - 待裁定：纯规则引擎，还是允许在 Eligibility/Capability 边界用极轻量 LLM 做语义匹配？建议默认纯规则，LLM 仅作可选增强且不影响「确定性」承诺。

2. **Responsibility Requirement 是否按 Content Type 细分约束**
   - 开放问题（契约 6 原问）：VIDEO/NOTE/IMAGE_SET 是否各自需要不同的 `required_*` 子集？本 Batch 建议统一 responsibility_type 枚举 + 可选 `required_content_type` 约束，不在本契约固化细分 schema。

3. **`account_context` 风格匹配的深度**
   - 责任 `account_context` 引用 Channel Account 的 `tone_style` / `language` 做自动风格匹配（SOFT 约束）。
   - 待裁定：风格不匹配时是「降级路由 + 提示」还是「硬阻塞」？本契约定 SOFT（不阻塞），具体阈值留 Runtime。

4. **`capacity_share` 首版计量**
   - DELTA 3 已定首版降复杂度：capacity_share 首版可简化为整段可用性，不做复杂 capacity score。
   - 待裁定：跨 Office 多 Assignment 的过载信号如何汇聚到 Bottleneck Candidate（契约 ⑨，后续 Batch）。

5. **Team Lead 是否本身也经 Router 路由**
   - 本契约定：Team Lead 是 Employee/Role，异常处置任务也可被 Router 派给具备 Lead 角色的 Employee（Invariant 8），不须固定指派。
   - 待裁定：Lead 的「管理判断」任务是否也走确定性 Router（仅候选池限定为 Lead 角色）？建议是。

---

## 3. 是否出现新 Primitive（与 Frozen 兼容检查）

**结论**：引入了**业务/机制对象**，与 Frozen P1–P7 **兼容、扩展（非修改）、不冲突**。

新增对象：
- `Responsibility Requirement`（OS Shared 声明层；扩展 P1 的上游）
- `Responsibility Assignment`（OS Shared 跨轴服务关系；链接 Employee ↔ Office）
- `Organization Router`（OS Shared 机制）+ `Routing Decision`（运行期记录）
- `Team Lead Exception`（异常路径；Team Lead 本身 = Employee/Role，**非新 primitive**）

**它们不是**：
- 新的 Shell 原语（Pane/Search/Toggle 不变）
- 对 P1–P7 的修改 —— P1 三层语义（Object Owner ≠ Current Responsibility ≠ Current Executor）**原样保留**；本 Batch 仅在 P1 之前插入「声明层（⑥）+ 求解层（⑦）」，使 WHO 运行期求解。
- 新的 Organization 原语 —— Employee/Team/Department 不变；Assignment 是关系而非新组织节点。

> 即：本 Batch 把「Process 只声明 WHAT、Organization 动态求解 WHO」从架构草案（Organization Routing Architecture）**固化为契约**，机制层完全叠加在 Frozen Shared Pattern 之上，不改任何既定义。

---

## 4. 与现有 Blueprint / P1–P7 的冲突检查

| 权威文档 | 冲突？ | 说明 |
|----------|:------:|------|
| **P1 三层责任语义** | 无（扩展） | ⑥ 是 P1「Current Responsibility」的上游声明层；⑦ 运行期解析为 P1 的 Current Responsibility/Current Executor。P1 三层定义**不变**。 |
| **P2 Employee Presence** | 无 | 员工在责任上的 Presence 仍由 P2 表达；本 Batch 不改 Presence 语义。 |
| **P3 System Activity** | 无 | Routing Decision 是运行期记录，性质接近 P3 派生；不重定义。 |
| **P4 Automation by default** | 无 | 路由自动发生，仅升级（Decision Gate）需人介入，符合 P4。 |
| **P5 Handoff** | 无 | 责任交接在 Employee 层；Team Lead 介入属 P5/P7 异常延伸，不改定义。 |
| **P6 Result Reference** | 无 | 结果引用机制不变。 |
| **P7 CEO Decision Package** | 无 | 路由无匹配时升级至 P7，结构不变；仅领域内容新增。 |
| **Product Blueprint** | 无 | Office 直接挂 Company（DELTA A3），与 Organization 树正交；Employee 经 Assignment 服务 Office 不隶属，不改 Blueprint。 |

**结论**：Batch B 三个契约**扩展（非修改）P1、不冲突、不修改**任何 Frozen 文档、不改 Blueprint。

---

## 5. 对 XHS / RD 当前实现的影响

**结论**：**ADDITIVE，非破坏性**。当前 XHS / RD Instance（APPROVED）不变。

- 当前 XHS Instance = 单 Office·单 XHS 账号退化形态；其「全能 AI 员工」在 Batch B 模型下可解读为：一个具备多 responsibility_types 的 Employee，经单一 Assignment 服务该 Office。
- 当前 RD Instance 同理：其专业化 Employee/Team 经 Assignment 服务 RD Office；Batch B 不改动已 Approved 的 Calendar/Note/Analytics 等专业能力。
- 未来若某 Instance 扩展为多 Employee / Team，**仅需**在该 Instance 内接入本 Batch 的 Responsibility Requirement + Assignment + Routing 契约，不改变已 Approved 的专业能力集合。

---

## 6. 五场景验证覆盖（Batch B 目标）

| 场景 | 验证的契约 | 结论 |
|------|-----------|------|
| CASE B1 确定性指派（无 Team Lead） | ⑥ + ⑦ + ⑧ | 字幕需求(zh-CN) → Router 选空闲字幕 Employee → 指派 ✅ |
| CASE B2 同责任服务多 Office（无复制） | ⑧ + ⑥ | 一个 SUBTITLE_PRODUCTION + `account_context` 多 Office → 同一 Employee 服务三者 ✅ |
| CASE B3 无固定 DAG（动态改派） | ⑦ + ⑧ | A 过载 → Router 改派 B / 标记 Lead，不写死「字幕=A」 ✅ |
| CASE B4 无匹配→升级（非静默丢弃） | ⑥ + ⑦ | 韩语字幕无具备者 → UNFILLED → Team Lead/CEO 决策增能力 ✅ |
| CASE B6 Team Lead 仅异常（非每任务） | ⑦ + ⑨(后续) | 积压(Abnormal Workload) → Team Lead 干预/建议增员，非每任务 ✅ |

**两大目标校验**：
- 「Process asks WHAT / Organization decides WHO / Capability determines HOW」→ ⑥(WHAT) + ⑦(WHO) + 能力层(HOW) 稳定表达 ✅
- 「Employee 安全跨多 Office 服务而不产生固定 DAG / 复杂用户配置」→ ⑧(服务关系) + ⑦(动态路由)，用户零路由配置 ✅

---

## 7. DELTA B1 — Shared Employee ≠ Shared Context（Review 批准补充）

**结论**：三份契约主方向 APPROVED WITH ONE DELTA。DELTA B1 已在 ⑥ / ⑧ / ⑦ 中落地。

**核心语义边界（仅定义，不实现）**：
- **Employee Persistent Context**（稳定长期）：Role / Specialty / Stable Skills / Stable Company-level rules / Stable Tool·Capability bindings。
- **Responsibility Execution Context**（瞬时任务作用域）：Current Responsibility / Current Office / Current Channel Account / Current Business Object / Current Task Inputs / Required Knowledge·Evidence only。
- **原则**：`Employee Service Relation ≠ Context Ownership`。Employee 服务 Office A/B/C，**不代表** A/B/C 全部 Knowledge/历史/策略永久进入 Employee 上下文。
- **每次执行流**：Responsibility → resolve current Office/Account/Object → retrieve only relevant Knowledge → assemble task-scoped Context Package → execute。
- **禁止**：全量加载服务 Office 资料 / 全量加载账号历史 / Office Context 串线 / 将 Organization Membership 当 Knowledge Access / 将 Responsibility Assignment 当永久 Context 绑定。
- **目标**：降 Token / 降上下文污染 / 防风格串线 / 保账号业务隔离 / 成本取决于任务复杂度而非公司总资料量。

**落地位置**：
- 契约 ⑧ §2b Context Isolation（专节）+ Invariant #7/#8（核心定义）。
- 契约 ⑥ Invariant #7/#8（需求解析触发任务作用域，需求 ≠ 上下文所有权）。
- 契约 ⑦ Invariant #7/#8（路由同步解析作用域、不造成串线）。

**Context Assembly 候选归属**（用户明确）：
- `Context Assembly`（按任务作用域检索 + 装配 task-scoped Context Package）= **Future Company OS Shared Candidate**。
- **本轮不新建第 10 个正式 Contract**；仅在 Batch B Review 记录其候选归属，待后续 Batch / Frozen 裁定时再决定是否独立契约化。
- 明确不做：Context Engine / RAG / Embedding / Vector DB / Runtime（本轮仅语义边界）。

---

## 8. 状态与下一步

**当前状态**：`CONTENT GROWTH CONTRACT BATCH B — APPROVED CANDIDATE`（未 Frozen）

**Review 结果**：总体 APPROVED WITH ONE DELTA。DELTA B1（Shared Employee ≠ Shared Context）已应用到 ⑥ / ⑧ / ⑦ 三份契约（服务关系 ≠ 上下文所有权 + 执行期 task-scoped Context Package 隔离 + Context Assembly 记为 Future Company OS Shared Candidate，不建第 10 契约）。三份契约均升 **APPROVED CANDIDATE**。

**下一步（已批准）**：
1. 进入 **Batch C**：契约 ⑤ Content Variant / Publication（消费 Batch A 的 Target Account Set，定义账号级变体与发布真相源）、契约 ⑨ Lightweight Queue / Bottleneck（观测 ⑥/⑧，贯穿运行）。
2. 仍按当前计划**只做契约设计**：不 Frozen、不开发 Runtime / Connector、不画 UI。
3. 将 ⑨ 个契约归并到 **Company OS Shared Contract Set** 与 **Content Growth Domain Contract Set** 两份权威契约文档，再视成熟度 Frozen。

*本文件为 Batch B Review，未 Frozen。以 Review 批准后的修订版为准。*

---

*CONTENT GROWTH CONTRACT BATCH B — APPROVED CANDIDATE*
