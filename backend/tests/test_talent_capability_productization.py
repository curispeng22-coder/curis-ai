import tempfile
import pytest
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


def test_repository_package_install_is_pinned_inert_and_survives_restart(tmp_path, monkeypatch):
    from test_skill_package import archive, REPO, COMMIT
    from app import skill_package
    source = {"repo_url": REPO, "commit": COMMIT, "subdirectory": "skills/research"}
    raw = archive()
    requests = []
    def fetch(url):
        requests.append(url)
        return raw
    monkeypatch.setattr(skill_package, "fetch_public", fetch)
    database_path = str(tmp_path / "package.sqlite")
    headers = {"X-Tenant-Id": "package-test", "X-Ceo-Id": "package-ceo"}
    with TestClient(create_app(database_path)) as client:
        preview = client.post("/api/workspace/skills/packages/preview", headers=headers, json=source)
        assert preview.status_code == 200, preview.text
        manifest = preview.json()
        assert len(manifest["files"]) == 4
        assert not (tmp_path / "skill-packages").exists()
        body = {**source, "expected_package_sha256": manifest["package_sha256"], "license_accepted": True}
        rejected = client.post("/api/workspace/skills/packages/install", headers=headers, json={**body, "expected_package_sha256": "0" * 64})
        assert rejected.status_code == 422
        assert not (tmp_path / "skill-packages").exists()
        installed = client.post("/api/workspace/skills/packages/install", headers=headers, json=body)
        assert installed.status_code == 201, installed.text
        skill = installed.json()
        again = client.post("/api/workspace/skills/packages/install", headers=headers, json=body)
        assert again.status_code == 201, again.text
        assert again.json()["skill_template_id"] == skill["skill_template_id"]
    with TestClient(create_app(database_path)) as client:
        rows = client.get("/api/workspace/skills/templates", headers=headers).json()["skills"]
        restored = next(row for row in rows if row["skill_template_id"] == skill["skill_template_id"])
        assert restored["package"]["package_sha256"] == manifest["package_sha256"]
        assert restored["installation_kind"] == "FULL_PACKAGE"
    assert all(url.endswith("/tar.gz/" + COMMIT) for url in requests)


def test_recruit_install_bind_and_restart_keep_canonical_truth():
    with tempfile.TemporaryDirectory(prefix="curis-talent-product-") as directory:
        database_path = str(Path(directory) / "curis.sqlite")
        headers = {"X-Tenant-Id": "talent-product", "X-Ceo-Id": "talent-ceo"}

        with TestClient(create_app(database_path)) as client:
            company = client.post(
                "/api/workspace/companies",
                headers=headers,
                json={"name": "人才与能力验收公司"},
            )
            assert company.status_code == 201
            recruit = client.post(
                "/api/workspace/talent-market/recruit",
                headers=headers,
                json={
                    "company_id": company.json()["company_id"],
                    "template_id": "et_product_manager",
                    "name": "产品经理小策",
                },
            )
            assert recruit.status_code == 201
            employee_id = recruit.json()["employee"]["id"]
            default_bindings = recruit.json()["skills"]["bindings"]
            assert default_bindings
            assert recruit.json()["tool_status"] == "blocked_required_capability"

            skill_id = "official.skill.requirement_analysis"
            first_install = client.post(
                f"/api/workspace/skills/templates/{skill_id}/install", headers=headers
            )
            second_install = client.post(
                f"/api/workspace/skills/templates/{skill_id}/install", headers=headers
            )
            assert first_install.status_code == 201
            assert second_install.status_code == 201
            assert first_install.json()["skill_template_id"] == second_install.json()["skill_template_id"]

            existing = client.get(
                f"/api/workspace/employees/{employee_id}/skills", headers=headers
            ).json()["bindings"]
            bindings = [
                {
                    "skill_template_id": item["skill_template_id"],
                    "capability_binding_ids": item.get("capability_binding_ids", []),
                    "priority": item.get("priority", 100),
                    "enabled": item.get("enabled", True),
                }
                for item in existing
            ]
            bindings.append(
                {
                    "skill_template_id": first_install.json()["skill_template_id"],
                    "priority": 50,
                    "enabled": True,
                }
            )
            assigned = client.put(
                f"/api/workspace/employees/{employee_id}/skills",
                headers=headers,
                json={"bindings": bindings},
            )
            assert assigned.status_code == 200
            assert {item["skill_template_id"] for item in assigned.json()["bindings"]} == {
                default_bindings[0]["skill_template_id"],
                first_install.json()["skill_template_id"],
            }

            connectors = client.get("/api/connectors", headers=headers).json()["connectors"]
            assert connectors
            assert all(item["authorization_status"] == "not_authorized" for item in connectors)
            assert all(item["health_status"] == "unknown" for item in connectors)
            assert all(item["mock_only"] for item in connectors)

        with TestClient(create_app(database_path)) as restarted:
            employees = restarted.get("/api/workspace/employees", headers=headers).json()["employees"]
            assert [item["id"] for item in employees] == [employee_id]
            bindings_after_restart = restarted.get(
                f"/api/workspace/employees/{employee_id}/skills", headers=headers
            ).json()["bindings"]
            assert {item["skill_template_id"] for item in bindings_after_restart} == {
                default_bindings[0]["skill_template_id"],
                first_install.json()["skill_template_id"],
            }

            other_headers = {"X-Tenant-Id": "other-tenant", "X-Ceo-Id": "other-ceo"}
            assert restarted.get(
                "/api/workspace/employees", headers=other_headers
            ).json()["employees"] == []


