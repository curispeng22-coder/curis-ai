# Local/Demo API Smoke Helper

Date: 2026-07-07

Owner seat: 系统交付席

Status: accepted by 产品规划席.

Source boundary: `docs/decisions/ADR-0014-local-demo-verification-automation-boundaries.md`

Boundary review: `reviews/033_local_demo_verification_automation_boundaries_review.md`

Helper artifact: `tools/local_demo_api_smoke.py`

Delivery review: `reviews/034_local_demo_api_smoke_helper_review.md`

## Objective

Implement the accepted local-only smoke helper for AI Task Executor MVP v0.1 local/demo verification.

## Allowed Scope

- Repo-local helper script under a non-runtime tooling path.
- Python standard-library HTTP calls only.
- Health check against `GET /health`.
- Task creation check against `POST /api/task` with existing `{ content }` payload.
- Task history check against `GET /api/tasks`.
- Optional CLI arguments for local API base URL and task content.
- Operator notes reference to the helper.
- Source-of-truth updates after implementation.

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

## Acceptance Criteria

- Helper script is added under a non-runtime tooling path.
- Helper uses Python standard-library HTTP calls.
- Helper checks health, task creation, and task history against a real local API.
- Helper exits non-zero on failed checks.
- Operator notes reference the helper while preserving manual smoke commands.
- No backend/frontend behavior files are changed.
- `git diff --check` passes.
- Source-of-truth files are updated.

## Handoff

Handoff: sent to 系统交付席.

Target seat: 系统交付席.

Compact payload:

- Issue: `issues/040_local_demo_api_smoke_helper.md`
- Objective: Implement local-only Local/Demo API Smoke Helper.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing execution behavior, Evolution Governor behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: local helper under non-runtime tooling path, Python standard-library HTTP calls, existing health/task-create/task-history smoke checks, CLI base URL/task content options, operator-note reference, and source-of-truth updates.
- Forbid: backend/frontend behavior changes, new features, complex UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, automatic evolution behavior changes, code self-modification, architecture mutation, unlocking locked modules, external services, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, future-layer scope, and mock/simulation substitution.

## Delivery Notes

Status: implemented by 系统交付席 on 2026-07-07.

Helper artifact: `tools/local_demo_api_smoke.py`.

Documentation update: `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`.

Delivery evidence: `reviews/034_local_demo_api_smoke_helper_review.md`.

Summary:

- Added local-only API smoke helper.
- Helper uses Python standard-library HTTP calls.
- Helper checks health, task creation, and task history against the existing local API.
- Operator notes now reference the helper and keep manual smoke commands.
- No backend/frontend behavior files were changed.

Completion handoff:

Handoff: sent to 质量运行席.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-07.

Quality evidence: `reviews/034_local_demo_api_smoke_helper_review.md`.

Verification results:

- Real local FastAPI smoke passed for health, task creation, and task history.
- Helper compilation passed.
- `git diff --check` passed.
- Backend/frontend diff guard passed; no implementation files changed.
- No mock data or simulation substitution was used.
- No blockers found.

Completion handoff:

Handoff: sent to 产品规划席.

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-07.

Acceptance evidence: `reviews/034_local_demo_api_smoke_helper_review.md`.

Accepted artifact:

- `tools/local_demo_api_smoke.py`

Product conclusion:

- Local/Demo Verification Automation first slice is complete.
- The current MVP can now be locally smoke-verified with a repeatable helper.
- No backend/frontend behavior changes, API semantic changes, persistence/schema changes, execution behavior changes, external services, mock/simulation substitution, or future-layer scope were approved.

Completion handoff:

Handoff: sent to main thread closeout.
