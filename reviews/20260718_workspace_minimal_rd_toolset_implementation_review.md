# Workspace 最小真实研发工具集实施质量 Review

- 日期：2026-07-18
- Issue：`issues/20260718_workspace_minimal_rd_toolset_implementation.md`
- 分支：`feat/roadmap-r1r2`
- 固定修订：`b508983709212615f26e8e46dce36fe2704c2ee6`
- 安全依据：`reviews/20260718_workspace_minimal_rd_toolset_security_review.md`
- 验证席：质量运行席

## 结论

**PASS（限本 Issue 的后端受控执行体）。**

五个固定 Tool ID 已接入同一 `LocalRDToolset` 与既有 `ToolExecutor`/Usage 审计链；文件读取、字面搜索、受控 unified diff、只读 Git 为真实本地动作。Test Runner 已实现精确 `command_id` 注册与拒绝框架，但本 Issue 按安全决定保持注册表为空，因此当前所有测试/Build 命令均 fail-closed，不能误报为已完成真实测试执行。

本 PASS 只允许产品规划席申请后续独立真实小 Issue；不授权模型、网络、前端、Admin 发布、任意命令或最终 AI E2E。

## 独立证据

### 1. 修订与范围

- 当前 HEAD：`b508983709212615f26e8e46dce36fe2704c2ee6`。
- 变更仅三文件：`backend/app/local_rd_toolset.py`、`backend/app/tool_executor.py`、`backend/tests/test_local_rd_toolset.py`。
- `git diff --check f01b3df4..b5089837`：PASS。
- 未改模型、Provider、Gateway、Admin、前端、资产或历史数据；未启动服务、未注 Key、未出网、未调用模型。

### 2. focused 与静态检查

命令：

```text
cd backend
.venv/bin/python -m pytest -q tests/test_local_rd_toolset.py tests/test_execution_engine.py
.venv/bin/python -m compileall -q app
```

结果：**44 passed / 0 failed**；compileall PASS。

覆盖：

- Reader/Search/Writer/Git 的真实本地正向动作；
- 相对路径、精确 allowlist、敏感路径、敏感值、UTF-8/大小边界；
- symlink、hardlink、删除、重命名、非法 diff、preimage hash；
- Writer 原子替换及最终审计失败回滚；
- 未登记/任意命令和 Git 写操作拒绝；
- 五个本地 Tool 无 fallback，trace 不保留 input/output；
- Tool Usage 固定 `model_call=0`、Token=0、成本=0、`outbound_attempted=false`。

### 3. 一次全量回归

命令：`cd backend && .venv/bin/python -m pytest -q`

结果：**677 passed / 20 failed / 2 skipped / 0 errors**，137.53s。

前一质量基线为 **671 passed / 20 failed / 2 skipped / 0 errors**；本修订新增 6 项 focused 且全部通过，失败与跳过集合未变化，没有新增回归。

### 4. 五个 Tool 边界

- `tl_ai_rd_file_reader`：只读单个精确 allowlist 普通 UTF-8 文本；敏感值整次拒绝。
- `tl_ai_rd_code_docs_search`：只在精确文件 allowlist 做有界字面搜索，无正则、目录遍历或代码执行。
- `tl_ai_rd_file_writer`：仅受控 unified diff；最多 10 文件/128 KiB，精确 preimage hash，禁止删除/重命名/元数据 diff，原子写入并在审计失败时回滚。
- `tl_ai_rd_git_client`：固定 `status`、`diff`、`diff --check`，使用路径终止符和 allowlist；不接受任意 Git 参数。
- `tl_ai_rd_test_runner`：只接受注册表中的精确 argv；当前注册表为空，任意 `command_id` 均拒绝，未启动子进程。

### 5. 审计与泄露复核

- 每次动作先写 started 审计，最终写 succeeded/rejected；审计不可写时动作不执行或 Writer 回滚。
- 审计只记录 Tool/scope/path hash/pre-post hash/command/结果/时间等最小字段，不记录文件正文、diff、prompt、环境变量或进程原文。
- `ToolExecutor` 对五个 Tool 固定单候选，不走 `default_tool`；trace 的 input/output 固定为空。
- 本修订无网络库、模型调用、凭据读取或 Admin 路由变更。

## Gate 判断

- 后端受控执行体：**通过**。
- 最终五步真实链：**尚未执行，符合本 Issue 禁止范围**。
- Test Runner 正向命令：**0 个，等待独立真实小 Issue 预登记精确 argv**。
- 是否可申请后续真实小 Issue：**可以**；仍须固定单一工作范围、单一补丁、单一命令，并独立验证无网络、审计和零模型成本。

Next Seat：产品规划席  
Handoff: sent to 产品规划席
