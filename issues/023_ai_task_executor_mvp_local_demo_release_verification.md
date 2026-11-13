# Issue: AI Task Executor MVP Local/Demo Release Verification

## Owner

质量运行席

## Context

产品规划席 accepted the release-candidate stabilization/documentation package in `reviews/021_ai_task_executor_mvp_release_candidate_stabilization_docs_review.md`.

The accepted release runbook is `docs/release/ai-task-executor-mvp-v0.1.md`.

This issue verifies the first-version local/demo release candidate. It does not approve implementation changes.

## Objective

Execute first-version local/demo release verification for the current AI Task Executor MVP.

## Verification Scope

- Backend regression.
- Frontend view-model tests.
- Frontend lint.
- Frontend build.
- Backend/frontend implementation diff guard.
- Diff hygiene.
- API smoke for health, task creation, and task history.
- Chinese operation-console guard.
- Forbidden-scope implementation scan.
- Source-of-truth alignment.
- Release-candidate restore point capture.

## Required Commands And Evidence

Backend regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Frontend regression:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
cd frontend && npm run lint
cd frontend && npm run build
```

Diff and scope guards:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "Create Task|Run Task|Task Composer|Task History|Selected Task Detail|No tasks yet|No task selected|Loading task evidence|Task Entry|Choose a starter|Freeform" frontend/app
rg -n "创建|运行|任务|执行|工作流|工具|学习|演进" frontend/app
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|new execution behavior|API semantic|persistence|new table|task-role association|task evidence attachment|automatic evolution|vector database|embedding|external service" backend/app backend/tests frontend/app
```

Local/demo API smoke:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/api/task -H "Content-Type: application/json" -d '{"content":"发布候选本地验证任务"}'
curl -s http://127.0.0.1:8000/api/tasks
```

If local server startup is not available in the quality environment, record the exact blocker and verify all non-server checks. Do not substitute mock data or simulation mode.

## Non-Goals

- New product features.
- Backend/frontend behavior changes.
- API semantic changes.
- Persistence, schema, or new table changes.
- Execution behavior changes.
- External service integration.
- Complex UI/dashboard changes.
- FastAPI warning fix.
- Future-layer scope such as ROI, business modules, Employee CRUD/expansion, company organization, multi-agent routing, or agent abstraction.

## Acceptance Criteria

- Release verification evidence is recorded in `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`.
- Backend regression result is recorded.
- Frontend regression/lint/build result is recorded.
- API smoke result is recorded or exact environment blocker is documented.
- Chinese UI guard result is recorded.
- Forbidden-scope implementation scan result is recorded.
- Restore point commit is recorded.
- FastAPI Python 3.14 warning remains classified as `defer-known-gap` unless separately approved.
- No implementation changes are made by this issue.

## Handoff

Handoff: sent to 质量运行席

Target seat: 质量运行席

Compact payload:

- Issue: `issues/023_ai_task_executor_mvp_local_demo_release_verification.md`
- Objective: Execute first-version local/demo release verification using `docs/release/ai-task-executor-mvp-v0.1.md`.
- Preserve: AI Task Executor MVP, Tool System v1.8, Chinese operation console, Task API `{ content }`, accepted readiness review, accepted release-candidate docs, Project Memory, Role Profiles, Role Context, Sprint 4 frontend-only boundary, and source-of-truth ownership.
- Allow: verification evidence only, backend/frontend regressions, lint/build, API smoke, Chinese UI guard, forbidden-scope scan, source-of-truth alignment check, restore point capture.
- Forbid: implementation changes, mock/simulation substitution, new features, API semantic changes, persistence/schema changes, execution behavior changes, external services, complex UI/dashboard, FastAPI warning fix, ROI/business/Employee/company/multi-agent/agent-abstraction/future-layer scope.

## Verification Notes

Status: verified by 质量运行席 on 2026-07-06.

Verification evidence: `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`.

Restore point: `c5011acd`.

Result:

- Backend regression, frontend view-model tests, frontend lint, frontend build, diff hygiene, backend/frontend diff guard, Chinese UI guard, forbidden-scope scan, source-of-truth alignment, and API smoke passed.
- API smoke used the real local FastAPI app with SQLite storage at `/private/tmp/curis_release_smoke.sqlite`.
- FastAPI Python 3.14 warning remains `defer-known-gap`.
- No implementation changes were made.

Completion handoff:

Handoff: sent to 产品规划席

## Product Acceptance Notes

Status: accepted by 产品规划席 on 2026-07-06.

Decision:

- First-version local/demo release candidate verification is accepted.
- Restore point `c5011acd` is accepted as the verified release-candidate point.
- Real local FastAPI smoke passed for health, task creation, and task history.
- FastAPI Python 3.14 warning remains classified as `defer-known-gap`.
- No implementation change, mock/simulation substitution, new feature, API semantic change, persistence/schema change, execution behavior change, external service, complex UI/dashboard, FastAPI warning fix, or future-layer scope is approved by this acceptance.

Next step:

- Close the first-version local/demo release candidate and decide whether to create the v0.1 release record/tag.
