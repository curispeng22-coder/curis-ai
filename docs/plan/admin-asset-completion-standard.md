# Admin 资产完成度标准（验收权威文档）

> 文档性质：Admin 资产工厂产品经理（许清楚）依据《WorkBuddy / Admin 跨线协作与当前开发规则》第七节"资产完成标准"落地出的权威验收文档。
> 用途：作为 Issue 091（悬空/空壳）、092（孤儿实例）、093（只读路由）的关闭 Checklist，也是后续任何官方资产能否标记"已真实可用"的唯一判分尺。
> 依据：本文所有"当前状态"均取自 `docs/review/2026-07-17_admin-asset-real-status-review.md` 的复盘快照，结论/原因/证据三列对齐复盘报告的真实证据（表名/行数/路由 file:line），不靠契约文档判断。
> 边界：本文不改任何源码、不 git 提交、不碰 Workspace 文件（frontend/app/ceo-office、employees、page.js、frontend-workspace 一律不动）。

---

## 一、引言

### 1.1 标准来源

协作规则第七节原文规定，任何官方资产**只有同时满足以下六个条件**，才可标记"已真实可用"：

```text
① 有真实内容
② 有稳定 ID 和版本
③ 引用目标真实存在
④ 有只读消费接口
⑤ 可被 Workspace 实例化或绑定
⑥ 有自动测试和真实验证证据
```

同一节还划了红线：**只有文档、表结构、占位行、字符串步骤或 mock，不得称为"已完成"。**

本文把这条规则翻译成"可逐条打勾的验收表"。每类资产对照六条件，给"判据"（怎样算满足）、"当前复盘快照状态"、"距达标缺口"三栏。

### 1.2 适用边界

**管什么：** Admin 自有资产——Company / Department / Employee / Persona / Skill / Tool / Workflow 模板，Dashboard 模板，Company Package，Capability Package，以及默认绑定（employee→skill/tool/persona）。

**不管什么（L2 冻结项，本团队不得自主推进，须升级总控 + 安全边界席）：**

- 外部连接器生态（能力包引用的 xiaohongshu / douyin / shopify 等）—— 触 L2 #3/#4/#5/#6（复盘第六节）。
- 真实计费 / 配额商业化（`cmcf_*` 计费、`quotas`/`platform_policies` 落地）—— 触 L2 #1/#2，属 design-only reservation（复盘 一/五节）。
- 真实多租户隔离（超出 ADR-0017 D1 `tenant_id` 列的 D2–D4）—— 触 L2 #5/#6（复盘 一/六节）。
- Marketplace——本仓库无 marketplace 表，冻结（复盘 五节）。
- 新行业扩展 / 新商业包（如 `ccp_ai_content_company` 入库、`ai_commercial` Dashboard 启用）—— 总控已暂停，待 L2 裁定（复盘 五/六节）。

**结论：** 本文验收口径只覆盖"把已有官方资产修到真实可查/可引用/可实例化/可被 Workspace 消费"，不替 L2 冻结项背书。冻结项哪怕今天有表、有规则，也只能标"只有设计（design-only）"，不能标"已真实可用"。

---

## 一之补、勘误（2026-07-17 复核，重要）

**结论：** 复盘报告第三节把「`wl_*` 全部悬空 → 公司包实例化工作流恒为 0」的结论，与当前 `data/curis.sqlite` 实际不符，本文原稿沿用了该错误，现予勘误。

**原因：** 实测当前库（arch-seat 提出、pm-seat 复核确认）发现 `workflow_contents` 表（种子 `backend/app/database.py:2505` `_seed_workflow_contents`）中，公司包 `ccp_ai_software_company.workflow_refs_json` 引用的 6 个 `wl_*` 全部真实存在且 active/enabled=1，并各自经 `workflow_template_ref` 指向真实 `wt_*`（`wt_software_dev_sop` / `wt_requirement_to_prd` / `wt_system_design_sop` / `wt_api_dev_sop` / `wt_code_review_sop` / `wt_ci_cd_sop`），6 个 `wt_*` 在 `workflow_templates`（`id` 主键）中均 active 存在。实例化代码 `_instantiate_workflow`（company_instantiation.py:191）走 `get_workflow_content(wl_ref)` → `wt_ref=content.workflow_template_ref` → `_create_workflow_instance(workflow_template_id=wt_ref)`，链路完整。**因此当前库实例化公司包应产出 6 条 workflow 实例，而非 0。**

