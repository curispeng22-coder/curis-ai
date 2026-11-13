# CURIS AUTONOMOUS OPERATING V1 — PHASE 2 SINGLE-CYCLE EXECUTION

**Issue ID:** `20260821_autonomous_operating_v1_phase2_single_cycle_execution_001`
**Authority Class:** IMPLEMENTATION ISSUE
**Status:** Review
**Disposition:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-21
**Parent:** `issues/20260821_autonomous_operating_v1_phase1_control_persistence_001.md`

## Goal

Prove one bounded Workspace-scoped chain:

`canonical Trigger Claim → existing CYCLE → existing Team Operating Work → real Employee/Provider Task+Session → existing Result/Artifact/Evidence → existing Acceptance → CLOSED Cycle`.

Series remains active. No Learning, next-cycle decision or successor is allowed.

## Reuse contract

- Existing `CYCLE` is also the Team Operating Work; no autonomous Work/Task is created.
- Existing `RESPONSIBILITY_WORKFLOW`, Assignment, Router and Employee execution bridge own execution.
- Existing ResultStore Task/Artifact and verified callback event own result/evidence truth.
- Existing `EVIDENCE` and `ACCEPTANCE` entities own acceptance-compatible close.

## Exact Allowed Files

1. `backend/app/runtime/autonomous_operating.py`
2. `backend/tests/test_autonomous_operating_phase2.py`
3. `issues/20260821_autonomous_operating_v1_phase2_single_cycle_execution_001.md`
4. `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE2_SINGLE_CYCLE_EXECUTION_REVIEW.md`

No other source file may change without a new Stop Gate.

Pre-change hash of the only existing owned source:

`backend/app/runtime/autonomous_operating.py` = `9452a1fc7829c831e145b68d8f21c4fdca4589192a422b0b23590cf7c181fb8c`.

## Explicit exclusions

- no second Task/Work/Router/Employee/Provider/Result/Evidence runtime;
- no Planner, Evaluation, Learning or Strategy mutation;
- no next-cycle Decision application;
- no successor Cycle;
- no API, frontend or UI;
- no shared Schema/state registry/Foundation/Team Operating/Router/main.py/ResultStore modification;
- no RD/XHS domain change;
- no active database;
- no stage, commit or push.

## Runtime gates

Before release, require current canonical Workspace/Business, active Series, intact Goal/Strategy/Envelope/Claim/Cycle pins, current valid Leader Assignment, one pinned Workspace workflow, active Employee capability grants, available Provider capability, no active conflicting execution and one approved bounded Plan.

Missing capability and missing employee permission are separate fail-closed outcomes using existing capability/binding truth.

## Acceptance

- valid Trigger starts the same existing Cycle as existing Team Operating Work;
- real Leader, Assignment, Router, Employee identity, Provider Task/Session and callback provenance;
- existing Result/Artifact plus persisted Evidence and Acceptance references;
- Cycle closes through the existing lifecycle; Series stays `ACTIVE`;
- replay/restart creates no duplicate Cycle/Work/Task/Result/Evidence;
- Router/Employee/Provider/capability/permission/partial/interrupted failure remains fail-closed;
- cross-tenant fails closed;
- Phase 1 and accepted Team Operating regressions pass;
- active SQLite fingerprints remain unchanged.

Evidence: `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE2_SINGLE_CYCLE_EXECUTION_REVIEW.md`.

```text
PHASE 2 IMPLEMENTED / REVIEW REQUIRED
NO LEARNING
NO NEXT-CYCLE DECISION
NO SUCCESSOR
NO COMMIT / NO PUSH
```
