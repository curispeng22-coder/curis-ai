# Phase-3 Demo Freeze Report

Date: 2026-07-09

Status: demo freeze ready.

Current commit at freeze verification: `0ca7fdd9 fix(workspace): include demo context for usage events`

Demo script: `docs/demo/phase3-demo-script.md`

RC evidence: `docs/release/phase3-workspace-self-extension-rc.md`

## Current Demo Capability

Curis Workspace can now demonstrate:

- Workspace private model configuration.
- Workspace private tool configuration.
- Workspace private connector configuration.
- unified capability selection across `official` and `tenant_private`.
- tenant_private task creation.
- task execution through Model Gateway Adapter.
- usage_event writing for model/tool/task execution.
- Admin usage query by `tenant_id`.
- tenant_private isolation from official catalog.
- no real credential storage in Workspace private capability metadata.

## Startup Commands

Local model gateway:

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
            "id": "chatcmpl-local-demo",
            "object": "chat.completion",
            "choices": [{"index": 0, "message": {"role": "assistant", "content": "Local demo model gateway response"}, "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 11, "completion_tokens": 7, "total_tokens": 18, "estimated_cost": 0.000018},
            "model": payload.get("model") or "local-demo-model",
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

Backend:

```bash
cd "/Users/yy/Documents/Curis AI Workspace/backend"
CURIS_DB=/tmp/curis_phase3_demo.sqlite \
CURIS_MODEL_GATEWAY_BASE_URL=http://127.0.0.1:18080 \
CURIS_MODEL_GATEWAY_API_KEY=env:LOCAL_DEMO_KEY \
CURIS_MODEL_GATEWAY_MODEL=local-demo-model \
CURIS_MODEL_GATEWAY_ESTIMATED_COST_PER_1K_TOKENS=0.001 \
./.venv/bin/python -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port 8000
```

Frontend:

```bash
cd "/Users/yy/Documents/Curis AI Workspace/frontend"
NEXT_PUBLIC_API_BASE=http://127.0.0.1:8000 \
NEXT_PUBLIC_CURIS_TENANT_ID=default \
NEXT_PUBLIC_CURIS_CEO_ID=local-demo-ceo \
npm run dev -- --hostname 127.0.0.1 --port 3000
```

## Demo Flow

Use `docs/demo/phase3-demo-script.md` as the operator script.

High-level flow:

1. Start local model gateway.
2. Start backend.
3. Start frontend.
4. Open Workspace.
5. Add private model/tool/connector.
6. Confirm selector shows `official` and `tenant_private`.
7. Create task with tenant_private tool.
8. Run task.
9. Query Admin usage by `tenant_id=default`.
10. Capture screenshot checklist.

## Demo Seed

Default context:

- `tenant_id`: `default`
- `ceo_id`: `local-demo-ceo`

Official examples:

- `official.newapi.default`
- `model_gateway_tool`
- optional connector rows from `/api/catalog/connectors`

Tenant-private demo examples:

- `demo-private-model`
- `demo-private-tool`
- `demo-private-connector`

All reference values are placeholders:

- `env:TENANT_MODEL_KEY`
- `env:TENANT_TOOL_CONFIG`
- `env:TENANT_CONNECTOR_CONFIG`

## Screenshot Checklist

Required screenshots:

- Workspace private capability panel.
- Capability selector with `official` and `tenant_private`.
- Completed task result.
- Admin usage_event query result.

## Stability Verification

Frontend unit tests:

```bash
cd frontend && node --test app/taskViewModel.test.mjs
```

Result: 28 tests passed.

Frontend lint:

```bash
cd frontend && npm run lint
```

Result: passed.

Frontend build:

```bash
cd frontend && npm run build
```

Result: passed.

Backend full regression:

```bash
cd backend && ./.venv/bin/python -m unittest discover tests
```

Result: 298 tests passed.

Diff check:

```bash
git diff --check
```

Result: passed.

Workspace frontend `/api/platform/*` runtime scan:

```bash
rg -n "/api/platform/" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs
```

Result: no matches.

Workspace execution/runtime `/api/platform/*` scan:

```bash
rg -n "/api/platform/" backend/app/result_store.py backend/app/orchestrator.py backend/app/tool_executor.py backend/app/model_gateway.py frontend/app/page.js
```

Result: no matches.

Secret scan:

```bash
rg -n "api_key|password|secret|Authorization|Bearer|sk-[A-Za-z0-9_-]{10,}|credential_ref\s*[:=]\s*['\"]sk-|config_ref\s*[:=]\s*['\"]sk-" frontend/app/page.js frontend/app/taskViewModel.mjs frontend/app/taskViewModel.test.mjs backend/app/main.py backend/app/database.py backend/app/result_store.py backend/app/model_gateway.py
```

Result: no unexpected real secret storage.

Expected matches:

- backend gateway redaction and Authorization boundary code.
- backend Admin bearer-token parsing.
- frontend negative test value for rejecting secret-like input.

## Known Limits

- This is local/demo only, not hosted production.
- Local model gateway in the demo script is a fake OpenAI-compatible gateway for repeatable demo evidence.
- Production New API/provider credentials remain operator-owned and outside Curis source control.
- Browser automation was unstable during RC; manual screenshot capture is recommended for final demo packet.
- FastAPI emits an upstream Python 3.14 deprecation warning during tests; this is deferred and non-blocking.

## Temporarily Not Included

Demo Freeze does not include:

- ROI system.
- Employee system.
- Department system expansion.
- Business modules.
- Capability marketplace.
- Real credential hosting.
- Tenant package or billing logic.
- Admin Platform governance changes.
- Provider SDK or direct provider calls.
- New API source changes.
- Curis dependency on New API internal database.

## Freeze Decision

Phase-3 is ready for local/demo freeze.

Next recommended step: capture the four screenshots listed above and run one manual demo pass from a clean `/tmp/curis_phase3_demo.sqlite` database before presenting to external viewers.
