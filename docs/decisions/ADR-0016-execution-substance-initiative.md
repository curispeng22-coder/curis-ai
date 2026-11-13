# ADR-0016: Execution Substance Initiative (Runtime Role Wiring, Governor Sandbox, Append-Only Evolution Log)

Date: 2026-07-07

Status: Accepted (approved by 总控决策席 via issues/048, option a, 2026-07-07)

Related gate: `issues/044_execution_substance_phase_gate.md`

## Context

After v0.1 local/demo release and the post-v0.1 reliability phase, the project has strong governance (gate + ADR + review per change) but thin executable behavior. Three specific debts are now blocking the product's stated trajectory toward a self-evolving AI Company System:

1. **Runtime role is not wired into the execution loop.** `backend/app/role_context.py` exists as a read-only helper using explicit profile id `curis.role.system-delivery.v1`, but it is not referenced by `prompt_builder.py`, `employee.py`, or any step-routing path. Role context is currently dead code from a runtime perspective.

2. **The Evolution Governor cannot actually execute a change.** It produces proposals, simulations, and rollback *records*, but there is no sandbox, permission model, or execution path that lets a controlled proposal be applied and rolled back in practice. "No automatic code self-modification without approval" is preserved, but the *safe execution substrate* was never built. When the product vision demands genuine self-improvement, there is no scaffold to stand on.

3. **Evolution state is mutable, not auditable.** `system_evolution_log`, `evolution_decisions`, `architecture_locks`, `evolution_simulations`, and `rollback_records` are ordinary SQLite tables that can be updated or deleted. For a system whose core claim is controlled self-modification, the audit trail must be append-only and tamper-evident; today it is not.

Trade-off being named: this initiative spends a bounded amount of implementation scope to convert three documentation/record-only capabilities into executable, verifiable ones. We give up strict "no production changes" purity for the v0.1-boundary era, in exchange for de-risking the L5/L6 and true-self-evolution future. All three slices remain *controlled* and *reversible*; none lifts the Stability > Optimization > Evolution policy or the human-approval gate for production mutation.

## Decision

Define an "Execution Substance Initiative" that lands three first slices, each reversible and narrow:

### Sub-decision A — Wire Runtime Role Context into the Execution Loop

Reference `backend/app/role_context.py` from `backend/app/prompt_builder.py` (and the step handoff in `backend/app/employee.py`) using the existing explicit profile-id contract. No implicit default role is introduced. If the profile id is missing or invalid, behavior is unchanged (role context omitted). Role context may only add prompt/context guidance; it must not select tools, route work, change task state, or trigger evolution.

### Sub-decision B — Sandbox the Evolution Governor

Add a controlled execution substrate (sandbox) in which a Stability-first proposal can be *applied and rolled back* against a throwaway copy of the codebase/state, with the result captured as evidence. The sandbox runs locally, writes nothing to the authoritative repo or SQLite, and requires explicit human approval before any production mutation. This converts "governor produces records" into "governor can safely demonstrate a change."

### Sub-decision C — Append-Only Evolution Event Log

Introduce an append-only event log (new table `evolution_events`, or a dedicated append-only store) that records every evolution proposal, simulation, decision, lock, and rollback as immutable events with a correlation id. Mutable tables may remain for query convenience, but the log is the system of record for audit. No existing table is dropped; this is additive.

## Required Preservation (all three slices)

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics (except the additive read/event endpoints this initiative introduces).
- Existing execution behavior (except the three narrow behavior changes above).
- Human approval gate for any production mutation.

## Forbidden Scope

- Lifting the human-approval gate for automatic code self-modification.
- Employee CRUD / employee expansion.
- Multi-agent system or agent abstraction layer.
- Company organization (L5), ROI/economy (L6), business modules.
- Complex UI / dashboard beyond minimal evidence display.
- External services / channels / secrets handling.
- Any change that mutates authoritative repo or SQLite outside the sandbox or the append-only log.

## Consequences

- Easier: role context becomes real behavior; governor can prove a change safely; evolution history is auditable and tamper-evident.
- Easier: the three biggest future blockers (runtime role, governor execution, evolution audit) move from deferred to demonstrable.
- Harder: each slice adds a small, reviewable production-diff surface — the first intentional break from the v0.1 "docs-only" pattern.
- Harder: quality verification must now cover real execution, not just absence of regression.

## First Implementation Slice Recommendation

Recommended order (each as its own gate-approved first slice):

1. `Runtime Role Context Wiring` — Sub-decision A. Lowest risk; pure additive prompt guidance.
2. `Append-Only Evolution Event Log` — Sub-decision C. Additive schema; no behavior change until read endpoints use it.
3. `Evolution Governor Sandbox` — Sub-decision B. Highest value, highest care; must run only on throwaway copies.

## Verification Plan

质量运行席 should verify each slice with the standard diff and forbidden-scope guards plus slice-specific checks:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "Employee CRUD|employee expansion|multi-agent|agent abstraction|company organization|ROI|business module|external channel|dashboard|automatic code self-modification" backend/app docs
```

Plus per slice:

- Slice A: assert `role_context` is imported in `prompt_builder`/`employee`; missing/invalid profile id yields unchanged output.
- Slice C: assert `evolution_events` is insert-only (no UPDATE/DELETE path) and carries a correlation id.
- Slice B: assert sandbox writes only to a throwaway path; zero writes to repo/SQLite under a dry run.

## Next Seat

Approved by 总控决策席 via issues/048 (option a) on 2026-07-07. Boundary verification routes to 质量运行席, then 产品规划席 acceptance, then 系统交付席 implementation per slice in order D1→D3→D2.
