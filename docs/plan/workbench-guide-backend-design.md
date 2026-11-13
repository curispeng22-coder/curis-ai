# 业务工作台引导（Workbench Guide）后端设计

> 状态：Draft（待评审）
> 日期：2026-08-03
> 范围：后端（模板 + 会话端点 + 落地生成器 + 模型解析）；前端向导页为下游依赖，本设计只定 API 契约。
> 关联：`docs/plan/phase1-impl-design-gate-cdef.md`（公司实例化复用）、运行时桥（tenant_private model/agent，已完成）

---

## 1. 背景与目标

用户在**已创建公司**后创建「业务」（形成工作台）时，需要一个类似公司创建引导的流程：引导 AI 与用户对话，把**业务需求摸清**（目标、领域、预期产出），结构化摘要成**工作台蓝图**，用户确认后**一键落地生成**项目/部门/员工/工作流。

本设计只做「业务工作台引导」后端；「公司 onboarding」（新用户首进、无公司）为平台级功能，**v1 不实现**，仅在模板注册表预留扩展点（见 §9）。

### 目标

1. 引导流程**数据驱动**（模板化），未来 admin 化 = 配置表，无重构。
2. 引导 AI 的模型/agent **用户自定义优先**（tenant_private，密钥不落库），官方默认兜底。
3. 落地生成**复用现有原语**（`create_department_instance` / `create_employee_instance` / `create_project`），不新建 Employee/Project CRUD。
4. 引导阶段无任务归属，AI 调用**不走任务计费链路**，独立轻量通道 + 脱敏事件。

### 红线（不触碰）

- 不新建商业包 / Marketplace / 收费（L2 Gate 项，触发即升级）。
- 不落任何密钥（`env:VAR` 引用，同 Step 5 约定）。
- 引导只产出**草稿**，落地前必须用户显式确认。
- 不把引导模板做成平台 admin 实体（v1 内置默认，注册表留位即可）。

---

## 2. 术语与实体映射

| 术语 | 含义 |
|------|------|
| 引导模板 GuideTemplate | 数据驱动的流程定义（步骤、Prompt、抽取 schema、蓝图 schema） |
| 引导会话 GuideSession | 一次引导流程的运行态（步骤游标 + 已收集内容 + 蓝图草案） |
| 工作台蓝图 WorkbenchBlueprint | AI 结构化输出的落地参数（项目 + 部门 + 员工 + 工作流引用） |
| 引导模型 GuideModel | 驱动引导对话的模型/agent（自定义优先、官方兜底） |
| 落地生成器 WorkbenchInstantiator | 蓝图 → 复用现有原语落库 |

「工作台」在现有实体模型中 = **项目（project）+ 其下部门实例 + 员工实例 + 工作流引用**（公司已存在，不新建公司）。

---

## 3. 总体架构

```
前端向导页
   │  POST /api/workspace/guides/sessions         （start：取步骤 1 + session_id）
   │  POST /api/workspace/guides/sessions/{id}/answer （回答 → AI 追问或蓝图草案）
   │  POST /api/workspace/guides/sessions/{id}/confirm （确认 → 落地生成）
   ▼
GuideService（编排）
   ├── GuideTemplateRegistry     内置模板（guide.business_workbench），注册表预留 onboarding
   ├── GuideSessionStore         guide_sessions 表（步骤游标 / 内容 / 蓝图草案）
   ├── GuideModelResolver       解析引导模型（自定义 agent/model 优先 → 官方偏好 → 默认网关）
   └── WorkbenchInstantiator    蓝图落地（复用 create_department_instance / create_employee_instance / create_project）
```

组件职责：

- **GuideTemplateRegistry**：读内置模板（v1 代码 seed，非表）；`list()` / `get(guide_id)`；未来 onboarding/admin 化在此加表驱动。
- **GuideSessionStore**：SQLite 表 `guide_sessions`（§5），会话生命周期 INIT → COLLECTING → READY → CONFIRMED → DONE / ABANDONED。
- **GuideModelResolver**：§7 解析策略，直接构造 `ModelGatewayAdapter` 调用（复用运行时桥的构造方式），不经过 `execute_model_gateway`（其要求任务归属，引导阶段无 task/employee/project）。
- **WorkbenchInstantiator**：§8 落地，蓝图字段校验 → 建部门 → 建员工 → 建项目 → 绑定 owner；全程 `TenantContext.scope`，记 `guide.workbench_created` 事件。

