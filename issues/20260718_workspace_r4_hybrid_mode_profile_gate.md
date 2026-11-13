# Workspace R4 第3项｜Hybrid Mode 边界定义 Gate

- 日期：2026-07-18
- 状态：OPEN — IN_PROGRESS（M3a/M3b 已复核，M3c 收口待确认）
- 父项：`issues/20260718_workspace_r4_agent_workflow_hybrid_mode_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席
- 分支：`feat/roadmap-r1r2`

## 目标

在不改现有执行引擎实现前提下，定义 Hybrid Mode 最小语义：何为“人+模型协同”的最短闭环，何为“不可协同”情形的拒绝边界。

已细分子项：

- M3a：`issues/20260718_workspace_r4_hybrid_mode_entry_switch_gate.md`（系统交付）  
- M3b：`issues/20260718_workspace_r4_hybrid_mode_handoff_contract_gate.md`（系统交付）
- M3c：本Issue 收口补充（定义可复核/不可复核边界与执行口径）

## 执行顺序

- 先 `issues/20260718_workspace_r4_hybrid_mode_entry_switch_gate.md`
- 再 `issues/20260718_workspace_r4_hybrid_mode_handoff_contract_gate.md`
- 再完成本Issue收口补充

## M3c 收口定义（当前）

- 允许复核项：以现有 `workflow_runs / workflow_steps / step_results / evolution_events / usage_*` 还原 run 的顺序推进与失败阻断。
- 不可复核项：当前 `event.payload` 无 `mode/handoff/intervention/human_takeover/model_takeover` 显式字段，因此当前无法从事实链唯一、确定重建“Human→Model/Model→Human”的交接时点。

### M3c 收口结论（建议）

- 当前范围内可闭合部分：
  - 以现有字段可复核的，仅到“顺序化失败阻断”和“越权不继续推进”。
  - M3a/M3b 结论一致：未发现明显越权推进或静默降级迹象。
- 当前范围内不可闭合部分：
  - 无法基于 `evolution_events` 显式确认 mode/handoff 切换。
  - 无法基于可复核字段确认交接成功与否，除“缺失痕迹”外。
- 建议：
  - 若本轮允许仅以“不可观测即不落盘”的保守策略，先将 Hybrid 收口为“无显式交接字段下不支持运行时重放证明”，并提交后续实现/日志字段 Issue。
  - 若必须一次性 PASS，则需要先补齐显式交接事件样本并追加复核。

## Must Do

1. 定义 Hybrid Mode 的可观测状态字段与前置条件（如已授权成员、同项目 session、绑定完整）
2. 定义何时需要回退到 Workflow Mode（fail-closed）
3. 定义跨项目/多角色并发下的冲突优先级与阻断（不得共享 step-context）
4. 给出最小验收命令，验证仅基于事实（run/task/usage）确认是否满足边界

## 当前收口口径（M3c）

- 本 Issue 先按 `已知事实可复核` 进行闭环：先不要求显式 mode/handoff 字段。
- 收口前提：`issues/20260718_workspace_r4_hybrid_mode_entry_switch_gate.md`、`issues/20260718_workspace_r4_hybrid_mode_handoff_contract_gate.md` 已同步复核 `PARTIAL` 结论。
- 下一步分配：产品规划席确认是否允许 M4 在“不可显式交接字段”前置下进行一次 focused 验收；若不允许，先立后续实现Issue补齐日志字段样本后再回到 M4。

## 允许范围

- 只写清边界，不改代码、不改前端、不改模型/网关、不改外部服务
- 只做一项定义：Hybrid 的准入条件 + 退出条件 + 冲突失败定义

## 严格限制

- 不定义新 UI、人工接管新入口
- 不改 `tenant/project/session/run` 的持久化写链
- 任何无法用现有事实复核的行为定义不允许落入本Issue

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_hybrid_mode_profile_gate.md`
Objective:
定义 Hybrid Mode 的可协作边界并与 Agent/Workflow Mode 保持互斥、可回退、可复核。
Special Constraints:
本项不实现，仅定义边界与复核逻辑；不得改执行器、数据库 schema、网关或凭据流。
Next Seat:
产品规划席（确认定义）→ 系统交付席（对齐实现范围）→ 质量运行席（focused 复核）
