import unittest
from pathlib import Path

from app.role_context import RoleContextReference


class RoleContextReferenceTest(unittest.TestCase):
    def setUp(self):
        self.profiles_path = Path(__file__).resolve().parents[2] / "knowledge" / "ROLE_PROFILES.md"
        self.reference = RoleContextReference(self.profiles_path)

    def test_builds_compact_context_from_explicit_profile_id(self):
        context = self.reference.build("curis.role.system-delivery.v1")
        full_profile = self.reference.full_profile("curis.role.system-delivery.v1")

        self.assertIsNotNone(context)
        self.assertEqual(context["profile_id"], "curis.role.system-delivery.v1")
        self.assertEqual(context["role_name"], "系统交付席")
        self.assertIn("Convert approved issues", context["role_intent"])
        self.assertIn("Owns system architecture", context["responsibility_boundary"])
        self.assertIn("Delivery", context["expected_output_shape"])
        self.assertIn("产品规划席", context["escalation_triggers"])
        self.assertIn("ADR-0005", context["source_references"])
        self.assertLess(len(context["context_excerpt"]), len(full_profile))
        self.assertNotIn("Minimal Context References", context["context_excerpt"])

    def test_missing_profile_id_omits_role_context_without_default(self):
        self.assertIsNone(self.reference.build(""))
        self.assertIsNone(self.reference.build(None))

    def test_invalid_profile_id_omits_role_context_without_inference(self):
        self.assertIsNone(self.reference.build("curis.role.unknown.v1"))


if __name__ == "__main__":
    unittest.main()
