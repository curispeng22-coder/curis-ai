# ADR-0005: Sprint 3 Lightweight Role And Responsibility Architecture Boundaries

## Status

Accepted by 系统交付席 for 质量运行席 verification planning.

## Context

Sprint 3 - Lightweight Role And Responsibility System is approved for architecture boundary definition before implementation. The final product goal is AI Company System, but the current launch scope remains AI Task Executor MVP. Sprint 3 must improve execution focus and reduce repeated prompt/context payload without creating Employee CRUD, company organization, multi-agent routing, or an agent abstraction layer.

The protected loop remains:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Decision

Sprint 3 lightweight roles are deterministic source-controlled execution guidance profiles. They are not employees, agents, departments, organization units, staffing records, or routing nodes.

A role profile may define:

- role intent,
- responsibility boundary,
- allowed context inputs,
- minimal role context payload,
- expected output shape,
- escalation triggers.

The first implementation slice should define role profiles only. Attaching a profile to task execution evidence, task records, prompt building, UI, or backend metadata is deferred unless a separate implementation issue proves the need and remains inside the approved boundary.

## Role Profile Boundary

Allowed role profile shape:

- Stable profile id.
- Human-readable role name.
- Intent statement.
- Responsibility boundary.
- Minimal context references, preferably to Project Memory segments.
- Expected output shape.
- Escalation triggers for product, architecture, quality, security, or user decision needs.
- Source references.

Not allowed:

- Employee record.
- Agent runtime object.
- Worker pool member.
- Department, reporting line, staffing assignment, or company ownership model.
- Autonomous role creation or mutation.
- Role performance score, compensation, ROI, cost, or economy model.

## Responsibility Boundary

Role profiles may clarify what the task should and should not decide.

Allowed escalation triggers:

- Product direction or acceptance ambiguity -> 产品规划席.
- Architecture redesign, module boundary, or implementation scope conflict -> 系统交付席.
- Verification, environment, or regression evidence gap -> 质量运行席.
- Secrets, external services, sensitive data, privacy, or security risk -> 安全边界席.
- Gate decision, sprint advancement, scope conflict, or user business judgment -> 总控决策席 or main thread according to the existing workflow.

Escalation triggers are guidance only. They must not create automatic routing, background agents, or new execution behavior.

## Project Memory Boundary

Role profiles may reference Project Memory to reduce repeated context, but they must not duplicate full project history or override source-of-truth files.

Allowed inputs:

- `knowledge/PROJECT_MEMORY.md`
- `knowledge/CURRENT_CONTEXT.md`
- `knowledge/003_Architecture.md`
- relevant ADRs, issues, and reviews by source reference only.

Project Memory remains a deterministic project-fact read model. Role profiles remain deterministic execution guidance. Neither layer owns product, architecture, quality, or security decisions.

## Execution Boundary

Sprint 3 must not change the Tool System v1.8 loop.

Role context must not:

- trigger tasks or tools,
- select tools,
- route work to multiple agents,
- mutate workflow steps,
- modify task state,
- change learning, meta-development, or evolution-governor behavior,
- apply code changes.

Any future use of role context in prompt building must be separately approved and must prove it reduces repeated context payload without adding execution behavior.

## Persistence Boundary

First implementation should use source-controlled role profiles only.

Backend persistence, new tables, metadata records, or task-role associations are blocked unless a separately approved metadata gap exists. Local documentation artifacts are preferred for the first slice.

## UI Boundary

No role-management dashboard is approved.

The first slice should not add UI. A future read-only display may be considered only if role context can be derived from approved source-controlled profiles or existing execution evidence without persistence changes or complex UI.

## Source-Of-Truth Boundary

Role profiles must not replace:

- `knowledge/`,
- `PROJECT_STATUS.md`,
- `TASKS.md`,
- ADRs,
- issues,
- reviews,
- Project Memory.

Corrections to project facts, sprint status, architecture decisions, issue scope, or review evidence must happen in the owning source first.

## First Implementation Recommendation

The next implementation issue should create a deterministic source-controlled role profile artifact, not a backend model:

- Input: accepted boundaries, Project Memory, and current role workflow.
- Output: compact fixed role profiles with source references and escalation triggers.
- Verification: deterministic output check, source-reference check, forbidden-scope scan, and no backend/frontend implementation changes.

Attaching profiles to execution evidence should wait for a separate issue.

## Verification Planning Boundary

质量运行席 should plan verification around:

- No backend/frontend implementation files changed for the first profile-only slice.
- Role profiles are deterministic and source-controlled.
- Profiles include responsibility boundaries, output expectations, escalation triggers, and source references.
- Profiles do not introduce Employee CRUD, employee expansion, company organization, multi-agent routing, agent abstraction, ROI/economy, role dashboard, new execution behavior, automatic evolution behavior, unapproved persistence, vector DB/embeddings, external role service, or external memory service.
- Future implementation preserves AI Task Executor MVP, Tool System v1.8, accepted Sprint 2 task-console boundary, Project Memory boundary, and source-of-truth ownership.

## Consequences

Positive:

- Sprint 3 can reduce repeated prompts without expanding into Employee or company systems.
- Role boundaries clarify escalation while preserving existing Curis seat ownership.
- First slice can be verified as deterministic documentation before runtime integration.

Trade-offs:

- No task-role persistence or UI selector in the first slice.
- Runtime prompt integration waits until source-controlled profiles are accepted.
