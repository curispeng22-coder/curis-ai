# Issue: Evolution Decision Evidence Map

## Owner

系统交付席

## Context

产品规划席 accepted Evolution Decision Evidence Reliability boundaries in `reviews/028_evolution_decision_evidence_reliability_boundaries_review.md`.

Boundary ADR: `docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md`.

This is the first implementation slice for the accepted boundary.

## Objective

Implement the `Evolution Decision Evidence Map` first slice.

## Allowed Scope

- Backend tests for existing stable do-not-evolve evidence.
- Backend tests for existing threshold-triggered controlled proposal, simulation, and rollback evidence.
- Backend tests for existing locked-module postpone evidence.
- API evidence checks for existing decision, simulation, and rollback surfaces.
- Documentation or review evidence needed to prove existing Evolution Governor decision observability.
- Source-of-truth updates after implementation and verification.

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

- API semantic changes.
- Persistence/schema/new table changes.
- UI changes.
- New product features.
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

- Stable do-not-evolve path is covered by backend tests or equivalent deterministic local evidence.
- Threshold-triggered controlled proposal, simulation, and rollback path is covered by backend tests or equivalent deterministic local evidence.
- Locked-module postpone path is covered by backend tests or equivalent deterministic local evidence.
- Evolution-decision API evidence is covered.
- Existing API semantics and persistence schema are preserved.
- Backend regression passes with `cd backend && ./.venv/bin/python -m unittest discover tests`.
- `git diff --check` passes.
- `git diff --name-only HEAD -- frontend` remains empty unless separately approved.
- `git diff --name-only HEAD -- backend/app` remains empty unless a separately approved implementation gap requires production code.
- Scope scan confirms no future-layer or forbidden-scope implementation drift.

## Handoff

Handoff: sent to 系统交付席.

Target seat: 系统交付席.

Compact payload:

- Issue: `issues/033_evolution_decision_evidence_map.md`
- Objective: Implement Evolution Decision Evidence Map first slice.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing Evolution Governor behavior, architecture locking behavior, rollback record behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: backend tests and evidence documentation for existing stable do-not-evolve evidence, threshold-triggered controlled proposal/simulation/rollback evidence, locked-module postpone evidence, and evolution-decision API evidence.
- Forbid: API semantic changes, persistence/schema/new tables, UI changes, new features, new execution behavior, automatic evolution behavior changes, code self-modification, architecture mutation, unlocking locked modules, external services, runtime prompt expansion, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, and future-layer implementation.

## Implementation Notes

Status: implemented by 系统交付席 on 2026-07-06.

Delivery evidence: `reviews/029_evolution_decision_evidence_map_review.md`.

Implementation summary:

- Added backend coverage for stable do-not-evolve evidence map.
- Added backend coverage for threshold-triggered controlled proposal, simulation, and rollback evidence map.
- Added backend coverage for locked-module postpone risk evidence map.
- Extended evolution-decision API evidence coverage for rollback, simulation performance impact, rollback performance comparison, and disabled automatic code modification.
- No backend production files were changed.
- No frontend files were changed.

Verification:

- Focused evolution evidence-map tests passed, 4 tests.
- Backend regression passed with 41 tests.
- `git diff --check` passed.
- Frontend diff guard passed.
- Backend production diff guard passed.
- Scope scan found no forbidden implementation drift.

Completion handoff:

Handoff: sent to 质量运行席.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-06.

Quality evidence: `reviews/029_evolution_decision_evidence_map_review.md`.

Verification results:

- Focused evolution evidence-map tests passed, 4 tests.
- Backend regression passed, 41 tests.
- `git diff --check` passed.
- Frontend diff guard passed; no frontend files changed.
- Backend production diff guard passed; no `backend/app` files changed.
- Forbidden-scope scan passed; matches were limited to issue/review preservation, forbidden-scope, or verification-command text.
- FastAPI Python 3.14 warning remains `defer-known-gap`.

Completion handoff:

Handoff: sent to 产品规划席.

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Acceptance evidence: `reviews/029_evolution_decision_evidence_map_review.md`.

Decision rationale:

- Stable do-not-evolve, threshold-triggered controlled proposal, locked-module postpone, simulation, rollback, and API evidence are now covered.
- Quality verification passed with focused tests and backend regression.
- Backend production code, frontend, API semantics, persistence schema, Evolution Governor behavior, automatic-evolution behavior, code self-modification rules, architecture mutation boundary, and future-layer boundaries remain preserved.

Next product move:

- Open a bounded closeout gate for the post-v0.1 Execution Reliability phase.
