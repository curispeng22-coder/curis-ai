# Issue: Workflow Error/Fallback Evidence Map

## Owner

系统交付席

## Context

产品规划席 accepted Workflow Error/Fallback Observability boundaries in `reviews/026_workflow_error_fallback_observability_boundaries_review.md`.

Boundary ADR: `docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md`.

This is the first implementation slice for the accepted boundary.

## Objective

Implement the `Workflow Error/Fallback Evidence Map` first slice.

## Allowed Scope

- Backend tests for existing primary-tool failure followed by successful fallback.
- Backend tests for existing full fallback-chain failure.
- Evidence checks for existing tool trace, workflow state, adaptation log, failure log, and tool performance behavior.
- Documentation or review evidence needed to prove existing workflow error/fallback observability.
- Source-of-truth updates after implementation and verification.

## Required Preservation

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing tool registry, tool router, tool executor, and workflow behavior.
- Project Memory.
- Role Profiles.
- Role Context.
- Release record/tag semantics.
- Source-of-truth ownership.

## Forbidden Scope

- API semantic changes.
- Persistence/schema/new table changes.
- UI changes.
- New product features.
- New execution behavior.
- New tool-routing behavior.
- New tool registry semantics.
- External services or new model-provider integrations.
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

- Successful fallback path is covered by backend tests or equivalent deterministic local evidence.
- Full fallback-chain failure path is covered by backend tests or equivalent deterministic local evidence.
- Existing tool trace, workflow state, adaptation log, failure log, and tool performance evidence are covered.
- Existing API semantics and persistence schema are preserved.
- Backend regression passes with `cd backend && ./.venv/bin/python -m unittest discover tests`.
- `git diff --check` passes.
- `git diff --name-only HEAD -- frontend` remains empty unless separately approved.
- Scope scan confirms no future-layer or forbidden-scope implementation drift.

## Handoff

Handoff: sent to 系统交付席.

Target seat: 系统交付席.

Compact payload:

- Issue: `issues/030_workflow_error_fallback_evidence_map.md`
- Objective: Implement Workflow Error/Fallback Evidence Map first slice.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing tool/workflow behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: backend tests and evidence documentation for existing primary-tool fallback success, full fallback-chain failure, tool trace, workflow state, adaptation log, failure log, and tool performance behavior.
- Forbid: API semantic changes, persistence/schema/new tables, UI changes, new features, new execution behavior, new tool routing/registry semantics, external services, automatic evolution behavior changes, runtime prompt expansion, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer implementation.

## Implementation Notes

Status: implemented by 系统交付席 on 2026-07-06.

Delivery evidence: `reviews/027_workflow_error_fallback_evidence_map_review.md`.

Implementation summary:

- Added backend coverage for successful primary-tool failure followed by fallback success.
- Added backend coverage for full fallback-chain failure.
- Covered existing tool trace, workflow state, adaptation log, failure log, and tool performance evidence surfaces.
- No backend production files were changed.
- No frontend files were changed.

Verification:

- Focused evidence-map tests passed, 2 tests.
- Backend regression passed with 38 tests.
- `git diff --check` passed.
- Frontend diff guard passed.
- Backend production diff guard passed.
- Scope scan found no forbidden implementation drift.

Completion handoff:

Handoff: sent to 质量运行席.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-06.

Quality evidence: `reviews/027_workflow_error_fallback_evidence_map_review.md`.

Verification results:

- Focused evidence-map tests passed, 2 tests.
- Backend regression passed, 38 tests.
- `git diff --check` passed.
- Frontend diff guard passed; no frontend files changed.
- Backend production diff guard passed; no `backend/app` files changed.
- Forbidden-scope scan passed; matches were limited to issue/review preservation, forbidden-scope, or verification-command text.
- FastAPI Python 3.14 warning remains `defer-known-gap`.

Completion handoff:

Handoff: sent to 产品规划席.

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Acceptance evidence: `reviews/027_workflow_error_fallback_evidence_map_review.md`.

Decision rationale:

- Successful fallback and full fallback-chain failure evidence maps are now covered.
- Quality verification passed with focused tests and backend regression.
- Backend production code, frontend, API semantics, persistence schema, tool-routing semantics, execution behavior, and future-layer boundaries remain preserved.

Next product move:

- Open a bounded gate for Evolution Decision Evidence Reliability as the next post-v0.1 reliability slice.
