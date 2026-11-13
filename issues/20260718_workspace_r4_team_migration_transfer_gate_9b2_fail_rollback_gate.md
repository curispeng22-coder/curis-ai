# Workspace R4 第9项｜9b.2｜迁移失败回滚 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（静态失败判定矩阵已补齐；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_team_migration_transfer_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

- 定义迁移过程遇阻时的可接受回滚与失败处理边界。
- 不允许无记录回滚或部分成功隐匿。

## 约束

- 不执行任何系统操作；
- 不新增恢复脚本。

## 失败处理

- 缺失交接契约、资产映射冲突、状态锁缺失时，必须阻断第9项并退回 9a/9b 修改。
- 只要出现未闭环引用，状态必须保持 `BLOCKED`（不得标记 PASS/完成或误写为 OPEN）。
- 回退动作仅为口径修订与清单修正，不可擅自改写历史记录。

## 静态失败判定矩阵

| check_id | trigger | expected_state | allowed_action | forbidden_action |
| --- | --- | --- | --- | --- |
| `TM-9B2-001` | 缺交接契约：9b.1 契约文件、唯一逐项快照或任一必需字段不存在 | `BLOCKED` | 仅修订交接契约文档或其引用 | 迁移实体、改写历史、导出凭据、执行回退脚本、标记 `PASS` |
| `TM-9B2-002` | 资产映射冲突：任一 `TM-*` 的 manifest 权威来源与交接快照映射不一致、重复或指向不同版本/路径 | `BLOCKED` | 仅修订权威清单、交接文档或引用，使映射恢复唯一一致 | 迁移实体、改写历史、导出凭据、执行回退脚本、标记 `PASS` |
| `TM-9B2-003` | 状态锁缺失：前置质量未 PASS 时，9b.2/9b.3/9b 汇总的 `BLOCKED` 或 `FROZEN` 锁缺失，或失败项被写为 `OPEN`/完成/`PASS` | `BLOCKED` | 仅修订状态锁文档或其引用 | 推进 9b.3、迁移实体、改写历史、导出凭据、执行回退脚本、标记 `PASS` |
| `TM-9B2-004` | 未闭环引用：任一 manifest 条目、第9项 Issue/Review 或 `issues/shared/*` 引用缺失、不可解析、无责任人/状态，或冲突核对未闭环 | `BLOCKED` | 仅补正文档、清单或引用并重新静态核对 | 忽略缺口继续、迁移实体、改写历史、导出凭据、执行回退脚本、标记 `PASS` |

判定规则：任一 trigger 命中即保持 `BLOCKED`；四项均未命中也不由本矩阵授予 `PASS`，只允许质量运行席继续静态复核。

## 验收

- 失败案例有明确定义且可复用为 check 规则（不是临时说明）。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_team_migration_transfer_gate_9b2_fail_rollback_gate.md`
Objective:
定义迁移失败与回退边界，禁止部分完成。
Special Constraints:
仅静态表；不执行回退动作，不迁移实体。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
