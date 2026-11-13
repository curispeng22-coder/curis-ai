# CURIS AUTONOMOUS OPERATING V1 — PHASE 0 RUNTIME TRUTH AUDIT

**Authority Class:** REVIEW  
**Status:** Review  
**Disposition:** START GATE PASSED — PHASE 0 AUDIT COMPLETE — IMPLEMENTATION NOT STARTED  
**Date:** 2026-08-21  
**Issue:** `issues/20260820_autonomous_operating_v1_implementation_001.md`  
**Owner:** 主开发 / Runtime Integration  
**Next Gate:** CEO Review of the minimal V1 control-plane gap and Phase 1 bounded scope

## 0. Verdict

```text
CANONICAL BUSINESS SPINE = IMPLEMENTED / ACCEPTED
AUTONOMOUS OPERATING V1 START GATE = PASSED
PHASE 0 RUNTIME TRUTH AUDIT = COMPLETE
AUTONOMOUS OPERATING V1 IMPLEMENTATION = NOT STARTED
```

Curis 已有真实、可复用的 Workspace-scoped 执行底座：canonical Scope、Work、Task、Responsibility Assignment、Router、Team Operating、Employee、Provider Task/Session、Result/Evidence/Artifact、Decision、Handoff、Context、Persistence 与 restart-safe failure truth。它不是空白系统。

Curis 尚未形成真实的跨周期 Autonomous Operating control plane。缺口集中在五个硬真相：长期 Operating Series、可靠 Trigger Claim 与 single-active Cycle、版本化 Strategy + Approved Strategy Envelope、Evidence-bound Review/Learning、以及六分支 Next-cycle Decision + exactly-one successor。现有 RD Cycle、Scheduler、Decision Packet 与 Review 能力只能作为扩展点，不能直接宣称已满足这些语义。

本轮没有发现需要新 Task、Workflow、Employee、Router、Provider、Result、Evidence 或 Decision Runtime 的理由。Package Method Metadata 不是 V1 硬依赖。

## 1. Audit boundary and evidence

### 1.1 Product and implementation inputs

- `issues/20260820_autonomous_operating_v1_implementation_001.md`
- `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_IMPLEMENTATION_READINESS.md`
- `docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md`
- `docs/reviews/CURIS_AUTONOMOUS_BUSINESS_OPERATION_SYNTHESIS.md`
- `docs/reviews/CURIS_THREE_LAYER_OPERATING_MODEL_RECONCILIATION.md`
- `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/reviews/CURIS_CANONICAL_BUSINESS_SPINE_IMPLEMENTATION_001_REVIEW.md`
- accepted Business Spine commit `50d058ca865c1817721536d7beb47a1c5f1f354d`

### 1.2 Runtime evidence inspected

- Schema: `backend/app/runtime/models.py`, `backend/app/runtime/scheduler.py`, ResultStore schema.
- Services/repositories: `RuntimeFoundation`, `CanonicalBusinessSpine`, `WorkspaceRuntime`, `ResponsibilityRoutingRuntime`, `RuntimeScheduler`, `ResultStore`, Workspace Package Runtime.
- API: `runtime_foundation_router.py`, `team_operating_router.py`, `ceo_day_router.py`, current app registration.
- State machines: `runtime/states.py`, `runtime/registry.py`, transition log and recorder.
- Tests: Team Operating E2E, Responsibility Routing, RD Operating Cycle / Phase 2B, Scheduler restart, Package lifecycle/migration/restart, Canonical Business Spine.
- Persistence/restart behavior: SQLite entities/links/transition logs, persisted scheduler rows, restart reconciliation, duplicate/idempotency tests.

No Runtime, Schema, API, test, frontend, package or active database was changed.

## 2. Start Gate record

The accepted Business Spine proves:

