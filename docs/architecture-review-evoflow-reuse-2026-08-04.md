# Curis 复用 EvoFlow 工程模式 · 架构评审意见

> 评审人：高见远（架构师）｜团队：software-arch-review-evoflow
> 日期：2026-08-04
> 范围：架构评审 + 增量设计草案，未产出代码与文件
> 说明：Curis 后端目录结构按「FastAPI 分层」通用形态假设（标注「假设」），最终以实际仓库为准。
> 上游依据：竞品研究报告 `docs/competitive-analysis-evoflow-vs-curis-2026-08-04.md`

## 1. 总评（TL;DR）

四项中**三项半可立项**。价值密度排序为 ②验收标准+全局任务引用 > ①阶段门 > ④trace 视图位 > ③持久化检查点。①②本质是在 Curis 已有的「能力路由层」与「业务生命周期状态机」上做**元数据扩展**，不新增架构层、不违背四原则，改造成本低而对「目标→执行→验收→返工→完成」自动化的杠杆最大。③工程量最重且受 sqlite 单写与副作用不可回滚约束，建议**切半立项**（先 pause/resume/cancel，局部重规划降到 P2）。④成本最低但直接压在 ADR-0017「禁止复杂 UI」边线上，必须限定为**只读单页 + 本地 mock**。全部四项均须先过 Business Runtime Blueprint 变更（涉及任务图 schema 与状态机语义），不得直接进 Code 阶段。

## 2. 四项逐项评估

### 2.1 阶段门（建议改称「能力相位闸门 Capability Phase Gate」）

| 维度 | 结论 |
|---|---|
| 可行性 | **高**。本质是能力路由层前置的一个谓词过滤器，不触碰任何能力实现 |
| 契合度 | **极高**。正向强化原则③——能力集合随运行相位动态变化，比「员工绑死固定 Agent」更动态，不存在回退风险 |
| 冲突点 | (a) 现有 7 项能力缺 `effect_class` 元数据，需逐项归类；(b) **闸门与能力路由降级的优先级冲突**：降级可能把写能力替换为等价实现，须明确「闸门是硬约束、降级是软策略，闸门先于降级求值」；(c) 相位来源需绑定运行层状态机当前节点，不能由调用方自报 |
| 落地形态 | 能力注册表增列 `effect_class(read/retrieve/write/exec)`；路由层挂 `phase_gate` 前置钩子；**deny-by-default**（未标注能力在 planning 相位一律拒绝）；拒绝需返回结构化原因写入 trace，而非静默丢弃 |

补充：EvoFlow 的「冷启动只挂核心+检索、按需挂载」与阶段门同源，建议**合并为一项**实现（挂载集合 = 相位允许集合 ∩ 岗位声明集合），不单列 P2。

### 2.2 任务图补验收标准 + 全局任务引用（建议字段名 `task_ref`，规避 boundTaskId 字面）

| 维度 | 结论 |
|---|---|
| 可行性 | **高**，且为四项中 ROI 最高 |
| 契合度 | **极高**。当前 accept/rework 只有业务态流转、缺技术判定依据，补此项后可把人工判定升级为可判定谓词，直击原则④ |
| 冲突点 | (a) 最大风险是验收标准退化为 LLM 生成的空泛自然语言 → 必须 schema 约束：`{type: assertion｜artifact｜command｜manual, expr, expected, weight}`，并**强制至少一条机器可判定项**（待产品确认）；(b) `task_ref` 需全局唯一且跨重规划稳定，不能用自增 id；建议 `run_id + 语义 slug + 序号`；(c) rework 需记录「未通过的具体判据」回灌下一轮，否则返工无信息增益 |
| 落地形态 | 任务节点 schema 扩展 + 独立 `acceptance evaluator` 在验收阶段执行，评估结果 append 到 trace；manual 类判据走人工确认位，不阻塞机器判据先跑 |

### 2.3 运行层持久化检查点（断点续跑）

| 维度 | 结论 |
|---|---|
| 可行性 | **中**。工程量为四项之最，且有硬约束 |
| 契合度 | 高（运行层是 Curis 核心），但 Curis **无图编排引擎**，检查点须自建；**明确不得为此引入 LangGraph 类框架**，否则偏移既定「非图编排」路线 |
| 冲突点 | (a) **副作用不可回滚**：写/命令类能力已执行的效果无法随检查点回退，因此语义只能是「至少一次 + 幂等」，必须给能力调用引入 `idempotency_key`；(b) sqlite 单写者 → 必须开 WAL + 运行层写入串行化，并顺带落**队列并发上限**（原 P2 项，此处顺带做，成本近零）；(c) 局部重规划导致任务图分叉 → 需 `graph_revision` 版本号，检查点必须携带版本，跨版本恢复要显式拒绝 |
| 落地形态 | **切半**：一期只做 pause / resume / cancel + 失败重试（状态快照 + 序号游标）；局部重规划（分叉/合并）降 P2 单独设计 |

