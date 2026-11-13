# Curis Minimal Shared Runtime Foundation Staged Validation

**Status:** Review  
**Date:** 2026-08-16  
**Scope:** G2/G3 common prerequisite — Minimal Shared Runtime Foundation Extraction  
**Decision:** No Shared Foundation staged; structural boundary is not yet commit-safe

## 1. Guard conditions

The existing G2 staged subset was preserved exactly. No G2 path was unstaged, restaged,
modified or committed.

Initial G2 staged diff fingerprint:

```text
91bae0a3ea8a0d063ace3f462093ee94591bef6e28c6c61f7076e20eef6f8622
```

No Shared Runtime file was added to the index during this review. The validation report
itself is also not staged.

## 2. Minimum common dependency identified

The true common runtime dependency is smaller than the current `WorkspaceRuntime` and
foundation bundle:

### Backend core concepts

- tenant/company/workspace scope checks
- persisted runtime entity and runtime link CRUD
- lifecycle transition execution through the existing state-machine engine
- transition history recording
- orthogonal presence / verification / evidence dimensions
- child execution reference attachment
- runtime entity schema and transition-log schema

### Frontend core concepts

- shared Runtime loading/error/empty states
- shared Workspace pane shell: navigation, Context, Utility, resize, compact overlay and
  maximize behavior
- a small Runtime bootstrap/context provider contract

The following are not Shared Foundation and must remain domain-owned:

- RD operating cycles, Task execution, file scope, artifacts and verification
- XHS/TTK ContentItem lifecycle, handoff, decision, receipt and interaction policy
- Staffing, capability supply and Workspace Studio gates
- Simulation scenarios and scenario-specific execution
- external publishing and analytics behavior

## 3. Current file-boundary audit

### `backend/app/runtime/foundation.py`

Contains reusable entity/link/scope/transition helpers, but also contains the entity-type
catalog, domain machine lookup and founding-company materialization behavior. It is not a
pure Shared Foundation file at its current boundary.

### `backend/app/runtime/models.py`

Contains runtime entity/link schema, but also legacy CEO-day tables, Workspace business
tables, simulation-run schema and domain-specific persistence. Whole-file staging would
include non-shared data contracts.

### `backend/app/runtime/registry.py`

Contains the generic registry mechanism together with concrete Business, Commitment,
Workspace, Cycle, Handoff, Decision, Simulation, Content and Interaction state machines.
The concrete registrations are domain logic, not shared infrastructure.

### `backend/app/runtime/states.py`

Contains generic dimensions such as Actor, Presence, Verification and Evidence, but also
Business, Commitment, Workspace, Cycle, Handoff, Decision, Simulation, Content and
Interaction state enums. Whole-file staging would misclassify domain state as Shared.

### `backend/app/runtime/store.py`

The SQLite transition recorder is close to shared infrastructure, but it imports and
attaches the mixed global runtime registry. It cannot form a complete independent commit
without resolving the registry/state dependency boundary.

### Frontend shared candidates

- `WorkspacePaneShell.js` is generic UI behavior, but is untracked, shared by XHS and RD,
  and not independently accepted in the current XHS Review.
- `RuntimeStates.js` is generic UI state presentation and is untracked; it is a safe
  candidate in isolation but does not solve the backend/API boundary.
- `RuntimeProvider.js` is a shared context provider, but it imports the mixed
  `runtimeApi.js` bootstrap surface.
- `runtimeApi.js` combines common bootstrap/workspace calls with RD cycle, Staffing,
  Simulation, Content and founding endpoints.

### Mixed business files

- `backend/app/runtime/workspace.py` combines shared workspace mechanics with Staffing,
  RD cycles, XHS/TTK Content, receipts and interactions.
- `backend/app/api/runtime_foundation_router.py` combines Company, Workspace, RD, Content,
  Simulation, Staffing, receipt, interaction and founding routes.

These boundaries match the Round 2 ownership report. They are not safe whole-file
Shared Foundation candidates.

## 4. Structural blocker

There is no currently existing, complete, independently testable Shared Foundation
package at file boundaries.

A real extraction would require at least:

1. separating generic entity/link/scope persistence from `foundation.py`;
2. separating runtime schema from legacy, simulation and business tables in `models.py`;
3. separating generic state-machine contracts from concrete domain state enums and
   registrations;
4. making the transition recorder depend on the generic registry contract rather than
   the mixed concrete registry;
5. separating the common frontend bootstrap contract from the mixed API client; and
6. deciding whether the shared pane/provider/state components are accepted foundation
   dependencies or remain a separate shared UI group.

Doing only one or two of these would produce a partial abstraction that still imports
domain code. Doing all of them is a source-structure refactor requiring a bounded Issue,
contract tests and an independent migration review. It is not safe to represent that
work as a staging-only operation in this round.

## 5. Source changes

**No source structure was modified.**

No new Shared Foundation module was invented, no existing business file was rewritten,
and no imports or runtime behavior were changed.

## 6. Staged isolation

The staged index still contains only the five previously staged G2 paths:

```text
backend/tests/test_xhs_calendar_note_runtime.py
frontend/app/ceo-office/workspace/xhs/page.js
frontend/components/xhs/XhsWorkspacePhaseOne.js
issues/XHS-WORKSPACE-INSTANCE-001.md
reviews/XHS-WORKSPACE-INSTANCE-001_review.md
```

`git diff --cached --check`: **PASS**.

No backend Shared Runtime file, frontend shared dependency, mixed API client, mixed
router, mixed workspace service or validation report is staged.

## 7. Regression evidence

No source was changed, so no new Shared Foundation regression suite was introduced.
The existing G2 validation remains green:

```text
backend XHS + Runtime Workspace Foundation: 14 passed
frontend Runtime Workspace UI: 7 passed
```

These tests validate the current working-tree implementation, not a newly extracted
Shared Foundation commit. They must not be misreported as proof that the Shared
Foundation has been extracted.

## 8. G2 blocker status

The G2 blocker is **not解除**.

The XHS-only five-file staged subset remains intact, but the XHS route still depends on
unstaged shared frontend files and the accepted backend/API behavior remains inside
mixed Runtime files. G2 cannot be promoted to a commit-ready complete slice until the
Shared Foundation boundary and the mixed XHS/RD service/API/test split are separately
resolved.

## 9. Final decision

```text
MINIMAL SHARED RUNTIME NOT READY FOR COMMIT
G2 STAGED SUBSET PRESERVED
NO COMMIT CREATED
NO PUSH PERFORMED
NO G3 STARTED
```
