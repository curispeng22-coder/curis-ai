# Workspace Engineering P0.5 — Company OS Integration Definition & Gap Audit

Status: Frozen

Updated: 2026-08-16

Scope: Accepted `customer-feedback-office` P0 substrate versus current Company OS Runtime

Decision: P0.5 DEFINITION / GAP AUDIT APPROVED AND IMPLEMENTED

Implementation: IMPLEMENTED / ACCEPTED

## 1. Audit question

Can the accepted Package substrate run this minimum proof without introducing a second Company OS?

```text
CustomerFeedback
→ real Workspace identity
→ real Responsibility Requirement / current Responsibility
→ real Employee
→ existing Capability
→ real Task / Execution
→ existing Evidence / Result Reference
→ CustomerFeedback state/result feedback
→ Desktop restart recovery
```

Handoff and Decision P7 are conditional. The minimum triage scenario has one holder/executor, no
cross-owner transfer, no external commitment and no CEO judgment, so both are `NOT REQUIRED FOR
P0.5` unless implementation evidence shows a real business trigger.

## 2. Status vocabulary

| Status | Meaning |
| --- | --- |
| ALREADY INTEGRATED | Accepted P0 already uses the real Core fact needed for this proof |
| REUSABLE | The real Company OS primitive/service exists, but the Package path does not yet consume it |
| GAP | The necessary real reference, command, validation or feedback path does not exist |
| NOT REQUIRED FOR P0.5 | Semantics do not require the primitive in the minimum proof |

`REUSABLE` never means integrated. It identifies the existing system that a bounded implementation
must call instead of copying.

## 3. Current P0 truth

Accepted P0 established:

- immutable local Package validation/store/registry/provenance;
- materialization into the existing `workspaces` identity;
- Registry-driven dynamic navigation and generic declarative surfaces;
- Package-scoped `CustomerFeedback` and activity persistence;
- Desktop restart recovery, fail-closed Package action handling and uninstall retention.

P0 did not establish Company OS integration:

- `workspace_package_objects.owner_ref` is text without Core entity validation;
- sample `responsibilityRef` and `evidenceRef` are Package JSON strings;
- accepted evidence used `employee:existing-owner` and `evidence:interview-001`, neither resolved to
  a real Core record;
- the Package object is stored outside `runtime_entities`, so existing `RuntimeFoundation.link()`
  cannot use it as a source/target;
- Package activities are local action audit, not real Task, Execution, Evidence or Result;
- only `core.domain-object.create` exists; no accepted Company operating transition follows it.

These are honest P0 scope limits, not a reversal of `WORKSPACE ENGINEERING P0 ACCEPTED`.

### 3.1 P0.5 closure result

`WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001` closed the audited gaps for the bounded
CustomerFeedback proof:

- Package projection and `runtime_entities(PACKAGE_DOMAIN_OBJECT)` share one object ID;
- Package-authored `owner_ref`, `responsibilityRef` and `evidenceRef` fail closed;
- existing scoped Role Slot, Employee, Capability Binding/catalog supply, Task, Execution,
  Artifact, Runtime Evidence and Outcome are resolved rather than copied;
- success transitions `NEW → TRIAGED` only after durable execution/evidence/result truth;
- a real failed Task/Execution leaves the object `NEW` with no Evidence/Outcome;
- full packaged Desktop restart resolves the same IDs and reverse links;
- Handoff and P7 remain `NOT REQUIRED`; Evolution remains `NOT IMPLEMENTED`.

The original matrix below remains the accepted pre-implementation gap snapshot. Closure evidence
is recorded in the formal Review rather than rewriting the baseline audit as if P0 had already
contained P0.5.

## 4. Gap matrix

