# Workspace：真实研发工具 E2E 小 Issue 候选选择

- 状态：`CLOSED`
- 优先级：`P0`
- 当前责任席：系统交付席
- 质量复核：质量运行席
- 前置：`issues/20260718_workspace_minimal_rd_toolset_implementation.md`（`CLOSED`）

## 目标

只读选出一个真实、已存在、足够小的代码问题，作为最终研发工具 E2E 的唯一目标。不得人为制造测试、示例文件或无业务意义的修改。

## 候选条件

候选必须同时满足：

1. 当前分支可复现，且有明确根因、一个或少量普通文本文件的最小修改面；
2. 路径不在安全拒绝目录或敏感文件范围；
3. 可用既有精确 `pytest` 或 `compileall` argv 验证，120 秒内可完成；
4. 不涉及数据库、部署、凭据、网络、模型、Admin 资产、前端或 provenance Step1；
5. 修复后可由 Git Diff、Tool 审计和成果摘要证明。

## 输出

系统交付席只读回传唯一候选的：问题事实、根因、允许文件相对路径 allowlist、受控 unified diff 上限、精确 `command_id → argv`、预期 Git Diff 与不可触碰路径。找不到合格候选必须明确回传“无”。

## 禁止范围

- 不修改代码、数据、配置或工具注册表；不运行模型、不注 Key、不出网。
- 不把 20 个既有失败中的任意一个自动视为候选；必须逐项满足以上条件。

## 后续

产品规划席仅在候选事实明确后，建立最终真实小 Issue，并将 allowlist / command_id 固化；模型调用仍需总控另行裁决。

## 候选结果

- 真实问题：`tools/verify_d1_tenant_reservation.py` 的运行时 `DEFAULT_TENANT=selfuse` 与 SQLite 列默认 `default` 的哨兵混用。
- 允许写入：`tools/verify_d1_tenant_reservation.py`；现有失败测试：`backend/tests/test_d1_verify_script.py`（只读）。
- 受控 diff 上限：4 KiB。
- command_id：`rd_e2e_verify_d1_tenant_reservation`。
- 精确 argv：`["backend/.venv/bin/python", "-m", "pytest", "-q", "backend/tests/test_d1_verify_script.py"]`。
- cwd：`/Users/yy/Documents/Curis AI Workspace`。

见系统交付席正式回传；候选选择收口。
