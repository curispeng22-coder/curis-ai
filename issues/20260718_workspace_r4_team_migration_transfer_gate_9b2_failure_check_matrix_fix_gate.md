# Workspace R4 第9项｜9b.2｜失败判定矩阵修复 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（待质量运行席静态复核）
- 前置：`issues/20260718_workspace_r4_team_migration_transfer_gate_9b2_fail_rollback_gate.md`
- Owner：系统交付席（静态判定表）→ 质量运行席（静态复核）

## 目标

把 9b.2 的失败场景固化为可重复的静态 check 矩阵；不新增脚本或执行动作。

## 每条必须字段

- `check_id`
- `trigger`（可识别的触发条件）
- `expected_state`（唯一值 `BLOCKED`）
- `allowed_action`
- `forbidden_action`

## 最小覆盖

1. 缺失交接契约。
2. 资产映射冲突。
3. 状态锁缺失。
4. 未闭环引用。

## 约束

- 允许动作仅限修订文档口径、清单或引用；不得移动/复制实体、改写历史、导出凭据、执行回退脚本或标记 PASS。
- 每个 trigger 只能命中一个 `expected_state=BLOCKED`，不得保留模糊“可继续”路径。

## 验收

- 四类失败均有完整五字段静态表项。
- 质量复核可仅凭表复现判定；PASS 后才重派 9b.2，9b.3 继续冻结。

## 实施证据

- 唯一矩阵位置：`issues/20260718_workspace_r4_team_migration_transfer_gate_9b2_fail_rollback_gate.md`。
- 固定 check：`TM-9B2-001..004`，分别覆盖缺交接契约、资产映射冲突、状态锁缺失、未闭环引用。
- 四项 `expected_state` 均固定为 `BLOCKED`；允许动作仅为文档、清单或引用修订。
- 禁止实体迁移、历史改写、凭据导出、回退脚本及由本矩阵标记 `PASS`；`9b.3` 继续冻结。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_team_migration_transfer_gate_9b2_failure_check_matrix_fix_gate.md`
Objective:
补齐可重复的失败判定矩阵。
Special Constraints:
仅静态表；不写脚本、不执行回退。
Next Seat:
质量运行席

Handoff: sent to 质量运行席
