# Curis Multi-Surface Workspace Package Implementation Review

Status: Review

Authority Class: REVIEW · IMPLEMENTATION EVIDENCE

Disposition: IMPLEMENTED / CEO ACCEPTED

Verdict: ACCEPTED — implementation and required Runtime/Desktop evidence pass

Owner: Workspace Engineering / Package Track

Date: 2026-08-22

Next Gate: bounded commit reconciliation; no push

## A. Accepted Contract Mapping

Implemented `Curis Core + curis.workspace-package/v2`. Package declares navigation, Surface
metadata, views, requirements and bounded projections. Core owns identity, resolution and operating
truth. No Surface Runtime exists.

## B. Exact Allowed Files

Only the eight paths in the Issue allowlist were changed or created. No Package API, database owner,
Shared/Autonomous Runtime, RD, XHS, TTK, Product/Frozen Authority or Prototype file was changed.

## C. v1 Compatibility

v1 retains its exact validator, stored legacy `main/context/utility` shape and renderer. P0 through
P1.5 regressions passed. v1→v2 contract transition fails closed.

## D. v2 Contract

`curis.workspace-package/v2` is separately dispatched and exact-field validated. Package digest
covers manifest, schemas, Domain Navigation, Surface Registry, Object Views, Responsibility
Requirements and Projection Profiles. Arbitrary fields, code, routes, queries and conditions fail.

## E. Domain Navigation

Stable keys, labels, Surface refs, unique order, optional group and availability ref compile from the
Package. Package supplies no href; Core retains the canonical Workspace route.

## F. Surface Registry

Four generic Surfaces compile in A; compatible B adds one OPTIONAL Surface. Surface keys exist only
inside the version/digest-covered Package model and are never inserted into Core Runtime tables.

## G. Workspace Identity

Every Surface projection resolves under one
`workspace-package-73c081f0-5c2f-4773-ad86-d975d18c5c14`. No Surface creates Workspace, Team or
Business identity.

## H. Routing / Deep Link

The renderer derives `?surface=<stable-key>` under the canonical Workspace path. It does not accept
raw Package routes. A real Tauri Research selection produced `?surface=research`; WebView reload
returned to Research under the same canonical Workspace ID.

## I. Default / Last Active / Gap

Renderer implements explicit → per-user/workspace local last active → eligible Package default →
first eligible REQUIRED → Core Workspace Gap. The real Desktop first opened Overview, selected
Operations last, quit fully, restarted, then restored Operations when entering the same Workspace
from a no-query navigation link. All four proof Surfaces were AVAILABLE, so no unavailable UI state
was applicable; focused Runtime tests retain required/optional/conditional gap coverage.

## J. Availability

REQUIRED, OPTIONAL and CONDITIONAL are finite. `WORKSPACE_HAS_OBJECTS` is the only accepted v2
condition. Unknown conditions fail validation. Required gaps produce DRAFT; optional/conditional
gaps do not fabricate Operational truth.

## K. Responsibility Resolution

Package declares a responsibility key only. Core resolves exactly one real Workspace-scoped
`RESPONSIBILITY_ASSIGNMENT`, Role, Employee and binding. Missing Assignment is
`RESPONSIBILITY_GAP`; invalid/missing Employee is `UNSTAFFED`. Employee replacement changes the
resolution without changing Package digest.

## L. Capability Resolution

Package requirement is compared against a real Assignment binding, active authorization and current
Company supply review. Missing, stale, unauthorized or blocked supply is `CAPABILITY_GAP`.
`granted_capabilities` remains empty; requirement is never treated as grant.

## M. Object View Boundary

Object View keys and Surface keys are disjoint. Overview owns three views. Renderer supports only six
finite Core components; no low-code or arbitrary component runtime was added.

## N. Shared Projections

The existing `SharedWorkspaceProjection` supplies real Work, Result and Evidence. Package profiles
select only Core-known types and current Workspace scope; Package SQL/JS/filter expressions are
impossible.

## O. Team / Employee Work Area Reuse

The same shared projection supplies Team roles, Employees and Capability Bindings. No Team or
Employee UI/runtime was duplicated.

## P. Package Versioning

Navigation, Surface Registry, requirements, views and projections are stored in existing
version/digest pin truth. Compatible A→B permits labels, additive views and an OPTIONAL Surface.

## Q. Running Work Protection

Company OS continuity fingerprints cover entities, links, tasks, executions and artifacts. Running
Package Work holds immutable Package/schema Operating Definition origin. A→B left its exact JSON
SHA3 unchanged. Removed Surface keys fail closed and historical data is never deleted.

## R. Restart

