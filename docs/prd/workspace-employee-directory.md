# PRD · Workspace 端「员工目录」最小版本（v1 自用）

- **文档状态**：草稿（v1 自用 · 待总控/架构师评审）
- **作者角色**：产品经理（许清楚）
- **关联决议**：07-12 自用决议 —— Workspace v1 范围内真实员工实例，不触发 L2 Gate，团队自主推进
- **红线约束**：仅 `selfuse` 单租户、不计费、不开放 Marketplace、不做多租户商业化；不写 Admin 资产工厂写链路；不碰 Credential Vault 明文语义、不写死商业规则

---

## 1. 产品目标

在 Workspace 端新增一个「员工目录」页面，让单创始人（自用）能在一个真实持久化的界面里**查看、新增、编辑、删除**自己的 AI 员工实例，并能在「官方部门模板」基础上**引用 + 自定义**部门结构。最小版本交付的是一个可真实 CRUD 的运行态界面：员工数据落库到 `selfuse` 租户下的 `employee_instances` 表，部门可从官方 `department_templates` 套用后再自定义，全程只读取 Admin 资产工厂的模板、绝不改写 Admin 端点。本 PRD 不引入多租户、计费或商业化逻辑。

---

## 2. 用户故事

| # | 角色 | 故事 | 验收要点 |
|---|------|------|----------|
| US-1 | 创始人 | 作为创始人，我想在一个页面看到我名下所有 AI 员工（按部门分组/列表），以便掌握组织全貌 | 列表展示姓名、角色、所属部门、状态；数据来自 `GET /api/workspace/employees` |
| US-2 | 创始人 | 作为创始人，我想新增一名员工并选择其部门与官方员工模板，以便快速实例化 | 表单提交 `POST /api/workspace/employees`（department_id + template_id + name）成功落库 |
| US-3 | 创始人 | 作为创始人，我想编辑某员工的姓名/指令覆盖/状态/启用开关，以便修正运行配置 | `PATCH /api/workspace/employees/{id}` 存在并可持久化（**当前后端缺失，见 §5**） |
| US-4 | 创始人 | 作为创始人，我想删除一名员工，以便清理不再使用的实例 | `DELETE /api/workspace/employees/{id}` 存在并软/硬删除（**当前后端缺失，见 §5**） |
| US-5 | 创始人 | 作为创始人，我想从官方「研发部」等模板一键建立部门，并可改部门名称/使命/负责人/启用哪些员工模板，以便既省事又可自定义 | 套用：`POST /api/workspace/departments`（template_id）；自定义：P1 `PATCH /api/workspace/departments/{id}`（name/mission/manager/status/enabled_employee_template_ids） |

---

## 3. 需求池

### P0（最小版本必须，团队自主推进）

- **P0-1 员工目录列表页**
  - 路由建议：`/employees`（落地于已存在的空目录 `frontend/app/employees/page.js`）。
  - 读取 `GET /api/workspace/employees`，按 `department_id` 分组展示；列表字段：姓名、角色(role)、所属部门、状态(status)、启用(enabled)。
  - 空态、错误态、加载态对齐现有 `ceo-office` 页面风格（client 组件 + `X-Tenant-Id: selfuse` 头）。

- **P0-2 员工新增**
  - 表单 → `POST /api/workspace/employees`（`EmployeeInstanceIn`：department_id、template_id、name、instructions_override、status、enabled）。
  - 部门下拉来自 `GET /api/workspace/departments`；员工模板下拉来自 `GET /api/workspace/employee-templates`。

- **P0-3 员工编辑（补齐后端缺口）**
  - 新增后端：`PATCH /api/workspace/employees/{employee_id}` + 服务层 `EmployeeTemplateContract.update_employee_instance(...)`。
  - 可编辑字段（最小集）：`name`、`instructions_override`、`status`（idle/assigned/disabled）、`enabled`。
  - 约束：编辑不改 `department_id`/`template_id` 引用关系（如需调动部门，走 P1 或重建实例）——待确认 §6。

- **P0-4 员工删除（补齐后端缺口）**
  - 新增后端：`DELETE /api/workspace/employees/{employee_id}` + 服务层 `delete_employee_instance(...)`。
  - 默认**软删除**（如置 `status='disabled'` 并 `enabled=0`；或物理删除——待确认 §6）；删除前若员工为某部门 `manager_employee_id`，需给出校验/提示。

