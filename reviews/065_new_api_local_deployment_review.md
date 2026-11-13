# Review 065: New API Local Deployment

Date: 2026-07-08

Issue: `issues/068_new_api_local_deployment.md`

## Quality Result

PASS.

## Scope Verified

- New API deployment documentation was added.
- Docker Compose file was added for `calciumion/new-api:latest`.
- Environment template was added.
- OpenAI-compatible smoke test script was added.
- New API source code was not modified.
- Curis does not depend on New API internal database.
- Docker CLI, Docker Compose, and Colima were installed locally.
- New API was started through Docker Compose.
- New API root setup was completed locally.
- A Curis Workspace local New API token was created and stored only in ignored local file `deploy/new-api/.env`.
- OpenAI-compatible `/v1/models` is reachable.
- DeepSeek upstream channel was configured as the first live model channel.
- OpenAI-compatible `/v1/models` includes `deepseek-v4-flash`.
- OpenAI-compatible `/v1/chat/completions` returns a successful response through New API.
- Workspace TestClient execution used `model_gateway_tool` and wrote one required `usage.model_call` event.

## Commands

```bash
docker --version
docker compose version
which docker
which colima
which podman
which orb
brew install docker docker-compose colima
colima start --cpu 2 --memory 4 --disk 20
docker-compose up -d
curl -i -s http://127.0.0.1:3000
curl -s http://127.0.0.1:3000/api/status
curl -s http://127.0.0.1:3000/api/setup
curl -s http://127.0.0.1:3000/v1/models
python3 tools/smoke_new_api_gateway.py
Workspace TestClient create/run plus `/api/platform/usage`
cd backend
../backend/.venv/bin/python -m unittest discover tests
```

## Evidence

- `docker --version`: `Docker version 29.6.1`.
- `docker-compose version`: `Docker Compose version 5.3.1`.
- `colima start --cpu 2 --memory 4 --disk 20`: completed successfully.
- `docker ps --filter name=curis-new-api`: `curis-new-api Up ... 0.0.0.0:3000->3000/tcp`.
- `docker logs --tail 120 curis-new-api`: New API started in SQLite mode and became ready.
- `curl -i -s http://127.0.0.1:3000`: HTTP 200 with `X-New-Api-Version: v1.0.0-rc.20`.
- `curl -s http://127.0.0.1:3000/api/setup`: setup completed after local root initialization.
- `curl -s http://127.0.0.1:3000/v1/models`: HTTP 200 and includes `deepseek-v4-flash`.
- `python3 tools/smoke_new_api_gateway.py`: returned `ok: true`, response content, and token usage.
- Workspace TestClient create/run plus usage query: run status 200, selected tool `model_gateway_tool`, usage query status 200, one `usage.model_call` event with required gateway fields.
- Initial local runtime detection before installation: `docker`, Docker Compose, Colima, Podman, and Orb were not available.
- `which podman`: not found.
- `which orb`: not found.
- Focused usage fail-closed test: 1 test passed.
- Backend regression: 198 tests passed.

## Known Gaps

- The Curis local New API token exists only in ignored `deploy/new-api/.env`; do not commit it.
- DeepSeek upstream key is stored in New API local configuration only; do not commit secrets or depend on New API internal database.

## Handoff

Next Seat: 产品规划席

Handoff: final closeout
