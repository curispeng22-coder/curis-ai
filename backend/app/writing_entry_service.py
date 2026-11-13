"""Built-in Writing entry; composes existing Package/Company/Employee services.

The release file is derived decision evidence, not a catalog or an execution grant.
"""
from __future__ import annotations

import hashlib
import json
import uuid
import math
from pathlib import Path

from .conversation_service import ConversationService
from .employee_templates import EmployeeTemplateContract, professional_team_contract
from .employee_execution_identity import EmployeeExecutionIdentity
from .model_preferences import TenantModelPreferenceResolver
from .result_attention import ResultAttention
from .runtime import RuntimeFoundation, RuntimeScopeError
from .runtime.responsibility_routing import ResponsibilityRoutingRuntime
from .tenant_context import TenantContext
from .workspace_package_runtime import WorkspacePackageRuntime, validate_package
from .writing_chapter_service import WritingChapterService, WritingConflict, PACKAGE_ID, PACKAGE_VERSION, PACKAGE_DIGEST

AUTHOR = "WRITING_CHAPTER_AUTHOR"
PURPOSE = "WRITING_CHAPTER_REPLY"
ASSETS = Path(__file__).resolve().parent / "bundled_workspace_packages"


def encoded(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def fingerprint(value):
    return hashlib.sha256(encoded(value).encode()).hexdigest()


class WritingEntryService:
    def __init__(self, database, *, conversation_service=None, execution_grant=None):
        self.db = database
        self.conversations = conversation_service or ConversationService(database)
        self.local = WritingChapterService(database, conversation_service=self.conversations)
        self.foundation = RuntimeFoundation(database)
        self.employees = EmployeeTemplateContract(database)
        self.routing = ResponsibilityRoutingRuntime(database)
        self.models = TenantModelPreferenceResolver(database)
        # Only authorized server composition may supply a grant. There is no client setter.
        self.execution_grant = execution_grant

    def actor(self, company, *, write=False):
        ceo = ResultAttention(self.db).actor(company)
        if write and TenantContext.current_identity().get("role", "").lower() not in {"ceo", "owner"}:
            raise RuntimeScopeError("只有公司所有者可以确认这项操作。")
        return ceo

    def publication(self):
        release = json.loads((ASSETS / "writing_authoring_release.json").read_text())
        if (release.get("packageId"), release.get("version"), release.get("digest")) != (PACKAGE_ID, PACKAGE_VERSION, PACKAGE_DIGEST):
            raise WritingConflict("写作组件与批准的版本不一致，暂不能启用。")
        if (release.get("approvedScope") != ["LOCAL_BOOK_CHAPTER", "AUTHOR_MANUAL_FORMAL", "LOCAL_DOWNLOAD"]
                or release.get("publicRelease") is not False or release.get("providerFeeGrant") is not False
                or not release.get("decision", {}).get("sha256")
                or release.get("decision", {}).get("candidateSHA256") != "9890cc7f086b78e6f3fdb795a25d6dbd267eed3391465cc634aa027c2e3878c7"):
            raise WritingConflict("缺少写作组件的限定批准来源。")
        source = ASSETS / "writing_authoring"
        package = validate_package(source)
        if package["digest"] != PACKAGE_DIGEST:
            raise WritingConflict("写作组件文件已变化，原批准不适用。")
        for rel, expected in release["files"].items():
            if hashlib.sha256((source / rel).read_bytes()).hexdigest() != expected:
                raise WritingConflict("写作组件来源校验失败。")
        return {"package_id": PACKAGE_ID, "version": PACKAGE_VERSION, "digest": PACKAGE_DIGEST,
                "release_sha256": fingerprint(release), "name": "本地写作工作空间",
                "scope": release["approvedScope"], "entry_acceptance": release["entryAcceptance"],
                "initial_team_contract": professional_team_contract(PACKAGE_ID, PACKAGE_VERSION, PACKAGE_DIGEST)}

    def definitions(self, company):
        self.actor(company)
        with self.db.connect() as con:
            departments = [dict(r) for r in con.execute("select id,name from department_instances where tenant_id=? and company_id=? "
                "and deleted_at is null and enabled=1 and status!='archived'", (TenantContext.current_tenant_id(), company)).fetchall()]
        try:
            definition = self.publication()
            return {"definition": definition, "departments": departments, "available": True,
                    "notice": "本地编辑、作者人工确认正式稿与下载；员工执行另需能力和授权。"}
        except (ValueError, OSError) as error:
            return {"definition": None, "departments": departments, "available": False, "notice": str(error)}

    def proposal(self, company, values):
        self.actor(company, write=True)
        definition = self.publication()
        if values.get("package_id") != PACKAGE_ID:
            raise WritingConflict("请选择当前获批准的写作组件。")
        department = values.get("department_id")
        if department not in {item["id"] for item in self.definitions(company)["departments"]}:
            raise RuntimeScopeError("请明确选择当前公司的合法部门。")
        snapshot = {key: str(values.get(key) or "").strip() for key in
                    ("intent", "business_name", "goal", "positioning", "workspace_name")}
        snapshot.update(company_id=company, department_id=department, package_id=PACKAGE_ID, definition=definition)
        return {**values, "snapshot": snapshot, "proposal_sha256": fingerprint(snapshot)}

    def assignments(self, con, company, workspace):
        rows = con.execute("select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
            "and entity_type='RESPONSIBILITY_ASSIGNMENT' and lifecycle_status='ACTIVE'",
            (TenantContext.current_tenant_id(), company, workspace)).fetchall()
        return [dict(row) | {"data": json.loads(row["data_json"])} for row in rows
                if json.loads(row["data_json"]).get("responsibilityKey") == AUTHOR]

    def pending(self, con, company, workspace):
        rows = con.execute("select event_type,payload from evolution_events where tenant_id=? "
            "and event_type in ('conversation.attempt.started','conversation.attempt.finished') "
            "and json_extract(payload,'$.company_id')=? and json_extract(payload,'$.context.workspace_id')=? "
            "and correlation_id in (select json_extract(payload,'$.output.conversation_ref') from evolution_events "
            "where tenant_id=? and event_type='writing.chapter.discussion.bound' "
            "and json_extract(payload,'$.scope.company_id')=? and json_extract(payload,'$.scope.workspace_id')=?) order by event_id",
            (TenantContext.current_tenant_id(), company, workspace, TenantContext.current_tenant_id(), company, workspace)).fetchall()
        attempts = {}
        for row in rows:
            value = json.loads(row["payload"]); attempts[value["attempt_id"]] = value
        return [value for value in attempts.values() if value.get("status") not in {"COMPLETED", "FAILED", "CANCELLED"}
                or value.get("effect_status") == "UNKNOWN"]

    def _configuration(self, con, workspace):
        row = con.execute("select event_type,payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type in ('writing.configuration.started','writing.configuration.finished') order by event_id desc limit 1",
            (TenantContext.current_tenant_id(), workspace)).fetchone()
        return json.loads(row["payload"]) if row else None

    def require_settled(self, con, company, workspace, *, configuration=False):
        if self.pending(con, company, workspace):
            raise WritingConflict("原请求正在处理或结果待核验；请先查询原请求，不能更换责任员工或模型。")
        current = self._configuration(con, workspace)
        if current and current["status"] == "RUNNING":
            raise WritingConflict("原责任配置尚未完成；请重新读取，不会清除原请求。")
        if not configuration and current and current["status"] != "COMPLETED":
            raise WritingConflict("责任配置未完成，请先核对配置。")

    def _selected(self, con, workspace):
        row = con.execute("select payload from evolution_events where tenant_id=? and correlation_id=? "
            "and event_type='writing.model.selected' order by event_id desc limit 1", (TenantContext.current_tenant_id(), workspace)).fetchone()
        return json.loads(row["payload"]) if row else None

    def metadata(self, company, workspace):
        with self.db.connect() as con:
            scope, _, _, _ = self.local._scope(con, company, workspace)
            assignments = self.assignments(con, company, workspace)
            pending = self.pending(con, company, workspace)
            selected = self._selected(con, workspace)
            configuration = self._configuration(con, workspace)
        employees = [e for e in self.employees.list_employee_instances()["employees"]
                     if e["company_id"] == company and e["enabled"] and e["status"] in {"idle", "assigned"}]
        assignment = assignments[0] if len(assignments) == 1 else None
        employee_ref = (assignment or {}).get("data", {}).get("employeeRef")
        try:
            runtime = self.foundation.get(employee_ref) if employee_ref else None
        except (KeyError, RuntimeScopeError):
            runtime = None
        company_employee_ref = (runtime or {}).get("data", {}).get("companyEmployeeRef") or employee_ref
        employee = next((e for e in employees if e["id"] == company_employee_ref), None)
        return {"scope": scope, "employees": [{"id": e["id"], "name": e["name"], "role": e["role"]} for e in employees],
                "assignment_ref": assignment["entity_id"] if assignment else "", "assignment_revision": assignment["data"]["revision"] if assignment else 0,
                "employee_ref": employee_ref or "", "company_employee_ref": company_employee_ref or "", "employee_name": employee["name"] if employee else "",
                "model_preference": self.models.read_current()["preference"], "models": self.models.available_models(), "selected_model": selected if selected and assignment and selected["employee_ref"] == employee_ref and selected["assignment_revision"] == assignment["data"]["revision"] else None,
                "pending": [{"attempt_id": a["attempt_id"], "status": "RUNNING" if a["attempt_id"] in self.conversations.running else "UNKNOWN"} for a in pending],
                "configuration": configuration, "execution": self.execution_policy(company, workspace)}

    def _configure(self, company, workspace, operation):
        """Existing APIs may commit separately; a persisted scope guard blocks execution throughout."""
        self.actor(company, write=True)
        token = str(uuid.uuid4())
        with self.db.connect() as con:
            con.execute("begin immediate")
            self.local._scope(con, company, workspace, write=True)
            self.require_settled(con, company, workspace, configuration=True)
            con.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,'writing.configuration.started',?,?)",
                (TenantContext.current_tenant_id(), workspace, encoded({"status": "RUNNING", "configuration_id": token}), token))
        status = "FAILED"
        try:
            operation()
            status = "COMPLETED"
        finally:
            self.conversations.events.record(correlation_id=workspace, event_type="writing.configuration.finished",
                payload={"status": status, "configuration_id": token}, idempotency_key=token + ":finished")
        return self.metadata(company, workspace)

    def assign(self, company, workspace, employee_id, expected_revision):
        def operation():
            employee = self.employees.get_employee_instance(employee_id)
            if (not employee or employee["company_id"] != company or not employee["enabled"]
                    or employee["status"] not in {"idle", "assigned"}):
                raise RuntimeScopeError("责任员工不属于当前公司或不可承担责任。")
            candidates = [r for r in self.foundation.list("AI_EMPLOYEE", company_id=company)
                if r["workspace_id"] in (None, workspace) and (r["entity_id"] == employee_id or r["data"].get("companyEmployeeRef") == employee_id)]
            if len(candidates) > 1:
                raise WritingConflict("员工运行身份不唯一，请先核对。")
            runtime = candidates[0] if candidates else self.foundation.create("AI_EMPLOYEE", entity_id=employee_id,
                company_id=company, lifecycle_status="AVAILABLE", data={"name": employee["name"], "role": employee["role"], "companyEmployeeRef": employee_id})
            runtime_ref = runtime["entity_id"]
            with self.db.connect() as con:
                current = self.assignments(con, company, workspace)
            revision = current[0]["data"]["revision"] if len(current) == 1 else 0
            if len(current) > 1 or revision != expected_revision:
                raise WritingConflict("责任安排已变化，请重新读取。")
            if current:
                if current[0]["data"]["employeeRef"] != runtime_ref:
                    self.routing.update_assignment(current[0]["entity_id"], employee_ref=runtime_ref)
            else:
                preset = self.publication()["initial_team_contract"]["members"][1]
                role = self.foundation.create("ROLE_SLOT", company_id=company, workspace_id=workspace,
                    lifecycle_status="ASSIGNED", data={"name": "章节作者", "role": "章节写作", "responsibility": "按作者依据讨论章节修改"})
                self.routing.create_assignment(company_id=company, workspace_id=workspace, scope_type="WORKSPACE", scope_ref=workspace,
                    role_ref=role["entity_id"], employee_ref=runtime_ref, responsibility_key=AUTHOR,
                    responsibility="按作者保存的正文与选文依据讨论章节修改",
                    input_contract=preset["inputContract"],
                    output_contract=preset["outputContract"])
            self.employees.update_employee_instance(employee_id, {"status": "assigned"})
        return self._configure(company, workspace, operation)

    def prepare_model(self, company, workspace, assignment_ref, model_key):
        self.actor(company, write=True)
        with self.db.connect() as con:
            self.local._scope(con, company, workspace, write=True)
            assignments = self.assignments(con, company, workspace)
        if len(assignments) != 1 or assignments[0]["entity_id"] != assignment_ref:
            raise WritingConflict("当前章节作者责任已变化。")
        self.models.prepare_employee_model(company, workspace, assignments[0]["data"]["employeeRef"], model_key, self.models.professional_grant(self.execution_grant, company, workspace, model_key))
        self.select_model(company, workspace, model_key)

    def select_model(self, company, workspace, model_key):
        def operation():
            self.publication()
            model = self.models._require_eligible_model(TenantContext.current_tenant_id(), model_key)
            with self.db.connect() as con:
                current = self.assignments(con, company, workspace)
            if len(current) != 1:
                raise WritingConflict("请先明确唯一的章节作者。")
            runtime_ref = current[0]["data"]["employeeRef"]
            identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company, workspace_id=workspace, runtime_employee_ref=runtime_ref)
            employee_id = identity["company_employee_ref"]
            bindings = self.employees.list_employee_capability_bindings(employee_id)["bindings"]
            matches = [v for v in bindings if v["enabled"] and v["capability_type"] == "model"
                       and v["capability_source"] == model["source"] and v["capability_id"] == model_key]
            if not matches:
                bindings = self.employees.set_employee_capability_bindings(employee_id, [*bindings,
                    {"capability_source": model["source"], "capability_type": "model", "capability_id": model_key, "enabled": True, "priority": 1}])["bindings"]
                matches = [v for v in bindings if v["enabled"] and v["capability_type"] == "model"
                           and v["capability_source"] == model["source"] and v["capability_id"] == model_key]
            if len(matches) != 1:
                raise WritingConflict("当前模型没有唯一合法执行来源。")
            bridge = EmployeeExecutionIdentity(self.db).resolve(company_id=company, workspace_id=workspace, runtime_employee_ref=runtime_ref)
            if bridge["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE" or (bridge.get("bridge") or {}).get("status") != "VERIFIED":
                EmployeeExecutionIdentity(self.db).bind(company_id=company, workspace_id=workspace, runtime_employee_ref=runtime_ref,
                    company_employee_ref=employee_id, employee_capability_binding_ref=matches[0]["id"])
            self.conversations.events.record(correlation_id=workspace, event_type="writing.model.selected",
                payload={"model": model, "binding_id": matches[0]["id"], "employee_ref": runtime_ref,
                         "assignment_ref": current[0]["entity_id"], "assignment_revision": current[0]["data"]["revision"]},
                idempotency_key="writing-model:" + str(uuid.uuid4()))
        return self._configure(company, workspace, operation)

    def execution_policy(self, company, workspace, *, connection=None, attempt_id=None):
        try:
            self.actor(company, write=True)
            self.publication()
            def resolve(con):
                self.local._scope(con, company, workspace, write=True)
                config = self._configuration(con, workspace)
                if config and config["status"] != "COMPLETED":
                    raise WritingConflict("责任配置未完成。")
                assignment = self.assignments(con, company, workspace)
                selected = self._selected(con, workspace)
                if len(assignment) != 1 or not selected:
                    raise WritingConflict("请明确章节作者并从统一模型列表选择可用模型。")
                data = assignment[0]["data"]
                if (selected["employee_ref"], selected["assignment_ref"], selected["assignment_revision"]) != (data["employeeRef"], assignment[0]["entity_id"], data["revision"]):
                    raise WritingConflict("责任已变化，请核对当前模型选择。")
                model = self.models._require_eligible_model(TenantContext.current_tenant_id(), selected["model"]["model_key"])
                if model != selected["model"]:
                    raise WritingConflict("模型来源已变化，请重新选择。")
                identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company, workspace_id=workspace, runtime_employee_ref=data["employeeRef"])
                binding = con.execute("select * from employee_capability_bindings where tenant_id=? and employee_id=? and id=? and enabled=1 "
                    "and capability_type='model' and capability_source=? and capability_id=?",
                    (TenantContext.current_tenant_id(), identity["company_employee_ref"], selected["binding_id"], model["source"], model["model_key"])).fetchone()
                if not binding:
                    raise WritingConflict("当前模型绑定已失效。")
                identity = EmployeeExecutionIdentity(self.db).resolve(company_id=company, workspace_id=workspace, runtime_employee_ref=data["employeeRef"])
                if identity["identity_status"] != "VERIFIED_EXPLICIT_BRIDGE" or (identity.get("bridge") or {}).get("status") != "VERIFIED":
                    raise WritingConflict("员工执行身份未验证。")
                return selected, dict(binding)
            if connection is not None:
                selected, binding = resolve(connection)
            else:
                with self.db.connect() as con:
                    selected, binding = resolve(con)
            grant = self.models.professional_grant(self.execution_grant, company, workspace, selected["model"]["model_key"], attempt_id=attempt_id, connection=connection)
            if (not isinstance(grant, dict) or grant.get("tenant_id") != TenantContext.current_tenant_id()
                    or grant.get("company_id") != company or grant.get("workspace_id") != workspace
                    or grant.get("model_key") != selected["model"]["model_key"] or not grant.get("grant_ref")
                    or type(grant.get("max_output_tokens")) is not int or not 1 <= grant["max_output_tokens"] <= 2048
                    or type(grant.get("max_cost_usd")) not in {int, float} or not 0 < grant["max_cost_usd"]
                    or grant.get("effective_system_authorization") is not True):
                raise WritingConflict("本地编辑可继续；员工回复的费用与系统授权尚未批准。")
            with self.db.connect() as con:
                consumed = con.execute("select payload from evolution_events where tenant_id=? and event_type='conversation.execution_bound' "
                    "and json_extract(payload,'$.execution_selection.grant.grant_ref')=?",
                    (TenantContext.current_tenant_id(), grant["grant_ref"])).fetchall()
            if any(json.loads(row["payload"])["attempt_id"] != attempt_id for row in consumed):
                raise WritingConflict("这次单次员工回复授权已使用，请核验原请求；新请求需新的授权。")
            if (type(grant.get("max_input_bytes")) is not int or not 1 <= grant["max_input_bytes"] <= 50000
                    or not grant.get("price_version") or any(type(grant.get(k)) not in {int, float}
                        or not math.isfinite(grant[k]) or grant[k] < 0 for k in
                        ("price_upper_bound_usd_per_input_byte", "price_upper_bound_usd_per_output_token"))
                    or not math.isfinite(grant["max_cost_usd"])):
                raise WritingConflict("缺少明确的输入/输出费用上限来源。")
            return {"status": "AVAILABLE", "selected": selected, "binding": binding, "grant": dict(grant)}
        except (ValueError, KeyError, RuntimeScopeError, OSError) as error:
            return {"status": "UNAVAILABLE", "reason": str(error)}
