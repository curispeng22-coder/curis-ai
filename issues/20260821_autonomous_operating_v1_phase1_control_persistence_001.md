# CURIS AUTONOMOUS OPERATING V1 — PHASE 1 CONTROL PERSISTENCE

**Issue ID:** `20260821_autonomous_operating_v1_phase1_control_persistence_001`
**Authority Class:** IMPLEMENTATION ISSUE
**Status:** Review
**Disposition:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-21
**Owner:** 主开发 / Runtime Integration
**Parent Issue:** `issues/20260820_autonomous_operating_v1_implementation_001.md`

## 1. Objective

建立 Workspace-scoped Autonomous Operating 的最小持久化控制真相，并只证明：

- Operating Series；
- deterministic Trigger Claim；
- existing `CYCLE` control pins；
- one active Cycle per Series；
- restart truth；
- duplicate/replay idempotency；
- `WAITING / PAUSED / STOPPED` 不会隐式继续。

本 Issue 不证明自主经营已经运行。

## 2. Product → Implementation mapping

| Product truth | Implementation mapping |
|---|---|
| Operating Responsibility | existing Workspace `RESPONSIBILITY_ASSIGNMENT`; Series only references it |
| Operating Series | new minimal `OPERATING_SERIES` control record in existing `runtime_entities` |
| Workspace Goal | current Workspace blueprint/version explicit Goal; no fallback to Business Goal |
| Business Goal | canonical parent constraint/reference from `canonical_businesses` |
| Strategy + Approved Envelope | one immutable versioned strategy/envelope snapshot inside Series control truth |
| Trigger Claim | new minimal `TRIGGER_CLAIM` record in existing `runtime_entities` |
| Operating Cycle | existing `CYCLE`, extended only through control pins in `data_json` |
| Plan / Evaluation | immutable nullable/reference snapshot slots; no Planner/Evaluator |
| Exactly-one active Cycle | `BEGIN IMMEDIATE` reload/check/insert transaction plus deterministic IDs |
| Restart | SQLite records are source of truth; no process-local authority |

## 3. Goal resolution rule

Current Authority establishes separate scopes:

- Workspace Goal is the primary Goal of a Workspace-scoped Operating Series.
- Business Goal is the governing parent direction and is pinned separately.
- Workspace Goal does not inherit/fallback to Business Goal and is not a technical override.
- Missing explicit Workspace Goal fails closed.

No second Goal Store is introduced.

## 4. Exact Allowed Files

| File | Ownership |
|---|---|
| `backend/app/runtime/autonomous_operating.py` | new Phase 1 control persistence service |
| `backend/app/runtime/__init__.py` | minimal public export only; pre-change hash `f1a41315c83c1d58a5ab519c98f643b0cdb84fff` |
| `backend/tests/test_autonomous_operating_phase1.py` | isolated SQLite acceptance/regression |
| `issues/20260821_autonomous_operating_v1_phase1_control_persistence_001.md` | Issue |
| `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE1_CONTROL_PERSISTENCE_REVIEW.md` | Review |

No other source file is allowed without Stop Gate review.

## 5. Explicit exclusions

- no Work release, Router, Employee, Provider, Result, Evidence, Review or Learning execution;
- no ADJUST application and no successor Cycle;
- no Task/Workflow/Employee/Router/Provider/Result/Evidence/Decision duplicate Runtime;
- no API/frontend/CEO Desk/Business/Workspace/Conversation/UI changes;
- no `states.py`, `registry.py`, `foundation.py`, `models.py`, Schema or migration change;
- no Package Method Metadata, generic event engine, threshold engine or autonomous loop;
- no active DB initialization/migration/repair;
- no commit or push before separate Gate.

## 6. Persistence and schema strategy

- Reuse `runtime_entities`, `runtime_links`, canonical Business Spine and existing `CYCLE` rows.
- `OPERATING_SERIES` and `TRIGGER_CLAIM` use explicit service validation because Phase 1 must not expand the global state registry.
- Strategy/Envelope versions live inside the Series snapshot; Cycle pins copy immutable refs/hashes.
- No dedicated table or schema migration.
- If generic persistence cannot guarantee deterministic claim identity or one-active invariant inside one transaction, stop without changing shared schema.

## 7. Transaction boundary

Trigger claim handling uses one SQLite `BEGIN IMMEDIATE` transaction to:

1. reload tenant/Company/Workspace/Series;
2. return an existing deterministic claim on replay;
3. inspect current non-terminal `CYCLE` rows linked to the Series;
4. create or merge the claim;
5. create at most one existing `CYCLE` row only when Series is `ACTIVE`;
6. update Series and links atomically.

No in-memory lock, UI state or process-local set is authoritative.

## 8. Runtime truth contract

### Operating Series

- one deterministic record per tenant + canonical Workspace;
- references canonical Company, Business, Workspace and Leader Assignment;
- pins Workspace Goal and parent Business Goal separately;
- contains one approved Strategy/Envelope version snapshot;
- lifecycle: `ACTIVE / WAITING / PAUSED / STOPPED`;
- stores current/last Cycle refs without implying external execution.

### Trigger Claim

- sources limited to `MANUAL`, `SCHEDULED`, `RESULT`;
- deterministic identity from tenant + Series + source type + source key;
- lifecycle: `CLAIMED / APPLIED / CANCELLED`;
- duplicate/replay returns the same record;
- active Cycle causes merge, not second Cycle;
- `WAITING/PAUSED` retains claim without starting a Cycle;
- `STOPPED` records a cancelled claim and never restarts the Series.

### Existing Cycle extension

The new control-created row remains `entity_type='CYCLE'`, starts `PLANNED`, and pins:

- Series and Trigger Claim refs;
- Workspace and Business Goal refs/versions/hashes;
- Strategy and Envelope refs/versions/hashes/approval provenance;
- Plan and Evaluation reference/snapshot slots;
- predecessor/successor structural slots (`successor = null` in Phase 1).

## 9. Required tests

- Series create and replay;
- invalid Workspace / cross-Company / cross-tenant;
- missing/invalid/non-Leader Assignment;
- explicit Workspace Goal resolution and Business governing Goal pin;
- Strategy version and Envelope approval provenance;
- manual/scheduled/result Trigger Claims;
- duplicate/restart/concurrent replay;
- one-active Cycle and merge;
- different Series/Workspace isolation;
- restart `ACTIVE/WAITING/PAUSED/STOPPED`;
- WAIT/PAUSE/STOP no hidden Cycle/resume;
- existing Runtime import and accepted Responsibility/Cycle primitives no-regression;
- active DB fail-fast environment and before/after fingerprints.

## 10. Stop Gates

Stop on:

- inability of `runtime_entities/runtime_links` to carry the invariant;
- need for shared Schema/migration/state registry changes;
- Goal or Strategy/Envelope ownership ambiguity;
- inability to resolve canonical Leader Assignment;
- inability to guarantee one-active Cycle transactionally;
- Product Authority conflict;
- active DB contact or destructive Git action;
- commit/push gate.

## 11. Acceptance state

Implementation evidence is recorded in
`docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE1_CONTROL_PERSISTENCE_REVIEW.md`.

```text
PHASE 1 IMPLEMENTED / REVIEW REQUIRED
NO EMPLOYEE EXECUTION
NO LEARNING
NO SUCCESSOR CREATION
NO COMMIT / NO PUSH
```
