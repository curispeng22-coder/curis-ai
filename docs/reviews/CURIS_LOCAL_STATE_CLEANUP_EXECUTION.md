# Curis Local State Cleanup Execution

Status: Review

Date: 2026-08-16

Hygiene commit: `a94bf6144bed0b2631bf0076204703580f3ed075`

Scope: low-risk generated-state deletion plus read-only provenance audit for local databases, Desktop evidence, artifacts, prototypes and migration sources.

## 1. Execution boundary

本轮没有：

- 处理 G2 / G3；
- 修改 Shared Runtime 或业务源码；
- 删除 primary SQLite、backup、正式 Evidence、Prototype 或 migration-source docs；
- push；
- commit 本报告。

低风险对象使用 macOS Trash 移出工作树，保留可恢复性；Trash 未清空，因此“释放空间”表示从工作树移除的空间，不声称已经永久回收磁盘空间。

## 2. Actual cleanup

### 2.1 Low-risk generated state removed from worktree

已移入 Trash：

- `desktop/runtime/__pycache__/` — 约 24 KB；
- `.workbuddy/artifacts/` — 约 4.3 MB；
- `.workbuddy/tmp/` — 约 4.2 MB；
- `.workbuddy/build/` — 约 5.0 MB；
- `.cache/` — 约 836 KB；
- `.next/` — 约 8 KB；
- `frontend/.cache/` — 约 348 KB；
- `data/issue_pipeline.sqlite-wal` — 0 bytes；
- `data/issue_pipeline.sqlite-shm` — 32 KB。

删除前检查：

- 所有目标均为工作区内普通目录或文件，不是 symlink；
- `lsof` 未发现活动进程持有相关 SQLite；
- `data/issue_pipeline.sqlite-wal` 为 0 bytes；
- read-only SQLite 检查：journal mode 为 `wal`、page count 173、freelist count 0；
- 目标均为可重建 cache / bytecode / WorkBuddy temporary output 或 stale journal sidecar。

本组从工作树移除约 **14.4 MiB**，可从 Trash 恢复。

### 2.2 Desktop intermediate DMG removed from worktree

正式 Desktop Packaging Issue 明确：`rw.*.dmg` 是构建中间文件，不接受为交付证据。且当前 Review 未引用以下具体文件：

- `desktop/target/release/bundle/macos/rw.31669.Curis_0.1.0_aarch64.dmg` — 约 576 MiB；
- `desktop/target/release/bundle/macos/rw.46167.Curis_0.1.0_aarch64.dmg` — 约 30 MiB；
- `desktop/target/release/bundle/macos/rw.93360.Curis_0.1.0_aarch64.dmg` — 约 30 MiB。

三项已移入 Trash，从工作树移除约 **635.1 MiB**。正式 `Curis.app` 和手工 DMG 未动。

### 2.3 Cleanup total

本轮从工作树移除约 **649.5 MiB**。由于使用 Trash，永久磁盘回收需另行清空 Trash；本轮未执行该操作。

## 3. Database provenance audit

### 3.1 Canonical active database

`DESKTOP-PACKAGING-001` Issue / Review 明确指定：

```text
data/curis.sqlite = unique active database
backend/data/curis.sqlite = external activity baseline / drift evidence
```

当前只读事实：

| Path | Current SHA prefix | Size | Schema tables | Selected data |
|---|---|---:|---:|---|
| `data/curis.sqlite` | `d99348dfae4fe9d4` | 1.1 MB | 96 total / 95 non-system | 2 migrations; companies/workspaces/projects/tasks currently 0 |
| `backend/data/curis.sqlite` | `a9d96a9536a5bce3` | 1.2 MB | 96 total / 95 non-system | 1 migration; 2 companies, 14 tasks, 1 workspace |

两者 hash、migration state 和业务数据不同。结论：

- `data/curis.sqlite`：**KEEP**，当前 canonical active path；
- `backend/data/curis.sqlite`：**KEEP / FORMAL EVIDENCE**，保留为不同 snapshot 的 external baseline；
- 不合并、不覆盖、不删除、不恢复 backend DB。

