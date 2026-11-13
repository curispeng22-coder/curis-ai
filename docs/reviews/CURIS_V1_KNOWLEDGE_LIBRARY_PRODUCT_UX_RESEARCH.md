# CURIS V1 — KNOWLEDGE LIBRARY PRODUCT + UX EXPLORATION

Status: Review  
Authority Class: RESEARCH  
Disposition: STOP FOR CEO REVIEW  
Scope: Product / UX exploration only; no Blueprint, Runtime, Schema, DB, Frontend or Figma change.

## 0. Executive summary

资料库已经是 Curis 的 Current Product Space，但当前实现仍是一个有限的 Knowledge Service：可在租户内保存手工资料，读取配置目录中的 `.md/.txt`，按标题/摘要/正文/标签做文本搜索，并把少量相关条目快照带入 Task Context。它还不是完整的 Company Reference Space：Business / Workspace 作用域、可追溯引用、来源版本与 freshness、资料被 Work / Result 使用的关系、外部同步和更细的权限都没有被当前实现完整承载。

本研究建议采用 **Company Reference Space（公司参考空间）** 的产品心智：

- 借用 File Library 的可浏览、可读、可导入习惯；
- 借用 Knowledge Base 的检索、标签和范围筛选；
- 但把核心问题放在“公司正在依据什么工作、这些资料被谁/哪项 Work 使用、哪些结论仍然可信”，而不是文件数量。

这不是新增 `LibraryItem`、`KnowledgeDocument` 或 Citation 数据库。现有 `Knowledge`、`Context`、`Reference`（待形成的产品关系）、`Evidence`、`Artifact`、`Result` 继续分工；本报告只标记当前实现差距与设计候选。

## 1. Authority and evidence boundary

| Source | Authority class / status | What this research consumes |
|---|---|---|
| `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md` | FROZEN · truth router | 资料库当前产品空间与实现状态指针；不被本报告覆盖 |
| `docs/01_Product/Curis_Product_Blueprint.html` §09 资料库 | CURRENT PRODUCT TRUTH · Frozen | 资料库是本地/外部/公司产生资料的统一入口，负责读取、索引、搜索、引用、权限、来源追踪、沉淀与复用 |
| `docs/01_Product/Curis_Product_Master_Map.md` 资料库/Knowledge rows and page map | CURRENT PRODUCT TRUTH · Frozen | 资料库与 Business/Workspace、Result、Evidence、Insights 的反向入口关系；当前尚缺完整字段级 Library Page Contract |
| `docs/01_Product/Curis_Product_UI_Blueprint.html` 资料库 references | CURRENT UI STRUCTURE · Frozen | 主区阅读 + 按需来源/Context/Utility；不定义本研究最终视觉 |
| `docs/03_Design/Curis_Company_OS_Shared_Authority.md` §5.1 / §6 | FROZEN SHARED AUTHORITY | Context Isolation：只检索完成当前责任所需的 Knowledge/Evidence；不得把组织成员资格当作 Knowledge Access |
| `backend/app/knowledge_service.py` | IMPLEMENTATION TRUTH (code) | Persisted `knowledge_entries`; manual/local-file source; `.md/.txt` connector; tenant boundary; project/department scope |
| `backend/app/context_service.py` | IMPLEMENTATION TRUTH (code) | Task-scoped retrieval and bounded context snapshot; max 3 Knowledge entries; project/department filtering |
| `backend/app/database.py` | IMPLEMENTATION TRUTH (code) | `knowledge_entries`, `memory_entries`, `context_packages` tables; Knowledge distinct from Memory and Context |
| `backend/tests/test_mvp_phase5_s10_knowledge_management.py` | EVIDENCE | Import/update, path safety, tenant isolation, manual project search, frontend real-flow assertions |
| `docs/01_Product/Curis 产品梳理 1.0_副本/Product Bible v1.0/12 资料中心（Knowledge Center）.md` | HISTORY / product draft | Historical rationale: not a file manager; local, external and Curis-produced sources; no Current override |

