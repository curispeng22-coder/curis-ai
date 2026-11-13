# Local/Demo Operator Release Notes Package

Date: 2026-07-06

Owner seat: 系统交付席

Status: accepted by 产品规划席.

Source boundary: `docs/decisions/ADR-0013-local-demo-operator-polish-boundaries.md`

Boundary review: `reviews/031_local_demo_operator_polish_boundaries_review.md`

Delivery artifact: `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`

Delivery review: `reviews/032_local_demo_operator_release_notes_package_review.md`

## Objective

Implement the accepted documentation-only first slice for Local/Demo Operator Polish.

## Allowed Scope

- Documentation-only operator release notes.
- Startup, health check, smoke verification, shutdown, rollback, known-warning, and evidence-reference sections.
- Summary of implemented AI Task Executor MVP v0.1 capability.
- Summary of post-v0.1 reliability improvements.
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

- Operator release notes are added or updated in `docs/release/`.
- The document clearly states current implemented capability.
- The document clearly states post-v0.1 reliability improvements.
- Startup, smoke verification, shutdown, rollback, known warning, and evidence references are included.
- No backend/frontend behavior files are changed.
- `git diff --check` passes.
- Source-of-truth files are updated.

## Handoff

Handoff: sent to 系统交付席.

Target seat: 系统交付席.

Compact payload:

- Issue: `issues/037_local_demo_operator_release_notes_package.md`
- Objective: Implement documentation-only Local/Demo Operator Release Notes Package.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing execution behavior, Evolution Governor behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: documentation-only operator release notes with startup, smoke verification, shutdown, rollback, known warning, evidence references, v0.1 capability summary, and post-v0.1 reliability summary.
- Forbid: backend/frontend behavior changes, new features, complex UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, automatic evolution behavior changes, code self-modification, architecture mutation, unlocking locked modules, external services, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, future-layer scope, and mock/simulation substitution.

## Delivery Notes

Status: implemented by 系统交付席 on 2026-07-06.

Delivery artifact: `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`.

Delivery evidence: `reviews/032_local_demo_operator_release_notes_package_review.md`.

Summary:

- Added documentation-only operator notes.
- Covered current v0.1 capability.
- Covered post-v0.1 reliability improvements.
- Covered startup, smoke verification, shutdown, rollback, known warning, and evidence references.
- No backend/frontend behavior files were changed.

Completion handoff:

Handoff: sent to 质量运行席.

## Quality Verification Notes

Status: verified by 质量运行席 on 2026-07-06.

Quality evidence: `reviews/032_local_demo_operator_release_notes_package_review.md`.

Verification results:

- Backend/frontend diff guard passed; no implementation files changed.
- `git diff --check` passed.
- Required operator-note sections are present.
- Forbidden-scope scan passed; matches were limited to preserved, forbidden, verification-command, and anti-scope language.
- No blockers found.

Completion handoff:

Handoff: sent to 产品规划席.

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Acceptance evidence: `reviews/032_local_demo_operator_release_notes_package_review.md`.

Accepted artifact:

- `docs/release/ai-task-executor-mvp-v0.1-operator-notes.md`

Product conclusion:

- Local/demo operator polish first slice is complete.
- Current AI Task Executor MVP v0.1 is easier to operate, demo, verify, and explain.
- No backend/frontend behavior changes, API semantic changes, persistence/schema changes, execution behavior changes, external services, mock/simulation substitution, or future-layer scope were approved.

Completion handoff:

Handoff: sent to main thread closeout.
