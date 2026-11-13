# AI Task Executor MVP v0.1 Release Candidate

Date: 2026-07-06

Scope: local/demo release-candidate package for the current AI Task Executor MVP.

Source issue: `issues/022_ai_task_executor_mvp_release_candidate_stabilization_docs.md`

Release record: `docs/release/ai-task-executor-mvp-v0.1-release-record.md`

Boundary evidence:

- `docs/decisions/ADR-0009-ai-task-executor-mvp-release-candidate-boundaries.md`
- `reviews/020_ai_task_executor_mvp_release_candidate_boundaries_review.md`

## Release Boundary

This package is documentation-only. It does not change backend behavior, frontend behavior, API semantics, persistence, execution behavior, UI behavior, external services, or future-layer scope.

Preserved release baseline:

- Chinese operation console.
- Task API payload shape `{ content }`.
- Tool System v1.8 loop.
- Accepted MVP readiness review with no blocker gaps.
- Project Memory, Role Profiles, Role Context, and Sprint 4 frontend-only boundaries.
- Source-of-truth ownership in `knowledge/`, `PROJECT_STATUS.md`, `TASKS.md`, issues, reviews, sprint docs, and ADRs.

## RC-PLAN Coverage

| ID | Status | Release artifact coverage |
| --- | --- | --- |
| RC-PLAN-001 | Covered | Canonical verification commands below. |
| RC-PLAN-002 | Covered | Local startup instructions below. |
| RC-PLAN-003 | Covered | Local/demo deployment instructions below. |
| RC-PLAN-004 | Covered | First-version release checklist below. |
| RC-PLAN-005 | Covered | Rollback notes below. |
| RC-PLAN-006 | Covered | FastAPI warning triage decision below. |

## Canonical Verification Commands

Run commands from the repository root unless a command starts with `cd`.

Backend regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

System Python is not the canonical backend test interpreter. The system `python3` command is unsupported for release-candidate verification unless dependencies are explicitly prepared for that interpreter.

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

Expected guard results:

- Backend and frontend regression commands pass.
- `git diff --name-only HEAD -- backend frontend` is empty for documentation-only release-candidate work.
- Old visible-console English labels do not reappear.
- Chinese operation-console labels remain present.
- Forbidden-scope scan has no implementation-path matches.

## Local Startup Instructions

Backend working directory:

```bash
cd backend
```

Install backend dependencies if the virtualenv is missing or stale:

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install -r requirements.txt
```

Start backend locally:

```bash
CURIS_DB=data/curis.sqlite ./.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Expected backend URL:

```text
http://127.0.0.1:8000
```

Frontend working directory:

```bash
cd frontend
```

Start frontend locally:

```bash
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000 npm run dev -- --hostname 127.0.0.1 --port 3000
```

Expected frontend URL:

```text
http://127.0.0.1:3000
```

Local configuration guidance:

- `CURIS_DB` may point to a local SQLite file. Default backend runtime path is `data/curis.sqlite`.
- `CURIS_ALLOWED_ORIGINS` defaults to `http://localhost:3000,http://127.0.0.1:3000`.
- `NEXT_PUBLIC_API_BASE` should point the frontend to the backend URL.
- Do not commit secrets.
- No external service is required for health, task creation, task status, or task history smoke checks.

## Local/Demo Deployment Instructions

The local/demo deployment uses the existing backend and frontend only.

1. Run canonical backend regression.
2. Run canonical frontend regression, lint, and build.
3. Start backend at `http://127.0.0.1:8000`.
4. Start frontend at `http://127.0.0.1:3000`.
5. Open the frontend and confirm the operation console is Chinese.
6. Create a local task using ordinary task content.
7. Confirm task history updates.
8. Select the task and confirm selected-task detail opens.
9. Run no-external API smoke commands below.

No-external API smoke:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/api/task -H "Content-Type: application/json" -d '{"content":"发布候选本地验证任务"}'
curl -s http://127.0.0.1:8000/api/tasks
```

The run endpoint may require the existing executor environment to have a valid `OPENAI_API_KEY`. Do not add or use new external services for this release-candidate package. Runtime execution smoke that uses an external model provider requires the existing approved executor configuration and should be treated as a separate quality verification step, not a new integration.

## First-Version Release Checklist

Before first-version local/demo release verification, 质量运行席 should confirm:

- Backend regression passed with `cd backend && ./.venv/bin/python -m unittest discover tests`.
- Frontend view-model tests passed.
- Frontend lint passed.
- Frontend build passed.
- API smoke passed for health, task creation, and task history.
- Chinese operation-console labels remain visible.
- Old visible-console English labels did not reappear.
- Source-of-truth files are aligned:
  - `PROJECT_STATUS.md`
  - `TASKS.md`
  - `knowledge/CURRENT_CONTEXT.md`
  - `knowledge/PROJECT_MEMORY.md`
  - current issue and review files
- Forbidden-scope scan over `backend/app`, `backend/tests`, and `frontend/app` has no implementation-path matches.
- No backend/frontend implementation diff is present unless a separately approved stabilization issue exists.
- Release-candidate commit or restore point is recorded.

## Rollback Notes

Use source control as the release-candidate restore point.

Before release-candidate verification:

1. Record the current commit hash.
2. Ensure working tree changes are either committed or intentionally left out of scope.
3. Keep untracked local files out of release evidence unless separately approved.

Rollback process:

1. Stop local backend and frontend processes.
2. Return to the recorded release-candidate commit or branch state using the project-approved git workflow.
3. Re-run backend regression and frontend regression after rollback.
4. Re-run API smoke for health, task creation, and task history.
5. Record rollback evidence in a review file if rollback was exercised.

Do not use destructive git commands unless explicitly approved by the user or 总控决策席.

## FastAPI Warning Triage

Decision: `defer-known-gap`.

Evidence:

- Backend regression passes with 34 tests.
- FastAPI emits a Python 3.14 deprecation warning during tests.
- The warning is already tracked as a known issue.

Release-candidate impact:

- Not a blocker for local/demo release-candidate verification.
- Do not fix the warning in this documentation package.
- If the warning becomes release-blocking, open a separate stabilization issue and verify backend regression remains PASS after the fix.

## Deferred Scope

These items remain outside release-candidate documentation implementation:

- Sprint 2 status filters and local presentation preferences.
- Project Memory execution-summary memory.
- Runtime prompt integration.
- Task evidence attachment.
- Role selector.
- Backend metadata, persistence, new tables, and task-role association.
- Broader task-entry expansion.
- New product features, external channels/services, ROI, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, automatic evolution behavior changes, vector DB/embeddings, and future-layer scope.
