"""Reviewed public-source evidence on the original Business research Work."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StringConstraints

from .agent_work_resources import AgentWorkResources
from .conversation_service import ConversationService, digest
from .employee_execution_identity import EmployeeExecutionIdentity
from .resource_scope_policy import ResourceScopePolicy
from .result_attention import ResultAttention
from .runtime import RuntimeFoundation, RuntimeScopeError
from .runtime.child_work import CanonicalChildWorkRuntime, leader_preferred_binding
from .tenant_context import TenantContext


RecommendationText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=500)]


class MarketEvidenceCitation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    evidence_ref: str = Field(min_length=1, max_length=256)
    evidence_version: str = Field(pattern=r"^[0-9a-f]{64}$")


class ChannelRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    suitability: RecommendationText
    hypothesis: RecommendationText


class SevenDayTest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    days: Literal[7]
    steps: list[RecommendationText] = Field(min_length=2, max_length=7)
    metrics: list[RecommendationText] = Field(min_length=2, max_length=6)
    decision_rule: RecommendationText


class ResearchRecommendation(BaseModel):
    model_config = ConfigDict(extra="forbid")
    evidence: list[MarketEvidenceCitation] = Field(min_length=1, max_length=12)
    short_video: ChannelRecommendation
    streaming_preview: ChannelRecommendation
    seven_day_test: SevenDayTest
    preferred_channel: Literal["short_video", "streaming_preview"]
    rationale: RecommendationText
    limitations: RecommendationText


def validate_research_recommendation(output, evidence_inputs):
    if not isinstance(output, dict) or output.get("status") != "ACCEPTED":
        raise ValueError("负责人尚未返回可交付的建议。")
    recommendation = ResearchRecommendation.model_validate(output.get("recommendation"))
    if [item.model_dump() for item in recommendation.evidence] != evidence_inputs:
        raise ValueError("负责人建议未引用本次固定证据版本。")
    if (len(set(recommendation.seven_day_test.steps)) != len(recommendation.seven_day_test.steps)
            or len(set(recommendation.seven_day_test.metrics)) != len(recommendation.seven_day_test.metrics)):
        raise ValueError("一周测试步骤或指标重复。")
    if recommendation.short_video == recommendation.streaming_preview:
        raise ValueError("两种渠道需要分别说明适用性和假设。")
    return recommendation


class MarketMetric(BaseModel):
    model_config = ConfigDict(extra="forbid")
    label: str = Field(min_length=1, max_length=200)
    value: str = Field(min_length=1, max_length=100)
    unit: str = Field(min_length=1, max_length=100)
    period: str = Field(min_length=1, max_length=200)
    population: str = Field(min_length=1, max_length=500)
    source_quote: str = Field(min_length=1, max_length=1000)


class AcceptMarketEvidenceIn(BaseModel):
    model_config = ConfigDict(extra="forbid")
    task_ref: str = Field(min_length=1, max_length=128)
    artifact_ref: str = Field(min_length=1, max_length=128)
    result_version: str = Field(pattern=r"^[0-9a-f]{64}$")
    snapshot_sha256: str = Field(pattern=r"^[0-9a-f]{64}$")
    request_id: str = Field(min_length=1, max_length=128)
    reviewed: StrictBool
    metrics: list[MarketMetric] = Field(min_length=1, max_length=12)
    limitations: str = Field(min_length=1, max_length=2000)



class MusicMarketEvidence:
    def __init__(self, database):
        self.db = database
        self.child = CanonicalChildWorkRuntime(database)
        self.tenant = TenantContext.current_tenant_id()


    def _entity(self, con, ref, kind="WORK"):
        return self.child._entity(self.child._row(con, ref, kind))


    def capture_for_model_task(self, context):
        """One host-owned public capture before this original worker's normal model call."""
        if context.get("type") != "model" or not str(context.get("execution_ref") or "").startswith("leader:worker:"):
            return None
        with self.db.connect() as con:
            work = self._entity(con, context["work_ref"])
            root_ref = work["data"].get("leaderRootWorkRef")
            if not root_ref or not self.applies(con, self._entity(con, root_ref)):
                return None
            configured = (work["data"].get("followupContract") or {}).get("marketEvidenceBrowser") or {}
        from .agent_browser_runtime import agent_browser_release, open_agent_browser_for_work
        from .agent_browser_policy import PublicTargets
        from .agent_tool_server import AgentToolSessions
        from .capability_authorizer import CapabilityAuthorizer
        from .company_execution_policy import agent_work_claim_active
        from .evolution_event_log import EvolutionEventLog
        hosts, source_url = configured.get("hosts") or [], configured.get("sourceUrl")
        PublicTargets(hosts).url(source_url)
        if "#" in source_url:
            raise ValueError("原文 URL 不能含页内片段。")
        release = agent_browser_release()
        identity = {"tenant_id": self.tenant, **{k: str(context.get(k) or "") for k in
            ("company_id", "work_ref", "task_id", "employee_id")}, "binding_ref": str(context.get("binding_id") or "")}
        actor = TenantContext.current_identity()

        def stopped():
            try:
                with TenantContext.scope(tenant_id=self.tenant, company_id=identity["company_id"],
                        ceo_id=actor.get("ceo_id"), role=actor.get("role")):
                    with self.db.connect() as con:
                        child, root, scope = self._lineage(con, identity["work_ref"])
                        task = con.execute("select * from tasks where tenant_id=? and task_id=?",
                            (self.tenant, identity["task_id"])).fetchone()
                        binding = con.execute("select * from employee_capability_bindings where tenant_id=? "
                            "and id=? and employee_id=? and capability_type='model' and enabled=1",
                            (self.tenant, identity["binding_ref"], identity["employee_id"])).fetchone()
                        joined = ConversationService(self.db)._work_database(con)
                        employee = EmployeeExecutionIdentity(joined).resolve(company_id=identity["company_id"],
                            runtime_employee_ref=child["owner_ref"])
                        authorizer = CapabilityAuthorizer(joined)
                        current = (child["data"].get("followupContract") or {}).get("marketEvidenceBrowser") or {}
                        return (agent_browser_release(verify_assets=False) != release or current != configured
                            or not task or task["status"] not in {"RUNNING", "PARSED", "PENDING", "RESUMED"}
                            or task["requested_capability_type"] != "model" or task["employee_id"] != identity["employee_id"]
                            or not binding or binding["capability_id"] != context.get("id")
                            or binding["capability_source"] != context.get("source")
                            or employee["company_employee_ref"] != identity["employee_id"]
                            or not authorizer.authorize(identity["employee_id"], "model", context.get("id", ""), connection=con)[0]
                            or not authorizer.authorize(identity["employee_id"], "tool", "reader", connection=con)[0]
                            or not agent_work_claim_active(con, **{k: identity[k] for k in
                                ("tenant_id", "company_id", "work_ref", "task_id")}, execution_ref=context["execution_ref"]))
            except (ValueError, KeyError, OSError, RuntimeScopeError):
                return True

        if stopped():
            raise RuntimeScopeError("公开取证需要原员工、岗位权限、模型绑定及仍有效的原 Task。")
        events = EvolutionEventLog(self.db)
        with self.db.connect() as con:
            con.execute("begin immediate")
            previous = con.execute("select 1 from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type in ('work.public_source.capture.claimed','work.public_source.captured')",
                (self.tenant, identity["task_id"])).fetchone()
            if previous:
                raise RuntimeScopeError("本 Task 已领取过浏览器采集；保留原回执，不自动重开。")
            events.record_in_connection(con, correlation_id=identity["task_id"], event_type="work.public_source.capture.claimed",
                payload={"identity": identity, "source_url": source_url, "release_sha256": release["releaseSha256"]},
                idempotency_key="public-source-claim:" + self.tenant + ":" + identity["task_id"])
        resources = AgentWorkResources(Path(self.db.path).absolute().parent / "agent-work",
            **{k: identity[k] for k in ("tenant_id", "company_id", "work_ref", "task_id")})
        resources.prepare([])
        browser = open_agent_browser_for_work(identity, stopped, hosts=hosts, source_url=source_url)
        tools = AgentToolSessions()
        token = tools.register(resources, [], stopped, browser=browser, seconds=80)
        try:
            for number, arguments in enumerate(({"action": "navigate", "url": source_url}, {"action": "observe"})):
                response = tools.handle(token, {"jsonrpc": "2.0", "id": number, "method": "tools/call",
                    "params": {"name": "browser", "arguments": arguments}})
                if response["result"]["isError"]:
                    raise RuntimeScopeError("浏览器未返回可核验原文，未启动模型分析。")
            receipts, calls = resources.collect(), tools.browser_evidence(token)
        finally:
            tools.close(token)
        shutdown = browser.shutdown_evidence or {}
        if (stopped() or not shutdown.get("normal_browser_close") or not shutdown.get("proxy_closed")
                or shutdown.get("held_process", {}).get("direct_child") != "EXITED" or len(receipts) != 1):
            raise RuntimeScopeError("浏览器关闭或原 Work 权限未核验，未启动模型分析。")
        calls[-1]["shutdown"] = shutdown
        raw = resources.read_output(receipts[0])
        if len(raw) > 120000:
            raise RuntimeScopeError("原文超出单次材料上限，未启动模型分析。")
        captured = {"identity": identity, "source_url": source_url, "release_sha256": release["releaseSha256"],
            "artifact_receipts": receipts, "browser_tool_calls": calls}
        events.record(correlation_id=identity["task_id"], event_type="work.public_source.captured", payload=captured,
            idempotency_key="public-source:" + self.tenant + ":" + identity["task_id"])
        return {**captured, "source_text": raw.decode("utf-8")}

    def applies(self, con, root):
        """Only Music Business research from the existing conversation confirmation."""
        cycle = self._entity(con, root["parent_id"], "CYCLE")
        origin = (cycle["data"].get("contract") or {}).get("conversationResearchSource")
        if not origin or root["workspace_id"] is not None:
            return False
        scope = self.child._scope(con, root)
        if scope["scope_type"] != "BUSINESS" or scope["business_id"] != origin.get("business_ref"):
            return False
        return con.execute("select 1 from workspace_package_instances p join workspaces w "
            "on w.tenant_id=p.tenant_id and w.workspace_id=p.workspace_id and w.company_id=p.company_id "
            "where w.tenant_id=? and w.company_id=? and w.business_id=? "
            "and p.package_id='com.curis.local.music' limit 1",
            (self.tenant, root["company_id"], scope["business_id"])).fetchone() is not None


    def _lineage(self, con, child_ref):
        work = self._entity(con, child_ref)
        root = self._entity(con, work["data"].get("leaderRootWorkRef"))
        scope = self.child._scope(con, root)
        ResourceScopePolicy.require_same_execution_scope(scope, self.child._scope(con, work))
        if (not self.applies(con, root) or root["lifecycle_status"] != "ACTIVE"
                or root["data"].get("responsibilityRouting", {}).get("status") != "ACTIVE"
                or work["lifecycle_status"] not in {"ACTIVE", "COMPLETED"}
                or child_ref not in root["data"].get("leaderDelegation", {}).get("childWorkRefs", [])
                or work["parent_id"] != root["parent_id"] or work["owner_ref"] == root["owner_ref"]):
            raise RuntimeScopeError("需要原 Music 研究下不同员工的同范围子工作。")
        cycle = self._entity(con, root["parent_id"], "CYCLE")
        origin = cycle["data"]["contract"]["conversationResearchSource"]
        rows = con.execute("select payload from evolution_events where tenant_id=? "
            "and event_type='conversation.research_work.confirmed' and correlation_id=? "
            "and json_extract(payload,'$.work_ref')=?", (self.tenant, origin["conversation_ref"], root["entity_id"])).fetchall()
        if (len(rows) != 1 or json.loads(rows[0]["payload"]) !=
                {**origin, "work_ref": root["entity_id"], "cycle_ref": cycle["entity_id"]}):
            raise RuntimeScopeError("原对话研究确认与 Work 来源不一致。")
        return work, root, scope


    def _proof(self, con, work, scope, task_ref, artifact_ref):
        expected_status = "ACCEPTED"
        records = [r for r in work["data"].get("responsibilityRouting", {}).get("executions", {}).values()
            if str(r.get("executionKey", "")).startswith("leader:worker:")
            and r.get("status") == expected_status and r.get("provenance", {}).get("verification_status") == "VERIFIED"]
        if (len(records) != 1 or records[0].get("status") != expected_status
                or records[0].get("taskRef") != task_ref
                or records[0].get("provenance", {}).get("verification_status") != "VERIFIED"
                or records[0].get("provenance", {}).get("callback_actor_ref") != work["owner_ref"]
                or artifact_ref not in records[0].get("artifactRefs", [])):
            raise RuntimeScopeError("需要原研究员工已核验的 Task 与成果文件。")
        task = con.execute("select * from tasks where tenant_id=? and task_id=?",
            (self.tenant, task_ref)).fetchone()
        joined = ConversationService(self.db)._work_database(con)
        employee = EmployeeExecutionIdentity(joined).resolve(company_id=work["company_id"],
            runtime_employee_ref=work["owner_ref"])["company_employee_ref"]
        if (not task or task["status"] != "COMPLETED" or task["requested_capability_type"] not in {"agent", "model"}
                or task["work_ref"] != work["entity_id"]
                or task["employee_id"] != employee or task["execution_ref"] != records[0]["executionKey"]):
            raise RuntimeScopeError("Task 并非原员工完成的研究结果。")
        ResourceScopePolicy.require_same_execution_scope(scope, self.child._scope(con, dict(task)))
        output = json.loads(task["output"] or "null")
        if (not isinstance(output, dict) or output.get("status") != "ACCEPTED"
                or not isinstance(output.get("summary"), str) or not output["summary"].strip()):
            raise RuntimeScopeError("原员工尚未交付完整分析结果。")
        usage = con.execute("select * "
            "from ai_usage_records where tenant_id=? and task_id=? "
            "and company_id=? and work_ref=? and execution_status='success'",
            (self.tenant, task_ref, work["company_id"], work["entity_id"])).fetchall()
        events = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='usage.task_execution'", (self.tenant, task_ref)).fetchall()
        if len(usage) != 1 or len(events) != 1:
            raise RuntimeScopeError("原 Task 的唯一执行与工具回执无法核验。")
        ResourceScopePolicy.require_same_execution_scope(scope, self.child._scope(con, dict(usage[0])))
        if usage[0]["employee_id"] != employee or usage[0]["execution_ref"] != task["execution_ref"]:
            raise RuntimeScopeError("原用量不属于本员工执行。")
        event = json.loads(events[0]["payload"])
        usage_ref = event.get("usage_record_id")
        if task["requested_capability_type"] == "model":
            model_events = con.execute("select event_id,payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type='usage.model_call'", (self.tenant, task_ref)).fetchall()
            model = json.loads(model_events[0]["payload"]) if len(model_events) == 1 else {}
            if (len(model_events) != 1 or str(model_events[0]["event_id"]) != records[0]["provenance"].get("evidence_event_ref")
                    or model.get("usage_record_id") != usage[0]["usage_record_id"]
                    or usage_ref not in {None, model.get("usage_record_id")}
                    or any(model.get(k) != event.get(k) for k in
                        ("task_id", "company_id", "work_ref", "employee_id", "execution_ref", "status"))
                    or model.get("capability_type") != "model" or model.get("capability_id") != task["requested_capability_id"]
                    or model.get("capability_binding_id") != usage[0]["capability_binding_id"]
                    or model.get("model_name") != usage[0]["model_name"]
                    or model.get("provider_id") != usage[0]["provider_id"] or model.get("outbound_attempted") is not True):
                raise RuntimeScopeError("原模型分析的正常用量与执行回执无法核验。")
            usage_ref = model["usage_record_id"]

        if (usage_ref != usage[0]["usage_record_id"] or event.get("task_id") != task_ref
                or event.get("work_ref") != work["entity_id"] or event.get("company_id") != work["company_id"]
                or event.get("employee_id") != employee or event.get("status") != "success"
                or event.get("execution_ref") != task["execution_ref"]):
            raise RuntimeScopeError("执行回执身份改变。")
        row = con.execute("select * from artifacts where tenant_id=? and task_id=? and artifact_id=? "
            "and artifact_type='agent_file_receipt'", (self.tenant, task_ref, artifact_ref)).fetchone()
        if not row or hashlib.sha256(row["content"].encode()).hexdigest() != row["content_sha256"]:
            raise RuntimeScopeError("原成果文件回执改变。")
        receipt = json.loads(row["content"])
        if (event.get("artifact_receipts") or []).count(receipt) != 1:
            raise RuntimeScopeError("原工具执行没有唯一记录该成果。")
        calls = [c for c in event.get("browser_tool_calls", [])
            if c.get("capture_kind") == "HOST_BROWSER_TEXT_V1" and c.get("snapshot_receipt") == receipt]
        if len(calls) != 1:
            raise RuntimeScopeError("没有宿主浏览器采集回执，不能接受手写网页来源。")
        capture = calls[0]
        if task["requested_capability_type"] == "model":
            captured = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
                "and event_type='work.public_source.captured'", (self.tenant, task_ref)).fetchall()
            source = json.loads(captured[0]["payload"]) if len(captured) == 1 else {}
            expected = {"tenant_id": self.tenant, "company_id": work["company_id"], "work_ref": work["entity_id"],
                "task_id": task_ref, "employee_id": employee, "binding_ref": usage[0]["capability_binding_id"]}
            configured = (work["data"].get("followupContract") or {}).get("marketEvidenceBrowser") or {}
            if (source.get("identity") != expected or source.get("artifact_receipts") != [receipt]
                    or source.get("browser_tool_calls") != event.get("browser_tool_calls")
                    or source.get("source_url") != configured.get("sourceUrl")
                    or capture.get("url") != configured.get("sourceUrl")
                    or not capture.get("shutdown", {}).get("normal_browser_close")
                    or not capture.get("shutdown", {}).get("proxy_closed")
                    or capture.get("shutdown", {}).get("held_process", {}).get("direct_child") != "EXITED"):
                raise RuntimeScopeError("原模型分析缺少同一 Work 的宿主采集与关闭回执。")

        resources = AgentWorkResources(Path(self.db.path).absolute().parent / "agent-work",
            tenant_id=self.tenant, company_id=work["company_id"], work_ref=work["entity_id"], task_id=task_ref)
        raw = resources.read_output(receipt)
        snapshot = json.loads(raw)
        url = urlsplit(capture.get("url", ""))
        try:
            captured = datetime.fromisoformat(capture.get("captured_at", ""))
        except (ValueError, TypeError) as error:
            raise RuntimeScopeError("采集回执缺少 UTC 时间。") from error
        if (capture.get("identity") != resources.identity or capture.get("action") not in {"observe", "extract"}
                or capture.get("result_sha256") != receipt["sha256"] or snapshot.get("url") != capture.get("url")
                or url.scheme != "https" or not url.hostname or url.username or url.password
                or captured.utcoffset() is None or captured.utcoffset().total_seconds() != 0
                or not capture.get("session_id") or not capture.get("browser_instance_id")):
            raise RuntimeScopeError("原工作浏览器来源、字节或时间不一致。")
        result = ResultAttention(joined).detail(work["company_id"], None, "task:" + task_ref, scope=scope)
        return {"acceptance_basis": "EMPLOYEE_ANALYSIS",
            "model_analysis_status": "ACCEPTED",
            "result_version": result["result_version"], "source_url": capture["url"],
            "captured_at": capture["captured_at"], "snapshot_sha256": receipt["sha256"],
            "snapshot": snapshot, "usage_record_id": usage[0]["usage_record_id"]}


    def review_sources(self, con, child):
        """Discover only host receipts whose current successful worker proof verifies."""
        work, _, scope = self._lineage(con, child["entity_id"])
        ResultAttention(ConversationService(self.db)._work_database(con)).actor(work["company_id"])
        if work["lifecycle_status"] == "COMPLETED":
            return []
        sources = []
        for record in work["data"].get("responsibilityRouting", {}).get("executions", {}).values():
            if (not str(record.get("executionKey", "")).startswith("leader:worker:")
                    or record.get("status") != "ACCEPTED"):
                continue
            for artifact in record.get("artifactRefs", []):
                try:
                    self._proof(con, work, scope, record["taskRef"], artifact)
                except (ValueError, PermissionError, KeyError, OSError):
                    continue
                sources.append({"work_ref": work["entity_id"], "task_ref": record["taskRef"], "artifact_ref": artifact})
        return sources

    def _research_root(self, con, root_ref):
        root = self._entity(con, root_ref)
        ResultAttention(ConversationService(self.db)._work_database(con)).actor(root["company_id"])
        if not self.applies(con, root) or root["data"].get("leaderRootWorkRef"):
            raise RuntimeScopeError("需要原对话确认的 Music 研究工作。")
        return root

    def _can_set_browser_scope(self, con, root):
        return (TenantContext.current_identity().get("role", "").lower() in {"owner", "ceo"}
            and root["lifecycle_status"] == "ACTIVE"
            and root["data"].get("responsibilityRouting", {}).get("status") == "ACTIVE"
            and not root["data"].get("leaderDelegation")
            and not root["data"].get("responsibilityRouting", {}).get("executions")
            and not con.execute("select 1 from tasks where tenant_id=? and work_ref=?",
                (self.tenant, root["entity_id"])).fetchone())

    def browser_scope(self, root_ref, hosts, source_url=None):
        """Owner narrows this unstarted Work's hosts; no permission or release changes."""
        from .agent_browser_policy import PublicTargets
        with self.db.connect() as con:
            con.execute("begin immediate")
            root = self._research_root(con, root_ref)
            if not self._can_set_browser_scope(con, root):
                raise RuntimeScopeError("只有所有者可在原研究尚未执行时设置公开来源域名。")
            if not isinstance(hosts, list) or not 1 <= len(hosts) <= 8:
                raise ValueError("请指定一至八个公开来源域名。")
            policy = PublicTargets(hosts)
            if source_url is not None:
                policy.url(source_url)
                if "#" in source_url:
                    raise ValueError("请选择不含页内片段的公开原文 URL。")
            root["data"]["marketEvidenceBrowser"] = {"hosts": sorted(policy.hosts), "sourceUrl": source_url}
            con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                (json.dumps(root["data"], ensure_ascii=False), self.tenant, root_ref))
        return self.readiness(root_ref)

    def readiness(self, root_ref):
        """Read existing gates without launching a browser, model, or permission change."""
        from . import agent_browser_runtime
        from .agent_browser_policy import PublicTargets
        from .capability_authorizer import CapabilityAuthorizer
        with self.db.connect() as con:
            root = self._research_root(con, root_ref)
            contract = root["data"].get("followupContract") or self._entity(con, root["parent_id"], "CYCLE")["data"].get("contract") or {}
            browser = root["data"].get("marketEvidenceBrowser") or {}
            hosts = browser.get("hosts") or []
            source_url = browser.get("sourceUrl")
            blockers = []
            def blocked(code, message, **fields):
                blockers.append({"code": code, "message": message, **fields})
            try:
                if not hosts: raise ValueError("请先设置本次研究允许访问的公开来源域名。")
                PublicTargets(hosts)
            except ValueError as error:
                blocked("PUBLIC_HOSTS_REQUIRED", str(error))
            try:
                if not source_url: raise ValueError("请明确选择本次研究的公开原文 HTTPS URL。")
                PublicTargets(hosts).url(source_url)
                if "#" in source_url: raise ValueError("原文 URL 不能含页内片段。")
            except ValueError as error:
                blocked("PUBLIC_SOURCE_URL_REQUIRED", str(error))
            try:
                agent_browser_runtime.agent_browser_release()
            except (ValueError, OSError) as error:
                blocked("BROWSER_RELEASE_REQUIRED", str(error))
            joined = ConversationService(self.db)._work_database(con)
            route = root["data"].get("responsibilityRouting") or {}
            workflow = self._entity(con, route.get("workflowRef"), "RESPONSIBILITY_WORKFLOW")
            assignments = workflow["data"].get("assignments") or []
            if not any(not a.get("isLeader") for a in assignments):
                blocked("RESEARCH_EMPLOYEE_REQUIRED", "原研究没有已发布的研究员工责任安排。")
            for assignment in assignments:
                ref = assignment["assignmentRef"]
                try:
                    identity = EmployeeExecutionIdentity(joined).resolve(company_id=root["company_id"],
                        workspace_id=root["workspace_id"], runtime_employee_ref=assignment["employeeRef"])
                    binding = leader_preferred_binding(joined, root, assignment, identity["company_employee_ref"])
                    kind, capability_id = binding["capability_type"], binding["capability_id"]
                    if binding["capability_source"] == "tenant_private":
                        capability = joined.get_tenant_private_capability(self.tenant, kind, capability_id)
                    elif binding["capability_source"] == "official" and kind == "model":
                        capability = joined.get_active_official_model(capability_id)
                    else:
                        capability = None
                    if not capability or capability.get("status") != "active":
                        raise ValueError("员工绑定的能力不可用。")
                    if kind != "model":
                        blocked("MODEL_BINDING_REQUIRED", "本次公开取证使用员工已有文本模型；请在现有配置中选择模型绑定。", assignment_ref=ref)
                    authorizer = CapabilityAuthorizer(joined)
                    allowed, reason = authorizer.authorize(identity["company_employee_ref"], kind, capability_id, connection=con)
                    if not allowed:
                        blocked("POSITION_PERMISSION_REQUIRED", reason, assignment_ref=ref)
                    if not assignment.get("isLeader"):
                        allowed, reason = authorizer.authorize(identity["company_employee_ref"], "tool", "reader", connection=con)
                        if not allowed:
                            blocked("POSITION_READ_PERMISSION_REQUIRED", reason, assignment_ref=ref)
                except (ValueError, PermissionError, KeyError) as error:
                    blocked("EMPLOYEE_BINDING_REQUIRED", str(error), assignment_ref=ref)
            return {"work_ref": root_ref, "ready": not blockers, "blockers": blockers, "hosts": hosts,
                "source_url": source_url, "can_set_browser_scope": self._can_set_browser_scope(con, root)}

    def preview(self, child_ref, task_ref, artifact_ref):
        with self.db.connect() as con:
            work, root, scope = self._lineage(con, child_ref)
            ResultAttention(self.db).actor(work["company_id"])
            return {"work_ref": child_ref, "root_work_ref": root["entity_id"], "task_ref": task_ref,
                "artifact_ref": artifact_ref, "content_verification": "UNVERIFIED",
                **self._proof(con, work, scope, task_ref, artifact_ref)}


    def accept(self, child_ref, request: AcceptMarketEvidenceIn):
        if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("只有当前公司所有者可以接受市场证据。")
        if not request.reviewed:
            raise RuntimeScopeError("需要明确核对来源、指标口径及限制后接受。")
        with self.db.connect() as con:
            con.execute("begin immediate")
            joined = ConversationService(self.db)._work_database(con)
            work, root, scope = self._lineage(con, child_ref)
            actor = ResultAttention(joined).actor(work["company_id"])
            proof = self._proof(con, work, scope, request.task_ref, request.artifact_ref)
            if proof["result_version"] != request.result_version or proof["snapshot_sha256"] != request.snapshot_sha256:
                raise RuntimeScopeError("接受前原 Result 或网页快照版本已改变。")
            # Quotes are located in captured text; the owner, not this byte check, reviews their meaning.
            def texts(value):
                if isinstance(value, str): return [value]
                if isinstance(value, dict): return [s for v in value.values() for s in texts(v)]
                if isinstance(value, list): return [s for v in value for s in texts(v)]
                return []
            source_text = texts(proof["snapshot"].get("result"))
            if any(not any(m.source_quote in s for s in source_text) for m in request.metrics):
                raise RuntimeScopeError("指标引文不在原快照正文内。")
            decision = request.model_dump()
            evidence_ref = "evidence-" + digest([self.tenant, child_ref, request.task_ref, request.artifact_ref])[:32]
            prior = con.execute("select data_json from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant, evidence_ref)).fetchone()
            if prior:
                data = json.loads(prior["data_json"])
                if (data.get("reviewRequest") != decision or data.get("reviewedBy") != actor
                        or data.get("payloadSha256") != digest({k: v for k, v in data.items() if k != "payloadSha256"})):
                    raise RuntimeScopeError("原证据已接受，不能覆盖已接受版本。")
                self.accepted(con, root)
                return {"work_ref": child_ref, "evidence_ref": evidence_ref, "evidence_version": data["payloadSha256"]}
            if work["lifecycle_status"] != "ACTIVE":
                raise RuntimeScopeError("只有未完成的原研究工作可新增接受。")
            at = datetime.now(timezone.utc).isoformat(timespec="seconds")
            data = {"kind": "MUSIC_MARKET_EVIDENCE", "contentVerification": "VERIFIED",
                "acceptanceBasis": proof["acceptance_basis"], "modelAnalysisStatus": proof["model_analysis_status"],
                "sourceTaskRef": request.task_ref, "sourceWorkRef": child_ref, "rootWorkRef": root["entity_id"],
                "businessRef": scope["business_id"], "resultRef": "task:" + request.task_ref,
                "resultVersion": request.result_version, "snapshotArtifactRef": request.artifact_ref,
                "sourceUrl": proof["source_url"], "capturedAt": proof["captured_at"],
                "snapshotSha256": proof["snapshot_sha256"], "usageRecordRef": proof["usage_record_id"],
                "metrics": [m.model_dump() for m in request.metrics], "limitations": request.limitations,
                "reviewedBy": actor, "reviewedAt": at, "reviewDecision": "ACCEPT", "reviewRequest": decision}
            data["payloadSha256"] = digest(data)
            foundation = RuntimeFoundation(joined)
            foundation.create("EVIDENCE", entity_id=evidence_ref, company_id=work["company_id"],
                workspace_id=None, parent_id=child_ref, owner_ref=actor, lifecycle_status="CURRENT",
                verification_status="VERIFIED", evidence_condition="CURRENT", data=data)
            acceptance = foundation.create("ACCEPTANCE", company_id=work["company_id"], workspace_id=None,
                parent_id=child_ref, owner_ref=actor, data={"resultRefs": [data["resultRef"]],
                    "evidenceRefs": [evidence_ref], "requestId": request.request_id, "decision": "ACCEPT",
                    "acceptanceBasis": proof["acceptance_basis"], "modelAnalysisStatus": proof["model_analysis_status"]})
            foundation.transition(acceptance["entity_id"], "ACCEPTED", actor="CEO", trigger="accept")
            foundation.transition(acceptance["entity_id"], "CLOSED", actor="SYSTEM", trigger="close")
            self.child._complete_work_locked(con, work, {"resultRefs": [data["resultRef"]],
                "artifactRefs": [request.artifact_ref], "evidenceRefs": [evidence_ref],
                "acceptanceRefs": [acceptance["entity_id"]]})
            return {"work_ref": child_ref, "evidence_ref": evidence_ref, "evidence_version": data["payloadSha256"]}


    def accepted(self, con, root):
        """Return exact reviewed versions, or None while any child awaits review."""
        inputs, sources = [], []
        for child_ref in root["data"].get("leaderDelegation", {}).get("childWorkRefs", []):
            work, _, scope = self._lineage(con, child_ref)
            if work["lifecycle_status"] != "COMPLETED":
                return None
            refs = work["data"].get("evidenceRefs", [])
            if len(refs) != 1:
                raise RuntimeScopeError("原研究工作需要唯一的正式市场证据。")
            evidence = self._entity(con, refs[0], "EVIDENCE")
            data = dict(evidence["data"])
            version = data.pop("payloadSha256", None)
            if (not version or digest(data) != version or data.get("kind") != "MUSIC_MARKET_EVIDENCE"
                    or data.get("contentVerification") != "VERIFIED" or data.get("fixture")
                    or evidence["lifecycle_status"] != "CURRENT" or data.get("sourceWorkRef") != child_ref
                    or data.get("rootWorkRef") != root["entity_id"] or data.get("businessRef") != scope["business_id"]):
                raise RuntimeScopeError("市场证据已改变或不属于原研究。")
            self.child._validate_outcome(con, work, result_refs=work["data"].get("resultRefs", []),
                artifact_refs=work["data"].get("artifactRefs", []), evidence_refs=refs,
                acceptance_refs=work["data"].get("acceptanceRefs", []))
            proof = self._proof(con, work, scope, data["sourceTaskRef"], data["snapshotArtifactRef"])
            if (proof["result_version"] != data["resultVersion"] or proof["snapshot_sha256"] != data["snapshotSha256"]
                    or proof["source_url"] != data["sourceUrl"] or proof["captured_at"] != data["capturedAt"]
                    or proof["acceptance_basis"] != data.get("acceptanceBasis", "EMPLOYEE_ANALYSIS")
                    or proof["model_analysis_status"] != data.get("modelAnalysisStatus", "ACCEPTED")):
                raise RuntimeScopeError("正式市场证据的原结果或来源已改变。")
            inputs.append({"evidence_ref": refs[0], "evidence_version": version})
            sources.append({k: data[k] for k in ("sourceWorkRef", "sourceTaskRef", "sourceUrl", "capturedAt",
                "snapshotSha256", "metrics", "limitations")})
            sources[-1].update(acceptanceBasis=proof["acceptance_basis"], modelAnalysisStatus=proof["model_analysis_status"])
        return {"inputs": inputs, "sources": sources} if inputs else None


    def pin_summary(self, con, root, summary_ref, expected, execution_key=None):
        current = self.accepted(con, root)
        if current != expected:
            raise RuntimeScopeError("汇总前原市场证据版本已改变。")
        summary = self._entity(con, summary_ref)
        if (summary["data"].get("leaderRootWorkRef") != root["entity_id"]
                or root["data"]["leaderDelegation"].get("summaryWorkRef") != summary_ref):
            raise RuntimeScopeError("汇总不属于原研究工作。")
        prior = summary["data"].get("marketEvidenceInputs")
        if prior is not None and prior != expected["inputs"]:
            raise RuntimeScopeError("不能替换原汇总的证据版本。")
        summary["data"]["marketEvidenceInputs"] = expected["inputs"]
        if execution_key:
            record = summary["data"]["responsibilityRouting"]["executions"][execution_key]
            if record.get("evidenceInputs") not in (None, expected["inputs"]):
                raise RuntimeScopeError("汇总执行的证据版本改变。")
            record["evidenceInputs"] = expected["inputs"]
        con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
            (json.dumps(summary["data"], ensure_ascii=False), self.tenant, summary_ref))
