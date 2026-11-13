# CURIS V1 — GENERAL WORKSPACE P1 OPERATING CLOSURE REVIEW

Authority Class: REVIEW / EVIDENCE  
Status: Review  
Date: 2026-08-29  
Owner: Main Development Session  
Disposition: IMPLEMENTED / PARTIAL

## Verdict

The bounded product and Runtime integration is implemented. The canonical General Workspace now has a real operating surface over existing Company OS truth. It does not invent a Team, Employee, Work, execution, Result or capability.

Full P1 Epic acceptance remains open because automatic Team materialization, General Handoff/P7 controls, richer Result Utility and a native packaged launch of this exact change were not accepted in this closure.

## 1. Canonical Assistant Unification

- The floating Company Assistant reads the canonical Runtime `snapshot.assistant` reference.
- Product fallback identity is `CEO 助理 / 公司级协调与经营跟进`; no second editable identity is created.
- The legacy `getAssistantIdentity` / `updateAssistantIdentity` path is no longer consumed by the primary floating Assistant.
- CEO Desk no longer auto-opens the Assistant. Browser evidence showed dialog count `0` before the user opened it and `1` after the explicit action.
- The old local Runtime-count reply and command composer were removed. The floating surface is now a factual attention summary; work input uses the existing `SharedConversation`.

Boundary: the current Runtime company projection exposes the canonical Assistant reference but not configured display metadata. This closure does not expand the Runtime Foundation response or create another identity store.

## 2. General Workspace Read Model

`SharedWorkspaceProjection.general_workspace()` now projects persisted canonical `WORK` routing facts:

- Business / Workspace / goal;
- real Team and Employees;
- responsibility key and Holder;
- Current Executor separately;
- Work and execution status;
- Result, Artifact and Evidence references;
- precise recovery action.

The projection is read-only and stores no second operating model.

## 3. Responsibility / Work / Execution Truth

Existing primitives were reused without schema change:

`GeneralWorkspaceDelivery.create_work()`  
→ canonical Cycle / Work  
→ persisted `responsibilityRouting`  
→ Team Operating `/works/{work_ref}/execute`  
→ Result / Artifact / Evidence references.

Focused evidence proved:

- no Team: `NEEDS_DECISION`, Owner `CEO`, next action `确认团队责任与员工`;
- attempted work creation without a Team: HTTP `409 RESPONSIBILITY_UNRESOLVED`, zero Cycle/Work side effects;
- legal Employee + accepted local capability: one canonical Work, real Holder, executor cleared after completion, Result/Evidence references retained;
- database reopen returned the same Work and completed routing truth.

The UI never equates Holder with Current Executor.

## 4. Product Surface

Generic Workspace routing now opens `GeneralWorkspaceOperating` rather than the professional-entry placeholder. The surface answers:

- what the business goal is;
- what work exists;
- who owns it;
- whether anyone is executing now;
- what result/evidence exists;
- what is missing and who acts next.

RD/XHS/TTK dedicated routes are unchanged.

## 5. Browser Evidence

Environment:

- frontend: fresh dev process on `127.0.0.1:3410`;
- backend: fresh process on `127.0.0.1:8410`;
- isolated SQLite: repository-external temporary database;
- identity mode: bounded test identity;
- canonical parent: `通用业务公司 / 业务部 / 客户反馈业务`.

Observed in the real Browser DOM:

- `客户反馈办公室` opened through its canonical parent path;
- goal `形成一个可验证改进` rendered;
- Team/Work/Result counts were all truthful zero;
- responsibility card showed `尚未形成唯一的团队责任安排`, Owner `CEO`, next action `确认团队责任与员工`;
- user-entered problem/expected result remained a draft and produced the same precise gap instead of a fake Work;
- Runtime DB still contained only one canonical Assistant and one FoundingRun; no Cycle/Work was created;
- floating Assistant did not auto-open and showed no editable identity or command composer after explicit open;
- browser console warning/error list was empty.

## 6. Restart / Persistence

The isolated backend was stopped and restarted against the same SQLite. The same Company, Business, Workspace, goal and `NEEDS_DECISION` projection were returned; Work count remained zero. Focused accepted-path evidence separately reopened a completed Work and recovered Holder, Result and Evidence references with Current Executor `none`.

Persistence was not treated as proof that an external provider remained live.

## 7. CEO Attention / Decision Boundary

No General-specific notification, Matter, Handoff, Approval or Decision system was added. Existing Company Attention remains the only return path for persisted Decision/Handoff/Result truth. This closure did not fabricate a Decision merely to demonstrate CEO attention.

## 8. Tests

- focused General Workspace + prior contracts: `6 passed`;
- backend bounded no-regression: `29 passed`;
- frontend focused source/contract tests: `6 passed`;
- scoped ESLint: PASS;
- Python compile: PASS;
- `git diff --check`: PASS;
- Next production build: PASS, 46 routes.

The backend set covered Batch 1 attention, M2/M2.5A General operating/context, canonical usage attribution, M4/M5, RD real execution, XHS Calendar/Note and DB Safety.

## 9. Desktop Evidence

Fresh packaging from current source completed:

- standalone frontend: PASS;
- Workspace/Gateway/Guardian sidecars: PASS;
- Cargo/Tauri release bundle: PASS;
- output: `desktop/target/release/bundle/macos/Curis.app`;
- size: `528M`;
- main binary SHA-256: `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf`.

Native packaged launch was not accepted. A pre-existing unrelated Python process owned fixed Gateway port `127.0.0.1:8080`. It was not terminated or modified. Therefore this Review does not claim packaged Browser/Desktop behavior for the new General operating page.

## 10. Active Database Safety

Both repository active databases were byte-identical before and after implementation, tests, Browser validation and packaging:

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1,232,896 | 1,786,873,339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1,277,952 | 1,786,783,659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

## 11. Changed Files

Backend:

- `backend/app/shared_workspace_projection.py`
- `backend/tests/test_v1_general_workspace_p1_operating_closure.py`

Frontend:

- `frontend/components/assistant/GlobalAssistant.js`
- `frontend/components/v1/GeneralWorkspaceOperating.js`
- `frontend/app/ceo-office/workspace/page.js`
- `frontend/lib/runtimeApi.js`
- `frontend/tests/v1GeneralWorkspaceOperating.test.mjs`

Delivery:

- `issues/CURIS-V1-GENERAL-WORKSPACE-P1-OPERATING-CLOSURE.md`
- `docs/reviews/CURIS_V1_GENERAL_WORKSPACE_P1_OPERATING_CLOSURE_REVIEW.md`
- `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md`
- `docs/00_Context/CURRENT_STATE.md`

No Product Authority, schema, active database, RD/XHS/TTK domain implementation, commit or push was changed.

## 12. Remaining P1 / Separate Blockers

1. Automatic goal-to-Team/Responsibility materialization is not implemented. Fresh General Workspace truthfully stops before Work creation.
2. General product integration for Handoff and P7 remains open; existing shared Runtime is preserved.
3. Rich Result Utility is not complete; canonical references are available now.
4. Durable conversation model selection and M3 native Keychain remain separate.
5. Packaged native acceptance must be rerun when fixed port `8080` is available; build itself is green.
6. Real external provider quality/cost was not verified. Accepted local deterministic capability evidence is not represented as a live external model.

## Final Status

**GENERAL WORKSPACE P1 — IMPLEMENTED / PARTIAL**

The bounded operating surface and truth bridge are real. The broader P1 Epic and fresh packaged native acceptance are not complete.

STOP FOR CEO / CHATGPT GENERAL WORKSPACE P1 REVIEW.
