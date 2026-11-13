# Issue: AI Task Executor MVP Release Candidate Gate

## Owner

总控决策席

## Context

AI Task Executor MVP readiness review was accepted by 产品规划席 on 2026-07-06. No blocker gaps were found.

The user approved opening the next release-candidate flow after asking how many development flows remain before the first online version.

## Objective

Decide whether to approve an AI Task Executor MVP release-candidate gate for stabilization, verification, and release documentation only.

## Scope To Decide

- Whether current AI Task Executor MVP can enter release-candidate preparation.
- Whether release-candidate work is limited to stabilization, verification, startup/deployment documentation, release checklist, and rollback notes.
- Whether future product scope remains blocked until after first-version release.

## Allowed Release Candidate Work

- Stabilization-only fixes for known readiness gaps.
- Verification command standardization.
- Environment and startup documentation.
- Local/demo deployment instructions.
- Release checklist and rollback notes.
- Regression verification for backend tests, frontend tests, lint, build, API smoke, Chinese UI, and scope drift.

## Forbidden Scope

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Company organization, departments, reporting lines, staffing, or ownership model.
- Multi-agent routing.
- Agent abstraction layer.
- External entry channels or third-party platform integrations.
- Complex UI, role dashboard, analytics dashboard, or company dashboard.
- New task execution behavior.
- API semantic changes.
- Backend metadata, persistence, new tables, or task-role association.
- Task evidence attachment.
- Runtime prompt integration beyond approved role-context helper behavior.
- Automatic evolution behavior.
- Vector database, embeddings, external role service, or external memory service.

## Evidence To Review

- `docs/sprints/ai-task-executor-mvp-release-candidate.md`
- `reviews/018_ai_task_executor_mvp_readiness_review.md`
- `reviews/019_chinese_operation_console_localization_review.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`

## Acceptance Criteria

- Gate decision is recorded in this issue.
- If approved, next seat is 系统交付席 for release-candidate boundary definition.
- If revised, revision notes identify the exact scope change.
- No implementation is approved directly by this gate.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-06.

Rationale:

- AI Task Executor MVP readiness review was accepted by 产品规划席 with no blocker readiness gaps.
- Chinese operation console localization was completed as frontend-only presentation work and preserves Task API `{ content }`, backend behavior, persistence, and execution-loop behavior.
- Release-candidate entry is constrained to stabilization planning, verification command standardization, startup/deployment documentation, release checklist, rollback notes, local/demo deployment instructions, and regression verification planning.
- No new product feature, ROI, business module, Employee expansion, company organization, multi-agent routing, agent abstraction, external channel, complex dashboard UI, new execution behavior, API semantic change, persistence/new table, task-role association, task evidence attachment, automatic evolution behavior, vector DB/embedding, external service, or future-layer scope is approved.

## Handoff

Handoff: HANDOFF_REQUIRED

Target seat: 系统交付席

Compact payload:

- Issue: `issues/021_ai_task_executor_mvp_release_candidate_gate.md`
- Objective: Define AI Task Executor MVP release-candidate boundaries and exact stabilization/documentation plan before any implementation.
- Preserve: AI Task Executor MVP, Tool System v1.8, Chinese operation console, current Task API `{ content }`, accepted readiness review, Project Memory, Role Profiles, Role Context, Sprint 4 frontend-only boundary, and source-of-truth ownership.
- Allow: stabilization planning, verification command standardization, startup/deployment docs, release checklist, rollback notes, local/demo deployment instructions, and regression verification planning only.
- Forbid: new product features, ROI, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, external channels, complex dashboard UI, new execution behavior, API semantic changes, persistence/new tables, task-role association, task evidence attachment, automatic evolution behavior, vector DB/embeddings, external services, and future-layer scope.

## Boundary Definition Notes

Status: defined by 系统交付席 on 2026-07-06.

Architecture record: `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`.

Boundary evidence: `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`.

Defined scope:

- Release-candidate work is limited to stabilization planning, verification command standardization, startup/deployment docs, release checklist, rollback notes, local/demo deployment instructions, and regression verification planning.
- Exact planned items are RC-PLAN-001 through RC-PLAN-006 in ADR-0009 and the review evidence.
- Implementation remains blocked until a separate approved issue defines exact stabilization/documentation work and verification.

Completion handoff:

Handoff: sent to 质量运行席

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Summary:

- `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md` is accepted.
- RC-PLAN-001 through RC-PLAN-006 are accepted as the only allowed release-candidate planning items.
- No implementation is approved by this acceptance.
- Release-candidate implementation remains blocked until a separate scoped issue defines exact stabilization/documentation work and verification.
