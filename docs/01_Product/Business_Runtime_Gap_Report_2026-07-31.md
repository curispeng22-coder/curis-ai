# Business Runtime Gap Report

Status: Review

Baseline: `main @ c0e1855f446a55aa3a384006cfcfed9877130338`

Updated: 2026-07-31

Revision note: Product Blueprint 5.0 is now the current product definition. This report is a historical
diagnostic snapshot; its earlier references to Blueprint 3.0 describe the state at the time of writing.
Product Blueprint 5.0 contains the CEO operating model,
ten module Runtime candidates, Stage Contracts, cross-module loops and
Simulation scenarios. This report remains the diagnostic baseline for the
gaps that existed before that revision; independent Review and Simulation
evidence are still required before implementation.

Decision:
`docs/07_Decisions/ADR-0041-business-runtime-completion-standard.md`

Scope: the single Current Product Blueprint only. No UI, route, API, schema or
business-code implementation is authorized by this report.

## 1. Executive Conclusion

The pre-3.0 Blueprint defined the product, navigation, visual direction and
cross-module flows, but did not define a complete Business Runtime for any
primary Company OS module. Blueprint 3.0 fills the product-planning layer;
this report's remaining concern is acceptance evidence, not page design.

Current maturity:

| Level | Meaning | Modules |
| --- | --- | --- |
| Page only | Page purpose and information zones exist | CEO Office, Business, Organization, Insight, Business Analysis, Knowledge & IP, Workspace Portal |
| Interaction / flow only | Actions or a linear happy path exist, without persisted lifecycle | Business Engineering, Capability, Workspace, Meeting |
| Complete Business Runtime | Lifecycle, state machine, stage contract, feedback, closure and simulation are complete | None |

Conclusion:

```text
Product Definition: complete enough for Runtime design
Business Runtime Blueprint: defined in Blueprint 3.0; independent Review and Simulation incomplete
UI / Code development: BLOCKED
```

## 2. Gap Criteria

A module is Runtime-complete only when it defines:

- Business Lifecycle
- persisted State Machine
- stage-by-stage Runtime
- Input and provenance
- durable Output
- Owner and participants
- Next Stage and transition guard
- feedback and exception paths
- closure and archive
- full Business Runtime Simulation acceptance

Page navigation, buttons, forms, diagrams and high-level arrows do not satisfy
these criteria.

## 3. Module Inventory

| Module | Current Blueprint content | Lifecycle | State Machine | Input / Output | Owner | Feedback | Closure | Simulation | Result |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CEO Office | page layout, operating items, metrics | Missing | Missing | Partial display facts only | Partial: CEO | Missing | Missing | Missing | Page only |
| Business | reality position, four page zones | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Page only |
| Organization | reality position, four page zones | Missing | Missing | Missing | Missing | Missing | Missing | Missing | Page only |
| Business Engineering | analyze → decompose → design → compose → deliver | Partial linear lifecycle | Missing | Partial | Partial: Business Engineering / CEO | Missing | Missing | Missing | Flow only |
| Meeting | company/workspace split and short happy path | Partial | Missing | Partial | Partial: host / CEO | Partial decision return | Missing | Missing | Flow only |
| Capability | resource definition and availability labels | Missing | Labels only | Partial catalog facts | Partial: Company / CEO | Missing | Missing | Missing | Interaction only |
| Insight | signals/trends/alerts page zones | Missing | Missing | Partial source drill-down | Missing | Missing | Missing | Missing | Page only |
| Business Analysis | commission/analysis page zones | Missing | Missing | Partial deliverable concept | Missing | Missing | Missing | Missing | Page only |
| Knowledge & IP | archive/exhibition page zones | Missing | Missing | Partial provenance/version concepts | Missing | Missing | Missing | Missing | Page only |
| Workspace Portal / Workspace | portal, four UI models, short execution flow | Partial | Missing | Partial composition list | Partial: Workspace member | Partial artifact return | Missing | Missing | UI + flow only |

## 4. Detailed Gaps

### 4.1 CEO Office Runtime

Current:

- CEO Office is positioned as the chairman's office.
- It shows decisions, risks, Workspaces and results.
- It offers a general `进入今日经营` action.

Missing:

- Lifecycle from company signal arrival to CEO decision, dispatch, monitoring
  and closure.
- Persisted states such as `observed`, `review_required`,
  `decision_pending`, `dispatched`, `in_execution`, `closed`, `archived`.