---

## 4. 引导模板数据结构（GuideTemplate）

```json
{
  "guide_id": "guide.business_workbench",
  "version": "1.0.0",
  "name": "业务工作台引导",
  "audience": "tenant_side",
  "steps": [
    {
      "step": 1,
      "type": "free_form",
      "title": "描述你的业务",
      "prompt": "你想做的业务是什么？请用几句话描述：业务目标、面向谁、预期产出。",
      "ai_turns": 3,
      "min_chars": 20,
      "extract_schema": {
        "goal": "string",
        "domain": "string",
        "audience": "string"
      }
    },
    {
      "step": 2,
      "type": "confirm",
      "title": "确认工作台方案",
      "prompt": "基于你的描述，我建议这样搭建工作台。请确认或修改：",
      "blueprint_schema": {
        "project_name": "string",
        "goal": "string",
        "description": "string",
        "departments": [
          {
            "template_id": "enum:official.department.software_rnd|official.department.content_growth",
            "name": "string",
            "employees": [
              { "template_id": "string", "name": "string" }
            ]
          }
        ],
        "owner_employee_ref": "string"
      }
    }
  ],
  "model": {
    "prefer": "custom",          // custom 优先用户自定义；official 固定官方
    "fallback": "official_default"
  },
  "blueprint": "workbench"       // 落地目标类型，注册表按此路由到 WorkbenchInstantiator
}
```

约束：

- `type` ∈ {`free_form`, `multiple_choice`, `confirm`}；v1 实现 `free_form` + `confirm`。
- `ai_turns`：单步内 AI 追问轮次上限（未抽齐 schema 必填字段则继续追问，不生成蓝图）。
- `extract_schema` / `blueprint_schema`：驱动 AI 输出 JSON 的契约；解析失败重试，2 次失败转人工兜底（前端提示用户直接填表单）。
- `model.prefer`：v1 默认 `custom`（用户自定义优先），可被引导设置覆盖。

---

## 5. 数据模型：guide_sessions

```sql
create table if not exists guide_sessions (
  session_id       text primary key,
  tenant_id        text not null,
  guide_id         text not null,
  guide_version    text not null,
  status           text not null,          -- INIT|COLLECTING|READY|CONFIRMED|DONE|ABANDONED
  current_step     integer not null default 1,
  collected_json   text not null default '{}',   -- 各步骤收集内容（脱敏）
  blueprint_json   text,                         -- AI 蓝图草案
  model_used       text,                         -- 实际使用的引导模型摘要（脱敏，无密钥）
  created_at       text not null default current_timestamp,
  updated_at       text not null default current_timestamp
);
create index if not exists idx_guide_sessions_tenant on guide_sessions(tenant_id, status);
```

约束：不存密钥 / 不存原始 Prompt 中的敏感输入全文（仅存结构化字段）；`collected_json` 写前经 `_reject_secret_like_metadata` 同款扫描。

---

## 6. API 契约

所有端点租户作用域（`TenantContext`），错误统一 `{detail}`，422/404。

### 6.1 列出引导模板

`GET /api/workspace/guides`

```json
{ "guides": [ { "guide_id": "guide.business_workbench", "version": "1.0.0",
                "name": "业务工作台引导", "steps": [{ "step": 1, "type": "free_form", "title": "描述你的业务" }] } ] }
```

### 6.2 开始会话

`POST /api/workspace/guides/sessions`

```json
{ "guide_id": "guide.business_workbench" }
```

→ 201

```json
{ "session_id": "gs-...", "guide_id": "guide.business_workbench",
  "status": "COLLECTING", "current_step": 1,
  "step": { "step": 1, "type": "free_form", "title": "描述你的业务",
            "prompt": "你想做的业务是什么？…", "ai_turns": 3, "min_chars": 20 } }
```

### 6.3 提交回答

`POST /api/workspace/guides/sessions/{session_id}/answer`

```json
{ "step": 1, "answer": "我想做一个 AI 短视频内容公司，目标是每周稳定产出 3 条爆款短视频…" }
```

行为：