- **P0-5 部门结构可引用官方模板并可自定义**
  - 引用：`GET /api/workspace/department-templates` 读取官方模板（只读，无鉴权，源自 `department_templates` 表 `source='official'`）。
  - 套用/自定义：`POST /api/workspace/departments`（template_id 一键建实例）+ `PATCH /api/workspace/departments/{id}`（改 name/mission/manager_employee_id/status/enabled_employee_template_ids）。
  - **不改动** Admin 写链路（`/api/platform/department-templates`，需 platform-admin 令牌）。

- **P0-6 数据持久化（selfuse 租户）**
  - 所有读写经 `TenantContext` 作用域，tenant 固定 `selfuse`（见 `backend/app/tenant_context.py:36` `DEFAULT_TENANT="selfuse"`）。
  - 落库表：`employee_instances`、`department_instances`（均含 `tenant_id` 列）。

### P1（建议）

- **P1-1 员工字段丰富度**：在列表/表单展示并编辑更多字段——角色(role)、技能(skills, `/employees/{id}/skills`)、能力绑定(capabilities, `/employees/{id}/capabilities`)、工具绑定(tools, `/employees/{id}/tools`)、所属部门。
- **P1-2 部门层级与汇报关系**：用 `department_instances.manager_employee_id` 表达部门负责人；支持部门间上级关系（当前 schema 无 parent_department 字段——是否新增待确认 §6）。
- **P1-3 简单搜索 / 筛选**：按姓名、角色、部门、状态过滤列表。
- **P1-4 部门自定义删除**：当前 `DELETE /api/workspace/departments` 缺失，建议补齐（删除前校验无在职员工）。

### P2（可选）

- **P2-1 员工与 Workflow 执行关联**：从员工目录跳转查看该员工的 workflow 运行/任务（复用 `company_project_runtime` / workflow 接口）。
- **P2-2 成本归属（仅自有成本计量，不计费）**：员工维度聚合 `usage_events`（只读、不计费、不开放 Marketplace），用于创始人查看自有成本归属。

---

## 4. UI 设计稿（对齐现有 Workspace 页面风格）

> 技术基线：Next.js 16 App Router + React 19 + Tailwind；页面为 `"use client"` 组件，`API_BASE` 取自 `NEXT_PUBLIC_API_BASE`，请求头固定 `X-Tenant-Id: selfuse`（与 `ceo-office/page.js:10-11` 一致）。视觉继承 `globals.css` 自定义类名设计语言（如 `ceo-shell / ceo-sidebar / ceo-*`，本页可复用同族暗色风格，命名建议 `ws-*` 以示 Workspace 运行态）。

### 4.1 员工目录列表页（/employees）

```
┌──────────────────────────────────────────────────────────────────┐
│ [⌂] 侧栏 nav（复用 Workspace 风格）                                  │
│     总部 | 部门 | 员工(active) | 工作流 | 凭证                        │
├──────────────────────────────────────────────────────────────────┤
│ 顶部条:  CURIS · EMPLOYEE DIRECTORY     tenant: selfuse  [+ 新增员工] │
├──────────────────────────────────────────────────────────────────┤
│ 筛选栏: [搜索姓名/角色]  部门:[全部▾]  状态:[全部▾]                    │
│ ──────────────────────────────────────────────────────────────── │
│ 部门: 研发部 (dept-xxx)         共 6 人   状态 ACTIVE                │
│ ┌────────┬──────────────┬────────┬────────┬────────┬────────┐       │
│ │ 姓名   │ 角色(role)   │ 部门   │ 状态   │ 启用   │ 操作   │       │
│ ├────────┼──────────────┼────────┼────────┼────────┼────────┤       │
│ │ 晓研   │ tech_lead    │ 研发部 │ idle   │ ✓      │ 编辑 删除│       │
│ │ 小产   │ product_mgr  │ 研发部 │ idle   │ ✓      │ 编辑 删除│       │
│ │ ...    │ ...          │ ...    │ ...    │ ...    │ ...    │       │
│ └────────┴──────────────┴────────┴────────┴────────┴────────┘       │
│ 部门: 内容增长部 (dept-yyy)     共 3 人   状态 ACTIVE                 │
│ ┌────────┬──────────────┬────────┬────────┬────────┬────────┐       │
│ │ ...    │ ...          │ ...    │ ...    │ ...    │ ...    │       │
│ └────────┴──────────────┴────────┴────────┴────────┴────────┘       │
│ 空态: 暂无员工 → [从官方模板新建部门并添加员工]                        │
└──────────────────────────────────────────────────────────────────┘
```

