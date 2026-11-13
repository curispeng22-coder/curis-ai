# CURIS CANONICAL BUSINESS SPINE — IMPLEMENTATION 001 REVIEW

Authority Class: REVIEW
Status: Review
Disposition: IMPLEMENTED / ACCEPTED
Date: 2026-08-21
Owner: 主开发 / Company OS Integration Owner

## 1. Verdict

The canonical `Company → Department → Business → Workspace` spine is implemented,
recoverable from the controlled clean source baseline, and accepted in a newly built
Packaged Desktop. The earlier Frontend and Desktop source-baseline blockers are closed by
their accepted closure records and are not Current blockers.

No active repository SQLite was initialized, migrated or mutated. The final scoped commit
contains only the exact accepted Business Spine, Frontend closure and Desktop source target
manifest; it was not pushed.

## 2. Accepted runtime truth

- Canonical Business is persisted and belongs to an existing Department in the same Company.
- Business without a valid Department is rejected.
- A resolved Workspace cannot reference a missing, cross-Company or archived Business.
- Business + First DRAFT Workspace + first Workspace version are created atomically.
- Existing Workspace Package installation uses the same canonical relation and transaction.
- Ambiguous legacy relations remain `UNRESOLVED`; explicit classification moves them to
  `QUARANTINED` without guessing a Business.
- Unresolved or quarantined Workspaces cannot create a Cycle or enter normal Operating.
- Parent Resolver returns authoritative `Workspace → Business → Department → Company` truth.
- Business Read Model derives its Workspace Directory, operating summary and team from
  canonical relations and existing Runtime objects; it does not create a second truth.

## 3. Controlled source baseline

Frontend closure consumed:

- `docs/reviews/CURIS_FRONTEND_BASELINE_CLOSURE_REVIEW.md`
- Business / Workspace routes and shared Runtime seams have accepted semantic ownership.

Desktop closure consumed:

- `docs/reviews/CURIS_DESKTOP_SOURCE_BASELINE_CLOSURE_REVIEW.md`
- exact 21-file Desktop source boundary plus `frontend/next.config.js` packaging delta;
- generated `.runtime`, `target`, `node_modules` and old `.app` outputs were excluded.

The final exact index contained 59 files. No broad add, generated output promotion or
unrelated worktree cleanup was used.

Clean source export:

- root: `/tmp/curis-business-spine-packaged-final.rNs44O`
- pre-review combined tree: `0107f5e167d44655cd4b45e6a096f7c8e3d1dc92`
- frontend standalone, Workspace/Gateway/Guardian sidecars and Cargo/Tauri were rebuilt from
  that clean source.

Fresh package:

- app: `/tmp/curis-business-spine-packaged-final.rNs44O/desktop/target/release/bundle/macos/Curis.app`
- executable SHA-256: `f2f91d2d282f03e15ff7c62ee26219020fc8fc17cd4f20751ebbac91b173e8b5`
- bundle identifier: `com.curis.desktop`

## 4. Clean verification

- canonical Business / Workspace Package focused backend suite: **13 passed**;
- Phase 7 canonical scenarios: **4 passed**;
- Python compile: **PASS**;
- frontend Runtime / Workspace regression: **19 passed**;
- shared Provider / State / Layout regression: **1 passed**;
- scoped ESLint: **0 errors**, 3 pre-existing RD Hook warnings;
- Next production build: **PASS**, 42 routes;
- fresh standalone / sidecars / Cargo / Tauri / `.app` build: **PASS**;
- `git diff --cached --check`: **PASS**.

## 5. Fresh Packaged Desktop evidence

Packaged acceptance used only the newly built `.app`, with isolated app-data and SQLite:

- app-data root: `/tmp/curis-business-spine-packaged-e2e.ifVVPW`
- database: `/tmp/curis-business-spine-packaged-e2e.ifVVPW/home/Library/Application Support/com.curis.desktop/data/curis.sqlite`
- integrity: `ok`; foreign-key check returned no violations.

