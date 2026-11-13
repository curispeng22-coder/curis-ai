# Phase-4 AI Employee System Demo Script

Status: Deprecated

Date: 2026-07-09

Demo status: local/demo only.

## Demo Defaults

Use these defaults unless a later demo gate changes them:

- `tenant_id`: `default`
- `ceo_id`: `local-demo-ceo`
- Backend URL: `http://127.0.0.1:8000`
- Frontend URL: `http://127.0.0.1:3000`
- Local model gateway demo URL: `http://127.0.0.1:18080`
- Admin usage query token: `platform-admin-dev`

## Demo Data

Official templates:

- DepartmentTemplate: `official.department.software_rnd`
- EmployeeTemplates:
  - `official.employee.tech_lead`
  - `official.employee.product_manager`
  - `official.employee.architect`
  - `official.employee.frontend_engineer`
  - `official.employee.backend_engineer`
  - `official.employee.qa_engineer`

Official capability example:

- Any active official tool shown in the Workspace capability selector, such as `model_gateway_tool`.

Tenant-private capability examples to create before binding:

- Private model:
  - `name`: `phase4-private-model`
  - `provider_type`: `newapi-compatible`
  - `base_url`: `https://tenant-gateway.local/openai`
  - `model_name`: `tenant-phase4-demo-model`
  - `credential_ref`: `env:TENANT_PHASE4_MODEL_REF`
  - `enabled`: checked
- Private tool:
  - `name`: `phase4-private-tool`
  - `type`: `llm_tool`
  - `description`: `Phase-4 tenant private tool`
  - `config_ref`: `env:TENANT_PHASE4_TOOL_CONFIG`
  - `enabled`: checked
- Private connector:
  - `name`: `phase4-private-connector`
  - `connector_type`: `crm`
  - `config_ref`: `env:TENANT_PHASE4_CONNECTOR_CONFIG`
  - `enabled`: checked

Reference fields must stay as `scheme:reference` placeholders. Do not enter real keys.

## Start Local Model Gateway

For a repeatable local demo without external provider dependency, start a local OpenAI-compatible fake gateway:

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
            "id": "chatcmpl-phase4-local-demo",
            "object": "chat.completion",
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Phase-4 local demo employee execution result"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 13,
                "completion_tokens": 7,
                "total_tokens": 20,
                "estimated_cost": 0.00002,
            },
            "model": payload.get("model") or "phase4-local-demo-model",
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
CURIS_DB=/tmp/curis_phase4_demo.sqlite \
CURIS_MODEL_GATEWAY_BASE_URL=http://127.0.0.1:18080 \
CURIS_MODEL_GATEWAY_API_KEY=env:LOCAL_DEMO_KEY \
CURIS_MODEL_GATEWAY_MODEL=phase4-local-demo-model \
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

## Open Workspace

Open:

```text
http://127.0.0.1:3000
```

## Demo Flow

1. Open Workspace.
2. In `研发部员工`, review the employee templates:
   - Tech Lead
   - Product Manager
   - Architect
   - Frontend Engineer
   - Backend Engineer
   - QA Engineer
3. In `私有能力`, add the private model, private tool, and private connector using the demo fields above.
4. Return to `研发部员工`.
5. Create a Software R&D department instance:
   - Template: `official.department.software_rnd`
   - Name: `Phase-4 研发部`
6. Create an employee instance:
   - Template: `Tech Lead`
   - Name: `技术负责人`
   - Instructions override: `优先拆解任务，保持研发边界。`
   - Status: `idle`
   - Enabled: checked
7. Bind an official capability to the employee:
   - Source: `official`
   - Type: `tool`
   - Capability: choose an active official tool such as `model_gateway_tool`
   - Priority: `20`
   - Enabled: checked
8. Bind a tenant_private capability to the employee:
   - Source: `tenant_private`
   - Type: `model`
   - Capability: `phase4-private-model`
   - Priority: `1`
   - Enabled: checked
9. In task creation, enter:
   - `让技术负责人完成 Phase-4 本地演示任务`
10. Select the created employee in the employee selector.
11. Create the task.
12. Run the task.
13. Confirm the task detail shows completed result text.
14. Confirm the task has employee attribution:
   - employee name
   - employee role
   - selected or default capability source
15. Query Admin usage events:

```bash
curl -s \
  -H "Authorization: Bearer platform-admin-dev" \
  "http://127.0.0.1:8000/api/platform/usage?tenant_id=default" | python3 -m json.tool
```

16. Confirm usage events include:
   - `tenant_id=default`
   - `task_id`
   - `employee_id` or `employee_role`
   - `capability_source=tenant_private`
   - `capability_type=model`
   - `capability_id=phase4-private-model`
   - `model_gateway_id=newapi`
   - `model_name=phase4-local-demo-model`
   - `status=success`
   - `created_at`

## Screenshot Checklist

Capture these screens for the demo packet:

- `研发部员工` employee template list.
- Employee instance list after creating `技术负责人`.
- Employee capability binding section showing official and tenant_private bindings.
- Task creation form with employee selector.
- Task execution result after completion.
- Admin usage_event query result showing employee attribution.

## Safety Notes

- Do not enter real provider API keys in `credential_ref` or `config_ref`.
- Keep `credential_ref` and `config_ref` as `scheme:reference`.
- Workspace frontend runtime must not call `/api/platform/*`.
- Admin usage query is read-only demo evidence.
- tenant_private capabilities must not appear in `/api/catalog/*`.
- Do not demonstrate ROI, marketplace, content operations, investment, ecommerce, or complex workflow engine behavior.

## Stop Local Services

Stop each terminal with `Ctrl+C`.

The demo SQLite DB is `/tmp/curis_phase4_demo.sqlite`; delete it if a fresh demo is needed.
