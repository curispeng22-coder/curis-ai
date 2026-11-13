# CURIS V1 ORGANIZATION CENTER PRODUCTIZATION REVIEW

Status: Review
Authority Class: REVIEW
Date: 2026-08-31
Issue: `CURIS-V1-ORGANIZATION-CENTER-PRODUCTIZATION-001`

## Verdict

**ORGANIZATION CENTER: IMPLEMENTED / ACCEPTED CANDIDATE**

The accepted Figma structure is implemented over canonical Company OS records. This Review does not create Product Authority and does not claim Vacancy, Risk or Talent routing when no corresponding canonical fact exists.

## 1. Legacy Reconciliation

- `KEEP`: existing legacy components, forms and routes remain in the repository for callers outside the canonical entry.
- `REWIRE`: `/ceo-office/organization` now delegates to `OrganizationCenter`.
- `SUPERSEDED IN CURRENT PATH`: Project dashboard, Capability asset panel and “AI 团队办公室” are not consumed by the canonical Organization Center.
- `PRESERVED`: the mixed-source legacy page remains as named export `LegacyOrganizationPage`; no unrelated hunk was deleted or absorbed.
- P2: remove the preserved legacy implementation only after an independent reference audit.

## 2. Accepted Figma Implementation

Consumed implementation references:

- Figma `2Fh7DgPPfLgdbvNtnzPnk9` node `106:3`: Company Map default.
- node `106:230`: Business Focus.
- node `106:457`: Employee Directory.

Implemented the accepted hierarchy, low-card Department containers, Business-first scan order, fixed top tabs, Business Focus composition, Employee-first directory and Direction D neutral/Iris language. Visual vignettes and fixture names were not copied into production data.

## 3. Top Tabs

`公司版图 / 员工目录` are fixed horizontal views inside one Organization Center route. Organization Center has no persistent secondary left context pane and creates no third tab.

## 4. Company Map

The default view renders the current Company summary, Department containers, canonical Businesses, real goals, verified leaders, role/staffing summaries and Workspace counts. Search covers Business, responsibility/role and verified owner names.

## 5. Department Container

Departments are low-emphasis containers. Businesses are the first visual work objects inside each container. Missing mission text remains “部门职责尚未设置”; no description is inferred.

## 6. Business-first

Business name, status, verified leader, goal, role/staffing and Workspace count lead the scan. Workspace remains a secondary execution-space entry and is not promoted to the Company Map root.

## 7. Staffing / Vacancy Truth

Staffing comes only from persisted Business-scoped `RESPONSIBILITY_ASSIGNMENT` plus a verified Runtime Employee → Company Employee identity bridge. Employee count is not used to infer a role.

No accepted Vacancy requirement record was present in the scenario, so vacancy remains `0/hidden`. Waiting, employee scarcity or DRAFT status do not create a vacancy or risk. No risk filter is shown without risk truth.

## 8. Business Focus

Selecting a Business keeps `公司版图` selected and shows canonical Department, Business goal/positioning, verified leader, role assignments, employees and Workspace summary. `进入业务详情` routes to the canonical Business surface; Workspace links route to canonical Workspace identity.

## 9. Employee Directory

The directory groups Company Employees by real Department. Each row presents Employee, ordinary-language status, role, and all verified Business Responsibility assignments. It creates no fake primary assignment.

## 10. Reverse Lookup

`Employee → Responsibility/Role → Business → Department` is resolved from one bounded read projection. Multi-Business assignments remain multiple. Runtime Employee IDs that cannot be resolved through the accepted identity bridge are not attached to a Company Employee.

## 11. Talent Routing

The product route is implemented conditionally as `/ceo-office/talent-market?source=organization`; it appears only when `vacancyCount > 0`. Because no proven vacancy existed, Browser/Desktop acceptance correctly did not expose the action and did not create or bind an Employee.

## 12. Empty / Loading / Error

- Loading uses `RuntimeLoading` and never flashes Figma fixtures.
- Empty Company/organization uses explicit empty states.
- Projection failure uses `RuntimeError` with retry behavior inherited from the shared Runtime pattern.
- Unresolved Business parent facts are withheld with a canonical-relation warning; Project fallback is forbidden.

## 13. Canonical Projection

Added one read-only endpoint:

`GET /api/workspace/runtime/foundation/companies/{company_id}/organization`

