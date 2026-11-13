# Phase-5 G2 Credential Vault Demo Script

Status: Deprecated

Date: 2026-07-09

Demo status: local/demo only.

## Demo Defaults

- `tenant_id`: `default`
- `ceo_id`: `local-demo-ceo`
- Backend URL: `http://127.0.0.1:8000`
- Frontend URL: `http://127.0.0.1:3000`
- Local model gateway URL: `http://127.0.0.1:18080`
- Admin token: `platform-admin-dev`
- Demo credential value: `demo-local-credential-value`

The demo credential value is a local-only fake value. Do not use real provider keys.

## Start Local Model Gateway

Start a local OpenAI-compatible demo gateway:

```bash
python3 - <<'PY'
from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("content-length", "0"))
        body = self.rfile.read(length)
        try:
            payload = json.loads(body.decode() or "{}")
        except Exception:
            payload = {}
        response = {
            "id": "chatcmpl-phase5-demo",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Phase-5 credential resolver demo result"
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 13,
                "completion_tokens": 7,
                "total_tokens": 20,
                "estimated_cost": 0.00002,
            },
            "model": payload.get("model") or "phase5-demo-private-model",
        }
        data = json.dumps(response).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format, *args):
        print(format % args)

HTTPServer(("127.0.0.1", 18080), Handler).serve_forever()
PY
```

## Start Backend

```bash
cd "/Users/yy/Documents/Curis AI Workspace/backend"
CURIS_ENV=local \
CURIS_DB=/tmp/curis_phase5_g2_demo.sqlite \
CURIS_MODEL_GATEWAY_BASE_URL=http://127.0.0.1:18080 \
CURIS_MODEL_GATEWAY_API_KEY=env:FALLBACK_ONLY \
CURIS_MODEL_GATEWAY_MODEL=phase5-demo-fallback-model \
CURIS_MODEL_GATEWAY_ESTIMATED_COST_PER_1K_TOKENS=0.001 \
./.venv/bin/python -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000
```

## Start Frontend

```bash
cd "/Users/yy/Documents/Curis AI Workspace/frontend"
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000 \
NEXT_PUBLIC_CURIS_TENANT_ID=default \
NEXT_PUBLIC_CURIS_CEO_ID=local-demo-ceo \
npm run dev -- --hostname 127.0.0.1 --port 3000
```

Open Workspace:

```text
http://127.0.0.1:3000
```

## Create tenant_private Credential

Create the credential:

```bash
curl -sS -X POST "http://127.0.0.1:8000/api/workspace/credentials" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d '{
    "name": "Phase-5 Demo Credential",
    "provider": "newapi",
    "credential_type": "api_key",
    "secret": "demo-local-credential-value"
  }' | tee /tmp/phase5_credential.json | python3 -m json.tool
```

Verify API response does not return plaintext:

```bash
! rg -n "demo-local-credential-value" /tmp/phase5_credential.json
```

Export `credential_ref` and `credential_id`:

```bash
export CREDENTIAL_REF="$(python3 -c 'import json; print(json.load(open("/tmp/phase5_credential.json"))["credential_ref"])')"
export CREDENTIAL_ID="$(python3 -c 'import json; print(json.load(open("/tmp/phase5_credential.json"))["credential_id"])')"
echo "$CREDENTIAL_REF"
```

Expected format:

```text
local-dev://tenant/default/credential/{credential_id}
```

## Create Private Capabilities

Create private model without storing plaintext:

```bash
curl -sS -X POST "http://127.0.0.1:8000/api/workspace/private-models" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d '{
    "name": "phase5-private-model",
    "provider_type": "newapi",
    "base_url": "http://127.0.0.1:18080",
    "model_name": "phase5-demo-private-model",
    "credential_ref": "",
    "enabled": true
  }' | python3 -m json.tool
```

Create private tool:

```bash
curl -sS -X POST "http://127.0.0.1:8000/api/workspace/private-tools" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d '{
    "name": "phase5-private-tool",
    "type": "llm_tool",
    "description": "Phase-5 demo private tool",
    "config_ref": "",
    "enabled": true
  }' | python3 -m json.tool
```

Create private connector:

```bash
curl -sS -X POST "http://127.0.0.1:8000/api/workspace/private-connectors" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d '{
    "name": "phase5-private-connector",
    "connector_type": "crm",
    "config_ref": "",
    "enabled": true
  }' | python3 -m json.tool
```

## Bind credential_ref To Private Capabilities

Bind private model:

```bash
curl -sS -X PUT "http://127.0.0.1:8000/api/workspace/private-capabilities/model/phase5-private-model/credential" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d "{\"credential_ref\":\"$CREDENTIAL_REF\"}" | python3 -m json.tool
```

Bind private tool:

```bash
curl -sS -X PUT "http://127.0.0.1:8000/api/workspace/private-capabilities/tool/phase5-private-tool/credential" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d "{\"credential_ref\":\"$CREDENTIAL_REF\"}" | python3 -m json.tool
```

Bind private connector:

```bash
curl -sS -X PUT "http://127.0.0.1:8000/api/workspace/private-capabilities/connector/phase5-private-connector/credential" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d "{\"credential_ref\":\"$CREDENTIAL_REF\"}" | python3 -m json.tool
```

Verify bound responses do not show plaintext:

```bash
curl -sS -H "X-Tenant-Id: default" "http://127.0.0.1:8000/api/workspace/private-models" \
  | tee /tmp/phase5_private_models.json | python3 -m json.tool
! rg -n "demo-local-credential-value" /tmp/phase5_private_models.json
```

