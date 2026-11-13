# Workspace：软件公司包来源链真实执行 Gate

- 状态：`PAUSED_BY_NEW_PRIORITY`
- 优先级：`P0`
- 发起：产品规划席
- 决策：总控决策席
- 执行：系统交付席 / 质量运行席
- 前置证据：`issues/20260718_workspace_package_workflow_versioned_bridge_implementation.md` 已 CLOSED

## 目标

在一个全新的隔离 tenant / Company 实例上，用已验收的版本化桥接创建 Package 来源可追溯的 Workflow Instance，并只在总控明确批准后完成一次受控真实模型执行，证明 Package → Company → Workflow → Run → Artifact → Token / Cost 是同一来源。

前置 setup Issue：`issues/20260718_workspace_company_package_provenance_isolated_setup.md`。该 Issue 未通过前，不得申请或执行模型调用。

## 已核验的本次唯一输入

- 固定 SHA：`0947b9e6425dc586e77303e559098df2394fa6ad`
- tenant：`tenant-3160d289-7dfa-4684-8e53-f25d1fa3fd8a`
- Company：`company-f108f133-597b-4d12-9682-53c821af5b32`
- Package / version：`ccp_ai_software_company@1.0.0`
- Bridge：`bridge.ccp_ai_software_company.1.0.0.software_rnd_sop.1.0.0`
- Workflow / version：`official.workflow.software_rnd_sop@1.0.0`
- Workflow Instance：`wfi-f0eb0523-0e36-4ed3-8c65-1b03fd5f2200`
- Project：`project-bc562b8d-37b3-4f03-bbff-658dcef851aa`
- Task：`087e4a8b-4aa4-4a35-a6fb-bff0b60e81a3`
- 唯一 pending Run：`wfr-06489c59-fd30-47f1-8bbf-0d19c5d15415`

| role | binding_id |
| --- | --- |
| tech_lead | `bind-1504ce7e-75fe-4db6-b3cb-094a80a2ffdf` |
| product_manager | `bind-1c42b740-8548-4af1-9060-91466659c86b` |
| architect | `bind-40bdb391-4ad1-4af1-bf55-c13e0ffedf3b` |
| frontend_engineer | `bind-5b69658a-2074-4c04-9803-d92f0b498eee` |
| backend_engineer | `bind-1b324332-4071-479c-aab3-308b345eae30` |
| qa_engineer | `bind-5aa4a90f-b541-45a1-a2ac-6d6cacb26095` |

上述 Run 仍为唯一 `pending`，7 Step 均 `pending`，Result / Execution / Usage / outbound / model event 均为零。除总控这次裁决外，不得替换任何输入。

## 已批准执行契约：仅 Step1 一次调用

- 仅 Run `wfr-06489c59-fd30-47f1-8bbf-0d19c5d15415` 的 Step1 可真实调用一次；Step2–7 必须保持 `pending`。
- 固定路径：OpenAI API / `gpt-5.4-mini-2026-03-17` / `newapi` / `https://api.openai.com:443/v1/chat/completions`。
- Key 仅由隐藏部署注入 `CURIS_MODEL_GATEWAY_API_KEY`；不得读取、输出、持久化或经消息传递。
- 输入 / 输出 / 总 Token 上限：8192 / 2048 / 10240；60 秒；0 重试；429 不重试；无 Fallback；累计成本硬上限 USD 0.10。
- 启动前服务端精确预检 Gate 中所有来源输入；任一差异必须在 Adapter 前拒绝。
- 调用后立即停机；失败即停；不得创建第二 Run、跳步、重置或重试。
- 质量运行席只执行此一次 Step1，并记录来源、HTTP、StepResult / Execution / Usage / Artifact、Token / 价格 / 成本及停机证据。其余六步必须待质量回传后另立 Gate。

## 等待状态

所有无凭据准备已通过。唯一外部依赖是 Owner 通过受控部署设施隐藏注入已有 `CURIS_MODEL_GATEWAY_API_KEY`；这不是代码或质量阻塞。等待期间不得启动或调用。

## 优先级暂停

总控已将唯一主目标切换为“真实研发工具闭环”。本 Gate 保留未消耗的 Step1 授权、所有实际来源输入和 pending Run，但不得注入 Key、启动或调用；仅在总控重新授权后恢复。

## 裁决所需固定项

总控必须逐项固定后才可启动：

1. tenant、Company Package ID / version、bridge ID、精确 Workflow Template / version、Project、Task、6 个角色 Binding；
2. 单一 Run 与逐步次数上限；
3. 已批准的 Provider、Model、Gateway、受控出口、凭据注入方式；
4. Token / 成本总上限、超时、0 重试、无 Fallback、失败即停；
5. 完成后停机与质量席独立核验方式。

## 禁止范围

- 未裁决前不创建运行实例、不启动服务、不注入 Key、不调用模型。
- 不修改历史 `company-a`、历史 Run/Usage、既有 Package 版本或 bridge。
- 不改模型/网关/成本规则、前端、Secretary、Admin 公开写 API 或身份边界。

## 验收

只有质量席独立确认以下项目，主来源追溯 Issue 才可收口：

1. Package、version、bridge、Company、Workflow Instance、Run 的来源快照逐跳一致；
2. Run 的 Result、Execution、Usage、Artifact、Token、价格版本和成本全部属于该 Run；
3. 每步限额与 fail-closed 保持；跨租户与来源错配拒绝；
4. 不存在默认、latest、同名、客户端覆盖或历史记录替代来源；
5. 运行结束后环境停止，凭据不进入日志、数据库、Issue 或 Review。
