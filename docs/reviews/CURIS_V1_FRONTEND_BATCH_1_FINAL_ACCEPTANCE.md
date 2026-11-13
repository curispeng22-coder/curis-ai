# CURIS V1 — FRONTEND BATCH 1 FINAL IMPLEMENTATION ACCEPTANCE

Authority Class: REVIEW  
Status: Review  
Date: 2026-08-29  
Disposition: ACCEPTED WITH RECORDED BOUNDARIES  
Owner: Main Development Session  
Scope: Read-only final implementation validation

## Final Verdict

**V1 FRONTEND BATCH 1 — IMPLEMENTED / ACCEPTED WITH RECORDED BOUNDARIES**

The accepted mainline is real and restart-safe:

`Welcome → Skip / Empty Curis` and `Welcome → Company + CEO Assistant → CEO Desk → Business Proposal → canonical Business + first General Workspace`.

No P0 acceptance blocker was found. The remaining gaps are bounded P1 or separate external/security blockers; they do not invalidate Batch 1 materialization.

## Validation Baseline

- Repository HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- Packaged app: `desktop/target/release/bundle/macos/Curis.app`
- Packaged main binary SHA-256: `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf`
- Path A isolated HOME: `/tmp/curis-v1-final-path-a.7TJHwf`
- Path B isolated HOME: `/tmp/curis-v1-final-path-b.msE3t3`
- Browser evidence used the frontend and Runtime sidecars owned by that packaged app on `127.0.0.1:3010/8002`.
- Desktop evidence used the exact packaged app path above, not a dev server window or another Curis bundle.

## Fresh Path Results

### Path A — Skip / Empty Curis

PASS.

- Fresh launch displayed Welcome.
- `先看看 Curis` entered an honest Empty Curis state.
- After packaged app stop/restart with the same isolated HOME, Empty Curis remained.
- Isolated SQLite after restart contained:
  - Company: `0`
  - canonical Business: `0`
  - Workspace: `0`
  - Employee instance: `0`
  - Runtime entity: `0`
- No Company, Business, Employee or fake CEO Assistant was materialized.

Evidence: `/tmp/curis-v1-batch1-final-acceptance/path-a-empty-first.png`.

### Path B — Company / Business / Workspace

PASS.

- Display identity `验收 CEO`, preset avatar `preset:violet`, and Company `Batch 1 验收公司` were submitted through the real UI.
- Runtime materialized one Company and one canonical `CEO_ASSISTANT` entity. AI readiness remained unavailable because no verified model existed.
- CEO Desk correctly showed zero business/workspace facts before business creation.
- A user intent produced an editable structured proposal; the proposal could be returned to and edited before confirmation.
- Confirmation atomically produced one canonical Business and one first General Workspace with `DRAFT` state and `RESOLVED` canonical Business relation.
- No keyword-based XHS/RD materialization occurred; the fallback was an honest generic Workspace.
- Packaged app stop/restart recovered the same display identity, Company, Business, Workspace and canonical IDs without duplication.

Isolated SQLite after restart:

- Company: `1`
- canonical Business: `1`
- Workspace: `1`
- `CEO_ASSISTANT`: `1`
- Business goal matched the submitted intent.
- Workspace referenced the canonical Business and remained `DRAFT`.
- Presentation state remained `welcome_dismissed=true`, `display_name=验收 CEO`, `avatar_ref=preset:violet`.

Evidence:

- `/tmp/curis-v1-batch1-final-acceptance/path-b-workspace.png`
- `/tmp/curis-v1-batch1-final-acceptance/path-b-desktop-restart.png`
- `/tmp/curis-v1-batch1-final-acceptance/path-b-ceo-desk-1024-dark.png`

## Capability Acceptance Matrix

