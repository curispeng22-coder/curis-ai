"""CEO viewing receipts over canonical results and the existing append-only log.

Viewing is not acceptance. GETs never append; only the explicit view command does.
"""

import hashlib
import json
import re
from uuid import UUID

from .evolution_event_log import EvolutionEventLog
from .runtime import RuntimeScopeError
from .resource_scope_policy import ResourceScopePolicy
from .shared_workspace_projection import SharedWorkspaceProjection
from .tenant_context import TenantContext


VIEWED = "result.viewed"
RESPONSE = "result.response"
CHOICES = {"ACCEPT", "REVISE", "REJECT"}


def result_version(result: dict) -> str | None:
    if result.get("kind") not in {"RESULT", "OUTCOME"}:
        return None
    # Exclude receipt/disposition and incidental timestamps. New content, execution
    # or artifact revision is a new result; merely re-reading is not.
    content = {key: result.get(key) for key in (
        "reference_id", "kind", "status", "content", "data", "execution_ref",
        "source_work_ref", "verification_status",
    )}
    content["artifacts"] = sorted(
        (str(item.get("artifact_id")), str(item.get("content_sha256")))
        for item in result.get("artifacts", [])
    )
    return hashlib.sha256(json.dumps(content, sort_keys=True, ensure_ascii=False).encode()).hexdigest()