### 2.4 CEO Office runtime trace 视图位

| 维度 | 结论 |
|---|---|
| 可行性 | **高**，成本最低 |
| 契合度 | 高。CEO Office UI V2 本就是未接后端的 UI 壳，占位天然成立 |
| 冲突点 | **直接压 ADR-0017「禁止复杂 UI」边线**：禁止引入 DAG 可视化库、禁止实时流/WebSocket、禁止交互式编辑。token 明细（含缓存命中/写入）字段先在 schema 定义、前端可留空 |
| 落地形态 | 先定 **append-only trace 事件 schema**（这是真正的资产，前端只是展示面）；前端仅做「时间线列表 + 任务引用分组」两个只读组件 + 本地 mock，Terra 暖色主题内联，不新增 UI 依赖 |

## 3. P2 可选项简评

| 项 | 可行性 | 结论 |
|---|---|---|
| 中间件链抽象 | 中 | **暂缓**。仅 7 项能力、当前只有「相位闸门」一个横切关注点，过早抽象。待横切关注点 ≥3 个（闸门/限流/幂等/审计）再抽链 |
| 任务队列并发上限 | 高 | **并入 2.3 一期**，sqlite 写并发本就需要限流，零额外成本 |
| Tauri 桌面壳 | 低 | **暂缓**。与 Web 优先路线冲突，无用户诉求，且引入第二套构建/发布链路 |
| 白名单能力加载 | 高 | **并入 2.1**，与阶段门同源，不单列 |

## 4. 红线风险判定

| 评估项 | ADR-0017 冻结项 | 四原则 | IP / 商标 | 结论 |
|---|---|---|---|---|
| 2.1 阶段门 | 不触 Employee CRUD / 计费 / Marketplace / 向量库 → 通过 | 正向强化③④ | `PlanGuard` 为 EvoFlow 专有术语 | **需规避**：改称「能力相位闸门」；仅借鉴「按相位过滤副作用能力」思想 |
| 2.2 验收标准+task_ref | 通过 | 直击④ | `boundTaskId` 字面需回避 | **需规避**：字段名用 `task_ref`；schema 自行设计不照搬 |
| 2.3 检查点 | 通过 | 通过 | 通用工程模式，无 IP 风险 | **通过，附条件**：不得引入 LangGraph 等图编排框架；不得因"续跑"需求引向量库做记忆 |
| 2.4 trace 视图位 | ⚠️「复杂 UI」边线 | 通过 | 避免 `Agent Trace` / `EvoPanel` 命名 | **需规避**：限定只读单页 + mock，无图库无实时流；命名用通用「运行轨迹 / Runtime Trace」 |
| 全局流程 | — | — | — | **强制前置**：涉及任务图 schema + 状态机语义变更，须先过 Business Runtime Blueprint，再 UI Design，最后 Code |
| 商业化关联 | 四项均不涉及 Marketplace/收费/多租户/外部 Agent 生态 | — | — | **通过** |

结论：**无「禁止」项**，四项均为「通过」或「需规避（命名/范围收敛即可）」。

## 5. 增量设计草案

**影响的服务/模块**：能力层（注册表 + 路由）、运行层（任务图 / 调度器 / 验收器 / 检查点）、持久层（sqlite 迁移）、前端 CEO Office（只读占位）。

**数据表变更草案（sqlite）**

| 表 | 变更 | 关键字段 |
|---|---|---|
| `capability_registry`（改） | 增列 | `effect_class TEXT`（read/retrieve/write/exec）、`phase_allow TEXT(JSON)` |
| `task_node`（改） | 增列 | `task_ref TEXT UNIQUE`、`acceptance_criteria TEXT(JSON)`、`graph_revision INTEGER` |
| `capability_invocation`（改） | 增列 | `idempotency_key TEXT`、`gate_decision TEXT`（allow/deny+reason） |
| `run_control`（新） | — | `run_id PK, status(running/paused/cancelled/failed), reason, graph_revision, updated_at` |
| `run_checkpoint`（新） | — | `id PK, run_id, graph_revision, task_ref, phase, seq, state_snapshot JSON, created_at` |
| `acceptance_result`（新） | — | `id PK, task_ref, criterion_idx, passed BOOL, actual, evaluated_at` |
| `runtime_trace_event`（新，append-only） | — | `id PK, run_id, task_ref, event_type, capability, tokens_in, tokens_out, cache_hit, latency_ms, payload JSON, created_at` |

