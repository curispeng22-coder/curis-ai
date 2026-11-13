# ADR-0019: D1 Runtime Role Wiring — Architecture Boundaries

Date: 2026-07-07
Status: Proposed — for 质量运行席 verification, then 产品规划席 acceptance.
Authorized by: ADR-0016 (Accepted) + ADR-0018 (Sprint 3 unblock, scoped to Sub-decision A).
First-slice issue: `issues/045_runtime_role_wiring_first_slice.md`
Depends on: ADR-0018 (unblock record)
Slice order: D1 → D3 → D2 (per approved gate decision, option a).

## Context

First slice of ADR-0016 (Sub-decision A). Converts the read-only `role_context.py` helper into real, constrained runtime prompt/context guidance. This is the lowest-risk, highest-value slice and the first intentional break from the v0.1 "runtime prompt integration blocked" purity (now explicitly unblocked by ADR-0018 for this scope only).

## Allowed Files / Modules (boundary)

- **Read**: `backend/app/role_context.py` (existing; explicit profile-id `curis.role.system-delivery.v1`).
- **Modify**: `backend/app/prompt_builder.py` — import and call `role_context` to attach an additive context excerpt.
- **Modify**: `backend/app/employee.py` — pass the role-context excerpt through the step handoff (no routing/selection logic).
- **Add**: backend tests asserting wiring + missing/invalid-profile fallback.
- **No** new tables, no schema change, no persistence change, no API semantic change, no UI change.

## Behavior Contract (ADR-0016 Sub-decision A + carried-forward 003 constraints)

- Explicit profile-id only; never implicit default.
- Missing/invalid profile id → behavior unchanged (role context omitted, no error).
- Role context MAY only add prompt/context guidance.
- Role context MUST NOT: select tools, route work, change task state, trigger evolution, create/select agents, mutate workflows, alter learning/meta/evolution, change API/storage semantics.
- No task evidence attachment, UI selector/dashboard, backend metadata, persistence, new tables, or task-role association.

## Verification Plan (for 质量运行席)

- `git diff --name-only HEAD -- backend frontend` → only `prompt_builder.py`, `employee.py`, `role_context.py` (read), and tests.
- `git diff --check` passes.
- `rg` forbidden-scope keywords → zero matches in changed files.
- Slice-specific: assert `role_context` imported in `prompt_builder`/`employee`; missing/invalid profile id yields unchanged output; valid profile id yields additive excerpt only.
- Regression: existing backend test suite passes (no behavior drift outside additive guidance).

## Forbidden Scope (superset of issues/045, ADR-0016, and ADR-0018 carried-forward constraints; enumerated for completeness)

Implicit default role; tool selection / work routing / task-state mutation / evolution triggering by role context; new execution behavior beyond prompt/context guidance; Employee CRUD / expansion; multi-agent; agent abstraction; complex UI / dashboard; API semantic changes; persistence / schema / new-table changes; ROI / economy; business modules; company organization; runtime prompt integration beyond role-context guidance; task-role association; task evidence attachment; automatic evolution behavior changes / automatic code self-modification.

Also forbidden (carried from ADR-0016 / ADR-0018, still in force): external services / channels / secrets handling; vector database / embeddings / external or agent memory stores; architecture lock bypass / uncontrolled architecture changes; any mutation of authoritative repo or SQLite outside the sandbox (D2 scope) or the append-only log (D3 scope); lifting the human-approval gate for automatic code self-modification.

## Consequences

- Easier: role context demonstrable in the execution loop.
- Harder: first production behavior-diff of the v0.1-boundary era; must be verifiable, not just absent.

## Next Seat

质量运行席 verifies boundaries (per Verification Plan); 产品规划席 accepts; then 系统交付席 implements per `issues/045`.
