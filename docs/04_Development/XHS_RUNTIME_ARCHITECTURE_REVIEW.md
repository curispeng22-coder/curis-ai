# XHS P0 Runtime Architecture Review

**Status:** Review  
**Date:** 2026-08-15  
**Mode:** Read-only Runtime architecture review. No production code, schema, API, database, Blueprint, Frozen design contract, or activity data was changed.  
**Authority read:** `docs/00_Context/CURRENT_STATE.md`; Frozen `docs/02_Architecture/Curis_System_Architecture.md`; Frozen ADR-0045; Frozen `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`; Approved `docs/03_Design/Curis_XHS_Workspace_Instance_Spec_v1.md`; Approved `docs/03_Design/Curis_XHS_Workspace_UI_Authority_Map.md`; newest relevant `docs/08_Change_Log/CHANGE_LOG.md`; current Runtime source and focused Runtime tests.

## 1. Review decision

The current Runtime already has the correct **Company → Workspace → business object
→ execution/evidence → human decision → result** persistence base.  XHS must compose
that base; it must not create its own Task, Agent, Gate, Artifact, or workflow system.

`CONTENT_ITEM` is an **XHS domain object** (a Note), not a new cross-Workspace Task.
Existing Task / Agent Adapter execution remains the execution substrate.  A Note links
to that substrate through its existing `execution_ref`, version references, evidence
and Runtime links.  It keeps XHS-specific scheduling, content and publishing facts.

The ContentItem lifecycle remains exactly:

```text
IDEA → DRAFT → IN_REVIEW → APPROVED → SCHEDULED → PUBLISHED
→ AWAITING_FEEDBACK → REVIEWED
```

Publish execution state (`working | completed | failed | waiting`) belongs to the
linked execution/result fact. Analytics system activity state (`waiting | running |
ready | failed`) belongs to a System Activity projection. Neither adds a ContentItem
state. Business Object State, Current Responsibility, Current Executor and System
Activity State remain four separate dimensions.

The P0 gap is deliberately small: current generic entities exist, but the concrete
helpers and public commands are hard-wired to the RD `CYCLE` path.  Add only a
subject-scoped responsibility/hand-off/decision/result composition layer in the
existing `WorkspaceRuntime`; do not build a DAG, a workflow engine, or a global XHS
lifecycle.

## 2. Four-way classification

### A. Company OS Shared Runtime

| Shared concern | Current basis | P0 rule |
| --- | --- | --- |
| Company/Workspace identity and isolation | `RuntimeFoundation`, `runtime_entities`, `runtime_links`, scoped Foundation router | Every new command validates current tenant, Company, Workspace and subject before it writes. |
| Object Owner | `runtime_entities.owner_ref` | Stable business ownership stays on the domain object. It is not overwritten by the last actor. |
| Current Responsibility | Role Slot / AI Employee entities and links | Project a referenced Role Slot / Employee separately from the owner. |
| Current Executor | existing `execution_ref`, Task execution controls, Agent Adapter | Show an employee only when an employee reference exists; System Activity is a non-employee executor. |
| Employee execution | existing Task, Agent Adapter, `TaskExecutionControlService`, `AI_EMPLOYEE` state machine | A task/run is an execution child of a Note, never a replacement Note lifecycle. |
| Handoff Event | persisted `HANDOFF`, state machine and transition log | One general subject-scoped command must create/link/transition it; source and target stay explicit. |
| Decision Gate | persisted `DECISION_PACKET`, `ACCEPTANCE`, decision state machine | Use `DECISION_PACKET` for a durable CEO decision on a business object; a user-facing `Needs CEO` surface derives from its `WAITING_CEO` state. |
| Evidence / Artifact / Result reference | `EVIDENCE`, legacy Task `artifacts`, `PUBLICATION_RECEIPT`, `INTERACTION_ITEM`, `OUTCOME` entity family | Keep technical execution output as an Artifact/Evidence reference; keep the business result domain-specific. Do not create a duplicate generic Result table. |
| Runtime/System Activity | execution events, transition log, receipts/interactions and simulation history | Project immutable Activity from persisted facts. Analytics never impersonates an employee. |
| Lifecycle audit | `runtime_transition_log`, state machines and links | All responsibility, decision and result changes append legal transitions/links; clients do not mutate stages locally. |

### B. XHS Domain Runtime

| XHS-only concern | Boundary |
| --- | --- |
| `CONTENT_ITEM` / Note | XHS business object; carries calendar date, title/body/tags/cover and the XHS work-stage summary. It is not a generic task. |
| Note versions | `CONTENT_VERSION`; immutable candidates and approved/published version references remain attached to the Note. |
| XHS fields | Platform variant, title/body/tags/cover, scheduled time, account/signal/brand references and XHS content format belong only to the Note/version payload. |
| XHS lifecycle meaning | `IDEA → DRAFT → IN_REVIEW → APPROVED → SCHEDULED → PUBLISHED → AWAITING_FEEDBACK → REVIEWED`; no XHS state is added to a global Company enum. |
| XHS review rules | Content quality, brand, copyright, facts and platform constraints are Note review evidence/rules, not a universal Gate policy. |
| Publishing adapter | XHS Connector capability and its receipt adapter. No connector, no claimed platform publication. |
| XHS analytics | XHS receipt/interaction/metric facts and their domain projection. Manual data remains manual and unverified. |