- Input provenance from Business, Meeting, Insight, Analysis, Capability and
  Workspace.
- Output contract for decision, priority, delegation and escalation.
- Owner rules for CEO, delegate and system aggregation.
- Feedback from downstream execution.
- Daily operating-cycle closure and archive.
- Simulation from signal arrival through final business result.

Candidate lifecycle:

```text
Signal Received
→ Prioritized
→ CEO Review
→ Decision
→ Dispatched
→ Execution Monitoring
→ Result Confirmed
→ Closed
→ Archived
```

### 4.2 Business Runtime

Current:

- Business is positioned as the company business map.
- The page concept includes portfolio, stage, owner, goal and Workspace.

Missing:

- Business lifecycle from proposal through validation, operation, scale/pivot,
  suspension and closure.
- State transition guards and CEO approval boundary.
- Inputs: opportunity, strategy, capital, resources and market evidence.
- Outputs: approved business charter, operating objectives, Workspace demand,
  review decision and closure package.
- Accountable business owner and supporting departments.
- Workspace operating feedback into business health.
- Failure, pivot, suspension and exit paths.
- End-to-end business launch simulation.

Candidate lifecycle:

```text
Proposed
→ Validating
→ CEO Review
→ Approved / Rejected
→ Preparing
→ Operating
→ Scaling / Pivoting
→ Suspended / Closed
→ Archived
```

### 4.3 Organization Runtime

Current:

- Organization is positioned as the HR and organization center.
- It defines structure, department, employee, role and affiliation views.

Missing:

- Workforce demand, role design, assignment, onboarding, active service,
  review, transfer and offboarding lifecycle.
- Department and employee state machines.
- Owner split between CEO, department owner, HR/system and employee.
- Inputs from Business and Workspace staffing demand.
- Outputs such as role charter, appointment, membership, performance review and
  offboarding record.
- Workload and performance feedback.
- Rules for the non-deletable Business Engineering system department.
- Complete staffing simulation.

Candidate lifecycle:

```text
Demand Raised
→ Role Designed
→ Approved
→ Recruiting / Instantiating
→ Onboarding
→ Active
→ Reviewing
→ Transferred / Offboarded
→ Archived
```

### 4.4 Build Runtime — Business Engineering

Current:

- Correct responsibility boundary is defined.
- A five-step happy path exists:
  analyze → decompose → design → compose → deliver.
- Resource gaps may produce procurement requests.

Missing:

- Request intake, prioritization and acceptance states.
- Stage owners, entry conditions, durable outputs and transition guards.
- Resource-check and procurement waiting loop.
- Workspace Blueprint review and version states.
- Runtime Simulation before delivery.
- CEO approval, rejection, modification and resubmission.
- Adoption monitoring and failed-delivery rollback.
- Completion condition proving the Workspace runs a real business lifecycle.

Candidate lifecycle:

```text
Request Received
→ Triaged
→ Analyzing
→ Decomposed
→ Designing
→ Resource Check
→ Awaiting Procurement (optional)
→ Composing
→ Runtime Simulation
→ CEO Review
→ Delivered / Rework
→ Adoption Monitoring
→ Closed
→ Archived
```

### 4.5 Meeting Runtime

Current:

- Company Meeting and Workspace Meeting are correctly separated.
- Topic, time, type, participants, decision and follow-up are named.
- The existing flow ends after decision and a generic follow-up.

Missing:

- Full Draft-to-Archive lifecycle.
- Discussion rounds and speech permissions.
- AI participant, Knowledge citation and data citation rules.
- Host summary structure and boundary between record and formal decision.
- CEO approval, modification, rejection and reopen transitions.
- Execution Plan creation and decomposition.
- Correlated handoff into Workspace.
- Workspace progress, delay, failure, cancellation and completion feedback.
- Meeting completion and archive conditions.
- Full Meeting Runtime Simulation.

Required lifecycle:

```text
Draft
→ Meeting Created
→ Participants Invited
→ Waiting
→ Discussion
→ Round 1 ... Round n
→ Host Summary
→ Meeting Decision
→ CEO Review
→ Approved / Rejected / Re-discuss
→ Execution Plan
→ Workspace Execution
→ Execution Feedback
→ Completed / Failed / Delayed / Cancelled
→ Archived
```

### 4.6 Capability Runtime

Current:

- Capability is correctly defined as Company Resource.
- Supply, authorization, cost, health and Workspace usage are named.
- Example display labels include available, unauthorized, procurement,
  restricted, failed and expiring.

Missing:

