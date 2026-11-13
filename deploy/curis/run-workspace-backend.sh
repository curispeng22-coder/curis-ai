#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
set -a
source "${CURIS_WORKSPACE_ENV:-deploy/curis/workspace.env.example}"
set +a
exec .venv/bin/uvicorn backend.app.main:app --host 127.0.0.1 --port 8002
