# Admin 内部资产修复：设计方案 + 任务分解（仅设计，不写最终源码）

> 作者：高见远（架构师 / arch-seat）
> 日期：2026-07-17
> 性质：只读复盘后的**修复设计**。本文件只产出设计、可执行 SQL 样例、伪代码；**不写最终源码文件、不 git 提交、不碰 Workspace 文件、不实现 L2 冻结项**（外部连接器 / 计费 / 多租户）。
> 数据基线：`data/curis.sqlite`（后端默认 `CURIS_DB`，见 `backend/app/main.py:696`）。隔离后 `data/admin.sqlite` 为字节级副本基线，所有数据修正落在该隔离库。
> 所有映射表均经 `data/curis.sqlite` 真实 SELECT 校验（证据见各节「实测」）。

---

## 〇、重要前提与一处实测偏差（必读）

复盘文档（`docs/review/2026-07-17_admin-asset-real-status-review.md`）把 091 的 `wl_*` 判定为「全部悬空 → 实例化工作流恒为 0」。**但实测当前 `curis.sqlite` 的 `workflow_contents` 种子已包含这 6 个 `wl_*` 且正确指向 `wt_*`**（见第三节实测）。可能原因：复盘后 `backend/app/database.py:_seed_workflow_contents`（2505 行）已补齐，或复盘时查的是更早基线。

**本设计的处理方式**：
- 第三节给出「权威 `wl_*`→`wt_*` 映射表」（与现有种子一致），作为单一真相源。
- 同时给出**幂等修复 SQL**：若隔离后的 `admin.sqlite` 是从「缺该种子的旧基线」fork，该 SQL 可补齐/校正且重复执行无害。
- 不假设复盘结论一定过期，也不假设一定有效 —— 以「映射表 + 校验查询 + 幂等修复」三件套兜底。

---

## 一、Issue 091 数据修正方案

### 1-1 `wl_*` → `wt_*` 精确映射表（6 条）

`company_packages.workflow_refs_json` 存的是 `workflow_content_id`（`wl_*`），
实例化时 `CompanyInstantiationService._instantiate_workflow`（`backend/app/company_instantiation.py:182`）调
`database.get_workflow_content(wl_ref)` → 取 `workflow_template_ref`（即 `wt_*`）写入 `workflow_instances`。

| 序号 | `wl_*`（包内引用） | 真实 `wt_*`（workflow_template_ref） | 名称 | 部门 |
|---|---|---|---|---|
| 1 | `wl_ai_rd_software_dev_sop` | `wt_software_dev_sop` | 软件研发 SOP | software_rnd |
| 2 | `wl_ai_rd_requirement_to_prd` | `wt_requirement_to_prd` | 需求转 PRD | software_rnd |
| 3 | `wl_ai_rd_system_design_sop` | `wt_system_design_sop` | 系统设计方案 | software_rnd |
| 4 | `wl_ai_rd_api_dev_sop` | `wt_api_dev_sop` | API 开发 SOP | software_rnd |
| 5 | `wl_ai_rd_code_review_sop` | `wt_code_review_sop` | 代码评审 SOP | software_rnd |
| 6 | `wl_ai_rd_ci_cd_sop` | `wt_ci_cd_sop` | CI/CD SOP | software_rnd |

> 若某 `wl_*` 无对应真实工作流，本应「映射到 `official.workflow.software_rnd_sop` 等真实 SOP 或移除该 ref」。
> **实测：6 条全部命中真实 `wt_*`，无需降级或移除。** 仅当未来 `admin.sqlite` 缺这些行时才需下方修复。

**修复/校验 SQL（幂等，落 `data/admin.sqlite`，属 Admin 区数据操作，非 Shared 源码）：**

