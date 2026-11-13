# Admin 资产工厂真实状态复盘（2026-07-17）

> 性质：产品规划席（齐活林）编排的只读复盘，不扩行业、不改代码、不提交。
> 方法：系统交付席查真实库/API/种子；质量运行席查可查/可引用/可实例化；安全边界席查 Admin/Workspace 与凭据边界。全部基于真实证据（表、种子行、API 路由、测试、实例化代码路径），不依据契约文档判断。
> 权威库：`data/curis.sqlite`（后端默认 `CURIS_DB`，见 `backend/app/main.py:696`）。隔离后 `data/admin.sqlite` 为字节级副本基线，`data/workspace.sqlite` 已做部分拆分。

---

## 〇、一句话结论

**Admin 资产工厂目前是"目录层真实、执行层多为壳、实例化链路有断点"的状态。** 部门模板、员工模板（`et_*`）、技能/工具/工作流目录、人格目录可真实查询与引用；但公司包实例化因工作流引用悬空而产出 0 工作流实例，能力包连接器悬空，运行时员工/部门实例是孤儿数据，收费/配额/多租户隔离全是 design-only 占位。**边界与凭据合规落地良好**（前端物理分离、后端双进程双库三层隔离、Vault 仅摘要、无真实 OAuth 接入）。

分类口径：
- **已真实可用**：数据 + 读 API 双齐备，可经 Admin/Workspace 真实消费或实例化。
- **部分可用**：有数据但缺读 API / 有悬空引用 / 仅单条。
- **只有设计**：表/投影缺失、无数据、引用悬空、或 ADR-0017 design-only reservation。
- **尚未开始**：无表、无数据、无代码。

---

## 一、各资产真实状态分类（结论 → 原因 → 证据）

| 资产 | 分类 | 原因（一句话） | 关键证据 |
|---|---|---|---|
| 部门模板 Department | **已真实可用** | 3 条 active、绑定齐、可实例化部门 | `department_templates`=3；`POST /api/workspace/departments`(main.py:1495)；`create_department_instance`(employee_templates.py:54) |
| 员工模板 Employee（`et_*` 6 条） | **已真实可用** | 6 条 active、persona/skill/tool 绑定全解析、可实例化员工 | `employee_templates` 中 `et_*` 绑定经 `GET /api/workspace/employees/{id}/skills`(1594) 校验通过；`create_employee_instance`(employee_templates.py:271) |
| 员工模板 Employee（`official.employee.*` 10 条） | **只有设计（壳）** | draft、绑定全空、未激活 | 10 行 `status='draft'`、`default_skill/default_tool/persona_ref` 空 |
| 人格 Persona | **部分可用** | 6 条 active、被 `et_*` 引用、有内容；但无 GET list 路由 | `persona_templates`=6；仅 `POST /api/platform/personas`(main.py:1750)，无 GET |
| 技能 Skill（`skl_ai_rd_*`，57） | **部分可用** | 目录可查可引用、有内容；按设计不实例化执行（仅提示注入） | `skill_templates`=57；`GET /api/workspace/skills/templates`(1626)；`skill_runtime.py:28`"Skills never execute on their own" |
| 工具 Tool（`tl_*`，115） | **部分可用（目录）/ 只有设计（执行）** | 目录可查可引用；默认 `tool_functions=None`、第三方连接器全 mock → 无执行实现 | `tool_templates`=115；`tool_runtime.py:10` 只读投影；`main.py:704` `tool_functions=None`；`ToolExecutor` 抛"not configured" |
| 工作流 Workflow（`wt_*`/`official.workflow.*`,18） | **部分可用** | 2 个 `official.workflow.*` 结构化可 run；16 个 `wt_*` 是字符串壳；公司包引用 `wl_*` 在当前库经勘误已解析到真实 `wt_*`（非悬空，见下 §三 勘误） | `workflow_templates`=18；` wt_*` `steps_json` 为纯字符串数组；`POST /api/workspace/rd-workflow/run`(1473)；`workflow_contents` 种子(database.py:2505) 含 6 个 `wl_*` 且 `workflow_template_ref` 指向 `wt_*` |
| 公司包 Company Package（`ccp_*`,1） | **部分可用** | 实例化代码真实，部门+员工成功；`workflow_refs`(`wl_*`) 经勘误当前库已解析（应产 6 workflow 实例，非 0）；但 `sub_package_refs` 悬空（`tp_/sp_` 全库无归属） | `company_packages`=1；`CompanyInstantiationService`(company_instantiation.py:38)；`POST …/instantiate`(main.py:1819) |
| 公司模板 Company Template（`ct_*`,1） | **部分可用** | 仅 1 条 AI 研发公司，无 content/commercial 公司模板 | `company_templates`=1（`ct_ai_software_company`）；仅 `POST /api/platform/company-templates`(1798)，无 GET |
| 能力包 Capability Package（1） | **只有设计** | `workflow_template_ids`/`employee_template_ids` 空；`connector_ids` 指向不存在的 xiaohongshu/douyin/shopify | `capability_packages`=1（`cp_content_ops`）；`connector_ids=["xiaohongshu","douyin","shopify"]` 全部悬空 |
| Dashboard Template（9） | **部分可用** | 9 条 active、组件引用全解析；但含 2 条 `ai_commercial` 冻结域、无 GET 路由 | `dashboard_templates`=9；仅 `POST /api/platform/dashboards`(1758)；`ai_commercial` 2 条无对应公司模板 |
| Plan / Pricing / Quota / Seat | **只有设计（design-only reservation）** | 规则表有种子+管理 API，但 `quotas`=0、`platform_policies`=0，无 `cmcf_*` 计费落地，`billing_store` amount 标注"非权威估算" | `plans`=3、`pricing_rules`=2、`quota_rules`=15、`quotas`=0、`platform_policies`=0；`cmcf_*` 表不存在 |
| Connector 目录 | **只有设计** | `connector_templates` 表不存在；`official_models` 仅 1 条 type='model'，零 connector 行 | `GET /api/catalog/connectors`(1031) 代理 `list_catalog_capabilities()` 读 `official_models`；`official_models`=1 且无 connector |
| 默认绑定（员工→Skill/Tool/Persona） | **已真实可用** | `et_*` 的 `default_skill/default_tool/persona_ref` 全部解析成功 | `employee_templates` JSON 列 + `GET /api/workspace/employees/{id}/skills`(1594)/`tools`(1610)/`capabilities`(1577) |
| 多租户隔离（ADR-0017 D1–D4） | **只有设计** | `tenant_id` 列已加、只读目录 facade 已建；隔离/Employee 多租户 CRUD/外部平台/L6 经济均未实现（ADR Status=Proposed） | `tenant_id` 列存在于多表（`database.py`）；ADR-0017 明确"实现暂缓" |
| 第三方 LLM / 连接器 / OAuth 凭证 | **只有设计** | 默认 mock/stub，无真实凭证、无真实外部连接；需配置环境变量或未来 gate | `CURIS_CONNECTOR_MODE=mock`(main.py:2591)；`credential_metadata`=0；`ModelGatewayAdapter` 缺 env 抛 RuntimeError |

