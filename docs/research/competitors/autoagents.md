# AutoAgents Research

Sources:

- Paper: [AutoAgents: A Framework for Automatic Agent Generation](https://arxiv.org/abs/2309.17288)
- GitHub: [Link-AGI/AutoAgents](https://github.com/Link-AGI/AutoAgents)

Local evidence path: `/tmp/curis-phase35-research/AutoAgents`

Deployment decision: not deployed. Paper abstract/architecture, README, role generation code, manager, observer, and custom role code were enough to understand the mechanism.

## Project Positioning

AutoAgents focuses on dynamic agent generation. Given a task, the system decides which expert roles are required, creates or selects roles, builds an execution plan, and uses observers/reflection to check whether roles and plans satisfy requirements.

This is future inspiration for Curis "automatic employee hiring," not a Phase-4 implementation target.

## Read Files

- `README.md`
- `autoagents/actions/create_roles.py`
- `autoagents/actions/check_roles.py`
- `autoagents/actions/check_plans.py`
- `autoagents/roles/manager.py`
- `autoagents/roles/observer.py`
- `autoagents/roles/custom_role.py`
- `autoagents/roles/group.py`
- role bank files

## Directory Structure

```text
autoagents/
  actions/
    create_roles.py
    check_roles.py
    check_plans.py
  roles/
    manager.py
    observer.py
    custom_role.py
    group.py
    role_bank/
```

## Core Concepts

- Planner/Manager: decomposes the task and proposes roles plus a plan.
- Tools: capabilities available to generated roles.
- Observers: check whether generated agents and plans are reasonable.
- Agents: roles with name, expertise, tools, prompt, and suggestions.
- Plan: ordered work allocation across roles.
- Reflection: iterative correction until role/plan checks pass or a limit is reached.

## Template Fields

Generated role fields in `create_roles.py`:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | generated expert name | future `EmployeeTemplate.name` suggestion |
| `description` | role expertise | `description` |
| `tools` | required tools | capability type/binding suggestions |
| `suggestions` | operating hints | `default_instructions` draft |
| `prompt` | role prompt | `default_instructions` draft |

Plan fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| role list | needed employees | employee suggestions |
| expected output | output contract | workflow step output |
| required input | dependencies | workflow input contract |
| execution order | plan | workflow steps |

Observer fields/patterns:

| Pattern | Meaning | Curis Mapping |
| --- | --- | --- |
| `ObserverAgents` | checks roles fit task | future PM/QA review |
| `ObserverPlans` | checks plan quality | future workflow review |
| max iterations | safety bound | required for any future auto-generation |

## Role / Employee / Agent Design

AutoAgents does not start from a fixed company chart. It creates roles from the task. This is powerful but risky for Curis because Workspace must keep predictable tenant boundaries, capability use, and usage_event attribution.

Curis should first ship official employee templates. Later, an "employee suggestion" feature can propose extra employees but should require CEO approval and should never auto-create runtime employees without a gate.

## Task / Workflow / SOP Design

AutoAgents flow:

```text
Task
-> Manager creates roles and plan
-> Observer reviews roles
-> Observer reviews plan
-> Custom roles execute assigned plan
-> Reflection/correction
```

Curis can reserve this as:

```text
Task
-> suggested_employee_templates
-> suggested_workflow_steps
-> approval
-> instantiate
```

## Reusable Points

- Dynamic role suggestion is useful after official templates are stable.
- Role generation should include required tools/capabilities.
- Observer/reviewer mechanism maps to QA and Product acceptance.
- Iteration limits are mandatory.

## Not Adopted

- Automatic employee creation in Phase-4.
- Automatic plan execution from generated roles.
- Open-ended reflection loops.
- Generated direct tool access without Curis CapabilityBinding.
- Role generation that bypasses Admin official catalog or tenant_private boundaries.

## Curis Phase-4 Field Suggestions

Reserve only:

- `suggested_employee_template_id`
- `suggestion_reason`
- `required_capability_types`
- `approval_status`
- `generated_from_task_id`

Do not implement dynamic generation. Phase-4 can leave "auto-recruit employee" as a future roadmap item after workflow traces and approval gates exist.
