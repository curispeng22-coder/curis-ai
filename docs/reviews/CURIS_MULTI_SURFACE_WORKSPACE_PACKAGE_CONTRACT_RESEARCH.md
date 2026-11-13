# Curis Multi-Surface Workspace Package Contract Research

Status: Review

Authority Class: RESEARCH

Disposition: RESEARCH COMPLETE / CEO REVIEW REQUIRED

Verdict: CURRENT PACKAGE PARTIAL / MINIMAL CONTRACT GAP IDENTIFIED

Owner: Workspace Engineering / Package Track

Date: 2026-08-21

Next Action: CEO review the companion contract candidate

Target Authority: `docs/02_Architecture/CURIS_MULTI_SURFACE_WORKSPACE_PACKAGE_CONTRACT_CANDIDATE.md`

Next Gate: bounded Implementation Issue only after CEO acceptance

Implementation Authorization: NONE

---

## 1. Purpose and truth boundary

This research answers one question:

> How can a Workspace Package declare a complete multi-Surface Professional Workspace without
> owning Company OS Runtime or embedding Domain semantics in Curis Core?

Current Product Truth is already Frozen: Workspace is a complete professional operating
environment, not a Page; one long-term Workspace has one canonical accountable Operating Team
responsibility boundary and may contain multiple Professional Surfaces. This document does not
reopen that decision and does not treat it as implemented.

No Runtime, Schema, database, Frontend, production Package, RD implementation or XHS implementation
was changed.

## 2. Inputs and authority classification

| Input | Authority / status | How it is used |
|---|---|---|
| Product Blueprint 5.5 | CURRENT / Frozen | Product definition: Professional Workspace, Team × Surface, Four-Pane responsibilities |
| Product Master Map 3.1 | CURRENT / Frozen | Product objects, entry, action, field and source expansion |
| Current UI Blueprint | CURRENT / Frozen | Context/Main/Utility responsibility model; not Package Schema |
| Company OS Shared Authority §9 | SHARED AUTHORITY / Frozen | One Team boundary, WHAT→WHO bridge, shared Truth, no Surface Runtime |
| Professional Workspace Authority Reconciliation | REVIEW / Frozen / CEO ACCEPTED | Exact accepted reconciliation and open implementation gaps |
| Workspace Engineering Methodology / Lifecycle | METHODOLOGY / Review | Package-first derivation and relevant Gates |
| Workspace Package Technical Proposal | ARCHITECTURE / Review | Candidate direction; stale P0 wording does not override Runtime evidence |
| Current State + P0/P0.5/P1/P1.5 Reviews | IMPLEMENTATION TRUTH / Frozen + accepted evidence | What Package Runtime actually proves |
| `workspace_package_runtime.py` and Package API/UI | CURRENT CODE / RUNTIME EVIDENCE | Exact manifest, validation, registration, route and renderer behavior |
| XHS Instance Authority reconciliation | INSTANCE AUTHORITY / reconciled | Primary Domain example; menu details remain unfrozen |
| RD Instance Spec | INSTANCE DESIGN INPUT / legacy status vocabulary | Cross-check only; does not freeze a final RD menu or Package migration |

No Current Authority conflict was found. Product → Implementation gaps are explicit.

## 3. Current Package reality

### 3.1 Exact current manifest

The accepted Runtime validates exactly:

```text
schemaVersion = curis.workspace-package/v1
packageId
version
coreCompatibility
workspace {
  name
  navigation { label, icon }
}
surfaces                  # file ref
domainSchemas             # object type → schema file ref
actions                   # currently exactly core.domain-object.create
capabilityRequirements    # currently must be []
retention                 # retain-business-data-read-only
migrationManifest?        # bounded P1.5 rename migration
```

The current `surfaces` file must contain exactly three keys:

```text
main    → object-list
context → object-detail
utility → object-create-form
```

All three must target a Package Domain Object schema. This is a bounded P0 renderer contract, not a
Professional Surface Registry.

### 3.2 Current operational proof

Current accepted evidence proves:

- install of a previously absent declarative Package after Desktop build;
- one generated canonical `workspace_id` and Package instance identity;
- one company-level dynamic Workspace navigation item;
- fixed Main / Context / Utility declarative rendering;
- Package Domain Object persistence and same-ID Core projection;
- fail-closed real Responsibility / Employee / Capability / Task / Execution / Evidence / Result
  integration for the customer-feedback proof;
- Package version pin, schema-stable update/restart/rollback;
- bounded transactional `renameField` data migration with failure atomicity;
- disable/uninstall navigation removal and read-only business-data retention.

