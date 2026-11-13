# Workspace Engineering P1.5 Transactional Migration & Identity Continuity Audit

Status: Review

Updated: 2026-08-17

Decision: BOUNDED PACKAGE-OWNED JSON MIGRATION ACCEPTED; FULL EVOLVABLE NOT ACCEPTED

## 1. Current runtime truth

P1 already accepts schema-identical Package version-pin update/restart/rollback. P1.5 does not
reopen it.

The Package Domain Schema is a declarative logical schema stored in
`installed_workspace_packages.schemas_json`. Instance business objects are rows in
`workspace_package_objects`; their Package-owned fields live in `data_json`, and the same object ID
is projected into `runtime_entities(PACKAGE_DOMAIN_OBJECT)`. A real Package schema/data migration
therefore changes the declared schema and persisted JSON payload/schema version. It does not require
or justify arbitrary SQLite `ALTER TABLE` supplied by a Package.

Ownership is split as follows:

| Fact | Owner | Migration permission |
| --- | --- | --- |
| Package manifest/surfaces/domain schema | immutable Package version | target version may replace projection at activation |
| `workspace_package_objects.data_json/schema_version` | Workspace instance/user business data | only declared, validated Package migration may transform |
| Package object ID/company/workspace/instance/owner/state | Curis Core identity boundary | immutable through migration |
| matching `runtime_entities(PACKAGE_DOMAIN_OBJECT)` payload | Core projection of the same object | updated in the same transaction; ID and Core refs immutable |
| Employee/Role Slot/Capability/Task/Execution/Evidence/Outcome/links | Company OS Core | Package migration may verify, never rewrite |
| Package Store files | immutable content-addressed Package version | staged before activation; never authoritative by file presence alone |

## 2. Existing gaps

| Concern | Current P1 status | P1.5 decision |
| --- | --- | --- |
| Schema-changing preflight | rejects every change | add pure validated migration plan and affected-object count |
| Migration declaration | absent | one bounded declarative rename-field contract only |
| Checkpoint | fingerprints only | durable pre-migration object/projection checkpoint in Package-owned journal |
| Atomic activation | version pin transaction exists | data transform + projection + pin + provenance in one `BEGIN IMMEDIATE` transaction |
| Failure journal | no migration attempt | append PREPARED/APPLIED/FAILED truth; PREPARED recovery is fail-safe |
| Reversible rollback | only schema-identical pin rollback | declared inverse rename + exact checkpoint verification + pin rollback atomically |
| Irreversible migration | unsupported | fail closed before Package Store or data mutation |
| Restart recovery | pin/history only | recover APPLIED state; mark interrupted PREPARED attempt failed while old pin remains authoritative |
| Multi-instance | registry/install model does not materialise a second instance for one tenant/package version | audit only; do not widen install/cardinality in P1.5 |
| Uninstall/history retention | P1 boundary only | retain packages/checkpoints referenced by migration history; broader GC remains Gap |

## 3. Bounded migration contract

P1.5 permits an optional Package manifest field:

```json
"migrationManifest": "migrations/manifest.json"
```

The referenced document has one exact transition:

```json
{
  "schemaVersion": "curis.workspace-migration/v1",
  "fromVersion": "0.1.0",
  "toVersion": "0.2.0",
  "reversible": true,
  "objects": {
    "FeedbackRecord": {
      "fromSchemaVersion": "0.1.0",
      "toSchemaVersion": "0.2.0",
      "up": [{"op": "renameField", "from": "customerRef", "to": "accountRef"}],
      "down": [{"op": "renameField", "from": "accountRef", "to": "customerRef"}]
    }
  }
}
```

Validation requires:

- exact current/target Package versions, same Package ID and compatible Core;
- `reversible=true`; irreversible declarations fail closed in P1.5;
- affected object types already exist in both Package versions;
- target schema equals the source schema after only the declared property/required-field rename and
  schema-version change;
- `down` is the exact inverse of `up`;
- every persisted affected object has each source field and no target-field collision;
- transformed payload validates against the target schema before any mutation.

No defaults, type conversion, delete, split/merge, arbitrary SQL/code or cross-object operation is
supported. This is deliberately not a global Migration Framework.

