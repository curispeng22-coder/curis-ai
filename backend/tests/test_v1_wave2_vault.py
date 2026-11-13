"""Wave 2 验证项 2（V1 单账号 Vault 读写）。

覆盖：
- 进程内：POST /api/credential 写入平台 cookie + 自有 AI key →
  GET /api/credential list 含新凭证 → resolve 还原明文。
- 安全红线：库内 credential_metadata 仅存 digest/metadata，不存明文 cookie/key
  （直接 grep 库行验证，并断言 encrypted_metadata 不含明文）。
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

os.environ.setdefault("CURIS_CONNECTOR_MODE", "mock")

from app.credential_vault import CredentialVaultService  # noqa: E402
from app.database import Database  # noqa: E402
from app.evolution_event_log import EvolutionEventLog  # noqa: E402
from app.main import create_app  # noqa: E402
from app.tenant_context import DEFAULT_TENANT  # noqa: E402

import pytest  # noqa: E402


def test_vault_create_list_resolve_in_process(seeded_db):
    """进程内：create → list 含新凭证 → resolve 还原明文。"""
    db = Database(seeded_db)
    db.initialize()
    event_log = EvolutionEventLog(db)
    vault = CredentialVaultService(db, event_log)

    cred = vault.create(
        name="抖音主号 cookie",
        provider="social_platform_douyin",
        credential_type="cookie",
        secret="sessionid=abc123; uid=42",
    )
    ref = cred["credential_ref"]
    # 引用含 selfuse 租户段
    assert "/tenant/selfuse/credential/" in ref, ref

    listed = vault.list()["credentials"]
    assert any(c["credential_id"] == cred["credential_id"] for c in listed)

    resolved = vault.resolve(ref)["secret"]
    assert resolved == "sessionid=abc123; uid=42"


def test_vault_no_plaintext_in_db(seeded_db):
    """安全红线：库内只存 digest/metadata，不存明文 cookie。"""
    db = Database(seeded_db)
    db.initialize()
    event_log = EvolutionEventLog(db)
    vault = CredentialVaultService(db, event_log)

    secret = "sessionid=SECRETCOOKIE123; uid=999"
    cred = vault.create(
        name="抖音主号 cookie",
        provider="social_platform_douyin",
        credential_type="cookie",
        secret=secret,
    )
    row = db.get_credential_metadata(DEFAULT_TENANT, cred["credential_id"])
    raw = str(row)
    # 明文 cookie 绝不落库
    assert "SECRETCOOKIE123" not in raw, "库内发现明文 cookie"
    # metadata 只含后端标识 + secret_digest，不含原值
    enc = row["encrypted_metadata"]
    assert "secret_digest" in enc
    assert "SECRETCOOKIE123" not in str(enc)
    # 返回给调用方的 safe 视图也不含 secret
    from app.credential_vault import safe_credential_metadata
    safe = safe_credential_metadata(row)
    assert "secret" not in safe
    assert "SECRETCOOKIE123" not in str(safe)


def test_vault_http_endpoints(seeded_db):
    """HTTP：POST /api/credential → GET /api/credential 含新凭证 →
    GET /api/credential/{id} 返回安全元数据（无明文）。"""
    app = create_app(db_path=seeded_db)
    from fastapi.testclient import TestClient

    client = TestClient(app)
    headers = {"X-Tenant-Id": DEFAULT_TENANT}

    resp = client.post(
        "/api/credential",
        headers={**headers, "Content-Type": "application/json"},
        json={"name": "自有 AI key", "provider": "model_gateway",
              "credential_type": "api_key", "secret": "sk-REALKEY987"},
    )
    assert resp.status_code == 201, resp.text
    body = resp.json()
    assert "/tenant/selfuse/credential/" in body["credential_ref"]

    lst = client.get("/api/credential", headers=headers)
    assert lst.status_code == 200
    assert any(c["credential_id"] == body["credential_id"] for c in lst.json()["credentials"])

    detail = client.get(f"/api/credential/{body['credential_id']}", headers=headers)
    assert detail.status_code == 200
    assert "sk-REALKEY987" not in str(detail.json())
    # 测试端点可跑通（local-dev 内存持有明文）
    t = client.post(f"/api/credential/{body['credential_id']}/test", headers=headers)
    assert t.status_code == 200 and t.json().get("status") == "ok"
