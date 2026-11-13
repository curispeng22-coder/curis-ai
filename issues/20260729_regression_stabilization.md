# Regression Stabilization — S2 全量回归收口

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_regression_stabilization_review.md`

## Objective

关闭 S2 Review 中记录的 13 项后端全量回归失败，使权威命令
`backend/.venv/bin/python -m pytest -q backend/tests` 全绿。

## Boundary

- 只修复已复现的测试隔离、历史契约和本地执行兼容问题。
- 不新增产品能力、依赖、数据库表、Workspace/Admin 或架构抽象。
- 不修改 S2 Company / Department / Home 产品行为。
- 保留工作区中未纳入本 Task 的既有未提交改动。

## Allowed Files

- `issues/20260729_regression_stabilization.md`
- `reviews/20260729_regression_stabilization_review.md`
- `backend/app/ceo_runtime_evidence.py`
- `backend/app/real_rd_executor.py`
- `backend/tests/test_bplan_seed_integrity.py`
- `backend/tests/test_pilot_b_activation.py`
- `backend/tests/test_pilot_b_agent_conversion.py`
- `backend/tests/test_multisource_agent_conversion.py`
- `backend/tests/test_ceo_runtime_evidence.py`
- `backend/tests/test_curis_pipeline_core.py`
- `backend/tests/test_p1_adapters.py`
- `issues/20260729_mvp_phase1_s2_workspace_model.md`
- `reviews/20260729_mvp_phase1_s2_workspace_model_review.md`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Root Causes

1. 四个历史测试在收集期把 `backend/app` 留在 `sys.path`，破坏顶层 import 共存守卫。
2. CEO Evidence 测试样本写入默认库而非受控临时库，且源码含被契约禁止的旧措辞。
3. Pipeline Runtime 测试 FakeResolver 未跟随现有 `employee_id` 参数。
4. MCP 测试未转义包含空格的 Python 可执行路径。
5. Real RD 生成的 pytest 命令与 LocalRDToolset 允许命令不一致。

## Acceptance

1. 五类失败的聚焦测试通过。
2. S2 聚焦测试通过。
3. 权威后端全量回归零失败。
4. `git diff --check` 通过。
5. Review、S2 状态和当前状态文件更新后提交推送。
