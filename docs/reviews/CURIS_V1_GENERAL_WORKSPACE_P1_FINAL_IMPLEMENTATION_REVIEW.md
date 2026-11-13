# CURIS V1 GENERAL WORKSPACE P1 FINAL IMPLEMENTATION REVIEW

Authority Class: REVIEW
Status: Review
Disposition: IMPLEMENTED / PARTIAL — PACKAGED NATIVE WORKSPACE INTERACTION UNVERIFIED
Date: 2026-08-29
Owner: Main Development Session
Source Issue: `issues/CURIS-V1-GENERAL-WORKSPACE-P1-OPERATING-CLOSURE.md`
Next Gate: repeat only the packaged Tauri WebView Workspace interaction when native Computer Use is available

## 1. Verdict

**GENERAL WORKSPACE P1 = IMPLEMENTED / PARTIAL.**

The Runtime, Browser, persistence, recovery and fresh package startup/restart portions are implemented. The remaining gate is narrow: the freshly built native window could be read, but every Computer Use click on its Tauri WebView failed with `Sky Computer Use native pipe closed before response`. Browser navigation and packaged Gateway reads are not treated as native interaction evidence.

## 2. Automatic Team Materialization

- Reuses the existing Role Slot, canonical Employee, Employee Capability Binding, Responsibility Assignment and Responsibility Workflow primitives.
- With one existing leader and existing executable non-leader assignments, publishes one `general-operating` Workspace workflow.
- Repeated call and Runtime restart return the same workflow; no duplicate Team, Responsibility or Employee is created.
- With incomplete truth, returns `TEAM_TRUTH_INCOMPLETE` / `NEEDS_DECISION` and creates nothing.
- It does not infer professional type, invent names, roles, skills or capabilities.

## 3. Team / Responsibility Truth

The read model keeps Object Owner, Responsibility Holder and Current Executor separate. Completed and waiting Work retain a Holder while Current Executor is `none`. Persisted execution history is not projected as a live executor after restart.

## 4. Handoff

The existing `HANDOFF` entity is used. It preserves source Work, source Result/Artifact context, from/to assignments, from/to canonical Employees, target responsibility and atomic acknowledgement. The General UI now renders readable Employee and Responsibility names. No `GeneralHandoffV2` exists.

## 5. P7 Decision Round-trip

- General Work creates one existing `DECISION_PACKET` through Responsibility Routing.
- Workspace and Company Attention reference the same packet ID.
- High-risk Layer 0 exposes only “查看方案 / 暂缓”.
- Layer 1 preserves option Impact/Risk/Cost and recommendation provenance (`EST`, `UNK`, `EVIDENCE`).
- CEO choice updates the same packet to `APPLIED`; Runtime restores the original responsibility and the UI automatically invokes continuation without a separate “下一步” button.
- Decision and Handoff remain different objects.

## 6. Result / Evidence Utility

The shared Utility opens existing `task:<id>` Result and Artifact references. It exposes status, verification state, owner, source Work, execution reference, callback provenance, changed Artifact references and timestamps without copying full evidence into the Workspace card. Failed execution remains `FAILED / UNVERIFIED`; direct Result text is not treated as proof.

## 7. Result → Next Responsibility

Focused Runtime E2E proves two distinct canonical Employees, two persisted ResultStore Tasks/Artifacts, one acknowledged Handoff and final Work closeout. The completed Work retains both Result references and one Handoff. Browser displays the persisted completed state and its Utility references.

## 8. Full General Operating Path

Verified canonical chain:

`Business → General Workspace → existing Team truth → materialized Workflow → Cycle/Work → Responsibility Holder → Employee execution → Result/Artifact/Evidence truth → Handoff → next Responsibility → P7 when required → CEO choice → automatic continuation → persisted state`.

The Browser invocation of the current local execution adapter failed truthfully when no matching executable capability was available: Work became `WAITING`, Result became `FAILED / UNVERIFIED`, Current Executor cleared and no success was fabricated. The successful multi-employee path is proven by focused deterministic local-provider E2E and persisted ResultStore objects; it is not claimed as an external live-model run.

## 9. Canonical Conversation / CEO Attention

The General surface continues to use Shared Conversation and the canonical Runtime `CEO_ASSISTANT`; no local canned answer or second Assistant identity was introduced. Company Attention reads the same P7 packet. Handoff and important Result remain existing Company OS facts rather than a General notification system.

