# CURIS AUTONOMOUS OPERATING V1 — PHASE 3A
## EVALUATION / LEADER REVIEW / NEXT-CYCLE DECISION TRUTH

**Issue ID:** `20260821_autonomous_operating_v1_phase3a_evaluation_decision_001`
**Authority Class:** IMPLEMENTATION ISSUE
**Status:** Review
**Disposition:** IMPLEMENTED / ACCEPTED
**Baseline HEAD:** `50d058ca865c1817721536d7beb47a1c5f1f354d`

## Goal

Extend the accepted Phase 2 closed-Cycle truth with one minimal, evidence-bound,
restart-safe chain:

```text
CLOSED Cycle + Result/Evidence/Acceptance + approved Evaluation Contract
→ Evaluation → canonical Workspace Leader Review
→ one existing DECISION_PACKET
```

The only decisions are `CONTINUE / ADJUST / WAIT / ESCALATE / PAUSE / STOP`.
Phase 3A records decision truth only: `successorCycleRef` remains `null` and no
Learning is promoted.

## Authority

- `docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md`
- `docs/reviews/CURIS_AUTONOMOUS_BUSINESS_OPERATION_SYNTHESIS.md`
- `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_IMPLEMENTATION_READINESS.md`
- CEO Phase 3A authorization dated 2026-08-21
- accepted Phase 1 and Phase 2 reviews

## Runtime truth and authority

- Evaluation Contract is a versioned approved pin on the existing Series/Cycle.
- Evaluation and Leader Review are Cycle-scoped persisted data, not new global
  Runtime primitives.
- Decision truth is the existing `DECISION_PACKET`.
- Leader may apply `CONTINUE`, in-envelope `ADJUST`, and `WAIT`.
- Out-of-envelope `ADJUST` becomes `ESCALATE` and waits for CEO.
- `PAUSE` requires CEO or an existing explicit Leader authorization. No such
  terminal policy is assumed by this Issue.
- `STOP` requires CEO or an existing explicit terminal policy. No such policy is
  assumed by this Issue.
- Missing/insufficient/conflicting evidence, stale pins, missing Leader and
  replay conflicts fail closed.

## Allowed Files

1. `backend/app/runtime/autonomous_operating.py`
2. `backend/app/runtime/registry.py` — only the bounded Leader-authorized
   `READY → DECIDED` transition for an Autonomous Next-cycle Decision Packet
3. `backend/tests/test_autonomous_operating_phase3a.py`
4. this Issue
5. `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE3A_EVALUATION_DECISION_REVIEW.md`

Pre-change hashes:

- `autonomous_operating.py`: `1232c22eca3d0c95a05f8f950dc58c2243eaac2aab79b4774f81b5e28dfbc321`
- `registry.py`: `cb6b66ef4f5e880c13fd19c1a2d754db2bf9f779c6f6e09fcaea6ba1a7dd1fc8`

## Explicit exclusions

- successor Cycle creation;
- accepted Learning / Knowledge / Strategy promotion;
- generic rules, review, workflow, evaluation or learning engine;
- new Schema or Runtime entity type;
- API / frontend / CEO UI;
- Business-scope Provider execution;
- Domain changes, active DB writes, stage, commit or push.

## Acceptance

1. successful, failed and insufficient evidence evaluation;
2. six canonical decision outcomes;
3. in-envelope `ADJUST`; out-of-envelope `ADJUST → ESCALATE`;
4. `WAIT` condition/time and durable Series state;
5. CEO-gated `PAUSE / STOP` authority;
6. exactly one Decision Packet per closed Cycle;
7. restart after Evaluation, Review and Decision without duplication;
8. stale Strategy/Envelope, missing Leader, conflicting/missing evidence,
   cross-tenant and replay conflicts fail closed;
9. no successor and no Learning;
10. Phase 1/2 and shared Decision/Team Operating no-regression;
11. three-variable isolated SQLite guard and unchanged active DB fingerprints.
