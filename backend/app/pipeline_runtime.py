"""验收 / 返工自动闭环（P0-5：验收/返工自动闭环）。

``PipelineRuntime.run_node(node, graph)`` 实现「执行 → 验收 → 失败自动重试 → 自动换
能力（调 CapabilityResolver 下一级）→ 超 MAX_CAP_SWITCH 自动重规划 → 仍失败/硬卡点
升级 CEO」的**全自动闭环**，是「目标→执行→验收→返工→完成」无人盯守的核心。

设计要点（架构 §8③ 默认阈值）：
- 重试 / 换能力 / 重规划 / 升级 四级决策，全部自动，**仅硬卡点（降级链耗尽 /
  重规划不可用）才升级 CEO**（通过 NodeResult.escalated + graph.escalations 暴露，
  供 API 上报）。
- 复用 ``ResultReviewer``（``issue_pipeline.ResultReviewer``）做验收；能力选路复用
  ``CapabilityResolver``（P0-4）。
- 成功路径 / 失败原因 / 有效降级链 经 ``LessonMemory`` 持久化（P0-6），供后续复用。
- 每节点完成后经 ``ProjectState`` 聚合并写回（P0-6）。

零新依赖：仅标准库 + 复用既有模块。
"""
from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

from .capability_resolver import CapabilityExhausted, CapabilityUnavailable, CapabilityRequirement
from .issue_pipeline import PipelineTask, ResultReviewer
from .task_graph import TaskGraph, TaskNode


# 重规划次数硬上限（防止重规划死循环；与 MAX_REWORK/MAX_CAP_SWITCH 同属 P0 默认）。
MAX_REPLAN = 2


@dataclass
class NodeResult:
    """单节点执行结果（供调度器 / API 消费）。"""

    node_id: str
    status: str                       # done | escalated
    output: dict[str, Any] | None = None
    capability_path: list[str] = field(default_factory=list)
    escalated: bool = False
    reason: str | None = None
    review: dict[str, Any] | None = None


