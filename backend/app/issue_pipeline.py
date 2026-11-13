"""自然语言任务管道系统。

四合一：
1. NL→IssueSpec 解析（NLParser → ModelGatewayAdapter）
2. 任务队列（IssueQueue, SQLite issue_pipeline 表）
3. 调度器（PipelineDispatcher → RealRDExecutor(CodexAgentAdapter)）
4. 结果审查（ResultReviewer → test_exit_code + diff）

事件脱敏：所有 ``a.pipeline.*`` 事件仅含 id/status/rounds，无路径/Key。
后端零新依赖（仅 Python 标准库 + 既有 ModelGatewayAdapter / RealRDExecutor）。
"""

from __future__ import annotations

import json
import os
import re
import sqlite3
import threading
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Any


# ---------------------------------------------------------------------------
# 路径/常量
# ---------------------------------------------------------------------------

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DB_PATH = os.path.join(_REPO_ROOT, "data", "issue_pipeline.sqlite")

_DEFAULT_TARGET_FILE = "tools/real_rd_fixture/target_a.py"
_DEFAULT_TEST_PATH = "backend/tests/test_real_rd_fixture_a.py"


# ---------------------------------------------------------------------------
# PipelineTask dataclass
# ---------------------------------------------------------------------------


@dataclass
class PipelineTask:
    """管道中的单个任务。"""
    id: str
    created_at: str                                        # ISO UTC
    natural_language: str
    issue_spec: dict[str, Any] | None = None               # {issue_id, target_file, issue, expected_test, max_rounds}
    status: str = "pending"                                # pending | queued | running | review | approved | rejected | failed
    queued_at: str | None = None
    started_at: str | None = None
    completed_at: str | None = None
    executor_result: dict[str, Any] | None = None          # {status, rounds, test_exit_code, diff_text, ...}
    rework_count: int = 0
    rework_feedback: list[str] = field(default_factory=list)
    review_decision: str | None = None
    review_note: str | None = None


# ---------------------------------------------------------------------------
# 数据库锁（SQLite 写串行化）
# ---------------------------------------------------------------------------

_db_lock = threading.Lock()


def _get_db_path() -> str:
    """返回 issue_pipeline SQLite 数据库路径。"""
    return _DB_PATH


def _ensure_schema(conn: sqlite3.Connection) -> None:
    """创建 issue_pipeline 表（幂等）。"""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS issue_pipeline (
            id TEXT PRIMARY KEY,
            created_at TEXT NOT NULL,
            natural_language TEXT NOT NULL,
            issue_spec TEXT,
            status TEXT NOT NULL DEFAULT 'pending',
            queued_at TEXT,
            started_at TEXT,
            completed_at TEXT,
            executor_result TEXT,
            rework_count INTEGER NOT NULL DEFAULT 0,
            rework_feedback TEXT,
            review_decision TEXT,
            review_note TEXT
        )
    """)


# ---------------------------------------------------------------------------
# NLParser：自然语言 → IssueSpec（用 ModelGatewayAdapter 或兜底默认值）
# ---------------------------------------------------------------------------

_NL_PROMPT_TEMPLATE = """你是一个研发任务解析器。用户说: {natural_language}

请根据用户的需求生成以下 JSON（只输出 JSON，不要附加任何其他文字）：

{{
  "issue_id": "task-{suffix}",
  "target_file": "tools/real_rd_fixture/target_a.py",
  "issue": "{natural_language_escaped}",
  "expected_test": "backend/tests/test_real_rd_fixture_a.py",
  "max_rounds": 3
}}

