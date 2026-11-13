# Runtime Role Context Wiring

Date: 2026-07-07

Owner seat: 系统交付席

Status: Implementation accepted by 产品规划席 on 2026-07-07 (质量运行席 verification PASS, 48 tests). D1 slice CLOSED. Next per ADR-0016 order: D3 Append-Only Event Log (its own gate/boundary).

Source gate: `issues/044_execution_substance_phase_gate.md`

Boundary ADR: `docs/decisions/ADR-0016-execution-substance-initiative.md` (Accepted) + `docs/decisions/ADR-0018-sprint3-role-context-runtime-unblock.md` (unblock record) + `docs/decisions/ADR-0019-d1-runtime-role-wiring-boundaries.md` (per-slice boundaries).

## Objective

Wire the existing read-only `backend/app/role_context.py` into the execution loop so role context becomes real prompt/context guidance instead of dead code.

## Allowed Scope

- Import and call `role_context.py` from `backend/app/prompt_builder.py` and the `backend/app/employee.py` step handoff.
- Use the explicit profile-id contract (`curis.role.system-delivery.v1`); omit role context when the profile id is missing or invalid.
- Add role-context excerpts to the prompt/context passed to the AI Employee.
- Backend tests covering the wiring and the missing/invalid-profile fallback.

## Required Preservation

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing execution behavior except the additive role-context guidance.
- Existing Evolution Governor behavior.
- Human-approval gate for production mutation.
- Role Profiles / Role Context semantics.

## Forbidden Scope

- Implicit default role.
- Tool selection, work routing, task-state mutation, or evolution triggering by role context.
- New execution behavior beyond prompt/context guidance.
- Employee CRUD / employee expansion, multi-agent, agent abstraction.
- Complex UI / dashboard.
- API semantic changes.
- Persistence / schema / new table changes.
- ROI / economy, business modules, company organization.
- Runtime prompt integration beyond role-context guidance.
- Task-role association, task evidence attachment.
- Automatic evolution behavior changes / automatic code self-modification.

## Acceptance Criteria

- `role_context` is referenced from `prompt_builder.py` and/or `employee.py`.
- With a valid explicit profile id, role context appears in the employee prompt/context.
- With a missing or invalid profile id, output is unchanged (no role context, no error).
- Backend regression passes; new focused tests cover wiring and fallback.
- `git diff --check` passes; forbidden-scope scan passes.

## Verification

质量运行席 verifies with diff guard, `git diff --check`, and forbidden-scope scan; plus focused tests asserting valid-profile wiring and missing/invalid-profile unchanged behavior.

## Handoff

Handoff: sent to 质量运行席 (after implementation).

Target seat: 质量运行席.

Compact payload:

- Issue: `issues/045_runtime_role_wiring_first_slice.md`
- Objective: Wire role_context.py into the execution loop.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing execution behavior, Evolution Governor behavior, human-approval gate, Role Profiles, Role Context.
- Allow: import/call role_context from prompt_builder/employee; explicit profile-id only; additive prompt/context guidance; backend tests for wiring and fallback.
- Forbid: implicit default role, tool selection/routing by role context, task-state mutation, evolution triggering, new execution behavior, Employee CRUD/expansion, multi-agent, agent abstraction, complex UI/dashboard, API semantic changes, persistence/schema/new table changes, ROI/economy, business modules, company organization, runtime prompt integration beyond role-context guidance, task-role association, task evidence attachment, automatic evolution behavior changes / automatic code self-modification.
