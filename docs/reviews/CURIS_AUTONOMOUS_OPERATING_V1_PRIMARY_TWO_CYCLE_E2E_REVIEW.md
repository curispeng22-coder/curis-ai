# CURIS AUTONOMOUS OPERATING V1 — PRIMARY TWO-CYCLE E2E REVIEW

**Authority Class:** REVIEW
**Status:** Review
**Disposition:** IMPLEMENTED / CEO REVIEW REQUIRED
**Date:** 2026-08-21
**Issue:** `issues/20260821_autonomous_operating_v1_primary_two_cycle_e2e_001.md`
**Baseline:** `86405404dd16e32b131fff8aa0008d8d11ea6961`

## A. Domain Readiness Matrix

| Runtime truth | RD | XHS |
|---|---|---|
| canonical Company / Department / Business / Workspace | READY | READY |
| valid Workspace Leader and Responsibility Assignment | READY | READY |
| existing Team Operating definition / routing | READY | PARTIAL |
| canonical Employee and capability binding | READY | READY |
| Provider Task / Session | READY WITH BOUNDED FIXTURE | PARTIAL |
| ResultStore Task / Artifact / Evidence / Acceptance | READY | PARTIAL |
| Domain-specific result meaning | code/test result contract | ContentItem truth exists; publish/analytics connectors are not connected |
| approved bounded Plan source | existing RD Operating Definition plus versioned Cycle Plan | no accepted Autonomous Plan-to-ContentItem result bridge |
| restart / duplicate safety | READY | accepted domain persistence, no cross-cycle proof |
| Primary proof readiness | **READY WITH BOUNDED FIXTURE** | **BLOCKED** |

## B. Selected Primary Domain

**RD Workspace** is the Primary Proof Domain.

The proof creates the Workspace through the real `WorkspaceRuntime` RD contract,
including all eight RD stages, explicit Workspace Goal, canonical parent Business,
RD Project, Workspace Leader role, canonical Employee, Assignment, capability
binding and existing Team Operating definition.

## C. Why This Domain

RD has the shortest truthful path from approved Plan to Employee/Provider Task,
Artifact, test-oriented Evidence and Acceptance. A deterministic local Provider is
used only to avoid production code changes, external account use, cost and side
effects. Provider Task, Session, callback, ResultStore, Artifact, routing and all
control objects remain real persisted Runtime facts.

XHS is not selected because its real `ContentItem`/version/review truth is not yet
connected to Autonomous Plan/Result ownership. Publishing and analytics are also
honestly unavailable. Selecting XHS would require a new Domain bridge, which is a
Stop Gate, not a test shortcut. This remains a future Cross-domain proof gap.

## D. Cycle 1 Full Trace

```text
SCHEDULED Trigger Claim: rd-observation-window-1
→ existing CYCLE 1 PLANNED / NOT_STARTED
→ approved rd-plan-v1
→ existing RD Team Operating definition rd-autonomous-primary
→ canonical Workspace Leader Assignment
→ canonical RD Employee
→ tenant-private controlled Provider capability binding
→ real Provider Task + rd-primary-session-1
→ completed Result Contract: rd-operating-result
→ real Artifact
→ verified Provider usage evidence
→ Runtime EVIDENCE
→ CEO Acceptance
→ CLOSED Cycle 1
```

Cycle 1 Plan means: establish a controlled repair/test evidence baseline for the
real isolated RD Project. The CEO does not create the Employee Task, start the
Provider or hand work between employees. CEO authority appears only in the
pre-approved Strategy/Envelope/Plan and ordinary Acceptance gate.

## E. Cycle 1 Evaluation / Decision

