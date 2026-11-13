# Workspace Engineering P1 Package Lifecycle Evidence

Status: ACCEPTED EVIDENCE — SCHEMA-STABLE SUBSTRATE ONLY

Date: 2026-08-17

## Isolation and build ordering

- Active DB baseline/final: size `1232896`, mtime `1786873339`, SHA-256
  `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, integrity `ok`.
- Desktop proof DB:
  `/tmp/curis-workspace-p1-desktop-home-20260817/Library/Application Support/com.curis.desktop/data/curis.sqlite`.
- `CURIS_DB`, `CURIS_DB_PATH`, `CURIS_WORKSPACE_DB` all resolved to that repository-external file.
- The Desktop build completed before
  `/tmp/curis-workspace-p1-desktop-20260817/{v1,v2,v3-incompatible}` existed.
- Executable: size `5267408`, SHA-256
  `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf`.
- Packaged backend: size `10655392`, SHA-256
  `0c2468f050c76574daf5660fd8719ed104afa45118990b52aa9014255f59f8c4`.
- Bundle scan before Package creation found zero Package ID / v2 label matches.

## Dynamic lifecycle proof

| Step | Result |
| --- | --- |
| Install/operate 0.1.0 | Package digest `d2945066...`; real CustomerFeedback and Operating chain completed |
| Preview 0.2.0 | compatible `true`; `EXACT_SCHEMA_STABLE`; `NONE_SCHEMA_IDENTICAL` |
| Upgrade 0.1.0→0.2.0 | same instance/workspace/object/Core IDs; surface title changed to `客户反馈 v2` |
| Preview 0.3.0 | compatible `false`; `MIGRATION_REQUIRED_NOT_SUPPORTED` |
| Apply 0.3.0 | HTTP 422; current remained 0.2.0; event count remained 1; no 0.3 store directory |
| Desktop restart 1 | 0.2.0 and all real Company OS references recovered |
| Rollback 0.2.0→0.1.0 | append-only second event; surface returned to `客户反馈 v1` |
| Desktop restart 2 | 0.1.0 and all real Company OS references recovered |

Lifecycle fingerprints:

| Transition | Identity | Business data | Company OS |
| --- | --- | --- | --- |
| Upgrade | `d9ae9ca6...` | `01032878...` before = after | `b0dfde88...` before = after |
| Rollback | `d9ae9ca6...` | `01032878...` before = after | `0c744767...` before = after |

The Company OS fingerprint legitimately changed between the two transitions because normal Desktop
restart recovery updated an existing Task recovery timestamp; each transition itself remained exact.

## Persistent identity proof

- company: `company-p1-desktop`
- workspace: `workspace-package-f5820be0-1df5-4a3d-bcd6-0016331d1fa3`
- instance: `workspace-package-instance-2d42f310-735d-46e5-a4b0-37172d7fac19`
- CustomerFeedback: `package-object-ed9f8b1a-6b71-4519-b6c0-c3568a99ea03`
- responsibility: `role-slot-p1-feedback-triage`
- employee: `ai-employee-p1-feedback-triage`
- capability binding: `capability-binding-p1-feedback-triage`
- task: `3d1b0d00-2b16-4b60-ad71-4715a484e697`
- execution: `1`
- evidence: `evidence-9d2818d3-7041-406a-b6dd-1743ce02b5da`
- outcome: `outcome-4f6b9853-5a20-47d8-b9ff-c6fb7c41c2c8`
- artifact: `artifact-3a21fc1e-0fdd-4ff4-9513-866b7c6f0597`

After both restarts: Company Integration `COMPLETED`, object `TRIAGED`, `resolvable=true`,
`reverseResolved=true`.

## Verification

- focused Package P0/P0.5/P1: `3 passed`;
- bounded backend no-regression: `25 passed`;
- frontend Package/RD/Runtime Workspace: `11 passed`;
- Python compile check: passed;
- isolated SQLite: `integrity_check=ok`, `foreign_key_check` returned no rows;
- final stored versions: `0.1.0`, `0.2.0`; no `0.3.0` directory;
- final instance pin after rollback/restart: `0.1.0`;
- active SQLite: exact baseline size/mtime/SHA-256 preserved, integrity `ok`.

## Acceptance ceiling

This evidence accepts only schema-identical Package lifecycle. No schema/data migration, general
rollback, Team continuity, external compensation, Marketplace/update distribution or full
Workspace Engineering `Evolvable` capability was implemented or accepted.
