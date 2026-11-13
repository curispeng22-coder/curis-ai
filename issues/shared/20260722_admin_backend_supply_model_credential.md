# Shared：前端牵引阶段 · 模型/Agent/凭证配置后端补给（现状核实 + 真实缺口定位）

- 状态：`DRAFT`（待 Workspace 前端确认 + Admin/Workspace 双 lead 会签 + 安全边界席/总控裁定鉴权模型）
- 发起：WorkBuddy/Admin 主理人 齐活林
- 目标：Codex / Workspace 团队（前端主导）
- 父 Gate：`issues/...` 新阶段「前端产品动线牵引开发」（2026-07-22 总控指令）切片①「模型、Agent 与凭证配置」
- 性质：**现状核实 + 真实缺口定位 + 待前端确认**——**非从零实现**，后端相关接口已大多真实存在。

## 1. 背景

新阶段 directive 切片①：用户在前端填写名称、地址和 Key → 测试连接 → 直接可用。Admin 作为后端供应方，先核实现状以避免重复建设。本 Issue 为选项 (A) 产物：把接口契约、字段、双 lead 会签先备好。

> **重要纠正**：初判"模型目录写接口/凭证接口不存在"经实测已推翻——相关接口已全部真实存在。本 Issue 据此从"待建清单"改为"已存在能力盘点 + 真实缺口"。

## 2. 已核实：后端已真实存在的接口（实测 `backend/app/main.py` + `database.py` + `credential_vault.py`）

| 能力 | 端点 | 鉴权 | 实测状态 |
| --- | --- | --- | --- |
| 凭证自服务 CRUD + 测试连接 | `POST/GET/PUT /api/workspace/credentials`、`POST /api/workspace/credentials/{id}/test`、`/disable`、`DELETE` | Workspace 自服务（tenant） | **真实**。secret 经 `local_backend.store` 存本地后端；DB 仅 `credential_ref`+`secret_digest`；production 故意禁建（`credential_vault.py:158`）。符合"绝不落明文" |
| 单账号 Vault「我的凭证」 | `POST/GET /api/credential`、`POST /api/credential/{id}/test` | Workspace | **真实**（Wave2 V1） |
| 私有能力（用户自定义 Agent/模型配置，元数据） | `POST/GET /api/workspace/capabilities/private` | Workspace 自服务 | **真实**。但 `_reject_secret_like_metadata` 显式拒绝 secret 类元数据——Key 必须走凭证库、配置只存 `credential_ref`（`main.py:1678`） |
| 能力选择器 | `GET /api/workspace/capabilities/selector` | Workspace | **真实** |
| 模型目录 CRUD | `POST/GET /api/platform/models`、`PUT .../{model_key}`(enable/disable) | **Admin token**（`_require_platform_admin`） | **真实**（`model_catalog`） |
| 统一能力目录 CRUD（model/tool/connector） | `POST/GET /api/platform/capabilities`、`PUT .../{capability_key}` | **Admin token** | **真实**（`capability_catalog`，ADR-0028 Phase-2） |
| 网关 CRUD（base_url + credential_ref） | `POST/GET /api/platform/gateways`、`PUT .../{gateway_id}` | **Admin token** | **真实**（`gateway_catalog`） |
| 外部 Agent 注册为能力 | `POST /api/platform/capabilities/external-agent` | **Admin token** | **真实**（P1 T10，零代码改动登记） |

**结论**：切片①所需的"写 + 测试连接"接口已全部存在。无需从零重建。

## 3. 真实缺口（Admin 侧待补 / 待决策）

1. **鉴权模型错位（核心缺口）**：凭证自服务是 Workspace/tenant 鉴权；但**模型官方目录**与**网关 base_url 配置**只有 Admin token 守卫，无自服务版本。统一 Workspace 前端"用户自服务配置模型/Agent/地址"无法用普通用户 token 调用 `/api/platform/*`。
   - 选项 A：为模型目录 + 网关暴露 **Workspace 作用域（自服务）配置端点**（与凭证一致）。
   - 选项 B：v1 自用场景下，创始人以 Admin token 配置模型/网关（符合"一人公司自用"），前端代为持有 Admin token——与"用户不需理解令牌"愿景相悖，但实现最快。
   - **需总控 / 产品规划席裁定**，属 scope/auth 决策（可能触发 L2 #5 权限边界）。
2. **私有能力 ↔ 凭证 绑定已通，但私有能力 ≠ 官方模型**：用户可在 `/api/workspace/capabilities/private` 建自定义 Agent（元数据 + `credential_ref`），但**官方模型目录写入仍是 Admin 门控**；自定义 base_url（本地 LLM 等）需 Admin 门控的网关。自服务"地址"配置缺落点。
3. **真实执行待确认**：R4 审计指出多数能力仍"契约/文档"。需确认 `credential_vault.test()` 与模型网关 `execute_model_gateway` 是否真实外呼，还是返回 mock。建议 QA 实跑 `test_phase5_credential_vault.py` + `test_d5_*` 确认真实执行链路（非仅契约）。

## 4. 安全边界（已合规，记录备查）

- 凭证：`local_backend.store` 存 secret，DB 仅 `credential_ref`+`secret_digest`；production 禁建。符合"绝不落明文"铁律。
- 红线：任何凭证/Auth 相关改动仍须经 **安全边界席** 评审；多租户/生产化凭证属 L2（当前 self-use 不触发）。

## 5. 待 Workspace 前端确认（决定 Admin 补给形态）

- 切片①前端将调用哪些端点？走 `/api/workspace/*`（自服务）还是预期 `/api/platform/*`（Admin）？
- "模型/Agent 配置"在前端是否由创始人（Admin）操作，还是普通成员自服务？
- 测试连接反馈形式（成功/失败文案、错误码）期望？
- 是否需要"用户自定义 base_url（本地模型端点）"——决定是否需要自服务网关端点。

## 6. 双 lead 会签 + 安全边界席

- 本 Issue 任何实现改动须 Admin + Workspace 双 lead 会签 + API 版本化兼容（07-17 部署隔离纪律）。
- 凭证 / Auth 改动另需 **安全边界席** + 总控对"鉴权模型"裁定（第 3.1 项）。

## Compact Handoff

Issue: `issues/shared/20260722_admin_backend_supply_model_credential.md`
Objective: 核实切片①后端现状、定位真实缺口（鉴权错位为主）、待前端确认补给形态。
Special Constraints: 仅现状核实与契约备案，未新增/修改代码；凭证/Auth 改动须经安全边界席 + 双 lead 会签。
Next Seat: Codex / Workspace 产品规划席（确认前端调用形态与鉴权预期）
Handoff: HANDOFF_REQUIRED → 请 Workspace 前端回传第 5 节确认项，Admin 据以决定补自服务端点或确认 Admin-token 方案。
