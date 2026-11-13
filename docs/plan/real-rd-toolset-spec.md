# 研发部最小真实工具集 · 产品规格（PRD-lite）

> **文档性质**：产品规格（PRD-lite）。只定义资产与绑定目标，不写代码、不改 `database.py`、不改测试、不碰 Workspace 文件。
> **分工边界**：Codex（Workspace 侧）负责 Tool 的真实执行与真实研发 E2E；**我们（WorkBuddy / Admin）负责官方 Tool 目录、模板、绑定与能力态**——即把这批最小真实工具作为官方资产登记进 `tool_templates`，标为可执行（`executable=1` / `mock_or_stub=0`），并绑定到官方研发工作流与研发员工。
> **对齐依据**：全部命名与机制均读自 `backend/app/database.py` 现有种子与建表代码（见 §2 各 `file:func/line` 指针）。

---

## 0. 结论一句话

**只做 6 个带 `_real` 后缀的研发工具（文件读取 / 代码搜索 / 受控代码修改 / 运行测试·Build / Git Diff / Tool 审计+成本），把它们以 `executable=1, mock_or_stub=0` 登记进官方 `tool_templates`，并通过既有的 `employee_capability_bindings` 表绑定到 `official.employee.*` 研发员工与 `official.workflow.software_rnd_sop` 工作流；最终用 Codex 在 Workspace 跑通的一个真实小 Issue 证明 AI 能「读代码 → 改代码 → 跑测试 → 出 Diff → 记审计」。** 这 6 个工具与现有 115 个空壳工具靠 `_real` 后缀 + 能力态列彻底区分。

---

## 1. 范围边界

### 1.1 做（本规格）
- 定义 6 个最小真实研发工具的资产规格（ID、用途、输入/输出、目标能力态）。
- 明确绑定目标：官方研发工作流 `official.workflow.software_rnd_sop` + 官方研发员工 `official.employee.*`（department_type=`software_rnd`）。
- 明确绑定机制：沿用既有 `employee_capability_bindings` 表（官方多对多能力绑定表），辅以员工 `default_tool` 字段。
- 明确与 115 个 mock 工具的区分方式（命名 + 能力态列）。
- 明确验收标准（含最终真实小 Issue 的通过条件）。

### 1.2 不做（明确排除）
- ❌ 不实现 115 个 Tool，只做上述 6 个。
- ❌ 不改 `backend/app/database.py`、不改测试、不碰 Workspace 文件（本规格仅产出本文档）。
- ❌ 不新增绑定表或新字段；完全复用既有 `tool_templates` / `employee_capability_bindings` 结构。
- ❌ 不改动 `official.workflow.software_rnd_sop` 的 `steps_json` 结构（工作流步骤只引用 `employee_role`，不引用 tool id，见 §2.3）。
- ❌ 不在本文档内写任何执行逻辑；真实执行由 Codex 在 Workspace 侧落地。

---

## 2. 现状对齐（读自现有代码，指向具体位置）

### 2.1 `tool_templates` 表字段与能力态列
- **建表**：`backend/app/database.py:2038`（`_seed_tool_templates` 内 `create table if not exists tool_templates`）。
  - 基础列：`tool_template_id`(PK)、`slug`、`name`、`description`、`tool_type`、`default_capability_types_json`、`instruction_excerpt`、`source`、`tenant_id`、`status`、`version`、`created_at`、`updated_at`。
  - 命名前缀：**官方研发包统一用 `tl_ai_rd_*`**（见 §2.2）。
- **能力态列（P1-1 后补）**：`backend/app/database.py:1257-1276`（`_ensure_column` 范式）。四列含义：
  - `enabled`：默认 1，供只读投影统一选取。
  - `catalog_visible`：目录可见，默认 1。
  - `configured`：凭证/环境变量就绪，默认 0。
  - `executable`：可真实执行，默认 0。
  - `mock_or_stub`：Mock/Stub 占位，默认 1。
  - **不变量**：`executable` 与 `mock_or_stub` 互斥（NOT 同时为真）——见 `backend/app/database.py:1253` 注释。

