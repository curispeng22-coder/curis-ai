# Workspace R3 真实模型执行 Gate

- 日期：2026-07-17
- 状态：CLOSED — PASS
- Parent Issue：`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`
- 固定分支：`feat/roadmap-r1r2`
- 前置提交：`758da525b15adff17c16a063261d8a0d487e7f3e`
- Owner：产品规划席
- Next Seat：产品规划席（Parent R3）

## 已确认事实

- `official.workflow.software_rnd_sop` 已是 `structured_executable`。
- 当前 115 个 Tool 均为 `configured=0`、`executable=0`、`mock_or_stub=1`。
- `official_models=0`、`model_gateways=0`、有效能力绑定为 0。
- 运行环境未提供模型网关必需配置。
- 系统交付席未修改文件、未伪造执行；R3 因此保持 BLOCKED。
- 总负责人已否决不完整申请：不得自行补齐或启用多 Provider / Fallback；须先形成可审定的唯一 Provider、Model、Gateway、出口、凭据注入和 Token / 成本上限契约。

## Gate 目标

在不泄露凭据、不放宽租户隔离、不伪造能力的前提下，确定一条最小、可审计、可撤销的真实模型执行路径，供 R3 单一 E2E 使用。

## 安全边界席必须给出的结果

1. 结论只能是 `PASS` 或 `BLOCKED_L2`。
2. 若 PASS，明确唯一批准的 Provider、Model、Gateway/Adapter、出口域名与调用协议。
3. 明确凭据来源和注入方式：只允许环境变量或现有密钥设施；禁止写入仓库、Issue、Review、日志或消息。
4. 明确租户、成员、项目和能力绑定校验；调用必须 fail-closed，禁止默认租户或跨租户复用执行记录。
5. 明确日志脱敏、请求/响应留存边界、超时、重试、速率限制和最大 Token / 成本上限。
6. 明确 Token、模型和成本审计字段及成本计算来源；缺价格不得写成真实 0 成本。
7. 明确最小部署/运行配置、验证命令、撤销与回滚方式。
8. 若 BLOCKED_L2，只给唯一不可自行解决的缺口，例如缺负责人批准的凭据或出口，不提出多套并行方案。

## PASS 验收

- 不暴露任何密钥值。
- 客户端不能选择未批准 Provider/Model 或绕过 Gateway。
- 仅批准测试租户、测试项目和单一 R3 场景；默认拒绝其他范围。
- 有可验证的 200/401/403/429/上限拒绝与日志脱敏要求。
- 有实际 Token、模型和成本审计要求。
- 安全边界席把 PASS 契约直接交系统交付席，并回传产品规划席。

## 禁止范围

- 不实现模型调用，不读取或粘贴密钥值。
- 不新增第二 Provider、自动路由、Fallback、模型市场、计费系统或前端。
- 不把 Mock、固定响应、本地手填结果标为真实模型执行。

## 交接

安全边界席完成 Gate 后，若 PASS，直接交系统交付席按唯一契约实施并继续 Parent Issue；若 BLOCKED_L2，回产品规划席保持 R3 阻塞。

## 当前补件顺序

1. 架构边界席只读现有模型调用代码、配置和依赖，形成唯一单路径契约，不实施。
2. 安全边界席对该单路径给出 PASS / BLOCKED_L2。
3. 产品规划席把完整契约提交总负责人审批。
4. 只有总负责人批准后，系统交付席才能实施并恢复 Parent R3。

## 产品规划席提交的唯一审批提案

以下值用于补齐架构 Review 中缺失的三项，不代表已获批准：

