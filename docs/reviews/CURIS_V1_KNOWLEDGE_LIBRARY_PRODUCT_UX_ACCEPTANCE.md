# CURIS V1 — KNOWLEDGE LIBRARY PRODUCT / UX ACCEPTANCE

Status: Review  
Authority Class: REVIEW  
Disposition: CEO ACCEPTED / APPROVED UX DIRECTION  
Date: 2026-09-01

## Accepted registration

- **Knowledge Library Product:** ACCEPTED
- **Internal product mind:** Company Reference Space
- **User-facing name:** 资料库
- **UX Direction:** Direction C — Company Reference Space, accepted as product/UX direction
- **Accepted structure:** Overview; Browse / Search; Reading / Reference Detail; Select Reference From Work; Used By Work / Result
- **Scope language:** 适用范围 / 使用范围（全公司、某业务、某工作空间）
- **Work ↔ Library ↔ Result:** accepted product relationship; content is not copied and usage remains traceable
- **Citation minimum:** name, source, location/stable locator when supported, last update, freshness/verification state
- **Truth states:** 可用、待连接、数据较旧、需要核实、未记录； no new global Conflict system

## Boundaries

`Source` is origin; `Knowledge / Reference` is reusable material; `Context` is the bounded snapshot used by one Work/Task; `Evidence` proves execution/result; `Result` records outcome. These continue to reuse existing Knowledge, Context, Reference relationship, Evidence, Artifact and Result truth. No `LibraryItem V2`, `KnowledgeDocument V2`, `CitationDB V2`, second Knowledge truth or second Context store is created.

Current implementation remains `PARTIAL / PRODUCT → IMPLEMENTATION GAP`: canonical Business/Workspace scope, first-class reference/citation relation, freshness/version history, Work/Result reverse relation, external connector integration, granular ACL and packaged restart evidence are not silently promoted by this registration. Search remains honest keyword/title/tag/scope search until a real semantic index exists; current manual and `.md/.txt` import remain the bounded supported inputs.

## Visual and implementation gates

- **Specific visual:** OPEN; next gate is `KNOWLEDGE LIBRARY DIRECTION D VISUAL CLOSURE`.
- **Frontend implementation:** PENDING.
- **Runtime / data:** PARTIAL.
- **Direction A File-first** and **Direction B Knowledge-base Search** remain interaction/retrieval pattern references, not parallel product directions.
- Figma, Frontend, Backend, Runtime, Schema, DB, connectors and release work are not authorized by this record.

Source research: `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCT_UX_RESEARCH.md`; exploration fixture: `docs/reviews/CURIS_V1_KNOWLEDGE_LIBRARY_UX_EXPLORATION.html`.
