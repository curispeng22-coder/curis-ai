# Execution Summary Memory

Date: 2026-07-07

Purpose: compact, deterministic summary of accepted Curis Workspace execution and release evidence.

This file is a Project Memory companion artifact. It does not own project truth. If a fact is wrong, update the owning source first, then refresh this summary.

## Source Rules

- Every summary below must point to owning source files.
- This file does not replace issues, reviews, ADRs, release docs, `PROJECT_STATUS.md`, `TASKS.md`, or `knowledge/CURRENT_CONTEXT.md`.
- No hidden memory store, vector database, embeddings, external memory service, agent memory, Employee memory, runtime prompt integration, task evidence attachment, multi-agent coordination, or new execution behavior is created here.

Sources:

- `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- `docs/release/ai-task-executor-mvp-v0.1.md`
- `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`
- `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`
- `reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md`
- `reviews/025_run_evidence_reliability_first_slice_review.md`
- `reviews/027_workflow_error_fallback_evidence_map_review.md`
- `reviews/029_evolution_decision_evidence_map_review.md`
- `reviews/030_post_v0_1_execution_reliability_closeout_review.md`
- `reviews/032_local_demo_operator_release_notes_package_review.md`
- `reviews/034_local_demo_api_smoke_helper_review.md`
- `issues/043_project_memory_execution_summary.md`

## Current Execution Baseline

- Current visible product: AI Task Executor MVP v0.1 local/demo release.
- Current user-facing operation mode: Chinese operation console.
- Current task entry contract: existing Task API payload `{ content }`.
- Current stable execution scope: task creation, run action, task status/history, selected-task detail, execution evidence, Project Memory, role profiles/helper, operator notes, and local API smoke helper.
- Current verification helper: `tools/local_demo_api_smoke.py` checks health, task creation, and task history against the real local FastAPI app.

Sources:

- `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`
- `reviews/034_local_demo_api_smoke_helper_review.md`

## Accepted Release Evidence

- AI Task Executor MVP v0.1 is accepted as a local/demo first version, not hosted production SaaS.
- Verified restore point for the first version is `c5011acd`.
- Release verification passed for backend regression, frontend view-model tests, frontend lint, frontend build, Chinese-console guard, forbidden-scope scan, and API smoke.
- Release API smoke used the real local FastAPI app for health, task creation, and task history.
- No mock data or simulation substitution was used for release verification.

Sources:

- `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`
- `reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md`

## Accepted Reliability Evidence

- Run Evidence Reliability is accepted: successful and failed run evidence chains are covered.
- Workflow Error/Fallback Evidence Map is accepted: primary failure, fallback success, full fallback failure, workflow trace, adaptation log, failure log, and tool performance evidence are covered.
- Evolution Decision Evidence Map is accepted: stable do-not-evolve evidence, threshold-triggered controlled proposal evidence, rollback evidence, locked-module postpone evidence, and evolution-decision API evidence are covered.
- Post-v0.1 Execution Reliability closeout found no blocker gaps.
- FastAPI Python 3.14 warning remains a known `defer-known-gap`.

Sources:

- `reviews/025_run_evidence_reliability_first_slice_review.md`
- `reviews/027_workflow_error_fallback_evidence_map_review.md`
- `reviews/029_evolution_decision_evidence_map_review.md`
- `reviews/030_post_v0_1_execution_reliability_closeout_review.md`

## Accepted Operator Evidence

- Local/demo operator notes are accepted.
- Operator notes cover startup, smoke verification, shutdown, rollback, known warning, evidence references, and still-blocked scope.
- The accepted operator polish slice is documentation-only.
- It does not change backend behavior, frontend behavior, API semantics, persistence, execution behavior, external services, or future AI Company System layers.

Sources:

- `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`
- `reviews/032_local_demo_operator_release_notes_package_review.md`

## Accepted Local Verification Automation Evidence

- Local/Demo API Smoke Helper is accepted.
- Helper artifact: `tools/local_demo_api_smoke.py`.
- Helper verifies `GET /health`, `POST /api/task` with existing `{ content }`, and `GET /api/tasks`.
- Quality verification ran the helper against the real local FastAPI app and passed.
- The helper is local-only tooling and does not change backend/frontend behavior.

Sources:

- `tools/local_demo_api_smoke.py`
- `reviews/034_local_demo_api_smoke_helper_review.md`
- `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`

## Blocked Or Deferred Scope

- Hosted production deployment remains deferred.
- L5 company organization remains blocked.
- L6 economy/ROI remains blocked.
- Business modules remain blocked.
- Employee CRUD/expansion remains blocked.
- Multi-agent routing and agent abstraction remain blocked.
- Complex dashboard UI remains blocked.
- API semantic changes and persistence/schema/new table changes remain blocked unless separately approved.
- Vector DB, embeddings, external memory service, hidden memory store, agent memory, and Employee memory remain blocked.
- Runtime prompt integration, task-role association, and task evidence attachment remain blocked unless separately approved.

Sources:

- `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- `reviews/030_post_v0_1_execution_reliability_closeout_review.md`
- `docs/decisions/ADR-0015-project-memory-execution-summary-boundaries.md`

## Future Gap Classification

Documentation gaps:

- Keep this file updated after accepted release, reliability, operator, verification, or sprint-closeout work.

Verification gaps:

- Re-run local API smoke helper before any new demo checkpoint.
- Keep backend regression and frontend verification commands in release docs as the canonical fuller verification path.

Future product-scope gaps:

- Any runtime Project Memory read API, execution-summary helper, vector memory, embedding memory, agent memory, Employee memory, or task evidence attachment requires a separate approved issue.

Sources:

- `issues/043_project_memory_execution_summary.md`
- `docs/decisions/ADR-0015-project-memory-execution-summary-boundaries.md`
