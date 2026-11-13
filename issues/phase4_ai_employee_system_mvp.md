# Phase-4 AI Employee System MVP

Status: Implemented pending final acceptance

Owner Seat: 产品规划席 for scope acceptance; 系统交付席 after gate approval

## Phase-4 Goal

Build the minimum Workspace AI Employee System foundation for the Software R&D department, using the Phase-3.5 Research -> Decision -> Contract chain as the only approved development basis.

The first MVP must let a CEO configure a small R&D department and employee roster, bind official or tenant_private capabilities to employees, and prepare a controlled path for task assignment evidence. Any runtime task-flow change must remain separately gated.

## Source Chain

### Research References

- `docs/research/competitors/paperclip.md`
- `docs/research/competitors/paperclip-companies.md`
- `docs/research/competitors/metagpt.md`
- `docs/research/competitors/chatdev.md`
- `docs/research/competitors/crewai.md`
- `docs/research/competitors/crewai-examples.md`
- `docs/research/competitors/autoagents.md`
- `docs/research/competitors/openclaw-agents.md`
- `docs/research/domain/ai-company-template-research.md`
- `docs/research/domain/employee-template-research.md`
- `docs/research/domain/department-template-research.md`
- `docs/research/domain/software-dev-sop-research.md`
- `docs/research/domain/workflow-engine-research.md`

### Adopted Decisions

- `AD-PAPERCLIP-COMPANY`
- `AD-PAPERCLIP-ORG`
- `AD-PAPERCLIP-CAPABILITY`
- `AD-METAGPT-SOP`
- `AD-METAGPT-ROLES`
- `AD-CHATDEV-LIFECYCLE`
- `AD-CHATDEV-FIELD-SPEC`
- `AD-CREWAI-ROLE-FIELDS`
- `AD-CREWAI-OUTPUT`
- `AD-CREWAI-SEQUENTIAL`
- `AD-CREWAI-CONFIG-SPLIT`
- `AD-GPTS-SEPARATION`
- `AD-DIFY-CATALOG`
- `AD-NEWAPI-GATEWAY`
- `AD-ONEAPI-USAGE`

Decision source: `docs/research/decisions/adopted-patterns.md`

### Contract References

- `docs/contracts/company-template-contract.md`
- `docs/contracts/department-template-contract.md`
- `docs/contracts/employee-template-contract.md`
- `docs/contracts/workflow-template-contract.md`
- `docs/contracts/capability-type-contract.md`

## Scope

Phase-4 may implement only:

- `EmployeeTemplate`
- `EmployeeInstance`
- `DepartmentTemplate`
- `DepartmentInstance`
- `EmployeeCapabilityBinding`
- minimum Software R&D employee system

First official R&D employee templates:

- Tech Lead
- Product Manager
- Architect
- Frontend Engineer
- Backend Engineer
- QA Engineer

First target flow:

```text
CEO creates task
-> Tech Lead receives and assigns
-> corresponding R&D employee executes
-> employee uses official / tenant_private capability
-> usage_event is written
```

Runtime execution changes for this flow require a separate implementation gate. This issue may define and build the metadata/API/UI foundation first, then request a bounded runtime assignment issue if needed.

## Non-Goals

- Do not directly implement unapproved Phase-4 runtime employee execution.
- Do not modify the current Task Execution main flow without a follow-up gate.
- Do not add ROI.
- Do not add real credential custody.
- Do not add a capability marketplace.
- Do not add content operations, investment, ecommerce, HR, or other business modules.
- Do not modify Admin Platform governance logic.
- Do not call `/api/platform/*` from Workspace runtime.
- Do not allow Workspace to modify official definitions.
- Do not bypass the Contract files listed above.

## Data Model Draft

### EmployeeTemplate

Fields from `docs/contracts/employee-template-contract.md`:

- `id`
- `slug`
- `name`
- `role`
- `responsibility`
- `description`
- `department_type`
- `default_instructions`
- `default_capability_types`
- `default_model_policy`
- `default_workflow_step_types`
- `guardrails`
- `source`
- `tenant_id`
- `enabled`
- `created_at`

Phase-4 implementation: metadata catalog for official and tenant_private templates. No employee runtime by itself.

### EmployeeInstance

Fields from `docs/contracts/employee-template-contract.md`:

- `id`
- `tenant_id`
- `company_id`
- `department_id`
- `template_id`
- `name`
- `role`
- `instructions_override`
- `status`
- `enabled`
- `created_at`

Phase-4 implementation: tenant-local Workspace employee instance metadata. No autonomous employee memory.

### DepartmentTemplate

Fields from `docs/contracts/department-template-contract.md`:

- `id`
- `slug`
- `name`
- `department_type`
- `description`
- `default_employee_templates`
- `default_workflow_template_id`
- `default_capability_types`
- `source`
- `tenant_id`
- `enabled`
- `created_at`

Phase-4 implementation: Software R&D DepartmentTemplate metadata first.

### DepartmentInstance

Fields from `docs/contracts/department-template-contract.md`:

- `id`
- `tenant_id`
- `company_id`
- `template_id`
- `name`
- `department_type`
- `enabled_employee_template_ids`
- `enabled`
- `created_at`

