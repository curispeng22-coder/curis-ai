"""NLParser.plan() 本地启发式 DAG 拆解 — 单元测试。

验证点（对应增强需求）：
- 单句简单目标 → ≥1 节点，goal 含具体动作词且非整句原样重复。
- 多步含连接词目标 → ≥3 节点，依赖顺序 n1→n2→n3 正确。
- cap_type 推断：含「检查/测试」节点→tool；含「生成/撰写」节点→model。
- **协作修复**：clarify 返回 questions 时 plan() 仍返回非空 nodes。
- 节点 goal 不等于整个目标字符串原样（含从目标提取的子任务关键词）。
- plan → TaskGraph.from_plan 兼容（deps / cap_requirement / 无环）。

运行：``cd backend && python3 -m pytest tests/test_nl_parser_plan.py -v``
"""
from __future__ import annotations

from app.issue_pipeline import NLParser
from app.task_graph import TaskGraph


# ---------------------------------------------------------------------------
# 1) 单句简单目标：≥1 节点，goal 含具体动作词，且不原样重复整句
# ---------------------------------------------------------------------------

def test_single_simple_goal_produces_concrete_node() -> None:
    goal = "修复登录页崩溃 bug"
    plan = NLParser().plan(goal)
    nodes = plan["nodes"]
    assert len(nodes) >= 1, "单句目标至少应生成 1 个节点"

    node = nodes[0]
    # 返回结构向后兼容：仅含 id/goal/cap_type/deps。
    assert set(node.keys()) == {"id", "goal", "cap_type", "deps"}
    # goal 含具体动作词（而非整句重复三遍的旧行为）。
    assert "修复" in node["goal"]
    # goal 不等于整句原样。
    assert node["goal"] != goal
    assert node["deps"] == []


# ---------------------------------------------------------------------------
# 2) 多步含连接词目标：≥3 节点，依赖顺序正确
# ---------------------------------------------------------------------------

def test_multi_step_with_connectors_orders_deps() -> None:
    goal = "先检查代码风格，再执行单元测试，并生成覆盖率报告"
    plan = NLParser().plan(goal)
    nodes = plan["nodes"]
    assert len(nodes) >= 3, "含 3 个连接词子句应拆出 ≥3 节点"

    ids = [n["id"] for n in nodes]
    assert ids[:3] == ["n1", "n2", "n3"]

    # 默认链式依赖 n1→n2→n3。
    assert nodes[0]["deps"] == []
    assert nodes[1]["deps"] == ["n1"]
    assert nodes[2]["deps"] == ["n2"]

    # 节点 goal 为具体子任务，而非整句原样。
    for n in nodes:
        assert n["goal"] != goal
        assert n["goal"] in ("检查代码风格", "执行单元测试", "生成覆盖率报告")


# ---------------------------------------------------------------------------
# 3) cap_type 推断
# ---------------------------------------------------------------------------

def test_cap_type_inference() -> None:
    parser = NLParser()
    # 工具类动作 → tool
    assert parser._infer_cap_type("检查代码风格") == "tool"
    assert parser._infer_cap_type("执行单元测试") == "tool"
    assert parser._infer_cap_type("校验覆盖率门槛") == "tool"
    assert parser._infer_cap_type("验证结果") == "tool"
    # 模型类动作 → model
    assert parser._infer_cap_type("生成覆盖率报告") == "model"
    assert parser._infer_cap_type("撰写设计文档") == "model"
    assert parser._infer_cap_type("实现登录功能") == "model"
    # 兜底 → model
    assert parser._infer_cap_type("未命名目标") == "model"


def test_cap_type_in_plan_nodes() -> None:
    goal = "先检查代码风格，再执行单元测试，并生成覆盖率报告"
    plan = NLParser().plan(goal)
    nodes = plan["nodes"]
    # 检查/执行类子任务 → tool；生成类 → model。
    tool_nodes = [n for n in nodes if n["cap_type"] == "tool"]
    model_nodes = [n for n in nodes if n["cap_type"] == "model"]
    assert any("检查" in n["goal"] for n in tool_nodes)
    assert any("执行" in n["goal"] for n in tool_nodes)
    assert any("生成" in n["goal"] for n in model_nodes)


# ---------------------------------------------------------------------------
# 4) 协作修复：clarify 有 questions 时 plan 仍返回非空 nodes
# ---------------------------------------------------------------------------

def test_clarify_questions_still_returns_nodes() -> None:
    # 过短目标会触发 clarify 的追问，但仍须产出初步 DAG（不阻塞计划展示）。
    goal = "做"
    parser = NLParser()
    questions = parser.clarify(goal)
    assert questions, "短目标应触发 clarify 追问"

    plan = parser.plan(goal)
    assert plan["questions"], "plan 应回传 clarify 的 questions"
    assert len(plan["nodes"]) >= 1, "即使有 questions，plan 也必须返回非空 nodes（修复验证）"


def test_ambiguous_short_goal_still_plans() -> None:
    # 「优化一下」：长度<6 且不含产出类关键词 → 两条 questions，仍须有节点。
    goal = "优化一下"
    parser = NLParser()
    assert parser.clarify(goal)
    plan = parser.plan(goal)
    assert plan["questions"]
    assert len(plan["nodes"]) >= 1


# ---------------------------------------------------------------------------
# 5) 兜底：空目标 / 无连接词单句仍产出 1 节点且结构合法
# ---------------------------------------------------------------------------

def test_empty_goal_fallback_single_node() -> None:
    plan = NLParser().plan("")
    nodes = plan["nodes"]
    assert len(nodes) == 1
    assert nodes[0]["id"] == "n1"
    assert nodes[0]["deps"] == []
    assert set(nodes[0].keys()) == {"id", "goal", "cap_type", "deps"}
    assert nodes[0]["goal"].startswith("完成：")


# ---------------------------------------------------------------------------
# 6) plan → TaskGraph.from_plan 兼容（消费端契约）
# ---------------------------------------------------------------------------

def test_plan_compatible_with_task_graph_from_plan() -> None:
    goal = "先检查代码风格，再执行单元测试，并生成覆盖率报告"
    plan = NLParser().plan(goal)
    graph = TaskGraph.from_plan(plan)

    assert set(graph.nodes.keys()) == {"n1", "n2", "n3"}
    # deps 正确映射。
    assert graph.nodes["n1"].deps == []
    assert graph.nodes["n2"].deps == ["n1"]
    assert graph.nodes["n3"].deps == ["n2"]
    # cap_type 正确落入 cap_requirement（供 resolver 后续选能力）。
    assert graph.nodes["n1"].cap_requirement["cap_type"] == "tool"
    assert graph.nodes["n3"].cap_requirement["cap_type"] == "model"
    # 无循环依赖：拓扑序覆盖全部节点。
    assert graph.topo_order() == ["n1", "n2", "n3"]


def test_plan_node_goal_keywords_extracted() -> None:
    """节点 goal 含从目标提取的子任务关键词，而非整句原样。"""
    goal = "分析需求，生成实现方案，验证结果"
    plan = NLParser().plan(goal)
    goals = [n["goal"] for n in plan["nodes"]]
    assert any("分析" in g for g in goals)
    assert any("生成" in g for g in goals)
    assert any("验证" in g for g in goals)
    for g in goals:
        assert g != goal
