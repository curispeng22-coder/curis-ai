# Issue: AI Task Executor MVP Release-Candidate Stabilization And Documentation

## Owner

系统交付席

## Context

产品规划席 accepted the release-candidate boundaries and exact stabilization/documentation plan in `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`.

This issue implements only the accepted RC planning items RC-PLAN-001 through RC-PLAN-006. It does not approve product features or runtime behavior changes.

## Objective

Create the release-candidate stabilization and documentation package needed before first-version local/demo release verification.

## Required Outputs

- Verification command standardization.
- Local backend/frontend startup instructions.
- Local/demo deployment instructions using existing backend and frontend only.
- First-version release checklist.
- Rollback notes.
- FastAPI Python 3.14 deprecation warning triage decision.

Recommended artifact:

- `docs/release/ai-task-executor-mvp-v0.1.md`

The implementation may update existing release-candidate sprint/status documents if needed.

## Allowed Scope

- Documentation-only release-candidate artifacts.
- `.env.example` or equivalent local configuration guidance if needed.
- Quality runbook wording for canonical verification commands.
- Stabilization triage notes for known readiness gaps.
- Source-of-truth updates after implementation.

## Forbidden Scope

- New product features.
- Backend behavior changes.
- Frontend behavior changes beyond documentation references.
- API semantic changes.
- Persistence, new tables, or schema changes.
- New task execution behavior.
- Complex UI/dashboard changes.
- External channels or external services.
- ROI, business modules, Employee CRUD/expansion, company organization, multi-agent routing, or agent abstraction.
- Task-role association or task evidence attachment.
- Automatic evolution behavior changes.
- Vector database, embeddings, external role service, or external memory service.
- Fixing the FastAPI Python 3.14 deprecation warning without a separate approved stabilization issue.

## Acceptance Criteria

- RC-PLAN-001 through RC-PLAN-006 are covered by source-controlled documentation.
- Backend regression command is documented as `cd backend && ./.venv/bin/python -m unittest discover tests`.
- System Python is documented as unsupported unless dependencies are prepared.
- Startup instructions identify backend/frontend working directories and expected local URLs.
- Local/demo deployment instructions do not require external services.
- Release checklist covers backend tests, frontend tests, lint, build, API smoke, Chinese UI, source-of-truth alignment, and forbidden-scope scan.
- Rollback notes identify a source-control restore point process.
- FastAPI deprecation warning is classified as fix-now, defer-known-gap, or separate-issue-needed.
- No backend/frontend implementation behavior is changed.

## Verification Requirements

- `git diff --check`
- `git diff --name-only HEAD -- backend frontend`
- `cd backend && ./.venv/bin/python -m unittest discover tests`
- `cd frontend && node --test app/taskViewModel.test.mjs`
- `cd frontend && npm run lint`
- `cd frontend && npm run build`
- Chinese UI guard:
  - old visible-console English labels do not reappear
  - Chinese operation-console labels remain present
- Forbidden-scope scan over implementation paths.

## Evidence To Use

- `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`
- `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`
- `docs/sprints/ai-task-executor-mvp-release-candidate.md`
- `reviews/019_chinese_operation_console_localization_review.md`
- `reviews/018_ai_task_executor_mvp_readiness_review.md`

## Handoff

Handoff: sent to 系统交付席

Target seat: 系统交付席

Compact payload:

- Issue: `issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md`
- Objective: Implement release-candidate stabilization/documentation package covering RC-PLAN-001 through RC-PLAN-006.
- Preserve: AI Task Executor MVP, Tool System v1.8, Chinese operation console, Task API `{ content }`, accepted readiness review, accepted release-candidate boundaries, Project Memory, Role Profiles, Role Context, Sprint 4 frontend-only boundary, and source-of-truth ownership.
- Allow: documentation-only release artifact, verification command standardization, local startup docs, local/demo deployment docs, release checklist, rollback notes, FastAPI warning triage, `.env.example` or equivalent local configuration guidance if needed, and source-of-truth updates.
- Forbid: new features, backend/frontend behavior changes, API semantic changes, persistence/new tables, execution behavior changes, complex UI/dashboard, external channels/services, ROI, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, task-role association, task evidence attachment, automatic evolution behavior changes, vector DB/embeddings, external role/memory services, and fixing FastAPI warning without a separate approved stabilization issue.

## Delivery Notes

Status: implemented by 系统交付席 on 2026-07-06.

Release artifact: `docs/release/ai-task-executor-mvp-v0.1.md`.

Delivery evidence: `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`.

Implemented scope:

- RC-PLAN-001 through RC-PLAN-006 are covered in source-controlled documentation.
- Backend regression command is standardized as `cd backend && ./.venv/bin/python -m unittest discover tests`.
- System Python is documented as unsupported unless dependencies are prepared.
- Local startup, local/demo deployment, release checklist, rollback notes, and local configuration guidance are documented.
- FastAPI Python 3.14 warning triage decision is `defer-known-gap`.
- No backend/frontend implementation behavior was changed.

Completion handoff:

Handoff: sent to 质量运行席

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Summary:

- `docs/release/ai-task-executor-mvp-v0.1.md` is accepted as the local/demo release-candidate runbook.
- `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md` is accepted.
- FastAPI Python 3.14 warning remains `defer-known-gap`.
- No backend/frontend behavior change, API semantic change, persistence, execution behavior change, external service, complex UI/dashboard, FastAPI warning fix, or future-layer scope is approved by this acceptance.