### 2.2 现有 115 个 mock 工具的命名规律
- **种子清单**：`backend/app/database.py:2059-2180`（变量 `tools`，共 **115 条** = 30 ai_rd + 16 Pack A + 15 Pack C + 14 Pack D + 12 Pack E + 28 Pack F-J）。
- **官方研发包（前 30 个，`tl_ai_rd_*`）** 关键示例（ID 即本文档 6 个真实工具的对标对象）：
  - `tl_ai_rd_code_executor`（`backend/app/database.py:2059`）
  - `tl_ai_rd_file_reader`（`backend/app/database.py:2064`，文件读取）
  - `tl_ai_rd_directory_search`（`backend/app/database.py:2066`，按名/模式搜文件，非内容 grep）
  - `tl_ai_rd_code_docs_search`（`backend/app/database.py:2075`，向量检索，非 grep）
  - `tl_ai_rd_test_runner`（`backend/app/database.py:2063`，测试运行）
  - `tl_ai_rd_git_client`（`backend/app/database.py:2067`，Git 客户端）
  - `tl_ai_rd_code_linter`（`backend/app/database.py:2062`，代码检查）
- **全量默认态（空壳根因）**：`backend/app/database.py:2263-2277`（`_annotate_tool_capability`）——一条幂等 UPDATE 把全部 115 个工具刷成 `catalog_visible=1, configured=0, executable=0, mock_or_stub=1`。即「目录可见 + Mock/Stub、未配置未执行」。

### 2.3 现有「工具如何绑定到工作流/员工」的机制（如实描述，不臆测）
现有机制有**两条互补路径**，且**工作流步骤本身不直接引用 tool id**：

- **路径 A — 员工 `default_tool` / `default_skill` 字段**
  - 列定义：`backend/app/database.py:1123-1124`（`employee_templates.default_skill` / `default_tool`，快照进 `employee_instances`）。
  - 已有范式：`backend/app/database.py:2661`（`_seed_employee_templates_phase1` 中 `et_qa_engineer` → `default_tool="tl_ai_rd_test_runner"`）。
  - 执行时取值：`backend/app/rd_workflow_runtime.py:216-217`（`_execute_step` 读 `employee["default_skill"]` / `employee["default_tool"]`）。

- **路径 B — `employee_capability_bindings` 多对多绑定表（推荐用于本规格）**
  - 表定义：`backend/app/database.py:680-694`。关键列：`employee_id`、`employee_template_id`、`capability_source`(official/tenant_private)、`capability_type`(model/tool/connector)、`capability_id`、`priority`、`enabled`。唯一约束 `(tenant_id, employee_id, capability_source, capability_type, capability_id)`。
  - 管理 API：`backend/app/employee_templates.py:372-446`（`set_employee_capability_bindings` / `list_employee_tool_bindings` / `set_employee_tool_bindings`）。`set_employee_tool_bindings` 会把 `capability_type` 强制写为 `'tool'`。
  - 取值优先级：`employee_templates.py:448`（`preferred_capability_for_employee`，按 `priority` 取 enabled=1 的首条）。

- **工作流步骤的引用方式（关键）**
  - 官方研发 SOP 种子：`backend/app/database.py:1900-1972`（`_seed_workflow_runtime_contract`，id=`official.workflow.software_rnd_sop`）。
  - `steps_json` 的每一步只含 `step_order`、`step_type`、`step_name`、`employee_role`（如 `"tech_lead"`）、`required_capability_types`（如 `["model"]`）——**不引用任何 tool id**。
  - 工作流能力态标注：`backend/app/database.py:2322-2340`（`_annotate_workflow_capability`）把该工作流显式提升为 `structured_executable`。
  - 部门默认指向：`backend/app/database.py:1883-1898`（`official.department.software_rnd` 的 `default_workflow_template_id='official.workflow.software_rnd_sop'`，`default_employee_templates_json` 含 6 个 `official.employee.*`）。

> **结论给架构师**：本规格的真实工具**不需要、也不应该改动 `steps_json`**。绑定发生在「员工层」——把真实 tool id 写进 `employee_capability_bindings`（或 `default_tool`），工作流按 `employee_role` 路由到该员工，员工再以其绑定/默认工具执行。这是现有闭环的真实路径。

### 2.4 现有审计 / 成本基建（供 `usage_audit_real` 对标）
- **`usage_event`（按执行记 token/成本，带敏感字段脱敏）**
  - 写入：`backend/app/result_store.py:570`（`_record_usage_events(task_id, tool_name, cost, usage)`）。
  - 读取/投影：`backend/app/evolution_event_log.py:75`（`list_usage_events`）、`:124`（`_usage_event_from_row`，只投影固定字段，顶层不含 api_key/token/secret）。
