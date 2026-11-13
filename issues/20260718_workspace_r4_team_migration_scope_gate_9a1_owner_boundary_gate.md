# Workspace R4 第9项｜9a.1｜迁移职责边界 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_team_migration_scope_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

- 明确 Codex 与 WorkBuddy 在迁移中的分工边界与可接收范围。
- 固定对项目长期运行资产（Issue、Review、测试、成果）不跨团队混改的责任线。

## 约束

- 不改历史；
- 不改运行时；
- 不新增模型/凭据/网关。

## 目标边界

- Codex 侧负责 Workspace runtime 的可复用交付、长期状态/记忆约束与结果验收边界说明。
- WorkBuddy 侧负责 Admin 官方资产、模板目录、官方包与只读清单交接说明。
- 共享侧只输出迁移契约、清单与验收条件，不承担各自运行实现。

## 验收

- 9a.1 完成后，9a 下游子任务必须直接引用该职责边界文本，且不得出现边界重叠。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_team_migration_scope_gate_9a1_owner_boundary_gate.md`
Objective:
冻结 Codex 与 WorkBuddy 的迁移责任边界。
Special Constraints:
仅边界定义；不改运行时。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
