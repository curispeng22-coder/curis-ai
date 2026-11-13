# Curis System Architecture

Status: Frozen

Baseline:
main @ c0e1855f

Updated:
2026-07-31

---

## 1. Architecture Overview

```text
Next.js Frontend
→ Trusted Local Gateway
→ FastAPI Workspace Backend
→ Domain Services / Runtime
→ SQLite data/curis.sqlite
```

The delivered architecture is one Desktop-first runtime. Logical
Platform/Admin permissions may exist inside it, but there is no second current
frontend or database.

The Frozen target product architecture adds a logical Company OS layer and
first-class Workspace aggregate inside this same runtime boundary:

```text
Company OS (fixed product shell and company operating context)
→ Workspace Portal
→ Workspace (business-specific execution aggregate)
→ existing Project / Task / Workflow / Artifact services as needed
```

This target is not yet implemented. The migration is
`BLOCKED_PENDING_BUSINESS_RUNTIME_BLUEPRINT`.

## 2. Frontend

- Current application: `frontend/`
- Framework: Next.js 16.2.10 with React 19.2.7
- Root layout: `frontend/app/layout.js`
- Product shell: `frontend/components/terra/TerraShell.js`
- Shared primitives: `frontend/components/terra/TerraPrimitives.js`
- Global Assistant host:
  `frontend/components/assistant/GlobalAssistant.js`
- Frontend calls the trusted Gateway/API boundary through
  `frontend/lib/api.js`.

The root layout owns the Assistant Provider. Pages provide structured page
context but do not create page-local Assistant runtimes.

Target frontend rules:

- Company OS primary pages reuse one shell, navigation grammar and interaction
  model.
- Workspace pages use a shared host/security boundary but may render different
  layouts, components and interaction models by Workspace Blueprint.
- Industry variation must not create separate frontend applications.

## 3. Backend

- Current service root: `backend/app/`
- Composition entry: `backend/app/main.py`
- Framework: FastAPI
- Domain services cover Company, Department, Project, Employee, Affiliation,
  Capability, Task, Workflow, Artifact, Knowledge, Memory, Context, AI Usage
  and Assistant Runtime.
- Routers are composed into the Workspace API; domain writes remain behind
  their services and Tenant context.

Target services to be introduced only after contract approval are Workspace
Blueprint, Workspace composition, Workspace membership, Meeting and Resource
Request. Existing Project/Task/Workflow services are migration inputs and stay
the execution substrate.

## 4. Runtime

Official local lifecycle:

```bash
CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh
./deploy/curis/stop-local.sh
```

Runtime endpoints:

- Frontend: `127.0.0.1:3001`
- Trusted Gateway: `127.0.0.1:8080`
- Workspace API: container internal port `8002`

The Gateway is the trusted browser-facing boundary. Model calls use the
approved Model Gateway path; credentials are not product data and must not be
persisted in Git, API payloads, logs or SQLite.

### Business Runtime Target

Each primary module requires a persisted business state machine. A transition
must carry:

- business object and current state
- actor and authority
- precondition and command
- Input provenance
- durable Output
- next state
- cross-module correlation
- feedback event
- audit evidence

UI state cannot be the source of business status. APIs are transition commands
and projections, not completion evidence. Cross-module handoffs such as
Meeting → Workspace and Workspace → Meeting feedback must share durable
correlation identifiers.

## 5. Data

- Current database: `data/curis.sqlite`
- SQLite schema version: `1`
- Migration record: `integration-v1-schema-baseline`
- Migration ledger: `schema_migrations`
- Employee affiliation table: `employee_affiliations`
- Fresh and existing databases must converge on the same schema.
- Unknown non-empty retired tables fail closed instead of being dropped.

Tenant identity is carried through domain records and service queries. Data
access must not fall back to cross-tenant reads.

## 6. Assistant Runtime

```text
Global Assistant Provider / Host
→ Identity
→ Snapshot / Notifications
→ Project or Business Department Query
→ Command
→ existing Task
→ Task Run
→ Capability / Model Gateway
→ AI Usage
→ Artifact
```

The Assistant may read structured current state and submit existing Task
commands. It must not bypass business services, mutate arbitrary objects or
create a parallel execution engine.

## 7. Capability

- Capability is a Company Resource. The current Capability Registry remains the
  callable inventory for Model, Skill and Tool capabilities.
- Employee bindings select enabled capabilities inside the current Tenant.
- Target Workspace resource bindings record which resources a business space
  requires and may use.
- Missing resources produce procurement requests; Business Engineering does
  not create replacement Agent, Capability, Tool or Plugin implementations.
- Runtime selection must validate source, type, status and ownership before
  execution.
- Model execution routes through the Model Gateway; provider-specific direct
  paths are not the current default architecture.

## 8. Workspace And Task Execution

Target composition:

```text
Workspace
→ members + resources + modules + business context
→ optional Project
→ Task / Workflow execution
→ Artifact / Knowledge / Insight
→ Company OS operating loop
```

Current delivered execution:

```text
Project
→ Task
→ assigned Employee
→ bound Capability
→ Workflow / execution events
→ result
→ Artifact
```

Task is the execution fact source. Execution status, structured events,
failures, usage and artifacts must remain traceable to the same Task. Knowledge
and Memory may enrich context but do not replace execution records.

Workspace becomes the business-facing aggregate without replacing Task as the
low-level execution fact source.

## 9. Identity Boundary

- Current operator mode is Local Owner.
- Tenant Context scopes Workspace requests and stored records.
- Company is the root business aggregate inside a Tenant.
- Trusted subject and membership checks protect sensitive execution and
  Platform/Admin routes.
- UI visibility is not authorization; backend checks own the security boundary.
- Future Workspace/Admin physical separation requires a separate identity,
  Tenant, API, data ownership, audit, deployment and migration contract.

## References

### Current Effective Sources

- `docs/00_Context/CURRENT_STATE.md`
- `docs/07_Decisions/ADR-0033-global-assistant-runtime.md`
- `docs/07_Decisions/ADR-0034-main-baseline-restoration.md`
- `docs/07_Decisions/ADR-0036-workspace-admin-boundary.md`
- `docs/07_Decisions/ADR-0037-domain-frozen-entry-documents.md`
- `docs/07_Decisions/ADR-0040-company-os-workspace-product-reset.md`
- `docs/07_Decisions/ADR-0041-business-runtime-completion-standard.md`
- `docs/01_Product/Curis_Product_Blueprint.html`
- `docs/01_Product/Business_Runtime_Gap_Report_2026-07-31.md`
- `docs/02_Architecture/Architecture_Migration_Report_2026-07-31.md`

### Historical References

- `docs/architecture/curis-backend-core-arch.md`
- `docs/architecture/curis-assistant-runtime-architecture-report.md`
- `reviews/20260730_integration_candidate_review.md`
- `reviews/20260730_global_assistant_live_model_validation_review.md`

### Deprecated Sources

- `docs/architecture/curis-assistant-architecture-review.md`
- `knowledge/003_Architecture.md`
- `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/00-SYSTEM-ARCHITECTURE.md`
- `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/02-CAPABILITY-ARCHITECTURE.md`

Deprecated sources remain historical only and cannot define current runtime
behavior.
