# Issue: Tool System v1.6 Meta Development System

## Owner

系统交付席

## Context

Current gate: Curis Workspace Tool System v1.6.

Minimal context:

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/003_Architecture.md`
- `docs/product/prd.md`
- `docs/sprints/tool-system-v1.6-meta-development.md`

Protected loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Storage
```

## Scope

Implement the v1.6 meta-development layer after the existing development learning step.

Allowed implementation areas:

- Backend meta-development analyzer.
- Internal issue planner.
- Verification planner.
- Source-of-truth advisor.
- SQLite persistence for meta development records.
- API endpoint to retrieve meta development records for a task.
- Backend tests proving the v1.6 behavior.
- Minimal documentation updates if implementation changes the active source of truth.

## Non-Goals

- Do not build ROI.
- Do not build Employee CRUD or employee expansion.
- Do not build a multi-agent system.
- Do not build business modules.
- Do not add UI complexity.
- Do not add mock data or simulation mode.
- Do not resume Sprint 1 company visualization UI.

## Allowed Files

- `backend/app/**`
- `backend/tests/**`
- `docs/sprints/tool-system-v1.6-meta-development.md`
- `knowledge/003_Architecture.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `reviews/002_tool_system_v1_6_meta_development_review.md`

## Acceptance Criteria

- [x] After task execution, the orchestrator creates a meta development report.
- [x] The report includes gap analysis.
- [x] The report includes planned internal issues.
- [x] The report includes verification plan.
- [x] The report includes source-of-truth suggestions.
- [x] Meta development records are persisted in SQLite.
- [x] API can retrieve meta development records by task id.
- [x] Backend tests cover successful meta development generation.
- [x] Backend tests cover persistence and retrieval.
- [x] No forbidden scope enters implementation.

## Verification

Backend:

```bash
cd backend
.venv/bin/python -m unittest discover -s tests
```

Scope drift search:

```bash
rg -n "ROI|Employee CRUD|multi-agent|business module|mock data|simulation mode" backend/app backend/tests frontend/app
```

API evidence:

- Create a task.
- Run the task.
- Retrieve task status.
- Retrieve meta development report for the task.

## Completion Notes

Implemented by 系统交付席 on 2026-07-06.

Evidence: `reviews/002_tool_system_v1_6_meta_development_review.md`.

Blockers: None.
