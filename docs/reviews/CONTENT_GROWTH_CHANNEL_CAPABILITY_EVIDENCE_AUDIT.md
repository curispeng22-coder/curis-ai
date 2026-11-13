# CONTENT GROWTH — CHANNEL CAPABILITY EVIDENCE AUDIT

Authority Class: EVIDENCE  
Status: Review  
Date: 2026-08-24  
Scope: CURRENT IMPLEMENTATION TRUTH ONLY  
Method: read-only source, test and accepted-evidence inspection; no external platform action, OAuth authorization, test execution, database write, code change or capability mutation.

## Executive conclusion

No audited channel capability is currently `VERIFIED` for XHS, Douyin, TikTok, YouTube or Bilibili.

Curis currently has three different, non-equivalent layers:

1. a generic connector catalog and a generic `social_auto_upload` HTTP bridge;
2. local credential metadata/secret-resolution plumbing and static platform-to-provider names;
3. an accepted XHS Workspace runtime that truthfully stops at `SCHEDULED`, accepts only CEO manual unverified receipts/interactions from its public API, and exposes publishing/analytics as waiting or unavailable.

None of those proves a connected channel account, successful native authorization, a live platform publication, a verified publication URL, live analytics, live comments, or multi-account isolation.

The IA blocker is nevertheless resolvable: IA may safely design the negative and conditional states recorded here. It may not treat any channel operation as available by default.

## Status vocabulary

- `VERIFIED`: Curis implementation plus locatable evidence proves the claimed capability.
- `PARTIAL`: implementation and evidence prove only a bounded portion of the chain.
- `CONDITIONAL`: an implementation path exists, but required external service/account/authorization or real-world evidence is absent.
- `UNKNOWN`: the repository contains insufficient evidence to make the claim.
- `UNAVAILABLE`: current implementation or accepted evidence explicitly says the capability is not present/supported.

## 1. Current Implementation Inventory

| Layer | Current implementation truth | Evidence | Boundary |
|---|---|---|---|
| Capability catalog | Generic capability/catalog infrastructure exists. No audited platform has a canonical channel capability definition proving auth/read/publish/analytics. | `backend/app/capability_catalog.py`; repository symbol search | Catalog visibility is not connection, authorization, health or execution proof. |
| Connector registry | Only `aitoearn` and generic `social_auto_upload` are registered. | `backend/app/connectors/registry.py`; `backend/app/connectors/__init__.py` | There is no native XHS/Douyin/TikTok/YouTube/Bilibili adapter in the registry. |
| Connector catalog API | Registered connectors are projected as `not_installed`, `not_authorized`, `health_status=unknown`, `not_company_resource`; default mode is `mock`. | `backend/app/main.py:5443-5480` | Switching `mock`/`real` mode does not install, authorize or verify a connector. |
| Generic publication bridge | `SocialAutoUploadConnector` can POST a publish package to an externally supplied `SAU_URL`; it accepts `platform`, cookie and account strings. | `backend/app/connectors/social_auto_upload.py:26-103` | This is a generic bridge, not a platform-native connector. The real branch has no accepted live-platform evidence, no response-schema verification, no published URL, no polling and no analytics/comments. Its fallback `status="published"` is not sufficient evidence. |
| Content workflow | A legacy workflow can generate a package and invoke the generic bridge after G1/G2 governance. | `backend/app/content_workflow_runtime.py:163-295`; `backend/app/runtime_governance.py:98-108,195-259` | The public endpoint does not prove a resumable approved external publication. A pending decision is cancelled fail-closed, and no canonical Channel Account/Publication is produced. |
| Credential plumbing | Local-dev Vault stores secrets in process memory and persists metadata/digest only. Static provider names exist for the five channels. | `backend/app/credential_vault.py:49-82,115-188`; `backend/app/content_workflow_runtime.py:40-54` | Vault `test()` proves only that a local secret can be resolved, not that a platform accepted it. No OAuth flow or account identity verification exists. |
| Credential account scope | Database compatibility includes an `account_id` column, but current credential service create/list/update projections do not consume or expose it. | `backend/app/database.py:1360-1361`; `backend/app/credential_vault.py:115-128,149-217` | A dormant column is not multi-account support. |
| Account selection | Legacy content workflow scans credentials and uses the first active credential matching a provider; the connector defaults `account="founder"`. | `backend/app/content_workflow_runtime.py:309-330`; `backend/app/connectors/social_auto_upload.py:35-49` | No canonical Channel Account is selected, checked for eligibility, or isolated per publication. |
| XHS domain runtime | ContentItem/version, internal scheduling, manual receipt/interaction records and truthful publishing/analytics projections exist. | `backend/app/runtime/workspace.py:3725-3865`; `backend/app/api/runtime_foundation_router.py:1366-1413,1660-1725` | Public routes reject `PLATFORM_API` claims; only a trusted backend integration may create them, and no such integration was found. |
| XHS accepted evidence | XHS Instance v1 is accepted through `SCHEDULED`; manual receipt is `UNVERIFIED`; direct `PUBLISHED` is rejected; analytics is `UNAVAILABLE`. | `reviews/XHS-WORKSPACE-INSTANCE-001_review.md:1-37,83-112`; `backend/tests/test_xhs_calendar_note_runtime.py:168-200` | The accepted Browser/Desktop proof explicitly used no platform account, external publication or analytics connector. |
| Cross-domain content proof | Controlled XHS Team Operating proof produces content artifacts while reporting `publicationStatus=NOT_CONNECTED` and `analyticsStatus=UNAVAILABLE`. | `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_CROSS_DOMAIN_CONTRACT_PROOF_REVIEW.md:7-31,70-71,143-147` | It proves internal Runtime/Provider callbacks, not external model quality, channel publication, receipt or analytics. |
| Tests | Connector tests prove mock response/persistence and local credential handling. No live `ConnectorMode.REAL` platform test or accepted E2E publication was found. | `backend/tests/test_v1_wave2_connector_mock.py`; `backend/tests/test_v1_wave2_vault.py`; `backend/tests/test_step4_connector_mode_toggle.py` | Mock success, mode selection and local secret resolution are not real-world channel evidence. |