```sql
-- 幂等补齐：若 workflow_contents 缺这 6 行，则插入并指向正确 wt_*；已存在则忽略（INSERT OR IGNORE）
INSERT OR IGNORE INTO workflow_contents
  (workflow_content_id, name, workflow_template_ref, pack, owner_roles_json,
   step_templates_json, source_attribution, version, status, source, tenant_id, enabled)
VALUES
  ('wl_ai_rd_software_dev_sop','软件研发 SOP','wt_software_dev_sop','ai_rd','["PM","Architect","TechLead","Engineer","QA"]','[]','MetaGPT SOP','1.0.0','active','official','platform',1),
  ('wl_ai_rd_requirement_to_prd','需求转 PRD','wt_requirement_to_prd','ai_rd','["Product Manager"]','[]','MetaGPT SOP','1.0.0','active','official','platform',1),
  ('wl_ai_rd_system_design_sop','系统设计方案','wt_system_design_sop','ai_rd','["Architect"]','[]','MetaGPT SOP','1.0.0','active','official','platform',1),
  ('wl_ai_rd_api_dev_sop','API 开发 SOP','wt_api_dev_sop','ai_rd','["Backend Engineer"]','[]','ChatDev workflow','1.0.0','active','official','platform',1),
  ('wl_ai_rd_code_review_sop','代码评审 SOP','wt_code_review_sop','ai_rd','["Architect/Tech Lead"]','[]','AutoGen pattern','1.0.0','active','official','platform',1),
  ('wl_ai_rd_ci_cd_sop','CI/CD SOP','wt_ci_cd_sop','ai_rd','["DevOps/SRE"]','[]','industry SOP','1.0.0','active','official','platform',1);

-- 校验：断言 6 条全部可解析到真实 wt_*（应返回 6 行，wt_exists=1）
SELECT wc.workflow_content_id, wc.workflow_template_ref AS wt,
       (SELECT 1 FROM workflow_templates wt WHERE wt.id = wc.workflow_template_ref) AS wt_exists
FROM workflow_contents wc
WHERE wc.workflow_content_id IN
  ('wl_ai_rd_software_dev_sop','wl_ai_rd_requirement_to_prd','wl_ai_rd_system_design_sop',
   'wl_ai_rd_api_dev_sop','wl_ai_rd_code_review_sop','wl_ai_rd_ci_cd_sop');
```

**种子更新方式（可选，若决定同步修正 `database.py` 种子——此步属 Shared 区，需走第九节双确认）：**
种子位置 `backend/app/database.py:2505 _seed_workflow_contents`。当前该函数的 `workflows` 列表**已含上述 6 行**，无需改动；仅当发现缺漏时按同格式追加。本设计默认**不改动 `database.py`**，仅靠数据层 SQL 兜底，规避 Shared 区改动。

### 1-2 `sub_package_refs` 清理

`company_packages.sub_package_refs_json` 当前 = `["tp_code_executor","sp_backend_coding","cp_content_ops"]`。
其中 `tp_code_executor` / `sp_backend_coding` 全库无归属（非厂包子包、无对应表行）。

**处置：移除这两个悬空引用，仅保留 `cp_content_ops`。** （`cp_content_ops` 本身在 1-3 中处置其悬空连接器。）

```sql
-- 幂等：仅当含悬空项时才改写为干净列表
UPDATE company_packages
SET sub_package_refs_json = '["cp_content_ops"]'
WHERE company_package_id = 'ccp_ai_software_company'
  AND sub_package_refs_json <> '["cp_content_ops"]';
```

> 若确认 `tp_code_executor` / `sp_backend_coding` 应有对应包，设计中**标明需先建包、不在此做**（超出本期范围，且涉及包目录建模）。本期只清理悬空。

### 1-3 能力包 `connector_ids` 处置

`capability_packages.connector_ids`（`cp_content_ops`）= `["xiaohongshu","douyin","shopify"]`，
三者全库不存在，触及 **V2 冻结「外部 Agent 生态导入」** → **不得补真实外部连接器**（L2 Gate）。

**处置：改为空数组 `[]`，彻底消除悬空；设计意图以本设计文档 + 表 `description` 标注为 design-only 占位。**

```sql
-- 幂等：仅当仍为悬空外部连接器时才置空
UPDATE capability_packages
SET connector_ids = '[]'
WHERE package_id = 'cp_content_ops'
  AND connector_ids <> '[]';

-- 同步把 design-only 意图写进 description（可选，便于审计）
UPDATE capability_packages
SET description = '内容运营包（design-only：外部连接器 xiaohongshu/douyin/shopify 受 V2 冻结，待 L2 Gate 后补；当前 connector_ids=[]）'
WHERE package_id = 'cp_content_ops';
```

> 备选「design-only 占位标注」：保留 `connector_ids` 内容但加 `_reserved_` 前缀（如 `["_reserved_xiaohongshu", ...]`）以明示非真实。
> **本设计推荐直接置 `[]`**——更干净、零悬空、不误导「已接入」。

