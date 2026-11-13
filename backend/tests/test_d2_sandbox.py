import os
import tempfile
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.evolution_governor import EvolutionGovernor
from app.governor_sandbox import GovernorSandbox
from app.result_store import ResultStore


class GovernorSandboxTest(unittest.TestCase):
    def test_run_produces_evidence(self):
        sandbox = GovernorSandbox({"module": "tool_router"})
        result = sandbox.run(
            {
                "proposal_type": "controlled_self_rewrite",
                "target_module": "tool_router",
                "change_summary": "tune routing weights",
            }
        )
        self.assertTrue(result["rolled_back"])
        self.assertIn("applied_state", result)
        self.assertIn("rollback_snapshot", result)
        self.assertIn("throwaway_path", result)
        self.assertIn("evidence_path", result)

    def test_throwaway_under_os_temp(self):
        sandbox = GovernorSandbox({})
        result = sandbox.run({"proposal_type": "x", "target_module": "y", "change_summary": "z"})
        self.assertTrue(result["throwaway_path"].startswith(tempfile.gettempdir()))

    def test_rollback_restores_exactly_and_apply_differs(self):
        original = {"module": "tool_router", "weight": 1}
        sandbox = GovernorSandbox(original)
        result = sandbox.run(
            {"proposal_type": "controlled_self_rewrite", "target_module": "tool_router", "change_summary": "tune"}
        )
        # applied changes the copy...
        self.assertNotEqual(result["applied_state"], result["rollback_snapshot"])
        self.assertIn("_sandbox_proposal", result["applied_state"])
        # ...but rollback restores the throwaway copy exactly to the original input.
        self.assertEqual(result["rollback_snapshot"], original)

    def test_apply_proposal_is_pure(self):
        snapshot = {"a": 1}
        out = GovernorSandbox._apply_proposal(snapshot, {"proposal_type": "x", "target_module": "y", "change_summary": "z"})
        # input is not mutated
        self.assertEqual(snapshot, {"a": 1})
        self.assertIn("_sandbox_proposal", out)


class GovernorDemonstrateSafetyTest(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.event_log = EvolutionEventLog(self.db)
        self.store = ResultStore(self.db, self.event_log)
        self.governor = EvolutionGovernor(self.store, self.event_log)

    def tearDown(self):
        self.tmp.cleanup()

    def test_demonstrate_writes_zero_bytes_to_authoritative_db(self):
        proposal = {
            "proposal_type": "controlled_self_rewrite",
            "target_module": "tool_router",
            "change_summary": "tune routing weights",
        }
        before_size = os.path.getsize(self.db.path)
        before_events = len(self.event_log.get_all())

        self.governor.demonstrate(proposal, dry_run=True)

        after_size = os.path.getsize(self.db.path)
        after_events = len(self.event_log.get_all())
        # No authoritative write, no evolution event emitted.
        self.assertEqual(after_size, before_size)
        self.assertEqual(after_events, before_events)

    def test_demonstrate_does_not_change_evaluate_behavior(self):
        task_record = self.store.create_task("demo-eval")
        task = {"task_id": task_record["task_id"]}
        workflow_plan = [{"action": "a1", "tool_required": "default_tool", "step": 0}]
        result = {"trace": [], "cost": 0.0}

        decision_before = self.governor.evaluate(
            task=task, workflow_plan=workflow_plan, result=result, inefficiencies=[]
        )
        self.governor.demonstrate(
            {"proposal_type": "controlled_self_rewrite", "target_module": "tool_router", "change_summary": "x"}
        )
        decision_after = self.governor.evaluate(
            task=task, workflow_plan=workflow_plan, result=result, inefficiencies=[]
        )
        # evaluate() logic unchanged by the additive demonstrate() method.
        self.assertEqual(decision_before["decision"], decision_after["decision"])


if __name__ == "__main__":
    unittest.main()
