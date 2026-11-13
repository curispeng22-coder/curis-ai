# CURIS V1 — KNOWLEDGE LIBRARY IMPLEMENTATION ACCEPTANCE

Authority Class: CURRENT IMPLEMENTATION TRUTH / ACCEPTANCE REGISTRATION
Status: Frozen
Date: 2026-09-01
Disposition: IMPLEMENTED / ACCEPTED

## Accepted result

- Knowledge Library Product: ACCEPTED
- Knowledge Library UX: ACCEPTED
- Knowledge Library UI: UI ACCEPTED
- Knowledge Library Implementation: IMPLEMENTED / ACCEPTED
- Canonical Knowledge Scope: VERIFIED
- Work → Knowledge Typed Reference: VERIFIED
- Reverse Used By Work: VERIFIED
- Result / Evidence Projection: VERIFIED
- Bounded Context Injection: VERIFIED
- Archive / Hard-delete Protection: VERIFIED
- Packaged Desktop: VERIFIED
- Restart / Persistence: VERIFIED
- Active SQLite Safety: PASS（byte-identical；integrity `ok`）

本登记消费 `CURIS_V1_KNOWLEDGE_LIBRARY_PRODUCTIZATION_REVIEW.md`、`CURIS-V1-KNOWLEDGE-LIBRARY-PRODUCTIZATION-001.md`、canonical scope / typed reference contract、Future Compatibility Review、Product / UI acceptance、CURRENT_STATE、Pointer、Completion Reconciliation 与 Execution Backlog。Review 未发现阻塞本次 V1 资料库实现验收的隐藏 P1。

## Evidence boundary

真实链覆盖：Company / Business / Workspace canonical scope、手工与 `.md/.txt` 资料、105 条规模、Overview、Browse、Search、显式 Load More、reading-first Detail、真实 Work 入口与 Work Picker、`WORK --USES_REFERENCE--> KNOWLEDGE` 持久化、exact return、Used By Work、Result / Evidence / Artifact 反查、显式引用优先 + bounded automatic retrieval、archive/unavailable、referenced hard-delete rejection、cross-tenant/company/scope fail-closed、Browser、fresh packaged Desktop、完全退出 / 同根 restart、Backend 43 passed、Frontend focused 1 passed、ESLint / Python compile / production build / PyInstaller / Tauri package / diff check。

证据路径与包身份：

- Curis.app：`/Users/yy/Documents/Curis AI Workspace/desktop/target/release/bundle/macos/Curis.app`
- Executable SHA-256：`cabc9d9be89ec65af2511c3670ace505a6668979d542ca7c062d0b2c943c5f5a`
- 隔离 app-data：`/tmp/curis-knowledge-desktop.HannLb`
- Browser / Desktop evidence：`/tmp/curis-knowledge-library-evidence/`

没有使用 Fixture 作为生产事实；没有建立第二套 Knowledge、Citation、Context、Result 或 reverse relation truth；仓库 active SQLite 未被写入。

## Current scope and reference truth

资料库适用范围固定为 `Company / Business / Workspace`，使用 canonical identity；`project_id` / `department_id` 仅作为 legacy compatibility / migration provenance，不能解释为 Business。当前 typed reference 是 `Work → USES_REFERENCE → Knowledge`，但 vocabulary 保持 generic，未来其他对象只有在独立 Authority 批准后才能复用。

Context 继续是 execution-derived snapshot：显式 Work refs first，再合并合法范围内 bounded automatic retrieval；不注入全库、全 Workspace、全 Conversation 或全历史。Knowledge 详情的 Used By 与相关 Result / Evidence 由同一关系及既有 Work output truth 投影，不复制正文。

已引用资料可 Archive / unavailable，但不能 hard delete；历史 reference 保留。该结论不等于完成完整 version、Citation、ACL、Connector、Semantic/Vector、Graph 或 retention platform。

## Remaining boundaries

以下继续保持 Future / Conditional / P2，不阻塞当前实现验收：

- PDF / DOCX / image / web / external Knowledge connectors；
- semantic/vector retrieval、full RAG、Knowledge Graph；
- source version browsing、section/paragraph citation；
- granular ACL、automatic promotion、dedup、formal conflict engine、full retention；
- dynamic scale optimization beyond the verified 105-entry case；
- Dark / 1024 / accessibility / keyboard adaptation（如未另行验收）。

无真实来源时继续显示 `待连接 / 暂无数据 / 数据较旧 / 需要核实 / 未记录`，不虚构外部结果或自动报告。

## Product Completion and next gate

资料库从 `PRODUCT ACCEPTED / UI ACCEPTED / IMPLEMENTATION PENDING` 更新为：

`PRODUCT ACCEPTED / UX ACCEPTED / UI ACCEPTED / IMPLEMENTED / ACCEPTED / CANONICAL SCOPE + REFERENCE VERIFIED`。

资料库不再属于 Areas Requiring Frontend Productization。下一 Product Completion 区域为：

`MEETING ROOM DIRECTION D VISUAL CLOSURE`。

本登记不修改 Product Blueprint、Master Map、UI Blueprint、Runtime、Schema、DB、Figma 或产品模型；不进行 commit / push。

**KNOWLEDGE LIBRARY IMPLEMENTATION ACCEPTANCE REGISTERED**
