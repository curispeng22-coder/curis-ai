# CrewAI Research

Source: [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)

Local evidence path: `/tmp/curis-phase35-research/crewAI`

Deployment decision: not deployed. README, installation docs, and crew concepts were enough to identify agent/task/crew/process fields.

## Project Positioning

CrewAI is a framework for building collaborative AI crews. It separates agents, tasks, crews, tools, knowledge, memory, and process modes. It is developer-centric, but its role/goal/backstory pattern is useful for Curis employee templates.

## Read Files

- `README.md`
- `docs/v1.15.2/en/installation.mdx`
- `docs/v1.15.2/en/concepts/crews.mdx`
- `docs/v1.15.2/en/learn/sequential-process.mdx`
- `docs/v1.15.2/en/learn/hierarchical-process.mdx`

## Directory Structure

```text
docs/
lib/
  crewai/
  crewai-core/
```

Newer CrewAI projects use JSONC:

```text
crew.jsonc
agents/<agent>.jsonc
knowledge/
skills/
tools/
```

Classic projects use Python/YAML:

```text
src/<project>/
  crew.py
  config/
    agents.yaml
    tasks.yaml
```

## Core Concepts

- Agent: role-based worker with goal, backstory, tools, LLM, and behavior.
- Task: work item with description, expected output, agent, context, and optional output file.
- Crew: group of agents and tasks.
- Process: sequential or hierarchical execution.
- Manager: optional coordinator for hierarchical crews.
- Tools/Knowledge/Skills: attachable capabilities or context.

## Template Fields

Agent fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `role` | employee job label | `EmployeeTemplate.role` |
| `goal` | objective | `responsibility` |
| `backstory` | behavior/persona detail | `default_instructions`, not CEO-facing |
| `llm` | model | `default_model_policy` metadata only |
| `tools` | available tools | capability bindings |
| `verbose` | logging | not needed |
| `max_rpm` | rate limit | reserve |
| `memory` | memory | reserve |
| `guardrails` | constraints | `guardrails` reserve |

Task fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | task id/name | `WorkflowStepTemplate.name` |
| `description` | instruction | `step_instructions` |
| `expected_output` | output contract | `output_contract` |
| `agent` | owner | employee assignment |
| `context` | upstream tasks | step dependencies |
| `output_file` | artifact path | artifact reference reserve |

Crew fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `agents` | participant list | department employees |
| `tasks` | task sequence | workflow steps |
| `process` | sequential/hierarchical | workflow mode |
| `manager_llm` | manager model | not exposed |
| `manager_agent` | coordinator | Tech Lead reserve |
| `memory` | crew memory | reserve |
| `planning` | planning step | reserve |
| `skills` | skill dirs | capability pack reserve |

## Role / Employee / Agent Design

CrewAI's `role`, `goal`, and `backstory` are useful but too developer-oriented if exposed directly to CEO users. Curis should translate:

```text
role -> Role
goal -> Responsibility
backstory -> Operating Instructions
tools -> Capabilities
llm -> Model Policy
```

## Task / Workflow / SOP Design

Sequential process is the right Phase-4 baseline:

```text
Task 1 output
-> Task 2 context
-> Task 3 context
```

Hierarchical process can inspire a future Tech Lead coordinator, but should not be implemented until Curis has stable workflow traces and employee assignment.

## Reusable Points

- Separate Agent / Task / Crew / Process.
- Use `expected_output` as a first-class contract.
- Support sequential flow first.
- Keep tools external to employee identity.
- Store role details in templates, not per task.

## Not Adopted

- Developer-first YAML/JSONC as the CEO-facing interface.
- Hierarchical manager execution in Phase-4.
- Memory, planning, checkpointing, and callbacks.
- Direct provider SDK/model configuration in Workspace employee templates.
- Arbitrary custom tools loaded from local Python.

## Curis Phase-4 Field Suggestions

`EmployeeTemplate`:

- `role`
- `responsibility`
- `description`
- `default_instructions`
- `default_capability_types`
- `default_model_policy`
- `guardrails`

`WorkflowStepTemplate`:

- `description`
- `expected_output`
- `owner_employee_template_id`
- `context_step_ids`

CEO-facing UI labels should avoid "backstory" and use "work style/instructions" only in advanced settings.
