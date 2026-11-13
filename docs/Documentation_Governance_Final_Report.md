# Curis Documentation Governance Final Report

Status: Frozen

Baseline:
main @ eb6a4dd7ab766fa226c7163d081297c5edafdc82

Updated:
2026-07-30

---

## 1. Final Conclusion

Curis Documentation Governance is:

`Completed — v1.0`

The repository now has one current fact entry, four Frozen domain entries, an
explicit status model, searchable historical material, an auditable Archive,
classified residual assets and a bounded Agent reading path.

This report is contained by the final governance commit. The product-code
baseline remains `main @ c0e1855f446a55aa3a384006cfcfed9877130338`;
documentation-only commits after that baseline do not change product logic.

## 2. Governance Stage Completion

| Stage | Status | Result |
| --- | --- | --- |
| Phase 1 | Completed | Established Current State, status rules, Decisions, Change Log and the first governance inventory |
| Phase 2 | Completed | Established one Frozen entry each for Product, Architecture, Design and Development |
| Phase 3-A | Completed | Added explicit Deprecated status to 62 low-risk historical Markdown files |
| Phase 3-B1 | Completed | Migrated 17 safe historical Markdown files into `docs/99_Archive/` |
| Phase 3-B2 | Completed | Inventoried and classified 425 tracked assets and 44 ignored/generated locations |
| Phase 3-C1 | Completed | Migrated 200 Safe Move assets with a complete old/new path map |
| Phase 3-C2 | Completed | Reviewed 177 non-delete Human Confirmation assets: 160 Archive recommendations and 17 Protected records |
| Phase 3-C3 | Completed | Reviewed 41 Delete Candidates: 35 Safe Delete, 0 Keep and 6 Protected |
| Governance v1.0 | Completed | Removed the 35 approved assets, preserved protected state and finalized the knowledge baseline |

## 3. Final Document Statistics

Statistics are taken from
`docs/00_Context/DOCUMENT_INVENTORY.md` after finalization.

| Document Status | Count |
| --- | ---: |
| Frozen | 344 |
| Review | 606 |
| Draft | 0 |
| Deprecated | 454 |
| Total | 1404 |

| Governance Result | Count | Notes |
| --- | ---: | --- |
| Migrated | 217 | 17 Markdown files in Phase 3-B1 plus 200 assets in Phase 3-C1 |
| Archived under `docs/99_Archive/` | 217 | Same migration cohort; paths remain traceable through Git |
| Deleted | 35 | 8 tracked generated/redundant assets and 27 ignored temporary/generated records |
| Phase 3-C3 Protected | 6 | Current build, runtime or environment dependencies |
| Phase 3-C2 Protected | 17 | 16 WorkBuddy Memory records and one local release bundle |
| Phase 3-B2 Forbidden Move | 51 | Evidence, runtime data, worktrees, sensitive state and configured consumers |
| Total protected/forbidden records | 74 | Non-overlapping Phase 3-B2, 3-C2 and 3-C3 protection cohorts |

Tracked deletions remain recoverable from Git history. The 27 ignored records
were moved to the system Trash. No product source file, database, formal
acceptance evidence, Issue, Review or Decision record was deleted.

## 4. Explicitly Protected Delete Candidates

The following six paths must remain unchanged until their release conditions
in the Phase 3-C3 review are satisfied:

- `.venv/`
- `backend/.venv/`
- `frontend/.next/`
- `frontend/node_modules/`
- `frontend/ceo-evidence/node_modules/`
- `frontend/ceo-evidence/dist/assets/`

`frontend/.next/` and `frontend/node_modules/` were in use by the current Next
development runtime during the Phase 3-C3 audit.

## 5. Single Source Of Truth

The only current fact entry is:

`docs/00_Context/CURRENT_STATE.md`

Authority order:

