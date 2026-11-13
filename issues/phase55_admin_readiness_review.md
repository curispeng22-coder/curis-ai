---
title: Phase-5.5 Admin Readiness Review（待命态三项只读复核）
phase: phase-5.5 (post-G2, standby)
owner: 主理人(Qi) 依代码实测起草 / 架构师(Gao) 待 Agent 恢复后复核补签
status: review-only (零代码改动)
related: issues/phase5_billing_mvp.md, issues/phase5_g2_credential_vault_gate.md
constraint: 不新增功能 / 不实现 Billing / 不实现 Marketplace / 不修改 Credential Vault 边界 / Admin·Workspace 边界仅复核不改
---

# Phase-5.5 Admin Readiness Review（待命态三项只读复核）

> 本文件是 Phase-5.5 Post-G2 Roadmap Review 等待态下，Admin Platform 被授权的三项低风险只读复核。
> **零代码改动**，仅实测取证 + 结论，为 Workspace 输出 Phase-5.5 Roadmap Review 后的决策点（Admin 是否进入 Billing 研究 / workflow usage governance 支持）备好底。
>
> 注：架构师 Agent 通道本次不可用（底层基础设施故障），由主理人齐活林依代码实测取证起草；待 Agent 恢复后由高见远复核补签。

## 复核 1 · usage_event 是否足够支持未来 workflow_run_id / workflow_step_id / employee_id 归因

### 现状证据
- **写入**：`backend/app/result_store.py:567` `_record_usage_events` → payload 为**扁平 JSON**（line 602+）
  - 已含 `employee_id`(608)、`employee_role`(609)、`employee_name`(610)、`task_id`(605)、`ceo_id`(606)
  - **缺失** `workflow_run_id` / `workflow_step_id`
- **读取投影**：`backend/app/evolution_event_log.py:124` `_usage_event_from_row` → 已投影 `employee_id`(137)、`task_id`(136)
  - **未投影** `workflow_run_id` / `workflow_step_id`
- **存储**：`evolution_events.payload` 为 JSON 列；`list_usage_events`(75-115) 用 `json_extract(payload,'$.field')` 过滤 7 维

### 结论
| 归因维度 | 状态 | 说明 |
|---------|------|------|
| `employee_id` | ✅ 已就绪 | 写入+投影均已支持，可立即按员工查询用量 |
| `task_id` | ✅ 已就绪 | 已落库 |
| `workflow_run_id` | ⚠️ 需最小扩展 | payload + 投影各加 1 字段，**零 schema 迁移**（JSON 列） |
| `workflow_step_id` | ⚠️ 需最小扩展 | 同上 |

### 建议（记录兼容性，当前不实施）
- 在 `result_store.py` payload 与 `_usage_event_from_row` 投影各预留 `workflow_run_id` / `workflow_step_id` 两个**可选字段**（默认空），待 Workspace Phase-6 Workflow MVP 确定写入时机后启用。
- 因 payload 为 JSON，**无需 ALTER TABLE**，属非破坏性扩展。
- **不阻塞**后续决策。

## 复核 2 · audit_event 是否可扩展 workflow 状态事件

### 现状证据
- **白名单**：`backend/app/database.py:2005` `list_audit_events` 仅暴露 `capability.%` / `governance.%` / `credential.%`
- **写入约束**：`backend/app/governance.py:23` 受控写仅限 `governance.propose` / `governance.apply`；其余 event_type 由各域写入 `evolution_events`
- `event_type` 为字符串列，无枚举约束

### 结论
- **可扩展，低风险**：新增 `workflow.%` 命名空间只需在 `database.py:2005` 白名单增加一处 OR 子句（如 `event_type like 'workflow.%'`），不影响既有 `capability./governance./credential.` 过滤。
- **回归风险低**：白名单是纯 SELECT 过滤，扩展为超集，既有查询行为不变。
- 需配套：定义 workflow 事件命名约定（如 `workflow.run.started` / `workflow.step.completed` / `workflow.run.finished`）并由受控写者（orchestrator）写入，遵循现有「零写审计投影」原则。

### 建议
- 扩展方式已明确，无需现在实施；待决定进入 workflow usage governance 支持时，作为该 issue 的**首个低风险变更**（白名单 + 受控写入 + 测试）。
- **不阻塞**后续决策。

## 复核 3 · Admin / Workspace 边界是否仍稳定

### 现状证据
- **Admin 守卫**：`backend/app/main.py:930` `_require_platform_admin` → 缺/错令牌 401；**所有** `/api/platform/*` 路由均调用（943, 999, 1028, 1085, 1145, 1183, 1228 等）
- **Workspace 只读目录**：`/api/catalog/*` 均为 GET（505 department-types, 516 models, 525 capabilities, 536 tools, 543 connectors, 1274 gateways）
- **tenant_private 写归属 Workspace**：`/api/workspace/capabilities/private`(562 POST)、`/api/workspace/private-models`(672 POST) 等，使用 `TenantContext.current_tenant_id()`，**不调用** `_require_platform_admin`，**不属** `/api/platform/*`
- **Admin 写恒 official**：`/api/platform/*` 写入路径 `source='official'`；全仓 Admin 路由零 tenant_private 引用

### 结论
- **边界仍稳定**：接口命名空间分离（`/api/platform` 管理 vs `/api/workspace` 租户私有 vs `/api/catalog` 只读目录）+ `_require_platform_admin` 守卫 + tenant_private 由 Workspace 自有路由写入，三层机制在现有代码中完整保留。
- 当前 git 工作树含 Workspace 线未提交变更，但边界机制（路由命名 + 守卫）未被破坏；**无新增 Admin 路由绕过守卫或写入 tenant_private 的路径**。

### 建议
- 待 Workspace Phase-5.5 评审产出后，若 Admin 进入 workflow usage governance 支持，须继续遵循：新增 Admin 路由必须 `_require_platform_admin`；workflow 用量观测走只读投影，不新增 tenant_private 写权限。
- **不阻塞**后续决策。

## 综合结论（主理人齐活林）

三项复核均**不阻塞** Admin 后续决策：

- **若进入 Billing 研究**：usage_event 已含 employee/task 归因；`estimated_cost` 为演示估算（Phase-4.5 已知），Billing 研究可基于现有 payload 扩展 `billing_event`（详见 `issues/phase5_billing_mvp.md`）。
- **若进入 workflow usage governance 支持**：usage_event 加 2 字段 + audit 白名单加 1 子句即可支撑，均为最小低风险变更。
- **Admin 边界稳定**：新增治理观测不需放宽现有安全模型。

**Admin 保持待命（standby）**：未做任何实现改动、未碰 Credential Vault 边界、未进入 Billing / Marketplace / 新治理功能。等待 Workspace 输出 Phase-5.5 Roadmap Review。

---

*主理人齐活林 依代码实测取证起草（evolution_event_log.py / result_store.py / database.py / main.py）；架构师高见远复核补签待 Agent 通道恢复。*
