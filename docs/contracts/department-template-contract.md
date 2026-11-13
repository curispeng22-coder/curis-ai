# Department Template Contract

Status: Phase-3.5 contract

Source chain:

- Research: `docs/research/competitors/paperclip-companies.md`, `docs/research/competitors/metagpt.md`, `docs/research/competitors/chatdev.md`
- Domain: `docs/research/domain/department-template-research.md`
- Decision: `docs/research/decisions/adopted-patterns.md`

Boundary: Phase-4 may implement Software R&D DepartmentTemplate metadata. It must not implement multi-department expansion or autonomous department execution.

## Fields

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated id | official / tenant_private / marketplace | implement | no | Admin owns official/marketplace; Workspace owns tenant_private | Paperclip Companies | AD-PAPERCLIP-ORG |
| `slug` | string | yes | none | official / tenant_private / marketplace | implement | no | stable id; official read-only in Workspace | Paperclip Companies | AD-PAPERCLIP-ORG |
| `name` | string | yes | none | official / tenant_private / marketplace | implement | no | CEO-facing display metadata | Paperclip / MetaGPT | AD-PAPERCLIP-ORG |
| `department_type` | string | yes | `software_rnd` for first official department | official / tenant_private / marketplace | implement | no | first approved value is `software_rnd`; new department types require later issue | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `description` | string | no | empty string | official / tenant_private / marketplace | implement | no | display/help metadata | Paperclip Companies | AD-PAPERCLIP-ORG |
| `default_employee_templates` | string[] | yes | six R&D employee template ids for `software_rnd` | official / tenant_private / marketplace | implement | no | references EmployeeTemplate ids; no employee execution by itself | MetaGPT / ChatDev | AD-METAGPT-ROLES |
| `default_workflow_template_id` | string nullable | no | null | official / tenant_private / marketplace | metadata only | yes | reference only; no workflow engine | MetaGPT / CrewAI | AD-METAGPT-SOP |
| `default_capability_types` | string[] | no | `["model","tool","connector"]` | official / tenant_private / marketplace | metadata only | no | allowed values from capability-type contract | Paperclip / GPTs | AD-PAPERCLIP-CAPABILITY |
| `source` | enum: official / tenant_private / marketplace | yes | `official` for platform templates; `tenant_private` for tenant-created templates | official / tenant_private / marketplace | implement | no | source determines write authority | Paperclip Companies / Dify | AD-DIFY-CATALOG |
| `tenant_id` | string nullable | conditional | null | tenant_private | implement | no | required for tenant_private; official is platform/global | Paperclip Companies | AD-PAPERCLIP-PACK |
| `enabled` | boolean | yes | true | official / tenant_private / marketplace | implement | no | lifecycle metadata only | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |
| `created_at` | datetime | yes | current timestamp | official / tenant_private / marketplace | implement | no | system generated | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |

## First Official Department

```text
department_type: software_rnd
default employees:
  - Tech Lead
  - Product Manager
  - Architect
  - Frontend Engineer
  - Backend Engineer
  - QA Engineer
```

## DepartmentInstance Fields

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated id | tenant_private | implement | no | Workspace-owned tenant-local department instance | Paperclip org chart | AD-PAPERCLIP-ORG |
| `tenant_id` | string | yes | current tenant | tenant_private | implement | no | tenant isolation boundary | Paperclip Companies | AD-PAPERCLIP-PACK |
| `company_id` | string nullable | no | current Workspace company shell id when available | tenant_private | implement metadata | no | local/demo Workspace company scope only | Paperclip | AD-PAPERCLIP-COMPANY |
| `template_id` | string | yes | Software R&D DepartmentTemplate id | official / tenant_private / marketplace | implement | no | may reference official read-only template or tenant_private template | Paperclip Companies | AD-PAPERCLIP-ORG |
| `name` | string | yes | template `name` | tenant_private | implement | no | CEO-facing local department name | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `department_type` | string | yes | template `department_type` | tenant_private | implement | no | first approved value is `software_rnd` | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `enabled_employee_template_ids` | string[] | yes | template `default_employee_templates` | tenant_private | implement | no | controls available R&D employee instances; no execution by itself | MetaGPT / ChatDev | AD-METAGPT-ROLES |
| `enabled` | boolean | yes | true | tenant_private | implement | no | lifecycle metadata only | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |
| `created_at` | datetime | yes | current timestamp | tenant_private | implement | no | system generated | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |

## Invariants

- DepartmentTemplate is metadata and does not execute tasks.
- Phase-4 does not add content, investment, ecommerce, HR, or cross-department routing.
- Workspace cannot modify official DepartmentTemplate definitions.
- tenant_private DepartmentTemplate must stay tenant-scoped.
