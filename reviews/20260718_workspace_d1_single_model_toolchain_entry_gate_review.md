# Workspace D1 单次模型到受控工具链入口质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_d1_single_model_toolchain_entry_gate.md`
- 分支：`feat/roadmap-r1r2`
- 固定修订：`d57da0da16ea39c16d65b4da500de6e5674257e0`
- 安全依据：`reviews/20260718_workspace_d1_single_model_toolchain_entry_security_review.md`、`reviews/20260718_workspace_d1_entry_owner_role_claim_fix_security_review.md`
- 验证席：质量运行席

## 结论

**PASS（仅无出网入口收口）。**

D1 固定空请求入口、服务端固定 scope、active owner/ceo preflight、单次 claim、两文件 Reader/Search、唯一脚本 Writer、唯一 TestRunner command、单文件 Git diff/diff-check 及失败回滚在同一修订成立。原角色授权阻塞已由质量与安全双 PASS 解除。

本 PASS 不授权启动、注 Key、模型调用、目标文件修改或 D1 pytest；父 E2E 继续 `WAIT_FOR_OWNER_INJECTION`。

## 独立证据

### 1. 固定修订与范围

- 当前 HEAD：`d57da0da16ea39c16d65b4da500de6e5674257e0`。
- 父入口实现范围为 `d1_single_model_toolchain.py`、`local_rd_toolset.py`、`main.py` 及两份 focused 测试；角色修复只改入口 preflight 与对应测试。
- `git diff --check b5089837..d57da0da`：PASS；compileall PASS。
- 未启动、未注 Key、未调用模型、未读写 D1 目标、未运行 D1 pytest、未出网。

### 2. 无出网 focused

命令：

```text
cd backend
.venv/bin/python -m unittest \
  tests.test_d1_single_model_toolchain_entry \
  tests.test_local_rd_toolset
```

结果：**12 passed / 0 failed**。

### 3. 固定入口与 preflight

- HTTP 路由只接受空请求体与空查询参数；执行方法无客户端参数。
- tenant/project/task/run、两输入路径、唯一写路径、4 KiB、command_id/argv、Provider/Model/Gateway、60s 与成本上限均为服务端常量。
- preflight 在 claim 前验证固定 tenant、active membership、`role in {owner, ceo}`、非空 `ceo_id`/request_id、Key 仅存在、Tool scope、路径集合、唯一 command registry 和审计 sink。
- `member`、空角色、revoked、错 tenant、缺 Key 均在 claim/model/Tool 前拒绝，focused 断言零副作用。

### 4. 唯一执行链

固定顺序为：

```text
Reader(target) → Reader(test) → Search
→ 单次 Model → Writer(单一 ≤4KiB preimage-matched diff)
→ TestRunner(唯一 command_id)
→ Git diff → Git diff-check
```

- 入口不调用 `ToolExecutor.execute_chain()`，无 dynamic planner、default Tool、fallback 或第二模型分支。
- claim 使用数据库 `begin immediate`，同一 Run 已有 D1/model 事件即拒绝。
- 非 raw unified diff、超限或多 diff 在 Writer 前停止；Writer 后测试失败会回滚且不进入 Git。
- Local Tool 审计保持正文/diff/trace 脱敏，Tool Token/成本为 0，`outbound_attempted=false`。

## Gate 判断

- D1 不可泛化入口：**通过**。
- owner/ceo claim：**通过**。
- 原 `BLOCKED_L2`：**解除**。
- 父 D1 E2E：仍为 `WAIT_FOR_OWNER_INJECTION`；仅在 Owner 隐藏注入与正式单次指令后才可执行。

Next Seat：产品规划席  
Handoff: sent to 产品规划席