It does not prove generic Domain Navigation, multiple Professional Surfaces or a Surface-selected
shared operating projection.

## 4. Capability audit

### 4.1 Summary

| Concern | Finding | Evidence / consequence |
|---|---|---|
| Package identity/version/digest | ALREADY SUPPORTS | Stable package ID/version, digest, store, registry and instance pin exist |
| Publisher metadata | MISSING | Runtime records digest/source path but current manifest has no publisher field or publisher trust contract |
| Workspace identity | ALREADY SUPPORTS | Core creates stable `workspace_id`; update/rollback preserve it |
| Canonical Workspace route | ALREADY SUPPORTS | Core derives `/ceo-office/workspace/installed/{workspace_id}` |
| Company-level Workspace navigation | ALREADY SUPPORTS | One label/icon/href per active Package instance |
| Package Domain Object schema | ALREADY SUPPORTS | Bounded string/enum object schema and persisted `data_json` |
| Safe action registry | ALREADY SUPPORTS | One allowlisted create action; unknown action fails closed |
| Version pin/restart/rollback | ALREADY SUPPORTS | P1 schema-stable lifecycle and P1.5 bounded data migration |
| Shared Core reference integrity | ALREADY SUPPORTS / BOUNDED | Same-ID projection and scoped Core references are fail-closed |
| Domain Navigation | MISSING | Current navigation is company-level Workspace entry only |
| Professional Surface Registry | MISSING | Current `surfaces` means fixed Pane slots, not professional work areas |
| Surface responsibility requirements | MISSING | No Package declaration or generic resolver path |
| Capability requirements | PARTIAL | Field exists but validator requires an empty list |
| Object View registry | PARTIAL | One list/detail/create combination; no named view registry or mapping |
| Detail / Utility mapping | PARTIAL | Utility is always create form; Context is always object detail |
| Work projection | MISSING | No generic selection of real scoped Work by Surface |
| Result / Evidence projection | PARTIAL | P0.5 exposes one object integration projection, not Package-declared rules |
| Shared Team / Employee Work Area projection | REUSABLE | Shared Company OS Runtime exists; Package-specific projection contract is missing |
| Optional / conditional Surface | MISSING | No activation/availability model |
| Default / last active / fallback | MISSING | One fixed Main; no Surface selection state or fallback resolution |
| Surface route/deep link | MISSING | No `workspace_id + surface key` route state |
| Multi-Surface UI | MISSING | Installed renderer is one technical object-list screen |
| Cross-Surface execution | REUSABLE / GAP | Workspace-scoped operating Core exists; generic multi-Work Surface projection E2E is unproven |
| Multiple same-Package instances | MISSING | Current uniqueness prevents a second same company/package/version instance |
| RD/XHS as Packages | LEGACY / MISSING | Both remain compiled/domain implementations, not installed multi-Surface Packages |
| Generic Workspace | LEGACY | Current generic adapter is a TTK compatibility entry, not the target generic Professional Workspace |

### 4.2 Conflicting semantic names

| Current name | Current meaning | Accepted product meaning | Decision |
|---|---|---|---|
| `workspace.navigation` | Company-level dynamic Workspace entry | Domain Navigation inside a Workspace | Keep as Workspace entry; add a distinct Domain Navigation contract |
| `surfaces.json` | Fixed Pane composition: Main/Context/Utility | Registry of Professional Surfaces | Do not extend by ambiguity; define a distinct Professional Surface registry |
| `main/context/utility` keys | Pane responsibilities/components | Professional Surface identity | Preserve as legacy P0 composition only; Surface key is separate |
| `responsibilityRef` field | Domain-object field later written by Core | Surface Responsibility Requirement declaration | Do not reuse; Requirement is a Core-resolved semantic declaration |
| installed Package route | Workspace identity route | Surface route/state | Keep Workspace route canonical; Surface is subordinate route state |

### 4.3 Current conflicts with target ownership

1. Current install creates a new canonical Business while installing a Package. A Package must not
   own Business identity. Materialization must receive an existing canonical Business or participate
   in an externally governed atomic Business + Workspace creation flow.
2. Current Company integration is proof-specific: one hard-coded customer-feedback responsibility
   and capability. It is not a generic responsibility/capability declaration resolver.
3. Current renderer shows Package ID/digest and `Capability requested 0 / granted 0`; this is
   engineering proof UI, not a Professional Workspace product surface.
4. Current validator requires exact P0 fields and rejects all unknown files, so a multi-Surface
   contract needs a new compatible contract version rather than silent field injection.
5. Technical Proposal §8/§11 still contains pre-P1 wording that migration is unsupported. Current
   P1/P1.5 accepted evidence supersedes that implementation statement, but not the proposal's
   multi-Surface direction.