### 1-4 `official.employee.*` 10 条壳 → 补全绑定 / design-only 预留

`employee_templates` 共 16 行：6 条 `et_*`（active、绑定齐）+ 10 条 `official.employee.*`（**draft、persona/skill/tool 全空**）。
其中 6 条 software_rnd 角色与 `et_*` 一一对应；4 条 content_growth 角色无 `et_*` 对应、且 content 技能/工具未在本期范围（L2 相关）。

**处置策略（分两类）：**
- **6 条 software_rnd**：镜像同 slug 的 `et_*` 绑定值（persona/skill/tool 均为真实存在的 ID），使其从「壳」变为「可解析」。
- **4 条 content_growth**：显式标记 **design-only reservation**——仅填一个真实 `persona_ref`（人格目录跨域可用），`default_skill/default_tool` 留空并注明待 L2 补 content 技能/工具；`status` 保持 `draft`。

**具体字段值建议：**

| `employee_template_id` | 类别 | `persona_ref` | `default_skill` | `default_tool` | 说明 |
|---|---|---|---|---|---|
| `official.employee.architect` | 镜像 et_architect | `pt_analytical_advisor` | `skl_ai_rd_system_design` | `tl_ai_rd_code_linter` | 与 et_architect 同值 |
| `official.employee.backend_engineer` | 镜像 et_backend_engineer | `pt_direct_executor` | `skl_ai_rd_python_development` | `tl_ai_rd_code_executor` | 与 et_backend_engineer 同值 |
| `official.employee.frontend_engineer` | 镜像 et_frontend_engineer | `pt_direct_executor` | `skl_ai_rd_python_development` | `tl_ai_rd_code_executor` | 与 et_frontend_engineer 同值 |
| `official.employee.product_manager` | 镜像 et_product_manager | `pt_supportive_coach` | `skl_ai_rd_requirement_analysis` | `tl_ai_rd_git_client` | 与 et_product_manager 同值 |
| `official.employee.qa_engineer` | 镜像 et_qa_engineer | `pt_supportive_coach` | `skl_ai_rd_test_design` | `tl_ai_rd_test_runner` | 与 et_qa_engineer 同值 |
| `official.employee.tech_lead` | 镜像 et_tech_lead | `pt_balanced_facilitator` | `skl_ai_rd_requirement_analysis` | `tl_ai_rd_git_client` | 与 et_tech_lead 同值 |
| `official.employee.content_creator` | design-only | `pt_creative_explorer` | `''`（待 L2） | `''`（待 L2） | content_growth，无对应 et_* |
| `official.employee.content_reviewer` | design-only | `pt_risk_aware_guardian` | `''` | `''` | content_growth |
| `official.employee.content_strategist` | design-only | `pt_balanced_facilitator` | `''` | `''` | content_growth |
| `official.employee.growth_analyst` | design-only | `pt_analytical_advisor` | `''` | `''` | content_growth |

**修复 SQL（幂等：仅当目标字段为空才填，避免覆盖既有真实值）：**

