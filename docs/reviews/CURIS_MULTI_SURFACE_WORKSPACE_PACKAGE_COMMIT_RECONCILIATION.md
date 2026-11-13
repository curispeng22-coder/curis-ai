# Curis Multi-Surface Workspace Package Commit Reconciliation

Status: Review

Authority Class: REVIEW · COMMIT EVIDENCE

Disposition: CEO ACCEPTED / BOUNDED COMMIT AUTHORIZED

Owner: Workspace Engineering / Package Track

Date: 2026-08-22

Baseline HEAD: `923d2ea3a7ed88d3daf5a41209137149a64005be`

## 1. Exact accepted file manifest

| # | Path | Ownership |
|---:|---|---|
| 1 | `backend/app/workspace_package_runtime.py` | v2 validation, compilation, Core resolution, projections and compatible update boundary |
| 2 | `frontend/components/workspace/InstalledWorkspaceRuntime.js` | finite generic multi-Surface renderer and fail-closed Workspace Gap guard |
| 3 | `backend/tests/test_workspace_package_multi_surface_v2.py` | v1 compatibility plus v2 resolver/projection/update/restart/failure regression |
| 4 | `frontend/tests/workspacePackageRuntime.test.mjs` | generic renderer, route, same-ID and real packaged gap regression |
| 5 | `issues/WORKSPACE-ENGINEERING-MULTI-SURFACE-PACKAGE-001.md` | accepted bounded Issue |
| 6 | `docs/02_Architecture/CURIS_MULTI_SURFACE_WORKSPACE_PACKAGE_CONTRACT_CANDIDATE.md` | accepted v2 contract baseline |
| 7 | `docs/reviews/CURIS_MULTI_SURFACE_WORKSPACE_PACKAGE_IMPLEMENTATION_REVIEW.md` | accepted implementation and Desktop evidence review |
| 8 | `docs/reviews/CURIS_MULTI_SURFACE_WORKSPACE_PACKAGE_COMMIT_RECONCILIATION.md` | this exact commit record |
| 9 | `artifacts/workspace-engineering-multi-surface-package-001/README.md` | evidence index and final acceptance matrix |
| 10 | `artifacts/workspace-engineering-multi-surface-package-001/ROOT_CAUSE_AND_BOUNDED_FIX.md` | Desktop failure root cause and exact bounded guard |
| 11 | `artifacts/workspace-engineering-multi-surface-package-001/packaged-workspace-api-response.json` | captured failing packaged payload used by the renderer regression |

The manifest contains exactly 11 files. Raw screenshots, successful-response copies and HTTP headers
remain preserved untracked evidence and are not required by the clean source/test closure. No
unrelated Product, Shared Runtime, RD, XHS, TTK, TRAE, generated build or active database path is
included.

## 2. Verification

All backend tests used one repository-external SQLite through identical `CURIS_DB`,
`CURIS_DB_PATH` and `CURIS_WORKSPACE_DB` values.

- Package P0/v1, P0.5, P1, P1.5, v2, Shared Projection and Responsibility Routing: `15 passed`
- focused frontend Package renderer: `2 passed`
- Python compile: passed
- isolated SQLite: `integrity_check=ok`; `foreign_key_check` returned no rows
- source and documentation whitespace/diff checks: passed

## 3. Active SQLite guard

| Path | size | mtime | SHA-256 | integrity |
|---|---:|---:|---|---|
| `data/curis.sqlite` | `1232896` | `1786873339` | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | `ok` |
| `backend/data/curis.sqlite` | `1277952` | `1786783659` | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | `ok` |

These values match the accepted Issue baseline exactly. Integrity reads did not mutate either file.

## 4. Commit boundary

Planned message: `feat(workspace): establish multi-surface package runtime`

Only the exact manifest above may be staged. The staged path list, file count, staged diff, generated
tree and active DB fingerprints must be checked immediately before commit. After commit, the real
index must contain zero staged changes. Existing unrelated dirty and untracked work remains in place.

Push is prohibited. No new Package v2 implementation follows this reconciliation.
