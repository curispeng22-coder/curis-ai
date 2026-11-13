# ADR-0040: One-Person AI Company OS, Fixed Core and Open Workspace

Status: Frozen

Baseline: main @ c0e1855f

Updated: 2026-07-31

Module: Product Definition

## Decision

Curis is a product for one-person company founders. Each current Company
Runtime is operated by one real CEO and a set of AI Employees. Curis helps the
CEO build, run, verify, optimize and expand a company; it is not a task manager,
workflow platform, Agent collection, tool platform or generic automation
product.

The current delivery is one Local Desktop used by one CEO. The future
commercial product has two logical layers:

~~~text
Curis Platform / Admin
→ capability supply, business patterns, versions, tenants and commercial service

Company Runtime
→ one CEO's company, businesses, AI Employees, Workspaces, commitments,
  evidence and decisions
~~~

The layers are intentionally co-located during self-validation. Billing,
Marketplace, multi-tenant administration and a physical split are future
scope, not current capability.

Curis has two product structures:

~~~text
Company OS
├── fixed business semantics, lifecycle, permissions and evidence rules
├── CEO surfaces: 经营 / 业务 / 公司 / 工作空间
└── cross-cutting Truth, Decision, CEO Assistant and Change runtime

Workspace
├── open business-specific execution space
├── variable layout, components and working model
└── composed AI Employee, Tool, Knowledge, Capability and Resource
~~~

Company OS is fixed. Workspace is open. Project, Task, Workflow and Artifact
may be used inside a Workspace, but they are not the product root or primary
navigation.

The Company Runtime actor model is explicit:

~~~text
Company
├── CEO                         human Owner / final decision
├── CEO Assistant                one persistent Company-level AI Employee
├── Professional AI Employees    stable professional result owners
└── Workspace AI                 Workspace-scoped runtime executors
~~~

CEO Assistant is a first-class object with its own responsibility contract,
context, capability, authority, quality evidence and lifecycle:

~~~text
Created → Configured → Learning Context → Operating
→ Evaluating → Upgraded / Reassigned
~~~

Operational reporting follows the same graph: the Assistant reports to the
CEO; Professional AI Employees report operationally to the Assistant while
owning their professional results; Workspace AI reports to the relevant
Professional AI / Workspace owner and escalates cross-business or high-impact
issues to the Assistant and then the CEO. This is an authorization and
accountability graph, not a human-style hierarchy or a flat Agent list.

## CEO surfaces

The four fixed surfaces answer different operating questions:

- 经营：现在发生了什么，什么需要 CEO 处理？
- 业务：公司为谁创造什么价值，是否值得继续投入？
- 公司：公司是否有能力兑现当前承诺？
- 工作空间：业务如何被交付，结果是否正在形成？

“建设” is a state mode, not a permanent primary navigation item.
Meeting, Knowledge, Analysis and Assistant are mechanisms or projections, not
parallel operating centers.

CEO Assistant is nevertheless a real Company Runtime actor, not merely a
global entry. It is the CEO's first AI Employee and Chief of Staff: it briefs,
prepares, classifies requests, convenes specialist AI Employees, tracks
handoffs, packages decisions, monitors exceptions and closes the operating
day. `CEO Operating Day` is its primary CEO surface; the Global Assistant
Runtime remains the shared identity, notification, query and command
infrastructure. The Assistant may execute reversible, authorized actions but
cannot silently make high-impact decisions or external commitments.

## Company design and organization

A company grows from results and responsibilities:

~~~text
Outcome gap → stable responsibility → required capability
→ repeated coordination → Department or Shared Service
~~~

A Department is not required on day one and is not a name/member CRUD object.
When created, it must define its purpose, responsibilities, capabilities,
capacity, authority, dependencies, service commitments and exit conditions.

AI Employees are real responsibility-bearing actors. Each AI Employee has a
role, result, business/data/action scope, capability contract, evidence
requirement, cost/quality boundary, escalation rule and fallback. The CEO
owns intent, business bets, high-impact resource decisions, authority and
acceptance. AI Employees operate within approved boundaries.

## Capability and Workspace

Capability is a Company Resource. It describes what can be done; Capacity
describes how much is currently available. Allocation binds available capacity
to a business commitment. A capability cannot be treated as available merely
because it is registered.

Workspace means Business Execution Space. A Workspace is created only when a
business has recurring multi-actor coordination, stable cycles, dedicated
capabilities/data/permissions, or independent evidence and closure needs.
Workspace must define a Business Runtime and pass a Runtime Simulation before
implementation acceptance.

Workspace is built in a separate `Workspace Studio` before it is operated.
Business Engineering analyzes the business, creates a versioned Workspace
Blueprint, composes stages/role slots/AI/Tools/Knowledge/Evidence rules,
checks capacity and authorization, simulates normal and failure paths, and
submits an impact-aware version for CEO approval. Approved Blueprints create a
Workspace Runtime version; Studio drafts cannot silently mutate a running
Workspace.

## External result and evidence

Curis owns operating facts, commitments, decisions and interpretations.
External systems may own raw execution facts, publishing, builds, analytics or
transactions. Curis may receive external evidence through an authorized API or
a CEO-entered evidence record with source, time window, provenance and
confidence. Neither source type is allowed to bypass the same Evidence and
Decision runtime.

## Consequences

- Product change order is Product Truth → Business Runtime → UI Design → Code.
- Product completion requires a complete business lifecycle, persisted state
  machine, owners, inputs/outputs, feedback, closure and Runtime Simulation.
- The first real business is Curis self-development: Curis uses its own
  software-development AI workforce to improve Curis.
- Current Product Blueprint is the single target-state source; Current State
  continues to describe delivered fact.
- The current local product must not be described as the future Platform/Admin
  commercial split.