1. 校验会话状态为 COLLECTING、`step` 为当前步。
2. `GuideModelResolver` 解析引导模型，用 `step.prompt + 已收集内容 + 新回答` 调模型，要求输出 JSON：
   - 若 `extract_schema` 必填字段未抽齐 → 返回 `{ "mode": "follow_up", "question": "…" }`（AI 追问，前端展示追问框）。
   - 若抽齐且当前为 `free_form` 最后一步 → 生成 `blueprint` 草案并推进到 confirm 步，返回 `{ "mode": "blueprint", "blueprint": {...} }`。
   - 若当前步为 `confirm` → 返回校验后蓝图。
3. 全部响应不回传密钥；`model_used` 只含 provider/model 摘要。

→ 200：见上。异常（模型调用失败 / 解析失败重试耗尽）：`{ "mode": "manual_fallback", "message": "…", "fields": [...] }`，前端渲染为普通表单。

### 6.4 确认并落地

`POST /api/workspace/guides/sessions/{session_id}/confirm`

```json
{ "blueprint": { "project_name": "AI 短视频工作室", "goal": "每周 3 条爆款短视频",
                 "description": "…", "departments": [ { "template_id": "official.department.content_growth",
                 "name": "内容部", "employees": [ { "template_id": "official.employee.content_editor", "name": "主编" } ] } ],
                 "owner_employee_ref": "内容部/主编" } }
```

行为：

1. 校验状态 READY（蓝图草案已生成）；用户可在确认时修改蓝图字段（以请求为准）。
2. `WorkbenchInstantiator.instantiate(blueprint)` 落地（§8），事务内建部门→员工→项目。
3. 记 `guide.workbench_created` 事件；会话置 DONE。
4. 返回 `{ "session_id", "status": "DONE", "workbench": { "project_id", "project_name",
   "department_ids": [...], "employee_ids": [...], "owner_employee_id" } }`。

### 6.5 放弃会话（可选）

`POST /api/workspace/guides/sessions/{session_id}/abandon` → 置 ABANDONED。不删除记录（审计）。

---

## 7. 引导模型解析（GuideModelResolver）

引导阶段**无 task/employee/project**，`execute_model_gateway` 的任务归属校验不适用，故独立解析 + 直调：

1. **引导配置**：会话创建时可带 `model_preference`（可空）。
   - `custom`（默认）：读 `database.list_tenant_private_capabilities(tenant_id, capability_type in model|agent, active)`；取 `metadata.endpoint`/`base_url` + `credential_ref`（`env:VAR` → `resolve_gateway_api_key`；vault ref → `credential_vault.resolve`）。选第一个 active，构造 `ModelGatewayAdapter(base_url=..., api_key=..., gateway_id=..., model_name=...)`。
   - 无自定义能力 → 兜底官方：`TenantModelPreferenceResolver.resolve_runtime_model()` → 无偏好则 `default_executor`。
   - `official`：直接官方偏好/默认。
2. **调用**：直调 adapter（复用运行时桥同款 `http_post` 注入，测试可录制）。
3. **重试/降级**：模型调用失败 → 重试 1 次 → 仍失败则返回 `manual_fallback`（前端表单），不静默降级到别的模型（避免用户以为用的是自己选的模型）。
4. **事件**：`guide.model_call` 事件记录 provider/model/结果，脱敏（同 `redact_model_gateway_text`）。

安全：`credential_ref` 只允许 `env:VAR` 或 vault 引用，拒绝内联密钥（复用 `_reject_secret_like_metadata` 语义）；`metadata` 中的密钥类字段一律拒绝落库。

---

## 8. 落地生成器（WorkbenchInstantiator）

```python
class WorkbenchInstantiator:
    def __init__(self, database, event_log, employees, company_runtime): ...

    def instantiate(self, blueprint: dict) -> dict:
        # 1. 校验（缺字段/枚举/空字符串 → ValueError）
        # 2. TenantContext.scope 内事务：
        #    for dept in blueprint.departments:
        #        dept_inst = employees.create_department_instance(
        #            template_id=dept.template_id, name=dept.name, company_id=company_id)
        #        for emp in dept.employees:
        #            employees.create_employee_instance(
        #                department_id=dept_inst["id"], template_id=emp.template_id,
        #                name=emp.name, company_id=company_id)
        #    project = company_runtime.create_project(
        #        company_id=..., name=blueprint.project_name, goal=blueprint.goal,
        #        description=blueprint.description, department_id=首个部门 id,
        #        owner_employee_id=owner_ref 解析的员工 id, status="active")
        # 3. 记 guide.workbench_created 事件；返回摘要
```