### 4.2 新增 / 编辑员工表单（抽屉或模态）

```
┌─ 新增员工 ────────────────────────────────────────────────┐
│ 部门 *          [ 研发部 (dept-xxx) ▾ ]   ← GET /departments │
│ 员工模板 *      [ Tech Lead (official.employee.tech_lead) ▾] │ ← GET /employee-templates
│ 姓名 *          [ 晓研________________ ]                     │
│ 状态            [ idle ▾ ] (idle/assigned/disabled)         │
│ 启用            [✓]                                         │
│ 指令覆盖        [ 多行文本：覆盖官方模板默认指令…… ]          │
│ ─────────────────────────────────────────────────────────  │
│ 预览: 将从模板冻结 persona_ref / default_skill / default_tool │
│ [取消]  [保存]                                              │
└────────────────────────────────────────────────────────────┘

编辑态差异：标题「编辑员工 · {name}」；部门/模板只读展示（引用关系不改，
参见 §6 待确认）；其余字段可改；底部多一个「删除员工」危险操作按钮。
```

### 4.3 部门引用/自定义（列表页内的「部门」分区）

```
部门卡片 (来自 GET /departments)
┌─────────────────────────────────────────────────────────┐
│ ◎ 研发部                      状态: ACTIVE   已启用 ✓      │
│   department_type: software_rnd  ·  dept-xxx               │
│   使命: 围绕 Curis 自用研发闭环运行                          │
│   负责员工: 晓研 (manager_employee_id)                      │
│   启用的员工模板: [Tech Lead, Product Mgr, Architect…]      │
│   [套用官方模板 ▾]  [编辑部门]  [新增员工到此部门]           │
└─────────────────────────────────────────────────────────┘
「套用官方模板」下拉 = GET /department-templates 的官方条目
  (official.department.software_rnd 等)，选中后 POST /departments 建实例。
```

---

## 5. 探索结论（关键依据，供实现参考）

**前端**
- 框架：Next.js 16 App Router + React 19 + Tailwind（`frontend/package.json`）。
- 现有 Workspace 页面：`ceo-office`（概览，只读）、`control/secret-vault`（凭证）、`platform/*`（Admin 后台）、`results`（结果）。员工目录页面应作为兄弟页新增。
- 落地路由建议：`frontend/app/employees/page.js` → URL `/employees`（目录 `frontend/app/employees` 已存在但为空，是天然落点）。
- 调用约定：client 组件，`const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://127.0.0.1:8000"`；请求头 `{ "X-Tenant-Id": "selfuse" }`（见 `ceo-office/page.js:10-11,36-39`）。
- 视觉：`globals.css` 自定义暗色类名（ceo-* 族），本页建议复用同族风格、以 `ws-*` 命名区分运行态。

**后端数据模型（SQLite，`backend/app/database.py`）**
- `employee_instances`：id, tenant_id, company_id, department_id, template_id, created_from_template_id, name, role, instructions_override, status, enabled, created_at。
- `department_instances`：id, tenant_id, company_id, template_id, name, department_type, manager_employee_id, mission, status, created_from_template_id, enabled_employee_template_ids_json, enabled, created_at, updated_at。
- `employee_templates` / `department_templates` / `employee_capability_bindings` 等同区存在。
- tenant 体现：`tenant_id` 列 + `TenantContext`（默认 `selfuse`，`tenant_context.py:36`）。所有读写经 `TenantContext.scope`。

**Admin 部门模板资产（`backend/app/employee_templates.py` + `database.py:4623`）**
- 官方部门模板字段：`id`(如 `official.department.software_rnd`)、`slug`、`name`(研发部)、`department_type`(software_rnd)、`description`、`default_employee_templates`(员工模板 id 列表)、`default_workflow_template_id`、`default_capability_types`、`source='official'`、`tenant_id='platform'`。
- Workspace 引用方式：只读 `GET /api/workspace/department-templates`（无鉴权）→ 选模板 `template_id` → `POST /api/workspace/departments` 建实例。模板本身**不被改写**；自定义发生在 `department_instances` 实例层（name/mission/manager/status/enabled_employee_template_ids）。
- Admin 写链路：`POST /api/platform/department-templates`（需 `X-Platform-Admin-Token`，`main.py:1707`）——本需求**不触碰**。

