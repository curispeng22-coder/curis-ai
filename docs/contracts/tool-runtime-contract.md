# Tool Runtime Contract

Status: Phase 1A backend foundation contract

Date: 2026-07-10

Owner: Workspace line

## Product Progress

Curis Workspace is preserving the existing Tool Router / Tool Executor while defining Tool Runtime as the company-level executable capability surface.

## Boundary

Tool Runtime wraps existing tool infrastructure and tenant-private capability metadata. It must not replace Model Gateway Adapter or Credential Vault.

Tool Runtime preserves:

- existing `tools` registry,
- Tool Router and Tool Executor,
- official tool catalog,
- tenant_private capability metadata,
- Model Gateway Adapter for model calls,
- Credential Vault resolver for secrets.

Tool Runtime does not implement:

- marketplace,
- billing,
- direct provider SDK calls outside approved adapters,
- unmanaged credential storage,
- complex tool orchestration beyond existing Workflow Runtime.

## ToolRuntime Fields

| Field | Type | Required | Default | Source Range | Phase 1A | Admin / Workspace Boundary |
| --- | --- | --- | --- | --- | --- | --- |
| `tool_runtime_id` | string | yes | generated id | official / tenant_private / marketplace | foundation | runtime-facing tool id |
| `tenant_id` | string nullable | conditional | null/platform | tenant_private | foundation | required for tenant_private |
| `company_id` | string nullable | no | null | tenant_private | reserve | optional company scope |
| `name` | string | yes | none | official / tenant_private / marketplace | already present/foundation | display and routing name |
| `tool_type` | string | yes | existing type | official / tenant_private / marketplace | already present/foundation | tool classification |
| `description` | text | no | empty string | official / tenant_private / marketplace | already present/foundation | display metadata |
| `entry` | string | no | empty string | official / tenant_private | already present/foundation | internal entry ref; never secret |
| `capability_source` | enum | yes | `official` | official / tenant_private / marketplace | foundation | source authority |
| `capability_id` | string | yes | tool name/id | official / tenant_private / marketplace | foundation | joins usage_event capability id |
| `credential_ref` | string nullable | no | null | tenant_private | already supported by private capability binding | reference only; no plaintext |
| `created_from_template_id` | string nullable | no | null | official / tenant_private | implement lineage | optional future ToolTemplate lineage; no template runtime is introduced |
| `status` | enum | yes | `active` | official / tenant_private / marketplace | foundation | `active` / `disabled` / `archived` |
| `created_at` | datetime | yes | current timestamp | official / tenant_private / marketplace | foundation | system generated |
| `updated_at` | datetime | yes | current timestamp | official / tenant_private / marketplace | foundation | system generated |

## Runtime Rules

- Tool Runtime is selected through EmployeeCapabilityBinding, SkillRuntime, WorkflowStep, or internal Tool Router.
- Model calls must continue through Model Gateway Adapter.
- tenant_private tool/connector credentials must resolve through Credential Vault only.
- usage_event must retain `capability_source`, `capability_type`, `capability_id`, model/token/cost fields when applicable.
- official tool definitions are read-only from Workspace.
- EmployeeToolBinding is a filtered projection of canonical `EmployeeCapabilityBinding` records whose `capability_type` is `tool`; it cannot become a second permission authority.

## API Contract Draft

| API | Purpose | Phase 1A |
| --- | --- | --- |
| `GET /api/catalog/tools` | read official tool catalog | already implemented |
| `GET /api/workspace/capabilities/selector` | read official + tenant_private capabilities | already implemented |
| `GET /api/workspace/tools/runtime` | read normalized ToolRuntime view | foundation |
| `GET /api/workspace/tools/runtime/{tool_runtime_id}` | get ToolRuntime detail | foundation |

## Invariants

- Tool Runtime cannot store plaintext secrets.
- Tool Runtime cannot call Admin `/api/platform/*`.
- Tool Runtime cannot calculate price/quota/billing.
- Tool Runtime cannot bypass Credential Vault when credential_ref is present.
- Tool Runtime cannot mutate official catalog definitions.
