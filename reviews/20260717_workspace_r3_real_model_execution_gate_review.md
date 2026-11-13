# Workspace R3 真实模型执行 Gate 质量 Review

- 日期：2026-07-17
- Issue：`issues/20260717_workspace_r3_real_model_execution_gate.md`
- 分支：`feat/roadmap-r1r2`
- 模型 Gate 修订：`8f426be98503a13455a6e0a5f3392cee92582246`
- 出口修订：`72186d5843106554c759f647b7998f1adf31406a`
- 可信 CEO 修订：`718af2c463e39820ac6928681b16818a9fbccc25`
- 安全依据：`reviews/20260717_workspace_r3_real_model_execution_security_review.md`
- 验证席：质量运行席

## 结论

**PASS（唯一授权 Run 的单次真实模型 Gate 验收通过）。**

总负责人唯一授权 Run `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc` 在调用前为 pending、7 Step 全 pending、`outbound_attempted=0`。质量席使用现有 JWKS 私钥在内存签发同主体短期 Token，仅经 Gateway 调用一次：HTTP 200，Run=`running`，首 Step 与 StepResult succeeded；真实 Provider、模型、Token、价格、成本、单次出网与可信 CEO 审计完整落库。未重试、未走 Fallback、未使用 mock、未改写历史记录。

本 Review 只判定真实模型执行 Gate PASS；Parent R3 后续 6 Step 与完整纵向链不在本次单调用授权内。

## 独立证据

### 1. 修订与工作区

- 最终 `git rev-parse HEAD`：`718af2c463e39820ac6928681b16818a9fbccc25`。
- 当前分支：`feat/roadmap-r1r2`。
- `backend/` 与 `deploy/curis/` 相对固定修订无本地差异；现有其他未提交文件未参与本次验证。

### 2. 聚焦测试

命令：

```text
cd backend
./.venv/bin/python -m pytest -q \
  tests/test_model_gateway_adapter.py \
  tests/test_d5_newapi_gateway.py \
  tests/test_phase6_workflow_mvp.py \
  tests/test_workspace_identity_membership.py \
  tests/test_tenant_model_preference.py \
  tests/test_phase8_workspace_billing_support.py
```

结果：**43 passed / 0 failed**，耗时 3.90s。

R3 新增的 6 项用例全部通过，覆盖：固定出口、固定模型、60s、Token 上限、批准价格、凭据缺失 401、越界输入出网前 422、429 单次且不泄密、批准模型目录、作用域审计、项目越界出网前 403。

### 3. 一次全量回归

命令：`cd backend && ./.venv/bin/python -m pytest -q`

结果：**609 passed / 19 failed / 0 skipped**，耗时 51.10s。

前置 R2 固定基线为 **603 passed / 19 failed / 0 skipped**。本修订正好新增 6 项 R3 测试且全部通过；失败集合仍为既有 19 项（Admin token 旧配置、`default/selfuse` 旧断言与校验脚本、Department/Platform 跨连接旧断言、vector 范围检查、禁改前端标签、Docker Compose 插件缺失），**R3 未新增全量失败**。

### 4. 单一路径与不可覆盖

静态复核 `backend/app/model_gateway.py`、`backend/app/main.py`：

- 唯一 Provider：`openai`；唯一 Gateway：`newapi`。
- 唯一出口：`https://api.openai.com:443/v1/chat/completions`；请求方法为 POST。
- 唯一模型：`gpt-5.4-mini-2026-03-17`。
- R3 profile 对 base URL、gateway、model、timeout 做精确相等校验；客户端请求体没有 Provider、Gateway、Model、出口或凭据覆盖入口。
- R3 工作流统一路由到 `model_gateway_tool`，其 fallback chain 只有自身；适配器只有一次 `urlopen`，无重试循环。429 被标记为 `rate_limited` 并立即返回，聚焦用例断言调用次数为 1。

### 5. fail-closed、限额与审计

- 调用前要求可信 subject、request id、批准 tenant/project/workflow run/capability binding 与审计 key；Company 必须匹配 membership。
- 数据库再次核对 active binding、Company 下 Project、同 Project/Company 的 Workflow、active official model 与 Gateway；任一缺失即拒绝。
- 同一批准 Workflow 已有一次 `outbound_attempted=1` 记录时，以 422 拒绝后续调用。
- 输入 8,192、输出 2,048、总量 10,240；超限拒绝。成本按固定版本 `2026-07-17` 的输入 `0.75/1M`、输出 `4.50/1M` 计算，非正成本或超过 USD 0.10 拒绝。R3 不接受客户端价格输入；凭据缺失返回 401。
- 成功/失败审计保留 request、subject 摘要、tenant、company、project、workflow、binding、精确 model、Token、价格版本、成本、HTTP 状态、延迟与出网标志。
- prompt 与工作流持久化输入写为 `[REDACTED:R3_MODEL_INPUT]`；异常对 API key、Authorization、prompt 和原始响应脱敏。聚焦用例已核对审计字段及脱敏结果。