It composes existing `companies`, `department_instances`, `canonical_businesses`, `workspaces`, Business-scoped `RESPONSIBILITY_ASSIGNMENT`, `employee_instances`, and the accepted `EmployeeExecutionIdentity.resolve()` bridge. It introduces no table, migration, write authority, Organization store or identity primitive. Tenant mismatch fails closed before any data is returned.

## 14. Restart

Repository-external SQLite `/tmp/curis-org-center-browser.hA3raj/organization.sqlite` retained the same Company, two Departments, two Businesses, two Employees, assignments and Workspace links after backend stop/restart. The packaged app used isolated root `/tmp/curis-org-center-desktop.koE8Xy`; full app exit closed ports `3010/8002/8080`, and reopening the same root restored the same Organization Center without duplicate objects.

## 15. Browser

1440×900 Browser acceptance at `http://127.0.0.1:3000/ceo-office/organization` passed:

- Company Map with two Department containers and two canonical Businesses.
- Business/owner search filtered to the matching Business.
- Business Focus retained the Company Map tab and showed canonical role/Workspace facts.
- Employee Directory showed both Employees and reverse Business assignments.
- Employee/Business search filtered correctly.
- reload after Runtime restart recovered the same records.
- console errors/warnings: `0`.

Evidence:

- `/tmp/curis-organization-center-evidence/browser-company-map.png`
- `/tmp/curis-organization-center-evidence/browser-business-focus.png`
- `/tmp/curis-organization-center-evidence/browser-employee-directory.png`

## 16. Packaged Desktop

Fresh source build:

- App: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`
- Binary: `/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app/Contents/MacOS/curis-desktop`
- Binary SHA-256: `cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`

Packaged UI acceptance passed Company Map, Business Focus, Employee Directory, canonical links, native 1440 layout, full exit, sidecar shutdown, reopen and relationship recovery. Browser evidence was not substituted for Desktop evidence.

Evidence:

- `/tmp/curis-organization-center-evidence/desktop-company-map.png`
- `/tmp/curis-organization-center-evidence/desktop-business-focus.png`
- `/tmp/curis-organization-center-evidence/desktop-employee-directory.png`

## 17. Tests / Build

- Backend focused/no-regression: `25 passed`.
- Frontend focused/no-regression: `29 passed`.
- Organization projection tests include canonical identity, tenant fail-closed, restart, no vacancy/risk inference, multi-assignment and empty truth.
- Python compile: PASS.
- Scoped ESLint: PASS with `0` errors/warnings in the new canonical files.
- Frontend production build: PASS, including `/ceo-office/organization`.
- Fresh PyInstaller sidecars + Cargo/Tauri app build: PASS.
- `git diff --check`: PASS.

The preserved legacy component still has one pre-existing `react-hooks/exhaustive-deps` warning outside the canonical implementation; it was not changed because the Issue owns only the default-route delegation hunk in that mixed-source file.

## 18. Active DB Safety

Both active databases remained byte-identical from preflight to closeout:

| Path | Size | mtime | SHA-256 | integrity_check |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

No active DB initialization, migration or write occurred.

## 19. Remaining P1 / P2

- P1: project canonical Vacancy and Risk only when an accepted persisted source exists; until then they remain hidden/unknown.
- P2: 1024/Dark visual acceptance and independent legacy-component cleanup.
- P2: improve generic Company status copy where a future accepted mapping exists.

These do not invalidate the accepted 1440 Light Organization Center candidate.

## 20. Changed Files

Issue-owned implementation:

- `backend/app/organization_projection.py`
- `backend/app/api/runtime_foundation_router.py` — one import and one GET endpoint hunk only
- `backend/tests/test_organization_center_projection.py`
- `frontend/app/ceo-office/organization/page.js` — canonical import/export delegation hunks only; prior mixed changes preserved
- `frontend/app/ceo-office/organization/OrganizationCenter.js`
- `frontend/app/ceo-office/organization/organizationCenter.module.css`
- `frontend/lib/organizationProjection.js`
- `frontend/lib/runtimeApi.js` — one GET wrapper hunk only; prior mixed changes preserved
- `frontend/tests/organizationCenter.test.mjs`
- `issues/CURIS-V1-ORGANIZATION-CENTER-PRODUCTIZATION-001.md`
- this Review

No commit and no push were performed.

## Final Decision

**ORGANIZATION CENTER: IMPLEMENTED / ACCEPTED CANDIDATE**

CEO / ChatGPT final implementation acceptance remains the next gate.
