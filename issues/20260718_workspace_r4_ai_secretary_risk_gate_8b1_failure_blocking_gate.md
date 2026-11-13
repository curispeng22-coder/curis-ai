# Workspace R4 第8项｜8b.1｜失败与超限阻断 Gate

- 日期：2026-07-18
- 状态：PASS（定义完成；待质量运行席复核）
- 父项：`issues/20260718_workspace_r4_ai_secretary_risk_gate.md`
- Owner：系统交付席
- Next Seat：系统交付席（定义）→ 质量运行席（复核）
- 分支：`feat/roadmap-r1r2`

## 目标

统一 AI Secretary 在输入非法、上下文缺失、越权、超限时的 fail-closed 阻断行为。

## 约束

- 不起新调用
- 不改前端
- 不新增凭据

## 统一失败矩阵（优先级）

1. `401`：缺 tenant/缺身份上下文（最优先）
2. `400`：参数非法、类型非法、必填空缺
3. `403`：越权/身份与 tenant/project/run 不匹配
4. `404`：对象不存在、不可见，或只读来源快照/状态不能安全承接

### 内部风险分类（不对外）

- `CONFLICT`：来源快照或状态冲突；对外映射既定 `404` 固定体。
- `STALE_CONTEXT`：非终态或不可安全读取；对外映射既定 `404` 固定体。
- 配额/速率与外部依赖异常不属于当前无新模型、无新接口、无外部消息服务的只读范围；本轮不新增限流、重试或依赖处理路径。

## 阻断规则（8b.1）

- 任一条件触发即立即终止本次请求，不返回部分成功集合。
- 无自动重试、无跨 tenant 重算、无自动改参数重放。
- 同一次调用最多一类失败码。
- 不对可疑来源做“降级返回空但成功”或“下一可用路由切换”。

## 对外失败响应与日志

- 对外仅允许 `401/400/403/404`，逐字复用 8a 已批准的对应固定两字段响应体与优先级 `401 > 400 > 403 > 404`。
- `CONFLICT`、`STALE_CONTEXT` 仅为内部 `fail_code`，仅能进入既定最小日志字段；不得新增对外字段、文案或状态码。

## 任务成果

- 失败优先级、内部风险映射与对外固定体冻结。
- 失败后无 partial body。
- 不跨租户/不降级继续。

## 复核入口

- `issues/20260718_workspace_r4_ai_secretary_risk_gate.md`

## Compact Handoff
Issue:
`issues/20260718_workspace_r4_ai_secretary_risk_gate_8b1_failure_blocking_gate.md`
Objective:
定义 AI Secretary 失败/超限/越权的单一阻断行为与返回优先级。
Special Constraints:
只读边界定义；不改 runtime，不起新调用。
Next Seat:
质量运行席


## 结果（待复核）

- 与 8b.1_rollout_queue 对齐，等待质量运行席一次性 focused 复核。

Handoff: sent to 质量运行席
