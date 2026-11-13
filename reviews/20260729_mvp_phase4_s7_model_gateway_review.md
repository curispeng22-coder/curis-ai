# MVP Phase 4 / S7 — Model Gateway Review

Date: 2026-07-29

Status: PASS

Issue: `issues/20260729_mvp_phase4_s7_model_gateway.md`

## Conclusion

T015 / T016 的 Provider 接入、人工模型选择、单次默认模型回退与真实用量记录闭环通过，本 Issue 关闭。

## Implemented

- 复用既有 `ModelGatewayAdapter`、New API / OpenAI-compatible Gateway、官方 Capability Registry、员工 Capability Profile、Task / Execution / UsageEvent；未新增表、依赖、Admin、Provider SDK 或第二套 Gateway。
- Model Capability 登记必须提供真实调用模型 ID；Workspace 安全摘要展示 Provider、模型、默认运行配置状态与当前租户模型用量，不返回凭证、Prompt 或原始响应。
- 创建 Project Task 时只展示并保存当前执行员工已绑定、已启用的官方 Model Capability。
- 统一执行入口调用人工选择模型；失败时仅回退一次到现有默认模型，回退失败保持明确失败。
- Task Job 与任务详情展示最终 Gateway / Model、Token、上游估算成本、币种与回退事实；无成本事实继续显示 `未记录`。
- 移动端执行事实使用可收缩事实网格，长模型 ID 不产生横向溢出。

## Passed Evidence

- `backend/.venv/bin/python -m pytest -q backend/tests/test_mvp_phase4_s7_model_gateway.py backend/tests/test_mvp_phase4_s6_capability_registry.py backend/tests/test_model_gateway_adapter.py::ModelGatewayAdapterTest::test_usage_event_payload_is_allowlisted_and_redacts_secret_like_values`：7 passed。
- `npm run lint`：PASS。
- `npm run build`：PASS，26 个静态页面生成成功。
- `git diff --check`：PASS。
- Desktop browser（隔离临时库与本地 OpenAI-compatible 验收 Provider）：
  - 员工绑定 `model.browser-primary` 后，任务抽屉仅展示员工已绑定模型；
  - 人工选择 `browser-primary` 创建并执行真实 Project Task；
  - 首选模型返回 503 后仅回退一次到 `browser-fallback`，Task 最终完成并输出“浏览器回退执行成功”；
  - 任务详情展示最终模型 `browser-fallback`、13 Token、`$0.0065 USD` 与 `browser-primary → browser-fallback`；
  - 模型能力详情展示 New API Gateway 已连接及明确的单次回退策略。
- Mobile browser（390×844）：`scrollWidth = clientWidth = 390`；任务状态、最终模型、Token、成本与回退事实单列可读。

## Full Regression

在 `628336dd59fce83961817da06bf3aa4b4c32f3fc` 干净提交树应用本 Issue 暂存差异后执行：

```bash
backend/.venv/bin/python -m pytest -q backend/tests
```

结果：`1125 passed, 2 skipped, 0 failed`。

## Boundaries

- 未实现智能路由、多级 Fallback、预算策略、Billing、Provider 管理器或凭证存储。
- 未改变 Curis v1.0 Capability / Gateway / Task / UsageEvent 架构。
- S8 研发模板与 Git / Codex / Claude Code / 测试 Workflow 未进入本 Sprint。

Handoff: sent to main thread
