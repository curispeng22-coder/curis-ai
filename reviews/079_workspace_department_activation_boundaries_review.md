# Review 079: Workspace Department Activation Boundaries

Date: 2026-07-08
Owner: 系统交付席 / 质量运行席 / 产品规划席
Issue: `issues/082_workspace_department_activation_boundary_gate.md`
Status: ACCEPTED_BY_PRODUCT

## Product Progress

Curis Workspace now has an accepted boundary for future tenant-local department activation, so the product can move from read-only department visibility toward CEO-configurable company structure without implementing department CRUD, employees, routing, Admin Platform, billing, or runtime changes.

## Delivery Result

PASS-FOR-QUALITY-PLANNING.

Workspace Department Activation boundaries are defined in `docs/decisions/ADR-0032-workspace-department-activation-boundaries.md`.

## Boundary Defined

- Future department activation is tenant-local selection over active official department type metadata.
- Admin Platform/shared contracts remain owner of official department type supply and policy.
- Workspace may later own tenant-local activation metadata only after a separate implementation issue is approved.
- No API, persistence, UI selector, department instance, workflow routing, Employee CRUD, Admin implementation, billing, business module, secret, Task API, or runtime behavior change is approved by the boundary.

## Allowed Future First Slice

Only after separate approval:

- Validate selected department type keys against active official department type metadata.
- Store tenant-local activation references only.
- Return a non-secret read model for the company frame.
- Test tenant scoping, official-only validation, no-secret persistence/exposure, and no execution behavior changes.

## Blocked Scope

- Implementation in this boundary issue.
- Backend/API/schema/persistence changes.
- New department APIs.
- Department CRUD, department instance management, staffing, permissions, reporting lines, org charts, or workflow routing.
- Employee CRUD or employee expansion.
- Admin Platform implementation or platform policy management.
- Billing, ROI, packages, marketplace, or L6 economy.
- Business modules or external business-platform connectors.
- Secret input/display, credential persistence, provider SDK/direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes.
- Execution-loop, tool routing, workflow, model-selection behavior, Project Memory write, or runtime behavior changes.

## Verification Plan

Required quality checks:

```bash
git diff --check -- docs/decisions/ADR-0032-workspace-department-activation-boundaries.md reviews/079_workspace_department_activation_boundaries_review.md issues/082_workspace_department_activation_boundary_gate.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
rg -n "tenant-local|official|metadata-only|department CRUD|Employee CRUD|workflow routing|Admin Platform|billing|ROI|marketplace|secret|Task API|runtime behavior|separate implementation" docs/decisions/ADR-0032-workspace-department-activation-boundaries.md reviews/079_workspace_department_activation_boundaries_review.md issues/082_workspace_department_activation_boundary_gate.md
git diff --name-only -- docs/decisions/ADR-0032-workspace-department-activation-boundaries.md reviews/079_workspace_department_activation_boundaries_review.md issues/082_workspace_department_activation_boundary_gate.md PROJECT_STATUS.md TASKS.md knowledge/CURRENT_CONTEXT.md knowledge/PROJECT_MEMORY.md
```

Expected evidence:

- Boundary/review/source-of-truth documentation only for this issue.
- Boundary explicitly preserves official department type ownership outside Workspace.
- Boundary blocks implementation and future-layer scope until separate approval.
- No backend/frontend behavior change is required by this issue. Existing unrelated or previously accepted dirty files are not evidence for this boundary task.

## Quality Verification

Quality Result: PASS.

Commands: boundary diff check, boundary keyword scan, boundary file-scope check, and source-of-truth status scan.

Evidence: ADR-0032 defines a metadata-only tenant-local activation boundary over active official department type metadata; it explicitly blocks implementation, backend/API/schema/persistence, new department APIs, department CRUD/instances/routing, Employee CRUD, Admin Platform, billing/ROI/packages/marketplace, business modules, secrets, Task API changes, and runtime behavior changes.

Risks: Future implementation still needs a separate issue and must decide exact API/persistence/UI shape. This boundary does not itself approve a department activation selector or backend state. The worktree contains pre-existing unrelated or previously accepted dirty files; they were not used as evidence for this boundary.

Blocked / Pass: Pass; no blockers found.

Next Seat: 产品规划席.

## Product Acceptance

Product Decision: ACCEPTED.

Priority: Close the department activation boundary and open a separate implementation gate only when the next slice is ready.

Scope: Accept ADR-0032 as the architecture/product boundary for future tenant-local department activation.

Acceptance Criteria:

- Boundary-only scope is preserved.
- Future activation remains tenant-local metadata over active official department types.
- Official department type ownership remains outside Workspace.
- No implementation, backend/API/schema/persistence, frontend selector, department CRUD, department instances, workflow routing, Employee CRUD, Admin Platform, billing, business module, secret, Task API, or runtime behavior change is approved.

Source Of Truth Updates: `issues/082_workspace_department_activation_boundary_gate.md`, `TASKS.md`, `PROJECT_STATUS.md`, `knowledge/CURRENT_CONTEXT.md`, and `knowledge/PROJECT_MEMORY.md` mark the department activation boundary accepted.

Next Seat: main thread closeout.

Open Questions: None.

Handoff: final closeout
