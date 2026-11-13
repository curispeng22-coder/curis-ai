# Workspace R3 AI 研发部真实纵向 E2E 质量 Review

- 日期：2026-07-17
- Issue：`issues/20260717_workspace_r3_ai_rd_vertical_e2e.md`
- 固定分支：`feat/roadmap-r1r2`
- 固定 SHA：`b0f791f74e449be1d6c907480cc183cf92a78209`
- Run：`wfr-33a17cee-eb1f-43d6-8f2f-01d521e46e50`
- 结论：`PASS`

## 结论

七步真实模型链通过。Step1→6 的既有成功证据保持不变；总负责人重新明确授权后，质量席仅补跑一次 Step7，并同时携带内存短期 member token 与 `X-Tenant-Id: tenant-a`。Step7 HTTP 200/succeeded，Run 与 7 个 Step 全部 succeeded，7 个 StepResult、Execution、outbound UsageEvent 一一对应，`final_report` 非空。

总计 7 次真实 model_call、9,622 tokens、成本 `$0.01326900`，低于 `$0.10`。没有重试、Fallback、第二 Run、代码/配置修改或历史记录改写；采证后环境已完全停止。

## 执行前核对

- Run=`pending`，7 个 Step 全部 `pending`，StepResult=0，outbound=0。
- 固定 Provider/Model/Gateway：OpenAI / `gpt-5.4-mini-2026-03-17` / `newapi`。
- 受控 egress、6 Employee、六角色精确 binding、可信 CEO、tenant/company/project/run scope 均在启动环境中匹配。
- `R3_WORKFLOW_CONTEXT_MAX_BYTES=7168`。
- 凭据仅检查“已注入”，未读取、输出或落盘。
- Step7 补跑前再次确认：Run=`running`，Step1→6=`succeeded`，Step7 是唯一 `pending`；StepResult/Execution/outbound UsageEvent 均为 6；累计成本 `$0.01081275`。
- Step7 请求前只记录 Header 名称 `Authorization`、`X-Tenant-Id`、`Content-Type`，没有输出 Header 值。

## 逐步真实执行证据

| Step | 类型 / 角色 | Binding | HTTP / 终态 | StepResult / Execution / UsageEvent | Token（入/出/总） | 成本 USD |
| --- | --- | --- | --- | --- | --- | ---: |
| 1 | `tech_lead_breakdown` / `tech_lead` | `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d` | 200 / succeeded | `wfrs-acb45b77-3276-478b-91e1-5fa3d36e838c` / 7 / 57 | 103 / 195 / 298 | 0.00095475 |
| 2 | `requirement_clarification` / `product_manager` | `bind-6d5b31e1-1b69-49a6-bd80-d2be741d6530` | 200 / succeeded | `wfrs-017d7810-13de-49f3-807d-adfb438548da` / 8 / 63 | 441 / 225 / 666 | 0.00134325 |
| 3 | `architecture_design` / `architect` | `bind-b476f200-6bfc-4d8e-b1d7-c2c6e4e5f938` | 200 / succeeded | `wfrs-37d5ec02-df19-4634-b7ac-c5205badb9a4` / 9 / 69 | 800 / 251 / 1,051 | 0.00172950 |
| 4 | `frontend_execution` / `frontend_engineer` | `bind-7275893a-7588-4f71-b780-ab55bef7db1d` | 200 / succeeded | `wfrs-0c0bbcb6-a9c2-44d4-a11d-ffd9a6b13e19` / 10 / 75 | 1,202 / 239 / 1,441 | 0.00197700 |
| 5 | `backend_execution` / `backend_engineer` | `bind-e2cbbcb3-b940-4bbd-bd09-1225b86a0eb3` | 200 / succeeded | `wfrs-12ab6453-1380-4062-8cb6-2c1c248a33a3` / 11 / 81 | 1,590 / 248 / 1,838 | 0.00230850 |
| 6 | `qa_verification` / `qa_engineer` | `bind-c04accdf-4567-4715-b9a3-46adf0eea40f` | 200 / succeeded | `wfrs-f342a232-44f0-42b7-ad24-3d8b7c87ee00` / 12 / 87 | 1,875 / 243 / 2,118 | 0.00249975 |
| 7 | `final_report` / `tech_lead` | `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d` | 200 / succeeded | `wfrs-fc612973-64e3-445e-9677-67781c7df99e` / 13 / 93 | 1,997 / 213 / 2,210 | 0.00245625 |

