# Curis Worktree Cleanup Final

Status: Review

Date: 2026-08-16

Scope: canonical document reconciliation、accepted / closed status sync、Preserved Development Baseline establishment。

## 1. Final decision

**SAFE TO RESUME DEVELOPMENT**

Worktree Cleanup can be marked **CLOSED for this reconciliation round**.

这不是 Git clean baseline，也不是所有 dirty source 已验收。它是一个可恢复、可保护、不会因继续开发而丢失既有成果的 development baseline：当前 remaining problems 已被分成 accepted fact、Review / Candidate、mixed source、migration source 和 non-blocking cleanup debt，没有 P0 级别的成果丢失或产品事实倒置风险阻塞下一阶段。

## 2. Baseline anchor

Canonical reconciliation 输入快照：

- HEAD before this docs-only sync: `a94bf6144bed0b2631bf0076204703580f3ed075`
- Product baseline remains: `main @ c0e1855f446a55aa3a384006cfcfed9877130338`
- G1 commit: `42db50cde54bc735d709bd603fe4d98d7f8233c8`
- Worktree before this final docs sync: 68 tracked worktree modifications, 312 untracked status entries, no staged paths
- Current product facts continue to be governed by `CURRENT_STATE.md`, Frozen ADRs and the canonical Pointer chain.

The docs-only reconciliation commit containing this record becomes the next Git anchor. It changes governance facts only; it does not replace, reset or normalize the dirty source baseline.

## 3. Canonical facts now reconciled

### G1 — Agent Computer Access

`AGENT-COMPUTER-ACCESS-RUNTIME-P0-001` is formally `IMPLEMENTED / ACCEPTED` and committed in `42db50cde54bc735d709bd603fe4d98d7f8233c8`.

Accepted boundary: requested/configured/effective truth, native mapping, persisted audit snapshot, supported sandbox mapping, Full fail-closed and fresh resume truth. This does not claim Full Computer Access or external provider-effective permission.

### G2 — XHS Workspace

XHS is `IMPLEMENTED / ACCEPTED` as a bounded internal vertical slice. It does not claim real external publication or Analytics.

Current source status:

> **ACCEPTED IMPLEMENTATION / COMMIT BLOCKED BY SHARED RUNTIME STRUCTURE**

The XHS page/component/test files are preserved together with mixed `runtime/workspace.py`, foundation router, `runtimeApi.js` and shared UI seams. No source restructuring was done to manufacture a historical commit boundary.

### G3 — RD

RD Phase 0/1 remains accepted for the bounded real execution slice:

```text
Project / Cycle → Task → Responsibility / Employee
→ Codex → declared-file change → Artifact / Evidence
→ Result Reference → restart / failure truth
```

The Issue / Review also contains Phase 2A design fidelity and `REVIEW REQUIRED`; therefore the accepted fact is not “all RD Phase 2A is complete”. Current source status is:

> **ACCEPTED BOUNDED SCOPE / BLOCKED BY MIXED SOURCE**

### RD long-running execution reliability

The reliability fix is **ACCEPTED / CLOSED**. This closes the reliability fix only. It does not upgrade RD Phase 2A design fidelity, Artifact Review, Handoff, P7 or other Review Required scope.

### Content Growth

Current stop state:

> **CONTENT GROWTH OPERATING STRATEGY UX TRANSLATION CLOSED**

T5 is the Employee Detail Shared-consistency closure. T1–T4 were not redone; they received only necessary in-place corrections over existing results. Visual Design / final high-fidelity remains deferred. The nine contract candidates remain Approved Candidate, while the two canonical Authority files remain the applicable Frozen semantic boundary.

### Workspace Engineering

- Dynamic Workspace Package Runtime: **NOT IMPLEMENTED**;
- Methodology Set: `Review / APPROVED CANDIDATE`;
- Technical Direction Proposal: `Review / TECHNICAL DIRECTION APPROVED CANDIDATE`;
- P0 Definition: `P0 DEFINED`;
- P0 Implementation Plan: `DRAFT / NOT STARTED`.

No document in this reconciliation claims that an installed Curis can dynamically install an unknown Workspace without source changes, rebuild or reinstall.

## 4. Preserved Development Baseline

The following remaining source is formally preserved and must not be reset, cleaned, overwritten or whole-file replaced by later work:

### Shared / mixed Runtime source

- `backend/app/main.py`;
- `backend/app/runtime/__init__.py`;
- `backend/app/runtime/models.py`;
- `backend/app/runtime/registry.py`;
- `backend/app/runtime/states.py`;
- `backend/app/runtime/store.py`;
- `backend/app/runtime/foundation.py`;
- `backend/app/runtime/execution_adapter.py`;
- `backend/app/runtime/legacy_execution_adapter.py`;
- `backend/app/runtime/simulation.py`;
- `backend/app/runtime/workspace.py`;
- `backend/app/api/runtime_foundation_router.py`;
- `frontend/lib/runtimeApi.js`;
- `frontend/components/runtime/`;
- `frontend/tests/runtimeWorkspaceUi.test.mjs`.