## 10. Restart / Idempotency

One isolated Browser SQLite was stopped and reopened. Team workflow, two Work IDs, one Handoff ID, one Decision Packet ID and all Result/Artifact IDs remained stable. Materialize and create/retry tests prove duplicate-safe behavior. Persisted `RUNNING` is not assumed live after restart.

## 11. Browser Acceptance

Status: **PASS**.

- URL: `/ceo-office/workspace?workspace_id=workspace-v1-general`
- Canonical parent path, Goal, three Employees, Responsibility Holder/Executor, waiting failure, completed Work, readable Handoff and Result Utility rendered.
- High-risk P7 Layer 0/Layer 1 and automatic continuation were exercised against the same isolated database.
- Backend stop/restart preserved the page truth.
- Evidence screenshot: `/tmp/curis-general-workspace-p1-browser.png`.

## 12. Packaged Desktop Acceptance

Status: **PARTIAL — NATIVE INTERACTION GATE**.

Passed:

- Fresh `pnpm build` rebuilt frontend standalone output, Workspace/Gateway/Guardian sidecars, Cargo release and `desktop/target/release/bundle/macos/Curis.app`.
- Two unrelated stateless `python -m http.server` processes on fixed port `8080` were identified by command/cwd and stopped with `TERM`; no unknown process was killed.
- A stale Curis process from worktree `d126` had no child/listener and was stopped with `TERM` to remove duplicate bundle identity.
- Fresh native window, frontend `3010`, Workspace `8002`, Gateway `8080`, isolated app-data and CEO Desk Company recovery passed.
- Packaged Gateway read `READY_FOR_WORK`, three Employees, the same two Work IDs, one Handoff ID, one Decision Packet ID and six Result/Artifact references.
- Closing and reopening the app preserved the same IDs and SQLite integrity.
- Error logs were empty except the pre-existing truthful warning `D1 toolchain unavailable; service continues without it`.
- Evidence screenshots: `/tmp/curis-general-p1-desktop-loaded.png`, `/tmp/curis-general-p1-desktop-restart.png`.

Not passed:

- Native Workspace link interaction. Computer Use repeatedly closed its native pipe on the Tauri WebView click, including after the duplicate old app was removed.
- The packaged database was an isolated copy of the Browser acceptance state with tenant/CEO identifiers adapted to packaged self-use identity. This proves packaged recovery, not packaged UI creation of the business chain.

## 13. Tests / Build

- Backend focused + regression: **42 passed**.
- Frontend source tests: **6 passed**.
- Focused ESLint: **PASS**.
- Python compile: **PASS**.
- `git diff --check`: **PASS**.
- Frontend production build: **PASS**, 46 routes.
- Fresh packaged build: **PASS**.

Covered regressions include Frontend Batch 1, App Entry/CEO Desk/Attention, General M2/M2.5A, canonical usage attribution, Responsibility Routing, Team Operating real Employee E2E, Shared Workspace projection, RD P7, XHS Calendar/Note and Backend DB Safety.

## 14. Active DB Safety

Both repository active databases are byte-identical to the preflight fingerprints and pass `integrity_check`:

| Path | Size | mtime | SHA-256 |
| --- | ---: | ---: | --- |
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` |

All Runtime tests used repository-external SQLite. Packaged testing used isolated app-data under `/tmp`.

## 15. Remaining Classification

- **P0:** none introduced by this implementation.
- **P1:** packaged native Workspace click/reopen observation only.
- **P2:** broader General cancel/history polish, if later required by Product Authority.
- **SEPARATE BLOCKER:** M3 durable native Keychain; external live-provider quality/cost.
- **DEFERRED:** professional auto matcher/materializer; it is not General Team materialization.

## 16. Changed Scope

Runtime/API/read projection, focused tests, General Workspace component/API wrappers, current Issue, this Review, Execution Backlog status and CURRENT_STATE implementation truth. No Product Authority, schema, active database, RD/XHS domain implementation, new primitive, commit or push.

## 17. Final Recommendation

Keep the Issue at **IMPLEMENTED / PARTIAL**. All four functional completion items are implemented over existing truth, but `V1-P1-010` cannot be accepted until a real native Tauri Workspace interaction is observed. Do not reopen Runtime architecture or repeat Browser work; retry only that exact native gate.