### Repository-negative findings

The audited backend/frontend source contains no canonical implementation named `ChannelAccount`, `channel_account`, `target_account`, `account_pool`, `platform_account` or equivalent account-scoped publication binding. No test invoking `SocialAutoUploadConnector._publish_real()` or a live `SAU_URL` was found. These are negative search results, so they support `UNKNOWN`/`UNAVAILABLE`; they do not prove that an external platform lacks the capability.

## 2. Channel × Capability Truth Matrix

### 2.1 Identity and acquisition

| Channel | Auth | Read Content | Search / Research | Multi-account |
|---|---|---|---|---|
| XHS | `PARTIAL` | `UNKNOWN` | `UNKNOWN` | `UNAVAILABLE` |
| Douyin | `PARTIAL` | `UNKNOWN` | `UNKNOWN` | `UNAVAILABLE` |
| TikTok | `PARTIAL` | `UNKNOWN` | `UNKNOWN` | `UNAVAILABLE` |
| YouTube | `PARTIAL` | `UNKNOWN` | `UNKNOWN` | `UNAVAILABLE` |
| Bilibili | `PARTIAL` | `UNKNOWN` | `UNKNOWN` | `UNAVAILABLE` |

Auth is `PARTIAL` only for Curis-side credential plumbing: provider names, local secret storage/resolution and a tested Douyin-cookie metadata path exist. It does **not** mean platform login/OAuth/account ownership is verified. Read and search remain `UNKNOWN`; controlled research results and generated content are not platform reads. Multi-account is `UNAVAILABLE` in the current path because there is no Channel Account object or per-account resolver, and the legacy resolver takes the first matching credential.

### 2.2 Distribution and feedback

| Channel | Publish | Schedule | Publication Status | Receipt / Published URL | Analytics | Comments / Feedback |
|---|---|---|---|---|---|---|
| XHS | `CONDITIONAL` | `PARTIAL` | `PARTIAL` | `PARTIAL` | `UNAVAILABLE` | `PARTIAL` |
| Douyin | `CONDITIONAL` | `UNKNOWN` | `UNKNOWN` | `CONDITIONAL` | `UNKNOWN` | `UNKNOWN` |
| TikTok | `CONDITIONAL` | `UNKNOWN` | `UNKNOWN` | `CONDITIONAL` | `UNKNOWN` | `UNKNOWN` |
| YouTube | `CONDITIONAL` | `UNKNOWN` | `UNKNOWN` | `CONDITIONAL` | `UNKNOWN` | `UNKNOWN` |
| Bilibili | `CONDITIONAL` | `UNKNOWN` | `UNKNOWN` | `CONDITIONAL` | `UNKNOWN` | `UNKNOWN` |

Interpretation:

