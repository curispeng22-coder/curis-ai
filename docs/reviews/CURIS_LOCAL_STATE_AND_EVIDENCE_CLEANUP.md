# Curis Local State and Evidence Cleanup Review

Status: Review

Date: 2026-08-16

Hygiene commit: `a94bf6144bed0b2631bf0076204703580f3ed075`

Scope: primary / local SQLite、数据库备份、异常 SQLite、Evidence、Prototype、WorkBuddy 和根目录迁移来源的 retention 分类。

## 1. Execution boundary

已完成：

- 提交 Repository Hygiene：`chore(repo): isolate generated and local runtime output`；
- 对目标对象做只读 inventory、文件类型、大小、mtime、hash、引用和原型差异检查；
- 生成本 Review 报告。

本轮没有：

- 删除任何文件；
- 修改 G2 / G3；
- 修改 Shared Runtime；
- 修改数据库内容；
- push；
- 重新 staging 或 commit 本报告。

本轮工作树仍保持 dirty，所有高风险或来源不明对象留待 Owner Review。

## 2. Current evidence snapshot

提交 hygiene 后工作树：

- tracked worktree modifications：68；
- index changes：0；
- `git status --short` untracked entries：310；
- `git ls-files --others --exclude-standard` exact untracked files：880；
- 当前没有 staged path。

审计时没有发现进程持有下列 SQLite 文件的活动句柄。该结果只说明审计时没有检测到活动句柄，不等同于数据库已获准删除。

## 3. Final retention classification

### 3.1 Primary / local SQLite

| Object | Evidence | Final classification | Decision |
|---|---|---|---|
| `data/curis.sqlite` | 1.1 MB，2026-08-16 更新，SQLite user_version 1，file counter 470 | **KEEP** | 当前主要本地数据库；保留，不加入 ignore，不删除 |
| `backend/data/curis.sqlite` | 1.2 MB，2026-08-15 更新，SQLite user_version 1，file counter 691 | **FORMAL EVIDENCE** | 与 `data/curis.sqlite` 不同快照；保留用于 provenance / Runtime evidence review |
| `data/issue_pipeline.sqlite` | 692 KB，2026-08-09 更新，SQLite file counter 93 | **KEEP** | Issue pipeline 本地状态；保留 |
| `data/b_layer_pending_decisions.sqlite` | 32 KB，SQLite file counter 31 | **KEEP** | Pending decision 本地状态；保留 |
| `data/quality.sqlite` | 0 bytes，empty | **DELETE CANDIDATE** | 看起来是空的本机残留，但仍需确认没有被固定路径或脚本依赖；本轮不删 |
| `backend/curis.sqlite` | 0 bytes，empty | **DELETE CANDIDATE** | 空数据库残留；需确认 backend 启动配置不会重新使用该路径；本轮不删 |
| `backend/curis_dev.db` | 0 bytes，empty | **DELETE CANDIDATE** | 空开发数据库残留；需 Owner 确认后删除 |

结论：主 SQLite 不删除、不提交、不重新加入 broad ignore。空数据库可以作为低风险 delete candidate，但尚未满足“来源和路径依赖已确认”的删除条件。

### 3.2 DB backups and journal files

| Object | Evidence | Final classification | Decision |
|---|---|---|---|
| `backend/data/curis.sqlite.bak-20260806` | 1.2 MB，2026-08-06，SQLite snapshot | **ARCHIVE** | 保留到确认正式 evidence 已抽取；不删除 |
| `data/curis.sqlite.bak-20260806` | 1.6 MB，2026-08-06，SQLite snapshot，free pages 115 | **ARCHIVE** | 与 backend backup 不同；保留并记录 provenance |
| `data/issue_pipeline.sqlite-wal` | 0 bytes，SQLite WAL sidecar | **DELETE** | 明确 journal 残留，且审计时无活动句柄；本轮仍未物理删除 |
| `data/issue_pipeline.sqlite-shm` | 32 KB，SQLite shared-memory sidecar | **DELETE CANDIDATE** | 无活动句柄但不是空文件；删除前确认 issue pipeline 未在运行并保留主库快照；本轮不删 |

WAL / SHM 已由 `.gitignore` 隔离，但物理清理仍需独立、可回滚的 cleanup 操作。

### 3.3 16 anomalous Database object SQLite files

根目录存在 16 个形如：

```text
<app.database.Database object at 0x...>
```

共同事实：

- 数量：16；
- 每个约 1.1 MB（1,159,168 bytes）；
- 生成时间集中在 2026-08-09 08:20–10:28；
- `file` 识别为 SQLite 3.x database；
- `.gitignore` 已不再隐藏它们；
- 当前没有活动句柄被检测到。

最终分类：**DELETE CANDIDATE**。

不能在本轮删除的原因：

