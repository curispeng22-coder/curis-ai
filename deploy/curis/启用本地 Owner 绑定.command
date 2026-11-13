#!/usr/bin/env bash
set -euo pipefail
set +x

export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"
root="$(cd "$(dirname "$0")/../.." && pwd)"
tmp="$(mktemp /tmp/curis-local-oidc.XXXXXX)"
chmod 600 "$tmp"
started=false
inject_attempted=false
keychain_created=false

cleanup() {
  rc=$?
  if [ "$keychain_created" = true ]; then
    if /usr/bin/security delete-generic-password \
      -a curis-local-owner -s com.curis.local.owner-bootstrap >/dev/null; then
      keychain_created=false
    else
      rc=1
    fi
  fi
  if [ "$rc" -ne 0 ] && [ "$inject_attempted" = true ]; then
    if reset_result="$(docker exec gateway-workspace-1 /usr/local/bin/python \
      -m backend.app.local_google_oidc reset 2>/dev/null)"; then
      [ "$reset_result" = "OWNER_BINDING_RESET=true" ] || rc=1
    else
      rc=1
    fi
  fi
  if [ "$rc" -ne 0 ] && [ "$started" = true ]; then
    "$root/deploy/curis/stop-local.sh" >/dev/null 2>&1 || true
  fi
  rm -f "$tmp"
  unset google_client_id google_client_secret bootstrap_material COMPOSE_FILE
  unset CURIS_WORKSPACE_FRONTEND_PORT
  trap - EXIT HUP INT TERM
  if [ "$rc" -ne 0 ]; then
    printf 'OWNER_BINDING_READY=false\n'
  fi
  exit "$rc"
}
trap cleanup EXIT
trap 'exit 1' HUP INT TERM

IFS= read -r -s -p 'Google OAuth Client ID: ' google_client_id </dev/tty
printf '\n' >/dev/tty
IFS= read -r -s -p 'Google OAuth Client Secret: ' google_client_secret </dev/tty
printf '\n' >/dev/tty
[ -n "$google_client_id" ] && [ -n "$google_client_secret" ] || exit 1

if /usr/bin/security find-generic-password \
  -a curis-local-owner -s com.curis.local.owner-bootstrap >/dev/null 2>&1; then
  /usr/bin/security delete-generic-password \
    -a curis-local-owner -s com.curis.local.owner-bootstrap >/dev/null
fi
bootstrap_material="$(/usr/bin/openssl rand -hex 32)"
printf '%s\n' "$bootstrap_material" | /usr/bin/expect -c '
  log_user 0
  set timeout 3
  gets stdin material
  if {$material eq ""} { exit 1 }
  spawn /usr/bin/security add-generic-password -a curis-local-owner \
    -s com.curis.local.owner-bootstrap -T "" -w
  expect {
    -exact "password data for new item:" { send -- "$material\r" }
    timeout { unset material; exit 1 }
    eof { unset material; exit 1 }
  }
  expect {
    -exact "retype password for new item:" { send -- "$material\r" }
    timeout { unset material; exit 1 }
    eof { unset material; exit 1 }
  }
  unset material
  expect {
    eof { set result [wait]; exit [lindex $result 3] }
    timeout { exit 1 }
  }
' >/dev/null 2>&1
keychain_created=true
unset bootstrap_material
/usr/bin/security find-generic-password \
  -a curis-local-owner -s com.curis.local.owner-bootstrap >/dev/null

cat >"$tmp" <<'YAML'
services:
  workspace:
    environment:
      CURIS_ENV: development
      CURIS_LOCAL_GOOGLE_OIDC_ENABLED: "1"
YAML
chmod 600 "$tmp"
[ "$(stat -f '%Lp' "$tmp")" = 600 ] || exit 1

unset COMPOSE_FILE
"$root/deploy/curis/stop-local.sh" >/dev/null
export CURIS_WORKSPACE_FRONTEND_PORT=3001
export COMPOSE_FILE="$root/deploy/curis/gateway/docker-compose.yml:$tmp"
"$root/deploy/curis/start-local.sh" >/dev/null
started=true

reset_result="$(docker exec gateway-workspace-1 /usr/local/bin/python \
  -m backend.app.local_google_oidc reset)"
[ "$reset_result" = "OWNER_BINDING_RESET=true" ] || exit 1
inject_attempted=true
inject_result="$({
  printf '%s\0%s\0' "$google_client_id" "$google_client_secret"
  /usr/bin/security find-generic-password \
    -a curis-local-owner -s com.curis.local.owner-bootstrap -w
} |
  docker exec -i gateway-workspace-1 /usr/local/bin/python \
    -m backend.app.local_google_oidc inject)"
[ "$inject_result" = "OWNER_BINDING_READY=true" ] || exit 1
/usr/bin/security delete-generic-password \
  -a curis-local-owner -s com.curis.local.owner-bootstrap >/dev/null
keychain_created=false
if /usr/bin/security find-generic-password \
  -a curis-local-owner -s com.curis.local.owner-bootstrap >/dev/null 2>&1; then
  exit 1
fi

curl --noproxy '*' --connect-timeout 2 --max-time 5 -fsS \
  http://127.0.0.1:8080/api/auth/google/status |
  /usr/bin/python3 -c 'import json,sys; value=json.load(sys.stdin); assert value=={"owner_binding_ready":True,"authenticated":False}; print("OWNER_BINDING_READY=true"); print("LOCAL_GOOGLE_OIDC_SET_AND_MATCH=true")'
printf 'PROJECT_RUNTIME_URL=http://127.0.0.1:3001/projects/local-project-b6f325cc-f347-4a74-a6d6-67528a3889b8\n'
/usr/bin/open http://127.0.0.1:3001/login
