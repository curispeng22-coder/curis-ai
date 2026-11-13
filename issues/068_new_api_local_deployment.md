---
issue: "068"
title: "New API Local Deployment"
status: "done"
owner: "系统交付席"
date: "2026-07-08"
depends_on: "issues/065_workspace_model_gateway_adapter.md"
---

# New API Local Deployment

## Objective

Document, deploy, and locally verify New API as Curis Workspace's first model gateway with one DeepSeek upstream channel.

## Scope

- Write local deployment documentation.
- Add Docker Compose deployment file for `calciumion/new-api:latest`.
- Add environment template for New API and Curis Workspace gateway config.
- Add OpenAI-compatible smoke test script.
- Install and start local container runtime when missing.
- Start New API locally.
- Initialize local New API root user.
- Create Curis Workspace local New API token.
- Verify OpenAI-compatible HTTP reachability.
- Configure one authorized upstream DeepSeek channel.
- Verify Workspace task execution through Adapter -> New API -> DeepSeek.
- Verify UsageEvent write after model execution.

## Non-Goals

- No New API source code modification.
- No dependency on New API internal database.
- No Curis Admin Platform page.
- No billing, tenant package, ROI, or platform governance.
- No credential persistence in Curis database.

## Verification

- `docker --version`
- `docker compose version`
- `which colima`
- `which podman`
- `which orb`
- `python3 tools/smoke_new_api_gateway.py` after runtime and New API token exist.
- `curl http://127.0.0.1:3000`
- `curl http://127.0.0.1:3000/v1/models`
- `python3 tools/smoke_new_api_gateway.py`
- Workspace TestClient task create/run plus `/api/platform/usage` query.

## Completion Notes

- Deployment docs and files are prepared.
- Docker CLI, Docker Compose, and Colima are installed locally.
- Colima is running with Docker runtime.
- New API container `curis-new-api` is running locally at `http://127.0.0.1:3000`.
- New API root initialization succeeded.
- Curis Workspace local New API token was created and stored only in ignored local file `deploy/new-api/.env`.
- DeepSeek upstream channel is configured as the first live model channel.
- OpenAI-compatible `/v1/models` returns HTTP 200 and includes `deepseek-v4-flash`.
- OpenAI-compatible `/v1/chat/completions` returns a successful model response through New API.
- Workspace TestClient create/run path selects `model_gateway_tool` and writes one `usage.model_call` event with tenant/task/gateway/model/token/cost/status fields.
- Workspace Model Gateway Adapter remains implemented and backend-verified separately.
