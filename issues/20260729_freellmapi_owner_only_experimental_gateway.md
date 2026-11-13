# Issue: FreeLLMAPI Owner-only Experimental Gateway

- **Issue ID**: `20260729_freellmapi_owner_only_experimental_gateway`
- **Owner**: 系统交付席
- **提出席**: 总控决策席（用户直接授权）
- **创建日期**: 2026-07-29
- **状态**: `IMPLEMENTED / QUALITY_PASS / BLOCKED_L2_LIVE_VALIDATION`（未注入 Key、未启动 Sidecar、未做真实出站）
- **相关前置**: `issues/shared/20260722_admin_backend_supply_model_credential.md`（模型/凭证配置后端补给，本 Issue 复用其 env/vault 凭证引用机制）

---

## 1. Objective

将 FreeLLMAPI 作为 Curis 的一个**实验型模型网关**接入，仅供 **Owner 自用**，用于降低非敏感研发任务的模型成本。它不是一个独立模型，而是「一个网关 + 多个动态模型」。

**兼容性与 Owner-only 隔离审查已证明“仅配置”不足；本 Issue 只增加安全边界席允许的最小守卫、目录过滤和服务端验证路径，不新增适配器、数据库表或抽象层。**

---

## 2. 研究结论（务必作为约束，不得作为产品承诺）

1. FreeLLMAPI 是自托管、OpenAI-compatible 聚合网关；供应商、模型端点和理论额度均为上游动态数据。**任何时点数字均不得作为产品承诺、SLA 或稳定额度。**
2. 源码 MIT，可部署/修改/商用；但免费额度仍受**每个上游供应商各自条款**约束。
3. 项目明确定位为**单用户、个人实验用途**，不具备多租户认证与用户计费；作者建议不要共享端点、不要用免费层支撑付费生产服务。
4. 本次**只允许 Owner 自用**，不开放给员工、租户或外部客户，不宣传「免费 Token 权益」。
5. 提示词**不经过 FreeLLMAPI 官方服务器**（自托管 Sidecar），但会发送到实际路由到的**上游供应商**，因此只允许**非敏感数据**。

**事实链接**
- 仓库：https://github.com/tashfeenahmed/freellmapi
- 使用限制与供应商条款综述：https://github.com/tashfeenahmed/freellmapi#terms-of-service-review
- MIT License：https://github.com/tashfeenahmed/freellmapi/blob/main/LICENSE
- 服务条款：https://freellmapi.co/terms
- 隐私说明：https://freellmapi.co/privacy
- 模型目录：https://freellmapi.co/models

---

## 3. Curis 现有复用点与当前缺口

| 复用点 | 文件 | 当前结论 |
|------|------|---------|
| OpenAI-compatible 网关适配 | `backend/app/model_gateway.py` | `ModelGatewayAdapter` 已实现，命中 `{base_url}/v1/chat/completions`；`api_key` 运行期从 `os.getenv("CURIS_MODEL_GATEWAY_API_KEY")` 或入参解析；`redact_model_gateway_text` 会对密钥与 prompt 做脱敏，满足「不记录明文密钥/完整提示词」。 |
| Admin 网关元数据 + env/vault 凭证引用 | `backend/app/model_catalog.py` + `backend/app/database.py` | `GatewayCatalog.create(...)` 可保存网关元数据；`credential_ref` 仅保存 `env/kms/vault` 引用，不保存密钥。 |
| 逐网关状态隔离 | `backend/app/database.py` | `set_model_gateway_status` 按 `gateway_id` 单行更新；`list_model_gateways` 独立枚举。**停用 `freellmapi.experimental` 不会影响其他网关。** |
| 密钥运行期解析 | `backend/app/main.py` | 专用验证路径仅服务端解析 `env:FREELLMAPI_API_KEY`，不进入前端或数据库。普通业务执行路径不接入该网关。 |
| Owner-only 可见性 | `backend/app/main.py` + `backend/app/database.py` | 专用验证同时要求本地 Owner session 与 loopback；Workspace 网关投影显式排除该实验网关。 |

