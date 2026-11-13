# Workspace R4 第6项｜6a｜统一 Artifact/Output 字段与来源契约 Gate

- 日期：2026-07-18
- 状态：PASS — 6a 完成，字段来源与只读契约闭环
- 前置：`issues/20260718_workspace_r4_unified_artifact_output_backend_gate.md`
- 父项：`issues/20260718_workspace_r4_unified_artifact_output_backend_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席 → 质量运行席 → 产品规划席
- 分支：`feat/roadmap-r1r2`

## 结论

用于第6项收口的字段来源契约。约束所有后续 Output/Artifact 复核仅引用已落库事实，不新增模型原文派生字段。

## 目标

1. 固化 `artifact`（含 report envelope）字段来源：
   - `source = workflow_runs.final_report`
   - `content_sha256` 为 `SHA-256(workflow_runs.final_report)`
   - `content_bytes` 只读自 `workflow_runs.final_report` 长度
2. 固化 `project_status` 与 `artifact` 的关联可复核规则：
   - `tenant/company/project/run/task` 均必须由 `workflow_runs` + 运行历史链路可回放；
3. 明确不可接受的 fallback（如拼接旧字段、重置 final_report、跨字段拼包）；
4. 输出 one-shot SQL 与复核结果模板（只读）。

## 约束

- 不改执行器与历史数据；
- 不新增 API，不改 `final_report`；
- 不改 Admin，不改前端，不改 token/模型/凭据。

## 复核最小清单（非实施）

1. `workflow_runs` 查询链可读到 `workflow_run_id` 的完整 `final_report`；
2. `artifact.source` 与 `artifact.content_sha256/content_bytes` 与 `final_report` 一致；
3. 失败 run 不输出 `artifact`（除非已有合法 `final_report`）；
4. 只读验证脚本可复用：`reviews/20260717_workspace_r3_artifact_project_status_architecture_review.md`、`reviews/20260717_workspace_r3_artifact_project_status_closure_review.md`。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_unified_artifact_output_contract_gate.md`
Objective:
定义第6项 Artifact 字段与来源契约，确保输出仅源于 `workflow_runs.final_report`。
Special Constraints:
仅定义契约与复核模板，不做实现，不改历史，不发起新 run。
Next Seat:
质量运行席（复核一次）

Review:
`reviews/20260718_workspace_r4_unified_artifact_output_contract_gate_review.md`
