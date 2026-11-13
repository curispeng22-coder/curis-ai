# CURIS AUTONOMOUS OPERATING V1
## IMPLEMENTATION ISSUE

**Issue ID:** `20260820_autonomous_operating_v1_implementation_001`  
**Authority Class:** IMPLEMENTATION ISSUE  
**Status:** Review  
**Disposition:** START GATE PASSED — PHASE 0 AUDIT COMPLETE — IMPLEMENTATION NOT STARTED  
**Date:** 2026-08-20  
**Owner:** 主开发（待 Start Gate 通过后）  
**Review Owner:** Product Architecture / Runtime Quality  
**Product Scope:** Workspace-scoped autonomous operation  
**Domain Candidates:** RD、XHS（首批证明域；不得预设均已可运行）

## 0. Hard Start Gate

本 Issue **不得开始实现**，直到 Canonical Business Spine 的独立 Review 正式返回：

```text
CANONICAL BUSINESS SPINE = IMPLEMENTED / ACCEPTED
```

至少必须由 Accepted Evidence 证明：

- canonical Business persisted identity；
- `Workspace → Business → Department → Company` parent resolver；
- Business + First Workspace 合法创建与 orphan fail-closed；
- legacy unresolved → quarantined 边界；
- clean tracked frontend baseline / shared route seam；
- Single / Multi / Generic E2E。

如果 Business Spine 返回 `PARTIAL`、`BLOCKED`、`PENDING`、`READY` 或仅有静态/候选证据，本 Issue 保持 `READY / NOT AUTHORIZED`。不得以旧 `business_ref`、默认 Business、测试 seed、临时 resolver 或局部页面绕过依赖。

**当前纪律：**本 Issue 不读取进行中的 Business Spine 实现来假定 PASS；只消费其最终 Accepted Review、Allowed Files 与真实证据。

## 1. Accepted Product Inputs

本 Issue 消费但不重写以下产品合同：

1. `docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md`  
   `CEO ACCEPTED / APPROVED CANDIDATE — NOT IMPLEMENTED / NOT RUNTIME ACCEPTED`
2. `docs/reviews/CURIS_AUTONOMOUS_OPERATION_PRODUCT_SURFACE_MAPPING.md`  
   `CEO ACCEPTED / APPROVED SURFACE MAPPING`
3. 当前 Product Blueprint、Master Map、UI Blueprint；三者仍是 Product Authority Chain。
4. Existing Team Operating / Responsibility Routing / Employee Execution Accepted Runtime。
5. Canonical Business Spine Accepted Review（仅在 Hard Start Gate 通过后可作为实施输入）。

本 Issue 不把上述 Product Contract 直接等同于 Schema，也不把视觉映射直接等同于代码。

## 2. Objective

在 canonical Company → Department → Business → Workspace 身份链已被接受后，建立一个 **Workspace-scoped、bounded、restart-safe 的 Autonomous Operating thin control plane**，使既有 Team Operating Engine 可以按经营责任连续运行：

```text
Goal
→ Strategy
→ Plan
→ Team Operating
→ real Employee execution
→ Result / Evidence
→ Review / Learning
→ Next-cycle Decision
→ exactly one next Cycle（仅 CONTINUE / ADJUST）
```

Business 只负责聚合 Goal / Strategy / Result / Workspace portfolio；本 Issue **不得声称 Business-scope Provider Execution 已实现**。

## 3. Scope and Non-scope

### 3.1 In scope

- Workspace operating scope 的唯一 active Cycle 约束；
- Trigger intake / claim 与幂等；
- Situation Snapshot、Strategy / Plan pinning；
- bounded Plan release 到既有 Team Operating；
- Review、Evaluation Contract、accepted Learning；
- Next-cycle Decision 与 exactly-one successor；
- durable WAIT / PAUSE / STOP；
- CEO Gate / ESCALATE；
- restart-safe continuation、late Result、duplicate callback、有限恢复；
- 既有 CEO Desk / Business / Workspace / Leader Conversation 的最小投影适配；
- Primary Autonomous E2E 与 Cross-domain Contract Proof。

### 3.2 Explicitly out of scope

