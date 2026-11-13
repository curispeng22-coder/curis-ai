# Curis Repository Hygiene Validation

Status: Review

Date: 2026-08-16

Scope: `.gitignore` boundary update and generated / local state isolation only.

HEAD before this hygiene change: `90f777440c76a75a69d7a49a499d7fdee8dd86b6`

## 1. Execution boundary

Completed in this pass:

- audited the existing `.gitignore` and visible / ignored local objects;
- updated only `.gitignore`;
- generated this validation report;
- precisely staged `.gitignore` and this report for review.

Not performed:

- no G2 / G3 source or test staging;
- no Shared Runtime change;
- no file deletion, move, reset, clean or database cleanup;
- no commit;
- no push.

## 2. `.gitignore` changes

### 2.1 Added or made explicit

The following rules are now explicit repository-hygiene boundaries:

```gitignore
.next/
.cache/
frontend/.cache/
desktop/target/
desktop/node_modules/
desktop/runtime/__pycache__/
*.sqlite-wal
*.sqlite-shm
*.db-wal
*.db-shm
```

`desktop/.runtime/` was already present and remains explicitly ignored as recreated Desktop packaging output.

`.DS_Store` and the broad `__pycache__/` rule were already present and were retained.

These rules cover rebuildable output or SQLite journal sidecars only. They do not ignore Desktop source, primary SQLite files, backups, evidence directories, prototypes or formal review material.

### 2.2 Removed unsafe broad database rules

The following broad rules were removed:

```gitignore
data/*.sqlite
backend/data/*.sqlite
backend/*Database*
```

Reason:

- `backend/data/*.sqlite` hid `backend/data/curis.sqlite`, which must remain visible for active/local SQLite retention review;
- `data/*.sqlite` hid primary and local databases whose provenance still needs review;
- `backend/*Database*` hid the 16 anomalously named SQLite files, which must remain visible until evidence / retention review decides whether they are archive or delete candidates.

The existing `backend/tests/data/*.sqlite` test-data rule was left unchanged because it is limited to the test-data directory and is not the active application database boundary.

## 3. Untracked-file measurement

Counts were measured with both Git’s status entries and Git’s exact untracked-file listing.

| Measurement | Before `.gitignore` update | After rule update, before staging this report | Change |
|---|---:|---:|---:|
| `git status --short` untracked entries | 291 | 310 | +19 visible entries |
| `git ls-files --others --exclude-standard` files | 23,541 | 880 | -22,661 files |

The apparent difference is expected: ignoring `desktop/target/`, `desktop/node_modules/`, `.next/`, `.cache/` and related rebuildable output removes tens of thousands of generated files, while removing broad database ignores makes the primary DBs, backups and 16 anomalous SQLite files visible again.

After this report is staged, the report itself is no longer counted as an untracked file. No local file was deleted.

## 4. Evidence / retention classification

