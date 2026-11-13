# WORKSPACE-ENGINEERING-MULTI-SURFACE-PACKAGE-001

Status: Review

Authority Class: CURRENT · IMPLEMENTATION ISSUE

Owner: Workspace Engineering / Package Track

Date: 2026-08-21

Source Contract: `docs/02_Architecture/CURIS_MULTI_SURFACE_WORKSPACE_PACKAGE_CONTRACT_CANDIDATE.md`

## Objective

Prove that a freshly built Curis can install a previously absent generic
`curis.workspace-package/v2` Package, compile Domain Navigation and at least three Professional
Surfaces, switch them under one canonical `workspace_id`, resolve real Core Responsibility /
Assignment / Employee / Capability truth fail-closed, consume shared Work / Result / Evidence
projections, recover navigation after restart, and preserve running Work and history through one
compatible Package version transition.

## Contract mapping

- Package declares Domain Navigation, Professional Surface metadata, Object Views, Responsibility
  and Capability requirements, bounded projection profiles and availability.
- Core owns route resolution, eligibility/default/gap truth, real Company OS identity and all Work /
  Execution / Result / Evidence state.
- Surface is never a Workspace, Team, Employee, Work, Cycle, Result, Session or Runtime entity.
- v1 `main/context/utility` remains the legacy pane contract and is not reinterpreted as v2.

## Scope

1. Version-dispatched v1/v2 validation with exact-field, finite-registry and digest coverage.
2. A compiled v2 model for Domain Navigation, Surface Registry, Object Views, requirements,
   projections and availability.
3. Core-owned resolution order: explicit deep link → per-user/workspace last active → Package
   default → first eligible required Surface → Workspace Gap.
4. Real Workspace-scoped Responsibility Assignment / Employee / Capability resolution with honest
   `RESPONSIBILITY_GAP`, `UNSTAFFED`, `CAPABILITY_GAP` and unknown-condition failure truth.
5. Read-only reuse of the existing shared Team / Employee / Work / Result / Evidence projection.
6. A finite generic renderer integrated into the existing four-pane Shell.
7. Compatible A→B update proof plus fail-closed removed-Surface impact detection.
8. Isolated backend/frontend/restart and fresh packaged Desktop build-before-Package evidence.

## v1 compatibility strategy

`curis.workspace-package/v1` continues through its exact existing validator, stored representation,
API projection, renderer and lifecycle paths. v2 is a distinct schema identifier and cannot be
silently treated as v1.

## v2 strategy

The accepted identifier is `curis.workspace-package/v2`. The existing Package row stores the exact
manifest, compiled Package model and domain schemas under the existing digest/version pin. No new
Surface table or Runtime entity is introduced.

## Business ownership

This Issue preserves the current installation boundary. The Package does not own Business identity.
The existing install command consumes the governed Business input used by the current substrate;
redesign of atomic Business + first Workspace creation is outside this Issue. If v2 cannot reuse
that boundary without creating a second Business, implementation stops.

## Running Work protection

- Package update continuity fingerprint must remain identical for Company OS entities, links, tasks,
  executions and artifacts.
- A running Work may carry immutable Operating Definition and Package/version provenance; an
  optional Surface origin is projection provenance only.
- Removed/changed Surface keys are rejected as requiring explicit migration. No historical entity
  or Package object is deleted.

## Exact Allowed Files

1. `issues/WORKSPACE-ENGINEERING-MULTI-SURFACE-PACKAGE-001.md`
2. `docs/02_Architecture/CURIS_MULTI_SURFACE_WORKSPACE_PACKAGE_CONTRACT_CANDIDATE.md`
3. `backend/app/workspace_package_runtime.py`
4. `frontend/components/workspace/InstalledWorkspaceRuntime.js`
5. `backend/tests/test_workspace_package_multi_surface_v2.py`
6. `frontend/tests/workspacePackageRuntime.test.mjs`
7. `docs/reviews/CURIS_MULTI_SURFACE_WORKSPACE_PACKAGE_IMPLEMENTATION_REVIEW.md`
8. `artifacts/workspace-engineering-multi-surface-package-001/` (evidence only)

No other file may be changed by this Issue. In particular: no Product/Frozen Authority, Shared /
Autonomous Runtime, Package API, database schema owner, RD, XHS, TTK, Prototype or active SQLite.

## Evidence and acceptance

- Repository-external isolated SQLite; all three DB environment variables resolve to the same file.
- v1 focused and P0/P0.5/P1/P1.5 regressions.
- v2 validator/resolver/projection/update/restart/cross-scope focused tests.
- Fresh Desktop build made before the generic v2 Package exists, followed by install, Domain
  Navigation, at least three same-ID Surface switches, honest unavailable gap, deep-link/last-active
  recovery and restart evidence.
- Before/after size, mtime, SHA-256 and integrity checks for `data/curis.sqlite` and
  `backend/data/curis.sqlite` must match exactly.

## Non-goals

RD/XHS/TTK migration; final Domain UI; arbitrary JS/Python/Shell/SQL; Workflow/DAG/Scheduler;
Marketplace/PKI; low-code builder; Sub-Workspace; Surface/Domain Runtime; cross-Surface autonomous
E2E; multiple same-Package instances; general update/migration engine.

## Git and stop gates

Preserve the dirty baseline. No broad add, reset, clean, staging, commit or push. Stop on any Contract
Stop Gate, active DB touch, Product Authority conflict or required file outside this allowlist.

## CEO decision and implementation return

CEO Decision on 2026-08-22: `ACCEPTED`.

Implementation, isolated tests, production build, packaged Runtime proof and the real Tauri Desktop
Gate are complete. The accepted proof includes three real Surface switches under one canonical
Workspace ID, explicit deep link, last-active recovery, full Desktop restart, fail-closed synthetic
Workspace Gap rendering and byte-identical active repository SQLite. No Surface Runtime, Workflow
Engine, RD/XHS migration, commit-time implementation or push is included.