Cycle 1 receives an approved versioned Evaluation Contract. Its observed fact
references Cycle 1's verified Evidence. The resulting Evaluation is `SUCCESS /
SUFFICIENT`, followed by the canonical Workspace Leader Review and one existing
`DECISION_PACKET` with `CONTINUE`.

Operating meaning: the first observation window produced sufficient verified RD
result/evidence to continue the same approved Strategy into a distinct second
observation window. Execution success is not used as a substitute for this
evidence-bound operating judgment.

## F. Successor Authorization

The applied Cycle-1 Decision is the sole successor authority. After reopening the
same SQLite through a new `Database` and `AutonomousOperatingControl`, both first
authorization and replay resolve the same deterministic Trigger Claim and Cycle 2.

No ordinary trigger, Result arrival, callback, Employee or UI action creates the
successor. The predecessor records one `successorCycleRef`; Cycle 2 records the
predecessor Cycle and Decision refs.

## G. Cycle 2 Full Trace

```text
Cycle-1 CONTINUE Decision
→ deterministic RESULT Trigger Claim
→ existing CYCLE 2 PLANNED / NOT_STARTED
→ approved rd-plan-v2 with predecessor context
→ same accepted RD Operating Definition, newly materialized Work
→ same canonical Responsibility Holder
→ new Provider Task + rd-primary-session-2
→ distinct Result Contract output
→ distinct Artifact / Provider evidence / Runtime EVIDENCE
→ distinct CEO Acceptance
→ CLOSED Cycle 2
```

Cycle 2 Plan is not a copy of Cycle 1. It uses another observation window and
explicitly pins Cycle 1, its Decision, Result refs, Evidence refs and Evaluation.
Its work is a second independent regression verification based on the first-cycle
evidence. The accepted Operating Definition is reused; no Planner Engine is added.

## H. Cycle 2 Evaluation / Decision

Cycle 2 receives its own evidence-bound Evaluation and canonical Leader Review.
The second Decision is `WAIT`, with a persisted reason and `nextCheckAt`.
`authorize_successor()` truthfully returns no Claim/Cycle for this Decision.

Operating meaning: two bounded observation windows are complete; the Series waits
for a future real observation window. This Review intentionally stops before a
third Cycle.

## I. Result / Evidence Separation

- Provider Result truth remains the existing ResultStore Task.
- Artifact truth is separately persisted in `artifacts`.
- Provider callback/usage evidence remains separately persisted.
- Runtime `EVIDENCE` references the Result, Artifact and Provider evidence.
- `ACCEPTANCE` references the Runtime Evidence and Result/Artifact refs.
- Evaluation references the verified Runtime Evidence.

The two Cycles have different Task, Session, Artifact, Evidence and Acceptance
identities. Conversation text, fixture summaries and execution status are not
treated as Evidence.

## J. Lineage

Cycle 2 persists:

- `predecessorCycleRef` = Cycle 1;
- `predecessorDecisionRef` = Cycle-1 Decision;
- Plan-body refs to Cycle-1 Result, Evidence and Evaluation;
- the inherited Strategy and Envelope pins authorized by `CONTINUE`.

The Cycle-1 control pins and Evaluation are deep-compared before/after Cycle-2
execution and remain immutable except for the already established successor link.
Cycle-1 and Cycle-2 Plan bodies and result identities are different.

## K. Restart / Replay

The proof verifies:

1. Cycle 1 closed/decided → reopen control → same Cycle 2.
2. Cycle-2 Work released → reopen control → same Work/Cycle, no duplicate release.
3. During the blocked second Provider call → reopen database/control → persisted
   real current executor remains readable; provider then completes once.
4. Cycle-2 Provider completed → reopen control → same Result/Artifact before close.
5. Duplicate execute call → same completed Work; no third Provider call or Task.
6. Duplicate Evaluation and Leader Review → same Evaluation/Decision refs.
7. Final reopen → Series remains `WAITING`, Cycle count remains exactly two.

## L. Failure Proof

| Cycle-2 case | Verified result |
|---|---|
| Provider timeout | Cycle 2 routing waits, then Cycle 2 is persisted `FAILED`; no Artifact/Evidence/Acceptance is fabricated |
| invalid Result Contract | partial Artifact is retained as failure truth; no Runtime Evidence/Acceptance is fabricated |
| capability disabled | materialization fails before second Provider Task |
| Employee paused | materialization fails before second Provider Task |
| duplicate successor authorization | same Claim/Cycle |
| duplicate execute/callback path | same Provider Task/Result; only two Provider calls in success proof |
| duplicate Evaluation/Review | same Evaluation/Decision |

Every failure keeps Cycle count at two, Decision count at one for the successful
first Cycle, and produces no Cycle 3 or Learning.

## M. Exact Object Counts

Successful proof final counts:

| Object | Count |
|---|---:|
| Operating Series | 1 |
| Cycle | 2 |
| Trigger Claim | 2 |
| Provider Task / Result | 2 |
| Artifact | 2 |
| Runtime Evidence | 2 |
| Acceptance | 2 |
| Evaluation | 2 |
| Leader Review | 2 |
| Decision Packet | 2 |

Both Provider Session refs are present and distinct.

## N. No Cycle 3 Proof

Cycle 2 ends with `WAIT`. Calling the existing successor adapter returns:

```text
created = false
claim = null
cycle = null
```

Final restart still reads exactly two Cycles. No Cycle-3 Trigger Claim exists.

## O. No Learning Proof

Both Cycle payloads are checked for the absence of `acceptedLearning` and
`learning`. No Knowledge, Memory, Strategy self-evolution or methodology mutation
is performed. Evaluation, Review and Decision remain operating evidence only.

## P. Active DB Safety

All tests set `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` to the same
repository-external temporary SQLite before import.

| Active path | Before / after size | Before / after mtime | Before / after SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896 / 1232896` | `1786873339 / 1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` / same | `ok / ok` |
| `backend/data/curis.sqlite` | `1277952 / 1277952` | `1786783659 / 1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` / same | `ok / ok` |

