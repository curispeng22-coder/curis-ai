# ADR-0018: Lift Sprint 3 Role Context Runtime Block — Scoped to ADR-0016 Sub-decision A

Date: 2026-07-07
Status: Accepted
Supersedes: `knowledge/003_Architecture.md` § "Sprint 3 Role Context Runtime Reference Boundary" (line 112–121), specifically the clause **"Runtime prompt integration remains blocked"** (line 114).
Authorized by: 总控决策席 gate decision on `issues/048_adr0016_gate_submission_package.md` (option a), 2026-07-07.

## Context

ADR-0016 was approved by 总控决策席 (issues/048, option a). Sub-decision A requires wiring `backend/app/role_context.py` into `prompt_builder.py` / `employee.py` step routing — a runtime prompt integration. This directly conflicts with `knowledge/003_Architecture.md` line 114 ("Runtime prompt integration remains blocked"), an approved Sprint 3 boundary.

Per `reviews/037_redesign_v2_architecture_review_decision.md` and `issues/048`, this conflict must be resolved by a **conscious, recorded supersede — not a silent bypass**. This ADR is that record (the "留痕" required by option a).

## Decision

Lift the runtime-prompt-integration block **only** for the narrow scope of ADR-0016 Sub-decision A (Runtime Role Wiring), effective when `issues/045_runtime_role_wiring_first_slice.md` is the active, gate-approved first-slice issue. All other Sprint 3 Role Context constraints are carried forward and remain in force.

### What is unblocked
- Referencing `role_context.py` from `prompt_builder.py` and the `employee.py` step handoff, using the existing explicit profile-id contract (`curis.role.system-delivery.v1`).
- Adding role-context excerpts as prompt/context guidance to the AI Employee.

### Constraints carried forward (from 003 line 115–121, still in force)
- Explicit issue-declared profile id only; no implicit default profile.
- If no profile id is declared, runtime proceeds without role context.
- Role context must NOT: select tools, route work, create/select agents, mutate workflows, change task state, trigger tasks, alter learning/meta/evolution behavior, change API semantics, or change storage behavior.
- No task evidence attachment, UI selector/dashboard, backend metadata, persistence, new tables, or task-role association is approved.
- Requires a separate approved issue (`issues/045`) with deterministic lookup, compact context excerpt, context-size reduction, fallback behavior, and forbidden-scope scan evidence.

### What remains blocked (unchanged)
- All L5/L6 future-layer scope (company org, ROI/economy, Employee CRUD, multi-agent, business modules, external services) — see ADR-0016 Forbidden Scope and ADR-0017 (future gate).
- Automatic code self-modification without human approval.
- D3 (append-only event log) and D2 (governor sandbox) remain their own separate slices/gates (order D1→D3→D2).

## Consequences
- Easier: role context can become real, constrained runtime behavior per ADR-0016 Sub-decision A.
- Harder: this is the first intentional break of the v0.1 "runtime prompt integration blocked" purity; it is bounded, recorded, and reversible.
- The supersede is explicit and traceable: this ADR is the single record; `003` line 114 is annotated to point here.

## Next Seat
系统交付席 defines D1 (Runtime Role Wiring) architecture boundaries (`docs/decisions/ADR-0019-d1-runtime-role-wiring-boundaries.md`), then 质量运行席 verifies, then 产品规划席 accepts.
