# Regression Stabilization Review

Date: 2026-07-29

Status: PASS

Issue: `issues/20260729_regression_stabilization.md`

## Conclusion

S2 Review 记录的 13 项历史全量回归失败已按五类根因收口。干净提交树的权威后端
全量回归为 `1112 passed, 3 skipped, 0 failed`，Regression Stabilization Task 关闭。

## Changes

- 删除四个历史测试对 `backend/app` 的全局 `sys.path` 污染，恢复顶层 import 共存守卫。
- CEO Evidence 样本改为写入受控临时库，并移除契约禁止的旧措辞。
- Pipeline Runtime FakeResolver 跟随现有 `employee_id` 参数。
- MCP stdio 测试使用标准命令转义，兼容包含空格的工作区路径。
- Real RD pytest 命令与 LocalRDToolset 现有允许命令统一。
- 未新增产品能力、依赖、数据库表或架构抽象。

## Evidence

- 五类聚焦回归：`104 passed`。
- 干净提交树权威全量回归：

```bash
backend/.venv/bin/python -m pytest -q backend/tests
```

结果：`1112 passed, 3 skipped`。

- `git diff --check`：PASS。
- 当前共享工作区叠加未纳入本 Task 的员工目录未提交改动时为
  `1112 passed, 1 failed, 2 skipped`；唯一失败是其部门删除文案差异。该改动未进入
  本 Task 暂存区或提交，干净提交树已证明本 Task 门禁全绿。

## Boundary

本 Task 只做回归稳定化，无产品 UI 或浏览器行为变化，因此复用 S2 已通过的
Desktop/Mobile 浏览器证据，不重复 E2E。

Handoff: sent to main thread