## 5. Ownership contract

### 5.1 Curis Core owns

- canonical Company / Department / Business / Workspace identity and scope;
- Package validation, digest, store, registry, pin, provenance and lifecycle;
- canonical Workspace route and subordinate Surface route resolution;
- finite navigation, view, detail, projection and action registries;
- availability evaluation and fail-closed reason codes;
- current Company OS Team, Responsibility, Assignment, Employee and Capability resolution;
- Work, Execution, Handoff, Cycle, Result, Evidence, Artifact, Decision and Learning truth;
- Shared Employee Work Area and shared projections;
- persistence, permissions, credentials, restart recovery and external-side-effect gates.

### 5.2 Package may declare

- immutable Package identity/publisher/version/Core compatibility;
- Workspace display composition, Domain Navigation and default Surface candidate;
- Professional Surface definitions and stable Package-scoped Surface keys;
- Package Domain Object schemas;
- named Object Views and Detail / Utility mappings from finite Core registries;
- Responsibility Requirement semantics (WHAT), never Employee IDs;
- Capability Requirement references, never grants;
- safe Work / Result / Evidence projection selectors from finite Core registries;
- required/optional/conditional availability declarations;
- allowed Core action IDs and retention/migration metadata.

### 5.3 Workspace Instance owns

- real `workspace_id`, canonical Business relation and Workspace goals/configuration;
- installed Package/version pin and instance provenance;
- enabled optional Surfaces and explicit instance overrides allowed by contract;
- per-user last active Surface and current navigation state;
- materialized scoped Requirement refs and their real Assignment/Employee resolution;
- actual Capability bindings/grants/health;
- private Knowledge references, credentials and connection refs;
- business objects, Work, Result, Evidence, history and user data.

### 5.4 Package may never own

- Team, Employee, Assignment, Work, Execution, Handoff, Cycle, Result, Evidence or Session;
- `employee_id`, credentials, private Knowledge or instance data;
- raw route/URL code, SQL, JavaScript, Python, Shell or arbitrary query expressions;
- capability/permission grants or claims of availability;
- a per-Domain Team, Knowledge, Result or Evidence store.

## 6. Minimal derived contract

The smallest contract needs six distinct declaration groups:

```text
Workspace Package
├── Workspace Entry                 # company-level label/icon; existing concept
├── Domain Navigation               # items → Surface refs
├── Professional Surface Registry   # stable keys and professional composition
├── Object View / Detail Mapping    # view definitions; no new canonical object
├── Responsibility / Capability Requirements
└── Shared Projection Profiles      # scoped Core Work/Result/Evidence consumption
```

It does not need a Surface Runtime, route scripting language, workflow engine, arbitrary layout
builder or Package-defined fallback chain.

## 7. Domain Navigation

Domain Navigation is declared by the Package because it comes from Domain semantics. Core validates
and renders it.

Each item minimally needs:

- stable item key;
- user-facing label;
- target Surface ref;
- stable order and optional group;
- availability ref.

The Package does not declare raw URLs. Core derives a subordinate route from
`workspace_id + surface_key`. Navigation order must not change in response to daily operating state.
Unavailable items remain understandable with a reason; they are not silently reordered or used to
force the user to another page.

## 8. Professional Surface Registry

A Professional Surface is a Package-scoped definition, not a canonical Core entity. It minimally
declares:

- stable key and professional purpose;
- navigation relation;
- default eligibility;
- primary and supported Object View refs;
- relevant Domain Object refs;
- Responsibility Requirement refs;
- Capability Requirement refs;
- Work / Result / Evidence projection profile refs;
- Detail / Utility mappings;
- availability mode and condition refs.

It does not declare Team, Employee, Work lifecycle, Cycle or Runtime.

Surface Registry is necessary. Without a stable Surface key, Domain Navigation, deep links, last
active state, projection scoping, default resolution and version impact cannot refer to the same
professional work area safely.

## 9. Responsibility and capability resolution

The required chain remains:

```text
Package Responsibility Requirement (WHAT)
→ Core materializes/resolves scoped Requirement
→ Organization Routing (WHO)
→ Workspace-scoped Assignment
→ Employee Holder / verified Executor
→ Capability Binding (HOW)
```

Fail-closed behavior:

