# ADR-0031: Workspace Company Foundation Boundaries

Date: 2026-07-08

Status: Accepted.

Source issue: `issues/077_post_first_version_workspace_company_foundation_gate.md`

## Context

The model-gateway-enabled AI Task Executor MVP has been closed out as a local/demo first version. Curis Workspace can create and run tasks, show execution evidence, read official model/tool metadata, use New API through `ModelGatewayAdapter`, store a tenant default model preference, and expose that preference inside the operation console.

The next product step is to define the first minimal CEO-facing company/workspace frame around those accepted capabilities. This must move the product toward the future AI Company System without prematurely implementing hosted production, Admin Platform management, billing/ROI, marketplace, Employee CRUD, complex organization, business modules, secret handling, or execution-loop changes.

## Decision

Define Workspace Company Foundation as a bounded local/demo company shell over accepted Workspace state.

The foundation is not a full L5 organization system. It is a minimal CEO-facing frame that can show how the current tenant/workspace, company identity, department catalog/instances, model preference, task console, and Project Memory relate to each other.

## Product Boundary

Allowed product concepts:

- `Workspace`: the CEO-facing local/demo operating space for one tenant context.
- `Company identity`: minimal display metadata for the CEO's local/demo company frame, such as company name/label and local workspace status.
- `Department foundation`: read-only or explicitly bounded display of existing department catalog/types and existing department instances.
- `Execution console`: the accepted AI Task Executor task composer, history, run action, selected detail, and review signals.
- `Model preference`: the accepted tenant default model preference over active official model catalog metadata.
- `Project Memory`: the accepted deterministic project-fact memory artifact and approved source-of-truth references.

Forbidden product concepts:

- Hosted production workspace.
- Admin Platform implementation or platform management UI.
- Billing, ROI, packages, marketplace, or L6 economy behavior.
- Employee CRUD, employee expansion, staffing, permissions, reporting lines, org charts, or complex company organization.
- Business modules or external business-platform connectors.
- Secret input, secret display, credential persistence, provider account editing, provider SDK, direct provider calls, New API source changes, or New API internal database dependency.
- Task API payload changes, execution-loop changes, tool routing changes, workflow mutation, runtime behavior changes, or automatic evolution behavior changes.

## Architecture Boundary

Workspace Company Foundation may aggregate only existing approved read models and source-controlled facts:

- tenant identity placeholder/current local tenant context;
- minimal company identity metadata once separately approved for implementation;
- existing department catalog/types and department instances;
- accepted model preference read model;
- accepted task console state and existing task APIs;
- Project Memory source references;
- local/demo release evidence and status files.

It must not create a new execution path. Task execution remains:

```text
Task -> Orchestrator -> Auto Workflow Generator -> Employee -> Tool Router -> Tool Executor -> Result -> Development Learning -> Meta Development -> Evolution Governor -> Storage
```

Model calls remain constrained to `ModelGatewayAdapter`. Official model/tool metadata ownership remains separated between Admin Platform supply and Workspace consumption. Workspace Company Foundation may consume approved catalog/read-model metadata but must not manage platform catalog supply.

## Source Ownership

| Area | Owner | Boundary |
| --- | --- | --- |
| Company foundation boundary | `docs/decisions/ADR-0031-workspace-company-foundation-boundaries.md` | Architecture/product boundary only. |
| Current issue | `issues/077_post_first_version_workspace_company_foundation_gate.md` | Gate decision and completion notes. |
| Verification evidence | `reviews/074_workspace_company_foundation_boundaries_review.md` | Boundary verification evidence. |
| Project facts | `knowledge/CURRENT_CONTEXT.md`, `knowledge/PROJECT_MEMORY.md`, `PROJECT_STATUS.md`, `TASKS.md` | Low-token status and next-seat routing. |
| Runtime task execution | existing backend/frontend task APIs | No semantic or payload change in this boundary. |
| Catalog supply | Admin Platform/shared contracts | Workspace consumes only approved non-secret metadata. |

## First Implementation Slice Boundary

Recommended first slice after quality acceptance:

Workspace Company Foundation first slice should be a minimal local/demo company frame in the existing Workspace operation console or an approved read-model layer for that frame.

The first slice may show:

- company/workspace identity label;
- current local/demo release status;
- current tenant/default workspace context;
- active official model preference summary;
- existing task console entry point/status summary;
- Project Memory/source-of-truth pointers;
- bounded department catalog/instance summary only if existing read access is available or a read-model gap is separately approved.

The first slice must not:

- add Employee CRUD, employee assignment, staffing, permissions, org chart, department workflow routing, business modules, ROI, packages, marketplace, Admin Platform management, secret handling, hosted production, new execution behavior, or Task API payload changes;
- create department type CRUD or platform policy management;
- introduce provider SDK/direct provider calls or New API internal database dependency;
- mutate task execution, model selection behavior, tool routing, workflows, Project Memory, or automatic evolution behavior.

Read-model gap rule:

- If implementation needs a new backend read API for company identity or department summaries, 系统交付席 must document the exact read-model gap and route back for approval before implementation.
- No new persistence table is approved by this boundary.

## Verification Plan

质量运行席 should verify:

- boundary-only files changed; no backend/frontend behavior files unless separately approved;
- ADR includes product boundary, architecture boundary, first-slice boundary, source ownership, and verification plan;
- forbidden scope remains explicit for hosted production, Admin Platform implementation, billing/ROI/packages/marketplace, Employee CRUD/expansion, complex organization, business modules, secrets, provider SDK/direct calls, Task API changes, and execution-loop/runtime changes;
- first implementation slice is constrained to a minimal local/demo Workspace company frame and documents read-model gap routing;
- source-of-truth status files align with this boundary and next seat routing.

## Consequences

This boundary creates a safe bridge from the local/demo AI Task Executor MVP toward the AI Company System. It lets the product frame existing execution, model preference, department groundwork, and Project Memory as one CEO-facing Workspace without unlocking the future company organization or economy layers.

Any implementation must be opened as a separate issue after this boundary is quality-verified and accepted.
