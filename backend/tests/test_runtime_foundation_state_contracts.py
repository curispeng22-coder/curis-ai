from __future__ import annotations

import tempfile
import unittest

from app.database import Database
from app.runtime import RuntimeFoundation, get_machine
from app.runtime.state_machine import ActorNotAllowedError, GuardRejectedError, IllegalTransitionError
from app.tenant_context import TenantContext


class RuntimeFoundationStateContractTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.NamedTemporaryFile(suffix=".sqlite")
        self.db = Database(self.tmp.name)
        self.db.initialize()

    def test_registry_rejects_illegal_actor_and_automatic_ceo_approval(self):
        self.assertTrue(get_machine("founding_run").can("ARRIVED", "INTENT_CAPTURED"))
        with self.assertRaises(IllegalTransitionError):
            get_machine("founding_run").transition("f", "ARRIVED", "COMPLETED", actor="CEO")
        with self.assertRaises(ActorNotAllowedError):
            get_machine("cycle").transition(
                "c", "WAITING_CEO", "ACCEPTED", actor="SYSTEM", context={"acceptanceId": "a"}
            )
        with self.assertRaises(GuardRejectedError):
            get_machine("cycle").transition("c", "WAITING_CEO", "ACCEPTED", actor="CEO")

    def test_lifecycle_and_evidence_are_orthogonal_and_fixture_never_verified(self):
        with TenantContext.scope("tenant-state"):
            service = RuntimeFoundation(self.db)
            evidence = service.create("EVIDENCE", data={"fixture": True})
            self.assertEqual(evidence["lifecycle_status"], "CURRENT")
            self.assertEqual(evidence["verification_status"], "UNVERIFIED")
            with self.assertRaises(ValueError):
                service.set_dimensions(evidence["entity_id"], verification_status="VERIFIED")

    def test_content_publish_and_interaction_response_require_version_and_receipt(self):
        with TenantContext.scope("tenant-content-state"):
            service = RuntimeFoundation(self.db)
            with self.db.connect() as conn:
                conn.execute("insert into companies(company_id, tenant_id, ceo_id, name) values ('company-content-state', 'tenant-content-state', 'ceo', 'Content')")
            content = service.create("CONTENT_ITEM", company_id="company-content-state")
            content = service.transition(content["entity_id"], "DRAFT", actor="SYSTEM", trigger="accept")
            content = service.transition(content["entity_id"], "IN_REVIEW", actor="AI_EMPLOYEE", trigger="review")
            with self.assertRaises(GuardRejectedError):
                service.transition(content["entity_id"], "APPROVED", actor="CEO", trigger="approve")
            service.set_version_refs(content["entity_id"], approved_version_id="version-1")
            content = service.transition(content["entity_id"], "APPROVED", actor="CEO", trigger="approve")
            service.set_version_refs(content["entity_id"], published_version_id="version-1")
            with self.assertRaises(GuardRejectedError):
                service.transition(content["entity_id"], "PUBLISHED", actor="CEO", trigger="publish")
            content = service.transition(
                content["entity_id"], "PUBLISHED", actor="CEO", trigger="publish",
                context={"manualFeedbackRef": "feedback-1"},
            )
            self.assertEqual(content["lifecycle_status"], "PUBLISHED")

            interaction = service.create("INTERACTION_ITEM", company_id="company-content-state")
            interaction = service.transition(interaction["entity_id"], "CLASSIFIED", actor="SYSTEM", trigger="classify")
            with self.assertRaises(GuardRejectedError):
                service.transition(
                    interaction["entity_id"], "RESPONDED", actor="SYSTEM", trigger="respond",
                    context={"replyPolicy": "AUTO_APPROVED"},
                )
            interaction = service.transition(
                interaction["entity_id"], "RESPONDED", actor="SYSTEM", trigger="respond",
                context={"replyPolicy": "AUTO_APPROVED", "responseVersion": "response-1", "externalReceipt": "receipt-1"},
            )
            self.assertEqual(interaction["lifecycle_status"], "RESPONDED")


if __name__ == "__main__":
    unittest.main()
