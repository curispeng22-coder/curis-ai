# CURIS AUTONOMOUS CROSS-SURFACE MULTI-WORK RUNTIME PROOF 001

Authority Class: CURRENT
Status: Frozen
Disposition: PROOF IMPLEMENTED / ACCEPTED
Date: 2026-08-22
Owner: Main Developer / Autonomous Operating Runtime

## Exact Objective

Prove that one canonical Workspace, one Operating Series and one existing Cycle can
own at least two distinct canonical Work objects across multiple Responsibilities,
with independent Result/Evidence/Acceptance provenance, acknowledged Handoff,
aggregated Evaluation, one Leader Review and one Decision.

The proof must not treat Surface as Runtime authority and must not count multiple
Employee executions inside one routed object as multiple Work.

## Authority → Runtime Mapping

| Authority concept | Required Runtime truth | Current implementation truth |
|---|---|---|
| one Workspace / one Team | Workspace-scoped workflow and Assignments | implemented |
| one active Cycle | one canonical `CYCLE` under one Series | implemented |
| multiple Work in one Cycle | distinct Work identity/lifecycle linked to the Cycle | **missing** |
| Responsibility bridges Work and Team | each Work pins its own Assignment/holder | only one routing record on the Cycle |
| Handoff | accountability transfer with accepted prior output and next Work | transfer exists, but only within the same `workRef` |
| Evaluation | aggregates Work-scoped Result/Evidence/Acceptance | reads a flat Cycle aggregate from one routing record |

## Current Runtime Reuse Map

- `AutonomousOperatingControl`: Series, Trigger Claim, Cycle, Plan pin, Cycle close,
  Evaluation, Leader Review and Decision are reusable.
- `ResponsibilityRoutingRuntime`: Assignment, canonical Employee, Provider execution,
  Result/Artifact/Evidence refs and acknowledged Handoff are reusable for one Work.
- Team Operating: sequential multi-Responsibility execution and restart/replay are
  real, but remain attached to one routed entity.
- ResultStore / Runtime Foundation: Result, Artifact, Evidence, Acceptance, Handoff
  and Decision persistence are reusable.
- No existing Runtime seam releases a second canonical Work from an accepted Result
  and Handoff in the same Cycle.

## Primary Domain Readiness

| Domain | Readiness | Evidence |
|---|---|---|
| XHS | BLOCKED for required proof | closest domain semantics; accepted proof performs topic → research → copy across Assignments, but all executions and Handoffs remain on the Cycle's single routing record |
| RD | BLOCKED for required proof | real code execution/review exists, but does not provide a generic second Work release under one Autonomous Cycle |

XHS remains the preferred future proof domain once shared Work identity is authorized.
The blocker is shared Runtime, not XHS domain readiness.

## Exact Allowed Files

CEO Acceptance of the Canonical Child Work Foundation reopens this proof with exactly:

1. `backend/tests/test_autonomous_cross_surface_multi_work_runtime_proof.py`
2. `issues/20260821_autonomous_cross_surface_multi_work_runtime_proof_001.md`
3. `docs/reviews/CURIS_AUTONOMOUS_CROSS_SURFACE_MULTI_WORK_RUNTIME_PROOF_REVIEW.md`

All Runtime source, API, schema, frontend, Package, Surface and database files remain
excluded. If accepted seams cannot satisfy the proof, implementation stops rather than
adding a new foundation.

## Reopen Authority

`CURIS CANONICAL CHILD WORK FOUNDATION = ACCEPTED` on 2026-08-22. The historical
blocked audit below remains valid provenance for the pre-Foundation state. The reopened
proof must use canonical child `WORK`, the accepted atomic next-Work release seam and
Work-scoped Cycle/Evaluation aggregation; it may not relabel multiple executions inside
one Cycle routing record as multiple Work.

## Persistence Strategy