- generic external-event engine；
- arbitrary threshold/rule engine；
- generic autonomous Agent Runtime；
- Business-scope Provider Execution；
- 第二套 Task / Workflow / Employee / Result Runtime；
- 新一级页面、Operating Console、Strategy Center、Review Center、Learning Center、Cycle UI；
- fake Result、fake Analytics、static UI 冒充 Autonomous E2E；
- external provider quality/cost 的虚构验证；
- 任何未经批准的 Schema migration、active DB rewrite 或 destructive data migration。

## 4. Runtime Reuse Contract

实现必须复用：

- Work；
- Responsibility Assignment；
- Responsibility Router；
- Team Operating Engine；
- Employee Execution；
- Provider Task / Session；
- Result；
- Evidence；
- Decision；
- Handoff；
- immutable Operating Definition；
- Context isolation；
- existing restart / recovery。

禁止创建：

- second Task Runtime；
- second Workflow Runtime；
- second Employee Runtime；
- second Result Runtime；
- generic Autonomous Agent Runtime；
- 与既有 Company / Workspace Truth 平行的 scope store。

Operating Lifecycle 是 Company OS 的 thin control plane，不接管专业 Domain Primary Surface。

## 5. Product Contract → Implementation Classification

实现开始前，逐项核对并在 Review 中填写实际映射；本表不是 Schema 预案：

| Product concept | Required classification | 约束 |
|---|---|---|
| Operating Responsibility | EXISTING OBJECT 或 EXTEND EXISTING | 复用现有责任 / Assignment；不得新造 Leader 身份 |
| Intent | EXISTING OBJECT / DERIVED | 读取现有经营意图；缺失时由 Conversation / Proposal 产生，不直接建重复 Truth |
| Goal | EXISTING OBJECT / EXTEND EXISTING | 使用 canonical Company / Business / Workspace scope |
| Approved Strategy Envelope | VERSIONED SCOPE TRUTH | 只存经批准的边界引用与版本；不得让 Leader 越界改 Goal |
| Strategy | VERSIONED SCOPE TRUTH 或 EXTEND EXISTING | 固定到 Cycle；不自动覆盖下一轮前的当前策略 |
| Operating Plan | VERSIONED SCOPE TRUTH | bounded、可解释、可回放；不做永久计划 |
| Operating Cycle | VERSIONED SCOPE TRUTH | 仅 Workspace scope；生命周期对象与 Work/Execution 分离但复用它们 |
| Situation Snapshot | DERIVED | 从当前 Company Truth / Result / Signal 生成，可重建；不作为第二事实源 |
| Result | EXISTING OBJECT | 复用既有 Result Contract；不从完成状态推断业务价值 |
| Evidence | EXISTING OBJECT | 来源、freshness、可信度和人工回填边界保持不变 |
| Signal | DERIVED | 必须可追溯到来源与窗口；不把 AI 猜测写成 Company Fact |
| Review | EXTEND EXISTING 或 DERIVED | 复用 Review / Decision 语义；不新建 Review Center |
| Learning | VERSIONED SCOPE TRUTH / EXTEND EXISTING | 只有 accepted Learning 才能影响下一轮 |
| Next-cycle Decision | VERSIONED SCOPE TRUTH | actor、理由、证据、nextCheckAt、幂等键必须可回放 |
| Trigger intake / claim | EXTEND EXISTING | 只实现三类 V1 trigger；必须幂等、可取消、可恢复 |
| Evaluation Contract | VERSIONED SCOPE TRUTH | 至少支持 metric/proxy、source、freshness、window、sample、baseline、materiality、confounder、cooldown、risk/permission/budget gate |
| Context Package | DERIVED | reference-first、summary-first、retrieve-on-demand；不默认携带完整历史 |
| Temporary AI reasoning | TEMP AI REASONING | 只能用于解释 / 提案；没有 Evidence / Review 不得直接改策略 |
| External event engine | NOT V1 | 未来由 Domain Adapter 扩展 |
| Business-scope Provider Execution | NOT V1 | 不得由 Workspace 证明冒充 |