- **`tool_traces`（按步记每次工具调用的输入/输出/错误）**：`backend/app/database.py:223-232`。
- **`tool_performance`（按工具聚合成功/失败/延迟/成本）**：`backend/app/database.py:283-292`（含 `total_cost`）。
- **`workflow_metrics`（按工作流聚合成本/工具链）**：`backend/app/database.py:294-303`（含 `total_cost`）。

> 即审计与成本归因能力**已有底座**，真实工具只需在真实执行后正确写入上述表即可，无需新建表。

---

## 3. 最小真实研发工具集（6 个）

> 命名规则：在既有 `tl_ai_rd_*` 基础上加 `_real` 后缀，明确区别于 115 个 mock 工具。
> 统一目标能力态：`catalog_visible=1, configured=1, executable=1, mock_or_stub=0`（即「目录可见 + 已配置 + 真实可执行 + 非 Mock」）。
> `source='official'`、`tenant_id='platform'`、`status='active'`、`version='1.0.0'`（与 `_seed_tool_templates` 写入口径一致，见 `database.py:2181-2189`）。

### 3.1 `tl_ai_rd_file_reader_real` — 文件读取（read project file）
- **用途**：按路径读取项目内单个文件内容（受项目根目录范围约束）。
- **输入**：`{ "path": "backend/app/database.py", "encoding?": "utf-8" }`
- **输出**：`{ "content": "<文件全文>", "bytes": 12345, "exists": true }`
- **目标能力态**：`catalog_visible=1, configured=1, executable=1, mock_or_stub=0`
- **对标 mock**：`tl_ai_rd_file_reader`（`database.py:2064`）。

### 3.2 `tl_ai_rd_code_search_real` — 代码搜索（grep/search across repo）
- **用途**：跨仓库按正则/字符串检索代码内容，返回匹配文件与行（区别于 `tl_ai_rd_directory_search` 的「按名/模式找文件」与 `tl_ai_rd_code_docs_search` 的「向量检索」）。
- **输入**：`{ "pattern": "def _seed_tool_templates", "path?": "backend/", "glob?": "*.py", "max_results?": 200 }`
- **输出**：`{ "matches": [ { "file": "...", "line": 2030, "text": "..." } ], "count": 3 }`
- **目标能力态**：`catalog_visible=1, configured=1, executable=1, mock_or_stub=0`
- **对标 mock**：无完全对应项（现有 `directory_search`/`code_docs_search` 语义不同），故为新增真实能力，ID 独立。

### 3.3 `tl_ai_rd_code_edit_real` — 受控代码修改（apply unified diff / targeted edit）
- **用途**：把统一的 unified diff 应用到项目文件；**必须含 dry-run 与范围校验**（仅允许改项目根目录内文件、禁止改 `database.py` 种子等被锁文件、禁止删除/外联）。
- **输入**：`{ "diff": "--- a/x.py\n+++ b/x.py\n@@ ...", "dry_run?": true, "allow_paths?": ["backend/app/"] }`
- **输出**：`{ "applied": true, "changed_files": ["..."], "rejected_hunks": [], "dry_run": false }`
- **目标能力态**：`catalog_visible=1, configured=1, executable=1, mock_or_stub=0`
- **对标 mock**：`tl_ai_rd_code_executor`（`database.py:2059`，沙箱执行，非受控编辑）。

### 3.4 `tl_ai_rd_test_build_real` — 运行测试 / Build（run test or build command）
- **用途**：在受控环境运行测试或构建命令，捕获退出码与输出（如 `pytest` / `npm test` / `npm run build`）。
- **输入**：`{ "command": "pytest backend/tests/test_x.py", "cwd?": "backend/", "timeout_ms?": 120000 }`
- **输出**：`{ "exit_code": 0, "stdout": "...", "stderr": "...", "passed": true }`
- **目标能力态**：`catalog_visible=1, configured=1, executable=1, mock_or_stub=0`
- **对标 mock**：`tl_ai_rd_test_runner`（`database.py:2063`）。

