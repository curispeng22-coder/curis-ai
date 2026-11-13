# Workspace R4 第1～7项代码构造独立审计 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_r4_items_1_7_code_construction_audit_gate.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`2da0367be0e8185421523d608f8fb4e1f7c7d737`
- 总结论：`BLOCKED`
- 允许恢复 8a.1a.2：`否`

## 总结

第1～6项在各自已声明的“只读投影/保守边界定义”范围内与代码和 focused 证据一致。第7项存在一个可独立复现的 fail-open：统一 Artifact/项目状态投影接受 `estimated_cost=0` 且缺少 `price_version` 的 usage，仍返回 `execution_status=completed` 和金额为 0 的 artifact。这与第7项“成本缺失或不可信时显示 unknown 并阻断预算判断”直接冲突。

因此本审计整体为 `BLOCKED`，第8项 8a.1a.2 不得恢复。

## 逐项结论

### 第1项｜项目长期状态与 Memory：PASS

- 代码入口：`WorkflowRuntime.get_run` → `_add_read_projection`。
- 数据读取：run、step、assignment、result、execution、usage、project 均从数据库只读回放；run/step/result/execution/usage/project 查询均带 tenant 约束。
- fail-closed：run 不存在返回 404；链路数量、顺序、归属、模型或结果不一致时 `artifact=None`、`execution_status=incomplete`。
- 状态源：`projects.status` 只作为 `stored_status`；执行状态来自 read projection，不回写 `projects`，没有把人工 project metadata 状态冒充执行状态。
- Memory 是版本化 scope key 与数据库恢复读法的边界定义，没有新增外部或内存状态源，符合 Gate 的“不实现新运行时”限制。
- 证据与 A1/A2/A3、B1/B2/B3 Review 一致。

### 第2项｜多项目 Session：PASS

- 实际入口仍为 tenant/project/run 只读链；没有新增 Session API 或独立缓存状态源。
- scope key 固定包含 `tenant_id + employee_id + project_id + scope`，不会只按 employee 复用。
- 样本员工跨两个 project 的 run 集合互斥；反向 project/run 查询无交集，失败与成功历史未被另一 project 覆盖。
- 该项只证明“项目级隔离边界”，不声称已有独立 Session Runtime，和 Gate/Review 一致。

### 第3项｜Agent / Workflow / Hybrid Mode：PASS（保守口径）

- 实际代码入口只有现有 `WorkflowRuntime.run_next_step` 顺序执行；没有独立 Agent/Hybrid mode 字段、切换 API 或第二状态源。
- 顺序、失败阻断与 run 隔离由现有 WorkflowRuntime 提供；显式 mode/handoff/switch 仍缺失。
- 原 M1/M3/M4c Review 的 `PARTIAL` 没有被误写成“模式运行时已实现”；父 Gate 明确按边界定义保守收口。因此本审计仅对该保守范围判 PASS，不扩大为 Agent/Hybrid 功能 PASS。

### 第4项｜自动推进、超时、恢复：PASS

- `run_next_step` 只选择最小 pending Step；终态直接返回，已有失败 Step 时不继续推进。
- `ModelGatewayAdapter` 固定 60 秒超时；没有自动重试循环。429 首次调用失败后，同一 run 不新增出网尝试。
- 重复、跳步、预算不足、错误 project/run 均在出网前拒绝。
- 恢复仍是只读派生判断，不存在后台调度器或隐式恢复状态源。

### 第5项｜停止、人工接管、风险升级：PASS

- Workspace 仅有创建 Run、读取 Run、`run-next-step`；没有 cancel/reset/reopen 接口。
- failed/succeeded/cancelled Run 为终态；失败 Step 会同步写 Run failed 与成对失败审计事件。
- 人工接管仅定义为人工确认后创建新 Run，不改写历史；Hold/Escalate 不触发后台重试。
- 该项为只读边界定义，不声称已存在人工接管运行时，和 Gate/Review 一致。

### 第6项｜统一 Artifact / Output：PASS

- 单一入口：`WorkflowRuntime._add_read_projection`，Artifact 只来自 `workflow_runs.final_report`。
- 仅在 7 个 Step/Result/Execution/Usage 全部唯一、成功、同 tenant/company/project/run/task 且项目存在时生成 Artifact。
- GET Run 的全部底层读取带 tenant 条件；跨 tenant、缺 tenant、错 run 均 fail-closed。
- Artifact、项目执行状态与第1项复用同一读投影，没有第二成果状态源。

### 第7项｜Token / 成本 / 预算：BLOCKED

通过项：

- `/api/platform/usage`、`/api/platform/usage-meter` 均要求 Admin 且 `tenant_id` 必填；跨 tenant 不聚合。
- 已批准真实 Run 的 7 条 usage 合计 9,622 tokens / USD 0.013269，与 Review 一致。
- R3 出网前预算闸门会检查历史 usage 的正成本、price_version 和累计上限。

阻塞证据：

- `backend/app/workflow_runtime.py:286-293` 只验证 `estimated_cost` 是数字，不验证 `> 0`，也不验证 `price_version` 存在且一致。
- `backend/app/workflow_runtime.py:331-333` 直接求和并返回金额。
- 内存构造 7 条 `estimated_cost=0`、无 `price_version` 的 usage 后，实际输出：

```text
execution_status=completed
artifact_present=True
estimated_cost=0.0
```

这会把不可信成本当作真实 0 成本展示，绕过第7项 fail-closed 契约。既有 focused 只覆盖“当前样本成本均有效”，没有覆盖 0/缺价格反例。

## 跨项审计

- 未发现 alternate Run/Session/Mode/Manual API 可绕过 `WorkflowRuntime` 顺序与终态守卫。
- 项目执行状态、Artifact、Token/成本读取共用 run/step/result/execution/usage 链，没有跨 tenant 查询分支。
- 第1～6项没有重复持久化状态源；Session、Mode、人工接管均保持定义层，没有伪装成已实现运行时。
- 唯一跨项缺口位于第7项成本有效性：第6项 Artifact 投影复用该金额后会把无效 0 成本暴露为已完成成果。

## Focused 证据

在正确 Admin 环境变量下独立运行 14 个 focused case，结果：`14 passed`。覆盖：

- Workflow 七步顺序与失败终止；
- R3 固定价格/上限、429 零重试；
- 重复结果、跳步、预算不足、错误 project 出网前拒绝；
- Artifact/项目状态只读投影；
- usage-meter Admin、tenant 必填和跨 tenant 隔离；
- Workspace 200/401/403/404 身份边界。

另执行一条纯内存、零写入的成本反例复核，稳定复现第7项 fail-open。未启动服务、未出网、未运行全量。

## 唯一最小修复 Issue

建议产品规划席仅创建并派发：

`issues/20260718_workspace_r4_unified_token_cost_budget_projection_failclosed_fix_gate.md`

最小范围：只修正 `_add_read_projection` 的成本可信性判断，并增加一个 focused 反例；当任一 usage 的 `estimated_cost` 缺失/非数字/`<=0`，或 `price_version` 缺失/不一致时，必须返回 unknown/不可结算语义并保持预算判断阻断。不得改 schema、模型调用、网关、前端或历史数据。

## 最终状态

- 第1项：PASS
- 第2项：PASS
- 第3项：PASS（保守边界定义）
- 第4项：PASS
- 第5项：PASS
- 第6项：PASS
- 第7项：BLOCKED
- 跨项：BLOCKED
- 8a.1a.2：继续冻结

Next Seat: 产品规划席

Handoff: sent to 产品规划席
