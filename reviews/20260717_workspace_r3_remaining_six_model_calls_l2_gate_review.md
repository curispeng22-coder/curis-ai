# R3 剩余六步模型调用 L2 Gate 质量 Review

- Issue：`issues/20260717_workspace_r3_remaining_six_model_calls_l2_gate.md`
- 固定分支/修订：`feat/roadmap-r1r2` @ `250fc6833e5b40ca5876d63bea654c6b407a1cef`
- Run：`wfr-e96fe025-bcef-41b3-abef-3b0e8d43cbdc`
- 结论：`BLOCKED_L2`

## 结论

严格顺序真实执行未完成。Step 2→5 各自唯一调用成功；Step 6 `qa_verification` 的唯一请求返回 HTTP 422，原因 `Model gateway input exceeds the approved limit`。该拒绝发生在出网前，`outbound_attempted=0`，未重试、未重置、未 Fallback，也未调用 Step 7。

当前 Run 已准确停为 `failed`，Step 6=`failed`、Step 7=`pending`、`final_report` 为空。七步闭环验收不成立，保持 `BLOCKED_L2`。

## 调用前预检

- HEAD 与固定 SHA 一致。
- Gateway/Workspace/egress/JWKS 正常运行，Workspace 无宿主 8002 直连端口；凭据已隐藏注入且未读取或输出。
- Provider/路径/模型：`OpenAI / https://api.openai.com/v1/chat/completions / newapi / gpt-5.4-mini-2026-03-17`。
- tenant/project/Run 与六角色 role→binding 服务端集合全部精确匹配。
- Run=`running`；Step 1=`succeeded`；Step 2 是唯一最小 pending；Step 3→7 pending。
- 已有成功 outbound=1，累计 Token=`416`，累计成本=`USD 0.00170700`。
- 六个 Employee + 六条唯一 active approved model binding 完整。

## 真实执行结果

| Step | role / binding | HTTP | Step 终态 | outbound |
| --- | --- | ---: | --- | ---: |
| 1 | `tech_lead` / `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d` | 200（历史） | succeeded | 1 |
| 2 | `product_manager` / `bind-6d5b31e1-1b69-49a6-bd80-d2be741d6530` | 200 | succeeded | 1 |
| 3 | `architect` / `bind-b476f200-6bfc-4d8e-b1d7-c2c6e4e5f938` | 200 | succeeded | 1 |
| 4 | `frontend_engineer` / `bind-7275893a-7588-4f71-b780-ab55bef7db1d` | 200 | succeeded | 1 |
| 5 | `backend_engineer` / `bind-e2cbbcb3-b940-4bbd-bd09-1225b86a0eb3` | 200 | succeeded | 1 |
| 6 | `qa_engineer` / `bind-c04accdf-4567-4715-b9a3-46adf0eea40f` | 422 | failed | 0 |
| 7 | `tech_lead` / `bind-e222f21e-09de-43a6-aff5-0c1ae8b6555d` | 未调用 | pending | 0 |

每次 HTTP 调用后均先只读确认唯一 StepResult、UsageEvent、Execution、binding、模型、Token、成本、可信 CEO 与累计预算，再进入下一步。Step 6 失败后立即停止。

## Token、成本与审计

| Step | input | output | total | estimated_cost | UsageEvent |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 44 | 372 | 416 | `0.00170700` | 20 |
| 2 | 410 | 310 | 720 | `0.00170250` | 26 |
| 3 | 708 | 1176 | 1884 | `0.00582300` | 32 |
| 4 | 1888 | 332 | 2220 | `0.00291000` | 38 |
| 5 | 2216 | 302 | 2518 | `0.00302100` | 44 |
| 6 | 0 | 0 | 0 | `0.00000000` | 49（`limit_rejected`） |

