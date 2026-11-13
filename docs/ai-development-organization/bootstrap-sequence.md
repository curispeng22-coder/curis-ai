# Bootstrap Sequence

## Purpose

The Bootstrap Sequence defines how the Curis AI Development OS starts from a design state and performs its first controlled runtime action.

## Bootstrap Mode

Bootstrap mode is historical for the pre-implementation setup phase. The current active state is defined in `docs/pmo/current-status.md` and `sprint-gate-system.md`.

Bootstrap mode is active when:

- The system is still in Sprint 0.
- Sprint 1 is closed.
- Governance and runtime documents exist.
- The next task is to prove the operating loop can run safely.

## Startup Sequence

```text
Start
  -> Load Root Instructions
  -> Load State And Gates
  -> Load Runtime Loop
  -> Create Task Envelope
  -> Confirm Boundaries
  -> Run MVP Loop
  -> Record Snapshot
  -> Stop At Review
```

## Step Rules

### Load Root Instructions

Read `AGENTS.md` first.

If root instructions conflict with optional process behavior, root instructions win.

### Load State And Gates

Read:

- `system-state-machine.md`
- `sprint-gate-system.md`
- `runtime-state-observer.md`

Confirm the current Sprint and business-code gates from the active source of truth.

### Load Runtime Loop

Read:

- `mvp-execution-loop.md`
- `task-runtime-engine.md`
- `agent-execution-loop.md`
- `token-governance-layer.md`

Use the MVP loop for first-run execution.

### Create Task Envelope

Use `standard-task-template.md`.

Do not proceed if the task envelope lacks phase, owner, file boundary, output, or verification.

### Confirm Boundaries

Check:

- Phase boundary
- Scope boundary
- File boundary
- Role authority
- Token level
- Verification method

### Run MVP Loop

Execute one slice only.

If feedback creates additional work, route it through `system-feedback-loop.md` as a new task or revision.

### Record Snapshot

Update or report:

- Current phase
- System state
- Gate status
- Changed files
- Verification result
- Next allowed action

### Stop At Review

Bootstrap mode stops at review. It does not open Sprint 1.

## First Runnable Capability

After bootstrap, the system can run this minimum capability:

```text
Accept allowed governance task
  -> wrap it in a task envelope
  -> execute one bounded slice
  -> verify the slice
  -> observe state
  -> report review-ready output
```

## Bootstrap Exit Criteria

Bootstrap mode is ready for review when:

- MVP Execution Loop exists.
- Standard Task Template exists.
- Bootstrap Sequence exists.
- Indexes and plugin skill reference the bootstrap layer.
- Sprint review checklist includes bootstrap outputs.
- Verification confirms no business code was introduced.
