# Workspace R4 第3项｜Agent/Workflow/Hybrid Mode 闭环验收 Gate

- 日期：2026-07-18
- 状态：PASS（保守口径收口）
- 父项：`issues/20260718_workspace_r4_agent_workflow_hybrid_mode_gate.md`
- Owner：质量运行席
- Next Seat：质量运行席
- 分支：`feat/roadmap-r1r2`

## 目标

对 Agent/Workflow/Hybrid 语义定义完成度进行一次focused复核，确认三类模式规则不冲突、可复核、fail-closed。

## 前置条件（本轮）

- 以 `reviews/20260718_workspace_r4_hybrid_mode_profile_gate_review.md` 为收口输入。
- 产品规划席需确认是否采用“保守口径”（当前仅基于现有事实字段，无显式 mode/handoff 交接日志）进行一次性复核。
- 若保守口径不通过，先回 M3c 完成显式交接字段补样本。

已细分子项：

- M4a：`issues/20260718_workspace_r4_mode_contract_validation_sequence_isolation_gate.md`（质量运行）
- M4b：`issues/20260718_workspace_r4_mode_contract_validation_failclosed_gate.md`（质量运行）
- M4c：`issues/20260718_workspace_r4_mode_contract_validation_compatibility_gate.md`（质量运行）

## 执行顺序

- 顺序已锁定：`issues/20260718_workspace_r4_mode_contract_validation_sequence_isolation_gate.md`
  → `issues/20260718_workspace_r4_mode_contract_validation_failclosed_gate.md`
  → `issues/20260718_workspace_r4_mode_contract_validation_compatibility_gate.md`
- 每个子Issue由质量运行席独立执行，但归档于同一focused窗口，禁止复用新环境与重复真实调用。

## 一次性执行约束

- 这三项合并为同一 focused 复核窗口（不跨 run、不跨会话重复创建临时环境）
- 共享只读事实口径，避免新增核验脚本与二次解释成本

## 下一步分配（本轮）

- M4a：由质量运行席执行 `issues/20260718_workspace_r4_mode_contract_validation_sequence_isolation_gate.md`
- M4b：由质量运行席执行 `issues/20260718_workspace_r4_mode_contract_validation_failclosed_gate.md`
- M4c：由质量运行席执行 `issues/20260718_workspace_r4_mode_contract_validation_compatibility_gate.md`
- 任何子任务出阻塞先回该Issue更新，并由产品规划席决策是否需要回退M3补显式交接日志样本。

## 要求

- 仅复核定义一致性，不发起真实出网模型调用
- 1 次聚焦核验，覆盖：
  - 同一 run 的 step 顺序不可被模式定义冲突打断
  - 模式边界中 session/project/tenant 的隔离约束
  - 冲突与缺失的默认拒绝结果（不得“静默降级”到旧行为）

## 允许范围

- 可读数据库查询、既有 run trace 复核、既有报告字段映射核验
- 不新增 API，不重启服务，不改数据库，不改前端

## 当前结果同步

- `issues/20260718_workspace_r4_mode_contract_validation_sequence_isolation_gate_review.md`：PASS（样本内无 step 顺序错位/串读证据）
- `issues/20260718_workspace_r4_mode_contract_validation_failclosed_gate_review.md`：PASS（失败后阻断 + 拒绝链路完整）
- `issues/20260718_workspace_r4_mode_contract_validation_compatibility_gate_review.md`：PARTIAL（角色/步骤归属冲突无；但缺显式 mode/handoff 字段，无法按模式语义最终判定“单一主导”）

## 复核结论

- 以现有字段复核 M4a/M4b 全部通过；M4c 在“无显式 mode/handoff”口径下复核为零冲突近似通过。
- 对外部结论输出：第3项可进入下一项，但保留“缺少显式交接字段”作为待改进风险，不影响当前第3项闭环。

## 风险留白（仅记录，不阻断下轮）

- `workflow_runs / workflow_steps / step_assignments` 已覆盖了顺序、归属与 fail-closed 的可复核性。
- 目前仍未在 run 事实链上看到 `mode / handoff / switch / takeover` 显式字段，后续实施若需运行时可重放重建交接主导关系，需补充日志/事件字段。

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_mode_contract_validation_gate.md`
Objective:
完成第3项三类模式边界的 focused 质量核验，确认是否可进入第3项 PASS。
Special Constraints:
只允许 1 次 focused 复核；不得发起真实模型调用，不得改行为，不得跨 3 个 mode 之外扩展范围。
Next Seat:
产品规划席
