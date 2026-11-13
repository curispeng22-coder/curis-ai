# EvoFlow 复用评审 · 实际仓库映射与能力归类修正

> 历史工程映射资料。当前产品形态、EvoFlow 借鉴边界与开发顺序以 `curis-product-completion-roadmap-evoflow-2026-08-10.md` 为准；本文件仅在获授权的 Runtime Issue 中提供技术参考。

> 日期：2026-08-04
> 依据：`docs/architecture-review-evoflow-reuse-2026-08-04.md`（架构评审，其 §5 文件路径为「假设」）
> 目的：把评审的假设路径/表名映射到 **Curis 实际仓库**，并基于实际代码完成 effect_class 归类（评审待确认问题 5）。
> 结论预览：评审四项结论可保留，但**工程量估计偏高**——实际仓库已有 DAG 任务图、返工/换能力计数与 trace 字段，四项大部分是「在已有基座上扩展字段/表」，不是「新建架构层」。

---

## 1. 关键发现：评审假设 vs 实际仓库

| 评审假设 | 实际仓库 | 结论 |
|---|---|---|
| Curis「无图编排引擎」，检查点须自建 | `backend/app/task_graph.py` **已有完整 DAG**：ready_nodes / topo_order / is_complete + TaskNode 状态机（pending→ready→running→review→approved→done/failed）+ 可序列化（to_dict/from_dict） | 评审低估；2.3 检查点是**序列化基座已存在**上的扩展 |
| 无技术层返工支撑 | TaskNode 已内置 `rework_count` / `cap_switch_count` / `attempts` / `capability_path`（实际尝试能力链含降级）/ `trace`（pipeline 维度可观测） | 返工计数与降级追踪**已存在**；2.2/2.4 是补「验收字段」与「独立事件表」 |
| 无独立网关 | `model_gateway.py`（ModelGatewayAdapter 9 方言）+ `d1_gateway_client.py` + Step5 已交付 | 网关能力已交付（评审撰写时未含最新能力） |
| 「后端 7 项能力」 | 能力注册表 10 类（model/agent/skill/tool/workflow/connector/cli/api/webhook/mcp）+ 官方目录（ct_/dt_/et_/pt_/skl_/tl_/wt_）+ tenant_private 模型/Agent/工具 + 运行时工具（tl_ai_rd_*）+ 引导/经营日新服务 | 能力面远超 7 项，effect_class 归类须全量覆盖 |

**结论**：评审的「部分立项（3.5/4）」判定与优先级（②>①>④>③）仍成立，但四项的落地形态应从「新建模块」改为「**扩展既有模块**」，实现顺序可更快。

---

## 2. 评审 §5 假设路径 → 实际仓库映射

| 评审假设路径 | 实际文件 | 备注 |
|---|---|---|
| `backend/app/capabilities/registry.py`（改） | `backend/app/capability_registry.py`（改） | 已是 APIRouter 模式；`REGISTRY_TYPES` 10 类 |
| `backend/app/capabilities/router.py`（改，挂阶段门钩子） | `backend/app/capability_resolver.py` + `backend/app/capability_adapters.py`（改） | 路由/降级逻辑在 resolver/adapters；闸门钩子挂这里 |
| 新 `backend/app/capabilities/phase_gate.py` | 新 `backend/app/capability_phase_gate.py` | 命名采纳「能力相位闸门」 |
| 改 `backend/app/runtime/task_graph.py` | **实际已存在**：`backend/app/task_graph.py`（改） | 加 acceptance_criteria / task_ref / graph_revision |
| 新 `backend/app/runtime/acceptance.py` | 新 `backend/app/acceptance_evaluator.py` | — |
| 新 `backend/app/runtime/checkpoint.py` | 新 `backend/app/run_checkpoint.py` | 复用 TaskNode.to_dict/from_dict |
| 新 `backend/app/runtime/trace.py` | 新 `backend/app/runtime_trace.py` | TaskNode.trace 已有字段，升格为独立 append-only 表 |
| 改 `backend/app/runtime/scheduler.py` | **实际已存在**：`backend/app/scheduler.py` + `backend/app/runtime/scheduler.py`（改） | pause/resume/cancel + 并发上限 |
| 新 `backend/app/api/routes/runs.py` | 端点内联在 `backend/app/main.py`（改）+ `backend/app/api/`（可挂新 router） | 已有 `api/ceo_day_router.py` 先例 |
| 新 `backend/app/db/migrations/` | **无独立目录**：迁移内联 `backend/app/database.py` 的 `_migrate_*` 静态方法（改） | 新增 4 表 + 增列按既有幂等范式追加 |
| 新 `frontend/app/ceo-office/runtime-trace/page.js` | 一致（`frontend/app/ceo-office/` 为实际前端目录） | — |
| 新 `frontend/components/runtime/*` | 一致（`frontend/components/terra/` 实际存在） | 组件放 `components/runtime/` 或 `components/terra/` |

### 实际表名映射（评审草案表 → 实际）