| Gate fact | Accepted evidence |
|---|---|
| Canonical Business | `canonical_businesses` persisted identity |
| Department relation | Business must reference an existing Department in the same Company |
| Workspace relation | Resolved Workspace must reference an existing canonical Business |
| Atomic first Workspace | Business + first DRAFT Workspace + first Workspace version in one transaction |
| Parent Resolver | authoritative `Workspace → Business → Department → Company` |
| Business Read Model | definition, operating summary, Workspace Directory and Business Team derived from canonical relations |
| Legacy ambiguity | `UNRESOLVED → QUARANTINED`, no guessed default Business |
| Clean frontend/Desktop | accepted controlled clean source baselines |
| Packaged proof | Single / Multi / Generic / Legacy / restart in freshly built Desktop |
| Accepted commit | `50d058ca865c1817721536d7beb47a1c5f1f354d` |

The Autonomous V1 canonical Workspace scope is therefore resolvable without legacy free-form identity.

## 3. Existing Runtime object audit

Status meanings in this audit are restricted to `IMPLEMENTED`, `PARTIAL`, `MISSING`, and `NOT REQUIRED V1`.

| Concept | Canonical object / source | Persistence, owner, scope, version/restart | Current consumers and extension point | Status / limitation |
|---|---|---|---|---|
| Work | Existing domain Work stored as `runtime_entities`; Team Operating attaches `responsibilityRouting` to the Work | SQLite; domain owner; Company/Workspace scope; pinned workflow version survives restart | Responsibility Router and Team Operating; bounded Plan may release existing Work | **IMPLEMENTED**. Work is not long-term Operating Responsibility or Cycle. |
| Task | ResultStore Task and Provider task records | SQLite; Runtime/Provider owner; execution scope; state/audit survives restart | Employee execution, Provider session/callback, RD execution | **IMPLEMENTED**. Must not become an Autonomous Task type. |
| Assignment | Existing role/employee assignment records | SQLite; Company/Workspace scope; immutable operating definition snapshots | Team Operating and execution identity | **IMPLEMENTED**. An assignment is not a continuing Operating Series. |
| Responsibility | Responsibility semantics on Work and Assignment | SQLite projection inside Work; holder/executor separated; restart-safe | Router, Employee workstations, execution bridge | **PARTIAL** for autonomous operation: current responsibility is real, but long-lived PAUSE/STOP series control is absent. |
| Responsibility Assignment | `RESPONSIBILITY_ASSIGNMENT` Runtime entity | SQLite; canonical Employee × Role × Scope; can be Workspace or Business scoped; restart-safe | Router, Team Operating, Business Team read model | **IMPLEMENTED**. Reuse as the holder/Leader authority source. |
| Responsibility Router | `ResponsibilityRoutingRuntime` | SQLite data + transaction/transition evidence; duplicate-safe | CONTINUE/WAIT/RETURN/CONSULT/REVIEW/HANDOFF/DECISION_GATE/NEED_LEADER | **IMPLEMENTED** for Work routing. It does not decide cross-cycle continuation. |
| Team Operating | `RESPONSIBILITY_WORKFLOW` + Team Operating adapter | SQLite; published version and default flow pinned on Work; restart-safe | real Employee execution loop | **IMPLEMENTED**. Reuse as Plan execution, not as the lifecycle controller. |
| Operating Definition | `RESPONSIBILITY_WORKFLOW` immutable published snapshot | SQLite; scoped and versioned; pinned on Work | Team Operating | **IMPLEMENTED**. It can carry bounded role/input/output routing, not Goal/Strategy authority. |
| Employee | canonical `AI_EMPLOYEE` Runtime entity | SQLite; Company/Workspace identity and lifecycle; restart-safe | Assignment, execution identity, UI projection | **IMPLEMENTED**. Do not add Autonomous Agent identity. |
| Role | `ROLE_SLOT` plus Assignment | SQLite; org/workspace version references | Team Operating and Employee assignment | **IMPLEMENTED**. Leader remains Employee × Role × Assignment. |
| Provider Task | ResultStore Task / execution binding | SQLite; provider/session provenance and callback verification | real Employee execution | **IMPLEMENTED**. External live provider quality/cost remains evidence-dependent. |
| Provider Session | Agent Adapter session/binding records | SQLite references; restart does not pretend an unverified external process is alive | RD/Codex and Team Operating execution | **IMPLEMENTED**. Session is executor evidence, not Employee or Responsibility. |
| Result | ResultStore result/output contract and Runtime result refs | SQLite; source/session/callback provenance | Router, Workspace, Review, Result Reference | **IMPLEMENTED**. Completion does not imply business value. |
| Evidence | `EVIDENCE` Runtime entities and ResultStore evidence refs | SQLite; verification status and condition; restart-safe | Acceptance, Review, Utility | **IMPLEMENTED**. Freshness/window semantics are not yet a full Evaluation Contract. |
| Artifact | ResultStore/runtime `ARTIFACT` with changed files/diff/test refs | SQLite; Task/Cycle parent and provider/session provenance | RD, Utility, Result Reference | **IMPLEMENTED**. May hold an accepted-learning artifact, but cannot by itself authorize Learning. |
| Decision | `DECISION_PACKET` state machine and P7-compatible packets | SQLite; actor/reason/evidence/options; restart-safe | Work decision gates and RD decisions | **PARTIAL** for Autonomous V1: current packet is real, but no six-action next-cycle policy, Leader envelope authorization, or atomic successor. |
| Handoff | shared persisted Handoff and RD provider-ACK path | SQLite; sender/receiver/ACK/provenance; restart and duplicate-safe | Team Operating, RD multi-employee | **IMPLEMENTED**. Handoff is responsibility transfer, not next-cycle decision. |
| Context | reference-first execution context and scoped refs | Work/Cycle data and links; reconstructed after restart | Employee execution / Provider prompt | **IMPLEMENTED**. Keep summary-first and retrieve-on-demand. |
| Workspace | canonical Workspace row + Runtime versions/entities | SQLite; Company/Business relation, blueprint and operating version; restart-safe | all domain Runtime and Package host | **IMPLEMENTED**. Autonomous V1 must be Workspace-scoped. |
| Business | `canonical_businesses` + Business Spine | SQLite; Company/Department relation; persisted goal and strategy-direction ref | Business read model, Workspace parent resolver | **IMPLEMENTED** identity; Strategy content is not implemented merely because a ref column exists. |
| Cycle | existing global `CYCLE` entity/state machine; RD-only creation/service | SQLite; bounded start/run/accept/review/close/failure/restart | RD Workspace | **PARTIAL**. Domain-specific; no one-active-series invariant, strategy/plan/evaluation pins, six decisions, or successor creation. |
| Trigger / Schedule | persisted `cadences`/`scheduled_runs`; manual API actions; Result callbacks | SQLite cadence/run rows; queued run restart test | CEO Day scheduler and execution adapters | **PARTIAL**. Schedule exists; manual exists; result callback exists. No canonical Workspace trigger claim/merge/cancel, result-driven next-Cycle intake, or trigger-storm protection. Default scheduler executor is simulated. |
| Capability | Catalog/Connection/Health/Binding Runtime | SQLite; scoped status and verification evidence | Workspace readiness and execution binding | **IMPLEMENTED**. Missing capability remains a recoverable wait/gap, not fake execution. |
| Package | Dynamic Workspace Package Runtime and lifecycle/migration journal | SQLite + package store; version/update/rollback/restart | generic Workspace surfaces and domain composition | **IMPLEMENTED** host/lifecycle. Method metadata is future capability, not V1 hard dependency. |

