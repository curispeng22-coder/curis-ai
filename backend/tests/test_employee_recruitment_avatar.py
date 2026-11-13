import tempfile
import sqlite3
from pathlib import Path

from fastapi.testclient import TestClient

from app.main import create_app


PNG_1X1 = (
    b"\x89PNG\r\n\x1a\n"
    b"\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x06\x00\x00\x00\x1f\x15\xc4\x89"
    b"\x00\x00\x00\rIDAT\x08\xd7c\xf8\xcf\xc0\xf0\x1f\x00\x05\x00\x01\xff\x89\x99=\x1d"
    b"\x00\x00\x00\x00IEND\xaeB`\x82"
)


def _recruit(client, headers, company_id, name, avatar_ref=""):
    response = client.post(
        "/api/workspace/talent-market/recruit",
        headers=headers,
        json={
            "company_id": company_id,
            "template_id": "et_product_manager",
            "name": name,
            "avatar_ref": avatar_ref,
        },
    )
    assert response.status_code == 201, response.text
    return response.json()["employee"]


def test_employee_avatar_upload_preset_fallback_and_restart():
    with tempfile.TemporaryDirectory(prefix="curis-employee-avatar-") as directory:
        database_path = str(Path(directory) / "data" / "curis.sqlite")
        headers = {"X-Tenant-Id": "avatar-company", "X-Ceo-Id": "avatar-ceo"}

        with TestClient(create_app(database_path)) as client:
            company = client.post(
                "/api/workspace/companies", headers=headers, json={"name": "头像验收公司"}
            )
            assert company.status_code == 201
            company_id = company.json()["company_id"]

            uploaded = _recruit(client, headers, company_id, "上传头像员工")
            preset = _recruit(client, headers, company_id, "预设头像员工", "preset:iris")
            fallback = _recruit(client, headers, company_id, "默认头像员工")

            upload = client.put(
                f"/api/workspace/employees/{uploaded['id']}/avatar",
                headers={**headers, "Content-Type": "image/png"},
                content=PNG_1X1,
            )
            assert upload.status_code == 200, upload.text
            uploaded = upload.json()
            assert uploaded["avatar_ref"].startswith("asset:")
            assert preset["avatar_ref"] == "preset:iris"
            assert fallback["avatar_ref"] == ""

            content = client.get(
                f"/api/workspace/employees/{uploaded['id']}/avatar/content", headers=headers
            )
            assert content.status_code == 200
            assert content.headers["content-type"].startswith("image/png")
            assert content.content == PNG_1X1

            before_invalid = uploaded["avatar_ref"]
            invalid = client.put(
                f"/api/workspace/employees/{uploaded['id']}/avatar",
                headers={**headers, "Content-Type": "text/plain"},
                content=b"not an image",
            )
            assert invalid.status_code == 415
            too_large = client.put(
                f"/api/workspace/employees/{uploaded['id']}/avatar",
                headers={**headers, "Content-Type": "image/png"},
                content=b"x" * (2 * 1024 * 1024 + 1),
            )
            assert too_large.status_code == 413
            employees = client.get("/api/workspace/employees", headers=headers).json()["employees"]
            by_name = {item["name"]: item for item in employees}
            assert len(employees) == 3
            assert by_name["上传头像员工"]["avatar_ref"] == before_invalid
            assert by_name["预设头像员工"]["avatar_ref"] == "preset:iris"
            assert by_name["默认头像员工"]["avatar_ref"] == ""
            assert all(not item["avatar_ref"].startswith("data:") for item in employees)

            other_headers = {"X-Tenant-Id": "other-company", "X-Ceo-Id": "other-ceo"}
            assert client.get(
                f"/api/workspace/employees/{uploaded['id']}/avatar/content",
                headers=other_headers,
            ).status_code == 404

            organization = client.get(
                f"/api/workspace/runtime/foundation/companies/{company_id}/organization",
                headers=headers,
            )
            assert organization.status_code == 200, organization.text
            projected = {item["name"]: item for item in organization.json()["employees"]}
            assert projected["上传头像员工"]["avatar_ref"] == before_invalid
            assert projected["预设头像员工"]["avatar_ref"] == "preset:iris"
            assert projected["默认头像员工"]["avatar_ref"] == ""

            with sqlite3.connect(database_path) as connection:
                connection.row_factory = sqlite3.Row
                row = connection.execute(
                    "select avatar_ref from employee_instances where id=?", (uploaded["id"],)
                ).fetchone()
                assert row["avatar_ref"] == before_invalid
                assert "data:" not in row["avatar_ref"]

        with TestClient(create_app(database_path)) as restarted:
            employees = restarted.get("/api/workspace/employees", headers=headers).json()["employees"]
            by_name = {item["name"]: item for item in employees}
            assert len(employees) == 3
            assert by_name["上传头像员工"]["avatar_ref"] == before_invalid
            assert by_name["预设头像员工"]["avatar_ref"] == "preset:iris"
            assert by_name["默认头像员工"]["avatar_ref"] == ""
            recovered = restarted.get(
                f"/api/workspace/employees/{uploaded['id']}/avatar/content", headers=headers
            )
            assert recovered.status_code == 200
            assert recovered.content == PNG_1X1


def test_recruit_rejects_unknown_preset_without_creating_employee():
    with tempfile.TemporaryDirectory(prefix="curis-employee-avatar-invalid-") as directory:
        database_path = str(Path(directory) / "curis.sqlite")
        headers = {"X-Tenant-Id": "avatar-invalid", "X-Ceo-Id": "avatar-ceo"}
        with TestClient(create_app(database_path)) as client:
            company_id = client.post(
                "/api/workspace/companies", headers=headers, json={"name": "头像校验公司"}
            ).json()["company_id"]
            response = client.post(
                "/api/workspace/talent-market/recruit",
                headers=headers,
                json={
                    "company_id": company_id,
                    "template_id": "et_product_manager",
                    "name": "错误预设",
                    "avatar_ref": "preset:not-real",
                },
            )
            assert response.status_code == 422
            assert client.get("/api/workspace/employees", headers=headers).json()["employees"] == []