- `Publish = CONDITIONAL`: all five names can be passed to the same generic bridge, but the bridge depends on an external self-hosted service, a cookie and approved external action. No live channel publication is evidenced. This must not be displayed as available or verified.
- XHS `Schedule = PARTIAL`: Curis persists `scheduledFor` and the ContentItem reaches internal `SCHEDULED`. There is no evidence that XHS accepted a platform-side scheduled publication.
- XHS `Publication Status = PARTIAL`: Curis truthfully distinguishes waiting capability and unverified manual receipt. It does not query platform status.
- XHS `Receipt / Published URL = PARTIAL`: a CEO can record an explicitly `UNVERIFIED` manual receipt; a trusted `PLATFORM_API` shape exists but has no connected producer. No real published URL is proved.
- Other channels `Receipt / Published URL = CONDITIONAL`: the generic bridge can pass through a `post_id` returned by its external service, but no real response was tested or schema-verified and no URL is returned.
- XHS `Comments / Feedback = PARTIAL`: CEO manual interaction records exist. Platform-origin interactions are rejected unless supplied by a trusted backend integration; none was found.
- XHS `Analytics = UNAVAILABLE`: current accepted projection explicitly returns no metrics/unavailable. For the other channels, absence of an implementation is recorded as `UNKNOWN`, not a claim that the platforms cannot provide analytics.

## 3. Evidence Map

| ID | Layer | Implementation path | Evidence / test | Proves | Does not prove |
|---|---|---|---|---|---|
| E1 | Connector code | `backend/app/connectors/social_auto_upload.py` | Source inspection | A generic mock/real HTTP publication bridge exists. | Installation, auth, health, native API support, live publication, receipt validity, URL, analytics, comments. |
| E2 | Workflow code | `backend/app/content_workflow_runtime.py` | Source inspection | Platform names map to provider strings; bridge is called only after governance. | Canonical Channel Account, per-account eligibility, live approved publish/resume, platform outcome. |
| E3 | Catalog API | `backend/app/main.py:5443-5506` | Source inspection | Connector discoverability and explicit not-installed/not-authorized/unknown-health projection. | A usable connector or connected account. |
| E4 | Mock connector test | `backend/tests/test_v1_wave2_connector_mock.py` | Existing mock test | Mock response shape and internal persistence. | Any real platform action. |
| E5 | Vault test | `backend/tests/test_v1_wave2_vault.py` | Existing local-dev test | Secret redaction, metadata/digest persistence and local resolution; one Douyin provider string. | OAuth, cookie validity, account ownership, platform authorization, multi-account isolation. |
| E6 | Mode test | `backend/tests/test_step4_connector_mode_toggle.py` | Existing test | Mode setting can read/write `mock` or `real`. | External service availability or connector health. |
| E7 | XHS runtime | `backend/app/runtime/workspace.py`; `backend/app/api/runtime_foundation_router.py` | Source plus focused XHS test | Internal scheduling; manual unverified receipt/interaction; trusted-source boundary; no direct fake publish. | A trusted platform integration, published URL or live feedback. |
| E8 | XHS acceptance | `reviews/XHS-WORKSPACE-INSTANCE-001_review.md` | Accepted Browser/Desktop/restart evidence | SCHEDULED, waiting publication capability, no executor, no analytics; persistence. | Real XHS publish/receipt/analytics. |
| E9 | Autonomous XHS proof | `docs/reviews/CURIS_AUTONOMOUS_OPERATING_V1_CROSS_DOMAIN_CONTRACT_PROOF_REVIEW.md` | Accepted controlled-provider proof | Internal content artifacts and provider callback provenance. | External channel quality, publication, receipt or analytics. |
| E10 | Governance | `backend/app/runtime_governance.py`; `backend/app/content_workflow_runtime.py:214-245` | Source inspection | External publish is high-impact and fail-closed without a completed decision path. | A user-approved, resumable live publish path. |
| E11 | Negative implementation search | backend/frontend source search | No canonical Channel Account or live real-connector test found | Current repository does not evidence those capabilities. | Platform theoretical support or future implementation feasibility. |

### Four-layer separation

| Layer | Current finding |
|---|---|
| A. Platform theoretically supports it | Out of scope; not used as implementation evidence. |
| B. Curis has connector code | Yes, one generic publication bridge. |
| C. Connector has been tested | Mock branch and mode/vault plumbing only. Real platform branch: no accepted evidence. |
| D. Real end-to-end operation proved | No, for every audited platform and capability. |

## 4. Multi-account Truth

| Requirement | Current truth | Verdict |
|---|---|---|
| Channel is distinct from Channel Account | Frozen product/domain authority says yes; current Runtime does not implement the account object. | `PARTIAL` at authority level; implementation unavailable. |
| Multiple accounts on one platform | No canonical account collection, selector or account-scoped eligibility was found. | `UNAVAILABLE` |
| Authorization per account | Credential metadata has no active account-scoped service/API contract; resolver selects first matching provider credential. | `UNAVAILABLE` |
| Eligibility per account | No implementation/evidence found. | `UNKNOWN` |
| Publication per account | Generic connector accepts a free-form `account` string but workflow does not pass a selected account and defaults to `founder`. | `UNAVAILABLE` |
| Receipt per account | No canonical account reference or tested receipt binding. | `UNKNOWN` |
| Context isolation per account | Tenant scoping exists for credentials and Workspace objects; account-scoped isolation is not implemented/tested. | `UNKNOWN` |
| Real multi-account test/E2E | None found. | `UNKNOWN` |

