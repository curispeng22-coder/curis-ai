# Workspace R4 第3项｜Agent / Workflow / Hybrid Mode（启动项）

- 日期：2026-07-18
- 状态：OPEN — 第3项已按保守口径收口，当前启动第4项
- 父项：`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
- Owner：产品规划席
- Next Seat：产品规划席 → 系统交付席 → 质量运行席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

在第四轮范围内，先不改执行器的前提下完成 Agent / Workflow / Hybrid 三类模式的最小可复核边界定义，给出统一的冲突与失败控制规则，并预留一次 focused 验收闭环。

## 约束（优先级）

1. 不改现有 Task/Workflow 执行核心、不改 `ModelGatewayAdapter` 行为
2. 不改 Admin/Workspace 边界模型，不改前端和不新增外部服务
3. 不发起额外真实模型调用，不新增数据库 schema
4. 不并行开启第4~9项；第4项独立启动前不扩张范围

## 工单拆分

- M1｜Agent Mode 边界定义  
  - 跳转：`issues/20260718_workspace_r4_agent_mode_profile_gate.md`（系统交付）
  - 目标：定义 Agent Mode 触发、作用域、失效与 fail-closed 规则
  - 细项：
    - M1a `issues/20260718_workspace_r4_agent_mode_entry_criteria_gate.md`（系统交付）
    - M1b `issues/20260718_workspace_r4_agent_mode_failclosed_gate.md`（系统交付）

- M2｜Workflow Mode 边界定义  
  - 跳转：`issues/20260718_workspace_r4_workflow_mode_profile_gate.md`（系统交付）
  - 目标：定义与现有顺序执行兼容的 Workflow Mode 语义与边界
  - 细项：
    - M2a `issues/20260718_workspace_r4_workflow_mode_entry_guard_gate.md`（系统交付）
    - M2b `issues/20260718_workspace_r4_workflow_mode_sequence_contract_gate.md`（系统交付）

- M3｜Hybrid Mode 边界定义  
  - 跳转：`issues/20260718_workspace_r4_hybrid_mode_profile_gate.md`（系统交付）
  - 目标：定义人机协作的允许/阻断条件与回退规则
  - 细项：
    - M3a `issues/20260718_workspace_r4_hybrid_mode_entry_switch_gate.md`（系统交付）
    - M3b `issues/20260718_workspace_r4_hybrid_mode_handoff_contract_gate.md`（系统交付）

- M4｜Mode 边界验证  
  - 跳转：`issues/20260718_workspace_r4_mode_contract_validation_gate.md`（质量运行）
  - 目标：一轮 focused 复核三模式边界是否无冲突、可复用、可复核

## 当前进展

- 第3项已完成二级拆解，当前执行序列与收口结论：
  - M1（Agent）：M1a → M1b（两者均产出 review；`M1a/M1b` 仍为 PARTIAL，`M1b` 缺更多反例）
  - M2（Workflow）：M2a → M2b（已完成，均 PASS；失败场景由 M2a 覆盖）
  - M3（Hybrid）：M3a → M3b（均 PARTIAL，缺少显式 mode/handoff 事实字段）
  - M3c：已按保守口径给出收口，`reviews/20260718_workspace_r4_hybrid_mode_profile_gate_review.md` 标注显式交接字段缺失为风险留白；
  - M4：`issues/20260718_workspace_r4_mode_contract_validation_gate.md` 已形成，M4a/M4b PASS，M4c 因缺显式 mode/handoff 为 PARTIAL；按保守口径收口通过。

`M1a` review：`reviews/20260718_workspace_r4_agent_mode_entry_criteria_gate_review.md`（PARTIAL）
`M1b` review：`reviews/20260718_workspace_r4_agent_mode_failclosed_gate_review.md`（PARTIAL）
`M2a` review：`reviews/20260718_workspace_r4_workflow_mode_entry_guard_gate_review.md`（PASS）
`M2b` review：`reviews/20260718_workspace_r4_workflow_mode_sequence_contract_gate_review.md`（PASS）
`M3a` review：`reviews/20260718_workspace_r4_hybrid_mode_entry_switch_gate_review.md`（PARTIAL）
`M3b` review：`reviews/20260718_workspace_r4_hybrid_mode_handoff_contract_gate_review.md`（PARTIAL）
`M3c` 判定：`reviews/20260718_workspace_r4_hybrid_mode_profile_gate_review.md`（PARTIAL；风险留白）

## 执行序列（仅本项）

- 优先：M1a → M1b
- 再：M2a → M2b
- 再：M3a → M3b → M3c（收口缺口）
- 收口：M4（先 M4a，再 M4b，再 M4c）  
  收口后返回产品规划席

## 当前收口分配

- 产品规划席：确认第3项按保守口径收口，进入第4项；
- 系统交付席：确认第4项独立 Issue 已就绪，不并行启用 5~9 项；
- 质量运行席：按 `issues/20260718_workspace_r4_mode_contract_validation_gate.md` 已完成 M4 一次性复核。

## 下一步（第4项）

- `issues/20260718_workspace_r4_auto_progress_timeout_retry_recovery_gate.md`

## 验收标准

- 三类模式有统一的 scope、触发、退出和冲突控制定义
- 不依赖新增实现即可复核定义一致性
- 第3项通过保守口径收口后，才能推进第4项

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_agent_workflow_hybrid_mode_gate.md`
Objective:
完成第四轮第3项范围拆解与最小语义边界定义闭环，确认保守口径收口并切换到第4项。
Special Constraints:
只做边界定义与复核安排，不改现网行为；不启用第4~9项并行；不涉及前端/凭据/网关/新模型/新服务。
Next Seat:
系统交付席（协同第4项路由）→ 产品规划席收口
