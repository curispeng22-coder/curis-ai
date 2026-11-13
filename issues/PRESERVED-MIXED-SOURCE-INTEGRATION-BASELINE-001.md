# PRESERVED-MIXED-SOURCE-INTEGRATION-BASELINE-001

**Status:** IMPLEMENTED / ACCEPTED
**Owner:** Runtime Integration
**Date:** 2026-08-18

## Goal

将已正式验收、但仍依赖 Preserved Development Baseline 中 dirty/untracked integration seam 的 Shared Employee execution trust、RD Phase 2B 和 Workspace Package lifecycle/P1.5 收口为可由当前 commits clean checkout 恢复的开发基线。

## Authority and accepted inputs

- `docs/00_Context/CURRENT_STATE.md`
- `reviews/SHARED-EMPLOYEE-EXECUTION-TRUST-001_review.md`
- `reviews/RD-PHASE-2B-E2E-CLOSURE-001_review.md`
- `reviews/WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001_review.md`
- Preserved Development Baseline snapshot `96cc3406645de69757f63190886ebe99933188a8`

## Current gap

At authorization HEAD `cc8bf4153c1b92a29891cc7084570b294a3d5c25`, accepted tests and standalone modules are committed, but clean HEAD lacks the Runtime Foundation router, Workspace Runtime, execution adapter and their `create_app()` registration. Clean-checkout collection fails before tests can run. The working copies of `runtime_foundation_router.py` and `runtime/workspace.py` match the exact post-change hashes recorded by the accepted RD E2E Review.

## Allowed files

```text
backend/app/main.py                         # Runtime router/executor registration hunks only
backend/app/database.py                     # ensure_runtime_foundation_schema call only
backend/app/api/runtime_foundation_router.py
backend/app/runtime/__init__.py
backend/app/runtime/models.py
backend/app/runtime/registry.py
backend/app/runtime/states.py
backend/app/runtime/store.py
backend/app/runtime/foundation.py
backend/app/runtime/workspace.py
backend/app/runtime/execution_adapter.py
backend/app/runtime/legacy_execution_adapter.py
backend/app/runtime/simulation.py
backend/tests/test_runtime_*.py              # accepted Runtime Foundation bounded regressions only
backend/tests/test_rd_workspace_real_execution.py
backend/tests/test_xhs_calendar_note_runtime.py
issues/PRESERVED-MIXED-SOURCE-INTEGRATION-BASELINE-001.md
reviews/PRESERVED-MIXED-SOURCE-INTEGRATION-BASELINE-001_review.md
```

## Explicit exclusions

- Product/Frozen authority/UI Blueprint/current product-document closure.
- New Runtime, schema or business behavior.
- Unrelated dirty changes in `main.py`, `database.py`, frontend, capability/talent/strategy work.
- Reset, clean, restore, whole-file overwrite, active DB mutation or push.
- Any hunk whose semantic owner cannot be proven.

## Acceptance

1. Integration Ownership Matrix identifies accepted, other and unresolved hunks.
2. Clean-baseline-equivalent export can import `create_app()` and reach Shared/RD/Package routes.
3. Shared identity/callback trust and `verify_handoff_ack()` regressions pass.
4. RD Phase 2B regression passes without hidden worktree files.
5. Package lifecycle/P1.5 migration regression passes without hidden worktree files.
6. XHS and Shared Workspace bounded no-regression pass.
7. Python compile, Backend DB Safety and relevant frontend regression/build pass.
8. All backend tests use one repository-external SQLite through all three DB variables.
9. Active `data/curis.sqlite` size/mtime/SHA/integrity remain unchanged.
10. Every commit passes `git show --check`; no unrelated dirty file is staged or committed.

## Closure

- Integration commit: `8c54bfc20b` (`chore(runtime): close accepted integration baseline`).
- A clean `git archive HEAD` export passes the bounded Shared/RD/XHS/Package suite, Python compile and frontend production build without reading hidden worktree files.
- The worktree intentionally remains dirty for unrelated owners; accepted integration hunks no longer depend on that dirty state.
