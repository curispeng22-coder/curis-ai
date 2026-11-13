# MVP Phase 1 / S2 — Workspace 基础模型 Review

Date: 2026-07-29

Status: PASS

Issue: `issues/20260729_mvp_phase1_s2_workspace_model.md`

## Conclusion

T003 / T004 / T005 的聚焦实现、浏览器流程与干净提交树全量后端回归均通过，本 Issue 关闭。

## Implemented

- Company：组织中心可创建、读取、编辑名称、描述和状态。
- Department：可创建、读取、编辑、暂停、恢复和受保护删除。
- Department Detail：改为读取真实部门、员工与项目，不再展示示例快照或本地草稿。
- Home：新增独立 Workspace Home router，聚合当前公司、部门、项目、AI 员工和真实内容成果。
- Navigation：移除硬编码部门/项目名称，动态详情仍正确高亮所属中心。
- 未新增依赖、数据库表、Workspace/Admin 或 Mock 经营数据。

## Passed Evidence

- `backend/.venv/bin/python -m unittest discover -s tests -p 'test_mvp_phase1_s2_workspace.py'`：2 passed。
- `pnpm --dir frontend lint`：PASS。
- `pnpm --dir frontend build`：PASS，26 个静态页面生成成功。
- `git diff --check`：PASS。
- Desktop browser（隔离临时库）：
  - 首页真实空状态可达；
  - 编辑 Company 后首页显示真实名称与描述；
  - 创建 Department 后组织中心和首页计数同步为 1；
  - Department 暂停、恢复和真实详情页通过。
- Mobile browser（390×844）：首页与组织中心无横向溢出，真实 Company / Department 可见。

## Full Regression Closure

权威命令：

```bash
backend/.venv/bin/python -m pytest -q backend/tests
```

Regression Stabilization Task 修复五类历史根因后，在干净提交树执行结果为：
`1112 passed, 3 skipped, 0 failed`。

详细证据：`reviews/20260729_regression_stabilization_review.md`。

## Change Summary

- 以一个小型 Home router 开始 M1 增量解耦，没有重写现有 Company/Department 服务。
- 组织中心从五条共享 API 顺序读取，避免本地跨域环境并发连接失败。
- 删除旧本地草稿、示例部门、硬编码进度与“能力包当项目”的错误投影。

Handoff: sent to main thread