要点：

- **company_id 来源**：租户默认公司（`companies where tenant_id=? and is_default=1`）；无默认公司 → 422 提示先创建公司。
- **owner_employee_ref**：`部门名/员工名` 定位；解析失败不阻断，owner 置空（后续可补）。
- **department 必须有**：`create_project` 强依赖 `department_id`，蓝图无部门时引导强制追问。
- **幂等**：落地前会话状态必须 READY；落地成功置 DONE；`guide.workbench_created` 事件带 `session_id`，重复 confirm 以会话状态拒绝（409）。
- 不新建任何 CRUD 端点，全部复用 §1 所列原语。

---

## 9. 未来扩展（不做，仅留位）

- **公司 onboarding 模板**：注册表 `guide.business_workbench` 旁预留 `guide.company_onboarding`（audience=platform，平台级默认模型，无租户绑定上下文，v1 不实现）。
- **admin 化**：模板改表驱动（`guide_templates` 表）+ admin 覆盖端点；前端零改动（因为流程定义在后端，前端只消费 steps）。
- **工作流绑定**：蓝图可选 `workflow_ref`（wt_*），落地后绑定到项目（待 workflow↔project 绑定能力就绪后接入，v1 不阻塞）。

---

## 10. 测试策略

| 层 | 用例 |
|----|------|
| 模板 | 注册表 list/get；未知 guide_id 404 |
| 会话 | start 建会话；answer 非法 step/状态 409；收集内容过 secret 扫描拒绝 |
| 模型解析 | custom 优先（env:VAR 直调私有端点，复用 RecordingHttpPost 录制断言）；无自定义兜底官方；失败重试后 manual_fallback |
| 蓝图 | extract 缺字段 → follow_up 追问；抽齐 → blueprint；confirm 校验枚举/必填 |
| 落地 | 蓝图 → 部门/员工/项目真实落库（复用 S8 夹具）；无默认公司 422；重复 confirm 409 |
| 回归 | 全量 1181 用例不回退 |

测试文件：`tests/test_workbench_guide_backend.py`（服务级 + API 级，复用 `test_runtime_bridge_private_model.py` 的夹具模式）。

---

## 11. 待办与依赖

实现状态：**后端已实现并全量回归通过（1192 passed / 2 skipped / 0 failed，2026-08-03）**。

1. [x] `guide_sessions` 表迁移（database.py `_migrate_guide_sessions`，幂等建表 + 索引）。
2. [x] `GuideTemplateRegistry` + 内置模板 seed（`backend/app/workbench_guide.py`）。
3. [x] `GuideModelResolver`（复用 `resolve_gateway_api_key` / `credential_vault` / `TenantModelPreferenceResolver`；调用失败重试后 manual_fallback，不静默降级）。
4. [x] `GuideService` + 5 个端点（list / sessions / answer / confirm / abandon）。
5. [x] `WorkbenchInstantiator`（复用 employee_templates / company_project_runtime 原语；默认公司惰性创建复用 `list_companies`）。
6. [x] 事件接入 `EvolutionEventLog`（`guide.model_call` / `guide.workbench_created`）。
7. [x] 测试 + 全量回归（`tests/test_workbench_guide_backend.py` 11 用例全绿）。
8. [x] 前端向导页（`frontend/app/guide/page.js` + `lib/api.js` 5 个引导 API；TerraShell/TerraPrimitives 风格；创建入口向导交互，2026-08-04 交付，eslint 通过）。

实现要点（与 Draft 差异）：
- `execute()` 返回精简结果 `{output, cost, ...}` 而非 OpenAI 原始结构，引导内容取自 `response["output"]`。
- 模型调用捕获 `(ModelGatewayExecutionError, RuntimeError)` 两类失败（RuntimeError 为配置不完整）。
- 默认公司通过 `company_runtime.list_companies()` 惰性创建，不直接查表。
