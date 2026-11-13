# ChatDev Research

Source: [OpenBMB/ChatDev](https://github.com/OpenBMB/ChatDev)

Local evidence path: `/tmp/curis-phase35-research/ChatDev`

Deployment decision: not deployed. YAML instances, authoring docs, and field specs were enough to understand workflow and role configuration.

## Project Positioning

ChatDev models software development as a virtual company and, in newer versions, as a zero-code multi-agent workflow platform. Its older product metaphor uses CEO, CTO, Programmer, Tester, and Reviewer roles; its newer implementation uses YAML graphs with agent/model/human/python/subgraph nodes and conditional edges.

For Curis, the useful part is the phase-based software lifecycle and explicit communication chain. The full DAG engine is too heavy for Phase-4.

## Read Files

- `README.md`
- `docs/user_guide/en/workflow_authoring.md`
- `docs/user_guide/en/field_specs.md`
- `yaml_instance/ChatDev_v1.yaml`
- `yaml_template/design.yaml`
- `entity/configs/*`
- `workflow/*`

## Directory Structure

```text
docs/user_guide/en/
entity/configs/
schema_registry/
workflow/
yaml_instance/
yaml_template/
frontend/public/
runtime/
```

## Core Concepts

- Workflow graph: versioned YAML with `vars` and `graph`.
- Node: agent, model, human, python, subgraph, passthrough, literal, loop_counter, loop_timer.
- Edge: transition with optional conditions and processors.
- Agent config: provider, base_url, api_key, model/name, role, tooling, thinking, memories, retry.
- Loop controls: counters and timers for review/test cycles.
- Field specs: schema-backed UI form definitions with type, default, description, enum, and nested child specs.

## Template Fields

Top-level workflow fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `version` | schema version | `WorkflowTemplate.version` reserve |
| `vars` | variables/env refs | reserve; no secrets in Workspace |
| `graph.id` | workflow id | `WorkflowTemplate.id` |
| `graph.description` | workflow summary | `description` |
| `graph.log_level` | runtime logging | not needed |
| `graph.is_majority_voting` | voting behavior | reject for Phase-4 |
| `graph.initial_instruction` | entry instruction | `task_goal_context` reserve |
| `graph.start` / `graph.end` | entry/exit nodes | reserve |
| `graph.nodes` | steps | future `WorkflowStepTemplate` |
| `graph.edges` | transitions | reserve |

Agent node fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `id` | node name | workflow step id |
| `type` | node type | step type |
| `config.role` | prompt role | employee instructions |
| `config.provider` | provider | not adopted; Model Gateway only |
| `config.base_url` | provider URL | forbidden in employee template |
| `config.api_key` | credential | forbidden |
| `config.name` | model name | model policy metadata only |
| `config.tooling` | tools | capability binding |
| `config.memories` | memory | reserve |
| `context_window` | context policy | reserve |

`FIELD_SPECS` fields:

| Field | Meaning | Curis Use |
| --- | --- | --- |
| `name` | field key | adopt for future template schemas |
| `display_name` | UI label | adopt |
| `type_hint` | field type | adopt |
| `required` | required flag | adopt |
| `default` | default value | adopt |
| `description` | helper text | adopt |
| `enum` / `enumOptions` | selectable options | adopt |
| `child` | nested schema | reserve |

## Role / Employee / Agent Design

ChatDev's software company roles include:

- Chief Executive Officer: requirement decision and policy.
- Chief Technology Officer: technical design in earlier flows.
- Programmer: coding and implementation.
- Code Reviewer: code review loop.
- Tester: test and test-modification loop.

Curis should avoid a CEO employee inside Workspace because the human user is the CEO. Instead, map roles to:

- Product Manager
- Tech Lead
- Architect
- Frontend Engineer
- Backend Engineer
- QA Engineer

## Task / Workflow / SOP Design

`ChatDev_v1.yaml` shows a staged workflow with loop counters:

```text
USER
-> CEO / planning prompts
-> Programmer Coding
-> Programmer Code Review
-> Code Complete loop
-> Test Phase loop
-> FINAL
```

The important Curis ideas:

- role-to-role handoff should be explicit
- review/test loops need max iteration guards
- workflows should have traceable nodes and edges
- human acceptance can be a node in later gates

## Reusable Points

- Workflow schema should be explicit and versioned.
- Each workflow step should know owner, inputs, outputs, and allowed capability types.
- Review loops need an iteration limit.
- Field specs help generate safe UI forms later.
- Literal prompt nodes map to Curis step instructions.

## Not Adopted

- Full graph/DAG editor in Phase-4.
- Provider/base_url/api_key fields in Workspace employee templates.
- Majority voting.
- Arbitrary Python node execution.
- Human node UI and subgraph composition before workflow gates.
- Multi-agent free conversation as the primary interface.

## Curis Phase-4 Field Suggestions

`WorkflowStepTemplate`:

- `id`
- `workflow_template_id`
- `step_type`
- `name`
- `description`
- `owner_employee_template_id`
- `input_contract`
- `output_contract`
- `required_capability_types`
- `max_iterations`
- `next_step_ids`
- `enabled`

`WorkflowTrace`:

- `id`
- `tenant_id`
- `task_id`
- `workflow_template_id`
- `step_id`
- `employee_id`
- `capability_source`
- `capability_type`
- `capability_id`
- `status`
- `input_summary`
- `output_summary`
- `started_at`
- `finished_at`

Phase-4 should only implement minimal task assignment or workflow metadata. A full ChatChain/SOPChain engine should remain reserved.
