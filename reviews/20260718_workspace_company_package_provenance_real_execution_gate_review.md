# Workspace 软件公司包来源链真实执行 Gate 质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_company_package_provenance_real_execution_gate.md`
- 裁决：`APPROVE_PROVENANCE_R3_STEP1_SINGLE_CALL`
- 分支：`feat/roadmap-r1r2`
- 固定 SHA：`0947b9e6425dc586e77303e559098df2394fa6ad`
- 固定数据库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- 质量结论：`PAUSED_BY_NEW_PRIORITY`

## 结论

本次唯一 Step1 调用未执行，授权未消耗。服务端固定输入与同库来源链预检全部匹配，但批准的隐藏部署变量 `CURIS_MODEL_GATEWAY_API_KEY` 在宿主环境未设置，现有 `quality.env` 变量集合中也不存在；当前没有 Workspace 运行容器可提供已注入状态。缺少执行所必需的外部凭据注入，按 Gate 的 Adapter 前 fail-closed、失败即停、不得重试约束停止，不启动服务、不发起 HTTP、不创建第二 Run。

## 固定输入预检

- HEAD 精确等于 `0947b9e6425dc586e77303e559098df2394fa6ad`。
- Run：`wfr-06489c59-fd30-47f1-8bbf-0d19c5d15415`，`pending`。
- tenant：`tenant-3160d289-7dfa-4684-8e53-f25d1fa3fd8a`。
- Company：`company-f108f133-597b-4d12-9682-53c821af5b32`。
- Package：`ccp_ai_software_company@1.0.0`。
- Bridge：`bridge.ccp_ai_software_company.1.0.0.software_rnd_sop.1.0.0`，`active`、未撤销。
- Workflow：`official.workflow.software_rnd_sop@1.0.0`。
- Workflow Instance：`wfi-f0eb0523-0e36-4ed3-8c65-1b03fd5f2200`。
- Project：`project-bc562b8d-37b3-4f03-bbff-658dcef851aa`。
- Task：`087e4a8b-4aa4-4a35-a6fb-bff0b60e81a3`。
- Company、Workflow Instance、Run 的 Package/version/Bridge/Workflow/version 来源快照逐项一致。
- 7 个 Step 全为 `pending`；StepResult=0、Execution=0、UsageEvent=0、outbound_attempt=0。
- 六角色 Binding 与 Gate 固定映射全部存在、enabled，均属于同一 tenant/Company/Department，并指向 `official.openai.gpt-5.4-mini-2026-03-17`。

## 凭据与停机证据

- 宿主仅检查变量是否存在：`CURIS_MODEL_GATEWAY_API_KEY=UNSET`；未读取或输出值。
- `deploy/curis/gateway/.generated/quality.env` 只枚举变量名，未发现 `CURIS_MODEL_GATEWAY_API_KEY`；未读取或输出任何变量值。
- 端口 `3000/3100/8001/8002/8080` 全部关闭；没有运行容器可核验 Key 注入。
- 未启动服务、未签发 Token、未发送 HTTP、未调用模型、未修改数据库。
- Run 与 7 Step 保持原状；调用次数仍为 0。

## 暂停前阻塞记录

唯一阻塞：安全边界席尚未通过批准的隐藏部署机制向 Workspace 运行容器注入 `CURIS_MODEL_GATEWAY_API_KEY`。

原恢复路径为受控部署设施或 Owner 完成隐藏注入，再由安全边界席回传 `SET_AND_MATCH`。该路径现已被 `PAUSED_BY_NEW_PRIORITY` 覆盖，不再授权质量席调用。

Next Seat：产品规划席（发起新的唯一前置 Gate）

Handoff: HANDOFF_REQUIRED

## 安全边界席正式回传

安全边界席独立确认宿主环境 `CURIS_MODEL_GATEWAY_API_KEY=MISSING`；未读取或输出值，未启动服务、未调用模型、未修改 Run。安全席不能凭空恢复凭据，也不得通过消息传递 Key。

此前状态为 `WAIT_FOR_OWNER_INJECTION`，不并列 `BLOCKED_L2`；凭据尚未注入不构成范围、设计或安全裁决失败。

## 优先级变更

总控决策席已将本 Gate 状态改为 `PAUSED_BY_NEW_PRIORITY`。即使后续收到 Key 注入或安全席 `SET_AND_MATCH` 证据，也不得继续调用；Run、7 Step 与唯一 Step1 授权均保持未消费状态。恢复必须等待总控或产品规划席新的明确 Gate，不得沿用此前等待注入的恢复路径。

质量运行席后续仅承接产品规划席发起的唯一前置 Gate，负责全量回归与真实研发工具 E2E 独立验收，不修改代码。