## 4. Transaction and checkpoint truth

1. Pure preflight validates Package, transition, every affected object and target payload.
2. Target Package is copied to the existing immutable content-addressed store.
3. A durable `PREPARED` journal row records old pin and exact Package-owned object/projection
   checkpoint; the operating pin is still unchanged.
4. One SQLite `BEGIN IMMEDIATE` transaction rechecks the pin, transforms all affected objects and
   same-ID projections, validates protected Core identity/links, activates the target pin, writes
   workspace/lifecycle provenance, and marks the journal `APPLIED`.
5. Any exception rolls the transaction back. The journal becomes `FAILED`, newly copied target
   files are removed when unreferenced, and the old office remains authoritative.
6. On restart, a remaining `PREPARED` row cannot represent a half-commit: SQLite either committed
   the APPLIED transaction or rolled it back. Runtime verifies the old pin and marks the attempt
   failed/recovered; it never infers activation from files.

Rollback of an applied reversible migration executes the declared `down` transform and must exactly
match the stored pre-upgrade checkpoint before the old pin is reactivated. A normal file-version
switch is not accepted as data rollback.

## 5. Identity continuity

P1.5 must preserve exact IDs and scoped links for Company, Business, Workspace, Package instance,
Package objects, Employee, Role Slot/Responsibility, Capability Binding, Task, Execution, Evidence,
Outcome and Artifact. Only Package-owned payload/schema version and Package/version projections may
change.

Frozen Company OS §9 requires a real Operating Team for a long-term Business. Current Runtime has no
authoritative `TEAM`/`OPERATING_TEAM` entity, table, lifecycle or resolvable Team ID. P1.5 must not
invent one in Package data or reinterpret Employee/Role Slot rows as a Team. Therefore:

```text
OPERATING TEAM IDENTITY CONTINUITY = NOT VERIFIABLE / CORE GAP
```

An Authority-aligned Core Team identity proposal is required before full Team continuity or Full
Evolvable can be accepted. This gap does not block the bounded Package-owned data migration proof.

## 6. Acceptance ceiling

Passing the bounded proof may declare:

```text
TRANSACTIONAL PACKAGE DOMAIN DATA MIGRATION SUBSTRATE IMPLEMENTED / ACCEPTED
REVERSIBLE RENAME MIGRATION + ATOMIC RECOVERY ACCEPTED
EVOLVABLE FOUNDATION PARTIAL
WORKSPACE ENGINEERING FULL EVOLVABLE NOT ACCEPTED
```

It may not declare physical arbitrary SQLite migrations, irreversible migration, multi-instance
lifecycle, Operating Team continuity, general migration/rollback, Marketplace or UI.

## 7. Implemented outcome

`WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001` implemented and accepted the exact bounded
contract above:

- optional digest-covered migration manifest;
- pure preflight and exact affected-object count;
- durable PREPARED/APPLIED/FAILED journal plus object/projection checkpoint;
- one SQLite transaction for data/projection transform, target registration, version pin, Workspace
  projection and lifecycle provenance;
- injected mid-up and mid-down failures with complete rollback;
- interrupted PREPARED restart recovery without file-based activation inference;
- reversible `customerRef ↔ accountRef` migration and exact checkpoint verification;
- irreversible migration rejection before Store/journal/data mutation;
- packaged Desktop build-before-Package migration, two restarts and continued Operating proof.

The Package Domain Schema and persisted `data_json/schema_version` changed for real. No physical
Package-authored SQLite DDL ran. Company/Business/Workspace/instance/object and all existing Core
references remained continuous. Operating Team continuity remains unverified because the current
Core still has no authoritative Team identity.

Final truth:

```text
TRANSACTIONAL PACKAGE DOMAIN DATA MIGRATION SUBSTRATE IMPLEMENTED / ACCEPTED
REVERSIBLE RENAME MIGRATION + ATOMIC RECOVERY ACCEPTED
OPERATING TEAM IDENTITY CONTINUITY NOT VERIFIED / CORE GAP
WORKSPACE ENGINEERING FULL EVOLVABLE NOT ACCEPTED
```
