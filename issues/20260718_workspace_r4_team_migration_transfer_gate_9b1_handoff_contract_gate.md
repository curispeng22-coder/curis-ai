# Workspace R4 第9项｜9b.1｜迁移交接契约 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（唯一逐项快照已补齐；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_team_migration_transfer_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

- 固定交接文档、Issue 引用、测试链路的最小可验证契约。
- 明确交接成功必须具备的 3 件事：源头、清单、核验方式。

## 约束

- 不改历史；
- 不改运行时；
- 不修改生产数据。

## 交接契约

- 源头：父项与子项链路清单（9a.1/9a.2/9a.3）。
- 清单：每项资产标注来源文件、当前状态、下一责任人。
- 核验：收口前提供 `issues/shared/*` 和本项 Issues 的闭环引用无冲突快照。

## 验收

- 任何一项未闭环引用即视为交接缺陷，不允许第9项通过。

## 唯一逐项交接快照

- 权威清单：`shared/pmo/CURIS_TEAM_MIGRATION_ASSET_MANIFEST.md`。
- 固定版本：`curis-team-migration-manifest/1.0.0`。
- 本表只引用清单 `TM-*` 行，不复制路径/用途列，不构成第二份资产清单。
- 9a.1 已确认第9项 Issue、Review、清单和验收条件均由 `Shared` 负责；Codex/WorkBuddy 只引用，不接管或复制这些文档。

| 资产 | 权威来源 | 当前状态 | 下一责任人 | 对应第9项 Issue（manifest 条目） | `issues/shared` 冲突 | 第9项内部冲突 |
| --- | --- | --- | --- | --- | --- | --- |
| `TM-001` | `manifest/1.0.0#TM-001` | `OPEN`；9a 已 PASS，9b.1 修复中 | `Shared` | `TM-001` | `PASS(SC-01..05)` | `PASS`：父 Gate 覆盖 9a/9b/9c，无职责重叠 |
| `TM-002` | `manifest/1.0.0#TM-002` | `OPEN`；队列当前停在 9b.1 | `Shared` | `TM-002` | `PASS(SC-01..05)` | `PASS`：严格串行，9b.2 未提前启动 |
| `TM-003` | `manifest/1.0.0#TM-003` | `PASS` | `Shared` | `TM-003` | `PASS(SC-01..05)` | `PASS`：9a.1/9a.2/9a.3 已一致收口 |
| `TM-004` | `manifest/1.0.0#TM-004` | `PASS`（质量） | `Shared` | `TM-004` | `PASS(SC-01..05)` | `PASS`：Codex/WorkBuddy/Shared 职责互斥 |
| `TM-005` | `manifest/1.0.0#TM-005` | `PASS`（质量+安全） | `Shared` | `TM-005` | `PASS(SC-01..05)` | `PASS`：仅文档引用，不含实体迁移 |
| `TM-006` | `manifest/1.0.0#TM-006` | `PASS`（由 `TM-016` 复核） | `Shared` | `TM-006` | `PASS(SC-01..05)` | `PASS`：唯一版本/路径与双侧引用一致 |
| `TM-007` | `manifest/1.0.0#TM-007` | `PASS`（由 `TM-008` 汇总） | `Shared` | `TM-007` | `PASS(SC-01..05)` | `PASS`：禁止项不与可交接文档重叠 |
| `TM-008` | `manifest/1.0.0#TM-008` | `PASS` | `Shared` | `TM-008` | `PASS(SC-01..05)` | `PASS`：9a 三项无冲突，可进入 9b.1 |
| `TM-009` | `manifest/1.0.0#TM-009` | `OPEN`；9a 前置满足，9b.1 进行中 | `Shared` | `TM-009` | `PASS(SC-01..05)` | `PASS`：仅交接验收，不授权迁移实体 |
| `TM-010` | `manifest/1.0.0#TM-010` | `BLOCKED`；本快照待质量复核 | `Shared` | `TM-010` | `PASS(SC-01..05)` | `PASS`：唯一缺口由本快照补齐，范围未扩张 |
| `TM-011` | `manifest/1.0.0#TM-011` | `FROZEN`；等待 9b.1 质量 PASS | `Shared` | `TM-011` | `PASS(SC-01..05)` | `PASS`：仅保留定义，未提前执行回滚动作 |
| `TM-012` | `manifest/1.0.0#TM-012` | `FROZEN`；等待 9b.1 质量 PASS | `Shared` | `TM-012` | `PASS(SC-01..05)` | `PASS`：敏感资产仍在禁止范围内 |
| `TM-013` | `manifest/1.0.0#TM-013` | `FROZEN`；等待 9b.1/2/3 复核 | `Shared` | `TM-013` | `PASS(SC-01..05)` | `PASS`：未提前汇总或宣称 9b 完成 |
| `TM-014` | `manifest/1.0.0#TM-014` | `OPEN`；等待 9b 汇总 | `Shared` | `TM-014` | `PASS(SC-01..05)` | `PASS`：9c 未提前启动 |
| `TM-015` | `manifest/1.0.0#TM-015` | `PASS`（9a.1 质量证据） | `Shared` | `TM-004` | `PASS(SC-01..05)` | `PASS`：证据与职责边界一致 |
| `TM-016` | `manifest/1.0.0#TM-016` | `PASS`（9a.2 质量证据） | `Shared` | `TM-005` | `PASS(SC-01..05)` | `PASS`：18 项清单与双侧引用已核验 |
| `TM-017` | `manifest/1.0.0#TM-017` | `PASS`（9a.2 安全证据） | `Shared` | `TM-005` | `PASS(SC-01..05)` | `PASS`：数据库/凭据/实体明确排除 |
| `TM-018` | `manifest/1.0.0#TM-018` | `ACTIVE`；仅作当前 Gate 指针 | `Shared` | `TM-001` | `PASS(SC-01..05)` | `PASS`：不复制历史正文，不承担迁移实体 |

## `issues/shared` 冲突核对集

| 核对项 | 路径 | 当前状态 | 与第9项逐项结果 |
| --- | --- | --- | --- |
| `SC-01` | `issues/shared/20260717_admin_company_package_verify.md` | `VERIFIED/CLOSED` | `PASS`：运行态消费证据，不是迁移资产，不复制或移动 |
| `SC-02` | `issues/shared/20260717_admin_orphan_instances.md` | `VERIFIED/CLOSED` | `PASS`：历史处置证据，不授权数据迁移或删除 |
| `SC-03` | `issues/shared/20260717_admin_r3_e2e_handoff.md` | `OPEN` | `PASS`：R3 执行交接，不属于第9项文档迁移范围 |
| `SC-04` | `issues/shared/20260717_admin_workspace_stash_handoff.md` | `CLOSED — RETAINED / DO_NOT_APPLY_OR_POP` | `PASS`：与“不迁移实体/不恢复 stash”一致 |
| `SC-05` | `issues/shared/20260717_workspace_shared_main_manual_merge_preparation.md` | `DUAL_LEAD_PASS` | `PASS`：共享代码合并证据；第9项不修改代码或 PR |

## 快照边界

- `SC-01..05` 仅是冲突核对集，不加入 manifest，不复制为迁移资产。
- 任一 `TM-*` 或 `SC-*` 状态变化后必须重新静态复核；不得据此自动移动文件、恢复 stash、读取数据库或凭据。
- 本快照只交接文档责任与状态，不交接实体内容。
- `9b.2` 在本 Gate 质量 PASS 前继续冻结。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_team_migration_transfer_gate_9b1_handoff_contract_gate.md`
Objective:
定义迁移交接的最小可核验契约。
Special Constraints:
仅定义文档与交接口径。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