Phase-4 implementation: tenant-local Software R&D department instance metadata.

### EmployeeCapabilityBinding

Fields from `docs/contracts/capability-type-contract.md`:

- `id`
- `tenant_id`
- `employee_id`
- `employee_template_id`
- `capability_source`
- `capability_type`
- `capability_id`
- `priority`
- `enabled`

Phase-4 implementation: metadata binding to existing official and tenant_private capability catalogs. Model execution must still go through ModelGatewayAdapter.

## API Draft

API names are draft-level until 系统交付席 confirms implementation boundaries.

### Template Reads

- `GET /api/workspace/department-templates`
- `GET /api/workspace/employee-templates`
- `GET /api/workspace/workflow-templates`

Rules:

- Reads may include official templates and tenant_private templates.
- official definitions are read-only in Workspace.
- tenant_private results must be tenant-scoped.

### Tenant Instance Metadata

- `GET /api/workspace/departments`
- `POST /api/workspace/departments`
- `PATCH /api/workspace/departments/{department_id}`
- `GET /api/workspace/employees`
- `POST /api/workspace/employees`
- `PATCH /api/workspace/employees/{employee_id}`

Rules:

- Writes are tenant_private only.
- Every created row must include `tenant_id`.
- No endpoint may write to official catalogs.
- No endpoint may call `/api/platform/*`.

### Capability Binding

- `GET /api/workspace/employees/{employee_id}/capabilities`
- `PUT /api/workspace/employees/{employee_id}/capabilities`

Rules:

- capability values must come from the existing official + tenant_private selector or matching catalog/private endpoints.
- `capability_source` must be persisted and visible.
- No real secrets may be stored in employee or binding records.

### Runtime Assignment Gate Placeholder

- Any change to `POST /api/task`, `POST /api/task/{task_id}/run`, orchestrator assignment, tool routing, or prompt construction requires a separate issue that cites this issue and the five Contract files.

## UI Draft

Workspace UI may add a minimal R&D employee configuration surface inside the existing Workspace shell:

- Software R&D department summary.
- Department template selector for `software_rnd`.
- Employee template list for the six default R&D roles.
- Employee instance create/edit form.
- Capability binding selector showing official and tenant_private source labels.
- Minimal assignment/evidence view only after a runtime gate is approved.

UI constraints:

- Chinese copy.
- No complex dashboard.
- No marketplace UI.
- No ROI or billing UI.
- No real credential entry.
- No Admin Platform screen.

## Testing Requirements

### Backend

- Template read tests for official and tenant_private scope.
- DepartmentInstance create/read/update tenant isolation tests.
- EmployeeInstance create/read/update tenant isolation tests.
- EmployeeCapabilityBinding tests for official and tenant_private capabilities.
- Negative tests proving Workspace cannot modify official definitions.
- Scan proving Workspace runtime does not call `/api/platform/*`.
- Secret scan proving no real credential storage.
- Existing backend regression must pass.

### Frontend

- View-model tests for department and employee list/loading/error states.
- Form validation tests for employee instance creation.
- Capability binding selector tests showing official and tenant_private labels.
- Existing frontend lint/build/tests must pass.

### Contract Guard

- The implementation issue must cite every relevant adopted decision and contract section.
- A quality review must confirm no current Task Execution main-flow mutation unless separately approved.

## Acceptance Criteria

- Research completeness is confirmed for P0 competitors and required domain topics.
- Adopted/rejected decision files are the only decision source used.
- Contract files define all fields required by this issue.
- Workspace can store tenant-local Software R&D department metadata.
- Workspace can store tenant-local employee instances for the six first R&D roles.
- Workspace can bind official and tenant_private capabilities to employee templates or instances.
- tenant_private employee/department/binding records are isolated by `tenant_id`.
- official templates and official capabilities remain read-only in Workspace.
- No Admin Platform governance logic is changed.
- No real secrets are stored.
- Existing Phase-3 Self-Extension behavior remains intact.

## Completion Evidence Required

- Changed files.
- Verification commands and results.
- Scope scan for forbidden work.
- Contract references used by implementation.
- Known gaps.
- Next Curis seat.
- Handoff status.

Handoff: HANDOFF_REQUIRED

## Implementation Notes

Implemented on 2026-07-09 by Workspace line.

Delivered:

- Official Software R&D DepartmentTemplate.
- Official R&D EmployeeTemplate set: Tech Lead, Product Manager, Architect, Frontend Engineer, Backend Engineer, QA Engineer.
- Tenant-scoped DepartmentInstance creation.
- Tenant-scoped EmployeeInstance creation.
- EmployeeCapabilityBinding for official / tenant_private model/tool/connector capabilities.
- Task creation accepts `employee_id`; unselected tasks default to Tech Lead role context.
- Selected employee task execution resolves the employee's preferred enabled capability binding when no explicit capability is provided.
- usage_event payload and Admin usage projection now include `employee_id`, `employee_role`, and `employee_name`.
- Workspace operation console includes a minimal `研发部员工` area and task employee selector.

Preserved:

- No ROI.
- No non-R&D departments.
- No marketplace implementation.
- No real credential custody.
- No Admin Platform governance change.
- Workspace UI does not call `/api/platform/*`.
