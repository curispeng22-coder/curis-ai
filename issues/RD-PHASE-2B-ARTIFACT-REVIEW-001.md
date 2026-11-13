# RD-PHASE-2B-ARTIFACT-REVIEW-001

**Status:** IMPLEMENTED / ACCEPTED WITH RECORDED ACTIVE-DB INCIDENT
**Date:** 2026-08-16
**Owner:** Curis main development / RD Workspace

## Goal

Implement one truthful two-Employee Artifact Review chain on the accepted RD Workspace:

```text
Developer remains Responsibility Holder
→ select one real Reviewer Employee
→ persist one Cycle-scoped Artifact Review Request
→ run one real reviewer Task through the existing Agent binding
→ persist Result / Evidence
→ return the review result to the Developer Workstation
→ restart and recover the same facts
```

Artifact Review is not a Responsibility Handoff and is not a CEO Decision.

## Authority

1. `docs/00_Context/CURRENT_STATE.md`
2. `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md` P1–P7
3. `docs/03_Design/Curis_RD_Workspace_Instance_Spec_v1.md`
4. `docs/04_Development/RD_PHASE_2B_PRE_IMPLEMENTATION_AUDIT.md` §9
5. `issues/RD-WORKSPACE-INSTANCE-001.md`
6. `reviews/RD-WORKSPACE-INSTANCE-001_review.md`
7. `docs/07_Decisions/ADR-0046-local-agent-computer-access-authority.md`

## Preserved Development Baseline

Audited Git HEAD: `6f03b5772e3f457e3b423b8b2445138e6715ce3b`.

### Pre-change source hashes

| Path | SHA-256 |
| --- | --- |
| `backend/app/runtime/workspace.py` | `3a101ad0ed174ee9a2339fe045c58fad1362606cddfe136ad52ae73e5d8edc54` |
| `backend/app/api/runtime_foundation_router.py` | `8454aab234618055d0c4cc5eb583e0bbabc0df6671658745f38074d3a6aabf34` |
| `backend/app/main.py` | `58c4c1a459286d47f348bb77a8068738fee327006289de4cae2b3e49cf2e3cec` |
| `backend/tests/test_rd_workspace_real_execution.py` | `b56f32a617faa04493064f4e201d73055cd10d233074504336f5e35900fa3b1f` |
| `frontend/components/rd/RdWorkspacePhaseTwo.js` | `706ed5ea0df808f153ac970e3cf5124503a895e58a61a8bc92aa859fb1fe3f4c` |
| `frontend/lib/runtimeApi.js` | `2a6bfd75d45d39fc7527d47f95de111428115b1945e79e1090fa488b2c4d7a11` |
| `frontend/tests/rdWorkspaceExecution.test.mjs` | `e22327ef5d85b5fe6c380cadfdf17f693c79068882f04d94ee99fd7a3fd70c9e` |
| `backend/tests/conftest.py` | `1bd3383b3287a173059c67da299be459cf4f1cca40e8ed78abd8730c3d511d1d` |

Active database incident baseline recorded before implementation edits:

```text
data/curis.sqlite | size=1232896 | mtime=1786871647
```

The original pre-incident byte SHA was not captured. The later provenance audit therefore
must not claim byte-for-byte unchanged. All subsequent tests must reject this path before
application import and use one fresh temporary SQLite path through `CURIS_DB`,
`CURIS_DB_PATH` and `CURIS_WORKSPACE_DB`.

## Owned functions and hunks

Only the following source areas are owned by this Issue:

- `backend/app/runtime/workspace.py`
  - new Cycle-scoped review request commands adjacent to accepted RD execution methods;
  - review request reconciliation only;
  - no edits to XHS content methods or shared state registries.
- `backend/app/api/runtime_foundation_router.py`
  - request DTO and RD Cycle artifact-review endpoints;
  - background completion for reviewer execution;
  - no changes to XHS, Simulation or Company materialization routes.
- `backend/app/main.py`
  - one bounded reviewer branch inside existing `execute_runtime_business()` only if
    required to create/run the real reviewer Task;
  - no app-factory, Provider, Agent Adapter or general Task refactor.
- `frontend/components/rd/RdWorkspacePhaseTwo.js`
  - reviewer selection, review status and Result Reference inside existing RD Workstation;
  - no shared Shell or XHS edits.
- `frontend/lib/runtimeApi.js`
  - artifact-review endpoint wrappers only.
- focused new/owned tests and this Issue/Review.
- `backend/tests/conftest.py`
  - one import-time call to the accepted Workspace P0 three-variable DB guard only;
  - no fixture, collection, Runtime or application changes.

Before editing a mixed file, its current hash must still equal the recorded pre-change
hash or the last hash produced by this Issue. Any unexplained mismatch is a conflict and
stops edits to that file.

## Allowed Files

