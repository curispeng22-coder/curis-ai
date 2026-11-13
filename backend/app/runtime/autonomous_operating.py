"""Minimal persisted control truth for Autonomous Operating V1 Phase 1.

This module owns no employee execution.  It only binds a canonical Workspace,
its existing Leader Assignment, one Operating Series, deterministic Trigger
Claims and the existing CYCLE entity inside SQLite transactions.
"""

from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from typing import Any

from ..database import Database
from ..tenant_context import TenantContext
from .child_work import CanonicalChildWorkRuntime, ChildWorkError
from .foundation import RuntimeFoundation
from .responsibility_routing import ResponsibilityRoutingRuntime


SERIES_STATES = frozenset({"ACTIVE", "WAITING", "PAUSED", "STOPPED"})
TRIGGER_TYPES = frozenset({"MANUAL", "SCHEDULED", "RESULT"})
TERMINAL_CYCLE_STATES = frozenset({"CLOSED", "REJECTED", "FAILED"})
EVALUATION_OUTCOMES = frozenset({"SUCCESS", "FAILURE", "INSUFFICIENT"})
NEXT_CYCLE_DECISIONS = frozenset({"CONTINUE", "ADJUST", "WAIT", "ESCALATE", "PAUSE", "STOP"})


class AutonomousControlError(ValueError):
    pass


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def _hash(value: Any) -> str:
    return hashlib.sha256(_json(value).encode("utf-8")).hexdigest()


def _stable_id(prefix: str, *parts: str) -> str:
    digest = hashlib.sha256("\x1f".join(parts).encode("utf-8")).hexdigest()[:32]
    return f"{prefix}-{digest}"


