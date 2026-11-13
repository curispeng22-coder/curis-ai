# Workspace 真实研发工具 E2E｜D1 Tenant Reservation 安全 Review

- Issue：`issues/20260718_workspace_real_rd_tool_e2e_d1_tenant_reservation.md`
- 结论：`PASS`（仅输入/输出与工具边界契约；不授权模型调用）
- 复核范围：仅 `tools/verify_d1_tenant_reservation.py`、`backend/tests/test_d1_verify_script.py`

## 固定输入与敏感边界

- 唯一工作区：`/Users/yy/Documents/Curis AI Workspace`。
- 模型可见文件严格为上述两份文件；读取顺序固定，禁止目录扫描、上下文扩展、读取 `backend/app`、数据库、部署文件、`.git`、环境变量或任何其他路径作为模型输入。
- 当前两份文件仅含本地 D1 验证代码与测试；已做敏感模式核对，未发现 API key、secret、password、Cookie、Authorization、Bearer、JWT、credential 或私钥文本。
- 发送前仍必须对路径、正文和组合 Prompt 做敏感扫描；命中凭据/Token/Cookie/JWT/Authorization/私钥格式时整体拒绝，不做部分脱敏后继续发送。

## 模型出站最小化

- 本 Review 不授权模型调用；总控另行批准前不得启动、注 Key、出网、写文件或运行测试。
- 获得独立模型 Gate 后，唯一请求内容只能是两份文件的相对路径标签、正文和固定修复目标；不得加入环境、数据库、Git、历史对话、凭据、隐藏 Prompt 或其他文件内容。
- 唯一外部出口只能复用后续总控批准的既有 Model Gateway；禁止直连 Provider、第二 Provider、Fallback、重试、网络搜索、Connector 或任意外部服务。
- Prompt、完整代码正文、模型原始输出、Authorization、Key、Cookie、Token 和环境变量不得写日志、审计、Issue、Review 或数据库。

## 模型输出到 diff 的唯一边界

- 模型输出必须是原始 unified diff；禁止 Markdown 围栏、解释文字、命令、脚本、Base64、二进制 patch 或多个候选 diff。
- 仅允许修改 `tools/verify_d1_tenant_reservation.py`；`backend/tests/test_d1_verify_script.py` 只能读取，其他路径一律拒绝。
- diff 总大小最多 4 KiB；必须通过相对路径、规范化、普通文本、preimage SHA-256、hunk 范围和敏感扫描校验。
- 禁止新增/删除/重命名目录或文件、符号链接、文件模式变化、`..`、绝对路径、子模块、任意命令、网络调用、凭据读取和数据库/部署路径访问。
- 任何解析失败、路径越界、preimage 不匹配、diff 超限、敏感命中、审计不可写或输出含非 diff 内容，均在写入前拒绝；不允许 partial apply。写入必须原子化，失败整体回滚。

## 受控 Tool 链

仅允许既有五个 Tool 中的受控动作：

1. File Reader：读取两份固定文件；不允许额外路径。
2. Code/Docs Search：仅在两份固定文件内做有界字面搜索；不扩展仓库。
3. File Writer：只接受上述 4 KiB unified diff，唯一写入目标为脚本文件。
4. Test Runner：只允许 `command_id=rd_e2e_verify_d1_tenant_reservation`，精确 argv 为：
   `backend/.venv/bin/python -m pytest -q backend/tests/test_d1_verify_script.py`；固定 cwd 为工作区；不得接受额外参数、Shell、环境覆盖或第二条命令。
5. Git Client：只读 `diff` / `diff --check`，仅查看唯一脚本路径；禁止 stage、commit、push、reset、checkout、clean、remote 或网络。

工具链不得记录文件正文、Prompt、模型原文或命令原文。所有工具 Usage 固定为 `model_call=0`、`cost_source=local_tool_no_model`；本地工具不产生模型 Token/成本，不得伪造模型成功或成本。

## 结论边界

- 安全 PASS 允许系统交付席实现/验证本 D1 小 E2E 的输入、diff、测试和 Git 只读护栏；不允许其自行启动模型或出网。
- 质量席必须独立确认仅两份输入、唯一脚本 diff ≤4 KiB、唯一 pytest、Git 只读、无网络/凭据/额外写入、审计脱敏和环境停机。
- 模型 Provider/Model/Gateway、凭据隐藏注入、Token/成本、单次调用和停机方式必须另经总控 Gate；Provenance Step1 仍保持 `PAUSED_BY_NEW_PRIORITY`。

Handoff: sent to 产品规划席
