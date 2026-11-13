# Workspace R3 可信 CEO UsageContext L2 Gate

- 日期：2026-07-17
- 状态：CLOSED — PASS
- Parent：`issues/20260717_workspace_r3_real_model_execution_gate.md`
- Owner：产品规划席
- Next Seat：产品规划席 → 总负责人（Parent R3 新单 Run 授权）
- 类型：身份与审计安全边界

## 结论

真实 Provider 已成功返回，但系统在写 Token / 模型 / 成本 UsageEvent 时要求可信 `X-Ceo-Id`，现有 Gateway 与 Workspace 身份上下文未提供该值，导致真实结果已产生、审计未落库、Run 最终失败。

本 Issue 只补齐可信 CEO 审计上下文，不修改 Provider、Model、Gateway、租户模型、成本规则或调用额度。

## 真实证据

- Run：`wfr-ecc7d911-f851-4c94-b4d6-98f657ad52f6`。
- 唯一 Gateway 调用：HTTP 200。
- StepResult：`wfrs-f54a67e0-58ec-463e-9e80-0d546c9793af`，`succeeded`。
- 模型：`gpt-5.4-mini-2026-03-17`。
- 已计算成本：`0.001302`。
- 精确失败：`X-Ceo-Id is required to write UsageEvent`。
- 质量 Review：`reviews/20260717_workspace_r3_real_model_execution_gate_review.md`。

## 安全边界席必须确定的唯一契约

1. `ceo_id` 必须来自可信身份链，不能相信客户端直接提交的 `X-Ceo-Id`。
2. 明确复用现有哪一个事实源：已验证 JWT claim、active membership、Company / Project 角色映射或现有 CEO 实体；不得新增平行身份体系。
3. Gateway 必须剥离客户端同名 Header；如由 Gateway 注入，必须来自签名验证后的固定映射。
4. 如由 Workspace 服务端推导，必须绑定当前 TenantContext、company、project 与 active membership，并保持跨租户 fail-closed。
5. Admin token 不能作为 Workspace CEO 身份；不得使用默认 CEO、固定字符串或仅凭 `X-Tenant-Id` 推导。
6. 缺失、已撤销、过期、角色不匹配或跨租户时，必须在模型出网前拒绝或以明确的审计前置错误终止。
7. 日志不得记录 token、Authorization、Cookie、完整 subject、API key 或模型原文。
8. 回滚不得恢复客户端可伪造 Header、默认 CEO 或跳过 UsageEvent。

## 允许范围

- 可信 Gateway 的最小 Header 清理 / 注入映射。
- Workspace 身份、membership、TenantContext 与 UsageEvent 写入链直接相关的最少后端文件。
- 直接相关的 focused tests、部署示例与本 Issue Review。
- 不出网的本地验证数据；不得使用真实模型调用验证实现阶段。

## 禁止范围

- 不创建新 Provider、Model、Fallback、重试或第二 Gateway。
- 不放宽现有 tenant / project / workflow / binding scope。
- 不让客户端自行指定 CEO 身份。
- 不改 Admin 产品身份，不新增完整 RBAC，不扩展前端。
- 不删除或修补既有失败 Run 与成功 StepResult。
- 未获新的单 Run 审批前，不创建用于出网的新 Run，不注入 Key，不调用模型。

## 实施前验收门槛

- 安全边界席给出 `PASS` 或 `BLOCKED_L2`，并明确唯一可信来源和 fail-closed 规则。
- 总负责人批准唯一契约。
- 系统交付席只做最小实现并运行 focused tests。
- 安全边界席复核 spoof、跨租户、撤销、缺失上下文与日志脱敏。
- 质量运行席在不出网条件下证明 UsageEvent 可获得可信 `ceo_id` 并完整写入测试字段。
- 上述全部 PASS 后，产品规划席才能申请新的单 Run 与一次调用授权。

## 最终验收

新的唯一授权 Run 必须同时形成：

