# CURIS WORKTREE RECONCILIATION DECISIONS

Status: Review  
Date: 2026-08-16  
Round: 2.5 — Reconciliation Decisions  
Source: Owner Correction in Round 2.5, Round 1/2 audit reports, current Issue / Review / Authority records  
Canonical root: /Users/yy/Documents/Curis AI Workspace/docs/

## 1. Purpose and boundary

本文件只记录本轮 Owner 已明确收敛的产品 / 实现 / 工作树事实。

本轮没有：

- 修改旧 Review、CURRENT_STATE、PRODUCT_DOCUMENT_POINTER 或 CHANGE_LOG。
- 修改业务代码、产品文档内容或 .gitignore。
- 删除、移动、归档或提交任何文件。
- 执行 staging、测试、build、regression 或 commit。

本文件不是对旧文档的物理修正，而是为后续文档 / Git reconciliation 提供当前决策记录。

## 2. Decision 1 — RD Long-running Reliability

### Current decision

- Implementation: Completed
- Acceptance: Accepted
- Current product truth: Closed
- Older Review mismatch: Documentation / Git Reconciliation Gap
- Action: 后续在对应文档整理组中同步状态
- This round: 不修改旧 Review

### Boundary

本决定只覆盖 long-running task reliability fix 本身，不自动升级 RD Phase 2A 其他范围。

因此：

- long-running reliability 不再归入纯 Candidate / Review Required bucket。
- RD Phase 2A 的其他设计、Artifact Review、Handoff、P7 CEO Decision 等仍按其正式证据保持原状态。
- 旧 RD Review / CURRENT_STATE / Change Log 若仍写成 long-running reliability Review Required，属于文档 / Git reconciliation gap，不代表需要重新验收。
- 不得将 long-running reliability 的 Accepted / Closed 状态泛化为整个 RD Phase 2A Accepted。

## 3. Decision 2 — Content Growth UX Translation

### Current decision

当前正确停止态：

> CONTENT GROWTH OPERATING STRATEGY UX TRANSLATION CLOSED

### Scope clarification

- T5 已补齐。
- T5 = Employee Detail Shared consistency。
- 停止态已修正。
- T1–T4 没有重做。
- T1–T4 只在已有结果上做必要的就地修正。
- Visual Design / final high-fidelity 仍 deferred。
- 不得描述为“重新完成 T1–T5 全套设计”。

### This round

- 不修改原设计文档。
- 不启动 Content Growth 新开发。
- 后续只在文档整理组中同步该停止态，保留 T1–T4 的历史连续性。

## 4. Decision 3 — Root Duplicate Product Docs

以下根目录文件正式按：

> MIGRATION SOURCE — DO NOT COMMIT

处理：

- Curis_Product_Master_Map_v2.0.md
- Curis_Page_Map_v1.0.md
- Talent_Market_Integration_Contract.md
- Talent_Market_Product_Map.md
- Talent_Market_Resource_Audit.md
- Curis_Product_Rethink_Reasoning.md

### Authority

Canonical Product Truth 继续以 docs/ 体系为准：

- docs/00_Context/CURRENT_STATE.md
- docs/00_Context/PRODUCT_DOCUMENT_POINTER.md
- docs/07_Decisions/ 中的 Frozen decisions
- canonical docs/01_Product、docs/02_Architecture、docs/03_Design
- docs/08_Change_Log/CHANGE_LOG.md

### This round

- 不删除。
- 不移动。
- 不 stage。
- 不让根目录副本覆盖 canonical docs。

## 5. Decision 4 — 16 Anomalous Database Object Files

### Current decision

16 个形如：

~~~text
<app.database.Database object at ...>
~~~

的文件已经确认是真实 SQLite 数据库副本。

当前策略：

> KEEP FOR NOW / DELETE CANDIDATE AFTER EVIDENCE REVIEW

### Required evidence review before any future cleanup

需要先确认：

- 是否存在 Review / Evidence 引用。
- 是否包含仍需保留的数据。
- 是否已有安全备份。
- 是否存在测试、脚本或历史复现流程引用这些路径。
- 是否可以区分重复内容与唯一内容。

### This round

- 不删除。
- 不归档。
- 不 stage。
- 不执行数据库查询或迁移。

## 6. Decision 5 — Local Runtime Database

### backend/data/curis.sqlite

当前策略：

> KEEP LOCAL / DO NOT COMMIT

- 不删除。
- 不 stage。
- 长期是否归档以后单独决定。

### WAL / SHM

当前策略：

> KEEP LOCAL / IGNORE CANDIDATE

- data/issue_pipeline.sqlite-wal
- data/issue_pipeline.sqlite-shm

本轮不修改 .gitignore，不清理 WAL / SHM。

## 7. Decision 6 — Desktop Generated Boundary

以下明确属于 generated/local：

- desktop/target/
- desktop/node_modules/
- desktop/.runtime/
- desktop/runtime/__pycache__/
- .DS_Store

长期策略：

> KEEP LOCAL / IGNORE

### Evidence exception

desktop/target/.../Curis.app 等 packaged Desktop 产物如果被正式 Acceptance / Evidence 引用，必须先完成 Evidence retention review。

### This round

- 不删除 desktop/target。
- 不 stage desktop/target。
- 不 stage desktop/node_modules、desktop/.runtime、.DS_Store。
- Desktop source 与 generated boundary 由 Round 2 ownership report 继续保留。

