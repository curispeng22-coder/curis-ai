# CURIS AUTONOMOUS OPERATING V1 — LONG-RUN CLOSURE REPORT

Authority Class: REVIEW
Status: Review
Disposition: IMPLEMENTED / ACCEPTED

## A. Primary Two-Cycle Baseline

The previously CEO-accepted RD Primary proof was revalidated and committed as an
independent three-file baseline:

- commit: `c311a62aa4a4a5d0b372e03af99bebe4db12b86a`;
- message: `test(runtime): prove primary autonomous two-cycle e2e`;
- exact counts: 2 Cycles, 2 Trigger Claims, 2 Provider Tasks, 2 Artifacts,
  2 Evidence, 2 Acceptances, 2 Evaluations, 2 Leader Reviews, 2 Decisions;
- Cycle 3: 0;
- Learning at Phase A: 0;
- regression: `74 passed`;
- pushed: NO.

## B. Cross-domain Contract Proof

XHS passed as the second Domain using the same Operating Series/Cycle/Trigger,
Team Operating, Employee/Provider, Result/Artifact/Evidence/Acceptance, Evaluation
and Decision contracts.

Professional differences are real:

- RD: controlled code/test result and software correctness value;
- XHS: audience/content/source/review strategy, topic/research/content package result,
  content-readiness evaluation and reviewable-content-asset value.

The proof uses a canonical XHS `ContentItem` and immutable version as Domain work,
four canonical Employees and three real Task/Session/callback executions. It creates
no XHS Autonomous Runtime. Publishing remains `NOT_CONNECTED`; analytics remains
`UNAVAILABLE`; the `ContentItem` remains `DRAFT`; no fake receipt, metric or KPI exists.

Phase B focused: `6 passed`. Phase B combined regression: `73 passed`.
Phase B was accepted by the CEO on 2026-08-21 and committed as bounded proof
`688bacbab` (`test(runtime): prove autonomous cross-domain contract`).

## C. Evidence-bound Learning

The minimal Learning path reuses existing hashed Artifact persistence and existing
Series/Cycle references. It adds no table, Memory system, Learning Engine, Workflow,
API or UI.

```text
Two closed Cycles
→ canonical Result/Evidence/Acceptance/Evaluation/Decision validation
→ Learning Candidate Artifact (generated)
→ explicit Leader/CEO authority
→ separate Accepted Learning Artifact (accepted)
→ reference-first future Context resolver
```

Learning is:

- evidence-bound and two-Cycle-bound;
- Workspace/Domain/Company-candidate scoped;
- confidence/conditions/limitations/revalidation aware;
- reviewable and deterministic under replay/concurrent acceptance;
- supersedable/invalidateable without deleting history;
- isolated across RD and XHS unless explicit CEO Company promotion exists.

Learning never automatically changes Strategy, Goal, Envelope, Methodology, Package,
prompt authority, capability routing or code. Future use is reference-only Context,
Plan input or Evaluation input. No Cycle 3 is created.

Phase C focused: `5 passed`. Full long-run regression: `85 passed`.
Phase C was accepted by the CEO on 2026-08-21 and is assigned to its bounded Runtime
commit.

## D. Runtime Reuse

Reused unchanged:

- canonical Company/Department/Business/Workspace;
- Operating Series, Trigger Claim and Cycle;
- Responsibility Routing and Team Operating;
- canonical Employee/Provider Task/Session/callback;
- ResultStore Task/Artifact;
- Runtime Evidence/Acceptance;
- Evaluation, Leader Review and Decision Packet;
- existing `artifacts` generated/accepted/archived lifecycle.

Only `AutonomousOperatingControl` receives bounded Learning candidate/acceptance,
retrieval and invalidation helpers. No second truth system exists.

## E. Domain Differences

The Cross-domain proof does not encode XHS performance metrics into Core. XHS Domain
semantics live in approved Strategy/Plan/Result/Evaluation payloads; Core only validates
canonical scope, Employee execution, typed Result, Evidence and authority transitions.

## F. Learning Boundaries

- Candidate is not Accepted Learning.
- Employee/LLM summary alone is not Learning.
- one Cycle is insufficient.
- stale/unverified Evidence blocks promotion.
- protected/Company use requires CEO.
- explicit conflicts require supersede authority.
- invalidated/superseded Learning remains archived history.
- accepted Learning can be retrieved, but cannot mutate authority.

## G. Active DB Safety

Every test used one repository-external SQLite through all three DB environment
variables before import.

| Active path | Final size | Final mtime | Final SHA-256 | integrity | Changed |
|---|---:|---:|---|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` | NO |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` | NO |

## H. Git State

- HEAD: `c311a62aa4a4a5d0b372e03af99bebe4db12b86a`;
- Phase A: committed, not pushed;
- staged tree: empty;
- Phase B: three untracked review-ready files;
- Phase C: one tracked bounded Runtime diff plus four untracked Issue/test/Review/report files;
- all unrelated tracked/untracked preserved worktree content remains untouched.

## I. Separate Future Gates

- external live Provider quality/cost remains unverified;
- real XHS publishing/receipt/analytics remain unavailable;
- no Autonomous Result-to-`ContentItem` lifecycle bridge is claimed;
- no Product/API/UI surface for Learning exists;
- no automatic cross-company/domain generalization;
- no Cycle 3 or indefinite autonomous operation proof;
- no Strategy/Package/code self-modification.

## J. Next Gate

Autonomous new-feature development stops. The next separate gate is Autonomous
Operating Runtime × Professional Workspace Product Integration after its product
authorities are reconciled. This report does not authorize that work.

## Final Evidence

- Cross-domain focused: `6 passed`.
- Learning focused: `5 passed`.
- Full Autonomous/RD/XHS/Team/DB Safety regression: `85 passed`.
- Python compile: PASS.
- `git diff --check`: PASS.
- Active DB: unchanged.
- Cycle 3: 0.
- Second Runtime: 0.
- Self-modifying software: 0.

**CURIS AUTONOMOUS OPERATING V1 — CEO ACCEPTED / CORE IMPLEMENTATION BASELINE CLOSED**
