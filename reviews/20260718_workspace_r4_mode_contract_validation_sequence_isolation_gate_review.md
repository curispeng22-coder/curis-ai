# 2026-07-18 Workspace R4 Mode 闭环验收（M4a）复核记录

- Issue：`issues/20260718_workspace_r4_mode_contract_validation_sequence_isolation_gate.md`
- 固定分支：`feat/roadmap-r1r2`
- 复核数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 结论：`PASS`（顺序与 run 级隔离口径成立）

## 取样

- 主 run：`wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`（running，tenant-a，project-652...）
- 边界失败 run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
- 成功 run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`

## 一次性检查结果

1. step 顺序
   - 三个样本 run 的 `workflow_steps.step_order` 均为完整 `1..7`，`sequence_ok=True`。
   - `workflow_steps.step_order` 无重复、无缺段、无越步。

2. 隔离边界
   - 选样样本显示 tenant 均为 `tenant-a`（同租户内多 project：`project-e84...` 与 `project-652...`），未见跨 tenant 混用。
   - run 内同 tenant/project 下 step 与 step_result 一一对应、无重复归属。
   - 未检出“run 间 step 结果被另一 run 复用”的冲突证据（基于 run 级映射核验）。

3. 失败阻断（边界样本）
   - `wfr-e96fe025...` 在 step6 失败后，step7 pending，未出现 non-pending 越步。

## 风险说明

- 当前样本未包含显式 session 标识字段；若要求按 session 口径可视为保守近似复核。

Handoff: sent to 产品规划席
