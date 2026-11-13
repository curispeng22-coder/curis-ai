# Capability Type Contract

Status: Phase-3.5 contract

Source chain:

- Research: `docs/research/competitors/dify.md`, `docs/research/competitors/coze.md`, `docs/research/competitors/new-api.md`, `docs/research/competitors/one-api.md`, `docs/research/competitors/litellm.md`, `docs/research/competitors/openclaw-agents.md`, `docs/research/competitors/gpts.md`
- Domain: `docs/research/domain/capability-catalog-research.md`, `docs/research/domain/model-gateway-research.md`, `docs/research/domain/capability-marketplace-research.md`
- Decision: `docs/research/decisions/adopted-patterns.md`

Boundary: CapabilityType remains the shared vocabulary for what employees/workflows may bind to. It must not be expanded to templates in Phase-4.

## Capability Types

| Value | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `model` | enum value | yes | built-in allowed value | official / tenant_private / marketplace | implement | no | official model catalog from Admin; tenant_private model from Workspace; all execution through ModelGatewayAdapter | New API / LiteLLM | AD-NEWAPI-GATEWAY |
| `tool` | enum value | yes | built-in allowed value | official / tenant_private / marketplace | implement | no | official tool catalog from Admin; tenant_private tool from Workspace | Paperclip / OpenClaw | AD-PAPERCLIP-CAPABILITY |
| `connector` | enum value | yes | built-in allowed value | official / tenant_private / marketplace | implement | no | official connector catalog from Admin; tenant_private connector from Workspace | GPTs / Coze / Dify | AD-GPTS-ACTIONS |

## CapabilityBinding Fields

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated id | official / tenant_private / marketplace | implement metadata | no | binding id | Paperclip | AD-PAPERCLIP-CAPABILITY |
| `tenant_id` | string | yes | current tenant | tenant_private / tenant usage | implement metadata | no | tenant isolation | Paperclip Companies | AD-PAPERCLIP-PACK |
| `employee_id` | string | conditional | null | tenant_private | implement if EmployeeInstance is implemented | no | references EmployeeInstance; tenant-local only | Paperclip org chart | AD-PAPERCLIP-ORG |
| `employee_template_id` | string | conditional | null | official / tenant_private / marketplace | implement metadata | no | template-level default binding | CrewAI Examples | AD-CREWAI-CONFIG-SPLIT |
| `capability_source` | enum: official / tenant_private / marketplace | yes | `official` | official / tenant_private / marketplace | implement | no | source determines authority | Dify / Paperclip | AD-DIFY-CATALOG |
| `capability_type` | enum: model / tool / connector | yes | `model` | official / tenant_private / marketplace | implement | no | no `template` type | Coze / Dify | AD-COZE-SURFACES |
| `capability_id` | string | yes | none | official / tenant_private / marketplace | implement | no | points to catalog/private capability id | GPTs / OpenClaw | AD-PAPERCLIP-CAPABILITY |
| `priority` | int | no | 100 | official / tenant_private / marketplace | implement metadata | no | lower number may mean preferred; no automatic optimization | Paperclip / CrewAI | AD-PAPERCLIP-CAPABILITY |
| `enabled` | boolean | yes | true | official / tenant_private / marketplace | implement metadata | no | lifecycle metadata | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |

## Model Gateway Measurement Fields

These fields remain in usage_event and are required for model-backed execution:

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `tenant_id` | string | yes | current tenant | official / tenant_private / marketplace | already implemented | no | Admin can query by tenant; Workspace writes usage | One API / New API | AD-ONEAPI-USAGE |
| `task_id` | string | yes | current task id | official / tenant_private / marketplace | already implemented | no | Workspace execution correlation | One API | AD-ONEAPI-USAGE |
| `model_gateway_id` | string | yes for model | configured gateway id | official / tenant_private | already implemented | no | gateway metadata from Admin or approved private config | New API / LiteLLM | AD-NEWAPI-GATEWAY |
| `model_name` | string | yes for model | selected model name | official / tenant_private | already implemented | no | model actually called | New API / One API | AD-ONEAPI-USAGE |
| `prompt_tokens` | int | yes for model | 0 when provider omits usage | official / tenant_private / marketplace | already implemented | no | usage metric | One API | AD-ONEAPI-USAGE |
| `completion_tokens` | int | yes for model | 0 when provider omits usage | official / tenant_private / marketplace | already implemented | no | usage metric | One API | AD-ONEAPI-USAGE |
| `total_tokens` | int | yes for model | prompt + completion | official / tenant_private / marketplace | already implemented | no | usage metric | One API | AD-ONEAPI-USAGE |
| `estimated_cost` | number | yes | 0 | official / tenant_private / marketplace | already implemented | no | estimate only; not billing | One API | AD-ONEAPI-USAGE |
| `status` | string | yes | execution status | official / tenant_private / marketplace | already implemented | no | success/failure state | One API | AD-ONEAPI-USAGE |

## Invariants

- Do not add `employee_template`, `department_template`, or `company_template` to capability_type.
- Templates are separate catalogs, not capabilities.
- Workspace must not call `/api/platform/*`.
- Workspace must not modify official capabilities.
- Real credentials remain outside templates and use `credential_ref` only when approved.
