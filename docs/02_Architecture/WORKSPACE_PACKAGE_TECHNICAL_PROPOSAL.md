# Curis Workspace Package Technical Proposal

**Status:** Review
**Technical Direction State:** `WORKSPACE ENGINEERING TECHNICAL DIRECTION APPROVED CANDIDATE`
**Date:** 2026-08-22
**Scope:** Target technical model and non-implementation PoC plan
**Depends on:** `WORKSPACE_ENGINEERING_RUNTIME_AND_EXTENSIBILITY_AUDIT.md`, Frozen Architecture / Shared Workspace Patterns, ADR-0046

## 1. Recommendation

Adopt:

```text
Curis Core
+
Declarative Workspace Package
+
Restricted Extension only when a declarative package is insufficient
```

Use a **declarative-only P0**. Do not load arbitrary JavaScript, arbitrary Python or arbitrary native code into the Curis process. Add restricted extensions later, only for demonstrated professional needs.

This is the smallest architecture that can prove the product claim while preserving the accepted Company OS Runtime:

```text
Workspace Package describes business composition
Curis Core owns identity, safety, rendering and Runtime truth
External Agent/Tool/Connector performs authorised work through existing adapters
```

The package must not create a parallel Employee, Task, Gate, Decision, Result or Workflow system.

### 1.0 Accepted product semantics / implementation boundary

产品层正式将 Workspace Package 理解为 **Domain Operating Capability Package**：专业工作面、Domain 语义、能力、方法引用、Result / Evaluation 与安全边界的声明式组合载体。它仍遵守 Package First，不新增 Playbook、Method Runtime 或行业 Workflow Engine。`Applicability / Objective / Recommended capabilities / Recommended activities / Required outputs / Evaluation guidance / Risk / Required gates / transition conditions` 的结构化方法元数据尚未形成已接受的统一 persisted implementation，登记为 Future Capability Architecture / Product → Implementation Gap；本段不授权 Schema、Runtime 或代码修改。

### 1.1 Methodology × Technical closure

```text
CURRENT DELIVERY PATH（current fact）
Workspace / Instance Design
→ Gap Audit
→ bounded Issue
→ modify Curis source
→ rebuild / accept

TARGET WORKSPACE STUDIO PRODUCT PATH（未完成）
Workspace Design
→ Package Composition
→ Core Expressibility Check
  ├─ EXPRESSIBLE → Validate → Install → Materialize → Run
  └─ CORE / CAPABILITY GAP → bounded Issue → extend Core → return to Package
```

The target path is **Package First**. Source modification is not its default delivery mechanism. Existing P0 / P0.5 evidence proves only a controlled declarative Package substrate; it does not prove that an unknown multi-Surface Workspace with Domain Navigation, responsibility declarations and generic projections can be installed and operated without further authorised work.

### 1.2 Lifecycle routing

- A new business Workspace resolves in this order: Current Company Truth → Domain / Scope / Risk recognition → Verified Match → Instance Configuration → Maintained Derived → Safe Composition; only a material Truth / Domain / Risk gap inserts bounded Research and the downstream Operating Model → Handoff → Translation → Semantic Model → Workspace Design → Package path. Generation is last resort.
- A verified Template instance reuses versioned research / Handoff / Translation evidence and only repeats Business Intent, Template Match, goal adaptation, capability check, materialisation and acceptance / activation.
- An existing Workspace evolution re-enters at the earliest affected stage and repeats every affected Gate.

Relevant Gates cannot be skipped; the complete Lifecycle is not mechanically rerun when valid versioned evidence remains applicable.

### 1.3 Professional Workspace authority candidate（CEO Accepted 2026-08-21）

Workspace Package 的产品责任是声明一个业务的完整专业环境，而不是声明一张页面。它需要支持 Domain Navigation、Professional Surface Registry、Surface responsibility requirements、Object View / Detail mapping、Work / Result / Evidence projection、optional / conditional availability 与 Capability requirements。该方向已被接受，但本轮不定义或冻结最终 Schema。

Package 不拥有 Team、Employee、Work、Cycle、Result 或新的 Runtime。Surface 只声明 WHAT；`Responsibility Requirement → Organization Routing → Assignment → Employee` 解析 WHO。禁止 Surface 或 Package 直接绑定 Employee ID，禁止新增 Surface Runtime / Agent / Cycle / Result / Session。

## 2. Target boundary

### Curis Core owns

