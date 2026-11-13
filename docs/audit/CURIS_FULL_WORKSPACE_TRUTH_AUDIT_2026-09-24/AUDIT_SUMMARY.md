# CURIS Complete Workspace Inventory & Product Truth Audit — Summary

Status: **READY FOR CEO REVIEW — filesystem inventory complete; full product truth adjudication is incomplete and explicitly marked UNKNOWN where evidence was not reconciled.** No existing files were modified or removed; audit outputs are isolated here.

## Workspace Scale

- Directories: **57394**
- Files: **349311**; total bytes: **15781960075**
- File Manifest data rows: **349311** (header excluded)
- Root-level scattered files: **50**
- Semantic-readable files: **16801**
- Machine-generated/dependency files inventoried, semantic reads skipped: **324452** across **54179** machine directories
- Non-text/oversize files not content-parsed: **8058**
- Code-like files: **212498** (includes dependency/generated code); formal source files: **12302**; HTML: **985**; Markdown: **14668**; images: **2480**
- Exploration candidate documents: **870**; candidate/review heuristic files: **2740**
- Review/closure heuristic files: **4047**; authority markers: **110**; backlog candidates: **5629**
- UNKNOWN semantic-readable files: **741**; proven conflicts: **0**; CEO gates proven: **0**

Inventory is based on `os.walk` with symlink following disabled; all encountered file paths are recorded, including `.git`, dependencies, caches, worktrees and hidden directories. Manifest row count is the enumeration proof. Directories contain nested items, so directory file totals are recursive. Machine paths are not content-read. No files were left out of the file inventory; some non-text/large and machine-generated content was intentionally not semantically parsed.

## Current Product Truth

Current Pointer states the 2026-09-23 V1 Product Contract is frozen for Content Growth, Writing, Music; product exploration is closed; Runtime/Capability verification remains separate; release is BLOCKED.

## V1 Scope

Content Growth, Writing, Music. RD and E-commerce are outside V1.

## Authority

Product/design: `PRODUCT_DOCUMENT_POINTER.md` → Blueprint → Master Map / UI Blueprint → applicable Frozen Shared/Domain authority. Implementation: `CURRENT_STATE.md` → active Issue / Allowed Files → accepted implementation evidence → code/runtime.

## Product Freeze

Frozen per the Current Pointer (2026-09-23).

## Frontend Reality

59 Next.js route files and 170 other production-source candidates identified; feature-level Contract-to-source acceptance mapping remains UNKNOWN in this scan. HTML explorations are not formal implementation.

## Runtime Reality

391 backend/desktop source files identified; route/service/schema/test-level product mapping remains UNKNOWN pending scoped source adjudication.

## Biggest Confusion Sources

1. Generated/dependency files: 324452 files across 54179 machine directories (inventoried, semantic reads skipped).
2. Backlog / plan heuristic: 5629 files.
3. Review / closure heuristic: 4047 files.
4. Candidate / exploration heuristic: 2740 files.
5. Research heuristic: 1989 files.

Additional shape indicators: 985 HTML files, 39 screenshot-named directories, 84 exploration-named directories, and 50 root-level files. Heuristic categories reflect path/name/body markers and do not establish validity.

## Real Conflicts

0 verified conflicting Current/Frozen statements. Automated detection is conservative and source-by-source contradiction review remains incomplete; do not interpret 0 as a proof of no conflicts. CEO gates proven: 0.

## Cleanup Opportunity

Safely verified cleanup candidates: **0** from this audit; path-only candidates remain REVIEW_REQUIRED. Cleanup plan proposes risk-bounded phases; no cleanup executed.

## Exact Next Step

**CEO reviews this audit; then decides whether to authorize itemized cleanup or a bounded follow-up reconciliation.**

## Enumeration Coverage

- Root: `/Users/yy/Documents/Curis AI Workspace/`
- Traversed directories: 57394.
- Enumerated files / manifest rows: 349311 / 349311.
- Semantic-readable files scanned for names, markers, links, and classifications: 16801; product/topic and implementation registries are discovery indices, not complete per-topic source-to-authority adjudication.
- Unparsed: 8058 non-text or >2MB files; dependencies/generated paths excluded from semantic reads: 324452.
- Regular-file path omissions: none detected in the completed traversal. Directory symlink entries are inventoried; symlink targets are not followed by design.

## Core outputs

- `CURIS_WORKSPACE_FILE_MANIFEST.csv`
- `CURIS_WORKSPACE_DIRECTORY_MANIFEST.md`
- `CURIS_PRODUCT_FACT_SOURCE_REGISTRY.md`
- `CURIS_AUTHORITY_GRAPH.md`
- `CURIS_PRODUCT_TOPIC_REGISTRY.md`
- `CURIS_FRONTEND_REALITY.md`
- `CURIS_RUNTIME_REALITY.md`
- `CURIS_EXPLORATION_REGISTRY.md`
- `CURIS_DECISION_HISTORY_REGISTRY.md`
- `CURIS_BACKLOG_REGISTRY.md`
- `CURIS_PRODUCT_TRUTH_CONFLICT_REGISTER.md`
- `CURIS_WORKSPACE_CONFUSION_ANALYSIS.md`
- `CURIS_FILE_DISPOSITION_MATRIX.csv`
- `CURIS_V1_PRODUCT_TRUTH_MATRIX.md`
- `CURIS_CURRENT_ENTRYPOINT.md`
- `CURIS_WORKSPACE_CLEANUP_PLAN.md`
- `inventory_metrics.json`
- `build_audit.py`