- 文件名来自异常 database path handling，但不能仅凭文件名证明内容已被其他数据库完整覆盖；
- 可能对应此前 Runtime / acceptance runs 的独立 evidence snapshot；
- 尚未完成 table-level 内容、hash 关系、Review 引用和 retention owner 对照。

下一步应先做只读 SQLite schema / record provenance 对照，并由 Evidence owner 确认后再批量删除或归档。

### 3.4 Artifacts / previews / delivery

| Object | Evidence | Final classification | Decision |
|---|---|---|---|
| `artifacts/` | 约 192 MB，多批 screenshot / audit artifact | **FORMAL EVIDENCE** | 保留；不得加入 broad ignore 或删除 |
| `previews/` | `ui-spec-preview.html` 等 preview material | **FORMAL EVIDENCE** | 保留到对应 Review 明确归档 / 过期 |
| `delivery/` | 约 644 KB，设计 / 研究交付文档 | **MIGRATION SOURCE** | 保留作为交付来源；需迁移 owner 确认 canonical 去向 |

这些对象不能因为“可重新生成”就直接删除。部分内容可能是历史验收、视觉比对或产品研究证据。

### 3.5 Desktop packaged tree

| Object | Evidence | Final classification | Decision |
|---|---|---|---|
| `desktop/` source tree | 约 5.5 GB；包含 Cargo / package manifest、runtime source、icons、scripts、build output | **FORMAL EVIDENCE / OWNER REVIEW** | 根目录不删除；源码和 package inputs 保留 |
| `desktop/target/` | 约 4.7 GB Rust build output | **FORMAL EVIDENCE** | 可能含 packaged / runtime acceptance material；不删除，先做 evidence retention mapping |
| `desktop/node_modules/` | 约 29 MB dependency output | **KEEP** | 可重建且已 ignore；本轮不物理删除 |
| `desktop/.runtime/` | 约 742 MB recreated packaging/runtime output | **FORMAL EVIDENCE** | 可能是 Desktop packaging evidence；不删除 |
| `desktop/runtime/__pycache__/` | Python bytecode cache | **DELETE** | 明确可重建；已 ignore；本轮不物理删除 |

`desktop/target/` 与 `.runtime/` 的大小很大，但大小本身不是删除授权。需要先确认是否仍被 Desktop Review、packaging evidence 或复现流程引用。

### 3.6 `.workbuddy/`

| Object | Evidence | Final classification | Decision |
|---|---|---|---|
| `.workbuddy/memory/` | 既有 tracked memory，也有 untracked 日期文件 | **OWNER REVIEW** | 不 broad ignore；保留可见性，按 owner / memory policy 处理 |
| `.workbuddy/output/` | 设计 / 研究类中文文档 | **MIGRATION SOURCE / FORMAL EVIDENCE** | 不隐藏、不删除；确认是否迁移至 canonical docs 或 evidence archive |
| `.workbuddy/artifacts/`、`.workbuddy/tmp/`、`.workbuddy/build/` | 本机生成目录 | **DELETE** | 可重建本地输出，已有窄规则隔离；本轮不物理删除 |

不能把整个 `.workbuddy/` 目录统一删除或 ignore，因为其中同时存在记忆、研究来源和生成物。

### 3.7 Prototype and backup

| Object | Evidence | Final classification | Decision |
|---|---|---|---|
| `curis-ui-prototype/` | 约 25 MB，当前 prototype source、audit scripts、p0/p1 previews、workspace reference pages | **FORMAL EVIDENCE** | 保留；它仍是 UI 研究与验收参考，不等于正式产品代码 |
| `curis-ui-prototype.bak/` | 约 6.9 MB，与当前 prototype 有大量差异；当前版本多出 `.audit`、`.workbuddy`、p1 preview 和多个系统组件 | **ARCHIVE / OWNER REVIEW** | 不能直接删除；先确认是否是唯一历史视觉基线 |

backup 与当前 prototype 并非 identical copy，因此不能按“重复目录”删除。

## 4. Root migration-source duplicate docs

以下根目录文件与 canonical `docs/` 文件名相近但内容不同，且已有 reconciliation evidence 将它们记录为迁移来源，不应直接提交为当前产品真相：