| Concern | Status | Current evidence | P0.5 conclusion |
| --- | --- | --- | --- |
| Package install/store/registry/provenance | ALREADY INTEGRATED | Accepted local immutable Package substrate | Reuse unchanged; no update/trust expansion |
| Real Workspace identity and scope | ALREADY INTEGRATED | Package instance materializes an existing `workspaces` row and Runtime version | Use this `workspace_id`; do not create a Package-private workspace identity |
| Declarative surfaces/object creation/restart | ALREADY INTEGRATED | P0 Desktop acceptance | Preserve as earlier-layer regression evidence |
| Package object as Core-linkable identity | GAP | `workspace_package_objects` is outside `runtime_entities` | One authoritative generic Package domain object must participate in existing Runtime Foundation |
| Employee primitive | REUSABLE | Existing `AI_EMPLOYEE` entity, staffing lifecycle and scope checks | Resolve a real available/operating Employee; never copy Employee fields into Package data |
| Package object → Employee link | GAP | `owner_ref` / `responsibilityRef` accepts arbitrary text | Persist a Core-owned validated relation and expose text only as a projection |
| Responsibility Requirement semantics | REUSABLE | Frozen Shared Authority: Process declares WHAT and never names Employee | Customer feedback triage declares a responsibility type/constraints, not an employee ID |
| Organization Routing / current Responsibility | GAP | Shared semantics exist; current concrete work-context command is `CONTENT_ITEM`-specific | Add the smallest generic Package-object integration command using existing staffing/routing truth; do not copy XHS/RD logic |
| Role Slot / responsibility holder facts | REUSABLE | Existing `ROLE_SLOT`, `AI_EMPLOYEE` and Workspace staffing facts | Resolve and validate same-company/workspace active facts |
| Capability Registry / Binding | REUSABLE | Existing catalog, health, authorization and `CAPABILITY_BINDING` review | Select an existing effective capability at execution time; Package requirement is not a grant |
| Customer-feedback capability requirement | NOT REQUIRED FOR P0.5 | Accepted package declares no capability requirements | Core may select an existing effective capability for the Core-owned operating command; do not mutate the accepted Package or invent a grant |
| Task / Execution substrate | REUSABLE | Existing `ResultStore`, orchestrator/execution services and execution adapters | Create/attach a real task/execution; Package activity cannot substitute for it |
| Package object → Task / Execution link | GAP | No task/execution is created or attached | Validate scope and persist the existing execution reference on the authoritative runtime object |
| Evidence primitive | REUSABLE | Existing Runtime `EVIDENCE` entities and `HAS_EVIDENCE` links | Create evidence from the real execution and link it through Runtime Foundation |
| Result / Artifact reference | REUSABLE | Existing execution result/artifact stores and Runtime result-reference patterns | Store real Core result/artifact IDs, not copied summaries as authority |
| Package object → Evidence / Result link | GAP | `evidenceRef` is unvalidated Package JSON | Add Core-owned links plus reverse lookup; reject forged/wrong-scope refs |
| Feedback state/result update | GAP | Package supports create only; `CustomerFeedback` remains `NEW` | Add one Core-owned, schema-validated transition after durable result/evidence exists |
| Failure truth | GAP | Invalid Package actions fail closed, but no Company execution failure exists | Prove one failed execution leaves feedback unadvanced and records retryable failure truth |
| Desktop restart of Company links | GAP | P0 recovered Package object/activity only | Recover Employee/Responsibility/Capability/Execution/Evidence/Result relations and current state |
| Reverse traceability | GAP | No Core relation chain from Employee/Task/Evidence back to feedback | Both originating object and Core facts must reconstruct the same chain |
| Handoff | NOT REQUIRED FOR P0.5 | Minimum proof keeps one current responsibility/employee | Add only if responsibility actually transfers and acknowledgement becomes meaningful |
| Decision P7 | NOT REQUIRED FOR P0.5 | Triage has no CEO judgment/external commitment/sensitive action | Add only on a real Frozen P7 trigger |
| Permission / Computer Access grant | NOT REQUIRED FOR P0.5 | Minimum proof can use an already-effective bounded capability; package requests no access | No permission auto-grant, Agent Adapter widening or Full Computer Access |
| Package update/migration/rollback | NOT REQUIRED FOR P0.5 | Explicitly outside current goal | Remains post-P0.5 |