任何项若无法归入上述类别，先 `STOP / REPORT PRODUCT → IMPLEMENTATION GAP`，不得直接加表或加 Primitive。

## 6. Minimum Control Responsibilities

仅允许增加以下必要控制职责：

1. Trigger intake / claim；
2. one active Cycle per canonical Workspace operating scope；
3. Situation Snapshot；
4. Strategy / Plan pinning；
5. bounded Plan release；
6. Review；
7. accepted Learning；
8. Next-cycle Decision；
9. atomic successor creation；
10. durable WAIT / PAUSE / STOP；
11. restart-safe continuation。

这些职责必须通过现有 Company / Workspace / Responsibility / Result 关系工作，不产生第二套组织或执行关系。

## 7. Cycle Contract

产品生命周期必须可投影为：

```text
START → SENSE → PLAN → OPERATE → REVIEW → DECIDE → CLOSE
```

Runtime 可以映射到既有状态，不要求同名 enum。硬约束：

- bounded；
- terminal；
- 同一 Workspace operating scope 最多一个 active Cycle；
- pinned Goal / Strategy / Plan / Operating Definition；
- idempotent；
- restart-safe；
- 不允许 `while(true)`、permanent agent session 或 implicit continuation。

Cycle Close 是正常周期终止，不等于 Operating STOP。

## 8. Next-cycle Decision Contract

支持：`CONTINUE`、`ADJUST`、`WAIT`、`ESCALATE`、`PAUSE`、`STOP`。

| Decision | 必须结果 |
|---|---|
| CONTINUE | 只创建 exactly one successor Cycle |
| ADJUST | 在 Approved Strategy Envelope 内调整，并只创建 exactly one successor Cycle |
| WAIT | 无 active Cycle；必须有 `nextCheckAt` 或明确 callback condition |
| ESCALATE | 进入 CEO / 已授权代理等待；不得偷偷继续 |
| PAUSE | 暂停 Operating Series，保留 Goal / Strategy / Responsibility / History；显式 Resume |
| STOP | 终止 Operating Responsibility / Goal Series；不得由普通 Cycle terminal 自动触发 |

没有 Work、一次失败、一次 Review 或一次 Cycle terminal，均不得自动 STOP 整个责任系列。

## 9. Approved Strategy Envelope

Leader 只能在已批准边界内调整：

- hypothesis；
- tactic；
- cadence；
- experiment；
- resource allocation；
- Work priority；
- content / execution mix；
- bounded Plan。

以下必须 CEO Gate：Goal、Success Contract、Positioning、Target Audience、Business / Monetization Model、protected Strategy Boundary、material Budget、high-impact / irreversible commitment。

`ADJUST` 不等于 Leader 可以修改任意 Strategy。

## 10. Evaluation / Learning Gate

禁止：`AI summary → Strategy change`。

必须形成：

```text
Result / Evidence
→ Signal
→ Interpretation
→ Authorized Review
→ accepted Learning
→ Strategy / Plan change
```

Evaluation Contract 至少支持：metric / proxy、source、freshness、observation window、minimum sample、baseline、materiality、confounder、cooldown、risk / permission / budget gate。

证据不足时只允许 `CONTINUE`、`WAIT` 或 `ESCALATE`，不能自主 `ADJUST Strategy`。

## 11. V1 Triggers

只实现：

1. Result-driven；
2. Scheduled review / `nextCheckAt`；
3. Leader / CEO initiated。

不实现 generic external event engine 或 arbitrary threshold rule engine；外部事件由未来 Domain Adapter 扩展。

## 12. Context Contract

Context 必须 reference-first、summary-first、retrieve-on-demand。默认仅带：

- scope / cycle refs；
- Goal summary；
- Strategy summary；
- Plan；
- accepted Learning；
- current Signals；
- Result metadata；
- Decision metadata；
- retrieval hints。

默认禁止携带 full conversations、all prior cycles、evidence bodies、provider traces、all employee sessions。

`1750–4500 tokens`、`p95 < 6000` 只是测试目标，不是 Product Truth；若实测超出，记录证据和恢复动作，不通过静态数字伪装达标。

## 13. Failure / Recovery Contract

