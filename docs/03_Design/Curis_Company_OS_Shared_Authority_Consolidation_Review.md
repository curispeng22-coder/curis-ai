# Company OS Shared — Authority Consolidation Review

> **状态**：AUTHORITY CONSOLIDATION REVIEW（未 Frozen · 本轮只评审不落定最终 Frozen 文档）
> **Review Record（2026-08-16 已落定 Frozen）**：本 Review 的评审结论已落定为 Frozen Authority —— `Curis_Company_OS_Shared_Authority.md`（⑥⑧⑦ + Context Isolation Truth Boundary；⑨ Lightweight Queue/Bottleneck **保持 APPROVED SHARED CANDIDATE**；原 `ROUTING_IS_DETERMINISTIC` 已被 `ROUTING_IS_POLICY_GOVERNED_AND_EXPLAINABLE` 取代）。本文件留作 **Review Record / Reference**，不删除、不覆盖。
> **范围**：候选集 A — ⑥ Responsibility Requirement · ⑧ Shared Employee Service Relation · ⑦ Organization Routing · ⑨ Lightweight Queue / Bottleneck
> **目标**：判定哪些语义真正值得升格为 **Company OS Shared Authority**（跨 Content Growth / RD / 未来客服 / 销售 / 其他 Professional Workspace），哪些仍保持 Candidate。
> **纪律**：不复制 Candidate 细节（见 §G）；不 Frozen 具体算法/权重/阈值/常量；不新建第 10 个 Context Contract；不修改任何现有 Frozen Authority。
> **前置**：9 契约全部 APPROVED CANDIDATE；`Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`（P1–P7 Frozen）；`Curis_Organization_Routing_Architecture.md`（DELTA 1/2/3）；`Curis_Content_Growth_Company_Evolution_Model.md`。

---

## 1. 升格门槛（B 节）重述

Company OS Shared 的门槛**高于** Domain：一个语义要升格，必须能回答——

> 「这个语义在 Content Growth 之外（RD / 客服 / 销售 / 其他 Professional Workspace）也成立吗？」

若只在 Content Growth 例子下成立，**不得**升 Company OS Shared，留在 Domain 或 Candidate。

逐项检查维度：
- **Responsibility Requirement**：能否抽象为「Process 声明需要什么 Responsibility」，**不携带** Video / Subtitle / Channel / Content 等领域词汇？
- **Organization Routing**：只 Freeze **机制**（Requirement → eligible candidates → deterministic routing → Holder/Executor），**不 Freeze** 评分算法 / 权重 / 阈值 / LLM 实现。
- **Shared Employee Service**：只 Freeze「Employee 属 Organization、经 Service/Assignment 服务多 Operating Context/Office、服务关系 ≠ 组织隶属、服务关系 ≠ 上下文所有权」，**不 Freeze** Content Growth 专属字段。
- **Queue / Bottleneck**：判断是否已成熟到 Shared Authority；若未成熟，**保持 APPROVED SHARED CANDIDATE**，不强 Frozen。

---

## 2. 逐项判定

### 2.1 ⑥ Responsibility Requirement — 判定：**FREEZE NOW（升格 Company OS Shared Authority）**

**跨业务适用性**：✅ 强。
- 任何业务过程的本质都是「我需要某类责任被履行」，而**不指名具体谁来做**。RD 声明「需要 code-review」、客服声明「需要 ticket-triage」、销售声明「需要 lead-followup」——语义完全领域无关。
- 契约本身已用 `responsibility_type`（枚举/编码）+ `constraints` 表达，**不出现** Video/Subtitle/Channel 等词；领域词只存在于具体 `responsibility_type` 取值（属配置/扩展，非 Shared 核心）。

**应 Freeze（Shared 核心）**：
- Definition：Responsibility Requirement = Process 对「所需责任类型 + 约束」的**声明**，永不直接指名 Employee。
- Invariant：REQUIREMENT_NAMES_NO_ONE（声明 WHAT，不绑定 WHO）；REQUIREMENT_IS_UPSTREAM_OF_P1（是 Frozen P1「Current Responsibility」的上游声明层）。
- Truth boundary：responsibility 解析的 WHO 由 Routing（⑦）决定，不由 Requirement 决定。

