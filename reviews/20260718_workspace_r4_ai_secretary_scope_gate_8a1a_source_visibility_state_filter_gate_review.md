# Workspace R4 第8项｜8a.1a.2 来源状态过滤 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_visibility_state_filter_gate.md`
- 分支：`feat/roadmap-r1r2`
- 复核基线：`fb827c37f4b7e7202326dc94e5648de6a4c8200c`
- 结论：`PASS`

## 结论

四类来源对象的状态白名单明确且为单值白名单；非接受态不得继续透传关联子对象。状态命中不能替代来源作用域校验，`tenant / project / workflow` 一致性仍须按入口上下文和父链 fail-closed 核验。

唯一缺口：无。可推进 `8a.1a.3`。

## 独立核对

| 来源对象 | 唯一接受态 | 非接受态处理 |
| --- | --- | --- |
| `workflow_runs` | `succeeded` | `pending / running / failed` 拒绝；其关联 `step_results` 不得单独透传 |
| `step_results` | `succeeded` | 其它状态拒绝；必须经 `workflow_step_id → workflow_run` 父链复核来源作用域 |
| `publish_packages` | `published` | `generated / failed` 保留源数据，但不得成为 Secretary 输入 |
| `content_workflow_runs` | `completed` | `running / failed` 拒绝，不得透传其关联子对象 |

## 一致性与 fail-closed

- 状态白名单只是必要条件，不是绕过来源字段白名单的授权。
- `workflow_runs` 必须与入口 `tenant_id / project_id / workflow` 一致；`step_results` 必须沿所属 Step 和 Run 继承并复核同一作用域。
- `publish_packages`、`content_workflow_runs` 继续受既有 tenant 范围读取约束；状态过滤不得扩大到其它 tenant。
- 对当前数据模型没有可核验 `project_id` 的来源，不得伪造项目归属或仅凭状态放行；后续运行时只能按已定义映射 fail-closed。

## 新鲜证据

执行现有聚焦验证，未启动服务、未出网：

```text
PYTHONPATH=backend backend/.venv/bin/python -m pytest -q \
  backend/tests/test_model_gateway_adapter.py \
  -k 'r3_workflow_allows_seven_ordered_steps_once'
```

结果：`1 passed, 24 deselected`。确认当前七步链完成态为 `workflow_runs.status=succeeded`，对应 Step/StepResult 为成功终态。

```text
PYTHONPATH=backend backend/.venv/bin/python -m pytest -q \
  backend/tests/test_v1_wave2_results.py \
  backend/tests/test_workspace_identity_membership.py::test_http_200_401_403_404
```

结果：`4 passed`。确认现有成果来源包含 `published` 包、`completed` 内容运行，并保持 tenant 身份/成员隔离基线。

静态核对确认：现有 `WorkflowRuntime` 写入成功 Run/StepResult 为 `succeeded`；成果汇总只将 `published`、`completed` 计入完成统计；四类读取均以当前 tenant 为边界。上述证据仅证明来源状态和既有隔离基线，本 Gate 为只读契约复核，不声称 Secretary 运行时过滤接口已实现。

## 范围声明

- 未修改实现、配置、数据库或历史记录。
- 未启动服务、未出网、未运行全量回归。
- 未推进 `8a.1a.3`；由产品规划席接收本 Review 后继续调度。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
