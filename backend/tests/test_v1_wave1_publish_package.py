"""Wave-1 验收：验证项 3（发布包 schema + /api/publish-package/export）。

运行方式（在 backend/ 目录下，使用项目 .venv）：
    ../.venv/bin/python -m pytest tests/test_v1_wave1_publish_package.py -v

覆盖：
- 合法载荷 → 200 且 to_markdown() 产出非空可读。
- 坏 source_workflow / 空 artifacts / 坏 artifact.type → 422，无 500 崩溃。
- ContentPublishPackage pydantic 校验真实生效（单测）。
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
sys.path.insert(0, str(Path(__file__).resolve().parent))  # 使 v1_wave1_helpers 可导入

from fastapi.testclient import TestClient
import pytest
from pydantic import ValidationError

from app.content_publish_package import (
    ARTIFACT_TYPES,
    ContentArtifact,
    ContentPublishPackage,
    PublishPackageError,
)
from app.main import create_app

from v1_wave1_helpers import TENANT, seed_wave1_full

VALID_ARTIFACT = {"type": "copywriting", "title": "春季护肤标题", "body": "误区一……"}
VALID_PAYLOAD = {
    "source_workflow": "wl_ai_content_content_production_sop",
    "artifacts": [VALID_ARTIFACT],
    "brand_voice_ref": "skl_ai_content_brand_voice",
    "platforms_targeted": ["xhs", "douyin"],
}


@pytest.fixture
def client(tmp_path):
    db = str(tmp_path / "curis.sqlite")
    seed_wave1_full(db)
    app = create_app(db)
    return TestClient(app)


def test_export_valid_returns_200_and_markdown(client):
    r = client.post(
        "/api/publish-package/export",
        json=VALID_PAYLOAD,
        headers={"X-Tenant-Id": TENANT},
    )
    assert r.status_code == 200
    body = r.json()
    assert body["package"]["source_workflow"] == "wl_ai_content_content_production_sop"
    md = body["markdown"]
    assert isinstance(md, str) and len(md) > 0
    # 可读：包含来源工作流与工件标题
    assert "wl_ai_content_content_production_sop" in md
    assert "春季护肤标题" in md
    # JSON 契约同样可用
    assert isinstance(body["json"], str) and len(body["json"]) > 0


def test_export_bad_source_workflow_422(client):
    payload = dict(VALID_PAYLOAD)
    payload["source_workflow"] = "wl_ai_rd_not_content"  # 不命中 ^wl_ai_content_*
    r = client.post(
        "/api/publish-package/export",
        json=payload,
        headers={"X-Tenant-Id": TENANT},
    )
    assert r.status_code == 422


def test_export_empty_artifacts_422(client):
    payload = dict(VALID_PAYLOAD)
    payload["artifacts"] = []
    r = client.post(
        "/api/publish-package/export",
        json=payload,
        headers={"X-Tenant-Id": TENANT},
    )
    assert r.status_code == 422


def test_export_bad_artifact_type_422(client):
    payload = dict(VALID_PAYLOAD)
    payload["artifacts"] = [{"type": "video", "title": "t", "body": "b"}]  # 非法 type
    r = client.post(
        "/api/publish-package/export",
        json=payload,
        headers={"X-Tenant-Id": TENANT},
    )
    assert r.status_code == 422


def test_export_no_500_on_malformed_artifacts(client):
    # 结构性畸形 artifacts（非 list / 非 dict 元素）应被校验 422 吞掉，绝不 500。
    # 注意：单条 artifact 缺 type 字段是合法的（默认 copywriting），不会触发 422；
    # 因此这里用整体结构错误的载荷来验证「不 500 崩溃」。
    payload = dict(VALID_PAYLOAD)
    payload["artifacts"] = "not-a-list"
    r = client.post(
        "/api/publish-package/export",
        json=payload,
        headers={"X-Tenant-Id": TENANT},
    )
    assert r.status_code == 422
    assert r.status_code != 500


def test_schema_validators_enforced():
    """ContentPublishPackage 的 pydantic 校验真实生效（不依赖 API 层）。"""
    # 坏 source_workflow（字段校验器）→ 被 pydantic 包成 ValidationError
    with pytest.raises((PublishPackageError, ValidationError)):
        ContentPublishPackage.create(source_workflow="wl_ai_rd_bad")
    # 坏 artifact.type（字段校验器）→ ValidationError
    with pytest.raises((PublishPackageError, ValidationError)):
        ContentArtifact(type="video")
    # 空 artifacts（validated() 显式校验）→ PublishPackageError
    with pytest.raises((PublishPackageError, ValidationError)):
        ContentPublishPackage.create(
            source_workflow="wl_ai_content_content_production_sop", artifacts=[]
        )
    # 合法构造 → to_markdown 非空
    pkg = ContentPublishPackage.create(
        source_workflow="wl_ai_content_content_production_sop",
        artifacts=[ContentArtifact(type="copywriting", title="t", body="b")],
    )
    assert len(pkg.to_markdown()) > 0
    # 枚举与正则常量自洽
    assert "copywriting" in ARTIFACT_TYPES
    assert "video" not in ARTIFACT_TYPES
