# Workspace R4 项目级 Memory 与恢复最小路径 Gate

- 日期：2026-07-18
- 状态：PASS — 第2子链已闭环
- 前置：`issues/20260718_workspace_r4_project_state_fact_source_gate.md`
- 父项：`issues/20260717_workspace_r4_project_long_term_state_and_memory_gate.md`
- Owner：系统交付席
- Next Seat：产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

定义并落地“项目级 Memory”最小恢复路径：给出一条可以在执行残缺/中断后继续推进的 Memory 键值与读取方式（`tenant_id + project_id + scope`），并验证一条从当前 Run 失败到可恢复状态的最小演练。

- Scope：仅本项内部，不改 Session、Agent/Workflow 运行器、AI 秘书、人工接管机制。
- 不新增外部服务和凭据。

## 工单拆分

- B1｜Memory Scope 与 key 规范（系统交付）
  - 跳转 Issue：`issues/20260718_workspace_r4_project_memory_recovery_b1_scope_key_gate.md`
  - 输出：scope 字典、key 唯一性、冲突判定。

- B2｜恢复演练与不可逆边界（系统交付）
  - 跳转 Issue：`issues/20260718_workspace_r4_project_memory_recovery_b2_recovery_runbook_gate.md`
  - 输出：一条可复现恢复演练记录（输入/输出/边界）。

- B3｜兼容性与历史保留验证（质量运行）
  - 跳转 Issue：`issues/20260718_workspace_r4_project_memory_recovery_b3_compatibility_gate.md`
  - 输出：历史失败保留与复用校验。

## Must Do

1. 定义 `scope` 最小集合（建议：`{run,step,execution,usage,project,owner}`）与键格式。
2. 定义 Memory 只读/更新接口（现有接口优先复用；无现有接口时给定只读 SQL 视图或最小派生查询）。
3. 给出 1 次无出网恢复演练步骤：
   - 取一条可复现历史失败/中断迹象；
   - 仅基于已有执行事实重建继续动作边界；
   - 输出恢复后状态、边界、不可逆字段。
4. 指明与 R3 收口证据兼容策略，保留历史失败 run 不变。

## 验收标准

- 存在可复现的 Memory key 与 scope 规范（含 tenant/project 唯一性）。
- 给出最小恢复演练记录（输入、操作、输出、边界）。
- 无 mock、无 stub、无新前端。

## 当前进展

- B1：PASS（已复核）
- B2：PASS（仅演练定义复核完成）
- B3：PASS（兼容性复核完成）

Compact Handoff:
Issue:
`issues/20260718_workspace_r4_project_memory_recovery_path_gate.md`
Objective:
补齐项目级 Memory 键值与最小恢复路径，验证从执行中断到可恢复的单次演练闭环。
Special Constraints:
不得跨界到 Session/Mode/人工接管/AI Secretary；保持与 R3 事实源一致。
Next Seat:
产品规划席
