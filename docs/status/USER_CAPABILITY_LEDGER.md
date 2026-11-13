# 用户能力总账（User Capability Ledger）

> 不按模块、Commit、Gate 汇报，按用户真实能力。任何能力没有「用户入口 → 真实执行 → 可查看结果」，不得称为已完成。
> 
> 最后更新：2026-07-23 | 维护人：齐活林（Delivery Director）
> 版本：v1.7（前端产品动线重校；项目负责人工作台第一纵向切片 PASS；旧 Project Runtime Local 降级为内部证据页）

---

## 能力成熟度定义

| 等级 | 含义 | 判断标准 |
|------|------|---------|
| 设计中 | 有设计文档/ADR，无代码 | 无 API/CLI/前端入口，无测试 |
| 技术存在 | 有实现代码，有测试 | 有 API/类/模块，但**用户没有稳定操作入口**（仅有内部调用/手动 SQL/临时脚本） |
| 演示可用 | 有对外入口，Demo 可跑 | 有 API/CLI，但依赖 mock 数据/特殊环境/人工准备，非自持 |
| 自用可用 | 自己日常可用，不需 mock | 从入口到执行到结果查看**全真实路径**，可在本机稳定复现 |
| 对外可用 | 对外发布，文档齐全 | 有文档/错误处理/版本兼容/可部署，外部用户可自主使用 |

## 本次进度校准（2026-07-23）

| 能力 | 真实状态 | 结论 | 核心证据 |
|---|---|---|---|
| 项目负责人工作台第一纵向切片 | 用户可通过本机 Google 登录进入项目负责人工作台，使用聊天式目标或结构化任务入口，看到同一结构化确认单，确认生成计划，启动运行，查看真实结果解释，并批准成果或“修改目标并继续” | **自用可用 / local-only** | `b349b4367e2002f3702ffd788162c477015a2c4f`；`issues/20260723_project_owner_workbench_product_flow.md`；Chrome 真链：双入口 -> 同一确认单 -> 运行 `7 passed` / `exit0` / `round1` -> trace -> 批准 -> 继续修改 |
| Project Runtime Local 证据页 | 可显示项目、运行状态、Task/Graph 和部分运行证据 | **内部证据页，不算产品完成** | 旧 Issue `issues/20260722_macos_keychain_google_oidc_project_runtime.md` 已改为 `PRODUCT_MISMATCH / PARTIAL` |
| RealRD 研发闭环 | API / CLI 已读代码、改代码、跑测试、交付 diff | **自用可用，但当前暂停让位于前端产品动线** | `60e3989f`、`6f91353b`、`test_rd_workflow_real_rd.py` 11 passed |
| D1 工具链 | 容器内可构建、非冻结路由进入 execute、`/health=200` | **演示可用；不作为当前产品主线** | `reviews/20260719_d1_unfreeze_qa.md` 16 passed，真实模型结果仍需受控网关凭据 |
| Agent 内核 / BudgetGuard / 治理闸 | 实现和测试存在，但默认关闭 | **技术存在** | 各自 focused 测试；未作为日常执行默认路径 |
| CEO 运行证据 SPA | 6 个只读端点和 7 页面可查看真实聚合数据 | **自用可用，但偏证据视角** | `b025236f`、24/24 后端测试、Vite build 通过 |

### 本轮产品口径

从 2026-07-23 起，能力总账按“用户能否在浏览器完成一件真实事情”计账。

不再把接口数量、测试数量、表数量、Gate 数量、容器诊断或内部 Review 当作主要产品进度。它们只能作为工程证据。

项目负责人工作台的完成标准是：

```text
进入项目
-> 与项目负责人沟通目标，或直接填写结构化任务
-> 进入同一结构化任务确认单
-> 用户确认后生成计划并启动
-> 查看员工/Workflow 进度、成果、成本、风险
-> 批准、返工、暂停或继续修改目标
```

---

## 目录

