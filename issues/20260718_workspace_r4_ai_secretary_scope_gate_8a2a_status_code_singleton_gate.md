# Workspace R4 第8项｜8a.2a｜返回码单例化 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

统一授权失败返回码策略，固定单码路径，避免分支变异导致行为泄露。

## 约束

- 不起新接口。
- 不改前端。
- 不改历史运行记录。

## 任务

1. 选择 1 套主返回码用于越权与归属失败。
2. 明确 401 的唯一适用场景。
3. 写出同类错误优先级，保证请求只出现 1 个主码。

## 返回码单例化策略

- 401：身份域缺失/无效（缺 tenant、Token 不可解析）。
- 403：授权失败、跨租户/跨项目尝试访问、对象归属不匹配（tenant/project/company/department/employee/workflow/task/ run/task）。
- 404：对象不存在（source id 命中不到）或被过滤为不可见状态，不泄露是否存在。
- 400：输入参数形态错误（空字符串、类型不合法）——适用于 8a.1a/8a.1b 及其下游判定；与其它失败同时命中时严格按下列全局优先级处理。
- 413：不适用本轮（未纳入单例集合）。

### 优先级（从高到低）

1. 401 > 400 > 403 > 404
2. 若同时满足多项，取最高优先项并立即终止。
3. 任一失败命中后不得返回 200、不得继续读子对象。

## 产物

- 返回码矩阵（401/403/404/400）与优先级表。
- 单码判定文案与统一响应体。

## 固定响应复用

- `401`、`400`、`403`、`404` 必须逐字复用 `issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_refusal_response_contract_gate.md` 的对应固定体。
- 只允许 `error_code`、`message`；不得按授权失败来源、实体 ID、归属字段、状态或查询路径增加字段、文案或细节。

## 结果（本批次）

- 状态：PASS（返回码单例化定义完成；待质量复核）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2_authorization_boundary_gate.md`。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a2a_status_code_singleton_gate.md`
Objective:
统一 AI Secretary 授权失败主返回码。
Special Constraints:
只读复核定义，不改引擎。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
