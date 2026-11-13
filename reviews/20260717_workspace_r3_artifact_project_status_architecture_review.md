# R3 Artifact 与 Project Status Closure Architecture Review

Issue：`issues/20260717_workspace_r3_artifact_project_status_closure.md`  
Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`  
结论：`PASS`（复用现有持久化与 HTTP 读取；不新增存储、不出网）。

## 唯一最小 Artifact

不新增对象存储、成果平台或 Memory。唯一 Artifact 是现有 `workflow_runs.final_report` 的 document/report 投影，正文逐字来自该字段，不重新生成、不调用模型、不拼接新的解释文本。

Artifact envelope 只增加可验证元数据：

- `artifact_type=document_report`；
- `tenant_id`、`company_id`、`project_id`、`workflow_run_id`、`task_id`；
- 7 个 `workflow_step_id`、对应 `step_result_id`、step order/status；
- `content_sha256=2d14cf90ca1fa850f7e8425763b922cda4c6c9c2132a2f55eac07791a07ba96c`；
- `content_length=6018` bytes；
- `model_gateway_id/model_name`、UsageEvent reference、`total_tokens=9622`、`estimated_cost=0.013269`；
- `source=workflow_runs.final_report`、immutable source reference。

正文不得使用首步/单个 StepResult 替代 final_report；七步、七个 Result、七个 Execution 和唯一 UsageEvent 必须全部存在且 scope 一致。

## 真实可打开方式

复用现有 Workspace HTTP：

`GET /api/workspace/workflows/wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`

该接口已返回 Run、steps、step_results 与 `final_report`，因此可打开并验证报告正文、Step 追溯和 Run 状态。Artifact envelope 可作为该接口的只读派生字段；不落新文件、不写 DB。跨租户请求必须按现有 TenantContext 返回 404，不能仅凭 Run ID 读取。

## Project Status 与下一步建议

Project 状态只做确定性读投影，不改写 `projects.status`：

- 当 Run= succeeded、7/7 Step= succeeded、7/7 StepResult 存在、final_report 非空且 hash/length 匹配时，派生 `execution_status=completed`；
- 任一条件不满足时，派生 `execution_status=incomplete`，不得伪称项目完成；
- 原有 `projects.status` 保持数据库事实，不由本投影静默更新。

`next_step_suggestion` 只允许引用 final_report 中已经明确存在的建议段/结构化字段；当前没有独立建议字段时返回 `null`，不能静态补写、不能调用模型、不能从标题猜测。报告中的原文建议若存在，只能携带原文及其位置 reference。

## 幂等、冲突、隔离与回滚

- Artifact identity 固定为 `(tenant_id, workflow_run_id, content_sha256)`；同值重复读取返回同一 envelope，不产生第二 Artifact。
- Run 不属于当前 tenant、company/project 不一致、不是固定 Workflow、Step/Result/Execution 数量不是 7、存在重复或跨租户记录、hash/length 不匹配、UsageEvent 不唯一或模型/成本元数据不一致，均 fail-closed 返回明确不完整/冲突结果。
- 原始 Run、StepResult、Execution、UsageEvent 和 final_report immutable；不修补、不删除、不复制历史失败 Run。
- 回滚无需数据回滚：移除只读派生 envelope 即恢复现有 workflow GET 行为；不得回退到首步 Result、手填 Artifact 或跨租户读取。

## 最少文件与验收

若实施只允许触及：现有 Workflow GET read-model 组装处、直接 focused test；不改 Workflow、Provider、Model、Gateway、binding、token、cost、数据库 schema、前端或 Memory。若现有接口暂不需 envelope，则只用既有 `final_report` 与 Run response 完成验收，避免新增字段。

Focused 验收：固定 Run HTTP 200；正文长度 6018、SHA 精确匹配；7/7 Step、Result、Execution/Usage reference 完整；tenant/company/project/run/task 链一致；派生 `execution_status=completed`；无明确建议时 `next_step_suggestion=null`；跨租户/错误 Run 404；重复读取幂等；原始存储字节不变；不产生出网、模型调用或写入。

Handoff: sent to 产品规划席；本 Review 不改变安全边界，无需安全席复核，除非后续实现新增跨租户读取或持久化写入。
