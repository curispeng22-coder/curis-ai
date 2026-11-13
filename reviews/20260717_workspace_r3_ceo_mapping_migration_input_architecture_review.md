# R3 CEO Mapping Migration Input Architecture Review

Issue：`issues/20260717_workspace_r3_ceo_mapping_migration_input_l2_gate.md`  
结论：`BLOCKED_L2`。

## 核对结果

当前仓内没有能同时证明 `company-a` 与 `membership-quality` 应使用同一个可信、非空 `ceo_id` 的现有事实源。

- 数据模型中，`companies.ceo_id` 是 Company 字段，但历史创建链由 `CeoContext.current_ceo_id()` 写入；该值来自客户端 `X-Ceo-Id` 占位链，不能作为可信迁移输入。
- `tenant_memberships` 已有 `issuer`、`subject_id`、`tenant_id`、`company_id`、状态和生命周期字段；`ceo_id` 是 additive 列，但目标 `quality.sqlite` 当前尚无该列/值。
- `backend/tests/test_workspace_identity_membership.py` 的 `company-a`/`ceo-a` 是测试 fixture，且主体为 `subject-123`、issuer 为测试 issuer；它没有证明生产/质量主体 `membership-quality` 的可信 CEO 归属，不能直接迁移。
- 其他 `ceo-*` 值出现在旧占位测试、客户端 Header 测试或治理 fixture 中，均不是 `membership-quality` 的服务端批准事实源。
- Project/Workflow/Employee 数据只能证明资源归属链，不能独立产生 CEO 身份；仅按 tenant、company 名称或默认 Company 推导均不安全。

因此不能安全给出唯一 `ceo_id`，也不能把 `ceo-a`、测试主体值、默认值、固定值或随机值代作迁移输入。

## 唯一待人工确认输入

总负责人必须单独确认一个非空、不透明的单值 `ceo_id`，并同时确认它属于：

`issuer + subject_id(membership-quality) + tenant_id + company_id(company-a) + active membership`。

该确认必须来自负责人批准记录或受信身份/成员管理事实源，不能来自客户端 Header、Admin token、测试 fixture、默认字符串或仅 tenant 推导。在该单值确认前，本 Issue 保持 `BLOCKED_L2`，不执行迁移。

## 批准后的最小迁移边界

仅允许对目标 `company-a + membership-quality` 做 additive/idempotent 写入：

1. 确认目标 membership 的 issuer、subject、tenant、company、status=active、未过期、未撤销；
2. 确认 `company-a` 存在、属于同一 tenant、active，且 Company/Project 资源链一致；
3. 确认目标唯一 membership 的 `ceo_id` 为空或与人工批准值相同；非空冲突、重复活动映射或 Company 不一致立即停止；
4. 写入同一个批准值，重复执行不得产生第二映射；
5. 双读校验 membership.ceo_id 与 active Company.ceo_id，一致性失败则不启用模型出网。

回滚只能删除/恢复本次目标映射的 additive 变更，并继续 fail-closed；不得恢复客户端 `X-Ceo-Id`、默认 CEO 或跳过 UsageEvent。不得修改其他租户、Company、membership、seed 或历史 Run/StepResult。

## 不出网验证要求

必须覆盖：目标主体映射成功；伪造 `X-Ceo-Id` 无效；无值、撤销、过期、角色不匹配、跨 tenant/company/project、Company 不一致和重复冲突均在 Adapter 前拒绝；UsageEvent 的 `ceo_id` 等于服务端批准值；日志不含 token、Authorization、Cookie、API key、完整 subject 或模型原文。

在人工单值确认、安全 PASS 和总负责人批准前，不修改代码/数据库/seed/fixture，不启动服务，不建 Run，不注入 Key，不调用模型。

Handoff: sent to 安全边界席复核，并回传产品规划席；等待唯一人工单值输入。