### A — Single Workspace Business

The Packaged Desktop displayed:

`Packaged Spine Company / Engineering Department / Curis 产品研发 / Curis 研发`.

The Workspace entry consumed the Parent Resolver and linked back to the canonical Business.
Direct refresh retained the same identity.

### B — Multi Workspace Business

`Curis 产品研发` displayed two independent Workspaces:

- `Curis 研发`
- `Curis 研发二组`

Both resolved to the same canonical Business and Department while retaining distinct
Workspace identities. Business Directory and both deep routes were verified in the
Packaged Desktop.

### C — Generic New Business

Package installation atomically produced:

- Business: `客户反馈业务`
- First DRAFT Workspace: `Feedback Lab`

The canonical Workspace entry opened the installed declarative work surface and remained
available after direct refresh. Missing-Department failure injection left no partial
Business.

### D — Legacy

The ambiguous legacy Workspace was explicitly changed from `UNRESOLVED` to `QUARANTINED`.
It was excluded from the canonical Workspace Directory, its direct route displayed
`工作空间归属尚未确认`, and Cycle creation remained rejected.

### E — Restart

The Packaged Desktop was closed and reopened through the macOS `.app` launch path with the
same isolated app-data. After restart it reread the same Company, two Businesses, three
canonical Workspaces, directories and Parent Resolver paths. Persisted data was not treated
as a substitute for Runtime startup; the UI changed from its pre-restart stale empty snapshot
to the current persisted Company only after the new Runtime was running.

## 6. Browser versus Packaged truth

Prior Browser acceptance remains valid, but it was not used as a substitute for this gate.
The Single, Multi, Generic, Legacy and restart observations above were performed against the
newly built Packaged Desktop WebView and packaged sidecars on ports 3010 / 8002 / 8080.

## 7. Active SQLite safety

Final fingerprints equal the Phase 0 fingerprints:

| Path | Size | mtime | SHA-256 | integrity |
| --- | ---: | ---: | --- | --- |
| `data/curis.sqlite` | 1232896 | 1786873339 | `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6` | ok |
| `backend/data/curis.sqlite` | 1277952 | 1786783659 | `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4` | ok |

## 8. Final acceptance answers

1. Canonical Business persisted: **YES**.
2. Orphan Business prohibited: **YES**.
3. Orphan Workspace prohibited: **YES**.
4. Business + First Workspace atomic: **YES**.
5. Legacy ambiguity fail-closed: **YES**.
6. Parent Resolver real: **YES**.
7. Business Read Model real: **YES**.
8. Frontend baseline clean-checkout recoverable: **YES**.
9. Browser passed: **YES**.
10. Fresh Packaged Desktop passed: **YES**.
11. Single / Multi / Generic E2E passed: **YES**.
12. Restart / reread passed: **YES**.
13. Active databases unchanged: **YES**.
14. Commit contains only the exact Issue scope: **YES**; not pushed.

## 9. Final status

`IMPLEMENTED / ACCEPTED`

CURIS CANONICAL BUSINESS SPINE
— CANONICAL BUSINESS IDENTITY LIVE
— COMPANY / DEPARTMENT / BUSINESS / WORKSPACE CLOSED
— ATOMIC FIRST WORKSPACE VERIFIED
— LEGACY QUARANTINE VERIFIED
— PARENT RESOLVER VERIFIED
— BUSINESS READ MODEL VERIFIED
— CLEAN FRONTEND BASELINE VERIFIED
— CLEAN DESKTOP SOURCE BASELINE VERIFIED
— FRESH PACKAGED DESKTOP VERIFIED
— PACKAGED SINGLE / MULTI / GENERIC E2E VERIFIED
— PACKAGED RESTART VERIFIED
— ACTIVE DB UNCHANGED
— COMMITTED
— NOT PUSHED
