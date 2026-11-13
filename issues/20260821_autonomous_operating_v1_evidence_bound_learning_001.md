# CURIS-AUTONOMOUS-OPERATING-V1-EVIDENCE-BOUND-LEARNING-001

Authority Class: CURRENT
Status: Review
Disposition: IMPLEMENTED / ACCEPTED

## Goal

Add the smallest accepted V1 path that turns two closed, evidence-bound Cycles into
a reviewable Learning Candidate, requires explicit bounded acceptance, preserves
scope/provenance/confidence, supports supersede/invalidate/retrieval, and never
changes Strategy, Goal, Package or source code automatically.

## Truth Audit

| Existing capability | Current truth | Decision |
|---|---|---|
| ResultStore Task/Artifact | persisted, tenant-scoped, content-hashed, task-provenanced | reuse Artifact rows for Candidate and Accepted Learning |
| Cycle Result/Evidence/Acceptance | canonical and restart-safe | mandatory source truth |
| Evaluation/Leader Review/Decision | canonical and evidence-bound | mandatory source provenance |
| MemoryService | user/project/employee memory; manual/task source; no multi-cycle acceptance | do not use as accepted Learning truth |
| LessonMemory | capability-path reuse heuristic | do not use for operating Learning |
| Knowledge entries | external/manual knowledge source | future context may reference accepted Learning; no automatic copy |
| Strategy/Envelope | approved versioned authority | read-only; Learning never mutates it |
| Package/Methodology | separate authority/lifecycle | no automatic mutation |

No Learning Engine, Memory system or new Schema is justified. V1 uses existing
Artifact persistence plus references on the existing Operating Series/source Cycle.

## Pre-change Ownership

- `backend/app/runtime/autonomous_operating.py`
  - pre-change SHA-256: `5ab0b0a7b94895b201e317370ed07e44203541f9ebf3bcd9c8b8fc2007f11de6`
  - clean at task entry;
  - owned change: append only bounded candidate/accept/retrieve/invalidate helpers.

## Allowed Files

1. `backend/app/runtime/autonomous_operating.py`
2. `backend/tests/test_autonomous_operating_evidence_bound_learning.py`
3. `issues/20260821_autonomous_operating_v1_evidence_bound_learning_001.md`
4. `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_EVIDENCE_BOUND_LEARNING_REVIEW.md`
5. `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_LONG_RUN_CLOSURE_REPORT.md`

## Explicit Exclusions

- no Learning Engine, Knowledge Graph, Workflow/DAG or new table;
- no MemoryService/LessonMemory rewrite;
- no API/UI;
- no automatic Strategy, Goal, Envelope, Methodology, Package, capability routing,
  prompt authority or source-code mutation;
- no Cycle 3;
- no cross-domain/company promotion without explicit authority;
- no commit before CEO review;
- no active database.

## Runtime Truth Model

- Candidate: existing `artifacts` row, `artifact_type=learning_candidate`,
  `status=generated`, content-hashed and tied to a completed source Task.
- Accepted Learning: separate existing `artifacts` row,
  `artifact_type=accepted_learning`, `status=accepted`, referencing Candidate hash,
  source Cycles/Result/Evidence/Evaluation/Decision and explicit accepter/time.
- Scope: `WORKSPACE`, `DOMAIN`, or `COMPANY_CANDIDATE`; retrieval is limited to the
  target Series Workspace/Domain. Company candidate acceptance requires CEO.
- Conflict: a new accepted artifact may supersede prior accepted refs; invalidation
  archives the accepted artifact and records evidence/reason without deleting history.
- Future use: bounded resolver returns accepted refs for Context/Plan/Evaluation input;
  it creates no Cycle and changes no Strategy.

## Acceptance

1. two distinct closed Cycles with Result/Evidence/Acceptance/Evaluation/Decision are required;
2. Candidate and Accepted artifacts are distinct and idempotent;
3. provenance includes source Cycles, Results, Evidence, Evaluations and Decisions;
4. insufficient/stale/unverified evidence fails closed;
5. Leader may accept Workspace/Domain context Learning only;
6. Company/protected promotion requires CEO;
7. RD Learning is not returned to an XHS Series;
8. restart/replay and exactly-once acceptance hold;
9. supersede/invalidate preserve history and remove old refs from active retrieval;
10. future retrieval returns compact reference-first truth;
11. Strategy/Goal/Package remain unchanged and Cycle count remains exactly two;
12. Phase 1–3B, Primary E2E, Cross-domain, Team Operating and DB Safety regressions pass;
13. both active SQLite files remain unchanged.

## Stop Gate

Stop if a new Schema/Runtime/Memory system is required, if evidence cannot be verified,
if scope isolation cannot be enforced, if Strategy/Package mutation is needed, or if a
third Cycle is created.

## Final Acceptance

CEO accepted Phase C on 2026-08-21. Accepted Learning remains Artifact-backed,
evidence-bound, scope-limited and explicitly authorized; it does not mutate Strategy,
Goal, Package or code and does not create Cycle 3.