class PipelineRuntime:
    """验收 / 返工自动闭环编排器。"""

    def __init__(
        self,
        reviewer: ResultReviewer,
        resolver: Any | None = None,
        database: Any | None = None,
        event_log: Any | None = None,
        project_state: Any | None = None,
        lesson_memory: Any | None = None,
        max_rework: int = 2,
        max_cap_switch: int = 2,
        node_timeout: int = 900,
        max_replan: int = MAX_REPLAN,
        review_text_artifacts: bool = False,
    ) -> None:
        """初始化闭环。

        Args:
            reviewer: 验收器（ResultReviewer 实例，必填）。
            resolver: 能力解析器（CapabilityResolver）；缺省 None → 任何解析都升级。
            database: 可选，持久化用。
            event_log: 可选，升级/执行审计。
            project_state: 可选，节点完成后聚合进度。
            lesson_memory: 可选，经验沉淀。
            max_rework: 重试上限（默认 2，沿用 ResultReviewer.escalated 阈值）。
            max_cap_switch: 换能力上限（默认 2，超则重规划）。
            node_timeout: 节点超时秒（默认 900，info 用，真实超时由执行器负责）。
            max_replan: 重规划上限（默认 2）。
            review_text_artifacts: 验收放宽——模型节点成功且输出非空即视为通过
                （不再要求 ``--- a/`` 文件 diff）。用于 resolver 驱动的 auto-run 闭环
                （chat 类能力返回文本产物）；manual dispatch 路径保持默认 False。
        """
        self.reviewer = reviewer
        self.resolver = resolver
        self.database = database
        self.event_log = event_log
        self.project_state = project_state
        self.lesson_memory = lesson_memory
        self.max_rework = max_rework
        self.max_cap_switch = max_cap_switch
        self.node_timeout = node_timeout
        self.max_replan = max_replan
        self.review_text_artifacts = review_text_artifacts

    # ── 公共 API ──────────────────────────────────────────────────────────
    def run_node(self, node: TaskNode, graph: TaskGraph) -> NodeResult:
        """对单个节点执行「执行→验收→重试→换能力→重规划→升级」闭环。

        就地更新 ``node.status``（running/done/failed）与 ``graph.escalations``。
        返回 ``NodeResult``。
        """
        if self.resolver is None:
            return self._escalate(
                node, graph, reason="未配置能力解析器（resolver=None）", tried=[]
            )

        node.status = "running"
        req = node.cap_requirement_obj()

        tried: list[str] = []
        cap_switch = 0
        replan_count = 0
        retried_current = False
        current_handle = None

        while True:
            # 1) 选能力（含降级链；exclude 已尝试过的 → 自动换能力）。
            if current_handle is None:
                try:
                    handle = self.resolver.resolve(
                        req, exclude_keys=tried, employee_id=node.employee_id
                    )
                except (CapabilityExhausted, CapabilityUnavailable) as exc:
                    return self._escalate(
                        node, graph,
                        reason=f"能力不可用（降级链耗尽）：{exc}",
                        tried=tried,
                    )
                tried.append(handle.key)
                current_handle = handle
                retried_current = False

            # 2) 执行。
            prompt = self._build_prompt(node)
            node.attempts += 1
            try:
                result = current_handle.execute(prompt)
            except Exception as error:  # noqa: BLE001 — 执行异常视为该能力失败
                result = {
                    "output": "",
                    "status": f"error: {type(error).__name__}",
                    "model_gateway_id": current_handle.key,
                    "model_name": current_handle.key,
                }

            # 3) 验收（复用 ResultReviewer）。
            review = self._review(node, result)
            # 可观测：把本次尝试（含降级事件）写入节点 trace，供 /api/pipeline/{id}/trace 查询。
            try:
                _step = list(graph.nodes.keys()).index(node.id)
            except ValueError:
                _step = 0
            node.capability_path = list(tried)
            node.trace.append({
                "step": _step,
                "tool": current_handle.key,
                "status": result.get("status", "success"),
                "error": None if review["passes"] else (review.get("feedback") or ["review failed"]),
                "at": datetime.now(timezone.utc).isoformat(),
            })
            if review["passes"]:
                return self._succeed(node, graph, result, current_handle, tried, review)

            # 4) 验收失败 → 决策：先重试同能力一次，再换能力，超阈重规划。
            node.rework_count += 1

            if not retried_current:
                # 重试同能力一次（rework）。
                retried_current = True
                continue

            # 已重试过 → 必须换能力（resolver 下轮因 exclude 选下一个）。
            retried_current = False
            current_handle = None
            cap_switch += 1
            node.cap_switch_count = cap_switch

            if cap_switch > self.max_cap_switch:
                # 超阈 → 自动重规划（局部重生成子图）。
                replan_count += 1
                new_node = self._replan(node, graph, replan_count)
                if new_node is None or replan_count > self.max_replan:
                    return self._escalate(
                        node, graph,
                        reason="降级链耗尽且重规划不可用/超限",
                        tried=tried,
                    )
                node = new_node
                tried = []
                cap_switch = 0
                continue

            # 否则继续循环：resolver 下轮返回下一个可用能力。

    # ── 内部：提示词 / 验收 / 成功 / 升级 / 重规划 ───────────────────────────
    def _build_prompt(self, node: TaskNode) -> str:
        """构造执行提示词（含重规划/重试上下文）。"""
        parts = [node.goal]
        if node.rework_count:
            parts.append(f"（第 {node.rework_count} 次重试，请修正上次问题）")
        if node.cap_switch_count:
            parts.append(f"（已切换 {node.cap_switch_count} 次能力）")
        return "\n".join(parts)

    def _review(self, node: TaskNode, result: dict[str, Any]) -> dict[str, Any]:
        """把执行结果转 PipelineTask 交给 ResultReviewer 验收。"""
        status = result.get("status", "success")
        if node.cap_requirement_obj().cap_type == "tool" and status == "success":
            return {
                "passes": True,
                "needs_rework": False,
                "escalated": False,
                "feedback": [],
            }
        # auto-run 闭环放宽：模型节点由 chat 类能力执行，返回文本产物（非文件 diff）。
        # 成功且输出非空即视为通过，使「目标→执行→验收→完成」可端到端走通。
        if (
            self.review_text_artifacts
            and node.cap_requirement_obj().cap_type == "model"
            and status == "success"
            and (result.get("output") or "").strip()
        ):
            return {
                "passes": True,
                "needs_rework": False,
                "escalated": False,
                "feedback": [],
            }
        executor_result = {
            "output": result.get("output", ""),
            "status": status,
            "diff_text": result.get("output", ""),
            "test_exit_code": 0 if status == "success" else 1,
            "rounds": node.attempts,
        }
        task = PipelineTask(
            id=node.id,
            created_at=datetime.now(timezone.utc).isoformat(),
            natural_language=node.goal,
            executor_result=executor_result,
            rework_count=node.rework_count,
        )
        return self.reviewer.review(task)

    def _succeed(
        self,
        node: TaskNode,
        graph: TaskGraph,
        result: dict[str, Any],
        handle: Any,
        tried: list[str],
        review: dict[str, Any],
    ) -> NodeResult:
        """验收通过：标记完成、沉淀经验、聚合进度。"""
        node.status = "done"
        node.result = result
        node.note = None
        # 经验沉淀：成功路径（含有效降级链）。
        self._record_lesson(
            node, outcome="success", reason="验收通过", cap_path=tried,
        )
        # 项目级状态聚合 + 写回。
        self._aggregate_and_persist(graph)
        return NodeResult(
            node_id=node.id,
            status="done",
            output=result,
            capability_path=list(tried),
            escalated=False,
            reason=None,
            review=review,
        )

    def _escalate(
        self,
        node: TaskNode,
        graph: TaskGraph,
        reason: str,
        tried: list[str],
    ) -> NodeResult:
        """硬卡点升级 CEO：标记失败、记录升级、沉淀失败经验。"""
        node.status = "failed"
        node.note = reason
        graph.escalations.append({
            "node_id": node.id,
            "reason": reason,
            "capability_path": list(tried),
            "at": datetime.now(timezone.utc).isoformat(),
        })
        self._record_lesson(
            node, outcome="fail", reason=reason, cap_path=tried,
        )
        if self.event_log is not None:
            try:
                self.event_log.record(
                    correlation_id=str(uuid.uuid4()),
                    event_type="capability.escalated",
                    payload={
                        "node_id": node.id,
                        "reason": reason,
                        "capability_path": list(tried),
                    },
                )
            except Exception:
                pass
        self._aggregate_and_persist(graph)
        return NodeResult(
            node_id=node.id,
            status="escalated",
            output=None,
            capability_path=list(tried),
            escalated=True,
            reason=reason,
            review=None,
        )

    def _replan(
        self, node: TaskNode, graph: TaskGraph, replan_count: int
    ) -> TaskNode | None:
        """局部重规划：重置当前节点为「换策略重跑」并微调目标（最小可用重生成）。

        返回被重置后的（同一）节点，使闭环在清空计数后以新策略继续；若节点已无
        重规划空间则返回 None（触发升级）。子类/上层可重写以接入真正的规划器。
        """
        if graph is None:
            return None
        # 重置：清状态与计数，附加重规划标记，目标微调（占位「换策略」）。
        node.status = "pending"
        node.attempts = 0
        node.rework_count = 0
        node.cap_switch_count = 0
        node.note = f"自动重规划（第 {replan_count} 次）：换策略重试"
        # 不新增孤立节点，避免污染 graph 完成判定。
        return node

    # ── 经验沉淀 / 进度聚合 ───────────────────────────────────────────────
    def _record_lesson(
        self, node: TaskNode, outcome: str, reason: str, cap_path: list[str]
    ) -> None:
        if self.lesson_memory is None:
            return
        try:
            req = node.cap_requirement_obj()
            signature = f"{req.cap_type}:{node.goal[:24]}"
            self.lesson_memory.record(
                signature=signature,
                cap_path=list(cap_path),
                outcome=outcome,
                reason=reason,
            )
        except Exception:
            pass

    def _aggregate_and_persist(self, graph: TaskGraph) -> None:
        if self.project_state is None:
            return
        try:
            self.project_state.aggregate(graph)
            self.project_state.persist()
        except Exception:
            pass