| Capability | Final status | Evidence / boundary |
|---|---|---|
| App Shell | IMPLEMENTED / ACCEPTED | Packaged Welcome, Empty Curis, CEO Desk and Workspace routes rendered. |
| Seven-area Navigation | IMPLEMENTED / ACCEPTED | CEO 工作台 / 业务空间 / 组织中心 / 人才与能力 / 经营洞察 / 资料库 / 会议; deep route and back/forward worked. |
| Welcome | IMPLEMENTED / ACCEPTED | Fresh packaged server state showed accepted Welcome hierarchy. |
| Skip | IMPLEMENTED / ACCEPTED | Persisted presentation choice only; created no business objects. |
| CEO Display Identity | IMPLEMENTED / ACCEPTED | Real presentation state restored after restart. |
| Avatar | IMPLEMENTED / PARTIAL | Preset and fallback paths exist; preset persistence was verified. Upload is implemented with bounded local data handling but was not interaction-accepted in this closure; no crop flow exists. |
| Company Creation | IMPLEMENTED / ACCEPTED | Real FoundingRun and Company materialization; restart/idempotency tests passed. |
| CEO Assistant Presence | IMPLEMENTED / ACCEPTED | One canonical Runtime assistant entity exists; presence is not represented as AI readiness. |
| Model Management | IMPLEMENTED / ACCEPTED WITH M3 BOUNDARY | Reads real provider/model registry; all unverified providers showed `未连接`; no Figma provider fixture was used. |
| Conversation | IMPLEMENTED / PARTIAL | Main V1 conversation does not fake AI output without a model. Legacy Global Assistant remains user-visible and can synthesize a local Runtime-summary answer. |
| Composer | IMPLEMENTED / PARTIAL | Attachment slot, model selector, disabled voice and send action are present; attachment/voice are not connected. |
| Model Selector | IMPLEMENTED / PARTIAL | Session-scoped conversation selection exists. Durable cross-restart selection and proven live-model execution are not implemented. |
| Empty Curis | IMPLEMENTED / ACCEPTED | Truthful, restart-safe zero-object state. |
| Empty Company | IMPLEMENTED / ACCEPTED | Company with no business/workspace shows a truthful start-business state. |
| Create Business | IMPLEMENTED / ACCEPTED WITH BOUNDED DELTA | Intent → structured understanding/proposal → edit/return → explicit confirmation is real. Clarification is minimal rather than a multi-turn one-question loop. |
| General Business | IMPLEMENTED / ACCEPTED | Canonical Business persisted with real goal/intent. |
| First General Workspace | IMPLEMENTED / ACCEPTED | Atomic generic DRAFT Workspace with canonical parent; full operating loop remains outside Batch 1. |
| CEO Desk | IMPLEMENTED / ACCEPTED WITH RECORDED UI DELTA | Attention-first real facts and honest empty states are present. Legacy Assistant auto-open conflicts with the accepted on-demand behavior. |
| Attention Projection | IMPLEMENTED / ACCEPTED | Reference-first projection over existing Runtime entities; deterministic ordering; no second Matter/Decision/Result/Evidence truth. |
| Restart Recovery | IMPLEMENTED / ACCEPTED | Both Empty Curis and materialized Company/Business/Workspace branches recovered from the same isolated state. |
| Packaged Desktop | IMPLEMENTED / ACCEPTED | Fresh isolated packaged launch, restart and canonical reread passed. |

## No-Fake-Data Audit

PASS for the accepted mainline.

- Company, Business, Workspace, Assistant presence, provider status and attention counts came from canonical Runtime/API or legal presentation state.
- Quiet/empty states explicitly said that no sample result or metric would be generated.
- Provider catalog default selection did not claim connection; every unverified provider remained `未连接`.
- General Workspace fallback did not use frontend keywords to choose XHS or RD.
- `Date.now()` is used only to form an internal founding intent reference; it is not shown as a business timestamp or evidence fact.
- No Figma fixture, random metric, fake decision, fake evidence, fake health or fake published result was found in the Batch 1 production path.

Recorded exception: legacy `GlobalAssistant` can produce a locally assembled Runtime-count answer. This is not used by the accepted Company/Business materialization chain, but its user-visible presence prevents the Conversation capability from being marked fully accepted.

## Model / Secret Boundary

- Model Management reads the current Provider Registry and truthful runtime state.
- API Key input is held in component state and sent only to the existing current-process credential endpoint.
- No key was entered during final acceptance.
- No secret was found in SQLite, URL, fixture or the tested logs.
- Conversation model choice is session storage only; it is not secret material.

