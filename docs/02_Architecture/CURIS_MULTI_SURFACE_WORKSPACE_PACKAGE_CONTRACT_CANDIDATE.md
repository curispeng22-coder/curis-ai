# Curis Multi-Surface Workspace Package Contract Candidate

Status: Review

Authority Class: REVIEW · ARCHITECTURE CONTRACT CANDIDATE

Disposition: CEO ACCEPTED / IMPLEMENTED CONTRACT BASELINE

Verdict: ACCEPTED AND VERIFIED BY `WORKSPACE-ENGINEERING-MULTI-SURFACE-PACKAGE-001`

Owner: Workspace Engineering / Package Track

Date: 2026-08-21

Source: `docs/reviews/CURIS_MULTI_SURFACE_WORKSPACE_PACKAGE_CONTRACT_RESEARCH.md`

Target Authority: Workspace Package Technical Contract

Next Gate: bounded commit reconciliation; future changes require a separate Issue

---

## 1. Contract goal

A Workspace Package declares one complete Professional Workspace with multiple Professional
Surfaces while Curis Core keeps canonical identity, Company OS truth and all execution Runtime.

```text
Workspace Package
→ Domain Navigation
→ Professional Surface Registry
→ Responsibility Requirements (WHAT)
→ Core Routing / Assignment / Employee (WHO)
→ Capability Binding (HOW)
→ shared Work / Result / Evidence truth
```

Surface is Package metadata and user-visible professional composition. It is not a Team, Employee,
Work, Cycle, Result, Session, Runtime or new Workspace.

## 2. Ownership

| Owner | Owns |
|---|---|
| Curis Core | Company/Business/Workspace identity and scope; Package validation/store/pin; route/default/availability resolution; finite component/view/projection/action registries; Team/Responsibility/Assignment/Employee/Capability; Work/Execution/Handoff/Cycle/Result/Evidence/Artifact/Decision/Learning; persistence, permission and recovery |
| Package | Domain Navigation; Professional Surface definitions; Domain Object schemas; Object View/Detail mappings; Responsibility/Capability requirements; bounded shared projection declarations; allowed Core actions; availability, retention and migration metadata |
| Workspace Instance | real IDs and Business relation; Package pin; optional Surface enablement; last active Surface; resolved Assignment/Employee/Capability refs; private Knowledge/credentials/configuration; business objects, Work, Result, Evidence and history |

Package must never contain `employee_id`, credentials, grants, instance data, arbitrary code/SQL,
raw routes, Team assignments or Surface Runtime.

## 3. Candidate package shape

This is a logical contract candidate, not the current manifest and not a frozen JSON Schema.

```text
workspace-package/
├── manifest.json
├── domain-navigation.json
├── professional-surfaces.json
├── object-views.json
├── responsibility-requirements.json
├── projection-profiles.json
├── schemas/
└── migrations/                 # only when required by accepted lifecycle contract
```

Candidate manifest references:

```json
{
  "schemaVersion": "curis.workspace-package/v2",
  "packageId": "domain-neutral.stable.package-id",
  "publisher": "stable publisher identity",
  "version": "0.x.y",
  "coreCompatibility": "bounded Core range",
  "workspace": {
    "name": "Workspace display name",
    "navigation": { "label": "Company-level entry", "icon": "Core icon ref" },
    "domainNavigation": "domain-navigation.json",
    "surfaceRegistry": "professional-surfaces.json",
    "defaultSurfaceRef": "stable-surface-key"
  },
  "domainSchemas": {},
  "objectViews": "object-views.json",
  "responsibilityRequirements": "responsibility-requirements.json",
  "projectionProfiles": "projection-profiles.json",
  "capabilityRequirements": [],
  "actions": [],
  "retention": "Core-known retention contract",
  "migrationManifest": "optional accepted migration ref"
}
```

The current P0 `surfaces.json = main/context/utility` contract remains legacy v1. It must not be
silently reinterpreted as the Professional Surface Registry.

## 4. Domain Navigation contract

Each navigation item declares only:

- stable `key`;
- `label`;
- `surfaceRef`;
- stable `order` and optional `group`;
- `availabilityRef` when conditional.

Package does not declare an href. Core derives route state from `workspace_id + surface_key` and
keeps `workspace_id` canonical. Navigation never owns execution and must not reorder itself from
daily operating state.

## 5. Professional Surface contract

Each Surface minimally declares:

| Concern | Contract meaning |
|---|---|
| `key` | Stable Package-scoped reference; not a Core entity ID |
| `purpose` | Stable professional problem/decision area |
| navigation relation | One or more Domain Navigation items may reference it |
| default eligibility | May be the Package default candidate only when eligible |
| Domain Objects | Relevant Package object types, not duplicated objects |
| Object Views | Primary and supported named view refs |
| Responsibility Requirements | WHAT refs only |
| Capability Requirements | Requirement refs only, never grants |
| Projection profile | Bounded Core Work/Result/Evidence selection |
| Detail / Utility mapping | Selected object → Core-registered detail/editor/preview/tool |
| availability | `REQUIRED`, `OPTIONAL` or `CONDITIONAL` plus named condition refs |

No Surface may declare Team, Employee, Work lifecycle, Cycle, Result/Evidence ownership, Session or
Runtime.

## 6. Responsibility contract

Each Package Responsibility Requirement declares a stable Domain semantic ref, purpose, Workspace
scope, required Capability refs and the Surface refs that consume it.

Resolution is exclusively:

```text
Requirement
→ Organization Routing
→ Workspace-scoped Assignment
→ Employee Holder / verified Executor
```

Missing real Requirement/Assignment/Employee/Capability is fail-closed. Required gaps block
Operational activation; optional gaps make only that Surface unavailable. Package installation may
remain DRAFT with an explicit gap report. Package never selects an Employee.

