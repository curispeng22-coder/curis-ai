# Phase-3 Workspace Self-Extension Demo Script

Status: Deprecated

Date: 2026-07-09

Demo status: local/demo only.

## Demo Defaults

Use these defaults unless a separate demo gate changes them:

- `tenant_id`: `default`
- `ceo_id`: `local-demo-ceo`
- Backend URL: `http://127.0.0.1:8000`
- Frontend URL: `http://127.0.0.1:3000`
- Local model gateway demo URL: `http://127.0.0.1:18080`

## Demo Data

Official examples are seeded/read from the existing catalog layer:

- Official model: `official.newapi.default`
- Official tool: `model_gateway_tool`
- Official connector: any active connector returned by `/api/catalog/connectors`; if none exists, say connectors are not part of this local demo seed.

Tenant-private examples to create during the demo:

- Private model:
  - `name`: `demo-private-model`
  - `provider_type`: `newapi-compatible`
  - `base_url`: `https://tenant-gateway.local/openai`
  - `model_name`: `tenant-demo-model`
  - `credential_ref`: `env:TENANT_MODEL_KEY`
  - `enabled`: checked
- Private tool:
  - `name`: `demo-private-tool`
  - `type`: `llm_tool`
  - `description`: `Demo tenant private tool`
  - `config_ref`: `env:TENANT_TOOL_CONFIG`
  - `enabled`: checked
- Private connector:
  - `name`: `demo-private-connector`
  - `connector_type`: `crm`
  - `config_ref`: `env:TENANT_CONNECTOR_CONFIG`
  - `enabled`: checked

Reference fields must stay as `scheme:reference` placeholders. Do not enter real keys.

## Start Local Model Gateway

For demo without external provider dependency, start a local OpenAI-compatible fake gateway:

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
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Local demo model gateway response"},
                    "finish_reason": "stop",
                }
            ],
            "usage": {
                "prompt_tokens": 11,
                "completion_tokens": 7,
                "total_tokens": 18,
                "estimated_cost": 0.000018,
            },
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

## Start Backend

```bash
cd "/Users/yy/Documents/Curis AI Workspace/backend"
CURIS_DB=/tmp/curis_phase3_demo.sqlite \
CURIS_MODEL_GATEWAY_BASE_URL=http://127.0.0.1:18080 \
CURIS_MODEL_GATEWAY_API_KEY=env:LOCAL_DEMO_KEY \
CURIS_MODEL_GATEWAY_MODEL=local-demo-model \
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

## Demo Flow

1. Open Workspace:
   - `http://127.0.0.1:3000`
2. In `私有能力`, add the private model using the fields above.
3. Add the private tool using the fields above.
4. Add the private connector using the fields above.
5. Confirm each list shows the new item with source `tenant_private`.
6. In `任务入口`, enter:
   - `Run Phase-3 demo task with demo-private-tool`
7. In `执行能力`, select:
   - `demo-private-tool - tenant_private / tool / demo-private-tool`
8. Click `创建任务`.
9. In task history/detail, click `运行任务`.
10. Confirm the task completes and returns `Local demo model gateway response`.
11. Open Admin usage query:

```bash
curl -s \
  -H "Authorization: Bearer platform-admin-dev" \
  "http://127.0.0.1:8000/api/platform/usage?tenant_id=default" | python3 -m json.tool
```

12. Confirm usage events include:
   - `tenant_id=default`
   - `capability_source=tenant_private`
   - `capability_type=model`
   - `capability_type=tool`
   - `capability_type=task`
   - `model_gateway_id=newapi`
   - `model_name=local-demo-model`
   - `status=success`

## Screenshot Checklist

Capture these screens for the demo packet:

- Workspace `私有能力` panel after private model/tool/connector are added.
- Workspace `执行能力` selector showing both `official` and `tenant_private`.
- Workspace task detail after successful execution.
- Admin usage_event query result for `tenant_id=default`.

## Safety Notes

- Do not enter real provider API keys in `credential_ref` or `config_ref`.
- Keep `credential_ref` and `config_ref` as `scheme:reference`.
- Workspace must not call `/api/platform/*` from frontend runtime.
- Admin usage query is read-only for demo evidence.
- tenant_private entries must not appear in `/api/catalog/capabilities`.

## Stop Local Services

Stop each terminal with `Ctrl+C`.

The demo SQLite DB is `/tmp/curis_phase3_demo.sqlite`; delete it if a fresh demo is needed.
