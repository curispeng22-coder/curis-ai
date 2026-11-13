# CURIS V1 Frontend Batch 1 — App Entry + CEO Desk

Authority Class: CURRENT IMPLEMENTATION ISSUE  
Status: Implemented / Review Required  
Date: 2026-08-29

## Goal

Implement the accepted App Entry and attention-first CEO Desk against existing Curis Runtime truth: optional Welcome, minimal CEO display identity, real Company + CEO Assistant creation, truthful model management, conversational Business creation, canonical first Workspace landing, and CEO operating attention projection.

## Authority

- `docs/reviews/CURIS_V1_APP_ENTRY_UI_ACCEPTANCE.md`
- `docs/reviews/CURIS_V1_CEO_DESK_OPERATING_UI_ACCEPTANCE.md`
- `docs/reviews/CURIS_V1_FRONTEND_IMPLEMENTATION_READINESS_REVIEW.md`
- `docs/reviews/CURIS_APP_ENTRY_LIFECYCLE_CONTRACT.md`
- `docs/reviews/CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md`
- `docs/reviews/CURIS_EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT.md`
- Figma `2Fh7DgPPfLgdbvNtnzPnk9`: App Entry nodes `1:2`–`1:2428`; CEO Desk node `69:3`

## Pre-change truth

- HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- Worktree is preserved and mixed. Only exact paths below are owned by this Issue; unrelated staged, unstaged, and untracked content is excluded.
- Active SQLite fingerprints are recorded in the implementation Review and must remain unchanged.
- Existing Runtime remains authoritative for Company, Assistant, FoundingRun, Capability/Health, Model Preference, Business, Workspace, Decision, Handoff, Result, Evidence and Responsibility.

## Allowed Files

### Backend seams

- `backend/app/api/frontend_v1_router.py` — minimal presentation preference and read-only CEO attention projection
- `backend/app/runtime/first_run_delivery.py` — bounded existing-Company FoundingRun adapter over canonical Business + first Workspace transaction
- `backend/app/main.py` — one owned router-registration hunk only
- `backend/tests/test_v1_frontend_batch1.py`

### Frontend

- `frontend/app/page.js`
- `frontend/next.config.js` — align the existing root redirect with the accepted Welcome entry
- `frontend/app/welcome/page.js`
- `frontend/app/onboarding/page.js` — compatibility redirect only if required
- `frontend/app/ceo-office/page.js`
- `frontend/app/ceo-office/capabilities/page.js`
- `frontend/components/v1/AppEntry.js`
- `frontend/components/v1/V1Sidebar.js`
- `frontend/components/v1/SharedConversation.js`
- `frontend/components/v1/ModelManagement.js`
- `frontend/components/v1/CeoDeskOperating.js`
- `frontend/components/terra/TerraShell.js`
- `frontend/components/terra/TerraSidebar.js`
- `frontend/components/terra/TerraNavData.js`
- `frontend/lib/api.js`
- `frontend/components/runtime/RuntimeProvider.js` — include the accepted Welcome route in existing bootstrap truth
- `frontend/lib/v1FrontendApi.js`
- `frontend/lib/runtimeApi.js`
- `frontend/tests/v1FrontendBatch1.test.mjs`
- `frontend/tests/runtimeWorkspaceUI.test.mjs` — migrate the obsolete inline CEO Desk source assertion to the accepted composed entry
- `frontend/public/avatars/curis-ceo-*.png` — accepted preset assets only, if needed

### Records

- `issues/CURIS-V1-FRONTEND-BATCH-1.md`
- `docs/reviews/CURIS_V1_FRONTEND_BATCH_1_IMPLEMENTATION_REVIEW.md`
- `docs/reviews/CURIS_V1_EXECUTION_BACKLOG.md` — status only
- `docs/00_Context/CURRENT_STATE.md` — implementation truth only

Expanding this list requires an Issue amendment before editing.

## Runtime / API seams

- Reuse Runtime Foundation for Company, FoundingRun, Business and first Workspace materialization.
- Reuse `/api/workspace/ai-capabilities` and `/api/workspace/model-preference`; provider fixtures never become Runtime truth.
- Persist only Welcome dismissal and CEO display presentation through existing `system_settings`; no schema or second identity model.
- Add one read-only attention projection over existing Runtime entities. It creates no Matter, Decision, Handoff, Result or ranking truth.
- Conversation model selection resolves explicit enabled selection, then existing default, then no model. It does not create a second router.

## Explicit exclusions

- No Product/Frozen Authority/Figma changes.
- No M3 native Keychain implementation and no claim of durable cloud credential readiness.
- No new identity, model, Decision, Matter, Conversation, Agent, Task, Workflow or ranking system.
- No keyword-based professional Workspace materialization.
- No schema migration, active database write, route deletion, broad legacy cleanup, commit, or push.
- No fake Assistant response, model health, Result, Evidence, Decision, Handoff, Current Executor, publication or analytics.

## DB safety

- Every backend test/import uses one repository-external isolated SQLite via `CURIS_DB`, `CURIS_DB_PATH`, and `CURIS_WORKSPACE_DB`.
- Tests fail before initialization if those variables are absent or resolve to an active repository SQLite.
- `data/curis.sqlite` and `backend/data/curis.sqlite` are fingerprinted before and after by size, mtime, SHA-256 and `integrity_check`.

## Test matrix

1. Fresh `Company=0 + welcome not dismissed` opens Welcome.
2. Skip persists without creating Company; restart opens Empty Curis.
3. CEO display name/avatar preset/upload/fallback persists independently of Company lifecycle.
4. Company setup creates one real Company and one real Assistant, never a Business.
5. Assistant identity without enabled verified model remains AI-not-ready; no fake response.
6. Provider directory, connect/health result and model preference come from current APIs; no secret is persisted by frontend or SQLite.
7. First and additional Business use the same FoundingRun flow; general path atomically creates canonical Business + first Workspace and is idempotent/fail-closed/restart-safe.
8. Empty Curis, Empty Company, Quiet, Partial, Waiting, Unknown and Unavailable remain truthful.
9. CEO Desk attention cards reference existing Decision/Handoff/Result/Evidence/Responsibility/Work truth and deterministic ordering.
10. Seven-area navigation, 1440 Light, 1024 adaptive layout and Dark render without console errors.
11. Existing XHS, RD, Business and Workspace entry tests remain green.
12. Browser vertical flow and, where the accepted source baseline allows, fresh packaged Desktop flow are recorded separately.

## Stop gates

Stop only the affected sub-item on a required schema migration, M3 durable secret dependency, ambiguous mixed-source ownership, Frozen conflict, active-DB risk, or professional Workspace auto-materialization decision. Continue independent accepted work and record the exact blocker.

## Result

Implemented within the bounded files above.

- Fresh App Entry supports Welcome, persistent Skip without Company creation, truthful Empty Curis, and minimal CEO display identity.
- Company setup materializes one real Company and one real Runtime CEO Assistant without creating a Business.
- Model Management consumes the existing provider registry/model preference and keeps every unverified provider `未连接`; M3 durable native Keychain remains blocked.
- CEO Desk consumes canonical Company/Business/Workspace and attention truth. The first-business conversation persists a `FoundingRun`, then atomically creates a canonical Business and first General Workspace.
- Browser and newly built Packaged Desktop both completed the fresh path and restart reread against repository-external isolated SQLite.

Formal evidence: `docs/reviews/CURIS_V1_FRONTEND_BATCH_1_IMPLEMENTATION_REVIEW.md`.
