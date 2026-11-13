# OpenClaw Agents / Skills Research

Actual researched repositories:

- [mergisi/awesome-openclaw-agents](https://github.com/mergisi/awesome-openclaw-agents)
- [openclaw/agent-skills](https://github.com/openclaw/agent-skills)

Local evidence paths:

- `/tmp/curis-phase35-research/awesome-openclaw-agents`
- `/tmp/curis-phase35-research/agent-skills`

Deployment decision: not deployed. Template files and skill package structure were sufficient.

## Project Positioning

Awesome OpenClaw Agents is a catalog of reusable agent templates. OpenClaw agent-skills is a catalog of reusable skills packaged as instruction folders. Together they are a strong reference for future Curis official capability packs and marketplace review, not for immediate runtime execution.

## Read Files

- `awesome-openclaw-agents/README.md`
- `awesome-openclaw-agents/agents.json`
- `awesome-openclaw-agents/agents/development/code-reviewer/SOUL.md`
- `agent-skills/README.md`
- `agent-skills/skills/handoff/SKILL.md`
- `agent-skills/skills/autoreview/SKILL.md`

## Directory Structure

Agent template catalog:

```text
agents/
  development/
    code-reviewer/SOUL.md
    docs-writer/SOUL.md
    bug-hunter/SOUL.md
  ...
agents.json
README.md
```

Skill catalog:

```text
skills/
  handoff/
    SKILL.md
  autoreview/
    SKILL.md
  behavior-validator/
    SKILL.md
```

## Core Concepts

- Agent template: a reusable role instruction file.
- Skill template: a reusable workflow/capability instruction file.
- Category: browsing and discovery dimension.
- Deploy metadata: where/how a template can be used.
- SOUL.md: persona and operating contract.
- SKILL.md: capability workflow and quality bar.

## Template Fields

`agents.json` sample fields:

| Field | Meaning | Curis Mapping |
| --- | --- | --- |
| `id` | catalog id | template id |
| `category` | category | department/capability category |
| `name` | display name | `EmployeeTemplate.name` |
| `role` | role label | `EmployeeTemplate.role` |
| `path` | template file path | source artifact ref |
| `deploy` | deployment metadata | reserve |

`SOUL.md` sections:

| Section | Meaning | Curis Mapping |
| --- | --- | --- |
| Core Identity | role/personality/communication | `default_instructions` |
| Responsibilities | scope | `responsibility` |
| Behavioral Guidelines | do/don't rules | `guardrails` |
| Severity Levels | review scale | QA policy reserve |
| Example Interactions | samples | template examples reserve |
| Integration Notes | usage notes | source notes |

`SKILL.md` fields/sections:

| Field/Section | Meaning | Curis Mapping |
| --- | --- | --- |
| `name` | skill id | capability id |
| `description` | skill summary | capability description |
| workflow | steps | tool/capability instructions |
| prompt rules | guardrails | capability guardrails |
| template | output format | output contract |
| quality bar | acceptance | verification criteria |

## Role / Employee / Agent Design

OpenClaw templates are highly reusable role definitions, but they are often written for developer tools. Curis should treat them as source material for official EmployeeTemplate and Capability Pack catalogs after Admin review.

## Task / Workflow / SOP Design

The skill catalog shows a simple packaging pattern:

```text
Skill name
-> description
-> workflow
-> rules
-> output template
-> quality bar
```

Curis can use this for future Capability Pack format, while Phase-4 only binds employees to existing official/tenant_private capabilities.

## Reusable Points

- Category-based template browsing.
- Separate employee templates from skill/capability templates.
- Instruction files can be source-controlled.
- Quality bars should be part of official capabilities.
- Developer/QA roles are good candidates for Curis R&D templates.

## Not Adopted

- Raw SOUL.md as CEO-facing UI.
- Marketplace publishing before Admin Platform review.
- Deploy metadata as executable config.
- Unreviewed third-party skill execution.
- Open-ended agent catalog import into Workspace official catalog.

## Curis Phase-4 Field Suggestions

Reserve future `CapabilityPack`:

- `id`
- `name`
- `description`
- `category`
- `capability_type`
- `source`
- `tenant_id`
- `instructions_ref`
- `output_contract`
- `quality_bar`
- `review_status`
- `enabled`

Phase-4 should only use official and tenant_private capabilities that already pass the current Workspace/Admin boundary.
