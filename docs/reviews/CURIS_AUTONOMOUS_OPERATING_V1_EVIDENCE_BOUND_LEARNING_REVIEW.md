# CURIS AUTONOMOUS OPERATING V1 — EVIDENCE-BOUND LEARNING REVIEW

Authority Class: REVIEW
Status: Review
Disposition: IMPLEMENTED / ACCEPTED

## Verdict

V1 now proves an evidence-bound, reviewable and scope-limited Learning path by
extending the existing `AutonomousOperatingControl` and reusing the existing
ResultStore `artifacts` table. It does not create a Learning Engine, Memory system,
Knowledge Graph, table, API or UI.

The Primary RD Two-Cycle proof is the real source. A Candidate can be created only
when at least two distinct source Cycles are closed and each has completed Provider
Results, current verified Evidence, closed Acceptance, Evaluation and an applied
Decision. Acceptance creates a separate immutable-content accepted Artifact with the
Candidate hash and explicit authority/time. Nothing automatically changes Strategy,
Goal, Envelope, Methodology, Package, prompt authority, capability routing or code.

## Learning Truth Audit

| Existing system | Why it is not the accepted Learning truth | Reuse decision |
|---|---|---|
| `MemoryService` | user/project/employee memory; manual or one Task source; no two-Cycle acceptance/scope authority | not used |
| `LessonMemory` | capability path heuristic and reuse counter | not used |
| Knowledge entries | external/manual knowledge content; no operating acceptance contract | future consumer only |
| development strategy tables | implementation self-evolution history, not current Operating authority | not used |
| ResultStore Artifact | tenant/task provenance, hash, generated/accepted/archived lifecycle | **reused** |
| Cycle Result/Evidence/Acceptance | canonical closed execution truth | **required source** |
| Evaluation/Leader Review/Decision | evidence interpretation and authority truth | **required source** |
| Strategy/Envelope | approved authority | read-only boundary |
| Package/Methodology | separate authority/lifecycle | untouched |

## Canonical Runtime Model

### Candidate

An existing `artifacts` row:

- `artifact_type=learning_candidate`;
- `status=generated`;
- tied to a completed source Provider Task;
- deterministic identity from tenant + Series + content hash;
- content includes claim, scope, confidence, conditions, limitations, proposed use,
  revalidation criteria, supersede/conflict refs and full provenance.

### Accepted Learning

A separate existing `artifacts` row:

- `artifact_type=accepted_learning`;
- `status=accepted`;
- references Candidate ID/hash;
- preserves Cycle/Result/Evidence/Evaluation/Decision provenance;
- records `acceptedBy` and `acceptedAt`;
- is referenced by the existing Operating Series/source Cycle.

Candidate and Accepted truth are separate. Replay returns the same deterministic
records. Concurrent duplicate acceptance creates exactly one accepted Artifact.

### Scope and Authority

| Scope/use | Required authority |
|---|---|
| Workspace/Domain + future Context/Plan/Evaluation input | active canonical Workspace Leader |
| Company candidate | CEO |
| Strategy/Goal/Package/Company policy use | CEO |

`resolve_learning_context()` returns only active reference-first Learning applicable to
the target Series Workspace, Domain or explicitly CEO-accepted Company candidate.
An RD Domain Learning is not returned for an XHS Series in the same Company.

## Two-Cycle Provenance Proof

The proof consumes the accepted Primary RD chain without creating replacement data:

```text
Cycle 1: Result → Artifact → Evidence → Acceptance → Evaluation → Decision CONTINUE
Cycle 2: Result → Artifact → Evidence → Acceptance → Evaluation → Decision WAIT
                         ↓
                Learning Candidate
                         ↓ explicit Leader acceptance
                Accepted Learning Artifact
```

The accepted record contains exactly two Cycle refs, two Result refs, two Cycle
Evidence refs, two Evaluation refs and two Decision refs. No Cycle 3 is created.

## Failure / Conflict / Recovery Evidence

| Case | Truth |
|---|---|
| one source Cycle | Candidate rejected |
| stale/unverified Evidence | Candidate rejected |
| Company/protected promotion by Leader | rejected; CEO required |
| duplicate/concurrent acceptance | same one accepted Artifact |
| explicit conflict without supersede | acceptance rejected |
| explicit supersede | prior accepted Artifact archived; replacement becomes active |
| invalidation | accepted Artifact archived; history/evidence/reason retained |
| restart | Candidate/Accepted/active context read from same SQLite |
| cross-domain retrieval | RD Domain Learning absent from XHS context |
| Strategy/Goal/Package mutation | none |

No history is deleted. Superseded or invalidated records remain archived Artifacts;
only active accepted refs are returned to future Context.

## Tests

- Evidence-bound Learning focused suite: `5 passed`.
- Combined Autonomous/Primary/Cross-domain/Learning/Team/DB Safety regression:
  `85 passed`.
- Python compile: PASS.
- `git diff --check`: PASS.

## Active DB Safety

All tests use one repository-external SQLite via `CURIS_DB`, `CURIS_DB_PATH` and
`CURIS_WORKSPACE_DB` before import. Final before/after fingerprints are recorded after
the combined regression.

| Active path | Before / after size | Before / after mtime | Before / after SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896 / 1232896` | `1786873339 / 1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` / same | `ok / ok` |
| `backend/data/curis.sqlite` | `1277952 / 1277952` | `1786783659 / 1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` / same | `ok / ok` |

Both active databases are unchanged.

## Acceptance Questions

1. **Canonical Learning truth:** existing hashed Artifact + existing Series/Cycle refs and explicit acceptance provenance.
2. **Second Memory system:** NO.
3. **Evidence-bound source:** YES.
4. **Real Two-Cycle evidence:** YES, accepted RD Primary proof.
5. **Candidate vs Accepted separated:** YES, distinct Artifact records/status.
6. **Who accepts:** active Leader for bounded Workspace/Domain use; CEO for Company/protected promotion.
7. **CEO gates:** Company, Strategy, Goal, Package and Company policy use.
8. **Scope:** canonical Workspace/Domain/Company candidate checks plus resolver filtering.
9. **RD leakage into XHS:** NO.
10. **Conflict:** explicit conflict must supersede; otherwise fail closed; invalidation archives history.
11. **Restart/replay:** YES.
12. **Automatic Strategy change:** NO.
13. **Automatic Package change:** NO.
14. **Cycle 3:** NO.
15. **Future Context reference:** YES, compact reference-first resolver.
16. **Evidence-bound Learning:** **IMPLEMENTED / ACCEPTED**.
17. **Remaining V1:** product/API surfacing, external live provider quality, broader domain evidence and any future promotion policy are separate gates.

## Commit Boundary

CEO accepted Phase C on 2026-08-21. The exact bounded Runtime implementation and
evidence are authorized for commit; no Product/API/UI or self-modification scope is
included.
