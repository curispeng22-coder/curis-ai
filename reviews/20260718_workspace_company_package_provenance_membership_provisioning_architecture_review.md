# 同源隔离链 Membership + CEO 一次性 Provisioning 架构 Review

- Issue：`issues/20260718_workspace_company_package_provenance_isolated_setup.md`
- 结论：`PASS`（仅批准一次性受控 provisioning 契约；不代表已写库、Setup 完成或真实模型执行放行）
- 复核范围：`tenant_memberships` 的可信 membership 与 Company CEO 映射
- 数据库：仅 `deploy/curis/gateway/.generated/data/quality.sqlite`

## 裁决

现有栈没有获批的 membership 创建/撤销或 Company CEO 绑定 API；可以批准一次性、additive、幂等、事务化的受控写入，但只能由停机状态下的系统交付席执行。该写入不是公开 API，不接受 Admin token、客户端 Header、默认 CEO 或 self-use 身份。

除本 Review 明确列出的三类新记录外，不得写任何数据。若任一前置检查、唯一性检查或审计写入失败，整个事务回滚并保持 `BLOCKED_L2`。

## 固定输入

- 实际数据库：绝对路径必须为 `/Users/yy/Documents/Curis AI Workspace/deploy/curis/gateway/.generated/data/quality.sqlite`；不得读取、合并或复制 `data/curis.sqlite`。
- 可信身份：`issuer=https://quality.issuer.local`、`subject_id=quality-member-sub`。这对值只来自既有受信 membership 事实，不从请求 Header 取得。
- 新 ID：执行时生成全新的不透明 `tenant_id`、`company_id`、`ceo_id`、`membership_id`；不得复用 `selfuse`、`tenant-a`、`tenant-b`、`company-a`、历史 CEO 或历史 membership。
- 固定 Company 来源快照：`ccp_ai_software_company@1.0.0`、`bridge.ccp_ai_software_company.1.0.0.software_rnd_sop.1.0.0`、`official.workflow.software_rnd_sop@1.0.0`。三者必须已在同一实际数据库中各自唯一、active、版本一致；否则不写。

## 唯一写入契约

1. 服务、Gateway、Admin、Workspace、Worker 和所有监听端口全部停止；执行者只打开 SQLite 文件，不启动应用，不使用 API，不读取凭据。
2. 先以只读查询确认固定 Package/Bridge/Workflow 来源链、目标 ID 不存在、目标 tenant/company/membership 没有任何同源记录，且同一 `issuer + subject_id` 没有目标租户的既有 membership。
3. 生成一个固定本次操作的 `provisioning_id` 与幂等键；重试只能按该幂等键读取并逐字段核对已完成记录，不能生成第二组 ID。幂等命中但任一字段不一致即停止。
4. 使用同一 SQLite 连接 `BEGIN IMMEDIATE`，仅按以下顺序写入：
   - 一条 `tenants`：新 `tenant_id`、active；
   - 一条 `companies`：新 `company_id`、新 tenant、`ceo_id` 为新 CEO、active，并固化上述五个来源字段（含 `created_from_template_id=ct_ai_software_company`），使后续既有 Package 实例化路径只能复用这家公司；
   - 一条 `tenant_memberships`：新 `membership_id`、固定 issuer/subject、新 tenant、新 company、新 CEO、`role=owner`、`status=active`，`expires_at`/`revoked_at` 为空。
5. 在同一事务追加一条 `evolution_events` provisioning 审计事件，使用相同幂等键；只记录 operation、provisioning_id、tenant/company/membership/ceo ID、issuer、subject_digest、source package/version、bridge、workflow/version、status 和 timestamp，不记录 subject 原值、Token、Cookie、Authorization、Key 或任何凭据。
6. 逐项回读并确认三条新记录唯一、active、CEO/Company/membership 完全同值后提交；提交失败、冲突、重复、来源漂移、审计失败或回读不一致均 `ROLLBACK`。

## 唯一性与禁止规则

- `tenant_id`、`company_id`、`ceo_id`、`membership_id` 必须全库不存在后再写；任何碰撞停止。
- 只允许一条新 active membership 和一条新 active Company 映射；不修改 `company-a`、`tenant-a`、`tenant-b`、历史 membership/CEO/Run/Usage。
- 不接受 `X-Tenant-Id`、`X-Ceo-Id`、Gateway Header、Admin token、默认值、固定 CEO、同名匹配、latest/default 推断或跨库补值。
- 不新增公开写 API，不改变身份实现、撤销逻辑、模型/网关/成本/前端或运行权限。

## 回滚与后续边界

- 事务提交前的任一异常：回滚三类记录及审计事件，确认目标 ID 计数为零。
- 提交后的取消只能对本次 provisioning_id 识别出的新 membership/company/tenant 做受控 revoke/inactive 补偿；不得删除审计或触碰历史数据。无法精确识别时保持阻塞。
- 本契约只产生可信 identity→membership→Company 前置事实；随后仍须经同一数据库的 Package 实例化、6 Binding、Project、Task、pending Run 和质量无出网 Review。它不授权 `run-next-step`、模型出网或凭据注入。

## 复核要求

质量席停机只读核对：同库路径、幂等事件、三条新记录唯一性、CEO 同值、历史零变更、冲突回滚、跨租户拒绝以及 `outbound_attempted=0`。证据写入 `reviews/20260718_workspace_company_provenance_isolated_setup_review.md`。

Handoff: sent to 总控决策席
