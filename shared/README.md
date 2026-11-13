# Curis Shared Space

This space contains files that both Admin Platform and Workspace must follow.

## Ownership

Shared owns cross-product rules and contracts:

- Operating-seat workflow and role boundaries.
- Source-of-truth rules.
- Multi-tenant contract definitions.
- Capability source contracts:
  - `official`
  - `tenant_private`
  - `marketplace`
- Usage, billing, and audit event contracts.
- Cross-product architecture and product briefs.
- Shared prototypes that explain both products together.

## Current Shared Entry Points

Some shared files remain at the repository root for tool compatibility:

- `AGENTS.md`
- `PROJECT_STATUS.md`
- `TASKS.md`
- `PROJECT_HANDOFF.md`
- `knowledge/`
- `issues/`
- `reviews/`

Treat these as shared project governance files until a separate migration gate approves moving them.

## Subdirectories

- `shared/product/`: cross-product PRD, product brief, and product-change documents.
- `shared/architecture/`: cross-product architecture and contract docs.
- `shared/prototypes/`: cross-product prototypes and visual product maps.
- `shared/governance/`: workflow, role, gate, and operating-seat rules.
- `shared/pmo/`: project-space maps, handoff maps, and PMO coordination docs.
