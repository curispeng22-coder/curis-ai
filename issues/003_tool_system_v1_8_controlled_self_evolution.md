# Issue: Tool System v1.8 Controlled Self-Evolution Kernel

## Owner

系统交付席

## Context

Current gate: Curis Workspace Tool System v1.8.

Minimal context:

- `AGENTS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/003_Architecture.md`
- `docs/product/prd.md`
- `docs/sprints/tool-system-v1.8-controlled-self-evolution.md`

Protected loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Scope

Implement controlled self-evolution after the v1.6 meta-development step.

Allowed implementation areas:

- Evolution Control Governor.
- Stability-first policy evaluation.
- Architecture locking records and checks.
- Controlled self-rewrite proposal records.
- Simulation records.
- Risk analysis records.
- Evolution decision records.
- Rollback records.
- API endpoint to retrieve evolution decisions for a task.
- Backend tests proving v1.8 behavior.
- Minimal documentation updates if implementation changes the active source of truth.

## Non-Goals

- Do not build UI changes.
- Do not build ROI.
- Do not build business modules.
- Do not build an agent abstraction layer.
- Do not build Employee CRUD or employee expansion.
- Do not build a multi-agent system.
- Do not add mock data or simulation mode.
- Do not allow uncontrolled architecture changes.
- Do not apply code changes automatically from evolution proposals.

## Allowed Files

- `backend/app/**`
- `backend/tests/**`
- `docs/sprints/tool-system-v1.8-controlled-self-evolution.md`
- `knowledge/003_Architecture.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `reviews/003_tool_system_v1_8_controlled_self_evolution_review.md`

## Acceptance Criteria

- [x] After task execution, the system creates an evolution decision record.
- [x] Evolution decision applies `STABILITY > OPTIMIZATION > EVOLUTION`.
- [x] Evolution decision can be `do_not_evolve` when thresholds are not met.
- [x] Evolution decision can be `postpone_evolution` when risk is too high.
- [x] Evolution proposal is generated only when thresholds are met.
- [x] Locked modules cannot be automatically modified.
- [x] Simulation record includes task flow, tool routing, workflow graph, and performance impact.
- [x] Risk analysis includes stability, regression, locked-module, and rollback risks.
- [x] Rollback record includes previous architecture, stable version, and performance comparison.
- [x] API can retrieve evolution decision records by task id.
- [x] Backend tests cover safe rejection, proposal generation, locked module blocking, and API retrieval.
- [x] No forbidden scope enters implementation.

## Verification

Backend:

```bash
cd backend
.venv/bin/python -m unittest discover -s tests
```

Scope drift search:

```bash
rg -n "ROI|business module|agent abstraction|multi-agent|Employee CRUD|mock data|simulation mode|uncontrolled architecture" backend/app backend/tests frontend/app
```

API evidence:

- Create a task.
- Run the task.
- Retrieve task status.
- Retrieve meta development report.
- Retrieve evolution decision record.

## Completion Notes

Implemented by 系统交付席 on 2026-07-06.

Evidence: `reviews/003_tool_system_v1_8_controlled_self_evolution_review.md`.

Quality verification: PASS by 质量运行席 on 2026-07-06.

Product acceptance: Accepted by 产品规划席 on 2026-07-06.

Blockers: None.
