# CURIS AUTONOMOUS OPERATING V1 — PHASE 1–3B COMMIT RECONCILIATION

**Authority Class:** REVIEW
**Status:** Review
**Disposition:** ACCEPTED / BOUNDED COMMIT AUTHORIZED
**Date:** 2026-08-21
**Baseline HEAD:** `50d058ca865c1817721536d7beb47a1c5f1f354d`

## 1. Exact manifest

| Phase | Path | Ownership | Git state before reconciliation | Diff scope / reason |
|---|---|---|---|---|
| 1–3B | `backend/app/runtime/autonomous_operating.py` | Autonomous Operating control plane | untracked | accepted continuous Phase 1 persistence, Phase 2 single-cycle execution, Phase 3A evaluation/decision and Phase 3B successor control |
| 1 | `backend/app/runtime/__init__.py` | Shared Runtime export seam | tracked modified | exactly 3 added lines: import and two public exports; no unrelated hunk |
| 3A | `backend/app/runtime/registry.py` | Existing Decision Packet state machine | tracked modified | exactly 6 added lines: bounded `READY → DECIDED` Leader transition for `AUTONOMOUS_NEXT_CYCLE`; no unrelated hunk |
| 1 | `backend/tests/test_autonomous_operating_phase1.py` | Phase 1 acceptance | untracked | control persistence, idempotency, restart and stop-state truth |
| 2 | `backend/tests/test_autonomous_operating_phase2.py` | Phase 2 acceptance | untracked | one real Team Operating / Employee / Provider cycle and failure truth |
| 3A | `backend/tests/test_autonomous_operating_phase3a.py` | Phase 3A acceptance | untracked | evidence-bound evaluation and Leader decision truth |
| 3B | `backend/tests/test_autonomous_operating_phase3b.py` | Phase 3B acceptance | untracked | exactly-one successor, non-successor decisions, concurrency and rollback |
| 1 | `issues/20260821_autonomous_operating_v1_phase1_control_persistence_001.md` | Issue | untracked | accepted Phase 1 boundary and evidence |
| 2 | `issues/20260821_autonomous_operating_v1_phase2_single_cycle_execution_001.md` | Issue | untracked | accepted Phase 2 boundary and evidence |
| 3A | `issues/20260821_autonomous_operating_v1_phase3a_evaluation_decision_001.md` | Issue | untracked | accepted Phase 3A boundary and evidence |
| 3B | `issues/20260821_autonomous_operating_v1_phase3b_successor_control_001.md` | Issue | untracked | accepted Phase 3B boundary and evidence |
| 1 | `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE1_CONTROL_PERSISTENCE_REVIEW.md` | Review | untracked | formal accepted Phase 1 record |
| 2 | `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE2_SINGLE_CYCLE_EXECUTION_REVIEW.md` | Review | untracked | formal accepted Phase 2 record |
| 3A | `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE3A_EVALUATION_DECISION_REVIEW.md` | Review | untracked | formal accepted Phase 3A record |
| 3B | `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE3B_SUCCESSOR_CONTROL_REVIEW.md` | Review | untracked | formal accepted Phase 3B record |
| 1–3B | `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE1_3B_COMMIT_RECONCILIATION.md` | Integration Review | new | exact manifest, test, database and exclusion record |

The umbrella readiness file `issues/20260820_autonomous_operating_v1_implementation_001.md` is excluded: it includes future Phase scope and is not an exact Phase 1–3B implementation record.

## 2. Accepted dependency mapping

- Phase 1 owns the minimal persisted `OPERATING_SERIES`, deterministic `TRIGGER_CLAIM`, existing `CYCLE` control pins and public Runtime export.
- Phase 2 extends the same module into one bounded existing Team Operating / Employee / Provider execution and closes one accepted Cycle with real Result, Artifact and Evidence.
- Phase 3A extends the same module with evidence-bound Evaluation and canonical Leader Review, and adds only the bounded existing `DECISION_PACKET` transition in `registry.py`.
- Phase 3B uses the applied canonical Decision as the sole authority for exactly one deterministic successor Claim and existing Cycle.

No second Task, Workflow, Employee, Result, Decision, Cycle or Learning system is included.

## 3. Verified operating truth

- `CONTINUE` creates exactly one Cycle 2.
- bounded `ADJUST` creates exactly one Cycle 2 with bounded adjusted pins.
- `WAIT`, `ESCALATE`, `PAUSE` and `STOP` create no successor Cycle.
- Cycle 2 is `PLANNED / NOT_STARTED`.
- no accepted Learning is created.
- no second-cycle Employee or Provider execution is started.
- duplicate, restart and concurrent successor authorization return the same deterministic Claim/Cycle.
- interrupted atomic successor creation rolls back Claim, Cycle and lineage together.

## 4. Verification

All tests used one repository-external temporary SQLite through `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` before import.

| Check | Result |
|---|---|
| Phase 1 focused | `11 passed` |
| Phase 2 focused | `7 passed` |
| Phase 3A focused | `14 passed` |
| Phase 3B focused | `15 passed` |
| Responsibility Routing + Team Operating real Employee E2E + RD Decision + DB Safety | `17 passed` |
| Python compile | PASS |
| working-tree `git diff --check` | PASS |

The exact staged tree was exported as Git tree
`7624096bf6c3fac98bcf57ca24759ed6b3a900db`. In that clean export, all four
Autonomous focused suites passed again (`11 + 7 + 14 + 15`). This proves the
Phase 1–3B chain does not depend on a hidden working-copy hunk.

The additional regression set passed `17/17` in the preserved working baseline.
It is intentionally not used as a clean-export closure claim: the RD Decision
test consumes unrelated preserved canonical-Business changes, and the DB Safety
test intentionally fingerprints repository active-database files that are not
present in a source-only archive. Neither dependency belongs to this Issue and
neither is promoted by this commit.

## 5. Active database safety

| Path | Size | mtime | SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

These values must remain identical after staging, clean-index verification and commit.

## 6. Explicit exclusions

- no Learning or Knowledge promotion;
- no second-cycle execution;
- no UI/API change;
- no Business-scope Provider execution;
- no Product, visual, Prototype or Business Spine files;
- no unrelated preserved worktree content;
- no active database write;
- no push.

## 7. Commit recommendation

Stage only the exact manifest above, verify the staged tree and clean-index-equivalent tests, then create:

`feat(runtime): establish autonomous operating control loop`

Final accepted boundary remains Phase 1–3B only.
