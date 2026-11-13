# CURIS FRONTEND BASELINE CLOSURE REVIEW

Authority Class: REVIEW
Status: Review
Disposition: FRONTEND DEPENDENCY BASELINE READY — CONTROLLED TARGET TREE VERIFIED — NOT STAGED OR COMMITTED
Date: 2026-08-20
Owner: Frontend Baseline Closure / Business Spine Main Developer
Next Action: regenerate the exact promotion manifest from the target objects below, then run Packaged Desktop and Phase 7 final E2E
Target Authority: `docs/reviews/CURIS_CANONICAL_BUSINESS_SPINE_IMPLEMENTATION_001_REVIEW.md` final acceptance record
Next Gate: controlled scoped commit after clean checkout, Packaged Desktop and Phase 7 pass

## A. Missing dependency root cause

The previously exported Business Spine promotion tree
`d1c8eb9f7b455f36c1425fe41b8e1c6e201c6ef0` contained the reconstructed Business page,
Workspace entry, `WorkspaceRuntimeView`, Runtime API seam and backend spine, but not the
shared provider/state source imported by the tracked root layout and accepted routes.

The same tree also retained older tracked copies of the Assistant/provider chain and omitted
the untracked accepted RD, XHS, TTK compatibility and Studio routes. The dirty worktree hid
that incomplete source closure. This was a source-baseline provenance failure, not a backend,
schema, database or Product Contract failure.

No whole directory is required. The verified delta from the previous exported tree is 14
frontend paths: 13 source files and one focused test.

## B. Semantic ownership matrix

`BASE` below means the known sibling snapshot `b7403bed68e44b466be2c7eedea4b5cda6e2db3d`
when a blob exists. `CANDIDATE/TARGET` is the preserved current-worktree Git object. The
TARGET equals the candidate because the semantic audit found no mixed domain block in the
shared files and the domain files already have accepted ownership.

| File | Importer / why required | Git state | BASE blob | TARGET object / SHA-256 | Current-required | Semantic owner | Action |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `frontend/components/runtime/RuntimeProvider.js` | root layout and accepted Company OS routes; one shared bootstrap/context boundary | untracked | `a6aa8071...` | `ecab841e...` / `e6cd6c56...` | yes | Shared Frontend Runtime | PROMOTE |
| `frontend/components/runtime/RuntimeStates.js` | Business, Workspace, RD/XHS/TTK and Studio honest loading/error/empty states | untracked | `e1beb671...` | `acafdc89...` / `833f0213...` | yes | Shared Frontend Runtime | PROMOTE |
| `frontend/app/layout.js` | establishes `RuntimeProvider → GlobalAssistantProvider` ordering | modified tracked | `369f3b1e...` | `81954987...` / `96ed21fd...` | yes | Shared App Shell | PROMOTE |
| `frontend/components/assistant/GlobalAssistant.js` | Terra shell and RD/XHS page-context seam; Runtime-backed overlay | modified tracked | `c492a34a...` | `17d95fe4...` / `4031ae48...` | yes | Shared Assistant | PROMOTE |
| `frontend/lib/assistantState.mjs` | Assistant Workspace context keys including `workspace_id` / `business_type` | modified tracked | `a646a79b...` | `2e65b7e8...` / `baa07ce5...` | yes | Shared Assistant | PROMOTE |
| `frontend/components/terra/TerraShell.js` | shared shell/Assistant seam and accepted three-theme control | modified tracked | `305c4911...` | `6e77227b...` / `708e68b8...` | yes | Shared App Shell | PROMOTE |
| `frontend/app/ceo-office/page.js` | current Runtime-backed workforce projection consumed by Assistant regression | modified tracked | `b805bdb9...` | `8b07ad2b...` / `3f16dfe3...` | yes | CEO Workforce accepted UI | PROMOTE |
| `frontend/app/ceo-office/workspace/software/page.js` | canonical RD dispatch | untracked | `ef20bed1...` | `bcaccac8...` / `ee675aed...` | yes | RD Workspace | PROMOTE |
| `frontend/components/rd/RdWorkspacePhaseTwo.js` | direct accepted RD professional surface | untracked | none | `2eca7026...` / `b2365020...` | yes | RD Workspace | PROMOTE |
| `frontend/components/rd/RdRealExecutionComposer.js` | direct RD component import; accepted real execution seam | untracked | none | `400084dd...` / `bf0c1ce5...` | yes | RD Workspace | PROMOTE |
| `frontend/app/ceo-office/workspace/xhs/page.js` | canonical XHS dispatch | untracked | `313b6b55...` | `314161a8...` / `49cd1afa...` | yes | XHS Workspace | PROMOTE |
| `frontend/app/ceo-office/workspace/shortvideo/page.js` | honest TTK compatibility dispatch used by canonical Workspace routing | untracked | `2baf22ff...` | `2baf22ff...` / `9d998dce...` | yes | Main Integration compatibility seam | PROMOTE |
| `frontend/app/ceo-office/workspace/studio/page.js` | accepted Workspace route; Blueprint Draft only | untracked | `91bb8782...` | `67eeaa07...` / `346316e6...` | yes | Workspace Studio | PROMOTE |
| `frontend/tests/runtimeProvider.test.mjs` | clean-tree provider/state/Assistant/layout regression | untracked | `e2ebd627...` | `0b9af7db...` / `8729c725...` | validation | Frontend Baseline Closure | PROMOTE |

