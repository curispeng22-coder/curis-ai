# CURIS-AUTONOMOUS-OPERATING-V1-CROSS-DOMAIN-CONTRACT-PROOF-001

Authority Class: CURRENT
Status: Review
Disposition: IMPLEMENTED / ACCEPTED

## Goal

Prove that the accepted Autonomous Operating lifecycle can carry one bounded XHS
content-production Cycle with XHS-specific Goal, Strategy, Team, Result, Evidence,
Evaluation and Value semantics without adding an XHS Autonomous Runtime or claiming
unavailable publishing/analytics facts.

## Authority

- `issues/20260820_autonomous_operating_v1_implementation_001.md` §15.2
- `docs/reviews/CURIS_OPERATING_LIFECYCLE_CONTRACT_CANDIDATE.md` §10.1.1
- CEO Long-Run Closure Mission, Phase B
- accepted commit `c311a62aa4a4a5d0b372e03af99bebe4db12b86a`

## Readiness Decision

XHS is the second Domain. Its accepted `ContentItem` and immutable version are real
Domain inputs. Existing Team Operating already provides a distinct content team and
typed content outputs. The proof intentionally stops at a reviewable content package:
publishing and analytics connectors remain unavailable, the `ContentItem` is not
advanced to `PUBLISHED`, and no external metric is invented.

TTK is not selected because its provider/connector supply is less complete. Generic
Package work is a valid fallback but provides a weaker professional contrast with RD.

## Allowed Files

1. `backend/tests/test_autonomous_operating_cross_domain_xhs.py`
2. `issues/20260821_autonomous_operating_v1_cross_domain_contract_proof_001.md`
3. `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_CROSS_DOMAIN_CONTRACT_PROOF_REVIEW.md`

## Explicit Exclusions

- no Runtime, Schema, API, frontend or active-database change;
- no XHS Plan/Result-to-ContentItem lifecycle bridge;
- no publishing, receipt, analytics or growth metric claim;
- no XHS-specific Series, Cycle, Evaluation or Decision system;
- no Learning, Knowledge, Memory or Strategy mutation;
- no successor Cycle requirement;
- no commit before CEO acceptance.

## Proof Contract

The proof must use the same canonical `OPERATING_SERIES`, `TRIGGER_CLAIM`, `CYCLE`,
Team Operating, Employee/Provider Task, Artifact, Evidence, Acceptance, Evaluation,
Leader Review and `DECISION_PACKET` contracts as RD. It must differ in:

- Workspace Goal: create a truthful, reviewable XHS content asset;
- Strategy: audience hypothesis, content angle and bounded review cadence;
- Team: content lead, topic researcher, content researcher and copy employee;
- Work: one real `ContentItem` and immutable `ContentVersion`;
- Result: topic plan, research brief and publish-package with publication explicitly
  `NOT_CONNECTED`;
- Evidence: accepted content package/provider provenance, not code/test evidence;
- Evaluation: content readiness, policy risk and source sufficiency;
- Value: a reviewable content asset, not software correctness or invented platform KPI.

## Acceptance

1. canonical Company/Department/Business/XHS Workspace and real ContentItem exist;
2. one Trigger produces one Cycle under the existing Series;
3. the existing Team Operating runtime invokes real canonical Employees and the
   controlled Provider callback path;
4. typed XHS results, Artifact, Provider evidence, Cycle Evidence and Acceptance exist;
5. evaluation uses XHS-specific semantics and canonical evidence refs;
6. one Leader Decision is persisted through the existing Decision contract;
7. restart/replay returns the same objects and no duplicate Provider work;
8. missing capability, malformed Domain Result, insufficient Evidence, unavailable
   Leader, stale Strategy/Goal and cross-tenant access fail closed;
9. ContentItem is not marked published and no external analytics are created;
10. Learning count remains zero and no successor Cycle is created;
11. Phase 1–3B, Primary E2E, Team Operating, Responsibility Routing and DB Safety regressions pass;
12. both active SQLite files remain byte-for-byte unchanged.

## Stop Gate

Stop if this proof requires a new shared/domain Runtime primitive, an XHS lifecycle
mutation, fake external evidence, an active database, an unowned file, or Cycle 2.

## Final Acceptance

CEO accepted Phase B on 2026-08-21. This acceptance proves contract portability only:
`ContentItem=DRAFT`, publishing remains `NOT_CONNECTED`, and analytics remains
`UNAVAILABLE`.
