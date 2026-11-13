---
title: Phase-5 Admin Billing MVP
priority: P1
phase: phase-5
owner: 产品经理(Xu)
status: draft
---

# Phase-5 Admin Billing MVP

## 背景
usage_event 已具备 7 维计量（tenant_id / employee_id / capability_type / capability_source / capability_id / model_gateway_id / model_name / tokens / estimated_cost / status / created_at），但 `estimated_cost` 为 env 单价估算、非权威计费；且 `usage.*` 属 evolution 事件、语义非账务（审计白名单已显式排除 `usage.*`，见 database.py:1870）。客户需要用量归因与计费雏形来验证商业模式。

## 目标
在现有 usage_event 基础上，新增 `billing_event`（或 `evolution_events` 扩展 `billing.*` 命名空间）+ 只读聚合 API，提供租户计量 / plan_tier 计量 / 周期聚合；**计量层先行，权威 cost 对齐等 G2 Gate**。

## 不做范围
- 不修改 `result_store.py` 写路径
- 不实现真实扣费 / invoice 出具 / 支付
- 不依赖 G2（计量层独立先行）
- 不进入真实凭证托管

## 数据模型影响
新增 `billing_event` 或 `evolution_events` 扩展 `billing.*` + 复用 `tenants.plan_tier`（database.py:909 已存在）。

## API 影响
新增 `/api/platform/billing` 只读聚合（复制 fail-closed，`tenant_id` 必填，仿 main.py:967），不改 `result_store.py:567` 写路径。

## UI 影响
新增 `/api/platform/billing` 对应的 Admin 只读用量 / 计费聚合视图（租户隔离，tenant_id 必填）；复用现有用量页呈现。

## 安全边界
只读聚合 + tenant 隔离（复制 usage 的 fail-closed，tenant_id 必填）；若 `billing.*` 需入审计须同步扩展 database.py:1870 白名单。

## 测试要求
`test_d5_billing.py` 覆盖 tenant 隔离 / plan_tier 计量 / 周期聚合（仿 test_d5_workspace_integration.py:150-253 多维断言风格）。

## 验收标准
1. test_d5_billing.py 覆盖 tenant 隔离 / plan_tier 计量 / 周期聚合
2. 只读聚合 fail-closed（tenant_id 必填）
3. 不影响 usage_event 写入路径
4. 不暴露明文成本字段

## 关联
- 权威 cost 对齐依赖 `issues/phase5_g2_credential_vault_gate.md`（P0）
- 计量层可先于 G2 落地，请勿因等待 G2 而整体推迟 Billing 规划