**应排除（不 Freeze 进 Shared）**：
- 具体 `responsibility_type` 词汇表（Video/Subtitle/.../code-review/...）—— 属 Domain 配置 / 扩展点。
- 任何把领域词硬编码进 Shared 类型的做法。

**Relation to Frozen P1**：EXTENDS（上游声明层），**不修改** P1。

---

### 2.2 ⑧ Shared Employee Service Relation — 判定：**FREEZE NOW（升格 Company OS Shared Authority）**

**跨业务适用性**：✅ 强（最基础的「一人服务多业务单元而不被组织隶属」模式）。
- Employee 始终在 Organization 轴；经 Assignment/Service 关系服务 N 个 Office/Operating Context；这是任何公司通用的组织-业务正交模型。

**应 Freeze（Shared 核心）**：
- Definition：Employee ∈ Organization；经 `Responsibility Assignment`（employee_id × office_id × responsibility_types[]）服务多 Office。
- Invariants（核心四则）：
  - SERVICE ≠ MEMBERSHIP（服务关系 ≠ 组织隶属；Employee 不因此成为 Office 的部门/成员）
  - SERVICE ≠ CONTEXT_OWNERSHIP（服务关系 ≠ 上下文所有权 —— **DELTA B1 落点**，见 §3）
  - NO_DAG（Assignment 是容量/资格，非硬编码路由；无固定 DAG）
  - ORG_AND_SERVICE_ORTHOGONAL（组织轴 Department/Team 与服务轴 Office Assignment 两正交轴，可同屏不可混淆）

**应排除（不 Freeze 进 Shared）**：
- Content Growth 专属字段（如某 Office 的 audience/content_strategy 不进 Shared）。
- 具体 Assignment 生命周期状态机细节（属实现，非 Shared 语义）。

---

### 2.3 ⑦ Organization Routing — 判定：**FREEZE NOW（升格 Company OS Shared Authority，仅机制）**

**跨业务适用性**：✅ 强。
- 任何业务都需要「把责任确定性地分派给合格执行者，异常才升级人工」——这是通用的责任调度机制。

**应 Freeze（Shared 机制）**：
- Definition（机制骨架）：Requirement → eligible candidates（按 Assignment/资格过滤）→ **deterministic routing**（低成本、可复现、无随机性）→ Holder / Executor。
- Invariant：ROUTING_IS_DETERMINISTIC（同输入同输出，可解释）；TEAM_LEAD_ONLY_ON_EXCEPTION（Team Lead/人工 **仅** 在异常/管理判断介入，不做日常调度）；NO_PRELOAD_FULL_CONTEXT（路由解析时只取 task-scoped 上下文，不预载全量 —— DELTA B1 落点）。
- Escalation boundary：无合格候选 → 升级 Team Lead / CEO，需求保持 UNRESOLVED，不静默丢弃。

**应排除（明确不 Freeze）**：
- 具体评分算法 / 权重 / 阈值 / LLM 实现细节 —— 属未来 Runtime Policy / 扩展点。
- Team Lead 的具体判断流程（只 Freeze「仅异常介入」边界）。

**Relation to Frozen P1**：⑦ 产出 P1 的 Current Responsibility / Executor，**不修改** P1。

---

### 2.4 ⑨ Lightweight Queue / Bottleneck — 判定：**KEEP APPROVED SHARED CANDIDATE（暂不 Frozen）**

**跨业务适用性**：⚠️ 概念成立，但成熟度不足。
- 「观测运行事实 → 检测瓶颈候选 → 建议非破坏式动作」确为通用模式；但**当前形态过新**，未经验运行时验证。