## 4. Autonomous concept truth map

### 4.1 Operating Responsibility

The holder must remain the existing Workspace-scoped `RESPONSIBILITY_ASSIGNMENT`. `Task`, `Work`, and `Assignment` must not be promoted into the long-lived series itself.

What is missing is a thin durable **series control record** that binds one canonical Workspace operating scope to the continuing Goal/Leader assignment, current Strategy version, lifecycle (`ACTIVE/WAITING/PAUSED/STOPPED` semantics), current/last Cycle refs and history. It is control truth, not a second Responsibility primitive.

### 4.2 Goal

- **Business Goal:** real and persisted in `canonical_businesses.goal`; returned by the Business Read Model.
- **Workspace Goal:** present inside Workspace blueprint/version/domain data, not normalized as one canonical, independently versioned Runtime Goal object.
- **Runtime pinning:** current RD Cycle stores `outcomeRef` and `intentRef`, not an authoritative Goal version/success contract snapshot.

Status: **PARTIAL**. Phase 1 must identify the authoritative existing Business/Workspace goal reference and pin it; it must not create a duplicate Goal store.

### 4.3 Strategy and Approved Strategy Envelope

`canonical_businesses.strategy_direction_ref` is only a nullable reference. No inspected service creates, versions, approves, resolves or enforces a Strategy body or Approved Strategy Envelope. Workspace blueprints can contain domain configuration, but that is not proof of authorized strategy truth.

