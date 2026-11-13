#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
generated="$root/deploy/curis/gateway/.generated"
runtime="$generated/runtime"

for name in frontend; do
  if command -v screen >/dev/null; then
    screen -S "curis-r1-$name" -X quit >/dev/null 2>&1 || true
  fi
  pid_file="$runtime/$name.pid"
  if [ -f "$pid_file" ]; then
    pid="$(cat "$pid_file")"
    kill "$pid" 2>/dev/null || true
    rm -f "$pid_file"
  fi
done
docker rm -f curis-quality-jwks >/dev/null 2>&1 || true
if [ -f "$generated/quality.env" ]; then
  set -a
  source "$generated/quality.env"
  set +a
  (cd "$root/deploy/curis/gateway" && docker-compose down)
fi
echo "Curis stopped"
