# Workspace R4 第8项｜8b｜AI Secretary 风控与失败阻断 Gate

- 日期：2026-07-18
- 状态：PASS — 8b.1/8b.2/8b.3 已完成质量复核，敏感日志边界已完成安全复核
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_backend_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）→ 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

- 定义失败、超限、越权、缺失事实时的统一阻断行为。
- 定义最小日志/回滚可见字段。

## 约束

- 不起新调用；
- 不新增前端；
- 不新增凭据。

## 当前核查事实（本轮）

- 目前无专用秘书消息服务、无外部消息网关；本轮对外失败仅复用既定 `401/400/403/404` 固定响应。
- 8b 先定义统一 fail-closed，不允许降级继续，不做跨租户重算。

## 任务拆分（本项 8b）

- 8b.1｜失败/超限阻断（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b1_failure_blocking_gate.md`
  - 输入非法、缺上下文、越权、容量超限统一阻断；
  - 一次失败不自动重试、不跨租户重算、不自动切换数据源。
- 8b.2｜来源完整性与篡改防护（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b2_source_integrity_tamper_gate.md`
  - 输出必须可追溯到 run/result/audit 记录；
  - 发现摘要缺失、引用失配、项目状态漂移时直接拒绝展示。
- 8b.3｜可见性与最小日志（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b3_minimal_logging_visibility_gate.md`
  - 仅记录结构化日志（tenant_id、对象 id、fail code、时间）；
  - 不记录 prompt 原文与 token 文本级副本。

## 本项验收（只读）

- 风控失败返回码统一为既定 `401/400/403/404` 与固定两字段响应；`CONFLICT`、`STALE_CONTEXT` 仅内部 fail_code 并映射 `404`；
- 无新网络出站行为；
- 不新增前端/新服务；
- 与 8a 边界保持一致。

## 当前进展

- 8b.1：PASS（质量复核通过）
- 8b.2：PASS（质量与安全复核通过）
- 8b.3：PASS（质量与安全复核通过）

## 复核入口

- `issues/20260718_workspace_r4_ai_secretary_risk_gate_8b_rollout_queue.md`

## 任务链（本项）

8b.1 → 8b.2 → 8b.3（完成顺序）

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_risk_gate.md`
Objective:
定义AI Secretary 风控与失败处理边界。
Special Constraints:
只读复核定义。
Next Seat:
质量运行席（复核一次）
Handoff: sent to 质量运行席
