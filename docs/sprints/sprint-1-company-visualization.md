# Sprint 1 - 公司运行可视化

Status: Deprecated

## Status

Product PRD slice drafted by 产品规划席 on 2026-07-06.

Gate status: approved by 总控决策席 on 2026-07-06 for architecture boundary definition.

Architecture boundary status: defined by 系统交付席 in `docs/decisions/ADR-0002-sprint-1-company-visualization-architecture-boundaries.md`.

Verification planning status: accepted by 产品规划席 on 2026-07-06.

First implementation slice: compact task list plus selected task detail.

First slice product acceptance: accepted by 产品规划席 on 2026-07-06.

First slice implementation status: completed by 系统交付席, verified by 质量运行席, and accepted by 产品规划席.

CEO-readable visualization polish status: implemented by 系统交付席, verified by 质量运行席, and accepted by 产品规划席 on 2026-07-06.

Next product step: Sprint 2 unified task console gate is opened by 产品规划席.

## Product Goal

Make the accepted v1.8 execution kernel visible and understandable to the user without expanding into business modules, Employee CRUD, ROI, or complex UI.

Sprint 1 should help the user answer:

- What task is running?
- Which workflow steps were generated?
- Which tool was selected or used as fallback?
- What result, trace, failure, learning, meta-development, and evolution decision were recorded?
- Where is the system stable, blocked, or waiting for user decision?

## User Story

As the CEO user, I want to see a task's execution lifecycle in one place so I can understand what Curis Workspace did, why it did it, what it learned, and whether the controlled evolution layer decided to evolve, not evolve, postpone, or rollback.

## Scope

Allowed product scope:

- Task execution status overview.
- Workflow step timeline.
- Tool routing and fallback visibility.
- Result, trace, failure, and learning evidence display.
- Meta-development report visibility.
- Evolution decision visibility.
- Compact AI Employee runtime step visibility.
- Minimal company operating status labels derived from existing execution state.

## Architecture Boundaries

- Sprint 1 visualization must read from accepted v1.8 execution records.
- Existing task creation and run actions may remain available, but visualization must not add new execution behavior.
- The first implementation slice should use compact task history plus selected task detail.
- Backend additions are limited to read-only aggregation over existing task, workflow, trace, learning, meta-development, and evolution records.
- New persistence is not part of Sprint 1 unless a read-model gap is documented and approved through a follow-up issue.
- UI labels must be derived from persisted execution state.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Multi-agent system.
- Agent abstraction layer.
- Complex UI or advanced dashboard customization.
- Company CRUD.
- New execution behavior beyond the accepted v1.8 loop.
- Automatic architecture changes.

## Product Requirements

### P0 - Execution Overview

- Show task status, created time, last run status, and final result.
- Show the current v1.8 loop as execution state, not as marketing copy.
- Keep the first screen focused on current task execution, not landing-page content.

### P0 - Workflow Timeline

- Show generated workflow steps in execution order.
- For each step, show action, purpose, required tool, status, and expected output.
- Preserve compact AI Employee workflow visibility: current step context, output, trace, blocker, and next step.

### P0 - Tool Routing Evidence

- Show selected tool and fallback events when available.
- Show tool trace status, latency/cost fields if already persisted, and errors.
- Do not introduce new cost or ROI calculations.

### P0 - Result And Learning Evidence

- Show execution result.
- Show failure log when present.
- Show learning outputs already recorded by Execution Learning Core.
- Show meta-development report if one exists.

### P0 - Evolution Decision Evidence

- Show evolution decision state: `evolve`, `do_not_evolve`, `postpone_evolution`, or `rollback_previous_evolution`.
- Show policy order: `STABILITY > OPTIMIZATION > EVOLUTION`.
- Show threshold evaluation, simulation summary, risk analysis, and rollback record when available.
- Make clear that proposals are records only and do not apply code automatically.

### P1 - Operating Status Labels

- Add minimal labels such as `Running`, `Completed`, `Failed`, `Blocked`, `Learning Recorded`, `Evolution Evaluated`.
- Labels must be derived from persisted execution state.
- Labels must not create a company/department/employee management feature.

## Acceptance Criteria

- User can inspect a completed task from status through result.
- User can see workflow steps and tool traces without reading raw JSON first.
- User can see whether fallback happened.
- User can see meta-development and evolution decision evidence for tasks that have it.
- User can distinguish execution status, learning status, and evolution status.
- UI remains minimal and does not add business modules, ROI, Employee CRUD, multi-agent behavior, or complex dashboard configuration.
- Backend tests remain passing.
- Frontend lint/build pass if frontend files are changed.
- Scope drift scan has no forbidden implementation.

## Open Product Questions

- First slice is accepted as compact task list plus selected task detail.
- Next polish should make execution overview, workflow timeline, tool evidence, result/learning evidence, and evolution decision evidence readable before raw detail inspection.

## Next Seat

Sprint 1 closed for current accepted scope. Sprint 2 gate moves to 总控决策席.
