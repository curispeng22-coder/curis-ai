# AI Development Organization

This folder defines the Curis Workspace AI Development Organization. It is the operating baseline for AI-assisted engineering work before business development begins.

## Organization Charter

The organization exists to make AI-assisted development predictable, reviewable, and safe. Its first responsibility is to build a durable engineering system: clear roles, bounded responsibilities, shared standards, and a Sprint workflow that prevents uncontrolled business-code drift.

## Required Review Scope

The organization review must cover:

- `team-structure.md`: organization topology and operating model
- `roles.md`: team roles and responsibility boundaries
- `responsibility-matrix.md`: accountability and blocking authority
- `collaboration-protocol.md`: collaboration, decision, and escalation rules
- `token-optimization-strategy.md`: AI context and token efficiency rules
- `task-execution-system.md`: executable task lifecycle and completion rules
- `context-boundary-system.md`: phase, file, role, decision, and token boundaries
- `decision-authority-matrix.md`: decision ownership, approval, and blocker authority
- `system-state-machine.md`: allowed system states and transitions
- `sprint-gate-system.md`: phase, Sprint, implementation, and release gates
- `task-runtime-engine.md`: runtime envelope, task states, and execution rules
- `agent-execution-loop.md`: repeatable agent observe-act-verify-report loop
- `ceo-reporting-standard.md`: shared conclusion-reason-recommendation reporting standard for development seats and product AI employees
- `system-feedback-loop.md`: review and verification feedback routing
- `token-governance-layer.md`: runtime token budgets and context escalation
- `runtime-state-observer.md`: phase, gate, drift, and verification observation
- `mvp-execution-loop.md`: minimum runnable closed loop for first execution
- `standard-task-template.md`: first executable task envelope and sample
- `bootstrap-sequence.md`: system startup mode and first-run sequence
- `../standards/directory-structure.md`: repository layout rules
- `../standards/documentation-standard.md`: documentation quality rules
- `../standards/coding-standard.md`: coding quality rules
- `../sprints/sprint-workflow.md`: Sprint workflow and gates
- `../sprints/sprint-0-organization-review.md`: current review checklist

## Current Scope Rule

MVP implementation is open only for the v1.6 loop defined in `docs/sprints/tool-system-v1.6-meta-development.md`.

## Current Operating State

Current state: Sprint 1A execution planning, Meta Development System.

MVP status: Open only for Curis Workspace Tool System v1.6.

Current allowed loop:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Storage
```

Forbidden: ROI system, Employee CRUD or employee expansion, multi-agent system, business modules, UI complexity, mock data, and simulation mode.
