# Workspace Engineering Evolvable / Package Lifecycle Gap Audit

Status: Review

Updated: 2026-08-17

Scope: Current accepted P0/P0.5 declarative Package Runtime at
`main@fe55ff5d585d92505e0188d506e2f2ea7c57625e`

Decision: SCHEMA-STABLE LIFECYCLE SUBSTRATE ACCEPTED; EVOLVABLE NOT ACCEPTED

## 1. Current truth

P0/P0.5 are accepted through `Operating` and are not reopened. Current Package Runtime already
provides immutable `(tenant, package_id, version, digest)` records, content-addressed Package files,
an instance pinned to one package version, install provenance, restart recovery, retained business
data and real Company OS references.

It does not provide update, upgrade candidate state, migration, rollback or evolution acceptance.
`install()` explicitly rejects those operations. Existing `runtime_workspace_versions` records the
installed Workspace version but is not an append-only Package lifecycle attempt log.

## 2. Gap matrix

| Concern | Current status | Evidence / consequence |
| --- | --- | --- |
| Package ID + semantic version + digest | ALREADY IMPLEMENTED | Registry primary key and immutable digest conflict check |
| Instance version pin | ALREADY IMPLEMENTED | `workspace_package_instances.package_version/package_digest` |
| Package provenance | PARTIAL | install source/stored path/digest/time exist; no transition history |
| Core compatibility | PARTIAL | exact accepted Core range only; no cross-version impact report |
| Read-only update preview | GAP | no candidate comparison or affected-data report |
| Update / upgrade | GAP | explicitly rejected by `install()` |
| Compatibility validation | GAP | no old-versus-new schema/surface/identity comparison |
| Schema/data migration | GAP / PROPOSAL REQUIRED | no declarative migration language, semantics or reversible contract |
| Rollback | GAP | no previous-pin recovery or append-only provenance |
| Pre/post data protection | GAP | instance data is separate, but no logical checkpoint/fingerprint around a transition |
| Failed update recovery | PARTIAL | install staging is cleaned; no upgrade attempt truth or mixed-version guard |
| Desktop restart after update | GAP | only install/restart is accepted |
| Workspace / Business identity continuity | GAP | no update exists; current IDs can be preserved by an in-place version pin switch |
| Employee / Responsibility / Company OS links | GAP | no update proof; same-ID Core rows/links can be fingerprinted and preserved |
| Operating Team identity continuity | RUNTIME GAP / PROPOSAL REQUIRED | Frozen Company OS §9 requires a real Operating Team for a long-term Business, but current Runtime has no authoritative Team entity/ID to resolve; Package Runtime must not invent one |
| External-side-effect rollback | NOT GENERICALLY POSSIBLE | rollback can restore local package/projection state only; it cannot pretend to undo external actions |
| Relevant Gate impact analysis | PROPOSAL REQUIRED | requires semantic/operating-model version boundaries beyond manifest version alone |

## 3. Safe implementation boundary

The bounded implementation may add a **schema-stable Package lifecycle substrate**:

1. validate the target Package with the existing P0 trust boundary;
2. require the same `packageId`, exact current Core compatibility and a strictly newer semantic
   version for upgrade;
3. require byte-equivalent normalized domain schemas, action set, capability request and retention
   contract;
4. report a read-only compatibility preview before any file or database mutation;
5. copy the target into the existing content-addressed Package Store;
6. atomically switch the existing instance pin while preserving company, business, workspace,
   instance, objects and every existing Core entity/link ID;
7. append Package lifecycle provenance with pre/post business-data and Company-OS fingerprints;
8. permit rollback only to the immediately previous applied schema-identical version;
9. recover the current pin and history after full Desktop restart;
10. reject every schema-changing target as `MIGRATION_REQUIRED_NOT_SUPPORTED` without residue.

For this substrate, migration truth is `NONE_SCHEMA_IDENTICAL`. This is not a disguised schema
migration and does not justify `EVOLVABLE ACCEPTED`.

## 4. Data and identity invariants

An applied upgrade or rollback must preserve:

- `company_id`, `business_id`, `workspace_id`, `instance_id`;
- every `workspace_package_objects.object_id`, state, schema version, owner and business payload;
- same-ID `PACKAGE_DOMAIN_OBJECT` identity;
- existing Employee, Role Slot / Responsibility, Capability Binding, Task, Execution, Artifact,
  Evidence and Outcome IDs;
- all scoped `runtime_links`;
- user/instance-owned strategy, targets, configuration, business data and history.

Only the instance package version/digest, Package-owned manifest/surfaces projection, Workspace
package blueprint version/digest, operating version and append-only lifecycle/version provenance may
change. A mismatch between pre/post logical fingerprints aborts the transition.

## 5. Failure and recovery truth

- Validation and compatibility failure performs no Package Store or instance mutation.
- A filesystem/database failure must leave the previous instance pin authoritative and readable.
- Content-addressed old versions remain available while referenced by rollback history.
- Restart reconciliation must never infer an upgrade from files alone.
- A missing currently pinned Package directory remains `BROKEN/DISABLED`; it must not silently
  fall forward or backward.
- Rollback restores only local Package/projection state and records that boundary explicitly.

## 6. Proposal-only gaps

The following are not authorized for implementation by this audit:

- declarative field add/rename/split/merge/default/backfill migration semantics;
- irreversible migrations or physical data deletion;
- migration of existing XHS/RD/Content Growth/TTK instances;
- a new Team primitive or Package-owned Team identity;
- operating-model/semantic-model version authority and Relevant Gate automation;
- external-side-effect compensation;
- Marketplace, publisher PKI, revocation service or arbitrary extension code;
- final Package lifecycle UI.

These require a separately reviewed contract, real Domain examples and—where Team identity is
concerned—an Authority-aligned Core implementation decision.

## 7. Acceptance ceiling for this task

Passing the bounded proof may declare:

```text
SCHEMA-STABLE PACKAGE LIFECYCLE SUBSTRATE IMPLEMENTED / ACCEPTED
EVOLVABLE FOUNDATION PARTIAL
EVOLVABLE NOT ACCEPTED
```

It may not declare real Schema migration, general rollback or full Team continuity.

## 8. Implemented outcome

`WORKSPACE-ENGINEERING-P1-PACKAGE-LIFECYCLE-001` implemented and accepted only the
schema-stable boundary above. A packaged Desktop build completed before the `0.2.0` and incompatible
`0.3.0` Packages existed. Without source edits, rebuild or reinstall, that same binary then proved:

- `0.1.0 → 0.2.0` in-place upgrade with unchanged identity, business-data and Company OS facts;
- full Desktop restart recovery of the `0.2.0` pin and Operating references;
- fail-closed schema-changing `0.3.0` rejection with no stored version or lifecycle event;
- `0.2.0 → 0.1.0` rollback with unchanged identity, data and Company OS facts;
- second full Desktop restart recovery of the rollback pin and Operating references.

The accepted implementation is a version-pin/projection lifecycle substrate, not data migration.
The remaining gaps in §6 stay open. In addition, multi-instance version retention/garbage collection,
history-aware disable/uninstall, and external-side-effect compensation require later bounded work.

Final truth:

```text
SCHEMA-STABLE PACKAGE LIFECYCLE SUBSTRATE IMPLEMENTED / ACCEPTED
EVOLVABLE FOUNDATION PARTIAL
WORKSPACE ENGINEERING EVOLVABLE NOT ACCEPTED
```
