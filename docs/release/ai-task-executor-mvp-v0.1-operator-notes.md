# AI Task Executor MVP v0.1 Operator Notes

Date: 2026-07-06

Scope: local/demo operator notes for the current AI Task Executor MVP.

Source issue: `issues/037_local_demo_operator_release_notes_package.md`

Release record: `docs/release/ai-task-executor-mvp-v0.1-release-record.md`

Release-candidate runbook: `docs/release/ai-task-executor-mvp-v0.1.md`

Post-v0.1 reliability closeout: `reviews/030_post_v0_1_execution_reliability_closeout_review.md`

## Operator Summary

Curis Workspace v0.1 is a local/demo AI Task Executor.

The current product lets an operator:

- Open the Chinese operation console.
- Create a task through the existing Task API payload `{ content }`.
- Use the existing run action.
- View task status and history.
- Inspect selected-task detail and execution evidence.
- Use compact local task-entry starters that prefill ordinary task content.
- Rely on Project Memory, source-controlled role profiles, and the approved read-only role-context helper as project guidance surfaces.

This document is documentation-only. It does not change backend behavior, frontend behavior, API semantics, persistence, execution behavior, UI behavior, external services, or future AI Company System layers.

## Post-v0.1 Reliability Improvements

After v0.1 release closeout, the execution base was strengthened with three accepted reliability slices:

- Run evidence reliability: successful and failed run evidence chains are covered.
- Workflow error/fallback evidence map: primary failure, fallback success, full fallback failure, workflow trace, adaptation log, failure log, and tool performance evidence are covered.
- Evolution decision evidence map: stable do-not-evolve, threshold-triggered controlled proposal, rollback evidence, and locked-module postpone evidence are covered.

These improvements make the existing AI Task Executor easier to verify and explain. They do not add ROI, business modules, Employee CRUD, company organization, multi-agent routing, agent abstraction, complex dashboard UI, external services, new API semantics, persistence changes, or new execution behavior.

## Startup

Backend:

```bash
cd backend
CURIS_DB=data/curis.sqlite ./.venv/bin/python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd frontend
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000 npm run dev -- --hostname 127.0.0.1 --port 3000
```

Expected URLs:

- Backend: `http://127.0.0.1:8000`
- Frontend: `http://127.0.0.1:3000`

No external service is required for health, task creation, task status, or task history smoke checks.

## Smoke Verification

Run backend regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Run no-external API smoke against the local backend:

```bash
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/api/task -H "Content-Type: application/json" -d '{"content":"本地演示验证任务"}'
curl -s http://127.0.0.1:8000/api/tasks
```

Or run the local helper from the repository root:

```bash
python3 tools/local_demo_api_smoke.py --base-url http://127.0.0.1:8000
```

The helper checks the same existing local API surfaces: health, task creation with `{ content }`, and task history. It does not start servers, call external services, run model-provider execution, or change backend/frontend behavior.

Optional frontend checks:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
cd frontend && npm run lint
cd frontend && npm run build
```

For a local/demo walkthrough:

1. Start backend and frontend.
2. Open the frontend URL.
3. Confirm the operation console is Chinese.
4. Create a task with ordinary task content.
5. Confirm task history updates.
6. Select the task and confirm selected-task detail opens.
7. Use the existing run action only when the approved executor environment is configured.

## Shutdown

Stop the local backend and frontend terminal processes with `Ctrl-C`.

Do not delete local SQLite data unless the current verification run explicitly requires a clean database.

## Rollback

Use source control as the restore mechanism.

Release baseline:

- v0.1 verified restore point: `c5011acd`
- v0.1 release record: `docs/release/ai-task-executor-mvp-v0.1-release-record.md`

Rollback process:

1. Stop local backend and frontend processes.
2. Return to the approved restore point or release branch using the project-approved non-destructive git workflow.
3. Re-run backend regression.
4. Re-run no-external API smoke.
5. Record rollback evidence in a review file if rollback was exercised.

Do not use destructive git commands unless explicitly approved by the user or 总控决策席.

## Known Warning

FastAPI emits a Python 3.14 deprecation warning during backend tests.

Decision: `defer-known-gap`.

Operator impact:

- The warning does not block local/demo operation.
- Do not fix the warning inside operator-notes or release-notes work.
- If it becomes release-blocking, open a separate stabilization issue.

## Evidence References

- v0.1 release candidate runbook: `docs/release/ai-task-executor-mvp-v0.1.md`
- v0.1 release record: `docs/release/ai-task-executor-mvp-v0.1-release-record.md`
- v0.1 release verification: `reviews/022_ai_task_executor_mvp_local_demo_release_verification_review.md`
- v0.1 release closeout: `reviews/023_ai_task_executor_mvp_v0_1_release_closeout_review.md`
- Post-v0.1 reliability closeout: `reviews/030_post_v0_1_execution_reliability_closeout_review.md`
- Run evidence reliability: `reviews/025_run_evidence_reliability_first_slice_review.md`
- Workflow fallback/error evidence: `reviews/027_workflow_error_fallback_evidence_map_review.md`
- Evolution decision evidence: `reviews/029_evolution_decision_evidence_map_review.md`

## Still Blocked

- Hosted production deployment.
- External entry channels.
- External services or new model-provider integrations.
- ROI/economy.
- Business modules.
- Employee CRUD/expansion.
- Company organization, departments, reporting lines, or staffing.
- Multi-agent routing.
- Agent abstraction layer.
- Complex dashboard UI.
- API semantic changes.
- Persistence/schema/new table changes.
- New execution behavior.
- Automatic evolution behavior changes.
- Mock data or simulation substitution for release/demo evidence.
