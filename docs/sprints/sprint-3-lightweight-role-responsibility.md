# Sprint 3 - Lightweight Role And Responsibility System

Status: Deprecated

## Status

Product PRD slice drafted by 产品规划席 on 2026-07-06.

Gate status: approved by 总控决策席 on 2026-07-06.

Architecture boundary status: defined by 系统交付席 in `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`; quality planning passed and accepted by 产品规划席.

Implementation status: first slice implemented in `knowledge/ROLE_PROFILES.md`, verified by 质量运行席, and accepted by 产品规划席 on 2026-07-06.

## Product Goal

Introduce a lightweight role and responsibility frame inside the AI Task Executor MVP so tasks can carry clearer execution intent, responsibility boundaries, and review expectations without becoming an Employee CRUD system, company organization system, or multi-agent platform.

Sprint 3 should help the CEO user answer:

- What kind of execution role is this task asking for?
- What responsibility boundary should the execution stay inside?
- What output and review expectation should the role follow?
- When should execution stop and request a product, architecture, quality, or security decision?

## User Story

As the CEO user, I want tasks to carry a simple role and responsibility context so the AI Task Executor can stay focused, avoid scope drift, and produce results that match the task's intent without requiring long repeated prompts.

## Entry Conditions

- Sprint 2 unified task console first slice is implemented, verified, and accepted.
- Project Memory first slice is implemented, verified, and accepted.
- Tool System v1.8 loop remains the active gate.
- Current launch scope remains AI Task Executor MVP.

## Scope

Allowed product scope:

- Define a small fixed set of execution role profiles for the current AI Task Executor.
- Let task execution reference a role profile or responsibility mode only when it reduces prompt/context size.
- Define role boundaries, allowed responsibilities, escalation triggers, and expected output shape.
- Keep role data source-controlled and deterministic at first.
- Use Project Memory and existing source-of-truth files as role context inputs only when needed.
- Surface minimal role/responsibility context in task execution evidence if already supported by existing records or approved read-only metadata.

## Architecture Boundaries

- Sprint 3 must preserve the accepted v1.8 execution loop.
- Sprint 3 may add lightweight role metadata, responsibility boundaries, or deterministic role profiles for task execution guidance.
- Sprint 3 must not add Employee CRUD, employee expansion, company departments, organization charts, multi-agent routing, autonomous role creation, or an agent abstraction layer.
- Sprint 3 must not add new execution behavior unless 系统交付席 documents a required gap and routes back for approval.
- Backend persistence is blocked unless a separately approved read-model or metadata gap exists.
- UI must stay minimal and operational; it is not a role-management dashboard.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Multi-agent system.
- Agent abstraction layer.
- Company organization, departments, reporting lines, or staffing.
- Autonomous role creation.
- Complex UI or role-management dashboard.
- New task execution behavior beyond the accepted v1.8 loop.
- Automatic evolution behavior.
- New persistence tables without a separately approved metadata gap.
- Vector database, embeddings, external role service, or external memory service.

## Product Requirements

### P0 - Fixed Lightweight Role Profiles

- Define a small set of deterministic role profiles for current execution guidance.
- Each profile must include role intent, responsibility boundary, output expectation, and escalation trigger.
- Profiles must be source-controlled and reviewable.

### P0 - Responsibility Boundary

- A task must be able to identify what it should and should not decide.
- If the task needs product direction, architecture redesign, quality acceptance, security approval, or user business judgment, it must stop and escalate to the appropriate seat.
- Role boundaries must reduce repeated prompt text rather than increase context payload.

### P0 - Minimal Role Context Injection

- Execution may receive only the smallest role context needed for the current task.
- Project Memory may be referenced for relevant facts, but role profiles must not duplicate full project history.
- Role context must not override source-of-truth files.

### P1 - Evidence Surface

- Show or store the selected role/responsibility context only if it can be derived from approved metadata or existing execution evidence.
- Do not create a complex role dashboard.

## Acceptance Criteria

- Sprint 3 has a clear product definition and source boundary.
- Role profiles stay deterministic, source-controlled, and minimal.
- Role context reduces repeated prompt/context payload.
- Role boundaries define escalation triggers for product, architecture, quality, security, and user decision needs.
- AI Task Executor MVP scope is preserved.
- No Employee CRUD, employee expansion, company organization, multi-agent behavior, agent abstraction layer, complex UI, ROI, business modules, new execution behavior, automatic evolution behavior, or unapproved persistence enters the implementation.
- Architecture boundaries are defined before any implementation.
- Scope drift scan has no forbidden implementation.

## Open Product Questions

- Resolved by ADR-0005: first implementation should define role profiles only.
- Runtime prompt integration, task evidence attachment, role selection UI, backend metadata, and persistence are deferred unless separately approved.

## Recommended First Slice

Start with deterministic source-controlled role profiles only.

Implemented first slice:

- Source-controlled deterministic role profile file: `knowledge/ROLE_PROFILES.md`.
- No backend persistence.
- No Employee CRUD or company organization.
- No role-management UI.
- Optional read-only display only if existing task evidence can safely reference the selected profile.

## Next Seat

总控决策席 for Sprint 3 closeout and Sprint 4 entry gate decision.
