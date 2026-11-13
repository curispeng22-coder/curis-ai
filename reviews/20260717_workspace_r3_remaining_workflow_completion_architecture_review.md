# R3 剩余 Workflow 完成路径 Architecture Review

Issue：issues/20260717_workspace_r3_remaining_workflow_completion_gate.md  
Run：wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc  
结论：BLOCKED_L2。

## 核对结论

该官方 structured_executable Workflow 固定 7 步，顺序为：

1. Tech Lead 接收并拆解（tech_lead_breakdown）
2. Product Manager 补充需求（requirement_clarification）
3. Architect 输出技术方案（architecture_design）
4. Frontend Engineer 执行前端任务（frontend_execution）
5. Backend Engineer 执行后端任务（backend_execution）
6. QA Engineer 验收（qa_verification）
7. Tech Lead 汇总结果（final_report）

WorkflowRuntime.run_next_step() 每次只取最小 pending step，查找对应 enabled Employee 与 capability binding，构造包含前序结果的输入，然后进入 employee.execute_step()。当前 6 个剩余 step 都声明 required_capability_types=[model]；现有执行映射没有本地转换、校验、归档或人工完成分支，均会继续走 model binding 和 ModelGatewayAdapter。首步结果只能作为下一步 prompt 上下文，不能伪造其余 StepResult，也不能让一个 Result 代表七步完成。

## 出网与唯一执行顺序

剩余 Step 2→7 的唯一现有执行顺序是逐步调用：

requirement_clarification → architecture_design → frontend_execution → backend_execution → qa_verification → final_report

每一步都需要一次新的模型调用；当前 Run 已消费 model_call=1/outbound_attempted=true，且批准契约禁止同一 Workflow 第二次出网、Fallback 和重试。因此当前 Run 没有合法的无出网完成路径，也不能直接 run-next-step。

若总负责人另行批准扩大调用额度，精确额外数量为 6 次；每次仍受输入 8,192、输出 2,048、总 Token 10,240 和单次成本上限 USD 0.10 约束，额外成本上界为 USD 0.60。该扩大不属于本 Gate，不能默认批准；在当前单 Workflow 一次调用契约下应保持阻塞。

## Result、Artifact 与项目状态落点

现有运行器在每一步成功时写入：

- workflow_steps.status/output；
- step_results 一条对应结果；
- executions.output/UsageEvent（模型执行路径）；
- 全部步骤 succeeded 后才在 workflow_runs.final_report 写最终报告并将 Run 置 succeeded。

现有 _complete_run() 只生成 final_report，没有把首步 Result 转换为代码/文档/Demo Artifact，也没有更新 projects.status 或项目成果索引。当前 Run 的 Result 非空只能证明首步成功，不能证明 Artifact、项目状态或七步闭环完成。

## 失败与人工接管

当前合法行为是保持 Run running、剩余步骤 pending，不调用模型、不改写历史 StepResult/Execution/UsageEvent。任一继续执行失败会由现有运行器将对应 Step 和 Run 标记 failed；这不能作为当前 Run 的完成路径。人工接管只能是产品/总负责人明确批准后建立新的实现/执行 Issue，不能手填结果、复制历史输出、跳步、mock/stub 或直接改库。

## 唯一最小缺口

缺少“无出网的 6-step 本地转换/校验/Artifact 归档/项目状态更新执行器”，且现有 6 步契约全部要求 model。若产品要求保持当前单次出网限制，必须另立唯一实现 Issue，先定义并安全复核该本地执行器的真实输入、输出和 Artifact/Project 状态落点；本 Review 不授权实现。

若不新增该本地执行器，唯一可行申请是把本 Run 的模型调用上限从 1 增至 7，额外 6 次、成本上界 USD 0.60，并为 Artifact 与项目状态补充独立落点契约；这同样需要新的总负责人批准，不能沿用当前 Run 授权。

## 验收要求

在任何后续实现/授权前，必须不出网证明：Step 1 结果可作为受控输入；Step 2→7 各自生成真实、非复制的 StepResult；顺序与状态可追溯；失败可停在准确 Step；最终报告、Artifact 位置和项目状态均有明确持久化落点；历史失败 Run 不变；无模型调用时不会新增 UsageEvent 或出网记录。只有完成这些后，质量席才可执行真实闭环验收。

Handoff: sent to 产品规划席；若选择新增本地执行器或扩大模型调用，安全边界变化时再交安全边界席复核。当前 R3 保持 BLOCKED_L2。
