# CURIS FRONTEND BASELINE PROVENANCE RECONCILIATION

Authority Class: REVIEW
Status: Review
Date: 2026-08-20
Issue: CURIS CANONICAL BUSINESS SPINE — PHASE 6A
Disposition: PROVENANCE RECONCILED BY SEMANTIC OWNERSHIP; CONTROLLED TARGET BASELINE RECONSTRUCTED; NOT STAGED OR COMMITTED

## 1. Scope and safeguards

This review covers only:

- `frontend/app/ceo-office/business/page.js`
- `frontend/app/ceo-office/workspace/page.js`
- `frontend/components/runtime/WorkspaceRuntimeView.js`

The exact pre-reconstruction working candidates were preserved as Git objects before editing:

| File | Candidate Git object |
|---|---|
| Business page | `f4375550e6fb574640b198b48e571fcbc9882f1b` |
| Workspace page | `6cabe75086349e1bc52b749fdb0c69e4875e56d2` |
| WorkspaceRuntimeView | `730fcbea60320e1d88e328518eb1cb03b6125d0e` |

No reset, clean, checkout, backend change, active-database write, bulk add, staging, commit, or push occurred. The current candidates remain recoverable from those objects.

## 2. Accepted authority consumed

- Current Product Blueprint and Master Map: Business is Definition + Operating Summary + Workspace Directory + Business Team.
- Canonical Business Spine Authority and accepted Phase 1–5 Runtime/API truth.
- Shared Workspace shell/entry truth and canonical Parent Resolver.
- Accepted XHS and RD domain routes/components; their business semantics were not modified.
- Accepted Team Operating, Assignment/Leader, Decision, Result Reference, and current tracked `runtimeApi` contracts.
- Workspace Package Runtime accepted lifecycle and generic installed-workspace route.

Visual references were used only for product structure. No Prototype or Visual HTML/JS/CSS was promoted.

## 3. Semantic ownership matrix

### 3.1 Business page

- BASE commits: `96cc3406645de69757f63190886ebe99933188a8` and `b7403bed68e44b466be2c7eedea4b5cda6e2db3d` (identical file blob).
- BASE blob: `64b1e50c3239d42406d0e266aaa334e7051465d6`.
- CANDIDATE object: `f4375550e6fb574640b198b48e571fcbc9882f1b`.
- TARGET blob: `fb0c53954f63f19a47d88c380576007340d95c9f`.
- TARGET SHA-256: `76a765b783e5fc155383700e01d1e3372ddaa386ba8d397c0ebe69693cee10da`.
- Final owner: Canonical Business Spine Integration.

KEEP:

- Existing Terra shell, page-state components, and canonical navigation style.

DROP:

- Project-as-Business projection.
- Business-embedded Workspace detail, simulation, health, workflow, goal/rules, and employee workstation surfaces.
- Free-form relation inference and legacy project/workspace substitution.

REBUILD:

- The four accepted blocks only: Business Definition, Operating Summary, canonical Workspace Directory, Business Team.
- Canonical Business list/read projection and explicit Business switching.

UNKNOWN / unresolved required blocks: none.

### 3.2 Workspace page

- BASE commits: `96cc3406645de69757f63190886ebe99933188a8` and `b7403bed68e44b466be2c7eedea4b5cda6e2db3d` (identical file blob).
- BASE blob: `4ae55749a8483ee47e1cad5c80e17d55cd084817`.
- CANDIDATE object: `6cabe75086349e1bc52b749fdb0c69e4875e56d2`.
- TARGET blob: `febeaabcec490905ab52e878a37754a8098ea726`.
- TARGET SHA-256: `f0f4ec1cc3513cde1ffc9672db9d36895da9d2f7a2eee74ecadd6e4a992bc627`.
- Final owner: Canonical Workspace Entry Integration.

KEEP:

- Existing Terra shell, shared route helpers, and honest loading/error/empty states.

DROP:

