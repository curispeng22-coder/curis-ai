from __future__ import annotations

import tempfile
import unittest

from app.database import Database
from app.runtime import RuntimeFoundation
from app.tenant_context import TenantContext


class RuntimeFoundationPersistenceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".sqlite")
        self.db = Database(self.tmp.name)
        self.db.initialize()

    def test_founding_company_assistant_and_reverse_links_survive_restart(self):
        with TenantContext.scope("tenant-persist"):
            service = RuntimeFoundation(self.db)
            founding = service.create("FOUNDING_RUN", owner_ref="ceo-1")
            for target, actor in (
                ("INTENT_CAPTURED", "CEO"), ("CLARIFYING", "SYSTEM"),
                ("PROPOSED", "SYSTEM"), ("CEO_CONFIRMED", "CEO"),
            ):
                founding = service.transition(founding["entity_id"], target, actor=actor, trigger="test")
            founding, assistant = service.materialize_company(
                founding["entity_id"], company_id="company-persist", ceo_id="ceo-1", name="Curis"
            )
            brief = service.create("BRIEF", company_id="company-persist", parent_id=assistant["entity_id"])
            handoff = service.create("HANDOFF", company_id="company-persist", parent_id=assistant["entity_id"])
            decision = service.create("DECISION_PACKET", company_id="company-persist", parent_id=assistant["entity_id"])
            closeout = service.create("CLOSEOUT", company_id="company-persist", parent_id=assistant["entity_id"])
            for child in (brief, handoff, decision, closeout):
                service.link(assistant["entity_id"], "HAS_RUNTIME_OBJECT", child["entity_id"])

            restarted = RuntimeFoundation(Database(self.tmp.name))
            self.assertEqual(restarted.get(founding["entity_id"])["company_id"], "company-persist")
            self.assertEqual(restarted.get(assistant["entity_id"])["entity_type"], "CEO_ASSISTANT")
            self.assertEqual(len(restarted.related(assistant["entity_id"], "HAS_RUNTIME_OBJECT")), 4)
            self.assertEqual(
                restarted.related(assistant["entity_id"], "CREATED_ASSISTANT", reverse=True)[0]["entity"]["entity_id"],
                founding["entity_id"],
            )
            self.assertEqual(restarted.history(founding["entity_id"])[-1]["target"], "COMPANY_CREATED")
            with self.assertRaises(Exception):
                restarted.create("CEO_ASSISTANT", company_id="company-persist")

    def test_role_employee_capability_and_cycle_chain_is_queryable(self):
        with TenantContext.scope("tenant-chain"):
            with self.db.connect() as conn:
                conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-chain', 'tenant-chain', 'ceo', 'Chain')")
            service = RuntimeFoundation(self.db)
            employee = service.create("AI_EMPLOYEE", company_id="company-chain")
            role = service.create("ROLE_SLOT", company_id="company-chain")
            binding = service.create("CAPABILITY_BINDING", company_id="company-chain", capability_ref="cap-1")
            service.link(role["entity_id"], "ASSIGNED_EMPLOYEE", employee["entity_id"])
            service.link(employee["entity_id"], "HAS_CAPABILITY_BINDING", binding["entity_id"])
            cycle = service.create("CYCLE", company_id="company-chain")
            handoff = service.create("HANDOFF", company_id="company-chain", parent_id=cycle["entity_id"])
            evidence = service.create("EVIDENCE", company_id="company-chain", parent_id=handoff["entity_id"])
            acceptance = service.create("ACCEPTANCE", company_id="company-chain", parent_id=evidence["entity_id"])
            decision = service.create("DECISION_PACKET", company_id="company-chain", parent_id=acceptance["entity_id"])
            for source, relation, target in (
                (cycle, "HAS_HANDOFF", handoff), (handoff, "PRODUCED_EVIDENCE", evidence),
                (evidence, "HAS_ACCEPTANCE", acceptance), (acceptance, "HAS_DECISION", decision),
            ):
                service.link(source["entity_id"], relation, target["entity_id"])
            self.assertEqual(service.related(role["entity_id"])[0]["entity"]["entity_id"], employee["entity_id"])
            self.assertEqual(service.related(employee["entity_id"])[0]["entity"]["entity_id"], binding["entity_id"])
            self.assertEqual(service.related(acceptance["entity_id"])[0]["entity"]["entity_id"], decision["entity_id"])

    def test_content_and_interaction_reverse_chains_are_queryable(self):
        with TenantContext.scope("tenant-content"):
            with self.db.connect() as conn:
                conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-content', 'tenant-content', 'ceo', 'Content')")
                conn.execute("insert into workspaces(workspace_id, tenant_id, business_id, company_id, name, status) values ('workspace-content', 'tenant-content', 'business', 'company-content', 'Content WS', 'DRAFT')")
            service = RuntimeFoundation(self.db)
            content = service.create("CONTENT_ITEM", company_id="company-content", workspace_id="workspace-content")
            run = service.create("CYCLE", company_id="company-content", workspace_id="workspace-content", execution_ref="content_workflow_run:run-1")
            outcome = service.create("OUTCOME", company_id="company-content", workspace_id="workspace-content")
            service.link(content["entity_id"], "HAS_RUN", run["entity_id"])
            service.link(run["entity_id"], "PRODUCED_OUTCOME", outcome["entity_id"])
            interaction = service.create("INTERACTION_ITEM", company_id="company-content", workspace_id="workspace-content", parent_id=content["entity_id"])
            response = service.create("INTERACTION_RESPONSE", company_id="company-content", workspace_id="workspace-content", parent_id=interaction["entity_id"])
            receipt = service.create("PUBLICATION_RECEIPT", company_id="company-content", workspace_id="workspace-content", parent_id=response["entity_id"])
            service.link(interaction["entity_id"], "HAS_RESPONSE_VERSION", response["entity_id"])
            service.link(response["entity_id"], "HAS_EXTERNAL_RECEIPT", receipt["entity_id"])
            self.assertEqual(service.related(content["entity_id"])[0]["entity"]["entity_id"], run["entity_id"])
            self.assertEqual(service.related(run["entity_id"])[0]["entity"]["entity_id"], outcome["entity_id"])
            self.assertEqual(service.related(interaction["entity_id"])[0]["entity"]["entity_id"], response["entity_id"])
            self.assertEqual(service.related(response["entity_id"])[0]["entity"]["entity_id"], receipt["entity_id"])


if __name__ == "__main__":
    unittest.main()