## 7. Object/View/Projection boundary

- Domain Object is persisted business truth.
- Object View is a finite Core-registered presentation over Domain Objects.
- Professional Surface organizes views, actions and shared projections.
- Detail/Utility maps the selected object to a registered detail/editor/preview/tool.
- Artifact, Result and Evidence remain Core-owned entities/references.
- Package projection profiles may use only current Workspace scope, declared object types,
  Requirement refs and Core-known relation/lifecycle selectors; no arbitrary query language.

XHS Calendar therefore remains a Content Operating Object View, not a Surface.

## 8. Availability/default/fallback

| Mode | Behavior |
|---|---|
| REQUIRED | Must resolve before Workspace is Operational |
| OPTIONAL | Instance explicitly enables/disables it; other Surfaces remain valid |
| CONDITIONAL | Core evaluates named conditions; unknown fails closed |

Core default resolution:

1. valid explicit deep link;
2. last active eligible Surface;
3. eligible Package default candidate;
4. first eligible required Surface in stable order;
5. Core-owned Workspace Gap surface.

Package does not define fallback chains. Stage/capability changes may mark an item unavailable but do
not silently reorder navigation, force page jumps or change Work/Holder/Cycle.

## 9. Versioning and identity continuity

- Navigation, Surface Registry, requirements, views and projections are Package-version and
  digest-covered truth.
- Workspace identity and route remain stable across Package versions.
- Surface keys are stable within the Package contract; label changes do not change identity.
- Running Work/Cycle keeps immutable Operating Definition and Package/Surface origin refs.
- Activation cannot rewrite Assignment, Employee, Capability grant, Work, Result or Evidence.
- Changed/removed Surface keys require explicit compatibility/impact handling.
- Surface removal never deletes instance data or historical Work.
- Schema/data migration uses accepted transactional migration; file rollback is not data rollback.

## 10. Contract examples

### XHS

`内容增长部 / 小红书运营 / AI 科技` can declare candidate Surfaces for Operating Overview,
Research Insights, Content Operating, Growth Analytics, User Feedback and optional
Commercialization. Exact labels/order remain unfrozen. Calendar is a Content Operating Object View.

### RD

The same contract can express candidate Development, Build/Test, Release and Architecture Surfaces.
Code, Diff, Terminal, Test and Artifact are registered views/tools. The final RD menu is not frozen.

### E-commerce

Product, Inventory, Order, Channel, Marketing, Customer Service, Content Production and Finance fit
as Surfaces only under one accountable Workspace boundary. Independent goals/team boundaries become
sibling Workspaces under the Business—never Sub-Workspace or Surface Runtime.

## 11. Required validator invariants

```text
WORKSPACE_ID_OWNED_BY_CORE
SURFACE_KEY_PACKAGE_SCOPED_NOT_CANONICAL_ENTITY
DOMAIN_NAV_ITEM_RESOLVES_ONE_DECLARED_SURFACE
DEFAULT_SURFACE_IS_DECLARED
SURFACE_DECLARES_REQUIREMENT_NOT_EMPLOYEE
CAPABILITY_REQUIREMENT_IS_NOT_GRANT
SHARED_PROJECTION_IS_WORKSPACE_SCOPED
OBJECT_VIEW_IS_NOT_SURFACE_IDENTITY
NO_SURFACE_TEAM
NO_SURFACE_RUNTIME
NO_RAW_ROUTE_OR_ARBITRARY_QUERY
RUNNING_WORK_PINNED_TO_IMMUTABLE_ORIGIN
REMOVED_SURFACE_DOES_NOT_DELETE_DATA
UNKNOWN_AVAILABILITY_FAILS_CLOSED
```

## 12. Minimal bounded Implementation Issue input

Suggested Issue:

`WORKSPACE-ENGINEERING-MULTI-SURFACE-PACKAGE-001`

Single proof:

> An already built Curis installs one previously absent unknown multi-Surface Package, renders stable
> Domain Navigation, switches at least three Professional Surfaces under one `workspace_id`, resolves
> real Responsibility/Employee/Capability gaps fail-closed, consumes real shared Work/Result/Evidence,
> restores selected/default behavior after Desktop restart, and preserves running operating truth
> across one Package version transition.

Minimal implementation scope:

1. versioned v2 Package validator alongside readable v1;
2. Domain Navigation + Professional Surface Registry compiled model;
3. Core-derived Surface route/default/last-active/gap resolution;
4. generic Requirement/Assignment/Capability resolver;
5. finite Object View/Detail and shared projection registry;
6. one generic multi-Surface renderer and isolated Desktop proof.

Explicit non-goals: Marketplace/PKI, arbitrary code, Workflow/DAG, Sub-Workspace, Surface Runtime,
general low-code UI, RD/XHS migration, final Domain menus, full cross-Surface Autonomous E2E.

## 13. Candidate decision

```text
MULTI-SURFACE PACKAGE CONTRACT = ACCEPTED
CURRENT RUNTIME SUPPORT = PARTIAL / NOT IMPLEMENTED
SURFACE REGISTRY = REQUIRED PACKAGE METADATA
PACKAGE KNOWS EMPLOYEE = NO
DOMAIN NAVIGATION DECLARER = PACKAGE; VALIDATOR/RESOLVER/RENDERER = CORE
WORKSPACE IDENTITY ACROSS SURFACES = STABLE
SUB-WORKSPACE / SURFACE RUNTIME = NOT REQUIRED
IMPLEMENTATION AUTHORIZATION = BOUNDED ISSUE ONLY
```

Proceed only through the bounded Issue and stop at its Implementation Review.
