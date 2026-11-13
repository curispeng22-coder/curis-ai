# CURIS AUTONOMOUS OPERATING V1 — PHASE 1 CONTROL PERSISTENCE REVIEW

**Authority Class:** REVIEW
**Status:** Review
**Disposition:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-21
**Issue:** `issues/20260821_autonomous_operating_v1_phase1_control_persistence_001.md`
**Baseline HEAD:** `50d058ca865c1817721536d7beb47a1c5f1f354d`

## A. Exact Allowed Files

Only the following five files were changed or created:

1. `backend/app/runtime/autonomous_operating.py`
2. `backend/app/runtime/__init__.py`
3. `backend/tests/test_autonomous_operating_phase1.py`
4. `issues/20260821_autonomous_operating_v1_phase1_control_persistence_001.md`
5. `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE1_CONTROL_PERSISTENCE_REVIEW.md`

The worktree contained substantial preserved unrelated changes before this Issue. They were not reset, cleaned, staged or absorbed. Staged file count remains zero.

## B. Product → Implementation Mapping

| Required truth | Implemented truth |
|---|---|
| Operating Responsibility | References an existing active Workspace Leader `RESPONSIBILITY_ASSIGNMENT` and its canonical `AI_EMPLOYEE` |
| Operating Series | Deterministic `OPERATING_SERIES` record in existing `runtime_entities` |
| Workspace Goal | Explicit Workspace blueprint Goal pin; missing Goal fails closed |
| Business Goal | Separate governing-direction pin from canonical Business |
| Strategy / Envelope | Approved version, body hash and approval provenance persisted in Series |
| Trigger Claim | Deterministic `TRIGGER_CLAIM` for `MANUAL / SCHEDULED / RESULT` |
| Operating Cycle | Existing `entity_type='CYCLE'`, initially `PLANNED`; no parallel Cycle model |
| Plan / Evaluation | Honest unresolved/reference pin slots only; no Planner/Evaluator |
| One active Cycle | SQLite `BEGIN IMMEDIATE` transaction plus active-Cycle recheck and deterministic identity |
| Restart | SQLite is authoritative; no process-local lifecycle state |

## C. Operating Series Contract

- One deterministic Series per tenant + canonical Workspace.
- Canonical Company, Business and resolved Workspace are validated before insert.
- Owner is an existing active Workspace Leader Assignment backed by a real `AI_EMPLOYEE`.
- Lifecycle is limited to `ACTIVE / WAITING / PAUSED / STOPPED`.
- A duplicate create with identical truth returns the same Series.
- A duplicate create with changed canonical strategy/envelope truth fails closed instead of silently replacing history.
- `STOPPED` is terminal. State transition is rejected while an active Cycle exists.

## D. Trigger Claim Contract

- Claim ID is derived from tenant + Series + source type + stable source key.
- Same trigger replay returns the same persisted Claim.
- A new trigger against an active Cycle is linked to that Cycle; it does not create a second Cycle.
- `WAITING / PAUSED` stores a `CLAIMED` trigger without creating a Cycle.
- `STOPPED` stores a `CANCELLED` trigger with `SERIES_STOPPED`; it does not restart.
- An unapplied Claim can be explicitly cancelled and remains cancelled after restart.

## E. Existing Cycle Extension

The implementation creates only the existing `CYCLE` entity type. Its `data.autonomousControl` contains control pins and `controlOnly=true`; execution starts as `NOT_STARTED`. No Task, Work, Employee execution, Router wake-up, Provider session, Result, Artifact or Evidence is created.

The Phase 1 Cycle records `predecessorCycleRef` and an explicit `successorCycleRef=null`. Closing a fixture Cycle does not stop the Series and does not create a successor.

## F. Goal / Strategy / Envelope Pinning

- Workspace Goal and Business Goal remain different scopes.
- Workspace Goal is required and never falls back to the Business Goal.
- Business Goal is pinned only as `GOVERNING_DIRECTION`.
- Strategy and Approved Envelope include version, body hash, approval actor and approval time.
- Plan/Evaluation remain `UNRESOLVED` unless an explicit reference pin is supplied.

## G. Single-active Transaction Invariant

`claim_trigger()` opens one SQLite `BEGIN IMMEDIATE` transaction before reading Series/Claim/Cycle truth. Within that transaction it replays an existing Claim, checks active Cycles, creates or merges the Claim, and creates at most one Cycle. A two-thread isolated SQLite test with distinct triggers produced two Claims and one shared active Cycle.

No process-local mutex, cache or UI state is authoritative.

## H. Restart Truth

