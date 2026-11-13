# Workspace R3 剩余 Workflow 完成契约 Gate

- 日期：2026-07-17
- 状态：CLOSED — PRODUCT_DECISION_RECORDED
- Parent：`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`
- Owner：产品规划席
- Next Seat：产品规划席（转剩余六次调用 L2 Gate）
- 类型：运行时完成路径与外部调用边界

## 先说结论

R3 真实模型执行 Gate 已 PASS：当前 Run 的首 Step 真实模型成功，Token、成本、可信 CEO 审计和 Result 已完整落库。但 Run 仍为 `running`，其余 6 Step pending；现有批准契约又限制同一 Workflow 只允许一次模型出网，不能直接继续调用。

本 Issue 只确定当前 Run 完成剩余 6 Step、产出最终 Artifact/项目状态的唯一最小路径，不实施、不启动、不注入 Key、不调用接口。

## 固定事实

- Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`。
- 首 Step / StepResult：succeeded；其余 6 Step pending；Run=running。
- 已消费唯一真实调用：`model_call=1`、`outbound_attempted=true`。
- 真实模型：`gpt-5.4-mini-2026-03-17`；Token 416；成本 `USD 0.001707`。
- Result 位于 `step_results.result` 与 `executions.output`，内容一致、非空。
- 环境已停止；历史失败 Run 保留。
- Parent R3 要求七步状态、可追溯成果、项目状态和下一步建议，不能只用首 Step PASS 代替完整闭环。

## 架构边界席唯一任务

1. 只读核对该 structured Workflow 的 7 Step 定义、当前运行器推进规则、每个剩余 Step 的执行器与是否必然触发模型出网。
2. 核对现有代码是否已有合法能力，可复用首步真实 Result 在不新增模型调用的前提下完成后续本地转换、校验、成果归档和项目状态更新。
3. 若已有无出网完成路径，给出唯一顺序、每步预期状态、失败/人工接管行为、Artifact/项目状态落点及最小验证方式。
4. 若没有无出网路径，只给一个最小不可避免的缺口和精确额外调用数量/成本上界；不得默认扩大为无限自动推进、重试或 Fallback。
5. 不得把直接改库、手填 StepResult、复制历史输出、mock/stub 或跳过 Step 写成真实完成。

## 允许范围

- 只读查看当前 Workflow 定义、运行器、Tool/Step 执行映射、Result/Artifact 与项目状态接口及直接测试。
- 落盘 Architecture Review；结论只能是 `PASS` 或 `BLOCKED_L2`。
- 如涉及新增外部调用或安全范围，交安全边界席复核后再提交总负责人。

## 禁止范围

- 不修改代码、数据库、配置、Issue 外实现或前端。
- 不启动服务、不注入或读取 Key、不调用 `run-next-step`、不创建新 Run。
- 不改变 Provider、Model、Gateway、受控出口、Token/成本、0 重试和无 Fallback 契约。
- 不删除、重置或改写当前 Run、历史失败 Run、StepResult、Execution 或 UsageEvent。

## Gate 输出

- `PASS`：证明存在现有、无额外出网、非 mock 的确定性完成路径，给出唯一执行与验收清单。
- `BLOCKED_L2`：证明剩余 Step 需要额外模型调用或缺少合法执行器，并给出唯一最小授权申请，不实施。

完成后直接交安全边界席（仅当边界变化）或回产品规划席；产品席据 Review 决定下一轮，不得自行继续当前 Run。

## 产品取舍

- Architecture Review：`reviews/20260717_workspace_r3_remaining_workflow_completion_architecture_review.md`，结论 `BLOCKED_L2`。
- 事实：Step 2→7 全部要求 model，现有运行器没有合法无出网执行器；首步 Result 不能代替剩余 Step。
- 产品决定：不为 R3 临时新增六步本地执行器，避免把 R4 的运行时建设提前塞入当前 Gate。
- 唯一后续路径：`issues/20260717_workspace_r3_remaining_six_model_calls_l2_gate.md`，申请同一 Run 严格顺序的额外 6 次模型调用；失败即停、每 Step 最多一次、0 重试、无 Fallback。
- Artifact 与项目状态落点不在该调用授权中伪造；七步成功后另按 Parent R3 的最小独立落点 Issue 收口。
