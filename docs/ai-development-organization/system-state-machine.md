# System State Machine

## Purpose

This state machine defines the operating states of Curis Workspace so AI agents can determine what actions are allowed at any moment.

## System States

```text
S0 Repository Initialized
  -> S1 Organization Drafting
  -> S2 Organization Operating System Drafting
  -> S2R Execution Runtime Layer Drafting
  -> S2B Bootstrap Runtime Layer Drafting
  -> S3 Organization Review
  -> S4 Sprint Planning
  -> S5 Sprint Execution
  -> S6 Release Review
```

Blocked work enters `SB Blocked` from any state. Cancelled work enters `SC Cancelled` by 总控决策席 or user instruction.

## Current State

Current state: `S5 Sprint Execution`

Current phase: Sprint 1A - Meta Development System

Sprint 1A status: Open for Tool System v1.6 meta-development loop.

## State Definitions

### S0 Repository Initialized

Repository exists but no organization baseline is defined.

Allowed:

- Create initial governance docs
- Define repository purpose

Blocked:

- Business implementation

### S1 Organization Drafting

Static organization baseline is being created.

Allowed:

- Team structure
- Role definitions
- Responsibility matrix
- Collaboration flow
- Token optimization strategy

Blocked:

- Business implementation
- Sprint 1 planning

### S2 Organization Operating System Drafting

Executable operating systems are being added to the organization baseline.

Allowed:

- Task execution system
- Context boundary system
- Decision authority matrix
- System state machine
- Sprint gate system

Blocked:

- Business implementation
- Sprint 1 planning
- Production architecture implementation

### S2R Execution Runtime Layer Drafting

The organization operating system is being converted into a runtime execution layer.

Allowed:

- Task runtime engine
- Agent execution loop
- System feedback loop
- Token governance layer
- Runtime state observer

Blocked:

- Business implementation
- Sprint 1 planning
- Production architecture implementation
- Runtime automation that executes product behavior

### S2B Bootstrap Runtime Layer Drafting

The execution runtime layer is being given its first runnable closed loop.

Allowed:

- MVP execution loop
- Standard executable task template
- Bootstrap sequence
- Source-of-truth updates for first-run capability

Blocked:

- Business implementation
- Sprint 1 planning
- Product runtime automation
- Production architecture implementation

### S3 Organization Review

Organization baseline and operating system are under review.

Allowed:

- Review comments
- Revisions to governance
- Approval recording

Blocked:

- Business implementation until approval is recorded

### S4 Sprint Planning

The next Sprint is approved for planning, but not yet implementation.

Allowed:

- Backlog shaping
- Architecture planning
- Test planning
- Implementation planning

Blocked:

- Implementation until the Sprint implementation gate is approved

### S5 Sprint Execution

Approved Sprint work is being implemented.

Allowed:

- Work inside approved Sprint scope
- Tests and verification
- Documentation updates
- MVP minimal working loop when explicitly approved

Blocked:

- Out-of-scope implementation
- Gate bypass
- Advanced agent system
- Multi-company system
- Autonomy system

### S6 Release Review

Completed Sprint work is being prepared for release or closure.

Allowed:

- Final verification
- Release notes
- Retrospective
- Risk review

Blocked:

- New feature scope without new intake

## Transition Rules

- S1 to S2: Phase 1 review identifies missing executable systems.
- S2 to S2R: Phase 2 requests execution runtime layer.
- S2R to S2B: Phase 3 requests bootstrap runtime layer.
- S2B to S3: Bootstrap runtime layer exists and is verified.
- S3 to S4: Sprint planning is approved.
- S4 to S5: Sprint implementation plan and gate are approved.
- S5 to S6: Sprint acceptance criteria and verification are complete.

No state may skip the next gate without 总控决策席 approval and documented rationale.