**建议：** 两种可能——(a) 复盘时查的是尚未补齐该种子的更早基线；(b) 种子在复盘后被人补过。无论哪种，**下游以"实际库 SELECT 为准"**，不得再据复盘原文把"必须先修 `wl_*`→`wt_*` 才能实例化"当作事实。真实仍悬空、需修的只有：`sub_package_refs` 的 `tp_/sp_`（`tp_code_executor`/`sp_backend_coding` 全库无归属）与能力包 `cp_content_ops.connector_ids` 的 xiaohongshu/douyin/shopify（触 L2 冻结）。`wl_*`→`wt_*` 映射已真实成立，不属 Issue 091 必改项。复盘报告本身的同款表述由产品规划席（齐活林）同步勘误，arch-seat 已提出可协助回改。

**本文受影响章节已就地修正：** §3.7、§3.9、§4.1、§6。修正后 Workflow / Company Package 的"引用目标真实存在（条件③）"判定相应上调，但 Company Package 仍因 `sub_package_refs` 悬空 + 缺 GET 路由（条件④）停在"部分可用"。

---

## 二、六条件通用判据（先说清楚怎么算满足）

为避免各席判分口径不一，对六个条件统一给"判据"：

| 条件 | 怎样算"满足" | 怎样算"没满足"（典型反例） |
|---|---|---|
| ① 真实内容 | 有可消费的实质数据：模板字段填全、instructions 有实质信息、组件/步骤可映射 | 占位行、27–35 字空壳 instructions、`steps_json` 纯字符串数组无法映射 |
| ② 稳定 ID + 版本 | 有稳定主键 ID（如 `ct_*`/`et_*`/`skl_*`）且可被版本/状态机追溯（active/draft 明确） | 无 ID、ID 与引用不一致（如 `wl_*` 对应不到 `wt_*`）、无版本概念 |
| ③ 引用目标真实存在 | 所有 `ref` 字段指向的 ID 在目标表里真实存在 | 悬空引用：`wl_ai_rd_*`、`tp_/sp_` 子包、xiaohongshu/douyin/shopify 连接器 |
| ④ 只读消费接口 | 有 GET 类路由可让 Admin/Workspace 只读查询该资产 | 仅有 POST 无 GET（如 Persona/Dashboard/Company Package/Company Template） |
| ⑤ 可被 Workspace 实例化或绑定 | 有真实实例化代码路径或绑定解析路径，且能跑通产出实例/绑定 | 实例化链路断点（工作流恒为 0）、孤儿实例无法经 API 重新解析 |
| ⑥ 自动测试 + 真实验证证据 | 有 backend 测试覆盖，且能贴出真实 SELECT/路由/实例化结果 | 仅文档声称、无测试、无查询证据 |

---

## 三、逐类资产验收表

> 状态取值沿用复盘口径：**已真实可用 / 部分可用 / 只有设计（壳）/ 尚未开始**。
> "证据"列直接引用复盘报告的表名/行数/路由 file:line。

### 3.1 Company Template（公司模板，`ct_*`）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **部分可用**（仅 1 条 `ct_ai_software_company`，无 content/commercial 公司模板） |
| ① 真实内容 | 部分满足：1 条 AI 研发公司模板，无商业公司模板 |
| ② 稳定 ID + 版本 | 满足：`company_templates`=1（`ct_ai_software_company`） |
| ③ 引用目标真实存在 | 满足（该条自身无悬空） |
| ④ 只读消费接口 | **不满足**：仅 `POST /api/platform/company-templates`(main.py:1798)，无 GET |
| ⑤ 可被 Workspace 实例化或绑定 | 满足（经 Company Package 间接实例化；`CompanyInstantiationService` company_instantiation.py:38） |
| ⑥ 自动测试 + 验证 | 部分：有实例化路径，但缺独立 GET 消费测试 |
| **距达标缺口** | 补 GET 只读路由（属 Issue 093）；补齐多行业公司模板内容（属 L2 冻结，暂停） |

