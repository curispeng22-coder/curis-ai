# Phase-6 Workflow MVP Demo Script

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
- Demo credential value: `demo-phase6-workflow-key`

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
            "id": "chatcmpl-phase6-demo",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {
                        "role": "assistant",
                        "content": "Phase-6 workflow demo step result"
                    },
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 17,
                "completion_tokens": 9,
                "total_tokens": 26,
                "estimated_cost": 0.000026,
            },
            "model": payload.get("model") or "phase6-workflow-private-model",
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
CURIS_DB=/tmp/curis_phase6_workflow_demo.sqlite \
CURIS_MODEL_GATEWAY_BASE_URL=http://127.0.0.1:18080 \
CURIS_MODEL_GATEWAY_API_KEY=env:FALLBACK_ONLY \
CURIS_MODEL_GATEWAY_MODEL=phase6-demo-fallback-model \
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

## Prepare tenant_private Credential

Create a local/demo credential:

```bash
curl -sS -X POST "http://127.0.0.1:8000/api/workspace/credentials" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: default" \
  -H "X-Ceo-Id: local-demo-ceo" \
  -d '{
    "name": "Phase-6 Workflow Demo Credential",
    "provider": "newapi",
    "credential_type": "api_key",
    "secret": "demo-phase6-workflow-key"
  }' | tee /tmp/phase6_credential.json | python3 -m json.tool
```

Verify the API response does not return plaintext:

```bash
! rg -n "demo-phase6-workflow-key" /tmp/phase6_credential.json
```

Export the credential fields:

```bash
export API="http://127.0.0.1:8000"
export TENANT_ID="default"
export CEO_ID="local-demo-ceo"
export CREDENTIAL_REF="$(python3 -c 'import json; print(json.load(open("/tmp/phase6_credential.json"))["credential_ref"])')"
export CREDENTIAL_ID="$(python3 -c 'import json; print(json.load(open("/tmp/phase6_credential.json"))["credential_id"])')"
echo "$CREDENTIAL_REF"
```

Expected `credential_ref` format:

```text
local-dev://tenant/default/credential/{credential_id}
```

## Prepare tenant_private Model

Create a private model bound to `credential_ref`:

```bash
curl -sS -X POST "$API/api/workspace/private-models" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Ceo-Id: $CEO_ID" \
  -d "{
    \"name\": \"phase6-workflow-private-model\",
    \"provider_type\": \"newapi-compatible\",
    \"base_url\": \"http://127.0.0.1:18080\",
    \"model_name\": \"phase6-workflow-private-model\",
    \"credential_ref\": \"$CREDENTIAL_REF\",
    \"enabled\": true
  }" | tee /tmp/phase6_private_model.json | python3 -m json.tool
```

Verify the private model response does not return plaintext:

```bash
! rg -n "demo-phase6-workflow-key" /tmp/phase6_private_model.json
```

## Create R&D Department And Employees

Create the Software R&D department:

```bash
curl -sS -X POST "$API/api/workspace/departments" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Ceo-Id: $CEO_ID" \
  -d '{
    "template_id": "official.department.software_rnd",
    "name": "Phase-6 Demo R&D",
    "company_id": "local-demo-company",
    "enabled": true
  }' | tee /tmp/phase6_department.json | python3 -m json.tool
```

Create the six R&D employee instances:

```bash
python3 - <<'PY'
import json
import urllib.request

API = "http://127.0.0.1:8000"
TENANT_ID = "default"
CEO_ID = "local-demo-ceo"
DEPARTMENT_ID = json.load(open("/tmp/phase6_department.json"))["id"]

headers = {
    "Content-Type": "application/json",
    "X-Tenant-Id": TENANT_ID,
    "X-Ceo-Id": CEO_ID,
}

def request(method, path, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(API + path, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

templates = request("GET", "/api/workspace/employee-templates")["employee_templates"]
roles = [
    "tech_lead",
    "product_manager",
    "architect",
    "frontend_engineer",
    "backend_engineer",
    "qa_engineer",
]
template_by_role = {item["role"]: item["id"] for item in templates}
employees = {}
for role in roles:
    employee = request(
        "POST",
        "/api/workspace/employees",
        {
            "department_id": DEPARTMENT_ID,
            "template_id": template_by_role[role],
            "name": f"Phase-6 {role}",
            "company_id": "local-demo-company",
            "instructions_override": f"Use bound capability as {role}.",
            "status": "idle",
            "enabled": True,
        },
    )
    employees[role] = employee

json.dump(employees, open("/tmp/phase6_employees.json", "w"), ensure_ascii=False, indent=2)
print(json.dumps(employees, ensure_ascii=False, indent=2))
PY
```

## Bind Employee Capabilities

Bind every R&D employee to the tenant_private model capability:

```bash
python3 - <<'PY'
import json
import urllib.request

API = "http://127.0.0.1:8000"
TENANT_ID = "default"
CEO_ID = "local-demo-ceo"
employees = json.load(open("/tmp/phase6_employees.json"))
headers = {
    "Content-Type": "application/json",
    "X-Tenant-Id": TENANT_ID,
    "X-Ceo-Id": CEO_ID,
}

for role, employee in employees.items():
    payload = {
        "bindings": [
            {
                "capability_source": "tenant_private",
                "capability_type": "model",
                "capability_id": "phase6-workflow-private-model",
                "priority": 1,
                "enabled": True,
            }
        ]
    }
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{API}/api/workspace/employees/{employee['id']}/capabilities",
        data=data,
        headers=headers,
        method="PUT",
    )
    with urllib.request.urlopen(req) as response:
        print(role, response.status, response.read().decode())
PY
```