### C. Existing Runtime Reusable

| Existing capability | Evidence / reuse decision | Limit to preserve |
| --- | --- | --- |
| Scoped entity graph | `RuntimeFoundation.create/get/list/link`, `runtime_entities`, `runtime_links` | Reuse; no XHS table in P0. |
| Domain objects and versions | `CONTENT_ITEM`, `CONTENT_VERSION`, version reference columns | Reuse, but repair the legal `IDEA` → `DRAFT` writer path before editing versions. |
| Employees and roles | `AI_EMPLOYEE`, `ROLE_SLOT`, `CAPABILITY_BINDING`, employee state machine | Reuse real IDs only; no display-only employee. |
| Execution substrate | existing Task records, `TaskExecutionControlService`, Agent Adapter and existing execution references | Reuse as child execution. Current `RuntimeExecutionAdapter` only supports selected simulation refs, so it is not itself the XHS production coordinator. |
| Handoff lifecycle | `HANDOFF`: `CREATED → SENT → ACKNOWLEDGED → COMPLETED/RETURNED/REJECTED` | Reuse entity/state machine; current `WorkspaceRuntime` helper is Cycle-specific and must be generalized narrowly. |
| CEO decision lifecycle | `DECISION_PACKET`: `DRAFT → READY → WAITING_CEO → DECIDED → APPLIED` | Reuse entity/state machine; current creator is Cycle-specific. Do not use legacy pending-gate storage as the XHS source of truth. |
| Acceptance and evidence | `ACCEPTANCE`, `EVIDENCE`, transition history | Reuse where the CEO is accepting a result; use a Decision Packet for pre-publish choice. They are not interchangeable. |
| Publication / interaction facts | `record_publication_receipt()` and `record_interaction()` | Reuse. `CEO_MANUAL` remains `UNVERIFIED`; Platform API requires external ID. |
| Artifact and execution result | `ResultStore` persists Task Artifacts/results and execution trace; `EVIDENCE` is already Workspace-scoped | Reuse Artifact by link/reference when a Task actually produced it. The existing legacy `ContentWorkflowRuntime` has its own tables/mock-oriented path and is not the new XHS office coordinator. |

### D. Missing Shared Primitive

| Minimal primitive | Why it is shared | P0 minimum | Explicit non-goal |
| --- | --- | --- | --- |
| **Work context projection** | Every Workspace object can distinguish owner, responsibility, executor and system activity. | A validated data contract on the existing subject: `objectOwnerRef`, `currentResponsibilityRef`, `currentExecutorRef`, `executorKind`, `activityStatus`, `returnStage`, `retryBoundary`. Foundation columns and existing `data_json` suffice for P0. | No new generic WorkItem table or global business states. |
| **Subject-scoped Handoff command** | Handoff already has a shared entity but only RD Cycle code creates it. | Create a `HANDOFF`, link it to any scoped subject, record legal `HANDOFF` transitions, and update the subject Work Context atomically. | No orchestration graph, fan-out planner or client-authored transition. |
| **Subject-scoped Decision Gate command** | `DECISION_PACKET` is shared, but its current write path is RD closeout only. | Create/link a packet to a subject, move it to `WAITING_CEO`, store allowed choices, evidence refs, return action and then apply a CEO decision through legal transitions. | No second Approval service, no generic visual-only modal state. |
| **Result reference projection** | A user must revisit a business result regardless of whether it came from an Artifact, receipt, interaction or manual fact. | Read links/references from the existing subject to `EVIDENCE`, Artifact reference, receipt, interaction and optional `OUTCOME`; return source, verification, timestamp and route. | No duplicate `Result` entity/table or fabricated analytics aggregate. |

## 3. Required composition for the first XHS slice

```text
CONTENT_ITEM (XHS Note, owner remains stable)
  → linked Task / existing Agent execution reference
  → Artifact or EVIDENCE only after an actual execution result
  → shared subject-scoped HANDOFF (creator → reviewer)
  → CONTENT_ITEM remains IN_REVIEW; linked DECISION_PACKET is WAITING_CEO
  → CEO decision is persisted and applied
  → approved Note uses existing receipt command or a truthful waiting state
  → PUBLICATION_RECEIPT / INTERACTION_ITEM / optional OUTCOME
  → shared System Activity + Result Reference projection
```

`Needs CEO` is therefore a **derived presentation state**, not a new global or
XHS lifecycle state: the Note is in legal `IN_REVIEW` and a linked decision packet is
`WAITING_CEO`. This preserves the current ContentItem state machine and makes the
same Decision mechanism available to RD and TTK without making their domain states
identical.

After a Note reaches `APPROVED`, its publish execution can be `working`, `waiting`,
`failed` or `completed` without changing the Note's domain state until a legal
publication receipt supports `PUBLISHED`. After that, Analytics is System Activity
(`waiting`, `running`, `ready` or `failed`), not an employee or ContentItem lifecycle.

