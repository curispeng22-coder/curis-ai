# R3 可信 CEO UsageContext Architecture Review

Issue：`issues/20260717_workspace_r3_trusted_ceo_usage_context_l2_gate.md`  
Security Review：`reviews/20260717_workspace_r3_trusted_ceo_usage_context_security_review.md`  
结论：`BLOCKED_L2`（事实源缺失；给出唯一最小 additive 映射，不实施）。

## 现有事实核对

现有可信身份链是：Gateway `sub/iss` → `tenant_memberships(issuer, subject_id, tenant_id, company_id, role, status, expires_at, revoked_at)` → `TenantContext` 的 `tenant_id/company_id/subject_id/role`。`X-Tenant-Id` 仅选择目标租户，不能形成 CEO 身份。

现有 CEO 相关字段/调用如下：

- `companies.ceo_id` 存在，且 Company 以 `tenant_id` 隔离；Project 以 `projects.tenant_id + project_id` 归属 Company。
- 但 `CompanyProjectRuntime` 创建 Company/默认 Company 时把 `CeoContext.current_ceo_id()` 写入 `companies.ceo_id`；当前 `CeoContext.parse_ceo_from_request()` 直接读取客户端 `X-Ceo-Id`。因此现有 `companies.ceo_id` 不是可信事实源，不能直接用于 UsageEvent。
- Employee、Workflow、StepResult 没有独立可信 CEO 主体字段；Workflow/Result 仅携带 tenant、company、project/run 等资源归属。
- `ResultStore._record_usage_events()` 当前从 `CeoContext.current_ceo_id()` 读取 CEO，缺失即失败，并将其写入 `usage.*` payload 的 `ceo_id`。
- `evolution_events`/UsageEvent 当前已有 `tenant_id` 和 payload 事件投影；不能用客户端 Header、Admin token、默认字符串或仅 tenant 推导 CEO。

## 唯一最小映射方案

不新增身份体系；在现有 `tenant_memberships` 上做 additive 映射，新增必需的服务端字段 `ceo_id`，将其定义为“该主体在该 tenant/company membership 下被批准的 CEO 归属”。唯一键仍由现有 `(issuer, subject_id, tenant_id, company_id)` 约束；同一主体可在不同 Company 有不同 `ceo_id`，但同一活动 membership 只能有一个有效值。

服务端确定性推导：

`verified Gateway (issuer, subject_id)` → 活动且未过期 membership → membership.`tenant_id/company_id/ceo_id` → 校验 `companies(tenant_id, company_id, ceo_id, status='active')` → 当前 Project 必须 `projects(tenant_id, project_id, company_id, status!='archived')` → 派生 `CeoContext`/UsageContext.ceo_id。

`companies.ceo_id`保留为 Company 的一致性投影/资源字段；在映射迁移完成后，服务端只允许它与活动 membership.`ceo_id`一致。客户端 `X-Ceo-Id` 必须由 Gateway 剥离，Workspace 不读取它。

## 缺失、撤销与跨域规则

模型出网前的共享前置校验必须 fail-closed：

- 无可信 subject、无活动 membership、membership `ceo_id` 为空、已撤销、已过期、role 不允许执行：拒绝；
- Company 不存在、非 active、`companies.ceo_id != membership.ceo_id`：拒绝；
- Project 不存在、非当前 tenant/company、已归档或不属于当前 Run：拒绝；
- Workflow/Run/Employee/Capability binding 的 tenant/company/project 不一致：拒绝；
- 客户端伪造 `X-Ceo-Id`、Admin token 或仅 `X-Tenant-Id`：全部忽略并拒绝无法通过服务端校验的请求。

拒绝必须发生在 `ModelGatewayAdapter.execute()` 之前；失败时不得写不完整的成功 UsageEvent。若需要记录拒绝事件，只能写完整脱敏的失败审计，不能写成功模型调用、token 或成本。

## UsageEvent 绑定

现有 `ResultStore._record_usage_events()` 的可信输入改为服务端 `UsageContext`，至少绑定：`ceo_id`、`subject_digest`、`tenant_id`、`company_id`、`project_id`、`workflow_run_id`、`workflow_step_id`、`employee_id`、`capability_binding_id`、`model_gateway_id`、`model_name`、token 字段、`price_version`、`estimated_cost`、status、request id。`ceo_id` 必须来自 membership 映射，不能从 request header 或普通 task payload 获取。

日志只保留不可逆 subject digest、tenant、company/project、ceo_id、结果类别和 request id；不得记录 token、Authorization、Cookie、API key、完整 subject、prompt 或模型原文。

## 迁移、唯一性与回滚

最小迁移仅为 `tenant_memberships.ceo_id` additive 列及现有 Company 一致性校验：

1. 新列无默认 CEO；历史 membership 缺值保持不可执行；
2. 由已批准的服务端迁移输入填充 mapping，并逐行校验对应 active Company；
3. 重复 active mapping、Company 不一致、撤销/过期记录一律阻止启用；
4. 双读期间同时读取 membership.ceo_id 与 companies.ceo_id，任何不一致 fail-closed；
5. 验证通过后切换 UsageContext 读取 membership.ceo_id。

回滚只能回到“仍拒绝缺失 CEO、仍不信任客户端 Header”的上一版本；不得恢复 `CeoContext.parse_ceo_from_request()` 作为 UsageEvent 来源，不得填默认 CEO 或跳过 UsageEvent。无法完成映射时保持 `BLOCKED_L2`。

## 最少文件范围

后续唯一实现 Issue 只允许触及：

- `backend/app/database.py`：`tenant_memberships.ceo_id` additive 迁移与一致性读取；
- `backend/app/identity_membership.py`：AuthorizedMembership 携带服务端 `ceo_id`；
- `backend/app/tenant_context.py` / `backend/app/ceo_context.py`：仅建立可信 UsageContext，移除 Workspace 对客户端 `X-Ceo-Id` 的依赖；
- `backend/app/main.py`：模型出网前统一前置校验与上下文传递；
- `backend/app/result_store.py`：UsageEvent 使用可信 CEO 字段；
- 直接相关 focused tests 与迁移/回滚验证；不改 Provider、Gateway、前端、Admin、计费规则或历史失败 Run/StepResult。

## Focused 验收

不出网测试必须覆盖：合法 subject→membership→tenant/company/project→ceo_id 成功；无 mapping、撤销、过期、角色不匹配、Company 不一致、Project 跨租户/跨公司、Run 不匹配均在 Adapter 调用前拒绝；伪造 `X-Ceo-Id` 无效；Admin token 无法生成 CEO；UsageEvent 字段完整且 `ceo_id` 与 membership 映射一致；日志脱敏；迁移双读不一致阻断启用。

在安全 PASS 与总负责人批准前，不创建新的真实 Run、不注入密钥、不调用模型。

Handoff: sent to 安全边界席复核，并回传产品规划席；当前 R3 保持 `BLOCKED_L2`。
