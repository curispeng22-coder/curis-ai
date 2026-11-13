# Workspace 启动失败信号受控撤销质量 Review

- Issue：`issues/20260719_workspace_startup_failure_signal_controlled_revert.md`
- 撤销修订：`f5b59f4526b8bf805bd86adb1f9a53dd6084db92`
- 目标修订：`fec65c1aa58010639d10eeca9cdfd099d54f805b`
- 基线修订：`00c46737cbfc2c1475698252ca2c5bb347fd45b1`
- 结论：`PASS`

## 独立证据

1. `f5b59f45` 的直接 parent 为 `fec65c1a`，且为其线性后继 revert；本地 HEAD 与 `origin/feat/roadmap-r1r2` 均为 `f5b59f45`。
2. 撤销提交精确包含 5 个路径，无第六文件：
   - `M backend/app/main.py`
   - `D backend/app/startup_failure.py`
   - `D backend/app/workspace_startup.py`
   - `D backend/tests/test_workspace_startup_failure_signal.py`
   - `M deploy/curis/gateway/Dockerfile.workspace`
3. 上述 5 路径相对 `00c46737` 的 diff 为空，五路径工作树 clean，revert `git diff --check` 通过。
4. `backend/app/main.py` 内存 compile 通过；Workspace CMD 已恢复为 `python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8002`。
5. `3000/3100/8001/8002/8080` 全部 `CLOSED`；固定 D1 correlation 的 claim/model/tool/usage 及其他事件均为 0。未启动、未注 Key、未调用模型、未执行 D1、pytest、外网或 sentinel。

## 结论

撤销提交精确抵消目标提交的五路径变更，未扩大提交范围，且恢复实施前基线，`CONTROLLED_REVERT` 验收为 `PASS`。父 D1 继续冻结。

Next Seat：产品规划席

Handoff: sent to 产品规划席
