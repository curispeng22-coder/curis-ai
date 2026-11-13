"""Atomic First Run delivery over existing Company OS primitives."""

from __future__ import annotations

import hashlib
import json
import uuid
import threading
import weakref
from functools import wraps
from pathlib import Path
from dataclasses import dataclass, field
from typing import Any

from ..database import Database
from ..employee_templates import EmployeeTemplateContract, professional_team_contract
from .business_spine import BusinessSpineError, CanonicalBusinessSpine
from .foundation import RuntimeFoundation
from .registry import get_registered_machine


# Concurrent HTTP requests in this process must observe the committed receipt,
# rather than mistaking another service instance for an abandoned process.
_activation_locks = weakref.WeakValueDictionary()
_activation_locks_guard = threading.Lock()


def serialized_activation(method):
    @wraps(method)
    def invoke(self, founding_run_id, *args, **kwargs):
        key = (str(Path(self.db.path).resolve()), self.foundation.tenant_id, founding_run_id)
        with _activation_locks_guard:
            lock = _activation_locks.get(key)
            if lock is None:
                lock = threading.RLock()
                _activation_locks[key] = lock
        with lock:
            return method(self, founding_run_id, *args, **kwargs)
    return invoke


@dataclass(frozen=True)
class FirstGeneralWorkspaceDraft:
    company_id: str
    ceo_id: str
    company_name: str
    department_name: str
    business_name: str
    goal: str
    positioning: str
    workspace_name: str
    intent_summary: str = ""
    recommendation_reason: str = ""
    template_match_status: str = "NO_VERIFIED_MATCH"
    blueprint: dict[str, Any] = field(default_factory=dict)