→ **结论：不需要新表、新适配器或新抽象层。首次登记强制 `inactive`；只有 Owner-local 固定非敏感验证成功后才能变为 `active`。**

---

## 4. 执行顺序

### 第 1 步：新建独立 Issue + 安全边界席确认
- 本文件即为独立 Issue。
- 安全边界席初审结论为 `BLOCKED`，指出 Admin token、Workspace 投影和运行期解析缺口；最小修复完成后复审结论为 `PASS`。
- **严禁绕过当前暂停状态直接注入 Key**。

### 第 2 步：使用 FreeLLMAPI 官方 Docker 作为独立 Sidecar
- 拉取官方镜像，**不 Fork、不复制其 Admin UI**。
- 以独立容器运行，与 Curis backend 同 compose 网络（或本机 localhost）。

### 第 3 步：仅绑定本机 / 容器内网
- FreeLLMAPI Dashboard、统一 API Key、`/v1` 端点**禁止公网暴露**。
- 仅 Curis backend 容器 / 127.0.0.1 可访问；不对外发布端口。

### 第 4 步：上游供应商 Key 由 Owner 自行提供，仅存 env/vault
- 上游供应商 Key 存入 **FreeLLMAPI 自身的 env/vault**（其 `.env` 或密钥机制），**Curis 永不见、永不存**这些上游 Key。
- Curis 侧仅持有 FreeLLMAPI 的**统一 API Key**，存入 Curis 的 `env` / `vault`，经 `credential_ref` 引用；**不进入 Curis 数据库、Issue、日志或前端**。

### 第 5 步：在 Curis Admin 登记（配置，非代码新增）
```python
# 复用现有 GatewayCatalog.create，不新增任何函数/表
gateway_catalog.create(
    gateway_id="freellmapi.experimental",
    name="FreeLLMAPI Experimental",
    gateway_type="newapi",            # OpenAI-compatible，复用现有适配器
    base_url="http://127.0.0.1:3101",
    status="inactive",
    credential_ref="env:FREELLMAPI_API_KEY",   # 指向第 4 步的 env/vault 引用
    default_model="auto",
)
```

### 第 6 步：复用现有 Owner-only 本地认证
- 不新增 RBAC、成员授权、套餐或计费系统。
- 该网关不得进入 Workspace 公共网关投影或员工可选模型目录。
- 验证调用只允许本地 Owner session；独立 Admin token 不能替代 Owner 身份。

### 第 7 步：仅验证一条非敏感 chat-completions 请求
- 由服务端固定 synthetic prompt 走通 `{base_url}/v1/chat/completions`。
- 记录：**实际 provider、model、status、延迟(ms)、Token 数**。
- **不记录完整提示词或密钥**（现有 `redact_model_gateway_text` 已保障）。

### 第 8 步：确认可停用且不影响其他网关
- 调 `set_model_gateway_status("freellmapi.experimental", "inactive")`，验证其他网关调用不受影响；该网关始终不进入 Workspace 投影。

---

## 5. 验收条件

- [ ] Owner 能通过 Curis 成功调用一次 FreeLLMAPI。
- [ ] 非 Owner 无入口、无凭证、无法直接访问 Sidecar。
- [ ] Curis 与日志中没有明文供应商 Key。
- [ ] FreeLLMAPI 未暴露公网。
- [ ] 失败 / 限流 / 无可用免费模型时返回**真实错误**，不伪装成功。
- [ ] 不新增 Workspace UI、Tenant、Plan、Quota、Billing、Usage 或商业化能力。

---

## 6. 安全边界（安全边界席确认内容）

### 6.1 外部凭证边界
- **两类密钥，物理隔离**：
  1. **FreeLLMAPI 统一 API Key**：自托管实例生成，Curis 用它向 Sidecar 鉴权。存 Curis `env`/`vault`，经 `credential_ref` 引用；**不进 DB / Issue / 日志 / 前端**。
  2. **上游供应商 Key**：Owner 提供，仅存 **FreeLLMAPI Sidecar**；**Curis 永不见、永不存**。
