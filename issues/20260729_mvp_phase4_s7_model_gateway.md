# MVP Phase 4 / S7 — Model Gateway

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase4_s7_model_gateway_review.md`

## Objective

按 Curis v1.0 既定 Model Gateway 完成：

- T015：把现有 New API / OpenAI-compatible Provider Adapter 与 Workspace Capability Registry、AI Employee Profile 接通。
- T016：用户创建 Task 时可从员工已绑定的 Model Capability 中人工选择；调用失败时受控回退到默认模型，并记录真实 Token 与成本。

## Product Boundary

- Model 仍是 Capability 资源，Task 不直接绑定具体 Provider SDK。
- 复用既有 `ModelGatewayAdapter`、`model_gateways`、`official_models`、员工 Capability Profile、Task/Execution 与 UsageEvent；不新增表、Admin 或第二套 Gateway。
- Provider 凭证继续由既有环境/Vault 边界注入；本 Sprint 不新增密钥存储或在 API/UI 返回密钥、Token、Authorization、Prompt 原文或原始响应。
- 人工选择只展示当前员工已启用且已绑定的 Model Capability；无选择时沿用现有默认模型。
- Fallback 只在人工选择模型调用失败且现有默认模型可用时执行一次；不实现智能调度、自动路由、预算限制或多级策略编辑器。

## Implementation

- Model Registry 补充真实调用模型 ID，并展示 Provider / Gateway / Model 状态。
- Task 创建抽屉读取员工 Capability Profile，保存人工选择的 Model Capability。
- 统一执行入口识别 official Model Capability；首选模型失败后回退到已配置默认模型，并保留最终模型 Token/成本事实。
- Workspace 提供当前 Provider、可用模型、人工偏好和本租户模型用量安全摘要。

## Allowed Files

- `issues/20260729_mvp_phase4_s7_model_gateway.md`
- `reviews/20260729_mvp_phase4_s7_model_gateway_review.md`
- `backend/app/main.py`
- `backend/app/capability_registry.py`
- `backend/app/model_gateway_workspace.py`
- `backend/app/orchestrator.py`
- `backend/app/result_store.py`
- `backend/app/task_jobs.py`
- `backend/app/tool_executor.py`
- `backend/tests/test_mvp_phase4_s7_model_gateway.py`
- `frontend/lib/capabilities.js`
- `frontend/app/ceo-office/capabilities/page.js`
- `frontend/app/ceo-office/capabilities/CapabilityFormDrawer.js`
- `frontend/app/ceo-office/capabilities/[type]/[id]/page.js`
- `frontend/app/ceo-office/projects/[id]/TaskFormDrawer.js`
- `frontend/app/ceo-office/execution/tasks/[id]/page.js`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. Workspace 可查看现有 Provider、可用 Model、调用模型 ID 与状态，不需要 Platform Admin。
2. 注册 Model Capability 时必须提供可调用模型 ID，且仍只保存安全元数据。
3. 创建 Project Task 时仅可人工选择该 AI Employee 已绑定并启用的 Model Capability。
4. 真实执行使用人工选择模型；该模型失败且默认模型可用时只回退一次。
5. Task/Execution 与 Workspace 用量摘要展示最终模型、Token 与真实/上游估算成本；无成本事实仍显示 `未记录`。
6. Fallback 失败明确失败，不把 mock、默认文案或 API 存在当作执行成功。
7. 不新增依赖、数据库表、Admin、Provider SDK、智能调度、Billing 或外部凭证。
8. 聚焦测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。
