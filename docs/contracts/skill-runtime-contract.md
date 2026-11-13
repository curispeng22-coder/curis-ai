# Skill Runtime Contract

Status: Phase 1A backend foundation contract

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace is defining Skill as the reusable employee ability layer between employee roles and concrete tools/models/connectors.

## Boundary

Skill Runtime is not a new provider integration and not a direct execution engine. It is a controlled binding layer that lets AI employees declare what they can do and which capabilities they may use.

Skill Runtime preserves:

- EmployeeTemplate / EmployeeInstance,
- EmployeeCapabilityBinding,
- official / tenant_private capability catalogs,
- Tool Router / Tool Executor,
- Model Gateway Adapter,
- Credential Vault.

Skill Runtime does not implement:

- autonomous skill generation,
- marketplace skill sales,
- unmanaged prompt injection,
- direct provider SDK calls,
- real secret storage.

## SkillTemplate Fields

| Field | Type | Required | Default | Source Range | Phase 1A | Admin / Workspace Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `skill_template_id` | string | yes | generated id | official / tenant_private / marketplace | reserve/foundation | Admin owns official/marketplace; Workspace owns tenant_private |
| `slug` | string | yes | none | official / tenant_private / marketplace | reserve | stable id |
| `name` | string | yes | none | official / tenant_private / marketplace | foundation | CEO-readable skill name |
| `description` | text | no | empty string | official / tenant_private / marketplace | foundation | display metadata |
| `skill_type` | enum | yes | `analysis` | official / tenant_private / marketplace | foundation | `planning` / `analysis` / `architecture` / `frontend` / `backend` / `qa` / `tool_operation` |
| `default_capability_types` | string[] | yes | `["model"]` | official / tenant_private / marketplace | foundation | values from Capability Type Contract |
| `default_tool_refs` | string[] | no | `[]` | official / tenant_private / marketplace | reserve | references ToolRuntime ids or catalog ids |
| `instruction_excerpt` | text nullable | no | null | official / tenant_private | implement bounded guidance | sanitized, size-bounded non-authoritative guidance; no secret, credential, tool-selection, or routing directive |
| `instruction_ref` | string nullable | no | null | official / tenant_private | future reserve | reference-only future field; never resolved into raw secret material |
| `source` | enum | yes | `official` | official / tenant_private / marketplace | foundation | source controls write authority |
| `tenant_id` | string nullable | conditional | null/platform | tenant_private | foundation | required for tenant_private |
| `status` | enum | yes | `active` | official / tenant_private / marketplace | foundation | `draft` / `active` / `disabled` / `archived` |
| `created_at` | datetime | yes | current timestamp | official / tenant_private / marketplace | foundation | system generated |
| `updated_at` | datetime | yes | current timestamp | official / tenant_private / marketplace | foundation | system generated |

## EmployeeSkillBinding Fields

| Field | Type | Required | Default | Source Range | Phase 1A | Admin / Workspace Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `binding_id` | string | yes | generated id | tenant_private | foundation | Workspace-owned tenant binding |
| `tenant_id` | string | yes | current tenant | tenant_private | foundation | tenant isolation |
| `employee_id` | string | yes | none | tenant_private | foundation | references EmployeeInstance |
| `skill_template_id` | string | yes | none | official / tenant_private / marketplace | foundation | references SkillTemplate |
| `capability_binding_ids` | string[] | no | `[]` | tenant_private | foundation | references EmployeeCapabilityBinding |
| `priority` | integer | no | 100 | tenant_private | foundation | lower priority preferred |
| `enabled` | boolean | yes | true | tenant_private | foundation | lifecycle metadata |
| `created_at` | datetime | yes | current timestamp | tenant_private | foundation | system generated |

## Runtime Rules

- Employee owns skills; skills reference allowed capabilities.
- Skill cannot execute without an EmployeeRuntime and an allowed capability binding.
- Skill cannot store plaintext prompts that contain secrets.
- Skill can provide bounded employee guidance, but Tool Router remains the execution selector and skill text cannot select tools, models, or credentials.
- Skill may produce usage_event attribution later only through existing Task/Workflow execution.

## API Contract Draft

| API | Purpose | Phase 1A |
| --- | --- | --- |
| `GET /api/workspace/skills/templates` | list skill templates | foundation |
| `POST /api/workspace/skills/templates` | create tenant-private skill metadata | foundation |
| `GET /api/workspace/employees/{employee_id}/skills` | list employee skill bindings | foundation |
| `PUT /api/workspace/employees/{employee_id}/skills` | set employee skill bindings | foundation |

## Invariants

- Skill is not a capability type.
- Skill is not a Tool.
- Skill cannot bypass EmployeeCapabilityBinding.
- Skill cannot call `/api/platform/*`.
- Skill cannot contain or expose credentials.