class AutonomousOperatingControl:
    """Workspace-scoped Series and Trigger Claim persistence.

    ``BEGIN IMMEDIATE`` is the concurrency boundary.  Deterministic identities
    make replay return the existing truth rather than create a second record.
    """

    def __init__(self, database: Database):
        self.db = database

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    @staticmethod
    def _entity(row) -> dict[str, Any]:
        item = dict(row)
        item["data"] = json.loads(item.pop("data_json"))
        return item

    def _row(self, connection, entity_id: str, *, entity_type: str | None = None):
        sql = "select * from runtime_entities where tenant_id=? and entity_id=?"
        params: list[Any] = [self.tenant_id, entity_id]
        if entity_type:
            sql += " and entity_type=?"
            params.append(entity_type)
        row = connection.execute(sql, params).fetchone()
        if row is None:
            raise KeyError(entity_id)
        return row

    def _workspace_truth(self, connection, company_id: str, workspace_id: str) -> tuple[dict, dict, dict]:
        workspace = connection.execute(
            "select * from workspaces where tenant_id=? and company_id=? and workspace_id=? "
            "and business_relation_status='RESOLVED'",
            (self.tenant_id, company_id, workspace_id),
        ).fetchone()
        if workspace is None:
            raise AutonomousControlError("Operating Series requires a resolved canonical Workspace")
        business = connection.execute(
            "select * from canonical_businesses where tenant_id=? and company_id=? and business_id=? "
            "and lifecycle_status!='ARCHIVED'",
            (self.tenant_id, company_id, workspace["business_id"]),
        ).fetchone()
        if business is None:
            raise AutonomousControlError("Workspace has no active canonical Business")
        blueprint = json.loads(workspace["blueprint_json"] or "{}")
        workspace_goal = str(blueprint.get("goal") or "").strip()
        if not workspace_goal:
            raise AutonomousControlError("Workspace requires its own explicit Goal; Business Goal is not a fallback")
        return dict(workspace), dict(business), blueprint

    def _leader_assignment(self, connection, company_id: str, workspace_id: str, assignment_ref: str) -> dict:
        assignment = self._row(connection, assignment_ref, entity_type="RESPONSIBILITY_ASSIGNMENT")
        item = self._entity(assignment)
        data = item["data"]
        if (
            item["company_id"] != company_id
            or item["workspace_id"] != workspace_id
            or item["lifecycle_status"] != "ACTIVE"
            or data.get("scopeType") != "WORKSPACE"
            or data.get("scopeRef") != workspace_id
            or not data.get("isLeader")
        ):
            raise AutonomousControlError("Leader Assignment is not active in the canonical Workspace scope")
        employee_ref = str(data.get("employeeRef") or "")
        employee = self._row(connection, employee_ref, entity_type="AI_EMPLOYEE")
        if employee["company_id"] != company_id or employee["workspace_id"] not in (None, workspace_id):
            raise AutonomousControlError("Leader Assignment Employee is outside the canonical Workspace scope")
        return item

    @staticmethod
    def _approved_snapshot(kind: str, value: dict[str, Any]) -> dict[str, Any]:
        version = str(value.get("version") or "").strip()
        body = value.get("body")
        approved_by = str(value.get("approvedBy") or "").strip()
        approved_at = str(value.get("approvedAt") or "").strip()
        if value.get("status") != "APPROVED" or not version or not isinstance(body, dict) or not body:
            raise AutonomousControlError(f"{kind} requires a non-empty approved versioned body")
        if not approved_by or not approved_at:
            raise AutonomousControlError(f"{kind} requires approval provenance")
        return {
            "version": version,
            "status": "APPROVED",
            "body": body,
            "bodyHash": _hash(body),
            "approvedBy": approved_by,
            "approvedAt": approved_at,
        }

    def _insert_entity(
        self,
        connection,
        *,
        entity_id: str,
        entity_type: str,
        company_id: str,
        workspace_id: str,
        parent_id: str | None,
        owner_ref: str,
        lifecycle_status: str,
        current_version_id: str | None = None,
        next_check_at: str | None = None,
        data: dict[str, Any],
        at: str,
    ) -> None:
        connection.execute(
            "insert into runtime_entities(entity_id, tenant_id, entity_type, company_id, workspace_id, "
            "parent_id, owner_ref, lifecycle_status, current_version_id, verification_status, "
            "evidence_condition, next_check_at, data_json, created_at, updated_at) "
            "values (?, ?, ?, ?, ?, ?, ?, ?, ?, 'UNVERIFIED', 'MISSING', ?, ?, ?, ?)",
            (
                entity_id,
                self.tenant_id,
                entity_type,
                company_id,
                workspace_id,
                parent_id,
                owner_ref,
                lifecycle_status,
                current_version_id,
                next_check_at,
                _json(data),
                at,
                at,
            ),
        )

    def _link(self, connection, company_id: str, workspace_id: str, source: str, relation: str, target: str, at: str) -> None:
        connection.execute(
            "insert or ignore into runtime_links(link_id, tenant_id, company_id, workspace_id, "
            "source_id, relation, target_id, created_at) values (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                _stable_id("link", self.tenant_id, source, relation, target),
                self.tenant_id,
                company_id,
                workspace_id,
                source,
                relation,
                target,
                at,
            ),
        )

    def create_series(
        self,
        *,
        company_id: str,
        workspace_id: str,
        leader_assignment_ref: str,
        strategy: dict[str, Any],
        envelope: dict[str, Any],
        plan_pin: dict[str, Any] | None = None,
        evaluation_pin: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        strategy_snapshot = self._approved_snapshot("Strategy", strategy)
        envelope_snapshot = self._approved_snapshot("Approved Strategy Envelope", envelope)
        at = _now()
        series_id = _stable_id("operating-series", self.tenant_id, workspace_id)
        strategy_ref = f"{series_id}:strategy:{strategy_snapshot['version']}"
        envelope_ref = f"{series_id}:envelope:{envelope_snapshot['version']}"
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            workspace, business, blueprint = self._workspace_truth(connection, company_id, workspace_id)
            assignment = self._leader_assignment(connection, company_id, workspace_id, leader_assignment_ref)
            workspace_goal = str(blueprint.get("goal") or "").strip()
            workspace_goal_pin = {
                "scopeType": "WORKSPACE",
                "scopeRef": workspace_id,
                "ref": f"workspace:{workspace_id}:blueprint:{workspace['blueprint_version']}:goal",
                "version": workspace["blueprint_version"],
                "valueHash": _hash(workspace_goal),
            }
            business_goal = str(business["goal"] or "").strip()
            business_goal_pin = {
                "scopeType": "BUSINESS",
                "scopeRef": business["business_id"],
                "ref": f"business:{business['business_id']}:goal:{business['updated_at']}",
                "version": business["updated_at"],
                "valueHash": _hash(business_goal),
                "relation": "GOVERNING_DIRECTION",
            }
            strategy_version = {
                "strategyRef": strategy_ref,
                **strategy_snapshot,
                "scopeType": "WORKSPACE",
                "scopeRef": workspace_id,
                "envelope": {"envelopeRef": envelope_ref, **envelope_snapshot},
            }
            expected = {
                "businessRef": business["business_id"],
                "leaderAssignmentRef": leader_assignment_ref,
                "workspaceGoalPin": workspace_goal_pin,
                "businessGoalPin": business_goal_pin,
                "strategyVersions": [strategy_version],
                "currentStrategyRef": strategy_ref,
                "planPin": dict(plan_pin or {"status": "UNRESOLVED"}),
                "evaluationPin": dict(evaluation_pin or {"status": "UNRESOLVED"}),
            }
            existing = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, series_id),
            ).fetchone()
            if existing is not None:
                item = self._entity(existing)
                comparable = {key: item["data"].get(key) for key in expected}
                if comparable != expected:
                    raise AutonomousControlError("Operating Series already exists with different canonical truth")
                return item
            data = {
                **expected,
                "currentCycleRef": None,
                "lastCycleRef": None,
                "createdAt": at,
                "updatedAt": at,
            }
            self._insert_entity(
                connection,
                entity_id=series_id,
                entity_type="OPERATING_SERIES",
                company_id=company_id,
                workspace_id=workspace_id,
                parent_id=business["business_id"],
                owner_ref=leader_assignment_ref,
                lifecycle_status="ACTIVE",
                current_version_id=strategy_ref,
                data=data,
                at=at,
            )
            self._link(connection, company_id, workspace_id, series_id, "HAS_LEADER_ASSIGNMENT", assignment["entity_id"], at)
            self._link(connection, company_id, workspace_id, series_id, "OPERATES_WORKSPACE", workspace_id, at)
            return self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))

    def get_series(self, series_id: str) -> dict[str, Any]:
        with self.db.connect() as connection:
            return self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))

    def set_series_state(self, series_id: str, target: str, *, next_check_at: str | None = None) -> dict[str, Any]:
        target = target.upper()
        if target not in SERIES_STATES:
            raise AutonomousControlError("Unsupported Operating Series state")
        if target == "WAITING" and not next_check_at:
            raise AutonomousControlError("WAITING requires nextCheckAt")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            row = self._row(connection, series_id, entity_type="OPERATING_SERIES")
            current = row["lifecycle_status"]
            allowed = {
                "ACTIVE": {"WAITING", "PAUSED", "STOPPED"},
                "WAITING": {"ACTIVE", "PAUSED", "STOPPED"},
                "PAUSED": {"ACTIVE", "STOPPED"},
                "STOPPED": set(),
            }
            if target == current:
                return self._entity(row)
            if target not in allowed[current]:
                raise AutonomousControlError(f"Operating Series cannot transition {current} -> {target}")
            if self._active_cycles(connection, series_id):
                raise AutonomousControlError("Series state cannot change while an active Cycle exists")
            data = json.loads(row["data_json"])
            data["updatedAt"] = _now()
            connection.execute(
                "update runtime_entities set lifecycle_status=?, next_check_at=?, data_json=?, updated_at=? "
                "where tenant_id=? and entity_id=? and lifecycle_status=?",
                (target, next_check_at, _json(data), data["updatedAt"], self.tenant_id, series_id, current),
            )
            return self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))

    def _active_cycles(self, connection, series_id: str) -> list[Any]:
        marks = ",".join("?" for _ in TERMINAL_CYCLE_STATES)
        return connection.execute(
            "select * from runtime_entities where tenant_id=? and entity_type='CYCLE' "
            "and json_extract(data_json, '$.autonomousControl.seriesRef')=? "
            f"and lifecycle_status not in ({marks}) order by created_at, entity_id",
            (self.tenant_id, series_id, *sorted(TERMINAL_CYCLE_STATES)),
        ).fetchall()

    def _successor_strategy(self, series: dict, decision: dict, predecessor_control: dict) -> tuple[dict, dict]:
        data = decision["data"]
        current = series["data"]["strategyVersions"][-1]
        pinned_strategy = predecessor_control.get("strategyPin") or {}
        pinned_envelope = predecessor_control.get("envelopePin") or {}
        if (
            data.get("strategyRef") != current["strategyRef"]
            or data.get("strategyVersion") != current["version"]
            or data.get("envelopeRef") != current["envelope"]["envelopeRef"]
            or data.get("envelopeVersion") != current["envelope"]["version"]
            or pinned_strategy.get("strategyRef") != current["strategyRef"]
            or pinned_strategy.get("version") != current["version"]
            or pinned_strategy.get("bodyHash") != current["bodyHash"]
            or pinned_envelope.get("envelopeRef") != current["envelope"]["envelopeRef"]
            or pinned_envelope.get("version") != current["envelope"]["version"]
            or pinned_envelope.get("bodyHash") != current["envelope"]["bodyHash"]
        ):
            raise AutonomousControlError("Next-cycle Decision Strategy or Envelope authority is stale")
        plan_pin = {
            "status": "UNRESOLVED",
            "predecessorDecisionRef": decision["entity_id"],
        }
        if data["decision"] == "CONTINUE":
            return current, plan_pin
        resolved, _, gate = self._decision_authority("ADJUST", current, data.get("adjustment"))
        if resolved != "ADJUST" or gate:
            raise AutonomousControlError("Adjusted successor pins are outside the Approved Strategy Envelope")
        changes = dict(data["adjustment"]["changes"])
        body = {**current["body"], **changes}
        digest = _hash({"base": current["strategyRef"], "changes": changes, "decision": decision["entity_id"]})
        version = f"{current['version']}.adjust.{digest[:12]}"
        strategy_ref = f"{series['entity_id']}:strategy:{version}"
        adjusted = {
            **current,
            "strategyRef": strategy_ref,
            "version": version,
            "body": body,
            "bodyHash": _hash(body),
            "approvedBy": data["actorRef"],
            "approvedAt": decision["updated_at"],
            "authorityDecisionRef": decision["entity_id"],
        }
        plan_pin.update({"adjustmentDecisionRef": decision["entity_id"], "requiredChanges": changes})
        return adjusted, plan_pin

    def claim_trigger(
        self,
        *,
        series_id: str,
        source_type: str,
        source_key: str,
        decision_ref: str | None = None,
    ) -> dict[str, Any]:
        source_type = source_type.upper()
        source_key = source_key.strip()
        if source_type not in TRIGGER_TYPES or not source_key:
            raise AutonomousControlError("Trigger requires a supported source type and stable source key")
        claim_id = _stable_id("trigger-claim", self.tenant_id, series_id, source_type, source_key)
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            series_row = self._row(connection, series_id, entity_type="OPERATING_SERIES")
            existing = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, claim_id),
            ).fetchone()
            if existing is not None:
                claim = self._entity(existing)
                cycle = self._entity(self._row(connection, claim["data"]["cycleRef"], entity_type="CYCLE")) if claim["data"].get("cycleRef") else None
                return {"claim": claim, "cycle": cycle, "replayed": True, "merged": bool(claim["data"].get("merged"))}
            series = self._entity(series_row)
            predecessor_id = str(series["data"].get("lastCycleRef") or "")
            cycles = self._active_cycles(connection, series_id)
            if len(cycles) > 1:
                raise AutonomousControlError("Operating Series has more than one active Cycle")
            if decision_ref and cycles:
                raise AutonomousControlError("Applied Decision cannot authorize a successor while another Cycle is active")
            decision = None
            predecessor = None
            successor_strategy = None
            successor_plan_pin = None
            if predecessor_id and series["lifecycle_status"] == "ACTIVE" and not cycles:
                if not decision_ref:
                    raise AutonomousControlError("A closed Cycle requires an applied Next-cycle Decision before another Trigger Claim")
                decision = self._entity(self._row(connection, decision_ref, entity_type="DECISION_PACKET"))
                predecessor = self._entity(self._row(connection, predecessor_id, entity_type="CYCLE"))
                predecessor_control = dict(predecessor["data"].get("autonomousControl") or {})
                decision_data = decision["data"]
                if (
                    decision["lifecycle_status"] != "APPLIED"
                    or decision["parent_id"] != predecessor_id
                    or decision_data.get("kind") != "NEXT_CYCLE_DECISION"
                    or decision_data.get("seriesRef") != series_id
                    or decision_data.get("cycleRef") != predecessor_id
                    or decision_data.get("decision") not in {"CONTINUE", "ADJUST"}
                    or decision_data.get("ceoGateRequired")
                ):
                    raise AutonomousControlError("Trigger Claim has no applied canonical successor authority")
                existing_successor = str(decision_data.get("successorCycleRef") or "")
                if existing_successor:
                    existing_claim_ref = str(decision_data.get("successorTriggerClaimRef") or "")
                    claim = self._entity(self._row(connection, existing_claim_ref, entity_type="TRIGGER_CLAIM"))
                    cycle = self._entity(self._row(connection, existing_successor, entity_type="CYCLE"))
                    if claim["data"].get("cycleRef") != existing_successor:
                        raise AutonomousControlError("Existing successor Claim/Cycle lineage is inconsistent")
                    return {"claim": claim, "cycle": cycle, "replayed": True, "merged": False}
                successor_strategy, successor_plan_pin = self._successor_strategy(series, decision, predecessor_control)
            at = _now()
            cycle_row = cycles[0] if cycles else None
            cycle_id = cycle_row["entity_id"] if cycle_row else None
            merged = cycle_row is not None
            claim_status = "CLAIMED"
            cancel_reason = ""
            if series["lifecycle_status"] == "STOPPED":
                claim_status, cancel_reason = "CANCELLED", "SERIES_STOPPED"
            elif series["lifecycle_status"] == "ACTIVE":
                claim_status = "APPLIED"
                if cycle_row is None:
                    cycle_id = _stable_id("cycle", self.tenant_id, series_id, claim_id)
                    strategy = successor_strategy or series["data"]["strategyVersions"][-1]
                    control = {
                        "schemaVersion": 1,
                        "seriesRef": series_id,
                        "triggerClaimRef": claim_id,
                        "workspaceGoalPin": series["data"]["workspaceGoalPin"],
                        "businessGoalPin": series["data"]["businessGoalPin"],
                        "strategyPin": {key: strategy[key] for key in ("strategyRef", "version", "bodyHash", "status", "approvedBy", "approvedAt")},
                        "envelopePin": strategy["envelope"],
                        "planPin": successor_plan_pin or series["data"]["planPin"],
                        "evaluationPin": series["data"]["evaluationPin"],
                        "predecessorCycleRef": series["data"].get("lastCycleRef"),
                        "successorCycleRef": None,
                        "predecessorDecisionRef": decision_ref,
                        "controlOnly": True,
                    }
                    self._insert_entity(
                        connection,
                        entity_id=cycle_id,
                        entity_type="CYCLE",
                        company_id=series["company_id"],
                        workspace_id=series["workspace_id"],
                        parent_id=series_id,
                        owner_ref=series["owner_ref"],
                        lifecycle_status="PLANNED",
                        current_version_id=strategy["strategyRef"],
                        data={"autonomousControl": control, "executionStatus": "NOT_STARTED"},
                        at=at,
                    )
                    self._link(connection, series["company_id"], series["workspace_id"], series_id, "HAS_CYCLE", cycle_id, at)
                    merged = False
            claim_data = {
                "seriesRef": series_id,
                "sourceType": source_type,
                "sourceKey": source_key,
                "cycleRef": cycle_id,
                "merged": merged,
                "cancelReason": cancel_reason,
                "decisionRef": decision_ref,
                "claimedAt": at,
                "appliedAt": at if claim_status == "APPLIED" else None,
                "cancelledAt": at if claim_status == "CANCELLED" else None,
            }
            self._insert_entity(
                connection,
                entity_id=claim_id,
                entity_type="TRIGGER_CLAIM",
                company_id=series["company_id"],
                workspace_id=series["workspace_id"],
                parent_id=series_id,
                owner_ref=series["owner_ref"],
                lifecycle_status=claim_status,
                data=claim_data,
                at=at,
            )
            self._link(connection, series["company_id"], series["workspace_id"], series_id, "HAS_TRIGGER_CLAIM", claim_id, at)
            if cycle_id:
                self._link(connection, series["company_id"], series["workspace_id"], cycle_id, "TRIGGERED_BY", claim_id, at)
            if claim_status == "APPLIED" and not merged:
                series_data = dict(series["data"])
                if decision and successor_strategy["strategyRef"] != series_data["currentStrategyRef"]:
                    series_data["strategyVersions"] = [*series_data["strategyVersions"], successor_strategy]
                    series_data["currentStrategyRef"] = successor_strategy["strategyRef"]
                series_data["currentCycleRef"] = cycle_id
                series_data["updatedAt"] = at
                if decision:
                    predecessor_data = dict(predecessor["data"])
                    predecessor_control = dict(predecessor_data.get("autonomousControl") or {})
                    if predecessor_control.get("successorCycleRef") not in (None, cycle_id):
                        raise AutonomousControlError("Predecessor already references another successor Cycle")
                    if (
                        predecessor_control.get("strategyPin", {}).get("strategyRef") != decision["data"].get("strategyRef")
                        or predecessor_control.get("envelopePin", {}).get("envelopeRef") != decision["data"].get("envelopeRef")
                    ):
                        raise AutonomousControlError("Predecessor pins do not match the applied Decision")
                    predecessor_control["successorCycleRef"] = cycle_id
                    predecessor_data["autonomousControl"] = predecessor_control
                    decision_data = dict(decision["data"])
                    decision_data.update({"successorTriggerClaimRef": claim_id, "successorCycleRef": cycle_id})
                    connection.execute(
                        "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                        (_json(predecessor_data), at, self.tenant_id, predecessor_id),
                    )
                    connection.execute(
                        "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                        (_json(decision_data), at, self.tenant_id, decision_ref),
                    )
                    self._link(connection, series["company_id"], series["workspace_id"], predecessor_id, "HAS_SUCCESSOR", cycle_id, at)
                    self._link(connection, series["company_id"], series["workspace_id"], cycle_id, "AUTHORIZED_BY_DECISION", decision_ref, at)
                connection.execute(
                    "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                    (_json(series_data), at, self.tenant_id, series_id),
                )
            claim = self._entity(self._row(connection, claim_id, entity_type="TRIGGER_CLAIM"))
            cycle = self._entity(self._row(connection, cycle_id, entity_type="CYCLE")) if cycle_id else None
            return {"claim": claim, "cycle": cycle, "replayed": False, "merged": merged}

    def authorize_successor(self, decision_id: str) -> dict[str, Any]:
        """Apply one canonical Decision to the existing Trigger Claim/Cycle factory."""
        with self.db.connect() as connection:
            decision = self._entity(self._row(connection, decision_id, entity_type="DECISION_PACKET"))
        data = decision["data"]
        if data.get("kind") != "NEXT_CYCLE_DECISION":
            raise AutonomousControlError("Decision Packet is not a next-cycle authority")
        if data.get("decision") not in {"CONTINUE", "ADJUST"}:
            return {"decision": decision, "claim": None, "cycle": None, "created": False}
        if decision["lifecycle_status"] != "APPLIED" or data.get("ceoGateRequired"):
            raise AutonomousControlError("Next-cycle Decision is not applied successor authority")
        series = self.get_series(data["seriesRef"])
        if series["lifecycle_status"] != "ACTIVE":
            raise AutonomousControlError("Successor authorization requires an ACTIVE Operating Series")
        result = self.claim_trigger(
            series_id=data["seriesRef"], source_type="RESULT",
            source_key=f"next-cycle-decision:{decision_id}", decision_ref=decision_id,
        )
        return {"decision": RuntimeFoundation(self.db).get(decision_id), **result, "created": not result["replayed"]}

    def cancel_claim(self, claim_id: str, *, reason: str) -> dict[str, Any]:
        reason = reason.strip()
        if not reason:
            raise AutonomousControlError("Claim cancellation requires a reason")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            row = self._row(connection, claim_id, entity_type="TRIGGER_CLAIM")
            if row["lifecycle_status"] == "CANCELLED":
                return self._entity(row)
            if row["lifecycle_status"] != "CLAIMED":
                raise AutonomousControlError("Only an unapplied Trigger Claim can be cancelled")
            data = json.loads(row["data_json"])
            at = _now()
            data.update({"cancelReason": reason, "cancelledAt": at})
            connection.execute(
                "update runtime_entities set lifecycle_status='CANCELLED', data_json=?, updated_at=? "
                "where tenant_id=? and entity_id=? and lifecycle_status='CLAIMED'",
                (_json(data), at, self.tenant_id, claim_id),
            )
            return self._entity(self._row(connection, claim_id, entity_type="TRIGGER_CLAIM"))

    def list_cycles(self, series_id: str) -> list[dict[str, Any]]:
        with self.db.connect() as connection:
            self._row(connection, series_id, entity_type="OPERATING_SERIES")
            rows = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_type='CYCLE' "
                "and json_extract(data_json, '$.autonomousControl.seriesRef')=? order by created_at, entity_id",
                (self.tenant_id, series_id),
            ).fetchall()
        return [self._entity(row) for row in rows]

    def materialize_cycle_work(
        self,
        *,
        series_id: str,
        cycle_id: str,
        workflow_key: str,
        plan: dict[str, Any],
    ) -> dict[str, Any]:
        """Release one Phase-1 Cycle into the existing Team Operating runtime."""
        plan_snapshot = self._approved_snapshot("Plan", plan)
        key = workflow_key.strip()
        if not key:
            raise AutonomousControlError("Plan requires an existing Team Operating workflow")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            series = self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))
            cycle = self._entity(self._row(connection, cycle_id, entity_type="CYCLE"))
            if series["lifecycle_status"] != "ACTIVE":
                raise AutonomousControlError("Operating Series is not ACTIVE")
            control = dict(cycle["data"].get("autonomousControl") or {})
            if control.get("seriesRef") != series_id or control.get("successorCycleRef") is not None:
                raise AutonomousControlError("Cycle control truth is not intact")
            claim = self._entity(self._row(connection, str(control.get("triggerClaimRef") or ""), entity_type="TRIGGER_CLAIM"))
            if claim["lifecycle_status"] != "APPLIED" or claim["data"].get("cycleRef") != cycle_id:
                raise AutonomousControlError("Cycle has no applied canonical Trigger Claim")
            workspace, business, blueprint = self._workspace_truth(
                connection, series["company_id"], series["workspace_id"],
            )
            if (
                control.get("workspaceGoalPin") != series["data"].get("workspaceGoalPin")
                or control.get("businessGoalPin") != series["data"].get("businessGoalPin")
                or control.get("workspaceGoalPin", {}).get("valueHash") != _hash(str(blueprint["goal"]).strip())
                or control.get("businessGoalPin", {}).get("valueHash") != _hash(str(business["goal"] or "").strip())
            ):
                raise AutonomousControlError("Cycle Goal pins no longer match canonical truth")
            self._leader_assignment(
                connection, series["company_id"], series["workspace_id"], series["owner_ref"],
            )
            workflows = connection.execute(
                "select * from runtime_entities where tenant_id=? and company_id=? and workspace_id=? "
                "and entity_type='RESPONSIBILITY_WORKFLOW' order by created_at, entity_id",
                (self.tenant_id, series["company_id"], series["workspace_id"]),
            ).fetchall()
            matches = [
                self._entity(row) for row in workflows
                if (data := json.loads(row["data_json"]))
                and data.get("scopeType") == "WORKSPACE"
                and data.get("scopeRef") == series["workspace_id"]
                and data.get("workflowKey") == key
            ]
            if not matches:
                raise AutonomousControlError("No existing Team Operating workflow matches the Plan")
            workflow = max(matches, key=lambda item: int(item["data"].get("version") or 0))
            leaders = [item for item in workflow["data"]["assignments"] if item.get("isLeader")]
            if len(leaders) != 1 or leaders[0].get("assignmentRef") != series["owner_ref"]:
                raise AutonomousControlError("Plan workflow does not resolve the canonical Operating Leader")
            assignments = {item["responsibilityKey"]: item for item in workflow["data"]["assignments"]}
            for responsibility_key in workflow["data"].get("defaultFlow") or []:
                assignment = assignments[responsibility_key]
                employee = self._row(connection, assignment["employeeRef"], entity_type="AI_EMPLOYEE")
                if employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}:
                    raise AutonomousControlError("Plan Employee is not available")
                employee_data = json.loads(employee["data_json"])
                company_employee_ref = str(employee_data.get("companyEmployeeRef") or employee["entity_id"])
                bindings = connection.execute(
                    "select * from employee_capability_bindings where tenant_id=? and employee_id=? and enabled=1",
                    (self.tenant_id, company_employee_ref),
                ).fetchall()
                if len(bindings) != 1:
                    raise AutonomousControlError("Plan Employee permission binding is missing or ambiguous")
                binding = bindings[0]
                if binding["capability_source"] == "tenant_private":
                    capability = connection.execute(
                        "select status from tenant_private_capabilities where tenant_id=? and capability_type=? and capability_id=?",
                        (self.tenant_id, binding["capability_type"], binding["capability_id"]),
                    ).fetchone()
                    if capability is None or capability["status"] != "active":
                        raise AutonomousControlError("Plan Employee capability is unavailable")
                elif binding["capability_source"] == "official":
                    capability = connection.execute(
                        "select 1 from official_models where model_key=? and status='active'",
                        (binding["capability_id"],),
                    ).fetchone()
                    if capability is None:
                        raise AutonomousControlError("Plan Employee capability is unavailable")
                else:
                    raise AutonomousControlError("Plan Employee capability source is unsupported")
            existing = dict(control.get("planPin") or {})
            plan_pin = {
                **plan_snapshot,
                "workflowRef": workflow["entity_id"],
                "workflowVersion": workflow["data"]["version"],
                "workflowKey": key,
            }
            if existing.get("status") == "APPROVED" and existing != plan_pin:
                raise AutonomousControlError("Cycle already owns a different approved Plan")
            if cycle["data"].get("responsibilityRouting", {}).get("currentExecutorRef"):
                raise AutonomousControlError("Cycle already has an active Employee execution")
            control["planPin"] = plan_pin
            data = dict(cycle["data"])
            data["autonomousControl"] = control
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(data), _now(), self.tenant_id, cycle_id),
            )

        routing = ResponsibilityRoutingRuntime(self.db)
        work = routing.start_work(
            cycle_id, scope_type="WORKSPACE", scope_ref=series["workspace_id"], workflow_key=key,
        )
        foundation = RuntimeFoundation(self.db)
        current = foundation.get(cycle_id)
        if current["lifecycle_status"] == "PLANNED":
            current = foundation.transition(cycle_id, "READY", actor="CEO", trigger="ready", reason="Approved bounded Plan released")
        if current["lifecycle_status"] == "READY":
            current = foundation.transition(cycle_id, "RUNNING", actor="CEO", trigger="start", reason="Team Operating accepted the Work")
        return current

    def request_cycle_close(self, *, series_id: str, cycle_id: str) -> dict[str, Any]:
        """Persist existing result/evidence truth and request ordinary Acceptance."""
        foundation = RuntimeFoundation(self.db)
        cycle = foundation.get(cycle_id)
        if cycle["lifecycle_status"] in {"WAITING_CEO", "ACCEPTED", "REVIEWING", "CLOSED"}:
            return cycle
        if cycle["lifecycle_status"] != "RUNNING":
            raise AutonomousControlError("Only a RUNNING Cycle can request close")
        try:
            child_work = CanonicalChildWorkRuntime(self.db).aggregate_cycle(cycle_id, require_complete=True)
        except ChildWorkError as error:
            raise AutonomousControlError(str(error)) from error
        if child_work["mode"] == "CHILD_WORK":
            result_refs = list(child_work["resultRefs"])
            artifact_refs = list(child_work["artifactRefs"])
            provider_evidence_refs = list(child_work["evidenceRefs"])
        else:
            route = dict(cycle["data"].get("responsibilityRouting") or {})
            if route.get("status") != "COMPLETED" or route.get("currentExecutorRef") is not None:
                raise AutonomousControlError("Team Operating Work is not complete")
            result_refs = list(route.get("resultRefs") or [])
            artifact_refs = list(route.get("artifactRefs") or [])
            provider_evidence_refs = list(route.get("evidenceRefs") or [])
        if not result_refs or not artifact_refs or not provider_evidence_refs:
            raise AutonomousControlError("Cycle close requires real Result, Artifact and Provider evidence")
        evidence_id = _stable_id("evidence", self.tenant_id, series_id, cycle_id, "execution")
        acceptance_id = _stable_id("acceptance", self.tenant_id, series_id, cycle_id)
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            series = self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))
            live_cycle = self._entity(self._row(connection, cycle_id, entity_type="CYCLE"))
            control = live_cycle["data"].get("autonomousControl") or {}
            if control.get("seriesRef") != series_id or control.get("successorCycleRef") is not None:
                raise AutonomousControlError("Cycle control truth is not intact")
            task_ids = [ref.split(":", 1)[1] for ref in result_refs if ref.startswith("task:")]
            if len(task_ids) != len(result_refs):
                raise AutonomousControlError("Cycle Result reference is not an existing Provider Task")
            for task_id in task_ids:
                task = connection.execute(
                    "select status, company_id from tasks where tenant_id=? and task_id=?",
                    (self.tenant_id, task_id),
                ).fetchone()
                if task is None or task["status"] != "COMPLETED" or task["company_id"] != series["company_id"]:
                    raise AutonomousControlError("Cycle Result Task is not completed in the canonical Company")
            if child_work["mode"] == "LEGACY":
                event_ids = {str(value) for value in provider_evidence_refs}
                found_events = {
                    str(row["event_id"]) for row in connection.execute(
                        "select event_id from evolution_events where tenant_id=? and event_type='usage.task_execution'",
                        (self.tenant_id,),
                    ).fetchall()
                    if str(row["event_id"]) in event_ids
                }
                if found_events != event_ids:
                    raise AutonomousControlError("Cycle Provider evidence is missing")
            evidence_data = {
                "kind": "MULTI_WORK_EXECUTION" if child_work["mode"] == "CHILD_WORK" else "SINGLE_CYCLE_EXECUTION",
                "seriesRef": series_id,
                "cycleRef": cycle_id,
                "workspaceRef": series["workspace_id"],
                "goalPin": control["workspaceGoalPin"],
                "planPin": control["planPin"],
                "leaderAssignmentRef": series["owner_ref"],
                "resultRefs": result_refs,
                "artifactRefs": artifact_refs,
                "providerEvidenceRefs": provider_evidence_refs,
            }
            if child_work["mode"] == "CHILD_WORK":
                evidence_data.update({
                    "workSummaries": child_work["workSummaries"],
                    "workAcceptanceRefs": child_work["acceptanceRefs"],
                    "aggregationHash": child_work["aggregationHash"],
                })
            existing_evidence = connection.execute(
                "select data_json from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, evidence_id),
            ).fetchone()
            if existing_evidence is None:
                self._insert_entity(
                    connection, entity_id=evidence_id, entity_type="EVIDENCE",
                    company_id=series["company_id"], workspace_id=series["workspace_id"],
                    parent_id=cycle_id, owner_ref=series["owner_ref"], lifecycle_status="CURRENT",
                    data=evidence_data, at=_now(),
                )
                connection.execute(
                    "update runtime_entities set verification_status='VERIFIED', evidence_condition='CURRENT' "
                    "where tenant_id=? and entity_id=?",
                    (self.tenant_id, evidence_id),
                )
            elif json.loads(existing_evidence["data_json"]) != evidence_data:
                raise AutonomousControlError("Cycle Evidence replay has different truth")
            existing_acceptance = connection.execute(
                "select data_json from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, acceptance_id),
            ).fetchone()
            acceptance_data = {
                "seriesRef": series_id, "cycleRef": cycle_id, "evidenceRefs": [evidence_id],
                "resultRefs": result_refs, "artifactRefs": artifact_refs,
            }
            if existing_acceptance is None:
                self._insert_entity(
                    connection, entity_id=acceptance_id, entity_type="ACCEPTANCE",
                    company_id=series["company_id"], workspace_id=series["workspace_id"],
                    parent_id=cycle_id, owner_ref="CEO", lifecycle_status="PENDING",
                    data=acceptance_data, at=_now(),
                )
            elif json.loads(existing_acceptance["data_json"]) != acceptance_data:
                raise AutonomousControlError("Cycle Acceptance replay has different truth")
            data = dict(live_cycle["data"])
            data.update({
                "resultRefs": result_refs, "artifactRefs": artifact_refs,
                "evidenceRefs": [evidence_id], "acceptanceId": acceptance_id,
                "executionOutcome": "COMPLETED", "executionCompletedAt": _now(),
            })
            if child_work["mode"] == "CHILD_WORK":
                data["childWorkAggregation"] = {
                    "workRefs": child_work["workRefs"],
                    "workAcceptanceRefs": child_work["acceptanceRefs"],
                    "aggregationHash": child_work["aggregationHash"],
                }
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(data), _now(), self.tenant_id, cycle_id),
            )
            self._link(connection, series["company_id"], series["workspace_id"], cycle_id, "HAS_EVIDENCE", evidence_id, _now())
            self._link(connection, series["company_id"], series["workspace_id"], cycle_id, "HAS_ACCEPTANCE", acceptance_id, _now())
        return foundation.transition(
            cycle_id, "WAITING_CEO", actor="SYSTEM", trigger="request_acceptance",
            reason="Bounded Team Operating execution completed", evidence_refs=[evidence_id],
        )

    def accept_and_close_cycle(self, *, series_id: str, cycle_id: str, reason: str) -> dict[str, Any]:
        """Apply ordinary CEO Acceptance; this is not a next-cycle Decision."""
        foundation = RuntimeFoundation(self.db)
        cycle = foundation.get(cycle_id)
        if cycle["lifecycle_status"] == "CLOSED":
            return cycle
        if cycle["lifecycle_status"] != "WAITING_CEO":
            raise AutonomousControlError("Cycle is not waiting for Acceptance")
        acceptance_id = str(cycle["data"].get("acceptanceId") or "")
        acceptance = foundation.get(acceptance_id)
        if acceptance["lifecycle_status"] == "PENDING":
            acceptance = foundation.transition(acceptance_id, "ACCEPTED", actor="CEO", trigger="accept", reason=reason)
        cycle = foundation.transition(
            cycle_id, "ACCEPTED", actor="CEO", trigger="accept", reason=reason,
            context={"acceptanceId": acceptance_id}, evidence_refs=cycle["data"].get("evidenceRefs") or [],
        )
        cycle = foundation.transition(cycle_id, "REVIEWING", actor="SYSTEM", trigger="review", reason="Acceptance recorded")
        cycle = foundation.transition(cycle_id, "CLOSED", actor="CEO", trigger="close", reason=reason)
        if acceptance["lifecycle_status"] == "ACCEPTED":
            foundation.transition(acceptance_id, "CLOSED", actor="SYSTEM", trigger="close", reason="Cycle closed")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            series = self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))
            if series["lifecycle_status"] != "ACTIVE":
                raise AutonomousControlError("Cycle close must not replace Series lifecycle truth")
            data = dict(series["data"])
            data.update({"currentCycleRef": None, "lastCycleRef": cycle_id, "updatedAt": _now()})
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(data), data["updatedAt"], self.tenant_id, series_id),
            )
        return foundation.get(cycle_id)

    @staticmethod
    def _evaluation_contract(value: dict[str, Any]) -> dict[str, Any]:
        snapshot = AutonomousOperatingControl._approved_snapshot("Evaluation Contract", value)
        required = {
            "observationWindow", "success", "failure", "insufficientEvidence",
            "continueObservation", "escalateWhen",
        }
        if any(not snapshot["body"].get(key) for key in required):
            raise AutonomousControlError("Evaluation Contract is missing required bounded evaluation semantics")
        return snapshot

    @staticmethod
    def _validate_observed_facts(facts: list[dict[str, Any]], allowed_refs: set[str]) -> list[dict[str, Any]]:
        if not facts:
            raise AutonomousControlError("Evaluation requires observed facts")
        seen: dict[str, str] = {}
        normalized = []
        for fact in facts:
            name = str(fact.get("name") or "").strip()
            source_ref = str(fact.get("sourceRef") or "").strip()
            if not name or "value" not in fact or source_ref not in allowed_refs:
                raise AutonomousControlError("Evaluation fact must reference existing Cycle Result/Evidence/Acceptance")
            value_hash = _hash(fact["value"])
            if name in seen and seen[name] != value_hash:
                raise AutonomousControlError("Evaluation evidence conflicts for the same observed fact")
            seen[name] = value_hash
            normalized.append({"name": name, "value": fact["value"], "sourceRef": source_ref})
        return normalized

    def _phase3a_truth(self, connection, series_id: str, cycle_id: str) -> tuple[dict, dict, dict, dict]:
        series = self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))
        cycle = self._entity(self._row(connection, cycle_id, entity_type="CYCLE"))
        control = dict(cycle["data"].get("autonomousControl") or {})
        if (
            cycle["lifecycle_status"] != "CLOSED"
            or control.get("seriesRef") != series_id
            or control.get("successorCycleRef") is not None
            or series["data"].get("lastCycleRef") != cycle_id
        ):
            raise AutonomousControlError("Phase 3A requires the canonical closed Cycle with no successor")
        strategy = series["data"]["strategyVersions"][-1]
        expected_strategy = {
            key: strategy[key] for key in ("strategyRef", "version", "bodyHash", "status", "approvedBy", "approvedAt")
        }
        if control.get("strategyPin") != expected_strategy or control.get("envelopePin") != strategy["envelope"]:
            raise AutonomousControlError("Cycle Strategy or Approved Strategy Envelope pin is stale")
        assignment = self._leader_assignment(
            connection, series["company_id"], series["workspace_id"], series["owner_ref"],
        )
        employee = self._row(connection, assignment["data"]["employeeRef"], entity_type="AI_EMPLOYEE")
        if employee["lifecycle_status"] not in {"AVAILABLE", "OPERATING"}:
            raise AutonomousControlError("Canonical Workspace Leader is unavailable")
        return series, cycle, control, strategy

    def evaluate_closed_cycle(
        self,
        *,
        series_id: str,
        cycle_id: str,
        contract: dict[str, Any],
        outcome: str,
        observed_facts: list[dict[str, Any]],
        comparison: dict[str, Any],
        confidence: str,
        sufficiency: str,
    ) -> dict[str, Any]:
        """Persist one evidence-bound Evaluation on the existing closed Cycle."""
        contract_snapshot = self._evaluation_contract(contract)
        outcome = outcome.upper()
        sufficiency = sufficiency.upper()
        if outcome not in EVALUATION_OUTCOMES:
            raise AutonomousControlError("Unsupported Evaluation outcome")
        if sufficiency not in {"SUFFICIENT", "INSUFFICIENT"}:
            raise AutonomousControlError("Evaluation sufficiency must be explicit")
        if (outcome == "INSUFFICIENT") != (sufficiency == "INSUFFICIENT"):
            raise AutonomousControlError("Evaluation outcome and sufficiency conflict")
        if not comparison or not str(confidence).strip():
            raise AutonomousControlError("Evaluation requires comparison and confidence")
        try:
            child_work = CanonicalChildWorkRuntime(self.db).aggregate_cycle(cycle_id, require_complete=True)
        except ChildWorkError as error:
            raise AutonomousControlError(str(error)) from error
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            series, cycle, control, strategy = self._phase3a_truth(connection, series_id, cycle_id)
            evidence_refs = list(cycle["data"].get("evidenceRefs") or [])
            result_refs = list(cycle["data"].get("resultRefs") or [])
            artifact_refs = list(cycle["data"].get("artifactRefs") or [])
            acceptance_ref = str(cycle["data"].get("acceptanceId") or "")
            if not evidence_refs or not result_refs or not acceptance_ref:
                raise AutonomousControlError("Closed Cycle is missing Result/Evidence/Acceptance truth")
            if child_work["mode"] == "CHILD_WORK":
                persisted = cycle["data"].get("childWorkAggregation") or {}
                if persisted.get("aggregationHash") != child_work["aggregationHash"]:
                    raise AutonomousControlError("Closed Cycle child Work aggregation is stale")
            for ref in result_refs:
                if not ref.startswith("task:"):
                    raise AutonomousControlError("Evaluation Result reference is not a Provider Task")
                task = connection.execute(
                    "select status, company_id from tasks where tenant_id=? and task_id=?",
                    (self.tenant_id, ref.split(":", 1)[1]),
                ).fetchone()
                if task is None or task["status"] != "COMPLETED" or task["company_id"] != series["company_id"]:
                    raise AutonomousControlError("Evaluation Result is missing or not completed in the canonical Company")
            for ref in evidence_refs:
                evidence = self._row(connection, ref, entity_type="EVIDENCE")
                if (
                    evidence["parent_id"] != cycle_id
                    or evidence["verification_status"] != "VERIFIED"
                    or evidence["evidence_condition"] != "CURRENT"
                ):
                    raise AutonomousControlError("Cycle Evidence is missing, stale or unverified")
            acceptance = self._entity(self._row(connection, acceptance_ref, entity_type="ACCEPTANCE"))
            if acceptance["lifecycle_status"] != "CLOSED" or acceptance["data"].get("evidenceRefs") != evidence_refs:
                raise AutonomousControlError("Cycle Acceptance does not cover the current Evidence")
            facts = self._validate_observed_facts(
                observed_facts,
                set(
                    result_refs + artifact_refs + evidence_refs + [acceptance_ref]
                    + (child_work.get("acceptanceRefs") or [])
                ),
            )
            contract_ref = _stable_id(
                "evaluation-contract", self.tenant_id, series_id,
                contract_snapshot["version"], contract_snapshot["bodyHash"],
            )
            contract_pin = {"contractRef": contract_ref, **contract_snapshot}
            existing_pin = dict(series["data"].get("evaluationPin") or {})
            if existing_pin.get("status") == "APPROVED" and existing_pin != contract_pin:
                raise AutonomousControlError("Operating Series is pinned to a different Evaluation Contract")
            payload = {
                "contractPin": contract_pin,
                "cycleRef": cycle_id,
                "resultRefs": result_refs,
                "evidenceRefs": evidence_refs,
                "acceptanceRef": acceptance_ref,
                "goalPin": control["workspaceGoalPin"],
                "strategyPin": control["strategyPin"],
                "envelopePin": control["envelopePin"],
                "observedFacts": facts,
                "comparison": comparison,
                "confidence": str(confidence).upper(),
                "sufficiency": sufficiency,
                "outcome": outcome,
            }
            if child_work["mode"] == "CHILD_WORK":
                payload.update({
                    "workRefs": child_work["workRefs"],
                    "workSummaries": child_work["workSummaries"],
                    "workAcceptanceRefs": child_work["acceptanceRefs"],
                    "aggregationHash": child_work["aggregationHash"],
                })
            input_hash = _hash(payload)
            evaluation_ref = _stable_id("evaluation", self.tenant_id, series_id, cycle_id)
            existing = cycle["data"].get("autonomousEvaluation")
            if existing:
                if existing.get("inputHash") != input_hash:
                    raise AutonomousControlError("Closed Cycle already has a conflicting Evaluation")
                return existing
            at = _now()
            evaluation = {
                "evaluationRef": evaluation_ref,
                **payload,
                "inputHash": input_hash,
                "evaluatedAt": at,
            }
            cycle_data = dict(cycle["data"])
            control["evaluationPin"] = contract_pin
            cycle_data["autonomousControl"] = control
            cycle_data["autonomousEvaluation"] = evaluation
            series_data = dict(series["data"])
            series_data["evaluationPin"] = contract_pin
            series_data["updatedAt"] = at
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(cycle_data), at, self.tenant_id, cycle_id),
            )
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(series_data), at, self.tenant_id, series_id),
            )
            return evaluation

    @staticmethod
    def _decision_authority(
        decision: str, strategy: dict[str, Any], adjustment: dict[str, Any] | None,
    ) -> tuple[str, str, bool]:
        requested = decision
        if decision == "ADJUST":
            changes = set((adjustment or {}).get("changes") or {})
            allowed = set(strategy["envelope"]["body"].get("allowed") or [])
            protected = set(strategy["envelope"]["body"].get("protected") or [])
            if not changes:
                raise AutonomousControlError("ADJUST requires explicit bounded changes")
            if changes - allowed or changes & protected:
                return "ESCALATE", "CEO_GATE_OUTSIDE_APPROVED_STRATEGY_ENVELOPE", True
            return decision, "APPROVED_STRATEGY_ENVELOPE", False
        if decision in {"CONTINUE", "WAIT"}:
            return decision, "APPROVED_STRATEGY_ENVELOPE", False
        if decision == "ESCALATE":
            return decision, "CEO_GATE_REQUIRED", True
        if decision in {"PAUSE", "STOP"}:
            return decision, f"CEO_{decision}_AUTHORITY_REQUIRED", True
        raise AutonomousControlError(f"Unsupported next-cycle decision: {requested}")

    def review_next_cycle(
        self,
        *,
        series_id: str,
        cycle_id: str,
        decision: str,
        reason: str,
        adjustment: dict[str, Any] | None = None,
        wait_reason: str | None = None,
        next_check_at: str | None = None,
        actor: str = "LEADER",
    ) -> dict[str, Any]:
        """Persist one Leader Review and one canonical existing Decision Packet."""
        requested = decision.upper()
        if requested not in NEXT_CYCLE_DECISIONS or not reason.strip():
            raise AutonomousControlError("Next-cycle Decision requires a supported choice and reason")
        actor = actor.upper()
        if actor not in {"LEADER", "CEO"}:
            raise AutonomousControlError("Next-cycle Decision actor must be LEADER or CEO")
        if requested == "WAIT" and not (str(wait_reason or "").strip() and next_check_at):
            raise AutonomousControlError("WAIT requires a reason and nextCheckAt")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            series, cycle, control, strategy = self._phase3a_truth(connection, series_id, cycle_id)
            evaluation = cycle["data"].get("autonomousEvaluation")
            if not evaluation:
                raise AutonomousControlError("Leader Review requires an evidence-bound Evaluation")
            if evaluation["sufficiency"] == "INSUFFICIENT" and requested in {"CONTINUE", "ADJUST"}:
                raise AutonomousControlError("Insufficient Evidence cannot continue or adjust autonomously")
            resolved, authority_basis, ceo_gate = self._decision_authority(requested, strategy, adjustment)
            if actor == "CEO" and resolved in {"PAUSE", "STOP"}:
                authority_basis, ceo_gate = "CEO", False
            elif actor == "CEO" and resolved == "ESCALATE":
                raise AutonomousControlError("ESCALATE records a CEO Gate; it is not a CEO terminal choice")
            assignment = self._leader_assignment(
                connection, series["company_id"], series["workspace_id"], series["owner_ref"],
            )
            leader_ref = assignment["data"]["employeeRef"]
            review_ref = _stable_id("leader-review", self.tenant_id, series_id, cycle_id)
            decision_id = _stable_id("decision", self.tenant_id, series_id, cycle_id, "next-cycle")
            decision_input = {
                "kind": "NEXT_CYCLE_DECISION",
                "seriesRef": series_id,
                "cycleRef": cycle_id,
                "evaluationRef": evaluation["evaluationRef"],
                "reviewRef": review_ref,
                "requestedDecision": requested,
                "decision": resolved,
                "reason": reason.strip(),
                "adjustment": adjustment or None,
                "waitReason": str(wait_reason or "").strip() or None,
                "nextCheckAt": next_check_at,
                "evidenceRefs": evaluation["evidenceRefs"],
                "actorRef": "CEO" if actor == "CEO" else leader_ref,
                "leaderAssignmentRef": series["owner_ref"],
                "authorityBasis": authority_basis,
                "strategyRef": strategy["strategyRef"],
                "strategyVersion": strategy["version"],
                "envelopeRef": strategy["envelope"]["envelopeRef"],
                "envelopeVersion": strategy["envelope"]["version"],
                "ceoGateRequired": ceo_gate,
                "successorCycleRef": None,
                "plainPackage": {
                    "whatHappened": f"Cycle evaluation: {evaluation['outcome']}",
                    "whyLeaderCannotDecide": authority_basis if ceo_gate else None,
                    "proposedChoice": resolved,
                    "reason": reason.strip(),
                    "afterChoice": "Record decision truth only; no successor Cycle is created in Phase 3A",
                    "evidenceRefs": evaluation["evidenceRefs"],
                },
            }
            input_hash = _hash(decision_input)
            existing = connection.execute(
                "select * from runtime_entities where tenant_id=? and entity_id=?",
                (self.tenant_id, decision_id),
            ).fetchone()
            if existing is not None:
                packet = self._entity(existing)
                if packet["data"].get("inputHash") != input_hash:
                    raise AutonomousControlError("Closed Cycle already has a conflicting next-cycle Decision")
            else:
                at = _now()
                packet_data = {**decision_input, "inputHash": input_hash, "recordedAt": at}
                self._insert_entity(
                    connection, entity_id=decision_id, entity_type="DECISION_PACKET",
                    company_id=series["company_id"], workspace_id=series["workspace_id"],
                    parent_id=cycle_id, owner_ref=series["owner_ref"], lifecycle_status="DRAFT",
                    next_check_at=next_check_at, data=packet_data, at=at,
                )
                review = {
                    "reviewRef": review_ref,
                    "evaluationRef": evaluation["evaluationRef"],
                    "leaderAssignmentRef": series["owner_ref"],
                    "leaderEmployeeRef": leader_ref,
                    "decisionPacketRef": decision_id,
                    "decision": resolved,
                    "reviewedAt": at,
                }
                cycle_data = dict(cycle["data"])
                cycle_data["autonomousLeaderReview"] = review
                cycle_data["nextCycleDecisionRef"] = decision_id
                connection.execute(
                    "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                    (_json(cycle_data), at, self.tenant_id, cycle_id),
                )
                self._link(connection, series["company_id"], series["workspace_id"], cycle_id, "HAS_NEXT_CYCLE_DECISION", decision_id, at)
        return self._advance_next_cycle_decision(decision_id)

    def _advance_next_cycle_decision(self, decision_id: str) -> dict[str, Any]:
        foundation = RuntimeFoundation(self.db)
        packet = foundation.get(decision_id)
        data = packet["data"]
        if packet["lifecycle_status"] == "DRAFT":
            packet = foundation.transition(decision_id, "READY", actor="SYSTEM", trigger="prepare")
        if data["ceoGateRequired"]:
            if packet["lifecycle_status"] == "READY":
                packet = foundation.transition(decision_id, "WAITING_CEO", actor="SYSTEM", trigger="request_decision")
            series = self.get_series(data["seriesRef"])
            if series["lifecycle_status"] == "ACTIVE":
                if not data.get("nextCheckAt"):
                    effective_next_check = packet["created_at"]
                    persisted = dict(data)
                    persisted["nextCheckAt"] = effective_next_check
                    with self.db.connect() as connection:
                        connection.execute(
                            "update runtime_entities set next_check_at=?, data_json=? where tenant_id=? and entity_id=?",
                            (effective_next_check, _json(persisted), self.tenant_id, decision_id),
                        )
                    data = persisted
                self.set_series_state(data["seriesRef"], "WAITING", next_check_at=data["nextCheckAt"])
            return foundation.get(decision_id)
        if data["actorRef"] == "CEO" and packet["lifecycle_status"] == "READY":
            packet = foundation.transition(
                decision_id, "WAITING_CEO", actor="SYSTEM", trigger="request_decision",
            )
        if data["actorRef"] == "CEO" and packet["lifecycle_status"] == "WAITING_CEO":
            packet = foundation.transition(
                decision_id, "DECIDED", actor="CEO", trigger="decide",
                reason=data["reason"], evidence_refs=data["evidenceRefs"],
                context={"decision": data["decision"]},
            )
        if packet["lifecycle_status"] == "READY":
            packet = foundation.transition(
                decision_id, "DECIDED", actor="AI_EMPLOYEE", trigger="leader_decide",
                reason=data["reason"], evidence_refs=data["evidenceRefs"],
                context={
                    "decisionDomain": "AUTONOMOUS_NEXT_CYCLE",
                    "leaderAuthorized": True,
                    "decision": data["decision"],
                },
            )
        if packet["lifecycle_status"] == "DECIDED":
            packet = foundation.transition(decision_id, "APPLIED", actor="SYSTEM", trigger="apply")
        self._apply_series_decision(data)
        return packet

    def apply_ceo_terminal_decision(self, decision_id: str, *, reason: str) -> dict[str, Any]:
        """Confirm a gated PAUSE/STOP without inventing a terminal policy."""
        foundation = RuntimeFoundation(self.db)
        packet = foundation.get(decision_id)
        data = packet["data"]
        if data.get("decision") not in {"PAUSE", "STOP"} or not data.get("ceoGateRequired"):
            raise AutonomousControlError("Decision Packet is not waiting for CEO terminal authority")
        if packet["lifecycle_status"] == "WAITING_CEO":
            packet = foundation.transition(
                decision_id, "DECIDED", actor="CEO", trigger="decide", reason=reason,
                evidence_refs=data["evidenceRefs"], context={"decision": data["decision"]},
            )
        if packet["lifecycle_status"] == "DECIDED":
            packet = foundation.transition(decision_id, "APPLIED", actor="SYSTEM", trigger="apply")
        if packet["lifecycle_status"] != "APPLIED":
            raise AutonomousControlError("Decision Packet is not in a CEO-applicable state")
        persisted = dict(data)
        persisted.update({"appliedActorRef": "CEO", "appliedAuthorityBasis": "CEO", "appliedAt": _now()})
        with self.db.connect() as connection:
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(persisted), persisted["appliedAt"], self.tenant_id, decision_id),
            )
        self._apply_series_decision(data)
        return foundation.get(decision_id)

    def _apply_series_decision(self, data: dict[str, Any]) -> None:
        decision = data["decision"]
        series = self.get_series(data["seriesRef"])
        if decision == "WAIT":
            if series["lifecycle_status"] == "ACTIVE":
                self.set_series_state(data["seriesRef"], "WAITING", next_check_at=data["nextCheckAt"])
        elif decision == "PAUSE":
            if series["lifecycle_status"] != "PAUSED":
                self.set_series_state(data["seriesRef"], "PAUSED")
        elif decision == "STOP":
            if series["lifecycle_status"] != "STOPPED":
                self.set_series_state(data["seriesRef"], "STOPPED")
        elif decision in {"CONTINUE", "ADJUST"} and series["lifecycle_status"] != "ACTIVE":
            self.set_series_state(data["seriesRef"], "ACTIVE")

    def fail_cycle(self, *, series_id: str, cycle_id: str, reason: str) -> dict[str, Any]:
        """Close a bounded technical failure without stopping its Series."""
        foundation = RuntimeFoundation(self.db)
        cycle = foundation.get(cycle_id)
        if cycle["lifecycle_status"] == "FAILED":
            return cycle
        if cycle["lifecycle_status"] != "RUNNING":
            raise AutonomousControlError("Only a RUNNING Cycle can record execution failure")
        data = dict(cycle["data"])
        route = dict(data.get("responsibilityRouting") or {})
        data.update({
            "executionOutcome": "FAILED",
            "failureReason": reason.strip()[:2000],
            "partialResultRefs": list(route.get("resultRefs") or []),
            "partialArtifactRefs": list(route.get("artifactRefs") or []),
            "partialEvidenceRefs": list(route.get("evidenceRefs") or []),
            "failedAt": _now(),
        })
        with self.db.connect() as connection:
            series = self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))
            if series["lifecycle_status"] != "ACTIVE" or data.get("autonomousControl", {}).get("seriesRef") != series_id:
                raise AutonomousControlError("Failure does not belong to an active Operating Series")
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(data), data["failedAt"], self.tenant_id, cycle_id),
            )
        return foundation.transition(cycle_id, "FAILED", actor="SYSTEM", trigger="fail", reason=reason)

    @staticmethod
    def _learning_artifact(row) -> dict[str, Any]:
        item = dict(row)
        item["data"] = json.loads(item["content"])
        return item

    def _learning_source_truth(
        self, connection, *, series_id: str, cycle_refs: list[str], scope_type: str, scope_ref: str,
    ) -> tuple[dict, list[dict], str, str]:
        series = self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))
        refs = list(dict.fromkeys(str(ref).strip() for ref in cycle_refs if str(ref).strip()))
        if len(refs) < 2:
            raise AutonomousControlError("Learning requires at least two distinct closed Cycles")
        workspace, _, blueprint = self._workspace_truth(connection, series["company_id"], series["workspace_id"])
        domain = str(blueprint.get("businessType") or "GENERIC").upper()
        scope_type = scope_type.upper()
        expected_scope = {
            "WORKSPACE": series["workspace_id"],
            "DOMAIN": domain,
            "COMPANY_CANDIDATE": series["company_id"],
        }.get(scope_type)
        if expected_scope is None or scope_ref != expected_scope:
            raise AutonomousControlError("Learning scope does not match the canonical Series")
        cycles = []
        for ref in refs:
            cycle = self._entity(self._row(connection, ref, entity_type="CYCLE"))
            data = cycle["data"]
            if (
                cycle["company_id"] != series["company_id"]
                or cycle["workspace_id"] != series["workspace_id"]
                or cycle["lifecycle_status"] != "CLOSED"
                or data.get("autonomousControl", {}).get("seriesRef") != series_id
                or not data.get("autonomousEvaluation")
                or not data.get("nextCycleDecisionRef")
            ):
                raise AutonomousControlError("Learning source Cycle is incomplete or outside the Series")
            decision = self._entity(self._row(connection, data["nextCycleDecisionRef"], entity_type="DECISION_PACKET"))
            if decision["lifecycle_status"] != "APPLIED" or decision["parent_id"] != ref:
                raise AutonomousControlError("Learning source requires an applied Cycle Decision")
            evidence_refs = list(data.get("evidenceRefs") or [])
            result_refs = list(data.get("resultRefs") or [])
            if not evidence_refs or not result_refs:
                raise AutonomousControlError("Learning source is missing Result or Evidence")
            for evidence_ref in evidence_refs:
                evidence = self._row(connection, evidence_ref, entity_type="EVIDENCE")
                if (
                    evidence["parent_id"] != ref
                    or evidence["verification_status"] != "VERIFIED"
                    or evidence["evidence_condition"] != "CURRENT"
                ):
                    raise AutonomousControlError("Learning source Evidence is stale or unverified")
            for result_ref in result_refs:
                if not result_ref.startswith("task:"):
                    raise AutonomousControlError("Learning source Result is not a Provider Task")
                task = connection.execute(
                    "select status, company_id from tasks where tenant_id=? and task_id=?",
                    (self.tenant_id, result_ref.split(":", 1)[1]),
                ).fetchone()
                if task is None or task["status"] != "COMPLETED" or task["company_id"] != series["company_id"]:
                    raise AutonomousControlError("Learning source Result is not completed in the canonical Company")
            cycles.append(cycle)
        source_task = cycles[-1]["data"]["resultRefs"][-1].split(":", 1)[1]
        return series, cycles, domain, source_task

    def create_learning_candidate(
        self,
        *,
        series_id: str,
        supporting_cycle_refs: list[str],
        claim: str,
        scope_type: str,
        scope_ref: str,
        confidence: str,
        conditions: list[str],
        limitations: list[str],
        proposed_use: str,
        revalidate_when: list[str],
        supersedes_refs: list[str] | None = None,
        conflicts_with_refs: list[str] | None = None,
    ) -> dict[str, Any]:
        """Persist a reviewable candidate from canonical two-Cycle truth only."""
        claim = claim.strip()
        confidence = confidence.upper()
        proposed_use = proposed_use.upper()
        if not claim or confidence not in {"HIGH", "MEDIUM", "LOW", "UNKNOWN"}:
            raise AutonomousControlError("Learning Candidate requires a claim and explicit confidence")
        if proposed_use not in {
            "FUTURE_CONTEXT", "FUTURE_PLAN_INPUT", "FUTURE_EVALUATION_INPUT",
            "STRATEGY_CHANGE", "GOAL_CHANGE", "PACKAGE_CHANGE", "COMPANY_POLICY",
        }:
            raise AutonomousControlError("Learning Candidate proposed use is unsupported")
        if not conditions or not limitations or not revalidate_when:
            raise AutonomousControlError("Learning Candidate requires conditions, limitations and revalidation criteria")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            series, cycles, domain, task_id = self._learning_source_truth(
                connection,
                series_id=series_id,
                cycle_refs=supporting_cycle_refs,
                scope_type=scope_type,
                scope_ref=scope_ref,
            )
            source_cycles = [cycle["entity_id"] for cycle in cycles]
            provenance = {
                "cycleRefs": source_cycles,
                "resultRefs": [ref for cycle in cycles for ref in cycle["data"]["resultRefs"]],
                "evidenceRefs": [ref for cycle in cycles for ref in cycle["data"]["evidenceRefs"]],
                "evaluationRefs": [cycle["data"]["autonomousEvaluation"]["evaluationRef"] for cycle in cycles],
                "decisionRefs": [cycle["data"]["nextCycleDecisionRef"] for cycle in cycles],
            }
            supersedes = list(dict.fromkeys(supersedes_refs or []))
            conflicts = list(dict.fromkeys(conflicts_with_refs or []))
            for ref in list(dict.fromkeys([*supersedes, *conflicts])):
                row = connection.execute(
                    "select * from artifacts where tenant_id=? and artifact_id=? and artifact_type='accepted_learning' and status='accepted'",
                    (self.tenant_id, ref),
                ).fetchone()
                if row is None:
                    raise AutonomousControlError("Learning can only supersede an active accepted Learning")
                old = json.loads(row["content"])
                if (
                    old.get("companyRef") != series["company_id"]
                    or old.get("scopeType") != scope_type.upper()
                    or old.get("scopeRef") != scope_ref
                ):
                    raise AutonomousControlError("Learning supersede scope mismatch")
            payload = {
                "kind": "LEARNING_CANDIDATE",
                "version": 1,
                "seriesRef": series_id,
                "companyRef": series["company_id"],
                "workspaceRef": series["workspace_id"],
                "domain": domain,
                "claim": claim,
                "scopeType": scope_type.upper(),
                "scopeRef": scope_ref,
                "confidence": confidence,
                "conditions": list(conditions),
                "limitations": list(limitations),
                "proposedUse": proposed_use,
                "revalidateWhen": list(revalidate_when),
                "supersedesRefs": supersedes,
                "conflictsWithRefs": conflicts,
                "provenance": provenance,
            }
            content = _json(payload)
            digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
            candidate_id = _stable_id("learning-candidate", self.tenant_id, series_id, digest)
            source_ref = f"autonomous.learning.candidate:{candidate_id}"
            existing = connection.execute(
                "select * from artifacts where tenant_id=? and artifact_id=?",
                (self.tenant_id, candidate_id),
            ).fetchone()
            if existing is None:
                connection.execute(
                    "insert into artifacts(artifact_id, tenant_id, task_id, title, artifact_type, status, content, source_ref, content_sha256) "
                    "values (?, ?, ?, ?, 'learning_candidate', 'generated', ?, ?, ?)",
                    (candidate_id, self.tenant_id, task_id, claim[:120], content, source_ref, digest),
                )
            elif existing["content_sha256"] != digest or existing["artifact_type"] != "learning_candidate":
                raise AutonomousControlError("Learning Candidate replay has conflicting truth")
            series_data = dict(series["data"])
            series_data["learningCandidateRefs"] = list(dict.fromkeys([
                *(series_data.get("learningCandidateRefs") or []), candidate_id,
            ]))
            latest = cycles[-1]
            cycle_data = dict(latest["data"])
            cycle_data["learningCandidateRefs"] = list(dict.fromkeys([
                *(cycle_data.get("learningCandidateRefs") or []), candidate_id,
            ]))
            at = _now()
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(series_data), at, self.tenant_id, series_id),
            )
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(cycle_data), at, self.tenant_id, latest["entity_id"]),
            )
            row = connection.execute(
                "select * from artifacts where tenant_id=? and artifact_id=?",
                (self.tenant_id, candidate_id),
            ).fetchone()
        return self._learning_artifact(row)

    def accept_learning_candidate(self, candidate_ref: str, *, actor: str) -> dict[str, Any]:
        """Create one separate accepted Artifact; Candidate remains reviewable history."""
        actor = actor.upper()
        if actor not in {"LEADER", "CEO"}:
            raise AutonomousControlError("Learning acceptance requires Leader or CEO authority")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            candidate_row = connection.execute(
                "select * from artifacts where tenant_id=? and artifact_id=? and artifact_type='learning_candidate'",
                (self.tenant_id, candidate_ref),
            ).fetchone()
            if candidate_row is None:
                raise KeyError(candidate_ref)
            candidate = json.loads(candidate_row["content"])
            series = self._entity(self._row(connection, candidate["seriesRef"], entity_type="OPERATING_SERIES"))
            protected_use = candidate["proposedUse"] in {
                "STRATEGY_CHANGE", "GOAL_CHANGE", "PACKAGE_CHANGE", "COMPANY_POLICY",
            }
            if actor != "CEO" and (candidate["scopeType"] == "COMPANY_CANDIDATE" or protected_use):
                raise AutonomousControlError("Learning promotion requires CEO authority")
            unresolved_conflicts = set(candidate.get("conflictsWithRefs") or []) - set(candidate.get("supersedesRefs") or [])
            if unresolved_conflicts:
                raise AutonomousControlError("Conflicting Learning requires explicit supersede authority")
            if actor == "LEADER":
                self._leader_assignment(connection, series["company_id"], series["workspace_id"], series["owner_ref"])
            accepted_id = _stable_id("accepted-learning", self.tenant_id, candidate_ref)
            existing = connection.execute(
                "select * from artifacts where tenant_id=? and artifact_id=?",
                (self.tenant_id, accepted_id),
            ).fetchone()
            if existing is not None:
                return self._learning_artifact(existing)
            accepted_at = _now()
            payload = {
                **candidate,
                "kind": "ACCEPTED_LEARNING",
                "candidateRef": candidate_ref,
                "candidateHash": candidate_row["content_sha256"],
                "acceptedBy": actor,
                "acceptedAt": accepted_at,
            }
            content = _json(payload)
            digest = hashlib.sha256(content.encode("utf-8")).hexdigest()
            connection.execute(
                "insert into artifacts(artifact_id, tenant_id, task_id, title, artifact_type, status, content, source_ref, content_sha256) "
                "values (?, ?, ?, ?, 'accepted_learning', 'accepted', ?, ?, ?)",
                (
                    accepted_id,
                    self.tenant_id,
                    candidate_row["task_id"],
                    candidate_row["title"],
                    content,
                    f"autonomous.learning.accepted:{candidate_ref}",
                    digest,
                ),
            )
            supersedes = set(candidate.get("supersedesRefs") or [])
            if supersedes:
                connection.executemany(
                    "update artifacts set status='archived', updated_at=? where tenant_id=? and artifact_id=? and status='accepted'",
                    [(accepted_at, self.tenant_id, ref) for ref in supersedes],
                )
            series_data = dict(series["data"])
            active = [ref for ref in series_data.get("acceptedLearningRefs") or [] if ref not in supersedes]
            series_data["acceptedLearningRefs"] = list(dict.fromkeys([*active, accepted_id]))
            series_data["learningAcceptanceHistory"] = [
                *(series_data.get("learningAcceptanceHistory") or []),
                {
                    "acceptedLearningRef": accepted_id,
                    "candidateRef": candidate_ref,
                    "acceptedBy": actor,
                    "acceptedAt": accepted_at,
                    "supersedesRefs": list(supersedes),
                },
            ]
            latest_cycle_ref = candidate["provenance"]["cycleRefs"][-1]
            latest_cycle = self._entity(self._row(connection, latest_cycle_ref, entity_type="CYCLE"))
            cycle_data = dict(latest_cycle["data"])
            cycle_data["acceptedLearningRefs"] = list(dict.fromkeys([
                *(cycle_data.get("acceptedLearningRefs") or []), accepted_id,
            ]))
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(series_data), accepted_at, self.tenant_id, series["entity_id"]),
            )
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(cycle_data), accepted_at, self.tenant_id, latest_cycle_ref),
            )
            row = connection.execute(
                "select * from artifacts where tenant_id=? and artifact_id=?",
                (self.tenant_id, accepted_id),
            ).fetchone()
        return self._learning_artifact(row)

    def resolve_learning_context(self, series_id: str) -> list[dict[str, Any]]:
        """Return active reference-first Learning that applies to this Series only."""
        with self.db.connect() as connection:
            series = self._entity(self._row(connection, series_id, entity_type="OPERATING_SERIES"))
            _, _, blueprint = self._workspace_truth(connection, series["company_id"], series["workspace_id"])
            domain = str(blueprint.get("businessType") or "GENERIC").upper()
            resolved = []
            rows = connection.execute(
                "select * from artifacts where tenant_id=? and artifact_type='accepted_learning' and status='accepted' "
                "order by created_at, artifact_id",
                (self.tenant_id,),
            ).fetchall()
            for row in rows:
                data = json.loads(row["content"])
                if data.get("companyRef") != series["company_id"]:
                    continue
                applicable = (
                    (data["scopeType"] == "WORKSPACE" and data["scopeRef"] == series["workspace_id"])
                    or (data["scopeType"] == "DOMAIN" and data["scopeRef"] == domain)
                    or (
                        data["scopeType"] == "COMPANY_CANDIDATE"
                        and data["scopeRef"] == series["company_id"]
                        and data["acceptedBy"] == "CEO"
                    )
                )
                if applicable:
                    resolved.append({
                        "acceptedLearningRef": row["artifact_id"],
                        "claim": data["claim"],
                        "scopeType": data["scopeType"],
                        "scopeRef": data["scopeRef"],
                        "confidence": data["confidence"],
                        "conditions": data["conditions"],
                        "limitations": data["limitations"],
                        "proposedUse": data["proposedUse"],
                        "provenance": data["provenance"],
                        "acceptedBy": data["acceptedBy"],
                        "acceptedAt": data["acceptedAt"],
                    })
            return resolved

    def invalidate_learning(
        self,
        accepted_ref: str,
        *,
        actor: str,
        reason: str,
        evidence_refs: list[str],
    ) -> dict[str, Any]:
        """Archive one accepted Learning without deleting its provenance."""
        actor = actor.upper()
        if actor not in {"LEADER", "CEO"} or not reason.strip() or not evidence_refs:
            raise AutonomousControlError("Learning invalidation requires authority, reason and Evidence")
        with self.db.connect() as connection:
            connection.execute("begin immediate")
            row = connection.execute(
                "select * from artifacts where tenant_id=? and artifact_id=? and artifact_type='accepted_learning'",
                (self.tenant_id, accepted_ref),
            ).fetchone()
            if row is None:
                raise KeyError(accepted_ref)
            data = json.loads(row["content"])
            series = self._entity(self._row(connection, data["seriesRef"], entity_type="OPERATING_SERIES"))
            if actor != "CEO" and data["scopeType"] == "COMPANY_CANDIDATE":
                raise AutonomousControlError("Company Learning invalidation requires CEO authority")
            if actor == "LEADER":
                self._leader_assignment(connection, series["company_id"], series["workspace_id"], series["owner_ref"])
            allowed_cycles = set(data["provenance"]["cycleRefs"])
            for evidence_ref in evidence_refs:
                evidence = self._row(connection, evidence_ref, entity_type="EVIDENCE")
                if evidence["parent_id"] not in allowed_cycles or evidence["verification_status"] != "VERIFIED":
                    raise AutonomousControlError("Learning invalidation Evidence is not canonical source truth")
            invalidation = {
                "acceptedLearningRef": accepted_ref,
                "actor": actor,
                "reason": reason.strip(),
                "evidenceRefs": list(dict.fromkeys(evidence_refs)),
            }
            series_data = dict(series["data"])
            history = list(series_data.get("learningInvalidations") or [])
            existing = next((item for item in history if _hash({k: item[k] for k in invalidation}) == _hash(invalidation)), None)
            if existing:
                return {"learning": self._learning_artifact(row), "invalidation": existing}
            invalidation["invalidatedAt"] = _now()
            series_data["acceptedLearningRefs"] = [
                ref for ref in series_data.get("acceptedLearningRefs") or [] if ref != accepted_ref
            ]
            series_data["learningInvalidations"] = [*history, invalidation]
            connection.execute(
                "update artifacts set status='archived', updated_at=? where tenant_id=? and artifact_id=?",
                (invalidation["invalidatedAt"], self.tenant_id, accepted_ref),
            )
            connection.execute(
                "update runtime_entities set data_json=?, updated_at=? where tenant_id=? and entity_id=?",
                (_json(series_data), invalidation["invalidatedAt"], self.tenant_id, series["entity_id"]),
            )
            archived = connection.execute(
                "select * from artifacts where tenant_id=? and artifact_id=?",
                (self.tenant_id, accepted_ref),
            ).fetchone()
        return {"learning": self._learning_artifact(archived), "invalidation": invalidation}
