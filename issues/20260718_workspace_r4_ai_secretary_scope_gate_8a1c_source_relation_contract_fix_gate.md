# Workspace R4 第8项｜8a.1c｜来源真实关联契约修复 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate.md`
- Owner：系统交付席（真实关系定义）→ 质量运行席（复核）→ 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

修正 8a.1c 来源错配矩阵，使其只使用现有 schema 中可核验的真实关联。

## 必须固化

- `workflow_runs` 唯一主键为 `workflow_run_id`。
- `step_results` 到 Run 只允许：`workflow_step_id → workflow_steps.workflow_step_id → workflow_steps.workflow_run_id → workflow_runs.workflow_run_id`。
- `content_publish_packages` 与 `content_workflow_runs` 只按自身 `tenant_id` 和本源字段核验；缺少 project/company/workflow 可验证关系时必须 fail-closed。

## 禁止

- 不得使用不存在的 `workflow_runs.id` 或 `step_results.workflow_run_id`。
- 不得从同名 `run_id`、名称、字符串拼接或默认值推断跨状态机关联。
- 不新增 schema、持久化关系、接口、模型调用或运行时。

## 验收

- 逐项列出四类来源允许使用的真实列与关联路径。
- 无法核验关系时固定拒绝，复用现有 403/404 响应契约。
- 质量静态复核 PASS 后才重新复核 8a.1c；不得推进 8a.2a。

## 实施证据

- 已在 `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_mismatch_isolation_gate.md` 用真实 schema 矩阵替换伪关系。
- focused：`backend/tests/test_ai_secretary_source_relation_contract.py`。
- 命令：`.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_source_relation_contract.py`。
- 结果：`4 passed`。
- 未修改 schema、API、运行时或历史数据；`8a.2a` 保持冻结。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1c_source_relation_contract_fix_gate.md`
Objective:
固化四类来源的真实可核验关联，删除伪关系。
Special Constraints:
仅契约；不改 schema/API/运行时；关系不可证即拒绝。
Next Seat:
质量运行席

Handoff: sent to 质量运行席
