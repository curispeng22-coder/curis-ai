# Local/Demo Verification Automation Boundaries

Date: 2026-07-07

Owner seat: 系统交付席

Status: verified by 质量运行席; ready for 产品规划席 acceptance.

Source gate: `issues/038_local_demo_verification_automation_gate.md`

Boundary ADR: `docs/decisions/ADR-0014-local-demo-verification-automation-boundaries.md`

Review evidence: `reviews/033_local_demo_verification_automation_boundaries_review.md`

## Objective

Define architecture boundaries and exact scope for Local/Demo Verification Automation before implementation.

## Boundary Decision

Local/Demo Verification Automation is bounded to local-only smoke verification support for the existing AI Task Executor MVP v0.1 local/demo release.

No implementation is approved by this boundary issue.

## Allowed Scope

- Architecture boundary definition only.
- Local-only verification helper planning.
- Deterministic smoke checks for `GET /health`, `POST /api/task`, and `GET /api/tasks`.
- Optional command-line arguments for local API base URL and task content.
- Documentation references in operator notes or release runbook.
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

- Backend/frontend behavior changes.
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

`Local/Demo API Smoke Helper`

Recommended scope:

- Repo-local helper script under a non-runtime tooling path.
- Python standard-library HTTP calls.
- Health, task creation, and task history smoke checks against the real local API.
- Documentation reference in operator notes.
- No backend/frontend/API/persistence/execution behavior changes.

## Handoff

Handoff: sent to 质量运行席.

Target seat: 质量运行席.

Compact payload:

- Issue: `issues/039_local_demo_verification_automation_boundaries.md`
- Objective: Verify Local/Demo Verification Automation architecture boundaries before product acceptance.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing execution behavior, Evolution Governor behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: architecture boundary definition only for local-only health/task-create/task-history smoke helper planning, operator-note references, and source-of-truth updates.
- Forbid: backend/frontend behavior changes, new features, complex UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, automatic evolution behavior changes, code self-modification, architecture mutation, unlocking locked modules, external services, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, future-layer scope, and mock/simulation substitution.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-07.

Quality evidence: `reviews/033_local_demo_verification_automation_boundaries_review.md`.

Verification results:

- Backend/frontend diff guard passed; no implementation files changed.
- `git diff --check` passed.
- Forbidden-scope scan passed; matches were limited to preserved, forbidden, verification-command, and anti-scope language.
- No blockers found.

Completion handoff:

Handoff: sent to 产品规划席.
