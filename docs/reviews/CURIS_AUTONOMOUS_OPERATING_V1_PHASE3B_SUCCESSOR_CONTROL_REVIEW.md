# CURIS AUTONOMOUS OPERATING V1 — PHASE 3B REVIEW
## SUCCESSOR AUTHORIZATION / EXACTLY-ONE NEXT CYCLE

**Authority Class:** REVIEW
**Status:** Review
**Disposition:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-21
**Issue:** `issues/20260821_autonomous_operating_v1_phase3b_successor_control_001.md`
**Baseline HEAD:** `50d058ca865c1817721536d7beb47a1c5f1f354d`

## 1. Implemented control chain

```text
Cycle 1 CLOSED
→ Phase 3A evidence-bound Evaluation / Leader Review
→ canonical applied CONTINUE or bounded ADJUST DECISION_PACKET
→ deterministic authorized existing TRIGGER_CLAIM
→ exactly one existing Cycle 2 (PLANNED / NOT_STARTED)
```

Decision is the only successor authority. Result arrival, callback, scheduler,
Employee, Provider, UI and Cycle close cannot create Cycle 2 independently.

## 2. Authority and trigger behavior

- The first Cycle remains compatible with the accepted Phase 1 three trigger
  types.
- Once a Series owns a closed `lastCycleRef` and has no active Cycle, any new
  Trigger Claim requires an applied canonical `CONTINUE / ADJUST` Decision.
- Successor authorization uses a deterministic existing `RESULT`
  `TRIGGER_CLAIM` whose source key is the Decision ID.
- While an authorized successor is already active, later ordinary trigger
  signals may merge into that existing Cycle; they cannot create another Cycle.
- Reusing the same Decision with any replay returns its recorded canonical
  Claim/Cycle.

## 3. CONTINUE evidence

Verified:

- one applied `CONTINUE` created exactly one `CYCLE`;
- Cycle 2 inherited canonical Company, Business, Workspace, Series, Leader,
  Goal, Strategy and Approved Envelope truth;
- Cycle 2 recorded the predecessor Cycle and predecessor Decision;
- Series remained `ACTIVE`, with `currentCycleRef=Cycle 2` and
  `lastCycleRef=Cycle 1`;
- no Task, Employee execution or Provider Session was created for Cycle 2.

## 4. bounded ADJUST evidence

Phase 3A's approved adjustment keys are rechecked against the same approved
Envelope before successor creation.

- a deterministic adjusted Strategy version is appended to Series history;
- its body is the prior immutable Strategy plus the bounded changes;
- it records the authorizing Decision;
- Cycle 2 pins that adjusted Strategy and the unchanged approved Envelope;
- Cycle 2 Plan remains `UNRESOLVED`, with predecessor Decision and required
  changes recorded; no Plan is fabricated;
- Cycle 1 Strategy, Envelope, Plan, Evaluation and Review pins remain unchanged.

Protected/unknown changes fail closed and create no Claim/Cycle.

## 5. Lineage and atomic persistence

The same SQLite `BEGIN IMMEDIATE` transaction persists:

1. deterministic successor Trigger Claim;
2. existing Cycle 2;
3. Cycle 1 `successorCycleRef`;
4. Cycle 2 `predecessorCycleRef` and `predecessorDecisionRef`;
5. Decision `successorTriggerClaimRef` and `successorCycleRef`;
6. Series current/last refs and adjusted Strategy version when applicable;
7. existing Runtime links.

An injected interruption during this transaction rolled back the Claim, Cycle
and lineage together. Retry then created one canonical successor.

Concurrent authorization was serialized by persistent SQLite truth, not an
in-memory lock: two calls returned one Cycle ID, with one `created=true` and one
replay.

## 6. Non-successor decisions

| Decision | Packet/Series truth | Successor |
|---|---|---|
| `WAIT` | applied Packet; Series `WAITING`; reason and `nextCheckAt` retained | none |
| `ESCALATE` | Packet `WAITING_CEO`; Series `WAITING` | none |
| `PAUSE` | CEO-applied Packet; Series `PAUSED` | none |
| `STOP` | CEO-applied Packet; Series `STOPPED` | none |

Scheduled triggers in `WAITING / PAUSED` remain unapplied Claims. A trigger in
`STOPPED` is cancelled. None revives the Series or creates a Cycle. No Resume
Product Flow or Event Engine was added.

## 7. Failure and restart truth

Verified fail-closed:

