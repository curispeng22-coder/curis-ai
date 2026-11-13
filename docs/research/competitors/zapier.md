# Zapier Research

Sources:

- [Zapier Help: How to Create a Zap](https://help.zapier.com/hc/en-us/articles/8496308527629-Create-your-first-Zap)
- [Zapier Platform Docs](https://platform.zapier.com/docs/reference)
- [Wikipedia: Zapier](https://en.wikipedia.org/wiki/Zapier)

Deployment decision: not deployed. Official help docs, platform reference, and Wikipedia were enough to identify the trigger→action step model, app/connection model, and multi-step Zap structure.

## Project Positioning

Zapier is a no-code automation platform that connects thousands of third-party apps. A user builds a "Zap" (automation) as a series of steps: a Trigger (when something happens in app A) followed by one or more Actions (do something in app B/C). It is useful for Curis as a reference for the "integration-as-capability" and "trigger→action step" mental models — directly relevant to `Capability` (connector type), `WorkflowStepTemplate`, and SOP metadata. However, Zapier is an agent-light, fully autonomous, multi-app automation product; its full no-code visual builder and real credential custody are too broad for Phase-4.

## Core Concepts

- Zap: a named automation consisting of a trigger and one or more action steps.
- Trigger: the event that starts a Zap (e.g. "new row in Google Sheets"); only one trigger per Zap.
- Action: a step that performs an operation in an app (e.g. "create a Slack message"); supports create, search, update.
- App / Connection: a third-party integration (Gmail, Slack, Salesforce); each connection holds an authenticated account.
- Multi-step Zap: a Zap with one trigger plus many sequential action steps.
- Filter / Path: conditional branching to control whether a step runs.
- Zap Template (shared): a pre-built Zap other users can copy.
- Zapier Interfaces / Tables: no-code app surfaces layered on top of Zaps (beyond Phase-4 scope).

## Directory / Product Structure

Zapier's conceptual product structure (not Curis code):

```text
Zap
  -> Trigger (single, app-bound event)
  -> Action Step 1 (app operation)
  -> Action Step 2 (app operation)
  -> Filter / Path (conditional)
  -> Connection (auth per app)
  -> Zap Template (shareable copy)

App
  -> Auth / Connection
  -> Triggers
  -> Actions (create/search/update)
```

Curis mapping (reserve only, no execution engine):

```text
EmployeeTemplate
  -> CapabilityBinding (model / tool / connector)
      -> Capability (connector == Zapier "app/connection" concept)
  -> WorkflowTemplate (reserve)
      -> WorkflowStepTemplate (reserve; Zapier "action step")
          -> required_capability_types (connector)
          -> output_contract
```

## Template / Agent / Capability Fields

| Zapier Concept | Curis Mapping | Decision |
| --- | --- | --- |
| app / connection | `Capability` (connector type) | adopt conceptually |
| action step | `WorkflowStepTemplate` | reserve |
| trigger | `WorkflowStepTemplate` (first step) | reserve; no auto runtime |
| Zap template | `WorkflowTemplate` | reserve |
| multi-step Zap | `WorkflowTemplate.step_templates[]` | reserve metadata |
| filter / path | conditional edge | reject for Phase-4 |
| credential / auth | `credential_ref` | reserve; no real secret storage |
| Zapier-owned app catalog | `source=official` capability | adopt |
| shared Zap template | `source=marketplace` | reject until G3 gate |

## Workflow / SOP Design

Zapier models flows as a single trigger followed by an ordered list of action steps, each bound to an app connection. Curis should adopt the *shape* — a step is a unit of work that requires a capability type and produces an output contract — but must NOT adopt the visual builder, the autonomous scheduler, or real connection auth.

Curis mapping:

```text
EmployeeTemplate
-> CapabilityBinding (connector)
-> WorkflowStepTemplate
    -> required_capability_types = ["connector:slack"]
    -> output_contract
    -> owner_employee_template_id
```

Phase-4 may only store SOP step metadata (owner, required capability type, output contract) and trace records. It must not run a Zap-like scheduler or edit live connections.

## Reusable For Curis

- Integration catalog as a capability precedent: each third-party app maps to `capability_type=connector`.
- Trigger→action as the simplest step model for `WorkflowStepTemplate`.
- App connection as the boundary where credentials live outside Workspace — Curis keeps auth behind `ModelGatewayAdapter` / connector boundary.
- Official app catalog mirrors `source=official` capabilities owned by Admin.
- Output contract per step as evidence-oriented `output_contract`.

## Not Suitable For Curis

- Full no-code visual workflow builder in Phase-4.
- Real credential configuration / connection auth inside Workspace template records.
- Marketplace of shared Zaps before G3 / security gates (source boundary is reserved only).
- Autonomous multi-step execution without human review (breaks Task Execution guardrail).
- Agent-first product without company/department hierarchy.
- Filters/paths conditional routing engine in Phase-4.

## Curis Contract Suggestions

- `CapabilityType` remains model/tool/connector — app integrations map to `connector` type.
- Templates bind to capabilities through `CapabilityBinding`, not by embedding integration config.
- `WorkflowTemplate` should reserve required capability types and output contracts.
- Official integrations remain Admin-owned; tenant_private integrations remain tenant-scoped.
- `credential_ref` stays a reference only; no secret storage in template/capability records.
