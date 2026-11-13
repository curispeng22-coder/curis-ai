# Curis Workspace Tool System v1.5

Status: Deprecated

Sprint name: Sprint 0 - AI 公司执行内核

## Goal

Run the minimal execution loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Storage
```

## Scope

Allowed:

- `POST /api/task`
- `POST /api/task/{task_id}/run`
- `GET /api/task/{task_id}`
- `GET /api/tasks`
- `POST /api/tool/register`
- `POST /api/tool/execute`
- `GET /api/tools`
- `GET /api/task/{task_id}/trace`
- `GET /api/task/{task_id}/workflow`
- Task parsing
- Prompt building
- Auto workflow generation, execution learning, autonomous development scoring, tool registration, dynamic step routing, chaining, fallback, trace, and async execution
- OpenAI-backed Codex/GPT/Claude/default tool execution
- Result persistence in SQLite `tasks`, `tools`, `executions`, `tool_traces`, `workflows`, `auto_workflows`, `workflow_traces`, `execution_patterns`, `failure_logs`, `tool_performance`, `workflow_metrics`, `execution_scores`, `development_strategies`, and `system_evolution_log` tables
- Minimal frontend input, run action, result display, and task history

Forbidden:

- ROI system
- Employee CRUD or employee expansion
- Multi-agent system
- Business modules
- UI complexity
- Mock data
- Simulation mode

## Runtime Modules

- `backend/app/main.py`: Task API, run API, status API, task list API
- `backend/app/orchestrator.py`: task orchestration, auto workflow generation, autonomous development loop, learning loop, and stateful workflow execution
- `backend/app/employee.py`: employee coordinator
- `backend/app/tool_registry.py`: tool registration and lookup
- `backend/app/tool_router.py`: task-to-tool selection
- `backend/app/tool_executor.py`: tool dispatch
- `backend/app/prompt_builder.py`: task-to-prompt conversion
- `backend/app/codex_executor.py`: OpenAI API execution
- `backend/app/result_store.py`: SQLite result storage
- `frontend/app/page.js`: minimal task submission UI

## Completion Checklist

- [ ] Task creation, run, status, history, trace, and workflow APIs are available.
- [ ] Auto workflow generation creates ordered step objects with action, purpose, required tool, and expected output.
- [ ] Tool Router selects primary tools and fallback order.
- [ ] Tool Executor supports single execution, chained execution, async execution, and fallback.
- [ ] Orchestrator records task state flow, workflow state, tool traces, workflow traces, execution result, failure logs, tool performance, workflow metrics, execution scores, development strategies, and system evolution logs.
- [ ] SQLite persistence covers all current execution tables.
- [ ] Minimal frontend can submit a task, run it, show status/result, and show task history.
- [ ] Backend tests pass.
- [ ] Frontend lint passes.
- [ ] Frontend build passes.
- [ ] No forbidden scope has entered implementation.

## Next Gate

Sprint 1 - 公司运行可视化 may begin only after this checklist is reviewed by 产品规划席, verified by 质量运行席, and approved by 总控决策席.