```sql
-- 6 条 software_rnd：镜像 et_* 绑定
UPDATE employee_templates
SET persona_ref='pt_analytical_advisor', default_skill='skl_ai_rd_system_design', default_tool='tl_ai_rd_code_linter'
WHERE id='official.employee.architect' AND (persona_ref IS NULL OR persona_ref='');

UPDATE employee_templates
SET persona_ref='pt_direct_executor', default_skill='skl_ai_rd_python_development', default_tool='tl_ai_rd_code_executor'
WHERE id='official.employee.backend_engineer' AND (persona_ref IS NULL OR persona_ref='');

UPDATE employee_templates
SET persona_ref='pt_direct_executor', default_skill='skl_ai_rd_python_development', default_tool='tl_ai_rd_code_executor'
WHERE id='official.employee.frontend_engineer' AND (persona_ref IS NULL OR persona_ref='');

UPDATE employee_templates
SET persona_ref='pt_supportive_coach', default_skill='skl_ai_rd_requirement_analysis', default_tool='tl_ai_rd_git_client'
WHERE id='official.employee.product_manager' AND (persona_ref IS NULL OR persona_ref='');

UPDATE employee_templates
SET persona_ref='pt_supportive_coach', default_skill='skl_ai_rd_test_design', default_tool='tl_ai_rd_test_runner'
WHERE id='official.employee.qa_engineer' AND (persona_ref IS NULL OR persona_ref='');

UPDATE employee_templates
SET persona_ref='pt_balanced_facilitator', default_skill='skl_ai_rd_requirement_analysis', default_tool='tl_ai_rd_git_client'
WHERE id='official.employee.tech_lead' AND (persona_ref IS NULL OR persona_ref='');

-- 4 条 content_growth：仅填 persona，skill/tool 留空（design-only reservation）
UPDATE employee_templates
SET persona_ref='pt_creative_explorer'
WHERE id='official.employee.content_creator' AND (persona_ref IS NULL OR persona_ref='');

UPDATE employee_templates
SET persona_ref='pt_risk_aware_guardian'
WHERE id='official.employee.content_reviewer' AND (persona_ref IS NULL OR persona_ref='');

UPDATE employee_templates
SET persona_ref='pt_balanced_facilitator'
WHERE id='official.employee.content_strategist' AND (persona_ref IS NULL OR persona_ref='');

UPDATE employee_templates
SET persona_ref='pt_analytical_advisor'
WHERE id='official.employee.growth_analyst' AND (persona_ref IS NULL OR persona_ref='');
```

> 注：`status` 保持 `draft`（不擅自激活）——激活属产品叙事决定，本期只补绑定消除「壳」。

### 1-5 种子更新方式小结

| 修正项 | 落点 | 是否改 `database.py`（Shared） |
|---|---|---|
| `wl_*`→`wt_*` 补齐 | `data/admin.sqlite` SQL | 否（种子已含，仅数据兜底） |
| `sub_package_refs` 清理 | `data/admin.sqlite` SQL | 否 |
| `connector_ids` 置空 | `data/admin.sqlite` SQL | 否 |
| `official.employee.*` 绑定 | `data/admin.sqlite` SQL | 否 |

**统一策略：全部用隔离库 SQL 执行，不碰 `backend/app/database.py` 种子源码**，规避 Shared 区改动与重新 seed 的不可控面。

---

## 二、Issue 092 孤儿实例映射规则

### 2-1 实测现状（孤儿证据）

```text
employee_instances(18, 未删) template_id 实际值（均不存在于 employee_templates）：
  et_ai_rd_backend, et_ai_rd_pm, et_ai_rd_architect, et_ai_rd_tech_lead, et_ai_rd_qa, et_ai_rd_devops,
  et_ai_content_operator, et_ai_content_researcher, et_ai_content_script_writer, et_ai_content_seo,
  et_ai_content_distribution, et_ai_content_planner, et_ai_content_auditor, et_ai_content_video_producer,
  et_ai_content_live_host, et_ai_content_community_manager, et_ai_content_data_analyst, et_ai_content_brand_manager

department_instances(2, 未删) template_id 实际值（均不存在于 department_templates）：
  dt_ai_rd, dt_ai_content

employee_templates 真实存在：et_*(6) + official.employee.*(10)
department_templates 真实存在：dt_engineering, official.department.software_rnd, official.department.content_growth
```

孤儿根因：这些是**历史导入残留**，沿用旧的 `et_ai_rd_*` / `dt_ai_rd` 命名空间，而现行真实模板已改名为 `et_*` / `official.*` / `dt_*`。

### 2-2 部门实例（2 条）→ 建议「选 A 回填」

部门只有 2 条、映射清晰，回填成本低、收益明确（实例重新可解析）：

| 孤儿 `template_id` | 回填到真实模板 | 依据 |
|---|---|---|
| `dt_ai_rd` | `dt_engineering` | 同 software_rnd；且 `ccp_ai_software_company` 的 `department_template_refs_json` 正是 `["dt_engineering"]` |
| `dt_ai_content` | `official.department.content_growth` | 同 content_growth 域 |

```sql
UPDATE department_instances SET template_id='dt_engineering',
       created_from_template_id='dt_engineering', department_type='software_rnd'
WHERE template_id='dt_ai_rd' AND deleted_at IS NULL;

UPDATE department_instances SET template_id='official.department.content_growth',
       created_from_template_id='official.department.content_growth', department_type='content_growth'
WHERE template_id='dt_ai_content' AND deleted_at IS NULL;
```

