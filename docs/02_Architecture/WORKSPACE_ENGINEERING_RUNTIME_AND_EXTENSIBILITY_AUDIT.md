# Curis Workspace Engineering Runtime & Extensibility Audit

**Status:** Review  
**Date:** 2026-08-16  
**Scope:** Read-only implementation audit  
**Evidence baseline:** current filesystem snapshot at `adb52210aaa4b230560412e6b224b37622dad495`, including the present dirty/untracked implementation state  
**Authority:** `CURRENT_STATE.md`, Frozen Architecture / Workspace Shell / Shared Patterns, ADR-0046, accepted XHS and Computer Access records, current RD Issue/Review

## 1. Executive verdict

**Current Curis Desktop cannot install, register, render, run, update, or uninstall a previously unknown Workspace without changing Curis Core and rebuilding the Desktop app.**

Today Curis can:

- create persisted instances of the three compiled business types `RD / XHS / TTK`;
- save and revise their existing Blueprint JSON;
- reuse Company OS Runtime objects such as Employee, Responsibility, Handoff, Decision Packet, Evidence, Result and Capability Binding;
- invoke a detected Codex CLI through the current Agent Adapter and preserve truthful Computer Access evidence;
- persist known Workspace instances and known Runtime entities across restart.

Today Curis cannot:

- discover a Workspace package from disk;
- validate or sign such a package;
- register a new Workspace type or navigation entry at runtime;
- render new Main / Context / Utility surfaces from package data;
- add a new business-object schema or action without backend code;
- install, update, migrate, roll back, disable or uninstall a Workspace package;
- export an installed Workspace as a safe shareable template.

Therefore the current “Workspace Engineering” chain is still a **development-time product direction**, not a delivered product Runtime capability.

The critical distinction is:

```text
Codex can modify Curis source files in an authorised working directory
≠
an installed Curis can dynamically assemble a new Workspace
```

## 2. Audit method and truth boundary

This audit inspected current source, Runtime schemas, current accepted Review records and official platform documentation. It did not execute a package installation, write SQLite, modify Runtime, create an Issue, or claim Browser/Desktop acceptance.

Because the working tree contains substantial pre-existing modified and untracked work, findings describe the **current filesystem snapshot**, not a clean `main` release. Accepted Issue/Review evidence is called out separately from unaccepted source presence.

Status meanings used below:

| Mark | Meaning |
| --- | --- |
| `IMPLEMENTED` | A current code path and accepted evidence support the stated capability. |
| `PARTIAL` | Useful pieces exist, but the requested end-to-end capability does not. |
| `MANUAL` | A person must translate, copy, decide or register the result outside the product Runtime. |
| `EXTERNAL` | The capability belongs to an external tool/process and is not owned by Curis Runtime. |
| `MISSING` | No current Core capability was found. |
| `BLOCKED` | Current validation or hardcoded architecture rejects the requested path. |

## 3. AS-IS architecture

### 3.1 Desktop delivery shape

The current app is **Tauri 2 + standalone Next.js + packaged Python services**, not Electron:

```text
Curis.app
├── Tauri shell
├── bundled standalone Next.js server :3010
├── bundled Trusted Gateway :8080
├── bundled Python Workspace Runtime :8002
└── application-data SQLite
```

`desktop/tauri.conf.json`, `desktop/src/lib.rs` and `desktop/scripts/build-runtime.sh` define fixed bundled resources and three fixed sidecars. The frontend routes and Python backend are packaged at build time. Adding React routes, backend modules, Python dependencies or native sidecars requires a fresh Desktop build.

