# Sprint 2 - 统一任务操作台

Status: Deprecated

## Status

Product PRD slice drafted by 产品规划席 on 2026-07-06.

Gate status: approved by 总控决策席 on 2026-07-06.

Architecture boundary status: defined by 系统交付席 in `docs/decisions/ADR-0003-sprint-2-unified-task-console-architecture-boundaries.md`; quality planning passed and accepted by 产品规划席.

Implementation status: first slice implemented by 系统交付席, verified by 质量运行席, and accepted by 产品规划席 on 2026-07-06.

First implementation issue: `issues/009_sprint_2_unified_task_console_first_slice.md`.

## Product Goal

Turn Curis Workspace from a single-task inspection view into a daily task operating console where the CEO user can create, run, inspect, rerun, and review tasks from one minimal workspace.

Sprint 2 should help the user answer:

- What task should I run next?
- Which tasks are pending, running, completed, failed, or blocked?
- Can I create and run a task without leaving the operating console?
- Can I inspect a previous task without losing the current task context?
- What needs review, rerun, or user decision?

## User Story

As the CEO user, I want one unified task console so I can operate the accepted v1.8 execution kernel day to day without switching between task input, history, run control, and execution evidence.

## Entry Conditions

- Sprint 1 CEO-readable visualization polish is implemented, verified, and accepted.
- The user can inspect a task's execution chain without reading raw engineering JSON first.
- Tool System v1.8 loop remains the active gate.

## Scope

Allowed product scope:

- Unified task composer connected to the existing task creation API.
- Compact task history with minimal status grouping or filtering.
- Run action using the existing `POST /api/task/{task_id}/run` behavior.
- Rerun affordance only if it reuses the existing Run API and does not create a new retry engine.
- Selected task detail using the accepted Sprint 1 visualization boundary.
- Review markers for existing execution states such as failed, blocked, learning recorded, or evolution evaluated.
- Basic presentation preferences if they are local UI state only and do not alter execution behavior.

## Architecture Boundaries

- Sprint 2 must preserve the accepted v1.8 execution loop.
- Sprint 2 may compose existing task creation, run, status, history, and trace surfaces into one operating console.
- Sprint 2 must not add new execution behavior, new business behavior, Employee CRUD, ROI, multi-agent behavior, or an agent abstraction layer.
- Backend changes are only allowed when 系统交付席 documents a required gap in existing read APIs and keeps the change read/control compatible with the accepted loop.
- UI must stay operational and minimal; it is not a complex dashboard or company management system.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Multi-agent system.
- Agent abstraction layer.
- Complex dashboard customization.
- Company CRUD.
- New execution behavior beyond the accepted v1.8 loop.
- Automatic evolution behavior.
- New persistence tables unless a required read-model gap is approved through a follow-up issue.

## Product Requirements

### P0 - Unified Task Composer

- Provide a clear place to enter a task.
- Create tasks through the existing Task API.
- Preserve existing run behavior and validation.
- Keep task creation separate from architecture evolution decisions.

### P0 - Task History And Status Focus

- Show recent tasks in a compact list.
- Support minimal status grouping or filtering for pending, running, completed, failed, and blocked states when data exists.
- Keep the selected task visible with enough context to avoid losing the user's place.

### P0 - Run And Inspect Flow

- Let the user run an existing task through the accepted Run API.
- Let the user inspect the selected task using the accepted Sprint 1 detail view.
- Do not introduce a new retry engine; rerun is only an affordance over the existing Run API.

### P0 - Review And Decision Signals

- Surface existing evidence that a task needs attention: failure, blocker, learning recorded, evolution evaluated, postponed evolution, rollback record, or user decision needed.
- Keep signals derived from persisted or returned execution state.
- Do not invent mock task states.

### P1 - Operating Preferences

- Allow small local presentation preferences only if they do not affect execution behavior.
- Examples: remembered selected task, compact/expanded detail preference, or local filter choice.

## Acceptance Criteria

- User can create a task, run it, and inspect the result from one console.
- User can browse recent tasks and select a previous task without losing the console workflow.
- User can identify tasks that need review, rerun, or user decision from existing state.
- Accepted Sprint 1 task detail remains available and readable.
- No ROI, business modules, Employee CRUD, multi-agent behavior, agent abstraction layer, complex UI, or new execution behavior enters the implementation.
- Backend tests remain passing if backend files change.
- Frontend lint/build pass if frontend files change.
- Scope drift scan has no forbidden implementation.

## Open Product Questions

- Whether Sprint 2 first implementation slice should include status filters immediately or start with composer, task history, run action, selected detail, and minimal review signals only.
- Whether local presentation preferences should wait until after the P0 console is stable.

## Recommended First Slice

Build the smallest unified console:

- Existing task composer.
- Compact task history with selected task state.
- Existing run action.
- Accepted Sprint 1 selected task detail.
- Minimal review signals derived from existing task/execution state.

## Next Seat

产品规划席 for next Sprint 2 follow-up or Sprint 3 entry decision.