The free-form `account` request field and dormant database `account_id` column must not be interpreted as multi-account support.

## 5. IA-safe Capability Assumptions

| IA question | Safe assumption | Allowed representation |
|---|---|---|
| Show a connected account? | **NO** | Show “未连接 / 未验证 / 未知”; do not invent account identity. |
| Show channel catalog entries? | **YES, as discoverable metadata only** | Clearly distinguish catalog visibility from installation, authorization and health. |
| Show Publish as available? | **NO / CONDITIONAL** | Disabled or responsibility state: “发布能力未连接”; configuration/recovery entry may be designed. |
| Show Curis-side schedule? | **YES for XHS only** | “已排期” means an internal plan, not platform scheduling. Other channels remain unknown. |
| Show platform publication status? | **NO** | XHS may show “等待发布能力” or “人工回执未验证”; no platform polling claim. |
| Show a real Published URL? | **NO** | No audited evidence supports it. |
| Accept a manual receipt? | **YES for XHS, explicitly unverified** | Label source `CEO_MANUAL` and verification `UNVERIFIED`; never convert it to verified platform truth. |
| Show Analytics? | **NO** | XHS: “暂无数据 / 数据能力未连接”; others: unknown/unavailable state only. |
| Show Comments / Feedback? | **NO for live platform data** | XHS may offer CEO manual input with explicit manual/unverified provenance. |
| Show channel Search / Research? | **NO as a channel capability** | Manual or controlled research may appear only with its own provenance, never as “已读取平台”. |
| Support Multi-account? | **NO** | Do not provide account switching, per-account eligibility or account-scoped publish claims. |
| Show a successful mock publication? | **NO** | Mock responses are test-only and must not enter IA as product truth. |

IA may therefore model `Unavailable`, `Not connected`, `Unknown`, `Needs authorization`, `Waiting for capability`, `Manual / Unverified`, and `Real-world evidence required`. It may not make `Connected`, `Publish`, `Published URL`, `Analytics`, `Comments` or `Multi-account` default operating capabilities.

## 6. Gaps / Real-world Evidence Required

The following gaps require implementation plus controlled real-world evidence before any status can become `VERIFIED`:

1. **Canonical Channel Account binding** — account identity, platform, Company/Workspace ownership, authorization reference and isolation.
2. **Per-account authorization evidence** — platform accepts the credential/token; refresh/revocation/failure behavior is known.
3. **Connector installation and health** — a specific adapter is installed, reachable and checked independently of catalog visibility/mode.
4. **Per-account eligibility** — supported operations and constraints are resolved for the selected account.
5. **Live publish proof** — approved external action, exact account, immutable request reference, real success/failure result and no mock fallback.
6. **Verified receipt** — trusted source, external ID, published URL where supplied, version/account binding and restart persistence.
7. **Publication status query/reconciliation** — pending/success/failure/deletion or platform drift from real source.
8. **Platform-side scheduling** — real schedule request, timezone, update/cancel semantics and platform confirmation per channel.
9. **Analytics ingestion** — metric source, account/publication binding, observation time, failure/unknown semantics and no invented values.
10. **Comments/feedback ingestion** — source identity, pagination/deduplication, sensitive-data policy and manual-vs-platform provenance.
11. **Multi-account E2E** — two accounts on one channel proving isolated auth, eligibility, publication, receipt, context and restart.

All eleven are `REAL-WORLD EVIDENCE REQUIRED`. This audit did not perform them.

## 7. Final Blocker Decision

**CHANNEL CAPABILITY BLOCKER RESOLVED**

Resolution is conservative, not a capability acceptance:

- IA now has a bounded current-truth baseline.
- No audited channel capability is `VERIFIED`.
- IA may proceed with unavailable/unknown/conditional/manual-unverified states.
- IA must not assume connected accounts, live publishing, platform scheduling, verified URLs, analytics, comments or multi-account support.
- Any future upgrade from this matrix requires implementation evidence and, where applicable, controlled real-world platform evidence.

Active databases were opened read-only only. At audit start:

- `data/curis.sqlite`: size `1232896`, mtime `1786873339`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, `integrity_check=ok`.
- `backend/data/curis.sqlite`: size `1277952`, mtime `1786783659`, SHA-256 `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`, `integrity_check=ok`.

No Runtime, Schema, Capability Registry, Connector, test, IA, Figma, account or publication was changed or created.
