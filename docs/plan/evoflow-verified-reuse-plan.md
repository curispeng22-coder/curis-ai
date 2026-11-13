# EvoFlow 复核结论与落地决策（2026-08-04 独立复核版）

> 历史工程复用评审。产品规划与开发顺序已由 `curis-product-completion-roadmap-evoflow-2026-08-10.md` 取代；本文件不得作为当前产品或开发优先级依据。

> 依据：GitHub README 独立复核（`docs/competitive-analysis-evoflow-vs-curis-2026-08-04.md` §4A）+ 实际仓库映射（`docs/plan/evoflow-reuse-repo-mapping.md`）
> 原则：① 竞品分析核心事实全部确认，无系统性错误；② 落地分「立即做（不越 Blueprint 边界）」与「需 S0 前置」两档；③ 只借鉴思想，零代码复制（Non-Commercial 1.0 + 商标红线）。

## 1. 复核结论（对照 GitHub 一次）

**竞品分析准确性：核心 16 项声明全部确认**（定位/LangGraph/LangChain/EvoPanel Tauri/FastAPI 网关/Supervisor+plan+boundTaskId/PlanGuard/中间件 10 段/检查点与恢复/Agent Trace token 明细/≤3 并发 15min/50+ SKILL/微信飞书/沙箱三模式/许可证/源码未公开）。
3 处遗漏已补：Smart Employees（值勤台/审批/名册）、ACP 适配器 planned 清单（Claude Code/Codex/Trae/CodeBuddy）、DeerFlow(MIT) 工程基线 + 端口拓扑。
1 处小偏差已修：EvoFlow 自定义 Agent 非「完全固定角色」（预设团队是 recommended pattern，可配 SOUL）。

## 2. 落地决策（两档）

### A. 立即做（不改变业务语义，不触碰任务 schema/状态机，符合 AGENTS.md 纪律）

| 项 | 内容 | 价值 | 落点 |
|---|---|---|---|
| A1 能力 effect_class 元数据 | 10 类注册表 + 运行时工具 + 官方目录的副作用面标注（read/retrieve/write/exec），只标注不改执行 | 为 A2/S0 闸门铺路；纯增量 | `capability_catalog` 投影 + `capability_registry`（effect_class 默认表） |
| A2 运行时 trace 事件表 | TaskNode.trace（内存）升格为独立 append-only `runtime_trace_event` 表，写入执行管道事件 + 只读查询 | 借鉴 EvoFlow 最成熟的可观测点；CEO 需要看见执行过程；AI Usage 已含 token 数据可衔接 | 新表 + `runtime_trace.py` + 只读端点 |

### B. 需 S0 前置（涉及任务 schema/状态机语义，须先过 Business Runtime Blueprint 评审）

| 项 | 内容 | 前置 |
|---|---|---|
| B1 能力相位闸门 | planning 相位拒绝写/exec 能力（deny-by-default）——改变执行行为 | S0 + A1 元数据就绪 |
| B2 验收标准 + task_ref | tasks 表增列 + acceptance_evaluator——任务 schema 变更 | S0（评审问题 1/3 拍板） |
| B3 持久化检查点 | run_control/run_checkpoint 表 + pause/resume/cancel——状态机语义 | S0（评审问题 4 拍板） |

## 3. 对「Smart Employees」的判断

EvoFlow 的智能员工（值勤台/审批/名册）与 Curis「员工=动态能力岗位」存在概念重叠，但 **EvoFlow 偏预设角色 + 审批流，Curis 员工抽象更先进**（岗位临时组装能力）。**不新增价值，不借鉴**——它反而是 Curis 员工体系方向正确性的佐证。

## 4. 执行顺序

A1（元数据，快）→ A2（trace 表，中）→ 提 B1-B3 进入 S0 待办（Blueprint 4.4 评审后按 `evoflow-reuse-repo-mapping.md` §4 落地）。

## 5. 实现状态（2026-08-04）

- [x] **A1 effect_class 已落地**：`catalog_constants.py` 新增 `effect_class_for_capability`（类型默认 + 工具名启发式）；`database.list_catalog_capabilities` 投影派生 `effect_class`（不落库）。全量回归 1202 passed。
- [x] **A2 runtime_trace_event 已落地**：`runtime_trace_event` append-only 表（幂等迁移）+ `runtime_trace.py`（RuntimeTraceService：write_event/list_recent）+ 只读端点 `GET /api/workspace/runtime-trace`。5 个新测试；`tasks` 表零改动（不改变任务语义）。
- [ ] **B1-B3** 待 S0（Blueprint 4.4 评审）后立项。
