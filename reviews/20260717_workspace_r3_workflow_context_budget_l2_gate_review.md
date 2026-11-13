# R3 Workflow 上下文预算 L2 Gate 质量 Review

- Issue：`issues/20260717_workspace_r3_workflow_context_budget_l2_gate.md`
- 固定分支/修订：`feat/roadmap-r1r2` @ `b0f791f74e449be1d6c907480cc183cf92a78209`
- 基线实现：`e906e86d2710deb0838132e9d545da3e3a35dff7`
- 结论：`PASS`

## 结论

7,168 UTF-8 bytes 硬预算、确定性截断、metadata/hash/reference、最新两步优先、原始结果不可变及全部异常 fail-closed 均成立。此前非文本结果会 canonical JSON 后继续的唯一阻塞已修复；dict/list/number/bool/null/bytes 现在均在 prompt 构造阶段明确拒绝，Adapter/Recorder=0。本 Gate 质量复核 `PASS`。

## 已通过证据

- HEAD 与修复 SHA 一致；修复提交仅改：
  - `backend/app/workflow_runtime.py`
  - `backend/tests/test_r3_workflow_context_budget.py`
- `R3_WORKFLOW_CONTEXT_MAX_BYTES=7168`；Adapter 原 `8192` input-token 上限未提高。
- 构造结果按 UTF-8 bytes 计数，长目标与多字节正文安全截断，带明确 `TRUNCATED` 标记。
- 所有前序成功 Step 均保留 `step_result_id/order/type/status/hash/reference/truncated`；最近两步正文从新到旧优先，早期正文使用次级预算。
- 相同快照重复构造结果一致；原 `step_results.result` 与 `executions.output` 未覆盖或压缩。
- 重复结果、同 Step 多结果、缺失 ID/结果、非 succeeded 前序、不可序列化对象、非法 UTF-8、Step/metadata 超预算均在 Adapter 前拒绝。
- 七步 RecordingHttpPost 测试确认每次 prompt ≤7168 bytes，原始七个结果完整保留；异常路径 Recorder=0。
- `compileall` 与 `git diff --check HEAD^ HEAD`：PASS。
- `3000/3100/8001/8002/8080` 全部 CLOSED；未启动、未注 Key、未出网、未跑全量。
- 失败 Run `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc` 仍为 failed；5 个既有 Result/Execution 内容一致，SHA-256 与执行 Review 全部相同。

## 独立测试

```bash
PYTHONPATH=backend backend/.venv/bin/python -m pytest -q \
  backend/tests/test_r3_workflow_context_budget.py \
  backend/tests/test_model_gateway_adapter.py -k 'r3_'
```

结果：`31 passed, 6 deselected, 4560 warnings in 5.06s`。

兼容聚焦：

```bash
CURIS_PLATFORM_ADMIN_TOKEN=platform-admin-dev PYTHONPATH=backend \
  backend/.venv/bin/python -m pytest -q backend/tests/test_phase6_workflow_mvp.py
```

结果：`3 passed, 760 warnings in 0.70s`。合计为 `34 passed, 6 deselected`；Warnings 均为 FastAPI/Python 3.14 既有弃用提示。

## 阻塞解除证据

`WorkflowRuntime._canonical_result()` 现在首先要求 `isinstance(value, str)`；非字符串统一抛出 `workflow context result body must be text`。空字符串仍使用 `[EMPTY_RESULT]`，合法字符串、多字节与截断逻辑保持不变。

独立最小复现逐项传入 dict/list/number/bool/null/bytes，六项全部 `REJECTED`；异常发生在 `_build_step_input()`，位于 `employee.execute_step()`/Adapter 之前，因此 Recorder=0。对应参数化测试和原七步字符串正向测试全部通过。

原 `NON_TEXT_CONTEXT_NOT_FAIL_CLOSED` 阻塞已解除，无本 Gate 剩余质量阻塞。

## 状态

- 上下文预算与 UTF-8 截断：`VERIFIED — PASS`
- 非文本 fail-closed：`VERIFIED — PASS`
- 最终：`PASS`
- 剩余阻塞：无（仅限本上下文预算 Gate；新 Run 与真实模型调用须另行授权）。
- Next Seat：产品规划席
- Handoff：sent to 产品规划席
