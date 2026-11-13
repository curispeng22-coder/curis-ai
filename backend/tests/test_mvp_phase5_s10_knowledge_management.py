from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import create_app


ROOT = Path(__file__).resolve().parents[2]
HEADERS = {"X-Tenant-Id": "tenant-s10", "X-Ceo-Id": "ceo-s10"}


class MVPPhase5S10KnowledgeManagementTests(unittest.TestCase):
    def setUp(self):
        database = tempfile.NamedTemporaryFile(delete=False)
        self.db_path = database.name
        database.close()
        self.addCleanup(lambda: os.path.exists(self.db_path) and os.unlink(self.db_path))
        self.vault = tempfile.TemporaryDirectory()
        self.addCleanup(self.vault.cleanup)
        vault = Path(self.vault.name)
        (vault / "notes").mkdir()
        (vault / "notes" / "brief.md").write_text(
            "# 可审计 AI 团队\n\n真实交付需要任务、人员、模型、成本和成果证据。",
            encoding="utf-8",
        )
        (vault / "readme.txt").write_text("Curis 本地资料连接。", encoding="utf-8")
        (vault / "ignored.pdf").write_bytes(b"%PDF")
        outside = Path(self.vault.name).parent / "outside-s10.md"
        outside.write_text("outside", encoding="utf-8")
        self.addCleanup(lambda: outside.exists() and outside.unlink())
        try:
            (vault / "escape.md").symlink_to(outside)
        except OSError:
            pass
        environment = patch.dict(
            os.environ,
            {
                "CURIS_ENV": "test",
                "CURIS_IDENTITY_MODE": "test",
                "CURIS_KNOWLEDGE_ROOTS": self.vault.name,
            },
        )
        environment.start()
        self.addCleanup(environment.stop)
        self.client = TestClient(create_app(self.db_path))
        self.addCleanup(self.client.close)

    def _root_id(self) -> str:
        response = self.client.get(
            "/api/workspace/knowledge/connectors/local-files",
            headers=HEADERS,
        )
        self.assertEqual(response.status_code, 200, response.text)
        payload = response.json()
        self.assertEqual(payload["connector"]["capability_type"], "connector")
        self.assertEqual(payload["connector"]["status"], "configured")
        self.assertEqual(len(payload["roots"]), 1)
        self.assertNotIn(self.vault.name, str(payload))
        return payload["roots"][0]["root_id"]

    def _project(self) -> str:
        company = self.client.get(
            "/api/workspace/companies", headers=HEADERS
        ).json()["companies"][0]
        department = self.client.post(
            "/api/workspace/departments",
            headers=HEADERS,
            json={
                "company_id": company["company_id"],
                "template_id": "official.department.software_rnd",
                "name": "S10 知识业务部",
            },
        ).json()
        response = self.client.post(
            "/api/workspace/projects",
            headers=HEADERS,
            json={
                "company_id": company["company_id"],
                "department_id": department["id"],
                "name": "S10 知识项目",
                "goal": "沉淀可检索项目资料",
                "status": "active",
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        return response.json()["project_id"]

    def test_local_connector_imports_and_updates_one_traceable_entry(self):
        root_id = self._root_id()
        listed = self.client.get(
            "/api/workspace/knowledge/connectors/local-files/files",
            headers=HEADERS,
            params={"root_id": root_id},
        )
        self.assertEqual(listed.status_code, 200, listed.text)
        paths = {item["relative_path"] for item in listed.json()["files"]}
        self.assertEqual(paths, {"notes/brief.md", "readme.txt"})

        response = self.client.post(
            "/api/workspace/knowledge/import",
            headers=HEADERS,
            json={
                "root_id": root_id,
                "relative_path": "notes/brief.md",
                "tags": ["AI 团队", "审计"],
            },
        )
        self.assertEqual(response.status_code, 201, response.text)
        first = response.json()
        self.assertEqual(first["title"], "可审计 AI 团队")
        self.assertEqual(first["source_path"], "notes/brief.md")
        self.assertNotIn(self.vault.name, str(first))
        self.assertEqual(first["scope"], "company")

        (Path(self.vault.name) / "notes" / "brief.md").write_text(
            "# 可审计 AI 团队\n\n更新后的真实交付证据。",
            encoding="utf-8",
        )
        updated = self.client.post(
            "/api/workspace/knowledge/import",
            headers=HEADERS,
            json={
                "root_id": root_id,
                "relative_path": "notes/brief.md",
                "tags": ["AI 团队"],
            },
        )
        self.assertEqual(updated.status_code, 201, updated.text)
        self.assertEqual(updated.json()["id"], first["id"])
        self.assertIn("更新后的真实交付证据", updated.json()["body"])

        searched = self.client.get(
            "/api/workspace/knowledge/entries",
            headers=HEADERS,
            params={"q": "更新后的真实交付"},
        )
        self.assertEqual(searched.status_code, 200, searched.text)
        self.assertEqual([item["id"] for item in searched.json()["entries"]], [first["id"]])

    def test_connector_rejects_unapproved_or_unsupported_paths(self):
        root_id = self._root_id()
        for path in ("../outside-s10.md", "ignored.pdf", "/etc/hosts", "escape.md"):
            response = self.client.post(
                "/api/workspace/knowledge/import",
                headers=HEADERS,
                json={"root_id": root_id, "relative_path": path},
            )
            self.assertEqual(response.status_code, 422, (path, response.text))
        unknown = self.client.get(
            "/api/workspace/knowledge/connectors/local-files/files",
            headers=HEADERS,
            params={"root_id": "unknown"},
        )
        self.assertEqual(unknown.status_code, 422, unknown.text)

    def test_manual_project_knowledge_is_searchable_and_tenant_scoped(self):
        project_id = self._project()
        created = self.client.post(
            "/api/workspace/knowledge/entries",
            headers=HEADERS,
            json={
                "title": "项目事实清单",
                "body": "浏览器验收必须检查真实任务闭环。",
                "tags": ["验收", "浏览器"],
                "project_id": project_id,
            },
        )
        self.assertEqual(created.status_code, 201, created.text)
        entry = created.json()
        self.assertEqual(entry["scope"], "project")
        self.assertEqual(entry["scope_name"], "S10 知识项目")

        project_entries = self.client.get(
            "/api/workspace/knowledge/entries",
            headers=HEADERS,
            params={"scope": "project", "q": "浏览器"},
        )
        self.assertEqual(project_entries.status_code, 200, project_entries.text)
        self.assertEqual(len(project_entries.json()["entries"]), 1)

        other_headers = {"X-Tenant-Id": "tenant-other", "X-Ceo-Id": "ceo-other"}
        other = self.client.get(
            "/api/workspace/knowledge/entries", headers=other_headers
        )
        self.assertEqual(other.status_code, 200, other.text)
        self.assertEqual(other.json()["entries"], [])
        hidden = self.client.get(
            f"/api/workspace/knowledge/entries/{entry['id']}",
            headers=other_headers,
        )
        self.assertEqual(hidden.status_code, 404, hidden.text)

        invalid = self.client.post(
            "/api/workspace/knowledge/entries",
            headers=HEADERS,
            json={
                "title": "越界项目",
                "body": "不可写入。",
                "project_id": "project-missing",
            },
        )
        self.assertEqual(invalid.status_code, 422, invalid.text)

    def test_frontend_replaces_samples_with_real_knowledge_flow(self):
        paths = [
            ROOT / "frontend/lib/knowledge.js",
            ROOT / "frontend/app/ceo-office/knowledge/page.js",
            ROOT / "frontend/app/ceo-office/knowledge/entries/[id]/page.js",
        ]
        source = "\n".join(path.read_text(encoding="utf-8") for path in paths)
        for value in (
            "getKnowledgeEntries",
            "getLocalKnowledgeRoots",
            "导入文件",
            "新建资料",
            "搜索标题、正文或标签",
            "相对路径",
            "资料正文",
        ):
            self.assertIn(value, source)
        self.assertNotIn("SAMPLE_ENTRIES", source)
        self.assertNotIn("TerraSampleBadge", source)
        self.assertIn("target_type", source)
        self.assertIn("getWorkKnowledgeReferences", source)
        self.assertNotIn("getProjects", source)
        self.assertNotIn("getDepartments", source)


if __name__ == "__main__":
    unittest.main()
