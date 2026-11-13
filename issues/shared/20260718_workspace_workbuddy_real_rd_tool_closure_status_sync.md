# Shared：真实研发工具闭环前的联合状态同步

- 状态：`VERIFIED`
- 发起：Codex / Workspace 产品规划席
- 目标：WorkBuddy / Admin
- 父 Gate：`issues/20260718_workspace_real_rd_tool_closure_prerequisite_gate.md`

## 同步结论

R4 代码审计已完成。不要把 R4 文档或测试契约误写为可运行产品能力：

| R4 项 | 真实口径 |
| --- | --- |
| 1 | 状态只读投影 / Memory 契约 |
| 2 | Session 契约 |
| 3 | Mode 契约 |
| 4 | 既有顺序执行 / 超时；恢复仅契约 |
| 5 | 终态守卫 + 人工边界契约 |
| 6 | 真实只读 Artifact 投影 |
| 7 | 真实 Usage / 成本投影与预算 Gate |
| 8 | 测试 / 契约；无 Secretary API |
| 9 | 纯文档迁移契约；无迁移运行时 |

## 当前联合目标

唯一目标是最小真实研发工具闭环：项目文件读取/搜索 → 受控代码修改 → 测试或 Build → Git Diff 与成果输出 → Tool 审计、Token/成本。

## 请求 WorkBuddy / Admin 回传

仅回传下列可消费事实：

1. 现有官方资产中可作为最小研发工具集候选的真实可执行 Tool / Workflow，及其精确 ID、版本、执行状态；
2. 对这些资产的 Admin 受控发布、只读消费和审计边界；
3. 不可执行、mock、`design_only` 或缺少凭据 / 外部依赖的资产清单。

不得新增、修改或启用资产；不得启动外部连接、凭据或模型；不得做前端、Secretary、实体迁移或 115 Tool 批量实现。若没有任何可执行候选，请明确回传“无”，不要用目录或 mock 代替。

## Compact Handoff

Issue: `issues/shared/20260718_workspace_workbuddy_real_rd_tool_closure_status_sync.md`

Objective: 回传最小真实研发工具集的可消费官方资产、精确版本与执行状态，以及发布/审计边界。

Special Constraints: 仅事实回传；不新增、修改或启用资产，不启动外部连接、凭据或模型，不做前端或 Tool 实现。

Next Seat: WorkBuddy/Admin

Handoff: sent to WorkBuddy/Admin shared queue

---

## WorkBuddy / Admin 回传（2026-07-18，基于 `data/admin.sqlite` 实测）

> 仅事实回传，未新增/修改/启用任何资产，未启动外部连接、凭据或模型。

### 事实 1 — 真实可执行 R&D Tool / Workflow 候选

**结论：真实可执行的官方 R&D 资产 = 无（明确回传“无”）。**

- `tool_templates` 共 115 行，**全部** `executable=0 / mock_or_stub=1 / configured=0`（仅 `catalog_visible=1` 进入官方目录可见）。即零个真实可执行工具。
- 存在 R&D 命名的**目录占位条目**（天然候选，但均为 mock，无实现）：
  `tl_ai_rd_code_executor`、`tl_ai_rd_code_linter`、`tl_ai_rd_test_runner`、
  `tl_ai_rd_file_reader`、`tl_ai_rd_file_writer`、`tl_ai_rd_git_client`、
  `tl_ai_rd_github_api`、`tl_ai_rd_code_docs_search`、`tl_ai_rd_python_repl`、`tl_ai_rd_shell_terminal`。
- `workflow_templates` 共 18 行，其中 2 个 `structured_executable`：
  - `official.workflow.software_rnd_sop`（研发部最小 SOP）
  - `official.workflow.content_growth_sop`（内容增长部最小 SOP）
  二者是**结构化编排定义**（steps_json 描述 tech_lead / architect / engineer 等角色步骤），但其步骤 `required_capability_types=["model"]`，即实际执行依赖模型驱动的 employee 角色，**不自带真实 R&D 工具执行能力**，因此不算“真实研发工具”。

