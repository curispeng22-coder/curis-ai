# WORKSPACE-ENGINEERING-P1-PACKAGE-LIFECYCLE-001 Review

Status: ACCEPTED — SCHEMA-STABLE SUBSTRATE ONLY

Date: 2026-08-17

Decision: `SCHEMA-STABLE PACKAGE LIFECYCLE SUBSTRATE IMPLEMENTED / ACCEPTED`

Ceiling: `WORKSPACE ENGINEERING EVOLVABLE NOT ACCEPTED`

## Reviewed boundary

The implementation reuses the accepted declarative Package Runtime and existing Company OS facts.
It adds preview, immutable target storage, in-place version-pin transition, append-only lifecycle
provenance and immediate-prior rollback only when normalized schema/actions/capability request and
retention are identical. It adds no migration language, Team primitive, Marketplace service,
arbitrary code or Domain migration.

## Acceptance evidence

| Gate | Result |
| --- | --- |
| Pure preview | PASS — `0.2.0` compatible; schema-changing `0.3.0` reports `MIGRATION_REQUIRED_NOT_SUPPORTED` |
| Upgrade | PASS — `0.1.0 → 0.2.0`, same company/workspace/instance/object/Core IDs |
| Failure truth | PASS — incompatible update HTTP 422; pin/event/store remain unchanged |
| Restart 1 | PASS — packaged Desktop recovers `0.2.0` and complete Operating chain |
| Rollback | PASS — `0.2.0 → 0.1.0`; pre/post data and Company OS fingerprints equal |
| Restart 2 | PASS — packaged Desktop recovers `0.1.0` and the same references |
| SQLite | PASS — isolated DB `integrity_check=ok`, no FK violations |
| Active DB guard | PASS — size/mtime/SHA-256 byte-identical to baseline, integrity `ok` |
| No regression | PASS — 25 backend, 11 frontend, focused Package/P0.5/P1 and compile checks |

Desktop build evidence:

- executable SHA-256: `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf`;
- packaged backend SHA-256: `0c2468f050c76574daf5660fd8719ed104afa45118990b52aa9014255f59f8c4`;
- build finished before the external version roots existed;
- the bundle contained neither the Package ID nor the `0.2.0` surface labels;
- after build, the same executable installed/operated `0.1.0`, upgraded to `0.2.0`, rejected
  incompatible `0.3.0`, restarted, rolled back and restarted again without rebuild/reinstall.

Detailed IDs, hashes and commands are recorded in
`docs/reviews/workspace-engineering-p1-lifecycle-2026-08-17/README.md`.

## Identity and data continuity

The proof preserved:

- company `company-p1-desktop`;
- workspace `workspace-package-f5820be0-1df5-4a3d-bcd6-0016331d1fa3`;
- instance `workspace-package-instance-2d42f310-735d-46e5-a4b0-37172d7fac19`;
- object `package-object-ed9f8b1a-6b71-4519-b6c0-c3568a99ea03`;
- real Role Slot, Employee, Capability Binding, Task, Execution, Evidence, Outcome and Artifact IDs.

Both upgrade and rollback recorded equal pre/post logical data and Company OS fingerprints.
After both restarts, Company Integration remained `COMPLETED`, object state remained `TRIAGED`, and
reverse resolution remained true.

## Remaining gaps

- real field/schema/data migration and its rollback semantics;
- authoritative Operating Team identity and continuity;
- multi-instance retention/garbage collection and history-aware uninstall/disable;
- external-side-effect compensation;
- semantic/operating-model versioning and Relevant Gate impact;
- Marketplace/update distribution/PKI and lifecycle UI.

No `EVOLVABLE ACCEPTED` claim is authorized.
