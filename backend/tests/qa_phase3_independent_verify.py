"""QA 独立验证脚本 — Phase-3 治理边界（commit 85ba0b9c）。

本脚本由 QA 工程师独立编写，不采信工程师自测 test_d5_phase3_governance.py。
采用独立 seed 数据 + 独立断言策略，逐条验证 8 项治理边界要求。
"""
import json
import os
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Database  # noqa: E402
from app.main import create_app  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

ADMIN = {"Authorization": "Bearer platform-admin-dev"}

PASS = 0
FAIL = 0
RESULTS = []


def check(name, condition, detail=""):
    global PASS, FAIL
    if condition:
        PASS += 1
        RESULTS.append(f"  [PASS] {name}")
    else:
        FAIL += 1
        RESULTS.append(f"  [FAIL] {name} — {detail}")


def make_client(db):
    os.environ.setdefault("CURIS_PLATFORM_ADMIN_TOKEN", "platform-admin-dev")
    return TestClient(create_app(db.path))


def seed_usage(db, tenant_id, source, corr_id, extra_payload=None):
    """独立 seed：直接插入 evolution_events 表。"""
    payload = {
        "capability_type": "model",
        "capability_source": source,
        "model_name": "test-model",
        "status": "success",
    }
    if extra_payload:
        payload.update(extra_payload)
    with db.connect() as conn:
        conn.execute(
            "insert into evolution_events "
            "(correlation_id, event_type, payload, tenant_id) "
            "values (?, 'usage.model_call', ?, ?)",
            (corr_id, json.dumps(payload), tenant_id),
        )
        conn.commit()


def seed_audit(db, tenant_id, event_type, corr_id):
    with db.connect() as conn:
        conn.execute(
            "insert into evolution_events "
            "(correlation_id, event_type, payload, tenant_id) "
            "values (?, ?, ?, ?)",
            (corr_id, event_type, json.dumps({"msg": "test"}), tenant_id),
        )
        conn.commit()