### 2-3 员工实例（18 条）→ 建议「默认选 B 标记 deprecated」

**推荐 B 的理由：**
1. 18 条里仅 6 条 software_rnd 与 `et_*` 有清晰角色对应；**12 条 content 孤儿角色（script_writer / seo / distribution / video_producer / live_host / community_manager / data_analyst / brand_manager 等）在 `official.employee.*`（仅 4 条 content_*）里根本没有对应模板**——强行回填将**伪造不存在的关系**，比悬空更危险。
2. 即使是 6 条 software_rnd，回填会改写 **Workspace 运行态实例**的 `template_id`，属跨域数据变更。
3. 孤儿实例本质是「历史残留」，业务上无真实消费方。软删（标记 deprecated）既能从「可被 API 解析」口径剔除、又不丢审计数据。

**B 方案 SQL（软删，可恢复）：**

```sql
-- 将 18 条孤儿员工实例标记为 deprecated（软删，保留审计）
UPDATE employee_instances
SET deleted_at = current_timestamp, enabled = 0, status = 'disabled'
WHERE deleted_at IS NULL
  AND template_id IN (
    'et_ai_rd_backend','et_ai_rd_pm','et_ai_rd_architect','et_ai_rd_tech_lead','et_ai_rd_qa','et_ai_rd_devops',
    'et_ai_content_operator','et_ai_content_researcher','et_ai_content_script_writer','et_ai_content_seo',
    'et_ai_content_distribution','et_ai_content_planner','et_ai_content_auditor','et_ai_content_video_producer',
    'et_ai_content_live_host','et_ai_content_community_manager','et_ai_content_data_analyst','et_ai_content_brand_manager'
  );
```

**A 方案（仅作「Workspace 确认后」的可选子路径，不建议默认）：** 若 Workspace 团队确认这些实例是真实运行态、需要保留，则对 6 条 software_rnd 回填到 `et_*`（其余 12 条 content 仍走 B）：

| 孤儿 `template_id` | 回填 `et_*` | 角色一致 |
|---|---|---|
| `et_ai_rd_backend` | `et_backend_engineer` | backend_engineer ✓ |
| `et_ai_rd_pm` | `et_product_manager` | product_manager ✓ |
| `et_ai_rd_architect` | `et_architect` | architect ✓ |
| `et_ai_rd_tech_lead` | `et_tech_lead` | tech_lead ✓ |
| `et_ai_rd_qa` | `et_qa_engineer` | qa_engineer ✓ |
| `et_ai_rd_devops` | （无对应 et_*）→ **仍走 B** | DevOps 无模板 |

> **结论：本期默认执行 B（员工全软删）+ A（部门回填）。** A 的员工子集仅在 Workspace 双确认后开启。因 092 涉及 Workspace 运行态 DB，执行前须与 Workspace 席对齐（见第九节纪律）。

### 2-4 092 校验查询

```sql
-- 断言：所有未删员工/部门实例的 template_id 均可解析到真实模板（应返回 0 行）
SELECT 'emp' AS kind, template_id FROM employee_instances
WHERE deleted_at IS NULL AND template_id NOT IN (SELECT id FROM employee_templates)
UNION ALL
SELECT 'dept', template_id FROM department_instances
WHERE deleted_at IS NULL AND template_id NOT IN (SELECT id FROM department_templates);
```

---

## 三、Issue 093 补只读 GET 路由设计

### 3-1 现状（4 个仅 POST）

| 资源 | 现有 POST 路由（file:line） | 缺 |
|---|---|---|
| persona_templates | `POST /api/platform/personas`（`backend/app/main.py:1750`） | GET list |
| dashboard_templates | `POST /api/platform/dashboards`（`main.py:1758`） | GET list |
| company_packages | `POST /api/platform/company-packages`（`main.py:1766`） | GET list |
| company_templates | `POST /api/platform/company-templates`（`main.py:1798`） | GET list |

现有可复用参考：
- **Admin 鉴权 + GET 风格**：`GET /api/platform/department-types`（`main.py:1693`）—— `_require_platform_admin(request)` + 调服务返回列表。四个新 GET 沿用同一模式。
- **只读目录输出（无 admin 令牌）风格**：`GET /api/catalog/templates`（`main.py:1807`）——供 Workspace 消费侧。
- **底层列表函数（已存在，直接可用）**：
  - `database.list_persona_templates(tenant_id)`（`database.py:3165`）
  - `database.list_dashboard_templates(tenant_id)`（`database.py:3182`）
  - `database.list_company_packages(tenant_id)`（`database.py:3210`）
  - `database.list_company_templates(tenant_id)`（`database.py:3198`）