**不成熟证据（B 节明确指引：未成熟则保持 Candidate）**：
- 阈值常量 / 持续窗口（`observed_since` 窗口）**未 Frozen**（属未来 Runtime Policy / Configuration，E.2 非阻塞）。
- `possible_cause` 最小事实规则**仅固化原则**（直接证据→具体因；证据不足→UNKNOWN；禁 LLM 猜根因），**未固化为常量/算法**（E.3 非阻塞）。
- 4 个 suggested_action（WAIT_AND_OBSERVE / REBALANCE_EXISTING / ADD_EMPLOYEE / ESCALATE_FOR_DIAGNOSIS）是**首版小集合**，未经验证是否完备。
- 无 throughput 预测 / capacity score / 智能负载 / 企业级 scheduler（DELTA 3 已降复杂度，但仍属年轻契约）。

**判定**：**KEEP APPROVED SHARED CANDIDATE** —— 概念归属 Company OS Shared，但**不强 Frozen**。待运行时验证 + 阈值/窗口/cause-rule 校准后，再考虑升格。

**不建第 10 契约**：Context Assembly 仍为 Future Company OS Shared Candidate（Batch B 已记录），本轮不新建。

---

## 3. Context Isolation 边界归属（C 节）

DELTA B1「Shared Employee ≠ Shared Context」是 Company OS Shared 的关键边界，必须写入 Authority。归属裁定：

| 边界内容 | 归属 | 理由 |
|---|---|---|
| 机制级原则：Service Relation ≠ Context Ownership | **⑧ Shared Employee Service Relation**（Invariant）+ **⑦ Organization Routing**（NO_PRELOAD_FULL_CONTEXT） | 服务关系定义与路由解析时即须遵守 |
| 规范级陈述：Employee Persistent Context（Role/Specialty/Stable Skills/Stable Company Rules）**vs** Responsibility Execution Context（Current Responsibility/Office/Account/Object/Required Knowledge only） | **Company OS Shared Authority Boundary**（Truth Boundaries 章节） | 跨 ⑧⑦ 的全局真理边界，单一归属避免两处各写各的 |
| 禁止清单（全量加载 Office 资料 / 全量账号历史 / 串线 / Org Membership 当 Knowledge Access / Assignment 当永久 Context 绑定） | **Company OS Shared Authority Boundary** | 同上，全局约束 |
| 每次执行 = resolve → retrieve relevant → assemble task-scoped → execute | **⑦ Organization Routing**（机制描述）| 路由即执行入口，天然在此 |

**结论**：Context Isolation 以「机制约束」形式落 ⑧⑦，以「规范级真理边界」形式在 Shared Authority Boundary 单点定义（避免重复）。**本轮不新建 Context Engine Contract**。

---

## 4. 冲突检查（F 节）

| 现有 Authority | 关系 | 说明 |
|---|---|---|
| Product Blueprint | NO CONFLICT | Office 直接挂 Company（DELTA A3）与 Blueprint「业务空间/Workspace」层级正交；Operating Context 已 DEFERRED 对齐 Blueprint Business，不冲突。 |
| Frozen P1–P7 | EXTENDS（仅扩展，不修改） | ⑥= P1 上游声明层；⑦ 产出 P1 Current Responsibility/Executor；⑧ 新增跨轴服务关系（P2 等不变）；⑨ 复用 P7 二选一。无修改。 |
| Agent Adapter Contract | NO CONFLICT | Employee 经 Execution Binding 引用 capability；契约只声明「能力可替换不拥有」，未重定义 Agent 适配内部。 |
| ADR-0046（Computer Access） | NO CONFLICT | Channel OAuth ≠ 本机电脑访问；契约不触碰电脑访问授权。 |
| XHS Approved Instance | EXTENDS / NO CONFLICT | 9 契约对 XHS 为 ADDITIVE；XHS = 单 Office·单账号退化形态，不破坏。 |
| RD Approved Instance | EXTENDS / NO CONFLICT | RD 责任模型 R1/R2/R3 可映射 ⑥；ADDITIVE。 |
| Current Runtime Foundation | NO CONFLICT（非阻塞扩展注记） | 契约仅语义层、未实现 Runtime；DELTA B1 上下文隔离是 Runtime 未来须遵守的需求（注记，非 REQUIRES DELTA）。 |

**结论：无任何现有 Frozen Authority 需修改，无 REQUIRES DELTA。** 所有关系为 NO CONFLICT 或 EXTENDS（扩展不修改）。

---

## 5. 三项非阻塞问题（E 节）处理确认

