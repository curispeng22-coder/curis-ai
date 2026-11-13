# Company Template Contract

Status: Phase-3.5 contract

Source chain:

- Research: `docs/research/competitors/paperclip.md`, `docs/research/competitors/paperclip-companies.md`
- Domain: `docs/research/domain/ai-company-template-research.md`
- Decision: `docs/research/decisions/adopted-patterns.md`

Boundary: CompanyTemplate is a contract reserved for the future AI Company System. Phase-4 may reference it but must not implement company pack import/export or automatic company activation.

## Fields

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated id | official / tenant_private / marketplace | no | yes | Admin owns official/marketplace ids; Workspace may own tenant_private ids only after a later gate | Paperclip Companies | AD-PAPERCLIP-PACK |
| `slug` | string | yes | none | official / tenant_private / marketplace | no | yes | stable portable id; Workspace cannot mutate official slug | Paperclip / Paperclip Companies | AD-PAPERCLIP-COMPANY |
| `name` | string | yes | none | official / tenant_private / marketplace | no | yes | display metadata | Paperclip / Paperclip Companies | AD-PAPERCLIP-COMPANY |
| `description` | string | no | empty string | official / tenant_private / marketplace | no | yes | display metadata | Paperclip | AD-PAPERCLIP-COMPANY |
| `version` | string | no | `1.0.0` | official / tenant_private / marketplace | no | yes | Admin controls official/marketplace versioning | Paperclip Companies | AD-PAPERCLIP-PACK |
| `source` | enum: official / tenant_private / marketplace | yes | `official` for platform templates; `tenant_private` for tenant templates | official / tenant_private / marketplace | no | yes | source determines write authority | Paperclip Companies | AD-PAPERCLIP-PACK |
| `tenant_id` | string nullable | conditional | null | tenant_private | no | yes | required for tenant_private; null/platform for official | Paperclip Companies | AD-PAPERCLIP-PACK |
| `default_department_templates` | string[] | no | `[]` | official / tenant_private / marketplace | no | yes | references DepartmentTemplate ids only | Paperclip | AD-PAPERCLIP-ORG |
| `default_goals` | string[] | no | `[]` | official / tenant_private / marketplace | no | yes | goal context only; no execution behavior | Paperclip | AD-PAPERCLIP-COMPANY |
| `default_workflow_templates` | string[] | no | `[]` | official / tenant_private / marketplace | no | yes | references WorkflowTemplate ids only | MetaGPT / Paperclip Companies | AD-METAGPT-SOP |
| `governance_policy_ref` | string nullable | no | null | official / marketplace | no | yes | Admin governed only; Workspace cannot write policy refs | Paperclip | AD-PAPERCLIP-GATE |
| `capability_pack_refs` | string[] | no | `[]` | official / marketplace | no | yes | future pack references; not executable | Paperclip Companies / OpenClaw | AD-OPENCLAW-PACK |
| `enabled` | boolean | yes | true | official / tenant_private / marketplace | no | yes | Admin controls official/marketplace; Workspace controls tenant_private only after gate | Paperclip Companies | AD-PAPERCLIP-PACK |
| `created_at` | datetime | yes | current timestamp | official / tenant_private / marketplace | no | yes | system generated | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |

## Invariants

- CompanyTemplate cannot modify Task Execution.
- CompanyTemplate import/export is not approved in Phase-4.
- Marketplace CompanyTemplate requires Admin review and G3/security gate.
- Workspace cannot modify official CompanyTemplate definitions.