| Gap | Required Surface | Optional Surface |
|---|---|---|
| Requirement declaration invalid | Package validation fails | Package validation fails |
| No real Responsibility / Assignment | Activation blocked with `RESPONSIBILITY_GAP` | Surface unavailable; no fake holder |
| No Employee | Activation blocked with `UNSTAFFED` | Surface unavailable |
| Capability unavailable/unhealthy | Activation blocked with `CAPABILITY_GAP` | Surface unavailable |
| Condition unresolved | `UNKNOWN` fails closed | Visible unavailable / explicitly disabled |

Install may create a DRAFT and a gap report. It may not call the Workspace Operational until all
required Surface requirements resolve.

## 10. Object and view boundary

| Concept | Owns identity/state? | Correct role |
|---|---:|---|
| Domain Object | Yes | Persisted Package-owned business truth under Workspace scope |
| Object View | No | Core-registered presentation/interaction over one or more objects |
| Professional Surface | No canonical Runtime identity | Stable professional problem space organizing views/actions/projections |
| Detail / Utility mapping | No | Contextual full view/editor/preview/tool for a selected object |
| Artifact | Yes, Core-owned | Produced/referenceable work output |
| Result | Yes, Core-owned | Accepted/recorded outcome truth |
| Evidence | Yes, Core-owned | Provenance and acceptance support |

Therefore XHS Calendar is an Object View inside Content Operating, not a Surface or canonical
entity. A code diff, test report or order detail is also a View/Utility mapping, not automatically a
Surface.

## 11. Shared projections

Package projection rules can only select from Core-owned projection types and bounded selectors:

- implicit current Workspace scope;
- declared Domain Object types;
- Responsibility Requirement refs;
- allowed Core relation types;
- Work/Result/Evidence lifecycle categories.

Core performs Tenant/Company/Workspace/type/lifecycle checks and returns reference-first shared
truth. Package selectors cannot contain SQL, arbitrary expressions or foreign IDs. Team, Knowledge,
Artifact, Result, Evidence and Employee Workstation remain Company OS projections.

## 12. Availability, default and fallback

### Availability modes

- `REQUIRED`: must resolve before the Workspace becomes Operational.
- `OPTIONAL`: explicitly enabled/disabled at Instance level; disabled does not invalidate other
  Surfaces.
- `CONDITIONAL`: evaluated only from named Core condition types. Capability-dependent is a
  condition. `UNKNOWN` fails closed.

Stage-dependent availability may mark a stable item unavailable, but must not produce a menu that
reorders or disappears every day. Changing availability does not change Work, Holder or Cycle.

### Default resolution

Core resolves in this order:

1. an explicit valid deep-link Surface;
2. the user's last active eligible Surface;
3. the Package-defined default candidate when eligible;
4. the first eligible required Surface in stable Domain Navigation order;
5. a Core-owned Workspace Gap surface showing why nothing is eligible.

The Package declares one default candidate, not a fallback graph. Runtime state never forcibly
navigates the user away from the current Surface.

## 13. Routing and identity

Canonical identity remains:

```text
workspace_id
```

Surface state is subordinate:

```text
workspace_id + package_version + surface_key [+ view_key / object_id]
```

Surface route must not become a Workspace, Business, Team or Runtime identity. Renaming a label does
not change the Surface key. Removing/renaming a key is a versioned compatibility change, not a URL
rewrite hidden from lifecycle review.

## 14. Versioning and running Work

Domain Navigation, Surface Registry, requirements, Object View mappings and projection profiles are
digest-covered Package version truth.

Required rules:

- Instance remains pinned to one immutable Package version during preview.
- Active Work/Cycle retains its Operating Definition and Package/Surface origin refs.
- Package activation cannot silently rewrite Holder, Assignment, capability grant, Work, Cycle,
  Result or Evidence.
- Additive Surface changes still require impact preview and required-gap checks.
- Changed/removed Surface keys are incompatible until explicit impact handling exists.
- Historical Work remains readable through its pinned version or a Core-owned unavailable/history
  presentation; removing a Surface never deletes its data.
- Schema/data changes continue through accepted transactional migration boundaries; file rollback is
  not data rollback.

Current P1/P1.5 provides Package pin and bounded migration substrate, but has no Surface-aware impact
classification or running-Work pin proof.

## 15. Domain proofs

### 15.1 XHS primary example

Scope remains the accepted candidate:

```text
Department: 内容增长部
Business:   小红书运营
Workspace:  AI 科技
```

The contract can express candidate Surface refs for Operating Overview, Research Insights, Content
Operating, Growth Analytics, User Feedback and optional Commercialization. It does not freeze their
labels/order. Publishing Calendar is an Object View referenced by Content Operating. All Surfaces
share one Workspace Operating Team boundary and consume real Company OS assignments.

Result: CONTRACT FITS. Current Runtime/UI migration remains missing.

