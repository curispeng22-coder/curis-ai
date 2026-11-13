# WORKSPACE-CAPABILITY-SUPPLY-REVIEW-001

Status: Completed  
Decision: `PASS_WORKSPACE_CAPABILITY_SUPPLY_REVIEW_WITH_APPROVAL_GATE`

## 1. 目的

在已通过 `ORG-001` 的 Workspace 候选组织上完成真实 Company Capability 供给审查：
CEO 为每个 `requirement:*` 选择当前可查询的 official 或 tenant-private Capability，Runtime
持久化供给来源、类型、可用性、权限、风险和成本门禁；任何缺口都必须阻止后续激活。

本 Issue 只完成 Resource Check，不授权 Role Slot、AI Employee、Capability Binding 或
Workspace，不提供 Approve / Operate 命令。

## 2. 前置契约

- Workspace 必须是当前 Tenant / Company 下的 `STUDIO_DRAFT`，Blueprint 与 orgVersion 当前有效。
- 当前 Workspace 必须存在未失效的 `ORG-001 PASSED / PASS`。
- 供给只能来自现有 Company Capability 目录：active official metadata 或当前 Tenant active
  private metadata；不读取、不返回、不持久化凭证值。
- CEO 选择只证明供给对应关系，不等于授权。Model 的成本上限、Connector 的连接配置、
  write / external effect 的权限范围缺失时必须返回明确 blocker。

## 3. 允许文件

- `backend/app/runtime/workspace.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_workspace_foundation.py`
- `frontend/lib/runtimeApi.js`
- `frontend/app/ceo-office/page.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- `issues/20260810_workspace_capability_supply_review_001.md`
- `docs/reviews/20260810_workspace_capability_supply_review_001_review.md`
- `docs/00_Context/CURRENT_STATE.md`
- `docs/08_Change_Log/CHANGE_LOG.md`

不得修改 Schema / Migration、状态机 Registry、Capability Catalog 写路径、旧 Project / Task /
Workflow 链、活动 `data/curis.sqlite`、Blueprint、导航、Desktop、平台 API、凭证或任何激活命令。

## 4. 验收条件

1. Runtime 从当前 Blueprint / Capability Binding 推导完整 `requirement:*` 集合；客户端少选、
   多选、重复、伪造来源 / 类型 / ID、跨 Tenant 或过期供给时整体失败，不产生部分更新。
2. 每项选择由服务端核对 active official / tenant-private metadata；响应与持久化只包含白名单
   metadata，不含 credential、token、api_key、secret 或私有 metadata。
3. 每个 Binding 持久化供给选择与四维审查：availability、permission、risk、cost；任何
   runtime config、成本上限或高影响权限缺口形成 blocker，不能伪造 `activationReady=true`。
4. 重试幂等、重启恢复；供给目录漂移后再次读取时 fail-closed 标记 stale / blocked。
5. Binding 保持 `PROPOSED / PROPOSED_NOT_AUTHORIZED`，Workspace 保持 `DRAFT /
   simulation_passed=0`，岗位和员工状态不变。
6. CEO Desk 只在 `ORG-001 PASS` 后显示真实供给选择与审查结果；明确“已审查不等于已授权”，
   不新增 Agent Center、第三栏或激活按钮。
7. Backend / Frontend 聚焦测试、scoped ESLint、Next build、临时 SQLite 重启与浏览器验收通过。
