# SHARED-BUSINESS-WORKSPACE-READ-MODEL-001

**Status:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-17
**Owner:** Curis Shared Runtime

## Goal

Expose one tenant/company/workspace-scoped read model over existing Company OS records so
RD, XHS and dynamically installed Workspaces can consume the same truthful projections for:

- Company → Business → Workspace → Team relationships;
- Employee identity, Role Slot, current responsibility and current executor;
- Employee UI status and System Activity without inventing execution;
- Capability-backed Composer availability without provider hardcoding;
- Result / Artifact / Evidence references for Utility reads.

This Issue adds no business command, lifecycle state, schema or second Company OS model.

## Authority and baseline

- `docs/00_Context/CURRENT_STATE.md`
- `docs/03_Design/Curis_Company_OS_Shared_Authority.md` (Frozen)
- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` (Frozen P1–P7)
- accepted Workspace Package Company integration P0.5
- Git baseline: `fe55ff5d5a1fbf5be1d08b6401904230b2bd3c1c`

Pre-change mixed-source SHA-256:

| File | SHA-256 | Owned hunk |
| --- | --- | --- |
| `backend/app/api/runtime_foundation_router.py` | `732eb4fffe484e73e2c2383389cfbf88dffde6260f512ce051dafe15084a1f53` | import, service construction, bounded GET routes only |

## Allowed Files

```text
backend/app/shared_workspace_projection.py
backend/app/api/shared_workspace_router.py
backend/app/api/runtime_foundation_router.py
backend/tests/test_shared_workspace_projection.py
issues/SHARED-BUSINESS-WORKSPACE-READ-MODEL-001.md
reviews/SHARED-BUSINESS-WORKSPACE-READ-MODEL-001_review.md
```

## Explicit exclusions

- schema, migration, seed or production DB resolution changes;
- writes to Company, Workspace, Employee, Responsibility, Task, Result or Capability records;
- new lifecycle states, Workflow/DAG, Organization Router or second identity model;
- provider-specific Composer behavior or provider-native conversation recreation;
- changes to RD/XHS/TTK or Package domain behavior/UI;
- Frozen authority, Product Blueprint, active SQLite or unrelated dirty baseline;
- broad staging, push or cleanup.

## Runtime truth rules

1. Object Owner, Responsibility Holder, Current Executor and System Activity remain distinct.
2. `Current Executor = none` never projects an Employee as running.
3. Employee UI status is a read projection only: working, blocked or idle.
4. Capability/Composer availability derives only from persisted Role Slot and Capability Binding facts.
5. Configured access is not effective access; unverifiable effective access remains `UNKNOWN`.
6. Results resolve only from existing Artifact, Evidence or Outcome records in the current scope.
7. Missing Business/Department links remain `UNKNOWN`; the reader does not infer relationships by name.

## Acceptance

1. One shared Workspace projection returns Company, resolvable Business, Workspace and operating Team.
2. Employee list/detail returns real Runtime Employee and Role Slot references.
3. Responsibility Holder and Current Executor derive from persisted work context and stay distinct.
4. Employee with responsibility but no executor is not shown as running.
5. System Activity remains separate from Employee execution.
6. Composer projection exposes only exact persisted capability supply and truthful access state.
7. Result reference API reads existing Artifact/Evidence/Outcome and rejects wrong-company/workspace refs.
8. Runtime restart returns the same projection from isolated SQLite.
9. Focused tests plus bounded RD/XHS/Package no-regression pass; active DB fingerprint is unchanged.

## Commit boundary

Only Allowed Files may be staged. One bounded local commit is allowed. No push.

## Implementation result

- Added one read-only `SharedWorkspaceProjection`; no schema or write path changed.
- Added scoped Runtime Foundation GET endpoints for Workspace, Employee Detail and Result Reference
  in a bounded tracked child router.
- Unified existing Runtime Employee, Role Slot, Capability Binding, work context, System Activity,
  Artifact, Evidence and Outcome facts without adding a new primitive.
- Missing Business/Department relations remain unresolved/empty; no name-based inference is used.
- The mixed-source Runtime router changed only in one import and one `include_router` hunk.
