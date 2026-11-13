# MetaGPT Research

Source: [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT)

Local evidence path: `/tmp/curis-phase35-research/MetaGPT`

Deployment decision: not deployed. README, examples, roles, actions, and software company code were enough to infer role fields and SOP flow.

## Project Positioning

MetaGPT presents itself as "Software Company as Multi-Agent System." It turns a one-line requirement into product documents, competitive analysis, requirements, data structures, APIs, and code through a software-company SOP.

The strongest Curis lesson is `Code = SOP(Team)`: define a repeatable team process first, then bind employees and capabilities to each step.

## Read Files

- `README.md`
- `metagpt/software_company.py`
- `metagpt/team.py`
- `metagpt/roles/product_manager.py`
- `metagpt/roles/architect.py`
- `metagpt/roles/engineer.py`
- `metagpt/roles/project_manager.py`
- `metagpt/roles/qa_engineer.py`
- `metagpt/actions/write_prd.py`
- `metagpt/actions/design_api.py`
- `metagpt/actions/write_code.py`
- `metagpt/actions/write_test.py`
- `examples/di/software_company.py`

## Directory Structure

```text
metagpt/
  software_company.py
  team.py
  roles/
    product_manager.py
    architect.py
    engineer.py
    project_manager.py
    qa_engineer.py
  actions/
    write_prd.py
    design_api.py
    write_code.py
    write_test.py
examples/
  di/software_company.py
config/
```

## Core Concepts

- Team: hires roles, invests budget, starts a project, and runs rounds.
- Role: stable responsibility holder with name, profile, goal, constraints, instruction, tools, actions, and watched messages.
- Action: atomic production step such as writing PRD, designing API, writing code, or writing tests.
- SOP: a role/action/message chain that converts requirements into artifacts.
- Investment: budget-like control, but not needed in Curis Phase-4.

## Template Fields

Role fields observed in code:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | role persona name | `EmployeeTemplate.name` or hidden seed |
| `profile` | business role | `EmployeeTemplate.role` |
| `goal` | role objective | `responsibility` |
| `constraints` | boundaries | `default_instructions` or `guardrails` |
| `instruction` | detailed prompt | `default_instructions` |
| `tools` | available tools | default capability types/bindings |
| `actions` | role can perform | `default_workflow_step_types` |
| `watch` | upstream messages | future workflow dependency |

Team/runtime fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `hire(roles)` | team members | department employee instances |
| `invest(investment)` | budget | reserve for L6 |
| `run_project(idea)` | task kickoff | current task -> future workflow |
| `run(n_round)` | repeated execution | reserve |

## Role / Employee / Agent Design

MetaGPT's software company baseline includes:

- Product Manager
- Architect
- Project Manager
- Engineer
- QA Engineer
- Data Analyst in some flows
- Team Leader in newer flows

Curis should adopt the software-development role family but simplify labels for a CEO:

- Product Manager: requirement and acceptance criteria
- Tech Lead: task decomposition and coordination
- Architect: boundaries, data/API shape, risk
- Frontend Engineer: UI implementation
- Backend Engineer: API/data/execution implementation
- QA Engineer: test plan and evidence

## Task / Workflow / SOP Design

MetaGPT flow in Curis terms:

```text
User requirement
-> Product Manager writes PRD / user stories / acceptance criteria
-> Architect writes system design / API / data structure
-> Project Manager decomposes implementation tasks
-> Engineer writes code
-> QA Engineer writes/runs tests
-> Review/report
```

Artifacts matter as much as chat. Phase-4 should store workflow traces and outputs, not just messages.

## Reusable Points

- Use a fixed Software R&D SOP as first department process.
- Separate role templates from step actions.
- Make each step produce a named artifact.
- Model upstream dependencies between steps.
- Use QA as a real role, not an afterthought.

## Not Adopted

- Full repository generation from one sentence.
- Unlimited role loops.
- Budget/investment enforcement.
- Role memory and social interaction simulation.
- Multi-role autonomous execution before Curis has safe workflow gates.

## Curis Phase-4 Field Suggestions

`EmployeeTemplate` should add:

- `responsibility`
- `default_instructions`
- `default_workflow_step_types`
- `default_capability_types`
- `guardrails`

`WorkflowStepTemplate` should reserve:

- `id`
- `step_type`
- `name`
- `owner_employee_template_id`
- `input_contract`
- `output_contract`
- `required_capability_types`
- `next_step_ids`

Phase-4 should implement only the minimal sequential Software R&D SOP metadata and one-step-at-a-time task assignment if approved.
