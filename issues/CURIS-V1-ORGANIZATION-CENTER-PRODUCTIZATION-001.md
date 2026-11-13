# CURIS-V1-ORGANIZATION-CENTER-PRODUCTIZATION-001

Status: Review
Authority Class: CURRENT IMPLEMENTATION ISSUE
Date: 2026-08-31
Owner: Main Development Session

## Goal

将已接受的 Organization Center Figma 基线接到现有 canonical Company / Department / Business / Workspace / Responsibility / Employee truth，形成可回访的“公司版图 + 员工目录”产品面；不创建第二套组织数据或写入 Authority。

## Authority

- `docs/reviews/CURIS_V1_ORGANIZATION_CENTER_UI_ACCEPTANCE.md`（Frozen）
- Figma `2Fh7DgPPfLgdbvNtnzPnk9`：`106:3`、`106:230`、`106:457`
- `docs/reviews/ORGANIZATION_CENTER_PAGE_CONTRACT_FINAL_REVIEW.md`
- `docs/reviews/CURIS_V1_PRODUCT_COMPLETION_RECONCILIATION.md`
- Current Product Blueprint / UI Blueprint / CURRENT_STATE

## Pre-change Ownership

| Path | SHA-256 | Ownership decision |
|---|---|---|
| `frontend/app/ceo-office/organization/page.js` | `a94502d0f5a258c03efd15ce54ac6401d6ca04af008a788144c84dd71305691b` | Mixed source. Existing capability-asset delta is preserved as exported legacy component; this Issue owns only canonical route delegation. |
| `frontend/lib/runtimeApi.js` | `6c29aea24f53330203e4a5693c81a396716d162a8bc9796fe2acbfbd7472568c` | Mixed source. This Issue owns one Organization projection GET wrapper beside the existing canonical Business APIs. |
| `frontend/lib/api.js` | `e06a18db7f28c5408e632ec23cd4ab2c8a52141c5ff472a9093c901c01c58350` | Read only; existing Company / Department / Employee APIs reused. |
| `backend/app/api/runtime_foundation_router.py` | `a1932d26204d45bbece6c8bbfba4911778a81140e4b0af760895815dbeb74241` | Mixed source. This Issue owns one import and one read-only Organization endpoint beside the existing Business endpoints. |
| `backend/app/runtime/business_spine.py` | `ff732cc035a1a7bf6d45101a02a15c912f2dc51a9d252e435b4c458eb0af3b72` | Read only; existing canonical Business read model reused. |

## Allowed Files

- `frontend/app/ceo-office/organization/page.js` — exact export/delegation hunk only
- `frontend/app/ceo-office/organization/OrganizationCenter.js`
- `frontend/app/ceo-office/organization/organizationCenter.module.css`
- `frontend/lib/organizationProjection.js`
- `frontend/lib/runtimeApi.js` — exact Organization projection GET wrapper hunk only
- `frontend/tests/organizationCenter.test.mjs`
- `backend/app/organization_projection.py`
- `backend/app/api/runtime_foundation_router.py` — exact import and GET endpoint hunks only
- `backend/tests/test_organization_center_projection.py`
- `issues/CURIS-V1-ORGANIZATION-CENTER-PRODUCTIZATION-001.md`
- `docs/reviews/CURIS_V1_ORGANIZATION_CENTER_PRODUCTIZATION_REVIEW.md`

Any expansion requires Issue amendment. No schema or write-path production change is authorized.

## Projection Contract

The read projection may only combine:

- Runtime company snapshot / canonical company identity
- `department_instances`
- `canonical_businesses` through the accepted Business read model
- canonical Business `workspaces`
- canonical Business-scope `RESPONSIBILITY_ASSIGNMENT` records
- Company `employee_instances`
- accepted `EmployeeExecutionIdentity.resolve()` bridge for Runtime Employee → Company Employee

Missing leader, goal, role, vacancy or risk remains unknown / absent. Project, Capability, Provider, Model and Figma fixtures are excluded.

The projection is read-only. An assignment whose canonical Employee bridge cannot be verified remains unresolved; the endpoint must not guess from names, roles or IDs outside the accepted exact-ID fallback.

## Acceptance

1. Canonical route shows fixed top tabs `公司版图 / 员工目录`.
2. Company Map renders real Department containers and Business-first content.
3. Business Focus stays within Company Map and links to canonical Business / Workspace surfaces.
4. Role/staffing uses only persisted Responsibility assignments.
5. Vacancy/risk are not inferred from employee count or generic Runtime status.
6. Employee Directory resolves Employee → Role/Responsibility → Business → Department without duplicating identity.
7. Search uses only real fields; empty/loading/error do not fall back to fixtures or Projects.
8. Restart with the same isolated SQLite preserves canonical relationships.
9. Browser and packaged Desktop exercise both tabs and Business Focus.
10. Existing App Entry / CEO Desk / Business / Workspace / Employee / Talent / Conversation / P7 / Result/Evidence regressions remain green.

## DB Safety

All Runtime tests use repository-external isolated SQLite and the existing three-variable fail-fast guard. Active databases are read-only fingerprints only.

Pre-change fingerprints:

- `data/curis.sqlite`: size `1232896`, mtime `1786873339`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, integrity `ok`
- `backend/data/curis.sqlite`: size `1277952`, mtime `1786783659`, SHA-256 `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`, integrity `ok`

## Explicit Exclusions

- Product redesign or Figma edits
- New Organization / Employee / Role / Responsibility / Business / Workspace primitive
- Organization write authority or schema migration
- Capability Catalog, Operating Intelligence, Meeting or Release changes
- Fixture production data, Project fallback, inferred vacancy/risk
- Dark/1024 visual acceptance beyond no-regression
- Commit or push

## Stop Gates

- Product Authority conflict
- Canonical relationships cannot express the accepted page without a new write authority/schema
- Active DB mutation
- Collision with another initiative in the exact owned hunk

## Current State

IMPLEMENTED / ACCEPTED CANDIDATE

- Canonical route now delegates to the bounded Organization Center implementation while preserving the mixed-source legacy component for later P2 cleanup.
- Read projection resolves Business-scoped Responsibility assignments through the accepted `EmployeeExecutionIdentity` bridge; unresolved identity remains unknown.
- Browser and fresh packaged Desktop evidence passed against repository-external isolated SQLite, including Runtime/app restart.
- No real Vacancy requirement or Risk record existed in the accepted scenario; neither was inferred or displayed. Talent routing remains conditional on a future proven vacancy.
- Active SQLite fingerprints remained byte-identical. No commit or push was performed.

Formal evidence: `docs/reviews/CURIS_V1_ORGANIZATION_CENTER_PRODUCTIZATION_REVIEW.md`.
