# CURIS V1 — KNOWLEDGE LIBRARY UI ACCEPTANCE

Status: Frozen  
Authority Class: CURRENT UI ACCEPTANCE / DESIGN BASELINE  
Date: 2026-09-01  
Disposition: UI ACCEPTED

## Accepted result

- **Knowledge Library Product:** ACCEPTED
- **Knowledge Library UX:** ACCEPTED
- **Knowledge Library UI:** UI ACCEPTED
- **Internal product mind:** Company Reference Space
- **User-facing name:** 资料库
- **Current Figma baseline:** `187:2` 资料库总览 · `187:276` 浏览 / 搜索 · `187:550` 阅读 / 资料详情 · `187:824` 从工作选择资料（1440 × 900 Light）

## Frozen UI responsibilities

- Reading Surface is the primary detail surface: find → read → judge source and freshness → inspect usage → return to Work.
- Large-library presentation uses a **Reference Row**: title, summary or nearby hit context, source, applicable scope, update time and truth state. It does not become a large Card Wall or File Tree + File List + metadata admin.
- Browse shows summaries / opening text; Search shows keyword-near context. Current limited search is not presented as semantic, vector or AI-ranked search.
- Loading uses an initial batch plus explicit **Load More**; approximately 30–50 rows is a UX/performance target, not a DB contract. Without reliable total count, show “已显示 N 条” only.
- Company / Business / Workspace are the lightweight current scope selector (`当前范围 · 全公司`), not fixed three library tabs.
- `187:824` is a compact Reference Picker, not a second Library. It shows current Work, Employee, lawful scope, search, simplified rows and selected references, then adds and returns to the original Work.
- Return restores keyword, filters, sort, scroll position and loaded batch as a Frontend behavior; it does not create a second Library session truth.
- Work ↔ Library ↔ Result remains traceable and content is not copied. Work Picker defaults to Company + current Business + current Workspace within existing access authority.
- Honest states remain 可用、数据较旧、需要核实、待连接、未记录; no zero or synthetic data replaces unknown.

## Implementation boundary

Current V1 source support remains manual content plus `.md` / `.txt`. PDF, DOCX, image, Web and external sync are not claimed. Dynamic batching, load failure, exact list-position restoration, Dark / 1024, accessibility / keyboard and real Runtime data-density verification remain P2. Frontend implementation is pending productization; Runtime / Data remains partial with the previously registered scope, citation, freshness/version, reverse Work/Result, connector, ACL and packaged-restart gaps.

Historical `CURIS_V1_KNOWLEDGE_LIBRARY_UX_EXPLORATION.html` remains accepted UX input / research provenance, not the Current Final Visual Authority. No Figma edit, Frontend, Backend, Runtime, Schema, DB, redesign, release, commit or push was performed by this registration.
