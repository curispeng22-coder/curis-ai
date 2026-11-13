# ADR-0032: Workspace Department Activation Boundaries

Date: 2026-07-08

Status: Accepted.

Issue: `issues/082_workspace_department_activation_boundary_gate.md`

## Context

Curis Workspace has an accepted local/demo company frame and an accepted read-only `部门目录` summary. Browser-visible evidence confirms the company frame and official department catalog summary render in the operation console.

The next product step is to define how a CEO may later activate a small set of tenant-local departments from official department type metadata. This moves toward the commercial AI Company System while keeping the current AI Task Executor MVP stable.

This ADR is boundary-only. It does not approve implementation, new APIs, schema changes, department instances, staffing, workflow routing, Employee CRUD, Admin Platform implementation, billing, or runtime behavior changes.

## Decision

Workspace Department Activation is defined as a future tenant-local selection layer over existing active official department type metadata.

The activation layer is not department CRUD, not an org chart, not staffing, not permissions, not workflow routing, not Employee management, and not Admin Platform policy management. It is only a future Workspace-owned record of which approved official department types a tenant wants visible or enabled in its company frame.

Admin Platform remains the owner of official department type supply and platform policy. Workspace may consume only active official department type metadata and may later store tenant-local activation metadata after a separate implementation issue is approved.

## Product Boundary

Allowed future product concept:

- Tenant-local department activation: CEO chooses which existing official department types are active in the Workspace company frame.

Allowed future first-slice behavior after separate approval:

- Show active official department type options.
- Let CEO activate or deactivate a small bounded set of department type references for the local tenant.
- Show activated department labels in the existing company frame.
- Keep copy in Chinese.
- Keep the feature local/demo until hosted production is separately approved.

Blocked product concepts:

- Creating custom official department types.
- Editing official department definitions.
- Cross-tenant marketplace or sharing.
- Department instance management beyond tenant-local activation references.
- Employee CRUD, employee assignment, staffing, permissions, reporting lines, org charts, or complex organization.
- Department workflow routing, task routing, tool routing, model-routing policy, or execution behavior changes.
- Business modules or external business-platform connectors.
- Billing, ROI, packages, marketplace, or L6 economy behavior.
- Admin Platform implementation or platform policy management.
- Secret input/display or credential persistence.

## Architecture Boundary

Future implementation may introduce a tenant-scoped activation read model only after a separate implementation issue is approved.

Allowed future activation state shape:

- `tenant_id`
- `department_type_key`
- `source`
- `enabled`
- `display_order`
- `updated_at`

Constraints:

- `department_type_key` must reference an active official department type.
- `source` must remain `official` for activated official department references.
- Activation metadata must not copy or mutate official department definitions.
- Activation metadata must not contain prompts, outputs, secrets, credentials, model policy, routing policy, billing fields, ROI fields, staffing fields, permission fields, reporting-line fields, or external-platform configuration.
- Any persisted activation state must be tenant-scoped.

Future API boundary may be defined in a separate implementation issue. If approved later, it should remain Workspace-local and metadata-only:

- read current tenant activation state;
- update only tenant-local activation references;
- return only non-secret official department metadata plus tenant-local enabled state.

No API is approved by this ADR.

## Runtime Boundary

Department activation must not affect task execution.

Task execution remains:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

Model execution remains constrained to:

```text
Workspace runtime -> ModelGatewayAdapter -> New API OpenAI-compatible API
```

Department activation must not:

- change Task API payload shape `{ content }`;
- mutate workflow generation;
- route tasks by department;
- assign employees;
- change tool routing;
- change model selection;
- write Project Memory;
- trigger autonomous evolution;
- create external side effects.

## Source Ownership

| Area | Owner | Boundary |
| --- | --- | --- |
| Official department type supply | Admin Platform / shared contract | Official definitions and policy, not Workspace-owned. |
| Department activation boundary | `docs/decisions/ADR-0032-workspace-department-activation-boundaries.md` | Boundary only. |
| Gate issue | `issues/082_workspace_department_activation_boundary_gate.md` | Gate decision and completion notes. |
| Verification evidence | `reviews/079_workspace_department_activation_boundaries_review.md` | Boundary verification and acceptance evidence. |
| Future implementation issue | TODO after gate | Required before any backend/frontend/API/schema changes. |
| Status context | `PROJECT_STATUS.md`, `TASKS.md`, `knowledge/CURRENT_CONTEXT.md`, `knowledge/PROJECT_MEMORY.md` | Low-token current-state routing. |

## Recommended First Implementation Slice

If 产品规划席 opens a separate implementation issue, the recommended first slice is backend-first metadata activation only:

- Validate selected `department_type_key` values against active official department type metadata.
- Store tenant-local activation references only.
- Return a non-secret read model for the existing company frame.
- Include focused tests for tenant scoping, official-only validation, no-secret persistence/exposure, and no execution behavior changes.

Frontend selector or company-frame activation display must be separately approved unless included explicitly in the implementation issue.

## Verification Requirements

Boundary verification must prove:

- This ADR is documentation-only.
- No backend/frontend behavior files are required by the boundary task.
- Official department type ownership remains outside Workspace.
- Future Workspace activation is tenant-local and metadata-only.
- New APIs, persistence, UI selector, and company-frame display remain blocked until separate implementation approval.
- Department CRUD, department instances, Employee CRUD, staffing, permissions, reporting lines, org charts, workflow routing, Admin Platform implementation, billing, ROI, marketplace, business modules, secrets, Task API changes, and runtime behavior changes remain blocked.

## Consequences

This boundary creates the next safe bridge from read-only company foundation toward CEO-configurable company structure. It lets Curis move toward the future AI Company System while preserving current local/demo stability and preventing premature L5 organization or L6 economy scope.