- 成功 outbound：`5`，每个成功 Step 恰好一次。
- 累计成功 Token：input=`5266`、output=`2492`、total=`7758`。
- 累计成本：`USD 0.01516350 < USD 0.10`。
- 所有成功调用均为 `newapi / gpt-5.4-mini-2026-03-17 / price_version=2026-07-17 / status=success`。
- 所有审计均使用可信 `ceo-f9d4d433-18af-45c9-8c16-f5ea31ecf5ae`；subject 仅保存 64 字符 digest，未保存完整主体。
- Step 6 形成唯一 `usage.model_call` 拒绝审计：HTTP 422、`limit_rejected`、`outbound_attempted=0`、Token/成本均为 0；没有 StepResult 或 Execution。

## Result / Execution 落点

| Step | StepResult | Execution | bytes | SHA-256 |
| --- | --- | ---: | ---: | --- |
| 1 | `wfrs-9169b874-72f3-45ce-8ebe-d99162bb166b` | 2 | 1353 | `ba44bc0b43e2b243425e44ffa1ac8305b96a4f879fafb92249c5f677a7ed47af` |
| 2 | `wfrs-a31bbdcb-4b04-4c75-b9d0-3ae26cc4d7dc` | 3 | 1042 | `fa6b042e63609e9d1eb3b902adebaef12797507c53452816d5cab16d82f34d07` |
| 3 | `wfrs-282435b5-a93b-4676-981d-d2bb919c56ac` | 4 | 3820 | `de30bbc99c31925575c8cd41629093bd3b137f8aaf6fa694ff701e50c0daffce` |
| 4 | `wfrs-2c82937b-9a57-4674-9b86-91e151084f89` | 5 | 1198 | `bc758a4ccd5012563f5cf4f24e32364ebefe1a34c8846467c47d3d3c70c15eb2` |
| 5 | `wfrs-ae2823dc-8c8c-4f11-ab03-73d23c4dd8e1` | 6 | 1103 | `0226e801cb2f070ba95c720f1f58c8ac2698f95d699652de155afd6f17b9cd8c` |

每个成功 Step 的 `step_results.result` 与对应 `executions.output` 非空、内容一致；本 Review 只记录位置、长度和哈希，不输出模型原文。Step 6/7 无成果落点，Run 无 final_report。

## 边界与停机

- 历史失败 Run `wfr-69926fdb-21a2-4166-b6c6-37059309d7ff`、`wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6` 保持 failed；首步 StepResult/Execution/UsageEvent 保持原 ID 与内容哈希。
- Workspace 日志未发现 Key、Authorization/Cookie 值、JWT、完整 subject、prompt 或 raw response。Gateway 启动日志仅出现静态 header 名称，未出现 Bearer/JWT/header 值或其他敏感内容。
- 系统交付席已执行 `deploy/curis/stop-local.sh`；质量席独立确认 `3000/3100/8001/8002/8080` 全部 CLOSED，Gateway/Workspace/egress/JWKS 相关容器均不存在。
- 未修改代码或配置、未直接改库；数据变化仅来自六次授权 API 中实际发生的 Step/Result/Execution/UsageEvent 状态写入。未提交、未跑全量、未扩大到 Artifact/项目状态。

## 唯一阻塞

现有 Workflow 把全部前序模型结果累积进下一 Step 输入；到 Step 6 时超过批准的 8192 input-token 上限并被 Adapter 正确 fail-closed。由于本次授权禁止重试、重置和第二 Run，当前 Run 已不可继续达到七步 succeeded。

唯一下一步：产品规划席就“受控压缩/裁剪前序上下文并使用新授权 Run”建立独立 Gate；不得重置或重试本 Run，也不得放宽 8192 Token 上限。

## 状态

- 顺序、单次、失败停机、预算与脱敏：`VERIFIED — PASS`
- 七步真实执行：`FAILED AT STEP 6`
- 最终：`BLOCKED_L2 — STEP6_INPUT_EXCEEDS_APPROVED_LIMIT`
- Next Seat：产品规划席
- Handoff：sent to 产品规划席
