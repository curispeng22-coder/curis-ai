# Workspace 最小真实研发工具集安全 Review

- Issue：`issues/20260718_workspace_minimal_rd_toolset_implementation.md`
- 结论：`PASS`（仅安全契约；不授权模型、网络、凭据、前端或 115 Tool 批量实现）
- 安全席：安全边界席

## 批准对象

仅允许以下五个 Tool ID，其他 Tool 保持 mock：

- `tl_ai_rd_file_reader`
- `tl_ai_rd_code_docs_search`
- `tl_ai_rd_file_writer`
- `tl_ai_rd_test_runner`
- `tl_ai_rd_git_client`

## 工作区与路径边界

- 唯一工作区根目录固定为 `/Users/yy/Documents/Curis AI Workspace`；启动时解析真实路径并拒绝根目录变化、符号链接、硬链接、绝对路径、`..`、NUL 字节和根目录外路径。
- 每次调用必须使用当前批准 Issue 提供的相对路径 allowlist；工具不得自行扩展到整个仓库。
- 文件读取、搜索、补丁均只允许普通文本文件；拒绝二进制、设备、FIFO、目录和符号链接。
- 禁止路径：`.git/`、`.env`/`.env.*`、`data/`、`deploy/`、`.ssh/`、`.aws/`、`.kube/`、`node_modules/`，以及名称或扩展名命中 `secret`、`credential`、`token`、`cookie`、`password`、`key`、`*.pem`、`*.crt`、`*.p12`、`*.pfx`、`*.jwk`、`*.sqlite`、`*.sqlite3`、`*.db` 的文件；命中即拒绝，不返回内容。
- 单次读取文件不超过 1 MiB；搜索最多扫描 512 KiB、返回 200 个匹配；超限 fail-closed。

## 五个动作的固定契约

### 1. File Reader / Code Docs Search

- Reader 只读一个 allowlist 内相对文件；Search 只做有界 UTF-8 文本字面搜索，模式不超过 256 bytes；禁止任意代码、Shell、正则执行或目录遍历。
- 输出只返回相对路径、行号和经敏感值扫描/脱敏后的短片段；发现疑似凭据、JWT、Cookie、Authorization 或密钥格式时整体拒绝该结果。
- 读取/搜索不得产生写入、子进程、网络或 Usage 模型事件。

### 2. File Writer

- 只接受受控 unified diff；diff 总大小不超过 128 KiB、最多 10 个文件，路径必须同时满足 allowlist 和根目录约束。
- 只允许普通文本文件新增/修改；禁止删除、重命名、目录操作、符号链接、文件模式变化、二进制 patch、子模块、绝对路径、`..` 和任意命令。
- 应用前校验 preimage SHA-256、目标路径与语法；任一不符立即拒绝。应用使用临时文件 + 原子替换，审计失败或异常时回滚，不产生部分写入。
- diff、输入、文件正文和失败上下文不得写入审计或日志。

### 3. Test Runner

- 只接受当前独立真实小 Issue 预先登记的 `command_id`，不接受命令字符串、Shell 脚本或任意参数。
- 唯一命令族为既有项目命令的精确 argv：`backend/.venv/bin/python -m pytest -q <Issue 明列的测试路径>` 与 `backend/.venv/bin/python -m compileall -q backend/app`；测试路径必须是 allowlist 内的 `backend/tests/test_*.py`。
- 子进程使用固定 cwd、净化环境、无网络、无凭据继承、无 Shell；超时 120 秒、输出 64 KiB，超时或异常杀掉进程树并 fail-closed。
- 测试/Build 只产生工具临时目录内的中间物并在结束清理；不得写生产 DB、部署目录、`.git` 或工作区 allowlist 外路径。

### 4. Git Client

- 只允许只读 `status`、`diff`、`diff --check`，且仅针对 allowlist 路径；Git 元数据只能由该只读动作内部读取，不能经 Reader/Search 暴露。
- 禁止 stage、commit、push、pull、fetch、remote、branch、merge、rebase、reset、checkout、clean、config、hook、任意 Git 参数透传和网络操作。
- 输出仅保留相对路径、状态、受控 diff 与 hash；不得返回 `.git` 内容或敏感路径内容。

## 审计、Token/成本与 fail-closed

- 审计最小字段固定为：`tool_id`、`request_id`、`run_id`、`tenant_id`、`project_id`、`task_id`、相对路径或 `path_hash`、`preimage_hash`/`postimage_hash`、`command_id`、`outcome`、`failure_code`、`exit_code`、`duration_ms`、`timestamp`。
- 不记录文件正文、prompt、命令原文、环境变量、进程输出原文、凭据、Cookie、JWT、Authorization、subject 原文或 token 值；审计失败时动作不执行或事务回滚。
- 五个工具均为本地 `tool` 能力：不得访问 Provider/Model/Gateway、不得出网、不得产生 `usage.model_call`。若既有 Usage 投影必须记录，固定 `capability_type=tool`、`model_call=0`、`total_tokens=0`、`estimated_cost=0`、`cost_source=local_tool_no_model`；不得伪造模型成本。
- 未知 Tool、路径越界、敏感路径、非法 diff、未登记命令、任意 Git 写操作、网络/凭据继承、审计不可写或 scope 缺失均 fail-closed，且零业务副作用。
- Tool ID、tenant、project、task 和 per-run allowlist 必须由服务端/批准 Issue 固定；客户端不能切换工作区、租户、路径根、命令或审计归属。

## 验收与边界

- 系统交付席只可在本 Review PASS 后实现五个动作；focused 测试必须覆盖正向动作以及越界路径、敏感路径、非法 diff、任意命令、Git 写操作、网络/凭据继承和审计失败。
- 质量运行席独立验证真实本地链路，禁止模型、网络、凭据和 115 Tool 批量；验证后才可由产品规划席决定是否进入独立真实小 Issue。
- 本 Review 不授权最终 AI E2E、模型调用、外部服务、前端、Git 写入或任何未列 Tool。

Next Seat：产品规划席（读取本 PASS 后再交系统交付席）
Handoff: sent to 产品规划席