### 3.5 `tl_ai_rd_git_diff_real` — Git Diff 输出（produce diff of changes）
- **用途**：产出当前工作区相对 HEAD（或某 base 分支）的 unified diff，作为交付物。
- **输入**：`{ "base?": "HEAD", "cached?": false, "paths?": ["backend/app/"] }`
- **输出**：`{ "diff": "diff --git ...", "files_changed": 2, "insertions": 12, "deletions": 3 }`
- **目标能力态**：`catalog_visible=1, configured=1, executable=1, mock_or_stub=0`
- **对标 mock**：`tl_ai_rd_git_client`（`database.py:2067`，通用 Git 客户端，非专门 Diff 输出）。

### 3.6 `tl_ai_rd_usage_audit_real` — Tool 审计 + Token/成本记录（record tool usage, token & cost）
- **用途**：在研发动作完成后，采集本次会话/任务的工具使用记录、Token 消耗与成本，并写入既有审计表（`usage_event` / `tool_performance` / `workflow_metrics`），供归因与计费准备。
- **输入**：`{ "task_id": "...", "tool_name": "tl_ai_rd_code_edit_real", "usage": { "prompt_tokens": 120, "completion_tokens": 30 }, "cost": 0.002 }`
- **输出**：`{ "recorded": true, "usage_event_id": "...", "attributed_tool": "tl_ai_rd_code_edit_real" }`
- **目标能力态**：`catalog_visible=1, configured=1, executable=1, mock_or_stub=0`
- **对标基建**：复用 `result_store.py:570`（`_record_usage_events`）与 `evolution_event_log.py:75`（`list_usage_events`），**不新建表**。

---

## 4. 绑定目标与绑定机制

### 4.1 绑定目标
- **工作流模板**：`official.workflow.software_rnd_sop`（`database.py:1967`，已是 `structured_executable`）。
- **研发员工 / persona**：`official.employee.*`（基线 6 个，`department_type='software_rnd'`，种子见 `database.py:1765-1882`）：
  - `official.employee.tech_lead`、`official.employee.product_manager`、`official.employee.architect`、`official.employee.frontend_engineer`、`official.employee.backend_engineer`、`official.employee.qa_engineer`。
  - （备选/同源：`et_*` Phase-1 模板，`database.py:2614-2663`，同样 `software_rnd`，已带 `default_tool` 范式。）
- **部门容器**：`official.department.software_rnd`（`database.py:1883-1898`，`default_workflow_template_id` 已指向该 SOP）。

### 4.2 绑定机制（推荐：路径 B `employee_capability_bindings`）
- 对每个真实工具，在 `employee_capability_bindings`（`database.py:680`）插入行：
  - `capability_source='official'`、`capability_type='tool'`、`capability_id=<上述 6 个 _real tool id>`、`enabled=1`、`priority`（建议 coding 类 100，audit 类 90）。
  - 通过既有 API `set_employee_tool_bindings`（`employee_templates.py:432`）写入即可，**不改动 `database.py` 种子**。
- **建议的员工↔工具映射**（沿 `steps_json` 的 `employee_role` 收敛到真实执行者）：
  - `backend_engineer` / `frontend_engineer` → `file_reader_real`、`code_search_real`、`code_edit_real`、`test_build_real`、`git_diff_real`（编码/测试步骤）。
  - `architect` → `code_search_real`、`file_reader_real`（设计阶段只读探索）。
  - `qa_engineer` → `test_build_real`、`git_diff_real`（验收步骤）。
  - `tech_lead` → `usage_audit_real`（汇总交付证据时记审计）。
- **辅助（可选，路径 A）**：如希望某员工有单一默认工具，可设其 `employee_templates.default_tool`（列见 `database.py:1124`），范式同 `et_qa_engineer → tl_ai_rd_test_runner`（`database.py:2661`）。但**主路径用 B**，便于一个员工绑定多个真实工具且可优先级排序。

### 4.3 为什么不必改 `steps_json`
- 工作流步骤只按 `employee_role` 路由（§2.3），真实工具是通过「员工→工具」绑定到达的。只要 `official.employee.*` 已绑定上述 `_real` 工具，SOP 跑编码/测试/验收步骤时自然落到真实工具，无需触碰 `official.workflow.software_rnd_sop` 的 `steps_json`。

---

## 5. 与现有 115 个 mock 工具的区分方式

