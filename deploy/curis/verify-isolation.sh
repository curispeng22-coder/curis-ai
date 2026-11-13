#!/usr/bin/env bash
set -euo pipefail

check() {
  local name="$1" url="$2" expected="$3" actual
  actual=$(curl -sS -o /dev/null -w '%{http_code}' "$url")
  [ "$actual" = "$expected" ] || { echo "FAIL $name: expected $expected, got $actual"; exit 1; }
  echo "OK   $name: $actual"
}

if [ "${CURIS_EGRESS_VERIFY:-0}" = "1" ]; then
  workspace="${CURIS_WORKSPACE_CONTAINER:-gateway-workspace-1}"
  docker exec "$workspace" sh -c '! env | grep -Eq "^(HTTP|HTTPS|ALL)_PROXY="'
  docker exec "$workspace" getent hosts api.openai.com >/dev/null
  ! docker exec "$workspace" getent hosts example.com >/dev/null 2>&1
  docker exec -i "$workspace" python - <<'PY'
import socket
import ssl


def allowed_tls():
    with socket.create_connection(("api.openai.com", 443), timeout=5) as raw:
        with ssl.create_default_context().wrap_socket(raw, server_hostname="api.openai.com"):
            pass


def rejected(host, port, server_name=None):
    try:
        with socket.create_connection((host, port), timeout=3) as raw:
            if server_name:
                with ssl.create_default_context().wrap_socket(raw, server_hostname=server_name):
                    pass
    except (OSError, ssl.SSLError):
        return
    raise SystemExit(f"unexpected egress: {host}:{port} sni={server_name or '-'}")


allowed_tls()
rejected("api.openai.com", 443, "example.com")
rejected("api.openai.com", 8443)
rejected("1.1.1.1", 443)
PY
  echo "Controlled api.openai.com:443 DNS/SNI egress checks passed."
  exit 0
fi

if [ "${CURIS_L2_VERIFY:-0}" = "1" ]; then
  : "${CURIS_MEMBER_TOKEN:?CURIS_MEMBER_TOKEN is required}"
  : "${CURIS_CROSS_TENANT_COMPANY_ID:?CURIS_CROSS_TENANT_COMPANY_ID is required}"
  GW="${CURIS_GATEWAY_URL:-http://127.0.0.1:8080}"
  APP="${CURIS_WORKSPACE_DIRECT_URL:-http://127.0.0.1:8002}"
  TENANT_A="${CURIS_MEMBER_TENANT:-tenant-a}"
  TENANT_B="${CURIS_NONMEMBER_TENANT:-tenant-b}"

  check "Gateway health" "$GW/health" 200
  check "Gateway requires token" "$GW/api/workspace/companies" 401
  actual=$(curl -sS -o /dev/null -w '%{http_code}' -H 'Authorization: Bearer invalid' "$GW/api/workspace/companies")
  [ "$actual" = 401 ] || { echo "FAIL invalid token: $actual"; exit 1; }
  actual=$(curl -sS -o /dev/null -w '%{http_code}' -H 'X-Curis-Gateway-Subject: forged' -H "X-Tenant-Id: $TENANT_A" "$GW/api/workspace/companies")
  [ "$actual" = 401 ] || { echo "FAIL forged identity header: $actual"; exit 1; }
  actual=$(curl -sS -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $CURIS_MEMBER_TOKEN" -H "X-Tenant-Id: $TENANT_A" "$GW/api/workspace/companies")
  [ "$actual" = 200 ] || { echo "FAIL active membership: $actual"; exit 1; }
  actual=$(curl -sS -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $CURIS_MEMBER_TOKEN" -H "X-Tenant-Id: $TENANT_B" "$GW/api/workspace/companies")
  [ "$actual" = 403 ] || { echo "FAIL nonmember tenant: $actual"; exit 1; }
  actual=$(curl -sS -o /dev/null -w '%{http_code}' -H "Authorization: Bearer $CURIS_MEMBER_TOKEN" -H "X-Tenant-Id: $TENANT_A" "$GW/api/workspace/companies/$CURIS_CROSS_TENANT_COMPANY_ID")
  [ "$actual" = 404 ] || { echo "FAIL cross-tenant resource: $actual"; exit 1; }
  if curl -fsS --connect-timeout 2 "$APP/health" >/dev/null 2>&1; then
    echo "FAIL Workspace direct port is reachable"
    exit 1
  fi
  echo "Trusted gateway isolation checks passed."
  exit 0
fi

check "Admin health" "http://127.0.0.1:8001/health" 200
check "Workspace health" "http://127.0.0.1:8002/health" 200
check "Admin frontend" "http://127.0.0.1:3100/platform" 200
check "Workspace frontend" "http://127.0.0.1:3000/" 200
check "Admin rejects Workspace API" "http://127.0.0.1:8001/api/workspace/companies" 404
check "Workspace rejects Admin API" "http://127.0.0.1:8002/api/platform/tenants" 404

echo "Isolation checks passed."