- Resource demand-to-retirement lifecycle.
- Persisted state machine and legal transitions.
- Procurement and authorization owners.
- Evaluation evidence, security checks and cost approval.
- Workspace binding, health monitoring and incident feedback.
- Renewal, suspension, revocation, replacement and retirement paths.
- Business impact output when a Capability fails or expires.
- Full acquisition-and-use simulation.

Candidate lifecycle:

```text
Need Detected
→ Catalog Matched / Not Found
→ Evaluation
→ Procurement Review
→ Authorized
→ Configured
→ Bound to Workspace
→ Active
→ Monitored
→ Suspended / Expired / Replaced
→ Retired
```

### 4.7 Insight Runtime

Current:

- Insight is positioned as the company operating radar.
- Signals, trends, alerts and source drill-down are shown.

Missing:

- Signal capture, validation, severity, assignment and resolution lifecycle.
- State machine separating raw signal from confirmed Insight.
- Input sources and confidence/provenance requirements.
- Owner for validation, triage and action.
- Output contract to CEO Office, Business Analysis or Workspace.
- False-positive dismissal and reopen paths.
- Action feedback and resolution evidence.
- Full signal-to-resolution simulation.

Candidate lifecycle:

```text
Signal Captured
→ Validating
→ Confirmed / Dismissed
→ Triaged
→ Assigned
→ Action Linked
→ Monitoring
→ Resolved / Reopened
→ Archived
```

### 4.8 Analysis Runtime

Current:

- Business Analysis is positioned as the consultant center.
- Commission, evidence, scenarios, advice and CEO decision are named.

Missing:

- Commission-to-follow-up lifecycle.
- State machine for scope, data readiness, draft, review and recommendation.
- Request owner, analyst, data owner and decision owner.
- Input quality and citation requirements.
- Formal analysis deliverable and recommendation output.
- CEO accept/modify/reject decision path.
- Link from accepted recommendation to Workspace execution.
- Outcome feedback into the analysis record.
- Full analysis-to-business-outcome simulation.

Candidate lifecycle:

```text
Commissioned
→ Scoping
→ Data Collecting
→ Analyzing
→ Draft
→ Internal Review
→ Recommendation Issued
→ CEO Decision
→ Execution Follow-up
→ Closed
→ Archived
```

### 4.9 Knowledge Runtime

Current:

- Knowledge & IP is positioned as archive and exhibition hall.
- Source, version, Workspace link, reuse and permission are named.

Missing:

- Capture-to-retirement lifecycle.
- States for review, classification, approval, publication and deprecation.
- Curator, owner, reviewer and consumer roles.
- Provenance, confidentiality and IP ownership inputs.
- Published knowledge, IP asset and reusable context outputs.
- Usage feedback, correction and supersession.
- Retention and archive rules.
- Full capture-to-reuse simulation.

Candidate lifecycle:

```text
Captured
→ Reviewing
→ Classified
→ Approved / Rejected
→ Published
→ Used
→ Updated / Superseded
→ Deprecated
→ Archived
```

### 4.10 Workspace Runtime

Current:

- Workspace is correctly defined as Business Execution Space.
- Four different interface models prove that Workspace UI may vary.
- A short Portal-to-execution-to-result flow exists.

Missing:

- Workspace request, design, approval, provisioning, configuration, simulation,
  active operation, suspension, completion and archive lifecycle.
- Shared Workspace state machine independent of industry UI.
- Blueprint version and running instance relationship.
- Member, resource, module and data readiness checks.
- Business owner, Workspace owner, Business Engineering and system ownership.
- Runtime-specific Input/Output contract.
- Execution feedback into Meeting, Business, Insight and CEO Office.
- Degraded, blocked, failed, cancelled, migration and restore paths.
- Full create-to-archive simulation.

Candidate lifecycle:

```text
Requested
→ Designed
→ Approved
→ Provisioning
→ Configuring
→ Runtime Simulation
→ Active
→ Operating
→ Degraded / Blocked
→ Completed / Suspended
→ Archived
```

Workspace Portal also lacks a portfolio runtime for registration,
availability, attention-required, suspension and archive states. The Portal
must reflect Workspace Runtime facts rather than invent its own status.

## 5. Cross-Module Closure Gaps

