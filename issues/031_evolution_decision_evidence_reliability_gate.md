# Issue: Evolution Decision Evidence Reliability Gate

## Owner

总控决策席

## Context

AI Task Executor MVP v0.1 has been closed as the first local/demo version.

Post-v0.1 Execution Reliability boundaries were accepted in `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`.

Run Evidence Reliability and Workflow Error/Fallback Evidence Map have been implemented, verified, and accepted.

The next proposed reliability slice should strengthen confidence that existing Evolution Governor decisions are visible, stable, and reviewable without changing automatic evolution behavior.

## Decision

Status: APPROVED by 总控决策席 on 2026-07-06.

Approve architecture boundary definition for a bounded Evolution Decision Evidence Reliability slice.

This approval does not approve implementation.

## Rationale

Run Evidence Reliability and Workflow Error/Fallback Evidence Map have strengthened execution-path evidence. The next highest-leverage reliability work is to make the existing Evolution Governor decision evidence more explicit and reviewable.

This remains inside the current AI Task Executor MVP and post-v0.1 Execution Reliability phase. It does not change evolution thresholds, automatic evolution behavior, architecture locking behavior, rollback behavior, code self-modification rules, or future AI Company System layers.

## Objective

Decide whether to approve architecture boundary definition for a bounded Evolution Decision Evidence Reliability slice.

## Allowed Scope

- Architecture boundary definition only.
- Existing Evolution Governor decision evidence.
- Existing stability-first decision evidence.
- Existing simulation, risk, approval, rollback, and threshold evidence review.
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
- Existing Evolution Governor behavior.
- Existing architecture locking behavior.
- Existing rollback record behavior.
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
- Automatic evolution behavior changes.
- Code self-modification.
- Architecture mutation.
- Unlocking locked modules.
- External services or new model-provider integrations.
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

- Issue: `issues/031_evolution_decision_evidence_reliability_gate.md`
- Objective: Define Evolution Decision Evidence Reliability architecture boundaries before implementation.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing Evolution Governor behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: architecture boundary definition only around existing Evolution Governor decision evidence, stability-first evidence, simulation, risk, approval, rollback, threshold evidence, verification planning, and gap classification.
- Forbid: implementation, new features, UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, automatic evolution behavior changes, code self-modification, architecture mutation, unlocking locked modules, external services, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer scope.
