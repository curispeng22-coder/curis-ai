# Physical Cleanup Execution Plan (Non-Executable)

Status: Review / no commands executed. This plan has no shell script and contains no wildcard or broad recursive delete command. CSVs are execution manifests, not authorization. Run one gate at a time only after its approval.

## Order and stop rules

1. **Gate 0 Authority Revision:** create a formal scoped issue; CEO approves the exact §14 change. Change only §14 plus necessary Pointer, Change Log and Governance references. Review exact diff and links.
2. **Gate 1 Governance Promotion:** only after CEO acceptance. Use two authorities: `AGENTS.md` and `docs/00_Context/DOCUMENT_STATUS_RULES.md`. Incorporate accepted clauses; reconcile supersession map; formally create the navigation-only entrypoint at `docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md`. Do not activate a third Authority.
3. **Before Gate 2:** take a fresh inventory and Git status baseline; confirm each file in Gate 2 still exists, remains exact regenerable data, has no active owner process and is not a sensitive/user-data path. Remove listed files individually; remove only directories that are empty. Rerun focused import/test-cache checks.
4. **Gate 3:** stop only the process whose exact working directory uses the listed root, with its owner. Confirm no process holds the root; verify source and lockfile; block `desktop/node_modules` until the package manager is resolved. Remove listed roots only, never their parent checkout. Reinstall/build per CSV, run targeted runtime/build checks, then inspect Git status. Apparent sizes may not equal released disk blocks due to hardlinks/store dedupe.
5. **Gate 4:** current eligible set is zero. Do not execute until every candidate has complete set ID, lawful successor/date, full/partial replacement scope, unique-source/evidence proof, Current Authority reference proof, current Git state, retained Decision Record/minimal evidence, and exact owner/CEO approval. Any untracked code/source must be preserved or separately archived before deletion. Delete complete set IDs atomically; never leave orphan HTML/CSS/JS/assets/screenshots.
6. **Gate 5:** approve a real destination outside this workspace and its backup/restore design. Verify source SHA-256 and size against Gate 5 CSV immediately before copy; copy preserving relative paths, verify target checksums, then only after a second approval remove source copies individually. Update links only when the targeted scan finds them. Archive remains in place if target or backup validation fails.
7. **Gate 6:** current documents are 36 NO_MOVE. Root MOVE rows need reference scan, class destination and owner; `DELETE` applies only to exact `.DS_Store` after confirmation. Update references before moving; one exact path at a time. No broad root cleanup.
8. **Worktrees:** excluded. Do not remove or prune any of the 17 present worktrees or 5 metadata entries in this package.
9. **Gate 7 final validation:** capture fresh After inventory and compare actual files/directories/apparent bytes with fresh Before. Run `git status --short`, `git diff --check`, Pointer/Authority/Entrypoint/Backlog link checks, accepted HTML reference existence, and appropriate frontend/runtime build checks. Review every unexpected diff or missing link and roll back the last gate if validation fails. Record actual removed files/dirs and reclaimed bytes; do not reuse Manifest projections as the After measurement.

## Current quantified projection

Part 3 manifest snapshot: 349,311 files / 57,394 dirs / 15,781,960,075 bytes. Gate 2: 1,008 files / 25 dirs / 23,153,022 B. Gate 3: 231,614 file observations / 41,054 descendant dirs / 4,384,012,303 apparent B. Gate 4: 0 eligible; 883 historical candidate rows / 206,110,003 B held. Gate 5: 18 files / 293,229 B to external archive, not destroyed.

If Gates 2, 3 and 5 all pass, the manifest-based projected active size is **11,374,501,521 B (11.374502 GB)** before Gate 6 root-internal moves and with Gate 4 held. Actual After size must be measured.

## Rollback and ledger

Gate 2/3: rebuild only using exact commands/lockfiles in manifests. Gate 5: restore exact paths from verified archive. Gate 6: move files back from recorded original paths. Gate 4: tracked files may be restored from Git only if present in history; untracked deletions are IRREVERSIBLE unless archived first, so they remain ineligible without a recorded recovery decision. After each approved gate, append a completed entry to `CURIS_CLEANUP_LEDGER.md`; the provided file is a template only.
