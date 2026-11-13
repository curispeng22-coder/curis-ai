# Business Department Organization Model Review

Issue: `issues/20260729_business_department_org_model.md`

Status: `PASS（实现、迁移与回归） / BLOCKED_L2（真实成果正向 Browser 证据）`

## 结论

业务部门组织模型的代码、迁移、自动化回归、官方启动与 Desktop/Mobile 信息架构验收通过：

`Local Owner → 业务部门 → 员工 / 项目 → Task → 成果`

当前主库的 8 个 Project 均有可解析的业务部门；其中 5 个历史 Project 已迁移到各自 tenant/company 下的“待归属业务部”。新建 Project 强制选择业务部门，Task 仍从 Project 创建，真实 Artifact 强制关联 `task_id`，跨 tenant 查询保持隔离。认证文件与 Local Owner 行为无本 Issue 增量。

但不能宣告完整 Browser 正向成果链通过：官方本地环境未配置 Model Gateway，质量席通过 UI 创建的真实 Task 执行失败；同时主库不存在可供迁移的 `COMPLETED + 非空 output` 历史 Task。因此浏览器只能证明失败 Task 不生成伪成果，不能展示一个真实成功 Artifact。自动化测试已覆盖成功 Task 自动登记 Artifact、按 Task/Project 查询、幂等迁移与租户隔离，但不能替代要求的真实 Browser 正向证据。

## 证据

### 来源与范围

- HEAD：`051b1af6ea810f57d1e67ad6d7e89e8ef0a1e42f`
- 数据库：`data/curis.sqlite`
- 当前 Local Owner tenant：`local-tenant-447e9ae9-9e30-477e-8ad0-73db68397ba4`
- 共享工作树存在 Issue 外既有改动；本 Review 仅核验 Issue Allowed Files。
- `git diff --check`：PASS。
- 认证边界复核：Google OIDC、Local Owner、JWT/trusted gateway、启动脚本、登录与 Onboarding 文件相对 HEAD 无本 Issue 增量。

### Backend

- 最终命令：`.venv/bin/python -m pytest backend/tests`
- 最终结果：`1158 passed, 2 skipped`，耗时 `118.66s`。
- `backend/tests/test_business_department_org_model.py`：`3 passed`。
- 覆盖：
  - Project 创建缺少 `department_id` 被拒绝，更新不能清空；
  - 历史空部门 Project 幂等归入“待归属业务部”；
  - `COMPLETED + 非空 output` 历史 Task 幂等迁移为一个 `task.output` Artifact；
  - 新成功 Task 自动登记 Artifact；
  - Artifact 可按 Task 与 Project 查询；
  - 跨 tenant 查询返回 `404`；
  - 无法确认 `task_id` 的旧内容包不冒充成果。
- 候选稳定过程曾发现并修复两类回归：
  - 旧测试 fixture 创建 Project 未传 `department_id`；
  - D1 旧 schema 的 `tasks` 表无 `output` 列时，成果迁移查询失败。
- 最终候选已补齐 fixture，并在统一 schema 兼容点先确保 `tasks.output`；最终全量全绿。

### Frontend

- Frontend tests：`49 passed`。
- Frontend lint：PASS。
- Frontend build：PASS，生成 `28` 个静态页面。
- 业务页面保持现有 Terra 视觉体系，未新增 Company 首层或新的 Workspace/Admin/BusinessDepartment 平行体系。

### 官方启动

- 最终候选命令：`CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh`
- 启动结果：PASS。
  - Frontend：`3001`
  - Workspace：容器内部 `8002`
  - Gateway：`8080`
- `GET http://127.0.0.1:8080/health`：`200`
- `GET http://127.0.0.1:3001/gateway/api/auth/local/status`：`200`
- 状态：`mode=local_desktop`、`initialized=true`。

### 迁移库

最终候选重启后直接核验主库：

- Project 总数：`8`
- 缺失 `department_id`：`0`
- 无法解析到同 tenant 业务部门：`0`
- 位于“待归属业务部”的历史 Project：`5`
- “待归属业务部”按 tenant 隔离；已确认 `default`、`quality-local-media`、`selfuse`、`tenant-local` 各自拥有独立部门。
- 主库可迁移的 `COMPLETED + 非空 output` Task：`0`
- Artifact：`0`

多次官方重启后 Project 总数、部门关系与空成果状态保持，未重复创建关系或伪造 Artifact。

### Desktop Browser

- 重启后旧 Session 失效，访问原 Project/Task 路径进入 `/login?next=<原路径>`；点击“进入 Curis”后返回原访问页面，未出现 `Failed to fetch`。
- CEO 首页：
  - Company：`Curis Local Desktop 验收公司`
  - `1` 个业务部门、`2` 名 AI 员工、`2` 个项目
  - 首层入口：`Local Desktop 研发部 · 2 人 · 2 项目`
  - 最近成果真实空状态：`尚无真实成果记录`
- 业务部门详情先显示 `直属员工`，再显示 `直属项目`。
- 员工详情显示主归属 `Local Desktop 研发部`；未配置事实保持 `未分配`。
- Project 工作台显示 `所属业务部门：Local Desktop 研发部`。
- 质量席通过 UI 创建 Task：
  - Task：`生成业务部门验收成果 20260729`
  - ID：`83eebab8-7d33-4462-99fd-5ecee7b992d1`
  - 执行员工：`Local Desktop 技术负责人`
- 执行结果：真实失败，页面显示：
  - `Model Gateway Adapter requires CURIS_MODEL_GATEWAY_BASE_URL, CURIS_MODEL_GATEWAY_API_KEY, and CURIS_MODEL_GATEWAY_MODEL`
- Task 详情保持真实事实：
  - 状态：`失败`
  - Artifact：`0`
  - 模型、Token、成本等无事实字段显示 `未记录`
- Project 成果页保持：
  - `暂无项目成果。任务成功执行并登记成果后会显示在这里。`
- 直接访问其他 tenant 的迁移 Project 返回 `resource not found`，与自动化跨租户 `404` 证据一致。

### Mobile Browser

视口：`390 × 844`。

- CEO 首页、业务部门详情、员工详情、Project 工作台、Task 详情、成果页均可访问。
- 页面均未出现横向溢出；各页 `scrollWidth == clientWidth`。
- 移动端同样显示业务部门首层、员工/项目归属、失败 Task 的真实原因与成果空状态。

## 阻塞项

`BLOCKED_L2`：

- 官方本地运行环境没有 Model Gateway 配置，真实 Task 无法成功执行。
- 当前主库没有可迁移的成功历史 Task，无法用既有真实数据补齐 Browser 正向 Artifact 证据。
- 不得用 mock、手工改库、内容包或自动化测试结果冒充真实 Browser 成果。

## 建议

1. 产品席可接受本 Issue 的数据库、API、迁移与前端组织模型实现。
2. 在安全边界批准的运行环境中注入现有 Model Gateway 配置，或提供一个同 tenant 的真实 `COMPLETED + 非空 output` 历史 Task。
3. 证据就绪后只补一次 Browser 正向复验：执行 Task 成功 → Task 详情出现 Artifact → Project 成果页出现同一 Artifact → 重启后仍可见。
4. 不重复 Backend 全量、Frontend tests/lint/build 或既有迁移验证，除非相关代码再次变化。

Handoff: sent to 产品规划席；实现与回归可接受，完整真实成果 Browser Gate 保持 `BLOCKED_L2`。