至少覆盖：Provider failure、capability missing、Result Contract failure、duplicate callback、late Result、Runtime restart、leader crash、CEO silence、repeated strategy failure、no new data、permission revoked、budget exhausted、trigger storm、Goal achieved。

每种失败都必须能回放：

```text
owner
state
reason
recovery path
next action
```

禁止伪造成功、吞掉失败、将 RUNNING 留作无责任终态、在未授权时自动重发外部副作用。

## 14. Product Surface Adapter Contract

实现完成后只增强既有表面：

| Surface | 只消费 |
|---|---|
| CEO Desk | Needs You / Important Result / Company Operating |
| Business | Operating Summary / Workspace Directory |
| Workspace | 经营状态 / 本轮重点 / 最新判断 / 下一步 / 条件性 Need/Risk |
| Leader Conversation | Why / Evidence / Boundary / Next |

禁止创建 Operating Console、Strategy Center、Review Center、Learning Center、Cycle UI，禁止把内部 enum 直接给用户。

## 15. Domain Proof Contract

### 15.1 Primary Autonomous E2E

至少一个真实 Domain 连续完成 ≥2 Cycles：

```text
Goal
→ Strategy
→ Plan
→ Team Operating
→ real Employee execution
→ Result / Evidence
→ Review
→ accepted Learning
→ CONTINUE / ADJUST
→ Cycle 2
→ second Result
```

并验证 restart、duplicate trigger、late Result、WAIT、ESCALATE、CEO Gate。不得用 fake Result、fake Analytics 或 static UI 冒充。

### 15.2 Cross-domain Contract Proof

第二 Domain 必须证明同一 Lifecycle 可适配不同 Strategy、Team Operating、Result Contract、Signal、Evaluation 与 Risk；允许 controlled / replay evidence，但必须标明来源和限制，不冒充真实外部 E2E。

XHS + RD 为首批候选，不预设哪一个先成为 Primary。

## 16. Implementation Phases / Queue

实现可以安全合并相邻 Phase，但必须保留证据边界：

| Phase | 目标 | 进入条件 |
|---|---|---|
| 0 | Current Runtime / schema / Cycle truth audit | Business Spine Accepted |
| 1 | Lifecycle control persistence / refs | Phase 0 无冲突 |
| 2 | Trigger claim + single active Cycle | Phase 1 |
| 3 | Situation / Strategy / Plan pinning | Phase 2 |
| 4 | Plan → existing Team Operating execution | Phase 3 + existing Employee path |
| 5 | Review / Learning / Evaluation gate | Phase 4 有真实 Result/Evidence |
| 6 | Next-cycle Decision + atomic continuation | Phase 5 |
| 7 | CEO Gate / WAIT / PAUSE / STOP / recovery | Phase 6 |
| 8 | Product surface adapters | Phase 7 |
| 9 | Primary 2-cycle E2E | Phase 8 + Domain evidence |
| 10 | Cross-domain proof + replay / context budget | Phase 9 + second Domain |

若 Phase 0 发现需要新 Runtime Primitive、canonical scope unresolved、Strategy ownership ambiguous 或 Evaluation Contract insufficient，立即停止并建立 Gap Review；不得进入下一 Phase。

## 17. Allowed Files / Evidence Boundary

本 Issue 只有在 Start Gate 通过且后续每个 Phase 生成独立 Allowed Files 后才授权代码修改。准备阶段不授权以下任何文件写入：

- Runtime / backend；
- Schema / migrations；
- database / active data；
- frontend / UI；
- Prototype / high-fidelity；
- dependencies / lock files；
- secrets / credentials。

实施时必须先在子 Issue / Approved Design 中列出精确 Allowed Files、输入、输出、测试与 Browser/Desktop/SQLite 证据。不得 whole-file promotion、bulk untracked copy、seed 伪造对象或跨隔离 DB 拼证据。

## 18. Stop Gates

立即 `STOP / REPORT`：

- canonical scope unresolved；
- Strategy ownership ambiguous；
- Evaluation Contract insufficient；
- 需要 new Runtime primitive；
- active DB migration；
- destructive migration；
- external side-effect authority unclear；
- Product Contract conflict；
- commit / push gate；
- 缺少合法 Browser/Desktop/restart/recovery evidence。