Both active databases are unchanged.

## Q. Remaining V1 Gaps

- Cross-domain Autonomous Contract Proof is not performed.
- XHS Autonomous Plan/Result-to-ContentItem integration is not implemented.
- External live Provider quality/cost is not verified.
- Learning/Knowledge/Memory promotion is intentionally not implemented.
- Cycle 3 and indefinite autonomous continuation are intentionally not proved.
- No UI/API product surface is added.

## Tests

- New Primary proof/failure suite: `5 passed`.
- Combined Phase 1–3B, Responsibility Routing, Team Operating real Employee E2E,
  RD real execution/P7, XHS persistence and DB Safety: `74 passed`.
- Python compile: PASS.
- `git diff --check`: PASS.

## Acceptance Questions

1. Primary Proof Domain: **RD**.
2. Why: most complete existing truthful Employee/Provider/Artifact/Evidence path.
3. Cycle 1 real execution: **YES**.
4. Real Team Operating: **YES**.
5. Real Employee/Provider Runtime objects: **YES**; Provider implementation is a bounded deterministic fixture, not an external live model claim.
6. Independent Cycle-1 Result/Evidence: **YES**.
7. Cycle-1 Evaluation/Review/Decision: **YES**.
8. Cycle 2 uniquely authorized by canonical Decision: **YES**.
9. Cycle 2 actually executed: **YES**.
10. Independent Cycle-2 Result/Evidence: **YES**.
11. Cycle 2 closed: **YES**.
12. Cycle-2 Evaluation/Leader Review: **YES**.
13. Second Decision: **YES, WAIT**.
14. Strategy/Plan pins: **YES**; Strategy/Envelope retained, Plan v1/v2 distinct.
15. Predecessor immutable: **YES**, apart from the already authorized successor link.
16. Restart without duplication: **YES**.
17. Cycle count exactly two: **YES**.
18. Cycle 3 created: **NO**.
19. Learning generated: **NO**.
20. CEO per-task dispatch: **NO**; only approved Plan/Acceptance authority is used.
21. Can this be called Primary Autonomous Two-Cycle E2E: **YES, pending CEO acceptance of this Review**.
22. Next V1 work: Cross-domain proof and, separately, a future Learning quality gate.

## Verdict

```text
CURIS AUTONOMOUS OPERATING V1
— PRIMARY DOMAIN SELECTED BY RUNTIME EVIDENCE
— CYCLE 1 REAL EXECUTION COMPLETE
— CYCLE 1 EVALUATION / DECISION COMPLETE
— DECISION-AUTHORIZED CYCLE 2 VERIFIED
— CYCLE 2 REAL EXECUTION COMPLETE
— CYCLE 2 RESULT / EVIDENCE VERIFIED
— CYCLE 2 EVALUATION / DECISION COMPLETE
— EXACTLY TWO CYCLES
— NO CEO TASK DISPATCH
— NO CYCLE 3
— NO LEARNING PROMOTION
— RESTART / REPLAY VERIFIED
— ACTIVE DB UNCHANGED
— PRIMARY AUTONOMOUS TWO-CYCLE E2E PROVED
— STOP FOR CEO REVIEW
```