- closed Cycle with no Decision;
- unapplied `CONTINUE / ADJUST` Decision;
- stale Decision Strategy version;
- stale Decision Envelope version;
- same-version mutated Strategy/Envelope hash;
- invalid adjusted keys;
- non-`ACTIVE` Series;
- unrelated active Cycle;
- cross-tenant Decision access;
- duplicate and concurrent successor apply;
- transaction interruption.

Restart after Decision, after atomic Claim/Cycle creation and after successor
creation returned the same Decision, Claim, Cycle and lineage. Atomic creation
means no durable intermediate state exists where a successor Claim is committed
without its Cycle and lineage.

## 8. Required answers

1. **successor 的唯一 authority 是什么？** The canonical applied Phase 3A `DECISION_PACKET`.
2. **CONTINUE 是否创建 exactly-one successor？** Yes.
3. **bounded ADJUST 是否创建 successor？** Yes, after Envelope revalidation.
4. **adjusted pins 是否正确进入 Cycle 2？** Yes; adjusted Strategy and unresolved adjusted Plan control are pinned.
5. **predecessor 是否保持 immutable？** Yes, except its required lineage field `successorCycleRef`.
6. **lineage 是否双向成立？** Yes.
7. **WAIT 是否不创建 successor？** Yes.
8. **ESCALATE 是否真正阻塞？** Yes; Packet/Series remain waiting.
9. **PAUSE 是否不会偷偷恢复？** Yes.
10. **STOP 是否不会被普通 Trigger 复活？** Yes.
11. **是否复用 Trigger Claim？** Yes, deterministic existing `TRIGGER_CLAIM`.
12. **是否复用 existing CYCLE？** Yes; no `AUTONOMOUS_CYCLE` exists.
13. **single-active invariant 是否仍成立？** Yes.
14. **restart 是否不重复 Cycle 2？** Yes.
15. **是否生成 Learning？** No.
16. **是否形成 two-cycle control proof？** Yes, for `CONTINUE` and bounded `ADJUST`.
17. **下一 Phase 真正剩什么？** Learning acceptance/promotion boundaries and, when separately authorized, executing/closing the second Cycle as a longer autonomous E2E. Neither is Phase 3B.

## 9. Tests

All tests used one repository-external SQLite assigned to `CURIS_DB`,
`CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` before import.

```text
Phase 3B focused successor matrix
15 passed in 6.27s

Phase 1 + Phase 2 + Phase 3A + Phase 3B
+ RD P7 Decision
+ Team Operating real Employee E2E
+ Backend DB Safety
59 passed in 20.10s

Python py_compile
PASS

git diff --check (owned tracked file)
PASS
```

## 10. Active DB safety

Final values equal the Phase 3B pre-change and prior accepted baselines:

| Path | Size | mtime | SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

## 11. Changed files and Git boundary

1. `backend/app/runtime/autonomous_operating.py`
2. `backend/tests/test_autonomous_operating_phase3b.py`
3. `issues/20260821_autonomous_operating_v1_phase3b_successor_control_001.md`
4. this Review

Post-change hashes:

- `autonomous_operating.py`: `5ab0b0a7b94895b201e317370ed07e44203541f9ebf3bcd9c8b8fc2007f11de6`
- `test_autonomous_operating_phase3b.py`: `6e6086217c6ba853dc523f5b570beb9c07f6d633c60224ff88f180850167466b`

No file was staged, committed or pushed. Phase 1–3B remain one accepted-but-
uncommitted dependency chain pending the explicitly requested bounded commit
reconciliation after CEO review.

## 12. Explicitly not implemented

- Learning / Knowledge / Memory promotion;
- second-Cycle Employee/Provider execution;
- Resume Product Flow;
- generic Event Engine;
- API/UI changes;
- external live-provider quality/cost proof.

```text
CURIS AUTONOMOUS OPERATING V1
— PHASE 3B SUCCESSOR CONTROL IMPLEMENTED
— DECISION IS SOLE SUCCESSOR AUTHORITY
— CONTINUE / BOUNDED ADJUST SUCCESSOR VERIFIED
— WAIT / ESCALATE / PAUSE / STOP BLOCK VERIFIED
— EXISTING TRIGGER CLAIM / CYCLE REUSED
— EXACTLY-ONE / LINEAGE / TRANSACTION VERIFIED
— TWO-CYCLE CONTROL PROOF COMPLETE
— NO LEARNING PROMOTION
— ACTIVE DB UNCHANGED
— REVIEW REQUIRED
```
