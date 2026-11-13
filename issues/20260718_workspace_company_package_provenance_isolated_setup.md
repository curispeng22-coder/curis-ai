# Workspace：同源版本化桥接隔离链准备

- 状态：`CLOSED`
- 优先级：`P0`
- 决策：总控决策席（`APPROVE_ONE_TIME_TRUSTED_MEMBERSHIP_CEO_PROVISIONING`）
- 执行：系统交付席
- 质量复核：质量运行席
- 父 Issue：`issues/20260718_workspace_company_package_provenance_real_execution_gate.md`
- 前置：`issues/20260718_workspace_package_workflow_versioned_bridge_implementation.md`（`CLOSED`）

## 目标

只准备一条新的、隔离的、可审计的 Package 来源链，产出执行前事实；不放行模型执行。

固定资产：

- Package：`ccp_ai_software_company@1.0.0`
- Bridge：`bridge.ccp_ai_software_company.1.0.0.software_rnd_sop.1.0.0`
- Workflow：`official.workflow.software_rnd_sop@1.0.0`
- Workflow capability：`structured_executable`

## 唯一执行范围

1. 在同一个实际执行数据库中，使用既有 Admin 受控版本化发布路径确认/落地上述 Package、Bridge、Workflow；不得从 `data/curis.sqlite` 与 `quality.sqlite` 拼接证据。重复、缺失、状态或版本不一致立即停止。
2. 在服务端完全停机、无公开写 API、无 Header、无 Admin token 的条件下，仅对实际 `quality.sqlite` 执行已批准的一次性 membership+CEO 受控 provisioning：使用既有可信 `https://quality.issuer.local` + `quality-member-sub`，生成全新 tenant/company/ceo/membership/operation ID，创建唯一 active membership 与 Company CEO 映射。使用 `BEGIN IMMEDIATE`，冲突、重复、非唯一、写入计数或审计条件不符整体 rollback。
3. 通过既有批准 API 创建全新隔离 tenant 的其余 Company、Department、Employee、Binding、Project、Task、Run；实际返回 ID 必须保存为本阶段输出。
4. 通过既有 Company Package 实例化路径创建 Department、6 Employee；按已批准六角色集合建立 6 个 active binding，均绑定既定 official model capability，不得复用 `company-a` 或历史 Employee/Binding。
5. 创建一个 Project、一个 Task 和唯一 `pending` Run。Run 必须从该新 Workflow Instance 继承来源快照；客户端不得提供或覆盖来源字段。
6. 创建完成后立即停机。此阶段不得调用 `run-next-step`、不得创建 Result/Execution/Usage/Artifact、不得出网。

## 必须保持的来源不变式

`tenant → active membership/CEO → Company → Package/version → Bridge → executable Workflow/version → Workflow Instance → Project → Task → pending Run`

每一跳必须在同一数据库由服务端字段或真实关联证明；禁止默认、latest、同名、客户端 Header、历史记录、跨库查询或人工拼接。任何不可证明关系 fail-closed，且不得产生部分实例。

六角色（Tech Lead、Product Manager、Architect、Frontend Engineer、Backend Engineer、QA Engineer）各有一个新的唯一 Binding。服务端必须为本次新隔离 tenant 的新 Employee 生成全新、不可预测的 UUID `binding_id`；不得复用、覆盖或引用 `tenant-a` 的任何历史 Binding。每个 Binding 必须属于新 tenant/Company/Department，并指向既定 official model capability；创建后实际返回的 `role → binding_id` 精确映射是本次 Setup 与后续真实执行 Gate 的唯一输入。

## 已批准的受控 provisioning 边界

- 仅允许一次性 additive/idempotent `BEGIN IMMEDIATE` 事务写入 `/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite`；不得跨库。
- 仅写本隔离链所需的新 tenant/company/ceo/membership/operation 记录与脱敏 append-only 审计元数据；不得修改历史 `company-a`、历史 Run/Usage、其他租户或既有 Package/Bridge/Workflow。
- 服务端生成全新 ID；可信 issuer/subject 固定为 `https://quality.issuer.local` + `quality-member-sub`。不得用默认主体、客户端 Header、Admin token 或外部网络。
- HMAC 审计 Key 缺失立即停止；不得读取、输出或落盘其值。审计不得含 token、Cookie、Authorization、Key 或 subject 原值。
- 冲突、重复、非唯一、来源不一致、写入计数不符或审计失败必须整体 rollback；提交后仅允许对本次 operation 可精确识别的记录做受控补偿撤销。
- 重复 `operation_id` 只能返回同一已创建的 `role → binding_id` 映射；不能证明相同 operation 的请求一律整体拒绝。
- 既有 R3 Provider、Model、Gateway、成本、身份和出口配置只读复用；本 Issue 不启动、不注入凭据、不改变配置。

## 停机后的质量核验

质量运行席只读核对：

