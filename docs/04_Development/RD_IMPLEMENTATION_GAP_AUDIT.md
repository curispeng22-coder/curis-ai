# RD Implementation Gap Audit

**Status:** Review  
**Date:** 2026-08-16  
**Mode:** Read-only implementation audit. No production code, schema, Product Blueprint, Frozen design contract, XHS, TTK, activity database, staging, commit, or push was changed.  
**Scope:** Migration of the approved RD Workspace from the current legacy Runtime page into the second real Professional Workspace Instance.

## 1. Authority and evidence boundary

### Product and design authority

- `docs/00_Context/CURRENT_STATE.md`
- `docs/01_Product/Curis_Product_Blueprint.html`
- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` — Frozen, S1–S7 + P1–P7
- `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md` — RD INSTANCE APPROVED
- `docs/03_Design/Curis_XHS_Workspace_UI_Authority_Map.md` — Approved authority map; includes the RD authority rows
- `docs/03_Design/Curis_RD_Workspace_High_Fidelity_v1.html` — Reference Only / Approved Visual Reference
- `docs/03_Design/Curis_RD_Workspace_UI_Drift_Audit_v1.md` — Review Record / Reference Only
- `docs/03_Design/Curis_RD_Design_Phase_Closeout_2026-08-15.md` — RD design closeout
- `curis-ui-prototype/_system/tokens.css` — Frozen token source referenced by the Authority Map

The visual reference was inspected only to understand the approved information hierarchy. Its HTML, JavaScript, CSS, mock data, and interaction implementation are not implementation authority and must not be copied.

### Current implementation evidence

- Accepted XHS implementation and formal record:
  `issues/XHS-WORKSPACE-INSTANCE-001.md`,
  `reviews/XHS-WORKSPACE-INSTANCE-001_review.md`
- Accepted Computer Access P0 implementation and formal record:
  `issues/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001.md`,
  `reviews/AGENT-COMPUTER-ACCESS-RUNTIME-P0-001_review.md`
- Current shell and RD/XHS routes under `frontend/`
- Runtime Foundation, Workspace Runtime, Task/Artifact store, Agent Adapter, execution binding, legacy RD Runtime and focused tests under `backend/`
- Newest relevant entries in `docs/08_Change_Log/CHANGE_LOG.md`

Reference, test, route, or persisted-table existence is not treated as delivered RD product capability unless the actual user path is connected.

## 2. Executive finding

The approved RD Instance is **not implemented**. The current RD route mounts
`WorkspaceRuntimeView({ businessType: "RD" })` inside `TerraShell` and presents Cycle,
Simulation, capability, and acceptance controls as generic Runtime cards. It does not
provide the approved four-pane professional office, employee workstations,
provider-native conversation/composer, artifact review, or truthful task-bound current
executor.

This should be a **gradual route migration**, not a global Shell rewrite and not a new
RD system:

1. Reuse and parameterize the XHS-accepted `WorkspacePaneShell`; do not create a second
   pane shell or refactor global `TerraShell`.
2. Keep `CYCLE` as the first responsibility-bearing RD work object. Add only the RD
   work-context fields and links needed by the approved workstations.
3. Connect a Cycle to the existing Company Task → Employee Binding → Codex Adapter →
   ResultStore path. Do not require the CEO to type `workflow_run:<id>`.
4. Persist Task, Artifact, Evidence, access snapshot and Runtime links under the same
   Company/Workspace/Cycle scope.
5. Add an RD-domain Artifact Review Request in the existing Runtime graph. It must not
   become a Handoff or a second approval system.

No evidence currently requires a new database table, DAG, Workflow Engine, generic
permission engine, or separate RD Agent/Task/Gate/Result subsystem.

## 3. Current implementation map

| Area | Current fact | Reuse decision |
| --- | --- | --- |
| RD route | `frontend/app/ceo-office/workspace/software/page.js` mounts the generic `WorkspaceRuntimeView`. | Replace the route presentation after a bounded Issue; keep the route and Runtime client. |
| Shared pane shell | `frontend/components/workspace/WorkspacePaneShell.js` is accepted through XHS for four panes, pointer resize, T1/T2/T3, Utility maximize, compact overlays and per-Workspace preferences. Some labels are still XHS-specific. | Reuse after small prop-based generalization; preserve XHS defaults and tests. |
| Search | The shell opens a search dialog, but current source explicitly says the Runtime query is still being connected and returns no object results. | Partial. Add a read-only provider over real loaded Company/Workspace objects before claiming RD search. |
| RD UI | Generic Cycle creation, manual `execution_ref`, Simulation, start/execute/review/close controls. | Migration input only; not an approved RD workstation. |
| RD work object | `CYCLE` is persisted, Company/Workspace scoped, state-machine backed, restart-safe and has outcome/intent/stages. | Reuse as the first responsibility-bearing work object. Remove the fixed `完善 Curis` default and add an explicit project/work-object reference. |
| Staffing | Role Slot, AI Employee and Capability Binding are persisted and validated for an Operating Workspace. | Reuse validation and identity. Current Cycle start incorrectly treats the whole team as concurrently executing one responsibility. |
| Responsibility | Cycle has `owner_ref`; XHS has an accepted persisted `workContext` projection. | Extend Cycle with the same four independent dimensions, using real employee refs. Do not copy XHS content state. |
| Handoff | Cycle start/output and XHS content completion persist `HANDOFF` entities and transition logs. | Reuse entity, links and state machine. Replace team-wide startup handoffs with a single real responsibility transfer. |
| Decision | `DECISION_PACKET` exists; XHS proves the same packet can drive Banner, Conversation reference and Detail using P7. Legacy Cycle close also writes a simpler post-acceptance packet. | Reuse XHS shared P7 semantics; do not reuse the legacy close packet as a Needs CEO package without migration. |
| Evidence | Cycle writes `EVIDENCE`; ResultStore writes Task `artifacts`; both persist. | Link real Task/Artifact/Test facts to Cycle Evidence. A text summary alone is insufficient for RD review. |
| Task execution | ResultStore, Orchestrator and ToolExecutor support Company/Project/Employee/Capability-bound Tasks. | Reuse. There is no Workspace/Cycle command that creates and runs this Task. |
| Codex | `CodexCliAdapter` supports real new/resume sessions, JSONL progress, session ID, file-change refs and truthful Computer Access snapshots. | Reuse through the existing Agent Binding. Do not call Codex directly from an RD component. |
| Legacy Real RD | `RealRDExecutor` and `LocalRDToolset` can perform allow-listed file/test operations, but the executor contains fixed evidence-fixture paths and a separate issue/workflow orchestration model. | Keep as legacy capability/test substrate only. It is not the new RD Instance entry or truth model. |
| Persistence | Runtime entities/links/transitions, Task/Execution/Artifact/Usage and access snapshot facts persist in SQLite. | Reuse. Add explicit Cycle → Task → Artifact/Evidence refs; persistence does not itself prove current execution. |

## 4. Gap Matrix

Labels are current implementation facts:

- **EXISTS** — current code already satisfies the approved need.
- **REUSABLE_FROM_XHS** — accepted XHS shared implementation can be reused without its domain behavior.
- **PARTIAL** — a real primitive exists, but the approved RD user/runtime chain is incomplete.
- **MISSING** — no current implementation of the approved RD behavior.
- **BLOCKED** — the vertical slice cannot truthfully pass until the named integration exists.

| Approved RD requirement | Status | Current fact | Required migration |
| --- | --- | --- | --- |
| Four Pane Shell | **REUSABLE_FROM_XHS** | Accepted `WorkspacePaneShell` exists; RD still uses `TerraShell`. | Mount the shared shell at the RD route and pass RD-specific Context/Utility titles and content. |
| Resizable Adaptive Surface | **REUSABLE_FROM_XHS** | Pointer-driven continuous widths, min/max, compact overlay and persistence passed XHS acceptance. | Reuse unchanged behavior; add RD/XHS regression checks. |
| Pane-local Header / T1–T3 | **REUSABLE_FROM_XHS** | Shared shell has independent headers and the three toggle types. | Parameterize labels/icons only; do not copy shell code. |
| Company-wide Object Search | **PARTIAL** | Search dialog exists but currently returns an honest “query connecting” message. | Supply real read-only results from current Company, Workspace, Employee, Cycle/Project and Result refs. No sample results. |
| Utility Maximize | **REUSABLE_FROM_XHS** | Accepted modal maximize/restore behavior exists. | Reuse with RD Source/Diff/Preview content. |
| RD Project / Work Object | **PARTIAL** | Legacy `projects` and Runtime `CYCLE` both exist, but the RD route does not bind them into the approved work object. Cycle creation still injects `完善 Curis`. | Use a real Company Project reference plus Cycle ID; require CEO-supplied goal/title and never seed a fixed task. |
| Employee Workstations | **MISSING** | No RD stacked workstation component. | Build RD-specific workstation stack from persisted Cycles/responsibilities; no Calendar/Note reuse. |
| Object Owner | **PARTIAL** | Workspace/Cycle `owner_ref` exists. | Project stable owner and current work-object owner must be projected separately from holder/executor. |
| Responsibility Holder | **PARTIAL** | Staffing assignments and Cycle owner exist; no per-Cycle holder projection. | Persist a validated active employee ref in Cycle work context. Holder survives waiting/needs_ceo/failed where the contract allows it. |
| Current Executor | **PARTIAL** | Current Cycle start marks every assigned employee RUNNING; XHS has a correct single-subject projection. | Set one real employee only while the linked Task/session is active; set none after completion, failure, waiting, review or CEO decision. |
| `waiting` semantics | **PARTIAL** | Cycle has `PAUSED`/`WAITING_CEO`; employee presence can be BLOCKED/WAITING_CEO, but holder and executor are not independently projected. | Preserve holder, set executor none, state the dependency/owner/resume condition. Waiting must not become idle. |
| `failed` / `idle` | **PARTIAL** | Failure is durable and resumable; no approved workstation presentation or idle distinction. | Derive workstation status from Cycle + linked Task/session facts, not from employee existence. |
| Employee Presence | **REUSABLE_FROM_XHS** | Accepted data-driven component requires a real `AI_EMPLOYEE` ref. | Reuse with RD employee identity/role/current responsibility; never fall back to a label or Agent name. |
| System Activity | **PARTIAL** | Accepted XHS component and semantic boundary exist; RD emits no suitable build/test/index activity projection. | Project only non-employee system work. When an Agent/employee executes, use Current Executor instead. |
| Conversation | **MISSING** | Global Assistant and Task output exist, but no responsibility-scoped employee conversation. | Present the persisted instruction, progress summary, result/error and P7 reference for the linked Task/session. Do not expose raw CLI/stack by default. |
| Composer | **MISSING** | Generic Cycle form and manual execution ref field are not the approved composer. | Add responsibility-scoped instruction input with supported provider/session controls and truthful Computer Access intent. |
| Handoff | **PARTIAL** | Real Handoff entities exist, but Cycle start hands the same responsibility to the entire team and result-to-CEO is conflated with acceptance flow. | Create Handoff only when holder changes A → B; link origin, target, responsibility, result refs and acknowledgement. |
| Artifact Review Request | **MISSING** | No persisted review request distinct from Handoff/Acceptance. | Add a bounded RD-domain entity/command in `runtime_entities`; reviewer inspects and responds while original holder remains. |
| CEO Decision P7 | **PARTIAL** | XHS shared P7 is accepted. Legacy RD close packet is not a high-risk Needs CEO package and lacks the full provenance contract. | Reuse one `DECISION_PACKET` per issue, with Banner/Conversation/Detail references and automatic continuation. High risk Layer 0 only offers 查看方案/暂缓. |
| Result Reference | **PARTIAL** | XHS shared view, Cycle Evidence and Task Artifact exist separately. | Persist and project one reference chain from Cycle → Task/Execution → Artifact/Test Evidence. |
| Evidence / Utility | **PARTIAL** | Runtime Evidence can contain a summary; Task Artifact contains output. No Source/Diff/Test evidence contract reaches RD Utility. | Build Utility from real file-change refs, content hashes, diff/test output or honest unavailable states. |
| Agent Execution | **BLOCKED** | Codex and Task execution are real, but Operating Cycle only accepts a pre-existing `workflow_run:<id>`. | Add the narrow Cycle → existing Task/Orchestrator bridge. No manual workflow ID and no fake successful executor. |
| Computer Access | **EXISTS** | P0 truth snapshots are accepted. New session maps requested intent to native sandbox; effective remains `UNKNOWN`. Resume is `NOT_CONFIGURABLE/UNVERIFIED/UNKNOWN`; Full is `UNSUPPORTED`. | Read and persist the snapshot unchanged. Verify actual file/test postconditions separately; never relabel configured as granted/effective. |
| Persistence | **PARTIAL** | Each subsystem persists, but Cycle, Task, Artifact, access snapshot and review request are not one scoped chain. | Add references/links and prove restart reads without converting stored access history into fresh verification. |

## 5. Reuse, migrate, and reject

### Reuse directly

- `WorkspacePaneShell` pane behavior, preference isolation, resize, compact overlays,
  Utility maximize and focus/escape behavior.
- XHS-accepted shared UI components for Employee Presence, System Activity, Handoff,
  Result Reference and P7 Decision, provided they remain domain-neutral.
- Runtime Foundation scope checks, entities, links and transition log.
- `CYCLE`, `AI_EMPLOYEE`, `ROLE_SLOT`, `CAPABILITY_BINDING`, `HANDOFF`,
  `DECISION_PACKET`, `EVIDENCE`, `ACCEPTANCE` and Workspace Operating Version checks.
- ResultStore Task/Execution/Artifact/Usage; Orchestrator; Agent Binding; Codex Adapter;
  Computer Access P0 snapshots.

### Migrate or extend

- `WorkspacePaneShell`: replace embedded XHS labels with props while preserving current
  defaults and accepted XHS behavior.
- `CYCLE`: add explicit `projectRef`, CEO-supplied work title and a subject-scoped work
  context. The Cycle ID is the first slice's stable Responsibility ID.
- Cycle start: select one legal responsibility holder/executor, not every employee.
- Cycle execute: create/run a real Task through existing binding and persist the child
  refs/result facts.
- Runtime projection: join Cycle, Task, Artifact/Evidence, access snapshot, review,
  Handoff and Decision without introducing a second store.
- Artifact Review Request: add only the minimal RD-domain entity/state transitions to
  the existing Runtime graph.

### Do not use as the new RD product path

- Generic `WorkspaceRuntimeView` as the RD office.
- CEO-entered `workflow_run:<id>`.
- `RealRDExecutor` fixed evidence fixture as a general customer task.
- `完善 Curis` or any other hard-coded default RD task.
- XHS Calendar, Note fields, ContentItem lifecycle, publishing or analytics code.
- Prototype HTML/JS/CSS or mock employee/project/result data.

## 6. Runtime truth and Computer Access boundary

The first slice must preserve:

```text
Business Object State
!= Responsibility Holder
!= Current Executor
!= System Activity State
!= Computer Access Effective State
```

### New Codex session

- `ASK_WHEN_NEEDED` maps to Codex `read-only`; configured can be recorded, effective
  remains `UNKNOWN` unless the provider returns new evidence.
- `AUTO_WITHIN_BOUNDARY` maps to `workspace-write`; configured can be recorded,
  effective remains `UNKNOWN`.
- A real file hash/diff/test result proves that operation's outcome. It does not prove
  a general effective permission state.

### Resume

- Do not pass the old sandbox as though it were newly configured.
- Do not inherit effective/granted state.
- Preserve `NOT_CONFIGURABLE / UNVERIFIED / UNKNOWN` where the provider cannot inspect
  or re-declare it.
- A mutable recovery that requires stronger assurance may start a new bounded session;
  it must not silently upgrade the resumed session.

### Full Computer Access

- Remains `UNSUPPORTED` and fail-closed before Codex process launch.
- RD need does not authorize P1/P2, dangerous flags, fallback to Auto, or UI claims of
  full access.

## 7. P0 blockers for the first real RD vertical slice

1. **Remove fixed work-item creation semantics.** New RD work must be CEO/project
   supplied; current `完善 Curis` default conflicts with the approved product rule.
2. **Cycle → Task/Codex bridge.** Without it, RD can only consume a manually prepared
   legacy workflow and cannot truthfully execute from the professional Workspace.
3. **Task-bound responsibility projection.** Current team-wide RUNNING state cannot
   represent holder/executor/waiting truth.
4. **Artifact/Evidence reference chain.** A result summary without file/test/source
   references is not sufficient RD evidence.
5. **Real search projection.** Current search surface is present but not functional.

Artifact Review Request, multi-employee Handoff and P7 are required for the approved
Instance acceptance, but they do not block building and validating the first
single-responsibility Codex slice.

## 8. Runtime architecture review decision

No separate `RD_RUNTIME_ARCHITECTURE_REVIEW.md` is created in this planning round.
The observed gaps fit the existing architecture:

- `CYCLE` is the first stable RD responsibility-bearing object;
- Task/Execution/Artifact stay execution substrate;
- Runtime links carry the cross-reference;
- XHS-proven shared semantics remain shared;
- Artifact Review Request is a bounded RD-domain addition in the existing Runtime
  entity store, not a new shared workflow system.

A separate architecture review becomes necessary only if implementation proves that
Company/Workspace/Cycle scope cannot be enforced atomically through the existing
Task and Runtime stores. Current code evidence does not establish that blocker.

## 9. Audit conclusion

The smallest safe migration is:

```text
RD route
→ shared WorkspacePaneShell
→ real Company Project + Cycle responsibility
→ real AI Employee / Binding
→ existing Task / Codex Adapter
→ truthful Computer Access snapshot
→ real Artifact / Test Evidence
→ Result Reference
→ Artifact Review Request or true Handoff
→ one P7 Decision when required
→ restart-safe projection
```

This is an implementation-planning result only. It does not authorize production code
and does not change the current RD delivery status.

**RD IMPLEMENTATION GAP AUDIT COMPLETE · PLAN REVIEW REQUIRED**
