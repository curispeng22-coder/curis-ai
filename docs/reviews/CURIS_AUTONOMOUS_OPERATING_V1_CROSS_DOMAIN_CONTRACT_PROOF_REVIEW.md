# CURIS AUTONOMOUS OPERATING V1 — CROSS-DOMAIN CONTRACT PROOF REVIEW

Authority Class: REVIEW
Status: Review
Disposition: IMPLEMENTED / ACCEPTED

## Verdict

The same accepted Autonomous Operating lifecycle completed one bounded XHS
content-production Cycle without an XHS-specific Series, Cycle, Team execution,
Evaluation or Decision runtime. The proof uses canonical XHS Workspace and
`ContentItem` truth, four canonical Employees, the real Team Operating callback
path, typed content Results, ResultStore Artifacts, Provider and Cycle Evidence,
Acceptance, Evaluation, Leader Review and one existing `DECISION_PACKET`.

This is a **Cross-domain Contract Proof**, not a second Primary E2E and not a claim
that XHS publishing or analytics is connected. The `ContentItem` remains `DRAFT`;
the final content result says `publicationStatus=NOT_CONNECTED` and
`analyticsStatus=UNAVAILABLE`; no platform metric or receipt is generated.

## Cross-domain Readiness Matrix

| Candidate | Canonical scope | Team/Employee/Provider | Professional object/result | External truth | Decision | Verdict |
|---|---|---|---|---|---|---|
| XHS | Company → Department → Business → XHS Workspace | accepted Team Operating path; controlled Provider callback | real `ContentItem`/version; topic plan, research brief, reviewable publish package | publishing not connected; analytics unavailable | existing Autonomous Decision | **SELECTED — READY FOR BOUNDED CONTRACT PROOF** |
| TTK | canonical Workspace foundation exists | capability supply remains partial | content/video draft semantics exist but supply proof is weaker | publishing/result connectors unavailable | shared Decision reusable | **PARTIAL — NOT SELECTED** |
| Generic Package Workspace | canonical Package Workspace and Team Operating are available | controlled execution is possible | declarative object/result semantics vary by package | package-dependent | shared Decision reusable | **READY BUT WEAKER PROFESSIONAL CONTRAST** |

XHS was selected because it has the strongest non-RD professional object and accepted
team semantics. Its missing publishing/analytics integrations are made explicit rather
than bypassed.

## Same Shared Lifecycle

The proof reuses, unchanged:

```text
OPERATING_SERIES
→ RESULT Trigger Claim
→ CYCLE
→ approved Strategy / Envelope / Plan pins
→ existing Team Operating definition
→ Responsibility Assignment
→ canonical AI Employees
→ Provider Tasks / Sessions / verified callbacks
→ ResultStore Artifacts / provider evidence
→ Cycle Evidence / Acceptance
→ evidence-bound Evaluation
→ Leader Review
→ existing DECISION_PACKET
→ WAIT (no successor)
```

No production Runtime, Schema, API or frontend file changed.

## Required Domain Differences

| Semantic | RD Primary | XHS Cross-domain proof |
|---|---|---|
| Goal | controlled code/test change | truthful, reviewable XHS content asset |
| Strategy | bounded software correction and regression | audience hypothesis, content angle and one-review cadence |
| Team | RD operating leader | content leader + topic + research + copy Employees |
| Work | project/cycle code verification | real XHS `ContentItem` and immutable version |
| Result | `rd-operating-result` | `xhs-topic-plan`, `xhs-research-brief`, `xhs-publish-package` |
| Evidence | code/test execution evidence | typed content outputs plus verified Provider/Cycle provenance |
| Evaluation | software result and regression correctness | content readiness, source sufficiency, brand/publish boundary |
| Value | verified software correctness | reviewable content asset; no invented performance KPI |
| Risk gate | protected goal/budget | protected goal/brand/external publication authority |

The Provider is a deterministic controlled local callback. It proves the real
Task/Session/callback and Result contract path, not external model quality or cost.

## Runtime Evidence

The successful proof persisted:

- one canonical XHS Business and Workspace;
- one `ContentItem` plus immutable `ContentVersion`;
- one Operating Series, Trigger Claim and Cycle;
- four Employee Assignments, with three Employee executions;
- three distinct Provider Tasks/Sessions and typed results;
- three ResultStore Artifacts and Provider usage evidence;
- one Cycle Evidence and one Acceptance;
- one XHS-specific Evaluation and one Leader Review;
- one `DECISION_PACKET` with `WAIT`;
- zero successor Cycles and zero accepted Learning.

Restart recreates `AutonomousOperatingControl` from the same isolated SQLite and reads
the same Series/Cycle/Decision. Replaying the Decision returns the same packet and
`authorize_successor()` returns no Claim/Cycle. Cross-tenant lookup fails closed.

## Failure / Authority Evidence

| Case | Observed truth |
|---|---|
| missing capability | Plan materialization rejects before any Provider call |
| malformed XHS Result | Team Operating waits; Cycle is explicitly failed; no Acceptance/Decision/Learning |
| insufficient Evidence | `CONTINUE` is rejected; `ESCALATE` creates one CEO-gated existing Decision packet |
| protected publication adjustment | requested `ADJUST` resolves to `ESCALATE / WAITING_CEO` |
| stale Workspace Goal | pinned-goal check blocks work release |
| unavailable Leader | Leader Review is rejected |
| cross-tenant read | canonical Series cannot be resolved |
| restart/replay | same persisted records; no duplicate Provider work or successor |

## Tests

- XHS Cross-domain focused suite: `6 passed`.
- Combined Phase 1–3B, Primary Two-Cycle, XHS Cross-domain, Team Operating,
  Responsibility Routing and DB Safety: `73 passed`.
- Python compile: PASS.
- `git diff --check`: PASS.

## Active DB Safety

All tests set `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` to one
repository-external temporary SQLite before import. Final size/mtime/SHA/integrity
comparison is recorded after the combined regression. No active database is an input.

| Active path | Before / after size | Before / after mtime | Before / after SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896 / 1232896` | `1786873339 / 1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` / same | `ok / ok` |
| `backend/data/curis.sqlite` | `1277952 / 1277952` | `1786783659 / 1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` / same | `ok / ok` |

Both active databases are unchanged.

## Acceptance Questions

1. **Second Domain:** XHS content operations.
2. **Why selected:** strongest accepted non-RD Domain object and Employee team path.
3. **Professional difference from RD:** content audience/source/review semantics, not code/test semantics.
4. **Same lifecycle reused:** YES.
5. **New Domain Runtime:** NO.
6. **Different Result semantics:** YES, typed content planning/research/package outputs.
7. **Different Evidence semantics:** YES, content output/provenance; no software diff/test claim.
8. **Different Evaluation semantics:** YES, content readiness/source/risk boundary.
9. **Different Value semantics:** YES, reviewable content asset; no universal KPI.
10. **Leader/Team real:** YES, canonical Workspace Assignments and Employees.
11. **Employee/Provider real path:** YES; controlled Provider, not external live quality proof.
12. **Restart/replay:** YES.
13. **Learning produced:** NO.
14. **Cross-domain Contract Proof:** **PASSED**, bounded before publishing/analytics and ContentItem lifecycle bridge.

## Remaining Boundary

- No Autonomous Result-to-`ContentItem` lifecycle mutation is claimed.
- Real XHS publishing, receipt and analytics connectors remain unavailable.
- This proof does not establish a second two-cycle Production E2E.
- CEO accepted Phase B on 2026-08-21. The bounded proof is authorized for its own
  exact-manifest commit; no XHS production claim is added by that acceptance.
