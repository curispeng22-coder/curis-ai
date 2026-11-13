# Curis Company OS Shared Authority

## 2026-09-15 — Product Truth Consolidation

Status: Frozen · Authority Class: CURRENT / SHARED PRODUCT AUTHORITY · Disposition: CEO ACCEPTED DECISIONS APPLIED; CONSOLIDATION REVIEW REQUIRED.

§10–18为正式共享产品合同，吸收已批准仲裁与F1/F2 Option A；产品义务不等实现完成。默认输入无需阅读研究稿。仅与本次明确修改冲突的旧句被替代；§7未Frozen扩展及原实现接受等级保持。实现仍读取[CURRENT_STATE](../00_Context/CURRENT_STATE.md)，G1-V～G6-V均NOT RUN。

## 2026-09-10 — Pre-Design-Research structure pointer

Authority Class: CURRENT / FROZEN. Disposition: RECORDED / CURRENT — INCLUDED IN CONTROLLED BASELINE PROMOTION.

设计研究前结构统一消费 [CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md](../01_Product/CURIS_PRODUCT_STRUCTURE_BASELINE_PRE_DESIGN_RESEARCH.md)。本段只登记结构入口：七区、Company → Department → Business → Workspace、原装组织、Employee/责任、Four-Pane、Reading/Working/Operating、Conversation 与 global CEO Assistant 继续按本 Authority；视觉组合不在此冻结，FINAL UI MASTER: **PAUSED — COMPETITIVE DESIGN RESEARCH REQUIRED**。

## 2026-09-09 Phase A.1 — Curis 原装公司经营组织

Authority Class: CURRENT / FROZEN. Disposition: CEO CURRENT DECISION REGISTERED.
依据 [Authority Repair · Phase A.1](../reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md)；仅替代本文件“仅默认部门/员工人数全部未定”的旧边界，其他Phase A与Frozen规则保留。

空间工程部、数据分析部是 **CURIS BUILT-IN COMPANY OPERATING DEPARTMENT / Curis 原装经营部门**，共同属于 **CURIS BUILT-IN COMPANY OPERATING ORGANIZATION**，不是用户Business/Template/Package/Demo。自动物化是实现方式，不是产品身份。
新Company必须有Company/CEO/same Assistant、两原装部门、对应canonical Employee实例、Role/Responsibility/Assignment和合法工作面关系；用户Business可0。没有Provider/Key也创建组织和员工，真实显示需配置/暂不可执行，不伪造绑定。

空间工程六类职责（Leader、行业研究、经营方法/设计翻译、产品/空间设计、搭建、Quality/反馈）从Shared §9.4/Methodology §9恢复；后续可合法兼任/调整Holder，但不能用一人兼任代替fresh六实例。**CEO ROLE DECOMPOSITION已裁决：freshCompany为6个Official Definitions / 6个不同canonical Employee实例，岗位为空间工程负责人、行业研究专家、经营方法专家、空间设计专家、搭建实施专家、质量验证专家**，不得将原型高建/研真/方法/小录/实施/QA当官方员工定义；未恢复“牧人”可定位Authority。
数据分析部**至少1 canonical Company Analyst / 公司经营分析师**，主要工作面为Operating Intelligence。产品称谓“司衡”有历史Blueprint/Accepted来源，可编辑，不是匹配员工的键；UI同名fixture不是实例证据。分析师归属必须由canonical Role/Responsibility/Assignment证明。Business0仍有分析师，诚实说明暂无业务/足够数据。

Official Definition（岗位/责任/推荐能力来源）→ Company Employee Instance（唯一运行真源）→ Assignment/Current Holder（三者不同）。不新增员工系统/表，不将Definition ID永久绑定责任。原装与用户员工共用Detail/Edit、身份/头像/Conversation/能力模型，按现有字段编辑；责任Requirement持续，Holder可合法替换，历史Work/Result不改写。缺Holder展示组织能力缺口。
Organization显示原装团队而非空部门；Talent是扩充，不把已有原装员工当待招聘。空间工程在新业务意图前已存在；模型未配是执行缺口，不要求用户先建团队。
Employee Profile作为官方示范应覆盖身份/Department/Role/职责/服务范围/Work Surface/能力/模型状态/工作/结果/Conversation/可编辑配置；仍Main Workstation+Utility detail，不把Conversation塞入Utility。不得默认暴露runtime refs/JSON。

技术definition ID映射由Phase B先审计复用templates/catalog；若需新canonical Definition primitive/schema则Architecture Review，不能直接建表。人数/岗位拆分已由CEO正式裁决，不再作为Gate；实例姓名可编辑，不能成为identity key。

## 2026-09-09 CEO Phase A — scoped Frozen amendment

Authority Class: CURRENT / FROZEN. Disposition: ACCEPTED.
Decision: [Core Product Authority Repair](../reviews/CURIS_CORE_PRODUCT_AUTHORITY_REPAIR.md) §§1–9。下列修订优先于本文件相冲突的旧措辞，其余Frozen规则不变。

- 新Company：Company + CEO identity + same canonical CEO Assistant + 空间工程部 + 数据分析部；用户Business可空，不默认种研发/内容增长/示例业务。两部门是SYSTEM-DEFAULT COMPANY SUPPORT DEPARTMENT；人数、固定Workspace、删除/改名政策UNRESOLVED。
- 空间工程部：理解目标→研究→Operating Model→空间设计→build→quality/test→Team/Workspace交付→演化。Leader持续领导；only-on-exception只约束WHO路由。
- 数据分析部负责Company/cross-Business分析、Report与Decision support；Company Analyst以canonical Responsibility/Assignment证明，禁止role文本推断。业务Allocation不改变functional department identity。
- Company→Department→Business→Workspace。Business是持续经营身份，不只是分类标签；Project为可选域/兼容对象，不是Business。
- Generic是真实可经营环境；Professional是稳定专业方法/工具/语义下的目标形态，不是所有长期Workspace强制前置。旧§9“长期Workspace必须Professional”及§9.5终态普遍约束解释SUPERSEDED；真实团队/责任承载不取消。
- 内容增长/研发是用户启用的业务或专业portfolio，不是默认支持部门。Channel≠Workspace；旧平台Workspace保留兼容，不定义Current Content Growth整体identity。
- §0及§5旧Conversation Continuity隔离解释收窄：Conversation可跨Assignment持续；每条消息与引用保留当时scope，并重新校验当前访问授权。不得因同Employee读全部历史，不得强制拆已验收Conversation。
- CEO Assistant是跨七区、可拖动/收起的global floating utility，同identity/durable conversation，不占Pane；Sidebar是另一canonical quick-access投影，不建新系统。
- 经营启用读Company并优先复用、必要Gate、canonical parent、atomic firstWorkspace、合法团队责任；CEO可直接创建/可委托，不要求DAG。Organization/Business Space需有入口。

本段是CEO显式冲突裁决，不是将实现反推为Authority；实现缺口由Current State及Phase B候选记录。

Status: **Frozen**

Updated: 2026-09-15

Scope: Company OS 跨业务共享语义（适用 Content Growth / RD / 未来客服 / 销售 / 其他 Professional Workspace）

Authority level: **Shared Authority** —— 高于任何 Domain Contract 与 Instance Spec；Domain 与 Instance 只可消费、不可重定义。

### 0.1 CEO Content Growth identity reconciliation（2026-08-24）

`Workspace` 是唯一 canonical user/product identity。Shared Authority 不定义 `Office = Workspace`；历史 Office、`office_id`、OfficeAccountBinding 等仅作为 Domain / implementation / migration provenance 保留，不得成为用户产品层级或新的 Shared primitive。Content Growth 是 Professional Workspace Candidate；XHS / Douyin / TikTok / YouTube / Bilibili 等是 Channel，具体账号是 Channel Account，且 `Channel ≠ Workspace`、`Channel ≠ Channel Account`。全局 Main Contract 保持 `selected Professional Surface + Shared Work Area`，Domain 默认 Surface 由对应 Domain Authority 决定，不反向改变 Shared Main。

---

## 0. 本文件的性质与边界

- 本文件只保留 **Definitions / Relationships / Invariants / Ownership / Truth Boundaries / Cross-domain Rules / Extension Points**。
- **Examples / CASE 验证 / Delta 推理史 / 字段候选 / 平台调查**不在此处，保留于对应 Contract Candidate 与 Consolidation Review（Reference / Design Record）。
- 本文件**不修改** Product Blueprint、Frozen P1–P7 原文、XHS Instance、RD Instance、Runtime、Connector、代码、UI。
- 与 Frozen P1–P7 的关系：**EXTENDS（扩展，不修改）**。

