# CURIS-V1-GAP1-AGENT-EXECUTOR-GENERALIZATION-20261007

## 1. 目标 / Objective

P2「GAP1 provider 泛化」第一切片（Owner 盘点决策 3：去除 canonical cycle 对 codex-cli 的硬绑定，启用 adapter 已支持的 claude_code/http/mcp/coze，M，含安全边界，不依赖外部订阅）。

现状调研（Implementation Truth，2026-10-07）：

- 实时 tenant_private agent 执行分支 [main.py:2055-2085](../backend/app/main.py) 硬编码两种 kind：`codex-cli`（CodexCliAdapter）与 `openai-compatible`（ModelGatewayAdapter）；其余 kind 一律 403 `configuration_rejected`。
- 泛化适配器早已存在但未接入实时执行路径：[capability_adapters.py](../backend/app/capability_adapters.py) 的 CliAdapter / HttpApiAdapter / McpAdapter（CapabilityAdapterFactory 仅被未挂主链路的 capability_resolver 消费；main.py 零引用）。
- Agent 品牌事实表 [ai_capability_registry.py](../backend/app/ai_capability_registry.py) `AGENT_ADAPTER_REGISTRY`：codex=LIVE；claude_code/trae/cursor/gemini_cli/github_copilot_cli/openclaw=RESEARCHED（含 commands 白名单事实）。
- coze 仅有 agent_conversion 导入清单契约，无执行适配器；其执行形态本质是带凭证的 HTTP API，可用本切片的 `http` kind 配置承接，不需要一方代码。
- RD/XHS/TTK 旧工作区对 codex-cli 的硬门（main.py:5208/5400/5573）属 legacy 清理范围（去留待产品裁定），**本切片不动**。
- 前端当前无 agent kind 配置 UI（私有能力仅 API 可达）；本切片**不改前端**。

本切片目标：把实时 agent 执行分派收敛为一个**带安全边界的 agent executor 分派器**，在保持 codex-cli / openai-compatible 行为字节级不变的前提下，新增三种实时可执行 kind：`local-cli`（白名单本地 CLI agent，如 claude/gemini）、`mcp`（stdio JSON-RPC MCP server）、`http`（通用 HTTP agent，承接 coze 等）。未知/不合法配置一律 fail-closed。不实现：Coze 一方适配器、legacy 工作区改动、前端 agent 配置页、analyst authoring/reports（P2 后续独立切片）。

- Authority Inputs：
  - Owner Decision：V1_APP_COMPLETION_INVENTORY §6 决策 3 与 §7 P2（REVIEW_REQUIRED 盘点中的 Owner 已决项）。
  - Implementation：[capability_adapters.py](../backend/app/capability_adapters.py)（T08 适配器抽象）、[agent_adapter.py](../backend/app/agent_adapter.py)（CodexCliAdapter + ADR-0046 intent 流）、AGENT_ADAPTER_REGISTRY、ADR-0046（computer access 不扩大）。
- Status: Draft → 实施后 Review。Disposition: REVIEW_REQUIRED。

## 2. Allowed Files / Directories

- `backend/app/agent_executor_dispatch.py`（**新增**：安全分派器，单一真源）
- `backend/app/main.py`（仅 2055-2085 tenant_private agent 分支最小替换 hunk，调用分派器；其余零改动）
- `backend/tests/test_agent_executor_dispatch.py`（**新增**）
- `artifacts/tasks/CURIS-V1-GAP1-AGENT-EXECUTOR-GENERALIZATION-20261007/**`
- 本 Issue、`docs/00_Context/CURRENT_STATE.md`、`docs/08_Change_Log/CHANGE_LOG.md`（仅追加）

禁止：capability_adapters.py / agent_adapter.py / ai_capability_registry.py 业务逻辑改动（仅允许 import；若实测必须微调，STOP 并登记追认）；前端任何改动；legacy RD/XHS/TTK 分支；数据库 schema；任何 shell=True；Git 写。

## 3. 验收证据 / Acceptance Evidence

1. 新分派器 `build_agent_executor(metadata, *, default_executor) -> executor`：
   - `codex-cli` → CodexCliAdapter，cwd/sandbox/computer_access_intent/timeout 语义与现状完全一致（回归 test_v1_m4_m5_continuous_delivery、test_codex_agent_backend 全绿）。
   - `openai-compatible` → ModelGatewayAdapter，现状语义不变。
   - `local-cli` → CliAdapter：`command` 必须精确命中 AGENT_ADAPTER_REGISTRY 全表 flatten 的 commands 白名单（单一真源，如 claude/gemini/copilot/trae-cli/openclaw/codex）；`args` 可选 list[str]（≤16 项、每项 ≤256 字符、仅 str）；不接受 metadata `cwd`（强制服务端工作目录，不接受租户指定路径）；timeout ≤900；`credentials_ref` 仅接受 `env:` 形态。
   - `mcp` → McpAdapter：`server_command` 经 shlex 解析后 argv[0] 必须命中同一白名单，参数规则同上；`tool_name` str ≤64。
   - `http` → HttpApiAdapter：`url` 仅 http/https（拒绝 file/ftp/空主机/非 str）；method 默认 POST；超时 ≤900；凭证 env: 形态。
   - 未知 kind、白名单外命令（bash/sh/zsh/python3/绝对路径/带路径分隔符/目录穿越）、非 str/越界 args → 抛配置拒绝异常（映射 403 configuration_rejected，与现状未知 kind 错误形态一致），**不创建子进程、不发请求**。