No research source is promoted to Current Product Truth by this document.

## 2. Existing Truth audit

### 2.1 Knowledge, Context and related objects

| Object | What it is now | Canonical? | Persisted / versioned | Consumer | Classification |
|---|---|---|---|---|---|
| Knowledge | Tenant-scoped source material with title, body, summary, tags, source type and hash | Yes as shared Product/Runtime concept; current schema is partial | `knowledge_entries`; content hash + timestamps, no version history | Knowledge page, ContextService | **IMPLEMENTED / PARTIAL** |
| Local text connector | Environment-configured roots; safe read of `.md/.txt`, max size/count, repeat import updates same source row | Yes as bounded connector path | Source path + hash; no sync cursor/history | Knowledge page/import API | **IMPLEMENTED / BOUNDED** |
| Context | Immutable snapshot assembled for one Task execution | Yes | `context_packages`, package hash, task pointer | Employee execution / provider prompt | **IMPLEMENTED / PARTIAL** |
| Memory | Long-term user/project/employee experience; distinct from Knowledge | Yes | `memory_entries`, confidence/status/use count | ContextService and employee memory | **IMPLEMENTED / DISTINCT** |
| Reference / citation | Product language exists; current payload has source label/path but no first-class reference or location object | Product concept, not current storage contract | Not independently persisted | Reading/Work/Evidence are intended consumers | **MISSING / PRODUCT→IMPLEMENTATION GAP** |
| Evidence | Truth-bearing proof of an external or internal result | Yes shared truth | Existing Result/Evidence paths; Knowledge does not become Evidence automatically | Result, Decision, Insights | **IMPLEMENTED elsewhere; relation missing** |
| Artifact / Report | Work output that may later be referenced | Yes shared truth | Existing Artifact/Report paths | Workspace, Insights, CEO Desk | **IMPLEMENTED elsewhere; Knowledge ingestion relation missing** |
| Result | Accepted work/external outcome truth; not a document store | Yes shared truth | Existing Result paths | CEO Desk, Insights, Work | **IMPLEMENTED elsewhere; Library reverse link missing** |

### 2.2 Current frontend reality

`frontend/app/ceo-office/knowledge/page.js` currently provides a real list page, search, all/company/project/department filters, manual creation, local-file import and source-root status. `entries/[id]/page.js` shows body, source type/label/path, scope, timestamp, hash and tags. This is reusable functional substrate, not the final visual authority.

The current UI still exposes legacy implementation terms (`project`, `department`, `知识库`) and does not show Business/Workspace identity, citation anchors, use-by-Work/Result, stale/conflict states, or source version history. Those are gaps, not permission to invent a second data model.

### 2.3 What tests actually prove

- `.md/.txt` files can be listed/imported from a configured root; unsupported types, traversal and symlinks are rejected.
- Re-import of the same local path updates one traceable row (same id) and refreshes content.
- Manual entries can be scoped to a project and searched; tenant isolation is enforced.
- Knowledge is distinct from Memory, and relevant Knowledge can be placed into a bounded Task Context.

Tests do **not** prove Business/Workspace scope, full-text indexing, citation location, external connectors, source version history, ACLs, Work/Result provenance or restart-specific Library UX.

## 3. Product mind: three candidates

| Candidate | Primary question | Useful pattern | Failure if adopted alone | Decision |
|---|---|---|---|---|
| A. File Library | “文件在哪里，怎么打开/导入？” | Familiar browse, folders, recent items, import | Turns Curis into a file cabinet; hides authority, scope and use in work | Keep mechanics only |
| B. Knowledge Base | “我能搜索到什么知识？” | Search-first, tags, collections, answer-oriented retrieval | Implies static articles and a second AI/RAG product; weak on source lifecycle and result truth | Use retrieval patterns |
| C. Company Reference Space | “公司正在依据什么工作，资料是否可信，在哪里被使用？” | Scope-aware browse, provenance, references, Work/Result back-links, honest freshness | Requires better source/relationship contracts; must stay bounded | **Recommended product mind** |

