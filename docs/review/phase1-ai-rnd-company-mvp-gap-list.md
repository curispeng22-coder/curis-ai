# Phase 1 AI R&D Company MVP Gap List

Status: Phase 1A backend foundation review

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace now has the contract basis to shift from Task-first execution toward an AI R&D Company OS where Company, Department, Project, Employee, Skill, and Tool form the backend product foundation.

## Current Kept Runtime

The following existing systems remain valid and must be preserved:

- Task persistence and execution substrate.
- Orchestrator.
- Tool Router.
- Tool Executor.
- Model Gateway Adapter.
- Credential Vault resolver.
- EmployeeTemplate / EmployeeInstance.
- DepartmentTemplate / DepartmentInstance.
- Workflow Runtime.
- tenant_private capability metadata.
- usage_event / audit_event / value_event.

## Product Entry Correction

Task must no longer be treated as the product main entry.

New intended entry hierarchy:

```text
CEO
  -> Company
    -> Project
      -> Department
        -> Employee / Skill / Tool
          -> Workflow / Task execution substrate
```

Task remains necessary for:

- Orchestrator correlation,
- execution persistence,
- tool/model invocation,
- usage_event correlation,
- audit/debug evidence.

Task should not remain the CEO-facing primary object after Phase 1 UI/API migration.

## Contract Outputs

| Contract | Path | Purpose |
| --- | --- | --- |
| Company Runtime Contract | `docs/contracts/company-runtime-contract.md` | Defines tenant company root and product entry aggregate. |
| Department Runtime Contract | `docs/contracts/department-runtime-contract.md` | Defines company department operating unit. |
| Project Runtime Contract | `docs/contracts/project-runtime-contract.md` | Defines CEO-facing work container above Task/Workflow. |
| Skill Runtime Contract | `docs/contracts/skill-runtime-contract.md` | Defines employee ability layer between role and capability. |
| Tool Runtime Contract | `docs/contracts/tool-runtime-contract.md` | Normalizes existing tool/capability runtime surface. |

## Backend Gaps To Fill

### P0 Backend Foundation

| Gap | Current State | Required Next |
| --- | --- | --- |
| CompanyRuntime persistence | Company is mostly a shell/id in existing employee/department records | Add tenant-scoped company runtime table/service/API. |
| ProjectRuntime persistence | WorkflowRun can link to Task, but no Project aggregate exists | Add project table/service/API and link Project -> WorkflowRun -> Task. |
| Task entry demotion | Task API remains direct product entry | Add Project-first creation flow; keep Task as internal substrate. |
| Company-scoped department listing | DepartmentInstance has company_id but Company root is not first-class | Expose company departments through CompanyRuntime APIs. |
| Runtime summary read model | Data exists across employees/workflows/usage but not as Company OS summary | Add read-only company/project summary projections. |

### P1 AI R&D Company Completeness

| Gap | Current State | Required Next |
| --- | --- | --- |
| SkillRuntime | EmployeeCapabilityBinding exists, but Skill is not modeled | Add SkillTemplate and EmployeeSkillBinding foundation. |
| ToolRuntime normalized view | Tool registry and tenant_private capability metadata are separate | Add read-only ToolRuntime projection over official/tenant_private tools. |
| Project status lifecycle | WorkflowRun has status; Project does not | Add Project status based on workflow/task state. |
| Project final report | WorkflowRun has final_report | Surface final report at ProjectRuntime. |
| Employee work context | Employee execution uses role/capability binding | Add project/company context to employee execution prompts only after gate. |

### P2 Product/API Migration

| Gap | Current State | Required Next |
| --- | --- | --- |
| CEO product entry | UI still exposes task creation heavily | Shift Workspace console to Company -> Project creation. |
| API compatibility | `POST /api/task` still exists | Keep for internal/debug compatibility; prefer `POST /api/workspace/projects`. |
| Usage attribution | usage_event has task/workflow/employee/capability fields | Add `project_id` only after shared/event contract if needed. |
| Audit attribution | workflow audit exists | Add company/project lifecycle audit events. |

## Explicit Non-Goals

Phase 1 AI R&D Company MVP must not implement:

- Billing / Pricing / Quota / Payment / Invoice.
- ROI dashboard or ROI calculation.
- Marketplace.
- content / investment / ecommerce departments.
- complex org chart UI.
- complex project management boards.
- direct provider SDK calls.
- plaintext credential storage.
- Workspace runtime `/api/platform/*` calls.

## Shared Contract Needs

Shared Contract / Gate is required before:

- Admin supplies official CompanyTemplate / DepartmentTemplate / EmployeeTemplate availability by plan/package.
- usage_event adds `company_id` or `project_id` as commercial-grade fields.
- Workspace enforces plan/quota/package limits.
- Marketplace skill/tool/company templates become executable.
- Company/Project lifecycle is exposed to Admin commercial configuration.

## Recommended Next Issues

1. `phase1a_company_project_runtime_backend`
   - Implement CompanyRuntime and ProjectRuntime tables/services/APIs.
   - Link Project to WorkflowRun and internal Task.
   - Do not change Tool Router, Model Gateway, Credential Vault, or Billing.

2. `phase1a_runtime_summary_read_model`
   - Add read-only Company/Project summaries over existing Department, Employee, Workflow, Usage, and Audit records.
   - No new execution behavior.

3. `phase1b_skill_runtime_foundation`
   - Add SkillTemplate and EmployeeSkillBinding metadata.
   - Keep execution through EmployeeCapabilityBinding and Tool Router.

4. `phase1b_tool_runtime_projection`
   - Add normalized ToolRuntime read model over official tools and tenant_private capabilities.
   - No provider or credential changes.

## Acceptance Direction

Phase 1 AI研发公司 MVP is ready to start backend implementation only after the above contracts are accepted as the new Workspace source of truth for Company OS runtime entry.
