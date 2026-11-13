# Workspace D1 单次模型到受控 Tool 链入口安全 Review

- Issue：`issues/20260718_workspace_d1_single_model_toolchain_entry_gate.md`
- 结论：`PASS`（仅入口安全契约；不授权启动、注Key、模型调用或实现外扩）
- 复用依据：
  - `reviews/20260718_workspace_minimal_rd_toolset_security_review.md`
  - `reviews/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation_security_review.md`

## 唯一入口契约

- 入口是 D1 专用服务端路径，不是通用 Agent、Shell、Python、代码执行器或可配置 Tool Router。
- 请求不得携带或覆盖 tenant、project、task、run、工作区根、文件路径、Tool ID、command、Provider、Model、Gateway、URL、凭据、diff 上限或调用次数；缺少服务端固定上下文即拒绝。
- 服务端只绑定当前批准的 D1 Run/scope；无法解析唯一 Run、租户、项目、任务或审计上下文时，在模型调用前拒绝。
- 不复用 `ToolExecutor.execute_chain()` 的 fallback chain、动态 planner 或默认 Tool；入口按固定链逐项调用既有五个受控 Tool：

`Reader/Search（两固定文件） → Writer（唯一脚本、≤4KiB diff） → TestRunner（唯一 command_id/argv） → GitClient（该脚本只读 diff/diff-check）`

- 只能发生一次模型调用；无第二调用、第二 diff、第二命令、跳步、重置、Fallback 或重试。

## 前置与模型边界

模型调用前必须服务端依次确认：

1. 工作区根目录、两份输入路径和唯一写入路径精确匹配 D1 Issue；
2. 两份输入通过敏感扫描，且模型 Prompt 只含两份文件的相对路径标签、正文和固定修复目标；
3. preimage SHA-256、4KiB 限额、唯一 `command_id=rd_e2e_verify_d1_tenant_reservation`、精确 pytest argv、Tool 审计 sink 和 Run scope 均可用；
4. Provider/Model/Gateway/出口/隐藏 Key 仅使用总控后续批准的既有配置，所有参数服务端固定；Key 仅检查存在，禁止读取、回传或进入请求体。

任一前置失败均不得启动模型、写目标文件、运行测试或执行 Git。

## 输出与工具 fail-closed

- 模型输出只能是原始 unified diff；不得含 Markdown、解释、命令、脚本、Base64、二进制或多个候选 patch。
- Writer 仅允许 `tools/verify_d1_tenant_reservation.py`，preimage 不匹配、路径/语法/敏感扫描/4KiB 任一失败即零写入；禁止 partial apply。
- TestRunner 仅运行注册的精确 argv：
  `backend/.venv/bin/python -m pytest -q backend/tests/test_d1_verify_script.py`；无额外参数、Shell、环境覆盖或第二命令。
- GitClient 仅对该脚本执行只读 `diff`/`diff --check`；禁止任何 Git 写操作或网络。
- 五个 Tool 均无网络、无凭据继承、无模型调用；Tool 失败、审计失败、路径越界、未知状态或输出不完整均停止后续链路并回滚未提交写入。

## 审计与成本

- 本次最多一条模型 Usage：固定 `model_call=1`；Reader/Search/Writer/TestRunner/GitClient Usage 固定 `model_call=0`、`cost_source=local_tool_no_model`。
- 审计只保留既有最小字段：Tool ID、request/run/tenant/project/task 关联、相对路径或 hash、diff hash、command_id、结果、失败码、退出码、耗时、时间；不记录 Prompt、文件正文、模型原文、命令原文、Key、Authorization、Cookie、JWT 或 token 值。
- 不产生第二模型事件、第二出站、额外成本或隐藏 Fallback；成本和 Token 只按总控批准的单次模型 Gate 记录。
- 入口结束后立即停机；未完整通过 Writer→TestRunner→GitClient 链时，不得报告成果或成功。

## 结论边界

本 PASS 只允许系统交付席实现 D1 专用入口并交质量 focused 验收；不替代总控对 Provider/Model/Gateway、凭据注入、单次模型调用、Token/成本和停机的批准。Provenance Step1 继续 `PAUSED_BY_NEW_PRIORITY`。

Handoff: sent to 产品规划席
