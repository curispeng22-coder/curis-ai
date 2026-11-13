# Directory Structure Standard

## Root Layout

The repository should use this layout as it grows:

```text
/
  AGENTS.md
  README.md
  docs/
    ai-development-organization/
    decisions/
    pmo/
    product/
    sprints/
    standards/
    99_Archive/
      curis_workspace_blueprint/
  backend/
  frontend/
  plugins/
    curis-ai-development-organization/
  curis_workspace_blueprint/
    ADR/
```

Current application directories are limited to the Tool System v1.5 implementation. Future business modules must be introduced through an ADR and approved Sprint plan.

## Directory Rules

- `docs/ai-development-organization/` contains team and collaboration governance.
- `docs/product/` contains active product requirements.
- `docs/pmo/` contains active PMO status, roadmap, backlog, and role-session coordination.
- `docs/standards/` contains durable engineering standards.
- `docs/sprints/` contains Sprint workflow, plans, reviews, and retrospectives.
- `docs/decisions/` contains ADRs.
- `backend/` contains the FastAPI Tool System v1.5 backend.
- `frontend/` contains the minimal Tool System v1.5 frontend.
- `plugins/` contains Codex plugins owned by this workspace.
- `docs/99_Archive/curis_workspace_blueprint/` contains the archived non-ADR
  blueprint material. The two historical decision records remain in
  `curis_workspace_blueprint/ADR/`. Neither location is an active
  implementation source of truth.

## Naming Rules

- Use lowercase kebab-case for directories and Markdown files.
- Use ADR names in the form `ADR-0001-short-title.md`.
- Keep documents focused on one responsibility.
- Avoid catch-all folders such as `misc/`, `temp/`, and `old/`.

## Ownership Rules

Every top-level directory must have:

- A clear purpose
- A documented owner role
- A review expectation