### 3.2 Backups

| Path | Current SHA prefix | Size | Schema tables | Final classification |
|---|---|---:|---:|---|
| `data/curis.sqlite.bak-20260806` | `b7df713b66e7d389` | 1.6 MB | 79 total / 78 non-system | **ARCHIVE** |
| `backend/data/curis.sqlite.bak-20260806` | `79520cd62b787771` | 1.1 MB | 91 total / 90 non-system | **ARCHIVE** |

两份 backup 互不相同，也都不是当前 active DB 的 byte-identical copy。它们保留 migration / historical provenance 价值，不能直接删除。

### 3.3 16 anomalous Database object SQLite files

共同事实：

- 16 个 root SQLite 文件；
- 每个 1,159,168 bytes；
- mtime 集中于 2026-08-09 08:20–10:28；
- 9 个 hash fingerprints：7 组双文件、2 个单文件；
- 代表性文件均为 96 tables / 95 non-system tables；
- representative samples 的 `companies`、`workspaces`、`projects`、`tasks` 均为 0；
- 没有活动句柄；
- 没有 Review / Issue 对具体异常文件名的引用；
- 它们不是当前 `data/curis.sqlite`、backend DB 或 backup 的 hash copy。

最终分类：**OWNER DECISION REQUIRED**。

理由：它们高度像测试 / 初始化残留，但 schema 中包含完整 Runtime / Company / Workspace 表，且尚未完成所有表的 row-level 内容与 acceptance evidence 对照。当前只完成了核心业务表抽样，证据还不足以把它们全部升级为 `SAFE TO DELETE`。

建议下一步：做一次只读的全表非空统计和 Review artifact 对照；若确认所有 16 个文件均无业务 / evidence 数据，再授权批量移入 Trash。

## 4. Desktop packaging / runtime provenance

### 4.1 Formal Evidence that must remain

Desktop Packaging Review 明确引用并验证过：

- `desktop/target/release/bundle/macos/Curis.app` — 当前约 524 MB；
- `desktop/target/release/bundle/dmg/Curis_0.1.0_manual_aarch64.dmg` — 当前约 232 MB；
- `.app` 内的 runtime、gateway、workspace、guardian 资源；
- `desktop/.runtime/runtime/BUILD-MANIFEST.json`；
- Review 中记录的 app / DMG SHA、isolated HOME、唯一 active `data/curis.sqlite` 事实。

这些对象最终分类：**KEEP / FORMAL EVIDENCE**。

### 4.2 Build output requiring retention decision

| Object | Evidence | Final classification |
|---|---|---|
| `desktop/target/` fingerprints / Cargo intermediates | 约 34,000 files；大部分为 Cargo build output | **OWNER DECISION REQUIRED** |
| `desktop/target/release/bundle/macos/CurisCopy.app` | 与正式 `Curis.app` 并存，但当前 Review 未确认其用途 | **OWNER DECISION REQUIRED** |
| `desktop/.runtime/` runtime binaries / specs | 约 13,606 files；既是可重建 staging，也是 packaging provenance 输入 | **KEEP / OWNER REVIEW** |
| `desktop/target/release/bundle/.DS_Store` 等本机杂项 | 可重建且无正式 evidence 语义 | **SAFE TO DELETE**，但本轮未处理整个 target tree |

不要因为 `desktop/target/` 被 `.gitignore` 隔离就把其中所有内容视为可删除。正式 `.app` / DMG 的复现与历史验收仍依赖该目录中的 provenance。

## 5. Evidence / prototype / migration source