---

## 二、当前真实库存

**已真实可用（可查 + 可消费/实例化）：**
- 部门模板：3 条（`dt_engineering`/`official.department.software_rnd`/`official.department.content_growth`），可实例化部门。
- 员工模板（`et_*`）：6 条 active，persona/skill/tool 绑定齐备，可实例化员工。
- 人格目录：6 条，被 `et_*` 引用、有内容。
- 默认绑定：`et_*` 的 Skill/Tool/Persona 绑定全解析。

**部分可用（有数据，但缺 API / 有悬空 / 仅单条）：**
- 技能目录 57、工具目录 115、工作流 18（2 结构化 + 16 壳）、员工模板共 16（含 10 壳）、人格 6（无 GET）、公司包 1（`workflow_refs` 经勘误已解析；`sub_package_refs` 悬空）、公司模板 1、Dashboard 9（含冻结域）。

**只有设计（壳 / 悬空 / 占位）：**
- 能力包 1（连接器悬空）、Connector 目录（表不存在）、Plan/Pricing/Quota/Seat（design-only）、多租户隔离 D1–D4、第三方 LLM/连接器/OAuth（全 mock/stub）、员工模板 `official.employee.*` 10 条壳。

**运行时实例（数据存在但断裂）：**
- `employee_instances`=18、`department_instances`=2、`workflow_instances`=0、`companies`=7、`tenants`=2。其中员工/部门实例是孤儿（见下）。

---

## 三、空壳与悬空项

### 悬空引用（引用了不存在的目标）

