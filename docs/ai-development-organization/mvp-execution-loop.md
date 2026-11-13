# MVP Execution Loop

## Purpose

The MVP Execution Loop is the first runnable closed loop for the Curis AI Development OS. It defines the smallest sequence an AI agent can execute to move one allowed task from request to review without starting Sprint 1.

## Loop Contract

The loop can run only when:

- The task is not business implementation.
- The current gate allows the task scope.
- The task has a clear owner role.
- The file boundary is known.
- Verification can be run or explicitly recorded as unavailable.

## Minimal Loop

```text
Boot
  -> Read Gate
  -> Build Task Envelope
  -> Bound Context
  -> Execute One Slice
  -> Verify
  -> Observe State
  -> Report
```

## Step Rules

### Boot

Load:

- `AGENTS.md`
- `docs/ai-development-organization/bootstrap-sequence.md`
- `docs/ai-development-organization/system-state-machine.md`
- `docs/ai-development-organization/sprint-gate-system.md`

### Read Gate

Confirm:

- Current phase
- Current system state
- Sprint 1 gate status
- Business-code gate status

If Sprint 1 is closed and the task asks for business implementation, stop.

### Build Task Envelope

Use `standard-task-template.md`.

The task envelope must include:

- Task ID
- Scope class
- Owner role
- Allowed files
- Required outputs
- Verification method
- Completion condition

### Bound Context

Use the lowest sufficient token level from `token-governance-layer.md`.

Do not load broad repository context unless the file boundary is unknown.

### Execute One Slice

Make one small reviewable change.

The slice must be reversible by reviewing the changed files. It must not create product behavior.

### Verify

Use the relevant verification method:

- Plugin validation when plugin files change
- Skill validation when skill files change
- Targeted search for gate contradictions
- File listing to confirm no business source directories were created

### Observe State

Use `runtime-state-observer.md` to confirm:

- State did not drift
- Gates remain correct
- Changed files match the task boundary
- Verification result is recorded

### Report

Report:

- Changed files
- Verification evidence
- Current state
- Sprint status
- Next allowed action

## Successful Run Definition

A successful MVP loop run produces:

- One completed task envelope
- One or more reviewable governance artifacts
- Verification evidence
- No open gate drift
- No business code