如果用户提到了明确的目标文件路径，请使用用户指定的路径替代默认值。
如果用户提到了明确的测试文件路径，请使用用户指定的测试路径替代默认值。
"""


class NLParser:
    """自然语言 → IssueSpec 解析器。

    通过 ModelGatewayAdapter 调用模型，解析模型输出的结构化 JSON。
    无模型网关时（测试/离线环境）返回默认 spec。
    """

    def __init__(self, model_gateway: Any | None = None) -> None:
        self._gateway = model_gateway

    def parse(self, natural_language: str) -> dict[str, Any]:
        """将自然语言解析为 IssueSpec dict。"""
        suffix = uuid.uuid4().hex[:8]
        escaped = natural_language.replace('"', '\\"').replace('\n', ' ')
        prompt = _NL_PROMPT_TEMPLATE.format(
            natural_language=natural_language,
            natural_language_escaped=escaped,
            suffix=suffix,
        )
        if self._gateway is None:
            return self._default_spec(suffix, natural_language)
        try:
            response = self._gateway.execute(prompt)
            output = response.get("output", "")
            spec = self._parse_json_output(output)
            # 填充缺失字段
            spec.setdefault("issue_id", f"task-{suffix}")
            spec.setdefault("target_file", _DEFAULT_TARGET_FILE)
            spec.setdefault("issue", natural_language)
            spec.setdefault("expected_test", _DEFAULT_TEST_PATH)
            spec.setdefault("max_rounds", 3)
            return spec
        except Exception:
            return self._default_spec(suffix, natural_language)

    def _default_spec(self, suffix: str, natural_language: str) -> dict[str, Any]:
        return {
            "issue_id": f"task-{suffix}",
            "target_file": _DEFAULT_TARGET_FILE,
            "issue": natural_language,
            "expected_test": _DEFAULT_TEST_PATH,
            "max_rounds": 3,
        }

    # ── P0 增强：澄清 → 结构化计划（DAG）本地启发式拆解 ─────────────────────
    # 连接词/标点（按文本出现顺序切分语义片段；同时携带顺序暗示）。
    # 说明：不拆分「和/与/以及」等名词短语连词，避免把「代码风格与静态规范」
    # 这类宾语误拆成无动词片段。
    _SPLIT_TOKENS = [
        "然后", "接着", "随后", "最后", "同时", "再",
        "；", "。", "\n", "，", "、",
    ]
    # 片段前缀顺序标记（切分后从片段开头剥离，避免带入 goal 文本）。
    _PREFIX_TOKENS = ["先", "再", "然后", "接着", "随后", "最后", "同时", "并", "并且"]
    # 动作词 → 能力类型映射（符合「能力可替换不写死」原则，仅做类型推断）。
    _TOOL_VERBS = ["检查", "校验", "验证", "测试", "运行", "执行", "跑", "lint"]
    _MODEL_VERBS = [
        "生成", "撰写", "编写", "创建", "实现", "开发", "设计",
        "产出", "汇总", "分析", "修复",
    ]
    _CLI_VERBS = ["部署", "发布", "配置", "安装"]

    # 正则延迟编译（避免模块导入期正则开销；首次使用时构建）。
    _SPLIT_RE: "re.Pattern[str] | None" = None
    _PREFIX_RE: "re.Pattern[str] | None" = None

    @classmethod
    def _ensure_re(cls) -> None:
        """懒编译拆分/前缀正则（长词优先，避免「再」抢先匹配「然后再」等）。"""
        if cls._SPLIT_RE is None:
            split_pattern = "|".join(re.escape(t) for t in cls._SPLIT_TOKENS)
            cls._SPLIT_RE = re.compile(split_pattern)
            prefix_pattern = (
                r"^(?:" + "|".join(re.escape(t) for t in cls._PREFIX_TOKENS) + r")+"
            )
            cls._PREFIX_RE = re.compile(prefix_pattern)

    def clarify(self, natural_language: str) -> list[str]:
        """目标澄清：若信息不足返回澄清问题列表，否则返回空列表（可直接生成计划）。

        轻量本地判断（基于长度 + 关键词）；复杂澄清对话留作后续阶段。
        注意：即使返回 questions，``plan()`` 仍会尽力生成初步 DAG（见协作修复）。
        """
        questions: list[str] = []
        text = (natural_language or "").strip()
        if len(text) < 6:
            questions.append("请补充更具体的目标描述（至少一句话）。")
        if not any(
            kw in text
            for kw in ("实现", "生成", "修复", "编写", "开发", "做", "完成", "分析", "设计")
        ):
            questions.append(
                "请说明期望的产出类型（如：实现某功能 / 修复某 bug / 生成某文档 / 分析某问题）。"
            )
        return questions

    def plan(self, natural_language: str) -> dict[str, Any]:
        """生成结构化执行计划（DAG）。

        返回：
            {"goal", "questions": [...], "nodes": [{id, goal, cap_type, deps}]}

        增强（相比 P0 最小实现）：
        1. 用本地启发式把目标**真正拆成有意义的 DAG 节点**（见 ``_build_plan_nodes``），
           不再把整句目标重复三遍。
        2. **协作修复**：即使 ``clarify()`` 返回 questions（信息不足），也生成初步 DAG
           （基于现有文本尽力拆解），questions 作为补充字段一并返回。这样前端提交后
           总能看到计划，clarify 问题作为「AI 需要澄清（参考）」展示，不阻塞计划展示。

        不调用任何外部模型/LLM，保证离线、无模型 key 环境可用（零新依赖）。
        """
        questions = self.clarify(natural_language)
        nodes = self._build_plan_nodes(natural_language)
        return {
            "goal": natural_language,
            "questions": questions,
            "nodes": nodes,
        }

    # ── 本地启发式拆解私有辅助 ───────────────────────────────────────────────
    def _split_subtasks(self, text: str) -> list[str]:
        """把自然语言目标按连接词/标点拆成候选子任务片段（保留出现顺序）。

        纯本地规则：按 ``_SPLIT_TOKENS`` 切分，去除空片段、残留标点和前缀顺序标记；
        若某片段无动作词（很可能是名词短语续接，如「代码风格与静态规范」），并入上一
        片段以保持语义完整。不调用任何外部模型，保证离线/无 key 环境可用。
        """
        self._ensure_re()
        raw = (text or "").strip()
        if not raw:
            return []
        # 先按标点/连接词切分。
        parts = self._SPLIT_RE.split(raw)  # type: ignore[union-attr]
        fragments: list[str] = []
        for p in parts:
            # 去除片段首尾残留标点与空白。
            p = p.strip("，。；、 \n\t")
            if not p:
                continue
            # 剥离前缀顺序标记（先/再/然后/...），避免带入 goal 文本。
            p = self._PREFIX_RE.sub("", p).strip("，。；、 \n\t")  # type: ignore[union-attr]
            if p:
                fragments.append(p)
        # 片段合并：无动作词的片段并入上一片段（名词短语续接保护）。
        merged: list[str] = []
        for frag in fragments:
            if merged and not self._has_action_verb(frag):
                merged[-1] = merged[-1] + frag
            else:
                merged.append(frag)
        return merged

    @staticmethod
    def _has_action_verb(fragment: str) -> bool:
        """片段是否含任一已知动作词。"""
        verbs = (
            NLParser._TOOL_VERBS
            + NLParser._MODEL_VERBS
            + NLParser._CLI_VERBS
        )
        return any(v in fragment for v in verbs)

    def _infer_cap_type(self, fragment: str) -> str:
        """从子任务片段推断能力类型（映射到能力层类型，能力可替换不写死）。

        - 含 检查/测试/校验/验证/lint/跑/执行/运行 → ``tool``
        - 含 生成/写/创建/实现/开发/设计/撰写/产出/汇总/分析/修复 → ``model``
        - 含 部署/发布/配置/安装 → ``cli``
        - 兜底 → ``model``
        """
        if any(v in fragment for v in self._TOOL_VERBS):
            return "tool"
        if any(v in fragment for v in self._MODEL_VERBS):
            return "model"
        if any(v in fragment for v in self._CLI_VERBS):
            return "cli"
        return "model"

    def _build_plan_nodes(self, natural_language: str) -> list[dict[str, Any]]:
        """本地启发式把目标拆成 DAG 节点列表（{id, goal, cap_type, deps}）。

        规则：
        - 按 ``_SPLIT_TOKENS`` 切分语义片段；单片段（无连接词）兜底为 1 个节点。
        - 依赖默认链式：n1→n2→n3…，顺序即文本出现顺序（含「先X再Y最后Z」亦成立）。
        - 节点仅含向后兼容字段 id/goal/cap_type/deps（供 ``TaskGraph.from_plan`` 消费）；
          如需扩展可加 input_refs/output_ref，但绝不删改既有字段名。
        """
        fragments = self._split_subtasks(natural_language)
        # 兜底：无有效片段（空目标/纯标点）→ 至少 1 个节点，goal 用「完成：…」表述。
        if not fragments:
            fallback_goal = (natural_language or "").strip() or "未命名目标"
            return [
                {
                    "id": "n1",
                    "goal": f"完成：{fallback_goal}",
                    "cap_type": self._infer_cap_type(fallback_goal),
                    "deps": [],
                }
            ]
        nodes: list[dict[str, Any]] = []
        prev_id: str | None = None
        for idx, frag in enumerate(fragments):
            node_id = f"n{idx + 1}"
            # 单片段时加「完成：」前缀，使 goal 与原始整句区分且更具体；
            # 多片段时直接使用具体子任务文本（如「检查代码风格」）。
            goal = f"完成：{frag}" if len(fragments) == 1 else frag
            cap_type = self._infer_cap_type(frag)
            deps = [prev_id] if prev_id is not None else []
            nodes.append(
                {
                    "id": node_id,
                    "goal": goal,
                    "cap_type": cap_type,
                    "deps": deps,
                }
            )
            prev_id = node_id
        return nodes

    @staticmethod
    def _parse_json_output(output: str) -> dict[str, Any]:
        """从模型输出文本中提取 JSON。"""
        text = output.strip()
        if not text:
            return {}
        # 尝试找 ```json ... ``` 或 ``` ... ``` 围栏
        for marker in ("```json", "```"):
            start = text.find(marker)
            if start >= 0:
                end = text.find("```", start + len(marker))
                if end >= 0:
                    text = text[start + len(marker):end].strip()
                else:
                    text = text[start + len(marker):].strip()
                break
        # 尝试直接解析
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass
        # 尝试找首个 { 并截取到匹配的 }
        brace = text.find("{")
        if brace >= 0:
            # 找出匹配的 }（简单括号计数）
            depth = 0
            for i, ch in enumerate(text[brace:]):
                if ch == "{":
                    depth += 1
                elif ch == "}":
                    depth -= 1
                    if depth == 0:
                        try:
                            return json.loads(text[brace:brace + i + 1])
                        except json.JSONDecodeError:
                            pass
                        break
        return {}


# ---------------------------------------------------------------------------
# IssueQueue：SQLite 任务队列
# ---------------------------------------------------------------------------


class IssueQueue:
    """基于 SQLite 的任务队列，线程安全。"""

    def __init__(self, db_path: str | None = None) -> None:
        self._db_path = db_path or _DB_PATH

    def _connect(self) -> sqlite3.Connection:
        """获取连接（自动建表）。"""
        os.makedirs(os.path.dirname(self._db_path), exist_ok=True)
        conn = sqlite3.connect(self._db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL")
        _ensure_schema(conn)
        return conn

    def enqueue(self, task: PipelineTask) -> str:
        """入队一个任务，返回 id。"""
        with _db_lock:
            conn = self._connect()
            try:
                conn.execute(
                    """INSERT INTO issue_pipeline
                       (id, created_at, natural_language, issue_spec, status,
                        queued_at, started_at, completed_at, executor_result,
                        rework_count, rework_feedback, review_decision, review_note)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (
                        task.id,
                        task.created_at,
                        task.natural_language,
                        json.dumps(task.issue_spec) if task.issue_spec else None,
                        task.status,
                        task.queued_at,
                        task.started_at,
                        task.completed_at,
                        json.dumps(task.executor_result) if task.executor_result else None,
                        task.rework_count,
                        json.dumps(task.rework_feedback) if task.rework_feedback else None,
                        task.review_decision,
                        task.review_note,
                    ),
                )
                conn.commit()
            finally:
                conn.close()
        return task.id

    def dequeue(self) -> PipelineTask | None:
        """取出下一个状态为 pending 的任务（按 created_at ASC），标记为 queued。"""
        with _db_lock:
            conn = self._connect()
            try:
                row = conn.execute(
                    "SELECT * FROM issue_pipeline WHERE status = 'pending' ORDER BY created_at ASC LIMIT 1"
                ).fetchone()
                if row is None:
                    return None
                now = datetime.now(timezone.utc).isoformat()
                conn.execute(
                    "UPDATE issue_pipeline SET status = 'queued', queued_at = ? WHERE id = ?",
                    (now, row["id"]),
                )
                conn.commit()
                task = self._row_to_task(dict(row))
                task.status = "queued"
                task.queued_at = now
                return task
            finally:
                conn.close()

    def update_status(self, task_id: str, **kwargs: Any) -> None:
        """更新任务字段（仅更新 allowed 字段中非 None 的值）。

        Args:
            task_id: 任务 ID
            **kwargs: 允许的字段：status, started_at, completed_at,
                executor_result, rework_count, rework_feedback,
                review_decision, review_note, issue_spec
        """
        allowed = {
            "status", "started_at", "completed_at", "executor_result",
            "rework_count", "rework_feedback", "review_decision", "review_note",
            "issue_spec",
        }
        updates: dict[str, Any] = {
            k: v for k, v in kwargs.items()
            if k in allowed and v is not None
        }
        if not updates:
            return
        set_clauses: list[str] = []
        params: list[Any] = []
        for key, value in updates.items():
            if key in ("executor_result", "issue_spec", "rework_feedback"):
                set_clauses.append(f"{key} = ?")
                params.append(json.dumps(value))
            else:
                set_clauses.append(f"{key} = ?")
                params.append(value)
        params.append(task_id)
        sql = f"UPDATE issue_pipeline SET {', '.join(set_clauses)} WHERE id = ?"
        with _db_lock:
            conn = self._connect()
            try:
                conn.execute(sql, params)
                conn.commit()
            finally:
                conn.close()

    def get(self, task_id: str) -> PipelineTask | None:
        """按 id 获取任务。"""
        conn = self._connect()
        try:
            row = conn.execute(
                "SELECT * FROM issue_pipeline WHERE id = ?", (task_id,)
            ).fetchone()
            if row is None:
                return None
            return self._row_to_task(dict(row))
        finally:
            conn.close()

    def list_all(self) -> list[PipelineTask]:
        """返回所有任务（按 created_at DESC）。"""
        conn = self._connect()
        try:
            rows = conn.execute(
                "SELECT * FROM issue_pipeline ORDER BY created_at DESC"
            ).fetchall()
            return [self._row_to_task(dict(r)) for r in rows]
        finally:
            conn.close()

    def list_pending(self) -> list[PipelineTask]:
        """返回所有 pending/queued 任务（按 created_at ASC）。"""
        conn = self._connect()
        try:
            rows = conn.execute(
                "SELECT * FROM issue_pipeline WHERE status IN ('pending', 'queued') ORDER BY created_at ASC"
            ).fetchall()
            return [self._row_to_task(dict(r)) for r in rows]
        finally:
            conn.close()

    @staticmethod
    def _row_to_task(row: dict[str, Any]) -> PipelineTask:
        """将 sqlite3.Row dict 转为 PipelineTask。"""
        return PipelineTask(
            id=row["id"],
            created_at=row["created_at"],
            natural_language=row["natural_language"],
            issue_spec=json.loads(row["issue_spec"]) if row.get("issue_spec") else None,
            status=row["status"],
            queued_at=row.get("queued_at"),
            started_at=row.get("started_at"),
            completed_at=row.get("completed_at"),
            executor_result=json.loads(row["executor_result"]) if row.get("executor_result") else None,
            rework_count=row.get("rework_count", 0) or 0,
            rework_feedback=json.loads(row["rework_feedback"]) if row.get("rework_feedback") else [],
            review_decision=row.get("review_decision"),
            review_note=row.get("review_note"),
        )