2. 安全：CLI/MCP 全程 argv 列表（subprocess 无 shell）；分片参数注入不可能产生 shell 解释；白名单为空或注册表缺失时 fail-closed；http 仅在显式配置时发起、零外发默认。
3. main.py 分派 hunk 替换后：codex-cli 成功/失败路径、openai-compatible 成功/401 路径、未知 kind 403 路径行为与替换前一致；新三类 kind 按 1 接通。
4. 测试：新增 pytest 覆盖 §1/§2 全分支（含用真实临时可执行桩文件验证白名单命令可跑、白名单外同名绝对路径被拒）；与 test_v1_m4_m5_continuous_delivery / test_codex_agent_backend / test_agent_adapter / test_ai_capability_registry 合跑全绿。
5. 前端零改动：node --test 全量维持 208/9 既有基线；eslint 不涉及；build 不要求重建（QA 如需浏览器只做回归面验证，不新增 UI）。
6. 独立 QA：隔离 sqlite + 隔离端口；用 /tmp 桩 CLI（白名单内命令名）与本地桩 HTTP server 真实跑通 local-cli/http 两类执行的端到端 HTTP 路径（复用 test_codex_agent_backend 的端点范式），mcp 用桩 stdio JSON-RPC server 跑通；白名单外命令端到端 403；零真实外发（forbidden provider 守卫 + 桩外 URL 零连接）；PREHASH=POSTHASH；受保护 DB 指纹前后一致。
7. 清理与登记：进程退出、端口释放、/tmp 删除；QA_REPORT + DEVELOPMENT_RETURN（含「不做项」：coze 一方适配器/前端配置页/analyst reports 的后续门）。

## 4. 输出

- agent_executor_dispatch.py + main.py 单 hunk + 新 pytest；
- `artifacts/tasks/CURIS-V1-GAP1-AGENT-EXECUTOR-GENERALIZATION-20261007/qa/QA_REPORT.md`、DEVELOPMENT_RETURN.md；
- Issue §6 Execution Record、CURRENT_STATE、CHANGE_LOG 追加。

## 5. Stop 条件

- 发现必须改动 capability_adapters.py / agent_adapter.py 业务逻辑才能接入 → STOP 登记（最小必要微调走追认，不静默改）。
- 发现实时执行链对 agent 结果有 codex 专属结构化契约（computer_access 快照等），泛化 kind 无法诚实满足 → 非 codex kind 明确降级为普通输出并在 title/结果中如实表达，不伪造 Agent 验证；若产品要求同质验证则 STOP 上报。
- legacy 工作区改动需求出现 → 不做，登记交 legacy 清理切片。

## 6. Execution Record

Status: Review · Authority Class: IMPLEMENTATION EVIDENCE · Disposition: REVIEW_REQUIRED（SLICE DONE / QA PASS，工程确认登记，待 Owner 接受）。

实施与独立 QA 完成（2026-10-07）。交付：`backend/app/agent_executor_dispatch.py`（新增安全分派器，五种 kind；`_LedgerIdentityMixin` 注入账本身份字段 provider_id=local-cli/mcp/http-agent，诚实类目不冒称厂商）、[main.py](../backend/app/main.py) 2055-2066 最小 hunk（tenant_private agent 分支收敛为一行 build_agent_executor 调用，其余零改动）、`backend/tests/test_agent_executor_dispatch.py`（34 用例）。证据：[QA_REPORT.md](../artifacts/tasks/CURIS-V1-GAP1-AGENT-EXECUTOR-GENERALIZATION-20261007/qa/QA_REPORT.md)、[DEVELOPMENT_RETURN.md](../artifacts/tasks/CURIS-V1-GAP1-AGENT-EXECUTOR-GENERALIZATION-20261007/DEVELOPMENT_RETURN.md)。

验收对照 §3 全过：分派器单测 34/34；Issue 点名五文件合跑 62/62；全量回归失败集与改动前精确基线 IDENTICAL（48 既有，零新增；首轮 51 含 3 个 writing_entry_readiness 子进程缺 PYTHONPATH 环境伪差，补正后 42/42）；独立 QA 隔离 sqlite/8027/8090 + /tmp 白名单桩 + forbidden 网关，full 45/45、冷重启 10/10、DB 探针 8/8（成功 4×1 条 usage / 拒绝 4×0 条）、零 5xx（被测路径）、零外发；POSTHASH 仅 2 个 Allowed 文件变化（QA 发现驱动），13 个受保护文件 identical；进程/端口//tmp 已清。

QA 过程登记（诚实）：①执行载体由 rd-workflow/run 切换为 Orchestrator 任务链（RealRDExecutor 的 usage/diff 契约会弹闸 zero-token 适配器结果，RD 专用契约非分派器缺陷）；②QA 发现 T08 适配器缺账本身份字段（provider_id / gateway_id / model_name 属性），修复落在本 Issue Allowed File（dispatch 模块 mixin），capability_adapters.py 零改动；③注册面只挡密钥形态（A1 422），结构合法但安全非法配置可注册、执行层 fail-closed（A2/A3 201 + A8/A9 400 零桩调用）——现行设计如实表达。

不做项（交后续门）：coze 一方适配器（http kind 承接）、前端 agent 配置页、legacy RD/XHS/TTK 硬门（需产品裁定）、analyst authoring/reports（GAP1 后续切片）、mcp tools 发现编排、真实 CLI 二进制语义（NOT RUN，无外部资源授权）。