### 3.2 Department Template（部门模板，`dt_*`）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **已真实可用** |
| ① 真实内容 | 满足：3 条 active，绑定齐 |
| ② 稳定 ID + 版本 | 满足：`department_templates`=3（dt_engineering / official.department.software_rnd / official.department.content_growth） |
| ③ 引用目标真实存在 | 满足 |
| ④ 只读消费接口 | 满足（可经 Admin 查询） |
| ⑤ 可被 Workspace 实例化或绑定 | 满足：`POST /api/workspace/departments`(main.py:1495)、`create_department_instance`(employee_templates.py:54) |
| ⑥ 自动测试 + 验证 | 满足（实例化路径有证据） |
| **距达标缺口** | 无（已达标，保持即可） |

### 3.3 Employee Template（员工模板，`et_*`）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **已真实可用**（`et_*` 6 条）/ **只有设计（壳）**（`official.employee.*` 10 条） |
| ① 真实内容 | `et_*` 满足：6 条 active、persona/skill/tool 绑定全解析；`official.employee.*` 不满足：10 行 draft、绑定全空、instructions 仅 27–35 字 |
| ② 稳定 ID + 版本 | `et_*` 满足（active 状态明确）；`official.employee.*` 不满足（draft 未激活） |
| ③ 引用目标真实存在 | `et_*` 满足；`official.employee.*` 空绑定无可验证 |
| ④ 只读消费接口 | 满足：`GET /api/workspace/employees/{id}/skills`(1594)/`tools`(1610)/`capabilities`(1577) |
| ⑤ 可被 Workspace 实例化或绑定 | `et_*` 满足：`create_employee_instance`(employee_templates.py:271)；`official.employee.*` 不满足（未激活，不可实例化） |
| ⑥ 自动测试 + 验证 | `et_*` 满足（绑定解析校验通过） |
| **距达标缺口** | `official.employee.*` 10 条壳：要么补内容激活，要么按 design-only 标注，不得称"已真实可用"（属 Issue 091 空壳清理范畴） |

### 3.4 Persona Template（人格模板）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **部分可用**（6 条 active、被 `et_*` 引用、有内容；但无 GET list 路由） |
| ① 真实内容 | 满足：`persona_templates`=6，有内容 |
| ② 稳定 ID + 版本 | 满足 |
| ③ 引用目标真实存在 | 满足（被 `et_*` 引用且解析通过） |
| ④ 只读消费接口 | **不满足**：仅 `POST /api/platform/personas`(main.py:1750)，无 GET |
| ⑤ 可被 Workspace 实例化或绑定 | 满足（作为员工绑定被解析，属目录引用，本就实例化——见第五节） |
| ⑥ 自动测试 + 验证 | 部分：有被引用证据，但缺独立 GET 消费测试 |
| **距达标缺口** | 补 GET 只读路由（属 Issue 093）。**注意：Persona 按设计是目录引用，不实例化执行，这不是缺陷**（第五节） |

### 3.5 Skill（技能目录，`skl_ai_rd_*`，57 条）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **部分可用（目录）/ 只有设计（执行）** |
| ① 真实内容 | 满足：57 条目录，有 `instruction_excerpt` 等指导型元数据 |
| ② 稳定 ID + 版本 | 满足：`skill_templates`=57 |
| ③ 引用目标真实存在 | 满足（被 `et_*` 绑定解析） |
| ④ 只读消费接口 | 满足：`GET /api/workspace/skills/templates`(main.py:1626) |
| ⑤ 可被 Workspace 实例化或绑定 | 满足（提示注入式绑定，非执行实例化——见第五节） |
| ⑥ 自动测试 + 验证 | 部分：有目录 GET 测试，但执行层本就 design-only |
| **距达标缺口** | 缺"真实验证证据"中的执行验证——但**执行本就按设计不实现**（`skill_runtime.py:28` "Skills never execute on their own"），所以 Skill 标"部分可用"而非"壳"。只要目录内容真实、ID 稳定、绑定解析、GET 可查，即满足"目录层真实可用"；执行能力属 L2 冻结，不在本次验收范围 |

