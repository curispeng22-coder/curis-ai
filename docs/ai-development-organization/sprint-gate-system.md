# Sprint Gate System

## Purpose

This system defines the gates that control movement from organization setup into planning, implementation, and release.

## Gate Types

- Phase gate: controls movement between Sprint 0 phases.
- Sprint gate: controls movement between Sprints.
- Implementation gate: controls when code work can begin.
- Release gate: controls release or delivery readiness.
- Exception gate: controls rare overrides.

## Current Gate

Current gate: Sprint 1A - Meta Development System.

Sprint 1A gate: Open only for Curis Workspace Tool System v1.6.

Business-code gate: Open only for the current Tool System v1.6 meta-development loop.

## Gate Table

| Gate | Opens When | Approver | Current Status |
| --- | --- | --- | --- |
| Sprint 0 Phase 1 complete | Static organization docs are reviewable | 总控决策席 | Review received |
| Sprint 0 Phase 1.5 complete | Missing operating systems are reviewable and verified | 总控决策席 | Review received |
| Sprint 0 Phase 2 complete | Execution runtime layer is reviewable and verified | 总控决策席 | Review received |
| Sprint 0 Phase 3 complete | Bootstrap runtime layer is reviewable and verified | 总控决策席 | Review received |
| Sprint 0 organization approved | Review checklist is approved | 总控决策席 | Approved |
| Sprint 0 implementation | Sprint 0 plan, acceptance criteria, and test plan are approved | 总控决策席 and 系统交付席 | Closed |
| Sprint 1A implementation | v1.6 Meta Development System is approved | 总控决策席 and 系统交付席 | Open for Tool System v1.6 |
| Sprint 1 planning | Sprint 1A completion checklist is accepted | 总控决策席 | Paused |
| Sprint 1 implementation | Sprint 1 plan, acceptance criteria, and test plan are approved | 总控决策席 and 系统交付席 | Closed |
| Release readiness | Sprint verification and review are complete | 总控决策席, 质量运行席, 安全边界席 when applicable | Closed |

## Gate Checks

Before work starts, check:

- Is the current system state compatible with the task?
- Is the task scope allowed by the current gate?
- Is the owner role authorized?
- Are file boundaries clear?
- Is verification defined?

If any answer is no, the task is blocked.

## Phase 1.5 Exit Criteria

Sprint 0 Phase 1.5 exits when these systems exist and are reviewable:

- Task Execution System
- Context Boundary System
- Decision Authority Matrix
- System State Machine
- Sprint Gate System

Required verification:

- Documents exist in `docs/ai-development-organization/`.
- Organization index links all systems.
- Sprint review checklist includes Phase 1.5 systems.
- Plugin governance skill references all systems.
- No business code has been added.

## MVP Scope Rule

MVP implementation is open only for:

- Task API
- Run API
- Status API
- History API
- Execution trace API
- Workflow API
- Orchestrator
- AI Employee coordinator
- Tool Registry
- Tool Router
- Tool Executor
- Tool chaining
- Async tool execution
- Tool fallback
- Auto Workflow Generator
- Execution Learning Core
- Autonomous Development Loop
- Stateful workflow execution
- Codex Executor
- Prompt Builder
- Result Store
- SQLite persistence
- Minimal Next.js frontend for task input, run action, result display, and task history
- FastAPI backend

ROI system, Employee CRUD or employee expansion, multi-agent system, business modules, UI complexity, mock data, simulation mode, advanced agent systems, multi-company systems, new AI Development OS architecture, and complex business automation remain closed.

## Exception Rules

Exceptions require:

- 总控决策席 approval
- Reason
- Risk
- Time limit
- Rollback or correction path
- Record in an ADR or Sprint review file

Business-code exceptions outside the MVP minimal working loop are not allowed.
