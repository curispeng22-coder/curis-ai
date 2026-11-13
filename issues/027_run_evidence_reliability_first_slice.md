# Issue: Run Evidence Reliability First Slice

## Owner

系统交付席

## Context

产品规划席 accepted the post-v0.1 Execution Reliability architecture boundaries in `reviews/024_post_v0_1_execution_reliability_boundaries_review.md`.

Boundary ADR: `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`.

This is the first implementation slice after v0.1 local/demo release closeout.

## Objective

Implement the `Run Evidence Reliability` first slice.

## Allowed Scope

- Backend tests for existing `/api/task/{task_id}/run` success behavior.
- Backend tests for existing `/api/task/{task_id}/run` failure behavior.
- Evidence checks for existing task status, execution row, workflow state, tool trace, workflow trace, learning metrics, meta-development report, and evolution decision records.
- Documentation or review evidence needed to prove existing run behavior reliability.
- Source-of-truth updates after implementation and verification.

## Required Preservation

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Project Memory.
- Role Profiles.
- Role Context.
- Release record/tag semantics.
- Source-of-truth ownership.

## Forbidden Scope

- API semantic changes.
- Persistence/schema/new table changes.
- UI changes.
- External services or new model-provider integrations.
- New product features.
- New execution behavior.
- Automatic evolution behavior changes.
- Runtime prompt integration beyond approved helper behavior.
- Task-role association.
- Task evidence attachment.
- ROI/economy.
- Business modules.
- Employee CRUD/expansion.
- Company organization, departments, reporting lines, or staffing.
- Multi-agent routing.
- Agent abstraction layer.
- Future-layer implementation.

## Acceptance Criteria

- Successful run reliability is covered by backend tests or equivalent deterministic local evidence.
- Failed run reliability is covered by backend tests or equivalent deterministic local evidence.
- Existing task status, execution row, workflow state, tool trace, workflow trace, learning metrics, meta-development report, and evolution decision evidence are covered.
- Existing API semantics and persistence schema are preserved.
- Backend regression passes with `cd backend && ./.venv/bin/python -m unittest discover tests`.
- `git diff --check` passes.
- `git diff --name-only HEAD -- frontend` remains empty unless separately approved.
- Scope scan confirms no future-layer or forbidden-scope implementation drift.

## Handoff

Handoff: sent to 系统交付席.

Target seat: 系统交付席.

Compact payload:

- Issue: `issues/027_run_evidence_reliability_first_slice.md`
- Objective: Implement Run Evidence Reliability first slice.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: backend tests and evidence quality around existing run success/failure behavior, task status, execution row, workflow state, traces, learning metrics, meta-development report, and evolution decision records.
- Forbid: API semantic changes, persistence/schema/new tables, UI changes, external services, new features, new execution behavior, automatic evolution behavior changes, runtime prompt expansion, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer implementation.

## Implementation Notes

Status: implemented by 系统交付席 on 2026-07-06.

Delivery evidence: `reviews/025_run_evidence_reliability_first_slice_review.md`.

Implementation summary:

- Added backend coverage for successful run evidence chain.
- Added backend coverage for failed run evidence chain.
- Fixed duplicate failed-run tool trace persistence.

Verification:

- Targeted failed-run RED check failed before the fix because failed tool traces were duplicated.
- Targeted failed-run GREEN check passed after the fix.
- Focused reliability tests passed.
- Backend regression passed with 36 tests.

Completion handoff:

Handoff: sent to 质量运行席.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-06.

Quality evidence: `reviews/025_run_evidence_reliability_first_slice_review.md`.

Verification results:

- Focused reliability tests passed, 2 tests.
- Backend regression passed, 36 tests.
- `git diff --check` passed.
- Frontend diff guard passed; no frontend files changed.
- Backend implementation diff guard passed during quality verification; no uncommitted backend implementation diff remained.
- Forbidden-scope scan passed; matches were limited to issue/review boundary text.
- FastAPI Python 3.14 warning remains `defer-known-gap`.

Completion handoff:

Handoff: sent to 产品规划席.

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Acceptance evidence: `reviews/025_run_evidence_reliability_first_slice_review.md`.

Decision rationale:

- The first post-v0.1 reliability slice improves the current AI Task Executor run evidence chain without expanding product scope.
- Successful and failed run behavior are covered by backend tests and quality verification.
- Duplicate failed-run tool trace persistence is fixed without changing API semantics, persistence schema, UI, external services, new feature scope, or execution-loop behavior.

Next product move:

- Open a bounded gate for Workflow Error/Fallback Observability as the next post-v0.1 reliability slice.