### 3.6 Tool（工具目录，`tl_*`，115 条）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **部分可用（目录）/ 只有设计（执行）** |
| ① 真实内容 | 满足：115 条目录可查可引用 |
| ② 稳定 ID + 版本 | 满足：`tool_templates`=115 |
| ③ 引用目标真实存在 | 满足（目录层） |
| ④ 只读消费接口 | 满足：`tool_runtime.py:10` 只读投影 |
| ⑤ 可被 Workspace 实例化或绑定 | 满足（绑定解析），但**执行未实现**：默认 `tool_functions=None`(main.py:704)，`ToolExecutor` 抛"not configured" |
| ⑥ 自动测试 + 验证 | 部分：目录 GET 可查，执行链 stub |
| **距达标缺口** | 第三方连接器执行全 mock（CURIS_CONNECTOR_MODE=mock，main.py:2591），属 L2 冻结（外部连接器/真实凭证）。**Tool 目录本身真实可查可引用，标"部分可用"；执行层"只有设计"是按设计，非本次必须修的缺陷** |

### 3.7 Workflow（工作流，`wt_*`/`official.workflow.*`，18 条）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **部分可用**（2 个 `official.workflow.*` 结构化可 run；16 个 `wt_*` 是字符串壳；公司包 `wl_*`→`wt_*` 映射经实测已真实成立，实例化应产 6 条 workflow，详见勘误） |
| ① 真实内容 | 部分满足：2 条结构化（有 `step_type`/`employee_role`/`required_capability`）；16 条 `wt_*` 的 `steps_json` 纯字符串数组，无法映射执行 |
| ② 稳定 ID + 版本 | 满足：`workflow_templates`=18 |
| ③ 引用目标真实存在 | **满足（勘误后）**：公司包 `workflow_refs_json`=6 个 `wl_ai_rd_*` 在 `workflow_contents` 均真实存在（active/enabled=1），并经 `workflow_template_ref` 指向真实 `wt_*`，6 个 `wt_*` 在 `workflow_templates` 均 active。原复盘"全部悬空→0 实例"结论已证伪，见勘误。 |
| ④ 只读消费接口 | 满足（`POST /api/workspace/rd-workflow/run` main.py:1473 可查可 run） |
| ⑤ 可被 Workspace 实例化或绑定 | 满足（勘误后）：`_instantiate_workflow`(company_instantiation.py:191) 经 `get_workflow_content(wl_ref)`→`wt_ref`→`_create_workflow_instance`，当前库实例化应产出 6 条 workflow 实例 |
| ⑥ 自动测试 + 验证 | 部分：2 条有 run 路径，16 条无执行映射；建议补一条实例化产出 6 workflow 的集成测试坐实 |
| **距达标缺口** | 16 条 `wt_*` 字符串壳要么补结构化步骤、要么标注 design-only（Issue 091 空壳）；`wl_*`→`wt_*` 映射已真实，不再列入 091 必改项（见勘误） |

### 3.8 Dashboard Template（Dashboard 模板，9 条）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **部分可用**（9 条 active、组件引用全解析；但含 2 条 `ai_commercial` 冻结域、无 GET 路由） |
| ① 真实内容 | 满足：9 条 active，组件引用全解析 |
| ② 稳定 ID + 版本 | 满足：`dashboard_templates`=9 |
| ③ 引用目标真实存在 | 部分：7 条引用真实；2 条 `ai_commercial` 无对应公司模板（冻结域悬空） |
| ④ 只读消费接口 | **不满足**：仅 `POST /api/platform/dashboards`(main.py:1758)，无 GET |
| ⑤ 可被 Workspace 实例化或绑定 | 满足（组件解析） |
| ⑥ 自动测试 + 验证 | 部分 |
| **距达标缺口** | 补 GET 只读路由（Issue 093）；2 条 `ai_commercial` 属 L2 冻结，暂停渲染/消费（复盘 五节） |

