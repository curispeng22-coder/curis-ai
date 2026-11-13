# Workflow Template Contract

Status: Phase-3.5 contract

Source chain:

- Research: `docs/research/competitors/metagpt.md`, `docs/research/competitors/chatdev.md`, `docs/research/competitors/crewai.md`, `docs/research/competitors/crewai-examples.md`
- Domain: `docs/research/domain/software-dev-sop-research.md`, `docs/research/domain/workflow-engine-research.md`
- Decision: `docs/research/decisions/adopted-patterns.md`

Boundary: Phase-4 may reserve workflow/SOP metadata. A full workflow engine, automatic Task -> Workflow expansion, and employee step execution remain blocked.

## WorkflowTemplate Fields

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated id | official / tenant_private / marketplace | metadata only | yes | Admin owns official/marketplace; Workspace owns tenant_private after later gate | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `slug` | string | yes | none | official / tenant_private / marketplace | metadata only | yes | stable id; official read-only in Workspace | CrewAI Examples | AD-CREWAI-CONFIG-SPLIT |
| `name` | string | yes | none | official / tenant_private / marketplace | metadata only | yes | display metadata | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `description` | string | no | empty string | official / tenant_private / marketplace | metadata only | yes | display metadata | MetaGPT / CrewAI | AD-METAGPT-SOP |
| `department_type` | string | yes | `software_rnd` | official / tenant_private / marketplace | metadata only | yes | first target is `software_rnd` | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `process_type` | enum: sequential / gated / hierarchical | yes | `sequential` | official / tenant_private / marketplace | metadata only | yes | Phase-4 baseline is sequential only; no engine | CrewAI | AD-CREWAI-SEQUENTIAL |
| `step_templates` | string[] | yes | six R&D step template ids | official / tenant_private / marketplace | metadata only | yes | ordered WorkflowStepTemplate ids only | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `source` | enum: official / tenant_private / marketplace | yes | `official` for platform templates; `tenant_private` for tenant templates | official / tenant_private / marketplace | metadata only | yes | source determines write authority | Dify / Paperclip Companies | AD-DIFY-CATALOG |
| `tenant_id` | string nullable | conditional | null | tenant_private | metadata only | yes | tenant scope | Paperclip Companies | AD-PAPERCLIP-PACK |
| `enabled` | boolean | yes | true | official / tenant_private / marketplace | metadata only | yes | lifecycle metadata | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |
| `created_at` | datetime | yes | current timestamp | official / tenant_private / marketplace | metadata only | yes | system generated | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |

## WorkflowStepTemplate Fields

| Field | Type | Required | Default | Source Range | Phase-4 | Reserved Only | Admin / Workspace Boundary | Research Source | Adopted Decision |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `id` | string | yes | generated id | official / tenant_private / marketplace | metadata only | yes | template step id | CrewAI Examples | AD-CREWAI-CONFIG-SPLIT |
| `workflow_template_id` | string | yes | parent workflow id | official / tenant_private / marketplace | metadata only | yes | parent workflow reference only | MetaGPT | AD-METAGPT-SOP |
| `step_type` | string | yes | none | official / tenant_private / marketplace | metadata only | yes | e.g. `requirement_understanding`; no automatic execution | MetaGPT / ChatDev | AD-METAGPT-SOP |
| `name` | string | yes | none | official / tenant_private / marketplace | metadata only | yes | display name | CrewAI Examples | AD-CREWAI-CONFIG-SPLIT |
| `description` | string | no | empty string | official / tenant_private / marketplace | metadata only | yes | step purpose | MetaGPT / CrewAI | AD-CREWAI-OUTPUT |
| `owner_employee_template_id` | string | yes | matching R&D employee template id | official / tenant_private / marketplace | metadata only | yes | owner template reference only | Paperclip Companies / MetaGPT | AD-PAPERCLIP-GATE |
| `input_contract` | object/text | no | `{}` | official / tenant_private / marketplace | metadata only | yes | expected input shape | ChatDev / CrewAI | AD-CHATDEV-FIELD-SPEC |
| `output_contract` | object/text | yes | evidence checklist for the step | official / tenant_private / marketplace | metadata only | yes | expected output/evidence | CrewAI | AD-CREWAI-OUTPUT |
| `required_capability_types` | string[] | no | `["model"]` | official / tenant_private / marketplace | metadata only | yes | model/tool/connector only | Coze / GPTs | AD-COZE-SURFACES |
| `context_step_ids` | string[] | no | `[]` | official / tenant_private / marketplace | metadata only | yes | prior step dependencies | ChatDev | AD-CHATDEV-LIFECYCLE |
| `max_iterations` | int | no | 1 | official / tenant_private / marketplace | metadata only | yes | bounded review loop only | ChatDev | AD-CHATDEV-LIFECYCLE |
| `next_step_ids` | string[] | no | `[]` | official / tenant_private / marketplace | metadata only | yes | future workflow graph | ChatDev | AD-CHATDEV-LIFECYCLE |
| `enabled` | boolean | yes | true | official / tenant_private / marketplace | metadata only | yes | lifecycle metadata | ChatDev schema metadata | AD-CHATDEV-FIELD-SPEC |