> **跨文档引用（2026-08-17 · 不新增 primitive）**：本 Authority **不定义 Employee UI Status，也不定义 Runtime State Schema**。
> - Employee 的**用户侧 UI Status（`空闲` / `工作中·<desc>` / `阻塞·<cause>`）是 Runtime Truth 的投影**，真源与投影规则定义在 `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` §3.1「Shared Employee UI Status」；现有 Runtime State Schema（`working`/`waiting`/`needs_ceo`/`completed`/`failed`/`idle`）本轮不删不改不迁移。
> - Shared Composer Shell（Shell Contract §3.5）消费的 **Provider Permission 真值（`requested ≠ configured ≠ effective`）** 消费本Authority §13与ADR-0046；旧Candidate技术映射不因此整体冻结。
> - Employee Presence（Shell Contract §3.8）的 Status 口径与 §3.1 Shared Employee UI Status 对齐（不混入 Work/Result 生命周期态）。

## 0A. Three-Layer Operating Model（CEO Accepted 2026-08-20）

Company OS 共享语义按三层分工：`User Surface → Employee Operating Layer → System Runtime`。Company OS 只固定跨业务责任、Truth、Evidence、Decision、Permission、Context 与 Recovery；Domain 方法、Skill、Knowledge、Tool、Connector 与 Package 由 Employee Operating Layer / Provider 侧组合。Runtime 只保证确定性、范围、版本、持久化、幂等、权限与恢复，不解释任何行业应如何经营。

“把这件事交给 Curis”统一进入 Intent → Situation / Capability Discovery → Research / Proposal → 必要 CEO Gate → Reuse / Compose / Acquire / Build → Leader Responsibility → Result / Evidence / Review → Next-cycle Decision。该箭头是责任转译契约，不是固定行业 Workflow。未知能力必须显式 `REFUSE / CANNOT OPERATE YET`，不得由 Domain 或 Provider 在 Core 中伪造成熟能力。当前不创建 Playbook、Method Runtime 或行业 Workflow Engine。

## 0B. Brand Neutrality（CEO Accepted 2026-08-20）

`Curis` 是用户可见的当前品牌，不是 Company OS、Business、Workspace、Operating Lifecycle、Capability 或 Runtime 的 canonical semantic。User Surface 可使用品牌文案；Employee Operating Layer 与 System Runtime 使用品牌中立的产品语义和稳定 canonical IDs。Rebrand 只应影响 Brand Configuration、UI copy、Logo/Icon、App metadata 与外部展示身份，不重建 Company / Business / Workspace 关系，不重新生成历史 Result / Evidence / Decision 引用。`curis.*` 等技术 namespace 不因该原则机械迁移；本文件不授权代码、Schema、DB 或批量 rename。

## 0.1 Leadership / Responsibility Assignment（2026-08-19 产品语义同步）

Leader 是 system-defined responsibility role，不是 Employee Type，也不等同于 Admin 或 System Permission。Department Leader、Business Leader、Workspace Leader / Operating Owner 都由普通 Employee 通过 `Employee × Role × Scope` 的 Responsibility Assignment 承担；同一 Employee 可同时承担多个普通 Role、Leadership Role 和多个 Workspace / Business Scope，Employee Identity 不复制。

Assignment 是产品责任承载：`Role Definition → Responsibility → Employee Binding → Responsibility Assignment`。Conversation、工作和 Result 默认路由到 Assignment，而不是裸 Employee；同Employee可多topic，Conversation可跨Assignment持续；各消息与引用保留真实Scope并校验当前访问权限，不以隔离为由强制复制或切断Conversation。Leader 的组织协调责任不绕过既有 Permission / Decision Gate。

Workflow 只描述一轮 Role → Responsibility → Handoff。Result 必须回到 Workspace Truth 与 Workspace Leader 的责任范围，由最低有效责任范围判断继续、调整、升级或等待新目标；Operating Escalation 为 `Employee → Workspace Leader → Business Leader → Department Leader → CEO`，不要求所有 Result 逐级上报或 CEO 逐任务批准。

### 0.2 Autonomous Business Operation boundary（CEO Accepted / Approved Candidate）

Operating Lifecycle 是 Company OS 的薄 Control Plane，位于 CEO Intent / Goal 与既有 Team Operating / Employee execution 之上；不创建第二套 Task、Workflow、Employee 或 Result Runtime。Operating Responsibility 默认持续，但每个 Runtime Cycle 必须 bounded 并 Close；Cycle Close 不等于 Business、Workspace 或 Responsibility 停止。PAUSE 暂停 Operating Series 并要求显式 Resume；STOP 终止当前 Operating Responsibility / Goal Series，只能由 CEO 或事先授权的 terminal policy 触发。

Leader 的自主调整只存在于 Approved Strategy Envelope：hypothesis、tactic、cadence、experiment、resource allocation、Work priority、content / execution mix 与 bounded Plan。Goal、Success Contract、Positioning、Target Audience、Business / Monetization Model、protected Strategy Boundary、material Budget 及高影响/不可逆外部承诺必须进入 CEO Gate。`CONTINUE / ADJUST` 才能产生 exactly one next Cycle；`WAIT / ESCALATE` 保持责任与证据可恢复，不创建未授权运行。

本节只冻结跨域产品语义和边界，不定义 Employee UI Status、Runtime State Schema、表结构或实现算法；实际执行仍消费既有 Assignment / Router / Employee / Result / Evidence / Decision / Handoff。Primary Autonomous E2E 与 Cross-domain Contract Proof 属后续验收证据等级，不在本 Authority 声称已实现。

---

> **HISTORICAL wording — 2026-09-09 scoped supersession：**下述“长期必为Professional”和“Business仅聚合”解释由本日修订替代：Generic合法经营、Professional按专业需要形成，Business是持续经营身份，真实团队责任保留。原记录：本次评审已完成窄范围语义清理，本文件§9上位经营规则为「长期 Workspace = Operating Team + Professional Workspace」，Business是同类Workspace分类/聚合层；渐进工作形态保留；空间工程可委托、非唯一入口。其余§0–§8仅在本日明确裁决处变更。Office仍仅历史隐喻。

## 1. Definitions（Frozen）

### 1.1 Responsibility Requirement（⑥）

业务过程对「**需要何种责任被履行**」的声明。

- Process asks **WHAT**：声明 `responsibility_type` + 约束条件。
- Requirement **永不直接指定 Employee**。
- 是 Frozen P1「Current Responsibility」的**上游声明层**。
- 领域责任词汇（具体 `responsibility_type` 取值）属 **Extension**，不在本 Authority。

### 1.2 Shared Employee Service Relation（⑧）

Employee 与 Workspace / Operating Context 之间的**服务关系**。

- **Employee ∈ Organization**（始终在组织轴）。
- Employee 经 Service / Assignment 关系**可服务多个 Workspace**。
- Assignment 表达「能服务」= 容量与资格，非「必须永远服务 X 做 Y」。

### 1.3 Organization Routing（⑦）

把 Requirement 解析为具体承担者的**机制**。

```
Requirement
  → eligible candidates
  → policy-governed / explainable routing
  → Holder / Executor
```

- Team Lead **only on exception**（异常 / 管理判断）。
- 具体评分算法 / 权重 / 阈值 / LLM 实现属 **Extension**，不在本 Authority。

### 1.4 Context Isolation Truth Boundary

Employee 上下文的两层划分（Frozen）：

| 层 | 内容 |
|---|---|
| **Employee Persistent Context** | Role · Specialty · Stable Skills · Stable Company Rules |
| **Responsibility Execution Context** | Current Responsibility · Current Workspace / Business Context · Current Account Context（若适用）· Current Business Object · Required Knowledge / Evidence only |

---

## 2. Relationships（Frozen）

```
Process
  └─ declares → Responsibility Requirement（⑥）        [WHAT]
                      │
                      ▼
            Organization Routing（⑦）                   [WHO]
              ├─ filters → eligible candidates（依 ⑧ Assignment 的资格/可用性）
              ├─ resolves → Holder / Executor  →  Frozen P1「Current Responsibility」
              └─ escalates → Team Lead / CEO（仅异常，需求保持 UNRESOLVED）
                      │
                      ▼
            Employee（⑧，∈ Organization）               [执行]
              ├─ serves → N × Workspace（经 Service / Assignment）
              └─ references → Capability（可替换，不拥有）  [HOW]
```

- **三层语义**：Process asks **WHAT** / Organization decides **WHO** / Capability determines **HOW**。
- 与 Frozen P1–P7：⑥ 为 P1 上游声明层；⑦ 产出 P1 的 Current Responsibility / Executor；⑧ 新增跨轴服务关系；均为 **EXTENDS**，P1–P7 原文不变。

---

## 3. Invariants（Frozen · 硬约束）

### 3.1 Responsibility Requirement