1. 全部记录来自同一实际数据库，tenant/Company/Department/6 Employee/6 Binding/Project/Task/Workflow Instance/Run 均唯一且 active/pending 状态正确；
2. Package、version、Bridge、Workflow、version 与 Company/Instance/Run 来源快照逐项一致；
3. 撤销 Bridge 后新 Task/Run 创建被拒绝且计数为零；跨租户读取被拒绝；
4. pending Run 的 `outbound_attempted=0`，Result/Execution/Usage/Artifact 均为零；
5. 日志、数据库、Issue、Review 不含凭据值。

质量复核输出：`reviews/20260718_workspace_company_package_provenance_isolated_setup_review.md`。
只有质量 `PASS` 后，才允许提交带实际 ID 的单次真实执行 Gate；本 Issue 不授权模型调用。

## 禁止范围

- 不修改历史 `company-a`、历史 Run/Usage、既有 Package/Bridge/Workflow 版本；
- 不启动服务、不注入 Key、不调用模型、不出网；
- 不新增 Provider、Model、Gateway、Fallback、重试、成本规则、前端、Billing、Secretary 或 RBAC；
- 不做历史回填、数据跨库复制或任何客户端身份/租户/CEO 覆盖。
- Bridge 表与 Workflow 版本列必须先由既有受控初始化发布路径在同一 `quality.sqlite` 落地并可证明存在；不得跨库拼接。

## 交接

系统交付席完成准备后直接交质量运行席；质量席只读复核并回产品规划席。

Issue：`issues/20260718_workspace_company_package_provenance_isolated_setup.md`
Objective：建立同库、同源、隔离的执行前来源链，不出网。
Special Constraints：不启动、不注Key、不调用模型；失败 fail-closed。
Next Seat：质量运行席

## 收口结果

质量运行席在 `0947b9e6` 对同一 `quality.sqlite` 完成停机只读核验并给出 PASS。来源链、6 个新 Employee / Binding、唯一 pending Run、7 个 pending Step、零 Result / Execution / Usage / outbound / model event 以及五端口全关闭均成立。见 `reviews/20260718_workspace_company_package_provenance_isolated_setup_review.md`。

## 系统交付结果（2026-07-18）

- 实际库：`deploy/curis/gateway/.generated/data/quality.sqlite`
- operation：`op-9f341260-0a91-4e39-8b83-e8fd9c62cd56`
- provisioning：`prov-7da2ad98-d821-4c6b-9f3d-cec35dfaf959`
- tenant：`tenant-3160d289-7dfa-4684-8e53-f25d1fa3fd8a`
- CEO：`ceo-55642f4c-9e00-4ef0-be11-8f4568d64430`
- membership：`membership-fcfabb3d-cf4a-4f1b-b97a-1df419d035a9`
- Company：`company-f108f133-597b-4d12-9682-53c821af5b32`
- Department：`dept-c0fb4115-6919-44b8-b4dc-d7f62b2ae17f`
- Workflow Instance：`wfi-f0eb0523-0e36-4ed3-8c65-1b03fd5f2200`
- Project：`project-bc562b8d-37b3-4f03-bbff-658dcef851aa`
- Task：`087e4a8b-4aa4-4a35-a6fb-bff0b60e81a3`
- pending Run：`wfr-06489c59-fd30-47f1-8bbf-0d19c5d15415`

| role | employee_id | binding_id |
| --- | --- | --- |
| tech_lead | `emp-1c1f3c1b-db51-451c-b33d-02e7d229b719` | `bind-1504ce7e-75fe-4db6-b3cb-094a80a2ffdf` |
| product_manager | `emp-a8d95229-fcb5-4786-b18b-fa8fc8fe8de7` | `bind-1c42b740-8548-4af1-9060-91466659c86b` |
| architect | `emp-d150ca5f-a671-40a2-83a6-f5a39d0171d2` | `bind-40bdb391-4ad1-4af1-bf55-c13e0ffedf3b` |
| frontend_engineer | `emp-12bf8b42-4cf8-4de2-a3c0-75e3b8924f12` | `bind-5b69658a-2074-4c04-9803-d92f0b498eee` |
| backend_engineer | `emp-5a1ce6bf-1a71-4d36-bab8-703313c35af2` | `bind-1b324332-4071-479c-aab3-308b345eae30` |
| qa_engineer | `emp-c88882bb-393d-4e64-9d1b-db142c0c622e` | `bind-5aa4a90f-b541-45a1-a2ac-6d6cacb26095` |

停机只读回读：tenant/company/membership/department/project/task/Run 各 1，Employee/active Binding 各 6，Package Workflow Instance 共 6 且精确 bridge 的 executable Instance 为 1，Run 为 `pending`、7 Step 全 `pending`；Result/Execution/Usage/outbound/model event 均 0。3000/3100/8001/8002/8080 全部关闭；未注入 Key、未出网、未调用模型。

Handoff: sent to 质量运行席。
