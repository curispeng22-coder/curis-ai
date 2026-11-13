# CURIS CANONICAL CHILD WORK FOUNDATION REVIEW

Authority Class: REVIEW
Status: Frozen
Disposition: IMPLEMENTED / ACCEPTED
Date: 2026-08-21
Issue: `issues/20260821_canonical_child_work_foundation_001.md`

## A. Blocker Mapping

The prior truth was one Cycle used as one routed `workRef`. The implementation adds
canonical child `WORK` rows; it does not reinterpret the legacy Cycle row or claim
that the previous Track C proof already contained multiple Work.

## B. Persistence Feasibility

Existing `runtime_entities` and `runtime_links` are sufficient. Work identity uses the
existing entity primary key. Cycle/lineage links use the existing unique link key.
Deterministic IDs plus `BEGIN IMMEDIATE` provide serialized, persistent replay. No
schema, index, table or migration was added.

## C. Exact Allowed Files

- `backend/app/runtime/child_work.py` — canonical Work, lifecycle, outcome validation,
  release transaction, lineage and aggregation.
- `backend/app/runtime/autonomous_operating.py` — bounded child-Work-aware close and
  Evaluation branches; legacy fallback retained.
- `backend/tests/test_canonical_child_work_foundation.py` — isolated proof.
- Issue and this Review.

No other file was modified by this Issue.

## D. Canonical Work Contract

Each `WORK` has a deterministic ID distinct from its Cycle, exactly one Cycle
`parent_id`, Workspace/Company scope, immutable Assignment/Responsibility/holder
snapshot, lifecycle, input refs, independent Result/Artifact/Evidence/Acceptance refs,
release key and row timestamps. The row is generic Shared Runtime truth.

Lifecycle implemented: `PLANNED → READY → ACTIVE`; ACTIVE may become WAITING,
BLOCKED, COMPLETED, FAILED or CANCELLED. WAITING/BLOCKED may resume ACTIVE or end
FAILED/CANCELLED. Terminal states cannot transition.

## E. Cycle → Work Relation

`Cycle -HAS_WORK→ Work`; successor and predecessor use
`HAS_SUCCESSOR_WORK` / `HAS_PREDECESSOR_WORK`. Tests prove one Cycle owns two
distinct Work IDs and preserves the lineage in SQLite.

## F. Backward Compatibility

When a Cycle has no child `WORK`, aggregation returns `LEGACY` and the pre-existing
flat `responsibilityRouting`, provider-event validation, close and Evaluation behavior
is unchanged. Autonomous Phase 1–3B, primary two-cycle and cross-domain tests pass.

## G. Responsibility / Assignment Binding

Creation resolves an existing Workspace-scoped `RESPONSIBILITY_ASSIGNMENT`, validates
Company/Workspace scope and a canonical AVAILABLE/OPERATING `AI_EMPLOYEE`, and stores
the Assignment revision and responsibility snapshot. A focused proof uses the same
Employee through two distinct Assignments without copying identity.

## H. Result / Evidence / Acceptance Ownership

Completion accepts only completed ResultStore Task refs, Artifacts owned by those
Tasks, VERIFIED/CURRENT Evidence parented to the Work, and CLOSED Acceptance parented
to the Work covering the same Result and Evidence. Missing or invalid truth fails
closed. Each Work owns separate refs before entering COMPLETED.

## I. Handoff vs Work Release

Existing same-Work Handoff remains untouched. The new bounded release seam requires a
completed parent Work, one accepted parent Result, a deterministic release key and a
valid target Assignment. One existing-type Handoff records release provenance; the
Handoff and successor Work are distinct objects.

## J. Exactly-one Release

The successor Work ID is deterministic from tenant, parent Cycle, parent Work and
release key. The Handoff ID is deterministic from tenant, parent Work and release key.
Same replay returns the same pair. A different target using the same release identity
fails closed. Two concurrent callers produced one Handoff and one successor Work.

## K. Transaction Boundary

One `BEGIN IMMEDIATE` transaction validates the parent/target, inserts Handoff,
creates successor Work, records Handoff lifecycle and persists all lineage links.
An injected SQLite abort at successor Work insertion rolled back the preceding
Handoff; retry then created one complete pair.

## L. Work Lineage

Work A retains its completed data byte-for-byte after Work B release. Work A links to
Work B; Work B links back to Work A and stores `predecessorWorkRef`. No lineage engine
or graph scheduler was introduced.