| ID | 约束 |
|---|---|
| `REQUIREMENT_NAMES_NO_ONE` | Requirement 声明 WHAT，**永不直接指定 Employee**。 |
| `REQUIREMENT_IS_UPSTREAM_OF_P1` | Requirement 是 Frozen P1「Current Responsibility」的上游声明层，不替代、不修改 P1。 |
| `DOMAIN_VOCABULARY_IS_EXTENSION` | 领域责任词汇（`responsibility_type` 取值表）属 Extension，不得硬编码进 Shared 类型。 |

### 3.2 Shared Employee Service Relation

| ID | 约束 |
|---|---|
| `SERVICE ≠ MEMBERSHIP` | 服务关系**不使** Employee 成为 Workspace 的部门 / 成员；Employee 始终在 Organization 轴。 |
| `SERVICE ≠ CONTEXT_OWNERSHIP` | 服务关系**不授予**该 Workspace 的上下文所有权（详见 §5.1）。 |
| `NO_FIXED_DAG` | Assignment 是容量 / 资格，**非**硬编码路由规则；实际 WHO 由 ⑦ 逐实例解析。 |
| `ORG_AND_SERVICE_ORTHOGONAL` | 组织轴（Department / Team）与服务轴（Workspace Assignment）严格正交，可同屏展示，**不得混淆**。 |
| `NO_EMPLOYEE_DUPLICATION` | **禁止**为每个 Workspace 复制同一 Employee。 |

### 3.3 Organization Routing

| ID | 约束 |
|---|---|
| `ROUTING_IS_POLICY_GOVERNED_AND_EXPLAINABLE` | 路由由 Policy 治理且必须可解释（五项原则见 §3.4）。 |
| `TEAM_LEAD_ONLY_ON_EXCEPTION` | **仅约束任务路由层（WHO 解析）**：普通任务由 Organization Routing 自动解析，Team Lead / 人工**仅**在异常或管理判断时手动介入分派，**不参与**每个普通任务的日常路由调度。本 Invariant **不**描述、也**不隐含** Leader 在业务经营层面的参与程度——业务领导力（目标 / 策略 / 协作 / 结果 / 异常 / CEO 沟通）由 §9 规定，与本规则正交。 |
| `NO_SILENT_DROP` | 无合格候选 → 升级 Team Lead / CEO，需求保持 UNRESOLVED，**不静默丢弃**工作。 |
| `NO_PRELOAD_FULL_CONTEXT` | 路由解析时只取 task-scoped 上下文，**不预载**全量 Workspace / 账号资料。 |
| `TEAM_LEAD_IS_NOT_A_PRIMITIVE` | Team Lead 是 Employee / Role 实例，**非**新增 primitive。 |

### 3.4 `ROUTING_IS_POLICY_GOVERNED_AND_EXPLAINABLE` 五项冻结原则

> 本条替代早期候选中过强的 `ROUTING_IS_DETERMINISTIC`（「所有路由永远必须同输入同输出」）。旧表述**不冻结**。

1. **常规 Routing 优先**：优先使用 deterministic · low-cost · structured facts（capability / eligibility / availability）完成解析。
2. **结果必须**：有依据 · 可解释 · 可追溯 · **不随机猜测**。
3. **未来允许（不进 Frozen Authority）**：当多个候选均满足结构化条件时，可由 **Runtime Policy** 使用 score / historical quality / style fit / task semantics / AI-assisted ranking 择一；**这些算法本身不属本 Authority**（见 §7）。
4. **Team Lead 任务路由边界不因此改变**：未来允许 AI-assisted routing，**不得**据此让 Team Lead 重新参与每个普通任务的路由分派；`TEAM_LEAD_ONLY_ON_EXCEPTION` 仅限任务路由层，继续有效，且不影响 §9 规定的业务领导力。
5. **Token 原则**：正常 Routing **不得默认调用 LLM**。AI-assisted routing 只能是未来 Runtime Policy，**不是默认 Shared 机制**。

---

## 4. Ownership（Frozen）

| 对象 | 归属 |
|---|---|
| Employee | Organization（组织轴） |
| Responsibility Requirement | 声明它的 Process |
| Routing 决策（Holder / Executor 解析结果） | Router（机制），非 Process、非 Employee |
| Service / Assignment 关系 | Organization（与 Workspace 双向引用，不构成隶属） |
| Capability | 能力层（Employee 引用而**不拥有**，可替换） |
| Exception 判断 | Team Lead / CEO（仅异常） |

---

## 5. Truth Boundaries（Frozen）

### 5.1 Context Isolation Truth Boundary

**原则**：`Employee Service Relation ≠ Context Ownership`。Employee 服务 Workspace A/B/C，**不代表** A/B/C 的全部 Knowledge、历史 Conversation、账号策略永久进入其上下文。

**每次执行必须**：

```
Responsibility
  → resolve current Workspace / Account / Object
  → retrieve only relevant Knowledge / Evidence
  → assemble task-scoped Context Package
  → execute
```

**禁止（Frozen）**：

- ❌ 服务多个 Workspace = 加载全部 Workspace Knowledge
- ❌ Organization Membership = Knowledge Access
- ❌ Responsibility Assignment = Permanent Context Binding
- ❌ 全量历史 Conversation 默认注入
- ❌ 全量 Account Context 默认注入

**目标**：降低 Token 消耗 · 降低上下文污染 · 防止不同 Workspace 风格串线 · 保持账号 / 业务隔离 · 使成本取决于「当前任务复杂度」而非「公司总资料量」。

### 5.2 WHO 的唯一解析入口

WHO 由 **Organization Routing（⑦）** 解析。Requirement 不决定 WHO，Assignment 不预定 WHO，Domain 不自行分派。

### 5.3 UNKNOWN 是合法事实状态

在本 Authority 覆盖范围内，事实不足时使用 UNKNOWN 是**合法且必须**的表达，**禁止**以推测填充。

---

## 6. Cross-domain Rules（Frozen）

1. Domain（如 Content Growth）与 Instance（如 XHS / RD）**只可消费**本 Authority，**不得重定义** Responsibility / Routing / Employee 服务关系 / Context Isolation 语义。
2. Domain 可提供 `responsibility_type` 词汇与领域约束（Extension），**不得**改变 §3 任何 Invariant。
3. Instance 专业能力**不得**反向提升为 Shared 基线。
4. 任何与本 Authority 冲突的 Domain / Instance / Review 文档，以本 Authority 为准，并须建立修正记录。

---

## 7. Extension Points（**不 Frozen**）

以下属 Extension / Registry / Runtime Policy / Candidate，**明确不在本 Authority 冻结范围**：

| 扩展点 | 归属 |
|---|---|
| `responsibility_type` 领域词汇表 | Domain Extension |
| Routing 算法 / 权重 / 评分 / AI-assisted ranking 实现 | 未来 Runtime Policy |
| LLM Routing 实现 | 未来 Runtime Policy（受 §3.4 原则 5 约束） |
| **⑨ Lightweight Queue / Bottleneck** | **APPROVED SHARED CANDIDATE**（未 Frozen）：`Curis_Lightweight_Queue_Bottleneck_Contract_Candidate.md` |
| Bottleneck 阈值 / 持续窗口 / `possible_cause` 算法 | 未来 Runtime Policy / Configuration |
| Context Assembly Engine（RAG / Embedding / Vector DB / 检索实现） | Future Company OS Shared Candidate（**本轮不建**独立 Contract；§5.1 边界已 Frozen） |

> Extension Points 的演化**不得**违反 §3 Invariants 与 §5 Truth Boundaries。

---

## 8. Reference / Design Record（非 Authority）

以下文档保留为 Reference，**不得**作为 Authority 引用，也**不得**删除或覆盖：

- `Curis_Responsibility_Requirement_Contract_Candidate.md`（⑥）
- `Curis_Shared_Employee_Service_Relation_Contract_Candidate.md`（⑧）
- `Curis_Organization_Routing_Contract_Candidate.md`（⑦；其 `ROUTING_IS_DETERMINISTIC` 表述已由 §3.4 取代）
- `Curis_Lightweight_Queue_Bottleneck_Contract_Candidate.md`（⑨，APPROVED SHARED CANDIDATE）
- `Curis_BATCH_B_CONTRACT_REVIEW.md` / `Curis_BATCH_C_CONTRACT_REVIEW.md`
- `Curis_Company_OS_Shared_Authority_Consolidation_Review.md`（Review Record）

用途：CASE 场景 · Delta 历史 · 设计理由 · 字段候选 · 实现场景 · 后续演化依据。

---

## 9. Business → Workspace → Operating Team（Professional 按需形成 · 上位经营规则 · Frozen）

> 本节为 Company OS 全局经营语义。它高于 Domain / Instance；固定用户经营层级为 Company → Department → Business → Workspace。每个 Business 至少拥有一个实际 Workspace；一个 Business 只有一个 Workspace 也成立。Business 聚合同类 Workspace，Workspace 是独立经营单元。长期 Workspace 由真实 Operating Team 承载。§0–§9 全部 Frozen。

