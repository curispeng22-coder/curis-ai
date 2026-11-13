# Issue: Workflow Error/Fallback Observability Gate

## Owner

总控决策席

## Context

AI Task Executor MVP v0.1 has been closed as the first local/demo version.

Post-v0.1 Execution Reliability boundaries were accepted in `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`.

The first reliability slice, Run Evidence Reliability, was implemented, verified, and accepted in `reviews/025_run_evidence_reliability_first_slice_review.md`.

The next proposed reliability slice should strengthen operator confidence in the existing workflow error and tool fallback evidence path before any future product-layer expansion.

## Decision

Status: APPROVED by 总控决策席 on 2026-07-06.

Approve architecture boundary definition for a bounded Workflow Error/Fallback Observability slice.

This approval does not approve implementation.

## Rationale

Run Evidence Reliability has strengthened the execution result evidence chain. The next highest-leverage reliability work is to make the existing workflow error and tool fallback evidence path more explicit and reviewable.

This remains inside the current AI Task Executor MVP and post-v0.1 Execution Reliability phase. It does not open ROI, company organization, business modules, external channels, new UI/dashboard, new tool semantics, or new execution behavior.

## Objective

Decide whether to approve architecture boundary definition for a bounded Workflow Error/Fallback Observability slice.

## Allowed Scope

- Architecture boundary definition only.
- Existing workflow error observability.
- Existing tool fallback observability.
- Existing failure log, workflow trace, tool trace, and adaptation-event evidence review.
- Verification planning for current behavior only.
- Gap classification for stabilization, verification, documentation, or future product scope.
- Source-of-truth updates after gate decision.

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

- 总控决策席 records approve or reject decision.
- If approved, next step routes to 系统交付席 for architecture boundary definition only.
- `PROJECT_STATUS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` are updated.
- No backend/frontend implementation files are changed by this gate.
- Compact handoff payload is ready for the next seat.

## Handoff

Handoff: sent to 系统交付席.

Target seat: 系统交付席.

Compact payload:

- Issue: `issues/028_workflow_error_fallback_observability_gate.md`
- Objective: Define Workflow Error/Fallback Observability architecture boundaries before implementation.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing tool/workflow behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: architecture boundary definition only around existing workflow error observability, tool fallback observability, failure log, workflow trace, tool trace, adaptation-event evidence, verification planning, and gap classification.
- Forbid: implementation, new features, UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, new tool routing/registry semantics, external services, automatic evolution behavior changes, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer scope.
