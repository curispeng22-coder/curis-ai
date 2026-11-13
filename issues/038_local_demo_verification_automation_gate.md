# Local/Demo Verification Automation Gate

Date: 2026-07-07

Owner seat: 产品规划席

Decision seat: 总控决策席

Status: APPROVED by 总控决策席 on 2026-07-07.

## Background

AI Task Executor MVP v0.1 is local/demo ready and now has operator notes for startup, smoke verification, shutdown, rollback, known warning, and evidence references.

The remaining operator risk is that local/demo verification is still mostly manual. The next bounded phase should reduce repeat verification effort without adding product features or changing the AI Task Executor runtime.

This gate does not approve implementation.

## Objective

Decide whether to approve a bounded Local/Demo Verification Automation phase.

## Allowed Scope

- Gate decision only.
- Planning for a local-only verification helper or checklist.
- Planning for deterministic health, task creation, and task history smoke verification against the existing local API.
- Planning for documentation updates that reference the verification helper.
- Source-of-truth updates after gate decision.

## Required Preservation

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing execution behavior.
- Existing Evolution Governor behavior.
- Project Memory.
- Role Profiles.
- Role Context.
- Release record/tag semantics.
- Source-of-truth ownership.

## Forbidden Scope

- Backend/frontend behavior changes.
- New product features.
- Complex UI/dashboard.
- New entry channels.
- API semantic changes.
- Persistence/schema/new table changes.
- New execution behavior.
- Automatic evolution behavior changes.
- Code self-modification.
- Architecture mutation.
- Unlocking locked modules.
- External services or new model-provider integrations.
- Runtime prompt integration beyond approved helper behavior.
- Task-role association.
- Task evidence attachment.
- ROI/economy.
- Business modules.
- Employee CRUD/expansion.
- Company organization, departments, reporting lines, or staffing.
- Multi-agent routing.
- Agent abstraction layer.
- Future-layer implementation.
- Mock data or simulation substitution for release/demo evidence.

## Acceptance Criteria

- 产品规划席 records next-phase selection.
- 总控决策席 records approve or reject decision.
- If approved, next step routes to 系统交付席 for architecture boundaries and exact scope definition only.
- `PROJECT_STATUS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` are updated.
- No backend/frontend implementation files are changed by this gate.
- Compact handoff payload is ready for the next seat.

## Handoff

Handoff: sent to 系统交付席.

Target seat: 系统交付席.

Compact payload:

- Issue: `issues/038_local_demo_verification_automation_gate.md`
- Objective: Define Local/Demo Verification Automation architecture boundaries before implementation.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing persistence schema, existing execution behavior, Evolution Governor behavior, Project Memory, Role Profiles, Role Context, release record/tag, and source-of-truth ownership.
- Allow: architecture boundary definition only for local-only verification helper/checklist, deterministic health/task-create/task-history smoke verification against existing local API, and release documentation references.
- Forbid: backend/frontend behavior changes, new features, complex UI/dashboard, API semantic changes, persistence/schema/new tables, new execution behavior, automatic evolution behavior changes, code self-modification, architecture mutation, unlocking locked modules, external services, task-role association, task evidence attachment, ROI/economy, business modules, Employee CRUD/expansion, company organization, multi-agent routing, agent abstraction, future-layer scope, and mock/simulation substitution.

## Decision

Decision: APPROVED by 总控决策席 on 2026-07-07.

Approved next step:

- 系统交付席 may define architecture boundaries and exact scope for Local/Demo Verification Automation.

This approval does not approve implementation.

Rationale:

- Operator notes made the local/demo workflow easier to understand.
- A bounded verification helper can reduce repeated manual smoke-check effort without changing product behavior.
- The phase remains inside AI Task Executor MVP v0.1 and does not open future AI Company System layers.