### 9.1 定义（Frozen）

- **Professional Workspace**：长期经营一项业务的完整专业环境，不是一张 Page。一个 Workspace 有一个 canonical Operating Team responsibility boundary、一个 Workspace Leader、多个 Responsibility，并可拥有多个 Professional Surface。
- **Professional Surface**：Workspace 内围绕特定专业对象、判断或工作组织的观察与工作面；不是 Team、Employee、Cycle、Runtime、Session 或新的 Workspace。
- **Operating Team（业务运营团队）**：承载一个长期业务的真实团队，由 Leader + 成员 + 明确职责构成；团队在 Organization 轴，不随办公室创建而虚构。
- **Workspace Leader Workstation**：长期 Professional Workspace 必须有真实 Workspace Leader / Operating Owner 的责任入口；负责人未设置时可以暂存，但不构成完整经营责任承载。具体视觉位置由 Workspace 设计另行确定。

### 9.1A Professional / Generic Workspace 边界（CEO Accepted 2026-08-22）

- **Professional Workspace** 是针对稳定 Domain / Operating Problem 的专业业务应用；Professional 不自动等于 Verified。
- **Generic Workspace** 是 Company OS 通用经营底座上的真实工作环境，适合未知、长尾、临时或缺少成熟专业包的业务；Generic 不是 Demo 或低配占位。
- Product Form（Professional / Generic）、Provenance（Curis Official / Partner / Community / User or AI Generated）与 Assurance（Verified / Candidate / Unverified / Deprecated）分离。Official 不等于 Verified；Generated 默认只能是 Candidate；组合后的 Workspace 需要重新验证。
- 该边界只定义产品形态与质量语义，不创建第二套 Team / Employee / Work / Result / Runtime；Business Configuration 仍归 Business，Professional Workspace 仍负责专业工作方式。
- **Business × Workspace 关系（CEO 2026-08-20 reconciliation）**：Business 是持续经营身份与整体方向，聚合相关Workspace、资源与结果，并且至少拥有一个Workspace；Workspace 是 Business 内的独立经营单元与专业工作环境。Workspace 由真实 Operating Team 承载，但不因此复制团队或 Employee identity；本条只澄清产品阅读顺序，不修改 Runtime / Schema。
- **Workspace / Operating Team Leader（业务 Leader）— 双重语义，必须严格区分**：当前产品在 Workspace Scope 使用 Workspace Leader / Operating Owner；历史“Team Leader”只作为团队语义别名，不构成第四种 Leader。
  - **(a) 业务领导（Business Leadership）**：Leader 持续负责该业务的*目标落地、策略执行、团队协作、结果汇总、异常判断与 CEO 沟通*。这是业务级领导力，要求 Leader 始终在业务中，**绝不能被理解为「平时不参与」**。
  - **(b) 任务路由（Task Routing）**：普通任务的 *WHO 解析* 由 Organization Routing（§3.3 ⑦）自动完成；Leader 仅在异常 / 管理判断时手动介入分派。
  - 两层正交、不冲突：`TEAM_LEAD_ONLY_ON_EXCEPTION`（§3.3）**仅约束任务路由层 (b)**，绝不能被上推解释为「Leader 平时不参与业务经营 (a)」。
- **Team Operating / Workflow 编辑边界**：用户产品语言为“团队运转 / 默认流程”。Workspace 内轻量编辑器表达 Role、Responsibility、Employee Binding、Input、Output、Default Flow、Review、Return；`A → B` 只表示默认下一 Responsibility，不是强制运行序列或任意 DAG 边。Reorder→Default Flow、Responsibility→Responsibility Contract、Employee Binding→scoped Assignment、Input→Context Contract、Output→Result Contract、Save→immutable Operating Definition Version；不形成独立 Workflow Console、自由 DAG / 无限画布或 Runtime / Automation Console。

### 9.2 Invariants（Frozen · 硬约束）

| ID | 约束 |
|---|---|
| `OFFICE_WORKSPACE_TEAM_ONLY_LONG_TERM` | **适用范围边界（最高优先级）**：本规则仅约束长期 Workspace。不得上推为「Curis 所有工作都必须建立 Business / Workspace」。轻量 Conversation、临时 Task、单 Employee 工作、多 Employee 临时 Task Team 都是合法、独立的工作形态，不强制升级为长期业务 |
| `OFFICE_REQUIRES_OPERATING_TEAM` | 每个长期 Workspace 都必须由真实 Operating Team（Leader + 成员 + 明确职责）承载；Business 可以聚合多个独立 Workspace，不要求共享同一 Team；只有 Workspace 没有团队 = 不完整 |
| `TEAM_LEADER_IS_CEO_ENTRY` | Team Leader 是 CEO 对该业务的*主要专业责任*入口（目标 / 策略 / 重大变化）；CEO 默认通过 Leader 经营业务 |
| `TEAM_LEADER_CONTINUOUS_LEADERSHIP` | Leader 在 (a) 业务领导层**持续负责**（目标 / 策略 / 协作 / 结果 / 异常 / CEO 沟通）；`TEAM_LEAD_ONLY_ON_EXCEPTION` 只限 (b) 任务路由层，不得上推到领导力层 |
| `CEO_CAN_DIVE_INTO_EMPLOYEE` | CEO 可随时进入具体员工的工作，与员工直接讨论和调整；不须经 Leader 中转 |
| `CONVERSATION_ANCHORED_TO_WORK` | Conversation 必须围绕真实职责、工作、经营方法和结果运转，不形成独立聊天世界 |
| `LEADER_OWNS_DIVISION_AND_COLLAB` | Leader 负责组织团队和分工；员工之间通过真实工作结果和必要的 Handoff 协作 |
| `TEAM_SKELETON_UNIFIED_UI_DIVERGENT` | 不同业务 UI 可以不同，但团队协作骨架统一（见 Frozen Shell Contract / P1–P7 Shared Patterns） |
| `SPACE_ENGINEERING_REUSES_STRUCTURE_FIRST` | 空间工程以 Operating Intent + Current Company Truth 为输入，先复用已有 Department / Business / Workspace，再按需创建或调整；建设长期 Workspace 时要求真实 Operating Team，Professional 形态仅在稳定专业方法、工具与语义成立时按需采用 |
| `NO_TEAM_NO_SUCCESS` | 没有真实团队承载的长期 Workspace，不得算空间工程完整成功，亦不得通过 Workspace Engineering End-to-End Acceptance |
| `ASSISTANT_AND_LEADER_NOT_EITHER_OR` | CEO Assistant 与 Team Leader **不是二选一入口**；两入口最终进入同一真实 Department Responsibility / Work Context，不得形成两套工作 |
| `ASSISTANT_COORDINATES_NOT_REPLACES` | Assistant 可协调 / 监督 / 汇报 / 升级，但**不能替代**专业部门完成行业研究、经营策略、设计、实施、Quality 等职责 |
| `PROGRESSIVE_WORK_FORMS` | 工作可沿 临时 Conversation / Task → 单 Employee 工作 → 多 Employee 临时 Task Team →（必要时）由真实 Operating Team 承载的长期 Workspace（Generic 或 Professional）渐进；**任一阶段都可合法停止，不强制升级** |
| `SPACE_ENGINEERING_DELEGABLE_NOT_ONLY_ENTRY` | 空间工程部是 Curis 默认核心【专业建设】部门，但**不是**创建 Business / Department / Workspace 的唯一入口；CEO 可自建，也可把新业务建设委托给空间工程部 |
| `ONE_ACCOUNTABLE_TEAM_BOUNDARY_PER_WORKSPACE` | 一个长期 Workspace 只有一条 canonical Operating Team responsibility boundary；团队成员和 Assignment 可以变化，但不能按 Surface 复制团队或形成 Surface-owned Team |
| `SURFACE_DECLARES_RESPONSIBILITY_NOT_EMPLOYEE` | Surface 只声明需要什么 Responsibility；由 `Responsibility Requirement → Organization Routing → Assignment → Employee` 解析 WHO，禁止 Surface 直接绑定 Employee ID |
| `EMPLOYEE_IDENTITY_CROSSES_SURFACES` | Employee 以同一 identity 和 scoped Assignment 跨多个 Professional Surface 工作；切换 Surface 不复制 Employee、Conversation truth 或责任历史 |
| `SURFACE_PROJECTS_SHARED_TRUTH` | Team、Knowledge、Artifact、Work、Result、Evidence、Decision、Learning 继续使用 Company OS 共享 Truth；Surface 只投影与当前专业工作相关的部分 |
| `CYCLE_CAN_CROSS_SURFACES` | 同一 Operating Cycle 可通过 `Work → Result → Evidence → Handoff / new Responsibility → next Work` 跨多个 Surface 连续推进；Surface 边界不切断 Cycle 或另造 Result |
| `NO_SURFACE_RUNTIME` | 禁止新增 Surface Runtime、Surface Agent、Surface Cycle、Surface Result、Surface Session；现有 Runtime 继续拥有 Work、Responsibility、Assignment、Employee、Handoff、Result、Evidence、Cycle、Evaluation、Decision、Learning |