## 5. Required reference architecture

### 5.1 One authoritative domain-object identity

The target technical proposal already recommends one generic Package domain-object type in the
existing `runtime_entities` / `runtime_links` foundation. P0 implemented a separate object table to
prove the substrate quickly. P0.5 must close that integration gap for newly created proof data.

Candidate rule:

```text
runtime_entities: PACKAGE_DOMAIN_OBJECT (authoritative object identity and scope)
  data_json: package/version/object type/schema version + Package-validated business data
  execution_ref: existing real execution reference when present
runtime_links: authoritative relationships to existing Core entities
Package renderer/API: projection of that same object
```

The existing Package object table must not become a second authoritative copy. A later bounded
Issue must decide the smallest compatibility projection needed by the accepted P0 API. P0.5 uses a
fresh isolated database and does not migrate accepted P0 evidence or active user data.

This is not Package update/migration: it is a Core integration correction for new P0.5 proof data.
Any need to migrate existing Package objects is post-P0.5 and must stop the bounded Issue.

### 5.2 Responsibility and Employee

The Package must not accept `responsibilityRef = employee-id` as assignment truth.

```text
CustomerFeedback declares: CUSTOMER_FEEDBACK_TRIAGE requirement (WHAT)
Company OS resolves: eligible Role Slot / Employee (WHO)
Core persists: current Responsibility / holder / executor relationships
UI or Package JSON displays: projections only
```

The Employee must already exist, be in the same tenant/company/workspace scope and be in an
eligible lifecycle state. The implementation must reuse existing staffing/routing facts. It may
not add a Package Employee table or clone the `CONTENT_ITEM`-specific work-context service.

### 5.3 Capability, Task and Execution

P0.5 does not change the accepted package manifest or add a Package capability grant. A Core-owned
feedback-triage command may resolve an existing effective Capability through the current Company OS
catalog/binding truth, then use the existing Task/Execution substrate.

The execution contract is:

```text
real CustomerFeedback ID
+ real current Responsibility/Employee
+ effective existing Capability
→ real Task ID + Execution ID/ref
→ durable result/artifact
```

If capability, binding, health, authorization or Employee eligibility is missing, execution fails
closed and the feedback cannot become `TRIAGED`.

### 5.4 Evidence, result and feedback

On success, one transactionally ordered Core command must ensure:

1. the child execution has completed successfully;
2. existing Result/Artifact truth can be resolved;
3. a real Runtime `EVIDENCE` entity records the execution/result provenance;
4. Core-owned links connect the feedback object to Evidence/Result;
5. `CustomerFeedback` transitions `NEW → TRIAGED` only after those facts exist;
6. the object records result/evidence IDs as read projections, not as independently trusted truth;
7. audit identifies actor, prior state, command, execution, result and time.

On execution failure, feedback remains `NEW`, the failure and retryability are durable, and no fake
Evidence/Result or `TRIAGED` state is produced.

## 6. Minimum P0.5 Company OS Integration Proof

### 6.1 Success path

1. Start an isolated Desktop/runtime database with a real Company.
2. Install the already accepted `customer-feedback-office` Package and create one real
   `CustomerFeedback` in `NEW`.
3. Materialize/resolve a real active Role Slot, Employee and existing effective Capability through
   current Company OS services.
4. Declare `CUSTOMER_FEEDBACK_TRIAGE` as WHAT; resolve WHO without trusting the Package string.
5. Start one real Core-owned feedback-triage Task/Execution.
6. Persist a real result/artifact and Runtime Evidence linked to the feedback.
7. Transition feedback `NEW → TRIAGED` and expose result/evidence projections.
8. Stop and restart the full Desktop runtime.
9. Prove the same Workspace, feedback, responsibility, Employee, Capability, Task/Execution,
   Evidence/Result, `TRIAGED` state and reverse links recover from SQLite.

### 6.2 Failure path

At minimum, prove both:

- a forged/wrong-type/cross-scope Employee or Evidence/Result reference is rejected before any
  relationship or state change; and
