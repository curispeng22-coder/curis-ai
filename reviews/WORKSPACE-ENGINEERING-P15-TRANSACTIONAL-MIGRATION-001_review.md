# WORKSPACE-ENGINEERING-P15-TRANSACTIONAL-MIGRATION-001 Review

Status: ACCEPTED — BOUNDED REVERSIBLE RENAME MIGRATION ONLY

Date: 2026-08-17

Decision: `TRANSACTIONAL PACKAGE DOMAIN DATA MIGRATION SUBSTRATE IMPLEMENTED / ACCEPTED`

Ceiling: `WORKSPACE ENGINEERING FULL EVOLVABLE NOT ACCEPTED`

## Reviewed boundary

The implementation migrates only Package-owned logical schema and JSON business data. A migration
may declare exact reversible `renameField` operations whose target schema is mechanically proven to
contain no undeclared change. It cannot run SQL/code, modify Core-owned relationship fields, perform
type conversion/delete/split/merge, or claim an Operating Team identity.

## Acceptance result

| Gate | Result |
| --- | --- |
| Manifest/provenance | PASS — migration file is declared, validated and included in Package digest |
| Pure preflight | PASS — exact transition, schema equivalence, reversibility, two affected objects and checkpoint digest |
| Real migration | PASS — persisted `customerRef → accountRef`, schema `0.1.0 → 0.2.0` |
| Atomic failure | PASS — SQLite failure after one row update rolled back both rows, projection, pin, registry and lifecycle |
| Old-office recovery | PASS — failed journal retained; v1 office and complete Company OS chain remained usable |
| Activation | PASS — data/projection migration + pin + Workspace projection + journal/event committed once |
| Restart/continue | PASS — v2 recovered; new v2 object created and completed through real Task/Evidence/Result |
| Down rollback | PASS — three objects migrated `accountRef → customerRef`; original checkpoint verified; v2-created object retained |
| Rollback failure | PASS in focused test — injected mid-down failure retained complete v2 state |
| Restart after rollback | PASS — v1 pin and the v2-created object's real Company OS chain recovered |
| Irreversible truth | PASS — v2→v3 rejected HTTP 422 before Store/journal/data mutation |
| SQLite/no regression | PASS — isolated integrity/FK, 23 backend + 11 frontend bounded regression |
| Active DB guard | PASS — size/mtime/SHA-256 byte-identical; integrity `ok` |

## Desktop build-before-Package evidence

- build began at epoch `1786952147` and completed before Package root creation;
- Package root was created at epoch `1786952294`;
- executable SHA-256: `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf`;
- packaged backend SHA-256: `77bc0e4d968a8c4476b8f548783d7a2aae7509434eec541cdeb0db6fc32a23fe`;
- bundle scan found zero Package ID / v2 surface-label matches;
- the same executable installed v1, failed and recovered one migration, applied v2, restarted,
  continued Operating, rejected irreversible v3, ran down migration and restarted again without
  source edit/rebuild/reinstall.

Detailed evidence is registered at
`docs/reviews/workspace-engineering-p15-migration-2026-08-17/README.md`.

## Identity continuity

Preserved exact IDs:

- company `company-p15-desktop`;
- business `package:com.curis.sample.customer-feedback-office`;
- workspace `workspace-package-8f135276-4d0a-4170-a38e-982b3e34e47d`;
- instance `workspace-package-instance-dde0ad88-c192-4053-8c8b-483b70ee53bb`;
- pre-migration object `package-object-a1d9ce83-4538-4041-9718-643b56a1f308`;
- Role Slot `role-slot-p15-desktop`, Employee `ai-employee-p15-desktop` and Capability Binding
  `capability-binding-p15-desktop`;
- original Task `7ab55a6b-3dfb-4f44-9b7a-3bf4e5cd4d5e`, Evidence
  `evidence-8125a523-be7a-4c03-afb7-ba9777e53d35` and result references;
- post-restart v2 object `package-object-4c116dfc-bcc2-4e94-a8bc-8d4b90205db0` and Task
  `c635044f-1f70-4442-b83a-eb9a2678a615` through rollback and second restart.

Both applied UP and DOWN events have different business-data fingerprints and equal protected
Company OS fingerprints, which is the required migration truth.

## Explicitly not accepted

- authoritative Operating Team continuity: current Core has no Team identity/table/lifecycle;
- arbitrary physical SQLite or general migration framework;
- type conversion, add/default/delete, split/merge, cross-object or irreversible migration;
- checkpoint restore as a substitute for an undeclared down migration;
- multi-instance install/cardinality and coordinated rollout;
- external-side-effect compensation, history GC/uninstall redesign;
- Marketplace/update distribution/PKI/UI and RD/XHS/TTK migration.

No Full Evolvable claim is authorized.