| 维度 | 现有 115 mock 工具 | 本规格 6 个真实工具 |
|---|---|---|
| ID 命名 | `tl_ai_rd_*`（及 `tl_*` Pack A–J） | `tl_ai_rd_*_real`（显式 `_real` 后缀） |
| `catalog_visible` | 1 | 1 |
| `configured` | 0 | **1** |
| `executable` | 0 | **1** |
| `mock_or_stub` | 1 | **0** |
| `source` / `tenant_id` | `official` / `platform` | 同（官方资产） |
| 绑定 | 未绑定 / 仅挂 `default_tool` 占位 | 经 `employee_capability_bindings` 绑定到 `official.employee.*` |
| 执行结果 | scaffold 降级（见 `rd_workflow_runtime.py:236-243`） | 真实读/改/跑/出 Diff/记审计 |

- **能力态不变量**：`executable` 与 `mock_or_stub` 互斥（`database.py:1253` 注释），真实工具必须 `executable=1 AND mock_or_stub=0`。
- **可查询区分**：列表/投影时以 `mock_or_stub=0 AND executable=1` 过滤即可得到「真实可执行工具集」，与 115 空壳天然隔离。

---

## 6. 验收标准（最终真实小 Issue 的通过条件）

### 6.1 资产层验收（本规格交付物，WorkBuddy/Admin 侧）
- **A1**：6 行 `tl_ai_rd_*_real` 均存在于 `tool_templates`，且能力态为 `catalog_visible=1, configured=1, executable=1, mock_or_stub=0`。
- **A2**：每个 `_real` 工具均通过 `employee_capability_bindings`（`capability_type='tool', enabled=1`）绑定到至少一个 `official.employee.*` 研发员工。
- **A3**：`official.workflow.software_rnd_sop` 经员工绑定可达真实工具（编码/测试/验收步骤不再仅 scaffold 降级）。
- **A4**：`tl_ai_rd_usage_audit_real` 真实执行后会写入 `usage_event`（脱敏）与 `tool_performance.total_cost`，使成本/Token 可按工具归因。

### 6.2 E2E 验收（真实小 Issue，Codex 在 Workspace 跑，仅说明通过条件）
用一个**真实小 Issue**（如「给 `tool_templates` 某处补一行注释并跑通对应测试」）证明闭环：
1. **读**：AI 用 `file_reader_real` / `code_search_real` 读取并定位代码。
2. **改**：AI 用 `code_edit_real`（先 dry-run 通过范围校验）应用修改。
3. **验**：AI 用 `test_build_real` 运行测试/Build，结果 `exit_code=0`。
4. **出**：AI 用 `git_diff_real` 产出相对 base 的 unified diff（有内容、文件数>0）。
5. **记**：AI 用 `usage_audit_real` 写入 `usage_event`，`cost>0` 或 `token>0` 且 `attributed_tool` 指向 `_real` 工具。
6. **通过条件**：上述 5 步全程 `executable=1`（无 mock 降级）、测试绿、diff 非空、审计记录存在且可查。即「AI 研发部能真开发」从 R3 的「工作流能跑」升级为「真实工具闭环能交付」。

---

## 7. 给架构师的实施入口（指向代码）
- 工具资产登记位置（仿写口径）：`backend/app/database.py:2038`（`_seed_tool_templates` 建表与 `tools` 数组），新增 6 行 `_real` 并随后在 `_annotate_tool_capability` 之后单独 UPDATE 为 `executable=1, mock_or_stub=0, configured=1`（或直接加一个 `_seed_real_rd_tools` 后钩子，形态同 `database.py:1277` 之后的 `_backfill_tool_security`）。
- 绑定写入 API：`backend/app/employee_templates.py:432`（`set_employee_tool_bindings`）。
- 工作流/员工/部门既有种子：`database.py:1765`（`_seed_employee_template_contract`）、`:1883`（`official.department.software_rnd`）、`:1900`（`_seed_workflow_runtime_contract`）、`:2614`（`_seed_employee_templates_phase1`）。
- 执行取值点：`backend/app/rd_workflow_runtime.py:216-217`。
- 审计/成本底座：`backend/app/result_store.py:570`、`backend/app/evolution_event_log.py:75`、`backend/app/database.py:223/283/294`。

> 注：本文档只定义规格，不执行上述任何改动；具体实现由架构师据此落地，真实执行与 E2E 由 Codex 在 Workspace 侧完成。