### 15.2 RD cross-check

The same contract can express candidate professional areas such as Development, Build/Test, Release
and Architecture, while mapping Code, Diff, Terminal, Test, Artifact and Review to registered views,
details and tools. RD's final menu remains unfrozen.

Result: CONTRACT FITS. Specialized Core view components/capabilities may be gaps; RD is not migrated.

### 15.3 E-commerce stress test

Product, Inventory, Order, Channel, Marketing, Customer Service, Content Production and Finance can
be declared as multiple Surfaces only when they remain one Workspace-level professional environment
under one accountable Operating Team responsibility boundary. Each Surface declares different WHAT
requirements; Organization Routing may resolve shared or different Employees without duplicating
identity.

If Domain research finds multiple independent goals, accountable Team boundaries or operating
units, the correct answer is multiple sibling Workspaces under a Business—not Sub-Workspace or
Surface Runtime.

Result: CONTRACT FITS WITHOUT Sub-Workspace / Surface Runtime / Domain Runtime.

### 15.4 Unknown Domain path

```text
Business Intent
→ Current Company Truth
→ Domain Research
→ Operating Model
→ Semantic Model
→ Professional Surface Model
→ Responsibility Model
→ Capability Map
→ Operating Team Design
→ Package Candidate
→ Core Expressibility Check
```

The user does not configure menus, draw Surfaces or bind Agents. Missing capability becomes an
explicit gap and return path.

## 16. Minimal implementation gap

The next bounded implementation needs only:

1. a new versioned Package contract validator, leaving P0 v1 readable;
2. distinct Domain Navigation and Professional Surface Registry declarations;
3. a compiled Package model returned by the existing Package API;
4. Core-derived Surface route/default/last-active/fallback resolution;
5. generic Requirement/Assignment/Capability resolution with fail-closed gap states;
6. finite Object View/Detail and shared Work/Result/Evidence projection registries;
7. one generic multi-Surface renderer proof;
8. version-impact and restart evidence preserving Workspace and running operating truth.

It does not need Marketplace, arbitrary extension, Workflow Engine, Sub-Workspace, Surface Runtime,
RD/XHS migration, general low-code layout or a new Company OS primitive.

## 17. CEO questions

1. **Can the current Package express multi-Surface?** No. It expresses one Workspace entry and fixed
   Main/Context/Utility object components.
2. **What is the smallest gap?** A versioned Domain Navigation + Professional Surface Registry
   contract with requirement/projection refs and Core resolution.
3. **Is Surface Registry necessary?** Yes, as Package metadata; not as a new Runtime entity.
4. **Who declares Domain Navigation?** Package/Domain design declares it; Core validates, resolves and
   renders it.
5. **How are Responsibility Requirements expressed?** Stable semantic requirement refs resolved by
   Core through Router → scoped Assignment → Employee.
6. **Does Package know Employee?** No. It must never contain `employee_id`.
7. **Object View vs Surface?** View presents objects; Surface organizes a stable professional problem
   area and references views.
8. **How are Team/Knowledge reused?** Core-owned Workspace-scoped projections; Package declares only
   bounded consumption.
9. **How are optional Surfaces handled?** Instance enablement plus fail-closed availability; stable
   navigation, no daily menu mutation.
10. **Does a Surface route affect Workspace identity?** No; it is subordinate state under the same
    `workspace_id`.
11. **How does Package version affect running Work?** It must not silently affect it; Work/Cycle stays
    pinned to immutable operating/package origin truth until an explicit safe transition.
12. **Does XHS fit?** Yes; Calendar is an Object View under Content Operating. Runtime migration is
    still missing.
13. **Does RD fit?** Yes; final menu remains unfrozen and specialized view capability gaps remain.
14. **Does e-commerce fit?** Yes under one accountable Workspace boundary; otherwise use sibling
    Workspaces, never Sub-Workspace/Surface Runtime.
15. **What must implementation really change?** Validator/compiled contract, Domain Navigation,
    Surface Registry, Core resolution, finite views/projections, route/default state and one real
    multi-Surface proof—nothing broader.

## 18. Research decision

```text
CURRENT PACKAGE MULTI-SURFACE SUPPORT = NO
CURRENT PACKAGE SUBSTRATE = REUSABLE
MINIMAL CONTRACT GAP = IDENTIFIED
SURFACE REGISTRY = REQUIRED AS PACKAGE METADATA, NOT RUNTIME
SUB-WORKSPACE / SURFACE RUNTIME / DOMAIN RUNTIME = NOT REQUIRED
IMPLEMENTATION = NOT AUTHORIZED
CEO REVIEW REQUIRED
```