- Template/simulation/health portal aggregation.
- Hard-coded parent labels, prototype state, and domain work surfaces embedded in the entry page.

REBUILD:

- No-ID directory derived only from canonical Business relations.
- ID route resolving Workspace and canonical Company / Department / Business parent path.
- Explicit dispatch to existing RD, XHS, TTK compatibility, or installed-package routes.

UNKNOWN / unresolved required blocks: none.

### 3.3 WorkspaceRuntimeView

- BASE commit: `b7403bed68e44b466be2c7eedea4b5cda6e2db3d`.
- BASE blob: `fd023ab556527b0ad8b7de6db0a025996573cf43` (`96cc34066` older blob: `e78d018d5e92b497dfdc6f7b4ac30f83b3a9d8b2`).
- CANDIDATE object: `730fcbea60320e1d88e328518eb1cb03b6125d0e`.
- TARGET blob: `04b58058169d3e7da86c79e499a9985a9719900b`.
- TARGET SHA-256: `d3c8dda16eccdf4fd1954fd78ae7d9a6daec45df38732b1d233fbba17312f890`.
- Final owner: Main Integration compatibility seam; future TTK professional domain remains TTK-owned.

KEEP:

- Canonical Workspace identity read, Parent Resolver read, shared shell entry, and honest state boundary.

DROP:

- Mixed RD/XHS/TTK domain business logic, content/cycle composers, simulation control, and operating-detail mega-view behavior.
- Any shared-file inference that a TTK workspace is already an accepted professional instance.

REBUILD:

- Minimal TTK compatibility entry that resolves canonical identity and states that the professional TTK instance is not yet accepted.
- RD and XHS remain owned by their already accepted dedicated route/components.

UNKNOWN / unresolved required blocks: none. The missing TTK professional instance is an explicit implementation gap, not a required Shared semantic block.

## 4. Controlled API seam

`frontend/lib/runtimeApi.js` received only the minimal accepted wiring:

- canonical Business list/read;
- canonical Workspace Parent Resolver;
- installed Package Workspace route mapping.

No new frontend data model or parallel relation store was introduced.

## 5. Verification

- Focused frontend test: `frontend/tests/runtimeWorkspaceUi.test.mjs` — 8 passed, 0 failed.
- Focused ESLint for the three TARGET files, `runtimeApi.js`, and the focused test — PASS.
- Production build with isolated Browser API base — PASS; 45 routes generated.
- Browser, isolated SQLite:
  - canonical Business four-block projection — PASS;
  - one Business with two Workspaces — PASS;
  - canonical Parent Resolver path Company / Department / Business / Workspace — PASS;
  - generic installed Package creates a separate canonical Business and first Workspace — PASS;
  - generic Workspace dispatches to the installed declarative work surface — PASS.
- Stop/restart on the same isolated SQLite: RD two-Workspace Business, generic one-Workspace Business, and resolved generic Parent Path were re-read through the API; `integrity_check=ok` — PASS.
- A browser tab kept across repeated local server restarts produced intermittent cross-origin `Failed to fetch`; a fresh tab against the production build on the default 3000/8000 topology passed the same canonical Workspace and installed-package routes. Bootstrap simulation reads were also serialized to avoid one unresolved parallel preflight holding the entire Runtime snapshot.
- Packaged Desktop was not run in this Phase 6A scope and remains a Phase 6B acceptance item.

## 6. Promotion and next gate

All three TARGETs now have explicit semantic ownership and no unknown Current-required block. They are intentionally not staged or committed because this task forbids whole-file promotion and bulk add. Consequently, a clean checkout still does not recover these three untracked TARGET files until a separately authorized controlled promotion/commit gate records them.

Phase 6A result:

`CURIS FRONTEND BASELINE — PROVENANCE RECONCILED BY SEMANTIC OWNERSHIP — CONTROLLED TARGET BASELINE RECONSTRUCTED — NO WHOLE-FILE PROMOTION — READY FOR PHASE 6B / PHASE 7`
