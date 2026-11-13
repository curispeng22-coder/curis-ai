"""Wave 2 验证项 4（F2 成果展示中心）。

覆盖：
- GET /api/results/summary 返回发布包 / 内容运行汇总
  （publish_packages≥1, content_runs≥1, completed≥1）。
- GET /api/results/publish-packages 至少含 1 个发布包。
- GET /api/results/content-workflow-runs 至少含 1 条内容运行。
- 前置：先通过 ContentWorkflowRuntime 跑一条内容闭环写入数据。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("CURIS_CONNECTOR_MODE", "mock")

from app.content_workflow_runtime import ContentWorkflowRuntime  # noqa: E402
from app.runtime_governance import AutoApproveSink  # noqa: E402
from app.credential_vault import CredentialVaultService  # noqa: E402
from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.main import create_app  # noqa: E402
from app.tenant_context import DEFAULT_TENANT, TenantContext  # noqa: E402

import pytest  # noqa: E402
from fastapi.testclient import TestClient


@pytest.fixture
def client_with_content_run(seeded_db):
    db = Database(seeded_db)
    db.initialize()
    event_log = EvolutionEventLog(db)
    vault = CredentialVaultService(db, event_log)
    with TenantContext.scope(DEFAULT_TENANT):
        cwr = ContentWorkflowRuntime(db, event_log, vault)
        cwr.run(
            prompt="夏季防晒：3 个误区",
            platforms=["xhs", "douyin"],
            source_workflow="wl_ai_content_content_production_sop",
            decision_sink=AutoApproveSink(),
        )
    app = create_app(db_path=seeded_db)
    return TestClient(app)


def test_results_summary(client_with_content_run):
    resp = client_with_content_run.get(
        "/api/results/summary", headers={"X-Tenant-Id": DEFAULT_TENANT}
    )
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data["tenant_id"] == DEFAULT_TENANT
    assert data["publish_packages"]["total"] >= 1, data
    assert data["publish_packages"]["published"] >= 1, data
    assert data["content_workflow_runs"]["total"] >= 1, data
    assert data["content_workflow_runs"]["completed"] >= 1, data
    # 研发工作流运行计数存在（研发部曾跑过则 >0；此处仅断言字段存在）
    assert "rd_workflow_runs" in data


def test_results_publish_packages_endpoint(client_with_content_run):
    resp = client_with_content_run.get(
        "/api/results/publish-packages?limit=50", headers={"X-Tenant-Id": DEFAULT_TENANT}
    )
    assert resp.status_code == 200, resp.text
    pkgs = resp.json()["publish_packages"]
    assert len(pkgs) >= 1
    assert pkgs[0]["source_workflow"].startswith("wl_ai_content_")


def test_results_content_workflow_runs_endpoint(client_with_content_run):
    resp = client_with_content_run.get(
        "/api/results/content-workflow-runs?limit=50", headers={"X-Tenant-Id": DEFAULT_TENANT}
    )
    assert resp.status_code == 200, resp.text
    runs = resp.json()["runs"]
    assert len(runs) >= 1
    assert runs[0]["status"] == "completed"