Known source/authority for the two RD files without a tracked BASE is
`issues/RD-WORKSPACE-INSTANCE-001.md`, `reviews/RD-WORKSPACE-INSTANCE-001_review.md`,
`issues/RD-PHASE-2B-E2E-CLOSURE-001.md` and
`reviews/RD-PHASE-2B-E2E-CLOSURE-001_review.md`. Those accepted records define the
professional RD route, real execution composer and boundary; no historical line authorship
was inferred.

## C. RuntimeProvider decision

TARGET owns only:

- the root shared React context;
- route-bounded Runtime bootstrap;
- shared `idle / loading / ready / empty / forbidden / error` projection;
- Company ID, snapshot, simulations and refresh seam.

It contains no RD, XHS, Studio, prototype, Simulation scenario or domain dispatch logic.
The sibling BASE contains additional local-profile/company-selection behavior not consumed
by the accepted current Runtime API target. It was not copied into this closure because doing
so would expand the shared provider contract beyond the verified current route requirement.

Decision: `PROMOTE CURRENT MINIMAL SHARED TARGET`.

## D. RuntimeStates decision

TARGET is shared UI/runtime vocabulary only: loading, safe error/forbidden and empty. It
contains no domain state machine, Operating Lifecycle enum, prototype visual state or legacy
Workflow state.

The BASE-only `Waiting`, `Unknown` and `Conflict` components have no importer in the verified
current dependency graph and were not restored speculatively.

Decision: `PROMOTE CURRENT MINIMAL SHARED TARGET`.

## E. RD dependency closure

```text
canonical Workspace entry
→ /ceo-office/workspace/software
→ RdWorkspacePhaseTwo
→ tracked RdArtifactReview / RdDecisionPackage / RdResponsibilityHandoff
→ RdRealExecutionComposer
→ tracked WorkspacePaneShell + Runtime/API seams
```

Only the route and two missing direct RD components require promotion. The other RD/shared
imports are already tracked in the previous controlled tree. No RD directory promotion,
product behavior change or Autonomous Operating code is included.

## F. XHS dependency closure

```text
canonical Workspace entry
→ /ceo-office/workspace/xhs
→ tracked XhsWorkspacePhaseOne
→ tracked WorkspacePaneShell / TeamOperatingDefinitionEditor
→ tracked Runtime/API seams
```

Only the route requires promotion. The accepted XHS component is already tracked. No old
six-tab structure, Business-embedded Workspace or analytics claim is restored.

## G. Studio / Assistant decision

- Studio is a directly accepted route, not an accidental barrel export. Its semantic owner is
  `WORKSPACE-STUDIO-BLUEPRINT-ASSEMBLY-001` plus the accepted staffing proposal Runtime record.
  It persists a Blueprint Draft and keeps Simulation / approval / operation gates closed.
- Assistant is a root overlay dependency shared by Terra shell and RD/XHS context. The minimum
  clean closure is `layout.js`, `GlobalAssistant.js`, `assistantState.mjs`, `TerraShell.js` and
  the Runtime-backed CEO workforce projection. It is not a third column and does not bypass
  Workspace confirmation to create Tasks.
