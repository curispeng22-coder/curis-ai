# Workspace R3 Workflow 上下文预算 L2 Gate

- 日期：2026-07-17
- 状态：CLOSED — PASS
- Parent：`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`
- Owner：产品规划席
- Next Seat：架构边界席 → 安全边界席 → 总负责人
- 类型：模型输入预算与结果可追溯

## 先说结论

真实七步执行已证明 Step 2→5 可成功，但 Step 6 在出网前因输入超过批准的 8,192 token 上限而失败。根因是运行器把全部前序 Step 输出持续拼入后续 prompt，没有确定性上下文预算。

本 Gate 只定义一条不新增模型调用的确定性上下文预算方案：原始 StepResult/Execution 完整保留，通过受控摘要字段、截断和引用把下一步输入限制在 8,192 内。当前失败 Run 永久保留，不重置、不重试。

## 固定事实

- 失败 Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`，终态 failed。
- Step 1→5 succeeded；Step 6 HTTP 422、outbound=0；Step 7 未调用。
- 成功 outbound=5，累计 7,758 tokens，成本 `USD 0.01516350`。
- Token、模型、价格、可信 CEO、六角色 binding 和 scope 审计均成立。
- 环境已停止；失败 Run 与所有历史记录不得删除、重置或改写。

## 架构边界席唯一任务

1. 只读核对 `WorkflowRuntime` 如何构造下一步输入、前序 StepResult 的结构、现有 Token 估算/上限检查和 Result 引用能力。
2. 给出唯一确定性预算算法，不调用模型、不新增依赖：必须保留当前目标/Step 指令、必要结构字段、每个前序 Step 的 ID/类型/状态/哈希或位置，并对正文使用明确优先级和硬预算。
3. 原始 StepResult/Execution 必须完整保留；上下文缩减只能作用于下一步请求，不能覆盖历史结果或把截断文本写成原始成果。
4. 明确预算单位与保守边界：在 Adapter 前证明最终 input ≤ 8,192 tokens，并为系统提示、固定字段和编码误差保留余量；超预算仍 fail-closed，不提高上限。
5. 明确最新一步与早期步骤如何分配预算、截断标记、hash/reference 可追溯、空/非文本/超长/多字节输入、重复执行与日志脱敏行为。
6. 给出最少文件、回滚与无出网 focused 验收；不得改模型、Token 上限、成本、binding、Provider/Gateway、Workflow Step 定义。

## 禁止范围

- 不修改代码、数据、配置或部署，不启动、不注入 Key、不出网、不创建 Run。
- 不用第二次模型调用做摘要，不增加 summarizer Provider，不用 mock/stub 或手填最终结果。
- 不提高 8,192 输入上限，不降低审计、scope、失败停机、0 重试或无 Fallback。
- 不重置/恢复当前 failed Run，不删除、覆盖或压缩已持久化的原始输出。
- 不在本 Gate 实现 Artifact、项目状态、前端或 R4 Memory。

## Gate 输出

- Architecture Review：唯一预算算法、精确输入结构、预算/余量、引用与截断规则、最少文件、回滚、focused tests，结论 PASS 或唯一 BLOCKED_L2。
- 安全边界席复核：prompt/output 不泄露、历史不可变、客户端不可覆盖预算、超限 fail-closed。
- 安全 PASS 与总负责人批准后，系统交付席才可最小实现并做无出网 focused 验证；通过后再申请新 Run 与七次调用授权。

## 架构与安全复核

- Architecture Review：`reviews/20260717_workspace_r3_workflow_context_budget_architecture_review.md`，结论 `PASS`（仅确定性上下文契约）。
- 唯一算法：下一步 prompt 限制为 7,168 UTF-8 bytes，预留 1,024 余量；固定保留当前目标/Step 指令、全部前序 metadata + hash/reference，最新两步正文优先、早期正文次级预算，UTF-8 安全截断并标记。
- 原始 Result/Execution 完整不变；Adapter 前再次断言输入 ≤ 8,192，缺失/重复/非文本/预算不足 fail-closed，outbound=0。
- Security Review：`PASS`（仅确定性上下文契约，不授权实施或出网）；预算、优先级、历史不可变、日志脱敏符合 R3 安全边界。
- 未改代码、数据、配置；未启动、未注入 Key、未出网。等待总负责人批准。

## 总负责人批准

- 决策：`APPROVED`，仅批准确定性上下文预算最小实现。
- 严格 7,168 UTF-8 bytes 正文预算 + 1,024 预留，Adapter 总 input ≤ 8,192。
- 必须保留完整历史 ID/type/status/hash/reference、UTF-8 安全截断与 `TRUNCATED` 标记，原始结果不可变；全项 fail-closed/outbound=0。
- 不提高 Token/成本，不新增模型/Provider/依赖，不改 binding/Gateway/Workflow，不重置失败 Run。
- 先无出网 focused 验证；之后另行申请新 Run。

## 首轮质量复核

- 实现修订：`e906e86d`；7,168B、UTF-8 安全截断、`TRUNCATED`、hash/reference、原始结果不变均通过。
- 质量独立聚焦：`26 passed / 6 deselected`。
- 唯一阻塞：批准契约要求非文本 fail-closed，但当前 dict/list 会被 canonical JSON 化后继续；最小复现 dict 生成 460B prompt，未拒绝。
- 只允许在上下文构造入口拒绝非字符串正文并补 focused 断言，确保 Recorder/outbound=0；不得修改预算、序列化其他字段、模型边界或历史 Run。

## 最终质量收口

- 最终修订：`b0f791f7`；非文本修复仅 2 个文件。
- dict/list/number/bool/null/bytes 均在上下文构造阶段拒绝，Recorder=0。
- 正常字符串、多字节、7,168B 截断、hash/reference、原始结果不变继续通过。
- 质量独立合计：`34 passed / 6 deselected`；端口全关闭，失败 Run 未改。
- Review：`reviews/20260717_workspace_r3_workflow_context_budget_l2_gate_review.md`，结论 `PASS`。
- 产品验收：本 Gate 关闭；只能另行申请全新 Run，旧 failed Run 不得重试或重置。
