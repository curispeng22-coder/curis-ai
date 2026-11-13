# GPTs Research

Source:

- [GPTs in ChatGPT](https://help.openai.com/en/articles/8554407-gpts-in-chatgpt)
- [Creating and editing GPTs](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts)
- [Configuring actions in GPTs](https://help.openai.com/en/articles/9442513-configuring-actions-in-gpts)

Deployment decision: not applicable. GPTs is a hosted ChatGPT feature; official docs are sufficient for template and governance research.

## Project Positioning

GPTs are no-code custom versions of ChatGPT configured for a specific purpose. They combine instructions, knowledge, capabilities, apps, and actions inside ChatGPT. For Curis, GPTs are useful as a reference for simple role configuration and sharing controls, but not as a company/department architecture.

## Core Concepts

- GPT: custom assistant configured for one purpose.
- Instructions: behavior, tone, goals, boundaries, and step structure.
- Knowledge: uploaded files used as reference material.
- Capabilities: built-in tools such as web search, image generation, canvas, or code/data analysis.
- Apps: user-connected outside services.
- Actions: external APIs defined by OpenAPI schema and authentication.
- Sharing: private, direct, workspace, link, or GPT Store depending on plan and workspace settings.
- Workspace controls: Enterprise/Edu admins can limit access, creation, sharing, and action domains.

## Product Structure

```text
GPT
  -> name
  -> description
  -> conversation starters
  -> instructions
  -> knowledge files
  -> recommended model
  -> capabilities
  -> apps OR actions
  -> share/publish settings
  -> version history
```

## Template / Agent / Capability Fields

| GPT Field | Curis Mapping | Decision |
| --- | --- | --- |
| name | `EmployeeTemplate.name` / `CapabilityPack.name` | adopt |
| description | `description` | adopt |
| conversation starters | template examples | reserve |
| instructions | `default_instructions` / `guardrails` | adopt |
| knowledge | future knowledge refs | reserve |
| recommended model | `default_model_policy` | adopt as metadata |
| capabilities | `default_capability_types` / capability bindings | adopt |
| actions schema | connector/action contract | reserve |
| authentication | `credential_ref` boundary | reserve; no real secret storage |
| version history | template version | reserve |
| sharing settings | source/governance | adopt conceptually |

## Workflow / SOP Design

GPTs do not provide a true company SOP. The useful workflow guidance is instruction authoring: explicit step structure, concrete examples, preview testing, and version history.

Curis should map this to:

```text
EmployeeTemplate.default_instructions
-> WorkflowStepTemplate.output_contract
-> Preview/Test evidence before publishing
```

## Reusable For Curis

- Simple CEO-facing role configuration.
- Clear separation of instructions and knowledge.
- Recommended model as a preference, not a hard provider credential.
- Actions require schema, authentication mode, and user/workspace approval.
- Version history supports rollbackable templates later.

## Not Suitable For Curis

- Chatbot-first product model.
- GPT Store as direct equivalent of Curis marketplace.
- Knowledge files as hidden employee memory.
- Apps/actions as unreviewed external calls.
- No-code assistant sharing without Curis tenant isolation and usage_event attribution.

## Curis Contract Suggestions

- `EmployeeTemplate.default_instructions`
- `EmployeeTemplate.default_model_policy`
- `EmployeeTemplate.default_capability_types`
- `CapabilityBinding.capability_source`
- `CapabilityBinding.capability_type`
- `CapabilityBinding.capability_id`
- `WorkflowStepTemplate.output_contract`
- `Template.version` reserved
