# CURIS AUTONOMOUS CROSS-SURFACE MULTI-WORK RUNTIME PROOF REVIEW

Authority Class: REVIEW
Status: Frozen
Disposition: PROOF IMPLEMENTED / ACCEPTED
Date: 2026-08-22

## 2026-08-22 Foundation Accepted → Proof Reopened

The 2026-08-21 blocked audit below remains the truthful historical pre-Foundation
record. CEO Acceptance of the Canonical Child Work Foundation removed that exact Stop
Gate. No historical finding was deleted or reinterpreted.

### Actual XHS E2E

The reopened proof uses the existing XHS Workspace controlled-provider path and no new
Runtime source:

```text
one Workspace / one Operating Series / one Cycle
→ Work A / Research Assignment / Research Employee
→ Provider Task A / Session A / Result A / Artifact A / Evidence A / Acceptance A
→ completed runtime-acknowledged Handoff + accepted Result A
→ exactly-one Work B
→ Work B / Content Assignment / Content Employee
→ Provider Task B / Session B / Result B / Artifact B / Evidence B / Acceptance B
→ Work-scoped Cycle Evaluation
→ canonical Workspace Leader Review
→ exactly-one existing DECISION_PACKET / WAIT
```

Surface labels are not Runtime authority. The fixture uses the accepted XHS domain
semantics and existing Workspace/Business records; it does not depend on Surface
Registry, Package v2, navigation or frontend.

### Runtime Truth Evidence

- Work A and Work B have distinct canonical `WORK` IDs under the same Cycle.
- Work A pins `xhs-research`; Work B pins `xhs-copy`.
- Both resolve existing Workspace-scoped Assignments and canonical Employees.
- Each Work executes through `ResponsibilityRoutingRuntime`, the real Team Operating
  endpoint, ResultStore Task/Artifact and persisted provider Session/event evidence.
- Work B is created only by `release_next_work()` after Work A completion and accepted
  Result; direct test insertion is not used.
- Handoff and Work B share deterministic release truth; replay returns the same pair.
- Work A/B Evidence is parented independently; Work A/B Acceptance is independently
  CLOSED and covers that Work's Result/Evidence.
- Cycle close persists the child Work aggregation hash and summaries. Evaluation
  recomputes that hash and carries both Work refs and Acceptance refs.
- The pre-existing Workspace Leader Assignment/Employee performs the existing Leader
  Review. No Research/Content reviewer identity was introduced.
- Decision replay returns the same `DECISION_PACKET`; `successorCycleRef=null`.

### Exact Successful-Proof Counts

| Truth | Count |
|---|---:|
| Operating Series | 1 |
| Cycle | 1 |
| canonical Work | 2 |
| Responsibility Assignments | 4 |
| canonical Employees | 4 |
| Provider Tasks | 2 |
| Provider Sessions | 2 |
| Artifacts | 2 |
| Evidence | 3 (2 Work + 1 Cycle aggregate) |
| Acceptances | 3 (2 Work + 1 Cycle) |
| Handoffs | 1 |
| Evaluation | 1 |
| Leader Review | 1 |
| Decision Packet | 1 |
| Successor Cycle | 0 |
| Learning | 0 |

### Restart / Replay / Concurrency

- restart after Work A completion reads the same Work A Result truth;
- release and Handoff replay return the same Work B/Handoff;
- restart after release reads the same Work B;
- replayed Work execution creates no second Provider Task/Session;
- replayed Work completion creates no second Work result projection;
- restart after Work B completion reconstructs both Work and aggregate hash;
- Evaluation replay returns one Evaluation;
- Leader Review/Decision replay returns one Review and one Decision;
- the accepted Foundation concurrent-release and transaction-abort proofs were rerun.

### Failure Evidence

The reopened proof directly verifies unavailable Content Employee and missing Content
Evidence fail closed while the Operating Series remains ACTIVE. The combined accepted
Foundation/XHS suites additionally verify invalid/malformed Result, capability missing,
invalid parent/Assignment/Employee/scope, cross-tenant access, release conflict,
concurrent release and restart/transaction interruption. Ordinary Work failure does not
STOP the Series.

### Regression

- reopened Track C proof: `2 passed`;
- Canonical Child Work Foundation focused suite: `5 passed`;
- Autonomous Phase 1/2/3A/3B, primary two-cycle, XHS cross-domain,
  evidence-bound Learning, Responsibility Routing, Team Operating real Employee E2E
  and DB Safety, combined with the above: `85 passed`;
- Python compile: PASS;
- diff whitespace check: PASS.

### Current Boundaries

- sequential multi-Work: PROVED;
- parallel/fan-out/fan-in/join/DAG/scheduler: NOT IMPLEMENTED / NOT PROVED;
- Surface Runtime: not added;
- Package v2 dependency: none;
- live external XHS publishing/analytics: not part of this controlled Runtime proof;
- no successor Cycle and no Learning were created.

