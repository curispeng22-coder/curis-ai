# AI Task Executor MVP v0.1 Release Record

Date: 2026-07-06

Release status: local/demo first version accepted.

Release type: local/demo only, not hosted production SaaS.

Release candidate runbook: `docs/release/ai-task-executor-mvp-v0.1.md`

Verification evidence: `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`

Release closeout issue: `issues/024_ai_task_executor_mvp_v0_1_release_closeout.md`

## Product Decision

Decision: APPROVED for local/demo v0.1 release record.

产品规划席 accepts the verified AI Task Executor MVP as the first visible local/demo version.

This decision does not approve any new backend behavior, frontend behavior, API semantic change, persistence/schema change, execution behavior change, external service, complex UI/dashboard, FastAPI warning fix, ROI/economy scope, business module, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, or future-layer implementation.

## Verified Restore Point

Release-candidate restore point: `c5011acd`.

Verification summary:

- Backend regression passed.
- Frontend view-model tests passed.
- Frontend lint passed.
- Frontend build passed.
- Backend/frontend implementation diff guard passed.
- Chinese operation-console guard passed.
- Forbidden-scope implementation scan passed.
- API smoke passed against the real local FastAPI app for health, task creation, and task history.
- API smoke used SQLite storage at `/private/tmp/curis_release_smoke.sqlite`.
- No mock data or simulation substitution was used.

Known non-blocker:

- FastAPI Python 3.14 deprecation warning remains `defer-known-gap`.

## Model Gateway Local/Demo RC Addendum

Follow-up local/demo release-candidate package: `docs/release/model-gateway-local-demo-rc.md`

First-version release closeout package: `docs/release/model-gateway-local-demo-first-version-release-record.md`

Source issue: `issues/075_model_gateway_local_demo_release_candidate_gate.md`

Closeout source issue: `issues/076_model_gateway_post_rc_next_phase_gate.md`

Status: local/demo first-version closeout package ready for quality verification.

Scope:

- New API model gateway local/demo path.
- Official model/tool catalog metadata reads.
- UsageEvent model-call meter fields.
- Runtime secret guardrails.
- Tenant model preference backend APIs and Workspace operation-console UI.
- Local E2E evidence for preference read/save/reset and content-only task creation.

This addendum does not change the accepted v0.1 restore point and does not approve hosted production deployment, Admin Platform implementation, billing, ROI, tenant packages, marketplace, secret persistence/display, provider SDK/direct provider calls, New API source/internal database dependency, Task API payload changes, execution-loop changes, or runtime behavior changes.

## Included Product Capability

The local/demo v0.1 version now includes:

- Chinese operation console.
- Task creation through the existing Task API payload `{ content }`.
- Existing run action.
- Task status and history.
- Selected task detail and execution evidence surface.
- Compact unified task console.
- Bounded local task-entry starters that prefill ordinary task content.
- Tool System v1.8 controlled self-evolution kernel guardrails.
- Project Memory deterministic project-fact read model.
- Source-controlled Curis role profiles.
- Minimal read-only role-context helper from explicit profile id.
- Release-candidate runbook, verification commands, local startup guidance, rollback notes, and known-gap triage.

## Deferred Scope

Deferred from v0.1:

- Hosted production deployment.
- External entry channels.
- Runtime model-provider execution smoke beyond existing approved executor configuration.
- FastAPI warning fix.
- Status filters and local presentation preferences.
- Project Memory execution-summary integration.
- Runtime prompt integration beyond the approved helper behavior.
- Task evidence attachment.
- Role selector and task-role association.
- New backend metadata, persistence, or tables.
- L5 company organization.
- L6 economy/ROI.
- Business modules.
- Employee CRUD/expansion.
- Multi-agent routing or agent abstraction.
- Automatic evolution behavior changes.

## Tag Decision

Decision: create local release tag `v0.1` after this release record is committed.

Tag meaning:

- `v0.1` identifies the source-controlled local/demo first-version release record.
- The verified code restore point remains `c5011acd`.
- The tag does not imply hosted production deployment.

## Rollback

Rollback baseline:

- Use `c5011acd` as the verified code restore point.
- Use this release record and `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md` as release evidence.

Rollback process must follow the non-destructive project-approved git workflow. Do not use destructive git commands unless explicitly approved by the user or 总控决策席.
