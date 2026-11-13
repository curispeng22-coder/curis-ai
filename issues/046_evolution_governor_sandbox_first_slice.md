# Evolution Governor Sandbox

Date: 2026-07-07

Owner seat: 系统交付席

Status: Implementation accepted by 产品规划席 on 2026-07-07 (质量运行席 verification PASS, 63 tests). D2 slice CLOSED. ADR-0016 Execution Substance Initiative (D1→D3→D2) fully complete.

Source gate: `issues/044_execution_substance_phase_gate.md`

Boundary ADR: `docs/decisions/ADR-0016-execution-substance-initiative.md`

## Objective

Add a controlled execution substrate where a Stability-first Evolution Governor proposal can be applied and rolled back against a throwaway copy of code/state, with evidence captured. This converts the governor from "produces records" into "can safely demonstrate a change."

## Allowed Scope

- Add a sandbox execution substrate that copies the current codebase/state to a throwaway path.
- Apply a controlled proposal to the throwaway copy; capture apply + rollback evidence (diffs, logs) as reviewable artifacts.
- Require explicit human approval before any production mutation; the sandbox itself never writes to the authoritative repo or SQLite.
- Backend tests proving a sandbox run writes zero bytes to repo/SQLite and that rollback restores the throwaway copy.

## Required Preservation

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing execution behavior except the additive sandbox substrate.
- Existing Evolution Governor decision policy (the sandbox does not change decision logic).
- Human-approval gate for production mutation.
- Role Profiles / Role Context semantics.

## Forbidden Scope

- Writing to the authoritative repo or SQLite during a sandbox run.
- Automatic production mutation without explicit human approval.
- Lifting the human-approval gate for code self-modification.
- Changing existing Evolution Governor decision policy beyond the sandbox substrate.
- Employee CRUD / employee expansion, multi-agent, agent abstraction.
- Complex UI / dashboard beyond minimal evidence display.
- API semantic changes.
- Persistence / schema / new table changes (except the append-only log in slice 047).
- ROI / economy, business modules, company organization.
- Runtime prompt integration beyond role-context guidance.
- Task-role association, task evidence attachment.
- Vector database, embeddings, external memory service, hidden memory store.
- Future-layer implementation.

## Acceptance Criteria

- A sandbox run applies a proposal to a throwaway copy and produces reviewable apply + rollback evidence.
- A sandbox dry run writes zero bytes to the authoritative repo and SQLite (asserted by test).
- Rollback restores the throwaway copy exactly.
- No production mutation occurs without an explicit human-approval path outside the sandbox.
- Backend regression passes; new focused tests cover no-prod-write and rollback.
- `git diff --check` passes; forbidden-scope scan passes.

## Verification

质量运行席 verifies with diff guard, `git diff --check`, forbidden-scope scan, and focused tests asserting zero authoritative writes and successful rollback.

## Handoff

Handoff: sent to 质量运行席 (after implementation).

Target seat: 质量运行席.

Compact payload:

- Issue: `issues/046_evolution_governor_sandbox_first_slice.md`
- Objective: Add a throwaway-copy sandbox so the governor can safely demonstrate a controlled change.
- Preserve: AI Task Executor MVP v0.1 local/demo release, Tool System v1.8 loop, Stability > Optimization > Evolution policy, Chinese operation console, Task API `{ content }`, existing API semantics, existing execution behavior, Evolution Governor decision policy, human-approval gate, Role Profiles, Role Context.
- Allow: sandbox substrate on throwaway copy; apply + rollback evidence capture; explicit human approval before production mutation; backend tests for no-prod-write and rollback.
- Forbid: writes to authoritative repo/SQLite during sandbox; automatic production mutation without approval; lifting human-approval gate; changing governor decision policy; Employee CRUD/expansion, multi-agent, agent abstraction; complex UI/dashboard; API semantic changes; persistence/schema changes except slice 047; ROI/economy, business modules, company organization; runtime prompt integration beyond role-context guidance; task-role association; task evidence attachment; vector/embeddings/external/hidden memory; future-layer scope.