### 9.3 CEO Assistant / Leader / Employee 三层关系（Frozen）

**Leader Responsibility Scope（2026-08-18 Product Architecture Sync）：**Department Leader、Business Leader 与 Workspace Leader 都是普通 Employee 的责任范围投影，不创建新的 Leader Employee 类型或专用 Agent。三者统一使用 Employee Workstation；Department / Business 的持续领导、Handoff、Exception、Decision Request 与 Follow-up 在 Business Space 对应 Work Surface 承载，Organization Center 只维护结构、Role、Staffing 与 Leader assignment。责任默认在最低有效 Scope 处理，只有跨 Scope、资源/策略冲突、无法解决或高风险/不可逆问题才向 `Workspace → Business → Department → Company / CEO` 上移。

**Business / Workspace Goal Semantics（2026-08-18 Product Architecture Sync）：**Business 持有 Business-level Goal / Strategy，负责业务整体方向；每个 Workspace 持有自己的 Workspace-level Goal / Positioning / Strategy，负责独立专业经营。Workspace 不默认共享彼此的 Workspace-level Goal / Strategy，但受所属 Business-level Goal / Strategy 的整体约束；不建立 Default → Override 技术模型。

**On-demand Workspace Engineering（2026-08-18 Product Architecture Sync）：**空间工程读取当前 Company Truth 后提出结构方案，优先复用已有 Department / Business / Workspace，再按需新增或调整；简单组织操作仍归 Organization Center，复杂经营建设才委托空间工程。空间工程不拥有第二套 Organization Truth。

- **CEO Assistant（公司级跨组织协调员工）**：理解 CEO 意图、搜集信息、传达需求、协调 / 监督部门、跟进结果、发现问题、升级异常。它是 CEO 与各部门之间的协调层，不是某业务的专业负责人。
- **两种入口，同一现实**：CEO 可以先和 Assistant 讨论新业务，由 Assistant 把真实工作交给空间工程部；也可以直接找空间工程 Leader。两条入口最终进入**同一个真实 Department Responsibility / Work Context**，不形成两套工作。
- **Assistant 的边界**：可以协调、监督、汇报、升级异常，但**不能替代**专业部门完成行业研究、经营策略、设计、实施、Quality 等职责。
- **Leader 的边界**：是部门 / 业务的专业负责人，负责组织团队和分工；但**不是所有 Conversation 的强制中转**——CEO 可随时直接进入具体 Employee 的真实工作上下文。
- **Employee**：承担具体 Responsibility 的执行者；CEO 可随时进入其 Workstation / Conversation 直接讨论和调整。

### 9.4 空间工程部的组织身份（Frozen）

- **Workspace Engineering / 空间工程部是 Curis 原装经营部门、第一支核心 Department**，不是隐藏 Runtime Service或纯seed。Phase A.1要求物化实际Employee/Role/Responsibility/Assignment；下列六责任允许兼任，不等于已裁决六个Employee定义。旧“默认存在”仅说明materialization方式。
- 它内部第一版至少具有这些固定 Responsibility（具体 Employee 可变化 / 复用；一人可承担多个 Responsibility；这些岗位**不** Frozen 成所有业务通用岗位）：

```text
空间工程 Leader
  → 行业研究（Domain Expert）
  → 经营 / 运营方法
  → 产品 / 空间设计
  → 搭建实施
  → Quality / 验收
  → 交付给新业务 Operating Team
```

- 详细岗位责任链见 Workspace Engineering Methodology §9（该结构只描述空间工程自身，非 Company OS 通用业务团队模板）。

### 9.5 新业务主路径（委托空间工程时的专业路径 · Frozen）

> 这是「CEO 委托空间工程部建设新业务」时的专业路径。它**不是**创建 Business / Department / Workspace 的唯一入口（见 9.6 边界 `SPACE_ENGINEERING_DELEGABLE_NOT_ONLY_ENTRY` 与 9.7 渐进工作形态）。CEO 也可自行创建部门 / 业务 / 团队 / Workspace，或把已有临时团队升级为长期业务。

```text
（CEO 委托 / 系统建议并经确认）
CEO / Assistant
  → 空间工程部承接（Workspace Engineering Department）
  → 空间工程 Leader 与 CEO 澄清需求（目标 / 受众 / 节奏 / 外部结果）
  → Leader 组织 Research / Operating / Design / Build / Quality
  → 同时为该 Business 的 Workspace 组建 Operating Team（Leader + 成员 + 职责）
  → Build Team Handoff（能力 / 责任 / 运行方式交给新业务团队）
  → 新业务 Leader / Operating Team 开始经营
```

- CEO 默认无需管理内部流程，但可随时查看每一步真实员工、Responsibility、进度、Result / Evidence，并进入具体 Employee Conversation 讨论和调整。

### 9.6 边界（Frozen）

- 本规则是 Company OS 全局经营规则，高于 Domain / Instance；不同业务的经营方法、岗位分工、专业 UI 可以不同，但团队协作方式统一。
- **本规则仅约束长期 Workspace 的责任承载**：它不要求每一段工作都建立 Business / Workspace；轻量 Conversation、临时 Task、临时团队都是合法工作形态，且可自然成长为长期 Workspace（见 9.7）。被 Frozen 的是「每个长期 Workspace 必须由真实 Operating Team 承载」；Professional 形态只在稳定专业方法、工具与语义成立时按需采用，Generic 也可长期合法经营。
- **本规则不规定所有业务使用同一套团队岗位**。业务团队的具体角色分工由各自 Domain Expert 的经营方法决定。
- 空间工程团队自身有一套专属岗位结构（§9.4 / Methodology §9），**该结构不是 Company OS 通用业务团队模板**，不得据此强制所有业务采用相同岗位。
- 与 §3（Shared Employee Service Relation / Organization Routing）的关系：§3 定义 Employee ∈ Organization、服务多个 Workspace、Team Lead 仅异常介入*任务路由*；本节在其上补充*业务级领导力与 CEO 入口*、*Assistant / Leader / Employee 三层关系*与*空间工程部身份*这一更高层规则，二者不冲突、不重复、不形成两套工作。

### 9.7 渐进工作形态（Progressive Work Forms · Frozen）

Curis 必须同时支持从「轻量」到「长期经营」的连续工作形态，而【不强制】每一步都升级为 Business / Workspace：

```text
① 临时 Conversation / Task
   → ② 单 Employee 工作
   → ③ 多 Employee 临时 Task Team
   → ④（必要时）由真实 Operating Team 承载的长期 Workspace（Generic 或 Professional）
```

- **任一阶段都可合法停止**：系统不得因「没有建立 Business」而判定工作不完整或强制升级。
- **CEO 可直接发起与操作**：
  - 直接发起临时 Conversation / Task；
  - 直接指定或选择 Employee 工作；
  - 随工作深入增加 Employee，形成临时团队；
  - 自己创建 Department / Business / Team / Workspace；
  - 将已有临时团队升级为长期业务；
  - 或把新业务建设委托给 Workspace Engineering Department。
- **空间工程部是可委托的专业建设路径，而非强制入口**：它在 CEO 委托、或系统建议且 CEO 确认时，提供完整的研究、经营方法、设计、搭建、组队和验收服务（见 9.4 / 9.5）。它不垄断 Business / Department / Workspace 的创建权。
- **临时工作可以自然成长为长期 Workspace**：当某段工作反复发生、需要稳定责任与协作时，才提升为由真实 Operating Team 承载的长期 Workspace，并满足 9.2 的团队承载要求（见 legacy-named invariant `OFFICE_REQUIRES_OPERATING_TEAM`、`NO_TEAM_NO_SUCCESS`）；是否采用 Professional 形态由专业成熟度决定。

---


## 10. Shared Operating Capability Contract（CEO Accepted 2026-09-15 · Frozen）

本节至§18是经CEO批准的 **CURRENT / FROZEN PRODUCT CONTRACT**，承接唯一Product Blueprint；不是运行实现验收。产品对象和用户可理解的状态在此定义；字段/入口由Master Map展开，空间由UI Blueprint/Shell消费。技术映射、调度算法、库、协议与G1-V～G6-V留在实施验证，不新增系统或Schema。本轮Consolidation执行结果仍等待CEO Final Product Truth Review。

### 10.1 唯一Owner与能力边界

