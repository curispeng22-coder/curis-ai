# Issue: Evolution Decision Evidence Reliability Boundaries

## Owner

系统交付席

## Context

总控决策席 approved the Evolution Decision Evidence Reliability gate in `issues/031_evolution_decision_evidence_reliability_gate.md`.

This issue defines architecture boundaries only. It does not approve implementation.

Boundary ADR: `docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md`.

## Objective

Define Evolution Decision Evidence Reliability architecture boundaries before implementation.

## Allowed Scope

- Architecture boundary definition only.
- Evidence map for existing Evolution Governor decision behavior.
- Evidence map for existing stability-first behavior.
- Existing threshold, proposal, simulation, risk, approval, rollback, and API evidence review.
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

- ADR is created under `docs/decisions/`.
- Review/evidence file is created under `reviews/`.
- First implementation recommendation is bounded to backend tests and evidence documentation only.
- No backend/frontend implementation files are changed.
- `PROJECT_STATUS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` route the next step to 质量运行席.

## Boundary Summary

Defined in `docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md`.

Recommended first implementation slice: `Evolution Decision Evidence Map`.

## Handoff

Handoff: sent to 质量运行席.

Target seat: 质量运行席.

Compact payload:

- Issue: `issues/032_evolution_decision_evidence_reliability_boundaries.md`
- Objective: Verify Evolution Decision Evidence Reliability architecture boundaries before implementation.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing Evolution Governor behavior, architecture locking behavior, rollback record behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: architecture boundary verification only for existing Evolution Governor decision evidence, stability-first evidence, threshold evaluation, proposal, simulation, risk, approval, rollback, API evidence, verification planning, and gap classification.
- Forbid: implementation, new features, UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, automatic evolution behavior changes, code self-modification, architecture mutation, unlocking locked modules, external services, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer scope.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-06.

Quality evidence: `reviews/028_evolution_decision_evidence_reliability_boundaries_review.md`.

Verification results:

- No backend/frontend implementation diff.
- `git diff --check` passed.
- Forbidden-scope scan passed; matches were limited to preserved/forbidden scope language and verification-command text.

Completion handoff:

Handoff: sent to 产品规划席.

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Acceptance evidence: `reviews/028_evolution_decision_evidence_reliability_boundaries_review.md`.

Accepted first implementation slice: `Evolution Decision Evidence Map`.

Implementation issue: `issues/033_evolution_decision_evidence_map.md`.

Decision rationale:

- Boundary stays inside post-v0.1 Execution Reliability.
- Quality verification passed with no backend/frontend implementation diff.
- First implementation is limited to backend tests and evidence documentation for existing Evolution Governor decision behavior.
