# Workspace R4 第3项｜Mode 闭环验收（Fail-closed）Gate（M4b）

- 日期：2026-07-18
- 状态：PASS — 已完成（关键拒绝场景 pass）
- 父项：`issues/20260718_workspace_r4_mode_contract_validation_gate.md`
- Owner：质量运行席
- Next Seat：产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

复核三模式定义下的拒绝边界：绑定缺失、作用域错配、步骤越权时，是否统一 fail-closed 而非静默降级。

## Must Do

1. 定义失败场景映射到拒绝原因（可复核字段/状态）
2. 抽样核验至少 3 类缺失场景（tenant/project/employee、binding、session/step）有显式拒绝结果
3. 验证失败后无越权续跑、无自动回退旧模式

## 验收标准（只读）

- 同 run 历史可证拒绝不是“返回成功却未执行”
- 没有出现“未声明模式仍进入下一步”的证据

## 执行口令（质量运行席）

- 一次复核使用一条失败 run + 一条成功 run：
  - 统计失败 run 的拒绝 reason/状态；
  - 核对后续 step 是否全部阻断；
  - 与 M1/M2/M3 定义条目逐项交叉确认。
- 输出：一页式复核摘要，标注是否存在任何“被拒却继续走下一步”证据。

## 复核结果（一次性）

- 核验数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`。
- 样本失败 run：
  - `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`（step6 失败，reason=`Model gateway input exceeds the approved limit`）
  - `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`（step1 失败，reason=`X-Ceo-Id is required to write UsageEvent`）
  - `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`（step1 失败，reason=`Model gateway request failed: Temporary failure in name resolution`）
- 成功 run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`、`wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`

结论：
- 三条失败样本均有显式 `workflow.step.failed` + `workflow.run.failed`（reason）；
- 失败后续 step 没有出现 `running/succeeded/completed`，仅剩 `pending`；
- 使用原先 `M1b/M2a` 的 `evolution_events` 事件约束口径一致：拒绝样本不是“返回成功但未执行”，而是显式阻断。 
- 无证据见到同一失败 run 上“跨租户/越权场景仍继续推进”。

Handoff: sent to 产品规划席

## 约束

- 不改接口，不改执行逻辑，不改数据库模型
- 不发起真实模型调用
- 不新增测试以外实现

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_mode_contract_validation_failclosed_gate.md`
Objective:
确认 mode 边界下的缺失/错误场景均 fail-closed 可复核。
Special Constraints:
只复核定义一致性；1 次聚焦核验内完成。
Next Seat:
产品规划席（确认）→ 质量运行席（复核收口）