Company → Department → Business → Workspace保持；Company/Department可以有合法Work/Result，Account/Platform不成为第五Scope。Employee为稳定身份，同一Employee通过不同Assignment/Responsibility/Scope/Context服务多个Business；目录一人、业务多处引用。Role不授予技术权限，能力存在≠安装/启用≠绑定≠有效授权≠执行可用，Capability≠Capacity。

Curis组织Model、External Agent、Skill、MCP、Connector、Browser/Computer、文件/专业工具和Knowledge成为员工可用能力。**DEFINE FIRST → REUSE BEFORE BUILD**；Provider提供执行/信息/数据，不是Employee，不拥有Company/Business/Work/Result真源。一个Work可以引用外部Task/Session，但不得复制为第二Work、Workflow、Employee、Result、Decision或Usage系统。Package First及Methodology/Skill composition/Operating Definition分工不变，不新增Playbook。

|层|责任与产品边界|
|---|---|
|Information|带来源、时间、合法scope与缺失；外部内容是数据，不是授权指令|
|Analysis|Employee解释口径、证据、推断、Unknown；不将生成文字当验证|
|Recommendation|提出可行方案、理由、风险与能力限制；建议不自动生效|
|Decision|经营方向、受保护边界、重大预算/不可逆承诺进入既有P7；技术授权与用户执行动作不自动成为P7|
|Execution|在有效权限、数据/预算/能力边界内由原Work执行并回收Evidence；Provider成功码不等外部业务价值|

每个具体动作如实表达 **AI Direct / Provider Execution / AI Assisted / User Required / Unknown / Unavailable**。这是产品责任/可行性表达，不是新增统一Runtime enum，也不推出“全业务L3/固定自治百分比”。未知业务先复用、组合、研究/适配、建设/获取能力，必要时升级或Cannot operate yet，不把缺口变成CEO复杂配置表单。

### 10.2 Context / Learning / 经营连续性

Conversation是持续工作关系，同Employee可多topic，亦可跨Assignment持续；每条消息与引用保留当时scope，并验证当前访问权限。不得默认携带全历史、所有账号资料、Evidence正文或Provider trace；reference-first、summary-first、retrieve-on-demand。Employee消费当前Assignment/Responsibility/Work/Input/Output与相关能力，不能复制Leader全部经营Context。

Result / Evidence → Signal → Interpretation → Authorized Review → accepted Learning → Strategy/Plan change。内部完成≠Business Result，AI总结不直接晋升永久能力。Evaluation至少说明metric/proxy、source、freshness、observation window、minimum sample、baseline、materiality、confounder、cooldown和risk/permission/budget gate。证据不足不能自主ADJUST Strategy，按合同CONTINUE/WAIT/ESCALATE。自主调整始终在Approved Strategy Envelope内；Goal/Success Contract/Positioning/Audience/Business Model/受保护策略/重大预算/高影响承诺仍CEO Gate。

复用既有bounded Cycle与不可变Goal/Strategy/Plan/Operating Definition引用；每Workspace operating scope one active Cycle，CONTINUE/ADJUST exactly one successor；WAIT无active Cycle且有nextCheckAt或明确callback条件；ESCALATE等待授权判断；PAUSE显式Resume；STOP仅CEO或预授权terminal policy。Cycle Close≠经营责任停止。四scope基础设施不等四层自主经营已验收；本合同不改变Autonomous V1 Issue。

## 11. Human Handoff / User Required（Frozen）

AI自治默认，但登录、MFA、手机确认、身份/现实动作、补材料及当前AI/Provider不能代理的必要动作，可以在**原Work**进入人工接续。它不自动创建P7 Decision、不自动触发Shell P5责任转移、不新增Work系统。真正的责任转移仍需原P5接收与证据；同时包含经营决定时单独关联原P7。

每次接续必须说明：**AI已完成什么、为何需要用户、用户做什么、去哪里、完成判据、之后Curis继续什么**；同时保留Work/Responsibility、合法Scope、目标/账号、Owner、原因、Evidence refs、等待/失效条件和返回位置。只取必要材料，不要求用户粘贴Secret。

用户报告“已完成”≠外部事实已确认。存在可验证事实时先核验；无接口时记录manual/source/time/unknown，不伪造Provider receipt。用户离开/沉默不视为成功；期限或权限失效后重新检查再继续，无法继续则原责任等待/升级。人工接管时AI不得同时争夺浏览器/电脑控制；用户结束接管后重新核对目标、权限和动作版本。

技术访问继续消费 [ADR-0046](../07_Decisions/ADR-0046-local-agent-computer-access-authority.md)：请求批准 / 自动处理 / 完全访问；Requested≠Configured≠Effective，完全访问≠root/admin≠已生效；GUI-only Agent不能被本合同假设为可自动改权限。无需将正常CLI工具逐条变成普通CEO审批表。

## 12. Web / Browser / Computer Shared Contract（Frozen Target）

|能力|输入与输出|边界 / 失败 / 恢复|
|---|---|---|
|Search|当前问题、研究范围/语言/时间条件→带来源与检索时间的候选引用|区别Company Object Search；搜索片段不是完整事实；覆盖不足/失败明确，不承诺全网实时|
|Reader|授权URL/资料引用→可读正文、来源、提取范围与时间|显示截断、访问限制、解析失败、过期；必要时重新读取/换合法来源，不能伪装完整阅读|
|Interactive Browser|原Work、授权账号/站点/目标/动作→可观察浏览过程、结果与Evidence|只读/上传/提交/发布等动作分别受限；接管/断线/权限失效/效果未知均回原Work|
|Computer|当前工作资源和有效电脑访问→实际可验证动作|读屏/控制、OS权限、Agent能力和模型能力分别证明；权限请求不是已生效；不绕过ADR-0046|

- 浏览session/account按Company、合法Work/Scope及账号隔离；不得静默使用CEO主浏览器Profile、Cookie或无关Business账号。共享账号仅经合法绑定/授权；Profile隔离不等安全沙箱，资源占用必须可解释。
- 进入时确认目标站点和账号；导航/登录改变、重连或resume后重验。观察入口显示当前动作、目标、接管与停止；不默认展示Console/网络trace或私有数据。
- 上传必须有文件读取/外发/目标授权；下载进入受控目录并保留来源/Work引用，不默认覆盖或打开可执行文件。localhost/内网访问仅对明确授权服务，不把浏览授权扩成任意本机访问。
- 自动控制、人工接管不得并发争用；终止控制不等撤销已发生外部效果。断线/崩溃/超时按§15核验效果，不直接重新提交。
- 网页/文件/插件文本不能改变权限、目标或系统指令；读取、引用、发送最小必要数据。受保护登录/身份验证只走合法人工流程，不绕过平台安全机制。
- **TARGET PRODUCT: YES；CURRENT IMPLEMENTATION: Interactive Browser NOT VALIDATED / G1-V NOT RUN。** 已有App Browser验收、静态WebView或预览不构成该能力验收。

## 13. Model / Connection / Capability Shared Contract（Frozen Target）

Provider Connection是认证/出口/租户范围的连接；Model是可选模型身份/版本；Capability是某用途是否可做。三者不合并。External Agent是能力供给，不变成公司员工；Skill/MCP/Connector按既有发现、安装、启用、绑定和有效权限机制使用。

模型事实按能力分别为 **SUPPORTED / UNSUPPORTED / UNKNOWN**，附source、model/provider version、checkedAt/freshness、test evidence与限制。chat成功不能证明Vision、Tool Calling、Computer Use或其他模态成功。声明、目录metadata与实际测试证据分开；版本/权限变化后必要能力重验。

产品事实包括：输入/输出Modalities、Vision、Reasoning、Tool Calling、Computer Use、Context硬限、Output limits、Cost（estimated/actual分开）、Rate limit、Availability。未知不编值；系统发现事实默认只读，用户别名/声明不升级Verified。只能收紧合法软预算/输出限制，不任意扩大模型硬能力。

连接至少说明名称、服务/认证方式、合法tenant/organization/project/region（仅需要时）、凭据可用性、Health、Discovery完整性、最近核验、限制与下一动作；凭据只留安全引用，不回显Secret。发现不完整不得把未返回模型自动判不存在。真实动态发现的tenant-private model按tenant/provider/health/eligibility可成为默认及Conversation候选，不退回official-only；手动model ID也需核验。

用途解析：**Work explicit → Employee purpose → Company default**，选择/继承同一全局池有效配置而非三份Model Truth，Employee用途偏好可继承、不是预绑定门禁；已启用可用Model/Agent自动进入Conversation候选，见§19.3。每层仍受Permission、Data Boundary、Budget和Capability约束。AI Ready必须由Credential availability＋Provider Health＋Model eligibility/availability判断，不能只看数据库metadata；restart重新验证。