## First R&D SOP Contract

```text
requirement_understanding -> Product Manager
task_breakdown -> Tech Lead
architecture_design -> Architect
coding -> Frontend Engineer / Backend Engineer
testing -> QA Engineer
report -> Tech Lead / Product Manager
```

## Official Workflow Content Binding（官方 Workflow 内容绑定 · Phase-1）

Phase-1 Asset Factory Consolidation（Gate C/D/E/F）把上述研发 SOP 以 **`wl_` 前缀的 `WorkflowContent`** 实体**折叠进 TemplateCatalog**（Variant B：目录项而非独立引擎），落表于 `backend/app/database.py` 的 `workflow_contents` 表。本绑定**仅承载元数据**，不实现工作流引擎、不触发自动执行（与本契约 Invariants 一致）。

### WorkflowContent 字段（与 `workflow_contents` 表对齐）

| 字段 | 类型 | 必填 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| `workflow_content_id` | string | 是 | — | 主键，`wl_` 前缀，纳入 9 类模板 ID 命名空间 |
| `name` | string | 是 | — | 展示名（如「AI 研发软件开发生命周期 SOP」） |
| `workflow_template_ref` | string | 否 | `''` | 指向本契约 `WorkflowTemplate.slug`（如 `software_dev_sop`）的引用；`wl_*` 内容绑定到某官方 SOP 模板 |
| `pack` | enum | 是 | `ai_rd` | 归属 pack：`ai_rd` / `ai_content` / `ai_commercial` |
| `owner_roles_json` | string[] | 否 | `[]` | 负责角色（对齐 EmployeeTemplate role，如 `["product_manager","tech_lead","architect","backend_engineer","frontend_engineer","qa_engineer"]`） |
| `step_templates_json` | string[] | 否 | `[]` | 有序步骤模板 id 列表（复用本契约 First R&D SOP Contract 的 6 步：`requirement_understanding → task_breakdown → architecture_design → coding → testing → report`） |
| `source_attribution` | enum | 否 | `Curis internal` | 内容来源归属（6 值生态：`Curis internal` / `curis_lab` / `partner` / `open_source` / `tenant` / `community`） |
| `version` | string | 否 | `1.0.0` | SemVer |
| `status` | enum | 否 | `active` | `draft` / `active` / `disabled` / `archived` |
| `source` | enum | 否 | `official` | `official` / `tenant_private` / `marketplace` |
| `tenant_id` | string | 否 | `platform` | 租户域；`platform` 为官方内容，对所有租户可见 |
| `enabled` | boolean | 否 | `1` | 生命周期标志 |

### 绑定规则

- **内容折叠进目录**：`wl_*` 作为第 9 类 `TemplateCatalogEntry` 输出（`template_id` / `version` / `name` / `description` / `source` / `status` / `metadata`），由 `catalog_fold` 服务投影，与其它 8 类同源。
- **引用而非内嵌**：`workflow_template_ref` 指向既有 `WorkflowTemplate`（`slug`），`owner_roles` / `step_templates` 仅存引用 id，不重复定义步骤体（单一真相源）。
- **无执行语义**：`WorkflowContent` 仅作目录/作者数据；实例化与步骤执行仍属后续 gate（与本契约 Invariants 一致），本期不触发任何 Task 流变更。
- **授权写入**：仅平台 Admin 可写官方 `wl_*` 内容（`_require_platform_admin`）；`tenant_private` 须后续 gate 解禁。

### 示例（ccp_ai_software_company 串联的 6 条研发 SOP）

```json
{
  "workflow_content_id": "wl_ai_rd_software_dev_sop",
  "name": "AI 研发·软件开发生命周期 SOP",
  "workflow_template_ref": "software_dev_sop",
  "pack": "ai_rd",
  "owner_roles_json": ["product_manager","tech_lead","architect","backend_engineer","frontend_engineer","qa_engineer"],
  "step_templates_json": ["requirement_understanding","task_breakdown","architecture_design","coding","testing","report"],
  "source_attribution": "Curis internal",
  "version": "1.0.0",
  "status": "active",
  "source": "official"
}
```

## Invariants

- WorkflowTemplate is not a workflow engine.
- No automatic step execution in Phase-4.
- No arbitrary Python/code nodes.
- No majority voting or unbounded reflection loop.
- No current Task Execution main-flow mutation.