### 3-2 四个 GET 路由设计（伪代码，非最终源码）

统一风格：路径 `GET /api/platform/<resource>`、`_require_platform_admin` 鉴权、返回 `{ "<resources>": [...] }` 信封，与 `list_platform_department_types`（`main.py:1693`）保持一致。

```python
# 落点：backend/app/main.py，紧邻各自 POST 兄弟路由（1750/1758/1766/1798）之后
# 鉴权与返回结构参考 main.py:1693 GET /api/platform/department-types

@app.get("/api/platform/personas")
def list_platform_personas(request: Request):
    _require_platform_admin(request)
    # db: Database = ...（复用 main.py 既有的 db 实例）
    return {"persona_templates": db.list_persona_templates()}


@app.get("/api/platform/dashboards")
def list_platform_dashboards(request: Request):
    _require_platform_admin(request)
    return {"dashboard_templates": db.list_dashboard_templates()}


@app.get("/api/platform/company-packages")
def list_platform_company_packages(request: Request):
    _require_platform_admin(request)
    return {"company_packages": db.list_company_packages()}


@app.get("/api/platform/company-templates")
def list_platform_company_templates(request: Request):
    _require_platform_admin(request)
    return {"company_templates": db.list_company_templates()}
```

**返回结构约定（信封字段）：**
- `GET /api/platform/personas` → `{"persona_templates": [ {persona_id, slug, name, archetype, status, ...}, ... ]}`
- `GET /api/platform/dashboards` → `{"dashboard_templates": [ {dashboard_template_id, name, company_type, status, ...}, ... ]}`
  - 注意：`dashboard_templates` 含 2 条 `ai_commercial` 冻结域（无对应公司模板），GET **仍返回但标注 `company_type='ai_commercial'` 为冻结**，不在此处消费/渲染，待 L2 裁定（见复盘第五节）。
- `GET /api/platform/company-packages` → `{"company_packages": [ {company_package_id, name, status, workflow_refs_json, sub_package_refs_json, ...}, ... ]}`
- `GET /api/platform/company-templates` → `{"company_templates": [ {company_template_id, name, company_type, status, ...}, ... ]}`

> 错误码：鉴权失败 401（沿用 `_require_platform_admin`），参数/查询异常 422。与现有 POST 兄弟路由一致。

### 3-3 Shared 双确认流程（第九节纪律第七节）

`backend/app/main.py` 属 **Shared 区**。按运营协定第九节纪律第七节：

> **任何对 Shared 区源码（含 `main.py` 路由）的改动，须 Admin 席 + Workspace 席双确认后，方可合入；架构师不得自行强推 / 自行 merge。**

落地步骤（在任务 T9/T10 中执行）：
1. 本设计方案评审通过（team-lead 确认）。
2. 工程师据此写最终路由代码，**开 PR（不自行合并）**。
3. PR 描述明示「Shared 区改动，触发第九节双确认」。
4. **Admin 席 + Workspace 席 双签** 后，由具合入权限者 merge。
5. 合入后在隔离 `admin.sqlite` 验证四路由返回非空且结构正确。

> 特别提示：复盘第六节 #5 指出 `main.py:1676-1678` `PLATFORM_ADMIN_TOKEN` 默认 `"platform-admin-dev"` 属安全红线（弱令牌）。本次虽不改该项，但 GET 路由沿用 `_require_platform_admin`，**若生产未注入环境变量，四路由同样以弱令牌暴露**——建议随 093 一并升级为「未配置即拒绝」，作为 L2 安全升级项单独跟踪（不在本期实现）。

---

## 四、有序任务分解（按实现顺序，含依赖）

角色：工程师=寇豆码，QA=严过关，协调=team-lead。Shared 标记：仅 093 是。