这些文件混合承载 Shared Runtime、RD、XHS、TTK / Content 和其他 Runtime wave。后续如需继续开发，必须先建立新的 bounded Issue、Allowed Files、ownership 和 evidence boundary。

### Accepted vertical-slice source and records

- XHS page / component / focused test 与 XHS Issue / Review；
- RD implementation / focused tests / RD Issue / Review；
- long-running reliability implementation facts与验收记录；
- G1 已提交代码与 formal acceptance record。

Accepted 不等于这些文件可以不经边界审计直接 whole-file stage。它表示当前成果必须被保留，不得在后续开发中被误清理或覆盖。

### Other dirty source and document waves

AI Capability、Talent Market、Content Growth candidate、frontend product wave、旧产品文档、Issue / Review / evidence 和本机 migration sources 仍处于各自的 Review / Candidate / Owner Review 状态。它们不阻塞恢复开发，但不得通过文件名、静态页面或未复核证据被自动升级为完成事实。

## 5. Why development can resume

继续开发的真正安全条件已满足：

1. G1 的正式提交存在且可追踪；
2. G2 / G3 / Shared Runtime mixed source 已明确登记，后续不会被误当成可随意删除的垃圾；
3. RD reliability 的 Accepted / Closed 事实已与整体 RD Phase 2A 分离；
4. Content Growth 的 T5-only closure 与 T1–T4 continuity 已记录；
5. Workspace Engineering 的目标态与当前未实现事实已分开；
6. primary SQLite、formal Evidence、Prototype 和 migration-source docs 未被清理；
7. generated/local cleanup 已完成低风险范围，剩余高风险对象已登记为 Owner Decision，不再阻塞开发；
8. canonical Current State、Pointer、Change Log 与本报告形成同一事实链。

没有发现需要通过 reset、clean、Shared Runtime refactor 或重新验收才能继续下一开发阶段的 P0 blocker。

## 6. Remaining non-blocking cleanup debt

- 16 个异常 Database object SQLite：仍需全表 provenance 后决定 KEEP / ARCHIVE / DELETE；
- `desktop/target/`：正式 `.app` / hand-built DMG 已识别，其余 build output retention 尚待 Owner mapping；
- `desktop/.runtime/`：需决定哪些 staging binaries / manifests 作为 packaging evidence 归档；
- `CurisCopy.app`：需确认是否为可删除的重复包装产物；
- 空 SQLite：需确认启动脚本或测试脚本是否固定引用；
- 两个 SQLite backup：需确定 archive location / retention period；
- `curis-ui-prototype.bak/`：需确定历史视觉基线保留期限；
- root Page Map / Master Map / Talent Market / Rethink docs：保持 `MIGRATION SOURCE — DO NOT COMMIT`，待 canonical migration owner 处理；
- `delivery/`、`.workbuddy/output/`、Deprecated root docs：待归档或迁移，不进入源码提交；
- `.workbuddy/memory/` 与剩余 generated / evidence 目录：继续按 owner / evidence policy 管理。

这些 debt 会影响后续仓库噪音和长期 retention，但不会导致当前 accepted source 丢失，也不会阻塞新开发开始。

## 7. Validation and commit scope

本轮允许提交的内容仅为：

- `docs/00_Context/CURRENT_STATE.md`；
- `docs/00_Context/PRODUCT_DOCUMENT_POINTER.md`；
- `docs/08_Change_Log/CHANGE_LOG.md`；
- `docs/reviews/CURIS_WORKTREE_CLEANUP_FINAL.md`。

它们只同步事实、状态、治理指针和 baseline record，不包含 G2/G3/Shared Runtime source。

提交前必须通过：

- exact staged path audit；
- `git diff --cached --check`；
- no backend / frontend / runtime / database / G2 / G3 source staged；
- current HEAD and remaining dirty scope re-check。

## 8. Next development recommendation

下一阶段优先：**Workspace Engineering P0**。

理由：

- 它已有独立 P0 Definition、Approved Candidate methodology 和 Technical Direction；
- 当前明确 `NOT IMPLEMENTED / NOT STARTED`，不会假装 reopen G2/G3 acceptance；
- 可在独立 worktree / isolated DB / bounded Issue 中证明动态 Package Runtime 的最小能力；
- RD Phase 0/1 与 long-running reliability 已收口，Content Growth T5 也已形成停止态，不应先被重新打开。

Workspace Engineering P0 只能在 Definition / Technical Direction Review 通过、输入 snapshot 冻结并创建 Allowed Files 明确的 Implementation Issue 后开始。本轮不启动 P0 实现。

## 9. Result

**WORKTREE CLEANUP CLOSED FOR THIS ROUND**

**SAFE TO RESUME DEVELOPMENT**

**PRESERVED DEVELOPMENT BASELINE ESTABLISHED**

**NO G2/G3 IMPLEMENTATION STARTED**

**NO SHARED RUNTIME REFACTOR PERFORMED**

**NO PUSH**
