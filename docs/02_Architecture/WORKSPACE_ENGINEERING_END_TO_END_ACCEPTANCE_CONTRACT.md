# Workspace Engineering End-to-End Acceptance Contract

Status: Frozen

Updated: 2026-08-16

Scope: All declarative Workspace Package deliveries built on Curis Core

Decision: WORKSPACE ENGINEERING END-TO-END ACCEPTANCE CONTRACT FROZEN

## 1. Purpose

Workspace Engineering uses one cumulative success standard:

```text
Installed → Operational → Company Integrated → Operating → Evolvable
```

This is a general delivery contract. It is not specific to
`customer-feedback-office` and does not turn a page, API, field, test or copied reference into
business acceptance.

The five layers answer five different questions:

| Layer | Question |
| --- | --- |
| Installed | Can an already-built Curis safely acquire and register this Workspace? |
| Operational | Can the installed Workspace perform its own declared work and preserve its facts? |
| Company Integrated | Does that work use the real Company OS identity, people, responsibility, capability, execution and result facts? |
| Operating | Does one realistic business loop run through those facts and feed the result back to the originating object? |
| Evolvable | Can an accepted Workspace change without losing truth, compatibility or the relevant acceptance gates? |

Each later layer includes all earlier layers. A delivery must declare the highest layer it has
actually proven. Layers cannot be skipped or inferred from source existence.

## 2. Governing truth

- `ADR-0041 Business Runtime Completion Standard` remains the completion authority: realistic
  operation, persisted state, real identity, durable output, exception truth and downstream
  feedback are required.
- Company OS Shared Authority remains authoritative for Responsibility Requirement,
  Organization Routing, Shared Employee Service Relation and Context Isolation.
- Curis Core owns Employee, Responsibility, Capability, Task / Execution, Handoff, Decision P7,
  Evidence and Result. A Package may reference or compose these facts; it may not redefine or
  duplicate them.
- Package requirements are requests. They are not grants, bindings, health, authorization or
  effective execution proof.
- This contract is the accepted cumulative delivery standard. It does not by itself authorize a
  future implementation Issue or modify the existing Company OS Frozen Authority.

## 3. Cross-layer acceptance rules

### 3.1 Real reference rule

A Company OS relationship is accepted only when all of the following are true:

1. the target is a real Core-owned record with a stable Core ID;
2. Core resolves the ID and validates entity type, tenant, company, workspace, lifecycle and any
   required authorization / health state;
3. the relationship is persisted through the existing Core-owned relationship or native service
   boundary;
4. both the Workspace object and the related Core fact can be traced back to each other;
5. restart preserves the relationship and its audit provenance;
6. missing, forged, stale or cross-scope IDs fail closed.

Copied labels, free-text IDs, Package JSON fields, UI strings and unvalidated `owner_ref` values are
display/input data only. They are not authoritative Company OS relationships.

### 3.2 Conditional primitive rule

- A `Handoff` is required only when accountability or execution responsibility actually moves to
  another holder / stage. One Employee completing one responsibility requires no artificial
  Handoff.
- Decision P7 is required only when the business situation requires CEO judgment, approval,
  external commitment, sensitive action or another Frozen P7 trigger. A deterministic low-risk
  result must not be routed through P7 merely to cover the primitive.
- When Handoff or P7 is not semantically required, acceptance records `NOT REQUIRED` and the
  reason. This is not a skipped gate.

### 3.3 Evidence rule

Acceptance evidence must identify the build/runtime under test, real IDs, scopes, state
transitions, durable outputs and restart observations. Mock state, hand-edited database rows and
screenshots without backend/data correlation cannot close a layer.

## 4. Layer acceptance

### 4.1 Installed Acceptance

`INSTALLED ACCEPTED` requires:

1. a Package unknown to the acceptance build is validated against a bounded declarative contract;
2. immutable package ID, version, digest, source provenance and Core compatibility are recorded;
3. installation materializes a real tenant/company-scoped Workspace identity;
4. navigation and active Registry state are derived from the installed Package, not compiled
   Package-specific code;
5. invalid package/path/schema/action/conflict inputs fail closed without partial active state;
6. disable/uninstall truth and the declared data-retention rule are observable;
7. install does not grant Capability, Connector, Computer Access, secrets or code execution.

Not sufficient: source files exist, a route was compiled, install API returned success, or a static
navigation item was added.

### 4.2 Operational Acceptance

`OPERATIONAL ACCEPTED` requires Installed Acceptance plus:

1. Main / Context / Utility render through approved Core declarative components;
2. at least one declared domain object is created through an allowed Core action;
3. schema, state, tenant, company, workspace and instance boundaries are enforced;
4. domain state and action audit are durably persisted in the existing SQLite boundary;
5. full Desktop restart restores Registry, Workspace, surfaces, object and activity facts;
6. unsupported actions and invalid object input fail closed without false success or residue;
7. uninstall removes active navigation/runtime access and applies the explicit retention/archive
   rule.

This layer proves that the installed Workspace works as a controlled declarative Runtime. It does
not prove that the Workspace is part of Company operations.

### 4.3 Company Integration Acceptance

`COMPANY INTEGRATED ACCEPTED` requires Operational Acceptance plus:

1. the Package object participates in the real Workspace / Company scope and has a Core-linkable
   identity;
2. a Responsibility Requirement declares WHAT without naming an Employee as WHO;
3. existing Organization / staffing / routing truth resolves a real eligible Employee and the real
   Role Slot / current responsibility relation;
4. execution validates an existing Capability and its current binding, availability, health and
   authorization truth; a requirement alone is not a grant;
5. a real existing Task and Execution are created or attached through the existing execution
   substrate;
6. durable existing Evidence / Result facts reference the execution and are linked back to the
   originating Package object;
7. forward and reverse queries reconstruct Object → Responsibility → Employee → Capability →
   Task / Execution → Evidence / Result without trusting copied strings;
8. forged, missing, stale, wrong-type and cross-scope references fail closed;
9. Desktop restart recovers the same Core relationships and current truth;
10. no Package-private Employee, Responsibility, Capability, Task, Execution, Handoff, P7,
    Evidence or Result store exists.

### 4.4 Operating Acceptance

`OPERATING ACCEPTED` requires Company Integration Acceptance plus one realistic Business Runtime
Simulation:

1. a real business trigger creates or selects the originating domain object;
2. the starting business state and input provenance are persisted;
3. Responsibility is resolved, a real Employee becomes the current holder/executor, and only the
   task-scoped context is assembled;
4. an effective existing Capability performs a real Task / Execution;
5. the execution produces durable Evidence / Result rather than a UI-only status;
6. the originating object changes state only after the required result is durably recorded;
7. owner, current executor, next responsibility/stage and audit facts remain distinguishable;
8. at least one relevant failure/retry path preserves failure truth and does not advance the object
   falsely;
9. downstream result feedback updates the originating object and can be traced in both directions;
10. Desktop restart restores the current operating state, relationships, result and next action;
11. Handoff and P7 are used only when their business triggers occur, under §3.2;
12. completion/archive conditions are explicit for the tested operating loop.

### 4.5 Evolution Acceptance

`EVOLVABLE ACCEPTED` requires Operating Acceptance plus a separately authorized evolution proof:

1. the change has an explicit package, semantic model and operating-model version boundary;
2. impact analysis identifies the earliest affected Lifecycle stage and all Relevant Gates;
3. unaffected accepted evidence is reused; affected gates are re-run and cannot be skipped;
4. compatibility rules cover persisted domain objects and all Company OS links;
5. upgrade/migration is explicit, testable, restart-safe and never inferred from a new manifest;
6. rollback or forward recovery preserves provenance and never reports a mixed version as healthy;
7. installed instances can identify current, candidate and failed evolution truth;
8. one real instance completes the declared evolution and resumes Operating Acceptance.

Evolution Acceptance is a future boundary only. It does not authorize Package update, migration,
rollback, Marketplace or publisher trust work.

## 5. Current evidence classification

The accepted `com.curis.sample.customer-feedback-office@0.1.0` P0 and P0.5 evidence supports:

| Layer | Current classification | Reason |
| --- | --- | --- |
| Installed | ACCEPTED by P0 record | Real build-before-Package Desktop install, Registry/navigation and uninstall truth |
| Operational | ACCEPTED by P0 record | Declarative surfaces, one persisted object/activity, restart and retention proof |
| Company Integrated | ACCEPTED by P0.5 record | Same-ID Core object identity; real scoped Role Slot, Employee, Capability Binding/catalog supply, Task, Execution, Artifact, Evidence and Outcome resolve in both directions after Desktop restart |
| Operating | ACCEPTED by P0.5 record | Real success and failure loops preserve execution truth; success feeds Evidence/Result back and transitions `NEW → TRIAGED`, while failure remains `NEW` without false Evidence/Result |
| Evolvable | NOT YET ACCEPTED | Update/migration/evolution was explicitly outside P0 and remains outside P0.5 |

P0.5 adds Company Integration and Operating evidence without reopening or weakening P0. It does
not turn the same instance into an Evolvable Workspace.

## 6. P0.5 boundary

P0.5 targeted and accepted:

- Company Integration Acceptance for one `CustomerFeedback`;
- one minimal Operating Acceptance loop using existing Core primitives;
- restart and fail-closed relationship evidence;
- Handoff/P7 `NOT REQUIRED` unless the scenario actually triggers them.

P0.5 did not target:

- Evolution Acceptance implementation;
- Package update, schema migration, rollback or Marketplace;
- arbitrary extension code;
- XHS/RD/TTK migration;
- Shared Runtime refactoring;
- a new UI or a second Company OS primitive.

## 7. Acceptance declaration format

Every future Workspace Engineering Review must state:

```text
Highest accepted layer: <Installed | Operational | Company Integrated | Operating | Evolvable>
Earlier layers: <evidence references>
Current layer: <PASS/FAIL by criterion>
Handoff: <USED with evidence | NOT REQUIRED with reason>
Decision P7: <USED with evidence | NOT REQUIRED with reason>
Known gaps: <explicit list>
Not claimed: <later layers and excluded capabilities>
```

**WORKSPACE ENGINEERING END-TO-END ACCEPTANCE CONTRACT FROZEN**