- Strategy: **MISSING** as an authoritative, versioned, Cycle-pinnable Runtime truth.
- Approved Strategy Envelope: **MISSING**. A Leader prompt or free-form instruction cannot substitute for it.

### 4.4 Operating Plan

Existing immutable Operating Definition, Work, Assignment and Team Operating can execute a bounded Plan. They do not currently provide one Cycle-level released Plan snapshot linking Goal/Strategy/Evaluation/Work refs.

Status: **PARTIAL**. Extend the existing Cycle control data with an immutable plan release manifest/reference; do not add a Workflow or DAG.

### 4.5 Operating Cycle

The existing Cycle is bounded, persisted, failure-aware, reviewable and closable. It is currently RD-specific at creation and binds RD execution requirements. Its `close_operating_cycle()` records a Decision Packet with `CONTINUE/ADJUST/PAUSE`, then closes the Cycle; it does **not** create a successor.

Status: **PARTIAL**. Required implementation classification: `EXTEND EXISTING`. Keep the canonical `CYCLE` entity/state machine and add a separate thin autonomous service/repository contract; do not create `AUTONOMOUS_CYCLE`.

### 4.6 Trigger

| Trigger type | Current truth | V1 disposition |
|---|---|---|
| Leader / CEO initiated | real API/manual action paths | reuse |
| Scheduled review / `nextCheckAt` | persisted cadence/run and entity `next_check_at` exist | extend into canonical Workspace claim |
| Result-driven | real provider callback/result completion exists | extend with idempotent trigger intake |
| Generic external event | no accepted generic engine | **NOT REQUIRED V1** |

Current trigger coverage is therefore **three sources partially available, zero accepted Autonomous trigger-claim paths**.

### 4.7 Evaluation Contract

Real pieces exist: Result output contracts, Evidence references/verification, Acceptance, test/build evidence and Review. Missing are one versioned evaluation snapshot with metric/proxy, source, freshness, observation window, sample, baseline, materiality, confounder, cooldown and risk/permission/budget gates.

Status: **MISSING** as a complete contract. It should be a bounded snapshot pinned on the Cycle, reusing Result/Evidence/Acceptance rather than a second evaluator system.

### 4.8 Review

Work Review, RD Artifact Review, Acceptance and CEO Decision are persisted and restart-safe. No inspected service performs an authorized Cycle-level Review that converts Result/Evidence into Signal/Interpretation and records an accepted Learning.

Status: **PARTIAL**. Reuse existing review/evidence/decision facts; add only a Cycle review snapshot and authorization rule.

### 4.9 Learning

Memory, Knowledge, Result, Evidence, Review and ResultStore evolution/development strategy tables are not an accepted Learning promotion path. No current code proves:

```text
Evidence → Signal → Interpretation → Authorized Review → accepted Learning
```

Status: **MISSING**. V1 can store the accepted Learning as a versioned Artifact/reference attached to the closed Cycle; no Learning Engine or second Knowledge system is justified.

### 4.10 Next-cycle Decision

Current Work `DECISION_GATE` and RD `DECISION_PACKET` are real. RD close supports only `CONTINUE`, `ADJUST`, `PAUSE`; all decisions are CEO-driven and no successor is created. `WAIT`, `ESCALATE`, `STOP`, Leader authority checks, `nextCheckAt`, predecessor/successor refs and deterministic successor idempotency are absent.

