import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from app.database import Database
from app.evolution_event_log import EvolutionEventLog
from app.evolution_governor import EvolutionGovernor
from app.result_store import ResultStore
from app.tenant_context import TenantContext


class EvolutionEventLogTest(unittest.TestCase):
    def setUp(self):
        self.tenant_scope = TenantContext.scope("selfuse", subject_id="offline-test")
        self.tenant_scope.__enter__()
        self.addCleanup(self.tenant_scope.__exit__, None, None, None)
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.event_log = EvolutionEventLog(self.db)

    def tearDown(self):
        self.tmp.cleanup()

    def test_table_created_on_initialize(self):
        with self.db.connect() as conn:
            row = conn.execute(
                "select name from sqlite_master where type='table' and name='evolution_events'"
            ).fetchone()
        self.assertIsNotNone(row)

    def test_record_and_get_by_correlation_id(self):
        self.event_log.record(correlation_id="c1", event_type="lock", payload={"module": "x"})
        rows = self.event_log.get_by_correlation_id("c1")
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["event_type"], "lock")
        self.assertEqual(rows[0]["payload"], {"module": "x"})
        self.assertEqual(rows[0]["correlation_id"], "c1")

    def test_reads_require_identity_and_isolate_tenants_with_same_correlation(self):
        self.event_log.record(correlation_id="shared", event_type="a1", payload={}, tenant_id="tenant-a")
        self.event_log.record(correlation_id="shared", event_type="b1", payload={}, tenant_id="tenant-b")
        self.event_log.record(correlation_id="shared", event_type="a2", payload={}, tenant_id="tenant-a")
        for tenant, expected in (("tenant-a", ["a1", "a2"]), ("tenant-b", ["b1"])):
            with TenantContext.scope(tenant, subject_id="fixture-" + tenant):
                self.assertEqual([x["event_type"] for x in self.event_log.get_by_correlation_id("shared")], expected)
                self.assertEqual([x["event_type"] for x in self.event_log.get_all()], expected)
        with TenantContext.scope("tenant-a"):
            with self.assertRaises(PermissionError):
                self.event_log.get_all()
            with self.assertRaises(PermissionError):
                self.event_log.get_by_correlation_id("shared")

    def test_worker_must_receive_the_trusted_context(self):
        import contextvars
        from concurrent.futures import ThreadPoolExecutor
        self.event_log.record(correlation_id="worker", event_type="worker-event", payload={}, tenant_id="tenant-a")
        with TenantContext.scope("tenant-a", subject_id="fixture-a"):
            captured = contextvars.copy_context()
        with ThreadPoolExecutor(max_workers=1) as pool:
            with self.assertRaises(PermissionError):
                pool.submit(self.event_log.get_all).result()
            rows = pool.submit(captured.run, self.event_log.get_by_correlation_id, "worker").result()
        self.assertEqual([row["event_type"] for row in rows], ["worker-event"])

    def test_real_task_job_routes_propagate_captured_identity(self):
        import asyncio
        from fastapi import BackgroundTasks
        from app.task_jobs import build_task_job_router

        log = self.event_log
        log.record(correlation_id="same-job", event_type="event-a", payload={}, tenant_id="tenant-a")
        log.record(correlation_id="same-job", event_type="event-b", payload={}, tenant_id="tenant-b")

        class Store:
            event_log = log
            database = self.db
            def get_task(self, task_id):
                return {"task_id": task_id, "project_id": "p", "status": "INIT", "state_flow": [],
                        "output": "", "error": "", "selected_tool": "", "cost": 0}
            def transition(self, task_id, state): pass
            def list_executions(self, task_id): return []

        class Orchestrator:
            seen = None
            async def run(self, task_id):
                self.seen = [e["event_type"] for e in log.get_by_correlation_id(task_id)]

        orchestrator = Orchestrator()
        router = build_task_job_router(Store(), orchestrator)
        start = next(r.endpoint for r in router.routes if "POST" in r.methods)
        status = next(r.endpoint for r in router.routes if "GET" in r.methods)
        background = BackgroundTasks()
        with TenantContext.scope("tenant-a", subject_id="owner-a"):
            self.assertEqual(start("p", "same-job", background)["task_id"], "same-job")
            self.assertEqual(status("same-job")["task_id"], "same-job")
        with TenantContext.scope("tenant-b", subject_id="owner-b"):
            asyncio.run(background())
        self.assertEqual(orchestrator.seen, ["event-a"])
        with TenantContext.scope("tenant-a"):
            with self.assertRaises(PermissionError):
                status("same-job")

    def test_real_governance_projection_respects_tenant(self):
        from app.governance import CompanyGovernance
        self.event_log.record(correlation_id="one", event_type="governance.action", payload={"origin": "a"}, tenant_id="tenant-a")
        self.event_log.record(correlation_id="one", event_type="governance.action", payload={"origin": "b"}, tenant_id="tenant-b")
        service = CompanyGovernance(self.db)
        for tenant, expected in (("tenant-a", "a"), ("tenant-b", "b")):
            with TenantContext.scope(tenant, subject_id="owner-" + tenant):
                self.assertEqual([e["payload"]["origin"] for e in service.list_governance_audit("ceo")], [expected])
        with TenantContext.scope("tenant-a"):
            with self.assertRaises(PermissionError):
                service.list_governance_audit("ceo")

    def test_existing_event_endpoint_filters_and_denies_missing_identity(self):
        from fastapi import HTTPException
        from app.main import create_app
        app = create_app(str(self.db.path))
        endpoint = next(route.endpoint for route in app.routes if getattr(route, "path", None) == "/api/evolution-events")
        self.event_log.record(correlation_id="same", event_type="first", payload={}, tenant_id="tenant-a")
        self.event_log.record(correlation_id="same", event_type="second", payload={}, tenant_id="tenant-b")
        with TenantContext.scope("tenant-a", subject_id="owner-a"):
            self.assertEqual([e["event_type"] for e in endpoint("same")], ["first"])
            self.assertEqual([e["event_type"] for e in endpoint()], ["first"])
        with TenantContext.scope("tenant-a"):
            with self.assertRaises(HTTPException) as error:
                endpoint("same")
            self.assertEqual(error.exception.status_code, 403)

    def test_no_update_or_delete_method(self):
        # Insert-only invariant: no mutation path must exist on the log.
        self.assertFalse(hasattr(self.event_log, "update"))
        self.assertFalse(hasattr(self.event_log, "delete"))
        self.assertFalse(hasattr(self.event_log, "mutate"))

    def test_correlation_linkage_isolates_events(self):
        self.event_log.record(correlation_id="c1", event_type="simulation", payload={"a": 1})
        self.event_log.record(correlation_id="c1", event_type="decision", payload={"b": 2})
        self.event_log.record(correlation_id="c2", event_type="rollback", payload={"c": 3})
        c1 = self.event_log.get_by_correlation_id("c1")
        self.assertEqual({e["event_type"] for e in c1}, {"simulation", "decision"})
        c2 = self.event_log.get_by_correlation_id("c2")
        self.assertEqual([e["event_type"] for e in c2], ["rollback"])


