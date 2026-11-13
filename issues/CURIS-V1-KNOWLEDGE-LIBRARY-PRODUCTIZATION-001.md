# CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001

Status: Review
Authority Class: CURRENT IMPLEMENTATION ISSUE
Date: 2026-09-01
Owner: Main Development Session
Implementation Status: IMPLEMENTED / ACCEPTED CANDIDATE

## Goal

将已接受的资料库 Product / UX / Figma 结构接到 Curis 现有 Knowledge、Context、Work、Result、Evidence、Artifact 与 canonical Company / Business / Workspace truth；保持“引用而非复制、来源可追溯、未知不虚构”，不创建第二套 Knowledge、Citation 或 Context 系统。

## Authority

- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCT_UX_ACCEPTANCE.md`
- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_UI_ACCEPTANCE.md`
- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCT_UX_RESEARCH.md`（Research only）
- Current Product Blueprint / UI Blueprint / `docs/00_Context/CURRENT_STATE.md`
- Current Knowledge / Context / Work / Execution / Result / Evidence / Artifact implementation
- Figma `2Fh7DgPPfLgdbvNtnzPnk9`: `187:2`, `187:276`, `187:550`, `187:824`

Figma只授权产品结构、层级、状态与交互方向，不是生产数据或 Runtime truth。

## Pre-change Inventory

HEAD: `c797db840bad285d7e9f1962d06eac61aa28508b`

| Path | SHA-256 | Ownership / current decision |
|---|---|---|
| `backend/app/knowledge_service.py` | `bc038085801eff6c1d29481561d543007d2445c787594dd5eca5332189b2e7c5` | Current Knowledge write/read authority; clean; reuse/extend only after architecture gate. |
| `backend/app/context_service.py` | `06ba08a922f45cf0d2a3e4dc32aadb61237bbe9c25654736b0b81924ac9ed15a` | Current bounded legacy Task context assembler; unchanged. General Workspace continues through its accepted bounded context seam. |
| `backend/app/database.py` | `2f19b439fa8083f968b463ecb8635fdc3e11d82707ee6188d07c1b0ff7c67d2d` | Mixed source; only the exact Knowledge columns, generic typed-reference table, indexes and delete guard described below are owned. |
| `backend/app/api/team_operating_router.py` | `883cf8719a7629ed46d31a43fa18942fc08c815e5b02f84440b1d55d86ab05be` | Mixed source; only General Work bounded Knowledge resolution/prompt projection hunks are owned. |
| `backend/app/main.py` | `f0df46a54ea1188afb47aff46aef0e88ff7156d45070959655232bd102ef7a81` | Mixed source; only Knowledge request models and `/api/knowledge/*` route hunks are owned. |
| `frontend/app/ceo-office/knowledge/page.js` | `b01796b7f769f965bf1ecef8781518175170d5ea0770e955f768c8d217c1951e` | Legacy current page; clean; accepted UI supersedes its product composition after the gate. |
| `frontend/app/ceo-office/knowledge/entries/[id]/page.js` | `30d894148708086e06f41e8e463e765a358e307e25184193db7e75ebf3b8677f` | Legacy detail; clean; reading-first reconstruction required after the gate. |
| `frontend/lib/knowledge.js` | `c73036c30724c2e8b1d31c2cacd00f3e41362702b0ef7a12221772a6d86bb4fc` | Current Knowledge client; clean; reuse/extend after the gate. |

The repository contains unrelated preserved staged/unstaged/untracked work. No reset, clean, broad staging, commit or push is authorized.

## Milestone 1 Audit

| Area | Decision | Current truth |
|---|---|---|
| `knowledge_service.py` | KEEP + EXTEND | Real manual entries and local `.md/.txt` imports; source path/hash/timestamps, tenant isolation and bounded text search exist. Scope is only Company/legacy Project/Department. |
| `context_service.py` | KEEP + REWIRE | Bounded context and up to three relevant Knowledge snapshots exist. Selection is legacy Project/Department-based and is not a canonical Work-selected reference contract. |
| `knowledge_entries` | BLOCKED | No canonical `business_id` or `workspace_id`; Project/Department cannot impersonate them. |
| `context_packages` | KEEP | Existing snapshot/evidence of context assembly; not a Knowledge relation write authority and not a reverse-reference index. |
| Work `inputRefs` / selected refs | PARTIAL | A Work may persist opaque refs, but Knowledge refs are not scope-validated, resolved or hydrated by the current resolver. |
| `runtime_links` | KEEP, NOT APPLICABLE | It only links resolvable Runtime entities. Knowledge, canonical Business and Workspace are not all legal `RuntimeFoundation` entities; direct inserts would bypass the contract. |
| Result / Evidence / Artifact refs | KEEP | Existing canonical output/evidence truth is reusable, but there is no validated Knowledge reverse-use relation. |
| Knowledge overview frontend | SUPERSEDED | Current card/dashboard and legacy scope semantics do not match the accepted Company Reference Space. |
| Knowledge detail frontend | SUPERSEDED | Current detail exposes IDs/hash by default and lacks reading-first source/use layers. |
| Browse / picker / return state | MISSING | No canonical Business/Workspace filters, bounded pagination contract, validated Work picker, or return-state contract. |

## Resolved Architecture Gate

The accepted product requires all three facts below to be true together:

1. A Knowledge entry has a verifiable canonical Company / Business / Workspace scope.
2. A Work-selected Knowledge reference is tenant/company/scope validated and is actually consumed through the existing bounded Context path.
3. The same persisted reference can be read in reverse as “used by Work / Result” without copying the Knowledge body or creating a second truth.

The previous implementation could not express this contract safely:

- `knowledge_entries` has no canonical Business/Workspace relation.
- `runtime_links` cannot legally link these non-uniform entity types through `RuntimeFoundation`.
- Work `inputRefs` accepts opaque references but does not validate or hydrate Knowledge.
- `context_packages.relevant_knowledge_json` is a derived snapshot, not the canonical user-selected relation.

Implementing the Figma now would require at least one prohibited shortcut: treating Project as Business, encoding scope in tags/JSON, directly bypassing `RuntimeFoundation`, or creating a second Citation/Knowledge relation store.

The gate is resolved by the accepted canonical scope and typed reference contracts:

- `docs/reviews/CURIS_KNOWLEDGE_CANONICAL_SCOPE_TYPED_WORK_REFERENCE_CONTRACT.md`
- `docs/reviews/CURIS_KNOWLEDGE_FUTURE_COMPATIBILITY_REVIEW.md`

Implementation is now authorized to add the smallest schema-stable contract: canonical Knowledge scope on the existing `knowledge_entries` table and one generic typed-reference relation. No parallel Knowledge, Citation, Context or Work system is authorized.

## Allowed Files — Bounded Implementation

- `backend/app/database.py` — exact Knowledge columns, generic typed-reference table, indexes and hard-delete guard only.
- `backend/app/knowledge_service.py` — canonical scope, search/batch reads, typed Work references, reverse projections and archive behavior.
- `backend/app/api/team_operating_router.py` — exact General Work bounded Knowledge context seam only.
- `backend/app/main.py` — exact Knowledge request models and routes only.
- `frontend/app/ceo-office/knowledge/page.js` — accepted Overview / Browse / Work picker surface.
- `frontend/app/ceo-office/knowledge/entries/[id]/page.js` — accepted reading-first detail.
- `frontend/lib/knowledge.js` — Knowledge API client only.
- `frontend/components/v1/GeneralWorkspaceOperating.js` — exact existing-Work → Knowledge picker entry and return path only; no conversation, execution or Workspace redesign.
- `backend/tests/test_v1_knowledge_library_productization.py` — isolated canonical scope/reference/context/restart/failure tests.
- `backend/tests/test_mvp_phase5_s10_knowledge_management.py` — migrate only the superseded Project-scope frontend assertion to the accepted canonical target/reference contract.
- `frontend/tests/knowledgeLibraryProductization.test.mjs` — product-surface contract regression.
- `issues/CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001.md`
- `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCTIZATION_REVIEW.md`

No other production, governance, authority, active-database, Desktop source or package file is allowed. Mixed-source files are owned only at the named semantic hunks; an overlapping change is a stop gate.

2026-09-01 acceptance amendment: packaged Desktop exposed that the accepted picker route had no originating Work entry because the existing composer control has no persisted Work identity. The bounded fix adds one reference action to each persisted Work card, carrying only `work_ref` and the current Workspace return path. This amendment is required by Acceptance 5 and does not alter Shared Conversation or Runtime semantics.

## 2026-09-01 Canonical Scope + Typed Work Reference Contract

**ACCEPTED / BOUNDED IMPLEMENTATION AUTHORIZED**

The candidate contract is recorded at `docs/reviews/CURIS_KNOWLEDGE_CANONICAL_SCOPE_TYPED_WORK_REFERENCE_CONTRACT.md` for CEO / Architecture review. It proposes the smallest reuse-first direction:

- explicit canonical Company / Business / Workspace `target_type + target_ref` scope;
- legacy `project_id` / `department_id` retained only as legacy / migration input / compatibility read, never Project-as-Business;
- typed Work → Knowledge semantics (`knowledge:<id>` candidate) through the existing Work reference and bounded Context path;
- reverse Used By from that same relation, with Result / Evidence reached through Work, not a second relation store;
- explicit Work refs first, then bounded legal automatic retrieval; no Context V2;
- non-destructive, no-guess migration and hard-delete protection for referenced Knowledge;
- **BOUNDED SCHEMA EXTENSION — REVIEW REQUIRED**, with no schema, Runtime, DB, UI or migration work authorized here.

The CEO / Architecture gate is closed. This Issue records exact implementation files, migration rules, isolated tests and stop gates before production changes begin.

## Runtime / Migration Scope

The bounded implementation extends existing truths, not a parallel system:

- Extend `knowledge_entries` with `company_id`, canonical `target_type + target_ref`, lifecycle/archive metadata and target indexes. Existing legacy Project/Department fields remain compatibility-only and are never guessed into canonical scope.
- Add one generic typed relation with source type/ref, relation, target type/ref and tenant/company/workspace ownership. `WORK --USES_REFERENCE--> KNOWLEDGE` is the first consumer, not a Work-private relation system.
- Teach the accepted General Workspace bounded Context seam to read explicit Work references first, then bounded legal automatic retrieval; no whole-library hydration and no Context V2.
- Derive reverse Work use from the same persisted relation and related Result/Evidence/Artifact through existing Work output truth. No direct Knowledge→Result relation is added.
- Archive referenced Knowledge; a database guard rejects hard deletion while references exist. Archived material remains resolvable for historical provenance but cannot be newly selected.
- Rebuild only the accepted overview, browse, detail and picker surfaces over that contract.

Fresh databases receive the full schema. Existing databases receive only additive nullable/defaulted columns and idempotent tables/indexes/triggers. No active database is initialized or migrated; all migration evidence uses repository-external isolated SQLite.

## Stop Gates

- A required change falls outside Allowed Files or overlaps an unowned mixed-source hunk.
- Canonical Company→Business→Workspace lineage cannot be verified without guessing.
- The accepted single typed-reference truth is insufficient and a second relation/citation store would be required.
- Migration would rewrite ambiguous legacy scope or operate on either repository active SQLite.
- Browser/Desktop acceptance requires a Desktop source change rather than rebuilding current accepted sources.

## Acceptance After Gate Resolution

1. Company / Business / Workspace scopes come only from canonical identities.
2. Manual and `.md/.txt` source truth remains traceable; unsupported formats remain unavailable.
3. Search, filters and 30–50 row bounded batches operate on real records.
4. Detail remains reading-first; IDs/hash are advanced evidence only.
5. Work picker persists a validated reference and returns to the originating Work.
6. Provider/Employee Context consumes only selected, bounded references; no whole-library hydration.
7. Reverse Work/Result use is durable and truthful; no inferred relation.
8. Cross-tenant/company/business/workspace references fail closed.
9. Restart preserves entries, scopes, references, search state and reverse projection.
10. Browser and packaged Desktop cover overview, browse, detail, picker, return and error/empty states.

## DB Safety

All future Runtime tests must use repository-external isolated SQLite with the three-variable fail-fast guard.

Pre-change active DB fingerprints:

- `data/curis.sqlite`: size `1232896`, mtime `1786873339`, SHA-256 `2ea2506f90f764e834d47d8f6bae3cb41c22d457757e0e9216c0ae8c39a39ec6`, integrity `ok`
- `backend/data/curis.sqlite`: size `1277952`, mtime `1786783659`, SHA-256 `a9d96a9536a5bce3b3b30f912e86a37f61d28527a8eb2d35af7a5857d29414e4`, integrity `ok`

## Explicit Exclusions

- Second Knowledge, Citation, Context, RAG or Reference database
- Project-as-Business or free-form canonical scope
- Direct `runtime_links` writes that bypass `RuntimeFoundation`
- PDF/DOCX/web/external connector claims without implementation evidence
- Whole Workspace/Conversation/History/Knowledge hydration
- Product/Figma redesign, Authority changes, UI fixture production data
- Active DB initialization/migration/write
- Parallel governance document overwrite
- Commit or push

## Current State

**IMPLEMENTED / ACCEPTED CANDIDATE**

The accepted canonical scope, typed Work reference, bounded Context, reverse projection, archive guard and Figma-derived product surfaces are implemented. Isolated Runtime, 105-entry scale, failure, Browser, fresh packaged Desktop, exact Work return, full sidecar exit/restart and no-regression evidence passed. The two repository active SQLite files remained byte-identical. Formal evidence is recorded in `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCTIZATION_REVIEW.md`.