### 3.9 Company Package（公司包，`ccp_*`，1 条）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **部分可用**（实例化代码真实，部门+员工成功；`workflow_refs` 经实测已真实解析可产 6 workflow；但 `sub_package_refs` 仍悬空 + 缺 GET 路由） |
| ① 真实内容 | 满足：`company_packages`=1（`ccp_ai_software_company`），实例化代码真实 |
| ② 稳定 ID + 版本 | 满足 |
| ③ 引用目标真实存在 | **部分满足（勘误后）**：`workflow_refs_json`=6 个 `wl_ai_rd_*` 已实测真实解析到 `wt_*`（见 3.7 勘误）；但 `sub_package_refs_json`=`["tp_code_executor","sp_backend_coding","cp_content_ops"]` 中 `tp_/sp_`（`tp_code_executor`/`sp_backend_coding`）全库无归属仍悬空 |
| ④ 只读消费接口 | **不满足**：仅 `POST …/instantiate`(main.py:1819)，无 GET |
| ⑤ 可被 Workspace 实例化或绑定 | 满足（勘误后）：部门+员工实例化成功，工作流当前库应可产 6 条（wl_*→wt_* 已解析） |
| ⑥ 自动测试 + 验证 | 部分：实例化路径有，工作流产出现需以实际库 SELECT/集成测试坐实，并经 Workspace 跨线验证（Shared Issue） |
| **距达标缺口** | `wl_*`→`wt_*` 已真实，不再列入 091 必改（见勘误）；清理 `sub_package_refs` 的 `tp_/sp_` 悬空（属 L2 冻结或标注，复盘 四/4）；补 GET 路由（Issue 093） |

### 3.10 Capability Package（能力包，1 条）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **只有设计（壳）** |
| ① 真实内容 | 不满足：`cp_content_ops` 的 `workflow_template_ids`/`employee_template_ids` 空 |
| ② 稳定 ID + 版本 | 满足：`capability_packages`=1 |
| ③ 引用目标真实存在 | **不满足**：`connector_ids`=`["xiaohongshu","douyin","shopify"]` 三者全悬空（tool_templates/connector_templates 均不存在） |
| ④ 只读消费接口 | 部分（可查） |
| ⑤ 可被 Workspace 实例化或绑定 | 不满足（引用全空/悬空） |
| ⑥ 自动测试 + 验证 | 不满足 |
| **距达标缺口** | 连接器悬空触 L2 冻结（外部 Agent 生态导入，复盘 三/3、六/1）。**该包今天即"只有设计"，不得称"已真实可用"**；要么改为冻结占位并标注，要么走 L2 Gate 后补，本次不自主推进 |

### 3.11 默认绑定（employee → skill / tool / persona）

| 项目 | 内容 |
|---|---|
| 复盘快照状态 | **已真实可用** |
| ① 真实内容 | 满足：`et_*` 的 `default_skill`/`default_tool`/`persona_ref` 全部解析成功 |
| ② 稳定 ID + 版本 | 满足（绑定解析经 `GET /api/workspace/employees/{id}/skills`(1594)/`tools`(1610)/`capabilities`(1577)） |
| ③ 引用目标真实存在 | 满足（绑定目标在 skill/tool/persona 目录真实存在） |
| ④ 只读消费接口 | 满足（上述三个 GET 路由） |
| ⑤ 可被 Workspace 实例化或绑定 | 满足（实例化员工时绑定全解析） |
| ⑥ 自动测试 + 验证 | 满足（复盘验证通过） |
| **距达标缺口** | 无（已达标，保持即可；注意仅 `et_*` 成立，`official.employee.*` 绑定空，见 3.3） |

---

## 四、Issue 关闭 Checklist（六条件逐条核对）

每个修复 Issue 关闭前，**必须**逐条核对六条件，缺一项不得标"已真实可用"。下表是 091/092/093 三张 Issue 的关闭闸门。

