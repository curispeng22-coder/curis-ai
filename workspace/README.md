# Curis Workspace Space

This space is reserved for the CEO-facing AI Company Workspace product.

## Ownership

Workspace owns tenant company operations:

- Company setup.
- Departments, employees, responsibilities, and workflow configuration.
- Task creation, execution, status, history, and result review.
- Project Memory and company knowledge.
- Use of official capabilities supplied by Admin Platform.
- Tenant-private self-extension:
  - private model providers
  - private tools
  - private connectors
  - private department templates
  - private workflow templates

## Current Implementation Note

The current AI Task Executor MVP implementation still lives in the root `backend/`, `frontend/`, `tools/`, `issues/`, `reviews/`, and `knowledge/` paths to preserve verified local/demo commands.

Do not physically move those runtime paths until a migration issue approves command, import, and documentation updates.

## Future File Placement

Place future Workspace-specific files here after the migration gate:

- `workspace/app/` for Workspace product implementation.
- `workspace/docs/` for Workspace-specific product, architecture, and release docs.
- `workspace/tests/` for Workspace-specific tests.

Shared contracts and rules belong in `shared/`, not here.
