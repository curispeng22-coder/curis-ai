# Workspace Package ↔ Company OS Identity / Reference Contract

Status: Frozen

Updated: 2026-08-16

Scope: `WORKSPACE-ENGINEERING-P05-COMPANY-INTEGRATION-001`

Authority: Subordinate to existing Frozen Company OS Shared Authority and ADR-0041; no existing
Frozen Authority is modified.

## 1. Decision

A Package domain object enters Company OS through one stable identity, real Core resolution and
Core-owned relationships. Package JSON never becomes an identity or relationship authority.

```text
workspace_package_objects.object_id
      == runtime_entities.entity_id
runtime_entities.entity_type
      == PACKAGE_DOMAIN_OBJECT
```

The Runtime entity is authoritative for tenant/company/workspace identity, lifecycle integration,
owner, capability/execution references and Company OS links. `workspace_package_objects` is the
existing declarative renderer/read projection and must use the same ID and state.

P0.5 does not migrate historical Package rows. Newly created P0.5 proof objects must satisfy this
contract atomically. A missing Core identity is fail-closed for Company integration.

## 2. Creation invariant

One Core transaction must create:

1. the Package renderer projection;
2. the same-ID `PACKAGE_DOMAIN_OBJECT` Runtime entity;
3. the Package action audit.

If any write fails, none may remain active. The Runtime entity records Package ID/version,
object type/schema version and a Package-validated business-data snapshot. It is a real source and
target for existing `runtime_links`; `runtime_links` itself is not widened to arbitrary IDs.

## 3. Reference invariant

A relationship can be persisted only after Core resolves both endpoints from their native stores
and validates:

- stable ID and expected entity/record type;
- current tenant;
- current company;
- current Workspace where the Core primitive is Workspace-scoped;
- eligible lifecycle/status;
- required binding, authorization, availability and health truth.

Missing, free-text, wrong-type, stale or cross-scope references fail closed before state advance.

## 4. Authoritative mappings

| Business meaning | Authoritative Core fact | Package projection |
| --- | --- | --- |
| Package object identity | `runtime_entities(PACKAGE_DOMAIN_OBJECT)` | same `object_id` row |
| Current Responsibility | validated link to existing `ROLE_SLOT` plus responsibility type | `data.responsibilityRef` read-only Core projection |
| Current Employee/executor | validated link to existing `AI_EMPLOYEE` | `owner_ref` read-only Core projection |
| Effective Capability | validated link to existing `CAPABILITY_BINDING` and current catalog supply | Company-integration read projection |
| Task / Execution | existing `tasks` / `executions` records | resolvable IDs only |
| Evidence | existing Runtime `EVIDENCE` entity and `HAS_EVIDENCE` link | `data.evidenceRef` read-only Core projection |
| Result | existing Artifact plus Runtime `OUTCOME` entity and `HAS_RESULT` link | resolvable result refs only |

`owner_ref`, `responsibilityRef` and `evidenceRef` are reserved Core projections. Package creation
may not submit non-empty values for them. Core writes them only after the native object and
relationship have been validated.

## 5. Responsibility / capability resolution

- The operating command declares a responsibility type (WHAT), not an Employee ID.
- Existing Company OS facts must resolve exactly one eligible Role Slot, assigned Employee and
  active Capability Binding (WHO/HOW).
- Zero or multiple eligible chains are unresolved and fail closed.
- The selected catalog capability must still be active, available, configured, permission-scoped
  and cost-declared when execution begins.
- A Package requirement or label is never a capability grant.

## 6. Task, Evidence, Result and feedback

The existing ResultStore owns Task, Execution and Artifact truth. Existing Runtime entities own
Evidence and Outcome truth. On success:

```text
Task COMPLETED + real Execution + Artifact
→ Runtime EVIDENCE + OUTCOME
→ Core-owned links from PACKAGE_DOMAIN_OBJECT
→ Package state NEW → TRIAGED
```

The Package state may advance only after Task/Execution/Artifact and Evidence/Outcome can all be
resolved. On execution failure, the Task and Execution preserve failure truth, the Package object
remains `NEW`, and no successful Evidence/Outcome link is created.

## 7. Restart / reverse-resolution invariant

After full Desktop restart, one Core query must reconstruct and validate:

```text
Package object
→ Role Slot / current Responsibility
→ Employee
→ Capability Binding + catalog supply
→ Task + Execution
→ Evidence + Outcome + Artifact
```

Reverse `runtime_links` queries must return the same originating object. A display value without
this resolution is not Company Integration evidence.

## 8. Explicit exclusions

- Handoff and Decision P7;
- new Employee, Responsibility, Capability, Task, Evidence or Result stores;
- arbitrary Package IDs in `runtime_links`;
- historical Package data migration;
- Package update/Marketplace/Evolution;
- XHS/RD/TTK migration;
- Shared Runtime refactor or existing Frozen Authority change.

**PACKAGE OBJECT ↔ COMPANY OS IDENTITY / REFERENCE CONTRACT FROZEN FOR P0.5**