### 4.1 Issue 091 — 悬空引用与空壳修复

关闭前逐条核对：

- ① 真实内容：空壳数据（10 条 `official.employee.*`、16 条 `wt_*` 字符串壳）已补内容或显式标注 design-only。**注意：`wl_*`→`wt_*` 映射已实测真实成立，不属本 Issue 必改项（见勘误）。**
- ② 稳定 ID + 版本：修复后引用 ID 与目标表真实主键一致，无残留 `tp_*`/`sp_*` 悬空（`wl_*` 已无需改）。
- ③ 引用目标真实存在：**核心闸门**——`ccp_ai_software_company.sub_package_refs_json`（`tp_code_executor`/`sp_backend_coding` 全库无归属）与 `cp_content_ops.connector_ids`（xiaohongshu/douyin/shopify 触 L2 冻结）全部解析到真实存在目标，或按 L2 冻结显式标注占位。`workflow_refs_json` 的 `wl_*`→`wt_*` 已实测解析，不再作为必改闸门（见勘误）。
- ④ 只读消费接口：本 Issue 不强制补 GET（归 093），但修复不得破坏现有 GET。
- ⑤ 可被 Workspace 实例化或绑定：重跑 `CompanyInstantiationService` 应产出 6 条 workflow 实例（`wl_*`→`wt_*` 已解析）；仅当 `sub_package_refs`/`connector_ids` 悬空项未清时才影响聚合完整性。
- ⑥ 自动测试 + 验证：有 backend 测试证明真实悬空引用（tp_/sp_、connector_ids）归零、实例化工作流产出符合预期，并贴出真实 SELECT 证据（以当前库为准，不依赖复盘旧结论）。

**判分：** 六条件全过 → 标"已真实可用"；仅目录层修复、执行仍 L2 冻结（如能力包连接器）→ 标"部分可用/只有设计（冻结）"，**不得**称"已真实可用"。

### 4.2 Issue 092 — 孤儿实例清理

关闭前逐条核对：

- ① 真实内容：18 行 `employee_instances` + 2 行 `department_instances` 已处置——要么回填真实 `et_*`/`dt_*` 模板来源，要么标记为历史导入残留、从"可被 API 解析"口径移除。
- ② 稳定 ID + 版本：保留的实例 `template_id` 必须指向真实存在的 `et_*`/`dt_*`。
- ③ 引用目标真实存在：**核心闸门**——`employee_instances.template_id` 不再出现 `et_ai_rd_*`/`et_ai_content_*` 等目标表不存在的值（复盘 三/4、5）。
- ④ 只读消费接口：清理后 `GET /api/workspace/employees/{id}/skills` 等能重新解析存活实例。
- ⑤ 可被 Workspace 实例化或绑定：存活实例可经 `create_employee_instance` 重新校验（之前因模板不存在抛 `ValueError`）。
- ⑥ 自动测试 + 验证：有测试证明孤儿清零、存活实例可解析，贴真实 SELECT 证据。

**判分：** 孤儿清零且存活实例可解析 → 标"已真实可用"；若选择保留为历史残留并移出口径，须在文档明确"非真实可用实例"。

### 4.3 Issue 093 — 补只读 GET 路由

关闭前逐条核对（本 Issue 直接命中条件 ④）：

- ① 真实内容：新 GET 路由返回真实数据（Persona 6 / Dashboard 9 / Company Package 1 / Company Template 1）。
- ② 稳定 ID + 版本：GET 支持按稳定 ID 查询。
- ③ 引用目标真实存在：GET 返回内容中引用的子资源真实存在（如 Dashboard 组件引用、Company Template 关联）。
- ④ 只读消费接口：**核心闸门**——补齐 `persona_templates`、`dashboard_templates`、`company_packages`、`company_templates` 的 GET 路由（复盘 四/3）。
- ⑤ 可被 Workspace 实例化或绑定：GET 返回的数据可被 Workspace 只读消费，不破坏实例化链路。
- ⑥ 自动测试 + 验证：有 GET 路由测试覆盖四类资产，贴路由 file:line + 真实响应证据。

