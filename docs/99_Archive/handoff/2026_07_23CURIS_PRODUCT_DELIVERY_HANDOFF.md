# Curis Product Delivery Handoff

Status: Deprecated

日期：2026-07-23  
当前分支：`feat/roadmap-r1r2`  
封存前 HEAD：`b349b4367e2002f3702ffd788162c477015a2c4f`  
状态：旧团队停止自主开发，转为技术资产支持组。

---

## 1. 当前系统如何启动

唯一完整本机启动入口：

```bash
cd "/Users/yy/Documents/Curis AI Workspace"
CURIS_WORKSPACE_FRONTEND_PORT=3001 ./deploy/curis/start-local.sh
```

唯一完整本机停止入口：

```bash
cd "/Users/yy/Documents/Curis AI Workspace"
./deploy/curis/stop-local.sh
```

启动后端口：

| 服务 | 端口 | 说明 |
| --- | --- | --- |
| Admin backend | `127.0.0.1:8001` | `deploy/curis/run-admin-backend.sh` 启动 |
| Workspace backend | 容器内 `8002` | 不作为用户直连入口，经 Gateway 访问 |
| Gateway | `127.0.0.1:8080` | Workspace 受控入口 |
| Admin frontend | `127.0.0.1:3100` | `frontend-admin` |
| Workspace frontend | `127.0.0.1:3001` | `frontend-workspace`；当前 Project Owner Workbench 使用此端口 |

本机 Owner 登录入口：

```bash
open "/Users/yy/Documents/Curis AI Workspace/deploy/curis/启用本地 Owner 绑定.command"
```

该启动器只用于 local/development：macOS Keychain Owner bootstrap -> Google OIDC -> Project Owner Workbench。不得用于生产。

---

## 2. 当前真实可复用的前端和后端目录

### 后端

| 目录 / 文件 | 用途 |
| --- | --- |
| `backend/app/main.py` | FastAPI 应用、主要 API 注册入口 |
| `backend/app/company_project_runtime.py` | Company / Project / Task 运行对象 |
| `backend/app/local_google_oidc.py` | 本机 Google OIDC Owner 登录与本地会话 |
| `backend/app/identity_membership.py` | Gateway 主体到 membership 的可信身份映射 |
| `backend/app/tenant_context.py` | TenantContext 派生 |
| `backend/app/resource_scope_policy.py` | 租户 / 公司 / 项目资源范围校验 |
| `backend/app/workflow_runtime.py` | Workflow 运行与 step 结果 |
| `backend/app/rd_workflow_runtime.py` | R&D Workflow 到 RealRD 的运行桥接 |
| `backend/app/real_rd_executor.py` | 真实研发闭环执行器 |
| `backend/app/dev_agent.py` | DevAgent 协议与后端适配器 |
| `backend/app/local_rd_toolset.py` | 本地最小研发工具集 |
| `backend/app/result_store.py` | Task / Result / Trace / 执行证据 |
| `backend/app/credential_vault.py` | Credential Vault 元数据与解析边界 |
| `backend/app/usage_meter.py` | Usage 只读聚合 |
| `backend/app/model_gateway.py` | ModelGatewayAdapter 与模型调用边界 |
| `backend/app/ceo_evidence_api.py` | CEO 运行证据只读 API |
| `backend/app/issue_pipeline_api.py` | Pipeline / Graph API |

### 前端

| 目录 / 文件 | 用途 |
| --- | --- |
| `frontend-workspace/app/projects/[project_id]/page.js` | 当前项目负责人工作台页面 |
| `frontend-workspace/app/projects/[project_id]/projectRuntimeViewModel.mjs` | 项目运行页 / 工作台 view model |
| `frontend-workspace/app/login/page.js` | 本地 Google 登录失败 / 登录入口页 |
| `frontend-workspace/app/control/secret-vault/page.js` | Workspace Credential Vault 前端 |
| `frontend-workspace/app/ceo-office/page.js` | Workspace CEO Office 页面 |
| `frontend-workspace/app/employees/page.js` | 员工目录页面 |
| `frontend-admin/app/platform/*` | Admin 平台目录、模型、网关、用量、商业配置面板 |
| `frontend/ceo-evidence/` | CEO evidence Vite SPA，只读证据视角 |
| `frontend/` | 旧合并前端目录，仍有历史页面；后续优先用 `frontend-workspace` / `frontend-admin` |

