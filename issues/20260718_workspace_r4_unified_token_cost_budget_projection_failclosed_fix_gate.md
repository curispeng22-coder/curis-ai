# Workspace R4 第7项｜成本投影 fail-closed 修复 Gate

- 日期：2026-07-18
- 状态：OPEN
- 前置：`issues/20260718_workspace_r4_items_1_7_code_construction_audit_gate.md`
- Owner：系统交付席（实现）→ 质量运行席（独立复核）→ 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

修复统一 Run / Artifact 读投影把不可信成本显示为真实 `0` 且仍标记完成的问题。

## 允许范围

- 仅调整 `WorkflowRuntime._add_read_projection` 的成本可信性判断。
- 为该反例补最小 focused 测试。
- 当任一关联 usage 的 `estimated_cost` 缺失、非数字或 `<= 0`，或 `price_version` 缺失/不一致时，投影必须使用现有 unknown / 不可结算语义；不得把它显示为真实零成本或已完成的可结算 Artifact。

## 不允许范围

- 不改 schema、历史数据、模型调用、网关、预算上限、前端、API 合约或运行时启动方式。
- 不重跑第1～6项，不恢复第8项 8a 队列。

## 验收

- 原有合法 7-step usage 投影保持完成，成本与 `price_version` 可追溯。
- 7 条 `estimated_cost=0` 且缺 `price_version` 的内存反例 fail-closed，不得输出完成且真实 0 成本 Artifact。
- focused 测试通过，未启动服务、未出网。
- 系统交付席回传实现文件、focused 结果与 SHA；质量运行席独立复核后才允许恢复 `8a.1a.2`。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_unified_token_cost_budget_projection_failclosed_fix_gate.md`
Objective:
修复不可信成本被投影为真实零成本的 fail-open。
Special Constraints:
仅读投影与 focused 测试；不改 schema/API/前端/模型运行；8a 继续冻结。
Next Seat:
系统交付席

Handoff: sent to 系统交付席