| Root object | Final classification | Reason |
|---|---|---|
| `Curis_Page_Map_v1.0.md` | **MIGRATION SOURCE** | 与 `docs/01_Product/Curis_Product_Page_Map_v1.0.md` diverged；canonical 已由 Pointer 指定 |
| `Curis_Product_Master_Map_v2.0.md` | **MIGRATION SOURCE** | 与 canonical Master Map diverged；根目录文件是 rebaseline 输入 / 来源 |
| `Curis_Product_Rethink_Reasoning.md` | **MIGRATION SOURCE** | 产品重新推导阶段交付，不是当前 canonical Blueprint |
| `Talent_Market_Integration_Contract.md` | **MIGRATION SOURCE** | 与 `docs/01_Product/Curis_Talent_Market_Integration_Contract.md` diverged |
| `Talent_Market_Product_Map.md` | **MIGRATION SOURCE** | 与 canonical Talent Market map diverged |
| `Talent_Market_Resource_Audit.md` | **MIGRATION SOURCE** | 与 canonical Talent Market audit diverged |
| `Curis 产品与愿景资料库/` | **MIGRATION SOURCE** | 产品事实、愿景和选题原始资料库，不是 canonical docs root |
| `docs/99_Archive/overview-curis-ui-prototype-freeze-delivery-2026-08-04.md` | **ARCHIVED EVIDENCE** | 原型冻结整改交付概览；已按 Wave 3 迁入治理归档 |
| `PROJECT_HANDOFF.md`、`PROJECT_STATUS.md`、`TASKS.md` | **ARCHIVE** | 明确 `Status: Deprecated` 的历史治理来源；删除前需查引用 |

这些文件不删除、不加入 `.gitignore`、不直接 stage。迁移工作应由单独的 canonical-document migration task 完成。

## 5. What can be safely deleted

有充分生成物证据、且不涉及正式业务数据的对象：

- `desktop/runtime/__pycache__/`；
- `.workbuddy/artifacts/`、`.workbuddy/tmp/`、`.workbuddy/build/`；
- `.cache/`、`.next/`、`frontend/.cache/`；
- 经过无活动句柄确认后的空 WAL sidecar；
- 经确认无未 checkpoint 数据后的 stale SHM sidecar。

本轮没有执行这些物理删除。原因是当前任务重点是 Review / retention 收口，且删除大目录或本机状态应使用独立、可回滚的 cleanup authorization。

## 6. What should be archived

- 两个 `curis.sqlite.bak-20260806` 数据库备份；
- `curis-ui-prototype.bak/`，至少在历史视觉基线 owner 确认前；
- `PROJECT_HANDOFF.md`、`PROJECT_STATUS.md`、`TASKS.md` 等 Deprecated 根目录历史文档；
- 经 evidence owner 确认不再 active 的旧 packaged Desktop output；
- 已完成迁移、但仍需保留 provenance 的 `delivery/` 与 `.workbuddy/output/` 来源材料。

## 7. What should be kept

- `data/curis.sqlite` 当前主要本地数据库；
- `data/issue_pipeline.sqlite`、`data/b_layer_pending_decisions.sqlite`；
- `backend/data/curis.sqlite` 作为不同 snapshot 的证据，直到 provenance 收口；
- `artifacts/`、`previews/` 和仍被 Review 引用的 `delivery/`；
- Desktop source / package inputs；
- `curis-ui-prototype/` 当前 prototype；
- 所有仍有 owner 或 evidence 引用的文档与数据库。

## 8. Owner Decision still required

以下对象不能由本轮自行删除或定为最终 archive：

1. 16 个异常 Database object SQLite 是否为可丢弃测试快照；
2. `backend/data/curis.sqlite` 与 `data/curis.sqlite` 谁是当前 active / evidence source；
3. 两个 DB backup 的 retention period 和归档位置；
4. `desktop/target/` 与 `desktop/.runtime/` 哪些文件属于正式 Desktop evidence；
5. `artifacts/`、`previews/`、`delivery/` 是否已完成 evidence migration；
6. `.workbuddy/output/` 是否迁移至 canonical docs 或 evidence archive；
7. `curis-ui-prototype.bak/` 是否保留为历史视觉基线；
8. 根目录 migration-source docs 何时迁移、归档或最终清理；
9. 空 SQLite 文件是否被启动脚本、测试脚本或本地工具固定引用。

## 9. Expected worktree after approved cleanup

即使执行所有低风险生成物清理，工作树仍会保留以下主要类别：

- G2 / G3 mixed business and Shared Runtime source；
- tracked product / architecture / frontend modifications；
- accepted / Review Required Issue and Review records；
- primary / evidence SQLite 与经过批准归档的 backups；
- formal `artifacts/`、preview、packaged Desktop evidence；
- prototype 与已确认的历史视觉基线；
- canonical docs 的 owner-review 修改；
- migration-source docs，直到 canonical migration 完成。

因此，低风险生成物清理只能减少噪音，不能把当前工作树变成可整体提交的 clean baseline。

## 10. Final result

**HYGIENE COMMITTED**

**LOCAL STATE / EVIDENCE REVIEW COMPLETE**

**NO HIGH-RISK DELETE PERFORMED**

**G2/G3 UNTOUCHED**

**SHARED RUNTIME UNTOUCHED**

Next step: Owner Review the DELETE / ARCHIVE / MIGRATION SOURCE decisions above; only then authorize a narrow cleanup operation.
