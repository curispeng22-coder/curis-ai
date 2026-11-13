"""Wave-1 验收：验证项 4（CEO 视图 /api/ceo/overview）。

运行方式（在 backend/ 目录下，使用项目 .venv）：
    ../.venv/bin/python -m pytest tests/test_v1_wave1_ceo_overview.py -v

覆盖：GET /api/ceo/overview → 200，返回
- 研发部(emp=6 / wf=17)
- 内容增长部(emp=12 / wf=12)
- 员工≈18 / 工作流实例≈29 / 公司包=2
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # 使 v1_wave1_helpers 可导入

from fastapi.testclient import TestClient
import pytest

from app.main import create_app

from v1_wave1_helpers import COMPANY_PACKAGES, TENANT, seed_wave1_full


@pytest.fixture
def client(tmp_path):
    db = str(tmp_path / "curis.sqlite")
    seed_wave1_full(db)
    app = create_app(db)
    return TestClient(app)


def test_ceo_overview_returns_200(client):
    r = client.get("/api/ceo/overview", headers={"X-Tenant-Id": TENANT})
    assert r.status_code == 200
    body = r.json()
    assert body["tenant_id"] == TENANT

    depts = {d["department_type"]: d for d in body["departments"]}
    assert set(depts.keys()) == {"tech.rd", "content.growth"}

    rd = depts["tech.rd"]
    content = depts["content.growth"]

    # 研发部
    assert rd["name"] == "研发部"
    assert rd["employee_count"] == 6
    assert rd["workflow_count"] == 17

    # 内容增长部
    assert content["name"] == "内容增长部"
    assert content["employee_count"] == 12
    assert content["workflow_count"] == 12

    # 聚合口径
    assert len(body["employees"]) == 18
    assert len(body["workflow_instances"]) == 29

    # 公司包
    pkg_ids = {cp["company_package_id"] for cp in body["company_packages"]}
    assert pkg_ids == set(COMPANY_PACKAGES)

    other = client.get("/api/ceo/overview", headers={"X-Tenant-Id": "other-tenant"})
    assert other.status_code == 200
    assert not ({cp["company_package_id"] for cp in other.json()["company_packages"]} & pkg_ids)


def test_ceo_overview_department_instances_present(client):
    """CEO 视图返回的两部门与 departments 表实例一致。"""
    r = client.get("/api/ceo/overview", headers={"X-Tenant-Id": TENANT})
    body = r.json()
    assert len(body["departments"]) == 2
    for d in body["departments"]:
        assert d["department_type"] in ("tech.rd", "content.growth")
        assert "employee_count" in d and "workflow_count" in d