| 任务 | 内容 | 负责 | Issue | Shared | 依赖 | 产出/验收 |
|---|---|---|---|---|---|---|
| **T1** | 备份 `admin.sqlite` 为 `.pre-split` 基线（`cp data/admin.sqlite data/admin.sqlite.<日期>.pre-split`；若 092 触 Workspace 运行态库，连 `workspace.sqlite` 一并备份） | 寇豆码 | — | 否 | 无 | 备份文件存在、可恢复 |
| **T2** | 091-① 补齐/校验 `wl_*`→`wt_*`（`workflow_contents` 幂等 INSERT OR IGNORE + 校验查询） | 寇豆码 | 091 | 否 | T1 | 校验查询返回 6 行且 `wt_exists=1` |
| **T3** | 091-② 清理 `sub_package_refs`（移除 `tp_code_executor`/`sp_backend_coding`） | 寇豆码 | 091 | 否 | T1 | `sub_package_refs_json='["cp_content_ops"]'` |
| **T4** | 091-③ 能力包 `connector_ids` 置 `[]` + description 标注 design-only | 寇豆码 | 091 | 否 | T1 | `connector_ids='[]'`，无悬空外部连接器 |
| **T5** | 091-④ 补全 `official.employee.*` 10 条（6 software_rnd 镜像 et_*；4 content_growth 填 persona、skill/tool 留空 design-only） | 寇豆码 | 091 | 否 | T1 | 10 行 `persona_ref` 非空；6 行 skill/tool 解析到真实 ID |
| **T6** | 092 孤儿处置：部门 A 回填 `dt_engineering`/`official.department.content_growth`；员工 B 软删 18 条（A 的员工子集待 Workspace 确认后开） | 寇豆码 | 092 | 否（触 Workspace 运行态，须先与 Workspace 对齐） | T1 | 未删实例 template_id 全部可解析（092 校验查询=0 行） |
| **T7** | 092 验证（跑 2-4 校验查询 + 确认软删实例不再被 `list_employee_instances` 返回） | 严过关 | 092 | 否 | T6 | 校验查询 0 行；API 列表不含孤儿 |
| **T8** | 091 端到端验证（对 `ccp_ai_software_company` 跑 `instantiate`，断言 `workflows` 数 > 0 且 `unresolved_refs.workflow_refs` 为空；`official.employee.*` 绑定非空） | 严过关 | 091 | 否 | T2–T5 | 实例化 workflows≥6，unresolved 空 |
| **T9** | 093 设计四 GET 路由伪代码 → 工程师据此写最终代码并**开 PR（不合并）** | 寇豆码 | 093 | **是** | 无（可并行） | PR 就绪，描述标注 Shared 双确认 |
| **T10** | 093 Shared 双确认 + 合入（Admin 席 + Workspace 席 双签后 merge），隔离库验证四路由 | team-lead + 双席 | 093 | **是** | T9 | 四路由返回非空、结构正确 |
| **T11** | 全量回归（重新 seed/admin 隔离后实例化端到端跑通；`unresolved_refs` 全空；四 GET 路由联调） | 严过关 | 跨 | 部分 | T2–T10 | 全链路通过 |

**推荐执行顺序**：`T1 → (T2,T3,T4,T5 并行数据修正) → T8(091 验证) → T6 → T7(092 验证) → T9/T10(093，可较早并行启动评审) → T11(总回归)`。
093 设计与评审可不与数据修正串行，但合入（T10）须等双确认，建议放在数据修正稳定后。

---

## 五、风险与回滚

### 5-1 备份建议（`.pre-split` 模式）

- 所有数据修正**只落隔离库 `data/admin.sqlite`**，不动 `data/curis.sqlite` 权威基线（除非团队决定回灌）。
- 修正前执行：
  ```bash
  cp data/admin.sqlite "data/admin.sqlite.$(date +%Y%m%d).pre-split"
  # 若 092 触 Workspace 运行态实例库：
  cp data/workspace.sqlite "data/workspace.sqlite.$(date +%Y%m%d).pre-split"
  ```
- `.pre-split` 命名含义：记录「Admin/Workspace 资产拆分前」的基线，便于一键回退到修正前状态。
- 备份文件 **不入库**（`.gitignore` 已忽略 `data/` 下运行时库；仅留本地 + 必要时归档到 `reviews/` 或备份目录）。

### 5-2 SQL 幂等性

