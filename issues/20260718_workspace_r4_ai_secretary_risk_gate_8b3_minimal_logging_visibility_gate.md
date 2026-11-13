# Workspace R4 第8项｜8b.3｜可见性与最小日志 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_ai_secretary_risk_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

定义 AI Secretary 风控失败可见性与日志字段最小集，避免 prompt 文本/令牌文本入库或回放。

## 约束

- 不改前端。
- 不新增日志后端。
- 不存储高敏明文。

## 最小日志字段

- 记录项（仅失败事件）：
  - `timestamp`
  - `tenant_id`
  - `project_id`
  - `run_id`
  - `task_id`
  - `fail_code`
  - `step`（如有）

- 禁止记录：
  - `prompt`
  - `raw_input`
  - `tool_payload`
  - `api_secret`
  - `token_text`
  - `employee_personal_text`
  - `principal` 及其 hash/digest/count 变体
  - `Authorization`、`cookie`、`JWT`、`member_token`、实体细节

## 响应日志一致性（8b.3）

- 查询成功：不新增日志字段或可执行 side effect。
- 失败：对外逐字复用 8a 已批准的对应固定两字段响应体；`fail_code` 仅进入上述内部最小日志，不泄露对象数量/存在性。
- 成功/失败都不新增可执行 side effect。

## 任务成果

- 成果字段白名单固化。
- 审计字段固定最小化。
- 与 8a 来源边界兼容。

## 复核入口

- `issues/20260718_workspace_r4_ai_secretary_risk_gate.md`

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b3_minimal_logging_visibility_gate.md`
Objective:
冻结 AI Secretary 风控日志最小字段与失败可见性输出边界。
Special Constraints:
只定义日志与响应边界，不改变调用链与模型。
Next Seat:
质量运行席


## 结果（待复核）

- 与 8b.3_rollout_queue 对齐，等待质量运行席一次性 focused 复核。

Handoff: sent to 质量运行席
