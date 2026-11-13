# Issue: Workflow Error/Fallback Observability Boundaries

## Owner

系统交付席

## Context

总控决策席 approved the Workflow Error/Fallback Observability gate in `issues/028_workflow_error_fallback_observability_gate.md`.

This issue defines architecture boundaries only. It does not approve implementation.

Boundary ADR: `docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md`.

## Objective

Define Workflow Error/Fallback Observability architecture boundaries before implementation.

## Allowed Scope

- Architecture boundary definition only.
- Evidence map for existing workflow error behavior.
- Evidence map for existing tool fallback behavior.
- Existing failure log, workflow trace, tool trace, adaptation-event, and tool-performance evidence review.
- Verification planning for current behavior.
- Gap classification for stabilization, verification, documentation, or future product scope.
- Source-of-truth updates after boundary definition.

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

- Backend/frontend implementation.
- New product features.
- New UI/dashboard.
- API semantic changes.
- Persistence/schema/new table changes.
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

- ADR is created under `docs/decisions/`.
- Review/evidence file is created under `reviews/`.
- First implementation recommendation is bounded to backend tests and evidence documentation only.
- No backend/frontend implementation files are changed.
- `PROJECT_STATUS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` route the next step to 质量运行席.

## Boundary Summary

Defined in `docs/decisions/ADR-0011-workflow-error-fallback-observability-boundaries.md`.

Recommended first implementation slice: `Workflow Error/Fallback Evidence Map`.

## Handoff

Handoff: sent to 质量运行席.

Target seat: 质量运行席.

Compact payload:

- Issue: `issues/029_workflow_error_fallback_observability_boundaries.md`
- Objective: Verify Workflow Error/Fallback Observability architecture boundaries before implementation.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing tool/workflow behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: architecture boundary verification only for existing workflow error observability, tool fallback observability, failure log, workflow trace, tool trace, adaptation-event evidence, tool performance evidence, verification planning, and gap classification.
- Forbid: implementation, new features, UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, new tool routing/registry semantics, external services, automatic evolution behavior changes, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer scope.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-06.

Quality evidence: `reviews/026_workflow_error_fallback_observability_boundaries_review.md`.

Verification results:

- No backend/frontend implementation diff.
- `git diff --check` passed.
- Forbidden-scope scan passed; matches were limited to preserved/forbidden scope language and verification-command text.

Completion handoff:

Handoff: sent to 产品规划席.

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Acceptance evidence: `reviews/026_workflow_error_fallback_observability_boundaries_review.md`.

Accepted first implementation slice: `Workflow Error/Fallback Evidence Map`.

Implementation issue: `issues/030_workflow_error_fallback_evidence_map.md`.

Decision rationale:

- Boundary stays inside post-v0.1 Execution Reliability.
- Quality verification passed with no backend/frontend implementation diff.
- First implementation is limited to backend tests and evidence documentation for existing behavior.
