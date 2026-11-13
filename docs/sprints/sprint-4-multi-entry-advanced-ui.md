# Sprint 4 - Multi-Entry And Advanced UI Gate

Status: Deprecated

## Status

Product PRD slice drafted by 产品规划席 on 2026-07-06.

Gate status: approved by 总控决策席 on 2026-07-06.

Architecture boundary status: defined by 系统交付席 in `docs/decisions/ADR-0007-sprint-4-multi-entry-advanced-ui-boundaries.md`; quality planning passed and accepted by 产品规划席.

Implementation status: first slice implemented by 系统交付席 in `frontend/app`, verified by 质量运行席, and accepted by 产品规划席.

Delivery evidence: `reviews/016_sprint_4_multi_entry_ui_first_slice_review.md`.

## Product Goal

Prepare Curis Workspace to expose the AI Task Executor through clearer entry points and a more capable operational UI while preserving the current AI Task Executor MVP and Tool System v1.8 boundaries.

Sprint 4 should improve how the CEO user starts, reviews, and navigates task execution without adding business modules, ROI, Employee CRUD, company organization, multi-agent routing, external channels, or new execution behavior.

## User Story

As the CEO user, I want the workspace to provide clearer ways to start and inspect AI execution tasks so I can move from intent to execution evidence with less repeated context and less screen friction.

## Entry Conditions

- Sprint 3 lightweight role profiles are implemented, verified, and accepted.
- Sprint 3 role-context runtime reference first slice is implemented, verified, and accepted.
- Tool System v1.8 loop remains the active gate.
- Current launch scope remains AI Task Executor MVP.

## Scope To Consider

Allowed product scope for the gate:

- Decide whether Sprint 3 can close.
- Decide whether Sprint 4 may open for architecture boundary definition.
- Define the Sprint 4 UI/product boundary before implementation.
- Preserve the existing task composer, task history, selected task detail, and role-context helper boundaries.
- Explore multiple task-entry surfaces only inside the existing AI Task Executor product shell.
- Improve operational UI clarity only where it supports task creation, task review, execution status, or compact context use.

## Recommended Sprint 4 Boundary

Sprint 4 should start with architecture boundary definition only.

Recommended first boundary focus:

- Multi-entry map for the existing AI Task Executor UI.
- Compact task-entry patterns that reuse existing Task API behavior.
- Selected-task detail navigation and status visibility improvements.
- No runtime behavior change unless a separately approved issue defines the exact gap.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Company organization, departments, reporting lines, staffing, or ownership model.
- Multi-agent routing.
- Agent abstraction layer.
- External entry channels such as browser extension, desktop app, mobile app, WeChat, Slack, email, or third-party platform integrations.
- Complex UI, role dashboard, analytics dashboard, or company dashboard.
- New task execution behavior.
- API semantic changes without a separately approved gap.
- Backend metadata, persistence, new tables, or task-role association.
- Task evidence attachment.
- Runtime prompt integration beyond separately approved role-context helper behavior.
- Automatic evolution behavior.
- Vector database, embeddings, external role service, or external memory service.

## Product Requirements

### P0 - Sprint 3 Closeout Decision

- Confirm Sprint 3 lightweight role and role-context first slices are complete enough to close.
- Preserve all Sprint 3 deferred scope as future gated work.

### P0 - Sprint 4 Entry Gate

- Confirm Sprint 4 can begin as architecture boundary definition only.
- Keep all implementation blocked until architecture boundaries and quality planning are accepted.

### P0 - Minimal Multi-Entry Principle

- Sprint 4 entry points must reuse existing task execution behavior.
- Entry points must reduce friction, not introduce new workflow semantics.
- UI improvements must stay operational and bounded to current AI Task Executor surfaces.

### P1 - Evidence Design

- Define how future implementation will prove no API drift, no execution-loop drift, no hidden persistence, no UI overexpansion, and no future-layer leakage into L5 company organization or L6 economy.

## Acceptance Criteria

- Sprint 3 closeout has a clear gate decision.
- Sprint 4 has a clear product definition and source boundary.
- Sprint 4 remains inside AI Task Executor MVP.
- Sprint 4 begins with architecture boundary definition only.
- No ROI, business modules, Employee CRUD, company organization, multi-agent routing, agent abstraction, external channels, complex UI, new execution behavior, automatic evolution behavior, or unapproved persistence is approved.
- If approved, 系统交付席 receives only architecture boundary definition work.

## Recommended Decision

Approve Sprint 3 closeout and open Sprint 4 architecture boundary definition only.

## Next Seat

Main thread closeout for Sprint 4 multi-entry UI first slice.
