# CURIS-V1-TALENT-CAPABILITY-PRODUCTIZATION-001

Status: Review
Authority Class: CURRENT IMPLEMENTATION ISSUE
Date: 2026-08-31
Owner: Main Development Session

## Goal

将现有 Talent Market、Employee、Skill、Capability Binding 与 Connector truth 收口为普通用户可理解的“人才与能力”产品区。固定一级结构为 `专家 / 技能 / 连接器`；复用 canonical 招聘、安装、绑定、健康与 Credential 边界，不建立第二套 Employee、Capability、Provider 或 Connector 系统。

## Authority

- `docs/reviews/CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md`
- `docs/01_Product/Curis_Talent_Market_Product_Map.md`
- `docs/01_Product/Curis_Talent_Market_Integration_Contract.md`
- `docs/reviews/CURIS_AVATAR_IDENTITY_PATTERN.md`
- Current Product Blueprint / Master Map / UI Blueprint
- Current Employee / Responsibility / Capability / Provider / Keychain implementation truth
- `docs/00_Context/CURRENT_STATE.md`

Specific Talent visual remains open. This Issue performs bounded in-place productization over the existing accepted composition and Direction D; it does not create a new IA or invoke Figma.

## Current Gap

- Current page exposes `Candidate`, `MCP`, source path, maturity and mock/runtime language.
- Experts do not clearly separate recruitable templates from current Company Employees.
- Employee ability truth is not visible from persisted Skill/Capability bindings.
- Connector definition is visible, but authorization/health is not translated into ordinary-user status.
- Recruitment/install/connection entry does not preserve a safe return to the originating Business/Workspace context.
- Catalog existence can visually resemble execution availability.

## Pre-change Ownership

| Path | SHA-256 | Ownership decision |
|---|---|---|
| `frontend/app/ceo-office/talent-market/page.js` | `3fc09ff972baa0de6b8e66dfa086be16f01c57e460a4ae0306a63ef402101196` | Untracked preserved candidate. This Issue owns only Talent product-language, current-employee, status and safe return-context semantics. |
| `frontend/lib/talentMarket.js` | `c3b2ac01f0798f5835e0bf07f7cbd805f45d392dcda306d5bd79e05f9b0bdc9f` | Untracked preserved candidate. This Issue owns only current Employee ability reads and product-state normalization helpers. |
| `frontend/app/ceo-office/organization/OrganizationCenter.js` | `e28d8401ed89058f7f04b637338990a721303cd5f141dd5984bf7121d7925975` | Read-only dependency. Existing `source=organization` link is consumed; no modification is authorized. |

HEAD at preflight: `c797db840bad285d7e9f1962d06eac61aa28508b`.

## Allowed Files

- `frontend/app/ceo-office/talent-market/page.js`
- `frontend/lib/talentMarket.js`
- `frontend/tests/talentCapabilityProductization.test.mjs`
- `backend/tests/test_talent_capability_productization.py`
- this Issue
- `docs/reviews/CURIS_V1_TALENT_CAPABILITY_PRODUCTIZATION_REVIEW.md`

No backend production source, Schema, Product Authority, Organization Center source, model settings or Connector registry change is authorized.

## Product Truth Contract

### Experts

- Distinguish `可招聘专家` and `公司员工`.
- Recruitable expert must be an active canonical EmployeeTemplate accepted by the existing recruitment endpoint.
- External candidates remain `正在准备 / 暂不可招聘`; catalog entries never become Employees by display alone.
- Company Employee detail reads canonical Employee identity plus persisted Skill/Capability bindings.

### Skills

- Definition/catalog presence is separate from Company installation and Employee binding.
- Installation reuses the idempotent existing Skill endpoint.
- Binding reuses existing Employee Skill Binding and is not automatically applied to every Employee.

### Connectors

- Display only ordinary-user states derived from current authorization and health truth.
- `not_authorized/unknown/mock` never becomes connected/working.
- Current missing authorization UI remains an honest unavailable/setup boundary; no fake success.

### Return Context

