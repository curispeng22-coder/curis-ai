# Task Runtime Engine

## Purpose

The Task Runtime Engine converts approved work requests into executable units with state, boundaries, authority, verification, and feedback. It is the runtime layer above the static Task Execution System.

## Runtime Contract

Every runtime task must carry this envelope:

```text
Task ID
Phase
System state
Sprint gate
Scope class
Owner role
Decision authority
Context boundary
Allowed files
Required outputs
Verification command or method
Feedback target
Completion status
```

If an envelope field is unknown, the task remains in `Intake` until the missing field is inferred from source-of-truth documents or clarified by the accountable role.

## Runtime States

```text
Intake
  -> Gate Check
  -> Context Load
  -> Plan Slice
  -> Execute Slice
  -> Verify Slice
  -> Observe State
  -> Feedback Apply
  -> Ready For Review
```

Blocked tasks move to `Runtime Blocked`. Invalid tasks move to `Runtime Rejected`.

## Runtime Rules

- Gate Check must run before any file edit.
- Context Load must follow `context-boundary-system.md`.
- Bootstrap tasks must use `bootstrap-sequence.md` before execution.
- First-run tasks must use `mvp-execution-loop.md`.
- Plan Slice must define the smallest useful work package.
- Execute Slice must stay inside allowed files.
- Verify Slice must produce evidence or record a gap.
- Observe State must update gate, phase, or task status when changed.
- Feedback Apply must route corrections back into the smallest affected slice.

## Input Schema

Required input:

- User request or Sprint item
- Current phase
- Current gate
- Desired output

Optional input:

- Target files
- Reviewer role
- Verification preference
- Known blockers

## Output Schema

Required output:

- Created or changed artifacts
- Verification evidence
- Runtime state after execution
- Gate status
- Next allowed action

## Rejection Conditions

Reject or block a task when:

- It asks for Sprint 1 before the Sprint 1 gate opens.
- It asks for business code during Sprint 0.
- It lacks a safe file boundary.
- It requires authority the acting role does not have.
- It cannot be verified and the requester requires verified completion.

## Bootstrap Runtime

The first runnable task path is defined by:

- `bootstrap-sequence.md`
- `mvp-execution-loop.md`
- `standard-task-template.md`
