import unittest

from app.agent_conversion.coze_adapter import CozeAdapter


class CozeAdapterTest(unittest.TestCase):
    def test_binding_keeps_external_and_credential_refs_opaque(self):
        binding = CozeAdapter.binding("published-agent:123", "env:COZE_API_KEY")
        self.assertEqual(binding["external_ref"], "published-agent:123")
        self.assertEqual(binding["credential_ref"], "env:COZE_API_KEY")

    def test_invoke_normalizes_authorized_transport_response(self):
        seen = []

        def transport(external_ref, credential_ref, prompt):
            seen.append((external_ref, credential_ref, prompt))
            return {"status": "success", "output": "ok", "usage": {"tokens": 3}}

        result = CozeAdapter().invoke(
            {"external_ref": "published-agent:123", "credential_ref": "env:COZE_API_KEY"},
            "检查这个需求",
            transport,
        )
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["usage"]["tokens"], 3)
        self.assertEqual(seen[0][1], "env:COZE_API_KEY")

    def test_plaintext_credential_is_rejected(self):
        with self.assertRaises(ValueError):
            CozeAdapter.binding("published-agent:123", "sk-plaintext")


if __name__ == "__main__":
    unittest.main()
