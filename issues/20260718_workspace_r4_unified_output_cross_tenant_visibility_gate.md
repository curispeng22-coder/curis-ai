# Workspace R4 第6项｜6b｜统一 Output/Artifact 可见域与 fail-closed Gate

- 日期：2026-07-18
- 状态：PASS — 6b 完成，跨租户/错Run fail-closed 与可见域约束闭环
- 前置：`issues/20260718_workspace_r4_unified_artifact_output_contract_gate.md`
- 父项：`issues/20260718_workspace_r4_unified_artifact_output_backend_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 质量运行席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 目标

统一定义第6项 Output 读取可见域：`GET /api/workspace/workflows/{workflow_run_id}` 必须严格按 tenant/company/project/run 边界 fail-closed。

## 约束

1. 不新增路由；
2. 不扩展权限模型；
3. 不调用模型/外网；
4. 不改历史。

## 必要边界

- 入参 `workflow_run_id` 解析成功但租户不符：返回 404（或等价 fail-closed）；
- 访问未授权 run（包括不同 tenant/project）的 `artifact/project_status`：不可读到任何 `step_results/usage`；
- 请求头中仅保留 `X-Tenant-Id` 等现有输入，不引入额外 tenant 来源；
- 命中错 tenant 后不得返回 `artifact/content` 内容。

## 输出

- 可复用复核样本（运行库读链）：
  - 成功 run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`、`wfr-16c20143-0119-4ae8-923a-8746fc01ad2e`
  - 历史失败 run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`、`wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`
- 复核失败样本仅验证 `status/reason/tenant/project` 无越权输出。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_unified_output_cross_tenant_visibility_gate.md`
Objective:
统一定义第6项 Output/Artifact 可见域 fail-closed 与错租户/错Run拒绝行为。
Special Constraints:
只定义边界，不改实现，不新增前端，不改权限。
Next Seat:
系统交付席（产出复核要点）→ 质量运行席（focused验证）

Review:
`reviews/20260718_workspace_r4_unified_output_cross_tenant_visibility_gate_review.md`