> **勘误（2026-07-17 复核）**：本节原第 1 条「公司包 `wl_*` 全部悬空 → 实例化工作流恒为 0 实例」对**当前 `data/curis.sqlite` 不成立**。经 arch-seat 实测、pm-seat 复核确认：`workflow_contents` 表（PK `workflow_content_id`，种子 `database.py:2505`）中公司包引用的 6 个 `wl_ai_rd_*`（software_dev_sop / requirement_to_prd / system_design_sop / api_dev_sop / code_review_sop / ci_cd_sop）**全部 active、enabled=1，且各自 `workflow_template_ref` 指向真实 `wt_*`**（表 `workflow_templates` 的 PK 是 `id`）；实例化代码 `_instantiate_workflow`(company_instantiation.py:191) 走 `get_workflow_content(wl_ref)` → `wt_ref=content.workflow_template_ref` → `_create_workflow_instance(workflow_template_id=wt_ref)`，链路完整，**当前库实例化应产 6 条 workflow 实例，并非恒为 0**。若隔离后的 `admin.sqlite` 是从「缺该种子的旧基线」fork，才会出现悬空——此种情况由 091 修复设计的「幂等补齐 SQL」兜底，下游以实际库 SELECT 为准。本复盘其余悬空项（`sub_package_refs` 的 `tp_/sp_`、`cp_content_ops.connector_ids` 的 xiaohongshu/douyin/shopify）仍属实。

1. **公司包工作流引用（勘误后：当前库已解析）**：`ccp_ai_software_company.workflow_refs_json` = 6 个 `wl_ai_rd_*`，在 `workflow_contents` 中均存在且 `workflow_template_ref` 指向真实 `wt_*`（全部 active）。后果：实例化时该 6 条可正常产出 workflow 实例，**不再恒为 0**；但若 `admin.sqlite` 缺该种子则退化为悬空（由 091 设计兜底）。真正仍悬空的是下方第 2、3 条。
2. **公司包子包引用悬空**：`sub_package_refs_json` = `["tp_code_executor","sp_backend_coding","cp_content_ops"]`，其中 `tp_code_executor`/`sp_backend_coding` 全库无归属。
3. **能力包连接器悬空**：`cp_content_ops.connector_ids` = `["xiaohongshu","douyin","shopify"]`，三者在 `tool_templates`/`connector_templates` 均不存在 → 触及 V2 冻结"外部 Agent 生态导入"。
4. **运行时员工实例孤儿（18 行）**：`employee_instances.template_id` = `et_ai_rd_*`/`et_ai_content_*`（18 个值），在 `employee_templates` 中均不存在 → 不可经 API 重新解析/校验（`create_employee_instance` 要求模板存在，否则 `ValueError`）。
5. **运行时部门实例孤儿（2 行）**：`department_instances.template_id` = `dt_ai_rd`/`dt_ai_content`，在 `department_templates` 中均不存在。

### 空壳数据
- `employee_templates` 的 `official.employee.*`（10 行）：draft、绑定全空、instructions 仅 27–35 字。
- `workflow_templates` 的 `wt_*`（16 行）：`steps_json` 纯字符串数组，无 `step_type`/`employee_role`/`required_capability`，无法映射到执行。
- `skill_templates`（57 行）：仅 `instruction_excerpt` 短句，按设计即"指导型元数据壳"（不执行）。
- `capability_packages.cp_content_ops`：`workflow_template_ids`/`employee_template_ids` 空 + 连接器悬空。
- `quotas`(0 行)、`platform_policies`(0 行)：空表，与 15 条 `quota_rules` 规则不成对。
- `dashboard_templates` 中 2 条 `ai_commercial`：冻结域，无对应公司模板。
- `employee_instances`(18)/`department_instances`(2)：存在但引用断裂的"壳实例"。

---

## 四、必须补齐顺序（优先级从高到低）

1. **修公司包 `sub_package_refs` 悬空 + 能力包 `connector_ids` 悬空**（高优先级数据修正，触 V2 冻结须 design-only 处置）。注（勘误）：原首位「`wl_*`→`wt_*` 工作流引用不一致致实例化=0」对当前库不成立——`wl_*` 已正确指向 `wt_*`，实例化应产 6 workflow；仅当 `admin.sqlite` 缺种子时才退化，由 091 设计幂等 SQL 兜底。**本期真悬空项为 `tp_/sp_` 与 xiaohongshu/douyin/shopify**，属纯数据修正，不扩行业。
2. **清理/归属 18 个员工实例 + 2 个部门实例孤儿**：要么回填对应 `et_*`/`dt_*` 模板（若有真实来源），要么标记为历史导入残留、从"可被 API 解析"的口径里移除，避免误判为"真实可用实例"。
3. **补只读 GET 路由**：`persona_templates`、`dashboard_templates`、`company_packages`、`company_templates` 目前仅 POST 无 GET，Admin 只读消费受限。
4. **清理悬空聚合引用**：公司包 `sub_package_refs` 的 `tp_/sp_`、能力包 `connector_ids` 的 xiaohongshu/douyin/shopify —— 要么改为冻结占位并标注，要么走 L2 Gate 后补（见下）。
5. **明确产品叙事**：`quota_rules`(15) 有规则但 `quotas`(0)/`platform_policies`(0) 空、无 `cmcf_*` → 统一表述为"规则已定义、计费未启用"，避免被误读为可用计费。
6. **标注执行链 stub 边界**：默认 `tool_functions=None`、LLM 网关 env 未声明、连接器 mock、凭证库空 → 在 Admin 资产说明里明确"目录/元数据层真实，端到端执行尚未默认启用"。

