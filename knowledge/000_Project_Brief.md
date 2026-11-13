# Project Brief

## Product

Curis Workspace's final product goal is an AI Company System for solo entrepreneurs.

Current launch scope is AI Task Executor MVP, not the full AI Company System.

The current stage must build the execution framework while preserving compatibility with future L0-L6 layers.

The user acts as CEO. Curis coordinates tasks, workflows, tools, execution results, learning records, and storage.

## Current Sprint

Sprint 1 - 公司运行可视化, pending 总控决策席 gate approval.

## Current Implementation

Curis Workspace Tool System v1.8.

Current loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

AI Employee workflow principle:

- Pass compact step packages.
- Do not repeat full context for every employee step.
- Each step records output, trace, blocker, and next step.
- Orchestrator performs final user-facing closeout.

## Current Scope

Allowed:

- Task API
- Run API
- Status API
- History API
- Trace API
- Workflow API
- Orchestrator
- AI Employee coordinator
- Tool Registry
- Tool Router
- Tool Executor
- Tool fallback
- Auto Workflow Generator
- Execution Learning Core
- Autonomous Development Loop
- Meta Development System
- Development gap analysis
- Internal issue planning
- Verification planning
- Source-of-truth alignment suggestions
- Evolution Control Governor
- Stability-first policy
- Architecture locking
- Controlled self-rewrite proposal
- Simulation and risk analysis
- Rollback records
- SQLite result storage
- Minimal frontend task input, run action, result display, and task history

Forbidden:

- ROI system
- Employee CRUD or employee expansion
- Multi-agent system
- Business modules
- UI complexity
- Mock data or simulation mode
- Uncontrolled architecture changes
- Automatic code self-modification without approval

## Source Of Truth

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/product/prd.md`
- `docs/pmo/current-status.md`
