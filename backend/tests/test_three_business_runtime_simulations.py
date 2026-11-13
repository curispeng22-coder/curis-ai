from __future__ import annotations

import tempfile
import unittest

from app.database import Database
from app.runtime import RuntimeFoundation, RuntimeScopeError, SimulationRuntime
from app.runtime.state_machine import ActorNotAllowedError
from app.tenant_context import TenantContext


TENANT = "tenant-three-business"
COMPANY = "company-three-business"
CEO = "ceo-three-business"
NOW = "2026-08-09T12:00:00+00:00"


class ThreeBusinessRuntimeSimulationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".sqlite")
        self.db = Database(self.tmp.name)
        self.db.initialize()
        with self.db.connect() as conn:
            conn.execute(
                "insert into companies(company_id, tenant_id, ceo_id, name) values (?, ?, ?, 'Three Business Co')",
                (COMPANY, TENANT, CEO),
            )
            for workspace_id, business_id in (
                ("workspace-rd", "business-rd"),
                ("workspace-xhs", "business-xhs"),
                ("workspace-ttk", "business-ttk"),
            ):
                conn.execute(
                    """
                    insert into workspaces(
                      workspace_id, tenant_id, business_id, company_id, name,
                      status, blueprint_version, simulation_passed
                    ) values (?, ?, ?, ?, ?, 'DRAFT', 'v1', 0)
                    """,
                    (workspace_id, TENANT, business_id, COMPANY, workspace_id),
                )
        with TenantContext.scope(TENANT):
            foundation = RuntimeFoundation(self.db)
            assistant = foundation.create(
                "CEO_ASSISTANT", company_id=COMPANY, owner_ref=CEO, org_version="org-v1",
                data={"contextVersion": "context-v1", "contractVersion": "contract-v1"},
            )
            employee = foundation.create(
                "AI_EMPLOYEE", company_id=COMPANY, owner_ref=assistant["entity_id"],
                org_version="org-v1", presence_state="AVAILABLE",
            )
            role = foundation.create("ROLE_SLOT", company_id=COMPANY, org_version="org-v1")
            binding = foundation.create(
                "CAPABILITY_BINDING", company_id=COMPANY, org_version="org-v1",
                capability_ref="capability.three-business",
            )
            foundation.link(assistant["entity_id"], "SUPERVISES_ROLE", role["entity_id"])
            foundation.link(role["entity_id"], "ASSIGNED_EMPLOYEE", employee["entity_id"])
            foundation.link(role["entity_id"], "AUTHORIZED_CAPABILITY", binding["entity_id"])
            self.participants = [assistant["entity_id"], employee["entity_id"], role["entity_id"]]

    def _runtime(self):
        return RuntimeFoundation(self.db), SimulationRuntime(self.db)

    @staticmethod
    def _handoff(handoff_id: str, output_ref: str) -> dict:
        return {
            "handoffId": handoff_id,
            "fromRole": "CEO_ASSISTANT",
            "toRole": "PROFESSIONAL_AI",
            "at": NOW,
            "inputRefs": ["ceo-intent"],
            "outputRefs": [output_ref],
            "acknowledgement": "ACCEPTED",
            "nextCheckAt": NOW,
        }

    @staticmethod
    def _decision(decision_id: str, choice: str, entity_id: str) -> dict:
        return {
            "decisionId": decision_id,
            "entityType": "SIMULATION",
            "entityId": entity_id,
            "choice": choice,
            "actor": "CEO",
            "at": NOW,
            "reason": f"CEO {choice}",
            "evidenceRefs": [],
            "resultingState": "RUNNING" if choice != "REJECT" else "REVISION_REQUIRED",
        }

    @staticmethod
    def _platform_receipt(receipt_id: str, platform: str) -> dict:
        return {
            "receiptId": receipt_id,
            "source": "PLATFORM_API",
            "platform": platform,
            "externalId": f"external-{receipt_id}",
            "status": "SUCCESS",
            "receivedAt": NOW,
            "verificationStatus": "VERIFIED",
        }

    def _verified_evidence(self, foundation, workspace_id: str, kind: str) -> dict:
        return foundation.create(
            "EVIDENCE", company_id=COMPANY, workspace_id=workspace_id,
            verification_status="VERIFIED", evidence_condition="CURRENT",
            data={
                "fixture": False,
                "kind": kind,
                "source": "CEO_ACCEPTANCE" if workspace_id == "workspace-rd" else "PLATFORM_API",
                "recordedAt": NOW,
                "responsibleActor": CEO,
            },
        )

    def _create_run(self, simulation, scenario_id: str, workspace_id: str) -> dict:
        return simulation.create(
            company_id=COMPANY,
            ceo_id=CEO,
            scenario_id=scenario_id,
            blueprint_version="v1",
            workspace_id=workspace_id,
            participants=self.participants,
            input_refs=[f"input-{scenario_id.lower()}"],
        )

    def test_rd_001_waits_for_ceo_acceptance_and_creates_next_cycle(self):
        with TenantContext.scope(TENANT):
            foundation, simulation = self._runtime()
            run = self._create_run(simulation, "RD-001", "workspace-rd")
            run_id = run["simulation_run_id"]
            simulation.transition(run_id, "RUNNING", actor="SYSTEM", trigger="start_rd")
            simulation.transition(run_id, "WAITING_CEO", actor="SYSTEM", trigger="scope_gate")
            with self.assertRaises(ActorNotAllowedError):
                simulation.transition(run_id, "RUNNING", actor="SYSTEM", trigger="auto_resume")
            simulation.append(run_id, "ceo_decisions", self._decision("decision-rd-scope", "CLARIFY", run_id))
            simulation.transition(run_id, "RUNNING", actor="CEO", trigger="resume_with_scope")

            cycle = foundation.create("CYCLE", company_id=COMPANY, workspace_id="workspace-rd", owner_ref=CEO)
            cycle = foundation.transition(cycle["entity_id"], "READY", actor="CEO", trigger="approve_scope")
            cycle = foundation.transition(cycle["entity_id"], "RUNNING", actor="CEO", trigger="start_cycle")
            cycle = foundation.transition(cycle["entity_id"], "WAITING_CEO", actor="SYSTEM", trigger="request_acceptance")
            acceptance = foundation.create(
                "ACCEPTANCE", company_id=COMPANY, workspace_id="workspace-rd",
                parent_id=cycle["entity_id"], owner_ref=CEO,
            )
            evidence_ids = []
            for kind in ("COMMIT", "BUILD", "TEST"):
                evidence = self._verified_evidence(foundation, "workspace-rd", kind)
                evidence_ids.append(evidence["entity_id"])
                foundation.link(cycle["entity_id"], "HAS_ENGINEERING_EVIDENCE", evidence["entity_id"])
                simulation.append(run_id, "evidence_refs", evidence["entity_id"])
            acceptance = foundation.transition(
                acceptance["entity_id"], "ACCEPTED", actor="CEO", trigger="accept_increment",
                evidence_refs=evidence_ids,
            )
            cycle = foundation.transition(
                cycle["entity_id"], "ACCEPTED", actor="CEO", trigger="accept_cycle",
                context={"acceptanceId": acceptance["entity_id"]}, evidence_refs=evidence_ids,
            )
            cycle = foundation.transition(cycle["entity_id"], "REVIEWING", actor="SYSTEM", trigger="review")
            cycle = foundation.transition(cycle["entity_id"], "CLOSED", actor="CEO", trigger="close_cycle")
            next_cycle = foundation.create("CYCLE", company_id=COMPANY, workspace_id="workspace-rd", owner_ref=CEO)
            foundation.link(cycle["entity_id"], "NEXT_CYCLE", next_cycle["entity_id"])

            simulation.append(run_id, "handoffs", self._handoff("handoff-rd", cycle["entity_id"]))
            simulation.append(run_id, "ceo_decisions", self._decision("decision-rd-accept", "ACCEPT", cycle["entity_id"]))
            simulation.set_final_state(run_id, "NEXT_CYCLE_PLANNED")
            run = simulation.review(run_id, reviewer="CEO", pass_status="PASS", notes="真实 commit/build/test 与 CEO 验收齐全")
            self.assertEqual((run["lifecycle_status"], run["pass_status"]), ("PASSED", "PASS"))
            self.assertEqual(foundation.related(cycle["entity_id"], "NEXT_CYCLE")[0]["entity"]["entity_id"], next_cycle["entity_id"])

    def test_xhs_001_preserves_ceo_rejection_and_requires_platform_receipt(self):
        with TenantContext.scope(TENANT):
            foundation, simulation = self._runtime()
            run = self._create_run(simulation, "XHS-001", "workspace-xhs")
            run_id = run["simulation_run_id"]
            simulation.transition(run_id, "RUNNING", actor="SYSTEM", trigger="start_xhs")

            version = foundation.create(
                "CONTENT_VERSION", company_id=COMPANY, workspace_id="workspace-xhs",
                data={"platformVariant": "XHS_CAROUSEL", "payloadRef": "artifact-xhs-v1"},
            )
            content = foundation.create(
                "CONTENT_ITEM", company_id=COMPANY, workspace_id="workspace-xhs",
                current_version_id=version["entity_id"], owner_ref="CONTENT_AI",
            )
            content = foundation.transition(content["entity_id"], "DRAFT", actor="SYSTEM", trigger="accept_idea")
            content = foundation.transition(content["entity_id"], "IN_REVIEW", actor="AI_EMPLOYEE", trigger="submit")
            content = foundation.transition(
                content["entity_id"], "DRAFT", actor="CEO", trigger="request_changes",
                reason="CEO 拒绝标题与表达",
            )
            simulation.append(run_id, "ceo_decisions", self._decision("decision-xhs-reject", "REJECT", content["entity_id"]))
            content = foundation.transition(content["entity_id"], "IN_REVIEW", actor="AI_EMPLOYEE", trigger="resubmit")
            foundation.set_version_refs(content["entity_id"], approved_version_id=version["entity_id"])
            content = foundation.transition(content["entity_id"], "APPROVED", actor="CEO", trigger="approve")
            foundation.set_version_refs(content["entity_id"], published_version_id=version["entity_id"])
            receipt = self._platform_receipt("receipt-xhs", "XHS")
            content = foundation.transition(content["entity_id"], "SCHEDULED", actor="SYSTEM", trigger="schedule")
            content = foundation.transition(
                content["entity_id"], "PUBLISHED", actor="EXTERNAL", trigger="publish",
                context={"externalReceipt": receipt["receiptId"]},
            )
            content = foundation.transition(content["entity_id"], "AWAITING_FEEDBACK", actor="SYSTEM", trigger="await_feedback")
            content = foundation.transition(content["entity_id"], "REVIEWED", actor="CEO", trigger="review_outcome")
            evidence = self._verified_evidence(foundation, "workspace-xhs", "PLATFORM_OUTCOME")

            simulation.append(run_id, "handoffs", self._handoff("handoff-xhs", content["entity_id"]))
            simulation.append(run_id, "receipts", receipt)
            simulation.append(run_id, "evidence_refs", evidence["entity_id"])
            simulation.append(run_id, "ceo_decisions", self._decision("decision-xhs-continue", "CONTINUE", content["entity_id"]))
            simulation.set_final_state(run_id, "CONTENT_REVIEWED")
            run = simulation.review(run_id, reviewer="CEO", pass_status="PASS")
            self.assertEqual(run["lifecycle_status"], "PASSED")
            history = foundation.history(content["entity_id"])
            self.assertTrue(any(item["source"] == "IN_REVIEW" and item["target"] == "DRAFT" for item in history))
            self.assertEqual(simulation.invalidate_workspace("workspace-xhs", blueprint_version="v2", change_kind="REPLY_POLICY"), 1)
            invalidated = simulation.get(run_id)
            self.assertEqual(invalidated["lifecycle_status"], "PASSED")
            self.assertEqual(invalidated["invalidation_reason"], "REPLY_POLICY")

    def test_ttk_001_manual_feedback_cannot_replace_verified_external_receipt_or_hide_failure(self):
        with TenantContext.scope(TENANT):
            foundation, simulation = self._runtime()
            run = self._create_run(simulation, "TTK-001", "workspace-ttk")
            run_id = run["simulation_run_id"]
            simulation.transition(run_id, "RUNNING", actor="SYSTEM", trigger="start_ttk")
            evidence = self._verified_evidence(foundation, "workspace-ttk", "VIDEO_ACCEPTANCE")
            simulation.append(run_id, "handoffs", self._handoff("handoff-ttk", evidence["entity_id"]))
            simulation.append(run_id, "evidence_refs", evidence["entity_id"])
            simulation.append(run_id, "ceo_decisions", self._decision("decision-ttk", "ACCEPT", run_id))
            simulation.set_final_state(run_id, "VIDEO_READY_FOR_REVIEW")

            manual = {
                "receiptId": "manual-ttk",
                "source": "CEO_MANUAL",
                "status": "RECEIVED",
                "receivedAt": NOW,
                "recordedBy": CEO,
                "verificationStatus": "UNVERIFIED",
            }
            simulation.append(run_id, "receipts", manual)
            with self.assertRaises(ValueError):
                simulation.review(run_id, reviewer="CEO", pass_status="PASS")
            with self.assertRaises(ValueError):
                simulation.append(run_id, "receipts", {**manual, "verificationStatus": "VERIFIED"})

            failure = {
                "failureId": "failure-ttk-processing",
                "entityType": "CONTENT_ITEM",
                "entityId": "video-ttk",
                "kind": "PLATFORM_PROCESSING_FAILED",
                "detectedAt": NOW,
                "detectedBy": "SYSTEM",
                "impact": "video not published",
                "recoveryCommand": "retry_after_fix",
                "resolvedAt": None,
                "evidenceRefs": [],
            }
            simulation.append(run_id, "failure_events", failure)
            simulation.append(run_id, "receipts", self._platform_receipt("receipt-ttk", "TTK"))
            with self.assertRaises(ValueError):
                simulation.review(run_id, reviewer="CEO", pass_status="PASS")
            simulation.resolve_failure(
                run_id, "failure-ttk-processing", resolved_at=NOW,
                evidence_refs=[evidence["entity_id"]],
            )
            simulation.set_final_state(run_id, "VIDEO_PUBLISHED_AND_REVIEWED")
            run = simulation.review(run_id, reviewer="CEO", pass_status="PASS")
            self.assertEqual(run["lifecycle_status"], "PASSED")
            self.assertEqual(run["receipts"][0]["verificationStatus"], "UNVERIFIED")
            self.assertEqual(run["failure_events"][0]["kind"], "PLATFORM_PROCESSING_FAILED")
            self.assertEqual(run["failure_events"][0]["resolvedAt"], NOW)

            failed = self._create_run(simulation, "TTK-001", "workspace-ttk")
            failed_id = failed["simulation_run_id"]
            simulation.transition(failed_id, "RUNNING", actor="SYSTEM", trigger="start_failure_path")
            failed = simulation.review(failed_id, reviewer="CEO", pass_status="FAIL", notes="平台处理失败")
            self.assertEqual((failed["lifecycle_status"], failed["pass_status"]), ("FAILED", "FAIL"))
            with self.assertRaises(ValueError):
                simulation.review(failed_id, reviewer="CEO", pass_status="PASS")

    def test_runs_are_queryable_after_restart_and_fail_closed_across_scope(self):
        with self.db.connect() as conn:
            conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-other', ?, ?, 'Other')", (TENANT, CEO))
            conn.execute("insert into workspaces(workspace_id, tenant_id, business_id, company_id, name, status, blueprint_version) values ('workspace-other', ?, 'business-other', 'company-other', 'Other', 'DRAFT', 'v1')", (TENANT,))
        ids = {}
        with TenantContext.scope(TENANT):
            _foundation, simulation = self._runtime()
            for scenario, workspace in (
                ("RD-001", "workspace-rd"),
                ("XHS-001", "workspace-xhs"),
                ("TTK-001", "workspace-ttk"),
            ):
                run = self._create_run(simulation, scenario, workspace)
                ids[scenario] = run["simulation_run_id"]
                self.assertEqual(simulation.list(company_id=COMPANY, workspace_id=workspace, scenario_id=scenario)[0]["simulation_run_id"], run["simulation_run_id"])
            with self.assertRaises(RuntimeScopeError):
                simulation.create(
                    company_id=COMPANY, ceo_id=CEO, scenario_id="RD-001",
                    blueprint_version="v1", workspace_id="workspace-other",
                )

            restarted = SimulationRuntime(Database(self.tmp.name))
            self.assertEqual({run["scenario_id"] for run in restarted.list(company_id=COMPANY)}, {"RD-001", "XHS-001", "TTK-001"})
            self.assertEqual(restarted.get(ids["RD-001"])["participants"], self.participants)
            rd_id = ids["RD-001"]
            restarted.transition(rd_id, "RUNNING", actor="SYSTEM", trigger="start_before_invalidation")
            evidence = self._verified_evidence(RuntimeFoundation(self.db), "workspace-rd", "TEST")
            restarted.append(rd_id, "handoffs", self._handoff("handoff-invalidated", evidence["entity_id"]))
            restarted.append(rd_id, "evidence_refs", evidence["entity_id"])
            restarted.append(rd_id, "ceo_decisions", self._decision("decision-invalidated", "ACCEPT", rd_id))
            restarted.set_final_state(rd_id, "READY")
            restarted.invalidate_workspace("workspace-rd", blueprint_version="v2", change_kind="CAPABILITY")
            with self.assertRaises(ValueError):
                restarted.review(rd_id, reviewer="CEO", pass_status="PASS")

        with TenantContext.scope("tenant-other"):
            restarted = SimulationRuntime(Database(self.tmp.name))
            self.assertEqual(restarted.list(company_id=COMPANY), [])
            with self.assertRaises(KeyError):
                restarted.get(ids["RD-001"])


if __name__ == "__main__":
    unittest.main()
