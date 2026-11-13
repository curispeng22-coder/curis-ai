# Curis Architecture Migration Report

Status: Review

Baseline: `main @ c0e1855f446a55aa3a384006cfcfed9877130338`

Updated: 2026-07-31

Decision: `docs/07_Decisions/ADR-0040-company-os-workspace-product-reset.md`

Boundary: inventory and migration design only. No business code was changed.

Current product authority: `docs/01_Product/Curis_Product_Blueprint.html` v5.0 and
`docs/00_Context/CURRENT_STATE.md`. This report is historical migration evidence and
does not define the current product shape or development order.

## 1. Executive Conclusion

The current runtime is technically reusable, but the product composition is
wrong for the new definition:

```text
Current product composition
Project → Task / Workflow → Artifact

Target product composition
Company OS → Workspace Portal → Workspace
Workspace → internal Project / Task / Workflow / Artifact as needed
```

The migration must not rewrite the runtime first. The smallest safe path is:

1. Freeze the new product object meanings.
2. Add Workspace as the business execution aggregate.
3. Reframe existing Project/Task services as Workspace internals.
4. Replace the primary navigation and entry routes.
5. Migrate pages one Workspace type at a time.

## 2. Current Evidence

| Area | Current evidence | Finding |
| --- | --- | --- |
| Navigation | `frontend/components/terra/TerraNavData.js` | Ten old primary entries; Project Center, Brainstorm, Execution Workbench and Company Runtime View still define the shell |
| Shell | `frontend/components/terra/TerraShell.js`, `TerraSidebar.js` | One reusable Company OS shell already exists |
| Project Center | `frontend/app/ceo-office/projects/page.js` | Lists Project grouped by Department; creates Project directly |
| Project detail | `frontend/app/ceo-office/projects/[id]/page.js` | A Task/Artifact execution workbench, not a business-specific Workspace |
| Duplicate route | `frontend/app/projects/page.js` | Redirects to the CEO Office Project Center |
| Legacy project runtime | `frontend/app/projects/[project_id]/page.js` | Separate goal/plan/run/review experience duplicates the newer route |
| State | page-local React state; `frontend/lib/api.js` | No shared Workspace identity, definition or renderer state |
| Business Engineering | `backend/app/employee_templates.py` | Auto-creates a deletable `Engineering Department` with `software_rnd` semantics |
| Capability | `frontend/app/ceo-office/capabilities/page.js`; capability APIs | Capability is presented as callable technical inventory rather than the full Company Resource center |
| Data | `companies`, department/project/task/capability tables in `data/curis.sqlite` | No first-class Workspace, Workspace Blueprint, Workspace composition or Meeting aggregate |
| API | `/api/workspace/projects`, `/tasks`, `/workflows`, capability endpoints | Existing execution APIs are reusable but expose Project/Task as product-level concepts |

## 3. Target Object Model

```text
Company
├── Business
├── Organization
├── System Department: Business Engineering
├── Company Resource
│   ├── Capability
│   ├── Tool
│   ├── Integration
│   └── Resource entitlement / procurement state
├── Workspace Blueprint
│   └── official or company-specific composition definition
├── Workspace
│   ├── members
│   ├── resources
│   ├── modules and layout
│   ├── Workspace meetings
│   └── internal execution records
│       ├── Project
│       ├── Task
│       ├── Workflow Run
│       └── Artifact
├── Company Meeting
├── Insight / Business Analysis
└── Knowledge & IP
```

Object rules:

- Workspace is the business-facing execution aggregate.
- Workspace Blueprint is a reusable composition definition, not a running
  Workspace.
- Project remains only where a Workspace needs project-shaped work.
- Task and Workflow remain execution facts, never primary product navigation.
- Capability is acquired/authorized Company Resource; employee binding remains
  an execution permission, not the definition of Capability.

## 4. High Priority

### 4.1 Delete from the target product

These are target removals. Physical deletion waits for an implementation Issue.

| Target removal | Current location | Migration rule |
| --- | --- | --- |
| Project Center as a primary product concept | `TerraNavData.js`, `/ceo-office/projects` | Replace with Workspace Portal; preserve Project records as Workspace internals |
| Execution Workbench as primary navigation | `/ceo-office/execution` | Move Task/Workflow views inside each Workspace or an internal operations view |
| Brainstorm as a primary Company OS place | `/ceo-office/brainstorm` | Rehome as a Workspace tool/module or CEO Office activity |
| Company Runtime View as primary navigation | `/ceo-office/company-runtime` | Reframe as Insight or CEO Office operating view |
| Capability categories that imply Curis develops Agents/Workflows | capability navigation labels | Replace with Company Resource taxonomy and source/procurement status |
| Duplicate old project runtime route | `/projects/[project_id]` | Keep compatibility redirect during migration, then remove after evidence |