- [A. 账本通览（速查表）](#a-账本通览速查表)
- [B. 资产工厂 / 平台管理（Admin）](#b-资产工厂--平台管理admin)
- [C. Workspace 运行（Company → 部门 → 员工 → 项目）](#c-workspace-运行company--部门--员工--项目)
- [D. 能力与凭证管理](#d-能力与凭证管理)
- [E. 内容发布与结果查看](#e-内容发布与结果查看)
- [F. 研发工具链（内部/DevOps）](#f-研发工具链内部devops)
- [G. 已冻结 / L2 Gate 能力（存在但不使用）](#g-已冻结--l2-gate-能力存在但不使用)
- [H. 用户验收场景（UAT）](#h-用户验收场景uat)（含 H.6 CEO Office SPA、H.7 B 层治理全链路）
- [I. 已知限制](#i-已知限制)
- [J. 运行时引擎与治理管控（本会话新增）](#j-运行时引擎与治理管控本会话新增)

---

## A. 账本通览（速查表）

| # | 能力 | 用户入口 | 执行真实度 | 结果可查 | 成熟度 | L2 冻结？ |
|---|------|---------|-----------|---------|--------|----------|
| P1 | 项目负责人工作台第一纵向切片 | 前端项目页（本机 Google 登录后进入） | ✅ 双入口 -> 同一确认单 -> 启动 -> 结果 -> 批准/继续 | 前端页面 + trace/artifact | **自用可用 / local-only** | 否 |
| P0 | Project Runtime Local 证据页 | 旧项目运行页 | ⚠️ 可查运行证据，但不是产品入口 | 前端页面 | 内部证据页 | 否 |
| A1 | 浏览部门类型目录 | API `/api/catalog/department-types` | ✅ 真实查询 DB seed | API 返回 | 自用可用 | 否 |
| A2 | 管理部门类型（增删改） | API `/api/platform/department-types/*` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A3 | 浏览模型目录 | API `/api/platform/models`, `/api/catalog/models` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| A4 | 管理模型（增改） | API `/api/platform/models/*` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A5 | 浏览网关配置 | API `/api/platform/gateways`, `/api/catalog/gateways` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| A6 | 管理网关（增改） | API `/api/platform/gateways/*` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A7 | 浏览官方能力目录 | API `/api/catalog/capabilities` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| A8 | 管理官方能力（增改） | API `/api/platform/capabilities/*` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A9 | 浏览/管理连接器 | API `/api/catalog/connectors`, `/api/connectors` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| A10 | 浏览/管理工具目录 | API `/api/catalog/tools`, `/api/platform/tools` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| A11 | 浏览/管理工作流模板 | API `/api/platform/workflows` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| A12 | 浏览/管理 Persona | API `/api/platform/personas` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A13 | 浏览/管理仪表盘 | API `/api/platform/dashboards` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A14 | 浏览/管理公司包 | API `/api/platform/company-packages/*` | ✅ 真实 CRUD + instantiate | API + DB | 自用可用 | 否 |
| A15 | 浏览/管理公司模板 | API `/api/platform/company-templates` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A16 | 浏览/管理部门模板 | API `/api/platform/department-templates` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A17 | 浏览/管理员工模板 | API `/api/platform/employee-templates` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A17 | 浏览/管理员工模板 | API `/api/platform/employee-templates` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A17b | devops_engineer 员工模板 | seed 预置 `et_devops_engineer` | ✅ seed 幂等 | DB | 自用可用 | 否 |
| A18 | 浏览/管理策略护栏 | API `/api/platform/policies` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| A19 | 浏览 Tenants | API `/api/platform/tenants/*` | ✅ 真实查询 | API + DB | 自用可用 | 否 |
| A20 | R&D 部门模板 | seed 预置 `dt_rd_department`（含 tech_lead/backend_engineer/qa_engineer/devops_engineer） | ✅ seed 幂等，含默认 workflow `wt_rd_pipeline` | DB + API 查询 | 自用可用 | 否 |
| B1 | 创建/查看 Company | API `/api/workspace/companies/*` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| B2 | 创建/查看部门 | API `/api/workspace/departments/*` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| B3 | 创建/查看员工 | API `/api/workspace/employees/*` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| B4 | 给员工分配能力/技能/工具 | API `/api/workspace/employees/{id}/capabilities`, `/skills`, `/tools` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| B5 | 浏览/管理部门激活状态 | API `/api/workspace/departments/activation` | ✅ 真实查询 | API + DB | 自用可用 | 否 |
| B6 | 创建/查看项目 | API `/api/workspace/projects/*` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| B7 | 发布 Task 给员工 | API `/api/task` (POST) | ✅ 真实执行 | API + DB | 自用可用 | 否 |
| B8 | 运行 Task | API `/api/task/{id}/run` (POST) | ✅ 真实执行 | API 返回 | 自用可用 | 否 |
| B9 | 查看 Task 状态/追踪 | API `/api/task/{id}`, `/trace` (GET) | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| B10 | 查看 Workflow 详情 | API `/api/workspace/workflows/{id}` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| B11 | 运行 Workflow 下一步 | API `/api/workspace/workflows/{id}/run-next-step` | ✅ 真实执行 | API + DB | 自用可用 | 否 |
| B12 | 管理模型偏好 | API `/api/workspace/model-preference` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| B13 | 管理私有能力(模型/工具/连接器) | API `/api/workspace/private-models`, `-tools`, `-connectors`, `capabilities/private` | ✅ 真实 CRUD | API + DB | 自用可用 | 否 |
| B14 | 管理凭证（Secret Vault） | API `/api/workspace/credentials/*` + 前端 `/control/secret-vault` | ✅ 真实 CRUD + test | API + DB + 前端 | **自用可用** | 否 |
| B15 | CEO 全局概览 | API `/api/ceo/overview` + 前端 `/ceo-office` | ✅ 真实查询 | API + 前端 | **自用可用** | 否 |
| B16 | 看结果摘要 | API `/api/results/summary`, `publish-packages`, `content-workflow-runs` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| C1 | 运行内容工作流 | API `/api/content-workflow/run` | ✅ 真实执行 | API 返回 | 自用可用 | 否 |
| C2 | 导出发布包 | API `/api/publish-package/export` | ✅ 真实导出 | API 返回 | 自用可用 | 否 |
| D1 | 看资产 Dashboard | 前端 `/platform/` | ❌ 页面存在但内容待填充 | 前端 | 演示可用 | 否 |
| D2 | 看资产完成度 | 无独立入口（seed 内嵌自检） | ⚠️ 技术存在，无用户入口 | 仅 seed 日志 | 技术存在 | 否 |
| E1 | 本地一键复跑真实研发闭环 | CLI `backend/scripts/run_real_rd.py` | ✅ 真实网关执行 | CLI stdout | 自用可用 | 否 |
| E2 | 真实研发闭环（AI读→改→测→交付Diff） | API `POST /api/workspace/rd-workflow/run` + CLI | ✅ 真实全链，已用 2 个 Issue 证明 | stdout + git diff | **自用可用** | 否 |
| E3 | D1 execute（受控执行 + 错误分类 + 降级三态） | API `POST /api/task/{id}/run`（内嵌） | ✅ 容器工具链真实解冻，路由可进入 execute | API + DB + d1_execution_log | **演示可用** | 否 |
| E4 | 进化事件审计 | API `/api/evolution-events` | ✅ 真实查询 | API 返回 | 自用可用 | 否 |
| E5 | 运行前置校验/合入检查 | CLI `backend/scripts/pre_merge_check.py` | ✅ 真实运行 | CLI stdout | 自用可用 | 否 |
| E6 | 研发后端统一接口（DevAgent 协议，6 后端可切换） | `RealRDExecutor(model=...)` 代码层注入 | ⚠️ 协议和降级已测；仅 ModelGateway 路径完成真实闭环 | 单测 + 代码审查 | 技术存在 | 否 |
| F1 | 多租户 Tenant 管理 | API `/api/platform/tenants/*` | ⚠️ 存在但冻结 | API + DB | 技术存在 | ✅ 是 |
| F2 | 计费管理（Plan/Pricing/Quota/Billing） | API `/api/platform/plans/*` 等 | ⚠️ 存在但冻结 | API + DB | 技术存在 | ✅ 是 |
| F3 | Usage 计量 | API `/api/platform/usage*` | ⚠️ 存在但冻结 | API + DB | 技术存在 | ✅ 是 |
| F4 | 商业配置/Commercial | 前端 `/platform/commercial/` | ⚠️ 页面存在，内容待定 | 前端 | 演示可用 | ✅ 是 |
| **N1** | **B 层治理闸引擎** | 内嵌于 `runtime_governance.evaluate()` + `gate_prompt.py` G1-G4 | ⚠️ 实现与测试存在，默认关闭 | 事件日志 + 决策落库 | 技术存在 | 否 |
| **N2** | **决策落库（A/B/C/D 待拍板）** | `decision_sink.PendingDecisionStore`，经 CEO Office 前端 `待拍板决策` 页 | ✅ 真实持久化到独立 sqlite | 前端审批卡 + API | **自用可用** | 否 |
| **N3** | **Agent 执行内核** | 内嵌于 `real_rd_executor.py`（default-off `agent_kernel_enabled=False`） | ⚠️ 41 测试全绿，默认关闭 | `agent_execution_claims` / `agent_task_sessions` / `agent_wakeup_requests` 表 | 技术存在 | 否 |
| **N4** | **预算硬停（BudgetGuard）** | 内嵌于 `real_rd_executor.py`（default-off `budget_enabled=False`） | ⚠️ 20+ 测试全绿，默认关闭 | 软提醒 + 硬暂停 | 技术存在 | 否 |
| **N5** | **CEO 运行证据（只读聚合 API + Vite SPA 前端）** | 后端 `GET /api/ceo/evidence/*`（6 端点）+ 前端 `frontend/ceo-evidence/` Vite SPA | ✅ 真实只读聚合，跨 A/C/B 层事件 | 前端 7 页面（概览/时间线/组织树/待拍板决策/执行状态/预算状态） | **自用可用** | 否 |

---

## B. 资产工厂 / 平台管理（Admin）

### B.1 浏览部门类型目录

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 查看所有预置部门类型（tech.rd, content.growth, design.ux 等）及其元数据 |
| **从哪里操作** | `GET /api/catalog/department-types`（公开目录）；`GET /api/platform/department-types`（管理端） |
| **最终得到什么** | 部门类型列表：`type_key`, `category`, `display_name`, `description`, `manifest` |
| **结果在哪里查看** | API 返回 JSON（如 `curl localhost:8000/api/catalog/department-types`） |
| **当前属于** | **自用可用** — seed 数据随 DB 启动加载到 `department_catalog` 表，API 直接查询 |
| **当前限制** | 无前端 UI 管理页面；仅通过 API/CURL 操作；seed 数据约 10 种部门类型 |
| **证据** | `database.py L1237-1249` seed 调用；`main.py L1578-1585` API 实现；`test_d1_execute.py` 中有测试覆盖 |

### B.2 管理部门类型（CRUD）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 新增、编辑、启用/停用、删除部门类型 |
| **从哪里操作** | `POST /api/platform/department-types`（创建）；`PUT /api/platform/department-types/{key}`（编辑）；`DELETE /api/platform/department-types/{key}`（删除） |
| **最终得到什么** | 新增/更新后的部门类型记录 |
| **结果在哪里查看** | API 返回 + DB `department_catalog` 表 |
| **当前属于** | **自用可用** — 完整 CRUD + `approved_by` 门控 |
| **当前限制** | `approved_by` 字段当前为占位符（human-approval gate 未接入）；无前端 UI |
| **证据** | `main.py L2300-2355` API 实现；`database.py L1706` seed；测试散见各集成测试 |

### B.3 浏览模型目录

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 查看所有官方模型的元数据（provider_id, display_name, supported_models, status 等） |
| **从哪里操作** | `GET /api/platform/models`（管理端）；`GET /api/catalog/models`（目录端） |
| **最终得到什么** | 模型列表，含 gateway_ref, default_model, status |
| **结果在哪里查看** | API 返回 JSON |
| **当前属于** | **自用可用** |
| **当前限制** | seed 数据默认含 10+ 种模型（deepseek-v4-pro, gpt 系列等）；无前端 UI |
| **证据** | `database.py L1743` seed；`main.py L2706-2749` API |

### B.4 管理模型（增改）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 新增模型目录条目、启用/停用模型 |
| **从哪里操作** | `POST /api/platform/models`（创建）；`PUT /api/platform/models/{key}`（启用/停用） |
| **最终得到什么** | 新增/更新后的模型记录 |
| **结果在哪里查看** | API + DB `official_model_catalog` 表 |
| **当前属于** | **自用可用** |
| **当前限制** | 无前端 UI；auth_type 仅形状占位（none / oauth / apikey），不存真实凭证 |
| **证据** | `main.py L2713-2749` API |

### B.5–B.7 网关 / 能力 / 工具 / 连接器

（模式类似 B.1–B.4：seed 数据 + CRUD API + 无前端 UI，自用可用。）

### B.14 浏览/管理公司包 + 实例化

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 查看预置公司包列表、创建公司包、实例化公司包（创建一家完整 Company） |
| **从哪里操作** | `GET /api/platform/company-packages`（列表）；`POST /api/platform/company-packages`（创建）；`POST /api/platform/company-packages/{id}/instantiate`（实例化） |
| **最终得到什么** | 公司包记录；实例化后得到一个完整 Company（含部门、员工、模板） |
| **结果在哪里查看** | API + DB `company_packages` 表；实例化后 companies 表 |
| **当前属于** | **自用可用** — `instantiate` 已实现为公司创建流程 |
| **当前限制** | 实例化目前仅支持 `selfuse` tenant；无前端 UI；实例化后不可撤销 |
| **证据** | `main.py L2383-2431` API；`database.py L2846` seed；`company_instantiation.py` 实现 |

---

## C. Workspace 运行（Company → 部门 → 员工 → 项目）

### C.0 项目负责人工作台

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 登录后进入项目，以聊天式目标或结构化任务两种方式提出下一步；看到同一结构化确认单；确认后生成计划并启动；查看结果解释；批准成果或修改目标继续 |
| **从哪里操作** | 本机 Google OIDC 登录后的项目负责人工作台页面 |
| **最终得到什么** | 新一轮项目计划、运行结果、trace/artifact、结果解释和继续动作 |
| **结果在哪里查看** | 前端页面；Task/Graph 只放在折叠证据区，不作为普通用户主语言 |
| **当前属于** | **自用可用 / local-only** — 第一纵向切片已通过 |
| **当前限制** | 仍是本机开发链路；员工未分配时必须如实显示；成本缺失显示“未记录”，不能伪造 0；模型、RealRD、凭据配置不在本切片内 |
| **证据** | `issues/20260723_project_owner_workbench_product_flow.md`；SHA `b349b4367e2002f3702ffd788162c477015a2c4f`；Chrome 真链：双入口 -> 同一确认单 -> 运行 `7 passed` / `exit0` / `round1` -> trace -> 批准 -> 继续修改 |

### C.1 创建/查看 Company

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 创建新的 AI Company、查看现有 Company 详情、编辑基本信息 |
| **从哪里操作** | `GET /api/workspace/companies`（列表）；`POST /api/workspace/companies`（创建，`status_code=201`）；`GET /api/workspace/companies/{id}`（详情）；`PATCH /api/workspace/companies/{id}`（编辑） |
| **最终得到什么** | Company 记录（含 id, name, tenant_id, company_template_id 等） |
| **结果在哪里查看** | API 返回 JSON |
| **当前属于** | **自用可用** — 完整 CRUD |
| **当前限制** | 创建需指定 company_template_id（模板预置）；单 tenant（selfuse）；无 L5/L6 经济系统 |
| **证据** | `main.py L1911-1936` API；`company_instantiation.py` 实现；散见集成测试 |

### C.2–C.5 部门 / 员工 / 项目（模式类似 C.1，CRUD 完整）

| 能力 | 入口 | 成熟度 |
|------|------|--------|
| 创建/查看部门 | `GET/POST /api/workspace/departments`, `GET/PATCH/DELETE /api/workspace/departments/{id}` | ✅ **自用可用** |
| 创建/查看员工 | `GET/POST /api/workspace/employees`, `PATCH/DELETE /api/workspace/employees/{id}` | ✅ **自用可用** |
| 给员工分配能力/技能/工具 | `GET/PUT /api/workspace/employees/{id}/capabilities`, `/skills`, `/tools` | ✅ **自用可用** |
| 创建/查看项目 | `GET/POST /api/workspace/projects`, `GET/PATCH /api/workspace/projects/{id}` | ✅ **自用可用** |
| 给项目添加 Task | `POST /api/workspace/projects/{id}/tasks` | ✅ **自用可用** |

**限制**：均无前端 UI，仅 API 操作；Employee CRUD 端点被铁律禁止真实多 Agent 交互（仅数据库层 CRUD）。

### C.6 发布 Task 给员工并运行

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 向公司某位 AI Employee 发布任务（task）、启动执行、查看执行结果 |
| **从哪里操作** | `POST /api/task`（创建 task）；`POST /api/task/{id}/run`（启动执行）；`GET /api/task/{id}`（查状态）；`GET /api/task/{id}/trace`（查追踪） |
| **最终得到什么** | task 执行结果（含 output, evolution-decisions, meta-development） |
| **结果在哪里查看** | API 返回 JSON；`GET /api/task/{id}/workflow` 看 Workflow；`GET /api/task/{id}/evolution-decisions` 看演化决策 |
| **当前属于** | **自用可用** — 完整 Task -> Employee -> Execution 路径 |
| **当前限制** | 无前端 UI；需员工已创建并分配了能力；执行依赖真实网关模型可达 |
| **证据** | `main.py L1509-1569` API；`orchestrator.py` 编排实现；`test_d1_execute.py` 31 passed（含集成测试） |

### C.7 管理凭证（Secret Vault）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 新增、查看、编辑、测试、禁用、删除凭证（API Key / Token，用于外部服务调用） |
| **从哪里操作** | 前端 `/control/secret-vault` + API `GET/POST /api/workspace/credentials`, `PUT/DELETE /api/workspace/credentials/{id}`, `POST test/disable` |
| **最终得到什么** | 凭证记录（元数据 + 加密存储）；测试结果（连通性验证） |
| **结果在哪里查看** | 前端页面可视化；API 返回 |
| **当前属于** | **自用可用** — 有独立前端页面 + 完整 CRUD + 测试验证 |
| **当前限制** | 凭证仅存储 digest/元数据（实际凭证由外部密钥托管/Resolver）；`credential_id` 为 UUID，手动关联到能力；无批量操作 |
| **证据** | `frontend/app/control/secret-vault/page.js` 前端；`main.py L1654-1703` API；`credential_vault.py` 实现；集成测试覆盖 |

### C.8 CEO 全局概览（升级版：只读聚合 API + Vite SPA）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 一站式查看公司/Agent/预算/治理全方位运行证据：概述计数、执行/预算/治理三层时间线、组织树、待 A/B/C/D 拍板决策、A 层执行锁/会话、C 层预算累加器 |
| **从哪里操作** | **新版 Vite SPA**：`cd frontend/ceo-evidence && npm run dev` → `http://localhost:5173`（7 页面）；**后端 API**：`GET /api/ceo/evidence/overview`, `/timeline`, `/org-tree`, `/pending-decisions`, `/execution`, `/budget`；**旧版（保留）**：前端 `/ceo-office` + `GET /api/ceo/overview` |
| **最终得到什么** | 全局状态仪表盘（实时、只读、脱敏），含运行证据时间线、组织树展开、审批卡 |
| **结果在哪里查看** | 新版 Vite SPA 前端可视化；旧版 `/ceo-office` 保留 |
| **当前属于** | **自用可用** — 6 只读端点 + 7 页面 SPA；24/24 后端测试全绿；Vite build 成功 |
| **当前限制** | 数据限于当前 tenant（selfuse）；Dashboard widget 数据部分为 seed 占位，未完全真实化；只读展示，不含 approve/resolve 写操作 |
| **证据** | `backend/app/ceo_evidence_api.py` + `frontend/ceo-evidence/` + `backend/tests/test_ceo_evidence_api.py` 24 passed + `b025236f` 提交

### C.9 Workflow 运行

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 创建 Workflow 运行、查看运行状态、执行下一步 |
| **从哪里操作** | `POST /api/workspace/workflows`（创建运行）；`GET /api/workspace/workflows/{id}`（状态）；`POST /api/workspace/workflows/{id}/run-next-step`（执行） |
| **最终得到什么** | Workflow 运行记录（含当前步骤、状态、结果） |
| **结果在哪里查看** | API 返回 JSON |
| **当前属于** | **自用可用** — 完整 Create → Run → Status 路径 |
| **当前限制** | run-next-step 为单步执行（非全自动编排）；无前端 UI；workflow 模板需预置 |
| **证据** | `main.py L2022-2076` API；`workflow_runtime.py` 实现 |

### C.10 结果与发布查看

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 查看内容工作流运行结果、发布包列表、结果摘要 |
| **从哪里操作** | `GET /api/results/summary`, `/api/results/publish-packages`, `/api/results/content-workflow-runs` |
| **最终得到什么** | 运行统计（completed/failed 数量）、发布包列表 |
| **结果在哪里查看** | API 返回 JSON |
| **当前属于** | **自用可用** |
| **当前限制** | 无前端 UI；数据依赖于内容工作流实际执行过 |
| **证据** | `main.py L3316-3363` API |

---

## D. 能力与凭证管理

（大部分能力已在前述 Workspace 部分覆盖，此处补充私有能力管理）

### D.1 管理私有能力（模型/工具/连接器）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 在 Workspace 级别注册/查看/删除私有模型、工具、连接器（非官方预置的） |
| **从哪里操作** | `GET/POST /api/workspace/private-models`, `private-tools`, `private-connectors` |
| **最终得到什么** | 私有能力记录 |
| **结果在哪里查看** | API 返回 JSON |
| **当前属于** | **自用可用** |
| **当前限制** | 无前端 UI；私有能力需关联凭证才能真实调用；不可与官方能力重名 |
| **证据** | `main.py L1732-1848` API |

### D.2 选择器（Selector）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 获取所有可用能力（官方+私有）的选择器列表，包含能力 ID/类型/标签/启用状态 |
| **从哪里操作** | `GET /api/workspace/capabilities/selector` |
| **最终得到什么** | 可用于前端下拉框的能力列表 |
| **结果在哪里查看** | API 返回 JSON |
| **当前属于** | **自用可用** |
| **当前限制** | 被设计为前端控件的数据源，当前前端布局暂停开发 |
| **证据** | `main.py L1850-1878` API |

---

## E. 内容发布与结果查看

### E.1 运行内容工作流

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 启动一次内容工作流执行（如文章生成、多平台发布） |
| **从哪里操作** | `POST /api/content-workflow/run` |
| **最终得到什么** | 工作流运行记录（run_id, status），执行后结果写入 result_store |
| **结果在哪里查看** | API 返回 run_id；后续可通过 `/api/results/content-workflow-runs` 查看 |
| **当前属于** | **自用可用** |
| **当前限制** | 需要员工+能力+凭证齐备方可成功；无前端触发入口 |
| **证据** | `main.py L3296-3314` API；`content_publish_package.py` 模型 |

### E.2 导出发布包

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 将工作流产物导出为可发布的包格式 |
| **从哪里操作** | `POST /api/publish-package/export` |
| **最终得到什么** | 发布包导出（含 artifacts, brand_voice_ref, platforms_targeted） |
| **结果在哪里查看** | API 返回 JSON |
| **当前属于** | **自用可用** |
| **当前限制** | 导出路径为 direction③ 兜底/自动发布前置；无前端触发入口 |
| **证据** | `main.py L3219-3247` API；`content_publish_package.py` 实现 |

---

## F. 研发工具链（内部/DevOps）

### F.1 真实研发闭环（AI 读→改→测→交付 git diff）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 对一个真实代码 Issue，让系统自动完成「读取代码 → 生成修改方案 → 应用 diff → 跑测试验证 → 交付 git diff」的全链闭环 |
| **从哪里操作** | CLI `backend/scripts/run_real_rd.py --issue-spec <path>`；API `POST /api/workspace/rd-workflow/run` |
| **最终得到什么** | `status=succeeded`, `rounds`, `test_exit_code=0`, `diff_text`（含 `--- a/ +++ b/`） |
| **结果在哪里查看** | CLI stdout；API 返回 |
| **当前属于** | **自用可用** — 已用 2 个真实 Issue（易 A + 中 B）证明；已集成到研发部工作流（通过 `/api/workspace/rd-workflow/run` 自动触发） |
| **当前限制** | 依赖本地 New API 网关可达（`http://127.0.0.1:3000`, `deepseek-v4-pro`）；当前以 OFF 模式直跑（sandbox-exec 不可用）；max_rounds 默认 5 轮，模型偶发 diff_context_mismatch 需重试吸收 |
| **证据** | `real_rd_executor.py`；真实网关证明 Issue A rounds=3、B rounds=2，均 succeeded；`test_rd_workflow_real_rd.py` 11 passed；提交 `f5378fa6` / `60e3989f` / `6f91353b`；全量 768 passed、6 sandbox 限制、2 skipped |

### F.2 本地一键复跑 CLI

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 用一条命令对任意 Issue 跑真实研发闭环，无需记忆 env 加载 |
| **从哪里操作** | `backend/scripts/run_real_rd.py --issue-spec <path> [--no-sandbox] [--max-rounds 5]` |
| **最终得到什么** | 同上 |
| **结果在哪里查看** | CLI stdout；diff 同时写入文件 |
| **当前属于** | **自用可用** |
| **当前限制** | 同上；需显式指定 Issue spec 文件（未集成到 Issue 队列自动调度） |
| **证据** | `backend/scripts/run_real_rd.py` 实现；QA 用此脚本跑通 A/B 两个 Issue |

### F.3 研发部工作流（自动触发 RealRDExecutor）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 创建一个研发部（`dt_rd_department`），添加员工，然后通过 API 触发一次完整研发工作流——工作流会自动识别 code_change 步骤、调用 RealRDExecutor 做真实代码修改、跑测试、交付 diff，其余步骤走模型文本生成 |
| **从哪里操作** | API `POST /api/workspace/rd-workflow/run`（`department_id`, `workflow_content_id`, `prompt`） |
| **最终得到什么** | 工作流运行记录（`workflow_run_id`、`status`、`steps` 数组），编码步骤的 output 含 RealRDExecutor 执行摘要 |
| **结果在哪里查看** | API 返回 JSON；DB `workflow_runs` / `workflow_steps` / `step_results` 表 |
| **当前属于** | **自用可用** — QA 10/10 端到端验证，覆盖正向/失败/降级三条路径 |
| **当前限制** | 依赖真实网关可达；department 须先通过 API 创建实例；workflow_content 须指向 `wt_rd_pipeline`；编码步骤 target 可从 prompt 提取或通过 `issue_spec_override` 传入（不再硬编码 target_a.py）；`RealRDExecutor` 的 `model` 参数须为 `DevAgent` 协议实现（4 后端可切换，见 F.8） |
| **证据** | `rd_workflow_runtime.py` `_execute_step` 第四分支（real_rd）+ `_build_issue_spec` 修复（commit `b40f5241`，仅含 `code_change_spec` 的步骤触发 real_rd，override 不再误用至非编码步骤）；`test_rd_workflow_real_rd.py` 11 passed；`tools/rd_dept_proof.py` 端到端证明步骤 3 真实改写 target_a.py（`BETA=2→3`） |

### F.4 D1 execute（受控执行 + 错误分类 + 降级三态）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 在受控闸门下执行 AI 任务（错误分类四类 + 降级三态 D/F/R + 执行日志落库） |
| **从哪里操作** | 内嵌于 `POST /api/task/{id}/run`；独立 `GET /api/workspace/internal/d1-tenant-reservation/status` 查看状态 |
| **最终得到什么** | 执行结果 + 执行日志（`d1_execution_log` 表） |
| **结果在哪里查看** | API 返回 + DB `d1_execution_log` 表 |
| **当前属于** | **演示可用** — 非冻结容器可构建真实 `D1SingleModelToolchain`，路由到达 `execute()` 且不再是 503 |
| **当前限制** | 完整 `.execute() → status=succeeded` 仍依赖受控 R3 模型网关凭据 / 网络，尚未作为真实模型调用验收；无前端 UI |
| **证据** | `d1_execute.py`, `d1_gateway_client.py`, `d1_config.py`；`reviews/20260719_d1_unfreeze_qa.md`（16 passed、`/health=200`、E2E 1/1 工具链解冻） |

### F.5 Sandbox 三态模式（AUTO/OFF/ENFORCE）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 控制 `LocalRDToolset.run_test` 是否使用 `sandbox-exec` 网络隔离 |
| **从哪里操作** | 环境变量 `CURIS_RD_SANDBOX`（auto/off/enforce）；或构造参数 `LocalRDToolset(..., sandbox_mode=SandboxMode.OFF)` |
| **最终得到什么** | run_test 在 sandbox-exec 可用时走网络隔离，不可用时降级直跑（OFF/AUTO）或拒绝（ENFORCE） |
| **结果在哪里查看** | 测试结果 + 审计日志含 `sandbox_degraded` 字段 |
| **当前属于** | **自用可用** — 单测全覆盖（5 passed），真实环境以 OFF 直跑验证通过 |
| **当前限制** | OFF/AUTO 缺失态失去网络隔离，仅限受信环境；文档已标注红线 |
| **证据** | `local_rd_toolset.py` `SandboxMode` 枚举 + 三分支 run_test；`test_local_rd_toolset_sandbox.py` 5 passed |

### F.6 进化事件审计

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 查看系统进化/执行/审计事件流 |
| **从哪里操作** | `GET /api/evolution-events` |
| **最终得到什么** | 事件列表（含 correlation_id, event_type, timestamp, payload） |
| **结果在哪里查看** | API 返回 JSON |
| **当前属于** | **自用可用** |
| **当前限制** | 仅最近事件；无前端可视化；无搜索/过滤 |
| **证据** | `main.py L1572` API；`evolution_event_log.py` 实现 |

### F.7 合入前置检查

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 在合入前自动检查工作树、测试、冲突、受保护文件等 5 项条件 |
| **从哪里操作** | `backend/scripts/pre_merge_check.py` |
| **最终得到什么** | 检查通过（exit 0）或失败报告（exit 非 0，含具体阻却项） |
| **结果在哪里查看** | CLI stdout |
| **当前属于** | **自用可用** |
| **当前限制** | 仅自动化 5 项检查，仍需人工核对 diff 边界 |
| **证据** | `backend/scripts/pre_merge_check.py` 实现 |

### F.8 研发后端统一接口（DevAgent 协议 + 6 后端可切换）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 将 `RealRDExecutor` 的底层开发 Agent 从「New API 模型网关」切换到任意兼容后端（Claude Code / OpenAI Codex / WorkBuddy / 其他），无需改动 `RealRDExecutor` 编排逻辑 |
| **从哪里操作** | 代码层：`RealRDExecutor(model=<DevAgent 实例>, ...)`；可选后端：`ClaudeCodeAdapter(...)` / `OpenAICodexAdapter(...)` / `WorkBuddyAdapter(...)` / `CodexAgentAdapter(...)` / `WorkBuddyAgentAdapter(...)` / `ModelGatewayAdapter(...)`（已有） |
| **最终得到什么** | 任意后端按统一 `{output, total_tokens, estimated_cost, model_gateway_id, model_name, status}` 格式返回开发结果，由 `RealRDExecutor` 统一编排 |
| **结果在哪里查看** | 同 F.1/F.3（`RealRDExecutor` 输出 + git diff），后端无关 |
| **当前属于** | **技术存在** — DevAgent Protocol、6 个适配器与 44 个协议 / 降级测试存在；仅 ModelGatewayAdapter 已完成真实研发闭环 |
| **当前限制** | ① `ModelGatewayAdapter` 后端做过真实网关往返（F.1/F.3 已验证）；② `ClaudeCodeAdapter` / `OpenAICodexAdapter` 为 OpenAI 兼容 chat 调用（非 Codex 原生 agent），仅验证「协议满足 + 无 key 降级」，尚未用真实 API key 实跑研发闭环（待用户提供 key）；③ `WorkBuddyAdapter` 的 SDK 路径依赖 `codebuddy_agent_sdk` 包，不可用时自动降级 CLI（`codebuddy run`）——**实测该 CLI 调法已失效**（`codebuddy` 无 `run`/`--agent`/`--prompt-file` 子命令），仅 SDK 路径可能可用且 SDK 包未装；④ `CodexAgentAdapter` 为**真·Codex agent 后端**——已单测验证「命令构造 + git diff 捕获 + 4 类降级 + 执行器 agent 分支跳过 diff apply 改用 git checkout 回滚」，但**尚未用真实 `codex` CLI 实跑一轮研发闭环**（环境已装且已登录，待一次真实验证）；⑤ `WorkBuddyAgentAdapter` 为**真·WorkBuddy agent 后端**——已单测验证「`-p --permission-mode` 命令构造 + 无 `CODEBUDDY_API_KEY` 降级 `no_api_key` + 4 类降级 + 执行器 agent 分支复用（跳过 diff apply、git checkout 回滚）」，**但不能开箱免 key**（实测无 key/假 key 均卡住超时，CLI 无 login 持久化），**必须配 `CODEBUDDY_API_KEY` 才能实跑**（待用户提供 key 后做真实验证） |
| **证据** | `backend/app/dev_agent.py`（DevAgent Protocol + ClaudeCodeAdapter + OpenAICodexAdapter + WorkBuddyAdapter + CodexAgentAdapter + WorkBuddyAgentAdapter）；`backend/app/real_rd_executor.py` L29 `from .dev_agent import DevAgent`、L101 `model: DevAgent`、L189 `is_agent = getattr(self.model, "mutates_filesystem", False)`、L558 `_build_agent_prompt`、L584 `_make_agent_rollback`；`backend/tests/test_dev_agent.py` **10 passed** + `backend/tests/test_codex_agent_backend.py` **16 passed** + `backend/tests/test_workbuddy_agent_backend.py` **18 passed**（共 44 passed，含端到端断言：`_apply_diff_transactional` 在 agent 模式**未被调用**、测试失败时 `git checkout -- <target>` 回滚被触发），纯离线 `unittest.mock` 验证 |

---

## J. 运行时引擎与治理管控（本会话新增）

### J.1 B 层治理闸引擎（Runtime Governance）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 在执行每个真实研发 Task 前，自动经过 4 道守卫闸评估 → 需要用户拍板时自动生成待决策落库 → 用户通过 CEO Office 审阅并拍板 A/B/C/D |
| **从哪里操作** | 全自动：`runtime_governance.evaluate()` 在 `real_rd_executor.py` 执行前调用；用户通过 CEO Office 前端「待拍板决策」页审阅 |
| **最终得到什么** | 每个 Task 执行时自动经过 `G1-deploy / G2-reputation / G3-data / G4-token+budget` 守卫评估；需人工拍板时 → `PendingDecisionStore` 持久化 → 前端展示 |
| **当前属于** | **技术存在** — 独立闸引擎、4 道提示词门、决策持久化与脱敏事件追踪均已实现并有 26+ 测试覆盖，但默认关闭，尚未形成日常用户执行入口 |
| **当前限制** | 当前 default-off（`enabled=False`），需在 `real_rd_executor.py` 接线点开启；决策审批功能仅展示待拍板，不含 resolve/approve 写操作（属未来任务） |
| **证据** | `runtime_governance.py` / `gate_prompt.py` / `decision_sink.py`；`test_b_layer_runtime_governance.py` 29 passed；`test_b_layer_gate_prompt.py` 测试覆盖 |

### J.2 Agent 执行内核（Execution Kernel）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 保证 Agent 运行不被重复执行、运行会话可持久化与续接、运行配置指纹防止旧配置续跑、进程崩溃后自动清理孤儿锁 |
| **从哪里操作** | 内嵌于 `real_rd_executor.py`，default-off（`agent_kernel_enabled=False`）；由 `run_config_fingerprint.py` + `agent_execution_kernel.py`（锁）+ `agent_wakeup_session.py`（唤醒/会话）三个模块协同 |
| **最终得到什么** | 执行锁（idempotent claim/release，TTL/heartbeat，force_release 清孤儿）、Agent 唤醒请求 + 运行会话（状态机 pending→running→completed|failed|recovered）、运行配置指纹（SHA-256 + Secret 脱敏）、恢复异常测试 |
| **当前属于** | **技术存在** — 41 测试全绿、红线守卫通过；默认关闭，尚未作为日常用户执行入口 |
| **当前限制** | default-off；无独立 sweeper 进程（恢复编排由调用方触发）；本期仅接 RealRD 执行器 |
| **证据** | `agent_execution_kernel.py` / `agent_wakeup_session.py` / `run_config_fingerprint.py` / `test_agent_execution_kernel.py` + `test_agent_execution_kernel_qa_extra.py` 41+3 全绿；提交 `1c582c88` / `15d57438` |

### J.3 BudgetGuard 预算硬停

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 设定 Agent/Project 的 token 成本上限，接近上限时软提醒、超过上限时硬暂停执行；防止无限消耗 |
| **从哪里操作** | 内嵌于 `real_rd_executor.py`，default-off（`budget_enabled=False`）；配置于 `budget_guard_config.json` |
| **最终得到什么** | `budget_guard_accumulators` 表记录每个 scope 累计 token；超限时 `budget_exceeded` 事件落库 + 执行中止 |
| **当前属于** | **技术存在** — 20+ 测试全绿；默认关闭，尚未作为日常用户执行入口 |
| **当前限制** | default-off；基于 total_tokens 而非价格；与 B 层 G4 闸并存但各自独立 |
| **证据** | 提交 `18e3dc89` |

### J.4 CEO 运行证据（只读聚合 + Vite SPA 前端）

| 字段 | 内容 |
|------|------|
| **用户能做什么** | 打开浏览器一站式查看：公司运行全局概览、三层事件时间线、组织树展开、待拍板决策卡片、A 层执行锁状态、C 层预算状态——全部只读、脱敏、真实数据 |
| **从哪里操作** | 后端 6 个只读 `GET /api/ceo/evidence/*` 端点 + 前端 `cd frontend/ceo-evidence && npm run dev`（Vite SPA，7 页面） |
| **最终得到什么** | `CeoOverviewDTO`（计数 + 层状态）、`TimelineEventDTO`（过滤 + 着色）、`OrgNodeDTO`（树形展开）、`PendingDecisionDTO`（审批卡）、`ExecutionStatusDTO` / `BudgetStatusDTO`（面板） |
| **当前属于** | **自用可用** — 24/24 测试全绿、70/70 基线回归、红线守卫 7/7、前端 Vite build 成功 |
| **当前限制** | 只读无写（不含 approve/resolve）；数据限于 selfuse tenant；前端为独立 Vite SPA，不与旧 Next.js CEO Office 合并 |
| **证据** | `ceo_evidence_api.py` / `ceo_evidence_api_config.json` / `test_ceo_evidence_api.py` 24 passed / `frontend/ceo-evidence/`（7 页面 + API 层 + 全部配置）；提交 `b025236f` |

---

## G. 已冻结 / L2 Gate 能力（存在但不使用）

以下能力代码已存在、seed 数据已落地、API 已注册，但因 L2 Gate 规则**冻结**，用户不应使用。

| # | 能力 | 冻结原因 | 相关代码 |
|---|------|---------|---------|
| G1 | 多租户 Tenant 管理（`/api/platform/tenants/*`） | L2 #5 Admin/Workspace 边界 + L2 #6 权限边界 — 当前 selfuse 场景不需要真实多租户，禁止创建/删除 tenant | `main.py L2522-2579`, `database.py L1230` seed |
| G2 | 计费 Plan CRUD（`/api/platform/plans/*`） | L2 #1 商业模式 + L2 #2 收费规则 — 不开放 Marketplace、不计费 | `main.py L2808-2863`, `database.py _seed_billing_mvp` |
| G3 | Pricing/Pricing Rules（`/api/platform/pricing-rules/*`） | L2 #2 收费规则 — 同上 | `main.py L2978-3027` |
| G4 | Quota/Quota Rules（`/api/platform/quotas/*`） | L2 #2 收费规则 — 同上 | `main.py L2880-3085` |
| G5 | Billing Events（`/api/platform/billing-events/*`） | L2 #2 收费规则 — 同上 | `main.py L2952-2976` |
| G6 | Usage 计量（`/api/platform/usage*`, `/api/platform/usage-meter`） | 同上；usage 数据依赖于真实计费场景才有意义 | `main.py L2579-2659` |
| G7 | 商业配置前端页面（`/platform/commercial/`） | L2 #1/#2 — 不开放商业功能，页面保持冻结 | `frontend/app/platform/commercial/page.js` |
| G8 | Employee CRUD 端点（`/api/workspace/employees`） | 禁止区铁律 — 禁止真实多 Agent 交互，仅保留数据库层 CRUD | `main.py L2151-2189` |
| G9 | 外部 Agent 生态导入（CrewAI/MCP/skill仓库） | L2 #4 Marketplace — 试点 B 已落地（5 商业 division），但多源扩展冻结 | `database.py _seed_agent_conversion_pilot_b`, `_seed_crewai`, `_seed_mcp`, `_seed_skill_repo` |

---

## H. 用户验收场景（UAT）

以下场景用以验证整条链路**从用户入口到结果**是完整的。

### H.1 创始人创建 AI 公司并运行

```
1. 启动后端：cd backend && ./run.sh
2. 创建 Company：POST /api/workspace/companies {"name":"我的AI公司","company_template_id":"...", "tenant_id":"selfuse"}
3. 创建部门：POST /api/workspace/companies/{id}/departments {"name":"研发部","department_type":"tech.rd"}
4. 创建员工：POST /api/workspace/employees {"name":"AI工程师","department_id":"...","employee_template_id":"..."}
5. 分配能力：PUT /api/workspace/employees/{id}/capabilities {"capability_ids":["..."]}
6. 创建项目：POST /api/workspace/projects {"name":"首个项目","company_id":"..."}
7. 发布任务：POST /api/task {"content":"分析需求","company_id":"...","employee_id":"..."}
8. 运行任务：POST /api/task/{id}/run
9. 查看结果：GET /api/task/{id}
10. 查看 CEO 概览：浏览器打开 /ceo-office
```

**预期**：全部 API 返回 2xx，CEO 页面展示部门/员工/Task 数据。

### H.2 凭证管理

```
1. 打开前端 /control/secret-vault
2. 新增凭证（名称、类型、凭证值）
3. 测试连通性
4. 编辑/禁用/删除凭证
5. 用 API 查看 GET /api/workspace/credentials
```

**预期**：前端页面完整 CRUD，API 返回一致。

### H.3 真实研发闭环（CLI）

```
1. export CURIS_RD_SANDBOX=off
2. source deploy/new-api/.env
3. backend/.venv/bin/python backend/scripts/run_real_rd.py \
     --issue-spec tools/real_rd_fixture/target_a.py \
     --sandbox-mode off
4. 查看 stdout 中的 status/rounds/test_exit_code/diff_text
```

**预期**：status=succeeded, rounds≥1, test_exit_code=0, diff_text 含 `--- a/+++ b/`。

### H.4 内容工作流发布

```
1. 准备内容工作流模板
2. POST /api/content-workflow/run {"workflow_template_id":"...","input":{...}}
3. GET /api/results/summary
4. GET /api/results/content-workflow-runs
5. POST /api/publish-package/export {"source_workflow":"...","artifacts":[...]}
```

**预期**：返回 run_id，结果摘要显示 completed 计数，发布包可导出。

### H.6 CEO 运行证据浏览（Vite SPA）

```
1. 启动后端：cd backend && python -m uvicorn app.main:app --reload
2. 新终端：cd frontend/ceo-evidence && npm run dev
3. 浏览器打开 http://localhost:5173
4. 查看「概览」：公司/员工/执行锁/预算/待决策计数 + 最近活动
5. 切换「时间线」：过滤 a.kernel / a.budget / b.governance 事件
6. 切换「组织树」：展开 Company → 部门 → 员工 → Skill/Tool
7. 切换「待拍板决策」：看审批卡，确认 title/business_risk/recommended 只读展示
8. 切换「执行状态」「预算状态」：看 A 层锁/会话、C 层累加器
```

**预期**：7 页面均有真实数据展示（非 mock），全部脱敏无路径/Key/Secret。

### H.7 B 层治理全链路验证

```
1. 修改 real_rd_executor.py 中 run() 里将 agent_kernel_enabled=True 临时打开
2. 跑一次真实研发闭环：backend/scripts/run_real_rd.py --issue-spec tools/real_rd_fixture/target_a.py
3. 运行后检查：
   - agent_execution_claims 表有 claim 记录（acquired → released 完整生命）
   - agent_task_sessions 表有 session（pending→running→completed）
   - evolution_events 表有 a.kernel.* 脱敏事件
4. 若 G1-G4 闸触发 pending 决策 → 检查 b_layer_pending_decisions.sqlite 有记录
5. 通过 curl GET /api/ceo/evidence/execution 查看活跃锁/会话
```

**预期**：内核全链路记录可查，CEO Office 可见运行证据。

---

## I. 已知限制

### I.1 全局性

| # | 限制 | 影响 | 优先级 |
|---|------|------|--------|
| L1 | 无前端管理 UI（platform/ 前端暂停） | 所有 Admin CRUD 需 curl/Postman | P0 |
| L2 | ~~Workspace 前端（ceo-office/employees/control）不属本团队~~ ✅ **已反转**（2026-07-21 总控裁定：本团队接手 Workspace 前端），CEO Office 已出 Vite SPA（`frontend/ceo-evidence/`）；Secret Vault 仍为旧 Next.js 前端，待后续对齐 | 现属本团队范围 | ✅ **已解决** |
| L3 | 员工（Employee）CRUD 端点铁律禁止真实多 Agent 交互 | 员工仅数据库记录，无实际 Agent 进程 | P0 |
| L4 | 无多租户隔离（仅 selfuse） | 不能创建第二个独立 tenant | P0 |
| L5 | ~6 个 sandbox 限制测试失败 | `pytest backend/tests/` 中 6 个 `test_local_rd_toolset.py` 因 sandbox-exec 不可用失败，属预存环境限制 | P2 |
| L6 | 资产完成度（10 类资产内容）有待补全 | skl_ai_rd_*/tl_ai_rd_* 等真实内容仅部分填充 | P1 |
| L7 | dashboard widget 数据部分为 seed 占位 | CEO Office 某些图表不准确 | P2 |
| L8 | Agent 执行内核 / BudgetGuard 均为 default-off | 生产启用需手动开启 `agent_kernel_enabled=True` / `budget_enabled=True` 并定夺 sweeper 编排 | P1 |
| L9 | B 层治理闸引擎当前 default-off | 启用后所有 Task 经过 G1-G4 评估，可能增加待拍板决策积压 | P2 |
| L10 | CEO Office Vite SPA 为独立前端（不合并旧 Next.js） | 旧 `/ceo-office` 与新 `:5173` 并存需用户自行选择启动方式 | P2 |
| L11 | 决策审批仅展示待拍板，不含 resolve/approve 写操作 | 用户通过 CEO Office 看到待 A/B/C/D 拍板的决策后，需手动通过 API 或未来 UI 拍板 | P0 |

### I.2 研发工具链限制

| # | 限制 | 影响 | 优先级 |
|---|------|------|--------|
| T1 | 真实研发闭环依赖本地 New API 网关可达 | 网关不可达时全部回退到 mock | P1 |
| T2 | sandbox-exec 在 WorkBuddy 沙箱内不可见 | 只能以 OFF 模式运行，无网络隔离 | P1 |
| T3 | deepseek-v4-pro 偶发 diff_contxt_mismatch | 需 retry 吸收，增大 rounds | P2 |
| T4 | 未接真实 Issue 队列（需调度器） | 当前手动指定 Issue spec 文件 | P2 |
| T5 | D1 容器工具链已解冻，但完整模型执行结果尚未实测 | 需在受控 R3 网关凭据 / 网络条件下验证 `.execute() → status=succeeded` | P1 |
| T6 | DevAgent 6 后端（含 `CodexAgentAdapter` / `WorkBuddyAgentAdapter` 两个真·agent 后端）的**协议一致性、无 key/无 CLI 降级、执行器 agent 分支**均已单测覆盖（10 + 16 + 18 = 44 passed）；剩余缺口 = 未用**真实 `codex` CLI（免 key）/ 真实 `CODEBUDDY_API_KEY`（WorkBuddy）** 实跑过一轮完整研发闭环 | 待一次真实验证：① 跑 `RealRDExecutor(model=CodexAgentAdapter(cwd=<repo>), ...)`（codex 已登录免 key）；② 配 `CODEBUDDY_API_KEY` 后跑 `RealRDExecutor(model=WorkBuddyAgentAdapter(cwd=<repo>), ...)`，均确认 agent 直接改文件 + 测试 + 交付 diff 全链路 | P2 |

### I.3 已冻结（L2 Gate）限制

| # | 限制 | 影响 | 优先级 |
|---|------|------|--------|
| F1 | Billing/Plan/Pricing/Quota 冻结 | 不能创建付费计划、不能计费 | — |
| F2 | Tenant 管理冻结 | 不能创建/管理多租户 | — |
| F3 | Marketplace 冻结 | 不能对外开放能力市场 | — |
| F4 | 外部 Agent 生态导入冻结 | 不能自动从 CrewAI/MCP/Coze 导入 | — |
| F5 | 新商业包线（内容公司/商业公司 `ccp_*`）冻结 | 不能创建新商业产品线 | — |
| F6 | 真实 instantiation / 外部平台 / ROI / 员工 冻结 | 不能做真实部署/面试/雇佣 | — |