Recommendation is a Research Candidate, not a Current UI decision.

## 4. Who the space serves

| User | Need | Default interaction |
|---|---|---|
| CEO | Know what the company can rely on; add a reference; inspect why a result used a source | Browse/search, read, attach, review provenance; not indexing administration |
| Department / Business Leader | Maintain shared operating references and see scope coverage | Scoped browse, import, deprecate/unavailable, link to Work/Result |
| Workspace Leader | Give current work the right references and notice stale/missing inputs | Select reference from Work, inspect source/freshness, return to Work |
| Employee | Retrieve only relevant, allowed references for current responsibility | Context-assisted search/citation; no whole-company dump |
| Workspace / Business | Provide a coherent reference boundary | Business/Workspace scope and reverse links; no duplicate copies |

## 5. Scope and source contract (research candidate)

### Scope

Canonical product scope is **Company → Business → Workspace**. Department may be a legitimate organizational context but must not replace Business/Workspace as the primary operating scope for a library item. Existing `project_id`/`department_id` rows are implementation/migration provenance; they should not be silently reinterpreted in this research.

### Source types

1. Manual note / decision reference entered in Curis.
2. Local `.md` / `.txt` import (current bounded implementation).
3. Work output / Artifact / Report reference (should link, not duplicate body).
4. Result / Evidence reference (should link, not become Knowledge automatically).
5. Future external sources: GitHub, Drive, Notion, web, cloud knowledge systems; availability is conditional and not currently claimed.

Rules:

- Source is where material came from; Knowledge is Curis’s usable reference projection.
- Knowledge/Reference is not Evidence; Evidence proves a result.
- Knowledge is not Result; a result may cite Knowledge, and a report may be promoted as a reusable reference only through an explicit review path.
- One source may feed multiple scopes through references; do not copy three bodies to represent Company/Business/Workspace.

### Provenance and freshness minimum

Every readable reference should be able to show (when available): source kind, human-readable source name, location/path or external URL, captured/updated time, content version/hash, scope, access state and freshness state. If any value is unavailable, show “未记录 / 待连接 / 数据较旧 / 需要核实”; never infer currentness from a missing timestamp.

Minimum citation for a Work/Result:

`name + source + location (or stable anchor) + last known update + verification/freshness state`.

Section/line anchors are a later enhancement unless the existing runtime can supply stable anchors; the UI must not fabricate them.

## 6. Work ↔ Library ↔ Result flow

```text
CEO / Leader expresses a need
→ Work scope resolves Company / Business / Workspace
→ browse or search allowed references
→ select a reference into the current Work context
→ Employee uses it and returns output / Result
→ Result / Evidence records which references were used
→ CEO / Leader reviews; useful material may be retained as a reference
→ next Work can discover it without copying the source
```

The reverse entry is equally important:

`Library item → Used by Work / Result / Meeting / Decision → open the source Work or result in its original context`.

Current `ContextService` only implements the forward retrieval slice (bounded matching into a Task snapshot). It does not yet provide the reverse relation or citation-grade source anchors.

## 7. AI relationship and trust states

AI may search, summarize, suggest references and attach allowed references to a scoped Work context. It must expose why a reference was selected and preserve scope isolation.

AI must not silently:

- treat a stale source as current;
- choose between contradictory sources;
- turn a Knowledge entry into Evidence or a Result;
- inject all company material into every Employee context;
- claim an external connector is connected when it is not.

Suggested user-facing data states: `可用`, `待连接`, `数据较旧`, `来源不一致 / 需要核实`, `未记录`. A formal global `Conflict` status is not introduced here.

## 8. Page and interaction directions

### Direction A — File-first Library (reference only)

Overview shows recent files, source roots, folders and import. Detail is a reader with a compact metadata pane. Good for first familiarity, but weak at Work/Result linkage and operational trust.