# ---------------------------------------------------------------------------
# ResultReviewer：执行结果审查
# ---------------------------------------------------------------------------


class ResultReviewer:
    """审查执行结果，决定通过/返工/升级。"""

    # 最小有效 diff 长度（含 header 和至少一个 @@）
    MIN_DIFF_LENGTH = 10

    def review(self, task: PipelineTask) -> dict[str, Any]:
        """审查任务执行结果。

        Returns:
            dict 含 keys:
            - passes: bool — 是否通过审查
            - needs_rework: bool — 是否需要返工
            - escalated: bool — 是否已超出最大返工次数
            - feedback: list[str] — 审查反馈/错误上下文
        """
        feedback: list[str] = []
        result = task.executor_result or {}

        test_exit_code = result.get("test_exit_code")
        diff_text = result.get("diff_text", "")

        # 检查测试退出码
        if test_exit_code is None:
            feedback.append("测试未执行")
        elif test_exit_code != 0:
            feedback.append(f"测试失败（exit_code={test_exit_code}）")

        # 检查 diff 有效性：非空、含 "--- a/" 头部
        has_valid_diff = bool(
            diff_text
            and len(diff_text) >= self.MIN_DIFF_LENGTH
            and "--- a/" in diff_text
        )
        if not has_valid_diff:
            feedback.append("未生成有效 diff（缺少 '--- a/' 头部或 diff 为空）")

        needs_rework = bool(feedback)
        escalated = task.rework_count >= 2

        return {
            "passes": not needs_rework,
            "needs_rework": needs_rework,
            "escalated": escalated,
            "feedback": feedback,
        }


