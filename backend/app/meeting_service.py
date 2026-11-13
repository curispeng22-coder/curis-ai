"""Canonical Meeting projection over existing shared Runtime primitives."""

from __future__ import annotations

import json
import hashlib
import re
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from typing import Any, Awaitable, Callable
from uuid import uuid4

from .database import Database
from .employee_execution_identity import EmployeeExecutionIdentity
from .knowledge_service import KnowledgeService
from .result_store import ResultStore
from .runtime.child_work import CanonicalChildWorkRuntime, ChildWorkError
from .runtime.foundation import RuntimeFoundation, RuntimeScopeError
from .runtime.general_workspace_delivery import GeneralWorkspaceDelivery, GeneralWorkspaceGap
from .runtime.responsibility_routing import ResponsibilityRoutingError, ResponsibilityRoutingRuntime
from .shared_workspace_projection import SharedWorkspaceProjection
from .tenant_context import TenantContext


EmployeeExecution = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class MeetingService:
    """Keep Meeting identity local while every business object remains canonical."""

    CONTEXT_TYPES = frozenset({"KNOWLEDGE", "WORK", "ARTIFACT", "EVIDENCE", "RESULT"})
    CEO_MODES = frozenset({"DECISION_ONLY", "OBSERVE", "JOIN"})

    LIMITS = {
        "maxTurns": 6,
        "maxConsecutiveTurns": 1,
        "maxNoProgress": 2,
        # maxProviderCalls 是「全局」provider call 上限，覆盖 门控 + 员工发言 + Leader 评估
        # 三类调用（不是每个员工 30 次）。3 员工时每轮 3+1+1=5 次，6 轮 = 30。
        "maxProviderCalls": 30,
        # 2026-09-05 live DeepSeek calibration: 11,207 tokens / four-call round;
        # six rounds ~67,242 plus bounded Work/context headroom. Saved limits stay intact.
        "maxConfirmedTokens": 80000,
        "maxConfirmedCost": "1.00",
        "maxElapsedSeconds": 300,
    }

    def __init__(self, database: Database, employee_execution: EmployeeExecution | None = None):
        self.db = database
        self.foundation = RuntimeFoundation(database)
        self.general = GeneralWorkspaceDelivery(database)
        self.shared = SharedWorkspaceProjection(database)
        self.routing = ResponsibilityRoutingRuntime(database)
        self.child_work = CanonicalChildWorkRuntime(database)
        self.identities = EmployeeExecutionIdentity(database)
        self.knowledge = KnowledgeService(database)
        self.employee_execution = employee_execution

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def _scope(self, company_id: str, business_id: str, workspace_id: str) -> tuple[str, str]:
        with self.db.connect() as connection:
            company = connection.execute(
                "select 1 from companies where tenant_id=? and company_id=?",
                (self.tenant_id, company_id),
            ).fetchone()
            if company is None:
                raise RuntimeScopeError("Company is outside the current tenant")
            workspace = None
            if workspace_id:
                workspace = connection.execute(
                    "select company_id, business_id, business_relation_status from workspaces "
                    "where tenant_id=? and workspace_id=?",
                    (self.tenant_id, workspace_id),
                ).fetchone()
                if workspace is None or workspace["company_id"] != company_id:
                    raise RuntimeScopeError("Workspace is outside the current Company")
                if workspace["business_relation_status"] != "RESOLVED" or not workspace["business_id"]:
                    raise RuntimeScopeError("Workspace has no resolved canonical Business")
                if business_id and workspace["business_id"] != business_id:
                    raise RuntimeScopeError("Workspace and Business do not match")
                business_id = workspace["business_id"]
            if business_id:
                business = connection.execute(
                    "select 1 from canonical_businesses where tenant_id=? and company_id=? and business_id=?",
                    (self.tenant_id, company_id, business_id),
                ).fetchone()
                if business is None:
                    raise RuntimeScopeError("Business is outside the current Company")
        return business_id, workspace_id

    def _participants(self, company_id: str, participant_refs: list[str], leader_ref: str) -> list[dict[str, Any]]:
        refs = list(dict.fromkeys(item.strip() for item in participant_refs if item.strip()))
        if not leader_ref or leader_ref not in refs:
            raise ValueError("推进负责人必须是会议参与员工")
        if not refs:
            raise ValueError("会议至少需要一名参与员工")
        marks = ",".join("?" for _ in refs)
        with self.db.connect() as connection:
            rows = connection.execute(
                f"select id, name, role, avatar_ref, status from employee_instances "
                f"where tenant_id=? and company_id=? and enabled=1 and deleted_at is null and id in ({marks})",
                (self.tenant_id, company_id, *refs),
            ).fetchall()
        by_id = {row["id"]: dict(row) for row in rows}
        if len(by_id) != len(refs):
            raise RuntimeScopeError("会议参与人必须是当前公司的在职员工")
        return [by_id[ref] for ref in refs]

    def _context(self, company_id: str, workspace_id: str, refs: list[dict[str, str]]) -> list[dict[str, str]]:
        normalized: list[dict[str, str]] = []
        for item in refs:
            kind = str(item.get("type") or "").upper().strip()
            ref = str(item.get("ref") or "").strip()
            if kind not in self.CONTEXT_TYPES or not ref:
                raise ValueError("会议资料引用类型无效")
            if kind == "KNOWLEDGE":
                with self.db.connect() as connection:
                    row = connection.execute(
                        "select company_id, target_type, target_ref from knowledge_entries "
                        "where tenant_id=? and id=? and lifecycle_status='ACTIVE'",
                        (self.tenant_id, ref),
                    ).fetchone()
                if row is None or row["company_id"] not in {None, "", company_id}:
                    raise RuntimeScopeError("Knowledge reference is outside the current Company")
                if workspace_id and row["target_type"] == "WORKSPACE" and row["target_ref"] != workspace_id:
                    raise RuntimeScopeError("Knowledge reference is outside the current Workspace")
            elif kind in {"WORK", "EVIDENCE"}:
                entity = self.foundation.get(ref)
                if entity["entity_type"] != kind or entity["company_id"] != company_id:
                    raise RuntimeScopeError("Runtime reference is outside the current Company")
                if workspace_id and entity["workspace_id"] != workspace_id:
                    raise RuntimeScopeError("Runtime reference is outside the current Workspace")
            else:
                if not workspace_id:
                    raise RuntimeScopeError("Result and Artifact references require a Workspace scope")
                self.shared.result(company_id, workspace_id, ref)
            normalized.append({"type": kind, "ref": ref})
        return list({(item["type"], item["ref"]): item for item in normalized}.values())

    @staticmethod
    def _message(kind: str, actor_type: str, actor_ref: str, text: str, **refs: Any) -> dict[str, Any]:
        return {
            "messageId": f"meeting-message-{uuid4()}",
            "kind": kind,
            "actorType": actor_type,
            "actorRef": actor_ref,
            "text": text.strip()[:4000],
            "createdAt": _now(),
            **refs,
        }

    def _save(self, meeting: dict[str, Any], **changes: Any) -> dict[str, Any]:
        value = meeting | changes
        return self.db.save_strategy_meeting(
            meeting_id=value["meeting_id"], tenant_id=self.tenant_id,
            company_id=value.get("company_id") or "", business_id=value.get("business_id") or "",
            workspace_id=value.get("workspace_id") or "", title=value["title"],
            agenda=value.get("agenda") or "", background=value.get("background") or "",
            participants=value.get("participants") or [], leader_employee_id=value.get("leader_employee_id") or "",
            ceo_participation_mode=value.get("ceo_participation_mode") or "DECISION_ONLY",
            conversation_id=value.get("conversation_id") or "", context_refs=value.get("context_refs") or [],
            decision_ref=value.get("decision_ref") or "", work_refs=value.get("work_refs") or [],
            result_refs=value.get("result_refs") or [], continuation_gap=value.get("continuation_gap") or "",
            orchestration=value.get("orchestration") or {},
            status=value.get("status") or "active", timeline=value.get("timeline") or [],
            closed_at=value.get("closed_at"),
        )

    @classmethod
    def _orchestration(cls, *, event: dict[str, Any] | None = None) -> dict[str, Any]:
        return {
            "version": 1,
            "budgetVersion": 1,
            "currentCycle": None,
            "cycleHistory": [],
            "status": "READY",
            "workflowKey": "",
            "assignments": {},
            "pendingEvents": [event] if event else [],
            "lastProcessedEventId": "",
            "activeRunId": "",
            "runStartedAt": None,
            "turnCount": 0,
            "providerCallCount": 0,
            "noProgressCount": 0,
            "lastVisibleSpeakerRef": "",
            "consecutiveVisibleTurns": 0,
            "contentHashes": [],
            "proposal": None,
            "turns": [],
            "usage": {"confirmedTokens": 0, "confirmedCost": "0", "unknownMetering": False},
            "limits": dict(cls.LIMITS),
            "lastOutcome": "",
            "blockedReason": "",
        }

    @staticmethod
    def _event(kind: str, source_ref: str, *, message_ref: str = "", refs: list[str] | None = None,
               requested_speaker_ref: str = "") -> dict[str, Any]:
        return {
            "eventId": f"meeting-event-{uuid4()}",
            "kind": kind,
            "sourceRef": source_ref,
            "messageRef": message_ref,
            "refs": list(dict.fromkeys(refs or [])),
            "requestedSpeakerRef": requested_speaker_ref,
            "createdAt": _now(),
        }

    def _update_orchestration(self, meeting_id: str, mutate) -> dict[str, Any]:
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute(
                "select orchestration_json from strategy_meetings where tenant_id=? and meeting_id=?",
                (self.tenant_id, meeting_id),
            ).fetchone()
            if row is None:
                raise KeyError(meeting_id)
            current = json.loads(row["orchestration_json"] or "{}")
            updated = mutate(dict(current))
            connection.execute(
                "update strategy_meetings set orchestration_json=?, updated_at=current_timestamp "
                "where tenant_id=? and meeting_id=?",
                (json.dumps(updated, ensure_ascii=False), self.tenant_id, meeting_id),
            )
        return updated

    def _queue_event(self, meeting_id: str, event: dict[str, Any]) -> dict[str, Any]:
        def mutate(state: dict[str, Any]) -> dict[str, Any]:
            self._import_cycle_history(meeting_id, state)
            for cycle in [*state.get("cycleHistory", []), state.get("currentCycle") or {}]:
                if event["eventId"] == cycle.get("triggerEventId") or event["eventId"] in cycle.get("eventIds", []):
                    event["budgetCycleId"] = cycle["cycleId"]
                    break
            if event.get("kind") == "RESULT_RETURNED" and state.get("activeRunId") and state.get("currentCycle"):
                event.setdefault("budgetCycleId", state["currentCycle"]["cycleId"])
            pending = list(state.get("pendingEvents") or [])
            if not any(item.get("eventId") == event["eventId"] for item in pending):
                pending.append(event)
            state.update({"pendingEvents": pending[-32:], "status": "READY", "blockedReason": ""})
            return state
        return self._update_orchestration(meeting_id, mutate)

    def _meeting_task_refs(self, meeting_id: str) -> list[str]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None:
            raise KeyError(meeting_id)
        prefixes = (f"meeting:{meeting_id}:", f"meeting-work:{meeting_id}:")
        with self.db.connect() as connection:
            return [row["task_id"] for row in connection.execute(
                "select task_id from tasks where tenant_id=? and company_id=? and workspace_id=? and "
                "(substr(execution_ref,1,?)=? or substr(execution_ref,1,?)=?)",
                (self.tenant_id, meeting["company_id"], meeting["workspace_id"],
                 len(prefixes[0]), prefixes[0], len(prefixes[1]), prefixes[1]),
            )]

    def _import_cycle_history(self, meeting_id: str, state: dict[str, Any]) -> None:
        if state.get("budgetVersion"):
            return
        state.update(budgetVersion=1, currentCycle=None, cycleHistory=[])
        if not (state.get("providerCallCount") or state.get("turnCount") or self._meeting_task_refs(meeting_id)):
            return
        # Historical totals have no proven event-budget boundary. Preserve them;
        # old pending/derived events cannot be relabelled as a fresh allowance.
        cycle_id = f"meeting-budget-legacy-{meeting_id}"
        state["currentCycle"] = {
            "cycleId": cycle_id, "triggerEventId": "", "legacy": True,
            "startedAt": state.get("runStartedAt"), "endedAt": _now(),
            "exhausted": True, "providerCallCount": state.get("providerCallCount", 0),
            "usage": dict(state.get("usage") or {}), "turnCount": state.get("turnCount", 0),
            "excludedTaskRefs": [], "eventIds": [],
        }
        for event in state.get("pendingEvents") or []:
            event["budgetCycleId"] = cycle_id

    @staticmethod
    def _cycle_event(state: dict[str, Any], kind: str, source_ref: str, **kwargs: Any) -> dict[str, Any]:
        event = MeetingService._event(kind, source_ref, **kwargs)
        cycle = state.get("currentCycle")
        if cycle:
            event["budgetCycleId"] = cycle["cycleId"]
        return event

    def _team_truth(self, meeting: dict[str, Any]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
        workflows = [
            item for item in self.foundation.list(
                "RESPONSIBILITY_WORKFLOW", company_id=meeting["company_id"], workspace_id=meeting["workspace_id"],
            )
            if item["data"].get("scopeType") == "WORKSPACE"
            and item["data"].get("scopeRef") == meeting["workspace_id"]
            and not str(item["data"].get("workflowKey") or "").startswith("meeting:")
        ]
        assignments: dict[str, dict[str, Any]] = {}
        for workflow in sorted(workflows, key=lambda item: int(item["data"].get("version") or 0), reverse=True):
            for assignment in workflow["data"].get("assignments") or []:
                runtime_ref = str(assignment.get("employeeRef") or "")
                try:
                    identity = self.identities.resolve(
                        company_id=meeting["company_id"], workspace_id=meeting["workspace_id"],
                        runtime_employee_ref=runtime_ref,
                    )
                except (KeyError, RuntimeScopeError):
                    continue
                company_ref = identity["company_employee_ref"]
                if company_ref in meeting["participants"]:
                    previous = assignments.get(company_ref)
                    if previous and previous["assignmentRef"] != assignment["assignmentRef"]:
                        raise ValueError(f"员工 {company_ref} 在当前工作空间有多个可执行责任")
                    assignments[company_ref] = assignment | {"runtimeEmployeeRef": runtime_ref}
        missing = [ref for ref in meeting["participants"] if ref not in assignments]
        if missing:
            raise ValueError("参会员工尚未绑定当前工作空间责任与执行能力：" + "、".join(missing))
        key = f"meeting:{meeting['meeting_id']}"
        existing = [
            item for item in self.foundation.list(
                "RESPONSIBILITY_WORKFLOW", company_id=meeting["company_id"], workspace_id=meeting["workspace_id"],
            ) if item["data"].get("workflowKey") == key
        ]
        if existing:
            workflow = max(existing, key=lambda item: int(item["data"].get("version") or 0))
        else:
            leader = assignments[meeting["leader_employee_id"]]
            workflow = self.routing.publish_workflow(
                company_id=meeting["company_id"], workspace_id=meeting["workspace_id"],
                scope_type="WORKSPACE", scope_ref=meeting["workspace_id"], workflow_key=key,
                assignment_refs=[assignments[ref]["assignmentRef"] for ref in meeting["participants"]],
                default_flow=[leader["responsibilityKey"]],
            )
        return workflow, assignments

    def create(self, *, company_id: str, title: str, background: str, business_id: str = "",
               workspace_id: str = "", participant_refs: list[str], leader_ref: str,
               ceo_participation_mode: str, context_refs: list[dict[str, str]]) -> dict[str, Any]:
        title = title.strip()
        if not title:
            raise ValueError("会议议题不能为空")
        mode = ceo_participation_mode.upper().strip()
        if mode not in self.CEO_MODES:
            raise ValueError("CEO参与方式无效")
        business_id, workspace_id = self._scope(company_id, business_id, workspace_id)
        participants = self._participants(company_id, participant_refs, leader_ref)
        refs = self._context(company_id, workspace_id, context_refs)
        meeting_id = f"meeting-{uuid4()}"
        system_message = self._message("SYSTEM", "SYSTEM", "", "会议已开始。")
        event = self._event("MEETING_STARTED", meeting_id, message_ref=system_message["messageId"])
        meeting = self.db.save_strategy_meeting(
            meeting_id=meeting_id, tenant_id=self.tenant_id, company_id=company_id,
            business_id=business_id, workspace_id=workspace_id, title=title,
            agenda=background.strip(), background=background.strip(),
            participants=[item["id"] for item in participants], leader_employee_id=leader_ref,
            ceo_participation_mode=mode, conversation_id=f"conversation-{uuid4()}",
            context_refs=refs, status="active",
            timeline=[system_message], orchestration=self._orchestration(event=event),
            continuation_gap="",
        )
        try:
            workflow, assignments = self._team_truth(meeting)
            orchestration = meeting["orchestration"] | {
                "workflowKey": workflow["data"]["workflowKey"],
                "assignments": {
                    ref: {
                        "assignmentRef": item["assignmentRef"],
                        "runtimeEmployeeRef": item["runtimeEmployeeRef"],
                        "responsibilityKey": item["responsibilityKey"],
                        "responsibility": item["responsibility"],
                    }
                    for ref, item in assignments.items()
                },
            }
            meeting = self._save(meeting, orchestration=orchestration, continuation_gap="")
        except (KeyError, ValueError, ResponsibilityRoutingError, RuntimeScopeError) as error:
            orchestration = meeting["orchestration"] | {
                "status": "BLOCKED", "blockedReason": str(error), "pendingEvents": [],
            }
            meeting = self._save(
                meeting, orchestration=orchestration,
                continuation_gap=f"MEETING_TEAM_EXECUTION_UNAVAILABLE: {error}",
            )
        return self._view(meeting)

    def list(self, company_id: str) -> dict[str, Any]:
        self._scope(company_id, "", "")
        meetings = [self._view(item, sync=False) for item in self.db.list_strategy_meetings(self.tenant_id, company_id)]
        return {
            "active": [item for item in meetings if item["status"] != "closed"],
            "history": [item for item in meetings if item["status"] == "closed"],
        }

    def get(self, company_id: str, meeting_id: str, *, sync: bool = True) -> dict[str, Any]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None or meeting.get("company_id") != company_id:
            raise KeyError(meeting_id)
        if sync:
            meeting = self.sync(company_id, meeting_id, hydrate=False)
        return self._view(meeting)

    def add_message(self, company_id: str, meeting_id: str, *, actor_type: str,
                    actor_ref: str, text: str, context_refs: list[dict[str, str]] | None = None) -> dict[str, Any]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None or meeting.get("company_id") != company_id:
            raise KeyError(meeting_id)
        if meeting["status"] == "closed":
            raise ValueError("会议已结束，不能继续发言")
        actor = actor_type.upper().strip()
        if actor not in {"CEO", "EMPLOYEE"}:
            raise ValueError("会议发言身份无效")
        if actor == "EMPLOYEE" and actor_ref not in meeting["participants"]:
            raise RuntimeScopeError("Employee is not a Meeting participant")
        if not text.strip():
            raise ValueError("消息不能为空")
        added = self._context(company_id, meeting["workspace_id"], context_refs or [])
        refs = list({(item["type"], item["ref"]): item
                     for item in [*(meeting.get("context_refs") or []), *added]}.values())
        if len(refs) > 32:
            raise ValueError("会议资料引用已达到上限，请只选择当前相关资料")
        message = self._message("MESSAGE", actor, actor_ref, text)
        meeting = self._save(meeting, timeline=[*meeting["timeline"], message], context_refs=refs)
        if actor == "CEO":
            requested = next((
                item["id"] for item in self._participants(
                    meeting["company_id"], meeting["participants"], meeting["leader_employee_id"],
                ) if f"@{item['name']}" in text or f"＠{item['name']}" in text
            ), "")
            self._queue_event(
                meeting_id,
                self._event(
                    "CEO_MESSAGE", message["messageId"], message_ref=message["messageId"],
                    refs=[item["ref"] for item in added],
                    requested_speaker_ref=requested,
                ),
            )
            meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        return self._view(meeting)

    @staticmethod
    def _fact(value: Any) -> dict[str, str]:
        return GeneralWorkspaceDelivery._decision_fact(value)

    def _map_leader_decision(self, meeting: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
        """Map bounded judgment content, never model-authored identity, into existing P7."""
        proposal = meeting["orchestration"].get("proposal") or {}
        proposal_ref = proposal.get("artifactRef")
        if not proposal_ref:
            raise ValueError("需要先形成可追溯的会议方案，再请求你的决定。")
        self.shared.result(meeting["company_id"], meeting["workspace_id"], proposal_ref)
        selected = self._context(meeting["company_id"], meeting["workspace_id"], meeting["context_refs"])
        legal = {item["ref"] for item in selected} | set(meeting["result_refs"])
        refs = list(dict.fromkeys([*proposal.get("evidenceRefs", []), *request.get("evidenceRefs", [])]))
        if any(ref not in legal for ref in refs):
            raise RuntimeScopeError("决策引用了本次会议未选择的资料，请核对来源后重试。")
        for ref in refs:
            if ref in meeting["result_refs"]:
                self.shared.result(meeting["company_id"], meeting["workspace_id"], ref)
        fields = ("event", "cannotDecideReason", "ceoChoicePrompt", "continuationPlan")
        if any(not isinstance(request.get(key), str) or not request[key].strip() for key in fields):
            raise ValueError("决策方案尚未说明清楚问题、为何需要你判断或选择后的工作，请负责人补充。")
        options = request.get("options")
        if not isinstance(options, list) or not 2 <= len(options) <= 4 or any(not isinstance(o, dict) for o in options):
            raise ValueError("决策方案需要两到四个可比较的选择。")
        index = request.get("recommendationIndex")
        if index is None:  # Existing accepted callers retain their local option vocabulary.
            recommended_id = (request.get("recommendation") or {}).get("optionId")
            index = next((i for i, option in enumerate(options)
                          if recommended_id and option.get("optionId") == recommended_id), None)
        if type(index) is not int or not 0 <= index < len(options):
            raise ValueError("负责人尚未明确推荐哪个方案，请补充推荐及理由。")

        def judgment(value: Any) -> dict[str, str]:
            if value is None:
                return {"value": "尚未验证", "provenance": "UNK"}
            fact = self._fact(value)
            # Model wording alone is not verified FACT/POLICY/EVIDENCE provenance.
            if fact["provenance"] != "UNK":
                fact["provenance"] = "EST"
            return fact

        if not request.get("recommendationReason"):
            raise ValueError("负责人尚未提供推荐理由。")
        return {
            **{key: request[key] for key in fields},
            "decisionKey": f"meeting:{meeting['meeting_id']}:proposal:{proposal_ref}",
            "complexity": "HIGH_RISK",  # Explicit trade-off: require Layer1, never quick-approve model risk claims.
            "options": [{"optionId": f"OPTION_{i + 1}", "label": option.get("label"),
                         **{key: judgment(option.get(key)) for key in ("impact", "risk", "cost")}}
                        for i, option in enumerate(options)],
            "recommendation": {"optionId": f"OPTION_{index + 1}", "provenance": "EST"},
            "recommendationReason": judgment(request["recommendationReason"]),
            "evidenceRefs": refs, "resultRefs": [proposal_ref],
            "workContract": {"problem": request["event"], "expectedResult": request["continuationPlan"],
                             "constraints": [meeting["background"], "仅执行CEO所选方案；未知事实保持未知，外部动作另行确认。"],
                             "references": [item["ref"] for item in selected]},
        }

    def request_decision(self, company_id: str, meeting_id: str, packet: dict[str, Any]) -> dict[str, Any]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None or meeting.get("company_id") != company_id:
            raise KeyError(meeting_id)
        if meeting["status"] == "closed" or not meeting.get("workspace_id"):
            raise ValueError("会议需要有效工作空间才能形成运行决定")
        key = str(packet.get("decisionKey") or "").strip()
        complexity = str(packet.get("complexity") or "").upper()
        event = str(packet.get("event") or "").strip()
        cannot_decide = str(packet.get("cannotDecideReason") or "").strip()
        choice_prompt = str(packet.get("ceoChoicePrompt") or "").strip()
        continuation = str(packet.get("continuationPlan") or "").strip()
        options = packet.get("options")
        if complexity not in {"LOW_RISK", "HIGH_RISK"} or not all((key, event, cannot_decide, choice_prompt, continuation)):
            raise ValueError("Decision Packet is incomplete")
        if not isinstance(options, list) or not 2 <= len(options) <= 4:
            raise ValueError("Decision Packet requires two to four options")
        normalized, ids = [], set()
        for option in options:
            option_id = str(option.get("optionId") or "").strip() if isinstance(option, dict) else ""
            label = str(option.get("label") or "").strip() if isinstance(option, dict) else ""
            if not option_id or option_id in ids or not label:
                raise ValueError("Decision option is incomplete")
            ids.add(option_id)
            normalized.append({
                "optionId": option_id, "label": label[:240],
                "impact": self._fact(option.get("impact")),
                "risk": self._fact(option.get("risk")),
                "cost": self._fact(option.get("cost")),
            })
        recommendation = packet.get("recommendation") or {}
        recommendation_id = str(recommendation.get("optionId") or "").strip()
        recommendation_provenance = str(recommendation.get("provenance") or "").upper()
        if recommendation_id not in ids or recommendation_provenance not in {"FACT", "POLICY", "EVIDENCE", "EST", "UNK"}:
            raise ValueError("Decision recommendation is invalid")
        reason = self._fact(packet.get("recommendationReason"))
        current = None
        if meeting.get("decision_ref"):
            current = self.foundation.get(meeting["decision_ref"])
            if current["data"].get("decisionKey") == key:
                return self._view(meeting)
            if current["lifecycle_status"] == "WAITING_CEO":
                raise ValueError("会议已有一个等待CEO处理的决定")
        data = {
            "kind": "MEETING_DECISION", "meetingRef": meeting_id,
            "businessRef": meeting.get("business_id") or "",
            "proposalRef": (meeting["orchestration"].get("proposal") or {}).get("artifactRef") or "",
            "requesterRef": meeting["leader_employee_id"],
            "assignmentRef": (meeting["orchestration"].get("assignments", {}).get(meeting["leader_employee_id"]) or {}).get("assignmentRef") or "",
            "conversationRef": meeting["conversation_id"], "decisionKey": key,
            "complexity": complexity,
            "layer0Actions": ["VIEW_OPTIONS", "DEFER"] if complexity == "HIGH_RISK" else ["FOLLOW_RECOMMENDATION", "VIEW_OPTIONS", "DEFER"],
            "event": event[:2000], "cannotDecideReason": cannot_decide[:2000],
            "options": normalized,
            "recommendation": {"optionId": recommendation_id, "provenance": recommendation_provenance},
            "recommendationReason": reason, "ceoChoicePrompt": choice_prompt[:1000],
            "continuationPlan": continuation[:2000], "workContract": packet.get("workContract") or {},
            "resultRefs": list(packet.get("resultRefs") or []),
            "evidenceRefs": list(packet.get("evidenceRefs") or []), "createdAt": _now(),
        }
        decision_id = "decision_packet-" + hashlib.sha256(f"{self.tenant_id}:{meeting_id}:{key}".encode()).hexdigest()
        try:
            decision = self.foundation.get(decision_id)
        except KeyError:
            decision = self.foundation.create(
                "DECISION_PACKET", company_id=company_id, workspace_id=meeting["workspace_id"],
                entity_id=decision_id, parent_id=meeting_id, owner_ref=meeting["leader_employee_id"], data=data,
            )
        if decision["lifecycle_status"] == "DRAFT":
            decision = self.foundation.transition(decision["entity_id"], "READY", actor="AI_EMPLOYEE", trigger="prepare")
        if decision["lifecycle_status"] == "READY":
            decision = self.foundation.transition(
                decision["entity_id"], "WAITING_CEO", actor="AI_EMPLOYEE", trigger="request_decision",
                reason=cannot_decide, evidence_refs=data["evidenceRefs"],
            )
        if decision["lifecycle_status"] != "WAITING_CEO":
            raise ValueError("该决定已有处理记录，需要核对原会议关联，不能重复创建。")
        if not meeting["orchestration"].get("currentCycle"):
            # A direct existing P7 request can precede the first model turn.
            # Close its initial event budget too; it cannot later refill a Work run.
            self._claim_advance(meeting_id)
            meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting["orchestration"].get("currentCycle"):
            meeting["orchestration"]["currentCycle"]["endedAt"] = _now()
        meeting = self._save(
            meeting, decision_ref=decision["entity_id"], orchestration=meeting["orchestration"] | {
                "status": "WAITING_CEO", "activeRunId": "", "runStartedAt": None,
                "lastOutcome": "NEEDS_CEO_DECISION",
            },
            timeline=[*meeting["timeline"], self._message(
                "DECISION_REQUEST", "EMPLOYEE", meeting["leader_employee_id"],
                "我发现这里需要你的判断，已经整理了方案和建议。",
                decisionRef=decision["entity_id"],
            )],
        )
        return self._view(meeting)

    def review_decision(self, company_id: str, meeting_id: str) -> dict[str, Any]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None or meeting.get("company_id") != company_id or not meeting.get("decision_ref"):
            raise KeyError(meeting_id)
        decision = self.foundation.get(meeting["decision_ref"])
        if decision["lifecycle_status"] != "WAITING_CEO":
            raise ValueError("Decision Package is not waiting for CEO")
        if not decision["data"].get("layer1ReviewedAt"):
            data = decision["data"] | {"layer1ReviewedAt": _now()}
            with self.db.connect() as connection:
                connection.execute(
                    "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                    (json.dumps(data, ensure_ascii=False), _now(), self.tenant_id, decision["entity_id"]),
                )
        return self._view(meeting)

    def choose_decision(self, company_id: str, meeting_id: str, *, choice: str, reason: str) -> dict[str, Any]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None or meeting.get("company_id") != company_id or not meeting.get("decision_ref"):
            raise KeyError(meeting_id)
        decision = self.foundation.get(meeting["decision_ref"])
        choice, reason = choice.strip(), reason.strip()
        if not choice or not reason:
            raise ValueError("Decision choice and reason are required")
        if decision["lifecycle_status"] == "APPLIED":
            if decision["data"].get("choice") != choice:
                raise ValueError("Decision was already applied with another choice")
            return self._view(meeting)
        if decision["lifecycle_status"] != "WAITING_CEO":
            raise ValueError("Decision Package is not waiting for CEO")
        if choice == "DEFER":
            data = decision["data"] | {"deferredAt": _now(), "deferReason": reason[:2000]}
            with self.db.connect() as connection:
                connection.execute(
                    "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                    (json.dumps(data, ensure_ascii=False), _now(), self.tenant_id, decision["entity_id"]),
                )
            return self._view(meeting)
        options = {item.get("optionId") for item in decision["data"].get("options") or []}
        if choice not in options:
            raise ValueError("Decision choice is not available")
        if decision["data"].get("complexity") == "HIGH_RISK" and not decision["data"].get("layer1ReviewedAt"):
            raise ValueError("High-risk Decision requires review before choosing")
        self.foundation.transition(decision["entity_id"], "DECIDED", actor="CEO", trigger="decide", reason=reason, context={"choice": choice})
        decision = self.foundation.transition(decision["entity_id"], "APPLIED", actor="SYSTEM", trigger="apply", reason=reason, context={"choice": choice})
        data = decision["data"] | {"choice": choice, "choiceReason": reason[:2000], "decidedAt": _now(), "appliedAt": _now()}
        work_refs = list(meeting["work_refs"])
        gap = ""
        contract = data.get("workContract") or {}
        if not data.get("workRef"):
            try:
                created = self.general.create_work(
                    company_id=company_id, workspace_id=meeting["workspace_id"],
                    problem=str(contract.get("problem") or data["event"]) + "\nCEO选择：" + next(item["label"] for item in data["options"] if item["optionId"] == choice),
                    expected_result=str(contract.get("expectedResult") or data["continuationPlan"]),
                    constraints=list(contract.get("constraints") or []),
                    references=list(contract.get("references") or meeting["context_refs"] and [item["ref"] for item in meeting["context_refs"]]),
                    idempotency_key=f"meeting:{meeting_id}:decision:{decision['entity_id']}",
                )
                data["workRef"] = created["work"]["entity_id"]
                work_refs = list(dict.fromkeys([*work_refs, data["workRef"]]))
            except GeneralWorkspaceGap as error:
                gap = f"{error.payload['code']}: {error.payload['reason']}；{error.payload['next_action']}"
            except (KeyError, RuntimeScopeError, ValueError) as error:
                gap = f"WORK_CONTINUATION_UNAVAILABLE: {error}"
        with self.db.connect() as connection:
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (json.dumps(data, ensure_ascii=False), _now(), self.tenant_id, decision["entity_id"]),
            )
        message = self._message(
            "DECISION_RESULT", "CEO", "", "决定已记录，运行系统正在按结论继续。",
            decisionRef=decision["entity_id"], workRef=data.get("workRef") or "",
        )
        if gap:
            message["text"] = "决定已记录；后续工作尚未启动，缺口已保留。"
            message["gap"] = gap
        meeting = self._save(
            meeting, work_refs=work_refs, continuation_gap=gap,
            orchestration=meeting["orchestration"] | {
                "status": "BLOCKED" if gap else "WAITING_WORK",
                "blockedReason": gap,
                "lastOutcome": "BLOCKED" if gap else "WAIT_FOR_WORK",
                "activeRunId": "", "runStartedAt": None,
            },
            timeline=[*meeting["timeline"], message],
        )
        # The persisted CEO choice is the new external trigger, not a retry of
        # the exhausted discussion event. Idempotent APPLIED choices return above.
        self._queue_event(meeting_id, self._event(
            "CEO_MESSAGE", message["messageId"], message_ref=message["messageId"],
        ) | {"workOnly": True})
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        return self._view(meeting)

    def sync(self, company_id: str, meeting_id: str, *, hydrate: bool = True) -> dict[str, Any]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None or meeting.get("company_id") != company_id:
            raise KeyError(meeting_id)
        returned = set(meeting["result_refs"])
        timeline = list(meeting["timeline"])
        for work_ref in meeting["work_refs"]:
            work = self.foundation.get(work_ref)
            if work["company_id"] != company_id or work["workspace_id"] != meeting["workspace_id"]:
                raise RuntimeScopeError("Meeting Work is outside the current Workspace")
            routing = work["data"].get("responsibilityRouting") or {}
            refs = list(dict.fromkeys([
                *routing.get("resultRefs", []), *routing.get("artifactRefs", []), *routing.get("evidenceRefs", []),
            ]))
            fresh = [ref for ref in refs if ref not in returned]
            if fresh:
                returned.update(fresh)
                timeline.append(self._message(
                    "RESULT_RETURNED", "SYSTEM", "", "工作结果已回到本次会议。",
                    workRef=work_ref, resultRefs=fresh,
                ))
        if returned != set(meeting["result_refs"]):
            fresh_refs = [ref for ref in returned if ref not in set(meeting["result_refs"])]
            meeting = self._save(meeting, result_refs=list(returned), timeline=timeline)
            self._queue_event(
                meeting_id, self._event("RESULT_RETURNED", meeting_id, refs=fresh_refs),
            )
            meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        return self._view(meeting) if hydrate else meeting

    def close(self, company_id: str, meeting_id: str) -> dict[str, Any]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None or meeting.get("company_id") != company_id:
            raise KeyError(meeting_id)
        if meeting["status"] != "closed":
            meeting = self._save(
                meeting, status="closed", closed_at=_now(),
                orchestration=meeting["orchestration"] | {
                    "status": "STOPPED", "activeRunId": "", "runStartedAt": None,
                    "pendingEvents": [], "lastOutcome": "DISCUSSION_SUFFICIENT",
                },
                timeline=[*meeting["timeline"], self._message("SYSTEM", "CEO", "", "会议已结束并进入历史记录。")],
            )
        return self._view(meeting)

    @staticmethod
    def _terms(text: str) -> set[str]:
        lowered = text.lower()
        latin = set(re.findall(r"[a-z0-9]{2,}", lowered))
        chinese = "".join(re.findall(r"[\u4e00-\u9fff]", lowered))
        return latin | {chinese[index:index + 2] for index in range(max(0, len(chinese) - 1))}

    @staticmethod
    def _json_output(value: str) -> dict[str, Any]:
        text = value.strip()
        if text.startswith("```"):
            text = re.sub(r"^```(?:json)?\s*|\s*```$", "", text, flags=re.IGNORECASE)
        try:
            parsed = json.loads(text)
        except (TypeError, json.JSONDecodeError) as error:
            raise ValueError("Employee response did not satisfy the Meeting Result contract") from error
        if not isinstance(parsed, dict):
            raise ValueError("Employee response did not satisfy the Meeting Result contract")
        return parsed

    def _event_text(self, meeting: dict[str, Any], event: dict[str, Any]) -> str:
        message_ref = str(event.get("messageRef") or "")
        message = next((item for item in reversed(meeting["timeline"]) if item.get("messageId") == message_ref), None)
        if message:
            return str(message.get("text") or "")
        if event.get("kind") == "RESULT_RETURNED":
            return "新的工作结果已经返回，需要判断是否足以结束讨论或产生新的问题。"
        return f"会议议题：{meeting['title']}。{meeting.get('background') or ''}"

    def _candidate_evaluation(
        self, meeting: dict[str, Any], event: dict[str, Any], assignments: dict[str, dict[str, Any]],
    ) -> list[dict[str, Any]]:
        text = self._event_text(meeting, event)
        if event.get("kind") == "CEO_MESSAGE" and text.strip().lower() in {"好的", "收到", "确认", "谢谢", "ok", "okay"}:
            return []
        event_terms = self._terms(f"{meeting['title']} {meeting.get('background') or ''} {text}")
        participants = {item["id"]: item for item in self._participants(
            meeting["company_id"], meeting["participants"], meeting["leader_employee_id"],
        )}
        owner_refs = set()
        for ref in [*(event.get("refs") or []), *(item["ref"] for item in meeting.get("context_refs") or [])]:
            try:
                entity = self.foundation.get(ref)
            except KeyError:
                continue
            if entity["company_id"] == meeting["company_id"] and entity["workspace_id"] == meeting["workspace_id"]:
                owner_refs.add(str(entity.get("owner_ref") or ""))
        candidates = []
        requested = str(event.get("requestedSpeakerRef") or "")
        previous = str((meeting.get("orchestration") or {}).get("lastVisibleSpeakerRef") or "")
        for company_ref in meeting["participants"]:
            assignment = assignments[company_ref]
            person = participants[company_ref]
            score, reasons = 0, []
            if requested == company_ref:
                score += 100
                reasons.append("CEO或推进负责人明确点名")
            if assignment["runtimeEmployeeRef"] in owner_refs or company_ref in owner_refs:
                score += 40
                reasons.append("持有本轮新增事实或结果")
            relevant = self._terms(
                f"{person.get('role') or ''} {assignment.get('responsibility') or ''} "
                f"{assignment.get('responsibilityKey') or ''}"
            ) & event_terms
            if relevant:
                score += min(30, 8 + len(relevant) * 3)
                reasons.append("岗位或责任与当前议题相关")
            if company_ref == meeting["leader_employee_id"]:
                score += 5
                reasons.append("负责推进并可补足当前讨论")
            if company_ref == previous and not requested:
                score -= 20
                reasons.append("上一轮已发言，降低连续发言优先级")
            candidates.append({
                "employeeRef": company_ref,
                "runtimeEmployeeRef": assignment["runtimeEmployeeRef"],
                "assignmentRef": assignment["assignmentRef"],
                "score": score,
                "reasons": reasons or ["当前没有可证明的新增相关性"],
                "selected": False,
            })
        return sorted(candidates, key=lambda item: (-item["score"], item["employeeRef"]))

    def _bounded_context(
        self, meeting: dict[str, Any], event: dict[str, Any], speaker_ref: str,
        assignment: dict[str, Any], *, leader: bool = False,
    ) -> dict[str, Any]:
        refs = list(dict.fromkeys([
            *(item["ref"] for item in meeting.get("context_refs") or []),
            *(event.get("refs") or []),
            *meeting.get("result_refs", []),
        ]))[:12]
        knowledge = []
        for item in meeting.get("context_refs") or []:
            if item.get("type") != "KNOWLEDGE" or len(knowledge) >= 3:
                continue
            entry = self.knowledge.get_entry(item["ref"])
            if entry.get("company_id") not in {None, "", meeting["company_id"]}:
                raise RuntimeScopeError("Meeting Knowledge is outside the current Company")
            knowledge.append({
                "ref": entry["id"], "title": entry["title"],
                "summary": str(entry.get("summary") or "")[:600],
                "bodyExcerpt": str(entry.get("body") or "")[:1200],
            })
        decision = None
        if meeting.get("decision_ref"):
            current = self.foundation.get(meeting["decision_ref"])
            decision = {"ref": current["entity_id"], "status": current["lifecycle_status"]}
            if leader and event.get("kind") == "RESULT_RETURNED":
                decision.update({key: str(current["data"].get(key) or "")[:800]
                                 for key in ("event", "choice", "choiceReason", "continuationPlan")})
        post_result = {}
        if leader and event.get("kind") == "RESULT_RETURNED":
            returned = []
            for ref in list(dict.fromkeys([*(event.get("refs") or []), *meeting.get("result_refs", [])[-6:]]))[:6]:
                if ref not in meeting.get("result_refs", []):
                    raise RuntimeScopeError("返回结果不属于本次会议")
                try:
                    item = self.shared.result(meeting["company_id"], meeting["workspace_id"], ref)
                except RuntimeScopeError:
                    returned.append({"ref": ref, "kind": "UNKNOWN", "status": "UNVERIFIED",
                                     "excerpt": "该引用当前无法验证或读取，不作为已核实证据。"})
                    continue
                content = item.get("content") or item.get("summary") or ""
                if isinstance(content, str):
                    try:
                        parsed = json.loads(content)
                        if isinstance(parsed, dict):
                            content = parsed.get("summary") or content
                    except ValueError:
                        pass
                returned.append({"ref": ref, "kind": item.get("kind"), "status": item.get("status"),
                                 "excerpt": str(content)[:1400]})
            post_result = {"returnedResults": returned}
        return {
            **post_result,
            "meeting": {
                "id": meeting["meeting_id"], "topic": meeting["title"],
                "background": str(meeting.get("background") or "")[:1600],
                "companyRef": meeting["company_id"], "businessRef": meeting["business_id"],
                "workspaceRef": meeting["workspace_id"],
            },
            "speaker": {
                "employeeRef": speaker_ref,
                "responsibility": str(assignment.get("responsibility") or "")[:1000],
                "responsibilityKey": assignment.get("responsibilityKey"),
                "isLeaderEvaluation": leader,
            },
            "trigger": {"kind": event.get("kind"), "text": self._event_text(meeting, event)[:2000]},
            "recentConversation": [
                {key: item.get(key) for key in ("messageId", "actorType", "actorRef", "text", "kind")}
                for item in meeting["timeline"][-10:]
            ],
            "proposal": (meeting.get("orchestration") or {}).get("proposal"),
            "selectedKnowledge": knowledge,
            "selectedRefs": refs,
            "decision": decision,
            "currentWork": [
                {"ref": ref, "status": self.foundation.get(ref)["lifecycle_status"],
                 **({"responsibility": self.foundation.get(ref)["data"].get("responsibilityRouting", {}).get("currentResponsibilityKey"),
                     "executionStatus": self.foundation.get(ref)["data"].get("responsibilityRouting", {}).get("status")}
                    if post_result else {})}
                for ref in meeting.get("work_refs", [])[-3:]
            ],
        }

    def _create_execution_work(
        self, meeting: dict[str, Any], assignment: dict[str, Any], *, event_id: str, purpose: str,
        context_refs: list[str],
    ) -> dict[str, Any]:
        release_key = f"meeting:{meeting['meeting_id']}:{event_id}:{purpose}:{assignment['runtimeEmployeeRef']}"
        # A captured execution keeps its original context when later evidence is
        # added to the Meeting. Do not recreate its immutable Cycle contract.
        with self.db.connect() as connection:
            cycles = connection.execute(
                "select entity_id from runtime_entities where tenant_id=? and company_id=? "
                "and workspace_id=? and entity_type='CYCLE' and json_extract(data_json,'$.releaseKey')=?",
                (self.tenant_id, meeting["company_id"], meeting["workspace_id"], release_key),
            ).fetchall()
        if len(cycles) > 1:
            raise ValueError("Meeting release identity is ambiguous")
        if cycles:
            works = self.child_work.list_cycle_work(cycles[0]["entity_id"])
            initial = [work for work in works if work["data"].get("releaseKey") == "initial"]
            if len(initial) != 1 or initial[0]["data"].get("responsibilityAssignmentRef") != assignment["assignmentRef"]:
                raise ValueError("Meeting release Work/Assignment provenance mismatch")
            captured = (initial[0]["data"].get("responsibilityRouting") or {}).get("executions", {}).get(release_key)
            if captured and captured.get("taskRef"):
                return initial[0]
        contract = {
            "problem": f"参与会议《{meeting['title']}》并完成{purpose}",
            "expectedResult": "返回符合 Meeting Result Contract 的可验证结果",
            "constraints": ["仅使用当前会议合法范围", "不得替CEO作经营决定", "不得编造Evidence"],
            "references": context_refs,
        }
        created = self.child_work.create_cycle_work(
            company_id=meeting["company_id"], workspace_id=meeting["workspace_id"],
            assignment_ref=assignment["assignmentRef"], release_key=release_key,
            contract=contract, input_refs=context_refs,
        )
        work = self.routing.start_work(
            created["work"]["entity_id"], scope_type="WORKSPACE", scope_ref=meeting["workspace_id"],
            workflow_key=meeting["orchestration"]["workflowKey"],
            initial_responsibility=assignment["responsibilityKey"],
        )
        if work["lifecycle_status"] == "PLANNED":
            self.child_work.transition_work(work["entity_id"], "READY", actor="SYSTEM", reason="会议轮次责任已确认")
            self.child_work.transition_work(work["entity_id"], "ACTIVE", actor="SYSTEM", reason="会议员工开始处理")
        return self.foundation.get(work["entity_id"])

    def _usage_for_task(self, task_ref: str) -> dict[str, Any]:
        with self.db.connect() as connection:
            rows = connection.execute(
                "select total_tokens, cost_amount, metering_status from ai_usage_records "
                "where tenant_id=? and task_id=? order by occurred_at, usage_record_id",
                (self.tenant_id, task_ref),
            ).fetchall()
        tokens = sum(int(row["total_tokens"] or 0) for row in rows if row["metering_status"] == "confirmed")
        cost = Decimal("0")
        unknown = not rows
        for row in rows:
            if row["metering_status"] != "confirmed":
                unknown = True
            if row["cost_amount"] is None:
                unknown = True
                continue
            try:
                cost += Decimal(str(row["cost_amount"]))
            except InvalidOperation:
                unknown = True
        usage = {"confirmedTokens": tokens, "confirmedCost": str(cost), "unknownMetering": unknown}
        task = ResultStore(self.db).get_task(task_ref)
        parts = str(task.get("execution_ref") or "").split(":")
        if len(parts) >= 3 and parts[0] in {"meeting", "meeting-work"}:
            # Re-project the one ledger, including pre-upgrade completed Tasks.
            # Persistence or repeated hydration must never add the same cost twice.
            prefixes = (f"meeting:{parts[1]}:", f"meeting-work:{parts[1]}:")
            with self.db.connect() as connection:
                all_rows = connection.execute(
                    "select t.task_id, u.usage_record_id, u.total_tokens, u.cost_amount, u.metering_status "
                    "from tasks t left join ai_usage_records u on u.tenant_id=t.tenant_id and u.task_id=t.task_id "
                    "where t.tenant_id=? and t.company_id=? and t.workspace_id=? "
                    "and t.status not in ('INIT','PENDING') "
                    "and (substr(t.execution_ref,1,?)=? or substr(t.execution_ref,1,?)=?)",
                    (self.tenant_id, task["company_id"], task["workspace_id"],
                     len(prefixes[0]), prefixes[0], len(prefixes[1]), prefixes[1]),
                ).fetchall()
            total = Decimal("0")
            unconfirmed = not all_rows
            for row in all_rows:
                if row["metering_status"] != "confirmed" or row["cost_amount"] is None:
                    unconfirmed = True
                if row["cost_amount"] is not None:
                    try:
                        total += Decimal(str(row["cost_amount"]))
                    except InvalidOperation:
                        unconfirmed = True
            usage["ledgerSnapshot"] = {
                "providerCallCount": len(all_rows),
                "usage": {
                    "confirmedTokens": sum(int(row["total_tokens"] or 0) for row in all_rows
                                           if row["metering_status"] == "confirmed"),
                    "confirmedCost": str(total), "unknownMetering": unconfirmed,
                },
            }
            usage["ledgerRows"] = [dict(row) for row in all_rows]
        return usage

    def _reuse_completed_execution(
        self, meeting: dict[str, Any], assignment: dict[str, Any], work: dict[str, Any],
        execution_key: str, expected_type: str,
    ) -> dict[str, Any] | None:
        """Read historical completion; never claim, route, execute or re-finalize it."""
        for key, expected in (("tenant_id", self.tenant_id), ("company_id", meeting["company_id"]),
                              ("workspace_id", meeting["workspace_id"])):
            if work.get(key) != expected:
                raise RuntimeScopeError("Completed execution scope mismatch")
        work = self.foundation.get(work["entity_id"])
        record = (work["data"].get("responsibilityRouting") or {}).get("executions", {}).get(execution_key)
        if not record:
            return None
        if record.get("status") != "ACCEPTED":
            if record.get("status") in {"FAILED", "CANCELLED", "REJECTED", "PARTIAL"}:
                raise ValueError("Execution did not complete successfully; explicit recovery is required")
            return None
        cycle = self.foundation.get(work["parent_id"])
        parts = execution_key.split(":")
        purposes = {"self-judgment": "meeting-self-judgment", "speaker": "meeting-contribution",
                    "leader-evaluation": "meeting-leader-evaluation"}
        if (
            len(parts) != 5 or parts[0] != "meeting" or parts[1] != meeting["meeting_id"]
            or not parts[2].startswith("meeting-event-")
            or purposes.get(parts[3]) != expected_type
            or parts[4] != assignment["runtimeEmployeeRef"]
            or cycle["data"].get("releaseKey") != execution_key
            or record.get("executionKey") != execution_key
            or record.get("assignmentRef") != assignment["assignmentRef"]
            or record.get("employeeRef") != assignment["runtimeEmployeeRef"]
            or record.get("resultType") != expected_type
        ):
            raise ValueError("Completed execution identity/purpose/release provenance mismatch")
        store = ResultStore(self.db)
        task = store.get_task(str(record.get("taskRef") or ""))
        if (
            task["status"] != "COMPLETED" or task.get("company_id") != meeting["company_id"]
            or task.get("workspace_id") != meeting["workspace_id"]
            or task.get("work_ref") != work["entity_id"] or task.get("execution_ref") != execution_key
            or record.get("resultRef") != f"task:{task['task_id']}"
        ):
            raise ValueError("Completed Task/Result provenance mismatch")
        callback = self.identities.verify_task_callback(
            company_id=meeting["company_id"], workspace_id=meeting["workspace_id"],
            runtime_employee_ref=assignment["runtimeEmployeeRef"], task_ref=task["task_id"],
            session_ref=record.get("sessionRef") or "",
        )
        if callback != record.get("provenance"):
            raise ValueError("Completed callback evidence mismatch")
        artifacts = store.list_artifacts(task_id=task["task_id"])
        if not artifacts or {a["artifact_id"] for a in artifacts} != set(record.get("artifactRefs") or []):
            raise ValueError("Completed Artifact references are missing or mismatched")
        if any(hashlib.sha256(a["content"].encode()).hexdigest() != a["content_sha256"] for a in artifacts):
            raise ValueError("Completed Artifact integrity mismatch")
        if not any(a["source_ref"] == "task.output" and a["content"] == task.get("output") for a in artifacts):
            raise ValueError("Completed Result does not match its output Artifact")
        parsed = self._json_output(str(task.get("output") or ""))
        if parsed.get("status") != "ACCEPTED" or parsed.get("resultType") != expected_type:
            raise ValueError("Completed Result contract mismatch")
        usage = self._usage_for_task(task["task_id"])
        with self.db.connect() as connection:
            rows = connection.execute(
                "select company_id,workspace_id,work_ref,execution_ref,employee_id from ai_usage_records "
                "where tenant_id=? and task_id=?", (self.tenant_id, task["task_id"]),
            ).fetchall()
            if not rows:
                raise ValueError("Completed execution has no Usage evidence")
            if any(row["company_id"] != meeting["company_id"] or row["workspace_id"] != meeting["workspace_id"]
                   or row["work_ref"] != work["entity_id"] or row["execution_ref"] != execution_key
                   or row["employee_id"] != task["employee_id"] for row in rows):
                raise RuntimeScopeError("Completed Usage ownership mismatch")
        return {
            "accepted": True, "parsed": parsed, "taskRef": task["task_id"], "workRef": work["entity_id"],
            "artifactRefs": record["artifactRefs"], "evidenceRefs": record.get("evidenceRefs") or [],
            "usage": usage, "callback": callback,
        }

    async def _run_employee(
        self, meeting: dict[str, Any], assignment: dict[str, Any], *, event: dict[str, Any],
        purpose: str, prompt: str, expected_type: str,
    ) -> dict[str, Any]:
        if self.employee_execution is None:
            raise ValueError("Employee execution bridge is unavailable")
        context_refs = list(dict.fromkeys([
            *(item["ref"] for item in meeting.get("context_refs") or []),
            *(event.get("refs") or []),
            *meeting.get("result_refs", []),
        ]))[:16]
        work = self._create_execution_work(
            meeting, assignment, event_id=event["eventId"], purpose=purpose, context_refs=context_refs,
        )
        execution_key = f"meeting:{meeting['meeting_id']}:{event['eventId']}:{purpose}:{assignment['runtimeEmployeeRef']}"
        return await self._execute_on_work(
            meeting, assignment, work=work, execution_key=execution_key,
            prompt=prompt, expected_type=expected_type,
        )

    async def _execute_on_work(
        self, meeting: dict[str, Any], assignment: dict[str, Any], *, work: dict[str, Any],
        execution_key: str, prompt: str, expected_type: str,
    ) -> dict[str, Any]:
        completed = self._reuse_completed_execution(meeting, assignment, work, execution_key, expected_type)
        if completed is not None:
            return completed
        claimed = self.routing.begin_employee_execution(
            work["entity_id"], execution_key=execution_key, assignment_ref=assignment["assignmentRef"],
        )
        record = claimed["execution"]
        task_ref = str(record.get("taskRef") or "")
        if not task_ref:
            submitted = await self.employee_execution({
                "execution_ref": "team_employee:auto", "mode": "submit",
                "company_id": meeting["company_id"], "workspace_id": meeting["workspace_id"],
                "work_ref": work["entity_id"], "execution_key": execution_key,
                "runtime_employee_ref": assignment["runtimeEmployeeRef"],
                "assignment": assignment | {"employeeRef": assignment["runtimeEmployeeRef"]},
                "prompt": prompt,
            })
            task_ref = str(submitted.get("task_ref") or "")
            if not task_ref:
                raise ValueError("Employee execution did not create a Provider Task")
            self.routing.attach_provider_task(work["entity_id"], execution_key=execution_key, task_ref=task_ref)
        raw = await self.employee_execution({
            "execution_ref": "team_employee:auto", "mode": "run",
            "company_id": meeting["company_id"], "workspace_id": meeting["workspace_id"],
            "work_ref": work["entity_id"], "execution_key": execution_key,
            "runtime_employee_ref": assignment["runtimeEmployeeRef"], "task_ref": task_ref,
        })
        callback = (raw.get("execution_binding") or {}).get("callbackProvenance") or {}
        try:
            parsed = self._json_output(str(raw.get("output") or ""))
        except ValueError:
            # Invalid model output is still a completed, billable provider attempt.
            # Finish the canonical execution as failed so its executor and usage
            # cannot be lost merely because the Meeting result is not valid JSON.
            parsed = {"status": "REJECTED", "resultType": expected_type}
        accepted = (
            str(raw.get("task_status") or "").upper() == "COMPLETED"
            and callback.get("verification_status") == "VERIFIED"
            and str(parsed.get("status") or "").upper() == "ACCEPTED"
            and str(parsed.get("resultType") or "") == expected_type
        )
        artifacts = [str(item) for item in raw.get("artifact_refs") or []]
        evidence = [str(callback["evidence_event_ref"])] if callback.get("evidence_event_ref") else []
        self.routing.finish_employee_execution(
            work["entity_id"], execution_key=execution_key, status="ACCEPTED" if accepted else "FAILED",
            task_ref=task_ref, session_ref=str(raw.get("session_ref") or ""),
            result_ref=f"task:{task_ref}", artifact_refs=artifacts, evidence_refs=evidence,
            result_summary=str(parsed.get("summary") or parsed.get("response") or "")[:2000],
            result_type=str(parsed.get("resultType") or ""), provenance=callback,
            context_metrics={"copiedConversationHistory": False, "providerTaskCount": 1, "providerSessionCount": 1},
        )
        if accepted:
            self.routing.route(
                work["entity_id"], signal="COMPLETED", result_refs=[f"task:{task_ref}"],
                artifact_refs=artifacts, evidence_refs=evidence,
            )
        return {
            "accepted": accepted, "parsed": parsed, "taskRef": task_ref,
            "workRef": work["entity_id"], "artifactRefs": artifacts, "evidenceRefs": evidence,
            "usage": self._usage_for_task(task_ref), "callback": callback,
        }

    def _assignment_for_work(self, work: dict[str, Any]) -> dict[str, Any]:
        route = work["data"].get("responsibilityRouting") or {}
        workflow = self.foundation.get(str(route.get("workflowRef") or ""))
        assignment = next((
            item for item in workflow["data"].get("assignments") or []
            if item.get("assignmentRef") == route.get("currentAssignmentRef")
        ), None)
        if assignment is None:
            raise ValueError("Work has no current Employee Responsibility")
        identity = self.identities.resolve(
            company_id=work["company_id"], workspace_id=work["workspace_id"],
            runtime_employee_ref=assignment["employeeRef"],
        )
        return assignment | {
            "runtimeEmployeeRef": assignment["employeeRef"],
            "companyEmployeeRef": identity["company_employee_ref"],
        }

    async def _execute_linked_work(self, meeting: dict[str, Any], work: dict[str, Any]) -> dict[str, Any]:
        assignment = self._assignment_for_work(work)
        route = work["data"].get("responsibilityRouting") or {}
        contract = self.foundation.get(work["parent_id"])["data"].get("contract") or {}
        expected_type = str((assignment.get("outputContract") or {}).get("resultType") or "general-business-result")
        prompt = (
            f"工作目标：{contract.get('problem') or '完成会议决定形成的工作'}\n"
            f"预期结果：{contract.get('expectedResult') or ''}\n"
            f"约束：{json.dumps(contract.get('constraints') or [], ensure_ascii=False)}\n"
            f"当前责任：{assignment.get('responsibility') or ''}\n"
            f"输出结果类型：{expected_type}\n"
            "只返回一个JSON对象："
            '{"status":"ACCEPTED|REJECTED","resultType":"...","summary":"...","problem":"..."}。'
        )
        number = 1 + len(route.get("executions") or {})
        return await self._execute_on_work(
            meeting, assignment, work=work,
            execution_key=f"meeting-work:{meeting['meeting_id']}:{work['entity_id']}:{number}",
            prompt=prompt, expected_type=expected_type,
        )

    def _claim_advance(self, meeting_id: str) -> str | None:
        run_id = f"meeting-run-{uuid4()}"
        claimed = False
        task_refs = self._meeting_task_refs(meeting_id)
        ledger_usage = self._usage_for_task(task_refs[-1]) if task_refs else None

        def mutate(state: dict[str, Any]) -> dict[str, Any]:
            nonlocal claimed
            self._import_cycle_history(meeting_id, state)
            if state.get("activeRunId"):
                try:
                    started = datetime.fromisoformat(str(state.get("runStartedAt") or ""))
                    stale = (datetime.now(timezone.utc) - started).total_seconds() > int(
                        (state.get("limits") or self.LIMITS)["maxElapsedSeconds"]
                    )
                except (TypeError, ValueError):
                    stale = True
                if stale:
                    state.update({
                        "activeRunId": "", "runStartedAt": None, "status": "BLOCKED",
                        "blockedReason": "上次自动推进已中断，无法证明外部员工仍在执行；请重新推进。",
                    })
                return state
            if ledger_usage:
                self._merge_usage(state, ledger_usage)
            if state.get("status") in {"WAITING_CEO", "STOPPED"}:
                return state
            if not state.get("pendingEvents") and state.get("status") != "WAITING_WORK":
                return state
            cycle = state.get("currentCycle")
            if cycle and self._budget_reason(state):
                cycle["exhausted"] = True
            pending = state.get("pendingEvents") or []
            fresh = next((event for event in pending if not event.get("budgetCycleId")
                          and event.get("kind") in {"MEETING_STARTED", "CEO_MESSAGE", "RESULT_RETURNED"}), None)
            if cycle and not cycle.get("endedAt") and not cycle.get("exhausted"):
                # An interrupted attempt resumes the same stable cycle.
                pass
            elif fresh:
                if cycle:
                    state["cycleHistory"] = [*state.get("cycleHistory", []),
                        {key: value for key, value in cycle.items() if key != "excludedTaskRefs"}]
                cycle_id = f"meeting-budget-{fresh['eventId']}"
                fresh["budgetCycleId"] = cycle_id
                state["currentCycle"] = {
                    "cycleId": cycle_id, "triggerEventId": fresh["eventId"], "startedAt": _now(),
                    "endedAt": None, "exhausted": False, "providerCallCount": 0,
                    "usage": {"confirmedTokens": 0, "confirmedCost": "0", "unknownMetering": False},
                    "turnCount": 0, "eventIds": [], "excludedTaskRefs": self._meeting_task_refs(meeting_id),
                }
                state.update(noProgressCount=0, consecutiveVisibleTurns=0, lastVisibleSpeakerRef="")
            else:
                if cycle and cycle.get("exhausted"):
                    state.update(status="BLOCKED", blockedReason=self._budget_reason(state))
                return state
            state.update({"activeRunId": run_id, "runStartedAt": _now(), "status": "RUNNING", "blockedReason": ""})
            claimed = True
            return state

        self._update_orchestration(meeting_id, mutate)
        return run_id if claimed else None

    @staticmethod
    def _compact_context(context: dict[str, Any], *, judgment: bool = False) -> dict[str, Any]:
        """Bound evaluation input; full selected evidence stays on the contribution path."""
        limit = 180 if judgment else 500
        proposal = context.get("proposal") or {}
        return {
            **({"returnedResults": context["returnedResults"],
                "employeeJudgments": context.get("employeeJudgments", [])}
               if not judgment and "returnedResults" in context else {}),
            "meeting": {"topic": str(context["meeting"].get("topic") or "")[:300],
                        "background": str(context["meeting"].get("background") or "")[:limit]},
            "speaker": {**context["speaker"], "responsibility":
                        str(context["speaker"].get("responsibility") or "")[:(300 if judgment else 600)]},
            "trigger": {"kind": context["trigger"].get("kind"),
                        "text": str(context["trigger"].get("text") or "")[:limit]},
            "recentConversation": [
                {"actorRef": item.get("actorRef"), "kind": item.get("kind"),
                 "text": str(item.get("text") or "")[:limit]}
                for item in context.get("recentConversation", [])[-(3 if judgment else 4):]
            ],
            "selectedKnowledge": [
                {"ref": item["ref"], "title": str(item.get("title") or "")[:120],
                 "summary": str(item.get("summary") or item.get("bodyExcerpt") or "")[:limit]}
                for item in context.get("selectedKnowledge", [])[:3]
            ],
            "selectedRefs": context.get("selectedRefs", [])[:12],
            "proposal": {key: str(proposal.get(key) or "")[:limit]
                         for key in ("summary", "rationale")} if proposal else None,
            "decision": context.get("decision"),
            "currentWork": context.get("currentWork", [])[-3:],
        }

    @staticmethod
    def _speaker_prompt(context: dict[str, Any]) -> str:
        return (
            "你是Curis公司中的真实AI员工，正在参加一次经营会议。只基于提供的合法上下文发言。"
            "必须带来新事实、专业判断、风险、反对意见、Evidence请求/引用、方案修改或明确问题；"
            "不要总结前文、客套或只说同意。无法判断时明确缺什么。\n"
            f"会议上下文：{json.dumps(context, ensure_ascii=False, separators=(',', ':'))}\n"
            "只返回一个JSON对象："
            '{"status":"ACCEPTED","resultType":"meeting-contribution","summary":"一句摘要",'
            '"response":"面向CEO和同事的中文发言","newFacts":["..."],"risk":"",'
            '"evidenceRefs":["仅可使用selectedRefs中的ref"],"proposalChange":"",'
            '"needsMoreEvidence":false,"missingFact":""}。'
        )

    @staticmethod
    def _leader_prompt(context: dict[str, Any], contribution: dict[str, Any]) -> str:
        context = MeetingService._compact_context(context)
        contribution = {key: contribution.get(key) for key in (
            "summary", "response", "newFacts", "risk", "evidenceRefs", "proposalChange",
            "needsMoreEvidence", "missingFact",
        )}
        for key in ("summary", "response", "risk", "proposalChange", "missingFact"):
            contribution[key] = str(contribution.get(key) or "")[:1200]
        contribution["newFacts"] = [str(item)[:300] for item in contribution.get("newFacts") or []][:5]
        contribution["evidenceRefs"] = list(contribution.get("evidenceRefs") or [])[:12]
        # The latest contribution is supplied separately, not copied twice.
        if context["recentConversation"] and contribution["response"].startswith(
            context["recentConversation"][-1]["text"]
        ):
            context["recentConversation"] = context["recentConversation"][:-1]
        return (
            "你是本次会议的推进负责人。评估最新员工贡献是否增加新信息，并只选择一个有限结果。"
            "若触发事件是RESULT_RETURNED，即使员工全部沉默，也须评估returnedResults与CEO所选目标是否一致；"
            "沉默不是完成证据。依据返回结果选择现有合法后续状态，内容不足则明确缺口，不强求结束。"
            "不要替CEO作决定，不要发明工作流，不要编造影响、风险、成本或Evidence。\n"
            f"会议上下文：{json.dumps(context, ensure_ascii=False, separators=(',', ':'))}\n"
            f"最新贡献：{json.dumps(contribution, ensure_ascii=False, separators=(',', ':'))}\n"
            "只返回一个JSON对象："
            '{"status":"ACCEPTED","resultType":"meeting-leader-evaluation",'
            '"outcome":"CONTINUE_DISCUSSION|REQUEST_SPECIFIC_EMPLOYEE|REQUEST_EVIDENCE|UPDATE_PROPOSAL|WAIT_FOR_WORK|NEEDS_CEO_DECISION|DISCUSSION_SUFFICIENT|BLOCKED|UNKNOWN",'
            '"summary":"判断依据","requestedEmployeeRef":"","evidenceRefs":[],'
            '"proposal":{"summary":"","rationale":"","unknowns":[]},'
            '"decisionPacket":null}。若需要CEO决定，decisionPacket只提供判断内容：'
            '{"event":"发生了什么，需要选择什么","cannotDecideReason":"为何不能自行决定",'
            '"ceoChoicePrompt":"请CEO选择的问题","continuationPlan":"选择后仅按所选方案完成的具体内部工作及结果",'
            '"options":[{"label":"方案一","impact":{"value":"员工估计或尚未验证","provenance":"EST或UNK"},'
            '"risk":{"value":"员工估计或尚未验证","provenance":"EST或UNK"},'
            '"cost":{"value":"尚未验证","provenance":"UNK"}},{"label":"方案二"}],'
            '"recommendationIndex":0,"recommendationReason":{"value":"推荐理由","provenance":"EST或UNK"},'
            '"evidenceRefs":[]}。推荐序号从0起，方案2到4个。未知影响/风险/成本可省略，由系统标UNK。'
            '必须填写问题、不能自决原因、CEO选择问题、继续工作和推荐理由；缺事实就REQUEST_EVIDENCE，不编造。'
            '只选已有合法引用；不要生成身份、scope、decisionKey、optionId、权限或其他系统字段。'
        )

    @staticmethod
    def _self_judgment_prompt(context: dict[str, Any], assignment: dict[str, Any]) -> str:
        context = MeetingService._compact_context(context, judgment=True)
        return (
            "你是Curis公司中的真实AI员工，正在参加一次经营会议。在决定本轮由谁发言之前，"
            "请先自行判断「我现在是否应该发言」。\n"
            "判断依据（只使用下面提供的合法上下文，不要编造）："
            "1) 你的岗位与责任；2) 你当前承担的工作与已有结果；3) 本次会议议题、背景与当前触发事件；"
            "4) 已有讨论，包含其他同事已经表达过的观点；5) 当前可引用的 Evidence / Result；"
            "6) 你若发言能带来的潜在贡献。\n"
            "只有当你能带来新事实、专业判断、风险、反对意见、Evidence请求或引用、方案修改或明确问题，"
            "并且不是在总结前文、客套或只说同意时，才 should_speak=true；"
            "否则 should_speak=false，并在 reason 中说明你为什么保持沉默。\n"
            "保持沉默（STAY_SILENT）是与发言同等合法的结果，不要为了发言而发言。\n"
            f"会议上下文：{json.dumps(context, ensure_ascii=False, separators=(',', ':'))}\n"
            "只返回一个JSON对象："
            '{"status":"ACCEPTED","resultType":"meeting-self-judgment","should_speak":true,'
            '"confidence":0.0,"reason":"判断理由，最多60字"}。'
            "不要生成正式发言、方案或会议总结；简短判断即可。"
        )

    async def _employee_self_judgment(
        self, meeting: dict[str, Any], assignment: dict[str, Any],
        event: dict[str, Any], context: dict[str, Any],
    ) -> dict[str, Any]:
        """Run one employee's own Speak/Stay-Silent judgment before candidate ordering.

        STAY_SILENT (``should_speak=False``) is a first-class legal result rather than a
        failure: an employee is allowed to stay silent when they can add nothing new.
        """
        result = await self._run_employee(
            meeting, assignment, event=event, purpose="self-judgment",
            prompt=self._self_judgment_prompt(context, assignment),
            expected_type="meeting-self-judgment",
        )
        parsed = result["parsed"]
        raw_should_speak = parsed.get("should_speak")
        if isinstance(raw_should_speak, str):
            should_speak = raw_should_speak.strip().lower() in {"true", "yes", "1"}
        else:
            should_speak = bool(raw_should_speak)
        try:
            confidence = float(parsed.get("confidence") or 0.0)
        except (TypeError, ValueError):
            confidence = 0.0
        return {
            "should_speak": should_speak,
            "contribution": str(parsed.get("contribution") or ""),
            "confidence": confidence,
            "reason": str(parsed.get("reason") or ""),
            "usage": result["usage"],
            "taskRef": result["taskRef"],
            "workRef": result["workRef"],
            "accepted": result["accepted"],
        }

    def _no_progress_stop(
        self, meeting: dict[str, Any], state: dict[str, Any],
        event: dict[str, Any], pending: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Record one "no new progress" round.

        Returns the terminated view once ``maxNoProgress`` is reached; otherwise persists
        the incremented counter and returns ``None`` to signal "continue the turn loop".
        """
        state["noProgressCount"] = int(state.get("noProgressCount") or 0) + 1
        state["lastProcessedEventId"] = event["eventId"]
        if state["noProgressCount"] >= int(state["limits"]["maxNoProgress"]):
            timeline = [*meeting["timeline"], self._message(
                "SYSTEM", "SYSTEM", "", "讨论暂时没有新的进展，已停止自动讨论。",
            )]
            meeting = self._save(meeting, timeline=timeline)
            return self._view(self._finish_advance(
                meeting, state, status="NO_PROGRESS", outcome="DISCUSSION_SUFFICIENT", pending=pending,
            ))
        state["pendingEvents"] = pending
        self._save(meeting, orchestration=state)
        return None

    @staticmethod
    def _merge_usage(state: dict[str, Any], usage: dict[str, Any]) -> None:
        if "ledgerSnapshot" in usage:
            state.update(usage["ledgerSnapshot"])
            cycle = state.get("currentCycle")
            if cycle and not cycle.get("legacy"):
                excluded = set(cycle.get("excludedTaskRefs") or [])
                rows = [row for row in usage.get("ledgerRows", []) if row["task_id"] not in excluded]
                cycle["providerCallCount"] = len(rows)
                cycle["usage"] = {
                    "confirmedTokens": sum(int(row["total_tokens"] or 0) for row in rows
                                           if row["metering_status"] == "confirmed"),
                    "confirmedCost": str(sum((Decimal(str(row["cost_amount"])) for row in rows
                                              if row["cost_amount"] is not None), Decimal("0"))),
                    "unknownMetering": any(row["metering_status"] != "confirmed" or row["cost_amount"] is None
                                           for row in rows),
                }
            return
        current = dict(state.get("usage") or {})
        current["confirmedTokens"] = int(current.get("confirmedTokens") or 0) + int(usage.get("confirmedTokens") or 0)
        current["confirmedCost"] = str(
            Decimal(str(current.get("confirmedCost") or "0")) + Decimal(str(usage.get("confirmedCost") or "0"))
        )
        current["unknownMetering"] = bool(current.get("unknownMetering") or usage.get("unknownMetering"))
        state["usage"] = current
        state["providerCallCount"] = int(state.get("providerCallCount") or 0) + 1
        if state.get("currentCycle"):
            # Compatibility for existing injected execution adapters without a ledger snapshot.
            MeetingService._merge_usage(state["currentCycle"], usage)

    @staticmethod
    def _budget_reason(state: dict[str, Any]) -> str:
        limits = state.get("limits") or MeetingService.LIMITS
        budget = state.get("currentCycle") or state
        if budget.get("exhausted"):
            return "本轮自主推进已达到安全边界，等待新的合法业务事件。"
        usage = budget.get("usage") or {}
        try:
            started = datetime.fromisoformat(str(budget.get("startedAt") or state.get("runStartedAt") or ""))
            if (datetime.now(timezone.utc) - started).total_seconds() >= int(limits["maxElapsedSeconds"]):
                return "本次自动讨论已达到运行时间上限"
        except (TypeError, ValueError):
            pass
        if int(budget.get("providerCallCount") or 0) >= int(limits["maxProviderCalls"]):
            return "模型调用已达到本次会议安全上限"
        if int(usage.get("confirmedTokens") or 0) >= int(limits["maxConfirmedTokens"]):
            return "已确认Token用量达到本次会议安全上限"
        if Decimal(str(usage.get("confirmedCost") or "0")) >= Decimal(str(limits["maxConfirmedCost"])):
            return "已确认模型成本达到本次会议安全上限"
        if int(budget.get("turnCount") or 0) >= int(limits["maxTurns"]):
            return "本轮自主推进已达到轮次上限。"
        return ""

    def _finish_advance(
        self, meeting: dict[str, Any], state: dict[str, Any], *, status: str,
        outcome: str, reason: str = "", pending: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:
        latest = self.db.get_strategy_meeting(self.tenant_id, meeting["meeting_id"]) or meeting
        desired = list(pending if pending is not None else state.get("pendingEvents") or [])
        desired_ids = {item.get("eventId") for item in desired}
        processed = state.get("lastProcessedEventId")
        for item in (latest.get("orchestration") or {}).get("pendingEvents") or []:
            if item.get("eventId") not in desired_ids and item.get("eventId") != processed:
                desired.append(item)
        state.update({
            "status": status, "lastOutcome": outcome, "blockedReason": reason,
            "activeRunId": "", "runStartedAt": None, "pendingEvents": desired,
        })
        cycle = state.get("currentCycle")
        if cycle:
            if self._budget_reason(state):
                cycle["exhausted"] = True
            if cycle.get("exhausted") or status in {"WAITING_CEO", "WAITING_WORK", "SUFFICIENT", "NO_PROGRESS", "STOPPED"}:
                cycle["endedAt"] = cycle.get("endedAt") or _now()
            cycle["lastOutcome"] = outcome
        return self._save(
            latest, orchestration=state,
            continuation_gap=reason if status == "BLOCKED" else "",
        )

    async def advance(self, company_id: str, meeting_id: str) -> dict[str, Any]:
        meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
        if meeting is None or meeting.get("company_id") != company_id:
            raise KeyError(meeting_id)
        run_id = self._claim_advance(meeting_id)
        if not run_id:
            return self.get(company_id, meeting_id)
        try:
            meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
            state = dict(meeting["orchestration"])
            workflow, assignments = self._team_truth(meeting)
            if workflow["data"]["workflowKey"] != state.get("workflowKey"):
                raise ValueError("Meeting execution workflow changed outside the persisted contract")

            # A canonical Work created by an applied Decision is executed by its existing holder.
            for _ in range(8):
                meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
                decision = self.foundation.get(meeting["decision_ref"]) if meeting.get("decision_ref") else None
                unfinished = []
                if decision and decision["lifecycle_status"] == "WAITING_CEO":
                    return self._view(self._finish_advance(
                        meeting, state, status="WAITING_CEO", outcome="NEEDS_CEO_DECISION",
                    ))
                if decision and decision["lifecycle_status"] == "APPLIED":
                    for ref in meeting.get("work_refs") or []:
                        work = self.foundation.get(ref)
                        route = work["data"].get("responsibilityRouting") or {}
                        if route.get("status") not in {"COMPLETED", "CANCELLED"}:
                            unfinished.append(work)
                if not unfinished:
                    break
                budget = self._budget_reason(state)
                if budget:
                    return self._view(self._finish_advance(
                        meeting, state, status="BLOCKED", outcome="BLOCKED", reason=budget,
                    ))
                work_result = await self._execute_linked_work(meeting, unfinished[0])
                self._merge_usage(state, work_result["usage"])
                if not work_result["accepted"]:
                    return self._view(self._finish_advance(
                        meeting, state, status="BLOCKED", outcome="BLOCKED",
                        reason="会议决定形成的工作执行失败；真实失败已保留。",
                    ))
                meeting = self.sync(company_id, meeting_id, hydrate=False)
                persisted = meeting.get("orchestration") or {}
                state = dict(persisted | state)
                state["pendingEvents"] = list(persisted.get("pendingEvents") or [])
            else:
                return self._view(self._finish_advance(
                    meeting, state, status="WAITING_WORK", outcome="WAIT_FOR_WORK",
                    reason="工作仍在推进，会议等待真实结果。",
                ))

            for _ in range(int(state.get("limits", {}).get("maxTurns") or self.LIMITS["maxTurns"])):
                meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
                persisted = meeting.get("orchestration") or {}
                state = dict(persisted | state)
                state["pendingEvents"] = list(persisted.get("pendingEvents") or [])
                pending = list(state.get("pendingEvents") or [])
                cycle = state.get("currentCycle")
                eligible = next((item for item in pending if not cycle or
                                 item.get("budgetCycleId") == cycle["cycleId"]), None)
                if not eligible:
                    return self._view(self._finish_advance(
                        meeting, state, status="SUFFICIENT", outcome="DISCUSSION_SUFFICIENT",
                    ))
                budget = self._budget_reason(state)
                if budget:
                    return self._view(self._finish_advance(
                        meeting, state, status="BLOCKED", outcome="BLOCKED", reason=budget,
                    ))
                event = eligible
                pending.remove(event)
                if event.get("workOnly"):
                    state["lastProcessedEventId"] = event["eventId"]
                    state["pendingEvents"] = pending
                    self._save(meeting, orchestration=state)
                    continue
                if cycle and event["eventId"] not in cycle["eventIds"]:
                    cycle["eventIds"].append(event["eventId"])
                candidates = self._candidate_evaluation(meeting, event, assignments)
                if not candidates and event.get("kind") != "RESULT_RETURNED":
                    # 琐碎 CEO 消息（好的/收到/…）会让 _candidate_evaluation 直接返回 []：
                    # 此时没有任何人该发言，不要为它浪费员工自我判断调用。
                    stopped = self._no_progress_stop(meeting, state, event, pending)
                    if stopped is not None:
                        return stopped
                    continue

                # ---- 员工自我判断门控（要求 #2/#4/#5/#6）----
                # 由员工自决 SPEAK / STAY_SILENT；_candidate_evaluation 的 score 降级为
                # 「自荐者之间的排序信号」，不再以 score<=0 否决资格（要求 #7）。
                # 终止由 maxTurns / maxNoProgress / 全局 maxProviderCalls 兜底。
                self_judgments: dict[str, dict[str, Any]] = {}
                turn_silences: list[dict[str, Any]] = []
                for candidate in candidates:
                    emp_ref = candidate["employeeRef"]
                    if emp_ref == meeting["leader_employee_id"]:
                        continue  # Leader 是编排者，不自我提名
                    budget = self._budget_reason(state)
                    if budget:
                        # 达到全局预算后安全停止，绝不继续调用（约束 #6）
                        return self._view(self._finish_advance(
                            meeting, state, status="BLOCKED", outcome="BLOCKED", reason=budget, pending=pending,
                        ))
                    emp_assignment = assignments[emp_ref]
                    judgment = await self._employee_self_judgment(
                        meeting, emp_assignment, event,
                        self._bounded_context(meeting, event, emp_ref, emp_assignment),
                    )
                    # 门控调用计入全局 providerCallCount（约束 #2/#3/#4）
                    self._merge_usage(state, judgment["usage"])
                    if not judgment["accepted"]:
                        return self._view(self._finish_advance(
                            meeting, state, status="BLOCKED", outcome="BLOCKED",
                            reason="员工自我判断模型调用或结果合同验证失败。", pending=pending,
                        ))
                    self_judgments[emp_ref] = judgment
                    if not judgment["should_speak"]:
                        # STAY_SILENT 是一等合法结果，不是异常/失败
                        turn_silences.append({
                            "employeeRef": emp_ref, "eventId": event["eventId"],
                            "confidence": judgment["confidence"], "reason": judgment["reason"],
                            "evaluatedAt": _now(),
                        })
                speakers = [
                    candidate for candidate in candidates
                    if self_judgments.get(candidate["employeeRef"], {}).get("should_speak", False)
                ]
                if not speakers and event.get("kind") != "RESULT_RETURNED":
                    # 全体员工都选择保持沉默 → 合法的无进展（要求 #5）
                    stopped = self._no_progress_stop(meeting, state, event, pending)
                    if stopped is not None:
                        return stopped
                    continue
                selected = None
                speaker = None
                if speakers:
                    candidates = speakers

                    selected = candidates[0]
                    if (
                        selected["employeeRef"] == state.get("lastVisibleSpeakerRef")
                        and int(state.get("consecutiveVisibleTurns") or 0) >= int(state["limits"]["maxConsecutiveTurns"])
                        and not event.get("requestedSpeakerRef")
                    ):
                        selected = next((item for item in candidates[1:] if item["score"] > 0), selected)
                    selected["selected"] = True
                    assignment = assignments[selected["employeeRef"]]
                    context = self._bounded_context(meeting, event, selected["employeeRef"], assignment)
                    budget = self._budget_reason(state)
                    if budget:
                        # 门控循环已逐候选复检并将计数推到上限，speaker 调用前再复检一次，
                        # 闭合硬约束 #5（任何情况不绕过全局 budget）与 #6（达上限安全停止）。
                        return self._view(self._finish_advance(
                            meeting, state, status="BLOCKED", outcome="BLOCKED", reason=budget, pending=pending,
                        ))
                    speaker = await self._run_employee(
                        meeting, assignment, event=event, purpose="speaker",
                        prompt=self._speaker_prompt(context), expected_type="meeting-contribution",
                    )
                    self._merge_usage(state, speaker["usage"])
                    if not speaker["accepted"]:
                        state["turns"] = [*state.get("turns", []), {
                            "turnId": f"meeting-turn-{uuid4()}", "event": event,
                            "candidates": candidates, "speakerRef": selected["employeeRef"],
                            "status": "FAILED", "workRefs": [speaker["workRef"]],
                            "taskRefs": [speaker["taskRef"]], "completedAt": _now(),
                        }]
                        return self._view(self._finish_advance(
                            meeting, state, status="BLOCKED", outcome="BLOCKED",
                            reason="员工模型调用或结果合同验证失败。", pending=pending,
                        ))
                    response = str(speaker["parsed"].get("response") or speaker["parsed"].get("summary") or "").strip()
                    digest = hashlib.sha256(re.sub(r"\s+", "", response).encode()).hexdigest()
                    duplicate = not response or digest in set(state.get("contentHashes") or [])
                    recorded = any(message.get("resultRef") == f"task:{speaker['taskRef']}"
                                   for message in meeting["timeline"])
                    if recorded:
                        # Timeline may have persisted before the turn checkpoint.
                        # Reuse its identity, not a new visible contribution.
                        if digest not in state.get("contentHashes", []):
                            state["contentHashes"] = [*state.get("contentHashes", []), digest][-12:]
                            state["noProgressCount"] = 0
                            state["consecutiveVisibleTurns"] = (
                                int(state.get("consecutiveVisibleTurns") or 0) + 1
                                if state.get("lastVisibleSpeakerRef") == selected["employeeRef"] else 1
                            )
                            state["lastVisibleSpeakerRef"] = selected["employeeRef"]
                    elif duplicate:
                        state["noProgressCount"] = int(state.get("noProgressCount") or 0) + 1
                        if state["noProgressCount"] >= int(state["limits"]["maxNoProgress"]):
                            meeting = self._save(meeting, timeline=[*meeting["timeline"], self._message(
                                "SYSTEM", "SYSTEM", "", "讨论暂时没有新的进展，已停止自动讨论。",
                            )])
                            return self._view(self._finish_advance(
                                meeting, state, status="NO_PROGRESS", outcome="DISCUSSION_SUFFICIENT",
                                pending=pending,
                            ))
                    else:
                        message = self._message(
                            "MESSAGE", "EMPLOYEE", selected["employeeRef"], response,
                            resultRef=f"task:{speaker['taskRef']}", artifactRefs=speaker["artifactRefs"],
                        )
                        meeting = self._save(meeting, timeline=[*meeting["timeline"], message])
                        state["contentHashes"] = [*state.get("contentHashes", []), digest][-12:]
                        state["noProgressCount"] = 0
                        state["consecutiveVisibleTurns"] = (
                            int(state.get("consecutiveVisibleTurns") or 0) + 1
                            if state.get("lastVisibleSpeakerRef") == selected["employeeRef"] else 1
                        )
                        state["lastVisibleSpeakerRef"] = selected["employeeRef"]

                leader_assignment = assignments[meeting["leader_employee_id"]]
                leader_context = self._bounded_context(
                    meeting, event, meeting["leader_employee_id"], leader_assignment, leader=True,
                )
                if event.get("kind") == "RESULT_RETURNED":
                    leader_context["employeeJudgments"] = [
                        {"employeeRef": ref, "should_speak": item["should_speak"], "reason": item["reason"][:300]}
                        for ref, item in self_judgments.items()
                    ][:8]
                budget = self._budget_reason(state)
                if budget:
                    # 门控循环与 speaker 调用后再次复检，防止越界 +1（硬约束 #5/#6）。
                    return self._view(self._finish_advance(
                        meeting, state, status="BLOCKED", outcome="BLOCKED", reason=budget, pending=pending,
                    ))
                leader = await self._run_employee(
                    meeting, leader_assignment, event=event, purpose="leader-evaluation",
                    prompt=self._leader_prompt(leader_context, speaker["parsed"] if speaker else {}),
                    expected_type="meeting-leader-evaluation",
                )
                self._merge_usage(state, leader["usage"])
                if not leader["accepted"]:
                    return self._view(self._finish_advance(
                        meeting, state, status="BLOCKED", outcome="BLOCKED",
                        reason="推进负责人无法验证本轮讨论结果。", pending=pending,
                    ))
                outcome = str(leader["parsed"].get("outcome") or "UNKNOWN").upper()
                allowed = {
                    "CONTINUE_DISCUSSION", "REQUEST_SPECIFIC_EMPLOYEE", "REQUEST_EVIDENCE",
                    "UPDATE_PROPOSAL", "WAIT_FOR_WORK", "NEEDS_CEO_DECISION",
                    "DISCUSSION_SUFFICIENT", "BLOCKED", "UNKNOWN",
                }
                if outcome not in allowed:
                    outcome = "UNKNOWN"
                turn = {
                    "turnId": f"meeting-turn-{uuid4()}", "event": event,
                    "candidates": candidates, "speakerRef": selected["employeeRef"] if selected else "",
                    # 评审证据：本轮每位员工的自我判断（should_speak / confidence / reason）
                    "selfJudgments": {ref: item | {"usage": {key: value for key, value in item["usage"].items()
                                                            if key != "ledgerRows"}}
                                      for ref, item in self_judgments.items()},
                    # 评审证据：本轮选择保持沉默的员工及其理由（要求 #5）
                    "silences": turn_silences,
                    "leaderRef": meeting["leader_employee_id"], "leaderOutcome": outcome,
                    "workRefs": ([speaker["workRef"]] if speaker else []) + [leader["workRef"]],
                    "taskRefs": ([speaker["taskRef"]] if speaker else []) + [leader["taskRef"]],
                    "resultRefs": ([f"task:{speaker['taskRef']}"] if speaker else []) + [f"task:{leader['taskRef']}"],
                    "status": "COMPLETED", "completedAt": _now(),
                }
                state["turns"] = [*state.get("turns", []), turn]
                # 沉默记录只在回合 COMPLETED 时落库，保证 Restart 不产生孤儿沉默或重复发言
                state["silences"] = [*state.get("silences", []), *turn_silences]
                state["turnCount"] = int(state.get("turnCount") or 0) + 1
                if cycle:
                    cycle["turnCount"] = int(cycle.get("turnCount") or 0) + 1
                state["lastProcessedEventId"] = event["eventId"]
                state["lastOutcome"] = outcome

                proposal = leader["parsed"].get("proposal")
                if isinstance(proposal, dict) and str(proposal.get("summary") or "").strip():
                    state["proposal"] = {
                        "summary": str(proposal["summary"])[:2000],
                        "rationale": str(proposal.get("rationale") or "")[:2000],
                        "unknowns": [str(item)[:400] for item in list(proposal.get("unknowns") or [])[:8]],
                        "artifactRef": (leader["artifactRefs"] or [""])[0],
                        "ownerRef": meeting["leader_employee_id"],
                        "conversationRefs": [item["messageId"] for item in meeting["timeline"][-10:]],
                        "evidenceRefs": [str(item) for item in leader["parsed"].get("evidenceRefs") or []],
                        "updatedAt": _now(),
                    }
                    meeting = self._save(meeting, timeline=[*meeting["timeline"], self._message(
                        "PROPOSAL", "EMPLOYEE", meeting["leader_employee_id"],
                        f"我已把讨论整理成方案：{state['proposal']['summary']}",
                        artifactRef=state["proposal"]["artifactRef"],
                    )])

                if outcome == "NEEDS_CEO_DECISION":
                    packet = leader["parsed"].get("decisionPacket")
                    if not isinstance(packet, dict):
                        return self._view(self._finish_advance(
                            meeting, state, status="BLOCKED", outcome="BLOCKED",
                            reason="推进负责人提出需要CEO决定，但没有形成合法P7决策包。", pending=pending,
                        ))
                    meeting = self._save(meeting, orchestration=state | {"pendingEvents": pending})
                    if cycle:
                        cycle["endedAt"] = _now()
                        meeting = self._save(meeting, orchestration=state | {"pendingEvents": pending})
                    return self.request_decision(company_id, meeting_id, self._map_leader_decision(meeting, packet))
                if outcome == "REQUEST_EVIDENCE":
                    legal = {item["ref"] for item in meeting.get("context_refs") or []} | set(meeting.get("result_refs") or [])
                    selected_refs = [str(item) for item in leader["parsed"].get("evidenceRefs") or [] if str(item) in legal]
                    if not selected_refs:
                        if cycle:
                            cycle["endedAt"] = _now()
                        return self._view(self._finish_advance(
                            meeting, state, status="BLOCKED", outcome="BLOCKED",
                            reason=str(leader["parsed"].get("summary") or "当前缺少可引用的事实依据。"), pending=pending,
                        ))
                    evidence_message = self._message(
                        "EVIDENCE_REFERENCE", "EMPLOYEE", meeting["leader_employee_id"],
                        "我补充了与当前判断直接相关的资料依据。", evidenceRefs=selected_refs,
                    )
                    meeting = self._save(meeting, timeline=[*meeting["timeline"], evidence_message])
                    pending.append(self._cycle_event(state, "EVIDENCE_ADDED", evidence_message["messageId"], refs=selected_refs))
                elif outcome in {"CONTINUE_DISCUSSION", "REQUEST_SPECIFIC_EMPLOYEE", "UPDATE_PROPOSAL"}:
                    requested = str(leader["parsed"].get("requestedEmployeeRef") or "")
                    if requested and requested not in meeting["participants"]:
                        requested = ""
                    pending.append(self._cycle_event(state,
                        "LEADER_REQUEST", leader["taskRef"], refs=[*(speaker["artifactRefs"] if speaker else []), *leader["artifactRefs"]],
                        requested_speaker_ref=requested,
                    ))
                elif outcome == "WAIT_FOR_WORK":
                    return self._view(self._finish_advance(
                        meeting, state, status="WAITING_WORK", outcome=outcome, pending=pending,
                    ))
                elif outcome == "DISCUSSION_SUFFICIENT":
                    return self._view(self._finish_advance(
                        meeting, state, status="SUFFICIENT", outcome=outcome, pending=pending,
                    ))
                else:
                    if cycle:
                        cycle["endedAt"] = _now()
                    return self._view(self._finish_advance(
                        meeting, state, status="BLOCKED", outcome=outcome,
                        reason=str(leader["parsed"].get("summary") or "推进负责人当前无法继续判断。"), pending=pending,
                    ))
                state["pendingEvents"] = pending
                meeting = self._save(meeting, orchestration=state)

            return self._view(self._finish_advance(
                meeting, state, status="NO_PROGRESS", outcome="DISCUSSION_SUFFICIENT",
                reason="本次自动讨论已达到轮次上限。",
            ))
        except Exception as error:
            meeting = self.db.get_strategy_meeting(self.tenant_id, meeting_id)
            state = dict(meeting.get("orchestration") or {})
            timeline = [*meeting["timeline"], self._message(
                "SYSTEM", "SYSTEM", "", "团队讨论遇到问题，已停止自动推进。",
            )]
            meeting = self._save(meeting, timeline=timeline)
            return self._view(self._finish_advance(
                meeting, state, status="BLOCKED", outcome="BLOCKED", reason=str(error)[:1000],
            ))

    def _view(self, meeting: dict[str, Any], *, sync: bool = False) -> dict[str, Any]:
        if sync:
            meeting = self.sync(meeting["company_id"], meeting["meeting_id"], hydrate=False)
        participants = self._participants(
            meeting["company_id"], meeting["participants"], meeting["leader_employee_id"],
        ) if meeting.get("company_id") and meeting.get("participants") else []
        decision = None
        if meeting.get("decision_ref"):
            decision = self.foundation.get(meeting["decision_ref"])
        works = []
        for ref in meeting.get("work_refs") or []:
            try:
                works.append(self.foundation.get(ref))
            except KeyError:
                continue
        results = []
        if meeting.get("workspace_id"):
            for ref in meeting.get("result_refs") or []:
                try:
                    results.append(self.shared.result(meeting["company_id"], meeting["workspace_id"], ref))
                except RuntimeScopeError:
                    results.append({"reference_id": ref, "kind": "UNKNOWN", "summary": "结果引用仍存在，但当前无法读取详情。"})
        orchestration = meeting.get("orchestration") or {}
        if meeting["status"] == "closed":
            operating_state = "ARCHIVED"
        elif decision and decision["lifecycle_status"] == "WAITING_CEO":
            operating_state = "WAITING_CEO"
        elif any(
            (work["data"].get("responsibilityRouting") or {}).get("status") not in {"COMPLETED", "CANCELLED"}
            for work in works
        ):
            operating_state = "WAITING_RESULT"
        elif orchestration.get("status") in {"WAITING_WORK"}:
            operating_state = "WAITING_RESULT"
        else:
            operating_state = "DISCUSSING"
        return {
            **meeting,
            "participants_detail": participants,
            "leader": next((item for item in participants if item["id"] == meeting.get("leader_employee_id")), None),
            "decision": decision,
            "works": works,
            "results": results,
            "operating_state": operating_state,
            "background_continuation": {
                "status": "AVAILABLE" if self.employee_execution and orchestration.get("workflowKey") else "UNAVAILABLE",
                "state": orchestration.get("status") or "UNKNOWN",
                "reason": meeting.get("continuation_gap") or orchestration.get("blockedReason") or "",
                "usage": orchestration.get("usage") or {},
            },
        }
