from __future__ import annotations

import tempfile
import unittest

from app.database import Database
from app.runtime import SimulationRuntime
from app.runtime.state_machine import ActorNotAllowedError
from app.tenant_context import TenantContext


class RuntimeFoundationSimulationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".sqlite")
        self.db = Database(self.tmp.name)
        self.db.initialize()
        with self.db.connect() as conn:
            conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-sim', 'tenant-sim', 'ceo', 'Sim')")
            conn.execute("insert into workspaces(workspace_id, tenant_id, business_id, company_id, name, status, blueprint_version, simulation_passed) values ('workspace-sim', 'tenant-sim', 'business', 'company-sim', 'WS', 'DRAFT', 'v1', 0)")

    def test_five_scenarios_fixture_evidence_and_pass_review(self):
        with TenantContext.scope("tenant-sim"):
            runtime = SimulationRuntime(self.db)
            run_ids = []
            for scenario in ("FIRST-ARRIVAL-001", "ORG-001", "RD-001", "XHS-001", "TTK-001"):
                run = runtime.create(
                    company_id="company-sim", ceo_id="ceo", scenario_id=scenario,
                    blueprint_version="v1", workspace_id="workspace-sim",
                )
                evidence = runtime.create_fixture_evidence(run["simulation_run_id"], label=scenario)
                self.assertEqual(evidence["verification_status"], "UNVERIFIED")
                run_ids.append(run["simulation_run_id"])
            run = runtime.transition(run_ids[0], "RUNNING", actor="SYSTEM", trigger="start")
            runtime.append(run["simulation_run_id"], "handoffs", {"handoffId": "h-1"})
            runtime.append(run["simulation_run_id"], "ceo_decisions", {"decisionId": "d-1", "choice": "accept"})
            runtime.set_final_state(run["simulation_run_id"], "CLOSED")
            with self.assertRaises(ValueError):
                runtime.review(run["simulation_run_id"], reviewer="CEO", pass_status="PASS")
            evidence = runtime.foundation.create(
                "EVIDENCE", company_id="company-sim", workspace_id="workspace-sim",
                verification_status="VERIFIED", evidence_condition="CURRENT",
            )
            runtime.append(run["simulation_run_id"], "evidence_refs", evidence["entity_id"])
            run = runtime.review(run["simulation_run_id"], reviewer="CEO", pass_status="PASS")
            self.assertEqual((run["lifecycle_status"], run["pass_status"]), ("PASSED", "PASS"))
            self.assertEqual(len(runtime.list(company_id="company-sim")), 5)

    def test_waiting_ceo_resume_failure_and_blueprint_invalidation(self):
        with TenantContext.scope("tenant-sim"):
            runtime = SimulationRuntime(self.db)
            run = runtime.create(
                company_id="company-sim", ceo_id="ceo", scenario_id="RD-001",
                blueprint_version="v1", workspace_id="workspace-sim",
            )
            run = runtime.transition(run["simulation_run_id"], "RUNNING", actor="SYSTEM", trigger="start")
            run = runtime.transition(run["simulation_run_id"], "WAITING_CEO", actor="SYSTEM", trigger="wait")
            with self.assertRaises(ActorNotAllowedError):
                runtime.transition(run["simulation_run_id"], "RUNNING", actor="SYSTEM", trigger="auto_resume")
            run = runtime.transition(run["simulation_run_id"], "RUNNING", actor="CEO", trigger="resume")
            runtime.append(run["simulation_run_id"], "failure_events", {"code": "fixture_failure"})
            run = runtime.review(run["simulation_run_id"], reviewer="CEO", pass_status="FAIL")
            self.assertEqual(run["lifecycle_status"], "FAILED")
            self.assertEqual(runtime.invalidate_workspace("workspace-sim", blueprint_version="v2", change_kind="CAPABILITY"), 1)
            self.assertIsNotNone(runtime.get(run["simulation_run_id"])["invalidated_at"])
            with self.db.connect() as conn:
                workspace = conn.execute("select blueprint_version, simulation_passed from workspaces where workspace_id = 'workspace-sim'").fetchone()
            self.assertEqual((workspace["blueprint_version"], workspace["simulation_passed"]), ("v2", 0))


if __name__ == "__main__":
    unittest.main()