- No other Studio, Assistant, Terra or navigation file is required.

## H. BASE → CANDIDATE → TARGET evidence

All current candidates were preserved with `git hash-object -w` before repository edits. The
object IDs in section B are recoverable from the object database. For files with a BASE:

```text
b7403bed6 tracked blob
→ preserved current worktree candidate object
→ identical controlled TARGET object
```

For `RdWorkspacePhaseTwo.js` and `RdRealExecutionComposer.js`:

```text
no tracked BASE
→ accepted Issue/Review semantic contract + preserved candidate object
→ identical controlled TARGET object
```

No candidate was deleted, overwritten, reset or checked out.

## I. Exact Allowed Files

Source promotion candidate:

```text
frontend/app/ceo-office/page.js
frontend/app/ceo-office/workspace/shortvideo/page.js
frontend/app/ceo-office/workspace/software/page.js
frontend/app/ceo-office/workspace/studio/page.js
frontend/app/ceo-office/workspace/xhs/page.js
frontend/app/layout.js
frontend/components/assistant/GlobalAssistant.js
frontend/components/rd/RdRealExecutionComposer.js
frontend/components/rd/RdWorkspacePhaseTwo.js
frontend/components/runtime/RuntimeProvider.js
frontend/components/runtime/RuntimeStates.js
frontend/components/terra/TerraShell.js
frontend/lib/assistantState.mjs
frontend/tests/runtimeProvider.test.mjs
docs/reviews/CURIS_FRONTEND_BASELINE_CLOSURE_REVIEW.md
```

The Business Spine files already present in tree `d1c8eb9...` and existing tracked helpers
remain prerequisites, not new closure promotions. No backend, schema, database, Product Truth,
prototype or visual-design file is in this delta.

## J. Clean build evidence

Current preserved worktree:

- focused Runtime API + Workspace UI: `19 passed`;
- focused Provider / States / Assistant / Layout: `3 passed`;
- scoped ESLint: exit 0, 0 errors, 3 pre-existing RD Hook dependency warnings;
- Next production build: PASS, 45 routes.

Controlled exported source tree:

- previous Business Spine tree: `d1c8eb9f7b455f36c1425fe41b8e1c6e201c6ef0`;
- verified frontend target tree before adding this review:
  `e9f200b1d24486f57c1de6e531907195e04ab1ea`;
- export root: `/tmp/curis-frontend-baseline-closure.9ChK35/export-v3`;
- focused Runtime API + Workspace UI: `19 passed`;
- focused Provider / States / Assistant / Layout: `3 passed`;
- scoped ESLint: exit 0, 0 errors, the same 3 RD Hook warnings;
- clean source production build: PASS with Next webpack, 42 routes;
- required generated routes include Business, Workspace, RD software, XHS, TTK shortvideo,
  Studio and generic `installed/[workspaceId]`.

The first exported build attempt used an external `node_modules` symlink. Turbopack rejected
that dependency layout because the symlink pointed outside the export root. This was isolated
dependency-materialization noise; the same exported source tree built successfully with the
installed Next webpack builder.

The real index fingerprint before and after isolated-index construction remained:
`e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.
Nothing was staged in the user's index.

## K. Remaining unknown blocks

No Current-required source or semantic ownership block remains unknown for this closure.

Known non-blocking items outside scope:

- the unfiltered `runtimeProvider.test.mjs` suite has two current-worktree assertion mismatches:
  CEO Desk copy expects `能力引用` while current code says `运行引用`, and navigation expects four
  persistent labels while current code contains five. These are existing product copy/navigation
  questions and were not changed by the dependency closure;
- `RdWorkspacePhaseTwo.js` emits three existing `react-hooks/exhaustive-deps` warnings, with no
  ESLint error;
- Packaged Desktop and final Phase 7 E2E were not run because this closure hands the verified
  frontend baseline back to the Business Spine main developer for those final gates.

## L. Recommended handoff to Business Spine main developer

`Frontend dependency baseline ready.`

The main developer now only needs to:

1. regenerate the exact promotion manifest using the target objects in section B;
2. export a clean checkout/tree;
3. run the production build;
4. build and verify Packaged Desktop;
5. run Phase 7 final E2E;
6. create the scoped commit.

No frontend provenance research, Business Spine backend redesign, schema change or Product
Contract change is required.
