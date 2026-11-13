# Adopted Research Patterns

Status: Phase-3.5 Research -> Decision -> Contract record

Rule: only decisions listed here may enter `docs/contracts/*`. Contracted content still cannot enter development until a follow-up issue cites the relevant research, decision, and contract files.

## Adopted Decision Table

| Decision ID | Source | Adopted Design | Why Adopt | Curis Module | Contract Field(s) | Phase-4 |
| --- | --- | --- | --- | --- | --- | --- |
| AD-PAPERCLIP-COMPANY | Paperclip | AI company as top-level product object | Keeps final product oriented around companies, not loose agents | CompanyTemplate | `CompanyTemplate.slug`, `name`, `description`, `default_department_templates` | reserve contract |
| AD-PAPERCLIP-ORG | Paperclip | org chart as department/employee relationship | Needed for L5 future company layer | DepartmentTemplate / EmployeeTemplate | `department_type`, `default_employee_templates`, `template_id`, `department_id` | implement metadata |
| AD-PAPERCLIP-CAPABILITY | Paperclip | skills separated from agents | Prevents employees from owning credentials or tool definitions | CapabilityBinding | `capability_source`, `capability_type`, `capability_id`, `priority` | implement metadata |
| AD-PAPERCLIP-PACK | Paperclip Companies | portable company pack | Supports future official/tenant/marketplace company templates | CompanyTemplate | `source`, `tenant_id`, `version`, `capability_pack_refs` | reserve |
| AD-PAPERCLIP-GATE | Paperclip Companies | single-responsibility phase gates | Fits Curis low-token role handoff model | Software R&D SOP | `WorkflowStepTemplate.owner_employee_template_id`, `step_type` | implement/reserve |
| AD-METAGPT-SOP | MetaGPT | software company SOP | Best first department flow for Curis product development | WorkflowTemplate / DepartmentTemplate | `default_workflow_template_id`, `step_templates` | implement minimal SOP metadata |
| AD-METAGPT-ROLES | MetaGPT | PM / Architect / Engineer / QA role family | Strong R&D employee baseline | EmployeeTemplate | `role`, `responsibility`, `default_workflow_step_types` | implement |
| AD-CHATDEV-LIFECYCLE | ChatDev | phase-based lifecycle and review loops | Makes testing/review first-class while staying traceable | WorkflowTemplate | `max_iterations`, `output_contract`, `WorkflowTrace.status` | reserve bounded loop |
| AD-CHATDEV-FIELD-SPEC | ChatDev | field-spec style schema metadata | Useful for safe future UI forms | Contracts | required/type/source/phase/default/boundary columns | implement in contracts |
| AD-CREWAI-ROLE-FIELDS | CrewAI | role / goal / backstory split | Clean employee template model after CEO-language translation | EmployeeTemplate | `role`, `responsibility`, `default_instructions` | implement |
| AD-CREWAI-OUTPUT | CrewAI | expected output per task | Keeps SOP steps evidence-oriented | WorkflowStepTemplate | `output_contract` | implement/reserve |
| AD-CREWAI-SEQUENTIAL | CrewAI | sequential process first | Low-risk process baseline | WorkflowTemplate | `process_type=sequential` | reserve; no engine |
| AD-CREWAI-CONFIG-SPLIT | CrewAI Examples | agent/task config separation | Good template file mental model | EmployeeTemplate / WorkflowStepTemplate | employee fields separate from step fields | implement metadata |
| AD-AUTOAGENTS-SUGGESTION | AutoAgents | role suggestion concept | Useful later for auto-recruiting, but unsafe now | EmployeeTemplate | `suggestion_reason`, `generated_from_task_id` | reserve only |
| AD-AUTOAGENTS-OBSERVER | AutoAgents | observer/reflection idea | Future QA review support | WorkflowTrace | `error_summary`, review notes future field | reserve only |
| AD-OPENCLAW-PACK | OpenClaw Agents / Skills | role template and skill pack catalogs | Good official template/capability pack precedent | EmployeeTemplate / CapabilityPack | `instructions_ref`, `quality_bar`, `review_status` | reserve pack; implement bindings |
| AD-GPTS-SEPARATION | GPTs | instructions vs knowledge vs capabilities separation | Prevents prompt/knowledge/tool mixing | EmployeeTemplate / CapabilityBinding | `default_instructions`, `default_capability_types`, `default_model_policy` | implement metadata |
| AD-GPTS-ACTIONS | GPTs | actions require schema/auth/workspace control | Good future connector governance model | CapabilityType / Connector | `credential_ref`, `auth_type`, `output_contract` | reserve |
| AD-COZE-SURFACES | Coze | prompt + RAG + plugin + workflow surfaces | Confirms separate capability and workflow planes | CapabilityType / WorkflowTemplate | `required_capability_types`, `capability_type` | implement/reserve |
| AD-DIFY-CATALOG | Dify | workflow/tool/plugin marketplace separation | Useful for Admin capability governance | CapabilityType | model/tool/connector only; marketplace source | implement source boundary |
| AD-NEWAPI-GATEWAY | New API | OpenAI-compatible model gateway | Already selected as first Model Gateway Adapter target | CapabilityType / Model Gateway | `capability_type=model`, `model_gateway_id`, `model_name` | implemented earlier; contract preserved |
| AD-ONEAPI-USAGE | One API | usage inclusion and channel metadata | Useful for gateway measurement fields | CapabilityType / UsageEvent | `model_gateway_id`, `model_name`, token fields | preserve |
| AD-LITELLM-ABSTRACTION | LiteLLM | provider abstraction behind gateway | Confirms no direct provider SDK in Workspace | CapabilityType | `model_gateway_id`, `default_model_policy` | reserve alternate gateway |
| AD-TASKADE-LAYERING | Taskade | workspace memory + agents + automations split | Useful long-term layered model | WorkflowTemplate / EmployeeTemplate | process/employee/capability separation | reserve |

## Phase-4 Adopted Baseline

```text
CompanyTemplate (contract reserved)
  -> DepartmentTemplate: Software R&D
      -> EmployeeTemplate:
          Tech Lead
          Product Manager
          Architect
          Frontend Engineer
          Backend Engineer
          QA Engineer
      -> Workflow/SOP:
          requirement understanding
          task breakdown
          architecture design
          coding
          testing
          report
      -> CapabilityBinding:
          official / tenant_private / marketplace
          model / tool / connector
```

Execution stays gated and must not alter current Task Execution without a separate development issue and gate approval.