---

## 五、应暂停事项（冻结/不扩行业）

- **不得补真实第三方连接器**（xiaohongshu/douyin/shopify 等）：违反 V2 冻结"外部 Agent 生态导入"，暂停至 L2 Gate。
- **不得启用真实计费 / `cmcf_*`**：Plan/Pricing/Quota 仅 design-only reservation，冻结。
- **不得建 Marketplace**：本仓库无 marketplace 表，冻结。
- **不得实现真实多租户隔离**（超出 ADR-0017 D1 `tenant_id` 列）：D2–D4 仍为 design-only，待各自边界 gate。
- **`ccp_ai_content_company` 自用例外**：总控已授权自用保留，但**库中目前无此包**（仅 `ccp_ai_software_company`）→ 暂停补入，待确认 selfuse 范围与边界后再立 Issue。
- **`ai_commercial` Dashboard（2 条）**：属商业域，无对应公司模板 → 暂停渲染/消费，待 L2 裁定。

---

## 六、L2 Gate 事项（须升级总控 + 安全边界席）

按运营协定 v2，以下触 L2 Gate，本团队不得自主推进：
1. **外部连接器生态**（能力包引用 xiaohongshu/douyin/shopify）→ L2 #3(新市场方向)/#4(Marketplace)/#5(权限边界)/#6(外部服务)。
2. **真实计费 / 配额商业化**（若要把 `quota_rules`/`plans`/`pricing_rules` 接成真实 billing）→ L2 #1(商业模式)/#2(收费规则)。
3. **新商业包 / content 公司产品线补全**（`ccp_ai_content_company` 入库、商业域 Dashboard 启用）→ L2 #1/#2/#3。
4. **真实多租户隔离实现**（超出 D1 列，涉及 Employee 多租户 CRUD / 数据物理隔离）→ L2 #5(权限边界)/#6。
5. **平台管理员缺省令牌硬编码**（安全边界席 upgrade 项，`backend/app/main.py:1676-1678` `PLATFORM_ADMIN_TOKEN` 默认 `"platform-admin-dev"`）：若生产未注入环境变量，所有 `/api/platform/*` 管理端点以弱令牌鉴权 → 等同默认口令。建议升级为"未配置即拒绝启动/拒绝 admin 请求"，或强制生产必须注入。**此项属安全红线，建议优先飞书升级。**

---

## 七、边界与凭据核查结论（安全边界席，摘要）

- **前端**：`frontend-admin/` 与 `frontend-workspace/` 物理分离，无交叉 import、无共享全局状态泄漏。合规。
- **后端**：`_product_scope_middleware`(main.py:811-819) 跨产品 API 互拒 404；`_tenant_scope_middleware`(main.py:821-827) 真实注入 TenantContext；数据层 `tenant_id` 过滤落地；双进程启动按 `CURIS_PRODUCT` 清理对方私有表。ADR-0017 D1 真实落地。
- **凭据**：`credential_vault.py` 仅落库 digest/元数据，明文只驻进程内存（local-dev）；`credential_metadata`=0 行无泄露；真实 `.env` 被 `.gitignore` 忽略永不入库。未发现明文密钥。
- **第三方**：无真实 SaaS OAuth 流程，连接器默认 mock，OAuth 仅元数据形状占位。
- **DB 隔离**：`admin.sqlite`/`workspace.sqlite` 为两个独立文件（md5 不同），各自 `CURIS_DB` 起双进程（8001/8002）。真实分离落地。
- **风险**：1 项需升级（见第六节 #5 缺省令牌）；2 项轻微非红线（`task_traces` 无 `tenant_id` 列、前端凭据读取路径 `/api/credential` vs `/api/workspace/credentials` 不一致导致 404）。

---

## 八、复盘边界声明

- 本次仅复盘，未修改任何源码、未提交、未迁移、未新增依赖。
- 所有结论均基于 `data/curis.sqlite` 真实 SELECT、`backend/app/` 路由与实例化代码、`backend/tests/` 测试证据。
- 三条验证线分工：系统交付席（库/API/种子+悬空+空壳）、质量运行席（可查/可引用/可实例化+孤儿实例+执行链 stub）、安全边界席（Admin/Workspace/凭据边界）。
- 报告全文以"先结论、再原因、最后建议"组织，供总控决策席与 Workspace 团队参考。
