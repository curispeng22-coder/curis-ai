# PRESERVED-MIXED-SOURCE-INTEGRATION-BASELINE-001 Review

**Status:** ACCEPTED
**Record Type:** Formal Acceptance Record
**Date:** 2026-08-18
**Issue:** `issues/PRESERVED-MIXED-SOURCE-INTEGRATION-BASELINE-001.md`

## Takeover truth

Authorization HEAD was `cc8bf4153c1b92a29891cc7084570b294a3d5c25`. The worktree had 73 tracked modified files, hundreds of untracked paths and no staged changes. Accepted standalone commits existed, but clean HEAD could not collect the accepted suites:

- `employee_execution_identity.py` imported a `RuntimeScopeError` absent from clean `app.runtime`;
- `workspace_package_runtime.py` imported an absent `runtime.workspace`;
- the clean `create_app()` had no Runtime Foundation router/executor registration.

The active database baseline was size `1232896`, mtime_ns `1786873339955841838`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, `integrity_check=ok`, foreign-key violations `0`.

## Integration Ownership Matrix

| File / seam | Ownership evidence | Closure |
| --- | --- | --- |
| `runtime/workspace.py` | controlled preserved baseline plus accepted XHS/RD evolution; current SHA `99acd951...` exactly matches RD E2E formal Review | tracked at accepted hash |
| `api/runtime_foundation_router.py` | controlled preserved baseline plus accepted Shared/XHS/RD routes; current SHA `f8773324...` exactly matches RD E2E formal Review | tracked at accepted hash |
| `runtime/foundation.py`, `execution_adapter.py`, `legacy_execution_adapter.py`, `simulation.py` | Shared Runtime Foundation only; no Product/UI/domain-private system | tracked as required shared substrate |
| `runtime/{models,states,registry,store,__init__}.py` | existing Shared Runtime state/schema registration consumed by the accepted router/workspace files | only the preserved Runtime deltas archived |
| `main.py` | mixed source | only `asyncio` and accepted Runtime executor/router hunk archived; dotenv, Provider, Talent, Strategy and Connector hunks remain unstaged |
| `database.py` | mixed source | only `ensure_runtime_foundation_schema()` initialization archived; capability ownership and strategy-meeting hunks remain unstaged |
| `WorkspacePaneShell.js` | accepted XHS Shared Shell reused by the already committed Package installed route | tracked; closes clean frontend import |
| Package API/runtime/registration | already committed by Workspace Engineering commits | no rewrite; clean route remains reachable |
| other 68 tracked / 327 untracked paths after closure | Product docs, capability/talent/strategy/UI, prototypes, local DB/evidence and unknown owners | preserved unchanged and excluded |

Before this closure, Shared callback trust, RD Phase 2B and Package P1.5 were individually committed but inaccessible or uncollectable from a clean checkout. After commit `8c54bfc20b`, no accepted hunk for those scopes remains only in `main.py`, `database.py`, the Foundation router or Workspace Runtime dirty state.

## Clean-baseline-equivalent verification

Verification used `git archive HEAD` at `8c54bfc20b`, not the working tree. All three DB variables pointed to one repository-external SQLite.

- Backend: `47 passed` covering Shared canonical Employee/callback trust, `verify_handoff_ack()`, Shared Workspace projection, RD Phase 2B/P7/review/handoff/real execution, XHS Calendar/Note no-regression, Package P0.5/P1/P1.5 migration and Backend DB Safety.
- Restart/persistence/failure/idempotency are exercised by the accepted focused suites, including P1.5 migration failure atomicity and RD same-Cycle retry/restart.
- Python: `compileall` passed for `backend/app` and `backend/tests`.
- Frontend: clean exported source passed `next build --webpack`; the Package installed route resolved the now-tracked Shared Pane Shell.
- Commit: `git show --check 8c54bfc20b` passed.

Active DB after verification remained byte-identical: size `1232896`, mtime_ns `1786873339955841838`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, integrity `ok`, foreign-key violations `0`.

## Remaining ownership risk

The repository worktree is intentionally not clean. Remaining `main.py` and `database.py` hunks belong to capability ownership, Talent/Strategy/Connector and other development lines; they were not guessed, staged or committed. Numerous frontend/domain files, product documents, local databases and evidence paths remain dirty/untracked under their existing owners. They do not supply the accepted Shared/RD Runtime/Package lifecycle integration proven by the clean export, but still require their own bounded reconciliation before those separate capabilities can claim a clean baseline.

**Decision:** `PRESERVED MIXED-SOURCE INTEGRATION BASELINE — ACCEPTED`
