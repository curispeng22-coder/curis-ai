# R3 Workflow 前序结果上下文预算 Architecture Review

Issue：`issues/20260717_workspace_r3_workflow_context_budget_l2_gate.md`  
结论：`PASS`（仅确定性上下文契约；不实施、不出网）。

## 唯一算法

只改变发送给下一步 Adapter 的 prompt，不改变任何 `step_results.result`、`workflow_steps.output`、`executions.output`、UsageEvent 或历史审计。对每个成功前序结果先生成 canonical text，再计算完整内容的 SHA-256；原始结果仅保留在既有存储中，下一步只携带受控摘要。

Adapter 当前 R3 上限是 8,192；上下文构造器固定把 prompt 上限收紧为 7,168 UTF-8 bytes，预留 1,024 bytes 给固定字段、编码差异和最终边界检查。构造完成后在 Adapter 前再次断言 `len(prompt.encode('utf-8')) <= 7,168`，并保留 Adapter 现有 8,192 fail-closed 检查；不提高任何模型上限。

固定布局及预算：

1. 当前目标/CEO requirement：最多 1,536 bytes；超长按 UTF-8 边界截断并标记 `[TRUNCATED:current_requirement]`。
2. 当前 Step instruction、step name、employee role：最多 512 bytes；固定字段超长即拒绝，不静默丢失 Step 语义。
3. 所有前序成功 Step 的 metadata：最多 2,048 bytes，按 step_order 升序，至少包含 `step_result_id`、step_order、step_type、status、完整结果 hash、原始位置 reference 和 truncation 状态。
4. 最近两个成功 Step 的正文：优先级最高，按时间/step_order 从新到旧，总预算 3,072 bytes，平均 1,536 bytes；先新后旧，逐条受剩余预算限制。
5. 更早成功 Step 的正文：次优先级，按 step_order 从早到晚使用剩余预算，最多 2,048 bytes；不足时保留 metadata/reference/hash，不复制全文。

预算采用固定顺序和固定切片函数，不依赖模型 tokenizer 或网络响应；同一 Run、同一 Step、同一存储内容必须生成相同 prompt。若固定段、metadata 或 delimiter 已使预算不足，直接 fail-closed，不调用 Adapter。

## 内容与边界规则

- 文本按 UTF-8 bytes 截断，不能切断多字节字符；空结果用 `[EMPTY_RESULT]`，非文本结果先以稳定排序的 canonical JSON 序列化，无法序列化则拒绝。
- 每个正文截断处附 `[TRUNCATED:step_result:<id>]`；完整 hash 和 reference 始终保留，便于人工回查，不把 hash 当作正文替代品。
- Step 1→N 的原始结果、Execution、Result 不删除、不压缩、不覆写；缩减只存在于下一步请求内存字符串。
- 不拼接重复结果；按唯一 `step_result_id` 去重，重复 ID 或同一步多个 succeeded Result 视为数据冲突并拒绝。
- 当前任务和 Step 指令优先于前序正文；最近两个结果优先于更早结果；早期结果即使正文被截断也必须保留 metadata/reference/hash。
- prompt、完整 subject、token、Authorization、Cookie、API key 和模型原文不得写入普通日志；R3 模型输入继续使用现有 `[REDACTED:R3_MODEL_INPUT]` 留存标记。

## 失败与重复执行

缺少 task、当前 Step、结果 ID、结果状态、hash/reference、UTF-8 可编码内容，或发生预算溢出、重复结果、非 succeeded 前序状态混入时，在 Adapter 前返回明确 context/limit/audit 错误，`outbound_attempted=0`，不重试、不 Fallback。重复调用同一 pending Step 必须按同一数据库快照生成同一 prompt；不得因重复执行追加副本或改变原始结果。

## 最少文件与回滚

后续实现只需：

- `backend/app/workflow_runtime.py`：替换 `_build_step_input()` 的全量拼接为上述固定预算构造器；
- `backend/app/model_gateway.py`：复用现有边界，并保留/补充 Adapter 前 7,168 bytes 断言；
- 一个直接相关 focused test 文件；不改数据库 schema、Workflow 定义、Provider/Model/Gateway、成本/binding/Run 状态语义。

回滚恢复旧构造器只允许在本地非出网回滚验证中使用；生产/真实 R3 回滚不得恢复无界全量拼接。若新构造器配置或断言缺失，保持 fail-closed 而非放宽到 8,192 以上。

## Focused 验收

不出网测试必须覆盖：Step 6 类输入不超过 7,168 bytes；前序 5 个结果保留 metadata/hash/reference；最新两个正文优先；早期正文按预算截断；空值、非文本、多字节、超长、重复 ID、缺字段和预算不足均确定性拒绝；原始 Result/Execution 字节内容不变；重复构造输出一致；Adapter 未被调用且 outbound=0；日志无凭据和模型原文；最终实际 prompt 永不超过 8,192 bytes。

Handoff: sent to 安全边界席复核，并回传产品规划席；不涉及新增安全边界，但需安全席确认脱敏与 fail-closed。
