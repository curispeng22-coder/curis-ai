# New API Local Deployment for Curis Workspace

Date: 2026-07-08

## Purpose

Use New API as the first Curis model gateway. Curis Workspace calls New API only through HTTP OpenAI-compatible APIs.

New API is not the Curis primary system. Curis does not modify New API source code and does not depend on New API internal database tables.

Sources checked:

- New API GitHub repository: `QuantumNous/new-api`
- Official Docker image noted by upstream: `calciumion/new-api:latest`
- Upstream quick start documents Docker Compose and Docker run deployment.

## Files

- `deploy/new-api/docker-compose.yml`
- `deploy/new-api/.env.example`
- `tools/smoke_new_api_gateway.py`

## Local Deployment

```bash
cd deploy/new-api
cp .env.example .env
```

Edit `.env`:

```env
NEW_API_PORT=3000
NEW_API_SESSION_SECRET=<long-random-string>
TZ=Asia/Shanghai
```

Start New API:

```bash
docker compose up -d
```

Open:

```text
http://127.0.0.1:3000
```

## Configure One Upstream Model Channel

In the New API web console:

1. Log in as the New API administrator.
2. Add one upstream channel using an upstream provider account/key that you are authorized to use.
3. Enable at least one model name on that channel.
4. Create one New API token for Curis Workspace.
5. Keep the token outside Git and put it only in local environment variables.

Curis does not store this token in its database.

## Curis Workspace Environment

Set these variables before starting the Workspace backend:

```bash
export CURIS_MODEL_GATEWAY_BASE_URL=http://127.0.0.1:3000
export CURIS_MODEL_GATEWAY_ID=newapi-local
export CURIS_MODEL_GATEWAY_MODEL=<model-name-enabled-in-new-api>
export CURIS_MODEL_GATEWAY_API_KEY=<new-api-token>
export CURIS_MODEL_GATEWAY_ESTIMATED_COST_PER_1K_TOKENS=0
```

## Verify OpenAI-Compatible API

After New API is running and a token/model are configured:

```bash
python3 tools/smoke_new_api_gateway.py
```

The script calls:

```text
POST /v1/chat/completions
```

Expected result:

- HTTP 200
- Response contains `choices[0].message.content`
- Response may contain `usage.total_tokens`

## Verify Workspace Execution Path

Start Workspace backend with the same environment variables. Then create and run a task with tenant and CEO headers:

```bash
curl -s http://127.0.0.1:8000/api/task \
  -H 'Content-Type: application/json' \
  -H 'X-Tenant-Id: tenant-acme' \
  -H 'X-Ceo-Id: ceo-local' \
  -d '{"content":"用一句话说明 Curis Workspace 当前能力"}'
```

Run the returned task id:

```bash
curl -s -X POST http://127.0.0.1:8000/api/task/<task_id>/run \
  -H 'X-Tenant-Id: tenant-acme' \
  -H 'X-Ceo-Id: ceo-local'
```

Verify UsageEvent:

```bash
curl -s 'http://127.0.0.1:8000/api/platform/usage?tenant_id=tenant-acme' \
  -H 'X-Platform-Admin-Token: platform-admin-dev'
```

Expected UsageEvent payload fields:

- `tenant_id`
- `task_id`
- `model_gateway_id`
- `model_name`
- `token`
- `estimated_cost`
- `status`

## Scope Boundaries

- Do not modify New API source code.
- Do not read or depend on New API internal database.
- Do not store New API token in Curis database.
- Do not build Admin Platform pages in this Workspace slice.
- Do not implement tenant packages, billing, ROI, or platform governance.
- Do not bypass `ModelGatewayAdapter`.

## Production Security Boundary

ADR-0029 defines the production-safe boundary for this gateway path.

- New API is only a model gateway, not a Curis primary system.
- Curis Workspace calls New API only through `ModelGatewayAdapter`.
- New API admin credentials, Curis New API tokens, upstream provider keys, Authorization headers, and session secrets must never enter Git, docs, logs, UsageEvent payloads, task payloads/results, traces, or Curis database tables.
- Local secrets may live only in ignored local files, local password managers, New API local configuration, or New API local data.
- Production secrets must come from env/secret-manager/KMS/Vault injection or equivalent platform controls.
- Curis database rows may store only non-secret gateway/model metadata and opaque `credential_ref` values.
- UsageEvent model-meter fields are limited to `tenant_id`, `task_id`, `model_gateway_id`, `model_name`, `token`, `estimated_cost`, and `status`, plus non-secret audit envelope fields required for attribution/idempotency.
- Prompts, user input, model output, raw HTTP bodies, Authorization headers, New API internal row ids, and provider account secrets must not be logged in UsageEvent.

## Local Verification Result

2026-07-08 on this machine:

- Docker CLI was installed locally: `Docker version 29.6.1`.
- Docker Compose was installed locally: `Docker Compose version 5.3.1`.
- Colima was installed and started with Docker runtime.
- New API container `curis-new-api` is running with port mapping `0.0.0.0:3000->3000/tcp`.
- New API log shows SQLite mode, `New API v1.0.0-rc.20 started`, and `ready`.
- `GET http://127.0.0.1:3000` returned HTTP 200 with `X-New-Api-Version: v1.0.0-rc.20`.
- `GET /api/setup` returned initialized state after local root setup.
- A Curis Workspace local New API token was created and stored only in ignored local file `deploy/new-api/.env`.
- DeepSeek upstream channel was configured in New API as the first local model gateway channel.
- `GET /v1/models` with the Curis token returned HTTP 200 and includes `deepseek-v4-flash`.
- `python3 tools/smoke_new_api_gateway.py` reached New API and returned `{"ok": true, ...}` with token usage.
- Workspace TestClient execution created a task, ran it through `selected_tool=model_gateway_tool`, and wrote one `usage.model_call` event.
- The UsageEvent payload included `tenant_id`, `task_id`, `model_gateway_id`, `model_name`, `token`, `estimated_cost`, and `status`.
- Workspace backend regression passed with 198 tests.

## Release Candidate Reference

The model-gateway-enabled local/demo release-candidate package is recorded in `docs/release/model-gateway-local-demo-rc.md`.

For release-candidate verification, combine this New API local deployment guide with:

- backend focused guardrail/preference tests;
- backend regression;
- frontend view-model tests, lint, and build;
- local preference read/save/reset evidence;
- content-only Task API payload evidence;
- UsageEvent model-call allowlist evidence;
- secret and scope drift scans.
