# Task Execution System

## Purpose

This system turns Curis Workspace work requests into controlled AI development execution. It prevents role ambiguity, scope drift, and premature business-code development.

## Execution Contract

Every executable task must define:

- Phase
- Scope
- Owner role
- Requested output
- Source-of-truth documents
- Allowed file boundaries
- Verification requirement
- Gate impact

If any field is missing, the acting role must infer conservatively from existing governance documents or ask for clarification when the risk is material.

## Task States

```text
Proposed
  -> Scoped
  -> Assigned
  -> In Progress
  -> Verification
  -> Review
  -> Accepted
```

Blocked tasks move to `Blocked` from any state. Cancelled tasks move to `Cancelled` by 总控决策席 decision or user instruction.

## State Rules

- Proposed: Request received, not yet checked against gates.
- Scoped: Phase, scope, and boundaries are known.
- Assigned: Accountable owner and consulted roles are known.
- In Progress: Work is being changed inside approved boundaries.
- Verification: Evidence is being collected.
- Review: Output is ready for reviewer decision.
- Accepted: Reviewer confirms the acceptance criteria.
- Blocked: Work cannot continue without decision, approval, or missing input.
- Cancelled: Work is intentionally stopped.

## Execution Steps

1. Read `AGENTS.md`.
2. Identify the current system state from `system-state-machine.md`.
3. Check Sprint gate rules in `sprint-gate-system.md`.
4. Classify the task scope.
5. Assign an owner from `decision-authority-matrix.md`.
6. Load context according to `context-boundary-system.md`.
7. Execute the smallest reviewable change.
8. Verify against the task's output requirement.
9. Update the relevant Sprint or organization status document.
10. Report changed files, verification, and gate status.

## Scope Classes

- Organization system: roles, gates, operating model, and governance.
- Standards system: documentation, code, directory, testing, and review standards.
- Sprint system: Sprint workflow, checklist, status, and ceremonies.
- Architecture system: ADRs, boundaries, interfaces, and technical direction.
- Business system: product features, user flows, APIs, schemas, and product UI.

During Sprint 0 Phase 2, only organization runtime, standards, Sprint, and architecture planning work is allowed. Business system work is blocked.

The runtime execution layer for these task states is defined in `task-runtime-engine.md`.

## Completion Criteria

A task is complete only when:

- Required outputs exist in the expected files.
- Source-of-truth indexes are updated.
- Verification has run or a verification gap is recorded.
- Gate status is explicitly unchanged or updated.
- No forbidden business-code work was introduced.
