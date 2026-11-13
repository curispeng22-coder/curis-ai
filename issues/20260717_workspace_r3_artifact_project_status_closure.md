# Workspace R3 Artifact 与项目状态收口

- 日期：2026-07-17
- 状态：PASS — ARTIFACT_PROJECT_STATUS_CLOSED
- Parent：`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`
- Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
- Owner：产品规划席
- Next Seat：产品规划席（收口 parent issue）

## 先说结论

七步真实 Workflow 已成功，且 parent R3 的成果与项目状态要求已完成独立复核并闭环。现在已形成可打开、内容非空、可追溯到 Task/StepResult 的成果与项目状态结果。

本 Issue 只复用已落库的 `final_report`、StepResult、Execution 和 UsageEvent 形成最小文档 Artifact 与项目状态投影；不再调用模型，不修改历史结果，不开发前端。

## 当前状态（2026-07-18）

- 系统交付席已完成静态校验与无出网 focused 实施，固定为 `2da0367b`，未扩张范围。
- 质量运行席已补齐对应复核并形成 `reviews/20260717_workspace_r3_artifact_project_status_closure_review.md`，结论 `PASS`。
- 本 Issue 已闭环收口，父 Issue 可进入 final closeout。

## 固定事实源

- Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`，状态 succeeded。
- Step 1→7 全 succeeded；7 个 StepResult/Execution/UsageEvent 唯一对应。
- `final_report`：6,018B，SHA-256=`2d14cf90ca1fa850f7e8425763b922cda4c6c9c2132a2f55eac07791a07ba96c`。
- Token：9,622；成本 `USD 0.01326900`；模型、价格、可信 CEO 与 binding 审计完整。
- 环境已停止；不需要也不允许再次注入 Key 或调用模型。

## 架构结论（PASS）

- Review：`reviews/20260717_workspace_r3_artifact_project_status_architecture_review.md`。
- Artifact 只读复用 `workflow_runs.final_report`，不新增成果表、文件系统或对象存储，不重新生成正文。
- 优先复用现有 `GET /api/workspace/workflows/{run_id}`；仅在现有返回不能满足验收时，补最小只读派生字段。
- Artifact 身份固定为 `(tenant_id, workflow_run_id, content_sha256)`，返回 tenant/company/project/run/task、7 步与 StepResult 引用、内容 SHA/长度、模型与 Usage 汇总。
- 项目执行状态只由 Run succeeded、7/7 Step succeeded、7/7 Result 存在及报告 SHA/长度一致确定性派生；不写 `projects.status`。
- `next_step_suggestion` 仅允许读取报告中的明确字段；当前报告若无明确字段，必须返回 `null`，不得推测或补静态建议。
- 跨租户、错误 Run 返回 404；原 Run、Result、Execution、UsageEvent 与 `final_report` 保持不可变。
- 本方案未新增安全边界，无需重复安全复核；如实施引入持久化、写操作或新的跨租户行为，立即停止并退回安全边界席。

## 架构边界席唯一任务

1. 只读核对现有 ResultStore、code_artifacts/成果接口、Task/StepResult 关联、Project 状态与下一步建议接口；优先复用现有表和 API，不新建通用成果平台。
2. 给出唯一最小 Artifact 落点：类型为 document/report，正文只能来自当前 Run final_report，不重新生成；必须保存或返回 run/step/task/project/company/tenant、SHA-256、内容长度、模型与 UsageEvent 引用。
3. 明确“可打开”的真实方式：现有 API 路由或受控文件位置；不得只给数据库 ID，也不得暴露原始 prompt、密钥或完整 subject。
4. 给出项目状态投影：状态必须由 Run/Step 终态计算；下一步建议必须引用 final_report 中明确字段或现有结构化结果，不能写静态文案或再调用模型。
5. 明确幂等键、重复调用、冲突停止、跨租户/跨项目 fail-closed、撤销/回滚和历史不可变。
6. 给出最少文件、focused 无出网测试与真实 HTTP 验收；不改 Workflow、模型、binding、Token/成本或前端。

## 禁止范围

- 不启动真实模型环境、不注入/读取 Key、不调用模型、不创建 Run。
- 不修改或覆盖 final_report、StepResult、Execution、UsageEvent，不伪造 Artifact 内容、Token、成本或下一步建议。
- 不新建成果中心前端、对象存储、通用版本系统、Marketplace 或 R4 Memory。
- 不把 mock、空文件、数据库 ID 或静态模板文案算作成果。

## 验收

- 一个 document/report Artifact 可通过真实 HTTP 或受控文件路径打开，内容非空且 SHA/长度与 final_report 一致。
- Artifact 可追溯到 tenant/company/project/Run/StepResult/Task，跨租户不可见。
- 项目状态由当前 Run 七步 succeeded 推导；下一步建议只有在 final_report 存在明确字段时才返回并带来源引用，否则为 `null`。
- 重复执行幂等，不产生第二份冲突成果；历史 failed Run 不变。
- 不产生新的 model_call、Token 或成本；日志脱敏。
- 最终由质量运行席执行真实 HTTP E2E、一次全量回归和边界复核，只有 PASS 才能关闭 Parent R3。
