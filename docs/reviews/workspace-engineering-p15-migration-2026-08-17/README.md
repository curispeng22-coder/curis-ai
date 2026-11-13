# Workspace Engineering P1.5 Transactional Migration Evidence

Status: ACCEPTED EVIDENCE — BOUNDED REVERSIBLE RENAME MIGRATION ONLY

Date: 2026-08-17

## Build and isolation

- active DB baseline/final: size `1232896`, mtime `1786873339`, SHA-256
  `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, integrity `ok`;
- Desktop proof DB:
  `/tmp/curis-workspace-p15-desktop-home-20260817/Library/Application Support/com.curis.desktop/data/curis.sqlite`;
- all three DB environment variables resolved to that repository-external isolated DB;
- Desktop build start `1786952147`; Package root creation `1786952294`;
- executable: size `5267408`, SHA-256
  `1e73656fd32f3978b8a3b4b929d1ce1d25ffb694bb2a6a6ae766359328d74abf`;
- packaged backend: size `10694640`, SHA-256
  `77bc0e4d968a8c4476b8f548783d7a2aae7509434eec541cdeb0db6fc32a23fe`;
- bundle Package ID / v2 label matches before external Package creation: `0`.

## Desktop transition evidence

| Step | Result |
| --- | --- |
| Install v1 | `com.curis.sample.customer-feedback-office@0.1.0`, digest `5ec42cd2...` |
| Create/operate | two v1 objects; first completed real Role/Employee/Capability/Task/Execution/Evidence/Outcome/Artifact chain |
| v2 preflight | compatible; `DECLARATIVE_RENAME_FIELDS_V1`; reversible; affected objects `2`; checkpoint `612145f0...` |
| Injected mid-up failure | HTTP 500; journal `FAILED/IntegrityError`; both rows v1; pin v1; lifecycle count 0; no v2 store directory |
| Retry UP | v2 digest `7e67edc5...`; both rows schema `0.2.0`; `customerRef` became `accountRef` |
| Irreversible v3 | preview reason `IRREVERSIBLE_MIGRATION_NOT_SUPPORTED`; apply HTTP 422; no v3 store/journal/event |
| Restart 1 | v2 pin and original Company OS IDs/reverse links recovered |
| Continue Operating | new v2 object created with `accountRef`; real Task/Evidence/Result completed |
| DOWN | all three rows schema `0.1.0`; `accountRef` became `customerRef`; original checkpoint verified |
| Restart 2 | v1 pin and post-v2 object's Task/Evidence/Result/reverse links recovered |

## Journal and fingerprints

| Direction | Status | Objects | Data before/after | Protected Core before/after |
| --- | --- | ---: | --- | --- |
| UP | FAILED | 2 | before retained; no after | no committed change |
| UP | APPLIED | 2 | `0ecf821f... → 466f3849...` | equal |
| DOWN | APPLIED | 3 | `033855d1... → e64085f9...` | equal |

Applied lifecycle events correctly record `data_same=0` and `company_os_same=1`.

## Persistent IDs

- workspace: `workspace-package-8f135276-4d0a-4170-a38e-982b3e34e47d`
- instance: `workspace-package-instance-dde0ad88-c192-4053-8c8b-483b70ee53bb`
- original object: `package-object-a1d9ce83-4538-4041-9718-643b56a1f308`
- post-restart v2 object: `package-object-4c116dfc-bcc2-4e94-a8bc-8d4b90205db0`
- responsibility: `role-slot-p15-desktop`
- employee: `ai-employee-p15-desktop`
- original task/evidence: `7ab55a6b-3dfb-4f44-9b7a-3bf4e5cd4d5e` /
  `evidence-8125a523-be7a-4c03-afb7-ba9777e53d35`
- post-restart task/evidence: `c635044f-1f70-4442-b83a-eb9a2678a615` /
  `evidence-e018bd2e-d6de-48c5-9b9f-62d72783f672`

## Verification

- P1.5 focused: `3 passed`;
- final bounded backend current-HEAD regression: `23 passed`;
- frontend Package/RD/Runtime Workspace: `11 passed`;
- Python compile: passed;
- isolated SQLite: `integrity_check=ok`, no foreign-key violations;
- packaged Desktop: build-before-Package, migration failure, activation, two restarts, continued
  Operating, irreversible rejection and declared down rollback passed;
- active SQLite exact baseline size/mtime/SHA-256 preserved, integrity `ok`.

## Acceptance ceiling

This evidence does not verify Operating Team identity: the isolated Runtime contains zero
`TEAM/OPERATING_TEAM` entities because no authoritative Core primitive exists. It also does not
accept general/physical/irreversible/multi-instance migration or Full Evolvable.