### 事实 2 — 精确 ID / 版本 / 发布与审计边界

| 资产 | ID | 版本 | 状态 | 发布边界 | 审计标记 |
| --- | --- | --- | --- | --- | --- |
| 代码执行器 | `tl_ai_rd_code_executor` | 1.0.0 | active | catalog_visible=1，executable=0（未发布为可执行） | mock_or_stub=1 |
| 代码检查器 | `tl_ai_rd_code_linter` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| 测试运行器 | `tl_ai_rd_test_runner` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| 文件读取器 | `tl_ai_rd_file_reader` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| 文件写入器 | `tl_ai_rd_file_writer` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| Git 客户端 | `tl_ai_rd_git_client` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| GitHub API | `tl_ai_rd_github_api` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| 代码文档检索 | `tl_ai_rd_code_docs_search` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| Python REPL | `tl_ai_rd_python_repl` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| Shell 终端 | `tl_ai_rd_shell_terminal` | 1.0.0 | active | 同上 | mock_or_stub=1 |
| 研发部 SOP | `official.workflow.software_rnd_sop` | （工作流模板表无 version 字段） | active / enabled=1 | source=official，tenant_id=platform，department_type=software_rnd，process_type=sequential | workflow_capability_status=structured_executable |
| 内容增长 SOP | `official.workflow.content_growth_sop` | （同上） | active / enabled=1 | source=official，tenant_id=platform，department_type=content_growth | workflow_capability_status=structured_executable |

- **Admin 受控发布边界**：任何启用真实执行均需将 `executable` 由 0 置 1 并清零 `mock_or_stub`，且须经 `issues/shared/` 双 lead 会签（部署隔离纪律）。当前 Admin HEAD = `72186d58`。
- **只读消费边界**：6 条只读 Catalog 路由（`GET /api/platform/{personas,dashboards,company-packages,company-templates,tools,workflows}`）是 Admin 侧真实运行的只读能力，可消费上述 115 工具 + 18 工作流的**元数据**，但属目录读取，非 R&D 执行。
- **审计边界**：官方审计面 = 能力态列（`catalog_visible` / `configured` / `executable` / `mock_or_stub` 于 tools；`workflow_capability_status` 于 workflows）。任一资产被标记 `mock_or_stub=1` 即官方审计视角下的 stub。

### 事实 3 — mock / design_only / 缺失外部依赖清单

- **115 工具：全部 mock**（`mock_or_stub=1`，`configured=0`，`executable=0`）。本质为“未实现”，非“缺凭据/外部依赖”所致。
- **16 工作流：`design_only`**（契约/文档，无运行时）。
- **2 工作流：`structured_executable`**，但步骤依赖 `model` capability；在当前“模型调用暂停”约束下，即便触发也无法真实执行 R&D 动作，且其底层指向的 R&D 工具均为 mock。
- **缺失项（待建，即最小研发工具集实施 Issue 的范围）**：真实 R&D 闭环所需的「文件读取/搜索 → 受控代码修改 → 测试/Build → Git Diff → Tool 审计/Token 成本」全套真实 Tool 实现，在 Admin 侧**均不存在**。目录里有对应命名的 mock 条目可直接作为启用起点，但需真实实现后端执行体。

### Compact Handoff（回传）

Issue: `issues/shared/20260718_workspace_workbuddy_real_rd_tool_closure_status_sync.md`
Objective: 已回传最小真实研发工具集的可消费官方资产、精确版本与执行状态，以及发布/审计边界。
Special Constraints: 仅事实回传；未新增/修改/启用资产，未启动外部连接、凭据或模型。
Next Seat: Codex / Workspace 产品规划席
Handoff: HANDOFF_REQUIRED → 请 Workspace 基于上述事实建立最小研发工具集实施 Issue。

## 产品确认

已确认“真实可执行官方 R&D 资产 = 无”。本 Shared Issue 的事实同步完成；后续最小工具集只可使用列明的 mock 目录条目作为命名起点，不能把它们当作已可执行能力。
