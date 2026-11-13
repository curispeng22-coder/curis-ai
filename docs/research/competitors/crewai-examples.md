# CrewAI Examples Research

Source: [crewAIInc/crewAI-examples](https://github.com/crewAIInc/crewAI-examples)

Local evidence path: `/tmp/curis-phase35-research/crewAI-examples`

Deployment decision: not deployed. Example folders, `agents.yaml`, `tasks.yaml`, and `crew.py` files were enough to infer template format and reusable team patterns.

## Project Positioning

CrewAI Examples is a collection of working crews, flows, and integrations. It is useful for studying how teams are packaged into portable configurations and how domain-specific roles/tasks are organized.

## Read Files

- root `README.md`
- `crews/job-posting/src/job_posting/crew.py`
- `crews/job-posting/src/job_posting/config/agents.yaml`
- `crews/job-posting/src/job_posting/config/tasks.yaml`
- `crews/screenplay_writer/config/agents.yaml`
- `crews/screenplay_writer/config/tasks.yaml`
- multiple `crews/*/README.md` files

## Directory Structure

```text
crews/
  job-posting/
    src/job_posting/
      crew.py
      config/agents.yaml
      config/tasks.yaml
  recruitment/
  stock_analysis/
  marketing_strategy/
  landing_page_generator/
flows/
  email_auto_responder_flow/
  lead-score-flow/
  meeting_assistant_flow/
  self-evaluation-loop/
integrations/
```

## Core Concepts

- A crew folder packages one use case.
- `agents.yaml` defines roles.
- `tasks.yaml` defines ordered or referenced work.
- `crew.py` binds agents/tasks/tools and picks process mode.
- Examples often include tool imports, structured outputs, and output files.

## Template Fields

`agents.yaml` fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| agent key | stable role id | `EmployeeTemplate.slug` |
| `role` | display role | `role` |
| `goal` | objective | `responsibility` |
| `backstory` | behavior and expertise | `default_instructions` |

`tasks.yaml` fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| task key | stable step id | `WorkflowStepTemplate.slug` |
| `description` | work instruction | step description |
| `expected_output` | output contract | output contract |
| `agent` | owner | owner employee template |
| `output_file` | artifact target | artifact ref reserve |

`crew.py` fields/patterns:

| Pattern | Meaning | Curis Mapping |
| --- | --- | --- |
| `agents_config` | agent template file | official/tenant template source |
| `tasks_config` | workflow step file | workflow template source |
| `@agent` | instantiate role | employee instance |
| `@task` | instantiate task | workflow step |
| tools list | runtime capabilities | capability binding |
| `Process.sequential` | execution mode | Phase-4 baseline |
| Pydantic output model | typed artifact | future output schema |

## Role / Employee / Agent Design

The job-posting example uses:

- Research Analyst
- Job Description Writer
- Review and Editing Specialist

The screenplay example uses:

- spam filter
- analyst
- scriptwriter
- formatter
- scorer

These show that Curis should allow future department packs to define role sets beyond R&D, but Phase-4 should stay with Software R&D.

## Task / Workflow / SOP Design

The job-posting example has a clean chain:

```text
research company culture
-> research role requirements
-> draft job posting
-> review/edit
-> industry analysis
```

The key Curis concept is that every step has an expected output. Phase-4 R&D should do the same.

## Reusable Points

- Portable use-case folder per team/workflow.
- Separate `agents.yaml` and `tasks.yaml` maps.
- Task expected output should be required.
- Tool binding belongs in runtime assembly, not in plain role text.
- Structured output schemas are useful later.

## Not Adopted

- Direct Python tool imports from Workspace templates.
- Tool execution from arbitrary example code.
- Non-R&D crews in Phase-4.
- Output files as local filesystem writes without Curis artifact policy.
- Classic decorator runtime as Curis architecture.

## Curis Phase-4 Field Suggestions

Template file direction:

```text
CompanyTemplate
  DepartmentTemplate
    EmployeeTemplate[]
    WorkflowTemplate
      WorkflowStepTemplate[]
```

Phase-4 should not expose YAML editing to CEO users, but the backend contract can mirror the simple agent/task separation.
