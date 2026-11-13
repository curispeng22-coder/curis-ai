# Tool System v1.8 - Controlled Self-Evolution Kernel

Status: Deprecated

Sprint name: Sprint 1B - Controlled Self-Evolution Kernel

## Final System Definition

Curis Workspace is now defined as:

AI Operating System Kernel with Controlled Self-Evolution.

It is not an agent system, not a tool system, and not a workflow system. It is an operating system kernel for AI execution.

## Goal

Transform the v1.6 execution and meta-development loop into a controlled self-evolving AI operating system that can:

- Execute tasks reliably.
- Optimize workflows safely.
- Propose architecture redesign under strict controls.
- Decide when not to evolve.
- Maintain rollback records for reversible evolution.

## Protected Loop

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

## Stability Policy

The system must enforce:

```text
STABILITY > OPTIMIZATION > EVOLUTION
```

No evolution is allowed unless evaluation passes.

## Scope

Allowed:

- Evolution Control Governor.
- Threshold evaluation for failure rate, latency increase, and workflow inefficiency.
- Architecture locking for core orchestrator, execution engine, and tool router base layer.
- Controlled self-rewrite proposal records.
- Simulation records for task flow, tool routing, workflow graph, and performance impact.
- Risk analysis records.
- Meta decision records: `evolve`, `do_not_evolve`, `postpone_evolution`, `rollback_previous_evolution`.
- Rollback records with previous architecture, stable version, and performance comparison.
- API evidence for retrieving evolution decisions.
- Backend tests and scope drift scan.

Forbidden:

- UI changes.
- ROI system.
- Business modules.
- Agent abstraction layer.
- Multi-agent system.
- Employee CRUD or employee expansion.
- Mock data or simulation mode.
- Uncontrolled architecture changes.
- Automatic code self-modification without approval.

## Completion Checklist

- [x] System can execute tasks reliably after v1.8 changes.
- [x] Evolution Governor evaluates threshold conditions.
- [x] Stability-first policy blocks unsafe evolution.
- [x] Locked modules cannot be marked for automatic modification.
- [x] System can create controlled self-rewrite proposals.
- [x] System can simulate task flow, tool routing, workflow graph, and performance impact.
- [x] System can produce risk analysis.
- [x] System can decide `evolve`.
- [x] System can decide `do_not_evolve`.
- [x] System can decide `postpone_evolution`.
- [x] System can record rollback data.
- [x] API can retrieve evolution decisions.
- [x] Backend tests pass.
- [x] Scope drift scan finds no forbidden implementation.

## Product Acceptance

Accepted by 产品规划席 on 2026-07-06.

Evidence:

- 系统交付席 delivery review completed with no blockers.
- 质量运行席 independent verification completed with PASS and no blockers.
- Backend regression, API evidence, and scope drift scan are recorded in `reviews/003_tool_system_v1_8_controlled_self_evolution_review.md`.

## Next Gate

Sprint 1 - 公司运行可视化 may resume from product planning. No UI implementation should start until the Sprint 1 PRD slice is refreshed and confirmed.