Status: **MISSING** for the Autonomous next-cycle contract, implemented by extending the existing `DECISION_PACKET`, not by adding a parallel decision type.

## 5. Leader authority truth

Workspace Leader identity is real when an existing `RESPONSIBILITY_ASSIGNMENT` resolves canonical Employee × Role × Workspace scope with `isLeader`. Team Operating can resolve and execute that assignment.

The authority boundary is incomplete because no Runtime representation of an Approved Strategy Envelope exists. Therefore:

- Leader identity/assignment: **IMPLEMENTED**.
- Leader autonomous adjustment authority: **PARTIAL**.
- A prompt saying “you may adjust strategy” is not authority evidence.
- Until an envelope is pinned and verified, `ADJUST` must fail closed or escalate to CEO.

## 6. Control-plane classification

### 6.1 REUSE

Canonical Company/Department/Business/Workspace; Work; Task; Responsibility Assignment; Router; Team Operating; Operating Definition; Employee; Role; Provider Task/Session; Result; Evidence; Artifact; Handoff; Context; Capability; Package; transition log; identity and callback provenance.

### 6.2 EXTEND

- existing `CYCLE`: autonomous scope refs, Goal/Strategy/Envelope/Plan/Evaluation pins, phases and predecessor/successor references;
- existing `DECISION_PACKET`: six next-cycle choices, actor authority, evidence/reason, `nextCheckAt`, idempotency and applied-successor reference;
- existing Responsibility Assignment: link from the series control record; no new Leader identity;
- existing scheduling/result/manual ingress: deterministic Workspace-scoped trigger claim;
- existing Artifact/Evidence/Review: accepted Learning artifact and Cycle review snapshot;
- existing projection/API: summary only, after Runtime acceptance.

### 6.3 NEW MINIMAL CONTROL TRUTH

Only two new durable control records are justified by current evidence:

1. **Operating Series control record** — one continuing Workspace operating scope, linking canonical Goal, Leader Responsibility Assignment, approved Strategy/Envelope version, lifecycle, current/last Cycle and history. It is not a new Responsibility, Task or Workflow.
2. **Trigger Claim record** — a deterministic claim for one of the three V1 trigger sources, with source key, Workspace/Series, status, merge/cancel/apply result and timestamps. It is required to survive restart and prevent duplicate active/successor Cycles.

The following do not require new top-level primitives in V1:

- Strategy/Envelope can be one versioned scope-truth record referenced by Series/Cycle; this is a versioned configuration truth, not a Strategy Engine.
- Plan release, Evaluation snapshot and Cycle Review can be immutable snapshots within/persisted beside the existing Cycle record.
- accepted Learning can be an evidence-bound Artifact/reference attached to the Cycle.
- Next-cycle Decision extends `DECISION_PACKET`.

Phase 1 must validate whether `runtime_entities` + `runtime_links` can persist these records without an active DB migration. A new dedicated table or migration is **not authorized by this audit**.

## 7. Required Gap Matrix

