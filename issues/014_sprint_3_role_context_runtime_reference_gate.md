# Issue: Sprint 3 Role Context Runtime Reference Gate

## Owner

总控决策席

## Context

Sprint 3 role profiles first slice is implemented, verified, and accepted.

Role profiles are defined in `knowledge/ROLE_PROFILES.md` as deterministic source-controlled guidance.

The final product goal remains AI Company System, but the current launch scope remains AI Task Executor MVP.

This issue does not approve runtime implementation. It only decides whether architecture boundary definition may begin.

## Objective

Decide whether Sprint 3 role-context runtime reference may open for architecture boundary definition by 系统交付席.

## Scope To Approve

- Define architecture boundaries for future minimal runtime role-context reference.
- Preserve role profiles as deterministic source-controlled guidance.
- Preserve Tool System v1.8 and accepted Sprint 2 task-console, Project Memory, and role-profile boundaries.
- Decide what future evidence would be required before runtime prompt integration can be implemented.

## Non-Goals

- ROI system.
- Business modules.
- Employee CRUD or employee expansion.
- Multi-agent system or routing.
- Agent abstraction layer.
- Company organization, departments, reporting lines, staffing, or ownership model.
- Autonomous role creation.
- Role dashboard, role-management UI, or UI selector.
- Runtime implementation.
- Task evidence attachment.
- Backend metadata, persistence, new tables, or task-role association.
- New execution behavior.
- Automatic evolution behavior.
- Vector database, embeddings, external role service, or external memory service.

## Decision Needed

- [x] Approve role-context runtime reference gate and route to 系统交付席.
- [ ] Block the gate and list required product changes.
- [ ] Request user decision if scope exceeds AI Task Executor MVP.

## Evidence To Review

- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/PROJECT_MEMORY.md`
- `knowledge/ROLE_PROFILES.md`
- `docs/sprints/sprint-3-role-context-runtime-reference.md`
- `reviews/012_sprint_3_role_profiles_first_slice_review.md`

## Completion Notes

Decision: APPROVED by 总控决策席 on 2026-07-06.

Rationale:

- This gate approves architecture boundary definition only; runtime implementation remains blocked.
- Role profiles remain deterministic source-controlled guidance in `knowledge/ROLE_PROFILES.md`.
- The scope preserves AI Task Executor MVP, Tool System v1.8, accepted Sprint 2 task-console boundary, accepted Project Memory boundary, accepted Role Profiles boundary, and source-of-truth ownership.
- The issue explicitly forbids runtime implementation, task evidence attachment, UI selector/dashboard, backend metadata/persistence/new tables/task-role association, Employee CRUD/expansion, company organization/departments/reporting lines/staffing, multi-agent routing, agent abstraction, ROI/economy, new execution behavior, automatic evolution behavior, vector DB/embeddings, external role service, and external memory service.
- No implementation is approved at this gate; the next step is architecture boundary definition by 系统交付席.

Evidence reviewed:

- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/sprints/sprint-3-role-context-runtime-reference.md`

Handoff: HANDOFF_REQUIRED

Target seat: 系统交付席

Compact payload:

- Issue: `issues/014_sprint_3_role_context_runtime_reference_gate.md`
- Objective: Define Sprint 3 role-context runtime reference architecture boundaries before implementation.
- Preserve: AI Task Executor MVP, Tool System v1.8 loop, accepted Sprint 2 task-console boundary, accepted Project Memory boundary, accepted Role Profiles boundary, and current source-of-truth ownership.
- Allow: architecture boundary definition for future minimal runtime role-context reference only; role profiles remain deterministic source-controlled guidance.
- Forbid: runtime implementation, task evidence attachment, UI selector/dashboard, backend metadata/persistence/new tables/task-role association, Employee CRUD/expansion, company organization/departments/reporting lines/staffing, multi-agent routing, agent abstraction, ROI/economy, new execution behavior, automatic evolution behavior, vector DB/embeddings, external role service, or external memory service.

Architecture boundary follow-up:

- 系统交付席 defined role-context runtime reference architecture boundaries in `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`.
- Boundary evidence is recorded in `reviews/013_role_context_runtime_reference_architecture_boundaries_review.md`.
- Handoff: sent to 质量运行席.

Quality and product acceptance follow-up:

- 质量运行席 verified role-context runtime reference architecture boundaries against commit `c72e86dd`.
- Quality planning status: PASS; no blockers were found by 质量运行席.
- 产品规划席 accepted the architecture-boundary verification plan on 2026-07-06.
- First implementation issue opened as `issues/015_sprint_3_role_context_runtime_reference_first_slice.md`.