Focused tests and the exact packaged Workspace sidecar recovered package registration, Workspace ID,
requirements, shared projections, object and Result/Evidence. A real Desktop process restart
recovered the same instance, canonical Workspace ID, `OPERATIONAL` Runtime response, dynamic
navigation, Context pane state and Operations last-active Surface.

## S. Generic Multi-Surface Renderer

The existing four-pane Shell now renders Package Domain Navigation in Context, selected Surface in
Main and finite detail/create mapping in Utility. v1 stays on its legacy renderer branch.

## T. Packaged Desktop Evidence

The prior failing Desktop proof was traced to a client first-render mismatch: the synthetic Core
`workspaceGap` has `eligible=true` but is not a Professional Surface and has no `viewRefs` or
`projectionRefs`. Before default-Surface state initialization, `MultiSurfaceMain` admitted that gap
and called `surface.projectionRefs.find`, producing the captured TypeError and global error boundary.
Route, v2 dispatch, API payload and old bundle provenance were all valid.

The bounded fix makes the generic renderer fail closed unless both Professional Surface arrays are
present. A new App was built before Package `com.curis.proof.render-path-fixed-office@0.1.0` existed.
After build, the Package was created, installed and operated in isolated SQLite. The real Tauri
Window showed `Render Fixed Office`, rendered Domain Navigation, switched Overview → Research →
Operations with one `workspace-package-102a6a2e-7c55-4d36-9f65-cb41f5aff600`, reloaded the explicit
Research deep link, and restored Operations after a full Desktop restart. Context, Main and Utility
all projected the same Package/Core truth. No Surface table or Runtime entity was created.

`PACKAGED DESKTOP UI PROOF = PASS`.

## U. Active DB Safety

All three test DB variables pointed to one repository-external database. Both repository SQLite
files match baseline size, mtime, SHA-256 and `integrity_check=ok` exactly.

## V. Regression

Backend P0/v1, P0.5, P1, P1.5, v2, shared projection and responsibility routing returned `15 passed`.
Focused frontend renderer returned `2 passed`; production build returned 45 routes; Python compile,
fresh Tauri build and `git diff --check` passed.

## W. Remaining Gaps

1. Multiple same-Package instances remains a documented current limitation.
2. Surface migration is intentionally unsupported; removal requires a future explicit Issue.
3. RD/XHS migration, cross-Surface autonomous E2E, Marketplace and general update/migration remain
   outside this Issue.

## X. Commit Decision

CEO authorized one exact-manifest bounded commit. Do not push and do not continue Package v2
development after the commit.

## Acceptance Questions

1. v1 continues readable: **Yes**.
2. v2 is a separate explicit contract: **Yes**.
3. Domain Navigation comes from Package: **Yes**.
4. Surface Registry exists: **Yes**.
5. Surface remains non-Runtime metadata: **Yes**.
6. At least three Surfaces switched: **Yes — Overview, Research, Operations in real Tauri**.
7. Three Surfaces keep one Workspace ID: **Yes**.
8. Surface route is Workspace-local state: **Yes; explicit Research deep link reloaded correctly**.
9. Package knows no Employee ID: **Yes**.
10. Core resolves Responsibility Requirement: **Yes**.
11. Missing Assignment/Employee fail closed: **Yes**.
12. Missing Capability fails closed: **Yes**.
13. REQUIRED/OPTIONAL/CONDITIONAL work: **Yes**.
14. default/last-active/fallback work: **Yes; default Overview and restart-restored Operations**.
15. Runtime does not force Surface jumps: **Yes**.
16. Object View is separate from Surface: **Yes**.
17. Work/Result/Evidence reuse Core truth: **Yes**.
18. Team/Employee Work Area is reused: **Yes**.
19. Running Work remains unchanged on update: **Yes**.
20. Surface deletion preserves history: **Yes; update is rejected before mutation**.
21. Restart recovers: **Yes — Runtime identity, navigation and last-active Surface**.
22. RD modified: **No**.
23. XHS modified: **No**.
24. Surface Runtime added: **No**.
25. Workflow Engine added: **No**.
26. Active DB completely unchanged: **Yes**.
27. Packaged Desktop proof fully passed: **Yes**.
28. True next step: **bounded commit reconciliation, then stop; no push**.

```text
MULTI-SURFACE PACKAGE V2 IMPLEMENTED = YES
PACKAGED RUNTIME PROOF = PASS
PACKAGED DESKTOP UI PROOF = PASS
THREE SURFACES REAL TAURI VERIFIED = YES
SAME WORKSPACE_ID / DEEP LINK / LAST-ACTIVE / RESTART = PASS
V1 REGRESSION = PASS
ACTIVE DB UNCHANGED = PASS
ISSUE CEO ACCEPTED = YES
STATUS = IMPLEMENTED / ACCEPTED
COMMIT = BOUNDED COMMIT AUTHORIZED
PUSH = NO
```