### Reopened Acceptance Questions

1. 同一个 Cycle：是，Cycle=1。
2. 至少两个 canonical Work：是，Work=2。
3. work_id 彼此不同：是。
4. 至少两个专业 Responsibility：是，Research与Content。
5. 真实 Assignment / Employee：是，均为既有Workspace-scoped canonical truth。
6. Work B由Work A accepted Result/Handoff合法释放：是。
7. Work B exactly-once：是，release/restart replay返回同一ID。
8. Work A/B独立Result：是，Provider Task refs各一。
9. 独立Evidence：是，各自parent到对应Work。
10. 独立Acceptance：是，各自CLOSED且覆盖对应Result/Evidence。
11. Evaluation按Work聚合：是，包含两Work summaries/refs/hash。
12. missing Work Evidence fail-closed：是。
13. 真实Workspace Leader Review：是，复用Series的canonical Leader。
14. Decision exactly-once：是，Decision=1。
15. restart不重复Work：是。
16. replay不重复Result/Evaluation/Decision：是。
17. one-active-Cycle：保持，Cycle=1。
18. 创建successor：否，0。
19. 生成Learning：否，0。
20. 实现parallel：否，未实现/未证明。
21. 新增Surface Runtime：否。
22. 依赖Package v2：否。
23. XHS真正证明跨专业multi-Work：是，Research→Content独立Work链。
24. 可正式称为Cross-Surface/Cross-Professional Multi-Work Runtime Proof：是，
    其中Cross-Surface是产品投影含义，Runtime事实是Cross-Professional Work。
25. Product Integration剩余：Surface/UI投影、Package mapping、真实外部发布/分析，
    以及未来如有授权的parallel proof；均不属于本Runtime Proof。

### Reopened Verdict

`CURIS AUTONOMOUS OPERATING — CROSS-PROFESSIONAL MULTI-WORK RUNTIME PROOF IMPLEMENTED`

Ready for CEO Acceptance Review. Parallel multi-Work remains explicitly outside this
proof.

---

## Historical 2026-08-21 Pre-Foundation Blocked Audit

## A. Authority Mapping

Frozen product authority permits multiple Work inside one Workspace Cycle and keeps
Surface as projection only. Current Runtime implements the Workspace/Team/Cycle side,
but not distinct Work identity under one Cycle. Product truth is therefore not yet an
implemented Runtime truth.

## B. Runtime Truth Audit

1. `RuntimeFoundation` registers `CYCLE`, `HANDOFF`, `DECISION_PACKET`, `ACCEPTANCE`
   and domain objects, but no canonical `WORK` entity/machine.
2. `AutonomousOperatingControl.materialize_cycle_work()` calls
   `ResponsibilityRoutingRuntime.start_work(cycle_id, ...)`: the Cycle itself is the
   routed Work.
3. `start_work()` stores one `responsibilityRouting` object on the supplied entity and
   returns that entity unchanged on replay.
4. Team Operating supports multiple Employee executions and real Handoffs, but they
   all retain the same `workRef`.
5. Handoff changes the Assignment/holder and persists transitions atomically on that
   same Work; it neither creates nor references a next Work.
6. Cycle close copies one routing record's accumulated refs into one Cycle Evidence
   and Acceptance.
7. Evaluation reads flat Cycle `resultRefs`, `artifactRefs`, `evidenceRefs` and one
   Acceptance. It does not validate Work membership or per-Work completeness.

## C. Primary Domain Readiness

XHS has the strongest semantic sequence (topic/research/content) and accepted distinct
Employees, provider results and Handoffs. RD also has real execution/review truth.
Neither can satisfy `Work >= 2` without inventing a shared Work identity.

## D. Selected Proof Domain

XHS is selected as the future primary domain, but implementation is **BLOCKED** before
fixture creation. This avoids relabeling its current one-Work/multi-execution proof.

## E. Exact Allowed Files

- `issues/20260821_autonomous_cross_surface_multi_work_runtime_proof_001.md`
- `docs/reviews/CURIS_AUTONOMOUS_CROSS_SURFACE_MULTI_WORK_RUNTIME_PROOF_REVIEW.md`

No source or test file changed.

## F. Multi-Work Contract

Not implementable from current accepted seams. The existing Cycle owns one routing
record, not multiple canonical Work objects.

## G. Responsibility / Assignment Model

Reusable and real: Workspace-scoped Assignments, canonical Employee identity,
different Employees for different Responsibilities, and one Employee across separate
Assignments are supported. What is missing is the Work-scoped binding boundary.

## H. Work Release Contract

Missing. No accepted Result/Handoff operation releases exactly one next Work under the
same Cycle. Test-side `foundation.create()` would bypass the required Runtime truth.

## I. Handoff Contract

Existing Handoff is a real, persisted, acknowledged accountability transfer. It is
same-Work responsibility routing, not cross-Work release.