### 4.2 Modify

| Area | Required modification | Files / objects |
| --- | --- | --- |
| Navigation | Replace old ten-item IA with the fixed Company OS places; move Settings to utility/footer | `TerraNavData.js`, `TerraSidebar.js` |
| Project Center | Change list semantics, labels, cards and actions to Workspace Portal / Workspace | `ceo-office/projects/*`, `ProjectCard` |
| Project detail | Stop using one generic Task dashboard as every business execution space | `ceo-office/projects/[id]/*` |
| Business Engineering | Change from software R&D department to non-deletable system department that designs Workspaces | `employee_templates.py`, department services, organization UI |
| Capability | Represent provider/source, access, entitlement, health, procurement and Workspace usage | capability pages, selector projections, catalog services |
| Assistant context | Add `workspace_id`, `workspace_type`, current module and safe business context | `TerraShell`, Global Assistant page context |
| Current Company summary | Count and surface Workspaces rather than treating Project count as the main operating measure | CEO Office summary projection |

### 4.3 Add

Minimum new product records:

| Object | Minimum fields | Reason |
| --- | --- | --- |
| `workspace_blueprints` | id, source, name, business_type, version, definition_json, status | Reusable official/company Workspace definition |
| `workspaces` | id, tenant_id, company_id, blueprint_id, name, business_type, status, owner_id, created_at, updated_at | Running Business Execution Space |
| `workspace_members` | workspace_id, subject_type, subject_id, role, status | Workspace team and access |
| `workspace_resources` | workspace_id, resource_type, resource_id, required, status, configuration_json | Composition of Capability/Tool/Knowledge/Integration |
| `workspace_modules` | workspace_id, module_key, module_type, position_json, configuration_json, status | Variable layout and components |
| `meetings` | id, company_id, workspace_id nullable, scope, topic, host_id, scheduled_at, status, decision_summary | Separate company and Workspace meetings |
| `resource_requests` | id, workspace_id, requested_type, requirement, business_reason, status, decision | Business Engineering procurement request |

Minimum new target routes:

```text
/ceo-office
/business
/organization
/business-engineering
/meeting
/capability
/insight
/business-analysis
/knowledge-ip
/workspaces
/workspaces/[workspace_id]
```

Minimum new API surface:

```text
GET/POST   /api/workspace/workspaces
GET/PATCH  /api/workspace/workspaces/{workspace_id}
GET/POST   /api/workspace/workspace-blueprints
POST       /api/workspace/workspaces/{workspace_id}/compose
GET/POST   /api/workspace/workspaces/{workspace_id}/members
GET/POST   /api/workspace/workspaces/{workspace_id}/resources
GET/POST   /api/workspace/meetings
GET/POST   /api/workspace/resource-requests
```

### 4.4 Migrate

| Current | Target | Rule |
| --- | --- | --- |
| Project Center | Workspace Portal | Route alias first; copy/rename only after browser acceptance |
| Project record | Workspace or internal Project | Classify by business boundary; do not mechanically convert every Project |
| Project owner | Workspace owner | Migrate only when a Project becomes a Workspace |
| Project Department | Workspace business/organization association | Preserve original relationship and audit mapping |
| Project Task/Workflow/Artifact | Workspace internal execution | Add `workspace_id`; retain existing project/task identifiers |
| R&D/content run drawers | R&D/Content Workspace modules | Reuse execution APIs; remove universal visibility |
| Engineering Department | Business Engineering system department | Create canonical system identity; retain old R&D department separately if it is a real business department |
| Workflow template | Workspace module/template composition | Keep runtime template; reference it from Workspace Blueprint |

### 4.5 Preserve

| Preserve | Reason |
| --- | --- |
| `TerraShell`, shared primitives and accessibility behavior | Valid Company OS shell foundation |
| Trusted Gateway, Tenant Context, Local Owner identity | Security boundary remains correct |
| Company, Department, Employee and Affiliation services | Still required by Company OS |
| Task, Workflow, Artifact and execution control services | Valid internal execution substrate |
| Capability catalog, resolver, Model Gateway and AI Usage | Reusable Company Resource runtime |
| Knowledge, Memory and Context Package services | Reusable Workspace composition resources |
| Global Assistant root Provider/Host | Cross-product assistant remains global |
| `data/curis.sqlite` and migration ledger | Single database direction remains current |