Fresh service instances reopened the same isolated SQLite and preserved all four Series states. Trigger behavior after restart remained state-correct:

- `ACTIVE` → applied Claim + one Cycle;
- `WAITING / PAUSED` → claimed only, no Cycle;
- `STOPPED` → cancelled Claim, no Cycle.

Persistence does not imply Employee or Provider execution.

## I. WAIT / PAUSE / STOP Truth

- `WAITING` requires an explicit next-check time.
- `WAITING / PAUSED` do not secretly continue.
- `STOPPED` cannot transition back to another state.
- None of these states creates a Cycle merely because a trigger is observed.
- Series state cannot change while an active Cycle exists, preventing contradictory control truth.

## J. Isolated SQLite Evidence

Focused acceptance used repository-external temporary SQLite paths with all three variables aligned: `CURIS_DB`, `CURIS_DB_PATH`, `CURIS_WORKSPACE_DB`.

Final focused result:

```text
backend/tests/test_autonomous_operating_phase1.py
11 passed in 1.17s
```

An additional runtime evidence database was created at a temporary `/tmp` path. It showed:

- two canonical Workspaces → two independent Series;
- one active Series receiving manual + scheduled Claims → one Cycle, replay/merge true;
- one waiting Series receiving a result Claim → Claim persisted, no Cycle;
- entity counts: `OPERATING_SERIES=2`, `TRIGGER_CLAIM=3`, `CYCLE=1`;
- no Result/Evidence/Artifact/Task side effects;
- `integrity_check=ok`.

## K. Active DB Safety

Both repository active SQLite files are byte-identical to their pre-change fingerprints:

| Path | Size | mtime | SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

The first malformed final-test invocation omitted two required isolated variables. The existing DB safety guard rejected the import before initialization; the corrected invocation then passed.

## L. Existing Runtime Regression

```text
Responsibility Routing
Team Operating Real Employee E2E
Runtime Operating Cycle
Scheduler
Canonical Business Spine Runtime
27 passed

Backend Test DB Safety
3 passed

Python compileall
PASS

git diff --check
PASS
```

No shared Schema, state registry, foundation, model, Workspace router, API or frontend file was changed.

## M. Remaining Phase 2 Gaps

Intentionally not implemented:

- Work release and Employee/Provider execution;
- Router wake-up and continuation;
- Result/Evidence collection and evaluation;
- `CONTINUE / ADJUST / WAIT / ESCALATE / PAUSE / STOP` decision application;
- successor Cycle creation;
- Learning and strategy evolution;
- API/UI projection;
- external live Provider quality/cost evidence.

These are later bounded phases, not Phase 1 defects.

## N. Commit Recommendation

No files are staged and no commit or push was made. After CEO Review, this exact five-file scope is suitable for one bounded commit. The preserved unrelated worktree must remain excluded.

## O. Direct Acceptance Answers

1. **Does Operating Series persist?** Yes, in existing `runtime_entities`.
2. **Is it Workspace-scoped?** Yes, with canonical Company/Business/Workspace validation.
3. **Is the Leader real?** Yes, an existing active Leader Assignment backed by `AI_EMPLOYEE`.
4. **Are Workspace and Business Goals conflated?** No; they are separately pinned.
5. **Is Strategy approved and versioned?** Yes, with hash and approval provenance.
6. **Are claims deterministic?** Yes.
7. **Are manual/scheduled/result sources supported?** Yes.
8. **Can replay create duplicate claims?** No.
9. **Can concurrent triggers create two active Cycles?** The isolated concurrency test says no.
10. **Is a new Cycle primitive introduced?** No; existing `CYCLE` is used.
11. **Does WAITING start work?** No.
12. **Does PAUSED start work?** No.
13. **Can STOPPED restart implicitly?** No.
14. **Does persistence imply execution?** No.
15. **Does Cycle close stop Series?** No.
16. **Is a successor created?** No.
17. **Are Employee/Provider/Result/Evidence paths invoked?** No.
18. **Does restart preserve control truth?** Yes.
19. **Were active databases modified?** No, verified by size/mtime/SHA/integrity.
20. **Was code committed or pushed?** No.

```text
CURIS AUTONOMOUS OPERATING V1
— PHASE 1 MINIMAL CONTROL PERSISTENCE IMPLEMENTED
— OPERATING SERIES PERSISTED
— TRIGGER CLAIM DETERMINISTIC
— ONE ACTIVE CYCLE ENFORCED
— RESTART / WAIT / PAUSE / STOP TRUTH VERIFIED
— NO EMPLOYEE EXECUTION
— NO LEARNING
— NO SUCCESSOR CREATION
— REVIEW REQUIRED
```
