# CURIS AUTONOMOUS OPERATING V1 — PHASE 3B
## SUCCESSOR AUTHORIZATION / EXACTLY-ONE NEXT CYCLE

**Issue ID:** `20260821_autonomous_operating_v1_phase3b_successor_control_001`
**Authority Class:** IMPLEMENTATION ISSUE
**Status:** Review
**Disposition:** IMPLEMENTED / ACCEPTED
**Baseline HEAD:** `50d058ca865c1817721536d7beb47a1c5f1f354d`

## Goal

Use one canonical applied Phase 3A Next-cycle `DECISION_PACKET` as the sole
authority for a deterministic existing Trigger Claim and exactly one existing
successor `CYCLE`:

```text
Cycle 1 CLOSED → applied CONTINUE / bounded ADJUST Decision
→ deterministic authorized TRIGGER_CLAIM → exactly one Cycle 2
```

`WAIT / ESCALATE / PAUSE / STOP` create no successor. Phase 3B creates no
Learning and does not execute Cycle 2.

## Authority

- accepted Phase 1, Phase 2 and Phase 3A Reviews;
- `docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md`;
- CEO Phase 3B authorization dated 2026-08-21.

## Runtime rules

- Decision is the only successor authority.
- Existing `TRIGGER_CLAIM` and existing `CYCLE` are reused.
- First Cycle triggers remain compatible; after a Series has a closed Cycle, a
  new Cycle requires an applied canonical `CONTINUE / ADJUST` Decision.
- Claim, successor Cycle, bidirectional lineage, Decision successor ref and
  Series current/last refs are persisted in one SQLite transaction.
- `ADJUST` creates a deterministic adjusted Strategy version from the bounded
  changes already accepted in Phase 3A; predecessor pins remain immutable.
- Successor Plan remains unresolved and records the predecessor Decision and
  required bounded changes. No Plan is fabricated.

## Allowed Files

1. `backend/app/runtime/autonomous_operating.py`
2. `backend/tests/test_autonomous_operating_phase3b.py`
3. this Issue
4. `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_PHASE3B_SUCCESSOR_CONTROL_REVIEW.md`

Pre-change implementation hash:

- `autonomous_operating.py`: `a2f5c366255c248b6594496475f5de91e56ea3eefda6fa4f7aacc59b9c8fbca6`

## Explicit exclusions

- Learning / Knowledge / Memory promotion;
- successor execution, Employee/Provider work or UI;
- Resume Product Flow or generic Event Engine;
- new Cycle/Claim/Decision/Strategy Schema or Runtime primitive;
- API/frontend/Domain changes;
- active DB writes, stage, commit or push.

## Acceptance

1. `CONTINUE` creates exactly one successor;
2. bounded `ADJUST` creates exactly one successor with adjusted immutable pins;
3. predecessor/successor lineage is bidirectional;
4. Series current/last refs are correct and state remains `ACTIVE`;
5. `WAIT / ESCALATE / PAUSE / STOP` create no successor;
6. ordinary triggers cannot bypass a closed Cycle Decision;
7. duplicate, concurrent and restart replay return the same Claim/Cycle;
8. stale/unapplied/conflicting Decision, stale Strategy/Envelope, invalid
   adjustment, non-ACTIVE Series, unrelated active Cycle and cross-tenant fail
   closed;
9. no successor execution and no Learning;
10. Phase 1–3A regression and active DB safety pass.