| Object | Current evidence | Final classification |
|---|---|---|
| `artifacts/` | 83 files，约 192 MB，多批 audit screenshots | **KEEP / FORMAL EVIDENCE** |
| `previews/` | 1 HTML preview | **KEEP / FORMAL EVIDENCE** |
| `delivery/` | 9 delivery docs，约 644 KB；已有 reconciliation 标为 migration/historical source | **MIGRATION SOURCE** |
| `.workbuddy/output/` | 8 design/research docs | **MIGRATION SOURCE / OWNER REVIEW REQUIRED** |
| `.workbuddy/memory/` | tracked + untracked memory files | **KEEP / OWNER REVIEW REQUIRED** |
| `curis-ui-prototype/` | 204 files，约 25 MB；source、audit scripts、P0/P1 previews | **KEEP / FORMAL EVIDENCE** |
| `curis-ui-prototype.bak/` | 59 files，约 6.9 MB；与 current prototype 大量不同 | **ARCHIVE / OWNER REVIEW REQUIRED** |

`curis-ui-prototype.bak/` 不是 identical copy：current prototype 新增 `.audit`、`.workbuddy`、P1 previews、system components 和 workspace reference 页面，backup 还包含不同版本的多页 UI。因此不删除。

## 6. Root migration-source documents

已有 ownership / reconciliation evidence 将下列 root files 明确标为 `MIGRATION SOURCE — DO NOT COMMIT`：

- `Curis_Page_Map_v1.0.md`；
- `Curis_Product_Master_Map_v2.0.md`；
- `Curis_Product_Rethink_Reasoning.md`；
- `Talent_Market_Integration_Contract.md`；
- `Talent_Market_Product_Map.md`；
- `Talent_Market_Resource_Audit.md`；
- `Curis 产品与愿景资料库/`；
- `delivery/` 中尚未迁移的历史交付材料。

这些文件与 `docs/` canonical 文件存在内容或 lineage 差异。最终分类：**MIGRATION SOURCE**。不删除、不直接提交、不加入 broad ignore；后续由 canonical-document migration owner 决定归档和引用迁移。

`PROJECT_HANDOFF.md`、`PROJECT_STATUS.md`、`TASKS.md` 标记为 `Deprecated`，最终分类：**ARCHIVE / OWNER REVIEW REQUIRED**，删除前仍需检查历史引用。

## 7. Remaining Owner Decision Required

仍需 Owner 决策的对象：

1. 16 个异常 SQLite 是否完成全表 provenance 后可批量删除；
2. `desktop/target/` 中除正式 `.app` / DMG 外的 build output retention period；
3. `CurisCopy.app` 是否为可删除的重复包装产物；
4. `.runtime` staging binaries 是否要归档为 packaging evidence；
5. 两个 SQLite backup 的归档位置与 retention period；
6. `.workbuddy/output/` 的 canonical migration destination；
7. `curis-ui-prototype.bak/` 的历史视觉基线保留期限；
8. root migration-source docs 的迁移 / archive / final cleanup 时间；
9. 空 `data/quality.sqlite`、`backend/curis.sqlite`、`backend/curis_dev.db` 是否被任何本地启动或测试脚本固定引用。

## 8. Final worktree state

清理后，工作树主要仍包含：

- 68 个 tracked modifications；
- G2 / G3 / Shared Runtime mixed source；
- 约 311 个 untracked status entries（本报告新增后会再增加 1 个）；
- active / baseline / backup SQLite；
- formal artifacts、preview、正式 Desktop `.app` / DMG 和 prototype；
- migration-source docs、`.workbuddy/output/` 和 deprecated historical docs；
- `desktop/target/` / `.runtime/` 中尚未完成 retention mapping 的 packaging output。

本轮低风险生成物物理移除后，工作树没有、也不应当变成 clean baseline；剩余噪音主要已从“未知生成物”收敛为“有 provenance 但待 Owner 决策的对象”。

## 9. Result

**LOW-RISK GENERATED STATE CLEANED**

**DATABASE PROVENANCE PARTIALLY RESOLVED**

**FORMAL EVIDENCE PRESERVED**

**NO G2/G3 OR SHARED RUNTIME CHANGE**

**NO PUSH**

Next step: Owner Review the 9 remaining decisions above, starting with the 16 anomalous SQLite files and Desktop `target/.runtime` retention mapping.