def test_link_install_bind_unbind_remove_retains_canonical_receipts(tmp_path, monkeypatch):
    import json
    from test_skill_package import archive, REPO, COMMIT
    from app import skill_package
    raw = archive({"repo/LICENSE": b"MIT fixture", "repo/guidance/SKILL.md": b"# Plain research", "repo/guidance/references/method.md": b"Cite sources"})
    monkeypatch.setattr(skill_package, "fetch_public", lambda url: json.dumps({"sha": COMMIT}).encode() if "/commits/" in url else raw)
    db = str(tmp_path / "journey.sqlite")
    headers = {"X-Tenant-Id": "skill-journey", "X-Ceo-Id": "ceo"}
    with TestClient(create_app(db)) as client:
        preview = client.post("/api/workspace/skills/packages/preview", headers=headers, json={"repo_url": REPO})
        assert preview.status_code == 200, preview.text
        manifest = preview.json()
        assert manifest["subdirectory"] == "guidance" and manifest["commit"] == COMMIT
        body = {"repo_url": manifest["repo_url"], "commit": manifest["commit"], "subdirectory": manifest["subdirectory"], "expected_package_sha256": manifest["package_sha256"], "license_accepted": True}
        installed = client.post("/api/workspace/skills/packages/install", headers=headers, json=body).json()
        assert installed["dependency_status"]["ready"] is True
        skill_id = installed["skill_template_id"]
        company = client.post("/api/workspace/companies", headers=headers, json={"name": "Skill test"}).json()["company_id"]
        employee = client.post("/api/workspace/talent-market/recruit", headers=headers, json={"company_id": company, "template_id": "et_product_manager", "name": "Researcher"}).json()["employee"]["id"]
        endpoint = f"/api/workspace/employees/{employee}/skills"
        old = client.get(endpoint, headers=headers).json()["bindings"]
        keep = [{key: x[key] for key in ("binding_id", "skill_template_id", "capability_binding_ids", "priority", "enabled")} for x in old]
        bound = client.post(endpoint + "/" + skill_id, headers=headers)
        assert bound.status_code == 200, bound.text
        assert bound.json()["bindings"][0]["binding_id"] == old[0]["binding_id"]
        assert client.put(endpoint, headers=headers, json={"bindings": keep}).status_code == 200
        assert len(client.get(endpoint, headers=headers).json()["bindings"]) == len(old)
        assert client.put(endpoint, headers=headers, json={"bindings": [*keep, {"skill_template_id": skill_id}]}).status_code == 200
        other = {"X-Tenant-Id": "other", "X-Ceo-Id": "other"}
        assert client.delete(f"/api/workspace/skills/templates/{skill_id}", headers=other).status_code == 422
        assert client.delete(f"/api/workspace/skills/templates/{skill_id}?company_id=another-company", headers=headers).status_code == 422
        removed = client.delete(f"/api/workspace/skills/templates/{skill_id}?company_id={company}", headers=headers)
        assert removed.status_code == 200 and removed.json()["history_retained"] and removed.json()["package_retained"]
        assert skill_id not in {x["skill_template_id"] for x in client.get(endpoint, headers=headers).json()["bindings"]}
        assert client.put(endpoint, headers=headers, json={"bindings": [{"skill_template_id": skill_id}]}).status_code == 422
        assert list((tmp_path / "skill-packages").rglob(".curis-package.json"))
    with TestClient(create_app(db)) as client:
        assert skill_id not in {x["skill_template_id"] for x in client.get("/api/workspace/skills/templates", headers=headers).json()["skills"]}
        assert client.post("/api/workspace/skills/packages/install", headers=headers, json=body).json()["skill_template_id"] == skill_id
        assert skill_id not in {x["skill_template_id"] for x in client.get(endpoint, headers=headers).json()["bindings"]}


