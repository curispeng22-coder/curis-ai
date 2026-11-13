# Workspace R4 第3项｜Workflow Mode 边界定义 Gate

- 日期：2026-07-18
- 状态：OPEN — IN_PROGRESS（M2a PASS，M2b 已形成PASS复核）
- 父项：`issues/20260718_workspace_r4_agent_workflow_hybrid_mode_gate.md`
- Owner：系统交付席
- Next Seat：产品规划席（确认定义）→ 系统交付席（确认口径）→ 质量运行席（focused 复核）
- 分支：`feat/roadmap-r1r2`

## 目标

给出“Workflow Mode”最小边界定义，确认第3项范围内该模式与现网 `run-next-step` 语义的兼容边界，避免引入新执行器。

已细分子项：

- M2a：`issues/20260718_workspace_r4_workflow_mode_entry_guard_gate.md`（系统交付）  
- M2b：`issues/20260718_workspace_r4_workflow_mode_sequence_contract_gate.md`（系统交付）

## 执行顺序

- 先 `issues/20260718_workspace_r4_workflow_mode_entry_guard_gate.md`（PASS）
- 再 `issues/20260718_workspace_r4_workflow_mode_sequence_contract_gate.md`（PASS）

## Must Do

1. 固定 Workflow Mode 的身份/项目作用域定义（tenant/project/employee/session）
2. 明确与现有顺序执行一致性（Step1→Step7，固定顺序、0重试、失败即停）
3. 明确模式切换入口不改现有 API 的前提下，禁止隐式跳步或跨项目/跨scope复用上下文
4. 明确日志与结果映射字段（run、step、result、execution）用于复核

## 允许范围

- 只在 Issue/文档层面固定规则，不改实现
- 可使用现有数据库事实与已有历史 run 做一致性核验
- 不改前端，不改网关，不改模型，不加测试以外的实现

## 现有约束内验收

- 无新增 endpoint
- 无新增数据库 schema
- 无模拟数据替代
- 有一条可复核的现有 run/step 读链一致性检查命令

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_workflow_mode_profile_gate.md`
Objective:
定义 Workflow Mode 与现有顺序执行闭环的兼容边界，不引入模式新行为。
Special Constraints:
不改变 `/api/workspace/workflows/{run_id}/next-step` 与现有 Task/Step 持久模型；不新增外部服务与凭据。
Next Seat:
产品规划席（确认定义）→ 系统交付席（确认落地）→ 质量运行席（focused 复核）
