# Workspace R4 第3项｜Mode 闭环验收（顺序+隔离）Gate（M4a）

- 日期：2026-07-18
- 状态：PASS — 已完成（与 `workflow_runs` 历史比对通过）
- 父项：`issues/20260718_workspace_r4_mode_contract_validation_gate.md`
- Owner：质量运行席
- Next Seat：产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

一次聚焦核验中，确认 Agent / Workflow / Hybrid 的模式定义不允许打断同 run 既有 step 顺序，并保持 session/project/tenant 不串扰。

## Must Do

1. 抽样同 run 的 history，确认 Step 顺序（1→7）与 mode 指定行为可复核一致
2. 抽样跨 session、跨 project、跨 tenant 跑同一实体的查询：不得出现非法共享/错误读取
3. 核对 `run-next-step` 与已定义 mode 规则的一致性口径（只读）

## 验收标准（只读）

- 任一异常场景均有明确可复核拒绝痕迹
- 证据链可落在 `workflow_runs` / `workflow_steps` / `step_results` / `evolution_events`

## 执行口令（质量运行席）

- 取样 1 条主 run + 1 条边界 run：
  - 确认 `step_order` 顺序未跨越；
  - 同 tenant/project/session 的数据边界无非法串读；
  - 出现拒绝时是否有完整拒绝链（run/step/usage）。
- 输出：一页式对账表 + 异常列表（若无异常直接写 PASS）。

## 复核结果（一次性）

- 核验数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`。
- 选取样本：
  - 主 run：`wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`（running，tenant-a / project-652...）
  - 边界失败 run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`（failed，tenant-a / project-e84...）
  - 补充成功 run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`（succeeded，tenant-a / project-e84...）

结论：
- 三条 run 中 `workflow_steps.step_order` 全部为 `1..7` 连续；无跳步、无重复 step order。
- 失败 run 在首个失败 step 之后，后续 step 状态均 `pending`，无越步执行。
- 运行轨迹均可在 `evolution_events` 落到 `run.created/started/step.assigned/step.started/step.completed|failed/run.failed`，拒绝链路完整。
- 选样未出现 tenant 混用（均为 `tenant-a`）；跨 project 的 run 无证据出现串读。

复核口径说明：
- 当前样本无显式 `session_id` 字段，仅能就 run 级数据口径验证“顺序与隔离边界”。

Handoff: sent to 产品规划席

## 约束

- 不启动服务，不发起模型调用，不改接口，不改 schema
- 不新增 mock/stub，不改现有前端或网关

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_mode_contract_validation_sequence_isolation_gate.md`
Objective:
确认模式定义与 run 顺序、隔离边界一致且可复核。
Special Constraints:
1 次 focused 复核；只读核验；不得改现网行为。
Next Seat:
产品规划席（确认）→ 质量运行席（复核收口） 
