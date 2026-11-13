# Coze / Coze Studio Research

Sources:

- [Coze Studio GitHub](https://github.com/coze-dev/coze-studio)
- [What is Coze Studio](https://github.com/coze-dev/coze-studio/wiki/1.-What-is-Coze-Studio)
- [Plugin Configuration](https://github.com/coze-dev/coze-studio/wiki/4.-Plugin-Configuration)

Deployment decision: not deployed. Repository README, wiki, and plugin documentation were enough to identify agent/workflow/plugin boundaries.

## Project Positioning

Coze Studio is an all-in-one visual AI agent development platform. It combines prompt, RAG, plugin, workflow, visual debugging, and deployment. It is useful for Curis as a reference for low-code agent building and plugin/workflow composition, but its full visual builder is too broad for Phase-4.

## Core Concepts

- Agent: conversation-based AI project that can call plugins or workflows.
- Prompt: behavior and response control.
- Knowledge/RAG: external knowledge connected to agents.
- Plugin: tool/API capability that agents and workflows can call.
- Workflow: visual low-code business logic.
- App template/build framework: reusable starting point for agents.
- Debug/deploy lifecycle: visual creation, debugging, and publishing.

## Directory / Product Structure

Coze Studio is built as a Go backend and React/TypeScript frontend with microservices and domain-driven design. Product-level structure:

```text
Agent
  -> prompt
  -> knowledge
  -> plugins
  -> workflows
  -> model/tools
  -> debug/deploy settings

Plugin
  -> official plugin list
  -> auth requirement
  -> third-party API behavior
  -> workflow node availability
```

## Template / Agent / Capability Fields

| Coze Concept | Curis Mapping | Decision |
| --- | --- | --- |
| agent name/description | `EmployeeTemplate.name` / `description` | adopt |
| prompt | `default_instructions` | adopt |
| knowledge | knowledge ref | reserve |
| plugin | `Capability` / `CapabilityBinding` | adopt conceptually |
| workflow | `WorkflowTemplate` | reserve |
| auth requirement | `credential_ref` | reserve; no real secret storage |
| official plugin | `source=official` capability | adopt |
| app template | Company/Department pack | reserve |

## Workflow / SOP Design

Coze workflows are visual low-code workflows with plugin nodes and business logic. Curis should not adopt a visual workflow builder in Phase-4. The reusable piece is the idea that an agent can call a reviewed plugin or a reviewed workflow node.

Curis mapping:

```text
EmployeeTemplate
-> CapabilityBinding
-> WorkflowStepTemplate.required_capability_types
```

## Reusable For Curis

- Prompt + knowledge + plugin + workflow as separate configuration surfaces.
- Official plugin list with auth state.
- Workflow nodes as future reusable capability calls.
- Visual debugging principle for later workflow traces.

## Not Suitable For Curis

- Full no-code agent/workflow builder in Phase-4.
- Plugin execution without Admin/Workspace capability boundary.
- Agent-first product model without company/department hierarchy.
- Real credential configuration inside Workspace template records.
- Marketplace/plugin sharing before G3/security gates.

## Curis Contract Suggestions

- `CapabilityType` remains model/tool/connector.
- Templates bind to capabilities through `CapabilityBinding`, not by embedding plugin config.
- `WorkflowTemplate` should reserve required capability types and output contracts.
- Official plugins/capabilities remain Admin-owned; tenant_private capabilities remain tenant-scoped.