---

## 3. 已真实可用的 API 与执行能力

| 能力 | 入口 | 当前状态 |
| --- | --- | --- |
| 健康检查 | `GET /health` | 可用 |
| 本机 Google OIDC | `/api/auth/google/status`、`/login`、`/callback`、`/logout` | local-only 可用 |
| Company CRUD | `/api/workspace/companies/*` | API 可用 |
| Project CRUD | `/api/workspace/projects/*` | API 可用 |
| Project Task 创建 | `POST /api/workspace/projects/{project_id}/tasks` | API 可用 |
| Task 创建 / 运行 / 查询 | `POST /api/task`、`POST /api/task/{task_id}/run`、`GET /api/task/{task_id}`、`GET /api/task/{task_id}/trace` | API 可用 |
| Workflow 模板 / Run / 下一步 | `/api/workspace/workflows/*` | API 可用 |
| R&D Workflow | `POST /api/workspace/rd-workflow/run` | 可真实触发 RealRD 路径；当前非产品主线 |
| Credential Vault | `/api/workspace/credentials/*` | API + 前端可用；不落明文 |
| Model Preference | `/api/workspace/model-preference` | API 可用 |
| Result Summary | `/api/results/summary`、`/api/results/publish-packages`、`/api/results/content-workflow-runs` | API 可用 |
| Usage 只读聚合 | `/api/platform/usage`、`/api/platform/usage-meter`、`/api/platform/usage/summary` | API 可用；不代表真实计费 |
| CEO Overview | `/api/ceo/overview` | API 可用 |
| CEO Evidence | `/api/ceo/evidence/*` | 只读证据 API 可用 |
| Pipeline / Graph | `issue_pipeline_api` 注册的 pipeline routes | 技术可用 |
| Admin Catalog | `/api/platform/*`、`/api/catalog/*` | 可用，属 Admin / Shared 边界 |

当前用户可见前端能力：

- 本机 Google 登录进入项目负责人工作台。
- 聊天式目标入口与结构化任务入口。
- 两路进入同一结构化确认单。
- 确认后生成计划并启动。
- 查看结果解释、trace / artifact 折叠证据。
- 批准成果或修改目标继续。

---

## 4. RealRD、DevAgent、Task、Workflow、Result、凭证和成本能力入口

| 能力 | 主要入口 | 说明 |
| --- | --- | --- |
| RealRD | `backend/app/real_rd_executor.py`；`POST /api/workspace/rd-workflow/run`；`backend/scripts/run_real_rd.py` | 已证明读代码、改代码、跑测试、交付 diff；当前暂停让位于前端产品动线 |
| DevAgent | `backend/app/dev_agent.py` | 协议与多个适配器存在；并非所有适配器都有真实外部执行能力 |
| Task | `POST /api/task`、`POST /api/task/{task_id}/run`、`GET /api/task/{task_id}`、`GET /api/task/{task_id}/trace` | AI Task Executor 基础路径 |
| Workflow | `backend/app/workflow_runtime.py`；`/api/workspace/workflows/*` | 可创建 run、查询 run、执行下一步 |
| Result | `backend/app/result_store.py`；`/api/results/*`；`/api/task/{task_id}/trace` | 保存和读取 task、execution、trace、summary |
| Credential Vault | `backend/app/credential_vault.py`；`frontend-workspace/app/control/secret-vault/page.js`；`/api/workspace/credentials/*` | 只存凭据元数据 / 引用 / digest；不得记录明文 |
| Usage / 成本 | `backend/app/usage_meter.py`；`backend/app/model_gateway.py`；`/api/platform/usage*` | Usage 可聚合；成本显示缺失时必须显示“未记录”，不得伪造 0 |

---

## 5. 真实执行、mock 与 default-off

### 真实执行 / 可复用

- 项目负责人工作台第一纵向切片：local-only，已通过真实浏览器链路。
- Google OIDC local Owner 登录：local/development 可用。
- Task 基础创建、运行、状态和 trace 查询。
- Workflow run / run-next-step 基础路径。
- RealRD 读代码 -> 改代码 -> 跑测试 -> diff 的研发闭环。
- Credential Vault 元数据管理和测试入口。
- CEO evidence 只读聚合。
- Admin / Catalog 目录 API。

### 技术存在或 default-off