## 19. Required Handoff / Acceptance Evidence

每个 Phase 必须回传：

1. Issue / Allowed Files；
2. Product → Implementation classification；
3. isolated SQLite 与 restart 证据；
4. Browser / Desktop（如适用）证据；
5. failure / recovery 证据；
6. no-fake / no-secret / no-cross-tenant 检查；
7. `git diff --check`、focused tests 与 baseline regression；
8. Review 的 Verdict / Disposition / Owner / Next Action / Target Authority / Next Gate。

只有 Accepted Review 才能解除下一 Phase。

## 20. Start / Stop State

```text
CURIS AUTONOMOUS OPERATING V1
— IMPLEMENTATION ISSUE PREPARED
— CONTRACT BOUNDARY LOCKED
— EXISTING RUNTIME REUSE LOCKED
— PRIMARY / CROSS-DOMAIN PROOF LOCKED
— WAITING FOR CANONICAL BUSINESS SPINE ACCEPTANCE
— NO IMPLEMENTATION
— STOP
```

## 21. Start Gate Passed / Phase 0 Audit Result（2026-08-21）

### 21.1 Start Gate evidence

Canonical Business Spine 已由 `docs/reviews/CURIS_CANONICAL_BUSINESS_SPINE_IMPLEMENTATION_001_REVIEW.md` 正式记录为 `IMPLEMENTED / ACCEPTED`，对应 commit：

```text
50d058ca865c1817721536d7beb47a1c5f1f354d
```

Accepted evidence 覆盖 canonical Business、Department relation、Workspace relation、Business + First Workspace 原子创建、Parent Resolver、Business Read Model、legacy `UNRESOLVED → QUARANTINED`、clean frontend/Desktop source baseline，以及 freshly packaged Desktop 的 Single / Multi / Generic / Legacy / restart 纵向证明。

因此本 Issue 的 Hard Start Gate 已通过；Phase 0 只读审计已获授权并完成。

### 21.2 Phase 0 result

正式审计记录：

- `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE0_RUNTIME_TRUTH_AUDIT.md`

结论：

- existing Work / Task / Responsibility Assignment / Router / Team Operating / Employee / Provider Task+Session / Result / Evidence / Artifact / Decision / Handoff / Context / Capability / Package 均有真实可复用底座；
- existing `CYCLE`、scheduler、Review 与 Decision 只能扩展，不能直接冒充 Autonomous control plane；
- Strategy、Approved Strategy Envelope、完整 Evaluation Contract、accepted Learning、六分支 Next-cycle Decision 与 exactly-one successor 尚未实现；
- 最小新控制真相仅为 Workspace-scoped Operating Series control record 与 deterministic Trigger Claim record；
- `CYCLE`、`DECISION_PACKET`、现有 Assignment/Result/Evidence/Review/trigger ingress 应受限扩展；
- Package Method Metadata 不是 V1 blocker；
- 不需要、也不允许创建第二套 Task / Workflow / Employee / Router / Provider / Result / Evidence / Decision Runtime。

### 21.3 Next Gate

Phase 1 尚未实现，也未由本记录授权修改 Runtime/Schema。建议下一 bounded Issue 只覆盖：

1. Operating Series / Trigger Claim 的最小持久化合同；
2. existing Cycle 的 Goal / Strategy / Envelope / Plan / Evaluation pin；
3. one active Cycle per Series；
4. trigger claim idempotency；
5. `WAIT / PAUSE / STOP` restart truth；
6. isolated SQLite / scope / duplicate / restart tests。

Phase 1 不执行 Employee、不产生 Learning、不创建 successor；若需要 shared schema/state registry 变更，必须先证明 `runtime_entities` / `runtime_links` 无法承载并返回 Review。

```text
CURIS AUTONOMOUS OPERATING V1
— START GATE PASSED
— PHASE 0 RUNTIME TRUTH AUDIT COMPLETE
— IMPLEMENTATION NOT STARTED
— READY FOR CEO REVIEW
— STOP
```
