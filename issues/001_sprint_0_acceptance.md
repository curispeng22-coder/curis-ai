# Issue: Sprint 0 Acceptance Verification

## Owner

质量运行席

## Context

Sprint 0 is `AI 公司执行内核`.

Current implementation gate: Curis Workspace Tool System v1.5.

Protected loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Storage
```

Relevant minimal context:

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/003_Architecture.md`
- `docs/sprints/mvp-implementation.md`

## Scope

Verify whether the existing Sprint 0 implementation satisfies the completion checklist.

Allowed verification areas:

- Task API
- Run API
- Status API
- History API
- Trace API
- Workflow API
- Auto workflow generation
- Tool routing
- Tool execution
- Fallback behavior
- Async/chained execution
- Orchestrator state transitions
- Execution learning records
- SQLite persistence
- Minimal frontend task input, run action, result display, and task history

## Non-Goals

- Do not build ROI.
- Do not build Employee CRUD or employee expansion.
- Do not build a multi-agent system.
- Do not build business modules.
- Do not add UI complexity.
- Do not add mock data or simulation mode.
- Do not redesign architecture.
- Do not open Sprint 1.

## Allowed Files

Verification may read:

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/003_Architecture.md`
- `docs/sprints/mvp-implementation.md`
- `backend/app/**`
- `backend/tests/**`
- `frontend/app/**`
- `frontend/package.json`
- `frontend/eslint.config.mjs`

If verification finds gaps, document them in:

- `reviews/001_sprint_0_acceptance_review.md`
- `knowledge/CURRENT_CONTEXT.md`
- `TASKS.md`

Implementation fixes are not part of this issue unless 产品规划席 and 总控决策席 approve a follow-up issue.

## Acceptance Criteria

- [x] Task creation, run, status, history, trace, and workflow APIs are available.
- [x] Auto workflow generation creates ordered step objects with action, purpose, required tool, and expected output.
- [x] Tool Router selects primary tools and fallback order.
- [x] Tool Executor supports single execution, chained execution, async execution, and fallback.
- [x] Orchestrator records task state flow, workflow state, tool traces, workflow traces, execution result, failure logs, tool performance, workflow metrics, execution scores, development strategies, and system evolution logs.
- [x] SQLite persistence covers all current execution tables.
- [x] Minimal frontend can submit a task, run it, show status/result, and show task history.
- [x] Backend tests pass.
- [x] Frontend lint passes.
- [x] Frontend build passes.
- [x] No forbidden scope has entered implementation.

## Verification

Backend:

```bash
cd backend
.venv/bin/python -m unittest discover -s tests
```

Frontend:

```bash
cd frontend
pnpm lint
pnpm build
```

Scope drift search:

```bash
rg -n "ROI|Employee CRUD|multi-agent|business module|mock data|simulation mode" AGENTS.md PROJECT_STATUS.md TASKS.md knowledge docs backend frontend
```

API evidence:

- Verify `POST /api/task`.
- Verify `POST /api/task/{task_id}/run`.
- Verify `GET /api/task/{task_id}`.
- Verify `GET /api/tasks`.
- Verify `GET /api/task/{task_id}/trace`.
- Verify `GET /api/task/{task_id}/workflow`.

## Completion Notes

质量运行席 verification completed on 2026-07-06.

Result: PASS.

Evidence: `reviews/001_sprint_0_acceptance_review.md`.

Blockers: None.

Decision: 总控决策席 approved Sprint 0 closure on 2026-07-06.