Fallback仅能在已授权、用途能力/输入完整性/数据目的地/地域/预算兼容的候选内发生，并可追溯替换理由、来源与Usage；缺合法候选则等待/修复/升级。不能静默丢附件、降能力、扩大外发、跨隐私边界或重发效果未知的外部写。测试是按用途必要的动作，非首次强制跑全套付费测试；说明费用/数据影响。

**CURRENT IMPLEMENTATION:** 既有Cloud/Keychain/DeepSeek链按CURRENT_STATE保留接受边界；完整用途测试/受控fallback/发现合同仍 **G2-V NOT RUN**，不声称所有Provider已验证。

## 14. Optional Local Background Operation（F2 Option A · Frozen Target）

**TARGET PRODUCT: ACCEPTED — OPT-IN LOCAL BACKGROUND SERVICE。CURRENT IMPLEMENTATION: G3-V NOT RUN / NOT IMPLEMENTED BY THIS CONSOLIDATION。**

|条件/动作|正式产品语义|
|---|---|
|未开启后台|不承诺UI退出后继续；告知受影响Work并安全保存，不伪造仍在工作|
|用户显式开启|关闭UI后合法、已授权Work可以在本机继续；不扩大权限、预算、Scope或自动启动无授权经营|
|Sleep / Shutdown / Logout|Sleep不保证运行；Shutdown不运行；Logout不保证运行；不能显示24/7在线|
|系统禁用后台/服务不可用|停止后台继续能力，显示实际原因/最后活动/恢复入口；配置Enabled不等实际Running|
|停止全部并退出|停止领取新动作，安全停止/保存受控本地执行；在途外部动作标待核验，停止≠撤销远端事实|
|重新打开UI|接回同一Runtime/Work/Conversation/Result历史；不创建第二daemon Truth或重放全部动作|
|恢复设备/网络/权限|核验运行Owner、Work、授权、输入版本与外部效果后按原合同继续；需要人则§11，不能假自动恢复成功|

调度只复用既有Result-driven、scheduled review/nextCheckAt、Leader/CEO initiated触发；默认合并错过/重复触发并重新检查现状，不盲目补跑过期外部写；不建立generic external-event/threshold engine。one active Cycle、原Work幂等、唯一后继、显式WAIT/PAUSE/STOP不因服务化改变。进程owner/lease/锁/调度库是实施责任，不是CEO设置字段。

## 15. Execution / Approval / External Effect Recovery（Frozen Target）

**EFFECT_UNKNOWN**是产品效果语义，不预设Runtime enum。外部写动作超时、掉线、崩溃可能已经发生效果，禁止统一FAILED→RETRY。继续保留唯一Work、Execution、Result、Evidence、P7 Decision和Usage。

|效果判断|允许的后续|
|---|---|
|effect confirmed|关联可信回执/外部查询/结果Evidence与原动作；按合同继续，不重复写|
|effect unknown|暂停可能重复的外写；显示原因、目标、Owner和核验下一步，不虚构失败|
|verification required|合法查询远端、核对回执或请求人工证明；来源与局限可见|
|safe retry|只有已确认未生效或具可信幂等/去重合同且仍有授权时，才按同Work安排安全尝试|
|cannot replay|无法证明安全、授权失效或不可重放时等待/人工接续/升级，不用新Provider绕过|

Approval必须绑定具体动作、目标、账号、资源、输入版本、预算/权限范围与有效期/条件；实质变化后旧Approval失效。技术访问许可、经营Decision、一次动作批准不是同一对象；本轮不要求新Approval表。执行前再次检查有效权限、能力、输入和预算。

每个失败/恢复必须有Owner、state语义、reason、recovery path、next action。包括Provider failure、capability missing、Result Contract failure、duplicate callback、late Result、restart/leader crash、CEO silence、no data、权限撤回、预算耗尽、trigger storm、反复策略失败和Goal achieved。迟到回执回原Work核验；取消不抹结果，local exactly-one successor不等远端exactly-once。全部映射既有责任/执行/恢复机制，缺primitive须另Architecture Gate。**G4-V NOT RUN**。

## 16. Professional / File Capabilities（Frozen Target）

以下按Employee能力绑定与Workspace专业需要提供，不新增Terminal/IDE/Data Studio/Media Editor一级产品区。原资料库依然Company Reference Space。

|能力|输入 / 可交付|必须显式的边界与恢复|
|---|---|---|
|File|合法文件/目录引用、版本、输出目标→真实产物与Work/Result引用|最小读取/写入授权；覆盖/冲突先核验另存/合并，不能破坏原文件；工作文件不自动全收进Library|
|Terminal|已授权环境/cwd/资源/命令→退出信息、产物与证据|进程树、取消、超时、输出截断、资源限制可追；退出码不等交付成功；不默认继承Shell秘密|
|Git|当前仓库/分支/dirty状态→diff/测试/交付引用|读、写、commit、push、破坏操作分别授权；保护他人变更，不隐式提交/重置|
|Preview|实际服务/端口/产物引用→可访问预览|本机服务不自动暴露外网；失败有进程/地址真实状态；预览不等部署/验收|
|Document Parsing / OCR|合法文件/页范围→提取内容与原文/页引用|格式、截断、低置信、缺页、失败真实表达；保留原件，不把猜测当完整解析|
|Data|授权数据源/口径/观察窗→查询结果快照/分析证据|默认只读、限范围/资源；写入另授权；口径不明或数据缺失显示Unknown，不建分析账本|
|Media|真实素材/规格/权限→可回读校验产物|理解≠生成≠编辑/转码；格式尺寸时长来源可查；版权/平台限制、Partial、成本不伪造|

基础Provider能力按可用性复用，Skill/插件/Agent更新涉及权限增量须复审；版本漂移不得静默扩大能力。Data与Media方法归Domain/员工，系统只保障权限、引用和执行。已有md/txt/文件能力验收不被抹掉，也不扩成PDF/DOCX/Image/Web/OCR全可用；**完整合同G5-V NOT RUN**。

## 17. Backup / Restore / Reconnect（Frozen Target）

**TARGET PRODUCT: YES；CURRENT IMPLEMENTATION: FULL BACKUP G6-V NOT RUN。**

完整恢复单元为Database＋Managed Files＋Manifest＋Integrity；Manifest解释版本、范围、文件引用/完整性与不包含项，不新增Company真源。只备DB不声称公司可恢复；校验和不等加密。

普通备份排除Credential、Cookie、Keychain Secret和Browser Profile；只保合法连接引用与后续重连清单。输出/导出说明范围、敏感性与保存位置，不承诺不存在的加密。不可管理的外部文件/服务明确列为未备份项。

Restore Preflight检查包完整性、版本兼容、空间、引用与影响；不符合条件则停止并给原因。恢复需停止相关写入并有安全保全/失败回退，不破坏现有公司；恢复后检查同一identity与Result/Evidence/文件引用，给Reconnect List。**Resume Check**重验凭据、权限、能力与外部效果；外部写默认先核验不自动重放。恢复不是创建新Company/Workspace，不复制员工或Usage。

## 18. Settings / Attention / Shared Interaction（Frozen）

七类是Owner维度，不是七个Settings Tab，也不是77个普通配置项。沿用头像→设置及已有设置分类；多个情境入口消费同一有效配置。动作（测试/接管/恢复/选择资料）不伪装长期配置。

|Owner|普通用户/自动事实|高级/内部边界|
|---|---|---|
|Personal|CEO名/头像、语言、显示时区、外观/减少动画、发送偏好、通知/锁屏隐私/安静时段/摘要、后台opt-in|OS授权需真实；移动通知按可用性；IME不得误发送|
|Company|公司名/经营时区、目标/边界、预算、用途默认、数据外发/审批政策、备份位置/范围、资料时效、归档影响|不是初始化全填表；成本无来源Unknown；撤销/归档保护责任/承诺/历史|
|Employee|职责与用途继承、相关Skill/Tool/MCP范围/授权|按工作最小Context；绑定不授永久全历史；不强制每员工配置模型|
|Workspace|研究范围、资料/输出目标、文件冲突、仓库/Preview、数据口径、排程、上传下载、工作素材|本次Work参数不复制公司设置；格式/媒体规格按交付需要，不强推所有业务|
|Provider / Connection|名称、认证、凭据状态、必要org/project/region、发现/健康/可用性；账号绑定|自定义endpoint、环境/连接传输、代理、合法证书按需高级；不禁用TLS；配额/地域/能力只读有来源事实|
|Capability Advanced|合法软预算/输出限制、用途fallback、Provider支持的采样/Reasoning参数、更新策略、必要解析/媒体参数|不扩大硬Context/Rate限；Timeout≠未生效；Retry不能绕过§15；执行路径/调试/自定义MCP不作普通门禁|
|System / Runtime|版本、真实存储/后台状态、可理解的资源占用与安全维护、诊断导出|owner/lease/进程锁/强制信任策略不暴露为普通设置；安全边界不能关闭；缓存清理不删Evidence/经营历史|

