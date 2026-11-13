# Shared `backend/app/main.py` 逐 hunk 语义合并清单

Issue：`issues/shared/20260717_workspace_shared_main_manual_merge_preparation.md`  
对比对象：当前分支 `8f426be9`、stash `348b68800cfdfa23129ff2a0c139aee2ae669338`、PR #2 commit `d7c0b21`。  
操作：只读；未 apply、未 pop、未 cherry-pick、未改代码。

## 结论

`backend/app/main.py` 存在 Shared 语义重叠，但不是互斥架构：Admin token 门禁与 Workspace IdentityMembership/ResourceScopePolicy/TenantContext 可共存，必须人工融合。PR #2 保持 Draft；本清单 PASS 仅表示可进入人工合并准备，不表示可合并或发布。

## 逐 hunk 清单

| Hunk | 位置/内容 | 决策 | 执行要求 |
| --- | --- | --- | --- |
| H1 | imports：PR 新增 `sys`；stash 新增 IdentityMembership、ResourceScopePolicy imports | 人工融合 | 保留四个 import；不得删除 IdentityMembership、ResourceScopePolicy。 |
| H2 | `create_app()` 初始化区 | 人工融合 | 保留 PR 的 Admin token 配置态与 strict fail-closed；同时保留 stash 的 IdentityMembership 配置校验和 ResourceScopePolicy。顺序为 DB → 边界校验/策略对象 → prune → services。 |
| H3 | `_tenant_scope_middleware` | 采用 stash，且与当前 product middleware 联查 | Workspace `/api/*` 走 membership → resource scope → TenantContext；Admin 继续走 Admin 隔离路径。不得保留 `X-Tenant-Id` 单独授权，不得让 Admin token 成为 Workspace 身份。 |
| H4 | PR 的 `PLATFORM_ADMIN_TOKEN` 旧默认逻辑 | 采用 Admin | 保留 `CURIS_PLATFORM_ADMIN_TOKEN` 与兼容变量；未配置统一 401，`ADMIN_STRICT=true` 拒启动；不得恢复 `platform-admin-dev`。该 token 仅供 Admin `/api/platform/*` 门禁。 |
| H5 | PR 新增 `/api/platform/tools`、`/api/platform/workflows` | 采用 Admin | 保留两个 GET 只读路由及 Admin token 门禁；不得变为 Workspace identity 路由。 |
| H6 | PR 的 `/api/catalog/*` 邻接区域 | 保留当前 | 不重排、复制或改变既有 Workspace Catalog 路径；继续受 product/membership 边界约束。 |
| H7 | PR 的 stderr warning | 采用 Admin，人工检查 | 可保留非秘密告警；不得输出 token、Authorization 或环境变量值。 |

## 明确丢弃项

- 丢弃 PR 的 `platform-admin-dev` 默认弱口令行为。
- 丢弃 stash 中把 `X-Tenant-Id` 作为无成员请求兜底授权的旧分支；仅保留身份、成员、资源策略语义。
- 丢弃整 stash 自动带入的 `.workbuddy/memory/2026-07-17.md`、`data/sample_publish_package.md`。

## 系统交付可执行的最小文件范围

第一步只处理 `backend/app/main.py`，按 H1–H7 人工融合；禁止整 stash、整 PR 合入。

只核对已存在的依赖，不从 stash 盲目覆盖：`backend/app/identity_membership.py`、`backend/app/resource_scope_policy.py`、`backend/app/tenant_context.py`、`backend/app/database.py`、`backend/app/department_catalog.py`、`backend/app/result_store.py`、`backend/app/tool_executor.py`、`backend/app/workflow_runtime.py`。

最小测试范围：`backend/tests/test_admin_token_policy.py`、`backend/tests/test_issue093_readonly_catalog_routes.py`、`backend/tests/test_workspace_identity_membership.py`、`backend/tests/test_d1_impl_multitenant.py`、`backend/tests/test_model_gateway_adapter.py`。

系统交付不得在本准备 Issue 修改数据库、前端、Admin 业务逻辑或执行 `stash pop/cherry-pick`。依赖文件缺失或接口不匹配时停止并回报唯一阻塞。

## 验收门槛

必须证明 Admin token 门禁、Workspace IdentityMembership/ResourceScopePolicy/TenantContext、两个 Admin 只读 Catalog 路由均保持有效；Admin token 不能作为 Workspace 身份；跨租户规则不被覆盖。

结论：`PASS`（合并准备边界）。PR 仍 Draft，合并与发布需后续系统交付/质量证据。

Handoff: sent to 产品规划席；下一席为系统交付席。