- one real execution failure leaves feedback `NEW`, records failure/retry truth and creates no
  successful Result/Evidence projection.

### 6.3 Handoff and P7

Expected result for this proof:

```text
Handoff: NOT REQUIRED — responsibility does not transfer
Decision P7: NOT REQUIRED — no CEO judgment or governed external action occurs
```

If implementation changes the scenario so either trigger becomes real, the corresponding existing
Core primitive and its acceptance evidence become mandatory. The Issue may not create substitutes.

## 7. P0.5 acceptance boundary

P0.5 is complete only if all of the following pass with real evidence:

- prior Installed and Operational regressions remain green;
- every Company link uses Core IDs and Core-owned validated relationships;
- the success and failure paths in §6 run on isolated SQLite;
- full Desktop restart recovers the complete relationship/result chain;
- forward and reverse traceability agree;
- active SQLite is not touched;
- XHS/RD/TTK focused accepted slices show no regression;
- no second Company OS primitive/store and no permission auto-grant is introduced.

Passing only the reference/link checks permits `COMPANY INTEGRATED ACCEPTED`. Passing the full
business loop, failure path and feedback/restart checks permits `OPERATING ACCEPTED` for this
minimum scenario. It does not permit `EVOLVABLE ACCEPTED`.

## 8. P0.5 versus post-P0.5

| Boundary | P0.5 | Post-P0.5 |
| --- | --- | --- |
| One generic Package object as a Core-linkable identity | Yes | Broader domain optimization only if measured |
| One real Responsibility/Employee/Capability/Task/Execution/Evidence/Result chain | Yes | General routing/operating policy expansion |
| One success + one relevant failure proof | Yes | Multi-stage, multi-team and external-side-effect scenarios |
| Desktop restart of integration truth | Yes | Fleet/distributed recovery |
| Handoff/P7 | Conditional only | Validate when a real Workspace scenario needs them |
| Evolution Acceptance definition | Defined by the contract | Implementation and acceptance |
| Package update/schema migration/rollback | No | Separate bounded Issue after P0.5 |
| Marketplace/signing/publisher trust | No | Separate future program |
| XHS/RD/TTK migration | No | Separate product/runtime decisions |
| Shared Runtime refactor | No | Only if a separately proven cross-cutting blocker exists |

## 9. Implemented bounded Issue

**ID:** `WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001`

**Status:** `IMPLEMENTED / ACCEPTED`

**Single goal:** prove one accepted `CustomerFeedback` can participate in a real Company OS
operating loop and recover after Desktop restart, without Package update/migration or a second
Company OS primitive.

**Candidate allowed files:**

- existing Package Runtime service/API and focused tests;
- existing Runtime Foundation entity-type/state/link registration and the smallest generic
  integration command;
- existing execution adapter/service seam and focused tests;
- one isolated Desktop acceptance evidence directory;
- Issue, Review, Current State/Pointer/Change Log only when acceptance changes current fact.

Exact files and baseline hashes were frozen in the authorized Issue. No broad directory wildcard
was used as an implementation allowance.

**Required checks:**

- all three DB environment variables point to the same isolated DB and active-DB guard fails fast;
- real ID/type/scope/lifecycle validation and reverse links;
- real Task/Execution plus existing Evidence/Result;
- success `NEW → TRIAGED`, execution failure remains `NEW`, forged/cross-scope refs fail closed;
- full Desktop restart recovery;
- P0 Package, Runtime Foundation, XHS and RD focused no-regression checks;
- active SQLite hash/mtime/integrity unchanged.

**Stop conditions:** any need for Frozen Authority changes, Package data migration, Shared Runtime
refactor, XHS/RD/TTK migration, arbitrary extension, Marketplace/update infrastructure or active DB
access.

**Acceptance owner:** Curis Runtime / Quality, closed through
`reviews/WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001_review.md`.

**WORKSPACE ENGINEERING P0.5 DEFINITION / GAP AUDIT FROZEN AND CLOSED**
