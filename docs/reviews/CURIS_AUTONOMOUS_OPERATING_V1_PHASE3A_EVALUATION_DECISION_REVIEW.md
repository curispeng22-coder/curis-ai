# CURIS AUTONOMOUS OPERATING V1 — PHASE 3A REVIEW
## EVALUATION / LEADER REVIEW / NEXT-CYCLE DECISION TRUTH

**Authority Class:** REVIEW
**Status:** Review
**Disposition:** IMPLEMENTED / ACCEPTED
**Date:** 2026-08-21
**Issue:** `issues/20260821_autonomous_operating_v1_phase3a_evaluation_decision_001.md`
**Baseline HEAD:** `50d058ca865c1817721536d7beb47a1c5f1f354d`

## 1. Implemented vertical truth

```text
existing CLOSED Cycle
+ existing completed Provider Task Result
+ existing Artifact / verified Evidence / closed Acceptance
+ approved versioned Evaluation Contract pin
→ persisted evidence-bound Evaluation
→ same canonical Workspace Leader Assignment / Employee Review
→ exactly one existing DECISION_PACKET
→ CONTINUE / ADJUST / WAIT / ESCALATE / PAUSE / STOP truth
```

Phase 3A creates no successor Cycle and promotes no Learning, Knowledge or
Strategy version.

## 2. Minimal runtime model

No Schema and no new global Runtime entity type were added.

- Evaluation Contract: approved/versioned/hash-pinned data on the existing
  Operating Series and closed Cycle.
- Evaluation: one deterministic Cycle-scoped persisted record containing the
  Cycle, Result, Evidence, Acceptance, Goal, Strategy, Envelope, observed facts,
  comparison, confidence, sufficiency and outcome.
- Leader Review: one deterministic Cycle-scoped persisted record resolving the
  existing canonical Workspace Leader Assignment and Employee.
- Decision: one deterministic existing `DECISION_PACKET` per closed Cycle.
- Decision replay: same input returns the same Packet; different input fails
  closed.

This is a thin extension of the accepted control plane. It is not an
Evaluation Engine, Review Engine, Learning Engine, Workflow Engine or second
Decision system.

## 3. Decision and authority evidence

| Requested truth | Runtime result |
|---|---|
| `CONTINUE` | Leader applies existing Packet; Series stays `ACTIVE` |
| bounded `ADJUST` | Envelope keys verified; Leader applies existing Packet; Series stays `ACTIVE` |
| out-of-envelope `ADJUST` | canonical choice becomes `ESCALATE`; Packet `WAITING_CEO`; Series `WAITING` |
| `WAIT` | reason + `nextCheckAt` required; Leader applies Packet; Series `WAITING` |
| `ESCALATE` | Packet `WAITING_CEO`; no hidden continuation; Series `WAITING` |
| `PAUSE` | Leader proposal cannot pause; same Packet waits CEO; CEO application moves Series to `PAUSED` |
| `STOP` | Leader proposal cannot stop; same Packet waits CEO; CEO application moves Series to `STOPPED` |

Current Product Contract allows `PAUSE` only for CEO or an explicitly
authorized Leader, and `STOP` only for CEO or an explicitly authorized terminal
policy. No such extra policy was assumed. CEO application is persisted in the
Packet transition log and Packet data; no Leader terminal authority is forged.

The shared Decision state machine gained only one bounded route:

```text
READY → DECIDED
actor = AI_EMPLOYEE
domain = AUTONOMOUS_NEXT_CYCLE
decision ∈ CONTINUE / ADJUST / WAIT
leaderAuthorized = true
```

Generic Decision Packets and terminal decisions cannot use that route.

## 4. Evaluation and fail-closed truth

Verified:

- approved contract requires observation window plus explicit success, failure,
  insufficient-evidence, continued-observation and escalation semantics;
- every observed fact references current Cycle Result, Artifact, Evidence or
  Acceptance;
- same fact with conflicting values is rejected;
- Result Task must still be completed in the canonical Company;
- Evidence must still be `VERIFIED / CURRENT` and belong to the Cycle;
- Acceptance must be closed and cover the current Evidence;
- insufficient Evidence cannot autonomously `CONTINUE` or `ADJUST`;
- stale Strategy or Envelope pin is rejected;
- unavailable/missing canonical Leader is rejected;
- cross-tenant read is rejected;
- conflicting Evaluation or Decision replay is rejected.

Result remains distinct from Evaluation: a completed execution does not itself
prove strategic success.

## 5. Restart, replay and exactly-once evidence

- Restart after Evaluation returns the same deterministic Evaluation.
- An injected restart after Leader Review persisted a single DRAFT Packet;
  replay advanced that same Packet instead of creating another.
- Restart/replay after Decision returns the same Packet.
- One closed Cycle produced exactly one Decision Packet and still exactly one
  Cycle.
- `successorCycleRef` remained `null` for all six decisions.
- No `acceptedLearning` or equivalent promotion was written.

## 6. Test evidence

All tests used one repository-external SQLite path assigned to
`CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` before import.

```text
Phase 3A focused matrix
14 passed in 7.10s

Phase 1 + Phase 2 + Phase 3A
+ RD P7 Decision
+ Team Operating real Employee E2E
+ Backend DB Safety
44 passed in 16.84s

Python py_compile
PASS

git diff --check (owned tracked files)
PASS
```

The controlled Provider proves the accepted real Task/Session/callback path. It
does not prove external live-model quality, latency or cost.

## 7. Active DB safety

Final values equal the pre-change and Phase 2 baselines:

| Path | Size | mtime | SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

No active DB, Schema, API, frontend, Domain, Team Operating, Responsibility
Router or Provider bridge file changed.

## 8. Changed files

1. `backend/app/runtime/autonomous_operating.py`
2. `backend/app/runtime/registry.py` — one bounded Leader-authorized transition
3. `backend/tests/test_autonomous_operating_phase3a.py`
4. `issues/20260821_autonomous_operating_v1_phase3a_evaluation_decision_001.md`
5. this Review

Post-change implementation hashes:

- `autonomous_operating.py`: `a2f5c366255c248b6594496475f5de91e56ea3eefda6fa4f7aacc59b9c8fbca6`
- `registry.py`: `4472bea6952f6d789ba93aea5e46fe1db04baa2df97ff6de3c99c887678edd46`
- `test_autonomous_operating_phase3a.py`: `789d763d8b430cd3f1e2409b6a6670f5189b5e9d0f3de8fabca3fd53a1b9f12c`

## 9. Explicitly not implemented

- successor Cycle creation or wake-up;
- accepted Learning / Knowledge / Strategy evolution;
- CEO UI or any new UI;
- generic evaluation/rules/workflow engine;
- Business-scope Provider execution;
- external live-provider quality/cost proof.

No files were staged, committed or pushed. Phase 1 and Phase 2 remain preserved
uncommitted dependencies and must be archived with Phase 3A only after CEO
acceptance and an exact bounded commit decision.

```text
CURIS AUTONOMOUS OPERATING V1
— PHASE 3A IMPLEMENTED
— EVALUATION CONTRACT PINNED
— EVIDENCE-BOUND EVALUATION VERIFIED
— CANONICAL LEADER REVIEW VERIFIED
— SIX NEXT-CYCLE DECISIONS VERIFIED
— PAUSE / STOP AUTHORITY VERIFIED
— EXACTLY-ONE DECISION VERIFIED
— RESTART / REPLAY VERIFIED
— NO SUCCESSOR
— NO LEARNING PROMOTION
— ACTIVE DB UNCHANGED
— REVIEW REQUIRED
```
