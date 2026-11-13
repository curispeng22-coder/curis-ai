#!/usr/bin/env bash
set -euo pipefail

root="$(cd "$(dirname "$0")/../.." && pwd)"
workspace_frontend_port="${CURIS_WORKSPACE_FRONTEND_PORT:-3001}"
generated="$root/deploy/curis/gateway/.generated"
runtime="$generated/runtime"
gateway_dir="$root/deploy/curis/gateway"
sentinel="${CURIS_GATEWAY_SENTINEL:-0}"
diagnostic_component=""
diagnostic_phase=""
diagnostic_http_code=""
diagnostic_failure_class=""
sentinel_data=""
sentinel_override=""

for command in docker docker-compose pnpm lsof curl; do
  command -v "$command" >/dev/null || { echo "缺少命令: $command" >&2; exit 1; }
done
[ -f "$generated/quality.env" ] || { echo "缺少 $generated/quality.env" >&2; exit 1; }
[ -f "$generated/jwks/jwks.json" ] || { echo "缺少本地 JWKS" >&2; exit 1; }
[ -d "$root/frontend" ] || { echo "缺少 frontend" >&2; exit 1; }
for port in "$workspace_frontend_port" 8002 8080; do
  ! lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null || {
    echo "端口 $port 已占用" >&2; exit 1;
  }
done

mkdir -p "$runtime"
chmod 700 "$runtime"
[ ! -L "$runtime" ] && [ "$(stat -f '%Lp' "$runtime")" = 700 ] || {
  echo "诊断目录必须是权限 0700 的普通目录" >&2; exit 1;
}

if [ "$sentinel" = 1 ]; then
  sentinel_data="$(mktemp -d "${TMPDIR:-/tmp}/curis-gateway-sentinel.XXXXXX")"
  chmod 700 "$sentinel_data"
  export OIDC_ISSUER="https://quality.issuer.local"
  export CURIS_WORKSPACE_DB="/srv/curis/data/sentinel.sqlite"
  export CURIS_DATA_DIR="$sentinel_data"
  export CURIS_GATEWAY_PORT=8080
  export CURIS_IDENTITY_AUDIT_KEY="curis-sentinel-audit-not-secret"
  export CURIS_MODEL_GATEWAY_PROFILE="r3_openai"
  export CURIS_MODEL_GATEWAY_BASE_URL="https://api.openai.com"
  export CURIS_MODEL_GATEWAY_API_KEY="curis-model-sentinel-not-secret"
  export CURIS_MODEL_GATEWAY_ID="newapi"
  export CURIS_MODEL_GATEWAY_MODEL="gpt-5.4-mini-2026-03-17"
  sentinel_override="$runtime/.gateway-sentinel-compose.$$.yml"
  umask 077
cat >"$sentinel_override" <<'YAML'
services:
  egress:
    command:
      - envoy
      - --log-level
      - info
      - --config-yaml
      - |
        static_resources:
          listeners: []
          clusters: []
  workspace:
    environment:
      CURIS_MODEL_GATEWAY_PROFILE: ${CURIS_MODEL_GATEWAY_PROFILE:?}
      CURIS_MODEL_GATEWAY_BASE_URL: ${CURIS_MODEL_GATEWAY_BASE_URL:?}
      CURIS_MODEL_GATEWAY_API_KEY: ${CURIS_MODEL_GATEWAY_API_KEY:?}
      CURIS_MODEL_GATEWAY_ID: ${CURIS_MODEL_GATEWAY_ID:?}
      CURIS_MODEL_GATEWAY_MODEL: ${CURIS_MODEL_GATEWAY_MODEL:?}
YAML
  chmod 600 "$sentinel_override"
  export COMPOSE_FILE="$gateway_dir/docker-compose.yml:$sentinel_override"
else
  set -a
  source "$generated/quality.env"
  set +a
  export CURIS_WORKSPACE_ENVIRONMENT=development
  export CURIS_LOCAL_OWNER_ENABLED=1
  export CURIS_LOCAL_GOOGLE_OIDC_ENABLED=0
  export CURIS_WORKSPACE_DB=/srv/curis/data/curis.sqlite
  export CURIS_DATA_DIR="$root/data"
  export CURIS_D1_FROZEN=1
  export CURIS_D1_EXECUTE_ENABLED=0
