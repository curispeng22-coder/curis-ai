# Paperclip Research

Source: [paperclipai/paperclip](https://github.com/paperclipai/paperclip)

Local evidence path: `/tmp/curis-phase35-research/paperclip`

Deployment decision: not deployed. README, docs, API docs, and company package spec were enough to identify product positioning, schema fields, and workflow boundaries.

## Project Positioning

Paperclip is an open-source control plane for AI companies. It treats an AI company as an organization with goals, agents, org charts, tickets, budgets, governance, audits, and adapters instead of treating agents as isolated chat sessions.

For Curis, the useful lesson is product framing: the company is the main object, employees are accountable execution roles, skills are separate reusable capabilities, and governance is explicit.

## Read Files

- `README.md`
- `docs/start/core-concepts.md`
- `docs/companies/companies-spec.md`
- `docs/api/companies.md`
- `docs/api/agents.md`
- `docs/api/goals-and-projects.md`
- `docs/api/issues.md`
- `docs/api/costs.md`

## Directory Structure

Observed major areas:

```text
docs/
  start/core-concepts.md
  companies/companies-spec.md
  api/
packages/
  adapters/
  db/
  skills-catalog/
  teams-catalog/
server/
cli/
```

The most relevant structure for Curis is the Agent Company package format:

```text
COMPANY.md
.paperclip.yaml
agents/<agent-slug>/AGENTS.md
teams/<team-slug>/TEAM.md
projects/<project-slug>/PROJECT.md
projects/<project-slug>/tasks/<task-slug>/TASK.md
skills/<skill-slug>/SKILL.md
assets/
scripts/
references/
```

## Core Concepts

- Company: business container with goals, agents, org structure, budget, and task hierarchy.
- Goal: strategic target that gives task context.
- Project: grouped work aligned to goals.
- Issue: work unit with status, priority, assignee, project, goal, parent, comments, documents, and interactions.
- Agent: employee-like runtime with role, title, capabilities, adapter, budget, status, and reporting line.
- Skill: reusable task ability referenced by agents.
- Heartbeat: scheduled or event-triggered wake/check/act loop.
- Governance: approvals, overrides, pause/resume, terminate, config revisions, audit, and cost tracking.

## Template Fields

Common package frontmatter:

| Field | Meaning | Curis Use |
| --- | --- | --- |
| `schema` | package schema version | adopt |
| `kind` | COMPANY / TEAM / AGENT / TASK / SKILL | adopt as `template_type` if needed |
| `slug` | stable portable id | adopt |
| `name` | display name | adopt |
| `description` | summary | adopt |
| `version` | package version | adopt |
| `license` | distribution license | reserve |
| `authors` | creators | reserve |
| `homepage` | source URL | reserve |
| `tags` | discovery labels | adopt |
| `metadata` | extension block | reserve |
| `sources` | provenance | adopt for official templates |

Company fields from spec and API:

| Field | Meaning | Curis Phase-4 |
| --- | --- | --- |
| `id` | runtime company id | use existing/current company model if present |
| `name` | company name | implement in template/instance |
| `description` | company purpose | implement |
| `slug` | portable id | implement for templates |
| `status` | active / paused / archived | implement for instances |
| `goals` | strategic goals | reserve or metadata |
| `includes` | included teams/agents/skills | reserve for Company Pack |
| `requirements.secrets` | required secret references | reserve only; no real secret storage |
| `budgetMonthlyCents` | monthly budget | reserve for L6 |
| `createdAt` / `updatedAt` | timestamps | implement for records |

Team fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | team name | `DepartmentTemplate.name` |
| `description` | team scope | `DepartmentTemplate.description` |
| `slug` | stable id | `DepartmentTemplate.slug` |
| `manager` | path to manager agent | `default_manager_template_id` reserve |
| `includes` | member agent references | `default_employee_templates` |
| `tags` | category labels | `tags` reserve |

Agent fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | agent name | `EmployeeTemplate.name` |
| `title` | business title | `EmployeeTemplate.role` |
| `reportsTo` | reporting line | reserve for org chart |
| `skills` | skill references | `CapabilityBinding` defaults |
| body instructions | canonical role instructions | `default_instructions` |
| `adapter.type` | runtime adapter | do not adopt; Curis uses ModelGatewayAdapter |
| `adapter.config.model` | model | `default_model_policy` metadata only |
| `inputs.env` | secret requirements | `credential_ref` style reference only |

Issue/task fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `title` | work title | task title or content summary |
| `description` | work description | task content |
| `status` | backlog/todo/in_progress/in_review/done/blocked/cancelled | reuse minimal task state if compatible |
| `priority` | priority | reserve |
| `assigneeAgentId` | assigned agent | future employee assignment |
| `projectId` | project scope | reserve |
| `goalId` | goal context | `goal_context` reserve |
| `parentId` | hierarchy | reserve |
| `billingCode` | cost grouping | forbidden until L6 gate |

Cost fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `provider` | model provider | already hidden behind Model Gateway |
| `model` | model name | `usage_event.model_name` |
| `inputTokens` | prompt tokens | `usage_event.prompt_tokens` |
| `outputTokens` | completion tokens | `usage_event.completion_tokens` |
| `costCents` | cost | `usage_event.estimated_cost` |

Curis should keep the measurement idea but not adopt budget enforcement in Phase-4.

## Role / Employee / Agent Design

Paperclip agents have:

- identity: name, role/title
- reporting line: manager/chain of command
- capabilities: skills and adapter capabilities
- status: running/idle/error/paused/terminated
- budget: monthly budget and spending
- config revisions: rollbackable runtime configuration

Curis Phase-4 should adopt identity, department membership, capability binding, status, and instructions. It should reserve reporting lines and config revisions, and it should not implement budget enforcement.

## Task / Workflow / SOP Design

Paperclip uses issues as the work queue and supports:

- parent/child hierarchy
- goal/project links
- checkout/release to prevent duplicate work
- documents keyed by stable names such as `plan`
- structured interactions for user approval
- comments and mentions that can wake agents

Curis Phase-4 should adopt the idea that tasks can gain a future assignment envelope:

```text
Task
  -> selected Department
  -> selected Employee
  -> selected CapabilityBinding
  -> WorkflowTrace
```

It should not copy atomic checkout/release or 24/7 heartbeat behavior yet.

## Reusable Points

- Company as the primary future product object.
- Portable company package idea.
- Department/team package includes employee templates.
- Employee instructions are file-backed and source-controlled.
- Skills/capabilities are separate from employees.
- Goal context should be preserved in task assignment.
- Governance and audit should be explicit rather than hidden.

## Not Adopted

- Full autonomous company heartbeats.
- Direct provider/adaptor execution path.
- Workspace-side budget enforcement.
- Employee API keys.
- Company import/export mutating official templates without Admin review.
- Agent config rollback before Curis has stable employee runtime.

## Curis Phase-4 Field Suggestions

Add or reserve contracts:

- `CompanyTemplate`
- `CompanyInstance`
- `DepartmentTemplate`
- `DepartmentInstance`
- `EmployeeTemplate`
- `EmployeeInstance`
- `CapabilityBinding`
- `WorkflowTrace`
- `goal_context`
- `template_source`: official / tenant_private / marketplace

Phase-4 implement recommendation:

- implement one official Software R&D DepartmentTemplate
- implement six official EmployeeTemplates
- implement tenant-scoped EmployeeInstances only if the gate approves UI/metadata
- keep CompanyTemplate mostly reserved
- keep budgets/governance references as metadata only