**判分：** 四类 GET 补齐且测试通过 → 对应资产的条件 ④ 由"不满足"升为"满足"；但这**不自动让资产变"已真实可用"**——还需 091/092 修完 ③/⑤ 才能综合达标。

### 4.4 关闭总闸门（适用于所有修复 Issue）

任一 Issue 关闭 PR 描述必须附：`结论 / 修改内容（资产·接口·ID映射） / 事实源（表·API·版本） / 交付证据（commit·测试命令·查询结果） / Workspace 应执行 / 风险`。**缺六条件任一项的验证证据，不得标"已真实可用"，只可标"部分可用"或"只有设计（冻结）"。**

---

## 五、按设计不实例化 / 非缺陷的资产（避免误判"壳"）

复盘里多处出现"目录可查可引用但执行未实现"，容易被人误判成"空壳"。本节明确：**以下资产按设计就是目录引用/元数据注入，不实例化执行，这不是缺陷，不计入"壳"。**

| 资产 | 设计定位 | 为何不是"壳" | 证据 |
|---|---|---|---|
| Skill | 指导型元数据，提示注入式绑定，不独立执行 | 目录真实、ID 稳定、被 `et_*` 绑定解析、有 GET；"不执行"是 `skill_runtime.py:28` 明确设计 | `skill_templates`=57；`GET /api/workspace/skills/templates`(1626) |
| Tool | 目录引用，执行靠 `tool_functions` 注入（默认 None） | 目录真实可查可引用；执行未启用是 `tool_functions=None`(main.py:704) 默认设计，第三方连接器 mock 属 L2 冻结 | `tool_templates`=115；`tool_runtime.py:10` 只读投影 |
| Persona | 人格目录，被员工绑定引用 | 6 条 active、有内容、被 `et_*` 引用解析；"无 GET"是缺口（归 Issue 093），但内容真实 | `persona_templates`=6；仅 `POST /api/platform/personas`(1750) |
| 默认绑定 | 员工→skill/tool/persona 的引用关系 | 绑定全部解析成功，是"已真实可用"的实例（3.11） | `GET /api/workspace/employees/{id}/skills`(1594) 等 |

**判定口径（关键）：** 判定一个资产是"部分可用"还是"壳"，看**是否有真实内容 + 引用是否真实存在**，而不是看它"是否独立执行"。

- Skill/Tool/Persona 有真实目录内容、ID 稳定、绑定解析真实 → 标**"部分可用（目录层真实）"**，其执行能力缺失是按设计/L2 冻结，**不是缺陷**。
- 真正算"壳/空壳"的是：绑定全空的 `official.employee.*`（10 条）、`steps_json` 纯字符串的 `wt_*`（16 条）、连接器悬空的 `cp_content_ops`、空表 `quotas`(0)/`platform_policies`(0)——这些才是 Issue 091 要清的空壳（复盘 三节）。

---

## 六、一句话总结

资产完成标准只有一把尺：六条件全过才叫"已真实可用"，缺一条只能叫"部分可用"或"只有设计（冻结）"。今天**已真实可用**的是部门模板、员工模板 `et_*`、默认绑定；**部分可用**的是公司模板/公司包/Persona/Skill/Tool/Workflow/Dashboard（公司包/Workflow 卡在缺 GET 路由或 `sub_package_refs` 悬空，Workflow 另含 16 条 `wt_*` 字符串壳——注意 `wl_*`→`wt_*` 映射经实测已真实成立，勘误已更正"恒为 0"旧结论）；**只有设计（壳/悬空/冻结）** 的是能力包、Connector 目录、Plan/Pricing/Quota/Seat、多租户 D2–D4、第三方连接器、10 条 `official.employee.*` 壳、16 条 `wt_*` 字符串壳。Skill/Tool/Persona 是目录引用，内容真实、不实例化执行是按设计，别误判成"壳"。

---

*文档维护：本文件随复盘快照更新。任何资产标记"已真实可用"前，须回填本文对应验收表的六条件证据。冻结项状态变更须先过 L2 Gate。*