1. `docs/00_Context/CURRENT_STATE.md`
2. Frozen Decisions in `docs/07_Decisions/`
3. the related Frozen domain entry
4. `docs/08_Change_Log/CHANGE_LOG.md`
5. the active Issue and Review
6. Review, Draft, Deprecated and archived historical material

Deprecated and Archive content remains searchable but cannot override a
Frozen current fact.

## 6. Agent Automatic Reading Path

Every new Agent starts with the minimum current context:

1. `docs/00_Context/CURRENT_STATE.md`
2. the relevant domain entry:
   - Product: `docs/01_Product/Curis_Product_Context.md`
   - Architecture: `docs/02_Architecture/Curis_System_Architecture.md`
   - Design: `docs/03_Design/Curis_Design_System.md`
   - Development: `docs/04_Development/Curis_Development_Guide.md`
3. the newest relevant entry in
   `docs/08_Change_Log/CHANGE_LOG.md`
4. only when implementation is authorized: the active Issue, its allowed
   files and the corresponding Review

Agents do not read all history by default. Deprecated or Archive material is
opened only for historical background, decision provenance or migration
analysis.

## 7. Final Validation

The finalization checks cover:

- Inventory rows: 1404
- Inventory paths present: 1404 / 1404
- Inventory status totals equal the row count
- Current authority and governance-document local paths resolve
- Local Markdown links checked: 1027 files, 0 broken paths
- Phase 3-C3 candidates classified: 41 / 41
- Approved Safe Delete actions executed: 35 / 35
- Tracked Safe Delete assets absent: 8 / 8
- Ignored Safe Delete residue may regenerate; `backend/selfuse.log` was
  recreated after deletion and remains ignored with no authority
- Protected paths present: 6 / 6
- Duplicate PNG retained copies verified before deletion: 6 / 6
- Curis Runtime stopped before final deletion verification
- `git diff --check`: pass
- Business-code changes: 0
- Configuration changes: 0
- Asset moves in finalization: 0
- Remote push: not performed

## 8. Remaining Risks

- The 160 Phase 3-C2 Archive recommendations remain at their current paths.
  Any later migration must move coherent packages and update every relative,
  Markdown, script/config and Agent reference atomically.
- WorkBuddy Memory may be consumed outside repository-visible references.
  Its 16 records remain protected until the tool owner provides a verified
  export or path-independent retention method.
- `deploy/curis/releases/` is ignored, locally stored and referenced by
  release scripts. It remains protected pending a release-owner decision.
- The six Phase 3-C3 dependency paths are reproducible but not currently safe
  to delete.
- Finder metadata, caches and runtime logs can regenerate after cleanup.
  Regeneration is not a governance regression because these paths remain
  ignored and carry no authority.
- Static reference scans cannot prove the absence of dynamically assembled
  paths.
- `.obsidian/` is user-local state outside Curis Documentation Governance and
  was not inspected, moved, deleted or committed.
- Project Delete remains `BLOCKED_PENDING_CONTRACT`; it is unrelated to
  documentation cleanup.

## 9. Maintenance Rules

- Update `CURRENT_STATE.md` whenever a current product or architecture fact
  changes.
- Record direction changes in a Frozen Decision before lower-authority
  documents adopt them.
- Add the newest Frozen change at the top of `CHANGE_LOG.md`.
- Give every core document one status: Draft, Review, Frozen or Deprecated.
- Keep one Frozen entry per domain; do not create competing current guides.
- Update `DOCUMENT_INVENTORY.md` when governed files are added, moved,
  archived or deleted.
- Run repository reference checks before every move, rename or deletion.
- Preserve formal evidence and historical decisions; archive rather than
  delete them.
- Keep Issue and Review scope explicit for business-code changes.
- Do not present Mock, prototype, local-only or experimental evidence as a
  completed product capability.
- Do not read all historical documentation by default.

## 10. Closure

Documentation Governance v1.0 is closed. Future work is ordinary maintenance
under the Frozen Current State, domain entries, status rules, Decisions and
Change Log rather than another bulk cleanup phase.