Not implemented. A future authorized design must use canonical persisted Work identity
under the existing Cycle and reuse existing Assignment, Handoff, Result, Artifact,
Evidence and Acceptance truth. A test fixture or nested JSON step list is insufficient.

## Transaction Boundaries

Current Handoff atomically validates the target Assignment/Employee, persists the
Handoff transitions and changes the holder on the same `workRef`. There is no current
transaction for:

```text
accepted Work A Result
→ completed Handoff
→ exactly-one Work B creation
```

Therefore crash safety for the required Work A → Work B boundary cannot be proved.

## Work Identity Rules

Required but absent:

- a distinct stable Work identity;
- canonical parent relation to exactly one Cycle;
- independent Responsibility/holder/status/context/output refs;
- deterministic release/idempotency key;
- no Surface identity as execution authority.

## Handoff Rules

Existing Handoff is real accountability transfer, validated atomically and persisted.
It references one unchanged `workRef`. It does not release or reference a next Work.
It therefore cannot satisfy this Issue's cross-Work Handoff contract without an
authorized shared Work primitive/seam.

## Result / Evidence Provenance

Current provider executions have distinct Task/Artifact/Evidence provenance, but refs
are accumulated in one `responsibilityRouting` record and later flattened into Cycle
evidence. There is no canonical Work A / Work B ownership boundary for those refs.

## Evaluation Aggregation

Current Evaluation safely consumes all Cycle-level Result/Evidence/Acceptance refs.
It cannot answer which required Work produced each ref or whether all required Work
were satisfied because canonical Work membership does not exist.

## Restart Matrix

Existing one-Work routing, Handoff, Result and Decision restart correctly. The required
restart cases for Work B release cannot be executed honestly because Work B has no
canonical persisted identity or release record.

## Replay / Idempotency Matrix

Provider callback, same-work Handoff and Evaluation replay are bounded today. Duplicate
next-Work release cannot be checked because no such Runtime operation exists.

## Failure Matrix

Existing paths fail closed for invalid Result, missing Capability/Assignment,
unavailable Employee, invalid Handoff target and cross-scope access. The required
transaction interruption between Work A acceptance and Work B creation has no current
operation to interrupt or recover.

## Active DB Guard

Any future test must set `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` to one
repository-external isolated SQLite before import. Both repository active databases
are read-only evidence and must remain byte-for-byte unchanged.

## Stop Gates Triggered

1. existing Cycle cannot currently own multiple canonical Work identities;
2. next Work has no legal Runtime release operation;
3. Handoff cannot reference/create a next Work;
4. Evaluation has only flat Cycle refs, not Work-scoped aggregation;
5. exactly-once Work B creation cannot be proved without a new shared primitive/seam.

Implementation stops before code. Creating an arbitrary Runtime entity in a test or
adding another routing JSON block would be a second, unauthoritative Work model.

## Required Authority Decision Before Resume

Authorize a separate bounded Shared Runtime Issue defining the smallest canonical
child Work identity and exactly-once release seam under an existing Cycle, preferably
using `runtime_entities` and existing links rather than a new table or engine. This
must be resolved before re-opening the proof; no Surface Runtime, DAG or scheduler is
needed or proposed here.

## 2026-08-22 Reopened Proof Result

The accepted Canonical Child Work Foundation removed the historical Stop Gate. A new
isolated XHS proof now demonstrates one Workspace, one Series and one Cycle owning two
distinct canonical Work across Research and Content Assignments/Employees. Each Work
uses the real Team Operating Provider Task/Session path and owns independent Result,
Artifact, Evidence and Acceptance truth. Accepted Work A plus the canonical atomic
Handoff/release seam creates exactly one Work B. Cycle Evaluation aggregates both Work;
the existing canonical Workspace Leader records one Review and one Decision with no
successor Cycle and no Learning.

Focused proof: `2 passed`. Combined Foundation/Autonomous/Learning/Responsibility/Team
Operating regression: `85 passed`. No Runtime source, schema, API, UI, Package or
active database was changed by the reopened proof.
