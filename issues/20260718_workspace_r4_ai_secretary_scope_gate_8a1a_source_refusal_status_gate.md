# Workspace R4 第8项｜8a.1a.3｜缺失/失配拒绝码映射 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 前置：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_visibility_state_filter_gate.md`
- 父项：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

统一定义 8a.1a 场景下的 fail-closed 错误返回（缺失、失配、不可读状态、跨租户或未授权来源）行为边界。

## 任务

1. 固定缺失 context_id/必要参数时的返回码与原因。
2. 固定来源对象不存在、状态不允许、字段不完整时的返回码与原因。
3. 固定 tenant/project/company/dept/workflow/task 不一致时的返回码与原因。

## 失败码（先后次序）

- 缺 tenant：`401`。
- 关键参数缺失或空字符串：`400`。
- 对象不存在（任意来源 ID 未命中）：`404`。
- 关联状态不允许（见 8a.1a.2）：`404`。
- 字段不完整/字段类型不匹配：`400`。
- tenant/project/company/department/task/workflow 关联不一致：`403`。

## 统一约束

- 一次请求只出现一个失败码；
- 一旦任一失败命中立即终止，不返回部分集合；
- 不泄露是否存在的差异化信息（统一失败响应）。
- 若命中多个条件，优先级固定为：`401` > `400` > `403` > `404`。

## 统一失败优先级（执行器）

1. `401`：鉴权前置失败（缺少 tenant、缺失 access context）。
2. `400`：参数缺失、空白值、字段类型不匹配（包含必填字段空、非法 null/空字符串）。
3. `403`：租户/项目/公司/部门/任务/流程五元组任一不一致、跨域读取尝试。
4. `404`：来源对象不存在、状态不可读、主对象缺失后续子对象。

### 统一行为约束（8a.1a）

- 任何一次 8a.1a 查询，最多只出现一个 HTTP 状态码。
- 无论对象缺失/失配，最终返回体固定、不可区分实体差异。
- 一旦拒绝，当前请求不允许查询任何关联表。

## 产物

- fail-closed 返回码矩阵（401/403/404/400）。
- 统一错误文案/行为边界清单。

## 结果（本批次）

- 状态：PASS（定义完成；待质量运行席复核）。
- 复核入口：`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_id_whitelist_gate.md`。

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_scope_gate_8a1a_source_refusal_status_gate.md`
Objective:
统一 8a.1a 的缺失与失配拒绝码边界。
Special Constraints:
不新增模型/接口，不起新 run。
Next Seat:
质量运行席（复核）

Handoff: sent to 质量运行席