- Provider 成功结果；
- Run / Step 成功状态；
- 真实 input / output / total tokens；
- 精确模型、`price_version` 与 `estimated_cost`；
- `model_call=1`、`outbound_attempted=true` 与可信 `ceo_id` 审计；
- 脱敏日志；
- Result 与 Artifact 位置。

任一缺失，R3 Gate 继续 `BLOCKED_L2`。

## 安全边界首轮结论

- Review：`reviews/20260717_workspace_r3_trusted_ceo_usage_context_security_review.md`。
- 结论：`BLOCKED_L2`。
- 现有可信链只提供 subject、tenant、company、role 与 membership 状态；尚无已确认的服务端 `ceo_id` 事实源或映射。
- 当前 `CeoContext` 直接读取客户端 `X-Ceo-Id`，不能作为 UsageEvent 可信审计身份。
- 下一步只允许架构边界席核对现有数据模型并形成唯一事实源方案；未获安全 PASS 与总负责人批准前不得实施。

## 唯一架构契约与安全复核

- Architecture Review：`reviews/20260717_workspace_r3_trusted_ceo_usage_context_architecture_review.md`。
- 唯一方案：在现有 `tenant_memberships` 上 additive 增加 `ceo_id`，不新增平行身份体系。
- 推导链：verified subject → active membership → tenant/company/ceo_id → active Company 一致性 → 当前 Project/Run。
- 模型出网前 fail-closed；UsageEvent 只读取服务端 UsageContext。
- 客户端 `X-Ceo-Id`、Admin token、默认 CEO、固定字符串和仅 tenant 推导全部无效。
- 安全边界席复核：`PASS`（仅架构契约）；实现和真实执行继续 `BLOCKED_L2`，等待总负责人批准。

## 总负责人批准

- 决策：`APPROVED`，仅批准本 Issue 的唯一方案。
- 实施范围严格限于 additive `tenant_memberships.ceo_id`、服务端 UsageContext 确定性推导与模型出网前 fail-closed。
- 不得修改 Provider、Model、Gateway、成本规则、前端或 Admin，不得删除历史失败 Run。
- 实施与修复阶段仅允许 focused、无出网验证；不得注入 Key、创建 Run 或调用模型。

## 首轮质量复核与返修要求

- 实现修订：`fee55346f49c4e71d1032ecfdaa580eef18dd391`。
- 质量 Review：`reviews/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate_review.md`。
- 结果：`11 passed / 1 failed`，继续 `BLOCKED_L2`。
- 唯一根因：binding 前置 SQL 使用了 Employee Runtime 不存在的 `status='active'`；合法可执行状态为 `idle / assigned` 且 `enabled`，`disabled` 必须继续 fail-closed。
- 本轮只允许修正该状态契约，并补足正向基线与 Run 错配的 Recorder 断言；不得放宽其余身份、租户、Company、Project、Run、binding 或审计边界。
- 修复后由质量运行席原样重跑同一无出网聚焦集；未全绿前不得申请新的单 Run 或真实模型调用。

## 最终收口

- 修复修订：`718af2c463e39820ac6928681b16818a9fbccc25`；仅修改 `backend/app/main.py` 与 `backend/tests/test_model_gateway_adapter.py`。
- 系统交付 focused：`14 passed`；质量运行席固定同修订独立复跑：`14 / 14 passed`。
- 正向 Workflow → UsageEvent：HTTP 200、Step succeeded、Recorder=1。
- Project / Run 错配与 disabled employee：HTTP 403、Recorder=0，均在出网前独立 fail-closed。
- additive `ceo_id` 迁移、服务端 CEO 推导、客户端伪造 Header 无效及其余身份/租户边界通过。
- 未启动服务、未注入 Key、未创建 Run、未调用模型、未跑全量回归。
- 产品验收：本 L2 Issue 关闭；Parent R3 仍保持 `BLOCKED_L2`，等待总负责人批准新的单 Run 与唯一一次真实调用。
