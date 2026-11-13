# Collaboration Flow

This document defines the Curis Workspace collaboration flow, decision protocol, and escalation path.

## Default Collaboration Flow

1. Clarify scope and owner.
2. Confirm the current phase and gate.
3. Read the relevant governance and module documents.
4. Propose a plan only when the request is not already executable.
5. Make narrowly scoped changes.
6. Verify the change with the strongest practical evidence.
7. Summarize what changed, what was verified, and what remains blocked.

## Sprint 0 Phase 1 Flow

1. 总控决策席 receives organization task.
2. 总控决策席 confirms the task is governance work, not business development.
3. 系统交付席 drafts the required organization artifact.
4. 产品规划席 checks clarity, file placement, and source-of-truth hygiene.
5. 质量运行席 checks whether the artifact has reviewable acceptance criteria.
6. 总控决策席 marks the artifact ready for review or sends it back for revision.

## Work Item Flow

```text
Request
  -> Scope and gate check
  -> Owner assignment
  -> Source-of-truth read
  -> Narrow change
  -> Verification
  -> Review
  -> Gate update
```

The executable lifecycle for this flow is defined in `task-execution-system.md`.

The repeated runtime loop for agent execution is defined in `agent-execution-loop.md`.

## Handoff Flow

Every handoff must include:

- Current phase
- Scope
- Owner role
- Files changed or expected
- Verification required
- Blockers
- Next allowed action

## Decision Protocol

Decisions must be documented when they affect:

- Repository structure
- System architecture
- Cross-role responsibility
- Coding standards
- Data handling or security posture
- Sprint scope or release gates

Use an ADR in `docs/decisions/` for durable technical or organization decisions.

## Scope Control

Every task must identify one of these scopes:

- Organization governance
- Development standards
- Sprint planning
- Architecture planning
- Business development

Until the Sprint 1 gate opens, business development scope is blocked.

Context boundaries for each scope are defined in `context-boundary-system.md`.

## Review Protocol

Reviewers should check:

- Does this stay inside the approved scope?
- Is ownership clear?
- Are standards updated if behavior changed?
- Is the change small enough to review?
- Is completion backed by evidence?

## Escalation Protocol

Escalate to the 总控决策席 when:

- Two roles disagree on scope or ownership
- A task would cross from governance into business development
- A standard is missing or contradictory
- Verification cannot be completed
- External services, sensitive data, or production access are involved

Decision ownership and blocker authority are defined in `decision-authority-matrix.md`.

Review feedback routing is defined in `system-feedback-loop.md`.

## Communication Protocol

Updates should be concise and evidence-based.

Required final status for completed work:

- Changed files
- Verification performed
- Known gaps or blocked items

## Token Discipline

Use `token-optimization-strategy.md` for context loading, handoff compression, and final update limits.