## 4. Direct answers

### 1. Which existing objects can carry the model?

`WorkspaceTask` / existing Task and Agent Adapter carry execution and retry control;
`AI_EMPLOYEE` / `ROLE_SLOT` carry human-readable responsibility; `CONTENT_ITEM` and
`CONTENT_VERSION` carry XHS business content; `HANDOFF`, `DECISION_PACKET`,
`ACCEPTANCE`, `EVIDENCE`, receipt and interaction entities carry the durable business
record. `ResultStore` Artifacts can be referenced when an actual Task created them.
None alone replaces the whole Note-to-publication chain.

### 2. What should extend instead of parallel creation?

Extend `WorkspaceRuntime` and its existing router projection with the four small
shared primitives above. Extend the `CONTENT_ITEM` command path to expose legal
version/review transitions. Reuse Foundation entity/link/state-machine operations.
Do not add `XhsTask`, `XhsAgent`, `XhsApproval`, `XhsResult`, or a second execution
store.

### 3. How should a Decision Gate reuse existing approval capability?

For a pre-publish business choice, create a linked `DECISION_PACKET`; execute its
existing `prepare → request_decision → decide → apply` transitions. For CEO acceptance
of completed evidence, use existing `ACCEPTANCE`. `PendingDecisionStore` / GatePrompt
can remain an implementation-level safe prompt renderer where applicable, but it is
not a replacement for the scoped, revisit-able `DECISION_PACKET`; its current content
workflow call path has no resume coordinator and therefore correctly fails closed.

### 4. How does Handoff enter the Employee / Task chain?

An execution-completion handler validates the actual Task result/Artifact or Evidence,
then calls the subject-scoped Handoff command in the same Workspace. That command
links the Note, the execution result and the target reviewer; it sets the Note Work
Context to the reviewer and records `HANDOFF` transitions. A browser click may request
or display recovery, but cannot impersonate a completed execution.

### 5. How does Result reuse existing Artifact / Result models?

Creation output stays in the existing Task Artifact/trace store and is referenced from
the Note/Evidence only after it exists. Publication is represented by the existing
receipt model; engagement by interactions and, when a business summary is actually
recorded, the existing `OUTCOME` entity. A single read-only Result Reference projection
collects those facts for the UI. It does not copy their payloads into a new result
system.

### 6. Is ContentItem a domain object rather than a generic Task?

**Yes.** A Note owns XHS content identity, versions, schedule, approval/publish facts
and analytics references. Task/run objects are transient execution children. This
keeps Calendar and publishing lifecycle out of Company OS global states and prevents
RD/TTK from inheriting XHS semantics.

### 7. How does XHS remain on Company OS Runtime?

All objects retain current Company/Workspace scope, existing employee IDs, Foundation
transitions, Runtime links and transition history. XHS only supplies the Note-specific
data and legal content state transitions. Handoff, decision, evidence, execution and
result references use Company OS primitives instead of private tables or UI state.

### 8. What is the smallest P0 addition?

Only: (1) the legal ContentItem create/edit/review bridge; (2) shared Work Context
projection; (3) one generic subject-scoped Handoff helper; (4) one generic
subject-scoped Decision Packet helper; and (5) a Result Reference read projection.
The existing table/graph/state machines are sufficient. Add a schema only if a focused
implementation proves the existing subject payload/link model cannot preserve a
required foreign reference transactionally.

## 5. P0 implementation blockers and acceptance proof

1. **Content write legality:** resolve the existing mismatch where creation leaves the
   item in `IDEA` while the version writer permits only `DRAFT`; no client workaround.
2. **Generalize, do not copy:** extract Cycle-specific Handoff/Decision creation into
   a subject-scoped helper without changing RD's Cycle states or endpoints.
3. **Real execution completion:** automatic handoff needs a real Task/Agent completion
   or an explicit manual input fact. A simulated click cannot create it.
4. **CEO decision transaction:** the decision command must update packet, subject work
   context and links under the same Company/Workspace scope, with a repeat-safe result.
5. **Result truth:** no receipt means not published; manual receipt stays unverified;
   no metric source means analytics is waiting.

P0 is accepted only after an isolated SQLite scenario survives restart and proves the
same Note → execution fact → Handoff → Decision Packet → receipt/result chain through
the scoped projection. No standalone component, mocked flow, legacy content workflow
run or browser-only transition is evidence of this Runtime contract.

## 6. Explicitly rejected P0 designs

- A DAG/Workflow Engine or universal process canvas.
- Global Company OS `PUBLISHING`, `ANALYTICS` or XHS review states, and ContentItem
  states such as `PUBLISHING`, `ANALYTICS_PENDING` or `ANALYTICS_READY`.
- New `XhsTask`, `XhsAgent`, `XhsGate`, `XhsResult` tables or stores.
- Reusing RD `CYCLE` as a Note lifecycle.
- Treating the legacy `ContentWorkflowRuntime` mock/default path as approved XHS
  production execution.
- Client-only automatic handoff, approval, publication or analytics.

**XHS RUNTIME ARCHITECTURE REVIEW REQUIRED**