class FirstRunDelivery:
    """Integration service; all persisted objects remain existing canonical types."""

    def __init__(self, database: Database):
        self.db = database
        self.foundation = RuntimeFoundation(database)
        self.businesses = CanonicalBusinessSpine(database)
        self.process_id = str(uuid.uuid4())

    @staticmethod
    def _ids(founding_run_id: str) -> dict[str, str]:
        suffix = hashlib.sha256(founding_run_id.encode("utf-8")).hexdigest()[:24]
        return {
            "department_id": f"department-first-{suffix}",
            "business_id": f"business-first-{suffix}",
            "workspace_id": f"workspace-first-{suffix}",
            "version_id": f"workspace-version-first-{suffix}",
        }

    @staticmethod
    def _clean(value: str, label: str) -> str:
        value = value.strip()
        if not value or any(ord(character) < 32 or ord(character) == 127 for character in value):
            raise BusinessSpineError(f"{label} is required")
        return value

    @staticmethod
    def _goal(value: str) -> str:
        value = value.strip()
        if not value or any((ord(c) < 32 and c != "\n") or ord(c) == 127 for c in value):
            raise BusinessSpineError("Goal is required")
        return value

    def materialize(self, founding_run_id: str, draft: FirstGeneralWorkspaceDraft) -> dict[str, Any]:
        if draft.template_match_status != "NO_VERIFIED_MATCH":
            raise BusinessSpineError("General fallback requires NO_VERIFIED_MATCH")
        ids = self._ids(founding_run_id)
        names = {
            "company": self._clean(draft.company_name, "Company name"),
            "department": self._clean(draft.department_name, "Department name"),
            "business": self._clean(draft.business_name, "Business name"),
            "workspace": self._clean(draft.workspace_name, "Workspace name"),
        }
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            assistant_id = self.foundation._materialize_company_in_connection(
                connection,
                founding_run_id,
                company_id=draft.company_id,
                ceo_id=draft.ceo_id,
                name=names["company"],
            )
            existing = connection.execute(
                "select department_id, name, goal, positioning from canonical_businesses "
                "where tenant_id=? and company_id=? and business_id=?",
                (self.foundation.tenant_id, draft.company_id, ids["business_id"]),
            ).fetchone()
            if existing is None:
                connection.execute(
                    "insert into department_instances("
                    "id, tenant_id, company_id, template_id, name, department_type, mission, status, "
                    "created_from_template_id, enabled_employee_template_ids_json, enabled, updated_at"
                    ") values (?, ?, ?, 'official.department.software_rnd', ?, 'business.general', ?, "
                    "'active', '', '[]', 1, current_timestamp)",
                    (
                        ids["department_id"], self.foundation.tenant_id, draft.company_id,
                        names["department"], draft.goal.strip(),
                    ),
                )
                self.businesses._create_draft_with_first_workspace(
                    connection,
                    company_id=draft.company_id,
                    department_id=ids["department_id"],
                    name=names["business"],
                    goal=draft.goal,
                    positioning=draft.positioning,
                    workspace_name=names["workspace"],
                    business_type="GENERIC",
                    blueprint_version="generic-v1",
                    blueprint={
                        **draft.blueprint,
                        "goal": draft.goal.strip(),
                        "intentSummary": draft.intent_summary.strip(),
                        "templateMatch": {
                            "status": draft.template_match_status,
                            "reason": draft.recommendation_reason.strip(),
                        },
                    },
                    business_id=ids["business_id"],
                    workspace_id=ids["workspace_id"],
                    version_id=ids["version_id"],
                )
                current = connection.execute(
                    "select data_json from runtime_entities where tenant_id=? and entity_id=?",
                    (self.foundation.tenant_id, founding_run_id),
                ).fetchone()
                data = json.loads(current["data_json"] or "{}")
                data["firstBusiness"] = {
                    **ids,
                    "templateMatchStatus": draft.template_match_status,
                }
                connection.execute(
                    "update runtime_entities set data_json=?, updated_at=current_timestamp "
                    "where tenant_id=? and entity_id=?",
                    (json.dumps(data, ensure_ascii=False), self.foundation.tenant_id, founding_run_id),
                )
            else:
                workspace = connection.execute(
                    "select name from workspaces where tenant_id=? and company_id=? and business_id=? and workspace_id=?",
                    (self.foundation.tenant_id, draft.company_id, ids["business_id"], ids["workspace_id"]),
                ).fetchone()
                if (
                    existing["department_id"] != ids["department_id"]
                    or existing["name"] != names["business"]
                    or existing["goal"] != draft.goal.strip()
                    or existing["positioning"] != draft.positioning.strip()
                    or workspace is None
                    or workspace["name"] != names["workspace"]
                ):
                    raise BusinessSpineError("FoundingRun was materialized with another first business request")

        return {
            "founding_run": self.foundation.get(founding_run_id),
            "assistant": self.foundation.get(assistant_id),
            "business": self.businesses.get_business(draft.company_id, ids["business_id"]),
            "parent": self.businesses.resolve_workspace_parent(ids["workspace_id"]),
            "creation_result": {
                **ids,
                "company_id": draft.company_id,
                "assistant_id": assistant_id,
                "template_match": {
                    "status": draft.template_match_status,
                    "reason": draft.recommendation_reason.strip(),
                },
                "next_action": "OPEN_FIRST_WORKSPACE",
            },
        }

    def materialize_for_existing_company(
        self, founding_run_id: str, draft: FirstGeneralWorkspaceDraft,
    ) -> dict[str, Any]:
        """Materialize a first/additional General Business after Company creation.

        The FoundingRun remains the idempotency boundary; the canonical Business and
        first Workspace are still written by ``CanonicalBusinessSpine`` in one DB
        transaction. No professional match is inferred here.
        """

        if draft.template_match_status != "NO_VERIFIED_MATCH":
            raise BusinessSpineError("General fallback requires NO_VERIFIED_MATCH")
        ids = self._ids(founding_run_id)
        names = {
            "department": self._clean(draft.department_name, "Department name"),
            "business": self._clean(draft.business_name, "Business name"),
            "workspace": self._clean(draft.workspace_name, "Workspace name"),
        }
        tenant_id = self.foundation.tenant_id
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            company = connection.execute(
                "select company_id, ceo_id from companies where tenant_id=? and company_id=?",
                (tenant_id, draft.company_id),
            ).fetchone()
            if company is None or company["ceo_id"] != draft.ceo_id:
                raise BusinessSpineError("Company is not owned by the current CEO")
            assistant = connection.execute(
                "select entity_id from runtime_entities where tenant_id=? and company_id=? "
                "and entity_type='CEO_ASSISTANT' order by created_at limit 1",
                (tenant_id, draft.company_id),
            ).fetchone()
            if assistant is None:
                raise BusinessSpineError("Company Assistant identity is missing")
            run = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=? and entity_type='FOUNDING_RUN'",
                (tenant_id, founding_run_id),
            ).fetchone()
            if run is None or run["owner_ref"] != draft.ceo_id:
                raise BusinessSpineError("FoundingRun is not owned by the current CEO")
            data = json.loads(run["data_json"] or "{}")
            if run["lifecycle_status"] == "COMPANY_CREATED":
                recorded = data.get("firstBusiness") or {}
                if recorded.get("business_id") != ids["business_id"] or run["company_id"] != draft.company_id:
                    raise BusinessSpineError("FoundingRun was materialized with another request")
                existing_business = connection.execute(
                    "select name, goal, positioning from canonical_businesses where tenant_id=? and company_id=? and business_id=?",
                    (tenant_id, draft.company_id, ids["business_id"]),
                ).fetchone()
                existing_workspace = connection.execute(
                    "select name from workspaces where tenant_id=? and company_id=? and workspace_id=?",
                    (tenant_id, draft.company_id, ids["workspace_id"]),
                ).fetchone()
                if (
                    existing_business is None or existing_workspace is None
                    or existing_business["name"] != names["business"]
                    or existing_business["goal"] != draft.goal.strip()
                    or existing_business["positioning"] != draft.positioning.strip()
                    or existing_workspace["name"] != names["workspace"]
                ):
                    raise BusinessSpineError("FoundingRun was materialized with another request")
            elif run["lifecycle_status"] != "CEO_CONFIRMED":
                raise BusinessSpineError("FoundingRun is not confirmed")
            else:
                department = connection.execute(
                    "select id from department_instances where tenant_id=? and company_id=? and id=? and deleted_at is null",
                    (tenant_id, draft.company_id, ids["department_id"]),
                ).fetchone()
                if department is None:
                    connection.execute(
                        "insert into department_instances("
                        "id, tenant_id, company_id, template_id, name, department_type, mission, status, "
                        "created_from_template_id, enabled_employee_template_ids_json, enabled, updated_at"
                        ") values (?, ?, ?, 'official.department.software_rnd', ?, 'business.general', ?, "
                        "'active', '', '[]', 1, current_timestamp)",
                        (ids["department_id"], tenant_id, draft.company_id, names["department"], draft.goal.strip()),
                    )
                self.businesses._create_draft_with_first_workspace(
                    connection,
                    company_id=draft.company_id,
                    department_id=ids["department_id"],
                    name=names["business"],
                    goal=draft.goal,
                    positioning=draft.positioning,
                    workspace_name=names["workspace"],
                    business_type="GENERIC",
                    blueprint_version="generic-v1",
                    blueprint={
                        **draft.blueprint,
                        "goal": draft.goal.strip(),
                        "intentSummary": draft.intent_summary.strip(),
                        "templateMatch": {
                            "status": draft.template_match_status,
                            "reason": draft.recommendation_reason.strip(),
                        },
                    },
                    business_id=ids["business_id"],
                    workspace_id=ids["workspace_id"],
                    version_id=ids["version_id"],
                )
                transition = get_registered_machine("founding_run").transition(
                    founding_run_id, "CEO_CONFIRMED", "COMPANY_CREATED", actor="SYSTEM",
                    trigger="persist_company", context={"companyId": draft.company_id}, record=False,
                )
                data["firstBusiness"] = {**ids, "templateMatchStatus": draft.template_match_status}
                connection.execute(
                    "update runtime_entities set company_id=?, parent_id=?, lifecycle_status='COMPANY_CREATED', "
                    "data_json=?, updated_at=? where tenant_id=? and entity_id=? and lifecycle_status='CEO_CONFIRMED'",
                    (draft.company_id, assistant["entity_id"], json.dumps(data, ensure_ascii=False), transition.at,
                     tenant_id, founding_run_id),
                )
                connection.execute(
                    "insert into runtime_transition_log(tenant_id, entity_type, entity_id, source, target, trigger, "
                    "actor, at, company_id, context_json) values (?, 'founding_run', ?, ?, ?, ?, ?, ?, ?, ?)",
                    (tenant_id, founding_run_id, transition.source, transition.target, transition.trigger,
                     transition.actor, transition.at, draft.company_id, json.dumps(transition.context)),
                )

        return {
            "founding_run": self.foundation.get(founding_run_id),
            "assistant": self.foundation.get(assistant["entity_id"]),
            "business": self.businesses.get_business(draft.company_id, ids["business_id"]),
            "parent": self.businesses.resolve_workspace_parent(ids["workspace_id"]),
            "creation_result": {
                **ids,
                "company_id": draft.company_id,
                "assistant_id": assistant["entity_id"],
                "template_match": {
                    "status": draft.template_match_status,
                    "reason": draft.recommendation_reason.strip(),
                },
                "next_action": "OPEN_FIRST_WORKSPACE",
            },
        }

    def package_creation_status(self, founding_run_id, company_id, ceo_id):
        run = self.foundation.get(founding_run_id)
        if run["owner_ref"] != ceo_id or run.get("company_id") not in (None, company_id):
            raise BusinessSpineError("FoundingRun is outside the current CEO Company")
        activation = dict(run["data"].get("v1Activation") or {})
        if activation.get("company_id") not in (None, company_id):
            raise BusinessSpineError("Confirmation belongs to another Company")
        if activation.get("status") == "RUNNING" and activation.get("process_id") != self.process_id:
            activation["status"] = "UNKNOWN"
        result = {"founding_run": run, "activation": activation}
        if run["lifecycle_status"] == "COMPANY_CREATED" and activation.get("status") == "COMPLETED":
            ids = run["data"]["firstBusiness"]
            result.update(business=self.businesses.get_business(company_id, ids["business_id"]),
                creation_result={**ids, "company_id": company_id, "next_action": "OPEN_FIRST_WORKSPACE",
                                 "workspace": {"workspace_id": ids["workspace_id"], "business_type": "PACKAGE"}})
            if "initialTeam" in run["data"]:
                result["creation_result"]["initial_team"] = run["data"]["initialTeam"]
        return result

    @serialized_activation
    def materialize_package_for_existing_company(self, founding_run_id, draft, *, package_runtime,
                                                source, definition, department_id, proposal_sha256, retry_no=0):
        """Persist the original confirmed proposal and Package instance in the same canonical transaction."""
        from ..tenant_context import TenantContext
        tenant = TenantContext.current_tenant_id()
        ids = self._ids(founding_run_id)
        snapshot = {"intent": draft.intent_summary.strip(), "business_name": self._clean(draft.business_name, "Business name"),
                    "goal": self._goal(draft.goal), "positioning": draft.positioning.strip(),
                    "workspace_name": self._clean(draft.workspace_name, "Workspace name"),
                    "company_id": draft.company_id, "department_id": department_id,
                    "package_id": definition["package_id"], "definition": definition}
        def check(connection, run):
            company = connection.execute("select ceo_id from companies where tenant_id=? and company_id=?",
                (tenant, draft.company_id)).fetchone()
            if not company or company["ceo_id"] != draft.ceo_id or run["owner_ref"] != draft.ceo_id:
                raise BusinessSpineError("Only the Company CEO can confirm this proposal")
            data = json.loads(run["data_json"] or "{}")
            proposal = data.get("v1Proposal") or {}
            if proposal.get("snapshot") != snapshot or proposal.get("proposal_sha256") != proposal_sha256:
                raise BusinessSpineError("The original confirmed proposal changed; retain it and query its result")
            return data
        with self.db.connect() as con:
            con.execute("begin immediate")
            run = con.execute("select * from runtime_entities where tenant_id=? and entity_id=? and entity_type='FOUNDING_RUN'",
                (tenant, founding_run_id)).fetchone()
            if not run:
                raise BusinessSpineError("FoundingRun does not exist")
            data = check(con, run)
            activation = data.get("v1Activation") or {}
            if run["lifecycle_status"] == "COMPANY_CREATED" or activation.get("status") == "RUNNING":
                return self.package_creation_status(founding_run_id, draft.company_id, draft.ceo_id)
            if run["lifecycle_status"] != "CEO_CONFIRMED":
                raise BusinessSpineError("The original proposal requires explicit CEO confirmation")
            team_contract = professional_team_contract(definition["package_id"], definition["version"], definition["digest"])
            if team_contract is not None and definition.get("initial_team_contract") != team_contract:
                raise BusinessSpineError("Initial team contract requires its original CEO-confirmed proposal")
            if retry_no not in (0, 1):
                raise BusinessSpineError("Only one explicit failed-confirmation retry is allowed")
            if activation and not (activation.get("status") == "FAILED" and retry_no == 1 and activation.get("retry_no") == 0):
                return self.package_creation_status(founding_run_id, draft.company_id, draft.ceo_id)
            activation = {"company_id": draft.company_id, "status": "RUNNING", "process_id": self.process_id,
                          "retry_no": retry_no, "snapshot": snapshot, "proposal_sha256": proposal_sha256}
            data["v1Activation"] = activation
            con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?",
                (json.dumps(data, ensure_ascii=False), tenant, founding_run_id))
        try:
            package, target = package_runtime.prepare_confirmed_assets(source)
            if package["digest"] != definition["digest"]:
                raise BusinessSpineError("The approved immutable Package changed")
            with self.db.connect() as con:
                con.execute("begin immediate")
                run = con.execute("select * from runtime_entities where tenant_id=? and entity_id=?", (tenant, founding_run_id)).fetchone()
                data = check(con, run)
                if run["lifecycle_status"] != "CEO_CONFIRMED" or data.get("v1Activation") != activation:
                    raise BusinessSpineError("Confirmation changed while preparing its immutable assets")
                assistant = con.execute("select entity_id from runtime_entities where tenant_id=? and company_id=? and entity_type='CEO_ASSISTANT'",
                    (tenant, draft.company_id)).fetchall()
                if len(assistant) != 1:
                    raise BusinessSpineError("Company requires its existing unique Assistant")
                package_runtime.install_confirmed_in_connection(con, package, target, draft.company_id,
                    department_id=department_id, business_id=ids["business_id"], business_name=draft.business_name,
                    business_goal=draft.goal, business_positioning=draft.positioning, workspace_id=ids["workspace_id"],
                    workspace_name=draft.workspace_name)
                if team_contract is not None:
                    team = EmployeeTemplateContract(self.db).materialize_professional_team_in_connection(
                        con, company_id=draft.company_id, business_id=ids["business_id"],
                        workspace_id=ids["workspace_id"], contract=team_contract)
                    writing = team_contract["departmentType"] == "writing"
                    members = team_contract.get("members") or [
                        {"templateId": team_contract["templateId"], "responsibilityKey": team_contract["leaderKey"]},
                        {"templateId": team_contract["templateId"], "responsibilityKey": team_contract["authorKey"]}]
                    refs = ([team.get("leaderRef"), team.get("employeeRef"), team.get("reviewerRef")]
                            if writing else [team.get("employeeRef"), team.get("employeeRef")])
                    if (not all(refs) or len(set(refs)) != (3 if writing else 1)
                            or team.get("leaderRef") != refs[0]
                            or team.get("templateRef") != team_contract["templateId"]
                            or team.get("contractSHA256") != team_contract["sha256"]
                            or len(team.get("assignments", [])) != len(members)):
                        raise BusinessSpineError("Initial team receipt is not fully materialized")
                    for index, (reference, member, employee_ref) in enumerate(zip(team["assignments"], members, refs)):
                        holder = con.execute("select id from employee_instances where tenant_id=? and company_id=? and id=? "
                            "and template_id=? and enabled=1 and deleted_at is null",
                            (tenant, draft.company_id, employee_ref, member["templateId"])).fetchone()
                        row = con.execute("select data_json from runtime_entities where tenant_id=? and company_id=? "
                            "and entity_id=? and entity_type='RESPONSIBILITY_ASSIGNMENT' and lifecycle_status='ACTIVE'",
                            (tenant, draft.company_id, reference["assignmentRef"])).fetchone()
                        assignment = json.loads(row["data_json"]) if row else {}
                        if (holder is None or assignment.get("employeeRef") != employee_ref or assignment.get("roleRef") != reference["roleRef"]
                                or assignment.get("scopeType") != ("BUSINESS" if index == 0 else "WORKSPACE")
                                or assignment.get("scopeRef") != ids["business_id" if index == 0 else "workspace_id"]
                                or assignment.get("isLeader") is not (index == 0)
                                or assignment.get("responsibilityKey") != member["responsibilityKey"]):
                            raise BusinessSpineError("Initial team receipt conflicts with its scoped responsibilities")
                    data["initialTeam"] = team
                data["firstBusiness"] = {**ids, "department_id": department_id}
                data["v1Activation"] = {**activation, "status": "COMPLETED"}
                transition = get_registered_machine("founding_run").transition(founding_run_id, "CEO_CONFIRMED", "COMPANY_CREATED",
                    trigger="persist_company", actor="SYSTEM", context={"companyId": draft.company_id, "assistantId": assistant[0]["entity_id"]}, record=False)
                con.execute("update runtime_entities set company_id=?,parent_id=?,lifecycle_status='COMPANY_CREATED',data_json=?,updated_at=? "
                    "where tenant_id=? and entity_id=?", (draft.company_id, assistant[0]["entity_id"], json.dumps(data, ensure_ascii=False),
                    transition.at, tenant, founding_run_id))
                con.execute("insert into runtime_transition_log(tenant_id,entity_type,entity_id,source,target,trigger,actor,at,company_id,context_json) "
                    "values (?,'founding_run',?,?,?,?,?,?,?,?)", (tenant, founding_run_id, transition.source, transition.target,
                    transition.trigger, transition.actor, transition.at, draft.company_id, json.dumps(transition.context)))
        except Exception as error:
            # Local files can be retained unreferenced. A committed Business is never relabeled as failure.
            with self.db.connect() as con:
                con.execute("begin immediate")
                row = con.execute("select lifecycle_status,data_json from runtime_entities where tenant_id=? and entity_id=?", (tenant, founding_run_id)).fetchone()
                if row and row["lifecycle_status"] == "CEO_CONFIRMED":
                    data = json.loads(row["data_json"])
                    if data.get("v1Activation") == activation:
                        data["v1Activation"] = {**activation, "status": "FAILED", "reason": str(error)[:300]}
                        con.execute("update runtime_entities set data_json=? where tenant_id=? and entity_id=?", (json.dumps(data, ensure_ascii=False), tenant, founding_run_id))
            return self.package_creation_status(founding_run_id, draft.company_id, draft.ceo_id)
        return self.package_creation_status(founding_run_id, draft.company_id, draft.ceo_id)
