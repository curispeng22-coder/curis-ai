# Workspace Package→Workflow 撤销桥接 fail-closed 修复质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_package_workflow_bridge_revocation_failclosed_fix.md`
- 分支：`feat/roadmap-r1r2`
- SHA：`bc9b55ecb07dfbb6b5f0464c682b4b3b938a1bd5`
- 质量结论：`PASS`

## 结论

撤销桥接在 Task/Run/Step/Usage 写入前 fail-closed 的修复复核通过。原父 Issue 唯一阻塞已消除；应重派父 Issue 完整静态收口，真实模型调用仍不在本次授权范围。

## 独立证据

- Run 创建路径已删除自建桥接查询，复用 `resolve_company_package_workflow_bridge` 唯一精确解析器。
- 解析器统一校验 Package 精确版本、active/enabled、桥接唯一 active、`revoked_at is null`、tenant 可见性、来源版本、目标版本和 `structured_executable` capability。
- 新回归先创建合法 Company/Workflow Instance，再撤销 bridge；创建 Run 返回 HTTP `422`。
- 撤销前后 Task、Run、Step、Usage 计数完全一致，证明拒绝发生在运行实体写入前。
- 独立 focused：`PYTHONPATH=backend .venv/bin/python -m pytest -q backend/tests/test_package_workflow_versioned_bridge.py backend/tests/test_r2_instantiation_evidence.py` → `16 passed`。
- `.venv/bin/python -m compileall -q backend/app` → `PASS`。

## 范围声明

- 提交仅修改 Run 桥接校验、focused 回归和本修复 Issue。
- 未修改 bridge 数据、历史 Company/Run/Usage、旧 Package 版本、模型、网关、成本、前端或公开 API。
- 未启动服务、未注入 Key、未出网、未调用模型，未运行全量回归。

## 唯一缺口

无。

Next Seat: 产品规划席

Handoff: sent to 产品规划席