- Agent execution kernel：实现和测试存在，默认关闭。
- BudgetGuard：实现和测试存在，默认关闭。
- Governance gate / Pending decision：部分可用，但不是当前前端主线。
- DevAgent 多适配器：协议存在，真实可用性依赖后端、CLI、密钥和环境。
- D1 工具链：演示可用，不作为当前产品主线。

### mock / 不得宣称完成

- `Project Runtime Local` 旧页面只算内部运行证据页，不是正式产品入口。
- 成本缺失时显示“未记录”，不能写成 0。
- 员工未真实分配时必须显示未分配，不能用假员工补齐。
- Real Billing、Invoice、Payment、Marketplace、外部 Connector 测试连接均未开放。
- 生产级身份、多用户组织管理、生产 Secret Manager / KMS / Vault 未完成。

---

## 6. 当前数据库位置和关键配置

### 数据库

| 路径 | 用途 |
| --- | --- |
| `data/admin.sqlite` | Admin 本地库 |
| `data/workspace.sqlite` | Workspace 示例库 |
| `data/curis.sqlite` | 当前共享 / 历史聚合库 |
| `backend/data/curis.sqlite` | 后端历史本地库 |
| `deploy/curis/gateway/.generated/data/quality.sqlite` | 当前 Gateway / Workspace local 运行库 |
| `deploy/curis/gateway/.generated/data/issue_pipeline.sqlite` | Issue / Pipeline 相关本地库 |

### 配置

| 配置 | 位置 / 说明 |
| --- | --- |
| 完整本机运行配置 | `deploy/curis/gateway/.generated/quality.env`；不要在文档或聊天中输出具体值 |
| Admin 示例配置 | `deploy/curis/admin.env.example` |
| Workspace 示例配置 | `deploy/curis/workspace.env.example` |
| Gateway Compose | `deploy/curis/gateway/docker-compose.yml` |
| Gateway Envoy 模板 | `deploy/curis/gateway/envoy.yaml.template` |
| Egress Envoy | `deploy/curis/gateway/egress.yaml` |
| Workspace Dockerfile | `deploy/curis/gateway/Dockerfile.workspace` |
| 本地 JWKS | `deploy/curis/gateway/.generated/jwks/`；本机生成物，不得迁移为生产密钥 |

关键固定值：

- Gateway：`http://127.0.0.1:8080`
- Workspace frontend：`http://127.0.0.1:3001`
- Admin frontend：`http://127.0.0.1:3100`
- Google redirect URI：`http://127.0.0.1:8080/api/auth/google/callback`
- Local project URL：`http://127.0.0.1:3001/projects/local-project-b6f325cc-f347-4a74-a6d6-67528a3889b8`

---

## 7. 已知阻塞

- 旧团队已停止自主开发、Gate、复盘、架构扩展和前端修改。
- 当前无活动实施 Issue；后续新团队以产品动线为主，不继承旧团队主动推进权。
- 生产身份体系未完成；当前 Google OIDC 只限本机 local/development。
- Google OAuth Client Secret 未写入仓库；不得通过聊天索取或回显。
- RealRD、模型调用、Key 注入、容器重建和取证均已暂停，不得自动恢复。
- Project Owner Workbench 第一切片是 local-only，不代表生产发布。
- 工作树在封存前包含大量旧团队未提交文件；本次封存保留现状，不回滚、不重写。

---

## 8. 不能修改的安全边界

- 不得绕过 Gateway、membership、TenantContext 和资源范围校验。
- 不得把客户端 Header、Admin token、默认身份或 email 当作 Workspace 身份。
- 不得记录、输出或持久化 Google code、state、token、Cookie、Authorization、Client Secret、API Key。
- 不得读取或复制旧敏感 access log 原文。
- 不得把 local Google OIDC / macOS Keychain bootstrap 复用到生产。
- 不得把 `Project Runtime Local` 或内部证据页包装为正式产品完成。
- 不得伪造成果、成本、员工分配或运行成功。
- 不得启用真实模型调用、外部出网、凭据注入或不可逆数据处置，除非新团队提出明确需求并重新授权。
- 不得主动新增功能、重构架构或重新解释产品方向。

---

## 9. 旧团队后续响应方式

旧团队转为技术资产支持组，保持 parked。

后续只在新团队提出明确问题时响应：

- 指出代码位置。
- 解释已有实现。
- 修复明确的既有缺陷。
- 提供验证证据。
