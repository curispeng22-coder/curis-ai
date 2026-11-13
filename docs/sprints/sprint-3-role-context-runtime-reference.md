# Sprint 3 Follow-up - Role Context Runtime Reference

Status: Deprecated

## Status

Product PRD slice drafted by 产品规划席 on 2026-07-06.

Gate status: approved by 总控决策席 on 2026-07-06.

Architecture boundary status: defined by 系统交付席 in `docs/decisions/ADR-0006-role-context-runtime-reference-boundaries.md`; quality planning passed and accepted by 产品规划席.

Implementation status: first slice implemented, verified, and accepted on 2026-07-06.

## Product Goal

Evaluate whether Curis Workspace should allow the AI Task Executor to reference accepted role profiles during task execution while preserving the current Tool System v1.8 loop and avoiding any expansion into Employee CRUD, multi-agent routing, company organization, role UI, or persistence.

This gate approved architecture boundary definition only. Runtime implementation requires a separate implementation issue with an explicit stable profile id.

## User Story

As the CEO user, I want the AI Task Executor to eventually use compact role context so task execution stays inside the right responsibility boundary without repeating long role prompts.

## Entry Conditions

- Sprint 3 role profiles first slice is implemented, verified, and accepted.
- `knowledge/ROLE_PROFILES.md` defines deterministic source-controlled role profiles.
- Tool System v1.8 loop remains the active gate.
- Current launch scope remains AI Task Executor MVP.

## Scope

Allowed product scope for this gate:

- Decide whether 系统交付席 may define architecture boundaries for minimal runtime role-context reference.
- Preserve role profiles as source-controlled guidance.
- Explore how runtime context could reference a stable role profile without adding new execution behavior.
- Define whether a future first slice should use a fixed default profile, issue-declared profile, or no runtime integration.
- Define evidence needed to prove token reduction and boundary preservation.

## Architecture Boundaries

- This gate may approve architecture boundary definition only.
- Runtime prompt integration remains blocked until a future implementation issue is approved.
- Task evidence attachment remains blocked.
- UI selector, role dashboard, backend metadata, persistence, task-role association, and new tables remain blocked.
- Role context must not select tools, route work, mutate workflow, change task state, trigger tasks, create agents, or alter learning/evolution behavior.
- Role context must reference `knowledge/ROLE_PROFILES.md` and source-of-truth files rather than duplicating project history.

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

## Product Requirements

### P0 - Boundary Decision

- Decide whether role-context runtime reference is eligible for architecture boundary definition.
- Keep all implementation blocked until architecture boundaries and quality planning are accepted.

### P0 - Minimal Context Principle

- Any future runtime reference must be smaller than repeating full role prompts.
- Role context must be derived from `knowledge/ROLE_PROFILES.md`.
- Project Memory may be referenced only for relevant facts, not copied wholesale.

### P0 - Execution Safety

- Role context must not alter the Tool System v1.8 execution loop.
- Role context must not create automatic routing, agent selection, tool selection, or workflow mutation.

### P1 - Future Evidence Design

- Define how a future implementation would prove deterministic profile lookup, context-size reduction, no backend/frontend drift, and no forbidden scope.

## Acceptance Criteria

- Gate has a clear product definition and source boundary.
- Scope remains inside AI Task Executor MVP.
- Runtime implementation remains blocked at this gate.
- Role profiles remain deterministic source-controlled guidance.
- No Employee CRUD, company organization, multi-agent routing, agent abstraction, UI selector, backend persistence, new execution behavior, or automatic evolution behavior is approved.
- If approved, 系统交付席 receives only architecture boundary definition work.

## Recommended Decision

Approve architecture boundary definition only.

Recommended boundary focus:

- How role profiles can be referenced by future runtime context without adding execution behavior.
- ADR-0006 decision: any future first runtime slice should require an explicit issue-declared profile id; it should not use an implicit default profile.
- What verification evidence is required before any runtime prompt integration is allowed.

## Product Acceptance

Accepted by 产品规划席 on 2026-07-06.

Accepted first implementation direction:

- Minimal read-only role-context reference.
- Explicit issue-declared profile id only.
- No implicit default role.
- No role selection, routing, persistence, UI, task evidence attachment, Employee expansion, company organization, or execution behavior change.

## First Slice Acceptance

Accepted by 产品规划席 on 2026-07-06.

Accepted implementation:

- `backend/app/role_context.py` provides deterministic read-only role-profile lookup and compact excerpt generation.
- `backend/tests/test_role_context.py` verifies explicit profile lookup and missing/invalid profile fallback.
- Runtime prompt integration, task evidence attachment, UI selector/dashboard, backend metadata, persistence, task-role association, and API semantic changes remain deferred.
- Any future runtime caller must be constrained by a separately approved issue-declared profile id.

## Next Seat

总控决策席 for Sprint 3 closeout and Sprint 4 entry gate decision.