- Provider：OpenAI API。
- Gateway / Adapter：复用 `backend/app/model_gateway.py` 的 `ModelGatewayAdapter`，`CURIS_MODEL_GATEWAY_ID=newapi`；不增加第二 Adapter。
- 唯一出口：`https://api.openai.com`，只允许 HTTPS 443 和 `POST /v1/chat/completions`，客户端不得覆盖。
- 精确 Model ID：`gpt-5.4-mini-2026-03-17`，禁止 alias 漂移和 Fallback。
- 凭据变量：`CURIS_MODEL_GATEWAY_API_KEY`；只由部署环境的现有密钥注入设施提供，仓库、Issue、Review、日志、消息和数据库均不得保存值；未注入即 fail-closed。
- 地址变量：`CURIS_MODEL_GATEWAY_BASE_URL=https://api.openai.com`。
- 模型变量：`CURIS_MODEL_GATEWAY_MODEL=gpt-5.4-mini-2026-03-17`。
- 价格：标准处理输入 `USD 0.75 / 1M tokens`、输出 `USD 4.50 / 1M tokens`；价格版本日期 `2026-07-17`，来源为 [OpenAI GPT-5.4 mini 官方模型页](https://developers.openai.com/api/docs/models/gpt-5.4-mini)。该页同时确认模型支持 `v1/chat/completions` 及固定 snapshot。
- 单次输入上限 8,192、输出上限 2,048、总 Token 上限 10,240；单 Workflow 和单 R3 E2E 各最多 1 次调用。
- 按上述价格，单次理论最大模型成本为 `USD 0.01536`；R3 总成本硬上限保持 `USD 0.10`，任何价格缺失或计算异常均在出网前拒绝。
- 超时 60 秒、重试 0、429 不重试、无 Fallback；其余绑定、审计、日志脱敏和回滚完全沿用架构 Review。

本提案只批准一个测试 tenant、一个 project、`official.workflow.software_rnd_sop` 和一个 active capability binding。安全边界席 PASS 且总负责人批准前，不得实施或注入凭据。

## 实施收口

- 总负责人 `APPROVED` 与安全边界席 `PASS` 已满足。
- 已固定唯一 Provider / Model / Gateway / 出口，禁止客户端覆盖、Fallback 与重试。
- 已实现租户、项目、Workflow Run、活动能力绑定 fail-closed，调用限制、撤销态检查、脱敏审计及批准价格计算。
- 聚焦测试 `43 passed`；未注入或保存真实凭据，真实网络由质量运行席使用部署密钥独立验证。

## 真实网络补件

- 模型凭据、固定模型配置和四个批准 scope 已安全注入。
- 质量运行席在内存签发同主体短期 member token，只调用一次既定 `run-next-step`：Gateway 返回 200，身份、membership 与 scope 均通过。
- 首个 Workflow Step 因 Workspace 容器无法解析 `api.openai.com` 而失败：`Temporary failure in name resolution`。
- 审计已记录 `model_call=1`、`outbound_attempted=true`、`status=network_error`；无重试、无 Fallback，输入保持脱敏；因为未到 Provider，Token 和成本未生成。
- 唯一下一步：在不开放通用互联网、不改变 Provider/Model/URL 的前提下，补齐仅允许 `api.openai.com:443` 的 DNS/HTTPS 受控出口；经架构与安全 PASS 后实施，再由质量席只补跑真实路径。
- 架构 Review：`reviews/20260717_workspace_r3_real_model_execution_dns_https_egress_review.md`，PASS。
- 安全边界：PASS。已固定精确 DNS/SNI/443 allowlist、deny-by-default、无直连/旁路/备用出口；现已交系统交付席实施。
- 受控出口实现：提交 `72186d5843106554c759f647b7998f1adf31406a` 已运行，egress healthy，批准/拒绝网络聚焦验证通过。
- 原批准 Workflow Run 已有一次 `outbound_attempted=1` 的网络失败记录，按单次调用契约额度已耗尽；质量席正确拒绝伪造第二次重跑。
- 唯一下一步：通过批准 API 创建一个新的同项目 Workflow Run，只更新 `CURIS_R3_APPROVED_WORKFLOW_RUN_ID`，由负责人再次隐藏注入凭据后执行一次真实调用；不得删除旧审计或放宽单次限制。

## 新 Run 真实 Provider 结果与当前唯一阻塞

- 总负责人批准的新 Run：`wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`。
- 调用前状态：Run `pending`、7 Step 全 `pending`、`outbound_attempted=0`。
- 质量运行席只经 Gateway 调用一次，HTTP 200；无重试、无 Fallback、无 mock。
- 真实 Provider 已成功返回：StepResult `wfrs-f54a67e0-58ec-463e-9e80-0d546c9793af` 为 `succeeded`，模型为 `gpt-5.4-mini-2026-03-17`，执行成本 `0.001302`。
- Provider 返回后的 UsageEvent 写入因缺少可信 `X-Ceo-Id` 失败，导致首 Step 与 Run 终态为 `failed`。
- 因审计写入失败，`model_call=0`，真实 input/output/total tokens、`price_version` 与 `outbound_attempted` 未持久化；无独立 Artifact 记录。
- 本次单 Run 授权已消费，不得重跑；现有成功 StepResult、Execution 与失败审计不得删除或改写。
- 唯一下一步：完成 `issues/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate.md` 的安全契约、审批、实施与无出网验证；之后才能申请新的单 Run 授权。

## 可信 CEO UsageContext 已收口

- 子 Issue：`issues/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate.md`，状态 `CLOSED — PASS`。
- 最终修订：`718af2c463e39820ac6928681b16818a9fbccc25`。
- 质量 Review：`reviews/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate_review.md`，固定修订独立无出网聚焦 `14 / 14 passed`。
- 正向 Workflow → UsageEvent 成立；Project / Run 错配、disabled employee、伪造 CEO Header 及缺失/撤销/跨租户条件均在出网前 fail-closed。
- Parent R3 的唯一剩余动作：总负责人批准创建一个全新同 tenant/project/workflow/binding 的 pending Run，并仅允许一次真实调用；旧失败 Run 全部保留且不得重试、删除或改写。

## 新单 Run 执行前数据阻塞

- 总负责人已批准“新建唯一 Run＋一次真实模型调用”，但该授权不包含 CEO 映射迁移。
- 系统交付席执行前核对发现：当前 `quality.sqlite` 尚无 `tenant_memberships.ceo_id` 列，`membership-quality` 与 `company-a` 均无可直接使用的可信非空 `ceo_id`。
- 因不能猜测、填默认值或临时写入，系统交付席已停止；未启动、未建 Run、未注入 Key、未调用模型。
- 唯一下一步：完成 `issues/20260717_workspace_r3_ceo_mapping_migration_input_l2_gate.md`，确定并单独审批 `company-a + membership-quality` 的唯一可信同值 CEO 迁移输入。

## CEO 映射前置已解除

- 子 Issue：`issues/20260717_workspace_r3_ceo_mapping_migration_input_l2_gate.md`，状态 `CLOSED — PASS`。
- 批准值：`ceo-f9d4d433-18af-45c9-8c16-f5ea31ecf5ae`；仅绑定目标 active membership 与 `tenant-a + company-a`。
- 运行库映射、Company 一致性和幂等核对均 PASS；无冲突，未启动、未建 Run、未注入 Key、未调用模型。
- 总负责人已再次确认：下一步仅创建一个全新 Run；确认 pending/outbound=0 后，质量运行席才可执行唯一一次真实调用。

## 最终唯一 Run 已创建

- Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`。
- 创建路径：批准 Gateway API，HTTP 201，仅创建一次。
- 创建后状态：Run `pending`、7 Step 全 `pending`、`outbound_attempted=0`。
- 同项目 Run 总数由 2 变 3；历史两个 Run 仍为 failed，未删除、改写或重试。
- 创建后系统已停止，端口全部关闭；未注入 Key、未调用模型。
- 唯一下一步：负责人按系统交付席给出的隐藏输入命令启动固定环境；启动成功后，质量运行席仅对本 Run 调用一次 `run-next-step`，不得重试。

## 安全启动确认

- 负责人已确认固定环境启动成功；密钥未通过消息、Issue、Review 或仓库传递。
- 当前只授权质量运行席对 `wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc` 执行唯一一次 `run-next-step`。
- 调用前必须再次确认 Run pending、7 Step pending、outbound=0；任何不一致立即停止。
- 调用后无论成功或失败都不得重试，并须立即交系统交付席停止含凭据环境。

## 最终质量验收

- 质量 Review：`reviews/20260717_workspace_r3_real_model_execution_gate_review.md`，结论 `PASS`。
- 唯一 Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`；调用前 pending、7 Step pending、outbound=0。
- 仅调用一次，Gateway/Provider HTTP 200；首 Step 与 StepResult succeeded，Run 当前 running，其余 6 Step pending。
- Provider/Gateway/Model：`openai / newapi / gpt-5.4-mini-2026-03-17`。
- Token：44 / 372 / 416；成本 `USD 0.001707`；价格版本 `2026-07-17`。
- `model_call=1`、`outbound_attempted=true`、可信 `ceo_id`、Result 位置和脱敏证据完整；历史失败 Run 未变。
- 环境已停止，端口全 CLOSED，相关容器和后台进程 NONE。
- 产品验收：本真实模型执行 Gate 关闭；该 PASS 只覆盖首个真实模型 Step，不代表 Parent R3 七步纵向闭环已完成。
