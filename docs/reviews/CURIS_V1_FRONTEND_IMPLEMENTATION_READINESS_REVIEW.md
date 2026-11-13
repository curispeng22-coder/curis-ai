# CURIS V1 — FRONTEND IMPLEMENTATION READINESS REVIEW

**Status:** Review  
**Authority Class:** REVIEW / ENGINEERING RECONCILIATION  
**Date:** 2026-08-28  
**Owner:** Main Development Session  
**Scope:** App Entry + CEO Desk；只读对账，不产生实现授权  
**Verdict:** READY WITH BOUNDED BLOCKERS

## 0. Executive decision

Accepted App Entry 与 CEO Desk 已足够开始真实 Frontend 实现，不需要先回 Figma 重新设计。当前阻塞不是页面结构，而是少数可命名的 Runtime / Security seam：

1. CEO Display Identity（名称 + 可选 Avatar）尚无可确认的 canonical persistence / API；Company 与 CEO Assistant materialization 已存在。
2. Optional Onboarding Skip 尚无独立于 Company lifecycle 的本机持久化。
3. Model Management 的真实 Provider registry、Health、Model discovery 与 default preference 已有后端基础，但 Accepted UI 尚未接线；当前页面仍是内部 Capability 管理界面。
4. M3 macOS Keychain 仍是安全阻塞：不阻塞 Model Settings UI 开发，但阻塞真实云端 Credential durable enable 与 packaged restart 后的 AI Ready 验收。
5. Conversation shared shell 存在，但当前 `GlobalAssistant` 仍包含本地合成/canned command 行为；Model Selector、Voice、Attachment/Context 的 accepted interaction 尚未实现。
6. M2.5B 的原 UI-HOLD 已被 Accepted App Entry / Create Business interaction contract 解除；现在是 **READY TO IMPLEMENT，但尚未接线**。
7. General Business + First Workspace 的 headless materialization 已存在；Professional Workspace 的自动匹配与 materialization 尚无统一、已验收的入口合同/API，不能宣称完成。
8. CEO Desk 的 Domain facts 分散存在，但缺少 Company-wide canonical attention read model；69:3 可以先做 deterministic projection，不需要复杂 ranking engine。

因此，Batch 1 可以立即实现 App Shell/App Entry/真实空态/Company 创建/Assistant presence/Model Settings 外壳与 CEO Desk composition；对 Keychain、CEO identity persistence、Conversation Model Selector、Professional materialization 和 CEO-wide attention projection 使用精确 blocker 或 bounded backend seam，不能用 fixture 补齐。

## 1. Evidence and truth boundary

### Current authority consumed

- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/reviews/CURIS_V1_APP_ENTRY_UI_ACCEPTANCE.md` — Frozen，13 个 App Entry frames
- `docs/reviews/CURIS_V1_CEO_DESK_OPERATING_UI_ACCEPTANCE.md` — Frozen，node `69:3`
- `docs/reviews/CURIS_APP_ENTRY_LIFECYCLE_CONTRACT.md`
- `docs/reviews/CURIS_CREATE_BUSINESS_FLOW_CONTRACT.md`
- `docs/reviews/CURIS_EMPLOYEE_CONVERSATION_MODEL_EXPERIENCE_CONTRACT.md`
- `docs/reviews/CURIS_FRONTEND_BASELINE_CLOSURE_REVIEW.md`
- `docs/reviews/CURIS_V1_M4_M5_CONTINUOUS_DELIVERY_REVIEW.md`
- `issues/V1-P0-003-MACOS-KEYCHAIN-CREDENTIAL-PERSISTENCE.md`

### Current implementation inspected

- Shell / navigation: `frontend/app/layout.js`, `frontend/components/terra/TerraShell.js`, `TerraSidebar.js`, `TerraNavData.js`
- Runtime bootstrap/state: `frontend/components/runtime/RuntimeProvider.js`, `RuntimeStates.js`
- App Entry: `frontend/app/onboarding/page.js`
- CEO Desk: `frontend/app/ceo-office/page.js`
- Assistant: `frontend/components/assistant/GlobalAssistant.js`, `frontend/lib/assistantState.mjs`
- Model UI/API: `frontend/app/ceo-office/capabilities/**`, `frontend/lib/api.js`, `backend/app/ai_capability_registry.py`, `backend/app/credential_vault.py`
- Company / first business: `backend/app/runtime/foundation.py`, `backend/app/runtime/first_run_delivery.py`, `backend/app/api/runtime_foundation_router.py`
- CEO operating projection: `backend/app/business_metrics.py`, `/api/workspace/ceo/operating-day`
- RD/XHS accepted domain surfaces and shared Workspace projection

### Repository and database safety

- HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`
- Worktree is highly mixed; this review does not classify or absorb unrelated changes.
- `data/curis.sqlite`: size `1232896`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, `integrity_check=ok`
- `backend/data/curis.sqlite`: size `1277952`, SHA-256 `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`, `integrity_check=ok`
- Both databases were opened read-only. No Runtime, schema, data, frontend, Figma or Product Authority was changed.

## 2. Current frontend inventory

| Area | Current truth | Classification | Implementation direction |
| --- | --- | --- | --- |
| Root layout | `RuntimeProvider → GlobalAssistantProvider` is already established | REUSE | Keep provider order and honest Runtime states |
| `TerraShell` | Shared topbar/sidebar/theme/drawer/Assistant entry exists | REFACTOR / MIGRATE | Keep shell mechanics; replace accepted visual/nav semantics in bounded steps |
| Navigation | Current navigation includes legacy/admin groups and does not match accepted seven-area product navigation | REPLACE | Build accepted primary navigation on current route truth; do not force UI to preserve legacy grouping |
| Runtime states | Loading/empty/forbidden/error components exist and are broadly consumed | REUSE | Preserve truthful state boundary |
| Onboarding | Runtime-backed `FoundingRun` exists, but UI exposes internal stages/IDs and starts with a business-intent textarea | REPLACE surface / REUSE API seam | Rebuild as Welcome → Company Setup → Company Created; retain recovery/materialization calls |
| CEO Desk | Runtime-backed workforce/staffing/capability composition exists | REPLACE composition / REUSE facts | Implement 69:3 attention-first surface; reuse only canonical facts/actions |
| Business Space | Canonical Business/Workspace routes exist; current surface is implementation-oriented | REFACTOR / MIGRATE | Keep canonical route/parent identity; implement accepted empty/create states |
| Assistant overlay | Identity/dialog/context plumbing exists | REFACTOR | Replace canned/local command behavior with real shared Conversation semantics |
| Model settings | Internal Capability catalog/detail exists; new real AI provider registry exists only on backend | REPLACE user surface / REUSE backend | Build accepted model management against `ai-capabilities` + model preference; keep technical details secondary |
| Employee UI | Organization and shared employee work-area components exist | REUSE selectively | Do not make Employee management the CEO Desk primary surface |
| Result/Evidence | Result Reference, Artifact/Evidence and domain Utility views exist | REUSE shared semantics | Add CEO-level read projection; never copy full evidence into Conversation |
| Decision UI | Domain P7 exists; current CEO decisions page derives pseudo-decisions and uses local placeholder action | REPLACE | Consume real `DECISION_PACKET`; no second decision object |
| Company runtime page | Honest empty/compatibility surface | DELETE AFTER REPLACEMENT | Remove only after accepted CEO Desk/Business routes cover its valid recovery duties |
| Legacy project/execution/admin routes | Still support accepted RD/compatibility behavior | KEEP OUTSIDE BATCH | Do not delete until replacements and regressions are proven |

## 3. App Entry: 13-frame engineering mapping

Status vocabulary: `EXISTS`, `PARTIAL`, `MISSING`, `BLOCKED`. Action vocabulary: `REUSE`, `ADAPT`, `BUILD`, `BLOCKED`.

| Frame | Frontend current truth | Required Runtime/API truth | Support | Action |
| --- | --- | --- | --- | --- |
| `1:2` Welcome | No accepted Welcome route/state; root redirects directly to CEO Desk | Local installation preference, Company existence query, Create/Skip actions | MISSING | BUILD |
| `1:83` Create Company | Existing onboarding can create/materialize Company from `FoundingRun`, but asks business intent and exposes internal stages | CEO display identity, optional avatar, Company name; atomic Company + CEO Assistant materialization | PARTIAL | ADAPT/BUILD |
| `1:188` Company Created | Existing UI has a success-like state but uses internal product language and does not present the accepted CEO/Company/Assistant result | Read materialized Company and actual CEO Assistant identity; separate AI readiness | PARTIAL | ADAPT |
| `1:424` Empty Curis — CEO Desk | Current CEO Desk has no-company empty state but Welcome skip/dismiss persistence is absent | `company=null` plus locally persisted Welcome dismissal; no fake Company/Business/Employee | PARTIAL | ADAPT + BUILD preference |
| `1:624` Empty Curis — Business Space | Business/Workspace routes exist; no accepted Empty Curis composition tied to Skip | Same truthful no-company context; Create Company return action | PARTIAL | ADAPT |
| `1:821` CEO Assistant — No Model | Assistant identity can exist; current dialog can render missing identity/context, but no accepted no-model conversation state | Real assistant identity + AI readiness derived from verified default model, not catalog row count | PARTIAL | ADAPT + bounded readiness projection |
| `1:1052` Model Management | Current Capability Center is an internal admin UI; real provider registry API exists | Provider list, connection state, discovered models, Health, enable/disable, default preference | PARTIAL | BUILD accepted surface; REUSE registry/preference APIs |
| `1:1292` Model Enabled | No accepted state; current readiness may count any private model row and is insufficient | Verified provider/model Health + durable credential + selected default model | BLOCKED for durable cloud readiness | BUILD UI; BLOCKED packaged restart truth by M3 |
| `1:1515` Empty Company | Current CEO Desk can show Company with zero workspaces/business activity | Company + Assistant exists; no Business; honest Create Business action | PARTIAL | ADAPT |
| `1:1727` Create Business | No accepted conversational implementation; current onboarding incorrectly mixes this with Company creation | Intent → Understanding → Clarification → Proposal → confirm → atomic Business + first Workspace | PARTIAL backend / MISSING frontend | BUILD; M2.5B READY TO IMPLEMENT |
| `1:1990` Add Model | Internal capability form exists, but accepted ordinary-user provider flow is absent | Provider selection, credential reference, endpoint rules, discovery/explicit model, connection test | PARTIAL | BUILD; M3 blocks durable cloud-secret acceptance |
| `1:2211` Advanced Settings | Internal detail forms expose many technical fields; no accepted advanced layer | Provider-specific allowed endpoint/auth/protocol fields with safe defaults and explicit risk | PARTIAL | ADAPT from registry metadata; do not expose Runtime internals by default |
| `1:2428` Model Selector Expanded | No shared Conversation model selector component found | Enabled model list + default preference + conversation selection semantics | MISSING/PARTIAL runtime | BUILD after selector contract wiring; no per-Employee forced binding in UI |

## 4. Company creation and identity truth

| Object | Current support | Gap / boundary |
| --- | --- | --- |
| CEO identity used for authorization | `X-Ceo-Id` exists, currently sourced from env/default `selfuse-ceo` | This is authorization identity, not accepted display identity |
| CEO Display Name | No canonical frontend/API persistence was found | Minimal identity presentation field/API is required; extend current local identity boundary, do not create `CEOProfileV2` |
| CEO Avatar | Shell currently hardcodes a glyph/avatar; no canonical upload/preset/fallback persistence found | Minimal optional presentation metadata is missing; must follow accepted shared Avatar pattern |
| Company | Real materialization exists in Runtime Foundation | Reuse; Company creation must not require Business or model readiness |
| CEO Assistant Runtime entity | Company materialization creates a real `CEO_ASSISTANT` entity | Reuse; identity existence must not be shown as AI Ready |
| CEO Assistant display identity | `assistant_identities` and GET/PUT identity API exist | Reuse; initialize/read the materialized Assistant consistently |

Minimum implementation gap: add or expose one canonical CEO display presentation record tied to the existing CEO identity, with name and optional avatar reference. Do not add a second account, employee or authentication identity model.

## 5. Optional onboarding truth

Current frontend does not implement `Welcome → Skip → Empty Curis`, and no durable `welcome_dismissed` preference was found.

Required minimum:

- Persist a local installation/user preference such as accepted Welcome version/dismissal.
- On restart, if dismissal exists and no Company exists, open truthful Empty Curis.
- Clearing or changing this preference must not create/delete Company or mutate Company lifecycle.
- Company presence always takes precedence over the local Welcome preference.
- The preference is presentation state only; it must never fabricate Company readiness.

Status: `MISSING`, bounded frontend/local-preference seam. This is not a schema justification by itself; use an existing app-local settings mechanism if one is already authoritative during implementation.

## 6. Model management and M3 security

### 6.1 Current provider/runtime support

The real backend registry currently describes these provider paths:

- Dynamic discovery: OpenAI, Anthropic, Google Gemini, DeepSeek, MiniMax, Moonshot/Kimi, Mistral, xAI, Groq, SiliconFlow, OpenRouter, NewAPI, OpenAI-compatible, Ollama, LM Studio.
- Explicit/curated model selection with conservative `not_tested` truth: Alibaba Qwen, Volcengine/Doubao, Zhipu.
- Local no-key/optional-key paths: Ollama and LM Studio.
- Official endpoints reject unapproved custom base URLs; loopback HTTP is restricted to local providers.

What is real today:

- Provider definitions, protocol/auth metadata and documentation URLs.
- Provider list API.
- Dynamic discovery or explicit model IDs by provider type.
- Connection/Health outcome and model catalog registration.
- Tenant default model metadata via `/api/workspace/model-preference`.
- Credential references through the existing vault service.

What is not proven:

- Every listed cloud provider has been connected end-to-end with a real account.
- Curated providers are healthy merely because a model ID was entered.
- Durable cloud credential recovery after packaged Desktop restart.
- A conversation-scoped model switch that is independent of employee binding.
- A complete enable/disable lifecycle projected through the accepted UI.

### 6.2 M3 boundary

`CredentialVaultService` defaults to an in-process `LocalDevCredentialBackend`. There is no accepted reusable macOS Keychain backend in the packaged Runtime.

| Scope | M3 impact |
| --- | --- |
| Model Settings frontend layout, provider browsing, local validation states | **Not blocked** |
| Ollama/LM Studio local discovery where no secret is needed | **Not blocked by Keychain**, still requires real local Health |
| Cloud credential entry contract and native handoff UI shell | **Can be implemented**, but not accepted as durable storage until M3 closes |
| Cloud model “Enabled/Connected” for the current process | **Conditional**; must not imply restart persistence |
| Packaged Desktop restart → credential recovered → Health → AI Ready | **BLOCKED by M3** |
| Entire App Entry | **Not blocked**; must render No Model / needs setup truthfully |

No secret may be placed in SQLite, frontend state persistence, logs, URL, environment fallback or fixture.

### 6.3 AI readiness correction

The current home summary can infer readiness from presence of a private-model row. That is not sufficient for the accepted `Model Enabled` state. V1 readiness must require, at minimum:

1. a selected default model;
2. its provider/model connection is currently verified/healthy under the authoritative registry;
3. required credential availability is proven for the current Runtime session;
4. after restart, M3 durable recovery is re-proven rather than inferred from database metadata.

## 7. Shared Conversation and Model Selector

### 7.1 Reusable foundation

- `GlobalAssistantProvider` and one global dialog/context entry already exist.
- Assistant display identity API exists.
- `SharedEmployeeWorkArea` establishes employee work/conversation/result-reference seams.
- Domain RD/XHS surfaces already use shared responsibility/result semantics.

### 7.2 Required migration

Current `GlobalAssistant.refresh()` synthesizes a snapshot from `RuntimeProvider`, and command submission returns canned/local responses instead of consuming the real Assistant command path. It is therefore not an accepted Conversation implementation.

One shared Conversation component should be used by:

- CEO Assistant;
- Team Leader;
- AI Employee.

The component should own shared presentation slots only: identity, message list, structured references, Composer, Model Selector, context/resource attachment, voice affordance and send state. Runtime actions remain role/context-specific adapters; do not create three chat systems.

### 7.3 Model selector Runtime gap

- Tenant default model metadata exists.
- Explicit employee/provider bindings exist in Runtime paths.
- No accepted frontend selector or proven conversation-scoped selection persistence was found.

Target behavior must not require the CEO to configure every Employee manually. Minimal V1 resolution order should be implemented in the existing model preference/binding path, not a new model system:

1. explicit conversation selection, if valid and enabled;
2. employee/role binding, if Runtime requires a specialized model;
3. tenant default model;
4. truthful No Model state.

The exact persistence location for conversation selection is an implementation gap. It must not be faked by labeling a tenant default as a per-conversation choice.

## 8. Create Business, M2.5B and Workspace materialization

### 8.1 Current delivery truth

- M1 canonical Business/Workspace ownership foundation: available.
- M2 General Workspace canonical execution: available headlessly.
- M2.5A bounded Business/Workspace/Work context propagation: closed.
- `FirstRunDelivery` accepts real `goal`, `positioning`, and `intent_summary`, and atomically materializes Company/Department/Business/First General Workspace.
- Current frontend sends/uses opaque founding intent and does not implement the accepted structured Conversation flow.

### 8.2 M2.5B decision

**M2.5B is no longer UI-HOLD. It is READY TO IMPLEMENT, not CLOSED.**

The Accepted App Entry UI and Create Business contract now define the interaction sufficiently: Intent → Understanding → Clarification → Structured Proposal → Confirm. Remaining work is frontend/adaptor wiring and truth-preserving state handling, not new product design.

### 8.3 General vs Professional truth

| Path | Current truth | Frontend implication |
| --- | --- | --- |
| General Business | Headless materialization and canonical Workspace execution exist | Can be implemented in Batch 1 after proposal confirmation |
| RD Professional Workspace | Accepted domain Workspace and real execution exist | A direct domain route exists, but no unified Create Business matcher/materializer was found |
| Content Growth / XHS Professional Workspace | XHS accepted instance and Content Growth headless runtime exist as separate truths | Do not equate either with automatic professional materialization from Create Business |
| Other business | Generic Workspace/package path exists in current foundations | Must show General Workspace unless a verified professional matcher/materializer exists |

Precise gap: one existing-authority integration seam must decide whether a confirmed proposal maps to a verified Professional Workspace package/domain or to General Workspace, then atomically create the canonical Business/First Workspace. Do not hardcode keyword matching in the page and do not claim Professional creation before this seam is tested.

## 9. CEO Desk 69:3 Runtime mapping

| Accepted responsibility | Current support | Truth and gap |
| --- | --- | --- |
| Company State | EXISTS | RuntimeProvider/company snapshot provides canonical Company and workspace context |
| Today Brief | DERIVABLE / PARTIAL | Deterministic summary can be produced from current canonical attention facts; existing operating-day service is partly legacy Project/Task oriented |
| Matters | PARTIAL | Current page has waiting/failed/invalidated simulation matters; no unified company-wide canonical matter projection |
| CEO Decision | PARTIAL | Real P7 `DECISION_PACKET` exists in domain Runtime; current CEO decisions page is a local placeholder and must not be reused as truth |
| Exception | PARTIAL | Domain failures and simulation failure facts exist; no aggregate Company projection |
| Handoff | PARTIAL | Persisted responsibility Handoff exists in shared/domain Runtime; no CEO Desk aggregate/read model |
| Important Result | PARTIAL | Result/Artifact/Evidence records exist; no canonical importance rule/company aggregation |
| Evidence | PARTIAL / EXISTS in domain | Real evidence is available by workspace/result reference; CEO Desk needs reference-only projection |
| Owner | PARTIAL | Responsibility/Employee identities exist; Company-level matter projection must expose the canonical holder |
| Current Work | PARTIAL | Workspace-scoped current Work/Execution exists; no company-wide query shaped for 69:3 |
| Return Time | MISSING | Some next-check timestamps exist in individual runtimes, but no accepted shared CEO return-time projection was found |
| Next Responsibility | PARTIAL | Handoff/assignment truth exists; aggregate next-responsibility read model is missing |
| CEO Assistant presence | EXISTS / PARTIAL UX | Identity and global entry exist; real shared Conversation is not implemented |

### Required bounded read-model seam

Do not make the frontend join every Runtime table. Add or adapt one Company-scoped read projection that returns references to existing truths, not copied objects:

- company state;
- attention items with source object/reference;
- canonical owner/current responsibility/current executor;
- decision/handoff/exception/result/evidence references;
- timestamps and next-check/return-time only when the source actually provides them;
- explicit unavailable/unknown fields when facts do not exist.

The legacy `/api/workspace/ceo/operating-day` can supply compatible facts only where lineage and semantics are canonical; it cannot silently define all 69:3 matters.

## 10. Attention ranking

No single canonical ranking service currently covers decision urgency, exception severity, Handoff follow-up, important Result and next responsibility. V1 does not need a ranking engine.

Minimum deterministic order using existing facts:

1. real `WAITING_CEO` Decision Packets;
2. real failed/blocked/invalid Runtime exceptions;
3. unacknowledged or overdue Handoffs;
4. real Results explicitly awaiting acceptance/review;
5. waiting/follow-up responsibilities with a real `next_check_at`/return time;
6. remaining recent factual matters.

Within a class: severity/irreversibility where present, then due/return time, then stable `updated_at + canonical ID` tie-breaker. Missing urgency/importance must remain `UNKNOWN`, not be guessed from message copy.

Status: `DERIVABLE` after the bounded canonical attention projection exists. Do not add machine-learned scoring, user-configurable weights or a new prioritization subsystem in Batch 1.

## 11. No-fake-data rule

The production CEO Desk and App Entry must never import Figma fixture data. If source facts are missing, render:

- `Empty`: the canonical object does not exist;
- `Quiet`: the object exists but there is nothing requiring attention;
- `Partial`: some source sections are available and others are not;
- `Waiting`: a real dependency/action is outstanding;
- `Unknown`: Runtime cannot prove the fact;
- `Unavailable`: the capability is not connected/supported.

Never fabricate Matter, Employee, Decision, Result, Evidence, timestamp, model Health or business status to match the accepted screenshot density.

## 12. Adaptation readiness

| Adaptation | Decision | Reason |
| --- | --- | --- |
| 1024 width | CAN DERIVE RESPONSIVELY | Current shell already has responsive drawer/layout mechanics; apply accepted hierarchy and validate, no new Figma required |
| Dark | V1 REQUIRED; CAN DERIVE FROM FROZEN TOKENS | Three-theme plumbing exists; this is implementation/validation, not design reopening |
| Dense Matters | CAN DERIVE FROM ACCEPTED COMPOSITION | Use bounded list density/overflow and stable ranking; no new product structure |
| Assistant Expanded | ALREADY COVERED BY SHARED PATTERN | Implement the accepted shared Conversation/Composer overlay |
| Decision Expanded | ALREADY COVERED BY P7 | Consume the same real Decision Packet; do not design another decision system |
| Evidence Expanded | ALREADY COVERED BY Result Reference / Utility | Default summary links to professional evidence; IDs/metadata stay in details |

Primary pixel fidelity remains the accepted 1440×900 Light baseline. Adaptations require Browser/Desktop validation but not another design round.

## 13. Shared component plan

Use the smallest set of product components; do not mirror every Figma frame as a component.

| Component/pattern | Current source | Action |
| --- | --- | --- |
| `AppShell` | `TerraShell` | REFACTOR/MIGRATE |
| `PrimaryNavigation` | `TerraNavData` + `TerraSidebar` | REPLACE data/semantics, reuse mechanics |
| `CEOIdentity` | hardcoded shell avatar + fixed CEO ID | BUILD minimal display projection |
| `Avatar` | no canonical shared frontend component found | BUILD one Upload/Preset/Fallback presentation component |
| `AssistantIdentity` | Assistant identity API/UI exists | REUSE/ADAPT |
| `Conversation` | `GlobalAssistant`, `SharedEmployeeWorkArea` partial seams | BUILD one shared presentation component; adapt role-specific runtime adapters |
| `Composer` | partial input/action surfaces exist | BUILD shared semantic slots; progressive availability |
| `ModelSelector` | missing | BUILD against enabled/default model truth |
| `StructuredSurface` | domain decision/result panels exist | EXTRACT/ADAPT shared wrapper only where semantics already match |
| `Matter` | CEO page simulation cards | REPLACE with canonical attention-item projection |
| `Result` | Result Reference/domain utilities | REUSE semantics, add CEO summary adapter |
| `ResponsibilityChain` | responsibility/handoff projections exist | REUSE shared projection; no new runtime |
| `EmptyState` | `RuntimeStates` + route-local states | REUSE and product-language adapters |

## 14. Replacement map

No deletion is authorized in this review.

| Old | New accepted UI | Replacement prerequisite | Delete condition |
| --- | --- | --- | --- |
| `/onboarding` FoundingRun debug-like flow | Welcome / Company Setup / Company Created | CEO display seam, Welcome preference, existing materialization adapter | New routes pass restart/recovery and no-company regression |
| Current CEO Desk workforce/staffing primary composition | CEO Desk 69:3 | Canonical company attention projection | 69:3 route is real-data-backed and workforce actions remain reachable elsewhere |
| Current capability admin page as ordinary model setup | Accepted Model Management/Add Model/Advanced | `ai-capabilities` + preference adapter; M3 truth states | New model routes cover provider list, Health, default, errors and local/cloud paths |
| `GlobalAssistant` canned/local command behavior | Shared real Conversation | Real command adapter, message/reference state and model selector | CEO/Leader/Employee conversation regressions pass |
| CEO decisions page local placeholder | P7 Decision projection | Company attention read model + real `DECISION_PACKET` action route | No local-only decision mutation remains |
| Company runtime compatibility page | Empty/Quiet/Partial CEO Desk + Business Space | Recovery duties mapped to accepted routes | Deep-link/recovery tests pass |
| Legacy nav/admin grouping | Seven-area primary navigation | Route ownership map and deep-link compatibility | All accepted routes + legacy redirects verified |

## 15. V1 Frontend Implementation Batch 1

No separate plan file is necessary; this bounded scope is sufficient for CEO review.

### MUST

1. App Shell and accepted seven-area navigation using current runtime provider and route truth.
2. Welcome, Create Company, Company Created, Empty Curis, Empty Company states.
3. Minimal CEO Display Name + optional Avatar projection/persistence seam; reuse existing CEO identity.
4. Optional Welcome skip persistence that does not mutate Company lifecycle.
5. CEO Assistant identity/presence and truthful No Model state.
6. Accepted Model Management shell against the real provider registry and model preference APIs; local/cloud/curated states remain distinct.
7. CEO Desk 69:3 composition with truthful Empty/Quiet/Partial/Waiting rendering.
8. One bounded canonical Company attention read-model seam; no frontend database reconstruction.
9. Create Business Conversation entry through Structured Proposal and General Business + First Workspace materialization.
10. Route, refresh and restart recovery on Browser and packaged Desktop candidate.

### SHOULD

1. Shared Conversation/Composer extraction for CEO Assistant, Leader and Employee.
2. Conversation Model Selector using enabled/default model truth.
3. Dark and 1024 adaptations.
4. Decision/Evidence expanded states by reusing P7 and Result Reference.
5. Dense-matter validation using deterministic ranking.

### DEFER

1. Automatic Professional Workspace matching/materialization until one verified shared matcher/materializer seam is approved and tested.
2. Voice capture and attachment ingestion if the underlying native/input handling is not already accepted; preserve honest disabled/unavailable affordances.
3. Advanced provider functionality beyond current registry protocols.
4. Full cleanup/deletion of legacy routes.

### BLOCKED

1. Durable cloud credential persistence and packaged restart AI Ready — `V1-P0-003` M3.
2. Any `Model Enabled` claim after restart without native Keychain recovery + Health.
3. Professional materialization claims without real matcher/materializer evidence.

### Exact initial implementation boundary recommendation

Before code, create one bounded frontend Issue. Its Allowed Files should start with existing shell/App Entry/CEO Desk/Assistant/model adapter files plus focused tests. Backend Allowed Files should include only explicitly approved CEO display, attention read-model, and adapter seams proven necessary. Do not include RD/XHS domain components, capability registry internals, credential backend, schema, Product Authority or Figma in the same Issue.

## 16. Test and acceptance plan

### Frontend unit/component

- Welcome/Create/Skip/Company Created state transitions.
- CEO display + avatar fallback/preset/upload reference rendering.
- Empty Curis vs Empty Company distinction.
- Model provider states: unconfigured, testing, healthy, failed, curated `not_tested`, unavailable.
- Shared Conversation rendering for CEO Assistant/Leader/Employee adapters.
- Model Selector default/explicit/invalid/unavailable states.
- CEO Matter/Result/Responsibility cards never render missing fixture values.

### Route and state rendering

- Fresh install/no preference/no Company → Welcome.
- Skip → Empty Curis; restart remains Empty Curis.
- Create Company → Company Created → No Model or Ready based on real truth.
- Company/no Business → Empty Company/Create Business.
- Direct links, back/forward, refresh and invalid context fail-closed.

### Runtime integration

- Company materialization returns one real Company and one real CEO Assistant.
- CEO display identity does not create a second CEO/Employee.
- Create Business confirmation persists canonical Business + First Workspace atomically.
- M2.5A bounded context remains intact.
- General Workspace can open and read its canonical parent path.
- Professional path remains unavailable/General unless a verified matcher/materializer returns a real domain Workspace.

### Credential/model

- Provider list reflects registry, not fixture.
- Ollama/LM Studio test uses real local Health when available; unavailable remains unavailable.
- Cloud model connection never persists secret in frontend/SQLite/logs.
- M3 acceptance requires native Keychain close/restart/Health/minimal call.
- Default model can only be set to an eligible real model.
- Conversation selector cannot list disabled/unverified models as ready.

### CEO Desk projection

- Real Company state.
- Deterministic attention order from canonical source facts.
- Real Decision/Handoff/Exception/Result/Evidence references.
- Unknown importance/return time stays unknown.
- Empty/Quiet/Partial/Waiting states with zero synthetic records.
- P7 Decision action updates the same Decision Packet.
- Result Reference opens the real evidence surface.

### Restart/recovery

- Browser reload, backend restart and packaged Desktop reopen preserve canonical Company/Business/Workspace and local Welcome preference.
- Persisted `RUNNING` does not prove a live executor after restart.
- Model readiness is re-evaluated; database metadata alone does not promote it to ready.
- Failed API/transport state recovers by rereading Runtime truth without duplicate creation.

### No-regression

- Accepted RD real execution and professional workspace routes.
- Accepted XHS instance/runtime routes.
- RuntimeProvider honest states.
- Shared Employee Work Area/Result Reference.
- canonical usage attribution and M2.5A context.
- Backend test DB safety with repository-external isolated SQLite.

### Browser/Desktop acceptance

- 1440×900 Light against accepted baselines.
- 1024 responsive layout.
- Dark theme.
- keyboard/focus/accessible names for navigation, Composer, dialogs and model management.
- packaged Desktop navigation, native credential handoff, resource paths, restart and console/IPC truth.

## 17. Final blocker ledger

| Blocker | Owner | Blocks | Does not block | Recovery gate |
| --- | --- | --- | --- | --- |
| CEO Display Identity persistence/API missing | Company OS identity integration | Accepted Company Setup completion | Shell/layout work, Company materialization | Approve minimal existing-identity extension and focused persistence test |
| Welcome skip persistence missing | Frontend/App local state | Skip/restart acceptance | Create Company path | Use authoritative app-local preference; prove no Company mutation |
| M3 native Keychain missing | Security + Desktop Runtime | Durable cloud enable and restart AI Ready | Provider UI, local model path, no-model state | Native Keychain packaged close/restart/Health/minimal call |
| Conversation Model Selector missing | Shared Frontend + existing model preference adapter | Frame `1:2428` real behavior | Model management UI | Implement selection resolution without second model system |
| Company-wide attention projection missing | Company OS read model | Full 69:3 real-data acceptance | Static composition/empty state implementation | One bounded reference-first projection + deterministic tests |
| Professional matcher/materializer missing | Workspace integration | Automatic RD/Content Growth materialization from Create Business | General Business path and direct existing domain routes | Verified proposal→domain package/workspace mapping and atomic E2E |

## 18. Final verdict

# READY WITH BOUNDED BLOCKERS

Immediate implementation is authorized only after a formal bounded Issue/Allowed Files is created. Accepted UI does not need another design round. The implementation must preserve real Runtime truth and stop short of these claims until evidence exists:

- durable cloud model enabled after packaged restart;
- conversation-specific model switching;
- automatic Professional Workspace materialization;
- complete CEO Desk attention data where no canonical source exists.

All other App Entry/CEO Desk structural work can proceed now using existing shell/runtime foundations and truthful empty/partial states.

**STOP FOR CEO / CHATGPT FRONTEND READINESS REVIEW**
