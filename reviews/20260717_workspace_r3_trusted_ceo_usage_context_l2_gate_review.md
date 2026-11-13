# Workspace R3 可信 CEO UsageContext L2 Gate 质量 Review

- 日期：2026-07-17
- Issue：`issues/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate.md`
- 分支：`feat/roadmap-r1r2`
- 基线修订：`fee55346f49c4e71d1032ecfdaa580eef18dd391`
- 修复修订：`718af2c463e39820ac6928681b16818a9fbccc25`
- 验证席：质量运行席

## 结论

**PASS（本 Issue 的独立无出网质量验收通过）。**

`membership.ceo_id → TenantContext/UsageContext → R3 UsageEvent` 正向链已闭合；伪造 Header、缺失/撤销/过期、角色错误、Company/Project/Run/binding/employee 状态不一致均保持出网前 fail-closed。前次 `employee.status='active'` 与既有 Runtime 状态域冲突已修复。

本 Issue 的质量阻塞可关闭；这不代表 Parent R3 真实模型 Gate 已通过。新的真实单 Run 仍需按安全和总负责人授权流程单独批准。

## 修订与范围

- HEAD：`718af2c463e39820ac6928681b16818a9fbccc25`，分支 `feat/roadmap-r1r2`。
- 相对 `fee55346` 仅修改：`backend/app/main.py`、`backend/tests/test_model_gateway_adapter.py`。
- 实现仅把 enabled employee 的可执行状态改为 `idle/assigned`；`disabled` 继续拒绝。
- 未修改 Provider、Model、Gateway、成本、Admin、前端或历史 Run。

## 独立无出网测试

命令：

```text
cd backend
./.venv/bin/python -m pytest -q \
  tests/test_workspace_identity_membership.py \
  tests/test_r3_trusted_ceo_usage_context.py \
  tests/test_model_gateway_adapter.py::ModelGatewayAdapterTest::test_r3_workflow_records_scoped_model_usage_and_approved_cost \
  tests/test_model_gateway_adapter.py::ModelGatewayAdapterTest::test_r3_trusted_ceo_scope_failures_are_rejected_before_network \
  tests/test_model_gateway_adapter.py::ModelGatewayAdapterTest::test_r3_workflow_rejects_unapproved_project_before_network \
  tests/test_model_gateway_adapter.py::ModelGatewayAdapterTest::test_r3_workflow_rejects_unapproved_run_before_network
```

结果：**14 passed / 0 failed**，2.01s。

## 验收证据

- 正向 Workflow→UsageEvent：HTTP 200、首 Step succeeded、Recorder=1。
- UsageEvent 仅采用服务端 `ceo_id`，忽略 payload 或客户端 `X-Ceo-Id` 伪造；包含 `subject_digest`、tenant/company/project/run/step/employee/binding/model、Token、`price_version`、成本、状态和 request id。
- 旧库迁移：`tenant_memberships.ceo_id` additive nullable；历史行保持 `NULL`，不填默认 CEO。
- 撤销、过期、缺映射、角色错误、Company CEO 不一致、Project 归档/跨 Company：HTTP 403，Recorder=0。
- Project scope 错配：HTTP 403，Recorder=0。
- Run scope 错配：HTTP 403，Recorder=0。
- Employee `idle/assigned + enabled` 可执行；`disabled`：HTTP 403，Recorder=0。
- 缺服务端 CEO UsageContext 时，UsageEvent 明确拒绝。

## 环境边界

- 测试使用注入式 Recorder，无真实 Provider 出网。
- 未启动服务、未注入 Key、未创建真实 Run、未调用模型、未跑全量回归。
- 端口 `3000/3100/8001/8002/8080` 全部关闭；Gateway/Workspace/JWKS/egress 容器均停止。

## 下一步

产品规划席读取本 Review，完成本 Issue 收口；如继续 Parent R3，只能重新走安全复核与总负责人单 Run 授权，不得复用已消费授权或历史失败 Run。

Next Seat：产品规划席  
Handoff: sent to 产品规划席
