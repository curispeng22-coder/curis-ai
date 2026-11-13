# CURIS-VISUAL-BASELINE-REAL-PRODUCT-INTEGRATION-001

Status: AUDITED / IMPLEMENTATION BLOCKED
Authority Class: CURRENT

## Goal

Reconcile the Frozen product and visual path

`Company -> Department -> Business -> Workspace -> Employee Work Area`

against the current frontend, API, persistence and accepted Runtime without redesigning the product, copying prototype fixtures, or creating another Runtime.

## Authority

- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`
- `docs/01_Product/Curis_Product_Blueprint.html`
- `docs/01_Product/Curis_Product_Master_Map.md`
- `docs/01_Product/Curis_Product_UI_Blueprint.html`
- `docs/03_Design/Curis_Company_OS_Shared_Authority.md`
- `docs/03_Design/Curis_Workspace_Shell_Contract_And_Shared_Patterns.md`
- Accepted Runtime record: `docs/reviews/CURIS_TEAM_OPERATING_REAL_EMPLOYEE_E2E_REVIEW.md`

## Preserved baseline

- HEAD: `d3ab0ce46d3a0ebbe13b7748b6722ac0c4bf264a`
- Worktree: preserved mixed-source, with extensive tracked and untracked changes owned by other initiatives.
- Staged files at takeover: none.
- Active SQLite files were read-only fingerprinted before and after audit tests.

Important UI integration files are not present in HEAD and remain untracked in the preserved worktree, including the current Business, Workspace Portal, Studio, XHS route, RD route and RD professional workspace files. They are evidence of current local implementation, not a clean-checkout delivery baseline.

## Current implementation truth

### Real and reusable

- Four-pane `WorkspacePaneShell`, pointer resize, local pane headers, utility maximize and local pane preferences.
- XHS content objects, versions, responsibility, handoff, decision packet, scheduling and truthful publishing/analytics boundary.
- RD Project/Cycle execution, responsibility, real Codex execution, Artifact, Evidence, Result Reference and persistence.
- Workspace-scoped Team Operating definition, immutable version, Assignment/Employee binding and accepted real Employee execution loop.
- Shared Workspace projection, canonical Employee identity bridge, callback trust and result provenance.
- Declarative installed Workspace package renderer and package lifecycle substrate within its accepted bounds.

### Partial or prototype-facing

- Business page is a Workspace-card list; it is not a persisted Business Definition, Operating Summary, Workspace Directory and Business Team surface.
- Workspace routes use query-string `workspace_id` and do not preserve a navigable Department/Business parent path.
- Company-wide Search renders an honest “正在接入” empty state and performs no real object query.
- Shared Employee Work Area exists but is not the common mounted surface for XHS and RD.
- Team Operating editor is mounted in XHS only; RD and Generic are not reconciled to the same product surface.
- Current Operating is assembled differently by domain and has no shared Workspace/Business operating projection contract.

### Missing or conflicting legacy

- No authoritative Business persistence relation to Company and Department.
- `business_directions` has `tenant_id` but no `company_id` or `department_id`.
- `workspaces.business_id` is an unchecked string reference and has no foreign key.
- Workspace creation accepts an unknown `business_ref`.
- No atomic `Department + Business + first Workspace + Leader Assignment` create path.
- Multiple legacy Department/Project/Office/Workspace paths remain; selecting one as canonical requires an Authority/Schema decision.
- Legacy CEO Day can create and operate `business_directions` and workspaces outside the Frozen hierarchy.

## Gap priorities

### P0 — product path cannot be truthfully completed

1. **Canonical Business identity and ownership relation**
   - Need: one authoritative Business record bound to one Company and one Department.
   - Current: no such constrained relation; legacy `business_directions` is tenant-only.
   - Stop reason: identity/reference contract and migration authority are unclear.

2. **Atomic first-Business creation**
   - Need: Department -> Business -> first Workspace -> Leader Assignment, atomically or rollback-safe.
   - Current: separate APIs and free-form references; partial creation is possible.
   - Depends on P0-1.

3. **Clean recoverable frontend integration baseline**
   - Need: Business, Portal, Studio, XHS and RD route registrations available from clean checkout.
   - Current: key routes/components are untracked mixed-source files.
   - Stop reason: ownership is not sufficiently attributable for safe broad staging or commit.

4. **Canonical hierarchy routes and parent path**
   - Need: Department page -> Business page -> Workspace page, refresh-safe and direct-link safe.
   - Current: `/ceo-office/business` lists Workspaces; professional pages take `?workspace_id=` and cannot derive a valid Department/Business path.
   - Depends on P0-1 and P0-3.

### P1 — Runtime works but product integration is incomplete

1. Business Definition / Operating Summary / Workspace Directory / Business Team projection and UI.
2. Shared Current Operating projection from Work, Result, Evidence and Need/Decision facts.
3. Mount Shared Employee Work Area consistently without replacing domain surfaces.
4. Mount Team Operating against RD and Generic while keeping arrows as Default Flow, not a DAG.
5. Real company-wide object search.
6. User-language layering for remaining Runtime IDs and technical state labels.
7. Generic-to-professional package upgrade preserving Workspace identity and instance data.

### P2 — visual and optional closure

1. Detail drawers for owner, goal, rules and configuration.
2. Cross-surface visual polish after hierarchy truth is implemented.
3. Additional aggregate Business indicators derived from accepted facts.

## Allowed files for this audit

- `issues/CURIS-VISUAL-BASELINE-REAL-PRODUCT-INTEGRATION-001.md`
- `docs/reviews/CURIS_VISUAL_BASELINE_REAL_PRODUCT_IMPLEMENTATION_REVIEW.md`

No implementation file is allowed until P0-1 receives an explicit Authority/Schema decision and P0-3 receives an ownership-safe baseline.

## Explicit exclusions

- No Product or Frozen Authority edits.
- No active database writes or migration.
- No new Workflow engine, Business Runtime, Employee system or Workspace identity.
- No prototype fixture or mocked E2E.
- No reset, clean, removal of untracked files, broad staging, commit or push.

## Acceptance required to reopen implementation

1. Freeze the canonical Business identity and its Company/Department constraints.
2. Define migration/coexistence handling for legacy `business_directions`, Project and Office/Workspace semantics.
3. Assign ownership for the untracked frontend integration files or promote a clean committed baseline containing them.
4. Then implement the smallest transaction and route adapter over existing Runtime primitives.

## Audit verdict

`PARTIAL — CLEAR REMAINING GAPS`

The accepted Workspace and Team Operating Runtime is real. The Frozen Company -> Department -> Business -> Workspace product path is not yet a truthful end-to-end implementation.