- Accept only safe local Curis paths from `returnTo` or the known Organization source.
- Recruitment/install/binding completion presents a direct return action; no automatic external navigation.
- Unsafe/external return references are ignored.

### Avatar

- Existing identity/fallback is reused.
- Upload/Preset persistence is not implemented by this Issue and is not a recruitment prerequisite.

## Acceptance Scenarios

1. Recruitable expert → canonical recruitment → real Employee → default Skill binding → Organization visibility.
2. Official Skill → idempotent Company install → explicit Employee binding → persisted read after restart.
3. Connector definition with no authorization/health → `未连接 / 需要授权 / 暂不可用`, never “已连接”.
4. Safe Business/Workspace return reference survives product flow and returns to the source path; unsafe path fails closed.
5. Current Employee shows real Role plus persisted Skill/Capability counts; missing bindings remain explicit.
6. External Candidate remains not recruitable and exposes no engineering maturity/path language.
7. Browser and fresh packaged Desktop: Experts, recruitment, Skills, Connectors, return context and restart.
8. Organization, Employee Detail, General Workspace, Cloud Model/Keychain, Operating Intelligence, Result/P7 and DB Safety no-regression.

## Active DB Protection

Preflight fingerprints:

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

All tests and Browser/Desktop evidence use repository-external isolated SQLite/app-data.

## Explicit Exclusions

- No new Product model, Employee/Avatar/Capability/Provider/Connector system.
- No model configuration redesign, Organization redesign, Marketplace, external Connector implementation, OAuth or real publication.
- No Candidate promotion, new provider, Figma, meeting, knowledge, operating intelligence or release work.
- No commit or push.

## Stop Gates

- A second Employee/Capability/Connector truth or unauthorised Schema is required.
- Current accepted composition cannot express the required UI without a new visual/IA decision.
- Active DB mutation or ownership collision occurs.

## Implementation Result

`IMPLEMENTED / ACCEPTED CANDIDATE`

Implemented within the bounded frontend and test scope:

- Product structure is `专家 / 技能 / 连接器`; ordinary users no longer see Candidate, MCP, source-path, maturity or mock/runtime vocabulary in the main path.
- Recruitable canonical EmployeeTemplate creates a real EmployeeInstance with its real default Skill; Company Employees read persisted Skill and Capability bindings.
- Supported official Skills install idempotently and bind explicitly to one Employee without replacing existing bindings.
- Unsupported official Skill types stay `暂不可用`; catalog presence is not promoted to runtime availability.
- Connector definitions stay visible, while current `not_authorized / unknown / mock_only` truth is rendered as `未连接 / 暂不可用于真实业务` with no false authorization entry.
- Safe local `returnTo` and Organization source context are preserved; external paths fail closed.
- Browser and fresh packaged Desktop verified recruitment, install, binding, Connector truth, Organization continuity, failure/retry and same-root restart persistence.

Acceptance evidence is recorded in:

- `docs/reviews/CURIS_V1_TALENT_CAPABILITY_PRODUCTIZATION_REVIEW.md`

Current truthful boundaries:

- External Candidates remain non-recruitable.
- Avatar upload/preset persistence is not implemented; the existing first-character fallback is reused.
- Real Connector authorization, external health and external execution are not connected.
- No new model/provider, Employee, Capability, Skill or Connector system was created.

## P1 Employee Avatar Closure · 2026-09-01

The bounded final P1 closure is recorded in:

- `issues/CURIS-V1-EMPLOYEE-RECRUITMENT-AVATAR-CLOSURE-001.md`
- `docs/reviews/CURIS_V1_EMPLOYEE_RECRUITMENT_AVATAR_CLOSURE_REVIEW.md`

This closure supersedes only the earlier avatar gap: Employee recruitment now supports validated upload, bundled Curis preset, and stable fallback through the same canonical Employee identity. Connector and unsupported external capability boundaries remain unchanged.

Recommended combined status: `TALENT & CAPABILITY: IMPLEMENTED / ACCEPTED` after CEO review of the avatar closure.
