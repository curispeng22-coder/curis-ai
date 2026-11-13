# SHARED-BUSINESS-WORKSPACE-READ-MODEL-001 Review

**Status:** IMPLEMENTED / ACCEPTED
**Record Type:** Formal Acceptance Record
**Date:** 2026-08-17
**Issue:** `issues/SHARED-BUSINESS-WORKSPACE-READ-MODEL-001.md`

## Decision

The first Shared Business Workspace Foundation slice is accepted as a read-only Core projection.
It reuses current Company OS records and introduces no schema, lifecycle state, workflow engine,
provider hardcoding or second identity model.

## Implemented

- Company / resolvable Business / Workspace / Project / Department projection;
- Workspace operating Team from real Role Slot and AI Employee entities;
- Employee list/detail with distinct responsibility holder and current executor;
- truthful `working` / `blocked` / `idle` UI status projection;
- independent System Activity projection;
- capability-backed Composer projection with model/agent flags derived from persisted supply;
- Computer Access truth preserved (`configured` never becomes `effective`);
- Utility result reads for scoped Artifact, Evidence and Outcome references;
- same-Company cross-Workspace and cross-Company reference rejection;
- restart recovery from the same isolated SQLite.

## API

```text
GET /api/workspace/runtime/foundation/companies/{company}/workspaces/{workspace}/shared
GET /api/workspace/runtime/foundation/companies/{company}/workspaces/{workspace}/shared/employees/{employee}
GET /api/workspace/runtime/foundation/companies/{company}/workspaces/{workspace}/shared/results/{reference}
```

No API command or mutation was added.

## Runtime and schema effect

- Runtime writes: none.
- Schema/migration/seed: none.
- Existing facts consumed: `companies`, `business_directions`, `workspaces`, `projects`,
  `department_instances`, `runtime_entities`, `runtime_links`, `tasks`, `artifacts`.
- Unknown links remain `UNKNOWN` or empty rather than inferred.

## Acceptance evidence

Isolated root:

`/tmp/curis-shared-read-model-regression.sShxA5/runtime.sqlite`

```text
13 passed
  backend/tests/test_shared_workspace_projection.py
  backend/tests/test_runtime_foundation_api.py
  backend/tests/test_rd_workspace_real_execution.py
  backend/tests/test_xhs_calendar_note_runtime.py
  backend/tests/test_workspace_package_company_integration_p05.py

python py_compile: pass
git diff --check: pass
SQLite integrity_check: ok
SQLite foreign_key_check: []
```

The focused test proves:

- a responsibility holder with no current executor is blocked/idle, never running;
- a real executor projects working;
- System Activity remains independent;
- Agent-backed capability and Computer Access `UNKNOWN` truth survive restart;
- Artifact and Evidence resolve through Result Reference;
- wrong-company and same-company/wrong-workspace Artifact reads return 404;
- a newly constructed Runtime reader returns the identical persisted projection.

## Active database truth

Before and after verification:

```text
size: 1232896
mtime: 1786873339
SHA-256: 2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6
```

The active database was not initialized, cleaned, restored or modified.

## Mixed-source protection

`backend/app/api/runtime_foundation_router.py` was untracked Preserved Development Baseline input.
Its pre-change SHA-256 was
`732eb4fffe484e73e2c2383389cfbf88dffde6260f512ce051dafe15084a1f53`.
Owned changes are limited to importing the bounded child router and one `include_router` call. The
file must not be staged wholesale in the bounded commit; all route behavior lives in tracked
`backend/app/api/shared_workspace_router.py`.

## Deferred

- Shared frontend Employee List/Detail/Result Utility consumption;
- Company-wide aggregation across multiple Workspaces;
- explicit Department linkage where no persisted relation exists;
- write-side normalization of legacy domain work-context fields.

These are separate slices; none is represented as implemented by this Review.

## Final result

**SHARED BUSINESS WORKSPACE READ MODEL IMPLEMENTED / ACCEPTED**
