# Active SQLite Guard Repair Evidence

**Status:** Review
**Issue:** `WORKSPACE-ENGINEERING-P0-001`
**Date:** 2026-08-16

## Pre-repair fact

Active database: `/Users/yy/Documents/Curis AI Workspace/data/curis.sqlite`

- size: `1232896` bytes
- byte SHA-256: `a5051402114c2ee60523a232d4468c02d7f7dd61c0295c6d288c2b79c1c0ea0f`
- `pragma integrity_check`: `ok`
- `pragma foreign_key_check`: empty
- no process held the database during backup or repair

The following tables matched the P0 DDL and each contained zero rows:

| Table | Recorded schema role | Rows |
| --- | --- | ---: |
| `installed_workspace_packages` | Package/version/digest/provenance Registry | 0 |
| `workspace_package_instances` | Company/Workspace instance version pin | 0 |
| `workspace_package_objects` | Scoped generic Package domain object | 0 |
| `workspace_package_activities` | Core action activity | 0 |

Their complete `sqlite_master.sql` definitions were captured in the execution evidence before repair and matched `backend/app/workspace_package_runtime.py`.

## Backup

SQLite online backup:

`/Users/yy/Documents/Curis AI Workspace/data/backups/curis-before-workspace-p0-guard-repair-20260816.sqlite`

- size: `1232896` bytes
- byte SHA-256: `ad350ba0a5634d0b75c3c4ef48ea1db23ccae620f603e7bbaf5e88109d2253ba`
- `pragma integrity_check`: `ok`
- `pragma foreign_key_check`: empty

## Bounded repair

One `BEGIN IMMEDIATE` transaction revalidated the exact expected columns and zero rows, then dropped only:

1. `workspace_package_activities`
2. `workspace_package_objects`
3. `workspace_package_instances`
4. `installed_workspace_packages`

Before and after the transaction, every non-target `sqlite_master` entry and every value in all non-target tables was hashed deterministically.

- non-target schema SHA-256: `91e6b246db77ac3d4ceed03c81d03d9548f54c2989be9e101efeef4a8b0a133c`
- non-target data SHA-256: `05a671d8030e0dcbf6b96c4cb2b4a19c740947f18b6157ef32e4c0342e645b39`
- compared non-target tables: `96`
- compared non-target rows: `391`

Both fingerprints and counts were identical before and after commit.

## Post-repair fact

- four target tables present: `0`
- `pragma integrity_check`: `ok`
- `pragma foreign_key_check`: empty
- post-repair byte SHA-256: `c838f41deaf643b6a0ef55aa63b7467dbaaf9bb6d3a0e5a425e3d459f7ca53f0`

The original byte hash is not restored and must never be reported as restored. This evidence proves only bounded logical repair and non-target logical equivalence.
