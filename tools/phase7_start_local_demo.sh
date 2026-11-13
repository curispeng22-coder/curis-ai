#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LOG_DIR="${CURIS_DEMO_LOG_DIR:-/tmp/curis_phase7_demo_logs}"
DB_PATH="${CURIS_DEMO_DB:-/tmp/curis_phase7_stable_demo.sqlite}"
GATEWAY_PORT="${CURIS_DEMO_GATEWAY_PORT:-18080}"
BACKEND_PORT="${CURIS_DEMO_BACKEND_PORT:-8000}"
FRONTEND_PORT="${CURIS_DEMO_FRONTEND_PORT:-3000}"

mkdir -p "$LOG_DIR"

echo "Curis Phase-7 local/demo startup"
echo "Logs: $LOG_DIR"
echo "Database: $DB_PATH"

python3 "$ROOT/tools/phase7_check_local_demo_env.py"

echo "Starting local OpenAI-compatible demo gateway on :$GATEWAY_PORT"
python3 - <<PY >"$LOG_DIR/model-gateway.log" 2>&1 &
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
        data = json.dumps({
            "id": "chatcmpl-phase7-demo",
            "object": "chat.completion",
            "choices": [{
                "index": 0,
                "message": {"role": "assistant", "content": "Phase-7 stable demo gateway result"},
                "finish_reason": "stop"
            }],
            "usage": {"prompt_tokens": 11, "completion_tokens": 13, "total_tokens": 24, "estimated_cost": 0.000024},
            "model": payload.get("model") or "phase7-workflow-private-model"
        }).encode()
        self.send_response(200)
        self.send_header("content-type", "application/json")
        self.send_header("content-length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, fmt, *args):
        print(fmt % args)

HTTPServer(("127.0.0.1", int("$GATEWAY_PORT")), Handler).serve_forever()
PY
GATEWAY_PID=$!

echo "Starting backend on :$BACKEND_PORT"
(
  cd "$ROOT/backend"
  CURIS_ENV=local \
  CURIS_DB="$DB_PATH" \
  CURIS_MODEL_GATEWAY_BASE_URL="http://127.0.0.1:$GATEWAY_PORT" \
  CURIS_MODEL_GATEWAY_API_KEY=env:FALLBACK_ONLY \
  CURIS_MODEL_GATEWAY_MODEL=phase7-demo-fallback-model \
  CURIS_MODEL_GATEWAY_ESTIMATED_COST_PER_1K_TOKENS=0.001 \
  ./.venv/bin/python -m uvicorn app.main:create_app --factory --host 127.0.0.1 --port "$BACKEND_PORT"
) >"$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

echo "Starting frontend on :$FRONTEND_PORT"
(
  cd "$ROOT/frontend"
  NEXT_PUBLIC_API_BASE="http://127.0.0.1:$BACKEND_PORT" \
  NEXT_PUBLIC_CURIS_TENANT_ID=default \
  NEXT_PUBLIC_CURIS_CEO_ID=local-demo-ceo \
  npm run dev -- --hostname 127.0.0.1 --port "$FRONTEND_PORT"
) >"$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!

cat >"$LOG_DIR/pids.env" <<EOF
GATEWAY_PID=$GATEWAY_PID
BACKEND_PID=$BACKEND_PID
FRONTEND_PID=$FRONTEND_PID
EOF

echo "Started:"
echo "  gateway pid=$GATEWAY_PID"
echo "  backend pid=$BACKEND_PID"
echo "  frontend pid=$FRONTEND_PID"
echo "Open: http://127.0.0.1:$FRONTEND_PORT"
echo "Stop with: kill $GATEWAY_PID $BACKEND_PID $FRONTEND_PID"