| Handoff | Current gap | Required closure |
| --- | --- | --- |
| CEO Office → module | Generic action only | Persist decision, recipient, expected output and due condition |
| Meeting → Workspace | Textual flow only | Execution Plan and correlated Workspace work package |
| Workspace → Meeting | Generic feedback only | Progress/result/failure events update Meeting state |
| Insight → Analysis | No runtime | Confirmed signal opens scoped analysis commission |
| Analysis → CEO Office | Advice concept only | Formal recommendation and CEO disposition |
| Business → Business Engineering | No runtime | Approved business need creates build request |
| Business Engineering → Capability | Procurement concept only | Resource Request with decision and fulfillment state |
| Capability → Workspace | Usage concept only | Authorized binding, health and revocation feedback |
| Workspace → Knowledge & IP | Artifact concept only | Reviewed publication/reuse lifecycle |
| Organization → Workspace | Member concept only | Membership, role, onboarding and offboarding state |

## 6. Missing Acceptance Process

The current Blueprint contains visual and navigation gates but no module-level
Business Runtime Simulation protocol.

Missing acceptance evidence:

- named realistic scenario
- initial state and persisted business object
- participating roles
- input provenance
- full transition log
- durable output at decisive stages
- failure/rejection/retry path
- cross-module handoff correlation
- downstream feedback
- completion and archive evidence
- browser evidence for human work
- backend/database evidence for system work

Until these are defined per module, no primary module is Runtime-complete.

## 7. Business Runtime Blueprint Refactor Plan

### Phase BR-0 — Freeze the standard

Deliverables:

- ADR-0041
- Business Runtime core chapter in the single Product Blueprint
- Runtime stage contract and simulation standard

Exit:

- Product, Architecture, Development, AGENTS and Change Log reference one
  completion standard.

### Phase BR-1 — Define shared runtime grammar

Deliverables:

- canonical stage schema
- state-transition schema
- owner/participant model
- input/output and provenance model
- feedback/correlation model
- exception and terminal-state rules
- Runtime Simulation evidence template

Exit:

- Product Review confirms the grammar can express all ten modules without
  forcing their business lifecycles to be identical.

### Phase BR-2 — Complete three foundation runtimes

Order:

1. Meeting Runtime
2. Workspace Runtime
3. Build Runtime

Reason:

- Meeting creates decisions.
- Workspace receives and executes decisions.
- Business Engineering creates and delivers Workspaces.

Exit:

- Each has full lifecycle, state machine and stage table.
- Meeting → Workspace → feedback closes on paper.
- Three independent Product Reviews pass.

### Phase BR-3 — Complete resource and company runtimes

Order:

1. Capability Runtime
2. Organization Runtime
3. Business Runtime
4. Knowledge Runtime

Exit:

- Resource acquisition, staffing, business activation and knowledge reuse link
  to Workspace Runtime.
- Four independent Product Reviews pass.

### Phase BR-4 — Complete intelligence and CEO runtimes

Order:

1. Insight Runtime
2. Analysis Runtime
3. CEO Office Runtime
4. Workspace Portal portfolio projection

Exit:

- Signal → analysis → CEO decision → execution → feedback is closed.
- Four independent Product Reviews pass.

### Phase BR-5 — Cross-runtime consistency review

Checks:

- state names and terminal meanings
- owners and approval authority
- handoff correlation
- input/output compatibility
- feedback loops
- timeout, retry, delay, failure and cancellation
- Tenant, Company, identity and audit boundaries

Exit:

- no orphan outputs
- no next stage without an owner
- no state without entry/exit rules
- no module marks itself complete from page/API evidence

### Phase BR-6 — Runtime Simulation design

Deliverables:

- one full simulation scenario per primary module
- one combined scenario:
  Business need → Build Runtime → Workspace → Meeting → Execution → Insight →
  Analysis → CEO decision → Knowledge archive
- required fixtures and evidence sources
- pass/block criteria

Exit:

- Product and Quality Review approve the simulations before implementation.

### Phase BR-7 — Unlock implementation

Implementation may begin only when:

- all ten Runtime Blueprints are complete
- all Runtime Blueprint Reviews pass
- cross-runtime review passes
- Runtime Simulation plans are approved
- a scoped business-code Issue names the Runtime stages and transitions it
  implements

Current status:

`BLOCKED_PENDING_BUSINESS_RUNTIME_BLUEPRINT`

## 8. Explicit Non-Actions

- No page, button, route, API, state store, schema or component was implemented.
- No existing Project, Task or Workflow record was migrated.
- No module is declared complete by this report.
- Candidate lifecycles are planning inputs, not yet Frozen module contracts.
- UI and code remain blocked until all Runtime Blueprints pass Review.
