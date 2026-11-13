# Workspace Cleanup CEO Gate

Status: PROPOSED — no Gate executed. Manifest baseline: 349,311 files / 57,394 directories / 15,781,960,075 bytes (15.781960 GB), snapshot 2026-09-24 03:43 Asia/Shanghai. Gate sizes below are apparent inventory bytes; later execution must establish a fresh Before baseline.

| Gate | CEO decision | Files | Dirs | GB | Risk | Reversible? | Expected result |
|---|---|---:|---:|---:|---|---|---|
| 0 Retention Authority | Approve narrow §14 revision? | 1 authority | 0 | n/a | high; changes frozen historical-retention policy | Yes, via authority revision history | Preserve decisions/provenance while allowing only fully proven artifact deletion. |
| 1 Governance | Approve two-authority model (`AGENTS.md` + `DOCUMENT_STATUS_RULES.md`)? | 2 authorities | 0 | n/a | medium; conflicting governance instructions if promotion is partial | Yes, revert exact authority issue | One governance route; proposals remain review evidence; no third policy. |
| 2 Safe Generated | Approve exact generated cleanup CSV? | 1,008 | 25 | 0.023153 | low after checks; exact bytecode/test caches only | Yes, regenerate | Remove only enumerated `.pyc`/`.pytest_cache` files and empty dirs. |
| 3 Conditional Generated | Approve after exact process/package gates? | 231,614 | 41,054 | 4.384012 | medium; active dependencies/build outputs and physical dedupe uncertainty | Yes if lockfile rebuild succeeds; apparent bytes may exceed physical release | Remove only exact root sets, keep all parent source/worktrees. |
| 4 Exploration | Approve historical deletion? | 0 eligible; 883 held | set-level | 0 eligible; 0.206 potential held | high; currently zero eligible, 883 candidates held | Tracked: Git history; untracked: maybe irreversible | Current matrix yields zero executable rows until scope, unique-source/evidence and untracked checks pass. |
| 5 Archive | Approve external destination and exact Writing set? | 18 | set-level | 0.000293 | medium; external destination and links/backup need approval | Yes, Move Back with checksum | Move exact 18 files outside Active Workspace after destination/backup/link checks. |
| 6 Root/Documents | Approve root disposition plan? | 50 | 0 | 0.021864 | medium; root docs may have inbound refs; all moves gated | Moves reversible; `.DS_Store` regenerable | Proposal: 5 KEEP, 16 MOVE, 1 DELETE, 28 REVIEW_REQUIRED. Current Document Set stays 36 NO_MOVE. |
| Worktree | Delete worktrees? | 0 approved | n/a | 0 approved | High / uncommitted and unique commits | Not assumed reversible | **No. 17 present remain blocked; 5 missing metadata rows reviewed separately.** |

## Exact CEO decisions needed

1. Gate 0: approve or reject the narrow §14 rule; this is a prerequisite to any historical Exploration deletion.
2. Gate 1: approve exactly two governance authorities and the formal Current Entrypoint location.
3. Gate 2: approve exact safe generated files after current-file/process prechecks.
4. Gate 3: approve exact conditional roots only after owner identifies/stops relevant processes and confirms rebuild method; `desktop/node_modules` remains blocked pending package-manager choice.
5. Gate 4: **no files are presently eligible**. Decide only after the 883 Part 2 candidate rows have complete replacement-scope, evidence, source, current-reference and untracked-work proof.
6. Gate 5: approve an actual external archive volume, independent backup/restore check, and exact checksummed Writing archive set. `/Volumes/CurisArchive/` is a placeholder, not verified.
7. Gate 6: approve root disposition; move rows require targeted inbound-link scan and destination by class.

No authority, pointer, code, worktree, archive, or cleanup action is executed by this package.