### Direction B — Knowledge-base Search (reference only)

Search is the primary action; filters are Company / Business / Workspace / source / freshness; results preview the matching passage and why it is relevant. Good for retrieval, but can feel like a separate AI search product if no original source and Work relationship are visible.

### Direction C — Company Reference Space (recommended)

1. **Overview**: current scope, source coverage, recently used references, stale/unavailable notices; no vanity counts.
2. **Browse / Search**: scope + source filters, readable result rows, short match explanation, freshness/provenance label.
3. **Read / Reference detail**: main reading surface; right utility shows source facts, scope, citation handle and Used by Work/Result.
4. **Select from Work**: compact picker opened from an existing Work/Conversation/Composer; returns to the exact originating context.
5. **Use history**: reverse links to Work, Result, Evidence, Meeting or Decision, without copying content.

This direction keeps the primary surface readable and uses utility/inline states instead of a wall of cards or a new “Knowledge Console”.

## 9. Required states for a future design exploration

| State | Must communicate | Allowed action |
|---|---|---|
| Empty Library | No company/business/workspace references are present in this scope; this is truthful, not a demo | Add note, import allowed text, connect a future source |
| Library Overview | What is available, where it came from, what needs attention | Browse, search, filter, open |
| Search Results | Match, scope, source, freshness and why it is relevant | Read, select into current Work |
| Reading / Reference Detail | Content plus provenance and citation handle | Copy reference, open source, inspect use history |
| Select Reference From Work | Current Work scope and the references being added | Select/remove, return to exact Work context |
| Source Unavailable / Stale | Material cannot be treated as current; reason and next step | Reconnect, inspect last known version, continue with explicit caution |
| Used By Work / Result | Where the reference influenced work or a result | Drill to original Work/Result/Evidence |

## 10. Runtime / data gap matrix

| Capability | Current evidence | Status | Product implication |
|---|---|---|---|
| Manual note | `createKnowledgeEntry` + API + tests | IMPLEMENTED / bounded | Reuse; expose as simple Add reference |
| Local `.md/.txt` import | Local roots/files/import API + path safety tests | IMPLEMENTED / bounded | Reuse; do not imply PDF/DOCX/web support |
| Search | SQL `LIKE` over title/summary/body/tags | PARTIAL | Product may say search; true indexing/relevance is a gap |
| Company scope | Null project/department maps to company | PARTIAL | Keep company entry; needs canonical Company relation |
| Business / Workspace scope | Not represented in `knowledge_entries` | MISSING | Hard Product→Implementation gap for Current model |
| Source provenance | source_type/label/path/hash/timestamps | PARTIAL | Add display only when real; no fabricated anchors |
| Version / freshness | content hash + updated_at, no history | PARTIAL | Need source-version/freshness contract before trust claims |
| Citation / stable location | No first-class citation relation/anchor | MISSING | Required for Work/Result reference flow |
| Work ↔ Library selection | ContextService retrieval only | PARTIAL | Need originating-context picker and return path |
| Result / Evidence relation | No Knowledge use relation in current code | MISSING | Link, do not copy body |
| Local connector | Env-configured local files | IMPLEMENTED / bounded | Treat as provider; external connectors remain future |
| External connectors | No current verified Drive/Notion/GitHub/web sync | MISSING / LATER | Conditional discovery only |
| Permission | Tenant isolation and scope checks | PARTIAL | Entity-level Company/Business/Workspace access still needed |
| Archive/delete/detach | No complete current API/UI contract | MISSING | Preserve history and references before destructive actions |
| Stale/conflict/unknown | UI has generic missing-data copy only | MISSING | Add truthful states, not a new global Conflict state |
| Restart/persistence | DB persistence exists; knowledge-specific packaged restart not evidenced here | UNVERIFIED | Require isolated restart evidence before acceptance claims |

## 11. V1 versus later (maturity, not an artificial roadmap)

### Can be completed when dependencies are real

