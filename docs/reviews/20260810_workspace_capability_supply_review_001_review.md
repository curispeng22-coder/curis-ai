# WORKSPACE-CAPABILITY-SUPPLY-REVIEW-001 Review

Status: Review  
Decision: `PASS_WORKSPACE_CAPABILITY_SUPPLY_REVIEW_WITH_APPROVAL_GATE`  
Date: 2026-08-10

## 结论

PASS。当前 `ORG-001 PASSED / PASS` 的 Workspace 可由 CEO 为完整 `requirement:*`
集合选择真实 active official 或当前 Tenant private Company Capability，并获得 availability、
permission、risk、cost 四维 Resource Check。选择与审查结果持久化在现有 Capability Binding
proposal 中；目录失效或 metadata 漂移时读取立即 fail-closed，重新核对前不能进入批准。

本 Review 只放行 Resource Check。即使 `resourceCheckPassed=true / readyForApproval=true`，
响应仍固定 `activationReady=false`；Binding 保持 `PROPOSED / PROPOSED_NOT_AUTHORIZED`，
没有 CEO Approve、授权、激活或 Operate 命令。

## 实际改动文件

- `backend/app/runtime/workspace.py`
- `backend/app/api/runtime_foundation_router.py`
- `backend/tests/test_runtime_workspace_foundation.py`
- `frontend/lib/runtimeApi.js`
- `frontend/app/ceo-office/page.js`
- `frontend/tests/runtimeApi.test.mjs`
- `frontend/tests/runtimeWorkspaceUi.test.mjs`
- Issue、本文、`CURRENT_STATE.md`、`CHANGE_LOG.md`

未修改 Schema / Migration、状态机 Registry、Capability Catalog 写路径、旧 Project / Task /
Workflow 链、活动数据库、Blueprint、导航、Desktop、平台 API、凭证或激活命令。

## Runtime 与安全证据

- 服务端从当前 Blueprint 与 Capability Binding 双向核对完整 requirement 集合；少选、重复、
  伪造来源 / 类型 / ID、跨 Tenant、Binding 缺失或版本漂移整体拒绝，不产生部分更新。
- 供给只接受 active official metadata 或当前 Tenant active private metadata。响应与持久化只包含
  白名单结论，不返回或保存 `credential_ref`、token、api_key、secret 或 private metadata。
- Catalog `live_status`、运行配置、权限 scope 与单位成本由服务端形成 blocker；目录 `updated_at`
  改变后标记 `SUPPLY_CHANGED_REVIEW_REQUIRED`，停用 / 启动裁剪后标记
  `SUPPLY_UNAVAILABLE_OR_CHANGED`。
- 本地 `CURIS_PRODUCT=workspace` 启动会按既有边界裁剪自定义 official rows，只保留批准的 R3
  Model；浏览器最终证据因此使用可重启恢复的 tenant-private Company Capability。该既有启动行为
  未进入本 Issue，official 选择在被裁剪后会被本 Resource Check 正确锁定。

## 自动验证

```text
Backend Runtime focused tests: 15 passed
Python compile: PASS
Frontend Runtime focused tests: 16 passed
Scoped ESLint: PASS
Next production build: PASS, 44/44 static pages
```

Backend 覆盖：完整选择、混合 official / tenant-private 供给、幂等、重启恢复、目录停用漂移、
跨 Tenant、缺少 Binding、原子失败、秘密不投影，以及 Proposal / Workspace 状态不变。

## 浏览器与临时 SQLite 验收

Codex In-app Browser，`http://localhost:3000/ceo-office`：

- 临时数据库：`/tmp/curis-capability-supply.TvUFjP/curis.sqlite`
- Workspace：`workspace-8acf6e94-1ab9-423c-84a9-4608b9174cc7`
- 前置 Simulation：`simulation-57a2b3d9-ec62-4e19-b1c8-97bb9519acfc`，
  `PASSED / PASS / invalidated_at=null`
- 初始 0/2 未选择；选择缺少 permission scope 的供给后显示“仍有 1 类阻塞”。
- Catalog metadata 改变后保持阻塞，CEO 明确“重新核对供给”后才变为
  “供给齐备 · 未授权”。
- 最终改用 2 个 tenant-private Company Capability；Backend 重启和页面重载恢复同一选择与
  `reviewComplete=true / resourceCheckPassed=true / readyForApproval=true /
  activationReady=false`。
- SQLite `integrity_check=ok`；Workspace `DRAFT / simulation_passed=0 /
  operating_version=0`；2 Role Slot 均 `DRAFT`，2 AI Employee 与 2 Capability Binding 均
  `PROPOSED`；已授权数量仍为 0。

视觉证据：

- `/tmp/curis-workspace-capability-supply-evidence/resource-check-passed-not-authorized.jpg`

活动 `data/curis.sqlite` 未作为写目标，SHA-256 保持
`884b2adeba5a61fb3bce68ddcf6d81b1453a730fb5df8740678537fe363d7662`。

## 仍未完成

1. 独立 Issue 定义 CEO Approval / Modify / Reject，必须再次核对当前 Blueprint、orgVersion、
   未失效 `ORG-001 PASS` 与当前 `resourceCheckPassed`。
2. 独立原子激活 / 回滚命令同步处理 Role Slot 分配、AI Employee lifecycle、Capability Binding
   授权和 Workspace operating version；任一失败整体回滚。
3. 激活后仍需真实工作项、执行、Evidence、Acceptance、Decision、失败恢复与回滚 Simulation，
   不能以 Resource Check 或页面状态替代 Business Runtime 完成。

