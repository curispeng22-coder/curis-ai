"""Three-business Workspace Runtime foundation."""

from __future__ import annotations

import json
import re
from datetime import datetime, timedelta, timezone
from uuid import uuid4

from ..catalog_constants import effect_class_for_capability
from ..database import Database
from ..tenant_context import TenantContext
from .foundation import RuntimeFoundation, RuntimeScopeError
from .registry import get_registered_machine
from .simulation import INVALIDATING_CHANGES, SimulationRuntime
from .state_machine import TransitionError


BUSINESS_TYPES = frozenset({"RD", "XHS", "TTK"})
RD_STAGES = ("INTAKE", "DESIGN", "IMPLEMENT", "VERIFY", "ACCEPT", "REVIEW", "IMPROVE", "ARCHIVE")
CONTENT_STAGES = ("INTAKE", "PRODUCE", "DELIVER", "COLLECT", "ACCEPT", "REVIEW", "IMPROVE", "ARCHIVE")
XHS_CONTENT_LIFECYCLE = ("IDEA", "DRAFT", "IN_REVIEW", "APPROVED", "SCHEDULED", "PUBLISHED", "AWAITING_FEEDBACK", "REVIEWED")
RECEIPT_SOURCES = frozenset({"PLATFORM_API", "CEO_MANUAL"})
REQUIREMENT_REF = re.compile(r"^requirement:[a-z0-9][a-z0-9-]{1,63}$")


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _staffing_proposal(blueprint: dict) -> tuple[list[dict], list[dict]] | None:
    if blueprint.get("lifecycleMode") != "STUDIO_DRAFT":
        return None
    roles = blueprint.get("roleSlots")
    capabilities = blueprint.get("capabilityBindings")
    if not isinstance(roles, list) or not roles or not isinstance(capabilities, list) or not capabilities:
        raise ValueError("Studio Blueprint requires roleSlots and capabilityBindings")

    capability_refs: set[str] = set()
    for capability in capabilities:
        if not isinstance(capability, dict):
            raise ValueError("Capability requirement must be an object")
        ref = str(capability.get("capabilityRef") or "")
        name = str(capability.get("capability") or "").strip()
        if not REQUIREMENT_REF.fullmatch(ref) or not name:
            raise ValueError("Capability requirement needs a stable requirement ref and name")
        if capability.get("bindingStatus") != "REQUIRED_NOT_AUTHORIZED" or ref in capability_refs:
            raise ValueError("Capability requirement must be unique and remain unauthorized")
        capability_refs.add(ref)

    role_names: set[str] = set()
    for role in roles:
        if not isinstance(role, dict):
            raise ValueError("Role Slot must be an object")
        name = str(role.get("role") or "").strip()
        responsibility = str(role.get("responsibility") or "").strip()
        refs = role.get("capabilityRefs")
        if not name or not responsibility or not isinstance(refs, list) or not refs:
            raise ValueError("Role Slot requires role, responsibility and capabilityRefs")
        if role.get("staffingStatus") != "PLANNED_NOT_MATERIALIZED" or name in role_names:
            raise ValueError("Role Slot must be unique and remain unmaterialized")
        if any(ref not in capability_refs for ref in refs):
            raise ValueError("Role Slot references an unknown capability requirement")
        role_names.add(name)
    return roles, capabilities