配套：开启 WAL；`runtime_trace_event` 建 `(run_id, created_at)` 索引；不新增任何 Employee 相关表/端点。

**后端改动文件（路径级，目录结构为假设）**
- 改：`backend/app/capabilities/registry.py`（effect_class 元数据）、`backend/app/capabilities/router.py`（挂前置钩子、明确闸门优先于降级）
- 新：`backend/app/capabilities/phase_gate.py`
- 改：`backend/app/runtime/task_graph.py`（节点 schema + task_ref 生成 + graph_revision）、`backend/app/runtime/scheduler.py`（pause/resume/cancel + 并发上限）
- 新：`backend/app/runtime/acceptance.py`、`backend/app/runtime/checkpoint.py`、`backend/app/runtime/trace.py`
- 改/新：`backend/app/api/routes/runs.py`（`POST /runs/{id}/pause|resume|cancel`、`GET /runs/{id}/trace` 只读）
- 新：`backend/app/db/migrations/`（4 张新表 + 3 处增列）

**前端改动点（CEO Office 占位）**
- 新：`app/ceo-office/runtime-trace/page.js`（只读单页）
- 新：`components/runtime/TraceTimeline.js`、`components/runtime/TaskRefList.js`（纯展示，Terra 主题）
- 新：`lib/mock/runtimeTrace.js`（本地 mock，本期不接后端）
- 不改动其余 47 页 UI 壳，不新增前端依赖

**依赖关系与实现顺序**

```
S0 Business Runtime Blueprint 变更（前置，强制）
 ├─ S1 能力元数据 + 相位闸门        [P0]（仅依赖 S0，可独立交付）
 ├─ S2 任务图 schema + 验收执行器    [P0]（依赖 S0；产出 task_ref 命名契约）
 │    ├─ S3 trace 事件 schema + 前端占位 [P1]（schema 依赖 S2；前端 mock 可并行）
 │    └─ S4 检查点 + 并发上限         [P1]（依赖 S2 的 graph_revision）
 └─ S5 局部重规划（图分叉/合并）      [P2]（依赖 S4，本期不做）
```

关键路径：S0 → S2 → S4。S1 与 S3 前端部分可完全并行。

## 6. 立项结论

**结论：部分立项（4 项中 3.5 项）**

| 项 | 结论 | 优先级 | 理由 |
|---|---|---|---|
| 2.2 验收标准 + task_ref | **建议立项** | **P0** | ROI 最高，直接把 accept/rework 从业务态流转升级为技术可判定，是原则④的核心补强；改造面小 |
| 2.1 能力相位闸门 | **建议立项** | **P0** | 复用现有能力路由层，纯增量元数据 + 一个钩子；同时兼顾安全与 token 成本；正向强化原则③ |
| 2.4 trace 视图位 | **建议立项（范围收敛）** | **P1** | 真正资产是 trace 事件 schema；前端严格限定只读 mock 单页，避开 ADR-0017 复杂 UI 红线 |
| 2.3 持久化检查点 | **有条件立项（切半）** | **P1**（一期）/ **P2**（重规划） | 一期只做 pause/resume/cancel/重试 + 并发上限；局部重规划涉及图版本分叉语义，未定型前不做 |
| P2 中间件链抽象 / Tauri 桌面壳 | **暂缓** | — | 前者过早抽象，后者与 Web 优先路线冲突且无诉求 |

强制前置条件：**S0 Business Runtime Blueprint 变更必须先完成并评审通过**，否则四项全部不得进入 Code 阶段。

## 7. 待确认问题（请主理人/用户拍板）

1. **验收标准最低可判定要求**：是否强制每个任务节点至少一条机器可判定判据（assertion/artifact/command）？若允许全 manual，自动化收益会大幅折损。
2. **trace 视图本期是否允许接后端只读端点**（`GET /runs/{id}/trace`），还是严格只做本地 mock？这关系 ADR-0017「UI 壳未接后端」边界的解释口径。
3. **局部重规划语义**：分叉出新 `graph_revision`（保留历史，可对比）还是原地修改（简单但丢溯源）？影响 S4 检查点表设计，建议前者。
4. **幂等键归属**：由能力实现方自行声明幂等语义，还是运行层统一生成并强制？建议运行层生成 + 能力方声明「是否幂等安全」。
5. **现有 7 项能力的 `effect_class` 归类**：需能力 owner 逐项确认，尤其是「看似只读但有远程副作用」的能力（如带写权限的 MCP 调用）。
6. **命名终审**：`Capability Phase Gate（能力相位闸门）` / `task_ref` / `Runtime Trace` 三个对外术语是否采纳，以规避 EvoFlow 专有术语混淆风险。