### 6. 过期 Token 预检（2026-07-17 13:48 CST）

- 容器注入状态：`CURIS_MODEL_GATEWAY_PROFILE`、`BASE_URL`、`MODEL`、`API_KEY`、4 个批准 scope、`CURIS_IDENTITY_AUDIT_KEY` 均为 `SET`；只核对是否存在，未输出值。
- Gateway health：HTTP 200。
- 补跑路径：`POST /api/workspace/workflows/wfr-69926fdb-21a2-4166-b6c6-37059309d7ff/run-next-step`，tenant=`tenant-a`。
- 实际 HTTP：**401**，Envoy 在身份验证阶段拒绝已过期成员 Token；该身份阻塞随后已用同 JWKS 私钥内存签发的短期 Token 解除。
- Step 结果：Workflow=`pending`，7 个 Step 均为 `pending`。
- 单次调用：模型出网次数 **0**；该 Workflow 的 `usage.model_call` 审计记录数 **0**。
- 模型、input/output/total tokens、`estimated_cost`、`price_version`：未生成，因为预检请求未到 Workspace。
- 脱敏：命令输出、Review 与消息均未包含 Authorization、Token、API key 或 scope 注入值。

### 7. 短期 Token 原地真实补跑（2026-07-17 13:53 CST）

- Token：复用当前 `curis-quality-jwks` 与 `.generated/jwks/private.pem`，保留原批准主体/tenant/company claims，仅在内存刷新时效并签名；Token 未输出、未落盘、未写日志或 Review。
- 唯一路径：`POST /api/workspace/workflows/wfr-69926fdb-21a2-4166-b6c6-37059309d7ff/run-next-step`，只调用一次。
- Gateway HTTP：**200**；Workflow：`failed`；首 Step `wfs-77590301-8ee3-4636-ace6-f3ef5e3e79ac`：`failed`；StepResult：0。
- 唯一失败原因：`<urlopen error [Errno -3] Temporary failure in name resolution>`；容器无法解析唯一批准域名 `api.openai.com`。
- 单次调用审计：`usage.model_call=1`，`outbound_attempted=true`，`status=network_error`，无重试、无 Fallback。
- 固定模型与价格审计：model=`gpt-5.4-mini-2026-03-17`，`price_version=2026-07-17`，`cost_source=openai_gpt_5_4_mini_2026_07_17`。
- 因未取得 OpenAI 响应：input/output/total tokens 均为 0，`estimated_cost=0`，OpenAI HTTP status=0；不得把这些写成真实模型成功数据。
- 脱敏核验：持久化 Step input 为 `[REDACTED:R3_MODEL_INPUT]`；失败信息与审计 JSON 均不含 Authorization、Bearer、API key、Cookie 或模型凭据变量名。

### 8. 出口修复后的调用资格复核

- 当前仓库：`feat/roadmap-r1r2@72186d5843106554c759f647b7998f1adf31406a`；`deploy/curis/gateway` 相对该修订无差异。
- `gateway-egress-1`：healthy；Workspace 未重建或重启，符合交付约束。
- 容器批准 run scope：与原 Run 相同，未切换到新 Run。
- 数据状态：Workflow=`failed`；Step 状态为 `failed + 6 pending`；既有 `outbound_attempted=true` 记录数为 1。
- 结论：当前 scope 不具备再次模型调用资格；未发起第二次 `run-next-step`，避免把终态短路返回误报为真实执行。

### 9. 总负责人批准的新 Run 单次验收