## 8. Decision 7 — AGENTS.md

当前策略：

> OWNER REVIEW / HOLD

- 不提交。
- 不 revert。
- 不修改。

原因：

- AGENTS.md 已跟随 Blueprint v5.1 更新。
- 但仓库 baseline、Current State 和 HEAD 尚未整体 reconciliation。
- 该治理文件不能和业务代码或产品 candidate 文档混合提交。

后续在文档基线收口时再决定 KEEP / UPDATE REQUIRED / REVERT CANDIDATE。

## 9. Decision 8 — Strategy Meeting Legacy Changes

当前没有足够新的 Authority / Accepted Review 证明 Strategy Meeting 相关修改属于本轮正式成果。

范围包括：

- backend/app/main.py 中 StrategyMeetingIn 和 strategy-meetings endpoints。
- backend/app/database.py 中 strategy_meetings schema 和 persistence methods。

当前策略：

> HOLD / OWNER REVIEW

明确排除：

- 不进入 G1。
- 不进入 Shared Runtime。
- 不删除。
- 不与 AI Capability、RD 或 XHS 混合提交。

## 10. Decision 9 — Ordinary-user CEO Office Frontend Wave

当前没有独立 Accepted Review。

当前策略：

> PRODUCT CANDIDATE / HOLD

不得随以下 group 提交：

- XHS
- RD
- Computer Access
- Shared Runtime

该 wave 后续需要独立 Product Issue / Review 或明确归入文档 / UI candidate group。

## 11. Corrected Group Status

| Group | Corrected current status | Boundary |
|---|---|---|
| G1 — Agent Computer Access P0 | Accepted | requested/configured/effective truth, snapshot/persistence, supported sandbox mapping, Full fail-closed, resume fresh snapshot |
| G2 — XHS Workspace | Accepted | bounded slice; no real external publish / analytics |
| G3 — RD Phase 0/1 | Accepted | accepted bounded execution slice |
| RD Long-running Reliability | Accepted / Closed | reliability fix and acceptance only; separate from other Phase 2A scope |
| RD Phase 2A other scope | Review Required where formal evidence says so | do not upgrade whole Phase 2A |
| G5 — Shared Runtime | SHARED RUNTIME INDEPENDENT COMMIT NOT YET SAFE | mixed domain service/router/UI boundary |
| G6 — Talent Market / AI Capability | Review / Candidate | no new development in this round |
| G7 — Frozen Authority | Frozen docs staging candidate | exact canonical files only |
| G8 — Product / Content Growth candidate docs/UI | Mixed | Frozen Authority separated from Review/Candidate |
| G9 — Workspace Engineering | Review / Approved Candidate / Not Started | Dynamic Workspace Runtime NOT IMPLEMENTED |
| G10 — Issue / Review / Evidence | Status follows each record | do not infer code acceptance from evidence presence |
| Repository Governance | Owner Review / Hold | AGENTS.md and .gitignore remain untouched |
| Generated / Local State | Keep local / evidence review / owner review | no cleanup in this round |

## 12. Reconciliation gaps now identified

The following are documentation / Git reconciliation gaps, not automatic reimplementation requirements:

1. Older RD records may still show long-running reliability as Review Required.
2. CURRENT_STATE / Change Log may not yet reflect Accepted / Closed reliability truth.
3. Content Growth documents may not yet record the corrected T5-only closure language.
4. Canonical documents may still contain short root-style Rethink filename references.
5. The dirty worktree and actual HEAD are not yet reconciled with the documented c0e1855f baseline.
6. AGENTS.md has the Blueprint v5.1 wording but remains Owner Review / Hold.

These gaps should be handled in a later documentation / Git reconciliation group, without changing accepted implementation scope.

## 13. Owner decisions captured

The Round 2.5 Owner Correction is captured in this record:

- RD long-running reliability = Accepted / Closed.
- Content Growth UX Translation = T5 closure; T1–T4 not redone; final high-fidelity deferred.
- Root duplicate docs = Migration Source — Do Not Commit.
- 16 anomalous SQLite files = Keep for now / delete candidate after evidence review.
- backend/data/curis.sqlite = Keep local / do not commit.
- WAL / SHM = Keep local / ignore candidate.
- Desktop generated boundary = Keep local / ignore target.
- AGENTS.md = Owner Review / Hold.
- Strategy Meeting = Hold / Owner Review.
- Ordinary-user CEO Office wave = Product Candidate / Hold.

## 14. Next-step boundary

The next permitted operation is the separate review of:

docs/reviews/CURIS_WORKTREE_G1_STAGING_MANIFEST.md

No staging is authorized by this document.

## 15. Document Registration

- Absolute path: /Users/yy/Documents/Curis AI Workspace/docs/reviews/CURIS_WORKTREE_RECONCILIATION_DECISIONS.md
- Status: Review
- Source: Round 2.5 Owner Correction, current G1 Issue / Review, Round 1 / Round 2 reports, current worktree facts.
- Pointer / CURRENT_STATE / CHANGE_LOG: not modified.
- Next step: review the G1 exact staging manifest; after owner approval, authorize at most one precise staging operation.

> NO FILES STAGED  
> NO FILES DELETED OR MOVED  
> NO OLD DOCUMENTS MODIFIED  
> NO TESTS RUN  
> NO COMMITS CREATED
