# 共享交接 Issue：Admin Roadmap 占树期间的 Workspace 暂存交接

- **状态**：CLOSED — RETAINED / DO_NOT_APPLY_OR_POP
- **创建人**：eng-seat（Admin 团队 R1/R2 实现）
- **日期**：2026-07-17
- **涉及分支**：`feat/roadmap-r1r2`（Admin） / `feat/093-readonly-catalog-routes`（Workspace）

## 背景

Admin 团队实现 R1/R2 自主代码项（A–E）前，工作树存在 **Workspace 团队未提交的在途改动**（tenant 身份/成员/作用域等）。
为遵守「部署隔离纪律」（不碰 Workspace 代码、不抢提交、保持干净树以建分支 + cherry-pick 093），
eng-seat 经 team-lead 批准，采用 **非破坏性、可完整回退** 的 `git stash -u` 将这些在途改动暂存。

## 暂存快照（stash）

- **stash 哈希**：`348b68800cfdfa23129ff2a0c139aee2ae669338`
- **来源分支上下文**：`feat/093-readonly-catalog-routes`
- **stash 描述**：`WIP: workspace in-progress shared-backend changes (tenant identity/membership/scope), stashed by Admin roadmap to unblock clean tree`

### stash 内文件清单（`git stash show --name-only`）

```
.workbuddy/memory/2026-07-17.md
backend/app/database.py
backend/app/department_catalog.py
backend/app/main.py
backend/app/tenant_context.py
backend/tests/conftest.py
data/sample_publish_package.md
```

## ⚠️ 当前工作树状态（恢复前必读）

自 stash 创建以来，**Workspace 团队已继续推进工作**，当前工作树中已重新出现（并新增了）Workspace 相关文件，且其中**部分不在上述 stash 清单内**，例如：

- `backend/app/identity_membership.py`（untracked，新增）
- `backend/app/resource_scope_policy.py`（untracked，新增）
- `backend/tests/test_workspace_identity_membership.py`（untracked，新增）
- `deploy/curis/gateway/`（untracked，新增目录）
- `issues/20260717_workspace_tenant_identity_membership_implementation.md`（untracked，新增）
- `reviews/20260717_workspace_tenant_identity_membership_implementation_review.md`（untracked，新增）
- `reviews/20260717_workspace_tenant_identity_membership_implementation_security_boundary_review.md`（untracked，新增）
- `deploy/curis/README.md`、`release-checklist.md`、`verify-isolation.sh`、`workspace.env.example`（modified）
- `knowledge/NOW.md`（modified）
- `backend/app/tenant_context.py`、`backend/tests/conftest.py`、`data/sample_publish_package.md`（modified）

**结论**：该 stash 已是**部分/较早的快照**，不能完整代表 Workspace 当前在途状态。
请勿直接 `git stash pop` 到当前工作树——会造成重复/冲突。

## 恢复建议（Workspace 团队）

1. 先 `git stash list` 确认 `348b688…` 仍在。
2. 在 **Workspace 自己的分支 / 干净工作树** 上恢复，而非 Admin 的 `feat/roadmap-r1r2`：
   - 预览：`git stash show -p 348b68800cfdfa23129ff2a0c139aee2ae669338`
   - 应用（保留 stash 以便核对）：`git stash apply 348b68800cfdfa23129ff2a0c139aee2ae669338`
   - 或直接弹出：`git stash pop 348b68800cfdfa23129ff2a0c139aee2ae669338`
3. 恢复后与当前已在途的 Workspace 新增文件做 **人工合并/去重**，尤其 `backend/app/main.py`
   的 tenant 作用域中间件（`_tenant_scope_middleware`）——该段代码当前在 stash 内，
   但 Admin 分支的 `main.py` 已重置为干净基线并仅含 Admin 的 R1/R2 改动（无 Workspace 中间件代码）。

## Admin 分支纪律确认

- `feat/roadmap-r1r2` 的提交仅包含 Admin R1/R2 改动：
  - `d7c0b21` `[Shared]` main.py 令牌门禁修复 + Tool/Workflow 只读目录路由
  - `019217d` `[Admin]` database.py Tool/Workflow 能力态列 + list 辅助
  - `d9157c9` `[Admin]` 令牌策略 + 实例化证据 pytest
- **未将任何 Workspace 文件纳入提交**；Workspace 在途改动仍保留为未提交状态（见上）。
- **eng-seat 未执行 `git stash pop`**（按 team-lead 护栏，由 Workspace 团队自行恢复）。
- `main.py` 为 Shared 代码，令牌修复与目录路由需 **Shared 双确认**（见 draft PR 说明）。

## 关闭条件

Workspace 团队确认其 tenant 身份/成员/作用域在途改动已妥善恢复并合并后，本 Issue 方可关闭。

## 总负责人最终处置（2026-07-17）

- PR #2 已保留在 `72186d5843106554c759f647b7998f1adf31406a`。
- stash `348b68800cfdfa23129ff2a0c139aee2ae669338` 不恢复、不 apply、不 pop；保留只作历史核对。
- 当前身份、membership、TenantContext 与 scope 已由独立 L2 Issue、Review 和合入提交覆盖，不再以恢复旧 stash 作为交付动作。
- 本处置取代上文早期“恢复建议”；不得据此宣称 stash 内容已恢复。
- 追溯 Review：`reviews/20260717_pr2_post_merge_scope_governance_review.md`。

恢复待办已被明确取消且边界已记录，本交接 Issue 关闭。