## M. Restart / Replay

Proof covers replayed Work creation, replayed Work completion, restart before release,
concurrent/replayed release, restart after Work B and aggregate reconstruction after
Cycle close. Deterministic identity prevents a second Work B.

## N. Cycle Aggregation

For child Work Cycles, aggregation validates every required Work and records Work
summaries plus distinct Result, Artifact, Evidence and Acceptance refs. It exposes
required/completed/failed Work sets and a deterministic aggregation hash. An incomplete
required Work or invalid Evidence/Acceptance blocks close.

## O. Evaluation Update

Cycle close persists `MULTI_WORK_EXECUTION` Evidence with per-Work provenance and the
aggregation hash. Evaluation recomputes and compares that hash, includes Work summaries
and Acceptance refs, and accepts observed facts only from current Cycle/Work truth.
Legacy Evaluation remains unchanged when no child Work exists.

## P. Failure Matrix

Verified fail-closed behavior for invalid parent type, missing Assignment, missing
Employee, cross-Workspace Assignment scope, cross-tenant read, incomplete predecessor,
missing Result/Evidence/Acceptance, pending Acceptance, incomplete required Work,
conflicting Work replay, conflicting release target and transaction interruption.

## Q. Active DB Safety

All tests used one repository-external SQLite referenced by `CURIS_DB`,
`CURIS_DB_PATH` and `CURIS_WORKSPACE_DB`.

Before and after:

- `data/curis.sqlite`: size `1232896`, mtime `1786873339.9558418`, SHA-256
  `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`,
  `integrity_check=ok`.
- `backend/data/curis.sqlite`: size `1277952`, mtime `1786783659.967573`, SHA-256
  `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`,
  `integrity_check=ok`.

## R. Autonomous Regression

- canonical child Work focused proof: `5 passed`.
- Autonomous Phase 1/2/3A/3B, primary two-cycle, XHS cross-domain,
  Responsibility Routing, Team Operating real Employee E2E and DB Safety:
  `73 passed`.
- Python compile: PASS.
- `git diff --check`: PASS.
- Single active Cycle: preserved by existing regression.
- Successor Cycle created by this Issue: `0`.
- Learning created by this Issue: `0`.

## S. Remaining Track C Gap

The Shared prerequisite is now implemented. The original Track C must still run its
real domain proof: one Cycle, multiple canonical Work, multiple Responsibility/Employee
executions, Handoff-driven release, per-Work Result/Evidence, and one aggregate
Evaluation/Leader Review. Parallel Work remains not proved and is not part of this
foundation.

## T. Commit Recommendation

No commit is authorized in this Issue. Exact-file commit can be considered only after
CEO Acceptance and a fresh ownership/staging review. Current state: unstaged, not
committed, not pushed.

## Acceptance Answers

1. Canonical Work真实存在：是。
2. Work有独立work_id：是。
3. Cycle能拥有多个Work：是。
4. work_id不等于cycle_id：是。
5. Work绑定真实Responsibility：是。
6. Work绑定Workspace-scoped Assignment：是。
7. Employee identity保持canonical：是。
8. Work拥有独立Result refs：是。
9. Work拥有独立Evidence refs：是。
10. Work拥有独立Acceptance refs：是。
11. Result A合法释放Work B：是，需完成态、Accepted Result和有效Assignment。
12. Work B exactly-once：是。
13. restart不重复Work B：是。
14. concurrent release安全：是。
15. predecessor/successor Work成立：是。
16. Work A保持immutable：是，完成数据未被释放动作改写。
17. Evaluation按Work聚合：是。
18. missing Work Evidence fail-closed：是。
19. legacy one-Work路径兼容：是，73项回归通过。
20. single-active Cycle仍成立：是。
21. 新增Surface Runtime：否。
22. 新增Workflow/DAG：否。
23. 依赖Package v2：否。
24. active DB完全不变：是，两个库size/mtime/SHA一致且integrity ok。
25. 原Track C剩余：真实跨专业多Work Domain E2E；parallel仍未证明。

## Verdict

`CURIS SHARED RUNTIME — CANONICAL CHILD WORK FOUNDATION IMPLEMENTED`

The implementation is ready to reopen the Cross-Surface Multi-Work Runtime Proof after
CEO Acceptance. This Review does not claim that Track C itself has passed.
