# Workspace Root Allowlist Proposal

Status: Review  
Authority Class: REVIEW  
Baseline: `78cacbd0857cc36c9f3fe0e4b11346489993b728`  
Updated: 2026-09-24  
Disposition: AUDIT / PROPOSAL — NON-AUTHORITATIVE; CEO review required.

## Root inventory result

The existing Manifest contains **50 root-level file entries**. This table classifies each one; `MOVE` and `DELETE_CANDIDATE` are proposals only. No paths were altered. An allowlist is a write gate: future work may create root-level files only from the KEEP set, or an exact Issue must grant a named exception.

## Proposed root allowlist

Allowed by default: `AGENTS.md`, `README.md`, `.gitignore`, `.dockerignore`, `skills-lock.json`; root-level build/config/source entry files only when they are actively consumed. `AGENT.md` is not auto-allowed because it duplicates agent routing and requires reconciliation. The default entry remains the existing PRODUCT_DOCUMENT_POINTER; the audit-only CURIS_CURRENT_ENTRYPOINT is not a new permanent authority route. Do not introduce another root Current file.

| Root file | Type | Bytes | Git status in Manifest | Manifest class | Disposition | Reason / proposed target |
|---|---|---:|---|---|---|---|
| `AGENT.md` | .md | 164 | tracked clean | UNKNOWN | REVIEW_REQUIRED | Potential duplicate/stale entry or routing artifact; compare explicit Current authority and references before disposition. |
| `skills-lock.json` | .json | 3,268 | tracked clean | UNKNOWN | KEEP | Required repository instruction / entry / configuration file. |
| `Curis-Professional-Workspace-Operating-Reconciliation-CEO-Review.md` | .md | 5,753 | ?? | CLOSURE / REVIEW EVIDENCE | REVIEW_REQUIRED | No safe class inferred from path alone. |
| `PROJECT_STATUS.md` | .md | 13,083 | tracked clean | SUPERSEDED | REVIEW_REQUIRED | Potential duplicate/stale entry or routing artifact; compare explicit Current authority and references before disposition. |
| `overview.md` | .md | 3,346 | ?? | CANDIDATE / REVIEW | REVIEW_REQUIRED | No safe class inferred from path alone. |
| `.DS_Store` | [no extension] | 55,300 | untracked or ignored (not in tracked/status maps) | TEMPORARY / GENERATED | DELETE_CANDIDATE | OS-generated directory metadata; safe only after exact-path and local-user check. |
| `Talent_Market_Product_Map.md` | .md | 7,575 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `<app.database.Database object at 0x10e6274d0>` | .database object at 0x10e6274d0> | 1,306,624 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `CURIS_FIGMA_MAKE_INPUT_MANIFEST.md` | .md | 12,872 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `<app.database.Database object at 0x10f54fd90>` | .database object at 0x10f54fd90> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `HANDOFF_DESIGN_AUTHORITY_2026-08-17.md` | .md | 10,620 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `<app.database.Database object at 0x10173d220>` | .database object at 0x10173d220> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `CONTENT_GROWTH_INDEPENDENT_RED_TEAM_REVIEW.md` | .md | 40,999 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `build_rd_pages.py` | .py | 25,451 | ?? | BACKLOG / PLAN | REVIEW_REQUIRED | Verify active consumer and ownership before allowing a helper in repository root. |
| `Curis_Product_Rethink_Reasoning.md` | .md | 47,757 | ?? | UNKNOWN | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `CURIS_FIRST_RUN_AND_BUSINESS_ENTRY_MODEL.md` | .md | 16,108 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `.tmp-fix-shell-common.mjs` | .mjs | 7,486 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Temporary-looking source file; check references and tracked/dirty ownership before proposed removal. |
| `CONTENT_GROWTH_INDEPENDENT_RED_TEAM_SECOND_PASS.md` | .md | 13,959 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `<app.database.Database object at 0x10ec85e00>` | .database object at 0x10ec85e00> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `CURIS_XHS_INTERACTIVE_PROTOTYPE_FROZEN_COMPLIANCE_AUDIT.md` | .md | 60,367 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `rebuild_rd_default.py` | .py | 16,954 | ?? | CANDIDATE / REVIEW | REVIEW_REQUIRED | Verify active consumer and ownership before allowing a helper in repository root. |
| `README.md` | .md | 863 | tracked clean | CURRENT / FROZEN AUTHORITY | KEEP | Required repository instruction / entry / configuration file. |
| `TASKS.md` | .md | 4,814 | tracked clean | SUPERSEDED | REVIEW_REQUIRED | Potential duplicate/stale entry or routing artifact; compare explicit Current authority and references before disposition. |
| `<app.database.Database object at 0x10a4196d0>` | .database object at 0x10a4196d0> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `.dockerignore` | [no extension] | 432 | tracked clean | TEMPORARY / GENERATED | KEEP | Required repository instruction / entry / configuration file. |
| `<app.database.Database object at 0x10b57da90>` | .database object at 0x10b57da90> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `Talent_Market_Integration_Contract.md` | .md | 10,058 | ?? | CANDIDATE / REVIEW | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `<app.database.Database object at 0x10fbff6b0>` | .database object at 0x10fbff6b0> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `<app.database.Database object at 0x10f052620>` | .database object at 0x10f052620> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `.gitignore` | [no extension] | 1,083 | tracked clean | TEMPORARY / GENERATED | KEEP | Required repository instruction / entry / configuration file. |
| `Curis_Page_Map_v1.0.md` | .md | 91,327 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `CURIS_FIGMA_MAKE_CURRENT_DESIGN_CONTEXT_PACK.md` | .md | 6,767 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `CONTENT_GROWTH_FINAL_PRE_IA_RED_TEAM_VERIFICATION.md` | .md | 12,826 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `<app.database.Database object at 0x10cf144b0>` | .database object at 0x10cf144b0> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `reproduce_rd_baseline_v1.py` | .py | 22,230 | ?? | CANDIDATE / REVIEW | REVIEW_REQUIRED | Verify active consumer and ownership before allowing a helper in repository root. |
| `<app.database.Database object at 0x10fbfea80>` | .database object at 0x10fbfea80> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `<app.database.Database object at 0x10f6b9a90>` | .database object at 0x10f6b9a90> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `<app.database.Database object at 0x10a41b660>` | .database object at 0x10a41b660> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `<app.database.Database object at 0x10e334460>` | .database object at 0x10e334460> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `CURIS_VISUAL_DESIGN_CHATGPT_HANDOFF_PACK.md` | .md | 21,938 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `Curis_Product_Master_Map_v2.0.md` | .md | 114,595 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `AGENTS.md` | .md | 5,558 | tracked clean | CURRENT / FROZEN AUTHORITY | KEEP | Required repository instruction / entry / configuration file. |
| `PROJECT_HANDOFF.md` | .md | 17,221 | tracked clean | CLOSURE / REVIEW EVIDENCE | REVIEW_REQUIRED | Potential duplicate/stale entry or routing artifact; compare explicit Current authority and references before disposition. |
| `CURIS_PRODUCT_REALITY_ALIGNMENT.md` | .md | 37,307 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `<app.database.Database object at 0x10bda4a50>` | .database object at 0x10bda4a50> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `<app.database.Database object at 0x10ec001e0>` | .database object at 0x10ec001e0> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `Talent_Market_Resource_Audit.md` | .md | 16,412 | ?? | CLOSURE / REVIEW EVIDENCE | MOVE | Non-root product/research/review artifact; proposed destination by class under docs/, subject to inbound-reference and Authority check. |
| `<app.database.Database object at 0x10e627700>` | .database object at 0x10e627700> | 1,306,624 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `<app.database.Database object at 0x10df8fac0>` | .database object at 0x10df8fac0> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |
| `<app.database.Database object at 0x10b57e990>` | .database object at 0x10b57e990> | 1,159,168 | ?? | TEMPORARY / GENERATED | REVIEW_REQUIRED | Database-looking artifact with content/data-loss risk; identify producer, consumer and integrity before any handling. |

## Root write rule (proposal)

- KEEP files are the root allowlist. Build/package configuration and actual application entry scripts may stay only when a repository consumer is verified.
- New research, review, candidate, HTML, screenshots, reports, backlog, audit and temporary evidence go to `artifacts/tasks/<TASK-ID>/` while active, then are promoted to their governed docs class or given an explicit archive/delete disposition.
- Root files marked MOVE, DELETE_CANDIDATE or REVIEW_REQUIRED need a later exact-path proposal with reference, Git status, data-risk and Owner evidence. Nothing in this audit authorizes action.