| Concept | Current object | Status | Evidence | Reuse? | Extension required? | New object required? | V1 / Future | Risk |
|---|---|---|---|---|---|---|---|---|
| Operating Responsibility | Workspace `RESPONSIBILITY_ASSIGNMENT` | PARTIAL | canonical scoped Assignment and Leader flag | yes | series linkage/lifecycle | minimal Series control only | V1 | confusing Work responsibility with long-lived series |
| Goal | Business row; Workspace blueprint/version | PARTIAL | persisted Business goal; no Cycle pin | yes | authoritative ref + pin | no duplicate Goal | V1 | stale/unversioned goal |
| Strategy | nullable Business strategy ref / domain config | MISSING | no authoring/version/approval service | limited | versioned scope truth | bounded strategy version record | V1 | AI reasoning promoted as fact |
| Strategy Envelope | none | MISSING | no representation/enforcement | no | authority validation | may share strategy-version record | V1 | Leader overreach |
| Operating Plan | Operating Definition + Work | PARTIAL | versioned workflow and Work routing | yes | Cycle plan-release snapshot | no | V1 | permanent/fixed workflow |
| Operating Cycle | existing `CYCLE` | PARTIAL | RD bounded lifecycle/restart | yes | generic control refs and invariants | no second Cycle | V1 | RD state mistaken for autonomous truth |
| Trigger claim | cadence/manual/result callbacks | PARTIAL | persisted schedule and callbacks, no claim | yes | canonical claim/merge/cancel | minimal Trigger Claim | V1 | duplicate Cycle/trigger storm |
| Evaluation Contract | output/evidence/acceptance fragments | MISSING | no complete versioned snapshot | yes | snapshot + gate | no evaluator engine | V1 | unsupported strategy adjustment |
| Review | Work/RD review and acceptance | PARTIAL | persisted review/decision facts | yes | Cycle review snapshot | no Review system | V1 | review without authority/evidence |
| Learning | none accepted | MISSING | no evidence-bound promotion path | use Artifact/Evidence | accepted-learning reference | no Learning Engine | V1 | AI summary mutates strategy |
| Next-cycle Decision | `DECISION_PACKET` | MISSING | current packets lack six choices/successor | yes | choice/authority/idempotency | no second Decision | V1 | duplicate or implicit continuation |
| Exactly-one successor | none | MISSING | RD close creates no successor | use DB transaction | deterministic successor creation | no queue engine | V1 | two active Cycles |
| Restart continuation | persisted Work/Cycle/Scheduler; fail-closed external execution | PARTIAL | restart tests and reconciliation | yes | lifecycle recovery/claim replay | no | V1 | stale RUNNING treated as live |
| External event engine | none | NOT REQUIRED V1 | contract explicitly excludes it | no | no | no | Future | scope expansion |
| Package Method Metadata | Package host exists; metadata gap | NOT REQUIRED V1 | first Plan can be explicitly pinned from accepted inputs | yes later | future package extension | no now | Future | architecture work before evidence |

## 8. Three-layer placement

| Layer | Autonomous V1 content |
|---|---|
| User Surface | current operating summary, latest result/judgment, next action, conditional Need/Risk/CEO Gate; no Cycle/trigger/router console |
| Employee Operating Layer | Leader consumes Goal, approved envelope, situation, bounded plan, accepted learning and result/evidence; Employee receives only Assignment-scoped context |
| System Runtime | Series/Cycle/trigger claim, version pins, Team Operating release, Result/Evidence links, review/decision truth, exactly-one successor, WAIT/PAUSE/STOP and restart recovery |

Internal Cycle phases, claim keys, router state and provider sessions remain technical details.

## 9. Persistence, restart and exactly-one successor

| Candidate truth | Why persist | Restart source of truth | Duplicate control |
|---|---|---|---|
| Operating Series | PAUSE/STOP/WAIT and current responsibility outlive processes | one canonical Workspace-scoped record | reject/return existing active series for same operating scope |
| Trigger Claim | trigger can arrive before/after restart and more than once | deterministic source key + persisted claim state | same trigger key returns/merges existing claim |
| Cycle control extension | pins what was actually operated and reviewed | existing persisted `CYCLE` + transition log | one active Cycle per Series; deterministic successor key |
| Strategy/Envelope version | authority cannot depend on prompt memory | persisted version and approval provenance | Cycle pins immutable version |
| Evaluation/Review snapshot | Learning and decisions must replay from evidence | closed Cycle snapshot + evidence refs | one finalized review per Cycle/version |
| Next-cycle Decision | actor/reason/evidence/action must survive restart | extended `DECISION_PACKET` | idempotent apply key; applied decision returns same successor |

Exactly-one successor should use one SQLite `BEGIN IMMEDIATE` transaction that:

