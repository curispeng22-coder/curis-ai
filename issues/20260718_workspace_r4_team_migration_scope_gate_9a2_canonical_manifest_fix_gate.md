# Workspace R4 第9项｜9a.2｜迁移资产同源清单修复 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（待质量运行席静态复核）
- 前置：`issues/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate.md`
- Owner：系统交付席（清单与引用路径）→ 质量运行席（静态复核）

## 目标

建立唯一、版本化的迁移资产清单，并给出 Codex 与 WorkBuddy 双侧对同一清单的真实引用路径。

## 约束

- 清单只能列第9项相关文档引用；不复制、移动、重建或导出实体、数据库、Secret、Key 或运行凭据。
- 必须有固定版本号、逐行资产条目、禁止项和唯一权威路径。
- Codex/WorkBuddy 两侧必须只引用同一清单版本，不维护副本。
- WorkBuddy 侧路径必须是已登记的真实路径；若当前工作区没有该路径或登记，停止并交总控决策席，不得猜测或创建伪引用。

## 验收

- 权威清单含版本、逐行资产条目、不可迁移项。
- 列出 Codex 与 WorkBuddy 的实际引用路径，均指向该同一清单。
- 质量静态复核 PASS 后才重派 9a.2；9a.3 继续冻结。

## 唯一清单与双侧引用

- 固定版本：`curis-team-migration-manifest/1.0.0`。
- 唯一权威路径：`shared/pmo/CURIS_TEAM_MIGRATION_ASSET_MANIFEST.md`。
- Codex 引用入口：本 Issue；只引用上述版本与路径，不复制清单正文。
- WorkBuddy 已登记工作区：`/Users/yy/Documents/Curis AI Workspace`；登记证据为 `/Users/yy/.workbuddy/app/sessions.json` 中现有 `workDir`。
- WorkBuddy 真实引用入口：`.workbuddy/memory/MEMORY.md`；只引用上述同一版本与路径，不维护副本。
- 范围仍仅为文档引用；未移动、复制、读取或导出实体、数据库、Secret、Key 或凭据。

## 聚焦证据

- 静态核对：清单 18 条逐行资产均真实存在；版本、权威路径、禁止项及双侧引用一致。
- `9a.3` 在本 Gate 获得质量 PASS 前继续冻结。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_team_migration_scope_gate_9a2_canonical_manifest_fix_gate.md`
Objective:
建立唯一版本化资产清单及双方真实引用证据。
Special Constraints:
只更新文档引用；WorkBuddy路径未登记即交总控，不得猜测。
Next Seat:
质量运行席

Handoff: sent to 质量运行席
