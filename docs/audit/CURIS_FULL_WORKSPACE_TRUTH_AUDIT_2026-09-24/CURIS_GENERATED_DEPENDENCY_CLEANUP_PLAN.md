# Generated / Dependency Cleanup Plan

Status: Review  
Authority Class: REVIEW / AUDIT EVIDENCE  
Baseline: File/Directory Manifest captured 2026-09-24 03:43 Asia/Shanghai; current Git worktree statuses were queried live later the same day.

## Classification and main candidates

| Family / exact root | Files / dirs | Manifest apparent bytes | Disposition | Rebuild / safe condition |
|---|---:|---:|---|---|
| `frontend/.next` | 5818 files / 895 dirs | 1,120,092,345 | SAFE_AFTER_PROCESS_STOP | Stop Next dev/build; `cd frontend && pnpm build` (or `pnpm dev` for dev output). This includes nested `.next/cache` and standalone output; do not double count. |
| `frontend/node_modules` | 21473 / 4333 | 394,517,032 | SAFE_AFTER_PROCESS_STOP | `frontend/pnpm-lock.yaml` exists; after stopping processes, exact `pnpm install --frozen-lockfile`. |
| `frontend/ceo-evidence/node_modules` | 52183 / 1619 | 129,778,651 | SAFE_AFTER_PROCESS_STOP | `package-lock.json` exists; after process stop, `npm ci`. |
| Four `.worktrees/*/frontend/node_modules` | four lockfile-backed roots | 2,419,950,693 | SAFE_AFTER_PROCESS_STOP for dependencies only; worktree roots BLOCKED | Stop per-branch process; reinstall using each `pnpm-lock.yaml`; do not remove worktree. |
| AiToEarn backend `node_modules` | 63151 / 16523 | 842,227,293 | SAFE_AFTER_PROCESS_STOP for dependencies only | Nested `pnpm-lock.yaml` exists; use `pnpm install --frozen-lockfile` only after stopping its process. Preserve parent `.curis/content-runtime/sources/AiToEarn` (business/user source). |
| `.worktrees/company-runtime-office-view/frontend/.next` | manifest-derived | 274,167,098 | SAFE_AFTER_PROCESS_STOP for build output; worktree BLOCKED | Stop process; rebuild from the branch; never remove parent checkout based on this row. |
| AiToEarn `.nx/cache` | manifest-derived | 15,645,630 | SAFE_AFTER_PROCESS_STOP | Stop that project's process; `pnpm exec nx reset`; preserve `.curis` sources. |
| `.pytest_cache` | 5 / 2 | 196,847 | SAFE_REGENERABLE_DELETE | Pytest recreates; retain failure evidence elsewhere. |
| Python `__pycache__` outside worktree/env/dependency/build roots | 1003 files / 22 dirs | 22,956,175 | SAFE_REGENERABLE_DELETE | Python recreates `.pyc`; source `.py` is retained. |
| `.venv` | 2443 / 315 | 42,625,793 | UNKNOWN | No complete environment lock established; don't include as safe. |
| `desktop/target`, `.runtime`, `.runtime/.trash` | mixed | directory manifest | UNKNOWN / KEEP_REQUIRED per subartifact | Release packages/runtime copies may be important or currently used; no blanket cleanup. |
| `.worktrees` source checkouts | 4 local roots in manifest | 3,303,189,101 | KEEP_REQUIRED / blocked | All local worktrees have dirty, untracked or unique commits. No checkout removal candidate. |

Part 1 inventory reports **324,452** machine-generated files and **54,179** machine-generated directories. This is a discovery metric, **not** safe cleanup volume. The exact explicit, non-overlapping dependency/cache roots above total **4,384,012,303 apparent bytes (4.384 GB)**; all require process/package/ownership gates before cleanup. Other `dist`, `build`, `coverage`, test-output and generated directories remain Unknown unless exact consumer/rebuild proof is recorded.

## Security and business-asset boundary

No browser profile, Chrome user-data, cookie, or session directory was identified by path-token review in the supplied Directory Manifest; no credentials, session content, or user data was opened. Any future discovered browser profile/session path is `SECURITY_SENSITIVE_REVIEW`, not cache. `.curis/content-runtime/sources/AiToEarn` is unique project/business source (about 1.14 GB in the manifest) and remains protected. `artifacts/`, CEO evidence, Figma/design sources, current visual references, release packages, and business-generated assets are not blanket cleanup targets. Active-process usage was not checked; every potentially live build/dependency root requires process stop and confirmation.

## Git ignored top 100 and tracked large files

`CURIS_STORAGE_RECLAMATION_MATRIX.csv` includes the **100 largest ignored individual file rows** verified with `git check-ignore` against paths already in the manifest (total apparent file sizes 5,119,952,981 bytes; rows overlap roots/hardlinks and are not additive). It also includes the current index's largest tracked files >=5 MB. Tracked binaries such as DMGs, runtimes, archives and evidence remain `KEEP_REQUIRED`/`UNKNOWN`; removal from the checkout alone would not reclaim Git history. No Git history strategy, `git gc`, or `git clean` is authorized.

## Node / Python package-manager inventory

- Frontend: `frontend/pnpm-lock.yaml`; `pnpm` rebuild is deterministic via `pnpm install --frozen-lockfile`.
- CEO evidence package: `frontend/ceo-evidence/package-lock.json`; `npm ci`.
- Desktop tooling: `desktop/pnpm-lock.yaml` and `package-lock.json` both exist; package-manager conflict is `UNKNOWN` until the build owner confirms which is canonical.
- Four in-repo worktree frontends: each has `pnpm-lock.yaml`; no worktree deletion is implied by dependency cleanup.
- Embedded AiToEarn backend: its `pnpm-lock.yaml` is present; preserve source tree and lockfile.
- `.venv`: no full environment lock was verified; leave in place.

## Reclamation totals (disjoint; apparent bytes from manifest)

- `SAFE_REGENERABLE_DELETE`: 1008 files / 23,153,022 bytes (**0.023 GB**).
- `SAFE_AFTER_PROCESS_STOP`: exact cache/dependency roots above, **4,384,012,303 bytes (4.384 GB)**; do not sum the overlapping Top-100 file rows.
- Part 2 old Exploration Delete Candidates: 883 files / 206,110,003 bytes (**0.206 GB**), contingent on Frozen §14 revision and CEO exact-set approval. Screenshot subset is 702 files and is included in, not added to, this total.
- Part 2 Archive Outside Active: 18 files / 293,229 bytes (**0.000 GB**); moving outside active preserves data and needs an approved external destination.
- Worktree removal candidates: 0; blocked worktree bytes are reported separately and are not reclaimable.
- Duplicate-document cleanup: 0 verified; no hashes in the Manifest, no file hash pass run.