能力事实、Context Window、Provider limit、版本默认只读；用户声明不能提升Verified。Advanced不等绕过安全。请求批准/自动处理/完全访问仍是三档用户意图，不拆成逐命令权限表。

Attention复用原Matter/Notification：普通继续安静；需要人、真实风险/决定、效果待核验、阻塞与后台异常时显示原因和下一步；尊重通知偏好/安静时段，不能悄悄批准风险。已处理Decision降为结果/历史，不长期高Attention。用户离开页面不终止合法工作。

统一交互责任：保留输入、来源Scope、对象、筛选/阅读位置及返回入口；配置完成回原Work重新检查，不自动重做未知外部写。状态区分Employee三态、Work等待/失败、来源不一致/需核实、资源占用和效果未知，不新增Global Conflict enum。键盘/输入法/缩放/可读状态与错误恢复必须后续验证，图稿不算通过。

诊断按范围选择→脱敏预览→导出；发送另外授权，不默认上传对话、Evidence正文、凭据或Provider trace。升级/恢复保identity和历史引用，相关能力版本复验；专业配置不把Curis变LLM Gateway/Browser/IDE。具体Modal/Drawer/Tab/像素仅经正式交互合同确认才固定，否则DESIGN OPEN。


## 19. Business Activation / Package Continuity（CEO Accepted · Frozen Product Contract）

Authority Class: CURRENT / FROZEN PRODUCT CONTRACT. Disposition: BUSINESS ACTIVATION PRODUCT TRUTH PATCH，2026-09-15。仅产品合同，非Catalog/Migration实施验收或具体Package发布决定。

### 19.1 Definition / Discovery / Publication

**AVAILABLE DEFINITION ≠ ACTIVATED BUSINESS。** Package声明专业方法、Professional Workspace定义、责任/能力要求、Result/Evidence、人工/安全边界及版本/迁移政策，不是用户Business。Catalog仅为已发布、允许启用且用户有权访问的Domain Operating Capability Package发现投影；不拥有Business、Workspace、Employee、Assignment、Work、Result，不新增canonical对象或第二Package/Capability系统。用户语言：“可开展的业务 / Curis可以帮助经营的业务”。

发布必须有完整产品/能力合同、诚实可执行范围、推荐范围真实验证、来源/维护/支持/迁移政策与正式发布决定。Official≠Verified；Research/Candidate≠可启用。未通过者不混入可启用集合，不显示正式启用按钮。Company缺模型/账号不改变发布资格，只影响相关Work。工程细则见[Workspace Engineering Lifecycle §1.0A](../05_Workspace_Engineering/Curis_Workspace_Engineering_Lifecycle.md)，该文件其它方法论Candidate不整体升级。

### 19.2 One Business Creation Experience

新Company已有CEO、same canonical Assistant、原装组织/Employee，用户Business可0。Business Space只列真实Business，0/N均以“新建业务”进入同一Main流程。Organization → 新建 → 新建Department / 新建Business；选择Business携合法Department建议进入同一创建。Assistant识别Intent、查已有Business、匹配已发布Package或Generic，进入同一Conversation / Structured Proposal / Confirmation；不得静默建Department/Business、绑定Provider或扩大权限。

Package → Catalog Projection → Discovery → Business Proposal → CEO Confirmation → Business Instance + First Workspace → Organization / Responsibility / Assignment → 合法Operating。浏览/点击启用是意向，不是安装插件、下载页面或启动Work；“确认创建业务”才授权实例化。Catalog、详情、Guided Proposal使用Main，不是第八导航、小Modal、Utility或Settings。

Proposal = Package/Generic＋CEO Intent＋合法Company Context。模糊Intent允许，系统推导、必要研究，只追问不能安全推导的重要事实；不填完整组织/模型/Workflow表单。说明名称、Goal/假设、Department、First Workspace、Leader/Responsibility、Assignment建议、组织变化、缺口、首步Work及权限/预算/自动化边界。复用相容组织优先；新Department连同提案确认，原装支持部门不自动拥有用户Business。Package只声明要求，不指定employee_id、不拥有Department、不绕Assignment；无Holder如实未落实，不复制员工。

创建须CEO有效确认、合法Company/Department及创建权限、明确经营方向、合法First Workspace。Business＋First Workspace原子成功；提案含新Department时组织可见结果亦一致。双击/重试/重开查同一确认结果，不重复实例化；失败保提案，不静默换包/降级Generic。成功落同一Company Truth，Business Space/Organization同步；责任/Assignment如实落实或报缺口。具体Work另检真实Holder/能力/权限/授权，不建复杂Business Readiness系统。

回程：Organization回原地图选中新Business；Assistant回同一Conversation给真实Business/Workspace链接；Business Space保既有First Workspace landing与回目录入口。取消/修复保原上下文；不同入口没有第二套创建系统。

### 19.3 Global Model / External Agent Pool

Model / External Agent Configuration是统一全局AI能力池，仍受tenant/permission/data boundary约束，不是跨租户共享凭据。主流模型预置连接配置，通常填写API Key后启用；支持自定义Model及External AI Agent，预置≠已连接/已验证。

已启用且当前可使用的Model/Agent自动进入统一Employee Conversation Composer可选列表，不需逐Business或逐Employee重复配置/绑定。§13 Work explicit → Employee purpose → Company default只解析同池有效选择/偏好；Employee purpose可继承，不是固定模型必填。Business Context决定Conversation/Work经营归属，不复制配置。health/eligibility/permission仍有效。

**没有Model也可合法创建Business。** 无AI不得假装理解/研究/提案生成；允许浏览、填写可确定事实并确认合法创建，AI动作诚实等待。特殊Work缺能力在Work/Capability Context提示，不加Business门禁。修复用原Settings并返回，不再次“给业务绑定GPT”。其它Skill/Tool仍按合法安装/启用/Binding与权限，不自动全员绑定。

### 19.4 Repeated Activation / Generic

同Package可用于多个Business。按Goal、Brand/Operating Identity、Strategy、Budget、Responsibility、Data/Permission boundary决定扩现有或建独立业务；同品牌同方向加Account优先扩展，独立目标/预算/边界可新建；歧义CEO确认。Account/Channel/Platform≠Workspace，不自动新Business。

无Package仍走Generic / Research / Capability Discovery；身份/归属明确可建真实Business＋Generic Workspace，诚实说明能做什么，不冒充Verified Professional。未来包成熟优先升级原Business环境/能力，不重新建Business。无法安全判定身份/授权才追问或先Company研究，不以研究伪造Business。

### 19.5 Version / Migration / Delisting

**Business Instance Identity ≠ Package Version ≠ UI Version。** 稳定Package identity＋不可变发布version；记录实际Business/Workspace应用关系及Work当时依据，不执行“latest”。同Business不同Workspace可用不同受支持版本，不预设单一business.package_version字段或Schema。

升级不是重新Activation：Compatibility → Migration Plan → Preflight / Recovery Point → 必要Data Migration → Capability/Permission Recheck → Workspace/Surface Upgrade → Resume Check → 原Business继续。复用Workspace Engineering、Work、Decision、Backup/Recovery、能力更新，不建第二Migration Runtime。纯展示通常不迁数据；UI不拥有Business Data Truth，必须读受支持旧数据，不得隐藏、填假默认或重建对象适配页面。

保Business/Account/Work/Result/Evidence/Learning/Conversation identity、Scope、历史意义；rename保ID，语义变化显式mapping，deprecated不删历史。新字段无证据Unknown，不能填0/成功/授权；新评价追加来源，不覆盖旧Result。Employee/Assignment历史不重挂旧Work。

在途Work固定输入/方法/能力/Permission/Approval snapshot，不热切；旧版安全则完成，否则等待/controlled Handoff/re-plan。EFFECT_UNKNOWN先查外部事实，不借升级重放。新Provider/外发目的地/费用/权限/重大责任变化需现有Decision/Permission重新确认；升级确认≠动作批准。自动更新仅既有政策覆盖、已验证兼容、无新增费用/权限/重大方法或责任变化、无丢失、历史可读且Recovery成立；版本号不决定安全。

恢复保护Company自定义、升级后新数据和其他Business，不可恢复A覆盖B新事实。回退有条件；不安全原地升级优先同Business sibling Workspace＋controlled Handoff，旧环境/历史保留。共享Core与混版兼容由实施验证。

Catalog下架≠Existing Business Lifecycle；不删除Business/历史。安全撤销只停受影响动作并给迁移/人工路线。旧定义保历史解释，支持窗口/混版细则消费Workspace Engineering；版本关联、兼容、迁移/恢复为Architecture/Implementation Gate，本轮不交付、不发布Content Growth。

*COMPANY OS SHARED AUTHORITY — FROZEN（§7明确排除项保持Candidate）*
