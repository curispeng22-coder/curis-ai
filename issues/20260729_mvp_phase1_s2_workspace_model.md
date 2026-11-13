# MVP Phase 1 / S2 — Workspace 基础模型

Status: CLOSED — PASS

Owner seat: 系统交付席

Approval date: 2026-07-29

Expected review: `reviews/20260729_mvp_phase1_s2_workspace_model_review.md`

## Objective

按 Curis v1.0 既定对象模型完成：

- T003：Company 创建、读取与编辑。
- T004：Department 创建、读取、编辑、暂停/恢复与受保护删除。
- T005：首页聚合真实公司、部门、项目、AI 员工和最近成果状态。

## Product Boundary

- 对象关系固定为 `Company -> Department -> Employee / Project`。
- 首页是行动入口和状态摘要，不做经营 Dashboard。
- 复用现有 `companies`、`department_instances`、`employee_instances`、`projects` 与内容成果数据。
- 不新增 Workspace/Admin、第二套对象、Mock 经营数据或自动 AI 执行。
- 不改 Curis v1.0 数据模型；本阶段不引入 ORM、队列、Artifact 新表或全量 `main.py` 拆分。

## Implementation

- 在现有 Workspace API 之上补一个独立 Home Summary router，开始 M1 增量解耦。
- 组织中心使用共享 API 层，移除本地草稿、示例部门和硬编码业务事实。
- Company 与 Department 表单复用 S1 的 Drawer/Input/Modal。
- 部门详情从真实接口读取，并展示真实员工与项目关系。
- 首页只展示接口返回事实；无成果时显示空状态。

## Allowed Files

- `issues/20260729_mvp_phase1_s2_workspace_model.md`
- `reviews/20260729_mvp_phase1_s2_workspace_model_review.md`
- `backend/app/routers/__init__.py`
- `backend/app/routers/home.py`
- `backend/app/main.py`（仅 Home router 注册；保留其他未提交改动）
- `backend/tests/test_mvp_phase1_s2_workspace.py`
- `frontend/lib/api.js`
- `frontend/components/terra/TerraNavData.js`
- `frontend/app/ceo-office/page.js`
- `frontend/app/ceo-office/organization/**`
- `knowledge/NOW.md`
- `knowledge/CURRENT_CONTEXT.md`
- `PROJECT_STATUS.md`
- `TASKS.md`

## Acceptance

1. 用户可在组织中心创建并编辑 Company，字段为名称、描述和状态。
2. 用户可创建、编辑、暂停/恢复 Department；有关联员工或项目时界面禁止删除，后端现有员工守卫继续生效。
3. 组织中心和部门详情不再显示本地草稿或示例业务事实。
4. 首页聚合当前 Company、Department、Project、AI Employee 与最近真实成果。
5. 新用户/空项目/空成果、加载失败和重试状态明确。
6. 所有请求保持租户隔离；不新增包或数据库表。
7. 聚焦后端测试、Frontend lint/build、完整后端回归与 Desktop/Mobile 浏览器 E2E 通过。

## Verification

```bash
(cd backend && .venv/bin/python -m unittest discover -s tests -p 'test_mvp_phase1_s2_workspace.py')
pnpm --dir frontend lint
pnpm --dir frontend build
(cd backend && .venv/bin/python -m unittest discover -s tests)
git diff --check
```

Browser hard gate: yes.
