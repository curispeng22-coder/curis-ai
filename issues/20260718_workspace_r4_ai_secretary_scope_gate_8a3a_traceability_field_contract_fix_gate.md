# Workspace R4 第8项｜8a.3a｜来源追溯真实字段契约修复 Gate

- 日期：2026-07-18
- 状态：IMPLEMENTED（待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md`
- Owner：系统交付席（真实字段定义）→ 质量运行席（复核）→ 产品规划席（收口）
- 分支：`feat/roadmap-r1r2`

## 目标

使 Secretary 建议的追溯字段只依赖四类来源已存在、可核验的真实字段，不把跨状态机关系或未落地哈希写成必选条件。

## 必须核对

- 逐一确认 `workflow_runs`、`step_results`、`content_publish_packages`、`content_workflow_runs` 可提供的真实 ID、tenant 与时间字段。
- 明确每类来源的最小可追溯引用；只有已有可核验路径才能携带 run/step/result 关联。
- `source_result_hash` 仅在已有稳定生成与可复验来源时可用；否则不得作为必选字段或新建持久化字段。

## 禁止

- 不得要求所有来源都有 `source_run_id`、`source_step_id` 或 project/company/workflow 关系。
- 不得用同名 ID、拼接、默认值或裸结果文本补足缺失关系。
- 不新增 schema、哈希持久化、接口、模型调用或运行时。

## 验收

- 输出按来源类型分列的 exact 可用字段、可选字段、拒绝条件与真实关联路径。
- 关系不可证或必需引用缺失时 fail-closed。
- 质量复核 PASS 后才重派父项 8a.3a；8a.3b/8a.3c 保持冻结。

## 实施证据

- 已在 `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_whitelist_gate.md` 按四类真实 schema 替换统一伪字段契约。
- focused：`backend/tests/test_ai_secretary_traceability_field_contract.py`。
- 命令：`.venv/bin/python -m pytest -q backend/tests/test_ai_secretary_traceability_field_contract.py`。
- 结果：`4 passed`。
- 未修改 schema、API、运行时或历史数据；未新增或持久化哈希；`8a.3b`、`8a.3c` 保持冻结。

## Compact Handoff

Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a3a_traceability_field_contract_fix_gate.md`
Objective:
将建议追溯字段收敛为真实可核验字段。
Special Constraints:
仅契约；不新建哈希/关系/schema/API/运行时。
Next Seat:
质量运行席

Handoff: sent to 质量运行席