1. reloads the predecessor Cycle, Decision Packet, Series and active-Cycle truth;
2. verifies Decision is authorized and not already applied;
3. derives a deterministic successor identity/idempotency key from Series + predecessor + Decision;
4. inserts exactly one successor only for `CONTINUE/ADJUST`;
5. records the predecessor/successor links and marks the Decision applied in the same transaction;
6. returns the existing successor on replay.

`WAIT`, `ESCALATE`, `PAUSE`, and `STOP` create no successor. No in-memory lock, EventBus or UI button may be the source of this invariant.

## 10. Failure and recovery reuse

| Failure | Current reusable truth | Autonomous gap |
|---|---|---|
| Cycle execution failure | RD Cycle becomes `PAUSED/FAILED`, failure artifact/evidence preserved, no success evidence | map recovery to Series/Cycle without implicit next Cycle |
| Provider/employee failure | provider Task/Session status, verified callback, execution failure, current executor cleared/fail-closed | trigger/retry ownership and bounded policy |
| Missing capability/permission | Capability Health/Binding and Workspace gap fail closed | Series `WAIT`/`ESCALATE` projection and next check |
| Waiting external result | `next_check_at`, pending system/external status patterns | canonical scheduled claim and late-result correlation |
| CEO decision pending | real `DECISION_PACKET` `WAITING_CEO` | next-cycle decision choices and silence/expiry recovery |
| Duplicate callback | existing execution identity/idempotency checks | correlate callback to Cycle review/trigger claim |
| Restart mid-execution | RD reconciliation does not pretend an unverified Agent is still running | Series/Cycle recovery owner and resumable/non-resumable classification |
| Trigger storm | persisted scheduler has queue/capacity, Router has loop guard | Workspace-scoped deterministic claim/merge/cancel |

Existing failure truth is strong at the execution layer. The missing work is control ownership across Cycle boundaries, not another failure system.

## 11. Package / method and unknown-business boundary

Package Method Metadata is **NOT REQUIRED V1**. A first Autonomous V1 proof can start from an explicit, accepted Goal/Strategy/Envelope/Plan snapshot and an existing Operating Definition. No evidence shows that Package Method Metadata is needed to execute, review and continue that bounded proof.

Phase 0 does not authorize a generic industry research engine, automatic Package generation, Playbook Runtime, Capability Planner or self-evolution. Future integrations only need stable references into the Series/Cycle control record and existing Package/Capability/Knowledge surfaces.

## 12. Minimal Phase 1 recommendation

Phase 1 should be one bounded persistence/control issue, not autonomous execution:

1. prove `runtime_entities`/`runtime_links` can hold one Workspace-scoped Operating Series and deterministic Trigger Claim without a dedicated table;
2. define the minimal data contract for Series, Claim and existing Cycle pins;
3. resolve and validate existing Leader `RESPONSIBILITY_ASSIGNMENT`, Business/Workspace Goal ref and versioned Strategy/Envelope ref;
4. enforce one active Cycle per Series and claim idempotency in a single transaction;
5. persist/reload `WAIT/PAUSE/STOP` control truth and restart behavior;
6. add isolated SQLite tests for create/replay/restart/cross-tenant/scope failure;
7. do **not** release Work, call Employees, evaluate Results, create Learning, or create a successor yet.

Phase 1 exact Allowed Files should be limited to a small autonomous control service/repository module, existing Runtime export/registration seam, focused tests, Issue and Review. Any proposed edit to shared schema/state registry must first prove `runtime_entities` cannot carry the required truth and return for review.

## 13. Direct answers to the 20 required questions