1. **平台 Scheduling 官方核实**：保持 Capability Truth（VERIFIED / CONDITIONAL / UNKNOWN / UNAVAILABLE）；UNKNOWN 合法存在。不 Frozen 具体平台 scheduling 事实（属 Capability Registry）。→ 在 ⑤ 已落实，本轮不影响 Shared 升格。
2. **Bottleneck 阈值 / 持续窗口**：不 Frozen 具体常量，属未来 Runtime Policy / Configuration。→ 支持 ⑨ **KEEP CANDIData**（不升格）。
3. **possible_cause 最小事实规则**：只固化原则（直接证据→具体因；不足→UNKNOWN；禁 LLM 猜根因），不设计复杂诊断算法。→ 已写入 ⑨ Invariant。

---

## 6. 建议的最终 Company OS Shared Authority 文档结构（本轮不创建）

> 仅规划结构，**不写最终 Frozen 文档**（H 节要求）。

```
Curis_Company_OS_Shared_Authority.md（未来）
├ §1 Definitions
│   ├ Responsibility Requirement（pattern：声明 WHAT，不指名 WHO）
│   ├ Shared Employee Service Relation（Employee∈Org，经 Assignment 服务多 Office）
│   └ Organization Routing（mechanism：Requirement→eligible→deterministic→Holder/Executor）
├ §2 Relationships（⑥→⑦→⑧ 的引用方向；与 P1 的上游/产出关系）
├ §3 Invariants
│   ├ REQUIREMENT_NAMES_NO_ONE
│   ├ SERVICE ≠ MEMBERSHIP
│   ├ SERVICE ≠ CONTEXT_OWNERSHIP
│   ├ ROUTING_IS_DETERMINISTIC
│   └ TEAM_LEAD_ONLY_ON_EXCEPTION
├ §4 Ownership（Employee 归 Organization；责任声明归 Process；路由决策归 Router）
├ §5 Truth Boundaries
│   ├ Context Isolation Boundary（Persistent vs Execution Context；禁止清单）★C 节
│   └ Capability Truth（cross-ref Domain；VERIFIED/CONDITIONAL/UNKNOWN/UNAVAILABLE）
├ §6 Cross-domain rules（Service ≠ Membership；Service ≠ Context Ownership；WHO 由 Routing 定）
├ §7 Extension points
│   ├ responsibility_type 词汇表（Domain 配置）
│   ├ Routing 算法 / 权重 / 阈值（未来 Runtime Policy）
│   ├ Bottleneck 阈值 / 持续窗口 / cause-rule（未来 Runtime Policy，⑨ 成熟后并入）
│   └ Context Assembly（Future Candidate，不建第 10 契约）
```

**Author 短、稳定、难反悔**（G 节）：§1–§6 只留 Definition/Relationship/Invariant/Ownership/Truth Boundary/Cross-domain rule；算法/常量/词汇表/具体场景全部下放 §7 Extension points 或留 Candidate/Review 作 Reference。

---

## 7. 升格清单（H 节 · 候选集 A）

| 契约 | 判定 | 理由摘要 |
|---|---|---|
| ⑥ Responsibility Requirement | **FREEZE NOW** | 跨业务「Process 声明 WHAT」抽象干净，领域词下放扩展点；EXTENDS P1 不修改 |
| ⑧ Shared Employee Service Relation | **FREEZE NOW** | 跨业务基础正交模型；Context Isolation 边界单点入 Shared Authority |
| ⑦ Organization Routing | **FREEZE NOW** | 仅 Freeze 确定性调度机制 + 异常升级边界；算法/阈值排除 |
| ⑨ Lightweight Queue / Bottleneck | **KEEP APPROVED SHARED CANDIDATE** | 概念属 Shared 但过新；阈值/窗口/cause-rule 未校准，待运行时验证后升格 |

**DEFER / REJECT**：候选集 A 内无 DEFER（除 ⑨ 暂留 Candidate 非永久 DEFER）、无 REJECT。

---

*本文件为 Authority Consolidation Review，未 Frozen。最终 Frozen 文档按 §6 结构在批准后续建。*