**CLOUD MODEL DURABLE RESTART READY: BLOCKED BY M3.**

Native macOS Keychain durability is a separate security blocker. It does not block Batch 1 App Entry, CEO Desk, General Business or Model Management UI acceptance.

## CEO Desk / Attention Truth

PASS with one recorded P1 drift.

The current Desk derives and displays:

- Company state and workspace count
- Today / primary attention state
- Watching / business entry
- Important Result empty state
- Next Responsibility unknown state
- CEO Assistant presence

No current Matter, Result or Responsibility was invented. Missing facts remained quiet/unknown.

P1 drift: the legacy Global Assistant opens automatically on `/ceo-office`, reports a separate `未命名 Assistant / 尚未设置角色` identity, and crowds the accepted attention-first Desk. The canonical CEO Assistant exists and the main V1 assistant surface is correct; the legacy overlay must be replaced or unified in a later bounded task.

## Browser / Desktop / Responsive Result

- Browser mainline: PASS.
- Fresh packaged Desktop launch/restart: PASS.
- Deep route, refresh, back/forward and canonical Workspace parent route: PASS.
- Browser console errors: none observed.
- Packaged frontend error log: empty.
- Gateway log contained only connection resets caused by the deliberate stop/restart acceptance sequence.
- Workspace log truthfully reported the optional D1 toolchain unavailable; the service continued without claiming it was connected.

1024 Dark remained functionally usable with the seven-area navigation, Desk, composer and Assistant controls present and no console error. It underused horizontal space and the auto-open legacy Assistant compressed the attention surface. This is an **acceptable Batch 1 implementation delta with P1 adaptation debt**, not a canonical identity or mainline blocker.

## Regression Evidence

- Backend focused/no-regression: `32 passed`.
- Frontend focused: `12 passed`.
- Scoped ESLint: PASS.
- Python compile: PASS.
- Next production build: PASS, 46 static pages generated.
- Covered Batch 1, first-run delivery, canonical Business Spine, DB safety, XHS Calendar/Note, RD Phase 2B / execution / P7, canonical usage attribution and M4/M5 delivery.

## Active Database Safety

Both repository active databases were read-only and byte-identical before and after acceptance:

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | 1,232,896 | 1,786,873,339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | 1,277,952 | 1,786,783,659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

No active DB mutation occurred.

## Remaining P1

1. Replace/unify the legacy Global Assistant with the canonical CEO Assistant identity and real conversation contract; remove auto-open and local canned responses from the primary product route.
2. Complete General Workspace P1 operating closure beyond first materialization.
3. Make conversation-specific model selection durable only when the product contract requires it; do not infer readiness from stored metadata.
4. Close attachment/voice Composer capabilities when real Runtime support exists.
5. Improve 1024 Dark composition and prevent the optional Assistant from crowding the primary attention surface.
6. Validate avatar upload end-to-end and decide separately whether crop is required.

## Separate / Deferred Blockers

- M3 native macOS Keychain durable credential recovery: BLOCKED / separate security issue.
- Professional Workspace automatic matcher/materializer: DEFERRED.
- Real external AI execution and model quality: NOT VERIFIED by this acceptance.
- General Workspace full business operating loop: P1, outside Batch 1.

## Recommended Current Truth Updates

Do not apply these in this read-only review. The next authorized Current Truth synchronization should record:

- Batch 1 App Entry, Skip, Empty Curis, Company creation, canonical CEO Assistant presence, CEO Desk, Model Management UI, Business Proposal, canonical General Business, first General Workspace, attention projection, restart and packaged Desktop as implemented/accepted.
- Conversation, Model Selector, Avatar upload and 1024 Assistant composition as partial/bounded.
- M3 Keychain and professional automatic materialization as separate/deferred blockers.

## Recommended Next Implementation Target

**GENERAL WORKSPACE P1 OPERATING CLOSURE.**

Its first bounded acceptance item should unify the canonical CEO Assistant identity/conversation projection so the General Workspace operating path does not depend on the legacy auto-open Assistant. This recommendation does not authorize implementation.

---

STOP FOR CEO FINAL ACCEPTANCE.
