# Workspace：真实研发工具 E2E｜D1 Tenant Reservation 哨兵修复

- 状态：`BLOCKED`
- 优先级：`P0`
- 发起：产品规划席
- 安全复核：安全边界席
- 模型调用裁决：总控决策席
- 执行：系统交付席 / 质量运行席
- 前置：`issues/20260718_workspace_minimal_rd_toolset_implementation.md`、`issues/20260718_workspace_real_rd_tool_e2e_candidate_selection.md`（均 `CLOSED`）

## 真实小问题

修复 `tools/verify_d1_tenant_reservation.py` 中运行时 `DEFAULT_TENANT=selfuse` 与 SQLite 列默认 `default` 的哨兵混用。当前 `backend/tests/test_d1_verify_script.py` 稳定 3 个失败。

## 唯一允许输入

- 工作区：`/Users/yy/Documents/Curis AI Workspace`
- 模型可读路径：
  - `tools/verify_d1_tenant_reservation.py`
  - `backend/tests/test_d1_verify_script.py`
- 唯一可写路径：`tools/verify_d1_tenant_reservation.py`
- 测试路径（只读）：`backend/tests/test_d1_verify_script.py`
- diff 总上限：4 KiB，仅普通文本 unified diff，且 preimage SHA-256 必须匹配。
- command_id：`rd_e2e_verify_d1_tenant_reservation`
- 精确 argv：`["backend/.venv/bin/python", "-m", "pytest", "-q", "backend/tests/test_d1_verify_script.py"]`
- cwd：`/Users/yy/Documents/Curis AI Workspace`

## 预期链路

```text
AI 只读允许文件
→ 受控 unified diff 修改唯一脚本
→ 登记 command_id 运行唯一 pytest
→ 只读 Git diff / diff-check
→ 成果摘要、Tool 审计、Token / 成本
```

## 安全与模型前置

本 Issue 先要求安全席确认：这两份允许文件可否作为唯一最小模型输入、是否存在敏感内容 / 出站风险，以及模型输出到受控 diff 的附加 fail-closed 条件。

安全 PASS 后，总控必须单独固定 Provider / Model / Gateway / 受控出口 / 隐藏 Key 注入、单一 Run、单次模型调用、Token / 成本上限、超时、0 重试、无 Fallback 与停机方式。此前不得启动、注 Key、调用模型、修改文件或运行测试。

安全边界席已 PASS：`reviews/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation_security_review.md`。两份输入的敏感扫描、唯一 diff、测试 argv、只读 Git、工具零模型成本与日志脱敏已固定；本 PASS 不授权模型调用。

## 已批准单次执行契约

- 仅一条模型调用，随后仅一次固定工具链：读取两文件 → 对唯一脚本应用一个 ≤4 KiB、preimage 匹配的 unified diff → 运行唯一 `command_id` → 对该文件只读 Git diff / diff-check → 审计与成果摘要。
- 不得有第二模型调用、第二 diff、第二命令、额外文件、额外网络或 provenance Step1 恢复。
- 固定路径：OpenAI API / `gpt-5.4-mini-2026-03-17` / `newapi` / `https://api.openai.com:443/v1/chat/completions`；Key 仅 `CURIS_MODEL_GATEWAY_API_KEY` 由 Owner 隐藏部署注入。
- 单次输入 / 输出 / 总 Token 上限：8192 / 2048 / 10240；60 秒；0 重试；429 不重试；无 Fallback；本次模型硬成本上限 USD 0.02，且不突破既有 USD 0.10 总上限。
- 启动前逐项检查固定路径、两文件敏感扫描、Key 仅存在、唯一命令及全部 diff 限制；任一不符写入前拒绝。
- 调用和工具链完成后立即停机；日志不得含 Key、Authorization、Cookie、Prompt、文件正文或模型原文。

所有无凭据准备已授权；唯一外部依赖是 Owner 隐藏注入已有 Key。Key 缺失时必须保持 `WAIT_FOR_OWNER_INJECTION`，不得降级、替换模型或调用。

## 运行入口前置

系统交付席确认当前默认运行时没有注册 D1 的单次模型到受控 Tool 链入口，`start-local` 也只能启动既有 R3 Workflow Gate。该缺口已登记为 `issues/20260718_workspace_d1_single_model_toolchain_entry_gate.md`，等待总控与安全裁决。未经该 Gate 通过，即使 Owner 注入 Key 也不得启动或调用。

入口 Gate 已在 `d57da0da` 完成质量收口；父 E2E 恢复为仅等待 Owner 隐藏注入 Key。单次模型、固定 Tool 链、成本和停机契约仍以本 Issue 已批准内容为准。

## 当前可信身份阻塞

实际 `quality.sqlite` 中 `selfuse` tenant 没有 active owner / ceo 且 `ceo_id` 非空的 membership；现有可信 membership 属于 `tenant-a`。D1 `_preflight` 在 claim / 模型 / Tool 前强制 `selfuse + active + owner/ceo + ceo_id`，所以 Key 不是当前唯一依赖，任何现有启动命令都会 fail-closed。

本 E2E 不能改用 `tenant-a` 或猜测身份。唯一继续条件见 `issues/20260718_workspace_d1_selfuse_trusted_identity_gate.md`；在该 Gate 裁决前不生成 Owner 执行命令。

可信 selfuse identity Gate 已 CLOSED，现只允许无出网静态预检重核固定身份、两文件、diff、命令、入口与零副作用。该预检 PASS 后，如 Key 仍缺失，状态回到 `WAIT_FOR_OWNER_INJECTION`；仍不授权启动或调用。

质量静态预检已 PASS：selfuse 可信链、两文件敏感扫描、clean diff、唯一 command / argv、owner / ceo preflight、D1 零副作用与端口全关闭均成立。Key 存在性为 `MISSING`，因此唯一外部依赖是 Owner 隐藏注入；未启动、未调用、未跑 pytest。

## 启动失败待诊断

Owner 已尝试隐藏注入并启动。容器构建、egress healthy、workspace / gateway 容器启动均出现，但启动脚本对 `http://127.0.0.1:8080/health` 的 30 秒健康检查未获得 200，报“Gateway 启动失败”后触发自动清理。未发生模型调用、D1 文件写入或 pytest。

在 `issues/20260718_workspace_d1_e2e_gateway_startup_diagnostic.md` 收口前，不得重复注入 Key 或重试启动。

## 禁止范围

- 不读取或写入其他文件；不扫描仓库；不访问 `.git`、`data/`、`deploy/`、凭据或敏感路径。
- 不使用通用 Shell、Python REPL、code executor、GitHub、网络或任意命令。
- 不创建第二 Run、第二次调用、第二个 diff 或第二条测试命令；不 stage、commit、push。
- provenance Step1 继续暂停，不能复用或消耗其授权。

## 成功验收

质量运行席独立确认：

1. 仅允许路径被读取 / 修改，且 diff 不超过 4 KiB；
2. 现有 3 个失败测试转为通过；
3. Git diff / diff-check、成果摘要、五个 Tool 审计链完整；
4. 仅本次模型调用产生 Token / 成本，所有工具 Usage 均 `model_call=0`、`cost_source=local_tool_no_model`；
5. 无网络外溢、无凭据、无未授权写入；完成后环境停止。
