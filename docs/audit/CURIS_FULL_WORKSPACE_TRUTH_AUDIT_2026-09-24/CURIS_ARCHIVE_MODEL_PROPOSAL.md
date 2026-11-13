# Curis Archive Model Proposal

Status: Review  
Authority Class: REVIEW / PROPOSAL — CEO approval required

## Four retention destinations

| Destination | Keep here | Why |
|---|---|---|
| A. Active Repo | Current authorities, code, active backlogs/issues, accepted evidence directly routed by Pointer, uniquely needed product/business assets. | Default development input and durable product memory.
| B. Repo `docs/99_Archive/` | Small, canonical decision/ADR provenance and superseded authority text when traceability is needed by current authority or future maintainers. | Git history and references are useful; keep only material that benefits from local discovery.
| C. Workspace-external archive | Old design sources, full exploration sets, large screenshot/evidence batches, historical research not in current search route, and records with genuine restoration value. | Remove from active Codex search and repo/Git growth while retaining controlled recovery.
| D. Delete | Reproducible caches/dependencies after process and lockfile gates; exact duplicated exports; superseded transient artifacts with no unique information, once the Freeze retention rule is revised and a specific decision authorizes it. | No decision value remains; restore is unnecessary.

No whole-history policy. `docs/99_Archive/` is not a default dumping ground. If history adds no provenance or restoration value, classify Delete Candidate rather than Archive.

## External archive proposal (do not create in Part 3)

- Proposed root: a CEO-selected encrypted, backed-up volume mounted as `/Volumes/CurisArchive/`; the exact device/path is **UNVERIFIED** and requires approval. The Part 2 archive plan uses this as a placeholder target only.
- Naming: `Curis-Archive/YYYY-MM-DD/<family>/<set-id>/`; preserve original-relative path inside the set, never flatten duplicate names.
- Index per set: CSV/JSON manifest with Original Path, file path, SHA-256, size, source Modified date, Authority Class/Status where known, Archive Reason, Superseded By, Decision/Closure link, retention owner, restore condition, and archive date. No credentials, browser cookies, tokens, or sessions.
- Git: outside the active Git worktree; never a submodule or alternate Git worktree. Avoid committing large archives.
- Backup: encrypted volume plus one independent encrypted backup; periodically validate checksums and restore one sample set. Do not treat sync alone as backup.
- Restore: locate by indexed original path / set ID; restore into an authorized task workspace as `HISTORY`/`EVIDENCE`, never directly to current authority path; record a new restore event.

## Archive entry contract

Every set must record Archive Reason, Original Path, Date, Superseded By, Why Retained, Restore Condition, Owner, checksum, and CEO/owner gate. Part 2's 18 archive candidate files total **293,229 bytes**; this is a small initial cohort, not a mandate to move all historical research. Archive target is not created yet.

## Keep in repo at minimum

- Current Frozen Authority and its accepted replacement provenance.
- CEO decisions / ADRs needed to explain why current truth changed.
- Closures and minimum evidence explicitly referenced by a Current Authority or active gate.
- Required migration records and a compact archive index for any external set.

Raw HTML, export duplicates, all screenshots and full rejected prototypes are not automatically protected merely because decision history is protected. The CEO must revise Product Freeze §14 before deleting any historical Exploration/Candidate.