| Object | Observed state | Classification | Handling in this pass |
|---|---|---|---|
| Active / local SQLite: `data/curis.sqlite`, `data/issue_pipeline.sqlite`, `data/quality.sqlite`, `data/b_layer_pending_decisions.sqlite`, `backend/data/curis.sqlite`, `backend/curis.sqlite`, `backend/curis_dev.db` | Multiple live or local databases, approximately 2 MB–2.1 MB each | **EVIDENCE REQUIRED**; keep local pending review | No ignore rule for primary DBs; no deletion or cleanup |
| DB backup: `backend/data/curis.sqlite.bak-20260806`, `data/curis.sqlite.bak-20260806` | Backup copies, approximately 1.1 MB / 1.6 MB | **ARCHIVE** pending provenance check | Remain visible; no deletion |
| 16 anomalous `<app.database.Database object at 0x...>` SQLite files | 16 root files, approximately 1.1 MB each | **DELETE CANDIDATE / EVIDENCE REQUIRED** | Broad ignore removed; files remain visible for review |
| `artifacts/` | Approximately 192 MB of screenshots / audit artifacts | **EVIDENCE REQUIRED** | Not ignored; retained for evidence review |
| `previews/` | HTML preview material | **EVIDENCE REQUIRED** | Not ignored; retained for review |
| `delivery/` | Generated delivery documents | **OWNER REVIEW** | Not ignored; no assumption that output is disposable |
| `desktop/` source and package inputs | Formal Desktop source, locks, icons, scripts and manifests | **OWNER REVIEW** | Root `desktop/` remains visible; only target/dependency/runtime output ignored |
| `desktop/target/` | Approximately 4.7 GB Rust build output | **KEEP LOCAL** | Now ignored; no source deletion |
| `desktop/node_modules/` | Approximately 29 MB dependency output | **KEEP LOCAL** | Now ignored; no source deletion |
| `desktop/.runtime/` | Approximately 742 MB recreated runtime packaging output | **KEEP LOCAL** | Existing ignore retained; no deletion |
| `desktop/runtime/__pycache__/` | Python bytecode cache | **KEEP LOCAL** | Explicitly ignored; no deletion |
| `.next/`, `.cache/`, `frontend/.cache/` | Rebuildable frontend / local cache output | **KEEP LOCAL** | Now ignored; no deletion |
| `.workbuddy/memory/` | Some tracked and some untracked local memory files | **OWNER REVIEW** | Not ignored or staged; preserve visibility and ownership review |
| `.workbuddy/output/` | Chinese design / research output documents | **EVIDENCE REQUIRED / OWNER REVIEW** | Not ignored; may contain source or evidence and must not be hidden |
| `.workbuddy/artifacts/`, `.workbuddy/tmp/`, `.workbuddy/build/` | Local generated WorkBuddy output | **KEEP LOCAL** | Existing narrow ignores retained |
| `curis-ui-prototype/` | Prototype source and previews | **EVIDENCE REQUIRED / OWNER REVIEW** | Not ignored; no assumption that it is disposable |
| `curis-ui-prototype.bak/` | Backup prototype tree | **DELETE CANDIDATE / EVIDENCE REQUIRED** | Remains visible; no deletion |

## 5. Explicit non-ignore boundaries

The following remain visible after the update:

- `backend/data/curis.sqlite`;
- primary databases under `data/` and `backend/`;
- DB backups;
- all 16 anomalous Database object SQLite files;
- `artifacts/`;
- `previews/`;
- `delivery/`;
- the `desktop/` source tree;
- `curis-ui-prototype/` and `curis-ui-prototype.bak/`;
- `.workbuddy/output/` and `.workbuddy/memory/`.

This is intentional. Visibility is required before deciding whether an object is evidence, an archive, a delete candidate or an owner-owned deliverable.

## 6. Validation

### `.gitignore` boundary checks

Passed:

- `desktop/target/` is ignored;
- `desktop/node_modules/` is ignored;
- `desktop/.runtime/` is ignored;
- `desktop/runtime/__pycache__/` is ignored;
- root `.next/` is ignored;
- root `.cache/` is ignored;
- `frontend/.cache/` is ignored;
- `.DS_Store` is ignored;
- SQLite WAL / SHM sidecars are ignored;
- primary SQLite files are not ignored;
- Database object files are not ignored;
- `artifacts/`, `previews/`, `delivery/`, Desktop source, prototypes and `.workbuddy/output/` are not ignored.

### Staging checks

The only staged paths are:

```text
.gitignore
docs/reviews/CURIS_REPOSITORY_HYGIENE_VALIDATION.md
```

`git diff --cached --check`: **PASS**.

No backend, frontend, issue, review, database, Desktop source, G2, G3 or Shared Runtime path is staged.

## 7. Remaining risks

- Active databases and their backups are now more visible, but their provenance and retention owner are unresolved.
- The 16 anomalous SQLite files may be disposable test residue, but deletion requires evidence review and is intentionally not automated.
- `artifacts/`, `previews/`, `delivery/`, packaged Desktop material and prototypes may contain formal evidence; they remain visible.
- `.workbuddy` contains both local generated output and tracked / potentially useful memory; no broad ignore rule was added.
- Existing tracked modifications in `AGENTS.md`, `.gitignore`, Current State, Pointer, Change Log and product documents remain outside this hygiene commit boundary.

## 8. Result

**REPOSITORY HYGIENE READY FOR COMMIT**

Ready means the `.gitignore` boundary and the validation report are precisely staged and checked. It does not mean this pass has committed, deleted or archived any local state.

Next step: Review the two staged paths, then commit only this repository-hygiene group if approved. G2/G3 and all evidence / retention decisions remain separate.
