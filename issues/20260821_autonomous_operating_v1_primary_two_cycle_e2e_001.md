# CURIS AUTONOMOUS OPERATING V1 — PRIMARY TWO-CYCLE E2E

**Issue ID:** `20260821_autonomous_operating_v1_primary_two_cycle_e2e_001`
**Authority Class:** IMPLEMENTATION ISSUE
**Status:** Review
**Disposition:** IMPLEMENTED / CEO REVIEW REQUIRED
**Date:** 2026-08-21
**Baseline:** `86405404dd16e32b131fff8aa0008d8d11ea6961`

## Goal

Prove one real Domain Workspace can complete two full bounded operating cycles
without CEO per-task dispatch:

```text
Operating Series → Cycle 1 real Team Operating / Employee / Provider execution
→ Result / Artifact / Evidence / Acceptance → Evaluation / Leader Decision
→ decision-authorized Cycle 2 → distinct Plan / execution / Result / Evidence
→ Acceptance / Evaluation / Leader Decision → stop with exactly two Cycles
```

This is a Runtime proof. It does not add a Domain, workflow, employee, provider,
result, evaluation or decision system.

## Domain Readiness Audit

| Capability | RD | XHS |
|---|---|---|
| Canonical Company / Department / Business / Workspace | READY | READY |
| Workspace Leader / Responsibility Assignment | READY | READY |
| Existing Team Operating definition and routing | READY | PARTIAL |
| Employee and capability binding | READY | READY |
| Provider Task / Session | READY WITH BOUNDED FIXTURE | PARTIAL |
| ResultStore / Artifact / Evidence / Acceptance | READY | PARTIAL |
| Domain result semantics | code/test result contract exists | ContentItem exists; publish/analytics connectors are not connected |
| Two-cycle Plan source | versioned bounded RD Plan can reuse the accepted Operating Definition | no accepted Autonomous Plan-to-ContentItem result bridge |
| Restart / replay | READY | domain persistence READY; autonomous cross-cycle proof absent |
| Primary Proof status | **READY WITH BOUNDED FIXTURE** | **BLOCKED** |

## Selected Primary Domain

**RD** is selected because its accepted Workspace contract already has a safe
execution subject, canonical Employee, capability binding, Provider Task/Session,
Artifact, test Evidence and failure truth. The proof uses an isolated RD Workspace
and a deterministic controlled Provider; it does not modify production code or a
real repository.

XHS is not selected because completing this proof would require a new accepted
bridge between Autonomous Plan/Result truth and the XHS `ContentItem` lifecycle.
Real publishing and analytics remain unavailable. This does not reject XHS as a
future Cross-domain proof.

## Exact Scope and Allowed Files

1. `backend/tests/test_autonomous_operating_primary_two_cycle_e2e.py`
2. `issues/20260821_autonomous_operating_v1_primary_two_cycle_e2e_001.md`
3. `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PRIMARY_TWO_CYCLE_E2E_REVIEW.md`

No existing Runtime, Schema, API, frontend, RD, XHS or shared file may change.
If the proof requires such a change, stop and report the exact architecture gap.

## Proof Scenario

- Create a real canonical RD Workspace through `WorkspaceRuntime` in an isolated
  SQLite database.
- Materialize one canonical Workspace Leader Employee, assignment, capability
  binding and existing Team Operating definition.
- Use one approved Strategy/Envelope and a bounded Cycle-1 RD Plan.
- Execute Cycle 1 through the existing Employee/Provider bridge and close it with
  real ResultStore Task, Artifact, Evidence and Acceptance.
- Evaluate Cycle 1 and apply a Leader `CONTINUE` decision.
- Restart, authorize the same deterministic successor, and materialize a distinct
  Cycle-2 Plan containing predecessor Result/Evidence/Evaluation/Decision refs.
- Execute and close Cycle 2, evaluate it, and record a final `WAIT` decision.
- Do not authorize a third successor.

## Fixture Boundary

- Repository-external SQLite only.
- The RD Workspace, Company hierarchy, Employee, Assignment, workflow, Provider
  Task, Session, Artifact, Evidence and decisions are real Runtime objects.
- The Provider is deterministic and local so the proof has no production code,
  account, cost or external side effect. It is not claimed as an external live
  model quality proof.
- CEO authority is limited to the already approved Strategy, Envelope, Plan and
  Acceptance gates. CEO does not create Employee Tasks, start Provider sessions,
  hand off work or close cycles one step at a time.

## Two-Cycle Contract

- Cycle 1 and Cycle 2 have different IDs, Trigger Claims, Plan versions, Provider
  Tasks, Sessions, Artifacts, Evidence, Acceptance, Evaluation, Review and Decision.
- Cycle 2 pins Cycle 1, its Decision, Result/Evidence and observation window as
  predecessor context.
- Cycle 1 historical pins and evaluation remain immutable.
- Cycle 2 ends with a canonical Decision but no Cycle 3 is authorized.
- No Learning, Knowledge, Memory or Strategy self-evolution is produced.

## Failure Matrix

| Case | Required truth |
|---|---|
| Cycle-2 Provider failure | Cycle 2 fails closed; Cycle 1 truth remains; no Cycle 3/Learning |
| Cycle-2 invalid Result | incomplete output is not accepted; evidence is not fabricated |
| missing capability | no Cycle-2 Provider Task starts |
| unavailable Employee | no Cycle-2 Provider Task starts |
| restart after Cycle-1 Decision | same deterministic Cycle 2 |
| restart after Cycle-2 Work release | no duplicate Work |
| restart after Cycle-2 Provider result | no duplicate Result/Artifact |
| duplicate callback / evaluation / review | same objects; no duplicate Decision or successor |

## DB Safety

`CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` must point to the same
repository-external SQLite before import. Both repository active databases must
retain size, mtime, SHA-256 and `integrity_check=ok` before and after.

## Stop Gates

Stop immediately if: RD cannot provide a valid Plan source; a new Domain or
shared Runtime primitive is required; Employee/Result truth must be faked; an
active database would be touched; Cycle 3 is created; Learning is promoted; or
the accepted Phase 1–3B contract conflicts with the proof.

## Acceptance

1. One Operating Series and exactly two Cycles.
2. Both Cycles execute through real Team Operating, Employee and Provider objects.
3. Both produce distinct ResultStore Tasks, Sessions, Artifacts, Evidence and Acceptance.
4. Both produce evidence-bound Evaluation, canonical Leader Review and Decision.
5. Cycle 2 is uniquely authorized by Cycle-1 Decision and consumes predecessor context.
6. Restart/replay and duplicate calls do not create duplicate Work, Result or Decision.
7. Required Cycle-2 failures fail closed.
8. No CEO per-task dispatch, Cycle 3 or Learning.
9. Active databases remain unchanged.
10. Existing Phase 1–3B, Team Operating, RD and XHS regressions pass.
