# Execution Substance Phase Gate

Date: 2026-07-07

Owner seat: 产品规划席 (proposes)

Target approval: 总控决策席

Status: Proposed — pending 总控决策席 approval.

Source ADR: `docs/decisions/ADR-0016-execution-substance-initiative.md`

## Objective

Approve architecture boundary definition for the Execution Substance Initiative. This gate authorizes boundary definition only; it does not approve implementation, new features, complex UI/dashboard, future-layer scope, API semantic changes, persistence/schema changes beyond the additive event log, external services, or automatic evolution behavior changes.

## Gate Brief Summary

The initiative converts three deferred capabilities into narrow, reversible, executable slices:

- **D1 Runtime Role Wiring** — wire `backend/app/role_context.py` into `prompt_builder.py` / `employee.py` step routing under the explicit profile-id contract only.
- **D2 Evolution Governor Sandbox** — apply and roll back a Stability-first proposal against a throwaway copy of code/state; capture evidence; zero writes to authoritative repo or SQLite; explicit human approval before any production mutation.
- **D3 Append-Only Evolution Log** — immutable event log (new `evolution_events` table or dedicated store) with correlation id; additive; mutable tables may remain for query.

## Allowed Scope (if approved)

- Architecture boundary definition only.
- Reference to `docs/decisions/ADR-0016-execution-substance-initiative.md`.
- Source-of-truth updates (this gate issue, the ADR).

## Required Preservation

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics (except additive read/event endpoints introduced here).
- Existing execution behavior (except the three narrow behavior changes above).
- Existing Evolution Governor decision policy.
- Human-approval gate for production mutation.
- Project Memory source-of-truth ownership.
- Role Profiles, Role Context, release record/tag semantics, and source-of-truth ownership.

## Forbidden Scope

- Backend/frontend behavior changes outside the three slices.
- New product features.
- Complex UI/dashboard beyond minimal evidence display.
- API semantic changes beyond additive read/event endpoints.
- Dropping or mutating existing persistence tables.
- Vector database or embeddings.
- External memory service or hidden memory store.
- Agent memory, Employee memory.
- Runtime prompt integration beyond role-context guidance.
- Task-role association, task evidence attachment.
- Multi-agent coordination or routing.
- New execution behavior beyond the three slices.
- Automatic evolution behavior changes / automatic code self-modification without approval.
- ROI/economy, business modules.
- Employee CRUD/expansion.
- Company organization, departments, reporting lines, or staffing.
- Agent abstraction layer.
- Future-layer implementation.

## Recommended Next

On approval: 系统交付席 defines per-slice boundaries; 质量运行席 verifies; 产品规划席 accepts; then first-slice issues `issues/045_runtime_role_wiring_first_slice.md`, `issues/046_evolution_governor_sandbox_first_slice.md`, and `issues/047_append_only_evolution_log_first_slice.md` may be opened.

## Handoff

Handoff: HANDOFF_REQUIRED to 总控决策席.

Compact payload:

- Issue: `issues/044_execution_substance_phase_gate.md`
- Objective: Approve Execution Substance Initiative architecture boundaries (no implementation).
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing execution behavior, Evolution Governor decision policy, human-approval gate, Project Memory ownership, Role Profiles, Role Context, release record/tag semantics, source-of-truth ownership.
- Allow: architecture boundary definition only for the three slices in ADR-0016; source-of-truth updates.
- Forbid: backend/frontend behavior changes outside the three slices, new features, complex UI/dashboard, API semantic changes beyond additive read/event endpoints, dropping/mutating existing tables, vector DB/embeddings, external memory service, hidden memory store, agent/Employee memory, runtime prompt integration beyond role-context guidance, task-role association, task evidence attachment, multi-agent coordination/routing, new execution behavior, automatic evolution behavior changes / automatic code self-modification without approval, ROI/economy, business modules, Employee CRUD/expansion, company organization, agent abstraction, future-layer scope.