- Authorization：`APPROVE_UNFREEZE_R3_SINGLE_RUN`；唯一 Run：`wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`。
- 调用前：Run=`pending`，7 Step 全 `pending`，`outbound_attempted=0`，容器 scope 与 Run 匹配。
- Token：使用现有 JWKS 私钥在内存签发；Token/私钥未输出、未落盘、未写日志或 Review。
- 唯一 HTTP 调用：Gateway `POST .../run-next-step` 返回 **200**；没有第二次调用。
- 终态：Run=`failed`；首 Step `wfs-738b3e06-5e74-4dd2-b846-0d3d4f0e53ce`=`failed`；其余 6 Step=`pending`。
- 精确失败：`X-Ceo-Id is required to write UsageEvent`。当前 Gateway 配置没有可信 `X-Ceo-Id` 映射。
- Provider 成功证据：StepResult `wfrs-f54a67e0-58ec-463e-9e80-0d546c9793af`=`succeeded`；Execution `1`，tool/model=`official.openai.gpt-5.4-mini-2026-03-17`，`estimated_cost=0.001302`。
- Artifact：没有独立 Artifact 表或 Artifact 记录；模型结果仅位于 `step_results.result` 与 `executions.output`，本 Review 不回传内容。
- 审计失败：`usage.model_call=0`；Provider HTTP status、input/output/total tokens、`price_version`、`outbound_attempted` 未持久化，不能从成本反推或伪造。
- 状态一致性：StepResult 已 succeeded，但 Workflow Step/Run 因后续审计异常 failed，属于真实结果已写入、审计未闭合的部分成功状态。
- 脱敏：首 Step input=`[REDACTED:R3_MODEL_INPUT]`；错误与现存日志未发现 Authorization、Bearer 或 API key；Token 和私钥未输出。

### 10. 最终唯一 Run 真实模型验收（2026-07-17 16:47 CST）

- 唯一 Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`；固定 scope 与 `tenant-a`、批准 Project、binding、SHA `718af2c4` 全部匹配。
- 调用前：Run=`pending`，7 Step 全 `pending`，`outbound_attempted=0`。
- Token：复用现有 JWKS 私钥，仅在内存签发同主体短期 Token；Token/私钥未输出、未落盘、未写日志或 Review。
- 唯一 HTTP 调用：Gateway `POST .../run-next-step` 返回 **200**；未发起第二次调用。
- 调用后：Run=`running`；首 Step `wfs-ed48590e-040c-4a86-823f-fa06dd096dde`=`succeeded`；其余 6 Step=`pending`。
- StepResult：`wfrs-9169b874-72f3-45ce-8ebe-d99162bb166b`=`succeeded`。
- Provider / Gateway / Model：`openai` / `newapi` / `gpt-5.4-mini-2026-03-17`；Provider HTTP=200。
- Token：input=44、output=372、total=416。
- 成本：`estimated_cost=0.001707 USD`；`price_version=2026-07-17`；input 单价 `0.75/1M`、output 单价 `4.50/1M`；`cost_source=openai_gpt_5_4_mini_2026_07_17`。
- 单次审计：`usage.model_call=1`、`status=success`、`outbound_attempted=true`、latency=4958ms。
- 可信身份：`ceo_id=ceo-f9d4d433-18af-45c9-8c16-f5ea31ecf5ae`；审计 `subject_id` 为 64 位不可逆摘要，未保存完整 subject。
- Result/成果位置：`step_results.result`（上述 StepResult）与 `executions.output`（Execution `2`）；两处内容一致、非空、1353 bytes，SHA-256=`ba44bc0b43e2b243425e44ffa1ac8305b96a4f879fafb92249c5f677a7ed47af`。运行库无独立 Artifact 表，本 Review 不输出模型原文。
- 脱敏：首 Step input=`[REDACTED:R3_MODEL_INPUT]`；UsageEvent 无 Authorization/API key/Cookie/prompt/output/raw response 字段，无 Bearer、完整 subject；Workspace 日志未发现上述秘密。
- 历史保持：`wfr-69926fdb-21a2-4166-b6c6-37059309d7ff` 与 `wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6` 仍为 failed，未重试、删除或改写。
- 环境停止：系统交付席已执行 `deploy/curis/stop-local.sh`；质量席复核 `3000/3100/8001/8002/8080` 全部 CLOSED，Gateway/Workspace/egress/JWKS 相关容器=NONE，Admin/前端相关后台进程=NONE。停止过程未读取或输出 Key，未再次调用 Run。

## Gate 验收结论

以下证据均已形成：

- Provider HTTP 200 与精确模型；
- 真实 input/output/total tokens；
- 价格版本、成本与单次出网审计；
- 可信 CEO、Result/成果位置与日志脱敏。

真实模型执行 Gate 无剩余质量阻塞，结论为 **PASS**。Run 保持 `running` 是单次 `run-next-step` 成功后的预期状态；后续 6 Step 不在本次授权范围内。

## 唯一下一步

产品规划席读取本 Review 收口 Gate。任何后续 Workflow Step 必须另行授权，不得把本次单调用授权扩展为继续执行。

Next Seat：产品规划席  
Handoff: sent to 产品规划席