- package discovery, validation, trust and compatibility;
- install, disable, update, rollback and uninstall;
- Tenant / Company / Workspace isolation;
- navigation registration and Shared Shell;
- a finite built-in Surface component registry;
- shared Employee, Responsibility, Handoff, Decision P7, Evidence, Result and System Activity;
- Capability/Connection/Health/Binding checks;
- Agent execution and ADR-0046 Computer Access truth;
- instance persistence, audit and migration transactions;
- secrets, credentials and external side-effect approval.

### Workspace Package may declare

- package identity, publisher, version and Core compatibility;
- Workspace composition and local navigation;
- Domain Navigation and Professional Surface registry;
- Surface responsibility requirements;
- Object View and Detail mapping;
- Work / Result / Evidence projection;
- optional / conditional Surface availability;
- Main / Context / Utility responsibility composition;
- package-domain object schemas;
- actions chosen from Core's allowed action registry;
- Employee/Responsibility templates;
- Strategy and Operating Rule defaults;
- Capability, Knowledge and Permission requirements;
- Result/Evidence presentation schemas;
- migration metadata and package assets.

### Workspace Package may not contain

- credentials, API keys, tokens or Keychain material;
- personal Knowledge contents or private source documents;
- conversations, memories or history;
- Company/Workspace instance data;
- pre-authorised Employee, Connector or Computer Access grants;
- arbitrary shell commands, arbitrary SQL or unrestricted code;
- claims that a required capability is available.
- direct Employee IDs or Surface-owned Team assignments;
- Surface Runtime, Surface Agent, Surface Cycle, Surface Result or Surface Session.

## 3. Semantic model and proposed package shape

### 3.1 Semantic Model Before Instance

Before any instance is materialised, a package must state its local business semantics:

- business objects;
- relationships;
- lifecycle states;
- responsibility references;
- critical business truths and unknown states.

The default boundary is a **Package Domain Schema**. A custom Workspace does not need a global Frozen Domain Authority. Promotion to Domain Authority / Frozen is required only when the semantics are reused across multiple instances, become an official Domain standard, affect Company OS, or need a long-term compatibility guarantee.

### 3.2 Target package shape

The long-term format may grow to the following shape, but P0 uses only the files listed in §3.3:

```text
customer-feedback-office.curis-workspace/
├── manifest.json
├── surfaces.json
├── objects/
│   └── customer-feedback.schema.json
├── templates/
│   ├── employees.json
│   ├── responsibilities.json
│   └── operating-rules.json
├── migrations/
│   └── manifest.json
├── assets/
└── signature.json
```

Conceptual manifest fields:

```json
{
  "schemaVersion": 1,
  "packageId": "com.curis.sample.customer-feedback-office",
  "version": "0.1.0",
  "publisher": "curis.sample",
  "coreCompatibility": { "minimum": "0.1.0" },
  "workspaceType": "customer_feedback",
  "navigation": { "label": "客户反馈办公室", "icon": "feedback" },
  "surfaces": "surfaces.json",
  "objects": ["objects/customer-feedback.schema.json"],
  "actions": ["core.domain-object.create", "core.domain-object.update"],
  "capabilityRequirements": [],
  "permissionRequirements": [],
  "migrationManifest": "migrations/manifest.json"
}
```

This is a proposal, not a current schema. P0 should omit every field not required by the PoC.

### 3.3 P0 package shape

```text
customer-feedback-office.curis-workspace/
├── manifest.json
├── surfaces.json
└── objects/
    └── customer-feedback.schema.json
```

P0 has no arbitrary code, migration script, employee template, private data, asset pipeline or general signing PKI. The manifest contains only identity/version/Core compatibility, navigation, Surface/schema references and allowed Core action IDs. Package digest and install provenance are recorded by Core; unsupported upgrades are rejected rather than migrated.

## 4. Declarative rendering model

### 4.1 Professional Surfaces

A package declares a professional environment, not HTML or React source. The following is a conceptual responsibility map, not the final Schema:

```text
Workspace
├── Domain Navigation
├── Professional Surface Registry
│   ├── Overview candidate
│   └── Domain Professional Surface(s)
├── Surface Responsibility Requirements
├── Object View / Detail Mapping
├── Work / Result / Evidence Projection
├── Optional / Conditional Availability
├── Capability Requirements
└── Main / Context / Utility responsibility mapping
```

Each Surface selects from a finite Core registry, for example:

- object list;
- object detail;
- field editor;
- status/owner summary;
- Employee Presence;
- Result Reference list;
- Evidence list;
- activity timeline;
- empty/failure/capability-gap card.

The Core renderer owns tokens, accessibility, pane behaviour, loading/failure states and data scoping. A package supplies labels, field binding and layout slots within approved limits.

### 4.2 Domain objects

