# Paperclip Companies Research

Source: [paperclipai/companies](https://github.com/paperclipai/companies)

Local evidence path: `/tmp/curis-phase35-research/companies`

Deployment decision: not deployed. Repository templates directly expose the company package structure and fields.

## Project Positioning

Paperclip Companies is a catalog of ready-to-deploy agent company templates. Each template is a portable company package with company metadata, agents, skills, teams, and sometimes projects. It is closer to Curis future `Company Pack` / `Business Pack` supply than to a runtime engine.

## Read Files

- root `README.md`
- `agentsys-engineering/.paperclip.yaml`
- `agentsys-engineering/COMPANY.md`
- `agentsys-engineering/README.md`
- `agentsys-engineering/agents/ceo/AGENTS.md`
- `agency-agents/teams/engineering/TEAM.md`

## Directory Structure

Typical company directory:

```text
<company-slug>/
  .paperclip.yaml
  COMPANY.md
  README.md
  agents/
    <agent-slug>/AGENTS.md
  skills/
    <skill-slug>/SKILL.md
  teams/
    <team-slug>/TEAM.md
  projects/
    <project-slug>/PROJECT.md
```

`agentsys-engineering` shows a compact software company:

```text
CEO -> CTO -> Staff Engineer -> QA & Release Lead
Research & Perf Analyst on demand
```

`agency-agents/teams/engineering/TEAM.md` shows a broad department package with one manager and many included specialist agents.

## Core Concepts

- A company template is a folder, not one giant JSON file.
- `COMPANY.md` defines company mission, goals, and workflow.
- `.paperclip.yaml` defines agent adapter defaults and secret requirements.
- `AGENTS.md` defines employee identity, reporting line, skills, instructions, workflow, handoff, and principles.
- `TEAM.md` defines department/team membership by referencing agent files.
- `SKILL.md` defines reusable capabilities.

## Template Fields

`.paperclip.yaml` fields:

| Field | Meaning | Curis Use |
| --- | --- | --- |
| `schema` | package config schema | adopt as versioned schema |
| `agents` | per-agent runtime config | reserve as template config |
| `adapter.type` | runtime adapter | do not adopt directly |
| `adapter.config.model` | default model | map to `default_model_policy` |
| `inputs.env.<name>.kind` | secret input type | map to `credential_ref` requirement only |
| `inputs.env.<name>.requirement` | optional/required | reserve |

`COMPANY.md` fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | company template name | `CompanyTemplate.name` |
| `description` | template summary | `CompanyTemplate.description` |
| `slug` | portable id | `CompanyTemplate.slug` |
| `schema` | package schema | `schema_version` |
| `version` | package version | `version` |
| `license` | license | reserve |
| `authors` | creators | reserve |
| `goals` | company objectives | `default_goals` reserve |

`AGENTS.md` fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | employee name | `EmployeeTemplate.name` |
| `title` | business role | `EmployeeTemplate.role` |
| `reportsTo` | reporting line | reserve |
| `skills` | capability references | default capability bindings |
| body identity | role personality/scope | `default_instructions` |
| body workflow | role SOP | `default_workflow_step_types` |
| body handoff | next role | `handoff_rules` reserve |

`TEAM.md` fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | department name | `DepartmentTemplate.name` |
| `description` | department purpose | `description` |
| `slug` | stable id | `department_type` or `slug` |
| `manager` | manager agent path | reserve |
| `includes` | employee template refs | `default_employee_templates` |
| `tags` | category | reserve |

## Role / Employee / Agent Design

The strongest pattern is single-responsibility role design. AgentSys Engineering states that discovery is not planning, planning is not implementation, implementation is not review, and review is not shipping. This maps well to Curis Phase-4 R&D roles.

Curis should translate this into CEO-readable employees:

- Product Manager: clarify and scope
- Tech Lead: decompose and coordinate
- Architect: design boundaries
- Backend Engineer: backend delivery
- Frontend Engineer: frontend delivery
- QA Engineer: verification and release evidence

## Task / Workflow / SOP Design

AgentSys Engineering has enforced phase gates:

```text
CEO discovers/prioritizes
-> CTO explores/plans
-> Staff Engineer implements
-> QA & Release Lead verifies
-> ship or review loop
```

Curis should adapt the shape, not the autonomous dispatch depth:

```text
CEO task
-> Product Manager requirement note
-> Tech Lead task split
-> Architect boundary
-> Engineer implementation
-> QA verification
-> report
```

## Reusable Points

- Portable company folders.
- Team file lists included agents.
- Agent file combines metadata and role instructions.
- Skill references are explicit.
- Phase gates are stated in plain language.
- Secret requirements are references, not secrets.

## Not Adopted

- Direct `claude_local` or other runtime adapters.
- Secret env injection inside Workspace templates.
- Very large department packs in Phase-4.
- Full import command mutating runtime state.
- Production shipping automation.

## Curis Phase-4 Field Suggestions

`CompanyTemplate` should include:

- `id`
- `slug`
- `name`
- `description`
- `version`
- `source`
- `tenant_id`
- `default_department_templates`
- `default_goals`
- `governance_policy_ref`
- `enabled`
- `created_at`

`DepartmentTemplate` should include:

- `id`
- `name`
- `department_type`
- `description`
- `default_employee_templates`
- `default_workflow_template_id`
- `source`
- `tenant_id`
- `enabled`
- `created_at`

Phase-4 should implement the R&D department template first and reserve Company Pack import/export.
