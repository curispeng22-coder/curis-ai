# Employee Template Contract

Status: Phase-3.5 contract

Source chain:

- Research: `docs/research/competitors/crewai.md`, `docs/research/competitors/metagpt.md`, `docs/research/competitors/chatdev.md`, `docs/research/competitors/gpts.md`
- Domain: `docs/research/domain/employee-template-research.md`
- Decision: `docs/research/decisions/adopted-patterns.md`

Boundary: Phase-4 may implement EmployeeTemplate metadata for the Software R&D department. Employee runtime, employee memory, automatic hiring, and direct prompt routing remain blocked unless a later issue/gate approves them.

## EmployeeTemplate Fields

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated id | official / tenant_private / marketplace | implement | no | Admin owns official/marketplace; Workspace owns tenant_private | CrewAI / MetaGPT | AD-METAGPT-ROLES |
| `slug` | string | yes | none | official / tenant_private / marketplace | implement | no | stable template id; official read-only in Workspace | CrewAI Examples | AD-CREWAI-CONFIG-SPLIT |
| `name` | string | yes | none | official / tenant_private / marketplace | implement | no | CEO-facing display | MetaGPT / ChatDev | AD-METAGPT-ROLES |
| `role` | string | yes | none | official / tenant_private / marketplace | implement | no | CEO-readable role label | CrewAI | AD-CREWAI-ROLE-FIELDS |
| `responsibility` | string | yes | none | official / tenant_private / marketplace | implement | no | CEO-language mapping of CrewAI `goal`; not social roleplay | CrewAI / MetaGPT | AD-CREWAI-ROLE-FIELDS |
| `description` | string | no | empty string | official / tenant_private / marketplace | implement | no | display/help text | CrewAI Examples | AD-CREWAI-CONFIG-SPLIT |
| `department_type` | string | yes | `software_rnd` | official / tenant_private / marketplace | implement | no | first approved value is `software_rnd` | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `default_instructions` | text | yes | role-specific instruction text | official / tenant_private / marketplace | metadata only | no | hidden/default role instructions; 须遵守《CEO 汇报标准》(结论→原因→建议, 中文白话, 见 ceo-reporting-standard.md); not direct runtime injection without a later runtime gate | GPTs / CrewAI | AD-GPTS-SEPARATION |
| `default_capability_types` | string[] | yes | `["model"]` plus role-specific tool/connector needs | official / tenant_private / marketplace | metadata only | no | values from capability-type contract | GPTs / Paperclip | AD-PAPERCLIP-CAPABILITY |
| `default_model_policy` | object | no | `{}` | official / tenant_private / marketplace | metadata only | no | policy only; no provider credential | GPTs / LiteLLM | AD-LITELLM-ABSTRACTION |
| `default_workflow_step_types` | string[] | no | `[]` | official / tenant_private / marketplace | metadata only | yes | links role to SOP steps; no automatic step execution | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `guardrails` | string[] | no | `[]` | official / tenant_private / marketplace | no | yes | future review/safety metadata | OpenClaw / AutoAgents | AD-OPENCLAW-PACK |
| `source` | enum: official / tenant_private / marketplace | yes | `official` for platform templates; `tenant_private` for tenant-created templates | official / tenant_private / marketplace | implement | no | source determines write authority | Paperclip Companies / Dify | AD-DIFY-CATALOG |
| `tenant_id` | string nullable | conditional | null | tenant_private | implement | no | required for tenant_private | Paperclip Companies | AD-PAPERCLIP-PACK |
| `enabled` | boolean | yes | true | official / tenant_private / marketplace | implement | no | lifecycle metadata only | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |
| `created_at` | datetime | yes | current timestamp | official / tenant_private / marketplace | implement | no | system generated | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |

## EmployeeInstance Fields

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated id | tenant_private | implement | no | Workspace-owned tenant-local employee instance | Paperclip org chart | AD-PAPERCLIP-ORG |
| `tenant_id` | string | yes | current tenant | tenant_private | implement | no | tenant isolation boundary | Paperclip Companies | AD-PAPERCLIP-PACK |
| `company_id` | string nullable | no | current Workspace company shell id when available | tenant_private | implement metadata | no | local/demo Workspace company scope only | Paperclip | AD-PAPERCLIP-COMPANY |
| `department_id` | string | yes | selected Software R&D department instance id | tenant_private | implement | no | references DepartmentInstance | Paperclip / MetaGPT | AD-PAPERCLIP-ORG |
| `template_id` | string | yes | selected EmployeeTemplate id | official / tenant_private / marketplace | implement | no | may reference official read-only template or tenant_private template | CrewAI Examples | AD-CREWAI-CONFIG-SPLIT |
| `created_from_template_id` | string | yes | selected EmployeeTemplate id | official / tenant_private / marketplace | implement lineage | no | immutable template-origin record for future migration; not a second template authority | Paperclip Companies | AD-PAPERCLIP-PACK |
| `name` | string | yes | template `name` | tenant_private | implement | no | CEO-facing local employee name | CrewAI | AD-CREWAI-ROLE-FIELDS |
| `role` | string | yes | template `role` | tenant_private | implement | no | copied/display role metadata | CrewAI | AD-CREWAI-ROLE-FIELDS |
| `instructions_override` | text nullable | no | null | tenant_private | implement metadata | yes | override is stored as metadata only; no prompt injection without later gate | GPTs | AD-GPTS-SEPARATION |
| `status` | enum: idle / assigned / disabled | yes | `idle` | tenant_private | implement metadata | no | status display only; no autonomous runtime | ChatDev / MetaGPT | AD-CHATDEV-LIFECYCLE |
| `enabled` | boolean | yes | true | tenant_private | implement | no | lifecycle metadata only | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |
| `created_at` | datetime | yes | current timestamp | tenant_private | implement | no | system generated | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |

## First Official R&D Templates

| Template | Role | Default Step |
| --- | --- | --- |
| Tech Lead | technical coordinator | task breakdown / report |
| Product Manager | product scope owner | requirement understanding |
| Architect | technical boundary owner | architecture design |
| Frontend Engineer | frontend delivery | frontend coding |
| Backend Engineer | backend delivery | backend coding |
| QA Engineer | verification owner | testing/report evidence |

## Invariants

- EmployeeTemplate is not EmployeeInstance.
- EmployeeTemplate cannot execute tasks by itself.
- EmployeeTemplate cannot store real secrets.
- EmployeeTemplate cannot directly call providers or tools.
- Capability access must go through CapabilityBinding.
