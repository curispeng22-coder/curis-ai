# Curis Project Space Map

Date: 2026-07-08

## Goal

Separate future Curis development into three project spaces:

- `admin-platform/`: platform-side management product.
- `workspace/`: CEO-facing AI Company Workspace product.
- `shared/`: rules, contracts, source-of-truth, and cross-product docs.

This map is the current routing source for where new files should be created.

## Current Top-Level Ownership

| Path | Owner Space | Current Action |
| --- | --- | --- |
| `admin-platform/` | Admin Platform | New Admin Platform project space. |
| `workspace/` | Workspace | New Workspace project space. |
| `shared/` | Shared | New shared contracts and PMO space. |
| `backend/` | Workspace | Keep in place until runtime migration gate. |
| `frontend/` | Workspace | Keep in place until runtime migration gate. |
| `tools/` | Workspace / Shared | Keep in place until commands are re-routed. |
| `data/` | Workspace | Keep in place; contains current local MVP data. |
| `knowledge/` | Shared | Keep in place for low-token context compatibility. |
| `issues/` | Shared | Keep in place for current workflow compatibility. |
| `reviews/` | Shared | Keep in place for evidence history compatibility. |
| `docs/` | Mixed legacy | New cross-product docs should go to `shared/`; product-specific docs should go to `admin-platform/docs/` or `workspace/docs/`. |
| `diagrams/` | Workspace legacy | Keep in place until prototype/diagram migration issue. |
| `docs/99_Archive/curis_workspace_blueprint/` | Shared / Workspace legacy | Archived non-ADR blueprint material. |
| `curis_workspace_blueprint/ADR/` | Shared / Workspace legacy | Historical decision records retained at the original path. |
| `plugins/` | Shared tooling | Keep in place until plugin ownership is reviewed. |
| `AGENTS.md` | Shared | Keep at root for agent discovery; shared operating contract. |
| `PROJECT_STATUS.md` | Shared | Keep at root for current workflow compatibility. |
| `TASKS.md` | Shared | Keep at root for current workflow compatibility. |
| `PROJECT_HANDOFF.md` | Shared | Keep at root for handoff compatibility. |
| `README.md` | Shared | Keep at root as repository entry point. |

## Migrated In This Pass

| Old Path | New Path | Owner |
| --- | --- | --- |
| `docs/product/curis-commercial-multitenant-change-brief.md` | `shared/product/curis-commercial-multitenant-change-brief.md` | Shared |
| `docs/product/curis-commercial-system-product-doc.md` | `shared/product/curis-commercial-system-product-doc.md` | Shared |
| `docs/product/curis-admin-workspace-flows.md` | `shared/product/curis-admin-workspace-flows.md` | Shared |
| `docs/architecture/curis-admin-workspace-product-architecture.md` | `shared/architecture/curis-admin-workspace-product-architecture.md` | Shared |
| `docs/prototypes/curis-full-system-high-fidelity-prototype.html` | `shared/prototypes/curis-full-system-high-fidelity-prototype.html` | Shared |

## Placement Rules For New Files

### Admin Platform

Place files in `admin-platform/` when they are only about:

- Platform operators.
- Tenant / CEO account management.
- Official capability supply.
- Usage and billing management.
- Platform audit and security administration.
- Marketplace review and platform-wide governance.

### Workspace

Place files in `workspace/` when they are only about:

- CEO company setup.
- Department, employee, workflow, and task execution.
- Workspace operation console.
- Tenant-private model, tool, connector, department, or workflow configuration.
- Company knowledge and Project Memory runtime behavior.

### Shared

Place files in `shared/` when both teams must follow them:

- Development workflow and role rules.
- Cross-product architecture.
- Shared data contracts.
- Tenant and billing event contracts.
- Capability source rules.
- Product-change briefs that affect both Admin Platform and Workspace.

## Migration Guardrails

- Do not move current runtime code until a dedicated migration issue exists.
- Do not move root `AGENTS.md` until agent discovery behavior is confirmed.
- Do not split `knowledge/`, `issues/`, or `reviews/` until the operating-seat workflow is updated.
- Do not duplicate conflicting source-of-truth files across spaces.
- When a file affects both products, keep it in `shared/`.
- When a file only affects one product, place it in that product space.
