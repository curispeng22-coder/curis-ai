# 补只读 Catalog/Platform GET 路由

状态：VERIFIED/CLOSED — POST_MERGE_TRACE
类型：[Admin][Fix]
发起团队：Admin（产品规划席 齐活林）
归属模块：Admin 目录接口
是否阻塞：否
是否触发 L2：否
共享后端：是（改 `backend/app/main.py`，须 Admin+Workspace 双确认后合入）

## 结论
补资产复盘发现的缺失只读 GET 路由，使 `persona` / `dashboard` / `company_package` / `company_template` 可被 Admin 只读消费（当前仅 POST，无 list 路由）。

## 真实证据
- `persona_templates`：仅 `POST /api/platform/personas` (main.py:1750)，无 GET list。
- `dashboard_templates`：仅 `POST /api/platform/dashboards` (main.py:1758)，无 GET list（仅经 `/api/ceo/overview` 消费）。
- `company_packages`：仅 `POST` + `/instantiate`，无 GET list。
- `company_templates`：仅 `POST`，无 GET。

## 修改内容
- 新增 `GET /api/platform/personas`（或 `/api/catalog/personas`）
- 新增 `GET /api/platform/dashboards`（只读投影）
- 新增 `GET /api/platform/company-packages`
- 新增 `GET /api/platform/company-templates`
（路由仅只读投影，复用现有 catalog 路由风格；不改写逻辑）

## 注意（九节纪律第七节）
此改 `backend/app/main.py` 属 Shared 区，须 Admin 与 Workspace 双方确认后合入。先建内部 Issue，提交前走双确认；不自行强推。

## 验收方式
- 各 GET 返回 200 + 真实行；QA 加接口测试断言行数 > 0。

## 任务分解
- T1 路由设计（架构师，复用 catalog 风格）
- T2 实现（工程师，寇豆码）
- T3 QA 测试（严过关）

## 合入后追溯验收（2026-07-17）

- 实现提交：`f6e020e8f3597cbd11c62d47a22aa19136db85da`；Shared 语义补件：`d7c0b21bea30487d71613dc4e2039da57944f065`。
- 合入修订：`72186d5843106554c759f647b7998f1adf31406a`。
- 自动测试：`backend/tests/test_issue093_readonly_catalog_routes.py` 覆盖四条 GET 的 200、真实种子行、无/错令牌 401；该测试已纳入合入前 Shared/Admin/Workspace focused 集。
- 运行证据：`reviews/20260717_workspace_r2_asset_instantiation_closure_review.md` 已记录 Catalog 200、无令牌 401、跨租户 403，R2 聚焦 66 passed、全量 603 passed / 19 failed。
- 追溯 Review：`reviews/20260717_pr2_post_merge_scope_governance_review.md`。

本结论是合入后的证据追溯，不伪装为提交前独立 Review。现有验收条件已满足，本 Issue 关闭。
