# Workspace D1 selfuse 可信 Owner / CEO 身份 Gate 安全 Review

- Issue：`issues/20260718_workspace_d1_selfuse_trusted_identity_gate.md`
- 结论：`BLOCKED_L2`（当前没有可信 selfuse membership；建议唯一继续路径为一次性受控 provisioning）
- 范围：只读安全裁决；未启动、未注Key、未调用模型、未读写 D1 目标

## 唯一建议

选择一次性、事务化、不可公开调用的 `selfuse` trusted provisioning；不改 D1 scope。改变固定 scope 会扩大身份边界并需要重新完成完整安全与质量预检，本 Issue 不提出该路径。

## 必须固定的可信链

`受信 Gateway issuer + subject → active tenant_memberships → tenant_id=selfuse → company_id → role=owner（单条）→ 非空 ceo_id → active Company.ceo_id 同值`

- `issuer`、`subject` 必须来自已批准的受信 Gateway 事实，不由请求 Header、Admin token、默认主体或执行者临时填写；当前尚缺这条精确 selfuse 映射的正式批准证据。
- 运行时必须使用 gateway 身份模式；不得使用现有 `selfuse` / `test` 身份适配器。现有 selfuse 适配器返回合成 owner 且 `ceo_id` 为空，不能作为可信生产授权。
- `X-Tenant-Id` 只能选择查询目标，不能单独授权；角色、company、CEO 均由服务端 membership/Company 读取并一致性校验。

## 一次性 provisioning 契约

1. 目标只能是当前 D1 实际执行库中的 `selfuse` 租户；禁止读取、拼接或复制其他数据库，禁止修改历史 tenant-a、membership、Company、Run、Usage 或 D1 文件。
2. 服务、Gateway、Admin、Workspace、Worker 与监听端口全部关闭；不使用公开 API、Header、Admin token、模型、网络或凭据值。HMAC 审计 key 只检查存在，缺失立即停止且不读取或输出值。
3. 由受控命令服务端生成新的不透明 `provisioning_id`、`company_id`、`ceo_id`、`membership_id`；不得使用默认值、同名推断、历史 CEO 或历史 membership。`selfuse` tenant 必须已存在且唯一，否则回滚并保持阻塞。
4. 使用同一 SQLite 连接 `BEGIN IMMEDIATE`。先只读确认目标记录不存在、同一 issuer+subject 在 selfuse 无冲突 membership、无重复 active Company 映射；然后最多新增一条 active Company 和一条 active owner membership，二者 tenant/company/ceo_id 精确一致。
5. 使用固定 `operation_id`/幂等键。重复执行只能逐字段返回同一已完成映射；任一部分缺失、重复、字段不一致、撤销/过期、CEO 不一致或写入计数异常，均整体拒绝，不生成第二组 ID。
6. 同一事务追加一条脱敏审计事件；审计失败、回读失败、唯一性失败或提交异常均 `ROLLBACK`。提交后若发现异常，只允许按该 operation_id 对本次新记录做精确 revoke/inactive 补偿，不删除审计、不碰历史记录。

## 审计与 fail-closed

审计仅允许 `operation_id`、`tenant_id=selfuse`、新 `company_id`/`ceo_id`/`membership_id`、`role`、`subject_digest`、`outcome`、`reason`、时间戳；禁止 subject 原文、Authorization、Cookie、JWT、Header 原文、Key、Token、数据库串和凭据。

任何缺少可信 issuer/subject、无 active membership、role 不为 owner/ceo、ceo_id 为空、Company 不存在/非 active/CEO 不同、跨 tenant、重复或撤销状态，均在 D1 claim 前 fail-closed，保证零 claim、零模型、零 Tool、零 D1 写入。

## 后续验收边界

总控批准该唯一 provisioning 契约后，系统交付席才可建立受控实施 Issue；质量席必须在停机、无出网条件下核对同库、唯一性、CEO 同值、幂等重放、冲突回滚、跨 tenant 拒绝和脱敏审计。Provisioning PASS 不授权 D1 模型调用、Key 注入或工具链执行；后续仍须重新通过 D1 运行 Gate。

## 唯一当前缺口

仓内现有证据只证明 `selfuse` 缺少符合条件的可信 membership，不能证明可用于 selfuse 的已批准 issuer+subject 映射。因此当前保持 `BLOCKED_L2`，不得用 tenant-a、客户端 Header、默认身份或 Admin token 替代。

Next Seat：产品规划席
Handoff: sent to 产品规划席
