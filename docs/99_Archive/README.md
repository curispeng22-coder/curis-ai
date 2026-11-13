# Curis Documentation Archive

Status: Frozen
Authority Class: CURRENT / ARCHIVE INDEX
Owner: Workspace Governance

Historical index baseline:
main @ 8ac3b814

Updated: 2026-10-25

---


## 2026-10-25 — CEO 已批准的三份旧根文档归档

只归档原清单 A01–A03，完整历史正文与原日期保留；正文相对导航链接按新位置换算，原始字节前像及可逆映射均保存。当前根路径留简短兼容导航，非第二套状态/任务队列。
来源：CEO 明确确认 / [既有维护决定的续执行登记](<../07_Decisions/DECISION-2026-10-25-development-baseline-doc-maintenance.md>) / [同一正式 Issue](<../../issues/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025.md>)。

| ID | 历史归档 | 保留入口 | 归档分类 |
|---|---|---|---|
| A01 | [PROJECT_STATUS.md](<development-baseline-2026-10-25/root-legacy-docs/PROJECT_STATUS.md>) | [原路径兼容指针](<../../PROJECT_STATUS.md>) | Deprecated / HISTORY |
| A02 | [PROJECT_HANDOFF.md](<development-baseline-2026-10-25/root-legacy-docs/PROJECT_HANDOFF.md>) | [原路径兼容指针](<../../PROJECT_HANDOFF.md>) | Deprecated / HISTORY |
| A03 | [TASKS.md](<development-baseline-2026-10-25/root-legacy-docs/TASKS.md>) | [原路径兼容指针](<../../TASKS.md>) | Deprecated / HISTORY |

[迁移回证](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/MIGRATION_RECEIPT.json>) / [引用与保全](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/CHECK_RESULTS.json>) / [结果](<../../artifacts/tasks/CURIS-V1-DEV-BASELINE-CONSOLIDATION-20261025/archive-a01-a03/RESULT.md>)。
恢复仅在未来精确授权下从前像恢复原路径，或按回证逆变换链接；不得自动覆盖后续用户编辑。其他目录及既有历史材料不动，无删除，模型 DEFERRED。
以下 July/September 段落属于原阶段历史，不扩大当前归档集合。

## Purpose

`docs/99_Archive/` is the governed destination for historical material that no
longer defines the current Curis product, architecture, design or development
process.

The directory preserves decision provenance and evidence. It is not a second
source of current truth.

## Historical Document Rules

- Product Truth follows Product Document Pointer; implementation facts remain in CURRENT_STATE. Archive material does not override either.
- Applicable domain standards follow the current Entrypoint / Pointer and lawful Frozen authority.
- Superseded standards use `Status: Deprecated`.
- Completed Issue, Review and Release evidence may retain `Status: Frozen`,
  but Archive placement removes current-standard authority.
- Deprecated or archived content cannot override a Frozen document.
- Historical decisions are preserved, not deleted.
- A file may move here only after repository references, scripts, CI, tests and
  build configuration are checked.
- Every migration requires an explicit old-path/new-path record and separate
  confirmation.

Phase 3-A created this index without moving historical files.

Phase 3-B1 migrated 17 Deprecated, non-ADR Markdown files from
`curis_workspace_blueprint/` into
`docs/99_Archive/curis_workspace_blueprint/`. The two historical ADR files
remain at `curis_workspace_blueprint/ADR/`.

Phase 3-C1 migrated 200 assets marked `Safe Move` by the Phase 3-B2 asset
analysis:

- 172 Deprecated UI V2 assets to `docs/99_Archive/design/curis-ui-v2/`
- 17 CEO Office historical design assets to
  `docs/99_Archive/design/ceo-office/`
- 7 standalone diagram prototypes to
  `docs/99_Archive/prototypes/diagrams/`
- 4 historical Handoff/governance documents to
  `docs/99_Archive/handoff/`

Phase 3-C2 reviewed the remaining non-delete Human Confirmation cohort:

- 160 historical assets are recommended for later coherent-package archive
  migration and remain at their current paths
- 16 WorkBuddy Memory records remain protected at their tool-owned paths
- `deploy/curis/releases/` remains protected pending release-owner review

Phase 3-C3 reviewed all 41 Delete Candidates:

- 35 regenerable, redundant or temporary assets were approved and removed
- 6 dependency paths remain protected:
  - `.venv/`
  - `backend/.venv/`
  - `frontend/.next/`
  - `frontend/node_modules/`
  - `frontend/ceo-evidence/node_modules/`
  - `frontend/ceo-evidence/dist/assets/`

Tracked deletions remain recoverable through Git history. Ignored assets were
moved to the system Trash before finalization. `.obsidian/` is user-local state
and is outside Documentation Governance.

Documentation Governance status: `Completed — v1.0`.

## Query

Start with:

1. AGENTS.md → docs/00_Context/CURIS_CURRENT_ENTRYPOINT.md
2. The task-specific Product Pointer / CURRENT_STATE and applicable Frozen authority
3. docs/00_Context/DOCUMENT_INVENTORY.md

Search historical material only when needed:

```bash
rg -n "search term" docs/99_Archive
rg -n "search term" docs knowledge reviews issues
rg -n "Status: Deprecated" --glob '*.md'
```

When citing history, include the exact path, document status and date. Do not
describe an archived or Deprecated statement as current behavior.
