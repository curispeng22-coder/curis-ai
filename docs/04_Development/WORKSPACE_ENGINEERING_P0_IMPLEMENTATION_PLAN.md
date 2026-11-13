# Workspace Engineering P0 Implementation Plan

**Status:** Review
**Plan State:** `P0 ACCEPTED`
**Execution State:** `IMPLEMENTED / ACCEPTED`
**Date:** 2026-08-16
**Scope:** P0 only; no P1/P2/Marketplace planning

## 0. Start gate

This start gate was satisfied by `issues/WORKSPACE-ENGINEERING-P0-001.md`, which froze the dirty input snapshot, Allowed Files, database boundary, evidence root and Review owner before implementation.

## 1. Phase 0 — Baseline and conflict lock

- Record the exact commit plus dirty/untracked input snapshot; do not treat the current filesystem as clean `main`.
- Identify ownership conflicts for Runtime Workspace, Runtime Foundation, API router, navigation/Shell, `WorkspacePaneShell`, `runtimeApi`, SQLite migration and Desktop packaging seams.
- Select an isolated worktree / branch and isolated HOME / SQLite evidence root.
- Capture the accepted no-regression commands and facts for XHS, RD Phase 0/1, shared Runtime scope/persistence and ADR-0046 Computer Access.
- This gate kept the Issue at `DRAFT / NOT STARTED` until the inputs were signed off; `WORKSPACE-ENGINEERING-P0-001` records the completed sign-off.

**Exit:** bounded Issue approved; Allowed Files and conflict window explicit. No production change before exit.

## 2. Phase 1 — Minimal package contract and validator

- Define only the P0 manifest fields: schema version, package ID/version, Core compatibility, navigation label/icon, Surface/schema refs and allowed action IDs.
- Define the local Semantic Model for `CustomerFeedback`: object, relationships, states, responsibility reference and truth/unknown rules.
- Validate JSON shape, declared files, action/component IDs, safe relative paths, file count/size limits, duplicate identity/version and Core compatibility.
- Compute immutable digest and import provenance; P0 local trust is controlled, not a general signature PKI.
- Leave one focused validator check covering valid package plus invalid path/action/schema/compatibility and atomic failure.

**Exit:** the sample Package validates; malformed input fails before any registry or file mutation.

## 3. Phase 2 — Package store and installed registry

- Add an atomic app-data Package Store and Installed Package Registry using existing SQLite migration governance.
- Persist install state, digest, import source, package/version, Core compatibility, install/disable timestamps and archived manifest/schema snapshot.
- Make install idempotent for the same digest/version and fail closed on conflicting content.
- Implement disable/uninstall metadata semantics without physical business-data deletion.
- Add restart recovery for Registry and Package Store consistency.

**Exit:** install/restart/disable/uninstall registry transitions are transactionally consistent in isolated SQLite.

## 4. Phase 3 — Generic domain object and safe action

- Reuse existing Runtime Foundation scope/link/audit semantics; add one generic package-domain-object representation only where current registered types cannot express P0.
- Persist `package_id`, pinned version, workspace/company/tenant scope, object type/schema version, lifecycle status, owner ref, validated data and timestamps.
- Add a finite Safe Action Registry with only `core.domain-object.create` for P0; reads use a scoped projection.
- Validate Package Domain Schema and scope on every write/read; unknown action/type/state fails closed.
- Link Activity / Result references through existing Core primitives; do not create a second Evidence or Decision system.

**Exit:** one real `CustomerFeedback` and activity survive restart; cross-scope, invalid schema and unknown action fail closed.

## 5. Phase 4 — Dynamic navigation and declarative renderer

- Project installed/enabled Registry entries into the existing “业务空间” navigation group; preserve the six fixed primary areas and existing compiled RD / XHS / TTK routes.
- Add one generic installed-package route/host; Package identity remains data, not a generated source route.
- Reuse `WorkspacePaneShell`; implement only the finite P0 component set needed for object list, selected-object detail/form and activity/provenance.
- Bind Main / Context / Utility to scoped projections; no HTML, JS, Python, shell or raw endpoint from Package.
- Keep the renderer opt-in for installed Package instances so accepted XHS/RD components remain untouched.

**Exit:** installing the Package causes navigation and all three Surfaces to appear without rebuild; disabling/uninstalling removes navigation without changing compiled routes.

## 6. Phase 5 — Template to instance materialization

- Materialize a Company-scoped Workspace Instance from the installed Package and pin its exact package version/digest.
- Keep Company/Workspace identity, strategy, employee assignments, credentials, private Knowledge and business data outside Package files.
- Require existing Capability Registry truth for declared requirements; the P0 sample declares none.
- If an owner is assigned, resolve an existing Employee reference; otherwise show unassigned. Never fabricate Employee Presence.

**Exit:** the instance can open, create/read feedback and explain its package/version provenance.

## 7. Phase 6 — Desktop acceptance and uninstall proof

- Build Curis once before introducing the sample Package; prove the build/source contains no sample package ID, workspace type or label.
- Launch the installed app with isolated HOME, then import the Package externally through the Core install boundary.
- Capture install → navigation → open → Main/Context/Utility → create feedback → restart → same records → uninstall → navigation gone → archived data retained.
- Verify active Package files are removed when unreferenced, while business data and archived manifest/schema/provenance remain.
- Run focused XHS, RD Phase 0/1, shared Runtime, Computer Access, frontend build and packaged Desktop cleanup checks defined by the future Issue.
- Record exact source/build/package digests, database path, object IDs, screenshots, logs, integrity result and no-regression result in the formal Review.

**Exit:** every Acceptance item in the P0 Definition passes. Any source edit/rebuild after sample introduction invalidates the PoC and requires a fresh acceptance run.

## 8. Stop condition

After P0 Review, stop. Do not start Package update/migration, arbitrary extensions, export/signing PKI, Marketplace, XHS/RD migration or Workspace Engineering product/UX work without a new approved definition and bounded Issue.

```text
WORKSPACE ENGINEERING P0 ACCEPTED
IMPLEMENTED / ACCEPTED
```

## 9. Execution record

The bounded Issue completed all phases. The formal acceptance record is `reviews/WORKSPACE-ENGINEERING-P0-001_review.md`; packaged Desktop evidence is under `docs/reviews/workspace-engineering-p0-2026-08-16/`.

The active SQLite guard incident was repaired only within the explicit owner authorization. Every non-target schema/data fingerprint remained identical, the four empty accidental Package tables were removed, and final regression used explicit isolated DB environment truth. The original active-database byte hash was not restored and is not claimed as restored.