1. **当前 Runtime 已有多少自主经营基础？** 执行底座 20 类核心对象/能力可复用；跨周期控制的五项硬真相仍未闭环。Curis 已会真实工作，但还不会可靠地自主经营下一轮。
2. **Operating Responsibility 谁承载？** 现有 Workspace-scoped `RESPONSIBILITY_ASSIGNMENT` 承载 Leader/责任人；新增的仅是一个薄 Operating Series 控制记录，不是第二责任对象。
3. **Goal 真实吗？** Business Goal 真实持久化；Workspace Goal 存于 blueprint/version/domain data，但缺少统一权威 pin；整体为 PARTIAL。
4. **Strategy 真实吗？** 不真实。只有 nullable ref/领域配置线索，没有版本化、批准、解析与执行证据。
5. **Strategy Envelope 真实吗？** 不真实，当前 MISSING。
6. **Plan 谁承载？** 现有 immutable Operating Definition + Work + Team Operating 承载执行；Cycle 只需薄的 Plan release snapshot/ref。
7. **Cycle 能否复用？** 能扩展现有 `CYCLE`，不能直接等同 Autonomous Cycle，也不能新建第二 Cycle。
8. **Evaluation 谁承载？** 复用 Result/Evidence/Acceptance，并在 Cycle 上增加版本化 Evaluation snapshot；当前完整合同 MISSING。
9. **Review 谁承载？** 复用既有 Work/RD Review、Acceptance、Decision 事实；补 Cycle-level authorized review snapshot。
10. **Learning 谁承载？** 当前无人承载 accepted Learning。V1 用 evidence-bound Artifact/reference + closed Cycle review，不建 Learning Engine。
11. **Next-cycle Decision 谁承载？** 扩展现有 `DECISION_PACKET`；不建第二 Decision 系统。
12. **Trigger 已有多少？** 三类来源都有部分基础：manual、scheduled、result callback；Autonomous claim 路径 0 条完整通过。
13. **Leader Authority 是否真实？** Leader identity/Assignment 真实；没有 Approved Strategy Envelope，因此自主调整权限仅 PARTIAL。
14. **restart continuation 已有多少？** Work/Task/Cycle/Scheduler/Package 持久化和执行 fail-closed 已有；Series/claim/next-cycle continuation 尚缺。
15. **exactly-one successor 如何保证？** 确定性 successor key + persisted trigger/decision state + SQLite 单事务 compare-and-create；重放返回同一 successor。
16. **哪些对象必须新增？** 最小仅 Operating Series control record 与 Trigger Claim record；Strategy/Envelope 需要版本化 scope truth，但不需要 Strategy Engine。
17. **哪些只需扩展？** `CYCLE`、`DECISION_PACKET`、现有 Assignment linkage、scheduler/result/manual ingress、Artifact/Evidence/Review projection。
18. **哪些绝对不能新增第二套？** Task、Workflow、Employee、Role、Router、Provider Task/Session、Result、Evidence、Artifact、Decision、Handoff、Context、Capability、Package、Company/Workspace identity。
19. **Package Method Metadata 是不是 V1 blocker？** 不是；记录为未来能力架构 gap。
20. **Phase 1 真正应该开发什么？** 只开发 Workspace-scoped Series/Trigger Claim/Cycle pin 的持久化和 single-active/restart/idempotency控制，不执行员工、不做 Learning、不创建 successor。

## 14. Active DB and Git safety evidence

Audit start:

- HEAD: `50d058ca865c1817721536d7beb47a1c5f1f354d`
- staged: `0`; preserved unstaged: `78`; preserved untracked: `368`
- no reset, clean, broad add, commit or push.

Active SQLite read-only baseline:

| Path | Size | mtime | SHA-256 | integrity_check | foreign-key truth |
|---|---:|---:|---|---|---|
| `data/curis.sqlite` | 1,232,896 | 1,786,873,339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` | no rows returned |
| `backend/data/curis.sqlite` | 1,277,952 | 1,786,783,659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` | 12 pre-existing orphan rows across legacy ResultStore tables, read-only observed; not modified or repaired |

The foreign-key observations are baseline facts, not Phase 0 changes. This audit did not initialize or migrate either database.

## 15. Stop state

```text
CURIS AUTONOMOUS OPERATING V1
— START GATE PASSED
— PHASE 0 RUNTIME TRUTH AUDIT COMPLETE
— EXISTING RUNTIME REUSE MAP COMPLETE
— MINIMAL CONTROL PLANE GAP IDENTIFIED
— NO IMPLEMENTATION
— READY FOR CEO REVIEW
— STOP
```
