# Curis Documentation Governance Phase 3-B1 Migration Report

Status: Review

Baseline:
main @ 4a8a0debbf8654c5c0dfd0fa20829406305213e4

Updated:
2026-07-30

---

## 1. Conclusion

Phase 3-B1 completed one reference-safe Markdown migration cohort.

- Files moved: 17
- Files deleted: 0
- Decision Records moved: 0
- Issue records moved: 0
- Review evidence moved: 0
- Business-code changes: 0
- Product-logic changes: 0

The two historical ADR files remain in `curis_workspace_blueprint/ADR/`.

## 2. Migration Map

| Old Path | New Path |
| --- | --- |
| `curis_workspace_blueprint/00-FOUNDATION/00-VISION.md` | `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/00-VISION.md` |
| `curis_workspace_blueprint/00-FOUNDATION/01-MISSION.md` | `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/01-MISSION.md` |
| `curis_workspace_blueprint/00-FOUNDATION/02-PRODUCT-PHILOSOPHY.md` | `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/02-PRODUCT-PHILOSOPHY.md` |
| `curis_workspace_blueprint/00-FOUNDATION/03-CORE-CONCEPTS.md` | `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/03-CORE-CONCEPTS.md` |
| `curis_workspace_blueprint/00-FOUNDATION/04-DESIGN-PRINCIPLES.md` | `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/04-DESIGN-PRINCIPLES.md` |
| `curis_workspace_blueprint/00-FOUNDATION/05-GLOSSARY.md` | `docs/99_Archive/curis_workspace_blueprint/00-FOUNDATION/05-GLOSSARY.md` |
| `curis_workspace_blueprint/01-ARCHITECTURE/00-SYSTEM-ARCHITECTURE.md` | `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/00-SYSTEM-ARCHITECTURE.md` |
| `curis_workspace_blueprint/01-ARCHITECTURE/01-DOMAIN-MODEL.md` | `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/01-DOMAIN-MODEL.md` |
| `curis_workspace_blueprint/01-ARCHITECTURE/02-CAPABILITY-ARCHITECTURE.md` | `docs/99_Archive/curis_workspace_blueprint/01-ARCHITECTURE/02-CAPABILITY-ARCHITECTURE.md` |
| `curis_workspace_blueprint/02-PRODUCT/00-PRODUCT-MODULES.md` | `docs/99_Archive/curis_workspace_blueprint/02-PRODUCT/00-PRODUCT-MODULES.md` |
| `curis_workspace_blueprint/02-PRODUCT/01-BUSINESS-PACKS.md` | `docs/99_Archive/curis_workspace_blueprint/02-PRODUCT/01-BUSINESS-PACKS.md` |
| `curis_workspace_blueprint/03-UX/00-INFORMATION-ARCHITECTURE.md` | `docs/99_Archive/curis_workspace_blueprint/03-UX/00-INFORMATION-ARCHITECTURE.md` |
| `curis_workspace_blueprint/03-UX/01-USER-FLOWS.md` | `docs/99_Archive/curis_workspace_blueprint/03-UX/01-USER-FLOWS.md` |
| `curis_workspace_blueprint/04-DEVELOPMENT/00-MVP-SCOPE.md` | `docs/99_Archive/curis_workspace_blueprint/04-DEVELOPMENT/00-MVP-SCOPE.md` |
| `curis_workspace_blueprint/04-DEVELOPMENT/01-SPRINT-PLAN.md` | `docs/99_Archive/curis_workspace_blueprint/04-DEVELOPMENT/01-SPRINT-PLAN.md` |
| `curis_workspace_blueprint/README.md` | `docs/99_Archive/curis_workspace_blueprint/README.md` |
| `curis_workspace_blueprint/RESEARCH/00-REFERENCE-PRODUCTS.md` | `docs/99_Archive/curis_workspace_blueprint/RESEARCH/00-REFERENCE-PRODUCTS.md` |

Git records these operations as renames; the Markdown content is preserved
except for reference corrections in the moved README.

## 3. Reference Audit

Checked before migration:

- Markdown links and path mentions
- `AGENTS.md`
- scripts and tests
- CI and configuration files

Results:

- AGENTS references to moved paths: 0
- script/test/CI/config references to moved paths: 0
- code references to moved paths: 0
- repository Markdown files requiring active path updates: 9
- moved README root references corrected: 5

`.workbuddy/memory/2026-07-07.md` retains one historical prose mention of the
old directory. It records old workspace state and is not an operational link;
Phase 3-B1 does not rewrite WorkBuddy Memory.

## 4. Reference Updates

Updated current and historical path references in:

- `docs/00_Context/DOCUMENT_INVENTORY.md`
- `docs/01_Product/Curis_Product_Context.md`
- `docs/02_Architecture/Curis_System_Architecture.md`
- `docs/04_Development/Curis_Development_Guide.md`
- `docs/Documentation_Governance_Phase3A_Report.md`
- `docs/Documentation_Governance_Report.md`
- `docs/pmo/source-control-baseline-freeze.md`
- `docs/standards/directory-structure.md`
- `shared/pmo/PROJECT_SPACE_MAP.md`

Governance state was synchronized in CURRENT_STATE, the migration plan, the
Archive index, Change Log and ADR-0039.

## 5. Inventory

The 17 inventory rows now use the archive paths and retain
`Status: Deprecated`. The two ADR rows keep their original paths.

After adding this report and ADR-0039:

- Total inventory entries: 1405
- Frozen: 343
- Review: 601
- Deprecated: 461

## 6. Risks

- One historical WorkBuddy prose mention remains intentionally unchanged.
- Several Review-status documents still describe the old blueprint as a
  historical cohort; they now use the archive and retained-ADR paths.
- No compatibility shim exists at the old non-ADR paths. This is acceptable
  because the audit found no code, script, test, CI or configuration consumer.
- Phase 3-B1 does not authorize another migration cohort.

## 7. Validation

- Moved-file count: PASS — 17 archive Markdown files and 2 retained ADR files
- Deprecated status coverage: PASS — all 17 archive files retain
  `Status: Deprecated`
- Inventory coverage: PASS — 1405 inventory rows and no missing listed path
- Old active-path references: PASS — none outside this migration map; one
  historical WorkBuddy prose mention remains intentionally unchanged
- Executable references: PASS — no AGENTS, code, script, test, CI or
  configuration reference
- Changed-file scope: PASS — Markdown only
- `git diff --check`: PASS
- `git diff --cached --check`: PASS
- untracked Markdown whitespace check: PASS

Product tests and builds are not required for this Markdown-only cohort because
the reference audit found no executable consumer.
