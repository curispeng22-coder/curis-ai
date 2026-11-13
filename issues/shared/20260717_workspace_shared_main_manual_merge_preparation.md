# Shared main.py 逐 hunk 人工合并准备

- 日期：2026-07-17
- 状态：DUAL_LEAD_PASS — WAITING_ADMIN_MERGE_AND_WORKSPACE_REBASE
- 总负责人决策：安全边界席已 PASS，批准进入逐文件、逐 hunk 语义合入流程；不批准整 stash、整 PR、直接合并或 `stash pop`
- 优先文件：`backend/app/main.py`
- PR：#2，继续保持 Draft
- Owner：产品规划席编排；架构边界席 → 安全边界席 → 系统交付席 → 质量运行席

## 目标

在不覆盖当前 Workspace 已验证实现的前提下，为 Shared `backend/app/main.py` 形成可审计的逐 hunk 合并结果，必须同时保留：

1. Admin token 门禁；
2. Workspace `IdentityMembership`；
3. Workspace `ResourceScopePolicy`；
4. Workspace `TenantContext`；
5. 六条 Catalog 只读路由。

Admin token 只用于 `/api/platform/*` Admin 边界，不得被解释为 Workspace 身份、成员凭据或租户授权。

## 禁止操作

- 禁止 `git stash pop`、整 stash apply、整 PR 合并或整提交 cherry-pick。
- 禁止直接修改或关闭 PR #2 的 Draft 状态。
- 禁止覆盖当前租户身份、成员授权、受信 Gateway 和资源作用域实现。
- 禁止把 Admin token 传入 Workspace 身份链或作为兼容 Header。
- 禁止顺带修改前端、模型、Workflow、Billing、Marketplace 或其他文件。

## 执行顺序

1. 架构边界席只读比较当前 `main.py`、stash `348b68800cfdfa23129ff2a0c139aee2ae669338` 与 PR #2，逐 hunk 标记 `保留当前 / 采用 Admin / 人工融合 / 丢弃过时`，不得改代码。
2. 安全边界席确认受信 Gateway、活动 membership、资源作用域、兼容 Header 和 Admin token 边界没有混用或降级。**已 PASS。**
3. 系统交付席只按已通过的 hunk 清单准备最小改动和 focused tests，不合并 PR。
4. 质量运行席只运行 Shared / Admin / Workspace 聚焦集，确认三条语义链同时成立并形成 Review。
5. 产品规划席根据 Review 提交 Admin + Workspace 双 lead 最终合入确认；在双 lead 确认前 PR #2 继续 Draft，本 Issue 本身不授权直接合并。

## 验收标准

- 有逐 hunk 决策清单，能追溯来源和去留原因。
- `/api/platform/*` 缺失或错误 Admin token 均拒绝。
- Workspace 无可信身份为 401，无活动成员或越权为 403，跨租户资源为 404。
- 客户端伪造 Gateway / tenant / identity Header 不能获得身份或越权。
- 六条 Catalog 只读路由保持真实数据、正确鉴权和租户边界。
- Shared、Admin、Workspace focused tests 全部通过且没有新增失败。
- PR #2 仍为 Draft；没有执行整 stash、整 PR 或直接合并。

## 预期交接

每席只回传其负责的唯一产物；未收到预期结果时才审查。最终由产品规划席统一向总负责人和 Admin 团队回传。

## 实际收口证据

- 架构 Review：`reviews/20260717_workspace_shared_main_manual_merge_preparation_review.md`，逐 hunk 边界 PASS。
- 固定起点：HEAD `8f426be9`，`backend/app/main.py` blob `0fa34bc6`。
- 当前 `main.py` 已同时保留 Admin token 门禁、六条 Catalog 路由、Workspace membership、`TenantContext` 和资源作用域；旧 `X-Tenant-Id` 单独授权语义不采用。
- Shared / Admin / Workspace 聚焦测试：`32 passed`；`git diff --check` 通过。
- 未执行 stash apply/pop、cherry-pick、文件修改或 PR 合并；PR #2 继续保持 Draft。
- 下一步只需 Admin + Workspace 双 lead 确认是否以当前语义融合结果作为合入基线。
- Workspace lead：**PASS**。逐 hunk 语义、身份边界、32 focused tests 与 diff-check 均满足。
- Admin lead：**PASS**。
- 双 lead 已闭环。由 Admin lead 在干净树执行 PR #2 合入；合入后 Workspace 基于 Admin rebase，并只核对共享 `main.py` 语义与既有 focused tests。
- Stash `348b68800cfdfa23129ff2a0c139aee2ae669338` 继续按去重清单处理，禁止直接 `pop`。
