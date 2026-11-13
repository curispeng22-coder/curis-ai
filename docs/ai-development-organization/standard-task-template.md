# Standard Task Template

## Purpose

This is the first standard executable task template for the Curis AI Development OS. It gives agents a repeatable shape for running governance and runtime tasks before Sprint 1.

## Template

```text
Task ID:
Task Name:
Phase:
System State:
Sprint Gate:
Business-code Gate:
Scope Class:
Owner Seat:
Decision Authority:
Context Level:
Allowed Files:
Required Outputs:
Execution Slice:
Verification Method:
Completion Condition:
Feedback Target:
Final State:
```

## Field Rules

- Task ID: Use `S0P<phase>-<short-name>` for Sprint 0 tasks.
- Task Name: Use a short action phrase.
- Phase: Must match the current phase.
- System State: Must match `system-state-machine.md`.
- Sprint Gate: Must state whether Sprint 1 is open or closed.
- Business-code Gate: Must state open or closed.
- Scope Class: Use a class from `task-execution-system.md`.
- Owner Seat: Use a role from `roles.md`.
- Decision Authority: Use `decision-authority-matrix.md`.
- Context Level: Use `token-governance-layer.md`.
- Allowed Files: Must be explicit.
- Required Outputs: Must be reviewable artifacts.
- Execution Slice: Must be the smallest useful change.
- Verification Method: Must be runnable or explicitly recorded as unavailable.
- Completion Condition: Must be observable.
- Feedback Target: Must identify where review comments return.
- Final State: Must state the runtime state after execution.

## Executable Task Sample

```text
Task ID: S0P3-bootstrap-runtime
Task Name: Add Bootstrap Runtime Layer
Phase: Sprint 0 Phase 3
System State: S2B Bootstrap Runtime Layer Drafting
Sprint Gate: Sprint 1 closed
Business-code Gate: Closed
Scope Class: Organization system
Owner Seat: 系统交付席
Decision Authority: 总控决策席 approves, 系统交付席 executes, 产品规划席 reviews
Context Level: L2 Cross-system
Allowed Files:
  - AGENTS.md
  - README.md
  - docs/ai-development-organization/
  - docs/sprints/sprint-0-organization-review.md
  - plugins/curis-ai-development-organization/skills/curis-development-organization/SKILL.md
Required Outputs:
  - MVP Execution Loop
  - Standard Task Template
  - Bootstrap Sequence
Execution Slice: Add Bootstrap Runtime Layer docs and update source-of-truth references.
Verification Method:
  - Validate Curis plugin
  - Validate Curis governance skill
  - Search for gate contradictions and forbidden business-code drift
  - List repository files outside `.git`
Completion Condition:
  - Required outputs exist
  - Indexes and review checklist reference outputs
  - Sprint 1 remains blocked
  - No business code exists
Feedback Target: docs/sprints/sprint-0-organization-review.md
Final State: Ready For Review
```

## Usage Rules

- Use this template before executing any new Sprint 0 task.
- Do not omit gate fields.
- Do not mark `Final State` as complete when verification failed.
- If the task asks for business implementation during Sprint 0, set `Final State` to `Runtime Blocked`.
