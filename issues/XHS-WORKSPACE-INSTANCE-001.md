# XHS-WORKSPACE-INSTANCE-001：小红书 Workspace 首个可运行纵向切片

**Status:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-15
**Owner:** Curis 主开发 / XHS Workspace
**Input:** `XHS_IMPLEMENTATION_GAP_AUDIT.md`; `XHS_RUNTIME_ARCHITECTURE_REVIEW.md`; `XHS_IMPLEMENTATION_PLAN_v1.md`

## 1. Goal

Implement the first truthful XHS Workspace vertical slice:

```text
Enter XHS Workspace → Calendar → select persisted Note → Split Working
→ real Employee Presence / Context / Utility → actual execution completion
→ automatic Handoff → Needs CEO → CEO Decision → legal continuation
→ publication receipt/result → System Activity / Analytics
```

The result must be a Workspace-local XHS office backed by existing Company OS Runtime
objects. It must not be a generic task page, a static visual reference, or a private
XHS workflow system.

## 2. Authority files

1. `docs/00_Context/CURRENT_STATE.md` — Frozen current fact.
2. `docs/07_Decisions/ADR-0045-ordinary-user-desktop-product-rebaseline.md` — Frozen.
3. `docs/02_Architecture/Curis_System_Architecture.md` — Frozen.
4. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` — Frozen.
5. `docs/03_Design/Curis_XHS_Workspace_Instance_Spec_v1.md` — Approved.
6. `docs/03_Design/Curis_XHS_Workspace_UI_Authority_Map.md` — Approved.
7. `curis-ui-prototype/_system/tokens.css` — Frozen token source.
8. `docs/04_Development/XHS_IMPLEMENTATION_GAP_AUDIT.md` — Review.
9. `docs/04_Development/XHS_RUNTIME_ARCHITECTURE_REVIEW.md` — Review.
10. `docs/04_Development/XHS_IMPLEMENTATION_PLAN_v1.md` — Review.

If a lower item conflicts with a Frozen source, the Frozen source wins and the issue
must be paused for correction rather than improvising a design change.

## 3. Runtime contract

`CONTENT_ITEM` is the XHS Note and retains only this legal domain lifecycle:

```text
IDEA → DRAFT → IN_REVIEW → APPROVED → SCHEDULED → PUBLISHED
→ AWAITING_FEEDBACK → REVIEWED
```

The following dimensions are independent and may not be collapsed in UI or storage:

```text
Business Object State ≠ Current Responsibility ≠ Current Executor ≠ System Activity State
```

- Publish Execution is `working | completed | failed | waiting`, attached to an
  execution/result fact, not to the Note lifecycle.
- Analytics System Activity is `waiting | running | ready | failed`, not an employee
  and not a ContentItem lifecycle state.
- `Needs CEO` derives from a scoped `DECISION_PACKET=WAITING_CEO` linked to a Note that
  remains in legal `IN_REVIEW`.
- Task / Agent execution remains a child execution substrate. `CONTENT_ITEM` does not
  become a general Task.

## 4. Allowed files

### May modify

```text
frontend/app/ceo-office/workspace/xhs/page.js
frontend/components/workspace/**
frontend/components/xhs/**
frontend/lib/runtimeApi.js
frontend/tests/xhs_*.test.mjs
frontend/tests/runtimeWorkspaceUi.test.mjs
backend/app/runtime/workspace.py
backend/app/api/runtime_foundation_router.py
backend/tests/test_xhs_*.py
backend/tests/test_runtime_workspace_foundation.py (XHS lifecycle fixture migration and focused no-regression only)
issues/XHS-WORKSPACE-INSTANCE-001.md
reviews/XHS-WORKSPACE-INSTANCE-001_review.md
docs/04_Development/XHS_IMPLEMENTATION_GAP_AUDIT.md
docs/04_Development/XHS_RUNTIME_ARCHITECTURE_REVIEW.md
docs/04_Development/XHS_IMPLEMENTATION_PLAN_v1.md
```

### May add only when directly required by an above phase

```text
frontend/components/workspace/WorkspacePaneShell.*
frontend/components/xhs/Xhs*.{js,mjs,css}
frontend/tests/xhs_*.test.mjs
backend/tests/test_xhs_*.py
```

## 5. Explicit exclusions

- `frontend/components/terra/TerraShell.js`, `TerraSidebar.js` and global navigation.
- RD and TTK routes, their office components, their Runtime controls and tests.
- `frontend/components/runtime/WorkspaceRuntimeView.js` shared legacy presentation.
- Product Blueprint, Frozen/Approved design contracts, tokens, desktop packaging and
  activity databases. The accepted closeout may synchronise `CURRENT_STATE.md`,
  `CHANGE_LOG.md` and `PRODUCT_DOCUMENT_POINTER.md` only; it may not alter their
  product or Frozen-design content.
- `data/curis.sqlite`, `backend/data/**`, secrets, keys, cookies and external platform
  accounts.
- `ContentWorkflowRuntime`, legacy content mock paths, a DAG / Workflow Engine, or
  XHS-private Task/Agent/Gate/Result systems.
- Copying Visual v4, Shell Exploration or any prototype HTML, JS or CSS.

## 6. Phase 0–6 execution plan

| Phase | Scope | Completion condition |
| --- | --- | --- |
| 0 — Migration Safety | Establish fresh isolated SQLite test path, baseline focused XHS/RD/TTK checks, preserve pre-existing dirty worktree changes. | No active DB write; scope/revision baseline recorded; no prohibited file touched. |
| 1 — Shell | Route-scoped XHS `WorkspacePaneShell`, four pane behavior, local headers, T1/T2/T3, adaptive resize, scoped object search surface and Utility maximize. | XHS route alone meets Frozen pane interaction contract; RD/TTK remain on their current shell. |
| 2 — Calendar / Note | Persisted Note calendar, multi-Note month rules, selection URL, split editing and immutable version bridge. | Calendar and Note survive reload/restart; no client-only note state. |
| 3 — Shared semantics | Work Context projection, Employee Presence, System Activity, Result Reference. | Owner/responsibility/executor/activity are separately represented from persisted scope facts. |
| 4 — Decision / Handoff | Subject-scoped Handoff and the single shared `DECISION_PACKET`, legal content transition bridge and recovery projection. | Actual execution completion creates Handoff; `IN_REVIEW + WAITING_CEO` derives Needs CEO; the P7 Layer 0 / employee conversation / Layer 1 surfaces all reference that one durable packet, and no client authors a transition. |
| 5 — Published / Analytics | Existing receipt/interaction facts and truthful analytics activity projection. | Connector result is verified only with external ID; manual receipt remains unverified; absent data stays waiting. |
| 6 — Acceptance | Full isolated Runtime Simulation, Browser/Desktop evidence, restart/recovery and no-regression checks. | Review records the same Runtime objects, evidence and tested database. |

## 7. Runtime Simulation

The first full simulation must use a fresh isolated SQLite database and prove:

1. Create an XHS Workspace and a persisted Note without creating a fixed sample task.
2. Enter Calendar and select the same Note into Split Working after reload/restart.
3. Bind only actual existing Employee/Role references; empty/gap states remain honest.
4. Trigger an actual child execution completion or an explicit manual input fact.
5. Verify the same Note receives a persisted `HANDOFF` and then a linked
   `DECISION_PACKET=WAITING_CEO`.
   The packet contains the Frozen P7 CEO-readable package semantics and provenance;
   it is the only object referenced by the banner, employee conversation and detail.
6. Approve, return and defer on separate runs; verify decision transitions and recovery
   retain Company/Workspace/Note identity.
7. Record either a truthful manual receipt (`UNVERIFIED`) or verified connector receipt;
   otherwise remain waiting, never published.
8. Show Analytics only as System Activity and only from provenance-backed facts.

## 8. Acceptance scenarios

1. Empty XHS office: no fabricated Note, employee, signal, receipt or metric.
2. Calendar density: 0/1/2–3/4+ Notes use Approved XHS priority rules.
3. Scope: cross-tenant, cross-company and cross-workspace Note access fails closed.
4. Responsibility: Owner, current responsible employee, executor and System Activity
   remain separately visible.
5. Handoff: is persisted automatically only after an actual execution completion.
6. Decision: Needs CEO is a decision packet surface, not CEO as a next-step button.
7. Result: trusted receipt, manual receipt and absent receipt are visibly distinct.
8. Recovery: failed execution preserves the same Note, return stage, reason and bounded
   retry; it does not fabricate a replacement Note/result.
9. Restart: selected Workspace/Note and all linked facts reload from the isolated DB.
10. UI: 1440 and 1024 desktop, system/light/dark themes, keyboard focus and zero fake
    native titlebar controls.

## 9. No-regression requirement

- Run focused existing RD and TTK route/API checks after each phase that touches shared
  Runtime projection.
- No Phase may change RD/TTK source files or claim their new shell implementation.
- Existing failures must be recorded as pre-existing; this Issue may not increase them.

## 10. Review and closeout

Create `reviews/XHS-WORKSPACE-INSTANCE-001_review.md` during Phase 6. It must record
actual changed files, focused tests, isolated DB path and integrity check, Browser and
Desktop evidence paths, Runtime object IDs in redacted form, failure/recovery proof,
no-regression result and remaining external Connector limits.

No Phase is product completion by itself. Do not mark the Issue complete before the
full Runtime Simulation and its independent Review accept the same vertical slice.

## 11. Accepted closeout

**Closure status:** IMPLEMENTED / ACCEPTED
**Formal acceptance record:** `reviews/XHS-WORKSPACE-INSTANCE-001_review.md`

The accepted instance includes the XHS Pane Shell, Calendar / Multi-Note, Note Split
Working and version persistence, Employee Presence, responsibility / executor truth,
Handoff, P7 Decision Package and automatic continuation, Scheduling, System Activity,
Context / Utility, resize, Utility Maximize, Search, packaged Desktop and isolated
SQLite persistence.

Capability boundary remains explicit: Publishing is `NOT_CONNECTED / waiting`; Analytics
is `UNAVAILABLE / no data`. Neither is simulated by this Issue.

**XHS WORKSPACE INSTANCE V1 IMPLEMENTATION CLOSED
**READY FOR NEXT DEVELOPMENT PRIORITY**
