# Local/Demo Operator Polish Boundaries

Date: 2026-07-06

Owner seat: 系统交付席

Status: verified by 质量运行席; ready for 产品规划席 acceptance.

Source gate: `issues/035_local_demo_operator_polish_gate.md`

Boundary ADR: `docs/decisions/ADR-0013-local-demo-operator-polish-boundaries.md`

Review evidence: `reviews/031_local_demo_operator_polish_boundaries_review.md`

## Objective

Define architecture boundaries and exact scope for Local/Demo Operator Polish and Release Notes before implementation.

## Boundary Decision

Local/Demo Operator Polish is bounded to release clarity, operator wording, and demo-readiness evidence for the existing AI Task Executor MVP v0.1 local/demo release.

No implementation is approved by this boundary issue.

## Allowed Scope

- Architecture boundary definition only.
- Local/demo runbook clarity planning.
- Release-note clarity planning.
- Startup, health check, smoke verification, shutdown, rollback, and known-warning wording.
- Documentation-only first-slice recommendation.
- Bounded Chinese-console wording polish only after separate product acceptance.
- Gap classification for stabilization, documentation, verification, or future product scope.
- Source-of-truth updates.

## Required Preservation

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing execution behavior.
- Existing Evolution Governor behavior.
- Project Memory.
- Role Profiles.
- Role Context.
- Release record/tag semantics.
- Source-of-truth ownership.

## Forbidden Scope

- Backend/frontend implementation.
- New product features.
- Complex UI/dashboard.
- New entry channels.
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
- Mock data or simulation substitution for release/demo evidence.

## Recommended First Slice

`Local/Demo Operator Release Notes Package`

Recommended scope:

- Documentation-only operator-facing release notes.
- Startup, smoke verification, shutdown, rollback, known warning, and evidence-reference sections.
- Summary of implemented v0.1 capability.
- Summary of post-v0.1 reliability improvements.
- No backend/frontend/API/persistence/execution behavior changes.

## Handoff

Handoff: sent to 质量运行席.

Target seat: 质量运行席.

Compact payload:

- Issue: `issues/036_local_demo_operator_polish_boundaries.md`
- Objective: Verify Local/Demo Operator Polish architecture boundaries before product acceptance.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing execution behavior, Evolution Governor behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: architecture boundary definition only for operator runbook clarity, release-note clarity, local/demo verification wording, rollback wording, known-warning wording, and documentation-only first-slice recommendation.
- Forbid: implementation, new features, complex UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, automatic evolution behavior changes, code self-modification, architecture mutation, unlocking locked modules, external services, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, future-layer scope, and mock/simulation substitution.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-06.

Quality evidence: `reviews/031_local_demo_operator_polish_boundaries_review.md`.

Verification results:

- Backend/frontend diff guard passed; no implementation files changed.
- `git diff --check` passed.
- Forbidden-scope scan passed; matches were limited to preserved, forbidden, verification-command, and anti-scope language.
- No blockers found.

Completion handoff:

Handoff: sent to 产品规划席.
