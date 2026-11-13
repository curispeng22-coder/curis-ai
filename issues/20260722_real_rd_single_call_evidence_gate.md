# RealRD Single-Call Persistent Evidence Gate

**Status: PAUSED_BY_USER_PRIORITY** — 用户当前唯一验收目标是可操作的 Project Runtime 页面；不得进行 Key 注入、模型调用、容器重建、测试或取证。

## Objective

以一次受控、真实的 RealRD 模型调用，取证同一 Run/Step/Tool 的持久审计与精确 Token、价格、成本联合证据。

## Fixed Model Contract

- Provider: OpenAI API。
- Model: `gpt-5.4-mini-2026-03-17`。
- Gateway: `ModelGatewayAdapter/newapi`。
- Egress: 仅 `https://api.openai.com:443/v1/chat/completions`。
- Credential: 仅 Owner 通过部署设施隐藏注入 `CURIS_MODEL_GATEWAY_API_KEY`；只核验存在，不读取、回传或持久化。
- Limits: input ≤8192、output ≤2048、total ≤10240、60 秒、attempt=1、retry=0、429 不重试、无 fallback、成本 ≤USD0.02，且不突破既有 USD0.10 总上限。

## Preparation Before Execution

系统交付席只可通过既有受控路径创建并固化一个全新的非生产小型 fixture Run；Task 的服务端映射即为固定 fixture，不新增 fixture registry。调用前回传实际 Task、Run、Step、Tool binding、唯一测试 command 与审计字段；Execution ID 仅在调用成功后作为唯一执行证据回传。不得使用历史 Run/Step/Tool、默认值、同名推断或客户端替换。

准备阶段不注 Key、不启动模型、不出网、不修改项目业务文件或历史 Run。

## Execution Acceptance

1. 启动前精确核对 SHA `8ca63ce7`、实际 IDs、scope、唯一性、模型/出口/预算/超时和敏感输入扫描；任一差异在 Adapter 前拒绝。
2. 仅一次：模型调用 → 受控 diff → 唯一测试 → 只读 git diff；无第二 Run、跳步、回填、重试或 fallback。
3. 调用后立即停机；失败即停。
4. 同一 Run/Step/Tool 的持久审计、Token、价格、成本可回查；不得记录 prompt、raw diff、token、Cookie、Authorization、Key 或绝对路径。

## Approved Evidence Shape

- 采用总控最小方案 A：禁止 pending Execution reservation；Execution ID 只能来自唯一真实调用后的既有持久化路径。
- 固定非生产 fixture 仅由 Task 的服务端映射表达；禁止新增 immutable fixture registry。
- 取证 Run 必须标记 `created_from_template_id=real_rd_single_call_evidence_gate/v1`；该标记存在时，Task 映射缺失、字段缺失或字段不一致一律在 Adapter 前拒绝，不回退普通 RealRD 路径。
- 固定目标：`tools/real_rd_fixture/target_b.py`；固定验证文件：`backend/tests/test_real_rd_fixture_b.py`。
- 固定 fixture manifest SHA-256：`1bf4f2e722b6ac0cfd1b5f49aa75c72138109cdc7315713b72876ad45224c3b9`。
- 唯一命令：`rd_evidence_fixture_b_v1` → `/usr/local/bin/python -m pytest -q backend/tests/test_real_rd_fixture_b.py`；禁止 Shell、第二命令或客户端替换。
- 固定 Tool capability：`real_rd_executor_tool`；调用前必须唯一命中同 tenant/company/department/employee/role/step 的 active official tool binding。
- 调用前必须确认该 Task 的 `executions=0`，该 Run 的 `usage.model_call=0`、`usage.tool_call=0`；不创建 pending Execution。
- 审计只允许既有结构化 ID、hash、状态、时长、Token、价格与成本字段；禁止 prompt、raw diff、token 字符串、Authorization、Cookie、Key 和绝对路径。

## Server-Owned Task Mapping

Task `content` 必须是 `real_rd_single_call_fixture/v1` 的精确 JSON 快照，且仅含：Issue/run source、operation/fixture/tenant/company/department/project/Run/Step/Employee/binding ID、fixture SHA、固定目标和测试路径、唯一 command ID/argv、allow paths 与既有审计字段 allowlist。客户端输入只可与该快照精确相等，不得覆盖；同 tenant 下该 command ID 必须唯一。

## Route

系统交付席无出网准备实际输入 → 安全边界席核对 Gate → 总控正式执行授权 → Owner 隐藏注入 → 质量席唯一调用与验收。

## Current State

- 容器运行时前置已解除：`issues/20260722_real_rd_container_runtime_prerequisite.md` 为 `PASS_WITH_NOTE`（`8ca63ce7` / image `a2cf1625`）。
- 下一步仅为无 Key 的启动命令静态复核；通过后才转为一次性 Owner 隐藏注入动作。