class ResultAttention:
    def __init__(self, database):
        self.db = database
        self.shared = SharedWorkspaceProjection(database)
        self.events = EvolutionEventLog(database)

    def actor(self, company_id: str) -> str:
        identity = TenantContext.current_identity()
        ceo_id = identity.get("ceo_id")
        if not ceo_id:
            raise RuntimeScopeError("CEO identity is required")
        if identity.get("company_id") and identity["company_id"] != company_id:
            raise RuntimeScopeError("Company identity does not match")
        with self.db.connect() as connection:
            company = connection.execute(
                "select ceo_id from companies where tenant_id=? and company_id=?",
                (TenantContext.current_tenant_id(), company_id),
            ).fetchone()
        if company is None or company["ceo_id"] != ceo_id:
            raise RuntimeScopeError("CEO does not own this Company")
        return ceo_id

    def _key(self, company_id: str, ceo_id: str, ref: str, version: str) -> str:
        scope = [VIEWED, TenantContext.current_tenant_id(), company_id, ceo_id, ref, version]
        return VIEWED + ":" + hashlib.sha256(json.dumps(scope).encode()).hexdigest()

    def viewed(self, company_id: str, ref: str, version: str) -> bool:
        ceo_id = self.actor(company_id)
        with self.db.connect() as connection:
            return connection.execute(
                "select 1 from evolution_events where tenant_id=? and event_type=? and idempotency_key=?",
                (TenantContext.current_tenant_id(), VIEWED, self._key(company_id, ceo_id, ref, version)),
            ).fetchone() is not None

    def detail(self, company_id: str, workspace_id: str | None, ref: str, *, scope=None) -> dict:
        self.actor(company_id)
        if ref.startswith("task:"):
            with self.db.connect() as connection:
                conversation = connection.execute(
                    "select 1 from evolution_events where tenant_id=? and correlation_id=? "
                    "and event_type='conversation.execution_bound' limit 1",
                    (TenantContext.current_tenant_id(), ref[5:]),
                ).fetchone()
            if conversation:
                raise RuntimeScopeError("Conversation execution is not a business Result")
        result = self.shared.result(company_id, workspace_id, ref, scope=scope)
        version = result_version(result)
        responses = []
        eligible = {"status": "INELIGIBLE", "reason": "此来源尚不能记录交付选择。"}
        if workspace_id and ref.startswith("task:"):
            with self.db.connect() as connection:
                try:
                    self._response_source_identity(connection, company_id, workspace_id, ref,
                        result.get("source_work_ref") or "")
                    responses = self._responses(connection, company_id, workspace_id, ref, TenantContext.current_identity()["ceo_id"])
                    self._response_source(connection, company_id, workspace_id, ref)
                    eligible = {"status": "ELIGIBLE", "reason": ""}
                except (RuntimeScopeError, ValueError) as error:
                    eligible["reason"] = str(error)
        current = next((item for item in responses if item["result_version"] == version), None)
        if current:
            eligible = {"status": "DECIDED", "reason": "已保存此版本的人类选择。"}
        return {**result, "tenant_id": TenantContext.current_tenant_id(),
                "company_id": company_id, "workspace_id": workspace_id, "result_version": version,
                "response_actor_ref": TenantContext.current_identity()["ceo_id"],
                "viewed": self.viewed(company_id, ref, version) if version else False,
                "user_response": current, "user_responses": responses,
                "response_eligibility": eligible}

    @staticmethod
    def _receipt(event: dict) -> dict:
        payload = event["payload"]
        if not isinstance(payload, dict) or any(key not in payload for key in (
                "company_id", "workspace_id", "result_ref", "result_version", "source_work_ref",
                "action", "reason", "request_id", "ceo_id")):
            raise ValueError("原选择记录无法核验。")
        return {key: payload[key] for key in ("company_id", "workspace_id", "result_ref", "result_version",
                "source_work_ref", "action", "reason", "request_id", "ceo_id")} | {
                    "tenant_id": event["tenant_id"], "receipt_ref": event["event_id"], "decided_at": event["created_at"]}

    def _responses(self, connection, company_id: str, workspace_id: str, ref: str, ceo_id: str) -> list[dict]:
        malformed = connection.execute(
            "select 1 from evolution_events where tenant_id=? and event_type=? and correlation_id=? "
            "and case when json_valid(payload) then json_type(payload) else 'invalid' end!='object' limit 1",
            (TenantContext.current_tenant_id(), RESPONSE, ref),
        ).fetchone()
        if malformed:
            raise ValueError("原选择记录格式无法核验。")
        rows = connection.execute(
            "select * from evolution_events where tenant_id=? and event_type=? and correlation_id=? "
            "and case when json_valid(payload) then json_extract(payload,'$.company_id') end=? "
            "and case when json_valid(payload) then json_extract(payload,'$.workspace_id') end=? "
            "and case when json_valid(payload) then json_extract(payload,'$.ceo_id') end=? order by event_id",
            (TenantContext.current_tenant_id(), RESPONSE, ref, company_id, workspace_id, ceo_id),
        ).fetchall()
        receipts = []
        for row in rows:
            event = self.events._event_from_row(row)
            receipt = self._receipt(event)
            if (event["tenant_id"] != TenantContext.current_tenant_id()
                    or receipt["company_id"] != company_id or receipt["workspace_id"] != workspace_id
                    or receipt["result_ref"] != ref or receipt["ceo_id"] != ceo_id
                    or receipt["action"] not in CHOICES or not isinstance(receipt["reason"], str)
                    or not receipt["reason"].strip()):
                raise ValueError("原选择来源无法核验。")
            receipts.append(receipt)
        return receipts

    def _response_source(self, connection, company_id: str, workspace_id: str, ref: str) -> dict:
        tenant = TenantContext.current_tenant_id()
        identity = TenantContext.current_identity()
        ceo = identity.get("ceo_id")
        if identity.get("role", "").lower() not in {"ceo", "owner"} or not ceo or identity.get("company_id") not in {None, "", company_id}:
            raise RuntimeScopeError("CEO identity does not match this Company")
        company = connection.execute("select ceo_id from companies where tenant_id=? and company_id=?", (tenant, company_id)).fetchone()
        if not company or company["ceo_id"] != ceo:
            raise RuntimeScopeError("CEO does not own this Company")
        try:
            ResourceScopePolicy.resolve_execution_scope(connection, tenant_id=tenant, company_id=company_id,
                scope_type="WORKSPACE", scope_ref=workspace_id)
        except ValueError as error:
            raise RuntimeScopeError("Result Workspace is outside current Company") from error
        if not ref.startswith("task:") or not ref[5:]:
            raise ValueError("仅原工作中已完成的交付结果可记录选择。")
        task = connection.execute("select * from tasks where tenant_id=? and company_id=? and workspace_id=? and task_id=?",
            (tenant, company_id, workspace_id, ref[5:])).fetchone()
        if not task or not task["work_ref"]:
            raise RuntimeScopeError("Result has no canonical source Work")
        work = connection.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='WORK' and entity_id=?", (tenant, company_id, workspace_id, task["work_ref"])).fetchone()
        if not work:
            raise RuntimeScopeError("Source Work is outside this Workspace")
        conversation = connection.execute("select 1 from evolution_events where tenant_id=? and event_type='conversation.execution_bound' "
            "and correlation_id=? limit 1", (tenant, ref[5:])).fetchone()
        if conversation:
            raise ValueError("员工对话执行不是此工作交付。")
        blueprint_row = connection.execute("select blueprint_json from workspaces where tenant_id=? and company_id=? and workspace_id=?",
            (tenant, company_id, workspace_id)).fetchone()
        try:
            blueprint = json.loads(blueprint_row["blueprint_json"]) if blueprint_row else None
            work_data = json.loads(work["data_json"])
        except (TypeError, json.JSONDecodeError) as error:
            raise ValueError("原工作来源资料无法核验。") from error
        if (not isinstance(blueprint, dict) or str(blueprint.get("productForm") or "").upper() != "GENERIC"
                or not isinstance(work_data, dict) or task["scope_type"] != "WORKSPACE"
                or task["scope_ref"] != workspace_id or not task["execution_ref"]):
            raise ValueError("交付不属于当前通用工作空间。")
        routing = work_data.get("responsibilityRouting")
        if (not isinstance(routing, dict) or routing.get("scopeType") != "WORKSPACE"
                or routing.get("scopeRef") != workspace_id or not isinstance(routing.get("executions"), dict)):
            raise ValueError("原工作责任来源无法核验。")
        result_refs = routing.get("resultRefs")
        human_input = routing.get("humanInput", {})
        if (type(result_refs) is not list or any(type(item) is not str or not item for item in result_refs)
                or type(human_input) is not dict):
            raise ValueError("原工作责任来源无法核验。")
        claims = [(key, value) for key, value in routing["executions"].items()
            if isinstance(value, dict) and (value.get("taskRef") == ref[5:] or value.get("resultRef") == ref)]
        if len(claims) != 1 or claims[0][0] != task["execution_ref"]:
            raise ValueError("原执行与工作责任未唯一绑定。")
        execution = routing["executions"].get(task["execution_ref"])
        if not isinstance(execution, dict):
            raise ValueError("原执行与工作责任未绑定。")
        provenance = execution.get("provenance") or {}
        if not isinstance(provenance, dict):
            raise ValueError("原执行核验来源无效。")
        workflow = connection.execute("select data_json from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='RESPONSIBILITY_WORKFLOW' and entity_id=?",
            (tenant, company_id, workspace_id, routing.get("workflowRef") or "")).fetchone()
        try:
            workflow_data = json.loads(workflow["data_json"]) if workflow else None
        except (TypeError, json.JSONDecodeError) as error:
            raise ValueError("原责任流程资料无法核验。") from error
        if not isinstance(workflow_data, dict):
            raise ValueError("原责任流程资料无法核验。")
        assignments = workflow_data.get("assignments")
        pinned = next((item for item in assignments if isinstance(item, dict)
            and item.get("assignmentRef") == execution.get("assignmentRef")), None) if isinstance(assignments, list) else None
        if (work["lifecycle_status"] not in {"ACTIVE", "COMPLETED"} or task["status"] != "COMPLETED"
            or not isinstance(task["output"], str) or not task["output"].strip()
            or workflow_data.get("scopeType") != "WORKSPACE" or workflow_data.get("scopeRef") != workspace_id
            or type(workflow_data.get("version")) is not int or type(routing.get("workflowVersion")) is not int
            or workflow_data.get("version") != routing.get("workflowVersion") or not pinned
            or pinned.get("employeeRef") != task["employee_id"]
            or execution.get("executionKey") != task["execution_ref"]
            or execution.get("employeeRef") != task["employee_id"]
            or execution.get("responsibilityKey") != pinned.get("responsibilityKey")
            or ref not in result_refs or human_input.get("state") not in {None, "CLOSED", "INVALIDATED"}
            or execution.get("taskRef") != ref[5:] or execution.get("resultRef") != ref
            or execution.get("status") != "ACCEPTED" or execution.get("humanInputSource") is True
            or execution.get("employeeRef") != task["employee_id"]
            or provenance.get("verification_status") != "VERIFIED"
            or provenance.get("task_ref") != ref[5:] or provenance.get("task_status") != "COMPLETED"
            or provenance.get("callback_actor_ref") != task["employee_id"]):
            raise ValueError("原工作交付尚无可核验的完整结果，或责任状态已变化。")
        result = self.shared._result(company_id, workspace_id, ref, include_content=True, connection=connection)
        if not result or result.get("source_work_ref") != task["work_ref"]:
            raise ValueError("原结果与工作来源不一致。")
        return {**result, "result_version": result_version(result)}

    def decide_response(self, company_id: str, *, workspace_id: str, result_ref: str, result_version_value: str,
                        source_work_ref: str, action: str, reason: str, request_id: str) -> dict:
        if (any(type(value) is not str or not value or value != value.strip() for value in
                (company_id, workspace_id, result_ref, result_version_value, source_work_ref, action, request_id))
            or type(reason) is not str or action not in CHOICES
            or not re.fullmatch(r"[0-9a-f]{64}", result_version_value)):
            raise ValueError("选择的对象、版本或动作无效。")
        try:
            if str(UUID(request_id)) != request_id:
                raise ValueError
        except ValueError as error:
            raise ValueError("请求标识必须是规范 UUID。") from error
        reason = reason.strip()
        if not reason or len(reason.encode("utf-8")) > 2000:
            raise ValueError("请填写不超过 2000 UTF-8 字节的理由。")
        tenant = TenantContext.current_tenant_id()
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            # First prove current actor and original Work scope, even for a historical replay.
            source = self._response_source_identity(connection, company_id, workspace_id, result_ref, source_work_ref)
            ceo = TenantContext.current_identity()["ceo_id"]
            key = RESPONSE + ":" + hashlib.sha256(json.dumps(
                [tenant, company_id, workspace_id, ceo, result_ref, result_version_value, request_id]).encode()).hexdigest()
            payload = {"ceo_id": ceo, "company_id": company_id, "workspace_id": workspace_id,
                "result_ref": result_ref, "result_version": result_version_value, "source_work_ref": source_work_ref,
                "action": action, "reason": reason, "request_id": request_id}
            prior = connection.execute("select * from evolution_events where idempotency_key=?", (key,)).fetchone()
            if prior:
                event = self.events._event_from_row(prior)
                if event["tenant_id"] != tenant or event["event_type"] != RESPONSE or event["correlation_id"] != result_ref or event["payload"] != payload:
                    raise ValueError("相同请求标识对应不同选择。")
                return {**self._receipt(event), "replayed": True}
            current = self._response_source(connection, company_id, workspace_id, result_ref)
            if current["source_work_ref"] != source["work_ref"] or current["result_version"] != result_version_value:
                raise ValueError("结果版本已变化，请重新读取原工作。")
            if any(item["result_version"] == result_version_value for item in
                   self._responses(connection, company_id, workspace_id, result_ref, ceo)):
                raise ValueError("此版本已经保存过人类选择。")
            event = self.events.record_in_connection(connection, correlation_id=result_ref,
                event_type=RESPONSE, payload=payload, idempotency_key=key)
            return {**self._receipt(event), "replayed": False}

    def _response_source_identity(self, connection, company_id: str, workspace_id: str, ref: str, work_ref: str):
        tenant = TenantContext.current_tenant_id()
        identity = TenantContext.current_identity()
        actor = identity.get("ceo_id")
        if identity.get("role", "").lower() not in {"ceo", "owner"} or not actor or identity.get("company_id") not in {None, "", company_id}:
            raise RuntimeScopeError("CEO identity does not match this Company")
        company = connection.execute("select ceo_id from companies where tenant_id=? and company_id=?", (tenant, company_id)).fetchone()
        if not company or company["ceo_id"] != actor:
            raise RuntimeScopeError("CEO does not own this Company")
        try:
            ResourceScopePolicy.resolve_execution_scope(connection, tenant_id=tenant, company_id=company_id,
                scope_type="WORKSPACE", scope_ref=workspace_id)
        except ValueError as error:
            raise RuntimeScopeError("Workspace is outside current Company") from error
        if not ref.startswith("task:"):
            raise RuntimeScopeError("Source is not a Task Result")
        task = connection.execute("select work_ref,scope_type,scope_ref,execution_ref from tasks where tenant_id=? and company_id=? and workspace_id=? and task_id=?",
            (tenant, company_id, workspace_id, ref[5:])).fetchone()
        work = connection.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='WORK' and entity_id=?", (tenant, company_id, workspace_id, work_ref)).fetchone()
        if (not task or task["work_ref"] != work_ref or task["scope_type"] != "WORKSPACE"
                or task["scope_ref"] != workspace_id or not task["execution_ref"] or not work):
            raise RuntimeScopeError("Result and original Work no longer share this scope")
        return {"work_ref": work_ref}

    def mark_viewed(self, company_id: str, workspace_id: str, ref: str, version: str) -> dict:
        if TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("Only the CEO can record a view")
        ceo_id = self.actor(company_id)
        result = self.detail(company_id, workspace_id, ref)
        if not result["result_version"] or result["result_version"] != version:
            raise ValueError("结果已更新，请重新打开最新版本。")
        if result["kind"] == "RESULT" and str(result["status"]).upper() not in {"COMPLETED", "FAILED"}:
            raise ValueError("结果尚未返回，请稍后重新查看。")
        event = self.events.record(
            correlation_id=ref, event_type=VIEWED,
            idempotency_key=self._key(company_id, ceo_id, ref, version),
            payload={"ceo_id": ceo_id, "company_id": company_id, "workspace_id": workspace_id,
                     "result_ref": ref, "result_version": version, "action": "viewed"},
        )
        return {"result_ref": ref, "result_version": version, "viewed": True, "receipt_ref": event["event_id"]}

    def unseen_results(self, company_id: str) -> list[dict]:
        self.actor(company_id)
        with self.db.connect() as connection:
            rows = connection.execute(
                "select task_id, workspace_id from tasks where tenant_id=? and company_id=? "
                "and workspace_id is not null and workspace_id!='' and upper(status) in ('COMPLETED','FAILED') "
                "and output is not null and output!=''",
                (TenantContext.current_tenant_id(), company_id),
            ).fetchall()
        results = []
        for row in rows:
            try:
                result = self.detail(company_id, row["workspace_id"], "task:" + row["task_id"])
            except (KeyError, RuntimeScopeError):
                continue  # Unresolvable historical lineage cannot become current Attention.
            if not result["viewed"]:
                results.append({
                    "source_ref": result["reference_id"], "source_type": "RESULT",
                    "workspace_id": row["workspace_id"], "status": result["status"],
                    "summary": result["title"] or "有一份新结果", "rank": 4,
                    "result_version": result["result_version"], "disposition": "NEW",
                    "owner_ref": result.get("owner_ref"), "updated_at": result.get("updated_at"),
                })
        return results