## J. Result / Evidence Provenance

Provider Tasks, Sessions, Artifacts and Evidence are distinct and verified, but their
refs are aggregated on one routed entity. Per-Work provenance is not canonical.

## K. Same-Cycle Ownership

One Cycle is canonical. Multiple Work ownership is missing and therefore unproved.

## L. Sequential Proof

**NOT PROVED.** Existing topic → research → copy sequence proves multiple
Responsibilities/executions within one Work only.

## M. Parallel Proof Status

**NOT PROVED.** No canonical multi-Work model or merge semantics exists. No DAG,
scheduler or join primitive was added.

## N. Evaluation Aggregation

Current Evaluation aggregates multiple flat Result/Evidence refs, but cannot prove
they came from distinct required Work or that all Work were satisfied.

## O. Leader Review

The canonical Workspace Leader and exactly-once review are reusable once a valid
multi-Work Evaluation exists. They are not the blocker.

## P. Decision

The existing `DECISION_PACKET` is reusable and exactly-once. No Decision was created
by this audit.

## Q. Restart / Replay

Current one-Work runtime is restart/replay safe. Required Work B release/recovery
cannot be tested because the release operation and identity do not exist.

## R. Transaction Safety

Same-Work Handoff is atomic. The required accepted Result A → Handoff → exactly-one
Work B transaction is absent, so half-chain and duplicate prevention cannot be proved.

## S. Failure Matrix

Current assignment, provider, callback, Handoff and scope failures are fail-closed.
Cross-Work interruption/recovery remains untestable rather than silently successful.

## T. Exact Object Counts

No proof objects were created. Required success counts (`Cycle=1`, `Work>=2`,
`Decision=1`, `successor=0`, `Learning=0`) are **NOT CLAIMED**.

## U. Active DB Safety

No test or initialization used either active database.

| Active path | size | mtime | SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

## V. Regression

No implementation was made, so no new focused suite was created. Previously accepted
Autonomous V1 core and Team Operating evidence remains the baseline; this audit does
not reinterpret it as multi-Work proof.

## W. Remaining Product Integration Gaps

1. an authorized minimal canonical child Work identity under an existing Cycle;
2. exactly-once Result/Handoff → next Work release;
3. Work-scoped Result/Evidence/Acceptance aggregation into Cycle Evaluation;
4. only after those exist, XHS cross-Surface projection and Package integration.

## X. Commit Recommendation

No commit. Keep both documents unstaged for CEO review as required.

## Acceptance Questions

1. Existing Cycle contains multiple canonical Work: **NO**.
2. At least two Responsibilities exist: **YES in current one-Work Team Operating; not a multi-Work proof**.
3. Real Workspace Assignments reused: **YES in current baseline**.
4. Canonical Employees execute: **YES in current baseline**.
5. Real Handoff occurs: **YES in current baseline**.
6. Handoff is accountability transfer: **YES, but within the same Work**.
7. Work A / Work B independent Results: **NO canonical Work A/B identity**.
8. Independent Evidence: **provider evidence exists; Work-scoped ownership is NO**.
9. Both belong to one Cycle: **NOT PROVABLE because distinct Work do not exist**.
10. One-active-Cycle invariant: **YES in current baseline**.
11. Legal Runtime releases second Work: **NO**.
12. Evaluation consumes multiple Work Evidence: **NO; it consumes flat Cycle refs**.
13. Real Workspace Leader Review: **YES in current baseline, not exercised here**.
14. Exactly one Decision: **not exercised; 0 created**.
15. Successor Cycle: **0 created**.
16. Learning: **0 created**.
17. Restart avoids duplicate Work: **not testable for absent Work B**.
18. Restart avoids duplicate Handoff: **supported for same-Work baseline; not exercised here**.
19. Replay avoids duplicate Result: **supported for same-Work baseline; not a Work B proof**.
20. Transaction interruption avoids half responsibility chain: **NO cross-Work transaction exists**.
21. Parallel multi-Work: **NOT PROVED; canonical multi-Work and merge semantics are absent**.
22. Surface Runtime added: **NO**.
23. Unfrozen Package Schema dependency: **NO**.
24. Can this be called Cross-Surface Multi-Work Runtime Proof: **NO**.
25. Remaining Product Integration: shared Work identity/release/aggregation first;
    Surface UI and Package mapping remain later separate gates.

## Final Verdict

`STOP FOR CEO REVIEW — EXISTING CYCLE CANNOT YET OWN MULTIPLE CANONICAL WORK`

The truthful current capability is:

`ONE CYCLE → ONE ROUTED WORK OBJECT → MULTIPLE RESPONSIBILITIES / EMPLOYEE EXECUTIONS / HANDOFFS`.

It must not be relabeled as:

`ONE CYCLE → MULTIPLE CANONICAL WORK`.