# ---------------------------------------------------------------------------
# PipelineDispatcher：调度器（编排执行 + 审查 + 返工循环）
# ---------------------------------------------------------------------------


class PipelineDispatcher:
    """调度器：驱动任务执行 → 审查 → 返工循环。

    用 RealRDExecutor(CodexAgentAdapter(cwd=REPO_ROOT)) 执行每个任务，
    审查结果后决定通过（→review 等待审批）或返工（重新排队，最多 2 次）。
    """

    def __init__(
        self,
        queue: IssueQueue | None = None,
        reviewer: ResultReviewer | None = None,
        repo_root: str | None = None,
        resolver: Any | None = None,
        pipeline_runtime: Any | None = None,
    ) -> None:
        self.queue = queue or IssueQueue()
        self.reviewer = reviewer or ResultReviewer()
        self._repo_root = repo_root or _REPO_ROOT
        # P0 接入：能力解析器 + 验收/返工自动闭环。缺省 None → 沿用原扁平队列逻辑。
        self.resolver = resolver
        self.pipeline_runtime = pipeline_runtime

    def _make_executor(self) -> Any:
        """构造 RealRDExecutor(CodexAgentAdapter)，用 pty 绕过 TTY 限制。"""
        from .dev_agent import CodexAgentAdapter
        from .real_rd_executor import RealRDExecutor

        # 最小事件日志（避免依赖真实 event_log DB schema）
        class _NullEventLog:
            database = None

            def record(self, **kwargs: Any) -> None:
                pass

        model = CodexAgentAdapter(
            cwd=self._repo_root,
            sandbox="danger-full-access",
            approval="never",
        )
        return RealRDExecutor(model=model, event_log=_NullEventLog())

    def _to_executor_spec(self, issue_spec: dict[str, Any]) -> dict[str, Any]:
        """将 Pipeline issue_spec 转换为 RealRDExecutor.run() 接受的格式。"""
        target_file = issue_spec.get("target_file", _DEFAULT_TARGET_FILE)
        expected_test = issue_spec.get("expected_test", _DEFAULT_TEST_PATH)
        return {
            "issue_id": issue_spec.get("issue_id", f"task-{uuid.uuid4().hex[:8]}"),
            "target_files": [target_file],
            "test_command_id": "rd_verify",
            "test_command_argv": ["pytest", expected_test],
            "instructions": issue_spec.get("issue", ""),
            "allow_paths": [target_file, expected_test],
            "max_rounds": int(issue_spec.get("max_rounds", 3) or 3),
        }

    def dispatch_one(self, task_id: str) -> PipelineTask:
        """执行单个任务：从队列获取 → 执行 → 审查 → 更新状态。

        Args:
            task_id: 任务 ID

        Returns:
            更新后的 PipelineTask

        Raises:
            ValueError: task_id 不存在
        """
        task = self.queue.get(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")

        # 更新为 running
        now = datetime.now(timezone.utc).isoformat()
        self.queue.update_status(task_id, status="running", started_at=now)
        task.status = "running"
        task.started_at = now

        # 构建 executor 并执行
        executor = self._make_executor()
        executor_spec = self._to_executor_spec(task.issue_spec or {})

        try:
            result = executor.run(executor_spec)
        except Exception as error:
            result = {
                "issue_id": executor_spec.get("issue_id", ""),
                "status": f"error: {type(error).__name__}",
                "rounds": 0,
                "diff_text": "",
                "test_exit_code": None,
                "files": [],
                "total_tokens": 0,
                "estimated_cost": 0.0,
                "audit_event_count": 0,
                "model_gateway_id": None,
                "model_name": None,
            }

        completed_at = datetime.now(timezone.utc).isoformat()
        self.queue.update_status(
            task_id,
            executor_result=result,
            completed_at=completed_at,
        )
        task.executor_result = result
        task.completed_at = completed_at

        # 审查
        review_result = self.reviewer.review(task)
        if review_result["passes"]:
            self.queue.update_status(task_id, status="review")
            task.status = "review"
        elif review_result["escalated"]:
            self.queue.update_status(task_id, status="failed")
            task.status = "failed"
        else:
            # 返工：追加反馈，重新排队
            new_feedback = list(task.rework_feedback)
            new_feedback.extend(review_result["feedback"])
            new_rework_count = task.rework_count + 1
            self.queue.update_status(
                task_id,
                status="pending",
                rework_count=new_rework_count,
                rework_feedback=new_feedback,
            )
            task.status = "pending"
            task.rework_count = new_rework_count
            task.rework_feedback = new_feedback

            # 如果有错误上下文，追加到 issue_spec 以指导下一轮
            if review_result["feedback"]:
                error_context = "; ".join(review_result["feedback"])
                updated_spec = dict(task.issue_spec or {})
                original_issue = updated_spec.get("issue", "")
                updated_spec["issue"] = (
                    f"{original_issue}\n\n"
                    f"上一次尝试失败：{error_context}，请修正这些问题"
                )
                self.queue.update_status(task_id, issue_spec=updated_spec)
                task.issue_spec = updated_spec

        return task

    def dispatch_auto(self, task_id: str, graph: Any | None = None) -> Any:
        """把扁平任务接入自动闭环（resolver + pipeline_runtime）。

        若已配置 ``pipeline_runtime``，则构造 TaskNode 走「执行→验收→重试→换能力→
        重规划→升级」闭环；否则回退原 ``dispatch_one`` 逻辑（保持向后兼容）。

        Returns:
            NodeResult（闭环结果）或 PipelineTask（回退路径）。
        """
        task = self.queue.get(task_id)
        if task is None:
            raise ValueError(f"Task {task_id} not found")
        if self.pipeline_runtime is None:
            return self.dispatch_one(task_id)

        from .task_graph import TaskGraph, TaskNode

        node = TaskNode(
            id=task.id,
            goal=task.natural_language,
            cap_requirement={"cap_type": "model"},
            status="running",
        )
        g = graph or TaskGraph(graph_id=task.id)
        g.add_node(node)
        result = self.pipeline_runtime.run_node(node, g)
        status_map = {"done": "approved", "escalated": "failed"}
        new_status = status_map.get(result.status, result.status)
        feedback = [result.reason] if result.reason else []
        self.queue.update_status(
            task_id,
            status=new_status,
            rework_count=node.rework_count,
            rework_feedback=feedback,
        )
        return result


# ---------------------------------------------------------------------------
# 便利函数：提交自然语言任务
# ---------------------------------------------------------------------------


def submit_natural_language(
    natural_language: str,
    queue: IssueQueue | None = None,
    parser: NLParser | None = None,
) -> PipelineTask:
    """提交自然语言任务：NL→IssueSpec → 入队。

    Args:
        natural_language: 自然语言描述
        queue: IssueQueue 实例（默认新建）
        parser: NLParser 实例（默认新建）

    Returns:
        已入队的 PipelineTask
    """
    queue = queue or IssueQueue()
    parser = parser or NLParser()

    issue_spec = parser.parse(natural_language)
    now = datetime.now(timezone.utc).isoformat()
    task = PipelineTask(
        id=issue_spec.get("issue_id", f"task-{uuid.uuid4().hex[:8]}"),
        created_at=now,
        natural_language=natural_language,
        issue_spec=issue_spec,
        status="pending",
    )
    queue.enqueue(task)
    return task


__all__ = [
    "PipelineTask",
    "NLParser",
    "IssueQueue",
    "ResultReviewer",
    "PipelineDispatcher",
    "submit_natural_language",
]