## Browser Demo Flow

In Workspace:

1. 查看研发部员工列表。
2. 查看员工 capability binding。
3. 查看 tenant_private credential_ref 已绑定到 private model。
4. 创建研发需求。
5. 启动研发 SOP workflow。
6. 查看 WorkflowRun 详情。
7. 查看每个 WorkflowStep 状态。
8. 查看每个员工 StepResult。
9. 查看 Tech Lead 最终汇总报告。

## API Demo Flow For Workflow Run

Create a Software R&D workflow run:

```bash
export DEPARTMENT_ID="$(python3 -c 'import json; print(json.load(open("/tmp/phase6_department.json"))["id"])')"

curl -sS -X POST "$API/api/workspace/workflows" \
  -H "Content-Type: application/json" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Ceo-Id: $CEO_ID" \
  -d "{
    \"workflow_template_id\": \"official.workflow.software_rnd_sop\",
    \"department_id\": \"$DEPARTMENT_ID\",
    \"name\": \"客户线索研发 SOP\",
    \"content\": \"开发一个客户线索管理页面和后端接口\"
  }" | tee /tmp/phase6_workflow.json | python3 -m json.tool
```

Execute the ordered SOP steps:

```bash
export WORKFLOW_RUN_ID="$(python3 -c 'import json; print(json.load(open("/tmp/phase6_workflow.json"))["workflow_run_id"])')"

for step in 1 2 3 4 5 6 7; do
  curl -sS -X POST "$API/api/workspace/workflows/$WORKFLOW_RUN_ID/run-next-step" \
    -H "X-Tenant-Id: $TENANT_ID" \
    -H "X-Ceo-Id: $CEO_ID" \
    | tee "/tmp/phase6_workflow_step_${step}.json" | python3 -m json.tool
done
```

Inspect the final run detail:

```bash
curl -sS "$API/api/workspace/workflows/$WORKFLOW_RUN_ID" \
  -H "X-Tenant-Id: $TENANT_ID" \
  -H "X-Ceo-Id: $CEO_ID" \
  | tee /tmp/phase6_workflow_detail.json | python3 -m json.tool
```

Expected result:

- WorkflowRun status is `succeeded`.
- Seven WorkflowSteps are completed in order.
- Seven StepResults are present.
- The final report contains the Tech Lead summary.

## Check usage_event Redacted Attribution

```bash
curl -sS "$API/api/platform/usage?tenant_id=$TENANT_ID&capability_source=tenant_private" \
  -H "Authorization: Bearer platform-admin-dev" \
  | tee /tmp/phase6_usage.json | python3 -m json.tool
```

Verify usage_event includes redacted workflow attribution:

```bash
python3 - <<'PY'
import json

events = json.load(open("/tmp/phase6_usage.json"))["usage_events"]
model_calls = [item for item in events if item.get("event_type") == "usage.model_call"]
assert model_calls, "missing model usage events"
required = [
    "tenant_id",
    "workflow_run_id",
    "workflow_step_id",
    "employee_id",
    "employee_role",
    "capability_source",
    "capability_type",
    "capability_id",
    "credential_id",
    "credential_ref_digest",
    "status",
    "created_at",
]
for item in model_calls:
    missing = [field for field in required if field not in item]
    assert not missing, f"missing fields: {missing}"
print("usage_event workflow attribution OK")
PY
```

Verify usage_event does not expose plaintext:

```bash
! rg -n "demo-phase6-workflow-key" /tmp/phase6_usage.json
```

## Check audit_event Workflow Changes

```bash
curl -sS "$API/api/platform/audit?tenant_id=$TENANT_ID&event_type=workflow.run.completed" \
  -H "Authorization: Bearer platform-admin-dev" \
  | tee /tmp/phase6_audit.json | python3 -m json.tool
```

Verify audit_event records workflow state changes without plaintext:

```bash
! rg -n "demo-phase6-workflow-key" /tmp/phase6_audit.json
```

## Verify Admin Cannot See tenant_private Plaintext

```bash
! rg -n "demo-phase6-workflow-key" \
  /tmp/phase6_credential.json \
  /tmp/phase6_private_model.json \
  /tmp/phase6_workflow_detail.json \
  /tmp/phase6_usage.json \
  /tmp/phase6_audit.json
```

Admin can observe redacted usage_event and audit_event only. Admin must not see tenant_private plaintext credential values.

## Screenshot Checklist

Capture these pages or outputs:

- 研发部员工列表。
- 员工 capability binding。
- tenant_private credential_ref 绑定。
- 创建研发需求。
- 启动研发 SOP workflow。
- WorkflowRun 详情。
- WorkflowStep 状态列表。
- StepResult 结果页。
- Tech Lead 汇总报告。
- Admin usage_event 脱敏归因。
- audit_event 脱敏审计。

## Stop Local Services

Stop the frontend, backend, and local model gateway terminal sessions with `Ctrl-C`.
