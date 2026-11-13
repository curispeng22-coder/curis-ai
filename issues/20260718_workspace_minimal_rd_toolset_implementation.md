# Workspace：最小真实研发工具集实施

- 状态：`CLOSED`
- 优先级：`P0`
- 发起：产品规划席
- 安全先行：安全边界席
- 实施：系统交付席
- 验证：质量运行席
- 前置：`issues/20260718_workspace_real_rd_tool_closure_prerequisite_gate.md`（`CLOSED`）

## 目标

把 5 个现有 mock 目录条目变成一条**本地、受控、无网络**的真实研发工具链：

```text
文件读取 / 搜索 → 受控补丁修改 → 已批准测试或 Build → Git Diff / 成果 → Tool 审计
```

候选 Tool ID 仅限：

- `tl_ai_rd_file_reader`
- `tl_ai_rd_code_docs_search`
- `tl_ai_rd_file_writer`
- `tl_ai_rd_test_runner`
- `tl_ai_rd_git_client`

不实现其余 110 个 Tool；不启用 `shell_terminal`、`python_repl`、`code_executor`、`github_api` 或任何通用命令执行器。

## 先决安全契约

安全边界席必须先给出 PASS 契约，系统交付席才可写代码。契约至少固定：

1. 只允许一个明确的本地工作区根目录；路径必须相对、规范化并留在根目录内。
2. 禁止读取或写入 `.env`、凭据、密钥、Cookie、数据库、部署配置、Git 元数据与根目录外文件。
3. 写入只接受受控 unified diff；禁止删除目录、重命名、符号链接、任意命令、网络与子进程透传。
4. 测试 / Build 仅允许此后独立真实小 Issue 列明的既有项目命令；禁止任意 shell。
5. Git 只允许只读 diff / status；禁止 stage、commit、push、reset、checkout 或远程操作。
6. 审计仅记录 Tool ID、相对路径、变更摘要 / hash、测试结果、退出码、时间与 Run 关联；不得记录文件正文、prompt、凭据或 token 值。

## 实施范围

1. 在现有 ToolExecutor / 审计链中实现上述 5 个受限动作；优先复用已有路径、审计和 Usage / 成本投影，不新增通用执行框架。
2. Admin 仅在 Workspace 后端执行体和质量证据完成后，通过 Shared 双 lead 会签把这 5 个条目从 mock 受控发布为 executable；其他目录项保持 mock。
3. 每个动作均需 fail-closed；未知 Tool、越界路径、敏感路径、非法 diff、未批准命令或审计失败均零副作用。

## 安全契约已通过

`reviews/20260718_workspace_minimal_rd_toolset_security_review.md` 已 PASS。实施必须逐字遵守其工作区、路径、受控 diff、精确 argv、只读 Git、脱敏审计和零模型/零成本边界。

`command_id` 不在本实施 Issue 自行发明；只能由后续独立真实小 Issue 按该 Review 预登记精确 argv。当前实施仅提供 fail-closed 的命令 ID 校验与执行框架，并用 focused 测试验证拒绝路径。

## 禁止范围

- 不做前端、Secretary、115 Tool 批量实现、Connector、GitHub、Provider、模型调用、凭据注入或网络。
- provenance Step1 继续 `PAUSED_BY_NEW_PRIORITY`。
- 不创建最终 AI E2E；该 E2E 必须另立真实小 Issue，并固定允许文件、单一补丁和测试 / Build 命令。

## 验收

1. 安全契约 PASS 后，系统交付席完成最小 focused 测试：正向读取/搜索/受控补丁/测试或 Build/Git Diff；负向越界、敏感路径、任意命令、任意 Git 写操作和审计失败全部拒绝。
2. 质量运行席独立验证真实本地工具链，不调用模型、不出网；Tool 审计与已有 Usage / 成本投影可读取。
3. 仅在质量 PASS 后，才可申请最终真实小 Issue，验证 AI 在批准范围内读取、修改、测试并交付 Diff。

## 验证结果

质量运行席在 `b5089837` 独立复核：focused 44/44，compileall PASS，全量 677 通过 / 20 既有失败 / 2 跳过 / 0 错误。Reader、Search、Writer、Git 的真实本地受控动作、审计、回滚与无 fallback 均成立。Test Runner 注册表仍为空，任意命令拒绝；本 Issue 不把它写成真实测试链。见 `reviews/20260718_workspace_minimal_rd_toolset_implementation_review.md`。
