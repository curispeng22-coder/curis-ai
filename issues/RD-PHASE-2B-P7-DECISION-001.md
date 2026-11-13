# RD-PHASE-2B-P7-DECISION-001

**Status:** IMPLEMENTED / INTEGRATION PASS / REAL PROVIDER REPLAY PENDING
**Date:** 2026-08-17
**Owner:** Curis main development / RD Workspace

## Goal

Implement one high-risk RD P7 Decision Packet on an accepted Developer responsibility:

```text
completed real RD execution + approved Artifact Review
→ one persisted DECISION_PACKET READY / WAITING_CEO
→ Layer 0 only VIEW_OPTIONS / DEFER
→ CEO reads Layer 1
→ CEO chooses one explicit option
→ same Decision becomes DECIDED / APPLIED
→ original Responsibility Holder remains
→ existing RD execution path automatically continues with the selected bounded instruction
```

No Handoff is created and no responsibility is transferred.

## Authority

1. `docs/00_Context/CURRENT_STATE.md`
2. Frozen `Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` §3.3/§3.13 P7
3. approved `Curis_RD_Workspace_Instance_Spec_v1.md` §7
4. `docs/04_Development/RD_PHASE_2B_PRE_IMPLEMENTATION_AUDIT.md` §6.2
5. accepted RD Phase 0/1, 2A, 2B-1 Reviews and Phase 2B-2 backend record

## Preserved baseline

Git HEAD at authorization: `a31504216`.

| Path | Pre-change SHA-256 |
| --- | --- |
| `backend/app/runtime/workspace.py` | `00a795c28a8e96565823a19697be9bacbc1d90cb8111a4ccf9396cf7eecac282` |
| `backend/app/api/runtime_foundation_router.py` | `2ff5d8bc2785063329760dc67661d65af728a82774da69db435e0b72ea82dfef` |
| `frontend/components/rd/RdWorkspacePhaseTwo.js` | `99298f443039c07e4c29b76fa3363fb40bfe6485635f090aeaa26ecfce0220a8` |
| `frontend/lib/runtimeApi.js` | `e60bf87333378dafc64ba318b3c70313baefac5f10df879ad7aa992094ace04f` |

Active DB read-only baseline remains SHA-256
`2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`,
size `1232896`, mtime `1786873339`.

## Owned boundary

- RD P7 commands adjacent to accepted RD methods in `workspace.py`.
- DTOs/endpoints/background continuation in the existing Runtime router.
- RD-only API wrappers and compact Decision UI projection.
- new focused tests, this Issue and its Review.

No shared registry/state/Foundation, XHS/TTK, Frozen Authority, Product Blueprint, active DB
or Provider/Agent implementation may change.

## Contract

1. Decision requires completed RD execution, approved Artifact Review, real Evidence and an
   inactive Current Executor.
2. Packet semantically includes: event, why AI cannot decide, options with impact/risk/cost,
   recommendation, recommendation reason, CEO choice prompt and continuation plan.
3. Impact/risk/cost/recommendation fields use only `FACT`, `POLICY`, `EVIDENCE`, `EST`, `UNK`.
4. High-risk Layer 0 exposes only `VIEW_OPTIONS` and `DEFER`.
5. Choice cannot apply before a persisted Layer 1 reviewed timestamp.
6. `DEFER` keeps `WAITING_CEO`, preserves holder and executor `none`.
7. Applying one valid option keeps the holder, creates no Handoff, archives prior Task/result
   refs, sets the selected bounded instruction/resource/test command, and atomically starts
   the existing RD Task path.
8. Duplicate create/view/choice is idempotent and creates no second Decision or Task.
9. Failure after choice uses the accepted RD failure/Evidence/retry truth; restart fails closed.

## Explicit exclusions

- generic approval engine or second Decision primitive;
- low-risk direct Banner approval;
- DB migration execution against Curis or any active database;
- Handoff, Organization Routing or Shared identity changes;
- multiple pending Decision Packets or arbitrary decision workflows;
- final visual design, packaged Desktop acceptance, push.

## Acceptance

1. One Decision Packet follows `DRAFT → READY → WAITING_CEO → DECIDED → APPLIED`.
2. Unreviewed high-risk choice is rejected; defer stays pending.
3. Provenance validation fails closed.
4. Applied choice automatically invokes one existing RD execution, with original holder equal
   to Current Executor only while real work runs and executor `none` afterward.
5. Same Decision, prior/new Task, Artifact/Evidence and result refs survive restart.
6. Handoff count remains zero; accepted RD/XHS/DB-safety behavior does not regress.

## Implementation outcome

The P7 Runtime/API/UI path is implemented. A high-risk packet cannot apply before Layer 1
review, provenance is fail-closed, defer remains pending, and one applied option restarts the
accepted asynchronous RD execution path on the same Cycle and original holder. Previous
Task/Artifact/Result/Review refs move into durable history instead of being overwritten.

Focused integration uses the real Runtime execution adapter boundary with a deterministic
executor and proves one automatic continuation call. The already accepted real Codex path
passes no-regression, but a fresh real-provider replay of this new P7 continuation was not
run in this batch; that evidence remains explicitly pending.