```text
backend/app/runtime/workspace.py
backend/app/api/runtime_foundation_router.py
backend/app/main.py
backend/tests/test_rd_artifact_review.py
backend/tests/conftest.py
frontend/components/rd/RdWorkspacePhaseTwo.js
frontend/components/rd/RdArtifactReview.js
frontend/lib/runtimeApi.js
frontend/tests/rdArtifactReview.test.mjs
issues/RD-PHASE-2B-ARTIFACT-REVIEW-001.md
reviews/RD-PHASE-2B-ARTIFACT-REVIEW-001_review.md
```

`RdArtifactReview.js` is optional and should exist only if it reduces edits in the mixed
RD page.

## Runtime truth model

```text
Cycle Responsibility Holder = Developer, unchanged
Cycle Current Executor = none after implementation execution
Review Request reviewer = real Reviewer Employee
Review Request Current Executor = Reviewer only while reviewer Task is active
Review Request Result = real Task output + Artifact/Evidence refs
HANDOFF count = 0
DECISION_PACKET count = 0
```

The request is stored inside the existing Cycle Runtime data with a stable request ref.
No new shared Runtime entity, table, state machine or registry entry is allowed.

## Implementation scope

1. Validate one completed RD Cycle with real Artifact/Evidence.
2. Validate a distinct real Reviewer Employee in the same Workspace and a real Agent
   capability binding.
3. Persist one Cycle-scoped request before execution.
4. Submit/observe one real reviewer Task asynchronously through the existing execution
   callback and Agent/ResultStore path.
5. Supply only selected Artifact/Evidence, acceptance expectation and relevant file refs.
6. Persist requested/reviewing/approved/changes-requested/failed truth and review Result
   refs on the Cycle record.
7. Keep developer responsibility unchanged and return the result to the same Workstation.
8. Guard duplicate active submission for the same Cycle and Artifact set.
9. On restart, retain request history but fail-close unverified active reviewer execution;
   persistence must not claim an external Agent is still running.

## Explicit exclusions

- true Responsibility Handoff;
- CEO Decision P7 or any Approval system;
- `HANDOFF`, `DECISION_PACKET`, `ACCEPTANCE` creation;
- Queue/Bottleneck, Organization Router, Workflow Engine or DAG;
- multiple concurrent reviewers or repeated review rounds;
- reviewer auto-fix/file modification;
- shared `states.py`, `registry.py`, `foundation.py` changes;
- Computer Access P1/P2 or Full Access;
- XHS, TTK, Product Blueprint, Frozen contracts, shared Shell refactor;
- activity database, credentials, staging, push or unrelated cleanup.

If implementation proves that a Cycle-scoped record is insufficient and needs a shared
Runtime primitive, this Issue becomes BLOCKED_ARCHITECTURE_REVIEW_REQUIRED immediately.

## Acceptance

1. Two distinct real Employees are visible in the same RD Workspace and have valid
   existing capability bindings.
2. Developer remains the original Cycle Responsibility Holder throughout review.
3. One request creates one reviewer Task; duplicate active submission creates no second
   Task or Agent session.
4. Reviewer Current Executor exists only while the reviewer Task is active.
5. Review result is backed by real Task output/Evidence and exposed by Result Reference.
6. approved, changes-requested and failed outcomes are distinct and durable.
7. Handoff count and Decision Packet count remain zero.
8. Same isolated SQLite stop/restart restores request, employees, Task, result and an
   inactive truthful executor.
9. Accepted primary RD execution, long-running reliability, Computer Access truth and XHS
   focused behavior do not regress.

## Verification boundary

- Fresh temporary SQLite with `CURIS_DB`, `CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` all
  pointing to that same path.
- Test bootstrap must fail fast if any resolved DB path equals `data/curis.sqlite`.
- Focused backend/frontend tests, failure/idempotency/restart, RD/XHS no-regression and
  bounded diff check.
- A real reviewer Task/Agent execution is required for final acceptance; deterministic
  injected executors may support focused state tests but cannot be the only evidence.

## Implementation outcome

The bounded implementation is complete without changes to `states.py`, `registry.py` or
`foundation.py`. One Cycle-scoped record now carries the request, reviewer execution,
Result/Evidence references and restart truth. No shared Review primitive was added.

The Runtime and UI acceptance chain passed on a fresh isolated database, including one
real primary Codex Task and one distinct real reviewer Codex Task. The Developer remained
the Cycle Responsibility Holder, reviewer Current Executor returned to `none`, and both
Handoff and Decision Packet counts remained zero.

The active-database provenance audit proved an empty schema/seed-metadata initialization
incident with no Company, Workspace, Employee, Responsibility, Task, Execution, Artifact,
Evidence, Result, RD, XHS or Package-instance business data. The existing backup was not
restored because the current schema and business-data truth are internally consistent.

Formal incident classification:

`ACTIVE DB EMPTY-INITIALIZATION INCIDENT — OWNER ACCEPTED`

The Review records the accepted post-incident SHA and explicitly does not claim
byte-for-byte unchanged. The shared pytest bootstrap now applies the existing Workspace P0
three-variable guard before test-module import. This Issue is therefore implemented and
accepted with the recorded incident; no Handoff, P7 or shared Runtime work is included.