Tauri capabilities can constrain which WebViews may invoke native commands, but they are app configuration rather than a dynamic Workspace package sandbox. Tauri sidecars and plugins are likewise registered through build configuration and Rust integration, not installed as arbitrary end-user Workspace packages. See [Tauri capabilities](https://v2.tauri.app/security/capabilities/), [sidecars](https://v2.tauri.app/develop/sidecar/) and [plugin development](https://v2.tauri.app/zh-cn/develop/plugins/).

### 3.2 Workspace frontend

Current Workspace product routes are physical Next.js routes:

- `/ceo-office/workspace/software`
- `/ceo-office/workspace/xhs`
- `/ceo-office/workspace/shortvideo`
- `/ceo-office/workspace/studio`

`frontend/lib/runtimeApi.js::workspaceOfficeHref()` hardcodes `RD → software`, `XHS → xhs`, and `TTK → shortvideo`.

Current business UI is compiled React:

- RD imports its RD professional component;
- XHS imports its accepted XHS instance component;
- TTK uses the existing generic Runtime view;
- Studio contains a static `TEMPLATES` map for RD/XHS/TTK.

`WorkspacePaneShell` is reusable for pane behaviour, search placement, resize, collapse and Utility maximize. It receives precompiled React nodes; it is **not** a manifest-driven Surface renderer.

### 3.3 Workspace backend

`backend/app/runtime/workspace.py` currently fixes:

- `BUSINESS_TYPES = {RD, XHS, TTK}`;
- RD and content stage lists;
- XHS ContentItem lifecycle;
- per-business Blueprint validation;
- per-business domain commands and projections.

Unknown business types are rejected. Adding “客户反馈办公室” currently requires backend changes for its type, object schema, actions, API projection and frontend route.

The shared Runtime Foundation is valuable but bounded. `runtime_entities` and `runtime_links` provide scoped persistence, yet `RuntimeFoundation.create()` accepts only the registered entity types and state machines. A new domain object currently needs Core registration or must be forced into an existing type, which would be semantically wrong.

### 3.4 Existing reusable Runtime

The following are real reusable foundations:

| Existing primitive | Current evidence | Reuse for Workspace packages |
| --- | --- | --- |
| Workspace row + immutable Blueprint versions | `workspaces`, `runtime_workspace_versions`, `revise_blueprint()` | Yes; extend to package/version provenance. |
| Tenant / Company / Workspace scope | Runtime queries and links fail closed by scope | Yes; mandatory for every package and instance. |
| Employee / Role Slot / Capability Binding | Current Runtime Foundation and Studio staffing chain | Yes; templates may propose them, never fabricate active employees. |
| Responsibility / Handoff | Accepted XHS shared chain and RD responsibility projection | Yes; packages reference shared commands and projections. |
| Decision Packet P7 | Accepted XHS implementation | Yes; packages must not define a private approval system. |
| Artifact / Evidence / Result Reference | Accepted XHS/RD evidence paths | Yes; package actions can produce references through existing Runtime. |
| Agent Adapter / Execution Binding | Real RD Codex execution | Yes; package requests use existing binding and truth boundaries. |
| Capability Catalog / Registry | Model, Agent, Skill, Tool, Connector and local capability facts | Yes; package requirements resolve against it. |
| Simulation records | Existing Runtime simulation model | Partial; can validate supported package contracts after a package substrate exists. |
| Computer Access snapshot | Accepted P0 requested/configured/effective separation | Yes; package install cannot bypass it. |

### 3.5 Existing “package” names are not Workspace packages

Several current models use the word package, but none provides Workspace installation:

| Existing term | Actual purpose | Why it is not a Workspace Package |
| --- | --- | --- |
| Company Package | Catalog aggregation / company instantiation assets | Does not install navigation, professional Surfaces or arbitrary domain schemas. |
| Capability Package | Commercial grouping of capabilities/connectors | Does not define a Workspace application. |
| Context Package | Immutable bounded context for one Task execution | Execution input only. |
| Content Publish Package | Structured content output for publishing | Business result payload only. |
| Skill template install | Installs a Skill template into Company resources | Does not register Workspace type or UI. |

The future Workspace Package must be a separate technical contract with an unambiguous name and provenance. Reusing one of these tables would collapse unrelated lifecycles.

## 4. End-to-end Workspace Engineering chain

| Step | Current mechanism | Status | Truthful conclusion |
| --- | --- | --- | --- |
| CEO states an operating goal | Studio accepts a goal for a known template | `PARTIAL` | Input exists, but only inside compiled RD/XHS/TTK assembly. |
| Call experts to research | Agent/Codex can execute bounded tasks when configured | `PARTIAL / EXTERNAL` | Curis can call an execution provider; it has no Workspace Engineering research lifecycle. |
| Form an operating method | Documents, conversations and human synthesis | `MANUAL` | No persisted method-to-package compiler or validated operating-rule artifact. |
| Product / Workspace design | Frozen specs and design work are prepared outside Runtime | `MANUAL / EXTERNAL` | WorkBuddy/Codex/design sessions transfer facts manually. |
| Generate Workspace definition | Studio saves known Blueprint JSON | `PARTIAL` | It cannot describe arbitrary Surfaces, schemas and actions. |
| Generate a Workspace package | None | `MISSING` | No manifest, assets, schema, signature or package archive contract. |
| Discover package | None | `MISSING` | No package directory watcher, registry scan or import API. |
| Validate compatibility/security | Known Blueprint validation only | `PARTIAL` | No package schema, Core-version compatibility, digest or signature validation. |
| Install | None | `MISSING` | No package store or atomic installation transaction. |
| Register navigation | Hardcoded route mapping | `BLOCKED` | New Workspace requires React source and route changes. |
| Render Main/Context/Utility | Precompiled business components | `BLOCKED` | Shell is reusable, but no declarative Surface renderer exists. |
| Register business objects/actions | Fixed entity and business-type registries | `BLOCKED` | Unknown objects/actions require backend code. |
| Bind Employee/Capability/Agent | Shared Runtime exists | `PARTIAL` | Can bind known Runtime objects after Core understands the Workspace. |
| Persist instance | Current Workspace/Runtime SQLite | `IMPLEMENTED` for known types | No package provenance or generic package-owned object storage. |
| Run | Known domain APIs and real Agent Adapter paths | `PARTIAL` | Execution works for implemented domains; a package cannot introduce a new run contract. |
| Update / migrate | Blueprint revision exists | `PARTIAL` | No installed package update, migration dry-run, instance compatibility or package rollback. |
| Uninstall | None | `MISSING` | No disable/unregister/data-retention contract. |
| Export / sign / publish | None | `MISSING` | Marketplace chain is not yet available. |

## 5. What a new Workspace requires today

| Required change for an unknown business | Today | Why |
| --- | --- | --- |
| Modify React/frontend source | **Yes** | New professional Surface is a compiled component. |
| Add a route or hardcoded route mapping | **Yes** | Workspace office destination is a fixed map. |
| Modify backend | **Yes** | Business type, object/actions and projection are fixed. |
| Add Runtime object/state handling | **Usually yes** | Entity types and state machines are registered in Core. |
| Register navigation manually | **Yes** | No installed-package navigation registry. |
| Rebuild Desktop | **Yes** | Next/Python resources are bundled into Curis.app. |
| Transfer research/design/Issue manually | **Yes** | No in-product Workspace Engineering artifact chain. |

For a new Workspace that uses only an already compiled business type and Surface, Studio can create another instance without a rebuild. That is instance creation, not extensibility.

## 6. Gap matrix

### 6.1 Core / Desktop

| Capability | Status | Gap |
| --- | --- | --- |
| Local Desktop + app-data SQLite | `IMPLEMENTED` | Stable base for a package store. |
| Bundled frontend/backend/gateway | `IMPLEMENTED` | Static build, no dynamic package host. |
| Package discovery/store | `MISSING` | No app-data package directory or registry. |
| Signature/trust verification | `MISSING` | Desktop app update signing does not verify Workspace packages. |
| Compatibility resolver | `MISSING` | No `minCoreVersion`, schema version or extension ABI. |
| Atomic install/disable/uninstall | `MISSING` | No transaction or recovery semantics. |

### 6.2 Shell / UI

| Capability | Status | Gap |
| --- | --- | --- |
| Shared Workspace pane shell | `IMPLEMENTED` | Reusable only from compiled React. |
| Resizable / Utility maximize / pane-local headers | `IMPLEMENTED` | Suitable built-in renderer primitives. |
| Dynamic Workspace navigation | `MISSING` | Routes are hardcoded. |
| Declarative Main/Context/Utility renderer | `MISSING` | No component registry or schema. |
| Dynamic object search | `PARTIAL` | Shared search placement exists; generic package object indexing does not. |
| Extension UI sandbox | `MISSING` | No isolated host or safe bridge. |

### 6.3 Runtime / domain

| Capability | Status | Gap |
| --- | --- | --- |
| Scoped generic entity/link persistence | `IMPLEMENTED` | Current create path still uses a fixed type/state registry. |
| Workspace Blueprint versions | `IMPLEMENTED` | No package identity/version pin. |
| Generic package-owned domain object | `MISSING` | Needed to avoid a Core table/state machine per template. |
| Generic allowed action dispatch | `MISSING` | Package cannot bind UI action to a safe Core command. |
| Shared Employee/Responsibility/Handoff/Decision/Evidence | `IMPLEMENTED / PARTIAL` | Reusable, provided packages reference rather than replace them. |
| Package migration/rollback | `MISSING` | Staffing rollback is not package/data migration rollback. |

### 6.4 Capability / execution / security

| Capability | Status | Gap |
| --- | --- | --- |
| Capability Catalog and scoped bindings | `IMPLEMENTED` | No package requirement resolver with package install status. |
| Real Codex adapter and evidence | `IMPLEMENTED` in accepted RD slice | External Codex availability is still a runtime dependency. |
| Requested/configured/effective access truth | `IMPLEMENTED` for current Codex P0 | Package permissions cannot be mapped to automatic grants. |
| Full Computer Access | `BLOCKED / UNSUPPORTED` | Must remain fail-closed under ADR-0046. |
| Restricted extension execution | `MISSING` | No WASM/process host, ABI, resource limits or capability tokens. |

## 7. Current reusable Core versus required Core work

### Reuse without replacement

- Workspace identity, Company/Tenant scope and SQLite persistence.
- Workspace Blueprint/version records, after adding package provenance.
- Shared Shell and approved Surface behaviours.
- Employee, Responsibility, Handoff, P7 Decision, Evidence, Result Reference and System Activity semantics.
- Capability Catalog, Connection/Health/Binding truth and Agent Adapter.
- ADR-0046 Computer Access boundary.
- Runtime transition log, scoped links and audit evidence.

### Core additions required

1. Workspace Package schema, validator, trust/signature verifier and compatibility resolver.
2. Package store plus install/disable/uninstall registry in application data.
3. Dynamic navigation generated from installed package registrations.
4. Declarative Workspace Surface renderer backed by a finite built-in component registry.
5. A minimal generic package-domain-object record and schema validation path.
6. A finite safe action registry that maps package actions to existing Core Runtime commands.
7. Template-to-instance materialisation with package version pinning and data separation.
8. Package update/migration/rollback lifecycle and audit trail.

These are Core changes made once. After they exist, compatible declarative Workspace packages should not require another Core rebuild.

## 8. Direct answers

1. **What can Curis do now?** Create and operate known RD/XHS/TTK instances, reuse shared Runtime facts, and invoke real bounded Agent execution. It cannot install an unknown Workspace type.
2. **What still depends on WorkBuddy/Codex/humans?** Research synthesis, operating-method formation, product/design translation, source implementation, route/object registration, review handoff and rebuilding the app.
3. **Is no-source dynamic Workspace creation technically feasible?** Yes, after a bounded Core package substrate and declarative renderer are implemented. It is not feasible in the current installed app.
4. **Which current Core capabilities are reusable?** Scope/persistence, Workspace versions, Shared Shell, Employee/Responsibility/Handoff/Decision/Evidence/Result, Capability Registry and Agent Adapter.
5. **What must be added or refactored?** Package lifecycle, renderer, navigation registry, generic domain-object/action contracts, compatibility/signing, and migration/rollback.
6. **How far is Workspace Engineering from a true Runtime capability?** The product model and shared Runtime foundation are substantial; the dynamic package substrate is absent. A focused P0 PoC is required before the phrase can describe a delivered capability.
7. **Does a Template Marketplace work on the current architecture?** Not today. It becomes technically credible only after package trust, compatibility, safe rendering, capability checks, migration and revocation exist.

## 9. Audit conclusion

The current architecture does not invalidate Workspace Engineering, but it changes the honest status:

```text
Current: Curis developers build Workspace implementations into Curis Core.
Target:  Curis Runtime installs and operates versioned Workspace Packages.
```

Until the proposed P0 PoC passes in an already installed Desktop without source modification or rebuild, “dynamic Workspace Engineering” must remain `NOT IMPLEMENTED`.
