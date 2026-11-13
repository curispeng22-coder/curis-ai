---
issue: "082"
title: "Workspace Department Activation Boundary Gate"
status: "done"
owner: "产品规划席"
date: "2026-07-08"
depends_on: "issues/081_workspace_department_catalog_local_demo_evidence_gate.md"
---

# Workspace Department Activation Boundary Gate

## Objective

Decide whether to approve architecture/product boundary definition for the next bounded Workspace Company Foundation step: tenant-local department activation planning.

## Minimal Context

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `knowledge/CURRENT_CONTEXT.md`
- `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md`
- `issues/081_workspace_department_catalog_local_demo_evidence_gate.md`
- `reviews/078_workspace_department_catalog_local_demo_evidence_review.md`

## Product Context

Curis Workspace now has a verified company frame and a verified read-only official department catalog summary. The next product step should move toward a configurable AI Company System by defining how a CEO may later activate a small set of tenant-local departments, without implementing department CRUD, employees, staffing, routing, or business modules in this gate.

This gate is boundary-only. It should decide whether 系统交付席 may define the architecture boundary for a future minimal activation slice.

## Product Recommendation

Recommended next phase: approve Option A, boundary definition only for tenant-local department activation.

Rationale:

- The product needs a bridge from read-only department catalog visibility to CEO-configurable company structure.
- Boundary-first keeps future L5 company organization from leaking into the current executor without review.
- A tenant-local activation boundary can define the smallest future slice while preserving Admin/Workspace separation: Admin supplies official department types; Workspace may later choose which types are active for the tenant.

## Options

### Option A: Department Activation Boundary Definition

Approve architecture/product boundary definition only.

Allowed:

- Define future tenant-local department activation concept.
- Define allowed source: existing active official department type metadata.
- Define future minimal activation state shape if needed.
- Define read/write API boundary only if separately approved for implementation later.
- Define UI boundary for a future minimal selector or status view.
- Define verification plan and forbidden-scope locks.
- Update source-of-truth files.

Forbidden:

- Implementation.
- Backend/API/schema/persistence changes.
- New department APIs.
- Department CRUD beyond future activation boundary definition.
- Department instance creation or management.
- Department workflow routing.
- Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, or complex company organization.
- Admin Platform implementation or platform policy management.
- Billing, ROI, packages, marketplace, or L6 economy.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes.
- Execution-loop, tool routing, workflow, model-selection behavior, Project Memory write, or runtime behavior changes.
- Hosted production deployment.

### Option B: Another UI Evidence Slice First

Defer department activation boundary and continue with evidence/polish only.

Use only if 总控决策席 decides activation boundary work is premature.

### Option C: Pause Workspace Company Foundation

Pause this track and return to 产品规划席 for a different product priority.

Use only if 总控决策席 decides the next slice should leave company foundation.

## Acceptance Criteria

- 总控决策席 selects Option A, B, or C.
- Decision states whether boundary definition may proceed.
- If Option A is selected, route to 系统交付席 for architecture/product boundary definition only.
- If Option B or C is selected, route back to 产品规划席.
- Decision preserves ADR-0031, accepted company frame, accepted department summary/evidence, existing Task API payload `{ content }`, model-gateway security boundary, Admin/Workspace separation, local/demo scope, no hosted production, no billing/ROI/packages/marketplace, no Employee CRUD/expansion, no department workflow routing, no complex organization, no business modules, no secrets, and no execution-loop/runtime behavior change.

## Verification

Gate-only review. No implementation verification is required at this decision step.

## Gate Decision

Decision: APPROVED by 总控决策席 on 2026-07-08.

Selected option: Option A - Department Activation Boundary Definition.

Reason:

- The company frame and read-only department catalog summary are accepted and browser-verified.
- Option A is boundary-only and does not approve implementation, new APIs, persistence, department instances, employees, routing, Admin Platform, billing, business modules, secrets, or runtime behavior changes.
- The boundary definition is the safest next step toward CEO-configurable company structure because it can define exact future limits before any code is written.

Approved scope:

- Architecture/product boundary definition only for future tenant-local department activation.
- Allowed source is existing active official department type metadata.
- Future activation may be described as tenant-local selection/enablement metadata only, but implementation remains blocked until a separate issue is approved.
- Verification plan, source ownership, and forbidden-scope locks must be explicit.

Forbidden scope remains:

- Implementation.
- Backend/API/schema/persistence changes.
- New department APIs.
- Department CRUD beyond future activation boundary definition.
- Department instance creation or management.
- Department workflow routing.
- Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, or complex company organization.
- Admin Platform implementation or platform policy management.
- Billing, ROI, packages, marketplace, or L6 economy.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes.
- Execution-loop, tool routing, workflow, model-selection behavior, Project Memory write, or runtime behavior changes.
- Hosted production deployment.

## Completion Notes

Approved Option A. Route to 系统交付席 for boundary definition only.

Boundary definition and acceptance completed on 2026-07-08.

- Added `docs/decisions/ADR-0032-workspace-department-activation-boundaries.md`.
- Defined future tenant-local department activation as metadata-only selection over active official department type metadata.
- Preserved Admin ownership of official department type supply and Workspace-only future activation metadata boundary.
- Blocked implementation, backend/API/schema/persistence, new department APIs, department instances, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, and runtime behavior changes.
- Quality and product acceptance evidence is recorded in `reviews/079_workspace_department_activation_boundaries_review.md`.

Next Seat: main thread closeout.

Handoff: final closeout

Handoff: sent to 系统交付席

Target seat: 系统交付席

Compact payload:

- Issue: `issues/082_workspace_department_activation_boundary_gate.md`
- Objective: Define architecture/product boundaries for future tenant-local department activation.
- Special Constraints: Boundary-only. No implementation, backend/API/schema/persistence changes, new department APIs, department instances, workflow routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, or runtime behavior changes.
- Next Seat: 系统交付席.
