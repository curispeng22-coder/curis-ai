# Make (Integromat) Research

Sources:

- [Make Help: Scenarios and Modules](https://www.make.com/en/help/scenarios)
- [Make Help: Connections](https://www.make.com/en/help/connections)
- [Wikipedia: Make (software)](https://en.wikipedia.org/wiki/Make_(software))

Deployment decision: not deployed. Official help docs (scenarios, modules, connections, routers) and Wikipedia were enough to identify the scenario/module/router model and the credential boundary.

## Project Positioning

Make (formerly Integromat) is a visual automation platform built around "Scenarios" — directed graphs of "Modules" connected by routes. Unlike Zapier's linear trigger→action list, Make emphasizes a visual canvas with Routers (branching), Aggregators, and Iterators. It is useful for Curis as a reference for the module/connection model and for understanding why a visual DAG builder is the wrong scope for Phase-4. Make is also a pure integration product with no company/department hierarchy, which Curis must not copy as a product center.

## Core Concepts

- Scenario: a visual automation graph (the Make equivalent of a Zap).
- Module: a node that performs an operation (trigger, action, search, transform); maps to an app.
- Router: a branching node that splits the flow into parallel routes.
- Connection: an authenticated link to a third-party app, reused across modules.
- Webhook: an inbound trigger that starts a scenario from an external HTTP call.
- Aggregator / Iterator: data collection / repetition helpers.
- Blueprint: the JSON definition of a scenario (exportable/shareable).
- Data store: persistent key-value storage inside Make.

## Directory / Product Structure

Make's conceptual product structure (not Curis code):

```text
Scenario (blueprint.json)
  -> Module (trigger)
  -> Module (action)
  -> Router
      -> Route A -> Module
      -> Route B -> Module
  -> Webhook (inbound trigger)
  -> Connection (auth per app)
```

Curis mapping (reserve only, no visual engine):

```text
EmployeeTemplate
  -> CapabilityBinding (model / tool / connector)
      -> Capability (connector == Make "app/connection")
  -> WorkflowTemplate (reserve)
      -> WorkflowStepTemplate (reserve; Make "module")
          -> required_capability_types
          -> output_contract
          -> next_step_ids (reserve; no auto routing)
```

## Template / Agent / Capability Fields

| Make Concept | Curis Mapping | Decision |
| --- | --- | --- |
| app / connection | `Capability` (connector type) | adopt conceptually |
| module | `WorkflowStepTemplate` | reserve |
| trigger / webhook | `WorkflowStepTemplate` (first step) | reserve; no auto runtime |
| scenario | `WorkflowTemplate` | reserve |
| blueprint | `WorkflowTemplate.step_templates` / metadata | reserve shape |
| router | conditional branching | reject for Phase-4 |
| aggregator / iterator | data helpers | reject for Phase-4 |
| credential / connection | `credential_ref` | reserve; no real secret storage |
| shared blueprint | `source=marketplace` | reject until G3 gate |

## Workflow / SOP Design

Make models flows as a visual DAG of modules with routes and routers. Curis should adopt only the *module concept* — a step requires a capability type and yields an output contract — and explicitly reject the visual canvas, router-based branching, and live connection editing.

Curis mapping:

```text
EmployeeTemplate
-> CapabilityBinding (connector)
-> WorkflowStepTemplate
    -> required_capability_types = ["connector:http"]
    -> output_contract
    -> owner_employee_template_id
```

Phase-4 may only reserve step metadata (owner, required capability type, output contract, `next_step_ids`). It must not implement a DAG runtime, router execution, or webhook ingestion.

## Reusable For Curis

- Module/connection separation: a module references a shared connection, same as `WorkflowStepTemplate` references a `Capability` via `CapabilityBinding`.
- Blueprint as a serializable scenario definition — informs future `WorkflowTemplate.step_templates` JSON shape.
- Connection reuse across steps — mirrors connectors being bound once and reused by many steps.
- Webhook as an inbound trigger concept — reserve for later `WorkflowStepTemplate` first-step typing.
- Official app list mirrors `source=official` connector capabilities owned by Admin.

## Not Suitable For Curis

- Full visual scenario builder / DAG canvas in Phase-4.
- Router, aggregator, iterator execution engine in Phase-4.
- Real connection auth / credential custody inside Workspace records.
- Marketplace of shared blueprints before G3 / security gates.
- Autonomous scenario execution without human review (breaks Task Execution guardrail).
- Data store as employee/company memory (Phase-4 excludes employee memory).
- Agent/product center without company/department hierarchy.

## Curis Contract Suggestions

- `CapabilityType` remains model/tool/connector — app integrations map to `connector` type.
- Templates bind to capabilities through `CapabilityBinding`, not by embedding module/connection config.
- `WorkflowTemplate` should reserve required capability types and output contracts.
- Official integrations remain Admin-owned; tenant_private integrations remain tenant-scoped.
- `credential_ref` stays a reference only; connections/auth live behind the connector boundary, never in template records.
