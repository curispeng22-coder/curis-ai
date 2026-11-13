# Workspace R4 第9项｜9a.2｜迁移资产范围 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_team_migration_scope_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

- 固定可迁移与不可迁移资产清单（文档、Issue、约束、验收证据）。
- 避免资产混合迁移导致历史链路不可追溯。

## 约束

- 不改历史数据；
- 不改历史调用链；
- 不移动生产运行实体。

## 资产范围

- 可迁移：`issues/*`、`knowledge/*` 中与第9项相关的收口说明、`reviews/*` 的收口契约。
- 不可迁移：Admin 正式生产数据库、Workspace 历史执行 DB、已归档 Secret / Key / 运行凭据。
- 变更规则：仅做“引用关系”更新，不做“实体转移”。

## 验收

- 双侧文档必须出现相同清单版本（同源同一行级口径）。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_team_migration_scope_gate_9a2_artifact_scope_gate.md`
Objective:
冻结迁移资产边界清单。
Special Constraints:
仅定义可迁移边界，拒绝跨库搬运。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