class StoreEventEmissionTest(unittest.TestCase):
    def setUp(self):
        self.tenant_scope = TenantContext.scope("selfuse", subject_id="offline-test")
        self.tenant_scope.__enter__()
        self.addCleanup(self.tenant_scope.__exit__, None, None, None)
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.event_log = EvolutionEventLog(self.db)
        self.store = ResultStore(self.db, self.event_log)

    def tearDown(self):
        self.tmp.cleanup()

    def test_store_emits_lock_event(self):
        self.store.save_architecture_lock(
            correlation_id="cx", module_name="tool_router", reason="r", locked_by="x"
        )
        rows = self.event_log.get_by_correlation_id("cx")
        self.assertEqual([e["event_type"] for e in rows], ["lock"])

    def test_store_emits_simulation_event(self):
        self.store.save_evolution_simulation(
            correlation_id="cy",
            task_id="t1",
            task_flow=["a"],
            tool_routing=["default_tool"],
            workflow_graph=[],
            performance_impact={},
        )
        rows = self.event_log.get_by_correlation_id("cy")
        self.assertEqual([e["event_type"] for e in rows], ["simulation"])

    def test_store_without_event_log_emits_nothing(self):
        silent_store = ResultStore(self.db)
        silent_store.save_architecture_lock(module_name="m", reason="r", locked_by="x")
        self.assertEqual(self.event_log.get_all(), [])


class GovernorEventEmissionTest(unittest.TestCase):
    def setUp(self):
        self.tenant_scope = TenantContext.scope("selfuse", subject_id="offline-test")
        self.tenant_scope.__enter__()
        self.addCleanup(self.tenant_scope.__exit__, None, None, None)
        self.tmp = TemporaryDirectory()
        self.db = Database(str(Path(self.tmp.name) / "curis.sqlite"))
        self.db.initialize()
        self.event_log = EvolutionEventLog(self.db)
        self.store = ResultStore(self.db, self.event_log)
        self.governor = EvolutionGovernor(self.store, self.event_log)

    def tearDown(self):
        self.tmp.cleanup()

    def test_governor_emits_correlated_events(self):
        task_record = self.store.create_task("governor-eval")
        task = {"task_id": task_record["task_id"]}
        workflow_plan = [{"action": "a1", "tool_required": "default_tool", "step": 0}]
        result = {
            "trace": [
                {
                    "action": "a1",
                    "tool_used": "default_tool",
                    "input": "i",
                    "output": "o",
                    "error": None,
                    "timestamp": "2026-07-07T00:00:00",
                }
            ],
            "cost": 0.0,
        }
        decision = self.governor.evaluate(
            task=task, workflow_plan=workflow_plan, result=result, inefficiencies=["workflow_length"]
        )
        correlation_id = decision["correlation_id"]
        self.assertIsNotNone(correlation_id)
        rows = self.event_log.get_by_correlation_id(correlation_id)
        types = {e["event_type"] for e in rows}
        self.assertEqual(types, {"proposal", "simulation", "decision", "rollback"})
        self.assertNotIn("lock", types)

    def test_governor_without_event_log_is_noop(self):
        silent_store = ResultStore(self.db)
        silent_governor = EvolutionGovernor(silent_store)
        task_record = silent_store.create_task("governor-eval-silent")
        task = {"task_id": task_record["task_id"]}
        workflow_plan = [{"action": "a1", "tool_required": "default_tool", "step": 0}]
        result = {"trace": [], "cost": 0.0}
        before = len(self.event_log.get_all())
        silent_governor.evaluate(
            task=task, workflow_plan=workflow_plan, result=result, inefficiencies=[]
        )
        self.assertEqual(len(self.event_log.get_all()), before)


if __name__ == "__main__":
    unittest.main()
