"""Persisted Runtime Foundation simulations."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from uuid import uuid4

from ..database import Database
from ..tenant_context import TenantContext
from .foundation import RuntimeFoundation
from .registry import get_registered_machine
from .states import SimulationPassStatus, normalize


SCENARIOS = frozenset({"FIRST-ARRIVAL-001", "ORG-001", "RD-001", "XHS-001", "TTK-001"})
INVALIDATING_CHANGES = frozenset({
    "BLUEPRINT", "STAGE", "AGENT", "ORGANIZATION", "CAPABILITY", "CONNECTOR",
    "PLATFORM_CONSTRAINT", "REPLY_POLICY", "EVIDENCE_RULE",
})
RECEIPT_SOURCES = frozenset({"PLATFORM_API", "CEO_MANUAL"})


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class SimulationRuntime:
    def __init__(self, database: Database):
        self.db = database
        self.foundation = RuntimeFoundation(database)

    @property
    def tenant_id(self) -> str:
        return TenantContext.current_tenant_id()

    def create(
        self,
        *,
        company_id: str,
        ceo_id: str,
        scenario_id: str,
        blueprint_version: str,
        workspace_id: str | None = None,
        subject_id: str | None = None,
        participants: list[str] | None = None,
        input_refs: list[str] | None = None,
    ) -> dict:
        if scenario_id not in SCENARIOS:
            raise ValueError(f"unsupported simulation scenario: {scenario_id}")
        self.foundation._require_company(company_id)
        if workspace_id:
            self.foundation._require_workspace(workspace_id, company_id)
            with self.db.connect() as conn:
                workspace = conn.execute(
                    "select blueprint_version, blueprint_json from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (self.tenant_id, company_id, workspace_id),
                ).fetchone()
            if workspace is None or workspace["blueprint_version"] != blueprint_version:
                raise ValueError("simulation blueprint is not current")
            business_type = json.loads(workspace["blueprint_json"]).get("businessType")
            expected_business = {"RD-001": "RD", "XHS-001": "XHS", "TTK-001": "TTK"}.get(scenario_id)
            if subject_id and expected_business and business_type != expected_business:
                raise ValueError("simulation scenario does not match workspace business_type")
        refs = list(input_refs or [])
        if subject_id:
            subject = self.foundation.get(subject_id)
            expected = "CYCLE" if scenario_id == "RD-001" else "CONTENT_ITEM" if scenario_id in {"XHS-001", "TTK-001"} else ""
            if (
                expected and subject["entity_type"] != expected
                or subject["company_id"] != company_id
                or subject["workspace_id"] != workspace_id
                or subject["blueprint_version"] != blueprint_version
                or scenario_id in {"XHS-001", "TTK-001"}
                and subject["data"].get("platform") != scenario_id.removesuffix("-001")
            ):
                raise ValueError("simulation subject does not match scenario or scope")
            refs = [f"subject:{subject_id}", *refs]
        run_id = f"simulation-{uuid4()}"
        at = _now()
        with self.db.connect() as conn:
            conn.execute(
                """
                insert into runtime_simulation_runs(
                  simulation_run_id, tenant_id, company_id, ceo_id, workspace_id,
                  blueprint_version, scenario_id, lifecycle_status, pass_status,
                  participants_json, input_refs_json, created_at, updated_at
                ) values (?, ?, ?, ?, ?, ?, ?, 'DRAFT', 'NOT_RUN', ?, ?, ?, ?)
                """,
                (run_id, self.tenant_id, company_id, ceo_id, workspace_id,
                 blueprint_version, scenario_id, json.dumps(participants or []),
                 json.dumps(list(dict.fromkeys(refs))), at, at),
            )
        return self.get(run_id)

    def create_staffing(
        self,
        *,
        company_id: str,
        ceo_id: str,
        workspace_id: str,
        blueprint_version: str,
    ) -> dict:
        self.foundation._require_workspace(workspace_id, company_id)
        with self.db.connect() as conn:
            workspace = conn.execute(
                "select blueprint_version, blueprint_json from workspaces "
                "where tenant_id = ? and company_id = ? and workspace_id = ?",
                (self.tenant_id, company_id, workspace_id),
            ).fetchone()
        if workspace is None or workspace["blueprint_version"] != blueprint_version:
            raise ValueError("staffing simulation blueprint is not current")
        blueprint = json.loads(workspace["blueprint_json"])
        if blueprint.get("lifecycleMode") != "STUDIO_DRAFT":
            raise ValueError("staffing simulation requires a Studio Draft")
        entities = [
            *self.foundation.list("ROLE_SLOT", company_id=company_id, workspace_id=workspace_id),
            *self.foundation.list("AI_EMPLOYEE", company_id=company_id, workspace_id=workspace_id),
            *self.foundation.list("CAPABILITY_BINDING", company_id=company_id, workspace_id=workspace_id),
        ]
        org_versions = {item["org_version"] for item in entities if item["org_version"]}
        if not entities or len(org_versions) != 1 or any(item["blueprint_version"] != blueprint_version for item in entities):
            raise ValueError("staffing proposal is incomplete or version-mismatched")
        org_version = next(iter(org_versions))
        for current in reversed(self.list(company_id=company_id, workspace_id=workspace_id, scenario_id="ORG-001")):
            if (
                current["blueprint_version"] == blueprint_version
                and f"org-version:{org_version}" in current["input_refs"]
                and not current["invalidated_at"]
                and current["lifecycle_status"] in {"DRAFT", "RUNNING", "WAITING_CEO", "PASSED"}
            ):
                return current
        return self.create(
            company_id=company_id,
            ceo_id=ceo_id,
            scenario_id="ORG-001",
            blueprint_version=blueprint_version,
            workspace_id=workspace_id,
            participants=[item["entity_id"] for item in entities],
            input_refs=[f"org-version:{org_version}", "scope:staffing-proposal"],
        )

    def get(self, run_id: str) -> dict:
        with self.db.connect() as conn:
            row = conn.execute(
                "select * from runtime_simulation_runs where tenant_id = ? and simulation_run_id = ?",
                (self.tenant_id, run_id),
            ).fetchone()
        if row is None:
            raise KeyError(run_id)
        result = dict(row)
        for field in (
            "participants_json", "input_refs_json", "state_transitions_json", "handoffs_json", "receipts_json",
            "evidence_refs_json", "failure_events_json", "ceo_decisions_json",
        ):
            result[field.removesuffix("_json")] = json.loads(result.pop(field))
        result["subject_id"] = next(
            (item.removeprefix("subject:") for item in result["input_refs"] if item.startswith("subject:")),
            None,
        )
        return result

    def list(
        self,
        *,
        company_id: str,
        workspace_id: str | None = None,
        scenario_id: str | None = None,
    ) -> list[dict]:
        clauses = ["tenant_id = ?", "company_id = ?"]
        params: list[object] = [self.tenant_id, company_id]
        if workspace_id is not None:
            clauses.append("workspace_id = ?")
            params.append(workspace_id)
        if scenario_id is not None:
            clauses.append("scenario_id = ?")
            params.append(scenario_id)
        with self.db.connect() as conn:
            ids = [row[0] for row in conn.execute(
                f"select simulation_run_id from runtime_simulation_runs where {' and '.join(clauses)} order by created_at, simulation_run_id",
                params,
            )]
        return [self.get(run_id) for run_id in ids]

    def transition(
        self,
        run_id: str,
        target: str,
        *,
        actor: str,
        trigger: str,
        reason: str = "",
        pass_status: str | None = None,
    ) -> dict:
        current = self.get(run_id)
        if pass_status and target not in {"REVIEWED", "PASSED", "FAILED"}:
            raise ValueError("pass_status changes only during review")
        normalized_pass = normalize(SimulationPassStatus, pass_status).value if pass_status else current["pass_status"]
        if target == "RUNNING" and current["lifecycle_status"] == "DRAFT":
            normalized_pass = "IN_PROGRESS"
        elif target == "FAILED":
            normalized_pass = "FAIL"
        record = get_registered_machine("simulation_run").transition(
            run_id, current["lifecycle_status"], target, actor=actor, trigger=trigger,
            reason=reason, context={"passStatus": normalized_pass}, record=False,
        )
        finished_at = record.at if record.target in {"PASSED", "FAILED", "CANCELLED"} else current["finished_at"]
        started_at = record.at if record.target == "RUNNING" and not current["started_at"] else current["started_at"]
        transitions = [*current["state_transitions"], record.as_dict()]
        with self.db.connect() as conn:
            cursor = conn.execute(
                "update runtime_simulation_runs set lifecycle_status = ?, pass_status = ?, state_transitions_json = ?, started_at = ?, finished_at = ?, updated_at = ? where tenant_id = ? and simulation_run_id = ? and lifecycle_status = ?",
                (record.target, normalized_pass, json.dumps(transitions, ensure_ascii=False), started_at,
                 finished_at, record.at, self.tenant_id, run_id, current["lifecycle_status"]),
            )
            if cursor.rowcount != 1:
                raise RuntimeError("simulation changed concurrently; retry from current state")
            conn.execute(
                """
                insert into runtime_transition_log(
                  tenant_id, entity_type, entity_id, source, target, trigger, actor,
                  at, reason, company_id, workspace_id, context_json
                ) values (?, 'simulation_run', ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (self.tenant_id, run_id, record.source, record.target, record.trigger,
                 record.actor, record.at, reason, current["company_id"], current["workspace_id"],
                 json.dumps(record.context)),
            )
        return self.get(run_id)

    def review(self, run_id: str, *, reviewer: str, pass_status: str, notes: str = "") -> dict:
        value = normalize(SimulationPassStatus, pass_status).value
        if value not in {"PASS", "FAIL", "REVIEW_REQUIRED"}:
            raise ValueError("review pass_status must be PASS, FAIL or REVIEW_REQUIRED")
        current = self.get(run_id)
        if value == "PASS":
            self._validate_pass(current)
        if current["lifecycle_status"] == "WAITING_CEO":
            current = self.transition(run_id, "RUNNING", actor="CEO", trigger="resume", reason="CEO opened review")
        if current["lifecycle_status"] != "RUNNING":
            raise ValueError("simulation must be RUNNING before review")
        at = _now()
        with self.db.connect() as conn:
            conn.execute(
                "update runtime_simulation_runs set reviewer = ?, review_notes = ?, reviewed_at = ?, updated_at = ? where tenant_id = ? and simulation_run_id = ?",
                (reviewer, notes, at, at, self.tenant_id, run_id),
            )
        reviewed = self.transition(
            run_id, "REVIEWED", actor="CEO" if reviewer == "CEO" else "SYSTEM",
            trigger="review", pass_status=value,
        )
        if value == "REVIEW_REQUIRED":
            return reviewed
        result = self.transition(
            run_id, "PASSED" if value == "PASS" else "FAILED",
            actor="CEO", trigger="pass" if value == "PASS" else "fail", pass_status=value,
        )
        if value == "PASS" and result["scenario_id"] != "ORG-001":
            self._mark_workspace_simulated(result)
        return result

    def execute_staffing(self, run_id: str) -> dict:
        run = self.get(run_id)
        if run["scenario_id"] != "ORG-001" or not run["workspace_id"] or run["subject_id"]:
            raise ValueError("staffing execution requires a scoped ORG-001 simulation")
        if run["lifecycle_status"] == "WAITING_CEO":
            return run
        if run["lifecycle_status"] != "RUNNING" or run["invalidated_at"]:
            raise ValueError("staffing simulation must be current and RUNNING")
        org_refs = [item.removeprefix("org-version:") for item in run["input_refs"] if item.startswith("org-version:")]
        if len(org_refs) != 1:
            raise ValueError("staffing simulation requires one orgVersion")
        org_version = org_refs[0]
        with self.db.connect() as conn:
            workspace = conn.execute(
                "select blueprint_version, blueprint_json from workspaces "
                "where tenant_id = ? and company_id = ? and workspace_id = ?",
                (self.tenant_id, run["company_id"], run["workspace_id"]),
            ).fetchone()
        if workspace is None:
            raise KeyError(run["workspace_id"])
        blueprint = json.loads(workspace["blueprint_json"])
        roles = self.foundation.list("ROLE_SLOT", company_id=run["company_id"], workspace_id=run["workspace_id"])
        employees = self.foundation.list("AI_EMPLOYEE", company_id=run["company_id"], workspace_id=run["workspace_id"])
        bindings = self.foundation.list("CAPABILITY_BINDING", company_id=run["company_id"], workspace_id=run["workspace_id"])
        assistants = self.foundation.list("CEO_ASSISTANT", company_id=run["company_id"])
        assistant_id = assistants[0]["entity_id"] if len(assistants) == 1 else ""
        expected_roles = {item.get("role") for item in blueprint.get("roleSlots") or [] if item.get("role")}
        expected_capabilities = {
            item.get("capabilityRef") for item in blueprint.get("capabilityBindings") or [] if item.get("capabilityRef")
        }
        role_names = {item["data"].get("name") for item in roles}
        capability_refs = {item["data"].get("requirementRef") for item in bindings}
        role_ids = {item["entity_id"] for item in roles}
        proposed_for = {
            item["data"].get("roleSlotRef")
            for item in employees
            if any(
                link["relation"] == "PROPOSED_FOR" and link["target_id"] == item["data"].get("roleSlotRef")
                for link in self.foundation.related(item["entity_id"])
            )
        }
        reporting = all(
            assistant_id and any(
                link["relation"] == "REPORTS_TO" and link["target_id"] == assistant_id
                for link in self.foundation.related(item["entity_id"])
            )
            for item in [*roles, *employees]
        )
        capability_links = {
            (role["entity_id"], link["target_id"])
            for role in roles
            for link in self.foundation.related(role["entity_id"], "REQUIRES_CAPABILITY")
        }
        expected_links = {
            (role["entity_id"], binding["entity_id"])
            for role in roles
            for requirement in role["data"].get("capabilityRefs") or []
            for binding in bindings
            if binding["data"].get("requirementRef") == requirement
        }
        checks = {
            "blueprintCurrent": workspace["blueprint_version"] == run["blueprint_version"],
            "orgVersionCurrent": bool(roles and employees and bindings) and all(
                item["org_version"] == org_version and item["blueprint_version"] == run["blueprint_version"]
                for item in [*roles, *employees, *bindings]
            ),
            "roleCoverage": role_names == expected_roles and len(employees) == len(roles),
            "candidateCoverage": proposed_for == role_ids,
            "capabilityCoverage": capability_refs == expected_capabilities and expected_links == capability_links,
            "reportingChain": reporting,
            "manualFallback": bool((blueprint.get("failurePolicy") or {}).get("manualFallback")),
            "isolatedDraft": all(item["lifecycle_status"] == "DRAFT" for item in roles)
            and all(item["lifecycle_status"] == "PROPOSED" for item in employees)
            and all(
                item["lifecycle_status"] == "PROPOSED"
                and item["data"].get("authorizationStatus") == "PROPOSED_NOT_AUTHORIZED"
                for item in bindings
            ),
            "participantScope": set(run["participants"]) == {item["entity_id"] for item in [*roles, *employees, *bindings]},
        }
        if all(checks.values()):
            evidence = None
            for evidence_id in run["evidence_refs"]:
                candidate = self.foundation.get(evidence_id)
                if candidate["data"].get("kind") == "STAFFING_PROPOSAL_VALIDATION":
                    evidence = candidate
                    break
            if evidence is None:
                evidence = self.foundation.create(
                    "EVIDENCE",
                    company_id=run["company_id"],
                    workspace_id=run["workspace_id"],
                    parent_id=run_id,
                    blueprint_version=run["blueprint_version"],
                    verification_status="VERIFIED",
                    evidence_condition="CURRENT",
                    data={
                        "fixture": False,
                        "kind": "STAFFING_PROPOSAL_VALIDATION",
                        "orgVersion": org_version,
                        "checks": checks,
                    },
                )
                self.append(run_id, "evidence_refs", evidence["entity_id"])
                self.append(run_id, "handoffs", {
                    "from": "SYSTEM",
                    "to": "CEO",
                    "status": "READY_FOR_REVIEW",
                    "orgVersion": org_version,
                    "evidenceRefs": [evidence["entity_id"]],
                })
            self.set_final_state(run_id, "STAFFING_PROPOSAL_VALIDATED")
        else:
            if not run["failure_events"]:
                failed = sorted(key for key, passed in checks.items() if not passed)
                self.append(run_id, "failure_events", {
                    "failureId": f"staffing-contract:{org_version}",
                    "kind": "STAFFING_PROPOSAL_CONTRACT",
                    "blockedBy": failed,
                    "owner": "CEO Assistant",
                    "recoveryPath": (blueprint.get("failurePolicy") or {}).get("manualFallback") or "RETURN_TO_STUDIO",
                })
                self.append(run_id, "handoffs", {
                    "from": "SYSTEM",
                    "to": "CEO",
                    "status": "BLOCKED",
                    "orgVersion": org_version,
                    "failedChecks": failed,
                })
            self.set_final_state(run_id, "BLOCKED")
        return self.transition(
            run_id,
            "WAITING_CEO",
            actor="SYSTEM",
            trigger="wait_for_ceo",
            reason="staffing proposal isolated validation completed",
        )

    def append(self, run_id: str, field: str, value: dict | str) -> dict:
        columns = {
            "handoffs": "handoffs_json", "receipts": "receipts_json",
            "evidence_refs": "evidence_refs_json", "failure_events": "failure_events_json",
            "ceo_decisions": "ceo_decisions_json",
        }
        column = columns.get(field)
        if column is None:
            raise ValueError(f"unsupported simulation collection: {field}")
        if field == "receipts":
            value = self._validate_receipt(value)
        current = self.get(run_id)
        items = [*current[field], value]
        with self.db.connect() as conn:
            conn.execute(
                f"update runtime_simulation_runs set {column} = ?, updated_at = ? where tenant_id = ? and simulation_run_id = ?",
                (json.dumps(items, ensure_ascii=False), _now(), self.tenant_id, run_id),
            )
        return self.get(run_id)

    def resolve_failure(
        self,
        run_id: str,
        failure_id: str,
        *,
        resolved_at: str,
        evidence_refs: list[str] | None = None,
    ) -> dict:
        current = self.get(run_id)
        failures = list(current["failure_events"])
        for index, event in enumerate(failures):
            if isinstance(event, dict) and event.get("failureId") == failure_id:
                failures[index] = {
                    **event,
                    "resolvedAt": resolved_at,
                    "evidenceRefs": list(evidence_refs or event.get("evidenceRefs") or []),
                }
                break
        else:
            raise KeyError(failure_id)
        with self.db.connect() as conn:
            conn.execute(
                "update runtime_simulation_runs set failure_events_json = ?, updated_at = ? where tenant_id = ? and simulation_run_id = ?",
                (json.dumps(failures, ensure_ascii=False), _now(), self.tenant_id, run_id),
            )
        return self.get(run_id)

    def set_final_state(self, run_id: str, final_state: str) -> dict:
        self.get(run_id)
        with self.db.connect() as conn:
            conn.execute(
                "update runtime_simulation_runs set final_state = ?, updated_at = ? where tenant_id = ? and simulation_run_id = ?",
                (final_state, _now(), self.tenant_id, run_id),
            )
        return self.get(run_id)

    def create_fixture_evidence(self, run_id: str, *, label: str) -> dict:
        run = self.get(run_id)
        evidence = self.foundation.create(
            "EVIDENCE", company_id=run["company_id"], workspace_id=run["workspace_id"],
            parent_id=run_id, verification_status="UNVERIFIED", evidence_condition="CURRENT",
            data={"fixture": True, "label": label, "scenarioId": run["scenario_id"]},
        )
        self.append(run_id, "evidence_refs", evidence["entity_id"])
        return evidence

    def invalidate_workspace(
        self,
        workspace_id: str,
        *,
        blueprint_version: str,
        change_kind: str,
        blueprint: dict | None = None,
        change_reason: str = "",
    ) -> int:
        kind = change_kind.upper()
        if kind not in INVALIDATING_CHANGES:
            raise ValueError(f"change does not invalidate simulations: {change_kind}")
        self.foundation._require_workspace(workspace_id, None)
        at = _now()
        with self.db.connect() as conn:
            workspace = conn.execute(
                "select company_id from workspaces where tenant_id = ? and workspace_id = ?",
                (self.tenant_id, workspace_id),
            ).fetchone()
            cursor = conn.execute(
                """
                update runtime_simulation_runs
                   set invalidated_at = ?, invalidation_reason = ?, updated_at = ?
                 where tenant_id = ? and workspace_id = ? and invalidated_at is null
                """,
                (at, kind, at, self.tenant_id, workspace_id),
            )
            if blueprint is None:
                conn.execute(
                    "update workspaces set blueprint_version = ?, simulation_passed = 0, updated_at = ? where tenant_id = ? and workspace_id = ?",
                    (blueprint_version, at, self.tenant_id, workspace_id),
                )
            else:
                conn.execute(
                    "update workspaces set blueprint_json = ?, blueprint_version = ?, simulation_passed = 0, updated_at = ? where tenant_id = ? and workspace_id = ?",
                    (json.dumps(blueprint, ensure_ascii=False), blueprint_version, at, self.tenant_id, workspace_id),
                )
            conn.execute(
                """
                insert into runtime_workspace_versions(
                  version_id, tenant_id, company_id, workspace_id, blueprint_version,
                  status, simulation_passed, change_kind, data_json, created_at, updated_at
                ) values (?, ?, ?, ?, ?, 'DRAFT', 0, ?, ?, ?, ?)
                on conflict(tenant_id, workspace_id, blueprint_version) do update set
                  simulation_passed = 0, change_kind = excluded.change_kind,
                  data_json = excluded.data_json, updated_at = excluded.updated_at
                """,
                (f"workspace-version-{uuid4()}", self.tenant_id, workspace["company_id"],
                 workspace_id, blueprint_version, kind,
                 json.dumps({"blueprint": blueprint or {}, "changeReason": change_reason}, ensure_ascii=False),
                 at, at),
            )
        return cursor.rowcount

    def _validate_pass(self, run: dict) -> None:
        if run["invalidated_at"]:
            raise ValueError("invalidated simulation cannot PASS")
        if run["workspace_id"]:
            with self.db.connect() as conn:
                current = conn.execute(
                    "select blueprint_version from workspaces where tenant_id = ? and company_id = ? and workspace_id = ?",
                    (self.tenant_id, run["company_id"], run["workspace_id"]),
                ).fetchone()
            if current is None or current["blueprint_version"] != run["blueprint_version"]:
                raise ValueError("simulation blueprint is no longer current")
        if not run["handoffs"] or not run["ceo_decisions"] or not run["final_state"]:
            raise ValueError("PASS requires handoff, CEO decision and final state")
        if run["scenario_id"] in {"XHS-001", "TTK-001"}:
            platform_receipts = [
                receipt for receipt in run["receipts"]
                if isinstance(receipt, dict)
                and receipt.get("source") == "PLATFORM_API"
                and receipt.get("verificationStatus") == "VERIFIED"
                and receipt.get("status") == "SUCCESS"
            ]
            if not platform_receipts:
                raise ValueError("content platform PASS requires a VERIFIED external receipt")
        verified = 0
        for evidence_id in run["evidence_refs"]:
            try:
                evidence = self.foundation.get(evidence_id)
            except KeyError:
                continue
            if evidence["verification_status"] == "VERIFIED" and not evidence["data"].get("fixture"):
                verified += 1
        if not verified:
            raise ValueError("PASS requires non-fixture VERIFIED evidence")
        unresolved = [event for event in run["failure_events"] if not isinstance(event, dict) or not event.get("resolvedAt")]
        if unresolved:
            raise ValueError("PASS requires every failure event to be resolved")

    @staticmethod
    def _validate_receipt(value: dict | str) -> dict:
        if not isinstance(value, dict):
            raise ValueError("receipt must be a structured object")
        source = str(value.get("source") or "").upper()
        if source not in RECEIPT_SOURCES:
            raise ValueError("receipt source must be PLATFORM_API or CEO_MANUAL")
        receipt = {**value, "source": source}
        required = {"receiptId", "status", "receivedAt", "verificationStatus"}
        missing = sorted(required - {key for key, item in receipt.items() if item not in (None, "")})
        if missing:
            raise ValueError(f"receipt missing fields: {', '.join(missing)}")
        if source == "CEO_MANUAL":
            if receipt["verificationStatus"] != "UNVERIFIED" or not receipt.get("recordedBy"):
                raise ValueError("CEO_MANUAL feedback must be UNVERIFIED and name recordedBy")
        elif receipt["verificationStatus"] != "VERIFIED" or not receipt.get("externalId"):
            raise ValueError("PLATFORM_API receipt must be VERIFIED and include externalId")
        return receipt

    def _mark_workspace_simulated(self, run: dict) -> None:
        if not run["workspace_id"]:
            return
        at = _now()
        with self.db.connect() as conn:
            workspace = conn.execute(
                "select company_id from workspaces where tenant_id = ? and workspace_id = ? and blueprint_version = ?",
                (self.tenant_id, run["workspace_id"], run["blueprint_version"]),
            ).fetchone()
            if workspace is None:
                return
            conn.execute(
                "update workspaces set simulation_passed = 1, updated_at = ? where tenant_id = ? and workspace_id = ? and blueprint_version = ?",
                (at, self.tenant_id, run["workspace_id"], run["blueprint_version"]),
            )
            conn.execute(
                """
                insert into runtime_workspace_versions(
                  version_id, tenant_id, company_id, workspace_id, blueprint_version,
                  status, simulation_passed, created_at, updated_at
                ) values (?, ?, ?, ?, ?, 'SIMULATED', 1, ?, ?)
                on conflict(tenant_id, workspace_id, blueprint_version) do update set
                  status = 'SIMULATED', simulation_passed = 1, updated_at = excluded.updated_at
                """,
                (f"workspace-version-{uuid4()}", self.tenant_id, workspace["company_id"],
                 run["workspace_id"], run["blueprint_version"], at, at),
            )