fi
case "$CURIS_WORKSPACE_DB" in
  /srv/curis/data/*) ;;
  *) echo "CURIS_WORKSPACE_DB 必须位于 /srv/curis/data" >&2; exit 1 ;;
esac
(cd "$gateway_dir" && ./render-config.sh)
workspace_db="$CURIS_DATA_DIR/${CURIS_WORKSPACE_DB#/srv/curis/data/}"
if [ "$sentinel" = 1 ]; then
  [ "$workspace_db" = "$sentinel_data/sentinel.sqlite" ] || {
    echo "Sentinel DB 必须位于临时隔离目录" >&2; exit 1;
  }
else
  [ "$workspace_db" = "$root/data/curis.sqlite" ] || {
    echo "Workspace DB 必须是 data/curis.sqlite" >&2; exit 1;
  }
fi

classify_http_code() {
  case "$1" in
    200) printf '200|health_ok' ;;
    401) printf '401|auth_rejected' ;;
    502|503|504) printf '503|upstream_unavailable' ;;
    000) printf '000|listener_unavailable' ;;
    *) printf '000|timeout' ;;
  esac
}

write_evidence() {
  local path="$1" content="$2" line
  [ ! -e "$path" ] && [ ! -L "$path" ] || return 1
  [ "$(printf '%s\n' "$content" | wc -l | tr -d ' ')" -le 200 ] || return 1
  while IFS= read -r line; do
    case "$line" in
      event=startup_failure|event=sentinel_health|component=admin|component=gateway|component=workspace|component=egress|phase=wait_for|phase=sentinel|http_code=000|http_code=200|http_code=401|http_code=503|failure_class=listener_unavailable|failure_class=auth_rejected|failure_class=upstream_unavailable|failure_class=process_exited|failure_class=timeout|failure_class=health_ok|state=created|state=running|state=restarting|state=exited|state=paused|state=dead|state=missing|health=healthy|health=unhealthy|health=starting|health=unknown|truncated=true|truncated=false|redaction_status=passed) ;;
      container=gateway-gateway-1|container=gateway-workspace-1|container=gateway-egress-1) ;;
      exit_code=-[0-9]*|exit_code=[0-9]*|line_count=[0-9]*|timestamp=[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]T[0-9][0-9]:[0-9][0-9]:[0-9][0-9]Z|file=gateway-startup-*.log) ;;
      *) return 1 ;;
    esac
  done <<<"$content"
  (set -C; : >"$path") || return 1
  chmod 600 "$path"
  printf '%s\n' "$content" >>"$path"
  [ -f "$path" ] && [ ! -L "$path" ] && [ "$(stat -f '%Lp' "$path")" = 600 ]
}

preserve_startup_evidence() {
  local event="$1" stamp prefix summary ps_output service name state health exit_code
  local line_count truncated content
  [ -n "$diagnostic_component" ] && [ -n "$diagnostic_http_code" ] || return 0
  stamp="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
  prefix="gateway-startup-$(date -u '+%Y%m%dT%H%M%SZ')-$$"
  summary="event=$event
component=$diagnostic_component
phase=$diagnostic_phase
http_code=$diagnostic_http_code
failure_class=$diagnostic_failure_class
timestamp=$stamp
redaction_status=passed"
  write_evidence "$runtime/$prefix-summary.log" "$summary" || return 1

  ps_output="$(cd "$gateway_dir" && docker-compose ps -a --format '{{.Name}}|{{.Service}}|{{.State}}|{{if .Health}}{{.Health}}{{else}}unknown{{end}}|{{.ExitCode}}' gateway workspace egress 2>/dev/null || true)"
  while IFS='|' read -r name service state health exit_code; do
    [ -n "$name" ] || continue
    case "$service" in gateway|workspace|egress) ;; *) return 1 ;; esac
    case "$name" in gateway-gateway-1|gateway-workspace-1|gateway-egress-1) ;; *) return 1 ;; esac
    [ -n "$state" ] || state=missing
    [ -n "$health" ] || health=unknown
    [ -n "$exit_code" ] || exit_code=-1
    content="component=$service
container=$name
state=$state
health=$health
exit_code=$exit_code
timestamp=$stamp
redaction_status=passed"
    write_evidence "$runtime/$prefix-ps-$service.log" "$content" || {
      find "$runtime" -maxdepth 1 -type f -name "$prefix-*.log" -delete
      return 1
    }
  done <<<"$ps_output"

  for service in gateway workspace egress; do
    line_count="$(cd "$gateway_dir" && docker-compose logs --no-color --tail 200 "$service" 2>/dev/null | wc -l | tr -d ' ')"
    truncated=false
    [ "$line_count" -lt 200 ] || truncated=true
    content="component=$service
phase=$diagnostic_phase
line_count=$line_count
truncated=$truncated
redaction_status=passed
timestamp=$stamp
file=$prefix-$service.log"
    write_evidence "$runtime/$prefix-$service.log" "$content" || {
      find "$runtime" -maxdepth 1 -type f -name "$prefix-*.log" -delete
      return 1
    }
  done
  echo "Gateway 诊断: HTTP $diagnostic_http_code $diagnostic_failure_class; evidence=$prefix" >&2
}

cleanup_sentinel_data() {
  [ -z "$sentinel_override" ] || [ ! -e "$sentinel_override" ] || rm -- "$sentinel_override"
  if [ -n "$sentinel_data" ] && [ -d "$sentinel_data" ]; then
    find "$sentinel_data" -mindepth 1 -maxdepth 1 -type f -delete
    rmdir "$sentinel_data"
  fi
}

started=true
cleanup_on_error() {
  if [ "$started" = true ]; then
    preserve_startup_evidence startup_failure || true
    "$root/deploy/curis/stop-local.sh" >/dev/null 2>&1 || true
  fi
  cleanup_sentinel_data
}
trap cleanup_on_error ERR

if [ "$sentinel" = 1 ]; then
  for image in gateway-workspace:latest envoyproxy/envoy:v1.31-latest python:3.14-slim; do
    docker image inspect "$image" >/dev/null 2>&1 || {
      echo "Sentinel 镜像缺失，拒绝联网拉取: $image" >&2
      exit 1
    }
  done
  if ! (cd "$gateway_dir" && docker-compose up --no-build -d); then
    diagnostic_component=egress
    diagnostic_phase=sentinel
    diagnostic_http_code=000
    diagnostic_failure_class=process_exited
    cleanup_on_error
    exit 1
  fi
else
  if ! (cd "$gateway_dir" && docker-compose up --build -d); then
    cleanup_on_error
    exit 1
  fi
fi
docker run -d --name curis-quality-jwks --network gateway_edge \
  -v "$generated/jwks:/srv/jwks:ro" -w /srv/jwks \
  python:3.14-slim python -m http.server 8765 --bind 0.0.0.0 >/dev/null
docker restart gateway-gateway-1 >/dev/null

if [ "$sentinel" = 1 ]; then
  for _ in $(seq 1 30); do
    [ "$(docker inspect -f '{{.State.Running}}' gateway-gateway-1 2>/dev/null || true)" = true ] &&
      [ "$(docker inspect -f '{{.State.Running}}' gateway-workspace-1 2>/dev/null || true)" = true ] &&
      docker logs gateway-workspace-1 2>&1 | grep -q 'Application startup complete' && break
    sleep 1
  done
  sentinel_code="$(curl --noproxy '*' --connect-timeout 2 --max-time 5 -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8080/health || true)"
  IFS='|' read -r diagnostic_http_code diagnostic_failure_class <<<"$(classify_http_code "$sentinel_code")"
  diagnostic_component=gateway
  diagnostic_phase=sentinel
  preserve_startup_evidence sentinel_health
  "$root/deploy/curis/stop-local.sh" >/dev/null 2>&1 || true
  cleanup_sentinel_data
  trap - ERR
  [ "$diagnostic_http_code" = 200 ] || exit 1
  echo "Gateway sentinel: HTTP 200 health_ok"
  exit 0
fi

launch_process() {
  local name="$1" workdir="$2" log="$runtime/$1.log"
  shift 2
  rm -f "$runtime/$name.pid"
  if command -v screen >/dev/null; then
    screen -S "curis-r1-$name" -X quit >/dev/null 2>&1 || true
    screen -dmS "curis-r1-$name" /bin/bash -c \
      'cd "$1"; log="$2"; pidfile="$3"; shift 3; echo $$ >"$pidfile"; exec "$@" >>"$log" 2>&1' \
      curis "$workdir" "$log" "$runtime/$name.pid" "$@"
  else
    (cd "$workdir" && nohup "$@" >"$log" 2>&1 </dev/null &
      echo $! >"$runtime/$name.pid")
  fi
}

pnpm_bin="$(command -v pnpm)"
launch_process frontend "$root/frontend" env \
  NEXT_PUBLIC_API_BASE=/gateway NEXT_PUBLIC_CEO_ID=local-ceo-660378a5-a637-45ff-b6bd-431cd36c7046 \
  "$pnpm_bin" dev --hostname 127.0.0.1 --port "$workspace_frontend_port"

wait_for() {
  local name="$1" url="$2" code
  for _ in $(seq 1 30); do
    code="$(curl -s -o /dev/null -w '%{http_code}' "$url" || true)"
    [ "$code" = 200 ] && return 0
    sleep 1
  done
  case "$name" in
    Admin) diagnostic_component=admin ;;
    Gateway) diagnostic_component=gateway ;;
    *) diagnostic_component="" ;;
  esac
  if [ -n "$diagnostic_component" ]; then
    IFS='|' read -r diagnostic_http_code diagnostic_failure_class <<<"$(classify_http_code "$code")"
    diagnostic_phase=wait_for
    echo "$name 启动失败: HTTP $diagnostic_http_code $diagnostic_failure_class" >&2
  else
    echo "$name 启动失败，日志位于 $runtime" >&2
  fi
  return 1
}

wait_for "Gateway" http://127.0.0.1:8080/health
wait_for "Frontend" "http://127.0.0.1:$workspace_frontend_port/ceo-office"
trap - ERR

echo "Curis started: Frontend $workspace_frontend_port, Workspace internal 8002, Gateway 8080"