- Curis `model_gateways` 表只存：`gateway_id / name / gateway_type / base_url / status / credential_ref / default_model`，**零密钥材料**。
- **注入护栏**：当前模型调用处于暂停态，本回合**不注入任何 Key**；Key 注入是 Owner 的运维动作，由 Owner 向 env/vault 写入，Admin 团队不代写。
- MIT 允许商用，但免费额度受各上游供应商条款约束 → **不承诺固定模型/额度/SLA**。

### 6.2 数据边界
- 提示词发往自托管 Sidecar（不经 FreeLLMAPI 官方服务器），但会**转发到实际路由的上游供应商**。
- 硬性约束：仅允许**非敏感研发数据**。禁止客户数据、PII、生产关键或敏感内容流经此网关。
- 该网关**不得成为任何租户 / 客户 / 项目数据的默认路由**，仅限 Owner 个人非敏感实验。
- Curis 日志只记 provider / model / status / 延迟 / Token，**不记完整 prompt 与密钥**（现有脱敏机制已保障）。

### 6.3 网络边界
- FreeLLMAPI Dashboard、统一 API Key 端点、`/v1` **仅绑定 localhost 或容器内部网络**，不发布到公网。
- Curis backend → Sidecar：内部网络（compose bridge 或 127.0.0.1）。
- Sidecar → 上游供应商：出站公网（固有、不可避免，但仅 Sidecar 持有上游 Key）。
- **不 Fork、不复制 FreeLLMAPI Admin UI** 进 Curis。

### 6.4 运维边界
- 复用现有 Owner-only 本地认证；不新增 RBAC / 成员授权 / 套餐 / 计费。
- 停用 `freellmapi.experimental` 为单行状态翻转，不影响其他网关（已实测 `set_model_gateway_status` 逐行隔离）。
- 限流 / 无可用免费模型时返回真实错误，不伪装成功（适配器现有错误透传 + 脱敏）。

---

## 7. 禁止范围（重申）

- 不开放给外部用户。
- 不共享 Owner 的免费 Key 池。
- 不处理客户数据、隐私数据或生产关键任务。
- 不承诺固定模型、固定额度、稳定性或 SLA。
- 不为未来多租户需求提前开发。
- 不新增 Workspace UI / Tenant / Plan / Quota / Billing / Usage / 商业化能力。

---

## 8. 当前阻塞项

1. ~~**安全边界复审**：Owner-local、Workspace 隔离、私网 URL、固定 prompt、路由元数据和重定向边界。~~ `PASS`。
2. **Owner 本机生成密钥**：FreeLLMAPI 统一 Key → Workspace Backend `FREELLMAPI_API_KEY`；上游供应商 Key → FreeLLMAPI Sidecar。
3. **Owner 启动 Sidecar**：官方镜像仅绑定 `127.0.0.1:3101`。
4. **真实验证**：完成一次固定 synthetic prompt 调用与停用隔离验证。

> 上述 2–4 均为 Owner 运维动作，Admin 团队在暂停态下不代注入。完成后由系统交付席执行第 5–8 步（配置 + 一次非敏感验证 + 停用验证）。

---

## 9. Delivery Evidence

- 聚焦与受影响回归：`48 passed`；新增重定向与敏感路由元数据负测后，Adapter 聚焦回归 `28 passed`。
- 安全边界席独立回归：`62 passed`，结论 `PASS`。
- 质量运行席唯一一次全量回归：Backend `1170 passed / 2 skipped / 0 failed`；Frontend `49 passed`，lint/build `PASS`。
- Review：`reviews/20260729_freellmapi_owner_only_experimental_gateway_review.md`。
- 产品规划席：`ACCEPT` 本地实现与安全边界；真实调用继续 `BLOCKED_L2`。
- Compose 静态投影：`host_ip: 127.0.0.1`、host port `3101`、container port `3001`。
- 官方镜像清单存在：`v0.6.4`，包含 `linux/arm64` 与 `linux/amd64`。
- 未读取、写入或输出任何真实供应商 Key / FreeLLMAPI unified Key。

---

## 10. Next Seat / Handoff

- **Next Seat**: Owner 完成密钥与 localhost Sidecar 供应 → 系统交付席仅执行一次真实验证和停用隔离。
- **Handoff**: `sent to Owner；等待运维前提`。
