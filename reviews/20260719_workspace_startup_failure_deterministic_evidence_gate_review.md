# Workspace 启动失败可判定证据 Gate 质量 Review

- Issue：`issues/20260719_workspace_startup_failure_deterministic_evidence_gate.md`
- 契约结论：`PASS`
- 被拒实现：`fec65c1aa58010639d10eeca9cdfd099d54f805b`
- 撤销修订：`f5b59f4526b8bf805bd86adb1f9a53dd6084db92`
- 撤销结论：`PASS`
- 当前边界：仅保留已通过的结构化证据契约；无 stage/signal 运行实现

## 独立撤销证据

1. `f5b59f45` 的直接 parent 为 `fec65c1a`，提交说明明确为其 revert；本地 `origin/feat/roadmap-r1r2` 同样指向 `f5b59f45`。
2. revert 仅覆盖原实现的 5 个路径：`backend/app/main.py`、`backend/app/startup_failure.py`、`backend/app/workspace_startup.py`、`backend/tests/test_workspace_startup_failure_signal.py`、`deploy/curis/gateway/Dockerfile.workspace`。
3. 上述 5 路径与实施前基线 `00c46737cbfc2c1475698252ca2c5bb347fd45b1` 的 diff 为空；五路径工作树 clean，`git diff --check` 通过。
4. 新增的 `startup_failure.py`、`workspace_startup.py` 与 focused 测试均已删除；`main.py` 内存 compile 通过。
5. Workspace Docker CMD 已恢复为 `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8002`。
6. `3000/3100/8001/8002/8080` 全部 `CLOSED`；未运行 pytest、未启动、未注 Key、未调用模型、未执行 D1、未出网或 sentinel。

## 结论与边界

受控撤销精确、完整且未扩大路径，原实现的契约偏差与授权越界已从当前代码中移除，撤销结论为 `PASS`。

本 PASS 仅恢复 Gate 的“契约已通过、实现未授权”状态，不证明 Workspace 启动根因已解决，也不授权下一次 sentinel。父 D1 继续冻结，后续实施仍须独立 Issue 与总控 / 安全授权。

Next Seat：产品规划席

Handoff: sent to 产品规划席
