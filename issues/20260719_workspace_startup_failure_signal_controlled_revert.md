# Workspace 启动失败信号未授权提交受控撤销

- 状态：`CLOSED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 目标提交：`fec65c1aa58010639d10eeca9cdfd099d54f805b`
- 父提交：`00c46737cbfc2c1475698252ca2c5bb347fd45b1`
- 父 E2E：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`（保持冻结）

## 裁决与审计事实

目标提交已推送，但原证据 Gate 明确排除阶段标记实现，且质量结论为 `BLOCKED_L2`。总控裁决 `CONTROLLED_REVERT`：不接受后补授权、逐 hunk 隔离或运行 sentinel。

## 精确范围

只撤销目标提交带来的以下五个文件变更：

- `backend/app/main.py`
- `backend/app/startup_failure.py`
- `backend/app/workspace_startup.py`
- `backend/tests/test_workspace_startup_failure_signal.py`
- `deploy/curis/gateway/Dockerfile.workspace`

## 执行约束

- 使用可审计的受控撤销，产生新的撤销提交；不得 `reset --hard`、强推、改写历史或影响其他既存修改/未跟踪文件；
- 撤销前后核对仅上述五个文件进入撤销 diff，工作树其余既存脏改动保持原样；
- 不启动 Docker/服务，不注 Key，不调用模型、D1、pytest 或外网；
- 回传撤销 SHA、五文件 diff 范围和工作树隔离证据；质量席仅复核撤销范围与零运行副作用。

## 验收

1. `fec65c1a` 的五文件变更被新撤销提交精确抵消；
2. 不含其他文件或历史改写；
3. D1 仍冻结，未执行 sentinel、模型、D1 或测试；
4. 质量独立复核 PASS 后，本撤销 Issue 收口。

## 收口证据

- 撤销提交：`f5b59f4526b8bf805bd86adb1f9a53dd6084db92`，直接 revert `fec65c1a`；
- 精确范围仅五个列明路径；相对 `00c46737` 的该范围 diff 为空，其他既存脏改动未纳入；
- 质量 Review：`reviews/20260719_workspace_startup_failure_signal_controlled_revert_review.md`，结论 `PASS`；
- 未启动 Docker / 服务，未注 Key，未调用模型 / D1，未运行 pytest、sentinel 或外网。
