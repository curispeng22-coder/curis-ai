# Workspace R4 项目长期状态与项目级 Memory

- 日期：2026-07-18
- 状态：PASS — 第1项与第2项闭环完成（第3项已拆分）
- 父项：第三轮真实纵向执行链路收口完成（`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`）
- 目标：固定一个面向项目的长期状态与 Memory 路径，保证项目可跨执行会话追溯、可恢复、可汇总，且不引入新前端与新外部运行时能力。
- Owner：系统交付席
- Next Seat：质量运行席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 先说结论

第一项与第2项闭环完成。第3项（Agent/Workflow/Hybrid）已拆分为边界定义 Issue，等待定义闭环后再进入实施。

## 目标定义（限定本 Issue）

1. 明确并冻结 `Project` 长期状态来源与优先级（来源：Workflow Run 结果、StepResult/Usage 记录、人工事件/失败原因），形成单点事实映射。
2. 定义项目级 Memory 的最小键与持久化来源（按 `tenant_id + project_id + scope` 唯一），支持后续查询与恢复，不复用数据库外状态。
3. 建立“项目状态—执行状态一致性”边界：
   - 项目状态变更必须由真实执行事件驱动；
   - 禁止直接覆盖/手工改写项目状态；
   - 允许只读查询长期状态，不改变当前执行结果。
4. 明确恢复与会话衔接最小接口：在不改 API 语义前提下，给出 Project Memory 可读写边界与验证方法。
5. 给出仅一次全量回归 + 聚焦验证清单（不扩散到其他功能）。

## 允许范围

- 只改项目状态映射与 Memory 边界定义文件/说明、最小测试与验收命令。
- 不新增前端，不改执行器与现有工作流运行器，不扩展 AI Secretary/前端/新服务。
- 不改动第三轮 R3 成熟闭环的数据与历史失败 run。

## 禁止范围

- 不启动新前端页面；不接新行业、新 Billing、Marketplace、外部 connector。
- 不做员工多项目 Session 实现、AI Secretary、人工接管实现。
- 不改 `projects.status` 的历史兼容行为外的现有写入链路。

## 验收标准

- 项目长期状态定义有明确事实源（run/task/step/execution/usage）。
- 项目级 Memory 的键、Scope 和不可变依据完整闭环，查询接口（或最小读取方式）可复现。
- 有一条从执行残缺到恢复衔接的最小恢复路径，且无 mock/stub 替代。
- 本 Issue PASS 前，不得开启第四轮第2~9项。
- 质量运行席出具一次 focused 验证 + 结果 Review。

## 已有事实接管

- 第三轮收口证据可直接复用：`reviews/20260717_workspace_r3_ai_rd_vertical_e2e_review.md`、`reviews/20260717_workspace_r3_artifact_project_status_architecture_review.md`、`reviews/20260717_workspace_r3_artifact_project_status_closure_review.md`。
- 禁止复用旧式“项目状态静态写入”作为恢复证据；本 issue 只允许定义与复用既有执行事实源。

## 下一步

1. 启动子 Issue A：`issues/20260718_workspace_r4_project_state_fact_source_gate.md`（已PASS）。
2. 子 Issue A PASS 后，启动子 Issue B：`issues/20260718_workspace_r4_project_memory_recovery_path_gate.md`（已PASS）。
3. 质量运行席对每个子 Issue 做一次 focused 验证并提交 review。
4. 两子 Issue 全部 PASS 后，由产品规划席签发本 item close，进入第3项边界定义。

## 子任务清单

- `issues/20260718_workspace_r4_project_state_fact_source_gate.md`（状态事实源映射）
- `issues/20260718_workspace_r4_project_memory_recovery_path_gate.md`（项目级 Memory 与恢复演练）

### 第1项子链（状态事实源映射）

- `issues/20260718_workspace_r4_project_state_fact_source_gate.md`
- `issues/20260718_workspace_r4_project_state_fact_source_a1_mapping_gate.md`
- `issues/20260718_workspace_r4_project_state_fact_source_a2_tenant_scope_gate.md`
- `issues/20260718_workspace_r4_project_state_fact_source_a3_focused_validation_gate.md`

### 第2项子链（项目级 Memory 恢复）

- `issues/20260718_workspace_r4_project_memory_recovery_path_gate.md`
- `issues/20260718_workspace_r4_project_memory_recovery_b1_scope_key_gate.md`
- `issues/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate.md`
- `issues/20260718_workspace_r4_project_memory_recovery_b3_compatibility_gate.md`

### 第3项子链（同一员工多项目 Session）

- `issues/20260718_workspace_r4_multi_project_session_gate.md`
- `issues/20260718_workspace_r4_multi_project_session_scope_gate.md`
- `issues/20260718_workspace_r4_multi_project_session_context_switch_gate.md`
- `issues/20260718_workspace_r4_multi_project_session_recovery_gate.md`

### 第4项子链（Mode 边界定义）

- `issues/20260718_workspace_r4_agent_workflow_hybrid_mode_gate.md`
- `issues/20260718_workspace_r4_agent_mode_profile_gate.md`
- `issues/20260718_workspace_r4_workflow_mode_profile_gate.md`
- `issues/20260718_workspace_r4_hybrid_mode_profile_gate.md`
- `issues/20260718_workspace_r4_mode_contract_validation_gate.md`

## 紧急阻塞条款

- 若无法确认“项目状态唯一事实源”或 Mode 边界冲突，立即阻塞，不得新增功能/模式；
- 第2项若出现跨项目越权、共享上下文污染风险，立即阻塞并提交总负责人处理；不得并行扩散到第3~9项。

Compact Handoff:
Issue:
`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
Objective:
启动第四轮第1项：定义项目长期状态与项目级 Memory 最小闭环，形成可恢复、可查询的状态事实源映射。
Special Constraints:
仅第一项与第一阶段闭环内容；第四轮第3项为边界定义先行，暂不实现；不得并行启动第3项之外功能。
Next Seat:
系统交付席（先实现约束映射）→ 质量运行席（focused）→ 产品规划席（验收）