- 全部用 `INSERT OR IGNORE` / `UPDATE ... WHERE <当前值不匹配>` / **软删（`deleted_at` + `enabled=0`）**——重复执行无害、不丢历史。
- 不做 `DELETE FROM ...`（硬删），保证可审计、可恢复。
- 回滚 SQL 示例：
  ```sql
  -- 回滚 1-1：移除补齐的 6 行 workflow_contents（仅当确为本次新增）
  DELETE FROM workflow_contents WHERE workflow_content_id IN
    ('wl_ai_rd_software_dev_sop','wl_ai_rd_requirement_to_prd','wl_ai_rd_system_design_sop',
     'wl_ai_rd_api_dev_sop','wl_ai_rd_code_review_sop','wl_ai_rd_ci_cd_sop')
    AND source='official' AND tenant_id='platform';

  -- 回滚 1-2/1-3：还原 sub_package_refs / connector_ids 原值
  UPDATE company_packages SET sub_package_refs_json='["tp_code_executor","sp_backend_coding","cp_content_ops"]'
   WHERE company_package_id='ccp_ai_software_company';
  UPDATE capability_packages SET connector_ids='["xiaohongshu","douyin","shopify"]' WHERE package_id='cp_content_ops';

  -- 回滚 1-4：清空本次补的 official.employee.* 绑定
  UPDATE employee_templates SET persona_ref='', default_skill='', default_tool=''
   WHERE id LIKE 'official.employee.%';

  -- 回滚 092-B：恢复软删的员工实例（按本次标记的 deleted_at 时间窗）
  UPDATE employee_instances SET deleted_at=NULL, enabled=1, status='idle'
   WHERE deleted_at IS NOT NULL AND template_id IN ( /* 2-3 的 18 个孤儿 id */ );
  -- 回滚 092-A：部门 template_id 还原
  UPDATE department_instances SET template_id='dt_ai_rd', department_type='software_rnd' WHERE template_id='dt_engineering' AND name LIKE '%遗留%';
  UPDATE department_instances SET template_id='dt_ai_content', department_type='content_growth' WHERE template_id='official.department.content_growth' AND name LIKE '%遗留%';
  ```
  > 注：092 回滚依赖执行时记录的操作时间窗/标识；建议在 T6 执行前先 `SELECT` 导出将改动的行主键，便于精确回滚。

### 5-3 风险点

| 风险 | 影响 | 缓解 |
|---|---|---|
| `admin.sqlite` 已含 `wl_*` 种子（实测）→ 1-1 SQL 成 no-op | 无副作用（幂等） | INSERT OR IGNORE 已保证 |
| 092 改 Workspace 运行态实例 | 跨域数据变更 | T6 前与 Workspace 席对齐；默认 B 软删（可恢复） |
| 093 改 Shared `main.py` | 双确认纪律 | T9 开 PR 不合并；T10 双签后合入 |
| `PLATFORM_ADMIN_TOKEN` 弱令牌红线 | GET 路由同样暴露 | 作为 L2 安全升级项单独跟踪，本期不改 |
| 补全 `official.employee.*` 绑定后误被激活消费 | 产品叙事偏差 | 保持 `status='draft'`，激活另立 Issue |

---

## 六、设计要点与推荐执行顺序（汇报摘要）

1. **091 的 `wl_*` 实测已正确指向 `wt_*`**（复盘结论可能基于旧基线）。设计以「映射表 + 幂等修复 SQL + 校验查询」兜底，不假设过期/有效。其余三项（sub_package_refs、connector_ids、official.employee.* 壳）确有悬空/空壳，按 1-2~1-4 修正。
2. **092 推荐「部门 A 回填 + 员工 B 软删」**：部门仅 2 条映射清晰；员工 18 条中 12 条 content 角色无对应模板，强行回填会伪造关系，故默认软删保留审计，A 的员工子集仅 Workspace 确认后开启。
3. **093 四 GET 路由**复用 `main.py:1693` 的 `_require_platform_admin` + GET 风格，调现有 `list_*` 函数；**属 Shared 区，须 Admin+Workspace 双确认后合入，不得自行强推**。
4. **执行顺序**：T1 备份 → T2–T5 数据修正并行 → T8 验证 091 → T6 孤儿处置 → T7 验证 092 → T9/T10 评审+双确认合入 093 → T11 全量回归。
5. **全程不触碰 L2 冻结项**（外部连接器/计费/多租户），不写最终源码、不 git 提交、不碰 Workspace 文件；仅产出本设计 + 可执行的幂等 SQL/伪代码样例。
