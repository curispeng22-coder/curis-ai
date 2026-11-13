# ADR-0012: Evolution Decision Evidence Reliability Boundaries

Date: 2026-07-06

Status: Proposed for quality verification

Related gate: `issues/031_evolution_decision_evidence_reliability_gate.md`

Related reliability phase: `docs/decisions/ADR-0010-post-v0.1-execution-reliability-boundaries.md`

## Context

AI Task Executor MVP v0.1 is released as the first local/demo version. Post-v0.1 reliability work is strengthening the existing L1-L4 execution base without opening future AI Company System layers.

Run Evidence Reliability and Workflow Error/Fallback Evidence Map are implemented, verified, and accepted.

The next reliability area is evidence for existing Evolution Governor decisions and stability-first behavior.

Current implementation surfaces already include:

- `EvolutionGovernor.evaluate`, which computes failure rate, latency increase, workflow inefficiency, threshold matches, proposal, risk analysis, and final decision.
- Decision outcomes: `do_not_evolve`, `evolve`, and `postpone_evolution`.
- Stability policy order: `STABILITY`, `OPTIMIZATION`, `EVOLUTION`.
- `automatic_code_modification_allowed=False` on stored decisions.
- Existing simulation evidence through `ResultStore.save_evolution_simulation`.
- Existing rollback evidence through `ResultStore.save_rollback_record`.
- Existing lock-risk evidence through architecture locks and `risk_analysis.locked_module_risk`.
- API evidence through `/api/task/{task_id}/evolution-decisions`.
- Existing backend tests for threshold rejection, controlled proposal generation, locked-module postponement, and evolution-decision API response.

This boundary does not approve implementation. It defines what a later implementation slice may verify or clarify.

## Decision

Define Evolution Decision Evidence Reliability as a bounded architecture slice over existing Evolution Governor behavior and evidence.

The slice must preserve:

- AI Task Executor MVP v0.1 local/demo release.
- Tool System v1.8 loop.
- Stability > Optimization > Evolution policy.
- Chinese operation console.
- Task API payload `{ content }`.
- Existing API semantics.
- Existing persistence schema.
- Existing Evolution Governor behavior.
- Existing architecture locking behavior.
- Existing rollback record behavior.
- Project Memory, Role Profiles, Role Context, release record/tag semantics, and source-of-truth ownership.

## Boundary Areas

### 1. Do-Not-Evolve Evidence

Allowed:

- Verify that a stable execution records `do_not_evolve`.
- Verify that no proposal is stored when thresholds are not met.
- Verify that threshold evaluation is visible and empty.
- Verify that automatic code modification remains false.

Not allowed:

- Changing thresholds.
- Changing decision semantics.
- Adding automatic evolution behavior.

### 2. Controlled Proposal Evidence

Allowed:

- Verify that threshold-triggered inefficiency records an approval-gated proposal.
- Verify that simulation evidence includes task flow, tool routing, workflow graph, and performance impact.
- Verify that rollback evidence includes previous architecture, stable version, and performance comparison.
- Verify that proposal evidence never implies automatic application.

Not allowed:

- Applying proposals automatically.
- Mutating architecture.
- Changing workflow generation behavior through this slice.

### 3. Postpone And Lock Evidence

Allowed:

- Verify that locked-module risk leads to `postpone_evolution`.
- Verify that locked modules are visible in risk analysis.
- Verify that architecture locks remain source-of-truth records, not runtime role or employee records.

Not allowed:

- Unlocking locked modules.
- Changing architecture lock semantics.
- Adding role, employee, department, or company-organization behavior.

### 4. Operator-Readable Evidence Map

Allowed:

- Define a deterministic evidence map from one execution to existing decision, simulation, rollback, threshold, proposal, risk, and API surfaces.
- Classify missing or weak evidence as stabilization, verification, documentation, or future product scope.
- Document which existing API or store method owns each evidence surface.

Not allowed:

- Adding a dashboard.
- Adding UI complexity.
- Adding external monitoring services.
- Adding future L5/L6 product-layer concepts.

## First Implementation Slice Recommendation

Recommended first slice after quality verification and product acceptance:

`Evolution Decision Evidence Map`.

Scope should be limited to backend tests and documentation/evidence around existing behavior:

- Stable execution records do-not-evolve evidence.
- Threshold-triggered execution records controlled proposal, simulation, and rollback evidence.
- Locked-module path records postpone-evolution risk evidence.
- Evolution-decision API returns decision, simulation, and rollback evidence.
- No API semantic change, persistence/schema change, UI change, external service, new execution behavior, automatic evolution behavior change, or future-layer scope.

## Verification Plan

质量运行席 should verify this boundary with:

```bash
git diff --name-only HEAD -- backend frontend
git diff --check
rg -n "ROI|business module|Employee CRUD|employee expansion|company organization|department|reporting line|staffing|multi-agent|agent abstraction|external channel|dashboard|API semantic change|persistence/schema change|new table|new execution behavior|automatic evolution behavior change|code self-modification|architecture mutation|unlocking locked modules|external service|task-role association|task evidence attachment|future-layer" docs/decisions/ADR-0012-evolution-decision-evidence-reliability-boundaries.md issues/031_evolution_decision_evidence_reliability_gate.md issues/032_evolution_decision_evidence_reliability_boundaries.md reviews/028_evolution_decision_evidence_reliability_boundaries_review.md
```

Expected result:

- No backend/frontend implementation diff.
- Diff hygiene passes.
- Forbidden terms appear only as explicit forbidden or preserved-scope text, not as allowed implementation work.

## Consequences

- This ADR does not approve implementation.
- The next seat is 质量运行席 for architecture-boundary verification.
- If accepted, 产品规划席 may open a separate first implementation issue.
- Any later implementation must preserve existing API semantics, persistence schema, UI scope, Evolution Governor behavior, architecture lock semantics, rollback semantics, automatic-evolution constraints, and future-layer boundaries.
