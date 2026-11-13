"""Persisted Business Runtime Foundation commands and queries."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from ..database import Database
from ..tenant_context import TenantContext
from .registry import get_registered_machine
from .state_machine import TransitionError
from .states import EvidenceCondition, ExceptionStatus, PresenceState, VerificationStatus, normalize


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _id(prefix: str) -> str:
    return f"{prefix}-{uuid4()}"


MACHINE_BY_TYPE = {
    "FOUNDING_RUN": "founding_run",
    "CEO_ASSISTANT": "ceo_assistant",
    "AI_EMPLOYEE": "ai_employee",
    "ROLE_SLOT": "role_slot",
    "CAPABILITY_BINDING": "capability_binding",
    "CYCLE": "cycle",
    "HANDOFF": "handoff",
    "DECISION_PACKET": "decision_packet",
    "ACCEPTANCE": "acceptance",
    "CONTENT_ITEM": "content_item",
    "INTERACTION_ITEM": "interaction_item",
}

INITIAL_STATUS = {
    "FOUNDING_RUN": "ARRIVED",
    "CEO_ASSISTANT": "CREATED",
    "AI_EMPLOYEE": "PROPOSED",
    "ROLE_SLOT": "DRAFT",
    "CAPABILITY_BINDING": "PROPOSED",
    "CYCLE": "PLANNED",
    "HANDOFF": "CREATED",
    "DECISION_PACKET": "DRAFT",
    "ACCEPTANCE": "PENDING",
    "EVIDENCE": "CURRENT",
    "BRIEF": "CREATED",
    "CLOSEOUT": "CREATED",
    "CONTENT_ITEM": "IDEA",
    "CONTENT_VERSION": "CREATED",
    "CONTENT_REVIEW": "PENDING",
    "PUBLICATION_RECEIPT": "RECEIVED",
    "INTERACTION_ITEM": "RECEIVED",
    "INTERACTION_RESPONSE": "CREATED",
    "OUTCOME": "CREATED",
    "QUALITY_SNAPSHOT": "CURRENT",
    "RESPONSIBILITY_ASSIGNMENT": "ACTIVE",
    "RESPONSIBILITY_WORKFLOW": "PUBLISHED",
}


class RuntimeScopeError(PermissionError):
    pass


class RuntimeFoundation:
    def __init__(self, database: Database):
        self.db = database

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def create(
        self,
        entity_type: str,
        *,
        entity_id: str | None = None,
        company_id: str | None = None,
        workspace_id: str | None = None,
        parent_id: str | None = None,
        owner_ref: str = "",
        lifecycle_status: str | None = None,
        presence_state: str | None = None,
        org_version: str | None = None,
        blueprint_version: str | None = None,
        capability_ref: str | None = None,
        execution_ref: str | None = None,
        current_version_id: str | None = None,
        approved_version_id: str | None = None,
        published_version_id: str | None = None,
        verification_status: str = "UNVERIFIED",
        evidence_condition: str = "MISSING",
        next_check_at: str | None = None,
        data: dict | None = None,
    ) -> dict:
        kind = entity_type.upper()
        if kind not in INITIAL_STATUS:
            raise ValueError(f"unsupported runtime entity: {kind}")
        status = lifecycle_status or INITIAL_STATUS[kind]
        machine_name = MACHINE_BY_TYPE.get(kind)
        if machine_name:
            normalize(get_registered_machine(machine_name).states, status)
        presence = normalize(PresenceState, presence_state).value if presence_state else None
        verification = normalize(VerificationStatus, verification_status).value
        condition = normalize(EvidenceCondition, evidence_condition).value
        payload = dict(data or {})
        if payload.get("fixture") and verification == "VERIFIED":
            raise ValueError("fixture evidence must remain UNVERIFIED")
        if kind == "CEO_ASSISTANT" and not company_id:
            raise ValueError("CEO_ASSISTANT requires company_id")
        if company_id:
            self._require_company(company_id)
        if workspace_id:
            self._require_workspace(workspace_id, company_id)
        value_id = entity_id or _id(kind.lower())
        at = _now()
        with self.db.connect() as conn:
            conn.execute(
                """
                insert into runtime_entities(
                  entity_id, tenant_id, entity_type, company_id, workspace_id,
                  parent_id, owner_ref, lifecycle_status, presence_state,
                  org_version, blueprint_version, capability_ref, execution_ref,
                  current_version_id, approved_version_id, published_version_id,
                  verification_status, evidence_condition, next_check_at, data_json, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (value_id, self.tenant_id, kind, company_id, workspace_id,
                 parent_id, owner_ref, status, presence, org_version,
                 blueprint_version, capability_ref, execution_ref,
                 current_version_id, approved_version_id, published_version_id,
                 verification, condition, next_check_at, json.dumps(payload, ensure_ascii=False), at, at),
            )
        return self.get(value_id)

    def get(self, entity_id: str) -> dict:
        with self.db.connect() as conn:
            row = conn.execute(
                "select * from runtime_entities where tenant_id = ? and entity_id = ?",
                (self.tenant_id, entity_id),
            ).fetchone()
        if row is None:
            raise KeyError(entity_id)
        result = dict(row)
        result["data"] = json.loads(result.pop("data_json"))
        return result

    def list(self, entity_type: str, *, company_id: str | None = None, workspace_id: str | None = None) -> list[dict]:
        clauses = ["tenant_id = ?", "entity_type = ?"]
        params: list[object] = [self.tenant_id, entity_type.upper()]
        if company_id is not None:
            clauses.append("company_id = ?")
            params.append(company_id)
        if workspace_id is not None:
            clauses.append("workspace_id = ?")
            params.append(workspace_id)
        with self.db.connect() as conn:
            rows = conn.execute(
                f"select * from runtime_entities where {' and '.join(clauses)} order by created_at, entity_id",
                params,
            ).fetchall()
        result = []
        for row in rows:
            item = dict(row)
            item["data"] = json.loads(item.pop("data_json"))
            result.append(item)
        return result

    def transition(
        self,
        entity_id: str,
        target: str,
        *,
        actor: str,
        trigger: str,
        reason: str = "",
        evidence_refs: list[str] | None = None,
        next_check_at: str | None = None,
        context: dict | None = None,
    ) -> dict:
        current = self.get(entity_id)
        machine_name = MACHINE_BY_TYPE.get(current["entity_type"])
        if not machine_name:
            raise ValueError(f"{current['entity_type']} has no lifecycle state machine")
        ctx = dict(context or {})
        ctx.update({
            "companyId": current["company_id"],
            "workspaceId": current["workspace_id"],
            "evidenceRefs": list(evidence_refs or []),
            "nextCheckAt": next_check_at,
            "approvedVersionId": current["approved_version_id"],
            "publishedVersionId": current["published_version_id"],
        })
        record = get_registered_machine(machine_name).transition(
            entity_id,
            current["lifecycle_status"],
            target,
            actor=actor,
            trigger=trigger,
            reason=reason,
            context=ctx,
            record=False,
        )
        with self.db.connect() as conn:
            cursor = conn.execute(
                "update runtime_entities set lifecycle_status = ?, next_check_at = ?, updated_at = ? where tenant_id = ? and entity_id = ? and lifecycle_status = ?",
                (record.target, next_check_at, record.at, self.tenant_id, entity_id, record.source),
            )
            if cursor.rowcount != 1:
                raise RuntimeError("runtime entity changed concurrently; retry from current state")
            conn.execute(
                """
                insert into runtime_transition_log(
                  tenant_id, entity_type, entity_id, source, target, trigger, actor,
                  at, reason, company_id, workspace_id, evidence_refs_json,
                  next_check_at, context_json
                ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (self.tenant_id, machine_name, entity_id, record.source, record.target,
                 record.trigger, record.actor, record.at, reason, current["company_id"],
                 current["workspace_id"], json.dumps(evidence_refs or []), next_check_at,
                 json.dumps(ctx, ensure_ascii=False)),
            )
        return self.get(entity_id)

    def set_dimensions(
        self,
        entity_id: str,
        *,
        presence_state: str | None = None,
        verification_status: str | None = None,
        evidence_condition: str | None = None,
        exception_status: str | None = None,
    ) -> dict:
        current = self.get(entity_id)
        updates: dict[str, str] = {}
        if presence_state is not None:
            updates["presence_state"] = normalize(PresenceState, presence_state).value
        if verification_status is not None:
            verified = normalize(VerificationStatus, verification_status).value
            if current["data"].get("fixture") and verified == "VERIFIED":
                raise ValueError("fixture evidence must remain UNVERIFIED")
            updates["verification_status"] = verified
        if evidence_condition is not None:
            updates["evidence_condition"] = normalize(EvidenceCondition, evidence_condition).value
        if exception_status is not None:
            updates["exception_status"] = normalize(ExceptionStatus, exception_status).value
        if not updates:
            return current
        updates["updated_at"] = _now()
        assignments = ", ".join(f"{key} = ?" for key in updates)
        with self.db.connect() as conn:
            conn.execute(
                f"update runtime_entities set {assignments} where tenant_id = ? and entity_id = ?",
                (*updates.values(), self.tenant_id, entity_id),
            )
        return self.get(entity_id)

    def link(self, source_id: str, relation: str, target_id: str) -> dict:
        source = self.get(source_id)
        target = self.get(target_id)
        for field in ("company_id", "workspace_id"):
            if source[field] and target[field] and source[field] != target[field]:
                raise RuntimeScopeError(f"cross-scope runtime link rejected: {field}")
        link_id = _id("link")
        with self.db.connect() as conn:
            conn.execute(
                "insert into runtime_links(link_id, tenant_id, company_id, workspace_id, source_id, relation, target_id, created_at) values (?, ?, ?, ?, ?, ?, ?, ?)",
                (link_id, self.tenant_id, source["company_id"] or target["company_id"],
                 source["workspace_id"] or target["workspace_id"], source_id, relation,
                 target_id, _now()),
            )
        return {"link_id": link_id, "source_id": source_id, "relation": relation, "target_id": target_id}

    def related(self, entity_id: str, relation: str | None = None, *, reverse: bool = False) -> list[dict]:
        self.get(entity_id)
        side, other = ("target_id", "source_id") if reverse else ("source_id", "target_id")
        clauses = ["tenant_id = ?", f"{side} = ?"]
        params: list[object] = [self.tenant_id, entity_id]
        if relation:
            clauses.append("relation = ?")
            params.append(relation)
        with self.db.connect() as conn:
            rows = conn.execute(
                f"select * from runtime_links where {' and '.join(clauses)} order by created_at, link_id",
                params,
            ).fetchall()
        return [{**dict(row), "entity": self.get(row[other])} for row in rows]

    def _materialize_company_in_connection(
        self, conn, founding_run_id: str, *, company_id: str, ceo_id: str, name: str,
    ) -> str:
        """Materialize Company/Assistant inside an already serialized transaction."""

        tenant_id = self.tenant_id
        row = conn.execute(
            "select * from runtime_entities where tenant_id = ? and entity_id = ?",
            (tenant_id, founding_run_id),
        ).fetchone()
        if row is None or row["entity_type"] != "FOUNDING_RUN":
            raise KeyError(founding_run_id)
        run = dict(row)
        if run["owner_ref"] != ceo_id:
            raise RuntimeScopeError("FoundingRun CEO does not match the current command")

        if run["lifecycle_status"] == "COMPANY_CREATED":
            if run["company_id"] != company_id:
                raise TransitionError("FoundingRun was materialized with another company")
            company = conn.execute(
                "select ceo_id, name from companies where tenant_id = ? and company_id = ?",
                (tenant_id, company_id),
            ).fetchone()
            assistant = conn.execute(
                "select entity_id from runtime_entities where tenant_id = ? and entity_id = ? "
                "and entity_type = 'CEO_ASSISTANT' and company_id = ?",
                (tenant_id, run["parent_id"], company_id),
            ).fetchone()
            link = conn.execute(
                "select 1 from runtime_links where tenant_id = ? and source_id = ? "
                "and relation = 'CREATED_ASSISTANT' and target_id = ?",
                (tenant_id, founding_run_id, run["parent_id"]),
            ).fetchone()
            if company is None or assistant is None or link is None:
                raise RuntimeError("materialized FoundingRun is incomplete")
            if company["ceo_id"] != ceo_id or company["name"] != name:
                raise TransitionError("FoundingRun was materialized with another request")
            return assistant["entity_id"]

        transition = get_registered_machine("founding_run").transition(
            founding_run_id, run["lifecycle_status"], "COMPANY_CREATED", actor="SYSTEM",
            trigger="persist_company", context={"companyId": company_id}, record=False,
        )
        existing = conn.execute(
            "select tenant_id from companies where company_id = ?", (company_id,),
        ).fetchone()
        if existing is not None:
            if existing["tenant_id"] != tenant_id:
                raise RuntimeScopeError("company id is outside the current tenant")
            raise TransitionError("company id is already in use")
        assistant_id = _id("ceo_assistant")
        link_id = _id("link")
        payload = json.dumps({"contextVersion": "context-v1", "contractVersion": "contract-v1"})
        at = transition.at
        conn.execute(
            "insert into companies(company_id, tenant_id, ceo_id, name, status) values (?, ?, ?, ?, 'draft')",
            (company_id, tenant_id, ceo_id, name),
        )
        from ..employee_templates import EmployeeTemplateContract

        EmployeeTemplateContract(self.db).materialize_builtin_organization(conn, company_id=company_id)
        conn.execute(
            """
            insert into runtime_entities(
              entity_id, tenant_id, entity_type, company_id, owner_ref,
              lifecycle_status, org_version, verification_status,
              evidence_condition, data_json, created_at, updated_at
            ) values (?, ?, 'CEO_ASSISTANT', ?, ?, 'CREATED', 'org-v1',
                      'UNVERIFIED', 'MISSING', ?, ?, ?)
            """,
            (assistant_id, tenant_id, company_id, ceo_id, payload, at, at),
        )
        cursor = conn.execute(
            "update runtime_entities set company_id = ?, parent_id = ?, lifecycle_status = ?, updated_at = ? "
            "where tenant_id = ? and entity_id = ? and lifecycle_status = 'CEO_CONFIRMED'",
            (company_id, assistant_id, transition.target, at, tenant_id, founding_run_id),
        )
        if cursor.rowcount != 1:
            raise RuntimeError("FoundingRun changed concurrently; company creation rolled back")
        conn.execute(
            """
            insert into runtime_transition_log(
              tenant_id, entity_type, entity_id, source, target, trigger, actor,
              at, company_id, context_json
            ) values (?, 'founding_run', ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (tenant_id, founding_run_id, transition.source, transition.target,
             transition.trigger, transition.actor, at, company_id,
             json.dumps(transition.context)),
        )
        conn.execute(
            "insert into runtime_links(link_id, tenant_id, company_id, source_id, relation, target_id, created_at) "
            "values (?, ?, ?, ?, 'CREATED_ASSISTANT', ?, ?)",
            (link_id, tenant_id, company_id, founding_run_id, assistant_id, at),
        )
        return assistant_id

    def materialize_company(self, founding_run_id: str, *, company_id: str, ceo_id: str, name: str) -> tuple[dict, dict]:
        with self.db.connect() as conn:
            # Serialize the single materialization boundary so concurrent retries
            # observe the committed FoundingRun instead of creating parallel assets.
            conn.execute("begin immediate")
            assistant_id = self._materialize_company_in_connection(
                conn, founding_run_id, company_id=company_id, ceo_id=ceo_id, name=name,
            )
        return self.get(founding_run_id), self.get(assistant_id)

    def history(self, entity_id: str) -> list[dict]:
        self.get(entity_id)
        with self.db.connect() as conn:
            rows = conn.execute(
                "select * from runtime_transition_log where tenant_id = ? and entity_id = ? order by at, log_id",
                (self.tenant_id, entity_id),
            ).fetchall()
        return [dict(row) for row in rows]

    def attach_execution_ref(self, entity_id: str, execution_ref: str, metadata: dict | None = None) -> dict:
        current = self.get(entity_id)
        payload = {**current["data"], **(metadata or {})}
        with self.db.connect() as conn:
            conn.execute(
                "update runtime_entities set execution_ref = ?, data_json = ?, updated_at = ? where tenant_id = ? and entity_id = ?",
                (execution_ref, json.dumps(payload, ensure_ascii=False), _now(), self.tenant_id, entity_id),
            )
        return self.get(entity_id)

    def set_version_refs(
        self,
        entity_id: str,
        *,
        current_version_id: str | None = None,
        approved_version_id: str | None = None,
        published_version_id: str | None = None,
    ) -> dict:
        self.get(entity_id)
        updates = {
            key: value for key, value in (
                ("current_version_id", current_version_id),
                ("approved_version_id", approved_version_id),
                ("published_version_id", published_version_id),
            ) if value is not None
        }
        if not updates:
            return self.get(entity_id)
        updates["updated_at"] = _now()
        with self.db.connect() as conn:
            conn.execute(
                f"update runtime_entities set {', '.join(f'{key} = ?' for key in updates)} where tenant_id = ? and entity_id = ?",
                (*updates.values(), self.tenant_id, entity_id),
            )
        return self.get(entity_id)

    def _require_company(self, company_id: str) -> None:
        with self.db.connect() as conn:
            row = conn.execute(
                "select 1 from companies where tenant_id = ? and company_id = ?",
                (self.tenant_id, company_id),
            ).fetchone()
        if row is None:
            raise RuntimeScopeError("company does not belong to current tenant")

    def _require_workspace(self, workspace_id: str, company_id: str | None) -> None:
        with self.db.connect() as conn:
            row = conn.execute(
                "select company_id from workspaces where tenant_id = ? and workspace_id = ?",
                (self.tenant_id, workspace_id),
            ).fetchone()
        if row is None or (company_id and row["company_id"] != company_id):
            raise RuntimeScopeError("workspace does not belong to current company")