Do not add a Python class and SQL table for every future Workspace. P0 should extend the
existing `runtime_entities` / `runtime_links` foundation with one generic package-domain
object type and package-schema metadata. A separate table is justified only if later
measurement or migration constraints prove the existing store insufficient.

Conceptually the projection is:

```text
WorkspaceDomainObject
├── object_id
├── package_id / package_version
├── workspace_id / company_id / tenant_id
├── object_type
├── schema_version
├── lifecycle_status
├── owner_ref
├── data_json
└── created_at / updated_at
```

The package schema validates `data_json`; a generic Core transition command validates the
package-declared domain-state enum. Shared facts such as Employee, Responsibility, Handoff,
Decision, Evidence and Result remain separate existing Core entities and link to the domain
object. This avoids two failures:

- hardcoding XHS/RD states into global Core;
- creating a private Runtime inside every package.

If a later domain needs transactional invariants that JSON validation cannot express, that is evidence for a bounded Core primitive or restricted extension—not permission to add a Workflow Engine.

### 4.3 Actions

Package actions reference approved Core command IDs. They never contain code or raw endpoints.

Example:

```text
“记录反馈”
→ core.domain-object.create
→ validate package schema
→ enforce Tenant/Company/Workspace scope
→ append audit activity
→ return real object ID and status
```

An unknown action ID is `UNSUPPORTED`. A known action with missing capability is blocked with a capability requirement; it is not silently downgraded.

## 5. Architecture option comparison

| Option | Safety | UI freedom | Performance | AI generation | Compatibility | Recommendation |
| --- | --- | --- | --- | --- | --- | --- |
| Declarative only | High; Core owns all execution | Medium | High | High; schema-constrained | High | **P0** |
| Declarative + restricted extension | Medium-high with narrow ABI/sandbox | High | Medium-high | Medium | Medium | **Long-term target** |
| Signed JS in main WebView | Low; signature identifies publisher but does not restrict behaviour | Very high | High | High | Low | Reject |
| Separate iframe/WebView | Medium if isolated origin and strict bridge | High | Medium | Medium | Medium-low | Exceptional UI only, not P0 |
| Out-of-process plugin | Medium-high with narrow RPC and OS limits | High for native logic | Medium | Low-medium | Medium | P1 specialist integration |
| WASM component | High for pure computation with explicit imports | Low for native UI | Medium-high | Medium | Medium-high with stable WIT | P1 optional pure logic |
| Local service / MCP | Depends on service trust and permission bridge | Not a UI model | Medium | Medium | Medium | Reuse for Tool/Connector capability, not package rendering |
| Tauri plugin | Strong native integration | High | High | Low | Build-coupled | Core feature only, not Marketplace package |

### 5.1 Why not signed JavaScript

