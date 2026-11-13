# Workspace R3 真实模型执行 Gate：单路径架构补件

Issue：`issues/20260717_workspace_r3_real_model_execution_gate.md`  
结论：`BLOCKED_L2`  
范围：仅架构契约；未读取密钥值，未修改代码。

## 只允许的一条现有栈路径

复用仓内 `backend/app/model_gateway.py` 的 `ModelGatewayAdapter`，通过 New API 的 OpenAI-compatible `POST /v1/chat/completions`。Workspace 不直连上游 Provider，不新增第二 Provider，不做自动路由或 Fallback。

唯一架构绑定：

- Gateway：`newapi` / `ModelGatewayAdapter`；
- 协议：HTTPS JSON，`POST /v1/chat/completions`；
- 凭据环境变量：`CURIS_MODEL_GATEWAY_API_KEY`；
- 网关地址环境变量：`CURIS_MODEL_GATEWAY_BASE_URL`；
- 模型环境变量：`CURIS_MODEL_GATEWAY_MODEL`；
- 审计网关标识：`CURIS_MODEL_GATEWAY_ID=newapi`。

## 当前不能 PASS 的唯一缺口

仓内现状没有可批准的真实 `CURIS_MODEL_GATEWAY_BASE_URL`、精确生产 Model ID、Provider/模型价格表或负责人批准记录；`newapi-model-a`、`https://newapi.example.com` 仅出现在测试/示例中，不能冒充真实执行配置。因此不能安全地把它们写入生产契约，也不能自行猜测 Provider、域名或模型。

在负责人补充并批准以下三项前，R3 必须保持 `BLOCKED_L2`：

1. 唯一出口域名：`CURIS_MODEL_GATEWAY_BASE_URL` 的真实 HTTPS origin，禁止客户端覆盖；
2. 唯一精确 Model ID：`CURIS_MODEL_GATEWAY_MODEL`，必须属于该 New API 网关的已批准模型；
3. 价格来源：该模型的输入/输出每 1K token 单价及生效日期/来源。

这不是并行方案；其余值均不得自行补齐。

## 绑定与 fail-closed

只允许一个测试 tenant、一个测试 project、一个 `official.workflow.software_rnd_sop` Workflow 和一个已批准 model capability binding。请求必须先通过可信身份、活动 membership、tenant/company scope、project scope、Workflow scope、能力绑定和 `status=active` 校验；任何缺失、不一致、默认租户、跨租户或客户端自选 Provider/Model 均拒绝。执行记录必须带 `tenant_id`、`company_id`、`project_id`、`workflow_id`、`subject_id`、`capability_id`，不得跨租户复用。

## 单次硬上限

在实现 Issue 固化以下不可由请求覆盖的上限：

- 输入：8,192 tokens；
- 输出：2,048 tokens；
- 总计：10,240 tokens；
- 单 Workflow：最多 1 次模型调用；
- 单 R3 E2E：最多 1 次 Workflow；
- 总成本：`USD 0.10` 硬上限；价格缺失或计算结果不可得即拒绝，不写真实 `0`。

超过任一上限先拒绝，不调用网关。

## 超时、重试与错误

- 单次请求超时：60 秒；
- 重试：0 次；
- 429：原样归类为 rate-limited，记录 `429` 并拒绝；不等待重试；
- 5xx、网络错误、解析错误、配置缺失、价格缺失：fail-closed；
- Fallback：禁用；
- 不得把 mock、固定响应或本地手填结果记为真实成功。

## 审计与留存

每次尝试至少记录：`request_id`、`subject_id`（不可逆关联标识）、`tenant_id`、`company_id`、`project_id`、`workflow_id`、`capability_id`、`gateway_id`、精确 `model_id`、`provider_id`、`prompt_tokens`、`completion_tokens`、`total_tokens`、`unit_price_input`、`unit_price_output`、`estimated_cost`、`currency`、`status`、`http_status`、`latency_ms`、`created_at`。价格必须来自经批准的静态配置/价格记录并带版本或生效时间；缺失即失败。

只留脱敏元数据和必要的结果引用；不留 prompt、原始响应、Authorization、API key、cookie 或完整 token。日志只记录错误类别，不记录凭据和秘密。

## 最少实施文件与验证

负责人批准后三个值齐全后，唯一实现 Issue 只允许触及：

- `backend/app/model_gateway.py`：固定出口/模型、上限、无重试、429 与价格缺失拒绝；
- 现有身份/成员、资源 scope、Workflow/Usage 共享入口：接入绑定与审计字段；
- `deploy/curis/workspace.env.example`：只增加变量名和非秘密默认拒绝配置；
- 一个现有 backend 测试文件及现有 `deploy/curis/verify-isolation.sh` 或其最小扩展。

验证命令必须使用仓内既有命令：

```bash
cd backend && ./.venv/bin/python -m unittest tests/test_model_gateway_adapter.py tests/test_d5_newapi_gateway.py
cd backend && ./.venv/bin/python -m pytest -q
```

真实网络验收必须证明：批准配置下 200；缺身份/配置 401；无成员、非批准 tenant/project/workflow/model 403；跨租户资源 404；超过 token/cost 上限在出网前拒绝；429 不重试；日志脱敏。当前因没有真实出口、模型和价格，不能执行或声称通过这些验收。

## 撤销与回滚

撤销任一批准 binding、模型、网关或凭据时立即置 inactive，后续请求拒绝。回滚恢复上一版本 Adapter/配置快照，但必须继续满足租户绑定、上限、无 Fallback 和 fail-closed；不得回退到 mock、默认模型、默认租户或旧的无约束调用路径。任何配置不完整、价格不可得、出口不可达或审计字段缺失均保持 R3 阻塞。

## Handoff

`BLOCKED_L2`：现有栈只有 New API Adapter 路径，但缺负责人批准的真实出口域名、精确 Model ID 和价格来源，架构席不能代填。已交安全边界席复核，并回传产品规划席；Parent R3 保持 `BLOCKED_L2`。
