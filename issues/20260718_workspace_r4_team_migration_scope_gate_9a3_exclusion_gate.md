# Workspace R4 第9项｜9a.3｜不可迁移项与依赖 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_team_migration_scope_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

- 明确本轮不迁移项，及其依赖阻断条件。
- 把“功能扩展”与“第三方平台改造”从迁移边界隔离。

## 约束

- 不更改历史代码；
- 不添加新功能；
- 不新增服务。

## 不可迁移定义

- 新前端开发、AI Secretary 实现、新 Dashboard；
- 第三方 OAuth/Connector；
- 生产账务/计费与外部 billing 变更；
- 未形成既定审计链路的数据清理动作。

## 触发阻断

- 子任务出现新范围请求时，必须提交总控决策席作范围裁决；涉及身份、凭据、外部服务、隐私或跨租户时并行交安全边界席。裁决前不允许在第9项内扩展。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_team_migration_scope_gate_9a3_exclusion_gate.md`
Objective:
锁定9a阶段不可迁移清单与阻断条件。
Special Constraints:
只定义阻断边界，不涉及执行改造。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