A signature answers “who produced these bytes?” It does not answer “what may this code access?” Loading package JavaScript into the main Next.js/WebView context would expose application state and any IPC available to that WebView. Current Tauri capabilities are designed around configured windows/WebViews and command permissions, not as a per-package JavaScript sandbox. See [Tauri capabilities](https://v2.tauri.app/security/capabilities/).

### 5.2 Why iframe/WebView is not P0

An isolated origin with a narrow `postMessage` bridge can contain custom UI, but it introduces focus, accessibility, theming, data-bridge and lifecycle complexity. MDN also warns that combining script and same-origin privileges can defeat sandbox isolation. See [MDN iframe sandbox](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements/iframe).

### 5.3 Why WASM is useful but later

The WebAssembly Component Model can express explicit imports/exports: an extension cannot access a resource that the host does not import. That makes it a good candidate for pure validation, transformation or calculation. It is not a complete professional UI, Connector or OS integration solution. See [WebAssembly Component Model worlds](https://component-model.bytecodealliance.org/design/worlds.html).

### 5.4 Why local service/MCP stays a capability

MCP or a local service is suitable for browser automation, a proprietary API, specialist computation or platform access. It belongs behind Tool/Connector/Agent capability contracts. It should not decide Curis navigation, directly mutate SQLite or render the Workspace shell.

## 6. Security and capability contract

### 6.1 Package trust

The target trust model requires:

- immutable digest;
- package signature;
- publisher identity and key ID;
- trust state: `OFFICIAL / VERIFIED / UNTRUSTED / REVOKED`;
- Core/schema compatibility;
- safe extraction checks: no path traversal, symlinks outside store, resource bombs or undeclared files;
- audit record for install, update, disable, rollback and uninstall.

Desktop app update signing is a useful precedent but is not the same trust domain. Tauri's updater verifies signed app updates and itself requires Core integration; Workspace packages need their own package registry and signature policy. See [Tauri updater](https://v2.tauri.app/zh-cn/plugin/updater/).

**P0 boundary:** do not build a general PKI, publisher marketplace or key-rotation platform. P0 records an immutable digest, import source, package/version provenance and a local trust classification for the controlled sample package; it validates safe extraction and declared files. General third-party signature verification is deferred and cannot be claimed from the P0 result.

### 6.2 Manifest permissions are requests, not grants

For every requirement, Core resolves one of:

```text
AVAILABLE
MISSING
NEEDS_AUTH
UNSUPPORTED
UNKNOWN
```

Resolution uses existing Capability Catalog, connection/health/binding facts and Employee/Workspace scope.

```text
Package requires capability
≠ capability is connected
≠ capability is authorised
≠ capability is bound
≠ capability is effective
```

### 6.3 Computer Access

ADR-0046 remains authoritative:

```text
requested ≠ configured ≠ effective
```

- Installing a package never grants filesystem, network, shell, secrets or Full Computer Access.
- Employee execution submits a requested intent through the existing Agent Adapter.
- The provider mapping and effective evidence remain session-specific.
- Unsupported Full access stays `UNSUPPORTED`; no package may request a dangerous fallback.
- Resume must re-inspect/re-verify rather than inherit effective access.

### 6.4 Secrets and external side effects

- Secrets remain in the existing Secret Broker/Keychain and are referenced by opaque IDs.
- Packages never receive plaintext credentials.
- Connector calls go through existing capability adapters.
- External publishing, payment, destructive filesystem action and other high-risk effects retain CEO confirmation and audit.

## 7. Template is not Instance

### Template/package data

- Workspace structure and Surface composition;
- domain object schema;
- Employee and Responsibility templates;
- Strategy and Operating Rule defaults;
- capability/knowledge/permission requirements;
- result/evidence presentation;
- package migration metadata.

### Instance data

- Company and Workspace identity;
- user strategy, targets and configuration;
- real Employee assignments;
- credentials and connection references;
- private Knowledge references;
- conversations and memory;
- business objects, history, evidence and results;
- decisions and external receipts.

Installation materialises an instance from a package version. The instance pins that package version, while all user-owned data remains outside the package store.

An upgrade must never overwrite user strategy or operating data merely because a new template default changed.

## 8. Evolution, migration and rollback

Workspace Engineering must support more than creation:

```text
Installed package v1
→ discover v2
→ compatibility + signature check
→ create candidate upgrade
→ show manifest/schema/permission impact
→ dry-run migration on instance metadata/data copy
→ capability check + simulation
→ CEO apply
→ audit and version pin v2
```

Required rules:

1. The current operating version remains immutable during evaluation.
2. Schema migration declares `from`, `to`, compatible Core range, reversible/irreversible status and affected object types.
3. A backup/checkpoint exists before a data migration.
4. Failed migration leaves the old operating version readable.
5. Rollback restores package/schema/projection state where reversible; it does not pretend to undo external side effects.
6. Removing a Surface does not silently delete its instance data.
7. Package revocation disables new execution when necessary while keeping user data exportable/readable.

P0 does not need full evolution. It needs version pinning and a clear “no migration supported” rejection for incompatible upgrades. Migration and rollback remain post-P0 work and are not planned in this closure.

## 9. Install and uninstall lifecycle

### Install

```text
Import archive
→ verify digest/provenance (and signature when the post-P0 trust model exists)
→ validate schema and Core compatibility
→ inspect capability/permission requirements
→ extract atomically into app-data package store
→ register package/version
→ optionally create Company-scoped instance draft
→ navigation appears from registry
```

Installation does not activate capabilities or start employees.

### Uninstall

```text
check active instances/runs
→ block or pause safely
→ unregister package navigation
→ disable package version and archive registry metadata/schema snapshot
→ remove package files when unreferenced
→ retain/archive instance data by default
```

“Uninstall makes the office disappear” means the active package entry, navigation and unreferenced package files disappear. P0 retains business objects and an archived manifest/schema/provenance snapshot as read-only archived data. Reinstalling the same compatible package may reattach the instance; physical deletion is outside P0 and requires a separate explicit retention decision.

## 10. Marketplace feasibility

The desired chain is technically valid:

```text
Creator builds Workspace
→ Export Template
→ Validate
→ Sign
→ Publish
→ Marketplace
→ Install
→ Capability Check
→ Configure
→ Run
```

It is not supportable on the current app. The largest blockers are:

1. **Execution trust:** preventing package code from becoming arbitrary local code execution.
2. **Data migration:** preserving instance-owned data across package versions.
3. **Publisher identity and revocation:** compromised or malicious signing keys.
4. **Core compatibility:** avoiding packages tied to private implementation details.
5. **Capability honesty:** installing structure without claiming that Agent/Connector/Computer Access is available.
6. **Cross-platform extensions:** signing, distribution and sandboxing native components per OS.

Marketplace UI is not needed to solve these blockers. A local package importer and official sample package must pass first.

## 11. Minimal PoC: 客户反馈办公室

### 11.1 PoC claim

On an already installed Curis Desktop, without source changes, rebuild or app reinstall:

```text
install a previously absent Workspace Package
→ navigation appears
→ create/open instance
→ Main / Context / Utility render
→ create one real business object
→ execute one allowed action
→ restart and recover
→ uninstall and remove navigation
```

### 11.2 Package contents

- Package: `com.curis.sample.customer-feedback-office@0.1.0`.
- Navigation label: `客户反馈办公室`.
- Domain object: `CustomerFeedback`.
- Minimal fields: summary, source, status, owner reference, created time.
- Main: feedback list and selected feedback detail.
- Context: customer/source context.
- Utility: evidence and handling activity.
- Owner reference: may reference an existing real Employee if assigned; otherwise remain unassigned. Never fabricate a working employee.
- Action: `记录反馈`, mapped to `core.domain-object.create`.
- Capability requirements: none for the first PoC.

### 11.3 PoC acceptance

1. Start with a Curis build whose source does not contain the package ID or Workspace type.
2. Import the package through a local package install command/API owned by Core.
3. Validate digest, declared files, schema, compatibility and controlled local trust/provenance state.
4. Observe the new Workspace navigation and create an instance.
5. Persist one real `CustomerFeedback` object and one activity record.
6. Restart Desktop; the package registration, instance and object remain readable.
7. Uninstall; navigation and active package files disappear.
8. Instance data is retained/archived according to the explicit uninstall choice, not silently deleted.
9. No React/Python/Rust source changes, rebuild, app update, raw SQL or secret is used.

Passing this PoC is the minimum proof that Workspace Engineering has moved from “developing Curis” to “a Curis Runtime capability.”

## 12. Minimal implementation route

### P0 — prove dynamic declarative installation

1. Define the smallest Review-state package manifest and compatibility rules required by the PoC.
2. Add package validator, digest/provenance record, safe extraction and atomic app-data package store.
3. Add installed-package registry and registry-driven Workspace navigation.
4. Add finite Core Surface component registry and declarative renderer.
5. Extend Runtime Foundation with one generic scoped package-domain-object type, a safe read projection and one allowed create action.
6. Materialise Template → Instance with package/version provenance.
7. Resolve package requirements through existing Capability Registry states.
8. Pass the customer-feedback install/restart/uninstall PoC.

P0 explicitly excludes arbitrary extension code, package update/migration, export tooling, general signing PKI and Marketplace. Later phases remain future candidates and are not planned in this closure.

## 13. Non-goals

This proposal does not require:

- a general DAG or Workflow Engine;
- arbitrary code execution inside Workspace packages;
- a second Capability/Employee/Decision system;
- per-template SQL tables;
- a Marketplace UI before local package safety works;
- Full Computer Access;
- migration of existing XHS/RD/TTK in the first PoC.

## 14. Technical decision summary

1. Controlled declarative Package P0 / P0.5 exists; generic multi-Surface Workspace creation is not yet implemented or accepted.
2. The recommended architecture is declarative packages first, restricted extensions later.
3. Shared Company OS Runtime remains authoritative; packages compose it.
4. Template structure and instance data are strictly separate.
5. Permissions are requirements, never grants.
6. Package evolution requires version pinning, candidate migration and auditable rollback.
7. Marketplace feasibility depends first on the controlled local-package PoC; P0 does not prove third-party trust or distribution.
8. The customer-feedback-office PoC is bounded substrate evidence, not generic multi-Surface product proof.

```text
WORKSPACE ENGINEERING TECHNICAL DIRECTION APPROVED CANDIDATE
CONTROLLED DECLARATIVE PACKAGE P0 / P0.5 IMPLEMENTED / ACCEPTED
MULTI-SURFACE WORKSPACE PACKAGE V2 FOUNDATION IMPLEMENTED / ACCEPTED / COMMITTED
USER-FACING STUDIO / PROFESSIONAL REGISTRY / PACKAGE EDITING NOT COMPLETE
FINAL PACKAGE SCHEMA NOT FROZEN
```
