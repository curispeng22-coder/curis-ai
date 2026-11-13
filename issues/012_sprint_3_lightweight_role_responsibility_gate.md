# Issue: Sprint 3 Lightweight Role And Responsibility Gate

## Owner

总控决策席

## Context

Sprint 2 unified task console first slice is implemented, verified, and accepted.

Project Memory first slice is implemented, verified, and accepted.

The final product goal remains AI Company System, but the current launch scope remains AI Task Executor MVP.

Sprint 3 product PRD slice is drafted in `docs/sprints/sprint-3-lightweight-role-responsibility.md`.

## Objective

Decide whether Sprint 3 - Lightweight Role And Responsibility System may open for architecture boundary definition by 系统交付席.

## Scope To Approve

- Define a lightweight role and responsibility frame inside the AI Task Executor MVP.
- Keep role profiles deterministic, source-controlled, and minimal.
- Use role profiles to reduce repeated prompt/context payload.
- Define responsibility boundaries and escalation triggers.
- Preserve Tool System v1.8 and the accepted Sprint 2 task-console and Project Memory boundaries.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Multi-agent system.
- Agent abstraction layer.
- Company organization, departments, reporting lines, or staffing.
- Autonomous role creation.
- Complex UI or role-management dashboard.
- New execution behavior beyond the accepted v1.8 loop.
- Automatic evolution behavior.
- New persistence tables without a separately approved metadata gap.
- Vector database, embeddings, external role service, or external memory service.

## Decision Needed

- [x] Approve Sprint 3 gate and route to 系统交付席.
- [ ] Block Sprint 3 gate and list required product changes.
- [ ] Request user decision if scope exceeds AI Task Executor MVP.

## Evidence To Review

- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `knowledge/003_Architecture.md`
- `docs/sprints/sprint-3-lightweight-role-responsibility.md`
- `reviews/010_project_memory_first_slice_review.md`

## Completion Notes

Decision: APPROVED by 总控决策席 on 2026-07-06.

Rationale:

- Sprint 3 is constrained to deterministic lightweight role profiles, responsibility boundaries, escalation triggers, and minimal role context inside the AI Task Executor MVP.
- The PRD preserves Tool System v1.8, the accepted Sprint 2 task-console boundary, the accepted Project Memory boundary, and current source-of-truth ownership.
- The scope supports token/context reduction and execution focus without creating Employee CRUD, company organization, multi-agent routing, or an agent abstraction layer.
- The issue explicitly forbids ROI, business modules, Employee CRUD/expansion, multi-agent system/routing, agent abstraction layer, company organization/departments/reporting lines/staffing, autonomous role creation, complex UI/role dashboard, new execution behavior, automatic evolution behavior, unapproved persistence, vector DB/embeddings, external role service, and external memory service.
- No implementation is approved at this gate; the next step is architecture boundary definition by 系统交付席.

Evidence reviewed:

- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/sprints/sprint-3-lightweight-role-responsibility.md`

Handoff: HANDOFF_REQUIRED

Target seat: 系统交付席

Compact payload:

- Issue: `issues/012_sprint_3_lightweight_role_responsibility_gate.md`
- Objective: Define Sprint 3 lightweight role and responsibility architecture boundaries before implementation.
- Preserve: AI Task Executor MVP, Tool System v1.8 loop, accepted Sprint 2 task-console boundary, accepted Project Memory boundary, and current source-of-truth ownership.
- Allow: deterministic lightweight role profiles, responsibility boundaries, escalation triggers, and minimal role context only when it reduces repeated prompt/context payload.
- Forbid: ROI, business modules, Employee CRUD/expansion, multi-agent system/routing, agent abstraction layer, company organization/departments/reporting lines/staffing, autonomous role creation, complex UI/role dashboard, new execution behavior, automatic evolution behavior, unapproved persistence, vector DB/embeddings, external role service, or external memory service.

Architecture boundary follow-up:

- 系统交付席 defined Sprint 3 lightweight role architecture boundaries in `docs/decisions/ADR-0005-sprint-3-lightweight-role-responsibility-boundaries.md`.
- Boundary evidence is recorded in `reviews/011_sprint_3_lightweight_role_architecture_boundaries_review.md`.
- Handoff: sent to 质量运行席.

Quality planning and product acceptance:

- 质量运行席 verified Sprint 3 lightweight role architecture boundaries against commit `cef5265`.
- Quality planning status: PASS; no blockers.
- 产品规划席 accepted the Sprint 3 lightweight role architecture-boundary verification plan on 2026-07-06.
- First implementation issue opened as `issues/013_sprint_3_role_profiles_first_slice.md`.
