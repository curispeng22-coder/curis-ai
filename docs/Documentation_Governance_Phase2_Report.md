# Curis Documentation Governance Phase 2 Report

Status: Review

Baseline:
main @ c0e1855f

Updated:
2026-07-30

---

## 1. Conclusion

Phase 2 established one Frozen entry document for Product, Architecture, Design
and Development without moving or deleting existing files.

This phase changed documentation only. It did not modify business code,
product logic, APIs, database schema or runtime behavior.

## 2. New Frozen Entry Documents

| Domain | Unique Frozen Entry |
| --- | --- |
| Product | `docs/01_Product/Curis_Product_Context.md` |
| Architecture | `docs/02_Architecture/Curis_System_Architecture.md` |
| Design | `docs/03_Design/Curis_Design_System.md` |
| Development | `docs/04_Development/Curis_Development_Guide.md` |

Supporting governance decision:

- `docs/07_Decisions/ADR-0037-domain-frozen-entry-documents.md`

`docs/00_Context/CURRENT_STATE.md` remains the first current authority and now
registers all four entries.

## 3. Domain Authority

Each entry has the same authority model:

```text
CURRENT_STATE
→ one domain Frozen entry
→ current Frozen Decisions
→ latest Change Log
→ Issue / Review evidence
→ historical or Deprecated sources when needed
```

Older files remain searchable, but none is a second current domain entry.

## 4. Reference Relationships

| Domain | Current Effective Sources | Historical References | Deprecated Sources |
| --- | --- | --- | --- |
| Product | Current State; ADR-0033, ADR-0035, ADR-0036, ADR-0037 | existing product baseline and current integration/Assistant Reviews | old current-stage vision and Workspace blueprint |
| Architecture | Current State; ADR-0033, ADR-0034, ADR-0036, ADR-0037 | backend/Assistant architecture reports and integration Reviews | `knowledge/003_Architecture.md` and old Workspace blueprint architecture |
| Design | Current State; ADR-0033; ADR-0035; current Terra implementation | App Shell/Design System Issue and Reviews | old CEO Office archives/samples, UI v2 assets and static prototypes |
| Development | AGENTS; Current State; Status Rules; ADR-0034; ADR-0037; Change Log | PMO/team workflows and integration Reviews | old Workflow/Sprint and Workspace blueprint development plans |

Every entry contains a detailed `References` section. Deprecated UI sources are
listed only as an exclusion boundary; no current Design rule is derived from
them.

## 5. AGENTS Update

Removed project-irrelevant personal conversation rules.

Added Context Size Discipline:

1. Read `docs/00_Context/CURRENT_STATE.md`.
2. Read the related Frozen entry.
3. Read the newest relevant Change Log entry.
4. Read Deprecated or archived documents only when historical background,
   provenance or migration analysis is required.

Module routing now points directly to the four Frozen domain entries.

## 6. Governance Synchronization

Updated:

- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`
- `docs/00_Context/DOCUMENT_INVENTORY.md`
- `AGENTS.md`

The Inventory includes all Phase 2 documents and preserves the Phase 1
classification model.

## 7. Unprocessed Migration Items

The following work remains intentionally deferred:

- Moving existing Product, Architecture, Design or Development documents
- Bulk application of Status headers to historical documents
- Migrating old current-state files into `docs/99_Archive/`
- Archiving old UI exports, HTML prototypes, WorkBuddy material or Workspace
  blueprint files
- Resolving exact duplicate binary design exports
- Removing logs, caches or generated output
- Repairing references inside historical documents
- Deleting any file

Each future migration domain requires an explicit reference audit and separate
confirmation.

## 8. Phase Boundary

Phase 2 is complete at the documentation-entry level.

Phase 3 file migration has not started. No move, rename, archive operation or
deletion was executed.
