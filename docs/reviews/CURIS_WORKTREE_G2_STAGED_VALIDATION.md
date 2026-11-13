# Curis Worktree G2 Staged Validation

**Status:** Review  
**Date:** 2026-08-16  
**Scope:** G2 — XHS accepted vertical slice staging audit  
**Decision:** G2 staged subset validated; full G2 commit is not ready

## 1. Source review

Rechecked:

- `issues/XHS-WORKSPACE-INSTANCE-001.md`
- `reviews/XHS-WORKSPACE-INSTANCE-001_review.md`
- `docs/reviews/CURIS_WORKTREE_OWNERSHIP_AND_ISOLATION_PLAN.md`
- `docs/reviews/CURIS_WORKTREE_RECONCILIATION_DECISIONS.md`
- current Git status and current working-tree contents

The accepted XHS boundary remains an internal Runtime-backed vertical slice through
`SCHEDULED`. It does not include a real external XHS publishing connector, external
publication receipt, or analytics connector.

## 2. Paths staged in this round

The following five XHS-only paths are staged:

```text
backend/tests/test_xhs_calendar_note_runtime.py
frontend/app/ceo-office/workspace/xhs/page.js
frontend/components/xhs/XhsWorkspacePhaseOne.js
issues/XHS-WORKSPACE-INSTANCE-001.md
reviews/XHS-WORKSPACE-INSTANCE-001_review.md
```

The Issue and Review were staged after removing only the trailing whitespace reported by
`git diff --cached --check`. No semantic text was changed.

## 3. Mixed-file boundary and exclusions

The following requested G2 files were inspected but intentionally not staged:

### `backend/app/runtime/workspace.py`

This is a new mixed file containing Workspace creation, capability supply, staffing,
RD operating-cycle execution, XHS/TTK content lifecycle, publication receipt and
interaction logic. The XHS content methods cannot be staged as a valid independent new
file without either including RD/Shared Runtime sections or creating a new source split.
Whole-file staging is prohibited by the existing reconciliation decision.

### `backend/app/api/runtime_foundation_router.py`

This is a new mixed router containing Company, Workspace, RD Cycle, XHS/TTK Content,
Simulation, Staffing, receipt, interaction and founding routes. The XHS content route
block is not a valid standalone new file for index-only staging; whole-file staging
would include RD, Staffing, Simulation and Shared Runtime routes.

### `frontend/lib/runtimeApi.js`

This is a new mixed API client containing company/bootstrap, simulation, staffing,
workspace, RD cycle, content/version, founding and shared entity APIs. Whole-file
staging would include RD and Shared Runtime API surface. A partial new-file index patch
would not be a valid commit-ready module.

### `frontend/tests/runtimeWorkspaceUi.test.mjs`

This is a new shared regression file. It contains XHS assertions together with RD,
TTK, Workspace Studio, Assistant and workforce assertions. It was not staged whole;
the XHS-only assertions cannot be committed as an independent valid new test file
without a dedicated test split, which is outside this staging round.

### Shared frontend dependencies

`frontend/components/workspace/WorkspacePaneShell.js`,
`frontend/components/runtime/RuntimeProvider.js`, and
`frontend/components/runtime/RuntimeStates.js` are untracked shared dependencies of
the XHS route/component. They were not staged because their ownership is shared and
they are not independently accepted XHS-only files in the current Issue/Review record.

Explicitly not staged:

- RD and TTK implementation files
- Shared Runtime non-XHS portions
- Talent Market and AI Capability
- Content Growth
- Workspace Engineering
- other frontend product waves
- database, active SQLite, WAL/SHM, build, cache, desktop and temporary artifacts
- the G2 validation report itself

## 4. Staged diff/path audit

```text
git diff --cached --stat
```

Result:

```text
5 files changed, 830 insertions(+)
```

`git diff --cached --name-status` contains exactly the five paths listed in Section 2.
No forbidden path is staged.

## 5. Staged whitespace check

Command:

```text
git diff --cached --check
```

Result: **PASS**.

## 6. Focused backend validation

Command:

```text
backend/.venv/bin/python -m pytest -q \
  backend/tests/test_xhs_calendar_note_runtime.py \
  backend/tests/test_runtime_workspace_foundation.py
```

Result: **PASS — 14 passed in 5.56s**.

The run used the existing isolated-test behavior and emitted only existing FastAPI
deprecation warnings.

## 7. Runtime Workspace UI validation

Command:

```text
node --test frontend/tests/runtimeWorkspaceUi.test.mjs
```

Result: **PASS — 7 passed**.

Node emitted the existing module-type warning for `runtimeApi.js`; no test failed.

## 8. Acceptance boundary

The staged XHS Issue/Review continue to state:

- XHS is accepted only as the internal Runtime-backed vertical slice.
- The accepted flow reaches `SCHEDULED` with truthful waiting/unavailable states.
- Real external publishing is not connected.
- Analytics data is unavailable without a verified external source.
- No external publication or analytics completion is claimed by this staging audit.

## 9. Working-tree preservation

All non-staged mixed files and other initiative changes remain in the working tree.
No reset, restore, clean, delete, move, commit or push operation was performed.

The five staged files are a clean XHS-only subset, but the required mixed Runtime/API
and shared-test pieces remain unstaged. Therefore the full accepted G2 slice is not yet
represented by a commit-ready staged set.

## 10. Scope deviation and recommendation

**Scope deviation:** the requested mixed G2 files could not be safely staged without
including non-XHS initiatives or creating incomplete new files in the index.

**Recommendation:** do not commit this five-file subset as G2. First authorize a
separate bounded source/test extraction or resolve shared ownership for the mixed files.

```text
G2 NOT READY FOR COMMIT
NO COMMIT CREATED
NO PUSH PERFORMED
NO G3 STARTED
```