def _concurrency_fixture(tmp_path):
    database_path = str(tmp_path / "concurrent.sqlite")
    headers = {"X-Tenant-Id": "skill-atomic", "X-Ceo-Id": "ceo"}
    with TestClient(create_app(database_path)) as client:
        employees = []
        companies = []
        for name in ["A", "B"]:
            company = client.post("/api/workspace/companies", headers=headers, json={"name": name}).json()["company_id"]
            companies.append(company)
            employees.append(client.post("/api/workspace/talent-market/recruit", headers=headers, json={"company_id": company, "template_id": "et_product_manager", "name": name}).json()["employee"]["id"])
        skills = [client.post("/api/workspace/skills/templates", headers=headers, json={"slug": "atomic-" + name, "name": name}).json() for name in ["target", "new"]]
        endpoint = f"/api/workspace/employees/{employees[0]}/skills/{skills[0]['skill_template_id']}"
        assert client.post(endpoint, headers=headers).status_code == 200
    return database_path, employees, companies, skills


def test_concurrent_item_unbind_keeps_new_skill_and_unrelated_binding_identity(tmp_path):
    import threading
    from app.database import Database
    from app.skill_runtime import SkillRuntime
    from app.tenant_context import TenantContext
    path, employees, _, skills = _concurrency_fixture(tmp_path)
    service = SkillRuntime(Database(path))
    tenant = skills[0]["tenant_id"]
    with TenantContext.scope(tenant):
        before = service.list_employee_bindings(employees[0])["bindings"]
    start = threading.Barrier(3)
    errors = []
    def change(remove):
        try:
            with TenantContext.scope(tenant):
                start.wait(timeout=3)
                service.change_employee_binding(employees[0], skills[0 if remove else 1]["skill_template_id"], remove=remove)
        except Exception as error:
            errors.append(error)
    threads = [threading.Thread(target=change, args=(remove,)) for remove in [True, False]]
    for thread in threads: thread.start()
    start.wait(timeout=3)
    for thread in threads: thread.join(timeout=5)
    assert not errors and all(not thread.is_alive() for thread in threads)
    with TenantContext.scope(tenant):
        after = service.list_employee_bindings(employees[0])["bindings"]
        ids = {x["skill_template_id"]: x["binding_id"] for x in after}
        assert skills[0]["skill_template_id"] not in ids and skills[1]["skill_template_id"] in ids
        for item in before:
            if item["skill_template_id"] != skills[0]["skill_template_id"]:
                assert ids[item["skill_template_id"]] == item["binding_id"]
        service.change_employee_binding(employees[0], skills[1]["skill_template_id"])
        assert ids == {x["skill_template_id"]: x["binding_id"] for x in service.list_employee_bindings(employees[0])["bindings"]}


@pytest.mark.parametrize("writer", ["item", "replace"])
def test_remove_holds_write_lock_before_reference_check_and_rejects_waiting_new_binding(tmp_path, writer):
    import threading
    from contextlib import contextmanager
    from app.database import Database
    from app.skill_runtime import SkillRuntime
    from app.tenant_context import TenantContext
    path, employees, companies, skills = _concurrency_fixture(tmp_path)
    checked, attempted, release, completed = [threading.Event() for _ in range(4)]
    errors = []
    class ObservedDatabase(Database):
        @contextmanager
        def connect(self):
            with super().connect() as connection:
                def trace(sql):
                    if threading.current_thread().name == "skill-remover" and sql.startswith("select distinct e.company_id"):
                        checked.set(); release.wait(timeout=3)
                    if threading.current_thread().name == "skill-binder" and sql == "BEGIN IMMEDIATE":
                        attempted.set()
                connection.set_trace_callback(trace)
                yield connection
    service = SkillRuntime(ObservedDatabase(path))
    tenant, target = skills[0]["tenant_id"], skills[0]["skill_template_id"]
    def remove():
        try:
            with TenantContext.scope(tenant): service.remove_template(target, companies[0])
        except Exception as error: errors.append(error)
    def bind():
        try:
            with TenantContext.scope(tenant):
                if writer == "item": service.change_employee_binding(employees[1], target)
                else: service.set_employee_bindings(employees[1], [{"skill_template_id": target}])
        except Exception as error: errors.append(error)
        finally: completed.set()
    first = threading.Thread(target=remove, name="skill-remover"); second = threading.Thread(target=bind, name="skill-binder")
    first.start()
    try:
        assert checked.wait(timeout=3)
        second.start()
        assert attempted.wait(timeout=3)
        assert not completed.wait(timeout=0.1), "binding entered between reference check and removal"
    finally:
        release.set(); first.join(timeout=5)
        if second.ident is not None: second.join(timeout=5)
    assert not first.is_alive() and not second.is_alive()
    assert len(errors) == 1 and isinstance(errors[0], ValueError) and "active" in str(errors[0])
    with TenantContext.scope(tenant):
        assert service._get_template(target)["status"] == "disabled"
        assert not any(x["skill_template_id"] == target for employee in employees for x in service.list_employee_bindings(employee)["bindings"])