## 5. Medium Priority

| Action | Area | Work |
| --- | --- | --- |
| Modify | CEO Office | Replace Project/Task-first metrics with business health, Workspace outcomes, decisions and resource gaps |
| Add | Business | Create company business-map read model and page |
| Modify | Organization | Mark Business Engineering as system-owned and non-deletable; distinguish business departments |
| Add | Meeting | Build company meeting collection, scheduling and decision follow-up; Workspace meetings default to members |
| Modify | Insight | Merge the useful Company Runtime view into operating radar; remove technical runtime framing |
| Add | Business Analysis | Add consultant deliverables and recommendations, not execution controls |
| Modify | Knowledge | Reframe as Knowledge & IP archive/exhibition with Workspace links and provenance |
| Add | Workspace renderer contract | Resolve modules/layout from Blueprint without a universal Dashboard schema |
| Modify | API client | Add Workspace/Meeting/Resource request methods to the existing dependency-free `workspaceFetch` layer |
| Modify | State | Keep server data authoritative; add only a scoped Workspace context and renderer state, no new global state dependency |

## 6. Low Priority

| Action | Area | Work |
| --- | --- | --- |
| Migrate | URLs | Maintain temporary redirects and route analytics until saved links are no longer used |
| Delete | Old labels and dead components | Remove only after repository reference checks and browser regression |
| Modify | Tests | Rename Project Center expectations after behavior migrates; keep execution unit tests |
| Add | Blueprint version history | Store revisions in the same Blueprint record/file; do not create parallel current files |
| Preserve | Historical documents | Archive with Deprecated status; never use them as current design authority |

## 7. Directory Target

This is a target map, not authorization to move files.

```text
frontend/
  app/
    ceo-office/
    business/
    organization/
    business-engineering/
    meeting/
    capability/
    insight/
    business-analysis/
    knowledge-ip/
    workspaces/
      page.js
      [workspace_id]/
        page.js
  components/
    company-os/
    workspaces/
      WorkspaceHost.js
      modules/
  lib/
    api.js
    workspaceDefinition.mjs

backend/app/
  workspace_blueprints.py
  workspace_service.py
  workspace_composition.py
  meeting_service.py
  resource_request_service.py
```

Do not create per-industry backend stacks. Industry variation belongs in
Workspace Blueprint definitions and modules that reuse shared services.

## 8. Migration Sequence and Gates

| Gate | Outcome | Coding status |
| --- | --- | --- |
| BR-0 Runtime Standard | ADR-0041, Gap Report and refactor plan reviewed | Required before Runtime design |
| BR-1 Runtime Blueprints | Ten primary module lifecycles, state machines and stage contracts reviewed | Blocked pending BR-0 |
| BR-2 Cross-runtime Closure | Meeting → Workspace feedback and all cross-module handoffs reviewed | Blocked pending BR-1 |
| BR-3 Simulation Design | One Business Runtime Simulation per module approved | Blocked pending BR-2 |
| G0 Product Definition | ADR-0040 and Blueprint 3.0 confirmed | Blocked pending BR-3 |
| G1 Data Contract | Workspace/Blueprint/Meeting/resource request schemas approved | Blocked pending G0 |
| G2 Compatibility | Existing Project/Task data mapping and rollback approved | Blocked pending G1 |
| G3 Company OS Shell | New primary navigation accepted in browser | Blocked pending implementation Issue |
| G4 Workspace Portal | List/create/open one Workspace accepted in browser | Blocked pending G3 |
| G5 First Workspace | One R&D or Content Workspace completes a real flow | Blocked pending G4 |
| G6 Independent Review | Quality verifies tenant, migration and real browser flow | Blocked pending G5 |

## 9. Explicit Non-Actions

- No business code, route, schema or API was changed by this report.
- No current Project or Task data is deleted.
- No second Workspace/Admin runtime is created.
- No universal industry-neutral Dashboard is proposed.
- No new frontend state-management dependency is required.
- No implementation may begin until every primary module Runtime Blueprint and
  Business Runtime Simulation plan passes Review, the Owner confirms the reset
  package, and a scoped Issue defines allowed files and transitions.