class WorkspaceRuntime:
    def __init__(self, database: Database):
        self.db = database
        self.foundation = RuntimeFoundation(database)
        self.simulations = SimulationRuntime(database)

    @property
    def tenant_id(self) -> str:
        return self.foundation.tenant_id

    def create_workspace(
        self,
        *,
        company_id: str,
        business_ref: str,
        business_type: str,
        name: str,
        blueprint_version: str,
        blueprint: dict,
    ) -> dict:
        self.foundation._require_company(company_id)
        kind = self._business_type(business_type)
        name = name.strip()
        if not name or any(ord(character) < 32 or ord(character) == 127 for character in name):
            raise ValueError("workspace name is required")
        snapshot = self._blueprint(kind, blueprint)
        staffing = _staffing_proposal(snapshot)
        workspace_id = f"workspace-{uuid4()}"
        version_id = f"workspace-version-{uuid4()}"
        org_version = f"org-{workspace_id}-{blueprint_version}"
        at = _now()
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            business = conn.execute(
                "select 1 from canonical_businesses where tenant_id=? and company_id=? and business_id=? "
                "and lifecycle_status != 'ARCHIVED'",
                (self.tenant_id, company_id, business_ref),
            ).fetchone()
            if business is None:
                raise ValueError("Workspace requires a canonical Business in the current Company")
            conn.execute(
                """
                insert into workspaces(
                  workspace_id, tenant_id, company_id, business_id, name,
                  blueprint_json, blueprint_version, operating_version, status,
                  simulation_passed, business_relation_status, business_relation_reason,
                  business_relation_owner, business_relation_source, business_relation_checked_at,
                  created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, 0, 'DRAFT', 0, 'RESOLVED', '',
                  'Workspace Runtime', 'CANONICAL', ?, ?, ?)
                """,
                (workspace_id, self.tenant_id, company_id, business_ref, name,
                 json.dumps(snapshot, ensure_ascii=False), blueprint_version, at, at, at),
            )
            conn.execute(
                """
                insert into runtime_workspace_versions(
                  version_id, tenant_id, company_id, workspace_id, blueprint_version,
                  status, simulation_passed, operating_version, change_kind, data_json,
                  created_at, updated_at
                ) values (?, ?, ?, ?, ?, 'DRAFT', 0, 0, 'BLUEPRINT', ?, ?, ?)
                """,
                (version_id, self.tenant_id, company_id, workspace_id, blueprint_version,
                 json.dumps({"blueprint": snapshot, "changeReason": "initial"}, ensure_ascii=False), at, at),
            )
            if staffing:
                assistant = conn.execute(
                    "select entity_id from runtime_entities where tenant_id = ? and company_id = ? "
                    "and entity_type = 'CEO_ASSISTANT'",
                    (self.tenant_id, company_id),
                ).fetchone()
                if assistant is None:
                    raise ValueError("Studio staffing proposal requires a Company CEO Assistant")
                assistant_id = assistant["entity_id"]
                roles, capabilities = staffing

                def insert_entity(
                    entity_type: str,
                    status: str,
                    data: dict,
                    *,
                    parent_id: str | None = None,
                    capability_ref: str | None = None,
                ) -> str:
                    entity_id = f"{entity_type.lower()}-{uuid4()}"
                    conn.execute(
                        """
                        insert into runtime_entities(
                          entity_id, tenant_id, entity_type, company_id, workspace_id,
                          parent_id, owner_ref, lifecycle_status, org_version, blueprint_version,
                          capability_ref, verification_status, evidence_condition, data_json,
                          created_at, updated_at
                        ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'UNVERIFIED', 'MISSING', ?, ?, ?)
                        """,
                        (entity_id, self.tenant_id, entity_type, company_id, workspace_id,
                         parent_id, assistant_id, status, org_version, blueprint_version,
                         capability_ref, json.dumps(data, ensure_ascii=False), at, at),
                    )
                    return entity_id

                def link(source_id: str, relation: str, target_id: str) -> None:
                    conn.execute(
                        "insert into runtime_links(link_id, tenant_id, company_id, workspace_id, "
                        "source_id, relation, target_id, created_at) values (?, ?, ?, ?, ?, ?, ?, ?)",
                        (f"link-{uuid4()}", self.tenant_id, company_id, workspace_id,
                         source_id, relation, target_id, at),
                    )

                binding_ids: dict[str, str] = {}
                for capability in capabilities:
                    ref = capability["capabilityRef"]
                    binding_ids[ref] = insert_entity(
                        "CAPABILITY_BINDING",
                        "PROPOSED",
                        {
                            "name": capability["capability"],
                            "requirementRef": ref,
                            "authorizationStatus": "PROPOSED_NOT_AUTHORIZED",
                        },
                        capability_ref=ref,
                    )

                for role in roles:
                    role_id = insert_entity(
                        "ROLE_SLOT",
                        "DRAFT",
                        {
                            "name": role["role"],
                            "responsibility": role["responsibility"],
                            "capabilityRefs": role["capabilityRefs"],
                            "reportingTo": assistant_id,
                            "staffingStatus": "DRAFT_NOT_ASSIGNED",
                        },
                        parent_id=assistant_id,
                    )
                    employee_id = insert_entity(
                        "AI_EMPLOYEE",
                        "PROPOSED",
                        {
                            "name": role["role"],
                            "roleSlotRef": role_id,
                            "responsibility": role["responsibility"],
                            "reportingTo": assistant_id,
                            "staffingStatus": "PROPOSED_NOT_HIRED",
                        },
                        parent_id=assistant_id,
                    )
                    link(role_id, "REPORTS_TO", assistant_id)
                    link(employee_id, "REPORTS_TO", assistant_id)
                    link(employee_id, "PROPOSED_FOR", role_id)
                    for ref in role["capabilityRefs"]:
                        link(role_id, "REQUIRES_CAPABILITY", binding_ids[ref])
        return self.get_workspace(company_id, workspace_id)

    def revise_blueprint(
        self,
        *,
        company_id: str,
        workspace_id: str,
        blueprint_version: str,
        blueprint: dict,
        change_kind: str,
        change_reason: str,
    ) -> dict:
        current = self.get_workspace(company_id, workspace_id)
        if current["workspace"]["blueprint_version"] == blueprint_version:
            raise ValueError("blueprint revision requires a new version")
        if any(item["blueprint_version"] == blueprint_version for item in current["versions"]):
            raise ValueError("historical blueprint versions are immutable and cannot be reused")
        kind = current["workspace"]["business_type"]
        snapshot = self._blueprint(kind, blueprint)
        self.simulations.invalidate_workspace(
            workspace_id,
            blueprint_version=blueprint_version,
            change_kind=change_kind,
            blueprint=snapshot,
            change_reason=change_reason,
        )
        return self.get_workspace(company_id, workspace_id)

    def get_workspace(self, company_id: str, workspace_id: str) -> dict:
        self.foundation._require_workspace(workspace_id, company_id)
        with self.db.connect() as conn:
            row = conn.execute(
                "select * from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                (self.tenant_id, company_id, workspace_id),
            ).fetchone()
            versions = conn.execute(
                "select * from runtime_workspace_versions where tenant_id = ? and company_id = ? "
                "and workspace_id = ? order by rowid",
                (self.tenant_id, company_id, workspace_id),
            ).fetchall()
        if row is None:
            raise RuntimeScopeError("workspace does not belong to current company")
        workspace = dict(row)
        workspace["blueprint"] = json.loads(workspace.pop("blueprint_json"))
        workspace["business_type"] = workspace["blueprint"]["businessType"]
        version_items = []
        for version in versions:
            item = dict(version)
            item["data"] = json.loads(item.pop("data_json"))
            version_items.append(item)
        entities = {
            kind: self.foundation.list(kind, company_id=company_id, workspace_id=workspace_id)
            for kind in (
                "AI_EMPLOYEE", "ROLE_SLOT", "CAPABILITY_BINDING",
                "CYCLE", "CONTENT_ITEM", "CONTENT_VERSION", "PUBLICATION_RECEIPT",
                "INTERACTION_ITEM", "OUTCOME", "EVIDENCE", "HANDOFF", "ACCEPTANCE",
                "DECISION_PACKET",
            )
        }
        return {
            "workspace": workspace,
            "versions": version_items,
            "entities": entities,
            "simulations": self.simulations.list(company_id=company_id, workspace_id=workspace_id),
        }

    def get_capability_supply_review(self, company_id: str, workspace_id: str) -> dict:
        self.foundation._require_workspace(workspace_id, company_id)
        with self.db.connect() as conn:
            context = self._supply_context(conn, company_id, workspace_id)
            catalog = self._supply_catalog(conn)
            requirements = []
            for binding in context["bindings"]:
                data = binding["data"]
                persisted = data.get("supplyReview")
                current = None
                blockers = ["SUPPLY_NOT_SELECTED"]
                stale = False
                if isinstance(persisted, dict):
                    supply = self._resolve_supply(
                        conn,
                        persisted.get("source"),
                        persisted.get("capabilityType"),
                        persisted.get("capabilityId"),
                    )
                    if supply:
                        current = self._assess_supply(conn, supply)
                        stale = persisted.get("catalogUpdatedAt") != current["catalogUpdatedAt"]
                        blockers = list(current["blockers"])
                        if stale:
                            blockers.append("SUPPLY_CHANGED_REVIEW_REQUIRED")
                    else:
                        blockers = ["SUPPLY_UNAVAILABLE_OR_CHANGED"]
                requirements.append({
                    "bindingId": binding["entity_id"],
                    "requirementRef": data.get("requirementRef"),
                    "name": data.get("name"),
                    "lifecycleStatus": binding["lifecycle_status"],
                    "authorizationStatus": data.get("authorizationStatus"),
                    "selection": persisted,
                    "currentReview": current,
                    "stale": stale,
                    "blockers": sorted(set(blockers)),
                })
        blockers = sorted({
            blocker
            for requirement in requirements
            for blocker in requirement["blockers"]
        })
        resource_check_passed = bool(requirements) and not blockers
        return {
            "workspaceId": workspace_id,
            "companyId": company_id,
            "blueprintVersion": context["blueprint_version"],
            "orgVersion": context["org_version"],
            "orgSimulationId": context["simulation_id"],
            "requirements": requirements,
            "catalog": catalog,
            "reviewComplete": bool(requirements) and all(item["selection"] for item in requirements),
            "resourceCheckPassed": resource_check_passed,
            "readyForApproval": resource_check_passed,
            "activationReady": False,
            "blockers": blockers,
        }

    def review_capability_supply(
        self,
        *,
        company_id: str,
        workspace_id: str,
        selections: list[dict],
    ) -> dict:
        self.foundation._require_workspace(workspace_id, company_id)
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._supply_context(conn, company_id, workspace_id)
            expected = {item["data"]["requirementRef"] for item in context["bindings"]}
            supplied = [str(item.get("requirementRef") or "") for item in selections]
            if set(supplied) != expected or len(supplied) != len(expected):
                raise ValueError("capability supply selections must cover each requirement exactly once")
            by_requirement = {item["requirementRef"]: item for item in selections}
            at = _now()
            for binding in context["bindings"]:
                data = binding["data"]
                selection = by_requirement[data["requirementRef"]]
                supply = self._resolve_supply(
                    conn,
                    selection.get("source"),
                    selection.get("capabilityType"),
                    selection.get("capabilityId"),
                )
                if supply is None:
                    raise ValueError("selected capability supply is not active in the current Company catalog")
                review = self._assess_supply(conn, supply)
                previous = data.get("supplyReview") if isinstance(data.get("supplyReview"), dict) else {}
                same_selection = all(previous.get(key) == review.get(key) for key in (
                    "source", "capabilityType", "capabilityId", "catalogUpdatedAt",
                ))
                data["supplyReview"] = {
                    **review,
                    "reviewedBy": "CEO",
                    "reviewedAt": previous.get("reviewedAt") if same_selection else at,
                }
                cursor = conn.execute(
                    "update runtime_entities set data_json = ?, updated_at = ? "
                    "where tenant_id = ? and company_id = ? and workspace_id = ? "
                    "and entity_id = ? and entity_type = 'CAPABILITY_BINDING' "
                    "and lifecycle_status = 'PROPOSED' and org_version = ? and blueprint_version = ?",
                    (
                        json.dumps(data, ensure_ascii=False), at, self.tenant_id, company_id,
                        workspace_id, binding["entity_id"], context["org_version"],
                        context["blueprint_version"],
                    ),
                )
                if cursor.rowcount != 1:
                    raise RuntimeError("capability proposal changed concurrently; retry from current state")
        return self.get_capability_supply_review(company_id, workspace_id)

    def get_staffing_approval(self, company_id: str, workspace_id: str) -> dict:
        self.foundation._require_workspace(workspace_id, company_id)
        with self.db.connect() as conn:
            workspace, version = self._workspace_version(conn, company_id, workspace_id)
            decision = version["data"].get("staffingDecision")
            entities = self._staffing_entities(conn, company_id, workspace_id)
            activation_ready = False
            rollback_ready = False
            blockers: list[str] = []
            if not decision and workspace["status"] == "DRAFT":
                try:
                    self._activation_context(conn, company_id, workspace_id)
                    activation_ready = True
                except ValueError as error:
                    blockers = [str(error)]
            if (
                isinstance(decision, dict)
                and decision.get("state") == "APPLIED"
                and workspace["status"] == "OPERATING"
            ):
                try:
                    rollback_ready = datetime.now(timezone.utc) <= datetime.fromisoformat(decision["rollbackUntil"])
                except (KeyError, TypeError, ValueError):
                    blockers = ["staffing decision has no valid rollback window"]
        return {
            "workspaceId": workspace_id,
            "companyId": company_id,
            "blueprintVersion": workspace["blueprint_version"],
            "operatingVersion": workspace["operating_version"],
            "workspaceStatus": workspace["status"],
            "orgVersion": self._one_org_version(entities),
            "decision": decision if isinstance(decision, dict) else None,
            "activationReady": activation_ready,
            "rollbackReady": rollback_ready,
            "roleSlotStatuses": sorted(item["lifecycle_status"] for item in entities["ROLE_SLOT"]),
            "employeeStatuses": sorted(item["lifecycle_status"] for item in entities["AI_EMPLOYEE"]),
            "bindingStatuses": sorted(item["lifecycle_status"] for item in entities["CAPABILITY_BINDING"]),
            "blockers": blockers,
        }

    def decide_staffing(
        self,
        *,
        company_id: str,
        workspace_id: str,
        choice: str,
        reason: str,
    ) -> dict:
        decision_choice = choice.upper()
        if decision_choice not in {"APPROVE", "MODIFY", "REJECT"}:
            raise ValueError("staffing decision must be APPROVE, MODIFY, or REJECT")
        reason = reason.strip()
        if decision_choice != "APPROVE" and not reason:
            raise ValueError("modify or reject requires a reason")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            workspace, version = self._workspace_version(conn, company_id, workspace_id)
            previous = version["data"].get("staffingDecision")
            if isinstance(previous, dict):
                if previous.get("choice") == decision_choice and previous.get("state") in {"APPLIED", "RECORDED"}:
                    return self.get_staffing_approval(company_id, workspace_id)
                raise TransitionError("staffing proposal already has a current CEO decision")
            context = self._activation_context(conn, company_id, workspace_id)
            at = _now()
            decision = {
                "decisionId": f"decision-{uuid4()}",
                "choice": decision_choice,
                "reason": reason,
                "decidedBy": "CEO",
                "decidedAt": at,
                "blueprintVersion": context["blueprint_version"],
                "orgVersion": context["org_version"],
                "simulationId": context["simulation_id"],
            }
            if decision_choice == "APPROVE":
                operating_version = int(workspace["operating_version"] or 0) + 1
                rollback_until = (datetime.fromisoformat(at) + timedelta(days=14)).isoformat(timespec="seconds")
                decision.update({
                    "state": "APPLIED",
                    "operatingVersion": operating_version,
                    "rollbackUntil": rollback_until,
                })
                self._activate_staffing(conn, workspace, version, context, decision, at)
            else:
                decision["state"] = "RECORDED"
                version["data"]["staffingDecision"] = decision
                conn.execute(
                    "update runtime_workspace_versions set status = ?, data_json = ?, updated_at = ? "
                    "where tenant_id = ? and company_id = ? and workspace_id = ? and blueprint_version = ?",
                    (
                        "CHANGES_REQUESTED" if decision_choice == "MODIFY" else "REJECTED_DRAFT",
                        json.dumps(version["data"], ensure_ascii=False), at, self.tenant_id,
                        company_id, workspace_id, workspace["blueprint_version"],
                    ),
                )
                conn.execute(
                    "update workspaces set status = 'BLUEPRINTING', updated_at = ? "
                    "where tenant_id = ? and company_id = ? and workspace_id = ? and status = 'DRAFT'",
                    (at, self.tenant_id, company_id, workspace_id),
                )
                conn.execute(
                    "update runtime_simulation_runs set invalidated_at = ?, invalidation_reason = ?, updated_at = ? "
                    "where tenant_id = ? and company_id = ? and workspace_id = ? and simulation_run_id = ? "
                    "and invalidated_at is null",
                    (at, f"CEO_{decision_choice}", at, self.tenant_id, company_id, workspace_id,
                     context["simulation_id"]),
                )
        return self.get_staffing_approval(company_id, workspace_id)

    def rollback_staffing(
        self,
        *,
        company_id: str,
        workspace_id: str,
        reason: str,
    ) -> dict:
        reason = reason.strip()
        if not reason:
            raise ValueError("staffing rollback requires a reason")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            workspace, version = self._workspace_version(conn, company_id, workspace_id)
            decision = version["data"].get("staffingDecision")
            if isinstance(decision, dict) and decision.get("state") == "ROLLED_BACK":
                return self.get_staffing_approval(company_id, workspace_id)
            if (
                not isinstance(decision, dict)
                or decision.get("choice") != "APPROVE"
                or decision.get("state") != "APPLIED"
                or workspace["status"] != "OPERATING"
                or workspace["operating_version"] != decision.get("operatingVersion")
            ):
                raise TransitionError("workspace has no active staffing decision to roll back")
            now = datetime.now(timezone.utc)
            try:
                rollback_until = datetime.fromisoformat(str(decision["rollbackUntil"]))
            except (KeyError, TypeError, ValueError) as error:
                raise TransitionError("staffing decision has no valid rollback window") from error
            if now > rollback_until:
                raise TransitionError("staffing rollback window has expired")
            at = now.isoformat(timespec="seconds")
            entities = self._staffing_entities(conn, company_id, workspace_id)
            if self._one_org_version(entities) != decision.get("orgVersion"):
                raise TransitionError("staffing organization version changed; rollback refused")
            self._rollback_active_staffing(conn, workspace, version, entities, decision, reason, at)
        return self.get_staffing_approval(company_id, workspace_id)

    def _workspace_version(self, conn, company_id: str, workspace_id: str) -> tuple[dict, dict]:
        workspace_row = conn.execute(
            "select * from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
            (self.tenant_id, company_id, workspace_id),
        ).fetchone()
        if workspace_row is None:
            raise RuntimeScopeError("workspace does not belong to current company")
        workspace = dict(workspace_row)
        version_row = conn.execute(
            "select * from runtime_workspace_versions where tenant_id = ? and company_id = ? "
            "and workspace_id = ? and blueprint_version = ?",
            (self.tenant_id, company_id, workspace_id, workspace["blueprint_version"]),
        ).fetchone()
        if version_row is None:
            raise ValueError("current Workspace Blueprint Version is missing")
        version = dict(version_row)
        version["data"] = json.loads(version.pop("data_json"))
        return workspace, version

    def _staffing_entities(self, conn, company_id: str, workspace_id: str) -> dict[str, list[dict]]:
        result = {kind: [] for kind in ("ROLE_SLOT", "AI_EMPLOYEE", "CAPABILITY_BINDING")}
        rows = conn.execute(
            "select * from runtime_entities where tenant_id = ? and company_id = ? and workspace_id = ? "
            "and entity_type in ('ROLE_SLOT', 'AI_EMPLOYEE', 'CAPABILITY_BINDING') "
            "order by created_at, entity_id",
            (self.tenant_id, company_id, workspace_id),
        ).fetchall()
        for row in rows:
            item = dict(row)
            item["data"] = json.loads(item.pop("data_json"))
            result[item["entity_type"]].append(item)
        return result

    @staticmethod
    def _one_org_version(entities: dict[str, list[dict]]) -> str | None:
        versions = {
            item["org_version"]
            for items in entities.values()
            for item in items
            if item.get("org_version")
        }
        return next(iter(versions)) if len(versions) == 1 else None

    def _entity_row(self, conn, entity_id: str) -> dict:
        row = conn.execute(
            "select * from runtime_entities where tenant_id = ? and entity_id = ?",
            (self.tenant_id, entity_id),
        ).fetchone()
        if row is None:
            raise KeyError(entity_id)
        item = dict(row)
        item["data"] = json.loads(item.pop("data_json"))
        return item

    def _insert_runtime_entity(
        self,
        conn,
        *,
        entity_type: str,
        company_id: str,
        workspace_id: str,
        owner_ref: str,
        lifecycle_status: str,
        data: dict,
        at: str,
        parent_id: str | None = None,
        org_version: str | None = None,
        blueprint_version: str | None = None,
        verification_status: str = "UNVERIFIED",
        evidence_condition: str = "MISSING",
    ) -> str:
        entity_id = f"{entity_type.lower()}-{uuid4()}"
        conn.execute(
            "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, "
            "parent_id, owner_ref, lifecycle_status, org_version, blueprint_version, verification_status, "
            "evidence_condition, data_json, created_at, updated_at) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                entity_id, self.tenant_id, entity_type, company_id, workspace_id, parent_id,
                owner_ref, lifecycle_status, org_version, blueprint_version, verification_status,
                evidence_condition, json.dumps(data, ensure_ascii=False), at, at,
            ),
        )
        return entity_id

    def _insert_link(
        self,
        conn,
        company_id: str,
        workspace_id: str,
        source_id: str,
        relation: str,
        target_id: str,
        at: str,
    ) -> None:
        conn.execute(
            "insert into runtime_links(link_id, tenant_id, company_id, workspace_id, source_id, relation, target_id, created_at) "
            "values (?, ?, ?, ?, ?, ?, ?, ?)",
            (f"link-{uuid4()}", self.tenant_id, company_id, workspace_id, source_id, relation, target_id, at),
        )

    def _operating_cycle_context(self, conn, company_id: str, workspace_id: str, cycle_id: str) -> dict:
        workspace, version = self._workspace_version(conn, company_id, workspace_id)
        version_data = version["data"]
        if (
            workspace["status"] != "OPERATING"
            or workspace["operating_version"] <= 0
            or version["status"] != "OPERATING"
            or version["operating_version"] != workspace["operating_version"]
            or version_data.get("approvedCurrent") is not True
            or (version_data.get("staffingDecision") or {}).get("state") != "APPLIED"
        ):
            raise TransitionError("Cycle requires the current approved Operating Workspace Version")
        cycle = self._entity_row(conn, cycle_id)
        if (
            cycle["entity_type"] != "CYCLE"
            or cycle["company_id"] != company_id
            or cycle["workspace_id"] != workspace_id
            or cycle["blueprint_version"] != workspace["blueprint_version"]
        ):
            raise RuntimeScopeError("Cycle is outside the current Operating Workspace")
        entities = self._staffing_entities(conn, company_id, workspace_id)
        org_version = self._one_org_version(entities)
        if not org_version or org_version != version_data.get("orgVersion"):
            raise TransitionError("Operating organization version is missing or changed")
        roles = entities["ROLE_SLOT"]
        employees = entities["AI_EMPLOYEE"]
        bindings = entities["CAPABILITY_BINDING"]
        if (
            not roles
            or len(roles) != len(employees)
            or any(item["org_version"] != org_version for item in [*roles, *employees, *bindings])
            or any(item["blueprint_version"] != cycle["blueprint_version"] for item in [*roles, *employees, *bindings])
            or any(item["lifecycle_status"] not in {"ASSIGNED", "OPERATING"} for item in roles)
            or any(item["lifecycle_status"] not in {"AVAILABLE", "OPERATING", "DEGRADED"} for item in employees)
            or not bindings
            or any(item["lifecycle_status"] != "ACTIVE" for item in bindings)
        ):
            raise TransitionError("Operating team is incomplete, unavailable, or unauthorized")
        employee_by_id = {item["entity_id"]: item for item in employees}
        assignments = []
        assigned_ids = set()
        for role in roles:
            employee_id = role["data"].get("assignedEmployeeRef")
            employee = employee_by_id.get(employee_id)
            if employee is None or employee["data"].get("roleSlotRef") != role["entity_id"]:
                raise TransitionError("Operating Role to Employee assignment is incomplete")
            assignments.append((role, employee))
            assigned_ids.add(employee_id)
        if assigned_ids != set(employee_by_id):
            raise TransitionError("Operating team has an unassigned Employee")
        return {
            "workspace": workspace,
            "version": version,
            "cycle": cycle,
            "org_version": org_version,
            "assignments": assignments,
            "bindings": bindings,
        }

    def _activation_context(self, conn, company_id: str, workspace_id: str) -> dict:
        workspace, version = self._workspace_version(conn, company_id, workspace_id)
        if workspace["status"] != "DRAFT" or workspace["operating_version"] != 0:
            raise TransitionError("staffing approval requires an inactive Workspace Draft")
        active_version = conn.execute(
            "select blueprint_version from runtime_workspace_versions where tenant_id = ? and company_id = ? "
            "and workspace_id = ? and status = 'OPERATING'",
            (self.tenant_id, company_id, workspace_id),
        ).fetchone()
        if active_version is not None:
            raise TransitionError("Workspace already has an Operating Version")
        supply = self._supply_context(conn, company_id, workspace_id)
        entities = self._staffing_entities(conn, company_id, workspace_id)
        roles = entities["ROLE_SLOT"]
        employees = entities["AI_EMPLOYEE"]
        bindings = entities["CAPABILITY_BINDING"]
        blueprint = json.loads(workspace["blueprint_json"])
        expected_roles = [item.get("role") for item in blueprint.get("roleSlots") or [] if isinstance(item, dict)]
        if (
            not roles
            or len(roles) != len(expected_roles)
            or {item["data"].get("name") for item in roles} != set(expected_roles)
            or len(employees) != len(roles)
            or len(bindings) != len(supply["bindings"])
            or self._one_org_version(entities) != supply["org_version"]
            or any(item["blueprint_version"] != supply["blueprint_version"] for items in entities.values() for item in items)
            or any(item["lifecycle_status"] != "DRAFT" for item in roles)
            or any(item["lifecycle_status"] != "PROPOSED" for item in employees)
        ):
            raise ValueError("staffing proposal is incomplete, active, or version-mismatched")

        links = [dict(row) for row in conn.execute(
            "select source_id, relation, target_id from runtime_links where tenant_id = ? and company_id = ? "
            "and workspace_id = ? order by created_at, link_id",
            (self.tenant_id, company_id, workspace_id),
        ).fetchall()]
        role_ids = {item["entity_id"] for item in roles}
        employee_ids = {item["entity_id"] for item in employees}
        binding_by_ref = {item["data"].get("requirementRef"): item["entity_id"] for item in bindings}
        for role in roles:
            role_id = role["entity_id"]
            assigned = {
                item["source_id"] for item in links
                if item["relation"] == "PROPOSED_FOR" and item["target_id"] == role_id
            }
            required = {
                item["target_id"] for item in links
                if item["relation"] == "REQUIRES_CAPABILITY" and item["source_id"] == role_id
            }
            expected = {binding_by_ref.get(ref) for ref in role["data"].get("capabilityRefs") or []}
            if len(assigned) != 1 or not assigned <= employee_ids or None in expected or required != expected:
                raise ValueError("staffing proposal relations are incomplete or forged")
        if {
            item["source_id"] for item in links
            if item["relation"] == "PROPOSED_FOR" and item["source_id"] in employee_ids
        } != employee_ids:
            raise ValueError("each proposed employee must cover exactly one current Role Slot")

        for binding in bindings:
            persisted = binding["data"].get("supplyReview")
            if not isinstance(persisted, dict):
                raise ValueError("capability Resource Check is incomplete")
            current = self._resolve_supply(
                conn, persisted.get("source"), persisted.get("capabilityType"), persisted.get("capabilityId"),
            )
            if current is None:
                raise ValueError("capability supply is unavailable or changed")
            assessed = self._assess_supply(conn, current)
            if assessed["blockers"] or any(
                persisted.get(key) != assessed.get(key)
                for key in ("source", "capabilityType", "capabilityId", "catalogUpdatedAt")
            ):
                raise ValueError("capability Resource Check is blocked or stale")
        return {
            **supply,
            "workspace": workspace,
            "version": version,
            "entities": entities,
            "links": links,
        }

    def _record_path(
        self,
        conn,
        *,
        machine_name: str,
        entity_id: str,
        source: str,
        steps: list[tuple[str, str, str, dict]],
        company_id: str,
        workspace_id: str,
        reason: str,
    ) -> str:
        current = source
        machine = get_registered_machine(machine_name)
        for target, actor, trigger, context in steps:
            record = machine.transition(
                entity_id, current, target, actor=actor, trigger=trigger,
                reason=reason, context=context, record=False,
            )
            conn.execute(
                "insert into runtime_transition_log(tenant_id, entity_type, entity_id, source, target, "
                "trigger, actor, at, reason, company_id, workspace_id, context_json) "
                "values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    self.tenant_id, machine_name, entity_id, record.source, record.target,
                    record.trigger, record.actor, record.at, reason, company_id, workspace_id,
                    json.dumps(record.context, ensure_ascii=False),
                ),
            )
            current = target
        return current

    def _activate_staffing(self, conn, workspace: dict, version: dict, context: dict, decision: dict, at: str) -> None:
        company_id = workspace["company_id"]
        workspace_id = workspace["workspace_id"]
        audit = {
            "decisionId": decision["decisionId"],
            "blueprintVersion": decision["blueprintVersion"],
            "orgVersion": decision["orgVersion"],
            "simulationId": decision["simulationId"],
            "operatingVersion": decision["operatingVersion"],
        }
        role_to_employee = {
            item["target_id"]: item["source_id"]
            for item in context["links"] if item["relation"] == "PROPOSED_FOR"
        }
        for role in context["entities"]["ROLE_SLOT"]:
            data = role["data"] | {
                "staffingStatus": "ASSIGNED",
                "assignedEmployeeRef": role_to_employee[role["entity_id"]],
                "assignedAt": at,
                "approvedBy": "CEO",
            }
            target = self._record_path(
                conn, machine_name="role_slot", entity_id=role["entity_id"], source="DRAFT",
                steps=[("READY", "SYSTEM", "validate_role", audit), ("ASSIGNED", "CEO", "assign", audit)],
                company_id=company_id, workspace_id=workspace_id, reason=decision["reason"],
            )
            cursor = conn.execute(
                "update runtime_entities set lifecycle_status = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'DRAFT'",
                (target, json.dumps(data, ensure_ascii=False), at, self.tenant_id, role["entity_id"]),
            )
            if cursor.rowcount != 1:
                raise RuntimeError("Role Slot changed during activation")

        for employee in context["entities"]["AI_EMPLOYEE"]:
            data = employee["data"] | {
                "staffingStatus": "HIRED_AVAILABLE",
                "activatedAt": at,
                "approvedBy": "CEO",
            }
            target = self._record_path(
                conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="PROPOSED",
                steps=[
                    ("CREATED", "CEO", "accept_proposal", audit),
                    ("CONFIGURED", "CEO", "configure", audit),
                    ("AVAILABLE", "CEO", "approve_simulation", audit),
                ],
                company_id=company_id, workspace_id=workspace_id, reason=decision["reason"],
            )
            cursor = conn.execute(
                "update runtime_entities set lifecycle_status = ?, presence_state = 'AVAILABLE', data_json = ?, "
                "updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'PROPOSED'",
                (target, json.dumps(data, ensure_ascii=False), at, self.tenant_id, employee["entity_id"]),
            )
            if cursor.rowcount != 1:
                raise RuntimeError("AI Employee changed during activation")

        for binding in context["entities"]["CAPABILITY_BINDING"]:
            review = binding["data"]["supplyReview"]
            data = binding["data"] | {
                "authorizationStatus": "AUTHORIZED_ACTIVE",
                "authority": review["effectClass"],
                "authorizedBy": "CEO",
                "authorizedAt": at,
                "activatedAt": at,
            }
            target = self._record_path(
                conn, machine_name="capability_binding", entity_id=binding["entity_id"], source="PROPOSED",
                steps=[("AUTHORIZED", "CEO", "authorize", audit), ("ACTIVE", "SYSTEM", "activate", audit)],
                company_id=company_id, workspace_id=workspace_id, reason=decision["reason"],
            )
            cursor = conn.execute(
                "update runtime_entities set lifecycle_status = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'PROPOSED'",
                (target, json.dumps(data, ensure_ascii=False), at, self.tenant_id, binding["entity_id"]),
            )
            if cursor.rowcount != 1:
                raise RuntimeError("Capability Binding changed during activation")

        workspace_target = self._record_path(
            conn, machine_name="workspace", entity_id=workspace_id, source="DRAFT",
            steps=[
                ("BLUEPRINTING", "CEO", "start_blueprint", audit),
                ("SIMULATED", "SYSTEM", "simulation_passed", audit | {"simulationPassed": True}),
                ("PENDING_APPROVAL", "CEO", "submit_for_approval", audit | {
                    "issuesResolved": True, "simulationPassed": True, "externalAgentReviewed": True,
                }),
                ("OPERATING", "CEO", "approve_and_launch", audit),
            ],
            company_id=company_id, workspace_id=workspace_id, reason=decision["reason"],
        )
        cursor = conn.execute(
            "update workspaces set status = ?, simulation_passed = 1, issues_resolved = 1, "
            "external_agent_reviewed = 1, operating_version = ?, updated_at = ? "
            "where tenant_id = ? and company_id = ? and workspace_id = ? and status = 'DRAFT' "
            "and blueprint_version = ? and operating_version = 0",
            (
                workspace_target, decision["operatingVersion"], at, self.tenant_id, company_id,
                workspace_id, decision["blueprintVersion"],
            ),
        )
        if cursor.rowcount != 1:
            raise RuntimeError("Workspace changed during activation")
        version["data"].update({
            "staffingDecision": decision,
            "approvedCurrent": True,
            "approvedBy": "CEO",
            "approvedAt": at,
            "orgVersion": decision["orgVersion"],
        })
        cursor = conn.execute(
            "update runtime_workspace_versions set status = 'OPERATING', simulation_passed = 1, "
            "operating_version = ?, data_json = ?, updated_at = ? where tenant_id = ? and company_id = ? "
            "and workspace_id = ? and blueprint_version = ? and status = 'DRAFT'",
            (
                decision["operatingVersion"], json.dumps(version["data"], ensure_ascii=False), at,
                self.tenant_id, company_id, workspace_id, decision["blueprintVersion"],
            ),
        )
        if cursor.rowcount != 1:
            raise RuntimeError("Workspace Version changed during activation")

    def _rollback_active_staffing(
        self,
        conn,
        workspace: dict,
        version: dict,
        entities: dict[str, list[dict]],
        decision: dict,
        reason: str,
        at: str,
    ) -> None:
        company_id = workspace["company_id"]
        workspace_id = workspace["workspace_id"]
        if (
            any(item["lifecycle_status"] != "ASSIGNED" for item in entities["ROLE_SLOT"])
            or any(item["lifecycle_status"] != "AVAILABLE" for item in entities["AI_EMPLOYEE"])
            or any(item["lifecycle_status"] != "ACTIVE" for item in entities["CAPABILITY_BINDING"])
        ):
            raise TransitionError("active staffing state changed; rollback refused")
        audit = {"decisionId": decision["decisionId"], "rollback": True, "orgVersion": decision["orgVersion"]}
        for role in entities["ROLE_SLOT"]:
            data = role["data"] | {"staffingStatus": "READY_AFTER_ROLLBACK", "rolledBackAt": at}
            target = self._record_path(
                conn, machine_name="role_slot", entity_id=role["entity_id"], source="ASSIGNED",
                steps=[("REASSIGNING", "CEO", "reassign", audit), ("READY", "SYSTEM", "return_to_ready", audit)],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'ASSIGNED'",
                (target, json.dumps(data, ensure_ascii=False), at, self.tenant_id, role["entity_id"]),
            )
        for employee in entities["AI_EMPLOYEE"]:
            data = employee["data"] | {"staffingStatus": "SUSPENDED_AFTER_ROLLBACK", "rolledBackAt": at}
            target = self._record_path(
                conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="AVAILABLE",
                steps=[("SUSPENDED", "CEO", "suspend", audit)],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = ?, presence_state = 'BLOCKED', data_json = ?, "
                "updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'AVAILABLE'",
                (target, json.dumps(data, ensure_ascii=False), at, self.tenant_id, employee["entity_id"]),
            )
        for binding in entities["CAPABILITY_BINDING"]:
            data = binding["data"] | {"authorizationStatus": "REVOKED", "revokedBy": "CEO", "revokedAt": at}
            target = self._record_path(
                conn, machine_name="capability_binding", entity_id=binding["entity_id"], source="ACTIVE",
                steps=[("REVOKED", "CEO", "revoke", audit)],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'ACTIVE'",
                (target, json.dumps(data, ensure_ascii=False), at, self.tenant_id, binding["entity_id"]),
            )
        workspace_target = self._record_path(
            conn, machine_name="workspace", entity_id=workspace_id, source="OPERATING",
            steps=[("PAUSED", "CEO", "pause", audit)], company_id=company_id,
            workspace_id=workspace_id, reason=reason,
        )
        cursor = conn.execute(
            "update workspaces set status = ?, simulation_passed = 0, issues_resolved = 0, "
            "external_agent_reviewed = 0, operating_version = 0, updated_at = ? "
            "where tenant_id = ? and company_id = ? and workspace_id = ? and status = 'OPERATING' "
            "and operating_version = ?",
            (workspace_target, at, self.tenant_id, company_id, workspace_id, decision["operatingVersion"]),
        )
        if cursor.rowcount != 1:
            raise RuntimeError("Workspace changed during rollback")
        decision.update({"state": "ROLLED_BACK", "rolledBackBy": "CEO", "rolledBackAt": at, "rollbackReason": reason})
        version["data"].update({"staffingDecision": decision, "approvedCurrent": False})
        conn.execute(
            "update runtime_workspace_versions set status = 'ROLLED_BACK', simulation_passed = 0, "
            "data_json = ?, updated_at = ? where tenant_id = ? and company_id = ? and workspace_id = ? "
            "and blueprint_version = ? and operating_version = ?",
            (
                json.dumps(version["data"], ensure_ascii=False), at, self.tenant_id, company_id,
                workspace_id, decision["blueprintVersion"], decision["operatingVersion"],
            ),
        )
        conn.execute(
            "update runtime_simulation_runs set invalidated_at = ?, invalidation_reason = ?, updated_at = ? "
            "where tenant_id = ? and company_id = ? and workspace_id = ? and simulation_run_id = ? "
            "and invalidated_at is null",
            (at, "STAFFING_ACTIVATION_ROLLED_BACK", at, self.tenant_id, company_id, workspace_id,
             decision["simulationId"]),
        )

    def _supply_context(self, conn, company_id: str, workspace_id: str) -> dict:
        workspace = conn.execute(
            "select blueprint_version, blueprint_json, status, simulation_passed from workspaces "
            "where tenant_id = ? and company_id = ? and workspace_id = ?",
            (self.tenant_id, company_id, workspace_id),
        ).fetchone()
        if workspace is None:
            raise RuntimeScopeError("workspace does not belong to current company")
        blueprint = json.loads(workspace["blueprint_json"])
        if blueprint.get("lifecycleMode") != "STUDIO_DRAFT":
            raise ValueError("capability supply review requires a Studio Draft")
        rows = conn.execute(
            "select * from runtime_entities where tenant_id = ? and company_id = ? and workspace_id = ? "
            "and entity_type = 'CAPABILITY_BINDING' order by created_at, entity_id",
            (self.tenant_id, company_id, workspace_id),
        ).fetchall()
        bindings = []
        for row in rows:
            item = dict(row)
            item["data"] = json.loads(item.pop("data_json"))
            bindings.append(item)
        expected_requirements = {
            item.get("capabilityRef")
            for item in blueprint.get("capabilityBindings") or []
            if isinstance(item, dict) and item.get("capabilityRef")
        }
        actual_requirements = [item["data"].get("requirementRef") for item in bindings]
        org_versions = {item["org_version"] for item in bindings if item["org_version"]}
        if (
            not bindings
            or set(actual_requirements) != expected_requirements
            or len(actual_requirements) != len(expected_requirements)
            or len(org_versions) != 1
            or any(item["lifecycle_status"] != "PROPOSED" for item in bindings)
            or any(item["data"].get("authorizationStatus") != "PROPOSED_NOT_AUTHORIZED" for item in bindings)
            or any(item["blueprint_version"] != workspace["blueprint_version"] for item in bindings)
        ):
            raise ValueError("capability proposal is incomplete, authorized, or version-mismatched")
        org_version = next(iter(org_versions))
        simulations = conn.execute(
            "select simulation_run_id, blueprint_version, lifecycle_status, pass_status, invalidated_at, input_refs_json "
            "from runtime_simulation_runs where tenant_id = ? and company_id = ? and workspace_id = ? "
            "and scenario_id = 'ORG-001' order by created_at desc, simulation_run_id desc",
            (self.tenant_id, company_id, workspace_id),
        ).fetchall()
        simulation = next((item for item in simulations if (
            item["blueprint_version"] == workspace["blueprint_version"]
            and item["lifecycle_status"] == "PASSED"
            and item["pass_status"] == "PASS"
            and not item["invalidated_at"]
            and f"org-version:{org_version}" in json.loads(item["input_refs_json"])
        )), None)
        if simulation is None:
            raise ValueError("capability supply review requires a current ORG-001 PASS")
        return {
            "blueprint_version": workspace["blueprint_version"],
            "org_version": org_version,
            "simulation_id": simulation["simulation_run_id"],
            "bindings": bindings,
        }

    def _supply_catalog(self, conn) -> list[dict]:
        official = conn.execute(
            "select * from official_models where source = 'official' and status = 'active' "
            "and gateway_ref != 'freellmapi.experimental' order by type, model_key"
        ).fetchall()
        private = conn.execute(
            "select * from tenant_private_capabilities where tenant_id = ? and source = 'tenant_private' "
            "and status = 'active' order by capability_type, capability_id",
            (self.tenant_id,),
        ).fetchall()
        return [
            self._assess_supply(conn, self._official_supply(dict(row))) for row in official
        ] + [
            self._assess_supply(conn, self._private_supply(dict(row))) for row in private
        ]

    def _resolve_supply(self, conn, source, capability_type, capability_id) -> dict | None:
        if source == "official":
            row = conn.execute(
                "select * from official_models where model_key = ? and type = ? "
                "and source = 'official' and status = 'active' and gateway_ref != 'freellmapi.experimental'",
                (capability_id, capability_type),
            ).fetchone()
            return self._official_supply(dict(row)) if row else None
        if source == "tenant_private":
            row = conn.execute(
                "select * from tenant_private_capabilities where tenant_id = ? and capability_id = ? "
                "and capability_type = ? and source = 'tenant_private' and status = 'active'",
                (self.tenant_id, capability_id, capability_type),
            ).fetchone()
            return self._private_supply(dict(row)) if row else None
        return None

    @staticmethod
    def _official_supply(row: dict) -> dict:
        try:
            runtime_meta = json.loads(row.get("runtime_meta_json") or "{}")
        except (TypeError, json.JSONDecodeError):
            runtime_meta = {}
        return {
            "source": "official",
            "capabilityType": row.get("type"),
            "capabilityId": row.get("model_key"),
            "displayName": row.get("display_name") or row.get("name") or row.get("model_key"),
            "catalogUpdatedAt": row.get("updated_at"),
            "authType": row.get("auth_type"),
            "gatewayRef": row.get("gateway_ref"),
            "runtimeMeta": runtime_meta if isinstance(runtime_meta, dict) else {},
        }

    @staticmethod
    def _private_supply(row: dict) -> dict:
        try:
            runtime_meta = json.loads(row.get("metadata_json") or "{}")
        except (TypeError, json.JSONDecodeError):
            runtime_meta = {}
        return {
            "source": "tenant_private",
            "capabilityType": row.get("capability_type"),
            "capabilityId": row.get("capability_id"),
            "displayName": row.get("display_name") or row.get("capability_id"),
            "catalogUpdatedAt": row.get("updated_at"),
            "authType": runtime_meta.get("auth_type"),
            "gatewayRef": runtime_meta.get("gateway_ref"),
            "runtimeMeta": runtime_meta if isinstance(runtime_meta, dict) else {},
        }

    @staticmethod
    def _assess_supply(conn, supply: dict) -> dict:
        runtime_meta = supply["runtimeMeta"]
        kind = str(supply["capabilityType"] or "")
        effect = effect_class_for_capability(kind, supply["displayName"])
        blockers = []
        live_status = str(runtime_meta.get("live_status") or "unknown").lower()
        availability = "AVAILABLE" if live_status == "available" else "UNAVAILABLE" if live_status == "unavailable" else "UNKNOWN"
        if availability != "AVAILABLE":
            blockers.append(f"LIVE_STATUS_{availability}")
        configured = True
        if supply["source"] == "official" and kind == "model":
            gateway = conn.execute(
                "select status, credential_ref from model_gateways where gateway_id = ?",
                (supply.get("gatewayRef"),),
            ).fetchone()
            configured = bool(
                gateway
                and gateway["status"] == "active"
                and (supply.get("authType") == "none" or gateway["credential_ref"])
            )
        elif kind in {"model", "connector", "api", "webhook"}:
            configured = bool(runtime_meta.get("credentials_ref") or runtime_meta.get("credential_ref"))
        if not configured:
            blockers.append("RUNTIME_CONFIGURATION_MISSING")
        permissions = runtime_meta.get("permissions")
        permission_status = "PLANNING_READ_ONLY" if effect in {"read", "retrieve"} else "SCOPE_DECLARED_AWAITING_CEO" if isinstance(permissions, list) and permissions else "PERMISSION_SCOPE_MISSING"
        if permission_status == "PERMISSION_SCOPE_MISSING":
            blockers.append(permission_status)
        cost_status = "UNIT_COST_DECLARED" if runtime_meta.get("cost_per_unit") is not None else "COST_METADATA_MISSING"
        if cost_status == "COST_METADATA_MISSING":
            blockers.append(cost_status)
        risk_status = "LOW_REVIEWED" if effect in {"read", "retrieve"} else "HIGH_AWAITING_CEO"
        return {
            "source": supply["source"],
            "capabilityType": kind,
            "capabilityId": supply["capabilityId"],
            "displayName": supply["displayName"],
            "catalogUpdatedAt": supply["catalogUpdatedAt"],
            "effectClass": effect,
            "availabilityStatus": availability,
            "runtimeConfigured": configured,
            "permissionStatus": permission_status,
            "riskStatus": risk_status,
            "costStatus": cost_status,
            "blockers": sorted(set(blockers)),
        }

    def create_cycle(
        self,
        *,
        company_id: str,
        workspace_id: str,
        blueprint_version: str,
        owner_ref: str,
        outcome_ref: str,
        intent_ref: str,
        execution_ref: str | None = None,
        project_ref: str | None = None,
        work_item_title: str = "",
        instruction: str = "",
        resource_refs: list[str] | None = None,
        test_command: list[str] | None = None,
        requested_access_intent: str = "AUTO_WITHIN_BOUNDARY",
        evidence_refs: list[str] | None = None,
        next_check_at: str | None = None,
    ) -> dict:
        workspace = self.get_workspace(company_id, workspace_id)["workspace"]
        if workspace["business_type"] != "RD":
            raise ValueError("Cycle endpoint only accepts RD workspaces")
        self._require_current_blueprint(workspace, blueprint_version)
        existing = self.foundation.list("CYCLE", company_id=company_id, workspace_id=workspace_id)
        evidence = self._evidence(evidence_refs or [], company_id, workspace_id)
        resource_refs = [str(item).strip() for item in (resource_refs or []) if str(item).strip()]
        test_command = [str(item) for item in (test_command or []) if str(item)]
        auto_requested = bool(project_ref or work_item_title.strip() or instruction.strip() or resource_refs or test_command)
        if auto_requested:
            if not all((project_ref, work_item_title.strip(), instruction.strip(), resource_refs, test_command)):
                raise ValueError("RD execution requires project, title, instruction, resource refs, and test command")
            with self.db.connect() as conn:
                project = conn.execute(
                    "select project_id from projects where tenant_id = ? and company_id = ? "
                    "and project_id = ? and status = 'active'",
                    (self.tenant_id, company_id, project_ref),
                ).fetchone()
            if project is None:
                raise RuntimeScopeError("RD Project is outside the current Company")
            if execution_ref and execution_ref != "rd_task:auto":
                raise ValueError("RD auto execution cannot bind a manual workflow run")
            execution_ref = "rd_task:auto"
        cycle = self.foundation.create(
            "CYCLE",
            company_id=company_id,
            workspace_id=workspace_id,
            owner_ref=owner_ref,
            blueprint_version=blueprint_version,
            execution_ref=execution_ref,
            next_check_at=next_check_at,
            data={
                "workItemName": work_item_title.strip() if auto_requested else ("完善 Curis" if not existing else f"研发周期 {len(existing) + 1}"),
                "outcomeRef": outcome_ref,
                "intentRef": intent_ref,
                "currentStage": RD_STAGES[0],
                "stages": list(RD_STAGES),
                "evidenceRefs": evidence,
                **({
                    "projectRef": project_ref,
                    "instruction": instruction.strip(),
                    "resourceRefs": resource_refs,
                    "testCommand": test_command,
                    "requestedAccessIntent": requested_access_intent,
                    "workContext": {
                        "objectOwnerRef": owner_ref,
                        "responsibilityEmployeeRef": None,
                        "currentExecutorRef": None,
                        "status": "idle",
                        "activity": "等待分配研发责任",
                        "updatedAt": _now(),
                    },
                } if auto_requested else {}),
            },
        )
        for evidence_id in evidence:
            self.foundation.link(cycle["entity_id"], "HAS_STAGE_EVIDENCE", evidence_id)
        return cycle

    def start_operating_cycle(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        reason: str,
    ) -> dict:
        reason = reason.strip()
        if not reason:
            raise ValueError("operating Cycle start requires a reason")
        current = self.foundation.get(cycle_id)
        rd_work = None
        if current["lifecycle_status"] == "PLANNED" and current.get("execution_ref") == "rd_task:auto":
            rd_work = self._ensure_rd_canonical_work(company_id, workspace_id, cycle_id)
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            if cycle["lifecycle_status"] != "PLANNED":
                if cycle["data"].get("operatingVersion") == context["workspace"]["operating_version"]:
                    return self.foundation.get(cycle_id)
                raise TransitionError("Cycle is not ready to start in the current Operating Version")
            if not cycle.get("execution_ref"):
                raise ValueError("Operating Cycle requires an explicit executionRef")
            if cycle["execution_ref"] == "rd_task:auto":
                role, employee, binding, selection = self._rd_execution_assignment(context)
                if rd_work is None:
                    raise TransitionError("RD canonical Work is unavailable")
                at = _now()
                audit = {
                    "cycleId": cycle_id,
                    "operatingVersion": context["workspace"]["operating_version"],
                    "orgVersion": context["org_version"],
                }
                self._record_path(
                    conn, machine_name="cycle", entity_id=cycle_id, source="PLANNED",
                    steps=[("READY", "CEO", "ready", audit), ("RUNNING", "CEO", "start", audit)],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                data = cycle["data"] | {
                    "operatingVersion": context["workspace"]["operating_version"],
                    "orgVersion": context["org_version"],
                    "teamRefs": [employee["entity_id"]],
                    "roleSlotRefs": [role["entity_id"]],
                    "inputHandoffRefs": [],
                    "executionStatus": "READY",
                    "canonicalWorkRef": rd_work["entity_id"],
                    "responsibilityAssignmentRef": rd_work["data"]["responsibilityAssignmentRef"],
                    "executionBinding": {
                        "responsibilityEmployeeRef": employee["entity_id"],
                        "roleSlotRef": role["entity_id"],
                        "capabilityBindingRef": binding["entity_id"],
                        "capabilitySource": selection["source"],
                        "capabilityType": selection["capabilityType"],
                        "capabilityId": selection["capabilityId"],
                        "projectRef": cycle["data"]["projectRef"],
                        "workspaceRef": workspace_id,
                        "requestedAccessIntent": cycle["data"]["requestedAccessIntent"],
                        "resourceRefs": cycle["data"]["resourceRefs"],
                    },
                    "workContext": (cycle["data"].get("workContext") or {}) | {
                        "responsibilityEmployeeRef": employee["entity_id"],
                        "responsibilityRoleSlotRef": role["entity_id"],
                        "currentExecutorRef": None,
                        "status": "idle",
                        "activity": "研发责任已分配，等待真实执行",
                        "updatedAt": at,
                    },
                    "startedAt": at,
                }
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'RUNNING', data_json = ?, updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'PLANNED'",
                    (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
                )
                return self._entity_row(conn, cycle_id)
            at = _now()
            audit = {
                "cycleId": cycle_id,
                "operatingVersion": context["workspace"]["operating_version"],
                "orgVersion": context["org_version"],
            }
            handoff_refs = []
            for role, employee in context["assignments"]:
                handoff_id = self._insert_runtime_entity(
                    conn,
                    entity_type="HANDOFF",
                    company_id=company_id,
                    workspace_id=workspace_id,
                    parent_id=cycle_id,
                    owner_ref=employee["entity_id"],
                    lifecycle_status="CREATED",
                    org_version=context["org_version"],
                    blueprint_version=cycle["blueprint_version"],
                    data={
                        "kind": "RESPONSIBILITY_INPUT",
                        "cycleId": cycle_id,
                        "fromRole": "CEO Assistant",
                        "toRole": role["data"].get("name"),
                        "roleSlotRef": role["entity_id"],
                        "employeeRef": employee["entity_id"],
                        "inputRefs": [cycle["data"].get("intentRef"), cycle["data"].get("outcomeRef")],
                        "outputRefs": [],
                        "acknowledgement": "AI_EMPLOYEE_ACCEPTED",
                        "actor": "AI_EMPLOYEE",
                        "at": at,
                    },
                    at=at,
                )
                self._record_path(
                    conn, machine_name="handoff", entity_id=handoff_id, source="CREATED",
                    steps=[
                        ("SENT", "SYSTEM", "send", audit),
                        ("ACKNOWLEDGED", "AI_EMPLOYEE", "acknowledge", audit),
                    ],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'ACKNOWLEDGED', updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'CREATED'",
                    (at, self.tenant_id, handoff_id),
                )
                self._insert_link(conn, company_id, workspace_id, cycle_id, "HAS_HANDOFF", handoff_id, at)
                handoff_refs.append(handoff_id)

                if role["lifecycle_status"] == "ASSIGNED":
                    self._record_path(
                        conn, machine_name="role_slot", entity_id=role["entity_id"], source="ASSIGNED",
                        steps=[("OPERATING", "AI_EMPLOYEE", "accept_assignment", audit)],
                        company_id=company_id, workspace_id=workspace_id, reason=reason,
                    )
                    conn.execute(
                        "update runtime_entities set lifecycle_status = 'OPERATING', updated_at = ? "
                        "where tenant_id = ? and entity_id = ? and lifecycle_status = 'ASSIGNED'",
                        (at, self.tenant_id, role["entity_id"]),
                    )
                self._record_path(
                    conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="AVAILABLE",
                    steps=[("OPERATING", "AI_EMPLOYEE", "accept_handoff", audit)],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'OPERATING', presence_state = 'RUNNING', "
                    "updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'AVAILABLE'",
                    (at, self.tenant_id, employee["entity_id"]),
                )

            self._record_path(
                conn, machine_name="cycle", entity_id=cycle_id, source="PLANNED",
                steps=[("READY", "CEO", "ready", audit), ("RUNNING", "CEO", "start", audit)],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            data = cycle["data"] | {
                "operatingVersion": context["workspace"]["operating_version"],
                "orgVersion": context["org_version"],
                "teamRefs": [employee["entity_id"] for _, employee in context["assignments"]],
                "roleSlotRefs": [role["entity_id"] for role, _ in context["assignments"]],
                "inputHandoffRefs": handoff_refs,
                "executionStatus": "READY",
                "startedAt": at,
            }
            conn.execute(
                "update runtime_entities set lifecycle_status = 'RUNNING', data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'PLANNED'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def _ensure_rd_canonical_work(self, company_id: str, workspace_id: str, cycle_id: str) -> dict:
        """Attach the accepted shared Work/Responsibility seam to one legacy RD Cycle."""
        from .child_work import CanonicalChildWorkRuntime
        from .responsibility_routing import ResponsibilityRoutingRuntime

        with self.db.connect() as conn:
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
        role, employee, binding, _ = self._rd_execution_assignment(context)
        routing = ResponsibilityRoutingRuntime(self.db)
        assignment_id = f"rd-assignment-{cycle_id}"
        try:
            assignment = self.foundation.get(assignment_id)
        except KeyError:
            assignment = routing.create_assignment(
                assignment_id=assignment_id,
                company_id=company_id,
                workspace_id=workspace_id,
                scope_type="WORKSPACE",
                scope_ref=workspace_id,
                role_ref=role["entity_id"],
                employee_ref=employee["entity_id"],
                responsibility_key="rd-primary-execution",
                responsibility="完成当前研发工作并返回代码、测试与证据",
                capability_binding_refs=[binding["entity_id"]],
                output_contract={"requiresResult": True, "resultType": "rd-code-change"},
            )
        workflows = [
            item for item in self.foundation.list(
                "RESPONSIBILITY_WORKFLOW", company_id=company_id, workspace_id=workspace_id,
            )
            if item["data"].get("workflowKey") == "rd-primary-execution"
        ]
        if not workflows:
            routing.publish_workflow(
                company_id=company_id,
                workspace_id=workspace_id,
                scope_type="WORKSPACE",
                scope_ref=workspace_id,
                workflow_key="rd-primary-execution",
                assignment_refs=[assignment["entity_id"]],
                default_flow=["rd-primary-execution"],
            )
        child = CanonicalChildWorkRuntime(self.db)
        work = child.create_work(
            cycle_id=cycle_id,
            assignment_ref=assignment["entity_id"],
            release_key="rd-primary",
            input_refs=context["cycle"]["data"].get("resourceRefs") or [],
        )
        work = routing.start_work(
            work["entity_id"],
            scope_type="WORKSPACE",
            scope_ref=workspace_id,
            workflow_key="rd-primary-execution",
        )
        if work["lifecycle_status"] == "PLANNED":
            child.transition_work(work["entity_id"], "READY", actor="SYSTEM", reason="RD responsibility ready")
            work = child.transition_work(work["entity_id"], "ACTIVE", actor=employee["entity_id"], reason="RD employee accepted")
        return work

    @staticmethod
    def _rd_execution_assignment(context: dict) -> tuple[dict, dict, dict, dict]:
        matches = []
        for binding in context["bindings"]:
            selection = binding["data"].get("supplyReview") or {}
            if not (
                selection.get("source") == "tenant_private"
                and selection.get("capabilityType") == "agent"
                and selection.get("capabilityId")
            ):
                continue
            requirement_ref = binding["data"].get("requirementRef")
            for role, employee in context["assignments"]:
                if requirement_ref in (role["data"].get("capabilityRefs") or []):
                    matches.append((role, employee, binding, selection))
        if len(matches) != 1:
            raise TransitionError("RD execution requires exactly one active Agent Runtime assignment")
        return matches[0]

    def begin_operating_cycle_execution(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            if cycle["lifecycle_status"] != "RUNNING" or cycle.get("execution_ref") != "rd_task:auto":
                raise TransitionError("RD Cycle is not ready for Task execution")
            if cycle["data"].get("executionStatus") != "READY":
                raise TransitionError("RD Cycle execution is not ready")
            _, employee, _, _ = self._rd_execution_assignment(context)
            at = _now()
            self._record_path(
                conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="AVAILABLE",
                steps=[("OPERATING", "AI_EMPLOYEE", "accept_handoff", {"cycleId": cycle_id})],
                company_id=company_id, workspace_id=workspace_id,
                reason="AI Employee 开始执行当前研发 Task",
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = 'OPERATING', presence_state = 'RUNNING', updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'AVAILABLE'",
                (at, self.tenant_id, employee["entity_id"]),
            )
            data = cycle["data"] | {
                "executionStatus": "RUNNING",
                "conversation": {
                    "summary": "研发员工已接手，正在允许范围内处理这项工作。",
                    "resultRefs": [],
                },
                "workContext": (cycle["data"].get("workContext") or {}) | {
                    "currentExecutorRef": employee["entity_id"],
                    "status": "working",
                    "activity": "Codex 正在声明边界内执行研发 Task",
                    "updatedAt": at,
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def record_operating_cycle_task_started(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        task_ref: str,
        execution_employee_ref: str,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            if cycle["lifecycle_status"] != "RUNNING" or cycle["data"].get("executionStatus") != "RUNNING":
                raise TransitionError("RD Task is not running")
            data = cycle["data"] | {
                "taskRef": task_ref,
                "executionBinding": (cycle["data"].get("executionBinding") or {}) | {
                    "executionEmployeeRef": execution_employee_ref,
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), _now(), self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    @staticmethod
    def _rd_artifact_review(cycle: dict) -> dict | None:
        review = cycle["data"].get("artifactReview")
        return review if isinstance(review, dict) else None

    @staticmethod
    def _rd_review_assignment(context: dict, reviewer_employee_ref: str) -> tuple[dict, dict, dict]:
        holder_ref = (context["cycle"]["data"].get("workContext") or {}).get("responsibilityEmployeeRef")
        if not holder_ref or reviewer_employee_ref == holder_ref:
            raise ValueError("Artifact Review requires a distinct Reviewer Employee")
        reviewer_assignment = next(
            (
                (role, employee)
                for role, employee in context["assignments"]
                if employee["entity_id"] == reviewer_employee_ref
            ),
            None,
        )
        if reviewer_assignment is None:
            raise RuntimeScopeError("Reviewer Employee is outside the current Workspace")
        role, employee = reviewer_assignment
        if employee["lifecycle_status"] != "AVAILABLE":
            raise TransitionError("Reviewer Employee is not available")
        role_requirements = set(role["data"].get("capabilityRefs") or [])
        domain_binding = next(
            (
                binding
                for binding in context["bindings"]
                if binding["data"].get("requirementRef") in role_requirements
            ),
            None,
        )
        if domain_binding is None:
            raise TransitionError("Reviewer Employee has no active review capability")
        return role, employee, domain_binding

    def create_artifact_review_request(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        reviewer_employee_ref: str,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            if cycle["lifecycle_status"] != "RUNNING" or cycle["data"].get("executionStatus") != "COMPLETED":
                raise TransitionError("Artifact Review requires a completed RD execution")
            artifact_refs = list(dict.fromkeys(cycle["data"].get("artifactRefs") or []))
            evidence_refs = list(dict.fromkeys(cycle["data"].get("evidenceRefs") or []))
            if not artifact_refs or not evidence_refs or not cycle["data"].get("taskRef"):
                raise TransitionError("Artifact Review requires persisted Artifact and Evidence")
            existing = self._rd_artifact_review(cycle)
            if existing:
                if (
                    existing.get("reviewerEmployeeRef") == reviewer_employee_ref
                    and existing.get("artifactRefs") == artifact_refs
                ):
                    return cycle
                raise TransitionError("Cycle already has an Artifact Review Request")
            role, reviewer, domain_binding = self._rd_review_assignment(context, reviewer_employee_ref)
            execution_binding = cycle["data"].get("executionBinding") or {}
            if execution_binding.get("capabilityType") != "agent" or not execution_binding.get("capabilityId"):
                raise TransitionError("Artifact Review has no current Agent Runtime binding")
            at = _now()
            review = {
                "requestRef": f"artifact-review-{uuid4()}",
                "status": "REQUESTED",
                "originalHolderRef": (cycle["data"].get("workContext") or {}).get("responsibilityEmployeeRef"),
                "reviewerEmployeeRef": reviewer["entity_id"],
                "reviewerRoleSlotRef": role["entity_id"],
                "reviewCapabilityBindingRef": domain_binding["entity_id"],
                "agentCapabilityBindingRef": execution_binding.get("capabilityBindingRef"),
                "capabilitySource": execution_binding.get("capabilitySource"),
                "capabilityType": execution_binding.get("capabilityType"),
                "capabilityId": execution_binding.get("capabilityId"),
                "requestedAccessIntent": cycle["data"].get("requestedAccessIntent"),
                "sourceTaskRef": cycle["data"].get("taskRef"),
                "artifactRefs": artifact_refs,
                "evidenceRefs": evidence_refs,
                "currentExecutorRef": None,
                "reviewTaskRef": None,
                "sessionRef": None,
                "resultRefs": [],
                "statusHistory": [{"status": "REQUESTED", "at": at}],
                "requestedAt": at,
                "updatedAt": at,
            }
            data = cycle["data"] | {
                "artifactReview": review,
                "reviewConversation": {
                    "summary": f"代码结果已送交 {reviewer['data'].get('name') or '审核员工'} 检查。",
                    "resultRefs": [],
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def begin_artifact_review_execution(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            review = self._rd_artifact_review(cycle)
            if review and review.get("status") == "REVIEWING":
                return cycle
            if (
                cycle["lifecycle_status"] != "RUNNING"
                or cycle["data"].get("executionStatus") != "COMPLETED"
                or not review
                or review.get("status") != "REQUESTED"
            ):
                raise TransitionError("Artifact Review is not ready")
            self._rd_review_assignment(context, str(review.get("reviewerEmployeeRef") or ""))
            at = _now()
            review = review | {
                "status": "REVIEWING",
                "currentExecutorRef": review["reviewerEmployeeRef"],
                "statusHistory": [*review.get("statusHistory", []), {"status": "REVIEWING", "at": at}],
                "startedAt": at,
                "updatedAt": at,
            }
            data = cycle["data"] | {
                "artifactReview": review,
                "reviewConversation": {
                    "summary": "审核员工正在检查代码变化和验证证据。",
                    "resultRefs": [],
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def record_artifact_review_task_started(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        request_ref: str,
        task_ref: str,
        execution_employee_ref: str,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            review = self._rd_artifact_review(cycle)
            if not review or review.get("requestRef") != request_ref or review.get("status") != "REVIEWING":
                raise TransitionError("Artifact Review Task is not current")
            at = _now()
            review = review | {
                "reviewTaskRef": task_ref,
                "executionEmployeeRef": execution_employee_ref,
                "updatedAt": at,
            }
            conn.execute(
                "update runtime_entities set data_json = json_set(data_json, '$.artifactReview', json(?)), updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(review, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def record_artifact_review_result(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        request_ref: str,
        result: dict,
    ) -> dict:
        outcome = str(result.get("review_outcome") or "").upper()
        if outcome not in {"APPROVED", "CHANGES_REQUESTED"}:
            return self.record_artifact_review_failure(
                company_id=company_id,
                workspace_id=workspace_id,
                cycle_id=cycle_id,
                request_ref=request_ref,
                code="review_outcome_unverified",
                summary=str(result.get("output") or "")[:1000],
                result=result,
            )
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            review = self._rd_artifact_review(cycle)
            if review and review.get("requestRef") == request_ref and review.get("status") in {"APPROVED", "CHANGES_REQUESTED"}:
                return cycle
            if not review or review.get("requestRef") != request_ref or review.get("status") != "REVIEWING":
                raise TransitionError("Artifact Review is not running")
            reviewer_ref = str(review.get("reviewerEmployeeRef") or "")
            self._rd_review_assignment(context, reviewer_ref)
            at = _now()
            artifact_refs = list(dict.fromkeys(str(item) for item in (result.get("artifact_refs") or []) if item))
            evidence_id = self._insert_runtime_entity(
                conn,
                entity_type="EVIDENCE",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=cycle_id,
                owner_ref=reviewer_ref,
                lifecycle_status="CURRENT",
                blueprint_version=cycle["blueprint_version"],
                verification_status="VERIFIED",
                evidence_condition="CURRENT",
                data={
                    "fixture": False,
                    "source": "RD_ARTIFACT_REVIEW",
                    "status": outcome,
                    "summary": str(result.get("output") or "")[:4000],
                    "requestRef": request_ref,
                    "taskRef": result.get("task_ref"),
                    "sessionRef": result.get("session_ref"),
                    "artifactRefs": artifact_refs,
                    "receivedAt": at,
                },
                at=at,
            )
            self._insert_link(conn, company_id, workspace_id, cycle_id, "HAS_EVIDENCE", evidence_id, at)
            result_refs = [*artifact_refs, evidence_id]
            review = review | {
                "status": outcome,
                "currentExecutorRef": None,
                "reviewTaskRef": result.get("task_ref") or review.get("reviewTaskRef"),
                "sessionRef": result.get("session_ref"),
                "executionBinding": result.get("execution_binding") or {},
                "artifactRefsProduced": artifact_refs,
                "resultRefs": result_refs,
                "computerAccess": result.get("computer_access") or {},
                "summary": str(result.get("output") or "")[:1000],
                "statusHistory": [*review.get("statusHistory", []), {"status": outcome, "at": at}],
                "completedAt": at,
                "updatedAt": at,
            }
            data = cycle["data"] | {
                "artifactReview": review,
                "evidenceRefs": [*cycle["data"].get("evidenceRefs", []), evidence_id],
                "reviewConversation": {
                    "summary": (
                        "审核已通过，研发员工可以继续处理后续工作。"
                        if outcome == "APPROVED"
                        else "审核员工已提出修改意见，原研发负责人继续持有这项责任。"
                    ),
                    "resultRefs": result_refs,
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def record_artifact_review_failure(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        request_ref: str,
        code: str,
        summary: str = "",
        result: dict | None = None,
    ) -> dict:
        result = result or {}
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            review = self._rd_artifact_review(cycle)
            if review and review.get("requestRef") == request_ref and review.get("status") == "FAILED":
                return cycle
            if not review or review.get("requestRef") != request_ref or review.get("status") != "REVIEWING":
                raise TransitionError("Artifact Review is not running")
            at = _now()
            artifact_refs = list(dict.fromkeys(str(item) for item in (result.get("artifact_refs") or []) if item))
            failure = {
                "code": str(code)[:128],
                "summary": str(summary or result.get("error") or "")[:1000],
                "at": at,
                "returnStage": "ARTIFACT_REVIEW",
            }
            evidence_id = self._insert_runtime_entity(
                conn,
                entity_type="EVIDENCE",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=cycle_id,
                owner_ref=str(review.get("reviewerEmployeeRef") or ""),
                lifecycle_status="CURRENT",
                blueprint_version=cycle["blueprint_version"],
                verification_status="VERIFIED" if result.get("task_ref") else "UNVERIFIED",
                evidence_condition="CURRENT",
                data={
                    "fixture": False,
                    "source": "RD_ARTIFACT_REVIEW_FAILURE",
                    "status": "FAILED",
                    "summary": failure["summary"],
                    "requestRef": request_ref,
                    "taskRef": result.get("task_ref") or review.get("reviewTaskRef"),
                    "sessionRef": result.get("session_ref"),
                    "artifactRefs": artifact_refs,
                    "receivedAt": at,
                },
                at=at,
            )
            self._insert_link(conn, company_id, workspace_id, cycle_id, "HAS_EVIDENCE", evidence_id, at)
            result_refs = [*artifact_refs, evidence_id]
            review = review | {
                "status": "FAILED",
                "currentExecutorRef": None,
                "reviewTaskRef": result.get("task_ref") or review.get("reviewTaskRef"),
                "sessionRef": result.get("session_ref"),
                "executionBinding": result.get("execution_binding") or {},
                "artifactRefsProduced": artifact_refs,
                "resultRefs": result_refs,
                "computerAccess": result.get("computer_access") or {},
                "failure": failure,
                "statusHistory": [*review.get("statusHistory", []), {"status": "FAILED", "at": at}],
                "completedAt": at,
                "updatedAt": at,
            }
            data = cycle["data"] | {
                "artifactReview": review,
                "evidenceRefs": [*cycle["data"].get("evidenceRefs", []), evidence_id],
                "reviewConversation": {
                    "summary": "这次代码审核没有完成，失败事实已保留；原研发责任没有转移。",
                    "resultRefs": result_refs,
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def prepare_rd_artifact_revision(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        request_ref: str,
        reason: str,
    ) -> dict:
        request_ref = request_ref.strip()
        reason = reason.strip()
        if not request_ref or not reason:
            raise ValueError("RD revision requires Review ref and reason")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            applied = cycle["data"].get("rdRevisionApplied") or {}
            if applied.get("reviewRequestRef") == request_ref:
                return cycle
            review = self._rd_artifact_review(cycle)
            work_context = cycle["data"].get("workContext") or {}
            if (
                cycle["lifecycle_status"] != "RUNNING"
                or cycle["data"].get("executionStatus") != "COMPLETED"
                or work_context.get("currentExecutorRef")
                or not review
                or review.get("requestRef") != request_ref
                or review.get("status") != "CHANGES_REQUESTED"
            ):
                raise TransitionError("RD revision requires current CHANGES_REQUESTED Review")
            holder_ref = str(work_context.get("responsibilityEmployeeRef") or "")
            if not holder_ref or review.get("originalHolderRef") != holder_ref:
                raise TransitionError("Responsibility Holder changed before RD revision")
            at = _now()
            review_summary = str(review.get("summary") or "").strip()
            instruction = str(cycle["data"].get("instruction") or "").strip()
            data = cycle["data"] | {
                "executionStatus": "READY",
                "instruction": f"{instruction}\n\n根据代码审核修改意见修订：{review_summary}"[:4000],
                "taskHistoryRefs": list(dict.fromkeys(item for item in [
                    *cycle["data"].get("taskHistoryRefs", []),
                    cycle["data"].get("taskRef"),
                ] if item)),
                "artifactHistoryRefs": list(dict.fromkeys([
                    *cycle["data"].get("artifactHistoryRefs", []),
                    *cycle["data"].get("artifactRefs", []),
                ])),
                "resultHistoryRefs": list(dict.fromkeys([
                    *cycle["data"].get("resultHistoryRefs", []),
                    *cycle["data"].get("resultRefs", []),
                ])),
                "artifactReviewHistory": [
                    *cycle["data"].get("artifactReviewHistory", []),
                    review,
                ],
                "artifactReview": None,
                "reviewConversation": None,
                "taskRef": None,
                "sessionRef": None,
                "artifactRefs": [],
                "resultRefs": [],
                "rdRevisionApplied": {
                    "reviewRequestRef": request_ref,
                    "reviewerEmployeeRef": review.get("reviewerEmployeeRef"),
                    "reason": reason[:2000],
                    "at": at,
                },
                "conversation": {
                    "summary": "审核员工提出了修改意见，原研发负责人正在同一责任流中修订。",
                    "resultRefs": list(review.get("resultRefs") or []),
                },
                "workContext": work_context | {
                    "currentExecutorRef": None,
                    "status": "idle",
                    "activity": "等待原研发负责人按审核意见修订",
                    "updatedAt": at,
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    @staticmethod
    def _rd_responsibility_handoff(cycle: dict) -> dict | None:
        handoff = cycle["data"].get("responsibilityHandoff")
        return handoff if isinstance(handoff, dict) else None

    @staticmethod
    def _rd_handoff_target(context: dict, target_employee_ref: str) -> tuple[dict, dict]:
        holder_ref = (context["cycle"]["data"].get("workContext") or {}).get("responsibilityEmployeeRef")
        if not holder_ref or target_employee_ref == holder_ref:
            raise ValueError("Responsibility Handoff requires a distinct target Employee")
        assignment = next(
            (
                (role, employee)
                for role, employee in context["assignments"]
                if employee["entity_id"] == target_employee_ref
            ),
            None,
        )
        if assignment is None:
            raise RuntimeScopeError("Handoff target Employee is outside the current Workspace")
        role, employee = assignment
        if employee["lifecycle_status"] != "AVAILABLE":
            raise TransitionError("Handoff target Employee is not available")
        return role, employee

    def create_rd_responsibility_handoff(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        target_employee_ref: str,
        responsibility_summary: str,
        reason: str,
        next_check_at: str | None = None,
    ) -> dict:
        summary = responsibility_summary.strip()
        reason = reason.strip()
        if not summary or not reason:
            raise ValueError("Responsibility Handoff requires summary and reason")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            work_context = cycle["data"].get("workContext") or {}
            if (
                cycle["lifecycle_status"] != "RUNNING"
                or cycle["data"].get("executionStatus") != "COMPLETED"
                or work_context.get("currentExecutorRef")
            ):
                raise TransitionError("Responsibility Handoff requires completed inactive RD work")
            review = self._rd_artifact_review(cycle)
            if not review or review.get("status") != "APPROVED":
                raise TransitionError("Responsibility Handoff requires an approved Artifact Review")
            existing = self._rd_responsibility_handoff(cycle)
            if existing:
                if existing.get("toEmployeeRef") == target_employee_ref:
                    return cycle
                raise TransitionError("Cycle already has a Responsibility Handoff")
            role, target = self._rd_handoff_target(context, target_employee_ref)
            at = _now()
            handoff_id = self._insert_runtime_entity(
                conn,
                entity_type="HANDOFF",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=cycle_id,
                owner_ref=target["entity_id"],
                lifecycle_status="CREATED",
                org_version=cycle["org_version"],
                blueprint_version=cycle["blueprint_version"],
                data={
                    "kind": "RD_RESPONSIBILITY_TRANSFER",
                    "cycleId": cycle_id,
                    "fromEmployeeRef": work_context["responsibilityEmployeeRef"],
                    "toEmployeeRef": target["entity_id"],
                    "toRoleSlotRef": role["entity_id"],
                    "responsibilitySummary": summary[:1000],
                    "reason": reason[:2000],
                    "nextCheckAt": next_check_at,
                    "contextRefs": list(dict.fromkeys(item for item in [
                        cycle["data"].get("taskRef"),
                        review.get("requestRef"),
                        *review.get("resultRefs", []),
                    ] if item)),
                    "createdAt": at,
                },
                at=at,
            )
            self._insert_link(conn, company_id, workspace_id, cycle_id, "HAS_HANDOFF", handoff_id, at)
            projection = {
                "handoffRef": handoff_id,
                "status": "CREATED",
                "fromEmployeeRef": work_context["responsibilityEmployeeRef"],
                "toEmployeeRef": target["entity_id"],
                "toRoleSlotRef": role["entity_id"],
                "responsibilitySummary": summary[:1000],
                "reason": reason[:2000],
                "nextCheckAt": next_check_at,
                "createdAt": at,
                "updatedAt": at,
            }
            data = cycle["data"] | {"responsibilityHandoff": projection}
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def send_rd_responsibility_handoff(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            projection = self._rd_responsibility_handoff(cycle)
            if not projection:
                raise TransitionError("Cycle has no Responsibility Handoff")
            handoff = self._entity_row(conn, str(projection.get("handoffRef") or ""))
            if handoff["lifecycle_status"] == "SENT":
                return cycle
            if handoff["lifecycle_status"] != "CREATED":
                raise TransitionError("Responsibility Handoff cannot be sent")
            work_context = cycle["data"].get("workContext") or {}
            if work_context.get("responsibilityEmployeeRef") != projection.get("fromEmployeeRef"):
                raise TransitionError("Responsibility Holder changed before Handoff was sent")
            at = _now()
            self._record_path(
                conn,
                machine_name="handoff",
                entity_id=handoff["entity_id"],
                source="CREATED",
                steps=[("SENT", "SYSTEM", "send", {"cycleId": cycle_id})],
                company_id=company_id,
                workspace_id=workspace_id,
                reason=str(projection.get("reason") or ""),
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = 'SENT', updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'CREATED'",
                (at, self.tenant_id, handoff["entity_id"]),
            )
            projection = projection | {"status": "SENT", "sentAt": at, "updatedAt": at}
            data = cycle["data"] | {"responsibilityHandoff": projection}
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def respond_rd_responsibility_handoff(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        decision: str,
        reason: str,
        provider_ack: dict | None = None,
    ) -> dict:
        decision = decision.upper()
        reason = reason.strip()
        if decision not in {"ACKNOWLEDGE", "RETURN", "REJECT"} or not reason:
            raise ValueError("Responsibility Handoff response is invalid")
        terminal = {"ACKNOWLEDGE": "COMPLETED", "RETURN": "RETURNED", "REJECT": "REJECTED"}[decision]
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            projection = self._rd_responsibility_handoff(cycle)
            if not projection:
                raise TransitionError("Cycle has no Responsibility Handoff")
            handoff = self._entity_row(conn, str(projection.get("handoffRef") or ""))
            if handoff["lifecycle_status"] == terminal:
                return cycle
            if handoff["lifecycle_status"] != "SENT":
                raise TransitionError("Responsibility Handoff is not awaiting response")
            work_context = cycle["data"].get("workContext") or {}
            if work_context.get("responsibilityEmployeeRef") != projection.get("fromEmployeeRef"):
                raise TransitionError("Responsibility Holder changed before Handoff response")
            if provider_ack is not None and (
                decision != "ACKNOWLEDGE"
                or provider_ack.get("verification_status") != "VERIFIED"
                or provider_ack.get("handoff_ref") != handoff["entity_id"]
                or provider_ack.get("ack_actor_ref") != projection.get("toEmployeeRef")
            ):
                raise TransitionError("Provider-native Handoff ACK is not verified")
            at = _now()
            if decision == "ACKNOWLEDGE":
                self._rd_handoff_target(context, str(projection.get("toEmployeeRef") or ""))
                steps = [
                    ("ACKNOWLEDGED", "AI_EMPLOYEE", "acknowledge", {"cycleId": cycle_id}),
                    ("COMPLETED", "AI_EMPLOYEE", "complete", {"cycleId": cycle_id}),
                ]
            else:
                steps = [(terminal, "AI_EMPLOYEE", decision.lower(), {"cycleId": cycle_id})]
            self._record_path(
                conn,
                machine_name="handoff",
                entity_id=handoff["entity_id"],
                source="SENT",
                steps=steps,
                company_id=company_id,
                workspace_id=workspace_id,
                reason=reason,
            )
            handoff_data = handoff["data"] | {
                "decision": decision,
                "responseReason": reason[:2000],
                "respondedAt": at,
            }
            if provider_ack is not None:
                handoff_data["providerAck"] = provider_ack
            conn.execute(
                "update runtime_entities set lifecycle_status = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'SENT'",
                (terminal, json.dumps(handoff_data, ensure_ascii=False), at, self.tenant_id, handoff["entity_id"]),
            )
            if decision == "ACKNOWLEDGE":
                work_context = work_context | {
                    "responsibilityEmployeeRef": projection["toEmployeeRef"],
                    "responsibilityRoleSlotRef": projection["toRoleSlotRef"],
                    "currentExecutorRef": None,
                    "status": "idle",
                    "activity": f"已接管：{projection['responsibilitySummary']}",
                    "updatedAt": at,
                }
                summary = "责任交接已完成；接收员工已成为负责人，当前尚未开始执行。"
            else:
                work_context = work_context | {
                    "currentExecutorRef": None,
                    "activity": "责任交接被退回，原负责人继续持有这项责任。",
                    "updatedAt": at,
                }
                summary = "责任交接未生效；原负责人继续持有这项责任。"
            projection = projection | {
                "status": terminal,
                "decision": decision,
                "responseReason": reason[:2000],
                "respondedAt": at,
                "updatedAt": at,
            }
            if provider_ack is not None:
                projection["providerAck"] = provider_ack
            data = cycle["data"] | {
                "responsibilityHandoff": projection,
                "responsibilityHandoffRefs": list(dict.fromkeys([
                    *cycle["data"].get("responsibilityHandoffRefs", []),
                    handoff["entity_id"],
                ])),
                "workContext": work_context,
                "conversation": {
                    "summary": summary,
                    "resultRefs": [handoff["entity_id"]],
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    @staticmethod
    def _rd_decision_provenance(value: object) -> str:
        if not isinstance(value, dict):
            raise ValueError("Decision fact requires value and provenance")
        provenance = str(value.get("provenance") or "").upper()
        if provenance not in {"FACT", "POLICY", "EVIDENCE", "EST", "UNK"}:
            raise ValueError("Decision provenance is invalid")
        if not str(value.get("value") or "").strip():
            raise ValueError("Decision fact value is required")
        return provenance

    def create_rd_decision_packet(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        packet: dict,
    ) -> dict:
        decision_key = str(packet.get("decisionKey") or "").strip()
        event = str(packet.get("event") or "").strip()
        cannot_decide = str(packet.get("cannotDecideReason") or "").strip()
        choice_prompt = str(packet.get("ceoChoicePrompt") or "").strip()
        continuation_plan = str(packet.get("continuationPlan") or "").strip()
        options = packet.get("options")
        recommendation = packet.get("recommendation")
        recommendation_reason = packet.get("recommendationReason")
        if not all((decision_key, event, cannot_decide, choice_prompt, continuation_plan)):
            raise ValueError("RD Decision Packet is incomplete")
        if not isinstance(options, list) or not 2 <= len(options) <= 4:
            raise ValueError("RD Decision Packet requires two to four options")
        option_ids: set[str] = set()
        normalized_options = []
        for option in options:
            if not isinstance(option, dict):
                raise ValueError("Decision option must be an object")
            option_id = str(option.get("optionId") or "").strip()
            label = str(option.get("label") or "").strip()
            instruction = str(option.get("continuationInstruction") or "").strip()
            resource_refs = [str(item).strip() for item in (option.get("resourceRefs") or []) if str(item).strip()]
            test_command = [str(item) for item in (option.get("testCommand") or []) if str(item)]
            if not option_id or option_id in option_ids or not label or not instruction or not resource_refs or not test_command:
                raise ValueError("Decision option execution boundary is incomplete")
            option_ids.add(option_id)
            for field in ("impact", "risk", "cost"):
                self._rd_decision_provenance(option.get(field))
            normalized_options.append({
                "optionId": option_id,
                "label": label,
                "impact": option["impact"],
                "risk": option["risk"],
                "cost": option["cost"],
                "continuationInstruction": instruction,
                "resourceRefs": resource_refs,
                "testCommand": test_command,
            })
        if not isinstance(recommendation, dict) or str(recommendation.get("optionId") or "") not in option_ids:
            raise ValueError("Decision recommendation must reference an option")
        self._rd_decision_provenance({
            "value": recommendation.get("optionId"),
            "provenance": recommendation.get("provenance"),
        })
        self._rd_decision_provenance(recommendation_reason)

        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            work_context = cycle["data"].get("workContext") or {}
            if (
                cycle["lifecycle_status"] != "RUNNING"
                or cycle["data"].get("executionStatus") != "COMPLETED"
                or work_context.get("currentExecutorRef")
            ):
                raise TransitionError("RD Decision requires completed inactive work")
            review = self._rd_artifact_review(cycle)
            if not review or review.get("status") != "APPROVED" or not cycle["data"].get("evidenceRefs"):
                raise TransitionError("RD Decision requires approved reviewed Evidence")
            existing_id = cycle["data"].get("rdDecisionPacketRef")
            if existing_id:
                existing = self._entity_row(conn, existing_id)
                if existing["data"].get("decisionKey") == decision_key:
                    return cycle
                raise TransitionError("Cycle already has an RD Decision Packet")
            at = _now()
            decision_id = self._insert_runtime_entity(
                conn,
                entity_type="DECISION_PACKET",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=cycle_id,
                owner_ref="CEO",
                lifecycle_status="DRAFT",
                blueprint_version=cycle["blueprint_version"],
                data={
                    "kind": "RD_HIGH_RISK_CHANGE",
                    "decisionKey": decision_key,
                    "cycleId": cycle_id,
                    "complexity": "HIGH_RISK",
                    "layer0Actions": ["VIEW_OPTIONS", "DEFER"],
                    "event": event,
                    "cannotDecideReason": cannot_decide,
                    "options": normalized_options,
                    "recommendation": recommendation,
                    "recommendationReason": recommendation_reason,
                    "ceoChoicePrompt": choice_prompt,
                    "continuationPlan": continuation_plan,
                    "evidenceRefs": list(dict.fromkeys(cycle["data"].get("evidenceRefs") or [])),
                    "responsibilityHolderRef": work_context.get("responsibilityEmployeeRef"),
                    "createdAt": at,
                },
                at=at,
            )
            self._record_path(
                conn,
                machine_name="decision_packet",
                entity_id=decision_id,
                source="DRAFT",
                steps=[
                    ("READY", "SYSTEM", "prepare", {"cycleId": cycle_id}),
                    ("WAITING_CEO", "SYSTEM", "request_decision", {"cycleId": cycle_id}),
                ],
                company_id=company_id,
                workspace_id=workspace_id,
                reason=cannot_decide,
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = 'WAITING_CEO', updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'DRAFT'",
                (at, self.tenant_id, decision_id),
            )
            self._insert_link(conn, company_id, workspace_id, cycle_id, "HAS_DECISION", decision_id, at)
            data = cycle["data"] | {
                "rdDecisionPacketRef": decision_id,
                "decisionConversation": {
                    "summary": event,
                    "resultRefs": [decision_id],
                },
                "workContext": work_context | {
                    "currentExecutorRef": None,
                    "status": "needs_ceo",
                    "activity": event[:240],
                    "updatedAt": at,
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def review_rd_decision_packet(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            decision = self._entity_row(conn, str(cycle["data"].get("rdDecisionPacketRef") or ""))
            if decision["lifecycle_status"] != "WAITING_CEO":
                if decision["data"].get("layer1ReviewedAt"):
                    return cycle
                raise TransitionError("RD Decision Package is not available for review")
            if decision["data"].get("layer1ReviewedAt"):
                return cycle
            at = _now()
            decision_data = decision["data"] | {"layer1ReviewedAt": at}
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'WAITING_CEO'",
                (json.dumps(decision_data, ensure_ascii=False), at, self.tenant_id, decision["entity_id"]),
            )
        return self.foundation.get(cycle_id)

    def apply_rd_decision_choice(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        choice: str,
        reason: str,
        next_check_at: str | None = None,
    ) -> dict:
        choice = choice.strip()
        reason = reason.strip()
        if not choice or not reason:
            raise ValueError("RD Decision choice and reason are required")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            decision = self._entity_row(conn, str(cycle["data"].get("rdDecisionPacketRef") or ""))
            if decision["lifecycle_status"] == "APPLIED":
                if decision["data"].get("choice") == choice:
                    return cycle
                raise TransitionError("RD Decision already applied with another choice")
            if decision["lifecycle_status"] != "WAITING_CEO":
                raise TransitionError("RD Decision is not awaiting CEO")
            at = _now()
            if choice == "DEFER":
                decision_data = decision["data"] | {
                    "deferredAt": at,
                    "deferReason": reason[:2000],
                    "nextCheckAt": next_check_at,
                }
                conn.execute(
                    "update runtime_entities set data_json = ?, next_check_at = ?, updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'WAITING_CEO'",
                    (json.dumps(decision_data, ensure_ascii=False), next_check_at, at, self.tenant_id, decision["entity_id"]),
                )
                return cycle
            if not decision["data"].get("layer1ReviewedAt"):
                raise TransitionError("High-risk RD Decision requires Layer 1 review")
            selected = next(
                (item for item in decision["data"].get("options", []) if item.get("optionId") == choice),
                None,
            )
            if selected is None:
                raise ValueError("RD Decision choice is not an available option")
            holder_ref = (cycle["data"].get("workContext") or {}).get("responsibilityEmployeeRef")
            if holder_ref != decision["data"].get("responsibilityHolderRef"):
                raise TransitionError("Responsibility Holder changed while Decision was pending")
            self._record_path(
                conn,
                machine_name="decision_packet",
                entity_id=decision["entity_id"],
                source="WAITING_CEO",
                steps=[
                    ("DECIDED", "CEO", "decide", {"choice": choice}),
                    ("APPLIED", "SYSTEM", "apply", {"cycleId": cycle_id, "choice": choice}),
                ],
                company_id=company_id,
                workspace_id=workspace_id,
                reason=reason,
            )
            decision_data = decision["data"] | {
                "choice": choice,
                "choiceReason": reason[:2000],
                "decidedAt": at,
                "appliedAt": at,
            }
            conn.execute(
                "update runtime_entities set lifecycle_status = 'APPLIED', data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'WAITING_CEO'",
                (json.dumps(decision_data, ensure_ascii=False), at, self.tenant_id, decision["entity_id"]),
            )
            previous_review = self._rd_artifact_review(cycle)
            data = cycle["data"] | {
                "executionStatus": "READY",
                "instruction": selected["continuationInstruction"],
                "resourceRefs": selected["resourceRefs"],
                "testCommand": selected["testCommand"],
                "taskHistoryRefs": list(dict.fromkeys(item for item in [
                    *cycle["data"].get("taskHistoryRefs", []),
                    cycle["data"].get("taskRef"),
                ] if item)),
                "artifactHistoryRefs": list(dict.fromkeys([
                    *cycle["data"].get("artifactHistoryRefs", []),
                    *cycle["data"].get("artifactRefs", []),
                ])),
                "resultHistoryRefs": list(dict.fromkeys([
                    *cycle["data"].get("resultHistoryRefs", []),
                    *cycle["data"].get("resultRefs", []),
                ])),
                "artifactReviewHistory": [
                    *cycle["data"].get("artifactReviewHistory", []),
                    *([previous_review] if previous_review else []),
                ],
                "artifactReview": None,
                "reviewConversation": None,
                "taskRef": None,
                "sessionRef": None,
                "artifactRefs": [],
                "resultRefs": [],
                "rdDecisionApplied": {
                    "decisionRef": decision["entity_id"],
                    "choice": choice,
                    "at": at,
                },
                "conversation": {
                    "summary": decision["data"]["continuationPlan"],
                    "resultRefs": [decision["entity_id"]],
                },
                "workContext": (cycle["data"].get("workContext") or {}) | {
                    "currentExecutorRef": None,
                    "status": "idle",
                    "activity": decision["data"]["continuationPlan"][:240],
                    "updatedAt": at,
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def reconcile_interrupted_rd_executions(self) -> list[str]:
        """Fail closed for RD executions that no longer have an owning Runtime process."""
        with self.db.connect() as conn:
            rows = conn.execute(
                "select tenant_id, company_id, workspace_id, entity_id, data_json "
                "from runtime_entities where entity_type = 'CYCLE' and execution_ref = 'rd_task:auto' "
                "and lifecycle_status = 'RUNNING'"
            ).fetchall()
        interrupted = []
        for row in rows:
            data = json.loads(row["data_json"] or "{}")
            with TenantContext.scope(row["tenant_id"], company_id=row["company_id"], role="system"):
                if data.get("executionStatus") == "RUNNING":
                    self.record_operating_cycle_failure(
                        company_id=row["company_id"],
                        workspace_id=row["workspace_id"],
                        cycle_id=row["entity_id"],
                        code="execution_interrupted_unverified",
                        summary="Runtime 重启后无法确认外部 Agent 仍在执行。",
                    )
                    interrupted.append(row["entity_id"])
                    continue
                review = data.get("artifactReview")
                if isinstance(review, dict) and review.get("status") == "REVIEWING":
                    self.record_artifact_review_failure(
                        company_id=row["company_id"],
                        workspace_id=row["workspace_id"],
                        cycle_id=row["entity_id"],
                        request_ref=str(review.get("requestRef") or ""),
                        code="review_interrupted_unverified",
                        summary="Runtime 重启后无法确认审核 Agent 仍在执行。",
                    )
                    interrupted.append(row["entity_id"])
        return interrupted

    def get_operating_cycle(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        states: set[str] | None = None,
    ) -> dict:
        with self.db.connect() as conn:
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
        if states and context["cycle"]["lifecycle_status"] not in states:
            raise TransitionError("Operating Cycle is not in the required state")
        return context["cycle"]

    def record_operating_cycle_execution(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        result: dict,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            if cycle["lifecycle_status"] != "RUNNING":
                if cycle["data"].get("acceptanceId"):
                    return self.foundation.get(cycle_id)
                raise TransitionError("Cycle is not running")
            if cycle.get("execution_ref") == "rd_task:auto":
                return self._record_rd_execution_result(
                    conn, context=context, cycle=cycle, result=result,
                )
            if cycle["data"].get("acceptanceId"):
                return self.foundation.get(cycle_id)
            if any(employee["lifecycle_status"] != "OPERATING" for _, employee in context["assignments"]):
                raise TransitionError("Operating team changed before execution result was recorded")
            at = _now()
            summary = str(result.get("output") or "")[:4000]
            evidence_id = self._insert_runtime_entity(
                conn,
                entity_type="EVIDENCE",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=cycle_id,
                owner_ref="AI Team",
                lifecycle_status="CURRENT",
                blueprint_version=cycle["blueprint_version"],
                verification_status="UNVERIFIED",
                evidence_condition="CURRENT",
                data={
                    "fixture": False,
                    "source": "AI_EXECUTION",
                    "executionRef": cycle["execution_ref"],
                    "status": "UNVERIFIED",
                    "summary": summary,
                    "receivedAt": at,
                },
                at=at,
            )
            handoff_id = self._insert_runtime_entity(
                conn,
                entity_type="HANDOFF",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=cycle_id,
                owner_ref="CEO",
                lifecycle_status="CREATED",
                org_version=context["org_version"],
                blueprint_version=cycle["blueprint_version"],
                data={
                    "kind": "RESULT_OUTPUT",
                    "cycleId": cycle_id,
                    "fromRole": "AI Team",
                    "toRole": "CEO",
                    "inputRefs": [cycle["execution_ref"]],
                    "outputRefs": [evidence_id],
                    "evidenceRefs": [evidence_id],
                    "acknowledgement": "WAITING_CEO",
                    "actor": "AI_EMPLOYEE",
                    "at": at,
                },
                at=at,
            )
            self._record_path(
                conn, machine_name="handoff", entity_id=handoff_id, source="CREATED",
                steps=[("SENT", "AI_EMPLOYEE", "send", {"cycleId": cycle_id, "evidenceRefs": [evidence_id]})],
                company_id=company_id, workspace_id=workspace_id, reason="AI 团队提交运行结果给 CEO",
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = 'SENT', updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'CREATED'",
                (at, self.tenant_id, handoff_id),
            )
            acceptance_id = self._insert_runtime_entity(
                conn,
                entity_type="ACCEPTANCE",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=cycle_id,
                owner_ref="CEO",
                lifecycle_status="PENDING",
                blueprint_version=cycle["blueprint_version"],
                data={
                    "cycleId": cycle_id,
                    "criteria": [cycle["data"].get("outcomeRef")],
                    "evidenceRefs": [evidence_id],
                    "decision": "PENDING",
                    "nextAction": "CEO_REVIEW",
                },
                at=at,
            )
            for relation, target in (
                ("HAS_EVIDENCE", evidence_id), ("HAS_HANDOFF", handoff_id), ("HAS_ACCEPTANCE", acceptance_id),
            ):
                self._insert_link(conn, company_id, workspace_id, cycle_id, relation, target, at)
            self._insert_link(conn, company_id, workspace_id, evidence_id, "HAS_ACCEPTANCE", acceptance_id, at)
            self._record_path(
                conn, machine_name="cycle", entity_id=cycle_id, source="RUNNING",
                steps=[("WAITING_CEO", "SYSTEM", "request_acceptance", {"acceptanceId": acceptance_id})],
                company_id=company_id, workspace_id=workspace_id, reason="真实执行结果等待 CEO 验收",
            )
            data = cycle["data"] | {
                "evidenceRefs": [*cycle["data"].get("evidenceRefs", []), evidence_id],
                "outputHandoffId": handoff_id,
                "acceptanceId": acceptance_id,
                "executionStatus": "COMPLETED_UNVERIFIED",
                "executionReceivedAt": at,
            }
            conn.execute(
                "update runtime_entities set lifecycle_status = 'WAITING_CEO', data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
            for _, employee in context["assignments"]:
                conn.execute(
                    "update runtime_entities set presence_state = 'WAITING_CEO', updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'OPERATING'",
                    (at, self.tenant_id, employee["entity_id"]),
                )
        return self.foundation.get(cycle_id)

    def _record_rd_execution_result(self, conn, *, context: dict, cycle: dict, result: dict) -> dict:
        if cycle["data"].get("executionStatus") == "COMPLETED":
            return cycle
        if cycle["data"].get("executionStatus") != "RUNNING":
            raise TransitionError("RD Task is not running")
        _, employee, _, _ = self._rd_execution_assignment(context)
        if employee["lifecycle_status"] != "OPERATING":
            raise TransitionError("RD executor is not active")
        at = _now()
        artifact_refs = list(dict.fromkeys(str(item) for item in (result.get("artifact_refs") or []) if item))
        changed_files = list(dict.fromkeys(str(item) for item in (result.get("changed_files") or []) if item))
        test_result = result.get("test_result") if isinstance(result.get("test_result"), dict) else {}
        evidence_id = self._insert_runtime_entity(
            conn,
            entity_type="EVIDENCE",
            company_id=cycle["company_id"],
            workspace_id=cycle["workspace_id"],
            parent_id=cycle["entity_id"],
            owner_ref=employee["entity_id"],
            lifecycle_status="CURRENT",
            blueprint_version=cycle["blueprint_version"],
            verification_status="VERIFIED",
            evidence_condition="CURRENT",
            data={
                "fixture": False,
                "source": "RD_EXECUTION_VERIFICATION",
                "status": "VERIFIED",
                "summary": str(result.get("output") or "")[:1000],
                "taskRef": result.get("task_ref"),
                "sessionRef": result.get("session_ref"),
                "artifactRefs": artifact_refs,
                "changedFiles": changed_files,
                "testResult": test_result,
                "receivedAt": at,
            },
            at=at,
        )
        self._insert_link(
            conn, cycle["company_id"], cycle["workspace_id"],
            cycle["entity_id"], "HAS_EVIDENCE", evidence_id, at,
        )
        self._record_path(
            conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="OPERATING",
            steps=[("AVAILABLE", "AI_EMPLOYEE", "complete_responsibility", {"cycleId": cycle["entity_id"]})],
            company_id=cycle["company_id"], workspace_id=cycle["workspace_id"],
            reason="真实研发 Task 已结束，Employee 退出 Current Executor",
        )
        conn.execute(
            "update runtime_entities set lifecycle_status = 'AVAILABLE', presence_state = 'IDLE', updated_at = ? "
            "where tenant_id = ? and entity_id = ? and lifecycle_status = 'OPERATING'",
            (at, self.tenant_id, employee["entity_id"]),
        )
        result_refs = [*artifact_refs, evidence_id]
        binding = (cycle["data"].get("executionBinding") or {}) | (result.get("execution_binding") or {})
        data = cycle["data"] | {
            "executionStatus": "COMPLETED",
            "executionReceivedAt": at,
            "taskRef": result.get("task_ref"),
            "sessionRef": result.get("session_ref"),
            "artifactRefs": artifact_refs,
            "evidenceRefs": [*cycle["data"].get("evidenceRefs", []), evidence_id],
            "resultRefs": result_refs,
            "changedFiles": changed_files,
            "testResult": test_result,
            "computerAccess": result.get("computer_access") or {},
            "executionBinding": binding,
            "conversation": {
                "summary": str(result.get("conversation_summary") or "代码修改已经完成，验证结果已保存。")[:500],
                "resultRefs": result_refs,
            },
            "workContext": (cycle["data"].get("workContext") or {}) | {
                "currentExecutorRef": None,
                "status": "completed",
                "activity": "真实执行已结束，结果可回访",
                "updatedAt": at,
            },
            "completedAt": at,
        }
        conn.execute(
            "update runtime_entities set data_json = ?, updated_at = ? "
            "where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
            (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle["entity_id"]),
        )
        return self._entity_row(conn, cycle["entity_id"])

    def record_operating_cycle_failure(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        code: str,
        summary: str = "",
        result: dict | None = None,
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            if cycle["lifecycle_status"] == "PAUSED" and cycle["data"].get("executionStatus") == "FAILED":
                return self.foundation.get(cycle_id)
            if cycle["lifecycle_status"] != "RUNNING":
                raise TransitionError("Cycle is not running")
            if cycle.get("execution_ref") == "rd_task:auto":
                return self._record_rd_execution_failure(
                    conn, context=context, cycle=cycle, code=code,
                    summary=summary, result=result or {},
                )
            at = _now()
            failure = {
                "failureId": f"failure-{uuid4()}",
                "kind": "AI_EXECUTION",
                "code": str(code)[:128],
                "summary": str(summary)[:1000],
                "occurredAt": at,
                "recoveryPath": "CEO_RESUME_AFTER_FIX",
            }
            self._record_path(
                conn, machine_name="cycle", entity_id=cycle_id, source="RUNNING",
                steps=[("PAUSED", "SYSTEM", "pause", {"failureId": failure["failureId"]})],
                company_id=company_id, workspace_id=workspace_id, reason="AI 执行失败，Cycle 已暂停",
            )
            data = cycle["data"] | {
                "executionStatus": "FAILED",
                "failureEvents": [*cycle["data"].get("failureEvents", []), failure],
            }
            conn.execute(
                "update runtime_entities set lifecycle_status = 'PAUSED', exception_status = 'FAILED', "
                "data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
            for _, employee in context["assignments"]:
                if employee["lifecycle_status"] != "OPERATING":
                    raise TransitionError("Operating team changed during execution failure")
                self._record_path(
                    conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="OPERATING",
                    steps=[("DEGRADED", "SYSTEM", "execution_degraded", {"failureId": failure["failureId"]})],
                    company_id=company_id, workspace_id=workspace_id, reason="当前责任执行失败",
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'DEGRADED', presence_state = 'BLOCKED', "
                    "updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'OPERATING'",
                    (at, self.tenant_id, employee["entity_id"]),
                )
        return self.foundation.get(cycle_id)

    def _record_rd_execution_failure(
        self, conn, *, context: dict, cycle: dict, code: str, summary: str, result: dict,
    ) -> dict:
        _, employee, _, _ = self._rd_execution_assignment(context)
        if employee["lifecycle_status"] != "OPERATING":
            raise TransitionError("RD executor changed during execution failure")
        at = _now()
        artifact_refs = list(dict.fromkeys(str(item) for item in (result.get("artifact_refs") or []) if item))
        changed_files = list(dict.fromkeys(str(item) for item in (result.get("changed_files") or []) if item))
        test_result = result.get("test_result") if isinstance(result.get("test_result"), dict) else {}
        failure = {
            "failureId": f"failure-{uuid4()}",
            "kind": "RD_TASK_EXECUTION",
            "code": str(code)[:128],
            "summary": str(summary or result.get("error") or "")[:1000],
            "occurredAt": at,
            "recoveryPath": "RETRY_SAME_CYCLE_AFTER_FIX",
        }
        evidence_id = self._insert_runtime_entity(
            conn,
            entity_type="EVIDENCE",
            company_id=cycle["company_id"],
            workspace_id=cycle["workspace_id"],
            parent_id=cycle["entity_id"],
            owner_ref=employee["entity_id"],
            lifecycle_status="CURRENT",
            blueprint_version=cycle["blueprint_version"],
            verification_status="VERIFIED" if test_result else "UNVERIFIED",
            evidence_condition="CURRENT",
            data={
                "fixture": False,
                "source": "RD_EXECUTION_FAILURE",
                "status": "FAILED",
                "summary": failure["summary"],
                "taskRef": result.get("task_ref"),
                "sessionRef": result.get("session_ref"),
                "artifactRefs": artifact_refs,
                "changedFiles": changed_files,
                "testResult": test_result,
                "receivedAt": at,
            },
            at=at,
        )
        self._insert_link(
            conn, cycle["company_id"], cycle["workspace_id"],
            cycle["entity_id"], "HAS_EVIDENCE", evidence_id, at,
        )
        self._record_path(
            conn, machine_name="cycle", entity_id=cycle["entity_id"], source="RUNNING",
            steps=[("PAUSED", "SYSTEM", "pause", {"failureId": failure["failureId"]})],
            company_id=cycle["company_id"], workspace_id=cycle["workspace_id"],
            reason="真实研发执行失败，Cycle 已暂停",
        )
        self._record_path(
            conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="OPERATING",
            steps=[("DEGRADED", "SYSTEM", "execution_degraded", {"failureId": failure["failureId"]})],
            company_id=cycle["company_id"], workspace_id=cycle["workspace_id"],
            reason="当前研发 Task 执行失败",
        )
        conn.execute(
            "update runtime_entities set lifecycle_status = 'DEGRADED', presence_state = 'BLOCKED', updated_at = ? "
            "where tenant_id = ? and entity_id = ? and lifecycle_status = 'OPERATING'",
            (at, self.tenant_id, employee["entity_id"]),
        )
        result_refs = [*artifact_refs, evidence_id]
        data = cycle["data"] | {
            "executionStatus": "FAILED",
            "taskRef": result.get("task_ref"),
            "sessionRef": result.get("session_ref"),
            "artifactRefs": artifact_refs,
            "evidenceRefs": [*cycle["data"].get("evidenceRefs", []), evidence_id],
            "resultRefs": result_refs,
            "changedFiles": changed_files,
            "testResult": test_result,
            "computerAccess": result.get("computer_access") or {},
            "executionBinding": (cycle["data"].get("executionBinding") or {}) | (result.get("execution_binding") or {}),
            "failureEvents": [*cycle["data"].get("failureEvents", []), failure],
            "conversation": {
                "summary": "这次执行没有通过验证，代码变化和失败证据已保留。",
                "resultRefs": result_refs,
            },
            "workContext": (cycle["data"].get("workContext") or {}) | {
                "currentExecutorRef": None,
                "status": "failed",
                "activity": "执行失败，保留原责任与恢复位置",
                "updatedAt": at,
            },
        }
        conn.execute(
            "update runtime_entities set lifecycle_status = 'PAUSED', exception_status = 'FAILED', "
            "data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'RUNNING'",
            (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle["entity_id"]),
        )
        return self._entity_row(conn, cycle["entity_id"])

    def resume_operating_cycle(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        reason: str,
    ) -> dict:
        reason = reason.strip()
        if not reason:
            raise ValueError("Cycle recovery requires a reason")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            if cycle["lifecycle_status"] == "RUNNING" and cycle["data"].get("executionStatus") == "READY":
                return self.foundation.get(cycle_id)
            if cycle["lifecycle_status"] != "PAUSED" or cycle["data"].get("executionStatus") != "FAILED":
                raise TransitionError("Cycle has no recoverable execution failure")
            is_rd_execution = cycle.get("execution_ref") == "rd_task:auto"
            if is_rd_execution:
                recovery_employees = [self._rd_execution_assignment(context)[1]]
            else:
                recovery_employees = [employee for _, employee in context["assignments"]]
            if any(employee["lifecycle_status"] != "DEGRADED" for employee in recovery_employees):
                raise TransitionError("Operating team is not recoverable")
            at = _now()
            for employee in recovery_employees:
                employee_steps = [("AVAILABLE", "SYSTEM", "gap_resolved", {"cycleId": cycle_id})]
                if not is_rd_execution:
                    employee_steps.append(("OPERATING", "AI_EMPLOYEE", "accept_handoff", {"cycleId": cycle_id}))
                target = self._record_path(
                    conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="DEGRADED",
                    steps=employee_steps,
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = ?, presence_state = ?, updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'DEGRADED'",
                    (target, "IDLE" if is_rd_execution else "RUNNING", at, self.tenant_id, employee["entity_id"]),
                )
            self._record_path(
                conn, machine_name="cycle", entity_id=cycle_id, source="PAUSED",
                steps=[("RUNNING", "CEO", "resume", {"cycleId": cycle_id})],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            failures = list(cycle["data"].get("failureEvents", []))
            if failures:
                failures[-1] = failures[-1] | {"resolvedAt": at, "resolution": reason}
            data = cycle["data"] | {"executionStatus": "READY", "failureEvents": failures}
            if is_rd_execution:
                data |= {
                    "taskHistoryRefs": list(dict.fromkeys(item for item in [
                        *cycle["data"].get("taskHistoryRefs", []),
                        cycle["data"].get("taskRef"),
                    ] if item)),
                    "artifactHistoryRefs": list(dict.fromkeys([
                        *cycle["data"].get("artifactHistoryRefs", []),
                        *cycle["data"].get("artifactRefs", []),
                    ])),
                    "resultHistoryRefs": list(dict.fromkeys([
                        *cycle["data"].get("resultHistoryRefs", []),
                        *cycle["data"].get("resultRefs", []),
                    ])),
                    "taskRef": None,
                    "sessionRef": None,
                    "artifactRefs": [],
                    "resultRefs": [],
                    "executionBinding": {
                        key: value
                        for key, value in (cycle["data"].get("executionBinding") or {}).items()
                        if key != "taskRef"
                    },
                    "workContext": (cycle["data"].get("workContext") or {}) | {
                        "currentExecutorRef": None,
                        "status": "idle",
                        "activity": "失败事实已保留，等待重新执行",
                        "updatedAt": at,
                    },
                }
            conn.execute(
                "update runtime_entities set lifecycle_status = 'RUNNING', exception_status = 'NONE', "
                "data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'PAUSED'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def review_operating_cycle(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        decision: str,
        evidence_refs: list[str],
        reason: str,
    ) -> dict:
        choice = decision.upper()
        if choice not in {"ACCEPT", "REJECT"} or not reason.strip():
            raise ValueError("Cycle review requires ACCEPT or REJECT and a reason")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            recorded = cycle["data"].get("acceptanceDecision")
            if recorded:
                if recorded.get("decision") == choice:
                    return self.foundation.get(cycle_id)
                raise TransitionError("Cycle already has another Acceptance decision")
            if cycle["lifecycle_status"] != "WAITING_CEO":
                raise TransitionError("Cycle is not waiting for CEO Acceptance")
            acceptance_id = cycle["data"].get("acceptanceId")
            handoff_id = cycle["data"].get("outputHandoffId")
            expected_refs = list(dict.fromkeys(cycle["data"].get("evidenceRefs", [])))
            refs = list(dict.fromkeys(evidence_refs))
            if not acceptance_id or not handoff_id or (choice == "ACCEPT" and (not refs or set(refs) != set(expected_refs))):
                raise ValueError("Acceptance requires the complete current Evidence set")
            acceptance = self._entity_row(conn, acceptance_id)
            handoff = self._entity_row(conn, handoff_id)
            if acceptance["parent_id"] != cycle_id or handoff["parent_id"] != cycle_id:
                raise RuntimeScopeError("Acceptance or Handoff is outside the current Cycle")
            for evidence_id in refs:
                evidence = self._entity_row(conn, evidence_id)
                if evidence["entity_type"] != "EVIDENCE" or evidence["parent_id"] != cycle_id:
                    raise RuntimeScopeError("Evidence is outside the current Cycle")
            at = _now()
            if choice == "ACCEPT":
                self._record_path(
                    conn, machine_name="acceptance", entity_id=acceptance_id, source="PENDING",
                    steps=[("ACCEPTED", "CEO", "accept", {"cycleId": cycle_id, "evidenceRefs": refs})],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                self._record_path(
                    conn, machine_name="handoff", entity_id=handoff_id, source="SENT",
                    steps=[
                        ("ACKNOWLEDGED", "CEO", "acknowledge", {"cycleId": cycle_id}),
                        ("COMPLETED", "CEO", "complete", {"cycleId": cycle_id}),
                    ],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                self._record_path(
                    conn, machine_name="cycle", entity_id=cycle_id, source="WAITING_CEO",
                    steps=[("ACCEPTED", "CEO", "accept", {"acceptanceId": acceptance_id})],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'ACCEPTED', data_json = json_set(data_json, '$.decision', 'ACCEPT', '$.reason', ?, '$.decidedAt', ?), updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'PENDING'",
                    (reason.strip(), at, at, self.tenant_id, acceptance_id),
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'COMPLETED', data_json = json_set(data_json, '$.acknowledgement', 'CEO_ACCEPTED'), updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'SENT'",
                    (at, self.tenant_id, handoff_id),
                )
                for evidence_id in refs:
                    conn.execute(
                        "update runtime_entities set verification_status = 'VERIFIED', updated_at = ? "
                        "where tenant_id = ? and entity_id = ? and verification_status = 'UNVERIFIED'",
                        (at, self.tenant_id, evidence_id),
                    )
                target_status = "ACCEPTED"
            else:
                self._record_path(
                    conn, machine_name="acceptance", entity_id=acceptance_id, source="PENDING",
                    steps=[("REJECTED", "CEO", "reject", {"cycleId": cycle_id})],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                self._record_path(
                    conn, machine_name="handoff", entity_id=handoff_id, source="SENT",
                    steps=[("REJECTED", "CEO", "reject", {"cycleId": cycle_id})],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                self._record_path(
                    conn, machine_name="cycle", entity_id=cycle_id, source="WAITING_CEO",
                    steps=[("REJECTED", "CEO", "reject", {"acceptanceId": acceptance_id})],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'REJECTED', data_json = json_set(data_json, '$.decision', 'REJECT', '$.reason', ?, '$.decidedAt', ?), updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'PENDING'",
                    (reason.strip(), at, at, self.tenant_id, acceptance_id),
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'REJECTED', data_json = json_set(data_json, '$.acknowledgement', 'CEO_REJECTED'), updated_at = ? "
                    "where tenant_id = ? and entity_id = ? and lifecycle_status = 'SENT'",
                    (at, self.tenant_id, handoff_id),
                )
                target_status = "REJECTED"
            for _, employee in context["assignments"]:
                self._record_path(
                    conn, machine_name="ai_employee", entity_id=employee["entity_id"], source="OPERATING",
                    steps=[("AVAILABLE", "AI_EMPLOYEE", "complete_responsibility", {"cycleId": cycle_id})],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'AVAILABLE', presence_state = 'AVAILABLE', "
                    "updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'OPERATING'",
                    (at, self.tenant_id, employee["entity_id"]),
                )
            data = cycle["data"] | {
                "acceptanceDecision": {"decision": choice, "reason": reason.strip(), "decidedAt": at},
                "executionStatus": "ACCEPTED" if choice == "ACCEPT" else "REJECTED",
            }
            conn.execute(
                "update runtime_entities set lifecycle_status = ?, data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'WAITING_CEO'",
                (target_status, json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
        return self.foundation.get(cycle_id)

    def close_operating_cycle(
        self,
        *,
        company_id: str,
        workspace_id: str,
        cycle_id: str,
        choice: str,
        reason: str,
    ) -> dict:
        next_action = choice.upper()
        if next_action not in {"CONTINUE", "ADJUST", "PAUSE"} or not reason.strip():
            raise ValueError("Cycle close requires CONTINUE, ADJUST or PAUSE and a reason")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            context = self._operating_cycle_context(conn, company_id, workspace_id, cycle_id)
            cycle = context["cycle"]
            existing = cycle["data"].get("decisionPacketId")
            if cycle["lifecycle_status"] == "CLOSED" and existing:
                if cycle["data"].get("nextAction") == next_action:
                    return self.foundation.get(cycle_id)
                raise TransitionError("Cycle is already closed with another decision")
            if cycle["lifecycle_status"] != "ACCEPTED":
                raise TransitionError("only an accepted Cycle can be reviewed and closed")
            acceptance_id = cycle["data"].get("acceptanceId")
            acceptance = self._entity_row(conn, acceptance_id)
            if acceptance["lifecycle_status"] != "ACCEPTED":
                raise TransitionError("Cycle Acceptance is not accepted")
            at = _now()
            decision_id = self._insert_runtime_entity(
                conn,
                entity_type="DECISION_PACKET",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=cycle_id,
                owner_ref="CEO",
                lifecycle_status="DRAFT",
                blueprint_version=cycle["blueprint_version"],
                data={
                    "cycleId": cycle_id,
                    "currentState": "ACCEPTED",
                    "whyNow": reason.strip(),
                    "evidenceRefs": cycle["data"].get("evidenceRefs", []),
                    "unknowns": [],
                    "options": ["CONTINUE", "ADJUST", "PAUSE"],
                    "recommendation": next_action,
                    "choice": next_action,
                    "effectiveAt": at,
                    "rollbackCondition": "创建新 Cycle 或 Blueprint Revision，不覆盖已关闭历史",
                },
                at=at,
            )
            self._record_path(
                conn, machine_name="decision_packet", entity_id=decision_id, source="DRAFT",
                steps=[
                    ("READY", "SYSTEM", "prepare", {"cycleId": cycle_id}),
                    ("WAITING_CEO", "SYSTEM", "request_decision", {"cycleId": cycle_id}),
                    ("DECIDED", "CEO", "decide", {"choice": next_action}),
                    ("APPLIED", "SYSTEM", "apply", {"cycleId": cycle_id, "nextAction": next_action}),
                ],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = 'APPLIED', updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'DRAFT'",
                (at, self.tenant_id, decision_id),
            )
            self._record_path(
                conn, machine_name="acceptance", entity_id=acceptance_id, source="ACCEPTED",
                steps=[("CLOSED", "SYSTEM", "close", {"decisionId": decision_id})],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = 'CLOSED', data_json = json_set(data_json, '$.nextAction', ?, '$.closedAt', ?), updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'ACCEPTED'",
                (next_action, at, at, self.tenant_id, acceptance_id),
            )
            self._record_path(
                conn, machine_name="cycle", entity_id=cycle_id, source="ACCEPTED",
                steps=[
                    ("REVIEWING", "SYSTEM", "review", {"decisionId": decision_id}),
                    ("CLOSED", "CEO", "close", {"decisionId": decision_id}),
                ],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            data = cycle["data"] | {
                "decisionPacketId": decision_id,
                "nextAction": next_action,
                "reviewReason": reason.strip(),
                "completedAt": at,
                "executionStatus": "CLOSED",
            }
            conn.execute(
                "update runtime_entities set lifecycle_status = 'CLOSED', data_json = ?, updated_at = ? "
                "where tenant_id = ? and entity_id = ? and lifecycle_status = 'ACCEPTED'",
                (json.dumps(data, ensure_ascii=False), at, self.tenant_id, cycle_id),
            )
            self._insert_link(conn, company_id, workspace_id, cycle_id, "HAS_DECISION", decision_id, at)
            self._insert_link(conn, company_id, workspace_id, acceptance_id, "HAS_DECISION", decision_id, at)
        return self.foundation.get(cycle_id)

    def create_content_item(
        self,
        *,
        company_id: str,
        workspace_id: str,
        blueprint_version: str,
        platform: str,
        owner_ref: str,
        outcome_ref: str,
        intent_ref: str,
        platform_variant: str,
        payload_ref: str,
        author: str,
        constraints_check: str,
        execution_ref: str | None = None,
        next_check_at: str | None = None,
        title: str = "",
        body: str = "",
        tags: list[str] | None = None,
        cover_ref: str = "",
        scheduled_for: str | None = None,
        format: str = "", topic: str = "", audience: str = "",
        target_account_refs: list[str] | None = None, references: list[dict] | None = None,
        request_id: str = "", start_draft: bool = False, script_metadata: dict | None = None,
    ) -> tuple[dict, dict]:
        workspace = self.get_workspace(company_id, workspace_id)["workspace"]
        from ..content_growth_entry_service import FORMATS, VERSION
        kind = "GRAPHIC" if format in FORMATS else self._business_type(platform)
        if kind != "GRAPHIC" and (kind not in {"XHS", "TTK"} or workspace["business_type"] != kind):
            raise ValueError("content platform must match its XHS or TTK workspace")
        if format and format not in FORMATS:
            raise ValueError("this content format is not supported")
        if kind == "GRAPHIC" and (target_account_refs or platform or scheduled_for or not request_id or not start_draft):
            raise ValueError("graphic creation needs an explicit draft action; account binding and publication are not verified")
        self._require_current_blueprint(workspace, blueprint_version)
        content_id = f"content_item-{uuid4()}"
        version_id = f"content_version-{uuid4()}"
        at = _now()
        version_data = {
            "platform": kind,
            "platformVariant": platform_variant,
            "payloadRef": payload_ref,
            "author": author,
            "constraintsCheck": constraints_check,
            "versionStatus": "READY",
            "title": title.strip() or intent_ref,
            "body": body,
            "tags": list(tags or []),
            "coverRef": cover_ref,
            "scheduledFor": scheduled_for,
        }
        if kind == "GRAPHIC":
            version_data.update(format=format, topic=topic, audience=audience, targetAccountRefs=[],
                                references=list(references or []), kind="draft")
            version_data["platform"] = None
            version_data["payloadRef"] = version_id
            version_data.update(script_metadata or {})
        content_data = {
            "platform": kind,
            "outcomeRef": outcome_ref,
            "intentRef": intent_ref,
            "ownerRole": owner_ref,
            "currentStage": XHS_CONTENT_LIFECYCLE[0] if kind == "XHS" else CONTENT_STAGES[0],
            "stages": list(XHS_CONTENT_LIFECYCLE if kind == "XHS" else CONTENT_STAGES),
        }
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            if kind == "GRAPHIC":
                from ..content_growth_entry_service import ContentGrowthEntryService
                from hashlib import sha256
                info = ContentGrowthEntryService(self.db).authoring_scope(company_id, workspace_id, connection=conn, write=True)
                if author != info["actor"] or owner_ref != info["actor"]:
                    raise RuntimeScopeError("graphic author must be the current Company owner")
                from ..content_growth_service import ContentGrowthService
                if any(not isinstance(value, str) or not value.strip() or len(value) > limit for value,limit in
                       ((title,240),(topic,1000),(audience,1000))):
                    raise ValueError("graphic needs bounded title, topic, audience and body")
                service=ContentGrowthService(self.db)
                raw={"title":title,"topic":topic,"audience":audience,"body":body,"references":references or [],"target_account_refs":[]}
                if info["definition"]["version"] != VERSION: raw.update(format=format,work=(script_metadata or {}).get("work"))
                expected=service.draft_metadata(info,raw)
                if (script_metadata or {}) != {k:expected[k] for k in ("work","qualification") if k in expected} or expected["format"]!=format:
                    raise ValueError("脚本结构或资格快照不是当前服务端依据。")
                if version_data["references"] != service.resolve_references(info["scope"], version_data["references"]):
                    raise ValueError("graphic references are not their qualified canonical snapshots")
                content_data.update(format=format, topic=topic, audience=audience, targetAccountRefs=[],
                                    platform=None, currentStage="PRODUCE")
                request = {"scope": info["scope"], "actor": author, "version": version_data | {"payloadRef": ""}}
                key = "cg:create:" + sha256(json.dumps([info["scope"], author, request_id], sort_keys=True).encode()).hexdigest()
                replay = conn.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                    (self.tenant_id, key)).fetchone()
                if replay:
                    value = json.loads(replay["payload"])
                    if value["request"] != request:
                        raise ValueError("同一请求标识不能创建不同内容。")
                    return self.foundation.get(value["content_ref"]), self.foundation.get(value["version_ref"])

            conn.execute(
                """
                insert into runtime_entities(
                  entity_id, tenant_id, entity_type, company_id, workspace_id,
                  parent_id, owner_ref, lifecycle_status, blueprint_version,
                  verification_status, evidence_condition, data_json, created_at, updated_at
                ) values (?, ?, 'CONTENT_VERSION', ?, ?, ?, ?, 'CREATED', ?,
                          'UNVERIFIED', 'MISSING', ?, ?, ?)
                """,
                (version_id, self.tenant_id, company_id, workspace_id, content_id,
                 author, blueprint_version, json.dumps(version_data, ensure_ascii=False), at, at),
            )
            conn.execute(
                """
                insert into runtime_entities(
                  entity_id, tenant_id, entity_type, company_id, workspace_id,
                  owner_ref, lifecycle_status, blueprint_version, current_version_id, execution_ref,
                  verification_status, evidence_condition, next_check_at, data_json,
                  created_at, updated_at
                ) values (?, ?, 'CONTENT_ITEM', ?, ?, ?, 'IDEA', ?, ?, ?,
                          'UNVERIFIED', 'MISSING', ?, ?, ?, ?)
                """,
                (content_id, self.tenant_id, company_id, workspace_id, owner_ref,
                 blueprint_version, version_id, execution_ref, next_check_at,
                 json.dumps(content_data, ensure_ascii=False), at, at),
            )
            conn.execute(
                "insert into runtime_links(link_id, tenant_id, company_id, workspace_id, source_id, relation, target_id, created_at) "
                "values (?, ?, ?, ?, ?, 'HAS_VERSION', ?, ?)",
                (f"link-{uuid4()}", self.tenant_id, company_id, workspace_id, content_id, version_id, at),
            )
            if kind == "GRAPHIC":
                self._record_path(conn, machine_name="content_item", entity_id=content_id, source="IDEA",
                    steps=[("DRAFT", "CEO", "accept_idea", {})], company_id=company_id,
                    workspace_id=workspace_id, reason="CEO explicitly created a local graphic draft")
                conn.execute("update runtime_entities set lifecycle_status='DRAFT' where tenant_id=? and entity_id=?",
                    (self.tenant_id, content_id))
                conn.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                    (self.tenant_id, content_id, "cg.content.created", json.dumps(
                        {"request":request,"content_ref":content_id,"version_ref":version_id}, ensure_ascii=False), key))
        return self.foundation.get(content_id), self.foundation.get(version_id)

    def _require_content_authoring_scope(self, conn, content, *, blueprint_version=None):
        if content["entity_type"] != "CONTENT_ITEM" or content["lifecycle_status"] != "DRAFT":
            raise ValueError("new content versions require a DRAFT ContentItem")
        from ..content_growth_entry_service import FORMATS
        if content["data"].get("format") in FORMATS:
            from ..content_growth_entry_service import ContentGrowthEntryService
            info = ContentGrowthEntryService(self.db).authoring_scope(content["company_id"], content["workspace_id"],
                connection=conn, write=True)
            if content["blueprint_version"] != info["blueprint_version"]:
                raise RuntimeScopeError("content Blueprint is not current")
            return info
        return None

    def _insert_content_version_in_connection(self, conn, content, data, author, *, head=False, expected=None):
        version_id = f"content_version-{uuid4()}"
        at = _now()
        conn.execute("insert into runtime_entities(entity_id,tenant_id,entity_type,company_id,workspace_id,parent_id,"
            "owner_ref,lifecycle_status,blueprint_version,verification_status,evidence_condition,data_json,created_at,updated_at) "
            "values (?,?,'CONTENT_VERSION',?,?,?,?,'CREATED',?,'UNVERIFIED','MISSING',?,?,?)",
            (version_id,self.tenant_id,content["company_id"],content["workspace_id"],content["entity_id"],author,
             content["blueprint_version"],json.dumps(data,ensure_ascii=False),at,at))
        conn.execute("insert into runtime_links(link_id,tenant_id,company_id,workspace_id,source_id,relation,target_id,created_at) "
            "values (?,?,?,?,?,'HAS_VERSION',?,?)",
            (f"link-{uuid4()}",self.tenant_id,content["company_id"],content["workspace_id"],content["entity_id"],version_id,at))
        if head:
            current = content["current_version_id"]
            if expected is not None and expected != current:
                raise ValueError("内容已在另一处更新，输入保留，请重新读取。")
            changes = {**content["data"], **{k:data[k] for k in ("topic","audience","targetAccountRefs") if k in data}}
            result = conn.execute("update runtime_entities set current_version_id=?,data_json=?,updated_at=? "
                "where tenant_id=? and entity_id=? and current_version_id=? and lifecycle_status='DRAFT'",
                (version_id,json.dumps(changes,ensure_ascii=False),at,self.tenant_id,content["entity_id"],current))
            if result.rowcount != 1:
                raise ValueError("内容版本冲突，没有保存。")
        return version_id

    def add_content_version(self, content_id: str, *, platform_variant: str, payload_ref: str,
                            author: str, constraints_check: str, title: str = "", body: str = "",
                            tags: list[str] | None = None, cover_ref: str = "", scheduled_for: str | None = None,
                            expected_version_ref: str | None = None, request_id: str = "", metadata: dict | None = None) -> dict:
        from hashlib import sha256
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            content = self._entity_row(conn, content_id)
            info = self._require_content_authoring_scope(conn, content)
            if info and (author != info["actor"] or not expected_version_ref or not request_id or scheduled_for):
                raise RuntimeScopeError("内容保存需要当前Owner、明确版本和原请求，不能排期。")
            data = {"platform":content["data"]["platform"],"platformVariant":platform_variant,
                    "payloadRef":payload_ref,"author":author,"constraintsCheck":constraints_check,
                    "versionStatus":"READY","title":title.strip() or content["data"].get("intentRef",""),
                    "body":body,"tags":list(tags or []),"coverRef":cover_ref,"scheduledFor":scheduled_for}
            if metadata:
                data.update(metadata)
            if info and (data.get("targetAccountRefs") or data.get("format") != content["data"].get("format")):
                raise ValueError("账号绑定或内容格式未获验证。")
            if info:
                from ..content_growth_service import ContentGrowthService
                from ..content_growth_entry_service import VERSION
                allowed={"format","topic","audience","targetAccountRefs","references","kind"} | (set() if info["definition"]["version"]==VERSION else {"work","qualification"})
                if set(metadata or {}) != allowed or data["kind"] != "draft":
                    raise ValueError("graphic save accepts only the declared draft fields")
                if any(not isinstance(value,str) or not value.strip() or len(value) > limit for value,limit in
                       ((title,240),(data["topic"],1000),(data["audience"],1000))):
                    raise ValueError("graphic draft fields exceed their bounds")
                service=ContentGrowthService(self.db)
                raw={"title":title,"topic":data["topic"],"audience":data["audience"],"body":body,"references":data["references"],"target_account_refs":[]}
                if info["definition"]["version"]!=VERSION: raw.update(format=data["format"],work=data["work"])
                expected=service.draft_metadata(info,raw)
                if expected != metadata: raise ValueError("保存的脚本结构或资格快照已改变。")
                if data["references"] != service.resolve_references(info["scope"],data["references"]):
                    raise ValueError("graphic references changed before atomic save")
            request = {"author":author,"expected_version_ref":expected_version_ref,"data":data}
            key = "cg:save:" + sha256(json.dumps([self.tenant_id,content_id,author,request_id]).encode()).hexdigest()
            if info:
                replay = conn.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",
                    (self.tenant_id,key)).fetchone()
                if replay:
                    value = json.loads(replay["payload"])
                    if value["request"] != request:
                        raise ValueError("同一请求标识不能保存不同内容。")
                    return self.foundation.get(value["version_ref"])
            version_id = self._insert_content_version_in_connection(conn,content,data,author,head=True,expected=expected_version_ref)
            if info:
                conn.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
                    (self.tenant_id,content_id,"cg.content.saved",json.dumps({"request":request,"version_ref":version_id},ensure_ascii=False),key))
        return self.foundation.get(version_id)

    def adopt_content_candidate(self, conn, content, candidate, *, author, request_id, expected_version_ref, checks):
        from hashlib import sha256
        info = self._require_content_authoring_scope(conn,content)
        if not info or author != info["actor"] or not request_id or any(value is not True for value in checks.values()) or set(checks) != {"content","references","account"}:
            raise ValueError("请明确完成内容、引用与账号边界检查。")
        request = {"candidate_ref":candidate["entity_id"],"expected_version_ref":expected_version_ref,"checks":checks,"actor":author}
        key = "cg:adopt:" + sha256(json.dumps([info["scope"],content["entity_id"],author,request_id],sort_keys=True).encode()).hexdigest()
        row = conn.execute("select payload from evolution_events where tenant_id=? and idempotency_key=?",(self.tenant_id,key)).fetchone()
        if row:
            value=json.loads(row["payload"])
            if value["request"] != request:
                raise ValueError("同一采用请求不能更换依据。")
            return value["version_ref"]
        if (candidate["entity_type"] != "CONTENT_VERSION" or candidate["parent_id"] != content["entity_id"]
                or candidate["company_id"] != content["company_id"] or candidate["workspace_id"] != content["workspace_id"]
                or candidate["data"].get("kind") != "candidate" or candidate["data"].get("basis_version_ref") != expected_version_ref):
            raise RuntimeScopeError("候选依据与当前内容不一致。")
        previous = conn.execute("select entity_id from runtime_entities where tenant_id=? and parent_id=? "
            "and entity_type='CONTENT_VERSION' and json_extract(data_json,'$.source_candidate_ref')=?",
            (self.tenant_id,content["entity_id"],candidate["entity_id"])).fetchone()
        if previous:
            raise ValueError("这个候选已采用，请查看原采用版本。")
        from ..content_growth_service import ContentGrowthService
        ContentGrowthService(self.db).check_qualification(info,candidate["data"])
        data={**candidate["data"],"kind":"adopted","source_candidate_ref":candidate["entity_id"],
              "adoption":{"actor":author,"checks":checks,"at":_now()}}
        version_id=self._insert_content_version_in_connection(conn,content,data,author,head=True,expected=expected_version_ref)
        conn.execute("insert into evolution_events(tenant_id,correlation_id,event_type,payload,idempotency_key) values (?,?,?,?,?)",
            (self.tenant_id,content["entity_id"],"cg.content.adopted",json.dumps({"request":request,"version_ref":version_id},ensure_ascii=False),key))
        return version_id

    def accept_content_idea(self, *, company_id: str, workspace_id: str, content_id: str) -> dict:
        content = self.foundation.get(content_id)
        if (
            content["entity_type"] != "CONTENT_ITEM"
            or content["company_id"] != company_id
            or content["workspace_id"] != workspace_id
        ):
            raise RuntimeScopeError("ContentItem is outside the current workspace")
        return self.foundation.transition(content_id, "DRAFT", actor="CEO", trigger="accept_idea")

    def set_content_work_context(
        self,
        *,
        company_id: str,
        workspace_id: str,
        content_id: str,
        responsibility_employee_ref: str | None,
        current_executor_ref: str | None,
        next_responsibility_employee_ref: str | None = None,
        activity: str = "",
        status: str = "idle",
        system_activity: dict | None = None,
    ) -> dict:
        """Persist the shared responsibility view for one scoped business object.

        This intentionally stores no XHS-only workflow state: it validates existing
        employees and records the four independent responsibility dimensions on the
        current subject.  Handoff/Decision commands update the same projection later.
        """
        allowed_statuses = {"working", "waiting", "needs_ceo", "completed", "failed", "idle"}
        if status not in allowed_statuses:
            raise ValueError("work context status is invalid")
        if system_activity is not None:
            if current_executor_ref:
                raise ValueError("System Activity requires Current Executor = none")
            if not isinstance(system_activity, dict):
                raise ValueError("System Activity must be an object")
            if system_activity.get("status") not in {"waiting", "running", "ready", "failed"}:
                raise ValueError("System Activity status is invalid")

        with self.db.connect() as conn:
            conn.execute("begin immediate")
            content = self._entity_row(conn, content_id)
            if (
                content["entity_type"] != "CONTENT_ITEM"
                or content["company_id"] != company_id
                or content["workspace_id"] != workspace_id
            ):
                raise RuntimeScopeError("ContentItem is outside the current workspace")

            def employee(employee_id: str | None) -> dict | None:
                if not employee_id:
                    return None
                item = self._entity_row(conn, employee_id)
                if (
                    item["entity_type"] != "AI_EMPLOYEE"
                    or item["company_id"] != company_id
                    or item["workspace_id"] != workspace_id
                    or item["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}
                ):
                    raise RuntimeScopeError("work context requires an available Workspace Employee")
                return item

            responsibility = employee(responsibility_employee_ref)
            executor = employee(current_executor_ref)
            next_employee = employee(next_responsibility_employee_ref)
            if executor and not responsibility:
                raise ValueError("Current Executor requires Current Responsibility")
            if executor and responsibility and executor["entity_id"] != responsibility["entity_id"]:
                raise ValueError("Current Executor must be the current responsible Employee in this slice")

            data = content["data"] | {
                "workContext": {
                    "responsibilityEmployeeRef": responsibility["entity_id"] if responsibility else None,
                    "responsibilityRoleSlotRef": responsibility["data"].get("roleSlotRef") if responsibility else None,
                    "currentExecutorRef": executor["entity_id"] if executor else None,
                    "nextResponsibilityEmployeeRef": next_employee["entity_id"] if next_employee else None,
                    "originEmployeeRef": (content["data"].get("workContext") or {}).get("originEmployeeRef") or (responsibility["entity_id"] if responsibility else None),
                    "activity": activity.strip()[:240],
                    "status": status,
                    "systemActivity": system_activity,
                    "updatedAt": _now(),
                },
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ?",
                (json.dumps(data, ensure_ascii=False), _now(), self.tenant_id, content_id),
            )
        return self.foundation.get(content_id)

    def _content_execution_context(self, conn, *, company_id: str, workspace_id: str, content_id: str) -> tuple[dict, dict]:
        content = self._entity_row(conn, content_id)
        if (
            content["entity_type"] != "CONTENT_ITEM"
            or content["company_id"] != company_id
            or content["workspace_id"] != workspace_id
        ):
            raise RuntimeScopeError("ContentItem is outside the current workspace")
        context = content["data"].get("workContext")
        if not isinstance(context, dict):
            raise TransitionError("ContentItem has no validated work context")
        return content, context

    def _assert_content_execution_open(self, conn, content: dict) -> None:
        decision_id = content["data"].get("decisionPacketId")
        if content["lifecycle_status"] == "IN_REVIEW" and decision_id:
            decision = self._entity_row(conn, decision_id)
            if decision["entity_type"] == "DECISION_PACKET":
                raise TransitionError("ContentItem is awaiting or has completed a CEO Decision")

    def record_content_execution_failure(
        self,
        *,
        company_id: str,
        workspace_id: str,
        content_id: str,
        code: str,
        summary: str = "",
    ) -> dict:
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            content, context = self._content_execution_context(
                conn, company_id=company_id, workspace_id=workspace_id, content_id=content_id,
            )
            self._assert_content_execution_open(conn, content)
            if content["lifecycle_status"] not in {"DRAFT", "IN_REVIEW"}:
                raise TransitionError("ContentItem is not in an executable stage")
            failure = {
                "code": str(code)[:128],
                "summary": str(summary)[:1000],
                "returnStage": content["lifecycle_status"],
                "retryCount": len(content["data"].get("executionFailures") or []) + 1,
                "at": _now(),
            }
            work_context = context | {"status": "failed", "failure": failure, "updatedAt": _now()}
            data = content["data"] | {
                "workContext": work_context,
                "executionFailures": [*(content["data"].get("executionFailures") or []), failure],
            }
            conn.execute(
                "update runtime_entities set data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ?",
                (json.dumps(data, ensure_ascii=False), _now(), self.tenant_id, content_id),
            )
        return self.foundation.get(content_id)

    def record_content_execution_completion(
        self,
        *,
        company_id: str,
        workspace_id: str,
        content_id: str,
        result: dict,
    ) -> dict:
        """Accept an already-successful child execution and advance only legal facts."""
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            content, context = self._content_execution_context(
                conn, company_id=company_id, workspace_id=workspace_id, content_id=content_id,
            )
            self._assert_content_execution_open(conn, content)
            stage = content["lifecycle_status"]
            executor_ref = context.get("currentExecutorRef")
            if stage not in {"DRAFT", "IN_REVIEW"} or not executor_ref:
                raise TransitionError("ContentItem has no active Employee execution")
            if not content.get("execution_ref"):
                raise TransitionError("ContentItem has no bound child execution")
            executor = self._entity_row(conn, executor_ref)
            if (
                executor["entity_type"] != "AI_EMPLOYEE"
                or executor["company_id"] != company_id
                or executor["workspace_id"] != workspace_id
                or executor["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}
            ):
                raise RuntimeScopeError("Content execution requires a current Workspace Employee")
            at = _now()
            evidence_id = self._insert_runtime_entity(
                conn, entity_type="EVIDENCE", company_id=company_id, workspace_id=workspace_id,
                parent_id=content_id, owner_ref=executor_ref, lifecycle_status="CURRENT",
                blueprint_version=content["blueprint_version"], verification_status="UNVERIFIED",
                evidence_condition="CURRENT", at=at,
                data={
                    "source": "AI_EXECUTION", "executionRef": content.get("execution_ref") or "",
                    "status": "UNVERIFIED", "summary": str(result.get("output") or "")[:4000], "receivedAt": at,
                },
            )
            self._insert_link(conn, company_id, workspace_id, content_id, "HAS_EVIDENCE", evidence_id, at)
            if stage == "DRAFT":
                reviewer_ref = context.get("nextResponsibilityEmployeeRef")
                if not reviewer_ref:
                    raise TransitionError("Content execution has no next responsible Employee")
                reviewer = self._entity_row(conn, reviewer_ref)
                if (
                    reviewer["entity_type"] != "AI_EMPLOYEE"
                    or reviewer["company_id"] != company_id
                    or reviewer["workspace_id"] != workspace_id
                    or reviewer["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}
                ):
                    raise RuntimeScopeError("Content handoff target is not an available Workspace Employee")
                handoff_id = self._insert_runtime_entity(
                    conn, entity_type="HANDOFF", company_id=company_id, workspace_id=workspace_id,
                    parent_id=content_id, owner_ref=reviewer_ref, lifecycle_status="CREATED",
                    blueprint_version=content["blueprint_version"], at=at,
                    data={
                        "kind": "RESPONSIBILITY_OUTPUT", "subjectId": content_id,
                        "fromEmployeeRef": executor_ref, "toEmployeeRef": reviewer_ref,
                        "inputRefs": [content.get("current_version_id")], "outputRefs": [evidence_id], "at": at,
                    },
                )
                self._record_path(
                    conn, machine_name="handoff", entity_id=handoff_id, source="CREATED",
                    steps=[("SENT", "SYSTEM", "send", {"subjectId": content_id}), ("ACKNOWLEDGED", "AI_EMPLOYEE", "acknowledge", {"subjectId": content_id})],
                    company_id=company_id, workspace_id=workspace_id, reason="内容创作完成，自动交接审核",
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'ACKNOWLEDGED', updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'CREATED'",
                    (at, self.tenant_id, handoff_id),
                )
                self._insert_link(conn, company_id, workspace_id, content_id, "HAS_HANDOFF", handoff_id, at)
                self._record_path(
                    conn, machine_name="content_item", entity_id=content_id, source="DRAFT",
                    steps=[("IN_REVIEW", "AI_EMPLOYEE", "submit_review", {"evidenceRefs": [evidence_id]})],
                    company_id=company_id, workspace_id=workspace_id, reason="创作执行完成，自动进入审核",
                )
                work_context = context | {
                    "responsibilityEmployeeRef": reviewer_ref,
                    "responsibilityRoleSlotRef": reviewer["data"].get("roleSlotRef"),
                    "currentExecutorRef": reviewer_ref, "activity": "内容审核", "status": "working",
                    "systemActivity": None, "updatedAt": at,
                }
                data = content["data"] | {"workContext": work_context, "lastEvidenceId": evidence_id}
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'IN_REVIEW', data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'DRAFT'",
                    (json.dumps(data, ensure_ascii=False), at, self.tenant_id, content_id),
                )
            else:
                decision_id = self._insert_runtime_entity(
                    conn, entity_type="DECISION_PACKET", company_id=company_id, workspace_id=workspace_id,
                    parent_id=content_id, owner_ref="CEO", lifecycle_status="DRAFT",
                    blueprint_version=content["blueprint_version"], at=at,
                    data={
                        "subjectId": content_id,
                        "whyNow": "内容审核需要 CEO 决策",
                        "evidenceRefs": [evidence_id],
                        "options": ["APPROVE", "RETURN", "DEFER"],
                        "recommendation": "APPROVE",
                        # The packet is the single shared decision object.  These
                        # are CEO-readable semantics, not a second XHS approval
                        # model or a UI-only banner payload.
                        "conversation": {
                            "message": "我已完成这篇内容的审核，发现它需要你的判断。我已经整理了几个方案，并给出了建议。",
                        },
                        "plainPackage": {
                            "happened": {"text": "这篇内容已完成审核，正在等待你的选择。", "source": "FACT"},
                            "cannotAutoDecide": {"text": "当前审核规则要求 CEO 在进入发布准备前确认。", "source": "POLICY"},
                            "options": [
                                {
                                    "key": "APPROVE", "label": "按建议处理",
                                    "impact": {"text": "进入发布准备；不会自动发布到平台。", "source": "FACT"},
                                    "risk": {"text": "外部发布仍需单独的连接与确认。", "source": "POLICY"},
                                    "cost": {"text": "当前未验证。", "source": "UNK"},
                                    "continuation": {"text": "Runtime 自动进入排期并等待发布执行；CEO 不会成为执行者。", "source": "FACT"},
                                },
                                {
                                    "key": "RETURN", "label": "退回修改",
                                    "impact": {"text": "回到草稿，并恢复内容创作责任。", "source": "FACT"},
                                    "risk": {"text": "对排期的影响尚未估算。", "source": "UNK"},
                                    "cost": {"text": "当前未验证。", "source": "UNK"},
                                    "continuation": {"text": "Runtime 自动恢复原责任；CEO 不需要再推动下一步。", "source": "FACT"},
                                },
                                {
                                    "key": "DEFER", "label": "暂缓",
                                    "impact": {"text": "保持审核中；不会进入发布准备。", "source": "FACT"},
                                    "risk": {"text": "需要等待新的 CEO 选择。", "source": "FACT"},
                                    "cost": {"text": "当前未验证。", "source": "UNK"},
                                    "continuation": {"text": "审核责任保持不变，Runtime 不会自行发布。", "source": "FACT"},
                                },
                            ],
                            "recommendation": {"key": "APPROVE", "text": "建议按审核结论进入发布准备。", "source": "POLICY"},
                            "recommendationReason": {"text": "审核步骤已完成，当前规则将继续前交给 CEO 确认。", "source": "FACT / POLICY"},
                            "ceoChoice": {"text": "选择一种处理方式；选择后 Runtime 会自动继续。", "source": "FACT"},
                        },
                        "at": at,
                    },
                )
                self._record_path(
                    conn, machine_name="decision_packet", entity_id=decision_id, source="DRAFT",
                    steps=[("READY", "SYSTEM", "prepare", {"subjectId": content_id}), ("WAITING_CEO", "SYSTEM", "request_decision", {"subjectId": content_id})],
                    company_id=company_id, workspace_id=workspace_id, reason="内容审核完成，等待 CEO 决策",
                )
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'WAITING_CEO', updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'DRAFT'",
                    (at, self.tenant_id, decision_id),
                )
                self._insert_link(conn, company_id, workspace_id, content_id, "HAS_DECISION", decision_id, at)
                work_context = context | {"status": "needs_ceo", "activity": "等待 CEO 决策", "updatedAt": at}
                data = content["data"] | {"workContext": work_context, "decisionPacketId": decision_id, "lastEvidenceId": evidence_id}
                conn.execute(
                    "update runtime_entities set data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'IN_REVIEW'",
                    (json.dumps(data, ensure_ascii=False), at, self.tenant_id, content_id),
                )
        return self.foundation.get(content_id)

    def decide_content_review(
        self,
        *,
        company_id: str,
        workspace_id: str,
        content_id: str,
        choice: str,
        reason: str,
    ) -> dict:
        choice = choice.upper()
        if choice not in {"APPROVE", "RETURN", "DEFER"} or not reason.strip():
            raise ValueError("content decision requires APPROVE, RETURN or DEFER and a reason")
        with self.db.connect() as conn:
            conn.execute("begin immediate")
            content, context = self._content_execution_context(conn, company_id=company_id, workspace_id=workspace_id, content_id=content_id)
            decision_id = content["data"].get("decisionPacketId")
            decision = self._entity_row(conn, decision_id) if decision_id else None
            if content["lifecycle_status"] != "IN_REVIEW" or not decision or decision["entity_type"] != "DECISION_PACKET" or decision["parent_id"] != content_id or decision["lifecycle_status"] != "WAITING_CEO":
                raise TransitionError("ContentItem has no current CEO Decision")
            at = _now()
            self._record_path(
                conn, machine_name="decision_packet", entity_id=decision_id, source="WAITING_CEO",
                steps=[("DECIDED", "CEO", "decide", {"choice": choice}), ("APPLIED", "SYSTEM", "apply", {"choice": choice})],
                company_id=company_id, workspace_id=workspace_id, reason=reason,
            )
            conn.execute(
                "update runtime_entities set lifecycle_status = 'APPLIED', data_json = json_set(data_json, '$.choice', ?, '$.reason', ?, '$.decidedAt', ?), updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'WAITING_CEO'",
                (choice, reason.strip(), at, at, self.tenant_id, decision_id),
            )
            if choice == "APPROVE":
                version_id = content.get("current_version_id")
                self._record_path(
                    conn, machine_name="content_item", entity_id=content_id, source="IN_REVIEW",
                    steps=[("APPROVED", "CEO", "approve", {"approvedVersionId": version_id}), ("SCHEDULED", "SYSTEM", "schedule", {"decisionPacketId": decision_id})],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                work_context = context | {
                    "currentExecutorRef": None, "activity": "等待发布执行", "status": "waiting",
                    "systemActivity": {"kind": "PUBLISH_EXECUTION", "label": "等待发布能力", "status": "waiting"}, "updatedAt": at,
                }
                data = content["data"] | {"workContext": work_context, "decisionPacketId": decision_id}
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'SCHEDULED', approved_version_id = ?, data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'IN_REVIEW'",
                    (version_id, json.dumps(data, ensure_ascii=False), at, self.tenant_id, content_id),
                )
            elif choice == "RETURN":
                creator_ref = context.get("originEmployeeRef")
                creator = self._entity_row(conn, creator_ref) if creator_ref else None
                if not creator or creator["entity_type"] != "AI_EMPLOYEE" or creator["workspace_id"] != workspace_id:
                    raise RuntimeScopeError("Content return target is missing")
                self._record_path(
                    conn, machine_name="content_item", entity_id=content_id, source="IN_REVIEW",
                    steps=[("DRAFT", "CEO", "request_changes", {"decisionPacketId": decision_id})],
                    company_id=company_id, workspace_id=workspace_id, reason=reason,
                )
                work_context = context | {
                    "responsibilityEmployeeRef": creator_ref, "responsibilityRoleSlotRef": creator["data"].get("roleSlotRef"),
                    "currentExecutorRef": creator_ref, "activity": "根据 CEO 意见修改", "status": "working", "systemActivity": None, "updatedAt": at,
                }
                data = content["data"] | {"workContext": work_context, "decisionPacketId": decision_id}
                conn.execute(
                    "update runtime_entities set lifecycle_status = 'DRAFT', data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = 'IN_REVIEW'",
                    (json.dumps(data, ensure_ascii=False), at, self.tenant_id, content_id),
                )
            else:
                work_context = context | {"status": "waiting", "activity": "CEO 暂缓，保留审核结论", "updatedAt": at}
                data = content["data"] | {"workContext": work_context, "decisionPacketId": decision_id}
                conn.execute("update runtime_entities set data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ?", (json.dumps(data, ensure_ascii=False), at, self.tenant_id, content_id))
        return self.foundation.get(content_id)

    def record_publication_receipt(
        self,
        content_id: str,
        *,
        source: str,
        status: str,
        approved_version_id: str,
        published_version_id: str,
        external_id: str = "",
        recorded_by: str = "",
        run_ref: str = "",
    ) -> dict:
        content = self.foundation.get(content_id)
        if content["entity_type"] != "CONTENT_ITEM":
            raise KeyError(content_id)
        source = source.upper()
        if source not in RECEIPT_SOURCES:
            raise ValueError("receipt source must be PLATFORM_API or CEO_MANUAL")
        if status not in {"SUCCESS", "FAILED", "RECEIVED"}:
            raise ValueError("receipt status must be SUCCESS, FAILED or RECEIVED")
        if approved_version_id != published_version_id or content["approved_version_id"] != approved_version_id:
            raise ValueError("published version does not match the approved immutable version")
        version = self.foundation.get(published_version_id)
        if version["entity_type"] != "CONTENT_VERSION" or version["parent_id"] != content_id:
            raise RuntimeScopeError("receipt version is outside the ContentItem")
        if source == "PLATFORM_API" and not external_id:
            raise ValueError("platform receipt requires external_id")
        if source == "CEO_MANUAL" and not recorded_by:
            raise ValueError("manual feedback requires recorded_by")
        verification = "VERIFIED" if source == "PLATFORM_API" else "UNVERIFIED"
        receipt = self.foundation.create(
            "PUBLICATION_RECEIPT",
            company_id=content["company_id"],
            workspace_id=content["workspace_id"],
            parent_id=content_id,
            blueprint_version=content["blueprint_version"],
            verification_status=verification,
            evidence_condition="CURRENT",
            data={
                "platform": content["data"]["platform"],
                "source": source,
                "status": status,
                "approvedVersionId": approved_version_id,
                "publishedVersionId": published_version_id,
                "externalId": external_id,
                "recordedBy": recorded_by,
                "runRef": run_ref,
                "receivedAt": _now(),
            },
        )
        self.foundation.link(content_id, "HAS_RECEIPT", receipt["entity_id"])
        return receipt

    def record_interaction(
        self,
        content_id: str,
        *,
        source: str,
        external_id: str,
        intent: str,
        sensitivity: str,
        reply_policy: str,
        recorded_by: str = "",
        next_check_at: str | None = None,
    ) -> dict:
        content = self.foundation.get(content_id)
        if content["entity_type"] != "CONTENT_ITEM":
            raise KeyError(content_id)
        interaction = self.foundation.create(
            "INTERACTION_ITEM",
            company_id=content["company_id"],
            workspace_id=content["workspace_id"],
            parent_id=content_id,
            blueprint_version=content["blueprint_version"],
            next_check_at=next_check_at,
            data={
                "platform": content["data"]["platform"],
                "source": source,
                "externalId": external_id,
                "intent": intent,
                "sensitivity": sensitivity,
                "replyPolicy": reply_policy,
                "recordedBy": recorded_by,
                "receivedAt": _now(),
            },
        )
        self.foundation.link(content_id, "HAS_INTERACTION", interaction["entity_id"])
        return interaction

    def _evidence(self, refs: list[str], company_id: str, workspace_id: str) -> list[str]:
        for evidence_id in refs:
            evidence = self.foundation.get(evidence_id)
            if (
                evidence["entity_type"] != "EVIDENCE"
                or evidence["company_id"] != company_id
                or evidence["workspace_id"] != workspace_id
            ):
                raise RuntimeScopeError("stage evidence is outside the current workspace")
        return list(dict.fromkeys(refs))

    @staticmethod
    def _business_type(value: str) -> str:
        value = value.upper()
        if value not in BUSINESS_TYPES:
            raise ValueError("business_type must be RD, XHS or TTK")
        return value

    @staticmethod
    def _require_current_blueprint(workspace: dict, blueprint_version: str) -> None:
        if workspace["blueprint_version"] != blueprint_version:
            raise ValueError("runtime object blueprint_version is not current")

    @staticmethod
    def _blueprint(business_type: str, blueprint: dict) -> dict:
        forbidden = {"prompt", "apikey", "api_key", "credential", "secret", "rawpayload", "raw_payload"}

        def check(value):
            if isinstance(value, dict):
                for key, item in value.items():
                    if str(key).lower() in forbidden:
                        raise ValueError("Workspace Blueprint cannot contain secrets or raw prompts")
                    check(item)
            elif isinstance(value, list):
                for item in value:
                    check(item)

        check(blueprint)
        stages = tuple(str(item).upper() for item in blueprint.get("stages", []))
        expected = RD_STAGES if business_type == "RD" else XHS_CONTENT_LIFECYCLE if business_type == "XHS" else CONTENT_STAGES
        if stages != expected:
            raise ValueError(f"{business_type} Workspace requires its complete eight-stage contract")
        platform = str(blueprint.get("platform") or "").upper()
        if business_type in {"XHS", "TTK"} and platform != business_type:
            raise ValueError("content Workspace platform must match business_type")
        return {**blueprint, "businessType": business_type, "stages": list(stages)}