七次成功调用均记录：model=`gpt-5.4-mini-2026-03-17`、price_version=`2026-07-17`、outbound_attempted=1、同一可信 CEO `ceo-f9d4d433-18af-45c9-8c16-f5ea31ecf5ae`。累计 9,622 tokens，累计成本 `$0.01326900`，低于 `$0.10`。

## 上下文预算与结果一致性

Step1→7 调用前只读重建的上下文分别为 354B、1,331B、2,429B、3,639B、4,798B、5,508B、5,749B，全部不超过 7,168B；Step6、Step7 已出现 `TRUNCATED`。所有既有 prior StepResult 的 SHA-256 与 `ref=step_results/<id>` 均存在于后续上下文元数据。

Step1→7 各只有一个 StepResult、一个 Execution 和一个 outbound UsageEvent；StepResult 与对应 Execution output 完全一致。结果 SHA-256：

- Step1：`4e1d38eb410227270b444b5a0697e5c05cdaf7df58fed11bfb543d959e1c199c`
- Step2：`72f139ace16dfcb8d15f3d85fd3929dff029d88d42aaca3462dd5fe658527467`
- Step3：`47237a262b01ad4143a08c3bf69381439b4042f8e0f0eb834e9612fb26ab28a9`
- Step4：`1ddd597e7d8131433d1a917121c96f8cf7f979e37780d69c6ad2f8d102467790`
- Step5：`d309c5cdd16be2af5b3ec8b90c79158769fdbf00df7d0303faa99c863a144526`
- Step6：`e16bae2e9b88928b04d64c60456ae6e01da024f23aa57213359b490d9d3f16d9`
- Step7：`d515dd8a5e231b7ee458e9c78486cf085e820b5410a827f58d434622708ded90`

Run 最终 `final_report` 为 6,018B，SHA-256=`2d14cf90ca1fa850f7e8425763b922cda4c6c9c2132a2f55eac07791a07ba96c`，内容非空。

## Step7 前次拒绝与本次收口

- 前次授权调用返回 HTTP 403；请求 ID=`d656b898-0382-4ada-b6c6-3d93ccf269d8`。
- Workspace 身份审计：`outcome=deny`、`reason=target_tenant_missing`、`tenant_id=""`。
- 失败发生在身份闸门，未进入 Workflow 分配、模型网关或 egress；Step7 没有 StepResult、Execution、outbound UsageEvent。
- 当次严格停止且没有重试。总负责人随后签发新的“一次 Step7”授权，本次请求补齐 `X-Tenant-Id: tenant-a`，仅调用一次并 HTTP 200。
- 本次调用新增且仅新增 Step7 的一组记录：StepResult=`wfrs-fc612973-64e3-445e-9677-67781c7df99e`、Execution=13、UsageEvent=93；Run=`succeeded`。
- 前次 403 没有计入 model_call；最终 outbound model_call=7、distinct workflow_step_id=7，每 Step 恰好一次。

## 边界与停机

- 历史 Run `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`、`wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`、`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc` 仍为 `failed`。
- Workspace/Gateway/egress 日志扫描：JWT、OpenAI Key、Bearer 值、Cookie 值、完整 subject、原始 prompt、原始 model response 命中均为 0。
- 系统交付席执行 `deploy/curis/stop-local.sh` exit 0；Gateway/Workspace/egress/JWKS 均已移除。
- 质量席独立核对：3000/3100/8001/8002/8080 全部 CLOSED；R3 容器=NONE；后台 screen=NONE。
- 按本轮明确约束，没有运行聚焦或全量回归，也没有扩大到 Artifact/项目状态。

## 最终状态

本次七步真实执行与停机验收为 `PASS`，前次 `target_tenant_missing` 阻塞已在新授权的一次 Step7 调用中关闭。本 Review 可交产品规划席验收；本轮不包含 Artifact 或项目状态扩展验证。

Handoff: sent to 产品规划席