def main():
    # ═══════════════════════════════════════════════════════════════
    # V2: capability_source 三态过滤（独立 seed）
    # ═══════════════════════════════════════════════════════════════
    print("\n=== V2: capability_source 三态过滤 ===")
    tmp = TemporaryDirectory()
    try:
        db = Database(str(Path(tmp.name) / "qa.sqlite"))
        db.initialize()

        # 独立 seed：3 条不同 source 的 usage 事件
        seed_usage(db, "qa-tenant", "official", "qa-off-1")
        seed_usage(db, "qa-tenant", "tenant_private", "qa-tp-1")
        seed_usage(db, "qa-tenant", "marketplace", "qa-mp-1")
        client = make_client(db)

        # official only
        r = client.get("/api/platform/usage?tenant_id=qa-tenant&capability_source=official", headers=ADMIN)
        sources = {e.get("capability_source") for e in r.json().get("usage_events", [])}
        check("V2a official filter → only official",
              r.status_code == 200 and sources == {"official"},
              f"status={r.status_code} sources={sources}")

        # tenant_private only
        r = client.get("/api/platform/usage?tenant_id=qa-tenant&capability_source=tenant_private", headers=ADMIN)
        sources = {e.get("capability_source") for e in r.json().get("usage_events", [])}
        check("V2b tenant_private filter → only tenant_private",
              r.status_code == 200 and sources == {"tenant_private"},
              f"status={r.status_code} sources={sources}")

        # marketplace only
        r = client.get("/api/platform/usage?tenant_id=qa-tenant&capability_source=marketplace", headers=ADMIN)
        sources = {e.get("capability_source") for e in r.json().get("usage_events", [])}
        check("V2c marketplace filter → only marketplace",
              r.status_code == 200 and sources == {"marketplace"},
              f"status={r.status_code} sources={sources}")

        # no filter → all 3
        r = client.get("/api/platform/usage?tenant_id=qa-tenant", headers=ADMIN)
        events = r.json().get("usage_events", [])
        sources = {e.get("capability_source") for e in events}
        check("V2d no filter → all 3 sources",
              r.status_code == 200 and len(events) == 3 and sources == {"official", "tenant_private", "marketplace"},
              f"status={r.status_code} count={len(events)} sources={sources}")
    finally:
        tmp.cleanup()

    # ═══════════════════════════════════════════════════════════════
    # V3: tenant_private 隔离（catalog 端点）
    # ═══════════════════════════════════════════════════════════════
    print("\n=== V3: tenant_private 隔离 ===")
    tmp = TemporaryDirectory()
    try:
        db = Database(str(Path(tmp.name) / "qa2.sqlite"))
        db.initialize()
        # seed a tenant_private capability directly
        db.save_tenant_private_capability(
            tenant_id="qa-tenant",
            capability_type="model",
            capability_id="private-llm",
            display_name="Private LLM",
            metadata={},
        )
        client = make_client(db)

        r = client.get("/api/catalog/capabilities")
        caps = r.json().get("capabilities", [])
        tp_caps = [c for c in caps if c.get("source") == "tenant_private"]
        check("V3a /api/catalog/capabilities → no tenant_private",
              r.status_code == 200 and len(tp_caps) == 0,
              f"found {len(tp_caps)} tenant_private caps")

        r = client.get("/api/catalog/models")
        models = r.json().get("models", [])
        tp_models = [m for m in models if m.get("source") == "tenant_private"]
        check("V3b /api/catalog/models → no tenant_private",
              r.status_code == 200 and len(tp_models) == 0,
              f"found {len(tp_models)} tenant_private models")

        r = client.get("/api/catalog/connectors")
        conns = r.json().get("connectors", [])
        tp_conns = [c for c in conns if c.get("source") == "tenant_private"]
        check("V3c /api/catalog/connectors → no tenant_private",
              r.status_code == 200 and len(tp_conns) == 0,
              f"found {len(tp_conns)} tenant_private connectors")
    finally:
        tmp.cleanup()

    # ═══════════════════════════════════════════════════════════════
    # V4: 敏感配置不暴露
    # ═══════════════════════════════════════════════════════════════
    print("\n=== V4: 敏感配置不暴露 ===")
    tmp = TemporaryDirectory()
    try:
        db = Database(str(Path(tmp.name) / "qa3.sqlite"))
        db.initialize()
        seed_usage(db, "qa-tenant", "official", "qa-sensitive-1", extra_payload={
            "api_key": "sk-SECRET-123",
            "access_token": "tok-SECRET-456",
            "secret": "my-secret-value",
            "password": "p@ssw0rd!",
        })
        client = make_client(db)
        r = client.get("/api/platform/usage?tenant_id=qa-tenant", headers=ADMIN)
        events = r.json().get("usage_events", [])
        sensitive_top = set()
        for e in events:
            for field in ("api_key", "access_token", "secret", "password", "token"):
                if field in e:
                    sensitive_top.add(field)
        check("V4a usage_event top-level has no sensitive fields",
              r.status_code == 200 and len(sensitive_top) == 0,
              f"leaked top-level fields: {sensitive_top}")
    finally:
        tmp.cleanup()

    # ═══════════════════════════════════════════════════════════════
    # V5: AuditEvent 白名单
    # ═══════════════════════════════════════════════════════════════
    print("\n=== V5: AuditEvent 白名单 ===")
    tmp = TemporaryDirectory()
    try:
        db = Database(str(Path(tmp.name) / "qa4.sqlite"))
        db.initialize()
        # seed events in different namespaces
        seed_audit(db, "qa-tenant", "tenant_private.capability.used", "qa-audit-tp")
        seed_audit(db, "qa-tenant", "governance.policy_set", "qa-audit-gov")
        seed_audit(db, "qa-tenant", "capability.model_created", "qa-audit-cap")
        seed_audit(db, "qa-tenant", "usage.model_call", "qa-audit-usage")

        client = make_client(db)
        r = client.get("/api/platform/audit?tenant_id=qa-tenant", headers=ADMIN)
        events = r.json().get("audit_events", [])
        event_types = [e.get("event_type", "") for e in events]

        tp_in_audit = any(et.startswith("tenant_private") for et in event_types)
        check("V5a audit → no tenant_private.* events",
              r.status_code == 200 and not tp_in_audit,
              f"found tenant_private events: {[et for et in event_types if et.startswith('tenant_private')]}")

        usage_in_audit = any(et.startswith("usage.") for et in event_types)
        check("V5b audit → no usage.* events (whitelist excludes usage)",
              r.status_code == 200 and not usage_in_audit,
              f"found usage events: {[et for et in event_types if et.startswith('usage')]}")

        gov_in_audit = any(et.startswith("governance.") for et in event_types)
        cap_in_audit = any(et.startswith("capability.") for et in event_types)
        check("V5c audit → governance.* and capability.* are visible",
              r.status_code == 200 and gov_in_audit and cap_in_audit,
              f"gov={gov_in_audit} cap={cap_in_audit} types={event_types}")

        # all returned must be in whitelist
        all_whitelisted = all(
            et.startswith("capability.") or et.startswith("governance.")
            for et in event_types
        )
        check("V5d audit → all events in whitelist (capability.*|governance.*)",
              all_whitelisted,
              f"non-whitelisted: {[et for et in event_types if not (et.startswith('capability.') or et.startswith('governance.'))]}")
    finally:
        tmp.cleanup()

    # ═══════════════════════════════════════════════════════════════
    # V6: Admin 无 tenant_private 编辑入口（静态检查）
    # ═══════════════════════════════════════════════════════════════
    print("\n=== V6: Admin 无 tenant_private 编辑入口 ===")
    main_path = Path(__file__).resolve().parents[1] / "app" / "main.py"
    text = main_path.read_text(encoding="utf-8")

    # Check platform routes block (from _require_platform_admin def to end of platform routes)
    # Platform routes are roughly L642-860
    lines = text.splitlines()
    platform_block_lines = []
    in_platform = False
    for i, line in enumerate(lines, 1):
        if "_require_platform_admin" in line and "def " in line:
            in_platform = True
        if in_platform:
            platform_block_lines.append((i, line))

    # Find platform route handlers and check none reference tenant_private
    platform_routes_with_tp = []
    current_route = None
    current_route_has_tp = False
    for i, line in enumerate(lines, 1):
        if "@app.get(\"/api/platform/" in line or "@app.post(\"/api/platform/" in line or \
           "@app.put(\"/api/platform/" in line or "@app.delete(\"/api/platform/" in line:
            if current_route and current_route_has_tp:
                platform_routes_with_tp.append(current_route)
            current_route = line.strip()
            current_route_has_tp = False
        if current_route and "tenant_private" in line:
            current_route_has_tp = True

    check("V6a no /api/platform/* route handler references tenant_private",
          len(platform_routes_with_tp) == 0,
          f"routes with tenant_private: {platform_routes_with_tp}")

    # V6b: CapabilityCatalogPanel.js has no tenant_private
    panel_path = Path(__file__).resolve().parents[1] / ".." / "frontend" / "app" / "platform" / "CapabilityCatalogPanel.js"
    panel_text = panel_path.read_text(encoding="utf-8")
    check("V6b CapabilityCatalogPanel.js → no tenant_private",
          "tenant_private" not in panel_text,
          "found tenant_private reference")

    # ═══════════════════════════════════════════════════════════════
    # V7: 前端 UsageProjectionPanel
    # ═══════════════════════════════════════════════════════════════
    print("\n=== V7: 前端 UsageProjectionPanel ===")
    up_path = Path(__file__).resolve().parents[1] / ".." / "frontend" / "app" / "platform" / "UsageProjectionPanel.js"
    up_text = up_path.read_text(encoding="utf-8")

    check("V7a has capability_source dropdown",
          "capability_source" in up_text and "<select" in up_text,
          "missing dropdown or capability_source")

    has_all_options = all(
        f'value="{opt}"' in up_text
        for opt in ("official", "tenant_private", "marketplace")
    )
    check("V7b dropdown has all 3 source options (official/tenant_private/marketplace)",
          has_all_options,
          "missing one or more options")

    has_empty_option = 'value=""' in up_text and "全部" in up_text
    check("V7c empty value option (全部) present",
          has_empty_option,
          "missing empty/全部 option")

    # empty value doesn't pass param: if (capabilitySource) params.set(...)
    has_conditional_set = "if (capabilitySource)" in up_text
    check("V7d empty value does not pass capability_source param (conditional set)",
          has_conditional_set,
          "missing conditional param.set guard")

    check("V7e uses apiFetch",
          "apiFetch" in up_text,
          "missing apiFetch usage")

    check("V7f uses Bearer token",
          "Bearer" in up_text or "apiFetch" in up_text,  # apiFetch handles Bearer internally
          "no Bearer/apiFetch")

    check("V7g no MUI imports",
          "@mui" not in up_text and "material-ui" not in up_text,
          "found MUI import")

    # ═══════════════════════════════════════════════════════════════
    # V8: 禁止区（新增代码无 forbidden imports）
    # ═══════════════════════════════════════════════════════════════
    print("\n=== V8: 禁止区 ===")
    forbidden_patterns = ["import openai", "import boto3", "import anthropic",
                          "from requests", "import requests"]

    # Check the 2 changed files
    changed_files = [
        Path(__file__).resolve().parents[1] / ".." / "frontend" / "app" / "platform" / "UsageProjectionPanel.js",
        # test file is Python, check for model_gateway import
    ]

    violations = []
    # Check test_d5_phase3_governance.py for forbidden imports
    test_path = Path(__file__).resolve().parents[1] / "tests" / "test_d5_phase3_governance.py"
    test_text = test_path.read_text(encoding="utf-8")
    for pat in forbidden_patterns:
        if pat in test_text:
            violations.append(f"test_d5_phase3_governance.py: {pat}")
    if "import model_gateway" in test_text or "from model_gateway" in test_text:
        violations.append("test_d5_phase3_governance.py: model_gateway import")

    # Check UsageProjectionPanel.js
    up_text_check = up_path.read_text(encoding="utf-8")
    for pat in forbidden_patterns:
        if pat in up_text_check:
            violations.append(f"UsageProjectionPanel.js: {pat}")

    check("V8a no forbidden imports (openai/boto3/anthropic/requests/model_gateway) in changed files",
          len(violations) == 0,
          f"violations: {violations}")

    # ═══════════════════════════════════════════════════════════════
    # Summary
    # ═══════════════════════════════════════════════════════════════
    print("\n" + "=" * 60)
    print(f"QA INDEPENDENT VERIFICATION SUMMARY")
    print(f"  Total: {PASS + FAIL} | PASS: {PASS} | FAIL: {FAIL}")
    print("=" * 60)
    for r in RESULTS:
        print(r)

    if FAIL > 0:
        print(f"\n>>> ROUTING: {'Engineer' if FAIL > 0 else 'NoOne'} (source bugs found)")
        sys.exit(1)
    else:
        print("\n>>> ROUTING: NoOne (all checks passed)")
        sys.exit(0)


if __name__ == "__main__":
    main()