| 评审草案表 | 实际落点 | 说明 |
|---|---|---|
| `capability_registry` 增 `effect_class` | `tenant_private_capabilities.metadata`（JSON，不新增列）或 `tools`/`official_models` 投影 | 官方目录资产统一走 `capability_catalog` 投影层，effect_class 建议放 metadata 避免动表 |
| `task_node` 增列 | **无 task_node 表**；任务实体 = `tasks` 表 + `task_graph.py` TaskNode（内存/序列化） | acceptance_criteria/task_ref 落 `tasks` 表新列（幂等 _ensure_column） |
| `capability_invocation` 增列 | 无此表；对应 `ai_usage_records`（已含 capability_id/capability_type/idempotency 候选） | gate_decision 可加列或走 trace 事件 |
| `run_control` / `run_checkpoint` / `acceptance_result` / `runtime_trace_event` | 4 张新表，按 `_migrate_*` 幂等范式新建 | 与既有表平级 |

---

## 3. 能力 effect_class 归类（评审待确认问题 5）

归类原则：`effect_class ∈ {read, retrieve, write, exec}`；**planning 相位 deny-by-default**（未标注一律拒绝）；mcp/api/webhook 等未知副作用一律 **exec/write**；agent 视为不可知副作用 → exec。

### 3.1 注册表 10 类（REGISTRY_TYPES）

| 类型 | effect_class | phase_allow（默认） | 说明 |
|---|---|---|---|
| model | read | planning + execution | 纯计算，无副作用（官方/tenant_private 皆然） |
| agent | exec | execution only | 内部可调任意能力，副作用不可知 → planning 拒绝 |
| skill | read | planning + execution | 提示模板/方法论，无执行 |
| tool | 按工具（见 3.3） | 按工具 | 文件/检索=read-retrieve；写/发布=write/exec |
| workflow | exec | execution only | 编排执行，有副作用 |
| connector | exec | execution only | 远程平台（社交上传等）副作用明确 |
| cli | exec | execution only | 命令执行，沙箱内 |
| api | write | execution only | 远程调用，默认副作用 |
| webhook | write | execution only | 出站推送 |
| mcp | **exec（deny-by-default）** | execution only | 未知权限面，必须显式声明只读子集才可进 planning |

### 3.2 官方目录资产（ct_/dt_/et_/pt_/skl_）

- ct_/dt_/et_/pt_：公司/部门/员工/persona **模板**，非可调用能力 → effect_class 不适用（视为 read，规划可读）。
- skl_*：技能模板 → read。
- wt_*：工作流模板 → exec（实例化后执行）。
- tl_*：工具目录 → 按 3.3 归类。

### 3.3 运行时工具（tl_ai_rd_*，来自 tool_registry / local_rd_toolset）

| 工具 | effect_class | 依据 |
|---|---|---|
| tl_ai_rd_file_reader | read | 只读文件 |
| tl_ai_rd_code_docs_search | retrieve | 检索 |
| tl_ai_rd_file_writer | write | 写文件（有 diff 审计 + 回滚） |
| tl_ai_rd_test_runner | exec | 执行测试（沙箱隔离） |
| tl_ai_rd_git_client | write | git 写操作被拒绝（fail-closed），读操作可用 → write |

### 3.4 tenant_private 自定义能力

- tenant_private model：read（同 model）。
- tenant_private agent：exec（同 agent）。
- tenant_private tool/connector：**需能力 owner 逐项声明**——带写权限的 MCP 调用是评审特别点名的风险，默认 exec + execution only。
- 密钥面：`env:VAR`/vault 引用不参与 effect_class，只影响 auth。

### 3.5 归类落点建议

- `capability_catalog` 投影层为每类提供默认 effect_class + phase_allow；tenant_private 的 metadata 可覆盖（但**只能收窄不能放宽**：planning 拒绝不能因自定义 metadata 放宽）。
- 「看似只读但有远程副作用」的能力（带写权限 MCP、connector）→ 默认 exec，除非显式声明 `effect_class: retrieve` + 只读 scope。

---

## 4. 修正后的立项形态（实际仓库版）

| 项 | 实际落地 | 优先级 |
|---|---|---|
| 2.2 验收标准 + task_ref | `tasks` 表增列（_ensure_column）+ TaskNode 增字段 + 新 `acceptance_evaluator.py` | P0 |
| 2.1 能力相位闸门 | `capability_resolver.py` 挂前置钩子 + 新 `capability_phase_gate.py`；effect_class 走 catalog 投影 + metadata | P0 |
| 2.4 trace 事件表 | TaskNode.trace 升格为独立 `runtime_trace_event` 表（append-only）+ 前端只读 mock 占位 | P1 |
| 2.3 检查点（切半） | 复用 TaskNode 序列化 + 新 `run_checkpoint.py` + `run_control` 表；WAL + 幂等键 | P1 |

依赖：S0（Blueprint 4.4 评审）→ S2（验收+task_ref）→ S4（检查点）；S1（闸门）与 S3（trace schema）可并行。实际工程量整体低于评审估计（因 DAG/返工计数/trace 字段已存在）。

---

## 5. 遗留确认（映射后仍需用户/产品拍板）

1. `tasks` 表增列 vs 独立 `task_ref` 命名空间：task_ref 建议 `run_id + slug + 序号`，需确认 run_id 来源（当前 tasks 无 run 概念，任务由 task_id 直管）。
2. effect_class 默认值从「逐能力显式声明」还是「按类型默认 + 例外覆盖」起步？建议后者（3.1 已给默认表）。
3. trace 事件表本期是否接后端只读端点（同评审问题 2，建议本期 mock）。