## Create Or Select R&D Employee

Create Software R&D department:

```bash
curl -sS -X POST "http://127.0.0.1:8000/api/workspace/departments" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d '{
    "template_id": "official.department.software_rnd",
    "name": "Phase-5 Demo R&D",
    "company_id": "local-demo-company",
    "enabled_employee_template_ids": ["official.employee.tech_lead"],
    "enabled": true
  }' | tee /tmp/phase5_department.json | python3 -m json.tool
```

Create Tech Lead employee:

```bash
export DEPARTMENT_ID="$(python3 -c 'import json; print(json.load(open("/tmp/phase5_department.json"))["id"])')"

curl -sS -X POST "http://127.0.0.1:8000/api/workspace/employees" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d "{
    \"department_id\": \"$DEPARTMENT_ID\",
    \"template_id\": \"official.employee.tech_lead\",
    \"name\": \"Phase-5 Demo Tech Lead\",
    \"company_id\": \"local-demo-company\",
    \"instructions_override\": \"Use tenant private model via resolver; never expose secrets.\",
    \"status\": \"idle\",
    \"enabled\": true
  }" | tee /tmp/phase5_employee.json | python3 -m json.tool
```

Bind the private model capability to the employee:

```bash
export EMPLOYEE_ID="$(python3 -c 'import json; print(json.load(open("/tmp/phase5_employee.json"))["id"])')"

curl -sS -X PUT "http://127.0.0.1:8000/api/workspace/employees/$EMPLOYEE_ID/capabilities" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d '{
    "bindings": [
      {
        "capability_source": "tenant_private",
        "capability_type": "model",
        "capability_id": "phase5-private-model",
        "priority": 1,
        "enabled": true
      }
    ]
  }' | python3 -m json.tool
```

## Execute Employee Task

Create the task and select employee:

```bash
curl -sS -X POST "http://127.0.0.1:8000/api/task" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d "{
    \"content\": \"Run Phase-5 credential resolver demo task\",
    \"employee_id\": \"$EMPLOYEE_ID\"
  }" | tee /tmp/phase5_task.json | python3 -m json.tool
```

Run the task:

```bash
export TASK_ID="$(python3 -c 'import json; print(json.load(open("/tmp/phase5_task.json"))["task_id"])')"

curl -sS -X POST "http://127.0.0.1:8000/api/task/$TASK_ID/run" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" | tee /tmp/phase5_task_result.json | python3 -m json.tool
```

Confirm task result:

```bash
python3 -c 'import json; p=json.load(open("/tmp/phase5_task_result.json")); print(p["status"], p["employee_role"], p["output"])'
```

Expected:

```text
COMPLETED tech_lead Phase-5 credential resolver demo result
```

## View usage_event Redacted Attribution

```bash
curl -sS \
  -H "Authorization: Bearer platform-admin-dev" \
  "http://127.0.0.1:8000/api/platform/usage?tenant_id=default&capability_source=tenant_private" \
  | tee /tmp/phase5_usage.json | python3 -m json.tool
```

Confirm usage_event contains credential attribution but no plaintext:

```bash
python3 - <<'PY'
import json
p = json.load(open("/tmp/phase5_usage.json"))
event = next(e for e in p["usage_events"] if e["event_type"] == "usage.model_call")
print({
    "tenant_id": event["tenant_id"],
    "task_id": event["task_id"],
    "employee_role": event["employee_role"],
    "capability_source": event["capability_source"],
    "capability_type": event["capability_type"],
    "capability_id": event["capability_id"],
    "credential_id": event["credential_id"],
    "credential_ref_digest": event["credential_ref_digest"],
    "status": event["status"],
})
PY
! rg -n "demo-local-credential-value" /tmp/phase5_usage.json
```

## View audit_event Redacted Audit

```bash
curl -sS \
  -H "Authorization: Bearer platform-admin-dev" \
  "http://127.0.0.1:8000/api/platform/audit?tenant_id=default&event_type=credential.resolved" \
  | tee /tmp/phase5_audit.json | python3 -m json.tool
```

Confirm audit_event contains only redacted metadata:

```bash
python3 - <<'PY'
import json
p = json.load(open("/tmp/phase5_audit.json"))
payload = json.loads(p["audit_events"][0]["payload"])
print(payload.keys())
print(payload)
PY
! rg -n "demo-local-credential-value" /tmp/phase5_audit.json
```

Allowed audit payload keys:

```text
tenant_id, credential_id, credential_ref_digest, actor_id, action, status, reason, timestamp
```

## Verify Admin Cannot See Plaintext

Run:

```bash
! rg -n "demo-local-credential-value" /tmp/phase5_credential.json /tmp/phase5_private_models.json /tmp/phase5_usage.json /tmp/phase5_audit.json
```

Expected:

```text
no matches
```

## Screenshot Checklist

Capture these artifacts for the demo packet:

- tenant_private credential creation API response or future credential page.
- credential_ref display or binding response.
- private model / tool / connector credential_ref binding response.
- Workspace employee capability binding section.
- Workspace employee task execution.
- Workspace task result page.
- Admin usage_event redacted attribution.
- Admin audit_event redacted audit.

## Stop Local Services

Stop each terminal with `Ctrl+C`.

The demo SQLite DB is `/tmp/curis_phase5_g2_demo.sqlite`; delete it for a fresh demo.