**现有 API 风格（`backend/app/main.py`）**
- Workspace 命名空间统一 `/api/workspace/*`，无额外鉴权（self-use 单账号）。
- 员工：`GET /api/workspace/employees`(1475)、`POST /api/workspace/employees`(1479)、能力/技能/工具绑定 put 接口(1494-1541)。
- 部门：`GET/POST /api/workspace/departments`(1437/1441)、`GET/PATCH /api/workspace/departments/{id}`(1457/1464)。
- 模板：`GET /api/workspace/employee-templates`(1268)、`GET /api/workspace/department-templates`(1371)。

**🔴 关键后端缺口（P0 必须补齐）**
- 员工**无编辑接口**：缺 `PATCH /api/workspace/employees/{id}` 及服务层 `update_employee_instance`（`EmployeeTemplateContract` 仅有 `create/list/get`）。
- 员工**无删除接口**：缺 `DELETE /api/workspace/employees/{id}` 及服务层 `delete_employee_instance`。
- 部门**无删除接口**：缺 `DELETE /api/workspace/departments/{id}`（P1）。
- 即：当前后端已具备「员工+部门 创建/列表、部门编辑」能力，但**员工完整 CRUD 缺 U 与 D**，本 PRD 的 P0-3/P0-4 即针对此。

**鉴权/会话**
- tenant 通过请求头 `X-Tenant-Id` 解析，缺省 `selfuse`（`tenant_context.py:71 parse_tenant_from_request`）。
- 创始人身份经 `X-Ceo-Id` 头（`ceo_context.py:26`），self-use v1 默认 `None`（无强鉴权）；`/api/workspace/*` 整体无令牌门禁，仅 `/api/platform/*` 需 admin 令牌。

---

## 6. 待确认问题（供总控 / 架构师拍板）

1. **员工最小字段集**：P0 编辑字段定为 `name / instructions_override / status / enabled` 是否足够？是否需把 `role`、技能/能力/工具绑定也纳入「编辑员工」主表单（而非分散在 P1 的 skills/capabilities 子页）？
2. **部门模板引用方式**：确认「引用」= 仅读取官方 `department_templates` 并以其 `template_id` 建实例（不做任何 Admin 写）；自定义只在 `department_instances` 实例层。是否允许创始人把官方模板**复制为 tenant_private 模板**再改（需触及写链路，可能越界，建议否定）？
3. **员工是否支持多部门归属**：当前 `employee_instances.department_id` 为单列（单部门）。是否需要多部门归属（需新增关联表或 JSON 字段）？建议 v1 维持单部门。
4. **删除语义**：员工/部门删除采用「物理删除」还是「软删除（status=disabled + enabled=0）」？软删除更利于审计与 Workflow 关联追溯，建议默认软删除。
5. **调动部门**：编辑时是否允许改 `department_id`（跨部门调动）？若允许，需同时校验 `employee_template.department_type == 新 department.department_type`（沿用 `create_employee_instance` 的约束）。建议 v1 编辑不改部门，调动走「删除+重建」或 P1。
6. **数据落库位置**：确认员工数据统一落在 `employee_instances` 表（已是），是否需要为「员工目录」页新增专有表？建议复用现有表，不新建。
7. **部门层级/汇报关系**：是否需要部门树（父部门）？当前 schema 无 `parent_department_id`，如需请在 P1 评估新增字段；汇报关系先用 `manager_employee_id` 表达单层负责人。
8. **与 CEO Office 的关系**：`ceo-office` 已有只读员工概览，本「员工目录」为其**可写补全页**，二者数据源一致（同一 `employee_instances`）。是否需要在 CEO Office 加「前往员工目录编辑」入口？建议加。

---

*治理声明：本文档范围内功能均属 07-12 自用决议授权的 Workspace v1 真实员工实例能力，不触发 L2 Gate；不引入多租户、计费、Marketplace 商业化逻辑，不改动 Admin 资产工厂写链路与 Credential Vault 明文语义。*
