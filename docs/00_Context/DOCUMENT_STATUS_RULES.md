# Curis Document Status Rules

Status: Frozen
Authority Class: FROZEN / DOCUMENT GOVERNANCE
Owner: Delivery Owner（本次导航维护）
Baseline: 既有 AGENTS 真相分层；本轮 Git 观察见 CURRENT_STATE，不以提交号定义 Product Truth
Updated: 2026-10-25
Decision: [2026-10-25 文档维护决定](<../07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>)

## 1. Allowed Status Values

Every core Markdown document must contain one status line near the title:

```text
Status: Draft
Status: Review
Status: Frozen
Status: Deprecated
```

### Draft

- 内容尚未完整
- 不能作为实现授权
- 不能覆盖 Frozen 文档

### Review

- 内容完整但尚未确认
- 可以用于评审
- 不能覆盖 Frozen 文档

### Frozen

- 当前有效标准或已经冻结的事实记录
- 可以作为实现、验证或治理依据
- 修改必须同步更新 Decision 和 Change Log

### Deprecated

- 已被新方案替代
- 只保留历史背景和追溯价值
- 不得作为当前实现或产品判断依据

## 2. Archive Rule

`Archive` 是文档处置位置，不是第五种 Status。

被替代的标准进入 `docs/99_Archive/` 时必须使用：

```text
Status: Deprecated
```

已完成的 Issue、Review 和 Release Evidence 可以保持 `Frozen`，但迁入 Archive 后只能
作为历史证据，不能成为当前产品标准。

`docs/99_Archive/README.md` 是 Archive 查询与治理入口，使用 `Status: Frozen`；
它不是被归档的历史内容。

## 3. Authority Routing

依据 [AGENTS](<../../AGENTS.md>) §1/2，先区分事实类别，不能用一个跨类排序让实现现状覆盖产品目标。

- Product Truth：Pointer → Product Blueprint → Master Map → UI Blueprint → 适用 Frozen Authority。
- Implementation Truth：CURRENT_STATE → 当前 Issue / Allowed Files / Approved Design → Code / Runtime → Accepted Evidence。
- Research / Review / History 只解释背景和当时证据；不因 Status、文件名或时间较新自动覆盖 Current。
- 同类 Current / Frozen Authority 冲突时 STOP / REPORT AUTHORITY CONFLICT；不能自行选择或创建第三种真相。
- Product 与 Implementation 不一致，登记 PRODUCT → IMPLEMENTATION GAP，不反向改写任一类事实。

原 2026-07-30 通用顺序的跨类表述由本轮 CEO 文档授权下的维护决定明确收窄；本节不改变产品模型、验收标准或任何领域 Frozen 合同。

## 4. Required Header

新建核心文档至少包含：

```text
# Title

Status: Draft | Review | Frozen | Deprecated

Baseline: main @ <full-sha>

Updated: YYYY-MM-DD
```

涉及具体模块时还应包含：

```text
Module: <module-name>
Owner: <owner-or-seat>
Supersedes: <path-or-none>
```

## 5. Status Transition

```text
Draft
→ Review
→ Frozen
→ Deprecated
→ docs/99_Archive/
```

- `Draft → Review`：作者完成自检
- `Review → Frozen`：Owner 或授权评审确认
- `Frozen → Deprecated`：新 Decision 明确替代
- `Deprecated → Archive`：完成引用审计并确认不再被代码或脚本依赖

## 6. Change Requirements

修改 Frozen 文档时必须：

1. 说明变更原因
2. 更新或新增 Decision
3. 更新 Change Log
4. 检查所有路径引用
5. 确认不改变未授权产品逻辑
6. 在需要时更新 `CURRENT_STATE.md`

## 7. Historical Evidence

- Issue：执行范围和验收标准
- Review：当时的验证证据
- Release：当时的发布事实
- Research：当时的研究结论
- Prototype：当时的设计探索

这些文档可以有效且可追溯，但不自动成为当前标准。

## 8. File Movement Rule

任何移动、重命名或删除前必须：

1. 使用 `rg` 检查仓库内引用
2. 检查脚本、CI、测试、构建和运行配置
3. 建立旧路径到新路径的迁移表
4. 一次只迁移一个文档域
5. 完成验证后再进入下一批

本规则禁止为了目录整洁一次性移动全部历史文档。

## 9. Document Classes And Metadata Contract

Every durable document belongs to one class: `CURRENT`, `FROZEN`, `RESEARCH`, `REVIEW`, `HISTORY`, or `EVIDENCE`. Use the existing status vocabulary above; `Authority Class` describes the document’s role and does not grant promotion by itself. Core documents include `Authority Class`, `Status`, `Owner` where applicable, source/baseline, and `Supersedes` when replacing another document. Task outputs include Task ID, allowed scope, disposition, and target authority/backlog when applicable.

Filenames and labels such as `FROZEN`, `FINAL`, `MASTER`, `CURRENT`, `ACCEPTED`, `LATEST`, or version numbers do not create Authority. Only the lawful decision and current Pointer / Authority chain establish current truth.

## 10. Lifecycle, Promotion, And Supersession

- `Draft → Review → Frozen → Deprecated → Archive` remains the lifecycle; every transition has an accountable Owner/decision and traceable source.
- Promotion requires explicit acceptance, a named target Authority or canonical Backlog, exact scope, evidence, and synchronized links / Change Log. A review or prototype is not promoted by filename or age.
- A successor records what it fully or partially replaces, what remains current or unique, and its Decision/Closure provenance. Product, visual, interaction, implementation, and source replacement are assessed separately.
- On conflict, follow the applicable Current Authority and its provenance. If the lawful successor cannot be proven, retain the older item as `REVIEW_REQUIRED`; do not choose by modification time.

## 11. Decision Evidence And Historical Retention

- Preserve CEO Decisions, Authority provenance, Closures / Decision Records, and only the minimum irreplaceable evidence needed to explain them.
- Historical Explorations may close while current visual or interaction sources remain active. Mark each accepted visual input explicitly in the governing Authority; do not make all historical HTML / exports default inputs.
- A closed Exploration’s ordinary reproducible screenshots, captures, HTML/CSS/JS, exports, and duplicate packages do not require permanent retention when an exact successor and replacement scope are proven and Decision/Closure provenance is retained.
- Before any historical artifact deletion, verify: lawful successor; replacement scope; conclusions absorbed into Current Authority or Decision Record; no unique editable source/evidence; no uncommitted or untracked protected work; no Current Authority reference requiring the path; a CEO-approved exact cleanup set; and a recorded rollback or `IRREVERSIBLE` decision.
- Screenshot retention is zero by default when the decision is fully explained and reproducible; retain only the smallest necessary set, normally one to three images, when they preserve otherwise unavailable Decision Evidence. Do not keep a full capture batch by default.
- Archive only material with recovery or provenance value, outside Active Workspace when that is the approved goal. Record original path, checksum, reason, successor, owner, restore condition, and verified destination/backup. Archive is not a status and must not remain on the default input route.
- `DELETE_CANDIDATE` is not approval. Every skipped/removed set is recorded in `CURIS_CLEANUP_LEDGER.md`; Gate 0 retention permission never authorizes a specific Gate 4 set by itself.