- Company/Business/Workspace scope mapping;
- readable browse/search and reference detail;
- `.md/.txt` import and manual notes;
- source/freshness/unknown labels based on real values;
- selecting a reference from Work and returning to the same context;
- lightweight citation and reverse link to Work/Result where canonical relations exist.

### Later / conditional until prerequisites exist

- PDF/DOCX/image/web ingestion;
- external connector sync and reconnect;
- section-level anchors, semantic/full-text index and ranking;
- granular ACL, legal hold and bulk retention policies;
- automatic promotion of Reports/Results into reusable Knowledge;
- cross-company sharing or a marketplace of knowledge.

“Later” here means a real dependency, evidence or model is not ready; it does not authorize suppressing a confirmed, safely implementable capability.

## 12. Competitor pattern scan (research only)

| Product family | Pattern worth learning | Do not copy as Curis truth |
|---|---|---|
| Notion / Obsidian | readable pages, backlinks, source navigation, gradual structure | a generic wiki as the company operating truth |
| Google Drive / file libraries | familiar import, browse, recency and permissions | treating file ownership as business responsibility |
| Glean / enterprise search | scope-aware retrieval and “why this result” | a separate search product detached from Work |
| SharePoint / Copilot | governed sources, enterprise permissions, citations | assuming enterprise ACL complexity is V1-ready |
| ChatGPT Projects / Claude Projects | project-scoped references and conversational use | a second conversation context store or hidden RAG truth |

These are comparative UX patterns, not implementation commitments or current provider integrations.

## 13. Answers A–P

**A. Product identity:** 资料库 is the seventh primary product area and Company Reference Space candidate; it is not merely a file manager.  
**B. Users:** CEO/Leader manage meaning and trust; Employees consume scoped references; Workspaces provide the working boundary.  
**C. Scope:** Company → Business → Workspace is the canonical product reading; legacy project/department rows remain provenance until a governed migration.  
**D. Sources:** Manual, local text, Work outputs, Result/Evidence references, then conditional external connectors.  
**E. Source vs Knowledge:** Source is origin; Knowledge is a usable reference projection.  
**F. Knowledge vs Evidence/Result:** Knowledge informs; Evidence proves; Result records outcome.  
**G. Freshness:** show version/hash/time only when real; otherwise unknown/stale/waiting.  
**H. Citation:** minimum source + location + update/verification state; stable section anchors only when runtime can supply them.  
**I. Work relation:** forward selection into Work and reverse “Used by Work/Result” links without copies.  
**J. AI:** retrieve, explain relevance, cite, flag stale/inconsistent; never silently choose or inject everything.  
**K. Connector:** provider of source material; authorization/health belongs to Settings/Capability, not a second Library system.  
**L. Permission:** start with Company share, Business share, Workspace use; do not promise full ACL before evidence.  
**M. Empty state:** honest absence of references, with Add/Import/Connect actions and no fake documents.  
**N. CEO Assistant:** can coordinate a reference search and return to the originating Desk/Business/Workspace context; it is not the Library owner or a hidden indexer.  
**O. Insights:** reports/analysis may reference Library material; Insights remains the canonical analytical surface and does not become a Knowledge store.  
**P. Recommended direction:** Company Reference Space, implemented with familiar File Library mechanics and Knowledge Base retrieval patterns.

## 14. Open questions for CEO Review

1. Accept **Company Reference Space** as the product mind for 资料库, while retaining File Library and Knowledge Base as interaction patterns?
2. Confirm that Work/Result “Used references” is a required product relationship for the first complete Library slice, subject to canonical Runtime support?
3. Confirm whether Company-shared, Business-shared and Workspace-use are the intended V1 permission language, with granular ACL deferred until a real need/evidence exists?

## 15. Disposition

This is a Review/Research artifact only. It does not change Current Product Truth, create a new Runtime primitive, or authorize implementation. The next gate is CEO review, followed by a bounded Page Contract / design decision if accepted.

