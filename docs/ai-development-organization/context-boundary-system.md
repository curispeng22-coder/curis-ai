# Context Boundary System

## Purpose

This system defines how AI agents load, limit, and hand off context in Curis Workspace. It converts token optimization from guidance into an executable boundary protocol.

## Context Boundary Contract

Each task must operate inside a declared context boundary:

- Phase boundary
- Scope boundary
- File boundary
- Role boundary
- Decision boundary
- Token boundary

## Phase Boundary

The current phase determines what work is allowed.

Sprint 0 Phase 2 allows:

- Operating-system governance for AI development
- Sprint gates and state-machine rules
- Decision authority definitions
- Context and execution protocols
- Execution runtime layer definitions
- Runtime state observation and feedback protocols

Sprint 0 Phase 2 blocks:

- Business feature implementation
- Product UI
- Production schemas
- APIs for business behavior
- External service integrations for product behavior

## File Boundary

Before editing, identify the smallest set of files needed.

Allowed files for this phase:

- `AGENTS.md`
- `README.md`
- `docs/ai-development-organization/`
- `docs/sprints/`
- `docs/standards/`
- `docs/decisions/`
- `plugins/curis-ai-development-organization/` when plugin governance guidance changes

Business source directories must not be created in this phase.

## Role Boundary

The acting role must be explicit when making decisions:

- 总控决策席 decides gates and conflicts.
- 系统交付席 turns approved governance into executable workflow.
- 产品规划席 protects source-of-truth structure.
- 质量运行席 checks evidence and completion criteria.
- 系统交付席 reviews system-level operating model boundaries.

## Decision Boundary

An AI agent may decide:

- Where to place governance documentation
- How to refine approved operating rules
- How to verify documentation and plugin validity
- Whether a request is blocked by the current gate

An AI agent may not decide without approval:

- To start Sprint 1
- To implement business features
- To override a blocking authority
- To introduce production architecture not covered by an ADR or Sprint plan

## Token Boundary

Use context tiers:

| Tier | Load | Use When |
| --- | --- | --- |
| T0 | `AGENTS.md` and current Sprint status | Every task |
| T1 | Relevant organization index and target docs | Governance tasks |
| T2 | Related standards, ADRs, and plugin skill | Cross-system changes |
| T3 | Broad repository search | Only when target files are unknown |

Do not move to a higher tier until the current tier is insufficient.

Runtime token budgets and escalation rules are defined in `token-governance-layer.md`.

## Handoff Boundary

Handoffs must contain only:

- Current phase and gate
- Active task state
- Owner role
- Changed files
- Verification evidence
- Blockers
- Next allowed action

Historical context belongs in documents, not repeated handoff text.
