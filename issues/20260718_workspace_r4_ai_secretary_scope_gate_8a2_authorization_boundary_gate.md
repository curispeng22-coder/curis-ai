# Workspace R4 第8项｜8a.2｜AI Secretary 越权与授权边界 Gate

- 日期：2026-07-18
- 状态：IN_PROGRESS — 8a.2a/8a.2b/8a.2c PASS（待质量复核），等待父项汇总复核
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1_source_contract_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（先完成）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

统一 Secretary 授权失败响应：无权/越权/缺 tenant 统一阻断，避免信息外泄与跨租户扩散。

## 约束

- 不改前端。
- 不起新调用。
- 不改历史记录。

## 任务

1. 定义统一拒绝行为：401、403/404、409 或 423 中一类并固定使用。
2. 定义缺 tenant、越权、会话不匹配的返回码与返回体。
3. 定义不回传对象存在性（统一空列表/统一文本）。

## 子任务（本轮）

- 8a.2a｜返回码单例化（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2a_status_code_singleton_gate.md`
  - 选择 1 个主返回码（建议 403）用于越权/不归属，401 专门用于缺 token/身份。
  - 同类错码不做多路分支兜底，避免泄露对象是否存在。
  - 产物：返回码选择矩阵（含优先级）。

- 8a.2b｜跨租户/失配封锁（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2b_cross_tenant_mismatch_lock_gate.md`
  - Tenant、Project、Run/Result 维度任意错配均拒绝，且不触发重试/降级展示。
  - 产物：跨租户与跨对象失配清单。

- 8a.2c｜状态码一致性与最小日志（系统交付）
  - 对应：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2c_logging_response_consistency_gate.md`
  - 统一 `secretary` 响应体（空 payload 或固定文本），不回传对象存活性。
  - 结构化日志仅保留 tenant_id、run_id/task_id、fail_code、time（不记录 prompt 明文）。
  - 产物：日志字段白名单与脱敏规则。

## 最低验收

- unauthorized / cross-tenant / missing tenant 全部 fail-closed。
- 未配置上下文不得返回历史对象明细。
- 不出现“自动降级继续”分支。

## 结果（本批次）

- 状态：进行中。8a.2a/8a.2b/8a.2c 已完成（待质量复核），等待 8a.3a 汇总复核。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate.md`。

## 执行顺序

8a.2a → 8a.2b → 8a.2c

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`
Objective:
统一 AI Secretary 越权与未授权阻断。
Special Constraints:
只读边界收敛，不改运行引擎。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
