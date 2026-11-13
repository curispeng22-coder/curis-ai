# 员工模板（Employee Template）领域研究

> 研究范围：Curis Admin Platform 的员工模板（EmployeeTemplate）应解决什么问题、字段设计、Admin 管理模板定义 vs Workspace 管理员工实例的边界、ADR-0017 员工 CRUD 禁止区的处理方式、official / tenant_private / marketplace 三态边界、与 CrewAI / MetaGPT / ChatDev 角色定义的对比、Phase-4 实现边界。
>
> 研究性质：纯研究文档，不含实现方案、不含代码改动。所有结论须与 ADR-0028 共享契约、issue 087 Phase-3.5 决策、capability-catalog-research 决策对齐。
>
> 关键约束：issue 087 §1.4 (C1) 明确 ADR-0017「员工 CRUD」禁止区须部分解禁——Template 定义（metadata）可解禁，Employee Instance 创建/执行仍锁定。

---

## 问题定义

### 1. 员工模板在 Curis 中解决什么问题

Curis 的 AI 公司由部门组成，部门由员工组成，员工执行任务。但「员工」这一概念在 Curis 中有两个层次：

- **员工实例（Employee Instance）**：租户内真实存在的员工，有生命周期（draft → active → paused → archived），绑定具体能力，执行具体任务。属于 ADR-0017 禁止区「员工 CRUD」的核心。
- **员工模板（Employee Template）**：定义员工的角色、职责、默认指令、能力类型偏好、模型策略，是**元数据**，不是员工实例本身。

员工模板解决的核心问题是：

1. **角色复用**：同一角色（如 Product Manager）可在多个部门、多个租户复用，无需每次从零定义。
2. **标准化基线**：official 员工模板提供跨租户的角色标准（如 MetaGPT 的 PM/Architect/Engineer/QA），保证 SOP 一致性。
3. **配置与实例分离**：模板定义「这个角色应做什么、可用什么能力」，实例决定「这个具体员工当前状态、绑定了哪些能力、执行哪些任务」。模板可解禁，实例仍锁定。
4. **marketplace 载体**：员工模板可作为 marketplace 商品（Role Pack），CEO 可订阅官方或第三方角色模板。

简言之：**员工模板定义角色，员工实例是角色的具象化**。模板是 metadata，可被 Admin/CEO 管理；实例是运行时实体，仍受 ADR-0017 禁止区约束。

### 2. 与 ADR-0017 禁止区的关系

issue 087 §1.4 (C1) 厘清了 Template vs Instance 的边界：

| 层次 | 对应表 | 性质 | ADR-0017 禁止区 | 评审意见 |
| --- | --- | --- | --- | --- |
| Template 定义 | `employee_templates` | 元数据 | **可解禁** | 类比 `department_types`（已解禁），不涉及真实员工创建/执行/路由 |
| Instance 实例 | `employee_instances` | 真实员工实例 | **仍锁定** | 涉及员工生命周期管理，属禁止区核心 |
| Runtime 执行 | `AIEmployee`（employee.py） | 运行时执行类 | **仍锁定** | 涉及任务路由、工具链执行、prompt 注入 |

**类比论证**：`department_types`（模板，已解禁）vs `departments`（实例，经 gate）vs 部门执行（future）；`official_models`（目录，已解禁）vs model gateway 调用（执行，经 gateway）；`employee_templates`（模板，建议解禁）vs `employee_instances`（实例，仍锁定）vs `AIEmployee` 执行（仍锁定）。

---

## 现状分析

### 1. `employee_templates` 表（已落地）

`database.py:442-456` 定义 `employee_templates` 表，Phase-3.5 已落地，含 `id`/`name`/`role`/`description`/`department_type`/`default_instructions`/`default_capability_types_json`/`default_model_policy_json`/`source`（CHECK 三态）/`tenant_id`/`enabled`/`created_at` 共 12 字段。

### 2. `employee_instances` 表（已落地，仍锁定）

`database.py:458-470` 定义 `employee_instances` 表，Phase-3.5 已创建表结构但**仍锁定**（ADR-0017 禁止区），含 `id`/`tenant_id`/`company_id`/`department_id`/`template_id`/`name`/`role`/`instructions_override`/`status`（draft/active/paused/archived）/`enabled`/`created_at`。

### 3. `employee_capability_bindings` 表（已落地）

`database.py:485-496` 定义实例级能力绑定表，`capability_source` CHECK 三态，`capability_type` CHECK **仅 3 类型**（model/tool/connector），不含 template 类型（issue 087 C4 确认）。

### 4. `AIEmployee` 执行类（仍锁定）

`backend/app/employee.py:8-48` 定义 `AIEmployee` 运行时执行类：`execute()`（执行完整任务）+ `execute_step()`（执行单步）+ `_with_role_context()`（注入角色上下文）。此执行类**仍锁定**。

### 5. 查询隔离已实现

`list_employee_templates` 已实现三态查询隔离：`source = 'official' or (source = 'tenant_private' and tenant_id = ?)`。

### 6. 已有决策锚点

- **issue 087 §1.4 (C1)**：Template 定义可解禁，须提交独立 ADR 明确解禁范围（metadata CRUD）与锁定范围（Instance 创建/激活、AIEmployee 执行）。
- **issue 087 §6.2 (C5)**：员工模板走独立 catalog，不扩展 `CAPABILITY_TYPE`。
- **issue 087 §5.3 (C4)**：`tenant_private_capabilities` 表不承载 template，tenant_private employee template 由 `employee_templates` 表自身承载。
- **issue 087 §1.2 缺失字段**：`updated_at` / `schema_version` 建议 Phase-4 S1 additive 补齐。

---

## 竞品参考

### 1. CrewAI Agent 字段

CrewAI 是员工模板字段设计的**首要参考对象**。核心字段：`role`（角色身份）、`goal`（目标）、`backstory`（背景故事）、`tools`（工具列表）、`LLM`（语言模型）、`max_iterations`（最大迭代）。

**CEO 用户面向适配**（CrewAI 字段对开发者友好，但对 CEO 过于技术化）：
- `role` → 保持 `role`（角色标签直观）
- `goal` → 转为 `responsibility`（更符合 CEO 语言）
- `backstory` → 转为隐藏的 `default_instructions`（不暴露给 CEO）
- `tools` → `CapabilityBinding`（间接绑定，不直接持有工具对象）
- `LLM` → `default_model_policy_json`（仅策略，不暴露 SDK 配置）
- `max_iterations` → `max_revision_count`（返工循环限制）

### 2. MetaGPT 角色定义

MetaGPT 内置 5 核心软件公司角色：Product Manager（输出 PRD）、Architect（设计架构/API）、Project Manager（任务分解/排期）、Engineer（实现代码）、QA Engineer（测试验证）。每个角色由具体 Action 组成（WritePRD/WriteDesign/WriteTasks/WriteCode/RunCode/WriteTest/DebugError），每个 Action 有明确输入/输出 schema。Phase-4 不引入 Action 系统，仅将 prompt 模板编码进 `default_instructions`。

### 3. ChatDev 角色定义

ChatDev 1.0 定义 7 角色（CEO/CPO/CTO/Programmer/Reviewer/Tester/Art Designer）。Curis 不用高管头衔，转化为中性角色名：CPO → Product Manager，CTO → Tech Lead/Architect，Programmer → FE/BE Engineer，Tester → QA Engineer。核心启发是双角色步骤模式（owner + reviewer），影响 `WorkflowStep` 设计而非 `EmployeeTemplate` 本身。

### 4. AutoAgents 动态角色生成

AutoAgents 支持根据任务动态生成角色。Curis 应将此作为 Workspace 内部能力（tenant_private），而非 Admin 强制能力。Phase-4 不做。

### 5. OpenAI GPT Store Custom GPT

GPT 的 `actions` + `capabilities` 模式与 Curis `default_capability_types_json` + `employee_capability_bindings` 模式类似。`visibility: private / link / public` 三档对应 Curis 三态，但 Curis 三态已足够覆盖 Phase-4 需求。

---

## 字段设计建议

### 1. EmployeeTemplate 字段表（扩展现有）

| 字段 | 类型 | 必填 | 来源 | 阶段 | 边界 |
| --- | --- | --- | --- | --- | --- |
| `id` | text PK | ✅ | 创建方 | Phase-4 S1 | 命名空间：`official.*` / `tenant:<tid>:*` / `marketplace:*` |
| `name` | text | ✅ | 创建方 | Phase-4 S1 | 模板展示名 |
| `role` | text | ✅ | 创建方 | Phase-4 S1 | 角色标签（tech_lead/product_manager/architect/frontend_engineer/backend_engineer/qa_engineer） |
| `description` | text | ✅ | 创建方 | Phase-4 S1 | 模板用途说明 |
| `department_type` | text | ✅ | 创建方 | Phase-4 S1 | → `department_types.type_key` 语义引用 |
| `default_instructions` | text | ❌ | 创建方 | Phase-4 S1 | 默认角色指令（源自 CrewAI `backstory`，隐藏不暴露给 CEO） |
| `default_capability_types_json` | text (JSON) | ❌ | 创建方 | Phase-4 S1 | 如 `["model", "tool"]`，与 `CAPABILITY_TYPE` 对齐 |
| `default_model_policy_json` | text (JSON) | ❌ | 创建方 | Phase-4 S1 | 如 `{"mode": "tenant_default"}`，不暴露 SDK 配置 |
| `source` | text (enum) | ✅ | 创建方 | Phase-4 S1 | CHECK `('official','tenant_private','marketplace')` |
| `tenant_id` | text | ✅ | 系统 | Phase-4 S1 | official='platform'，private=实际租户 |
| `enabled` | integer | ✅ | 创建方 | Phase-4 S1 | 1/0 |
| `created_at` | datetime | ✅ | 系统 | Phase-4 S1 | ISO8601 UTC |
| `updated_at` | datetime | ❌ | 系统 | Phase-4 S1 additive | **缺失字段补齐**（issue 087 §1.2） |
| `schema_version` | text | ❌ | 系统 | Phase-4 S1 additive | ADR-0028 §0.1 元约定，默认 `0.0` |
| `responsibility` | text | ❌ | 创建方 | Phase-4 S1 additive | 源自 CrewAI `goal`，CEO 面向的职责描述 |
| `role_profile` | text (JSON) | ❌ | 创建方 | Phase-4+ 预留 | 角色画像（技能、经验、风格） |
| `default_workflow_step_types` | text (JSON) | ❌ | 创建方 | Phase-5+ 预留 | 默认参与的 WorkflowStep 类型 |
| `version` | text | ❌ | 创建方 | Phase-5+ 预留 | 语义化版本 |

### 2. 字段设计理由

#### 2.1 `role` vs `responsibility` vs `default_instructions`

| 字段 | 源自 | 暴露给 CEO | 用途 |
| --- | --- | --- | --- |
| `role` | CrewAI `role` | ✅ 公开 | 角色标签（短词，如 tech_lead） |
| `responsibility` | CrewAI `goal` | ✅ 公开 | 职责描述（一句话，CEO 可读） |
| `default_instructions` | CrewAI `backstory` | ❌ 隐藏 | 详细指令（prompt 模板，CEO 不可见） |

这种分离避免了 CrewAI `backstory` 作为公开必填字段对 CEO 的技术化负担，同时保留 prompt 工程灵活性。

#### 2.2 `default_capability_types_json` vs `employee_capability_bindings`

- `default_capability_types_json`：**模板级**的类型偏好（如 `["model", "tool"]`）
- `employee_capability_bindings`：**实例级**的具体能力绑定（如 `model:gpt-4o`）

建议：instance 创建**不自动**生成 bindings，CEO 须手动配置。`default_capability_types_json` 仅作为 UI 推荐提示。

#### 2.3 `default_model_policy_json` 边界

仅定义策略形状（如 `{"mode": "tenant_default"}` 或 `{"mode": "specific", "model_key": "official.gpt_4o"}`），**不暴露** SDK 配置。模型调用须经 Model Gateway Adapter。

#### 2.4 命名空间

| source | 唯一键 | 示例 |
| --- | --- | --- |
| `official` | 全局 key | `official.employee.tech_lead` |
| `tenant_private` | 复合 key | `tenant:<tid>:employee.my_custom_analyst` |
| `marketplace` | 全局 key | `marketplace:employee.financial_analyst_v2` |

禁止 tenant_private 使用 `official.*` 或 `marketplace:*` 前缀。

### 3. 首批 Official EmployeeTemplate 建议

基于 MetaGPT 5 核心角色 + Curis 改进（增加 Tech Lead，拆分 FE/BE），Phase-4 S1 应预置 6 个 official employee templates：

| ID | role | responsibility | default_capability_types |
| --- | --- | --- | --- |
| `official.employee.tech_lead` | tech_lead | 负责任务分解、排序和最终技术协调 | `["model", "tool"]` |
| `official.employee.product_manager` | product_manager | 澄清目标、用户需求、验收标准和范围 | `["model"]` |
| `official.employee.architect` | architect | 定义模块边界、数据/API 形状和技术风险 | `["model", "tool"]` |
| `official.employee.frontend_engineer` | frontend_engineer | 在批准范围内实现 UI 和前端行为 | `["model", "tool"]` |
| `official.employee.backend_engineer` | backend_engineer | 实现 API、数据模型、执行和服务端测试 | `["model", "tool"]` |
| `official.employee.qa_engineer` | qa_engineer | 运行验证、收集证据并分类已知缺陷 | `["model", "tool", "connector"]` |

Curis 相比 MetaGPT 的改进：增加 Tech Lead 作为协调者；将 Engineer 拆分为 Frontend/Backend；Phase-4 保持最小角色集，不引入 Reviewer/Designer 等次级角色。

---

## 治理边界

### Admin 管理（official / marketplace）

#### 1. Official Employee Template

- Admin 经 `/api/platform/employee-templates` 写通道，`source='official'`，`tenant_id='platform'`
- 全局可见，所有租户经 `/api/catalog/employee-templates` 只读
- 审计事件：`template.created` / `template.status_changed`

#### 2. Marketplace Employee Template（Role Pack）

- CEO 提交 tenant_private 员工模板 → Admin 经 `/api/platform/marketplace-review` 审核 → approve 后提升为 `source='marketplace'` + `tenant_id='platform'`
- 跨租户共享触发 G3 gate
- marketplace 员工模板即「Role Pack」

#### 3. Admin API 端点建议（issue 087 §3.3）

```
POST   /api/platform/employee-templates          # 创建 official
GET    /api/platform/employee-templates          # 列表（含 inactive）
PATCH  /api/platform/employee-templates/:id      # 编辑
POST   /api/platform/employee-templates/:id/status  # 启停
```

#### 4. Admin 可见性

- Admin 可见所有 official / marketplace 员工模板（完整字段）
- Admin 可见 tenant_private 员工模板的元数据（`id`/`name`/`source`/`tenant_id`/`enabled`/`created_at`）
- Admin **不可见** tenant_private 员工模板的业务配置（`default_instructions`/`default_model_policy_json`/`responsibility`）

### Workspace 管理（tenant_private）

- CEO 经 `/api/tenant/employee-templates` 内部写通道，`source='tenant_private'`，`tenant_id=实际租户`
- CEO 可基于 official 模板派生 tenant_private 模板（复制 + 修改 `default_instructions`）
- CEO 可从零创建 tenant_private 模板（自定义业务角色）
- CEO 可提交至 marketplace 审核
- CEO **不可**修改 official 模板，**不可**跨租户共享

只读通道（Phase-4 S1）：`GET /api/catalog/employee-templates`

内部写通道（Phase-4 S2）：
```
POST   /api/tenant/employee-templates             # CEO 创建 tenant_private
GET    /api/tenant/employee-templates              # 列表（official + 本租户 private）
PATCH  /api/tenant/employee-templates/:id          # 编辑本租户 private
POST   /api/tenant/employee-templates/:id/status   # 启停本租户 private
```

### 禁止区

#### 1. ADR-0017 禁止区处理（C1 条件）

| 层次 | 表 | ADR-0017 禁止区 | Phase-4 状态 |
| --- | --- | --- | --- |
| Template 定义 | `employee_templates` | **可解禁** | Phase-4 S1-S3 解禁（metadata CRUD） |
| Instance 实例 | `employee_instances` | **仍锁定** | Phase-4 不解锁 |
| Runtime 执行 | `AIEmployee` | **仍锁定** | Phase-4 不解锁 |

**gate 建议**：提交独立 ADR（如 ADR-00xx Employee Template 解禁），明确解禁范围（metadata CRUD）与锁定范围（Instance 创建/激活、AIEmployee 执行、任务路由注入），不变式（template 不得被 `Orchestrator`/`ToolRouter`/`AIEmployee` 引用）。

#### 2. ADR-0028 §9 gate

G3（marketplace Role Pack 跨租户共享，待 gate）、G4（私有模型/工具自带凭证，员工模板不得持久化凭证）、G5（LOCKED_ACTIONS 全程锁定）。

#### 3. 不变式（Phase-4 全程）

- `employee_templates` 不得被 `Orchestrator`/`ToolRouter`/`AIEmployee` 直接引用
- `employee_instances` 创建/激活/执行仍锁定
- 员工模板不持久化任何凭证/密钥
- 员工模板不触发任务路由或 prompt 注入
- 员工模板不扩展 `CAPABILITY_TYPE`，不复用 `official_models`/`tenant_private_capabilities` 表

---

## Admin 管理模板定义 vs Workspace 管理员工实例的边界

### 1. 边界矩阵

| 维度 | EmployeeTemplate（模板定义） | EmployeeInstance（员工实例） |
| --- | --- | --- |
| 管理方 | Admin（official）/ CEO（tenant_private） | CEO（Workspace） |
| 表 | `employee_templates` | `employee_instances` |
| ADR-0017 禁止区 | **可解禁**（C1） | **仍锁定** |
| Phase-4 状态 | S1-S3 实现 | 不实现 |
| source 三态 | ✅ | N/A（实例始终属于某租户） |
| 内容 | 角色、职责、默认指令、能力类型偏好、模型策略 | 具体员工名、状态、指令覆盖、能力绑定 |
| 生命周期 | active/inactive（启停，无物理删除） | draft→active→paused→archived |
| 引用方向 | 被 department_templates/company_templates 引用 | 引用 employee_templates（template_id） |

### 2. 职责分工

**Admin 职责**：提供标准化角色模板、维护 official template 目录、审核 marketplace 提交。不管理员工实例。

**CEO 职责**：基于 official template 派生 tenant_private template、创建员工实例（Phase-5+ 经 gate 解锁）、为员工实例配置 `employee_capability_bindings`、管理员工实例生命周期。

### 3. 派生关系

```text
official.employee.tech_lead  ──派生──→  tenant:<tid>:employee.my_tech_lead  ──实例化──→  employee_instances
                                           (CEO 修改 default_instructions)                 (CEO 配置 capability_bindings)
```

---

## 前置条件

### 1. Phase-4 解锁条件

- **G-C1**：ADR-0017「员工 CRUD」禁止区部分解禁（Template 定义层），提交独立 ADR，总控决策席 + 安全边界席 gate
- **G-C3**：Admin template catalog 服务设计（`EmployeeTemplateCatalog`）
- **G-C4**：`tenant_private_capabilities` 不承载 template 的设计意图文档化
- **G-C5**：`CAPABILITY_TYPE` 保持 3 类型的决策文档化

### 2. 切片解锁依赖

- S2 依赖 S1 完成 + G-C1 gate 通过
- S3 依赖 S2 完成 + G-C3 gate 通过
- S4 依赖 S2 + S3 完成 + `employee_capability_bindings` 表结构稳定
- Marketplace 依赖 G3 gate 解锁 + 独立 ADR + 审核队列表设计

---

## Phase-4 建议

### 1. Phase-4 实现

| 切片 | 内容 | 优先级 |
| --- | --- | --- |
| S1 | Workspace 只读 official employee template（`/api/catalog/employee-templates`） | P0 |
| S1 | additive 补齐 `updated_at` / `schema_version` 列 | P0 |
| S1 | 预置 6 个 official employee templates | P0 |
| S2 | Workspace tenant_private employee template CRUD | P0 |
| S3 | Admin official employee template 管理 API（`EmployeeTemplateCatalog`） | P1 |
| S4 | Template-Capability 绑定（`employee_capability_bindings` 填充，instance 仍锁定） | P1 |

### 2. Phase-4 预留（不实现）

`role_profile`（角色画像，Phase-5+）、`default_workflow_step_types`（依赖 WorkflowStep，Phase-5+）、`version`（Phase-5+ marketplace）、Employee Instance 创建/激活（ADR-0017 禁止区，Phase-5+ gate）、AIEmployee 执行（Phase-5+ gate）、Marketplace Role Pack 审核（G3 gate 后）、动态员工生成（Workspace 内部，Phase-5+）、员工记忆（Phase-4 不做）、Hierarchical 管理者路由（Phase-5+）。

### 3. 永不实现

员工模板直接持有 `api_key`/SDK 配置（必须通过 Model Gateway Adapter）；`backstory` 作为公开必填字段（转为隐藏的 `default_instructions`）；员工模板直接绑定工具对象（须通过 `CapabilityBinding`）；员工模板触发任务路由或 prompt 注入；无界多智能体自由讨论；员工模板持久化凭证。

---

## 首批 Official Employee Template 详细定义

下表展开 `official.employee.*` 6 个模板的 `default_instructions` 形状（仅结构示例，不含完整 prompt）：

### 1. official.employee.tech_lead

```yaml
role: tech_lead
responsibility: 负责任务分解、排序和最终技术协调
default_instructions: |
  你是技术负责人。你的职责：
  1. 将 Product Manager 提供的需求拆解为可执行任务
  2. 评估任务依赖关系，制定执行顺序
  3. 协调 Frontend/Backend/Architect 的工作
  4. 在关键决策点提供技术判断
  5. 汇总团队成员的产出，形成最终交付物
  
  你不直接编码。你的输出是任务清单、决策记录、汇总报告。
default_capability_types_json: ["model", "tool"]
default_model_policy_json: {"mode": "tenant_default"}
```

### 2. official.employee.product_manager

```yaml
role: product_manager
responsibility: 澄清目标、用户需求、验收标准和范围
default_instructions: |
  你是产品经理。你的职责：
  1. 理解 CEO 提供的高层目标
  2. 澄清模糊需求，提出追问
  3. 输出 PRD（产品需求文档）：用户故事、验收标准、范围边界
  4. 评估需求优先级，与 Tech Lead 协调
  
  你不参与编码或架构设计。你的输出是 PRD 和需求澄清记录。
default_capability_types_json: ["model"]
default_model_policy_json: {"mode": "tenant_default"}
```

### 3. official.employee.architect

```yaml
role: architect
responsibility: 定义模块边界、数据/API 形状和技术风险
default_instructions: |
  你是架构师。你的职责：
  1. 基于 PRD 设计系统架构
  2. 定义模块边界和接口契约
  3. 识别技术风险并提出缓解方案
  4. 输出架构文档（含数据模型、API schema、部署拓扑）
  
  你不编码实现。你的输出是架构文档和接口契约。
default_capability_types_json: ["model", "tool"]
default_model_policy_json: {"mode": "tenant_default"}
```

### 4. official.employee.frontend_engineer

```yaml
role: frontend_engineer
responsibility: 在批准范围内实现 UI 和前端行为
default_instructions: |
  你是前端工程师。你的职责：
  1. 基于架构契约和 PRD 实现 UI
  2. 与 Backend Engineer 协调 API 调用
  3. 编写前端单元测试
  4. 遵守架构边界，不越权修改后端逻辑
  
  你的输出是可运行的前端代码和测试。
default_capability_types_json: ["model", "tool"]
default_model_policy_json: {"mode": "tenant_default"}
```

### 5. official.employee.backend_engineer

```yaml
role: backend_engineer
responsibility: 实现 API、数据模型、执行和服务端测试
default_instructions: |
  你是后端工程师。你的职责：
  1. 基于架构契约实现 API 和数据模型
  2. 编写服务端业务逻辑
  3. 编写后端单元测试和集成测试
  4. 遵守架构边界，不越权修改前端逻辑
  
  你的输出是可运行的后端代码和测试。
default_capability_types_json: ["model", "tool"]
default_model_policy_json: {"mode": "tenant_default"}
```

### 6. official.employee.qa_engineer

```yaml
role: qa_engineer
responsibility: 运行验证、收集证据并分类已知缺陷
default_instructions: |
  你是 QA 工程师。你的职责：
  1. 基于 PRD 验收标准设计测试用例
  2. 执行验证（功能、回归、边界）
  3. 收集测试证据（截图、日志、复现步骤）
  4. 分类缺陷（blocker / major / minor / enhancement）
  5. 输出测试报告
  
  你不修复缺陷。你的输出是测试报告和缺陷清单。
default_capability_types_json: ["model", "tool", "connector"]
default_model_policy_json: {"mode": "tenant_default"}
```

### 7. 与 MetaGPT 角色集对比

| Curis 角色 | MetaGPT 对应 | 差异 |
| --- | --- | --- |
| tech_lead | （新增） | MetaGPT 无显式 Tech Lead，由 Project Manager 兼任；Curis 拆分协调职责 |
| product_manager | Product Manager | 一致 |
| architect | Architect | 一致 |
| （无） | Project Manager | Curis 将 PM 任务分解职责合并入 Tech Lead |
| frontend_engineer | Engineer | Curis 拆分 FE/BE，MetaGPT 不区分 |
| backend_engineer | Engineer | Curis 拆分 FE/BE，MetaGPT 不区分 |
| qa_engineer | QA Engineer | 一致 |

Curis 6 角色 vs MetaGPT 5 角色，核心改进是 Tech Lead 独立 + FE/BE 拆分。Phase-4 不引入 Reviewer/Designer 等次级角色，保持最小集。

---

## Phase-4 S1-S4 详细验收标准

### S1 验收（只读 official）

- [ ] `GET /api/catalog/employee-templates` 返回 6 个 official 模板
- [ ] 返回字段含 `id`/`name`/`role`/`responsibility`/`description`/`department_type`/`default_capability_types_json`/`default_model_policy_json`/`source`/`enabled`
- [ ] `default_instructions` 字段对 CEO 隐藏（仅 Admin 可见）
- [ ] `updated_at` / `schema_version` 列已 additive 补齐
- [ ] 命名空间校验：所有 official 模板 `id` 以 `official.employee.` 开头
- [ ] 查询隔离：tenant A 无法看到 tenant B 的 tenant_private 模板

### S2 验收（tenant_private CRUD）

- [ ] `POST /api/tenant/employee-templates` 创建 tenant_private 成功
- [ ] 创建时 `source` 强制为 `tenant_private`，`tenant_id` 强制为当前租户
- [ ] 命名空间校验：tenant_private 模板 `id` 须以 `tenant:<tid>:employee.` 开头，禁止 `official.*` / `marketplace:*` 前缀
- [ ] `PATCH` 仅允许修改本租户 private 模板，official 模板只读
- [ ] `POST /:id/status` 启停仅作用于本租户 private 模板
- [ ] 派生 API：`POST /api/tenant/employee-templates/:id/derive` 基于 official 创建 tenant_private 副本
- [ ] 软删除策略：`enabled=0` 而非物理删除，保留引用完整性

### S3 验收（Admin 管理）

- [ ] `POST /api/platform/employee-templates` Admin 创建 official 成功
- [ ] Admin 可见所有 official / marketplace 模板完整字段
- [ ] Admin 可见 tenant_private 模板元数据（`id`/`name`/`source`/`tenant_id`/`enabled`/`created_at`）
- [ ] Admin **不可见** tenant_private 模板的 `default_instructions` / `default_model_policy_json` / `responsibility`
- [ ] 审计事件 `template.created` / `template.status_changed` 写入 `audit_events` 表

### S4 验收（Template-Capability 绑定）

- [ ] `employee_capability_bindings` 表可填充（仅 metadata，instance 仍锁定）
- [ ] `capability_type` CHECK 仅允许 `model` / `tool` / `connector`，禁止 `template` 类型
- [ ] `capability_source` CHECK 三态生效
- [ ] 部门 → 员工 → 能力类型链路验证：从 `department_templates.default_employee_templates_json` → `employee_templates.id` → `default_capability_types_json` → `CAPABILITY_TYPE` 全链路可追溯
- [ ] 引用完整性 CHECK：删除 employee template 前须检查是否被 department template 引用

---

## 风险分析

### 1. 设计风险

| 风险 | 描述 | 影响 | 缓解 |
| --- | --- | --- | --- |
| 角色集不足 | 6 个 official 角色无法覆盖所有业务场景 | CEO 须创建 tenant_private | Phase-4 允许 tenant_private 自由扩展，Phase-5+ 视需求补充 official 角色 |
| 角色集膨胀 | 引入过多 official 角色增加维护负担 | Admin 负担 | Phase-4 严格保持 6 角色，次级角色推迟 |
| 指令泄露 | `default_instructions` 误暴露给 CEO | prompt 工程泄露 | API 响应字段白名单 + Admin 与 CEO 响应分离 |
| 派生漂移 | tenant_private 派生后与 official 差异过大 | 失去标准化基线 | Phase-4 接受自由派生，Phase-5+ 评估 rebase 机制 |

### 2. 实现风险

| 风险 | 描述 | 缓解 |
| --- | --- | --- |
| ADR-0017 gate 延迟 | 独立 ADR 未通过 | Phase-4 S1 不依赖 gate（仅只读），S2 须 gate 通过 |
| `updated_at` 补齐失败 | additive 列添加失败 | 须有 migration 脚本 + 默认值 `created_at` |
| 命名空间校验遗漏 | API 层未校验前缀 | 须在 service 层 + DB CHECK 双重校验 |

### 3. 安全风险

| 风险 | 描述 | 缓解 |
| --- | --- | --- |
| prompt 注入 | `default_instructions` 含恶意指令 | Admin 创建前审查 + sandbox 试用 |
| 凭证持久化 | 误在 `default_model_policy_json` 写入 api_key | 字段形状校验 + 禁止 `api_key`/`secret`/`token` 关键词 |
| 跨租户泄露 | 查询隔离失效 | 单元测试覆盖 + 集成测试跨租户场景 |

---

## 开放问题（待 ADR 决策）

### Q1: 是否引入 Reviewer 角色

MetaGPT 无显式 Reviewer，ChatDev 有 Reviewer。Curis 是否在 Phase-5+ 引入？

- 选项 A：不引入，Tech Lead 兼任审查职责
- 选项 B：引入 `official.employee.reviewer` 作为独立角色

建议：选项 A，Phase-4/5 保持 6 角色。Phase-6+ 视 WorkflowStep 设计评估。

### Q2: `responsibility` 是否多语言

`responsibility` 字段是否支持多语言（如中英文双语）？

- 选项 A：单语言（创建方选择）
- 选项 B：多语言（`responsibility_i18n_json`）

建议：选项 A，Phase-4/5 单语言。i18n 推迟到 Phase-7+ 评估。

### Q3: 派生时是否复制 `default_instructions`

CEO 基于 official 派生 tenant_private 时，`default_instructions` 是否复制？

- 选项 A：复制（CEO 可自由修改）
- 选项 B：引用（tenant_private 仅持有 override，未 override 字段回退到 official）

建议：选项 A，复制。简化治理，避免运行时 JOIN。Phase-7+ 评估选项 B 的 override 机制。

### Q4: 员工模板与 WorkflowStep 的绑定时机

`default_workflow_step_types` 字段 Phase-5+ 预留。是否在 Phase-5 引入？

- 选项 A：Phase-5 引入，与 WorkflowStep 同步上线
- 选项 B：Phase-6+ 引入，待 WorkflowStep 稳定后再绑定

建议：选项 B，避免 Phase-5 双新功能耦合。Phase-5 仅引入 WorkflowStep 本身，Phase-6+ 绑定到 EmployeeTemplate。

### Q5: 员工记忆（Memory）的实现时机

员工记忆（基于过往任务的对话/决策历史）何时引入？

- 选项 A：Phase-5 引入（与 Employee Instance 解锁同步）
- 选项 B：Phase-6+ 引入（待 Instance 稳定后）

建议：选项 B，Phase-4/5 不做员工记忆。记忆属 Instance 层运行时能力，须待 ADR-0017 Instance gate 解锁后评估。

---

## 竞品字段映射汇总

| Curis 字段 | CrewAI 来源 | MetaGPT 来源 | ChatDev 来源 | 暴露给 CEO |
| --- | --- | --- | --- | --- |
| `role` | `role` | 角色名 | 角色名 | ✅ |
| `responsibility` | `goal`（转化） | 职责描述 | 职责描述 | ✅ |
| `default_instructions` | `backstory`（转化） | 角色 prompt | 角色 prompt | ❌ 隐藏 |
| `default_capability_types_json` | `tools`（类型化） | Action 依赖工具类型 | 研讨会工具类型 | ✅ |
| `default_model_policy_json` | `LLM`（策略化） | N/A | N/A | ✅（仅策略） |
| `department_type` | N/A | 部门归属 | 研讨会归属 | ✅ |
| `source` | N/A | N/A | N/A | ✅ |
| `enabled` | N/A | N/A | N/A | ✅ |

---

## 结论

### 1. 核心结论

1. **员工模板定义角色，员工实例是角色的具象化**。模板是 metadata（可解禁），实例是运行时实体（仍锁定）。
2. **ADR-0017 禁止区部分解禁**（C1）：Template 定义层可解禁，Instance 创建/激活、AIEmployee 执行仍锁定。
3. **字段设计采纳 CrewAI + MetaGPT**：`role` + `responsibility`（CrewAI `goal` 转化）+ `default_instructions`（CrewAI `backstory` 转化，隐藏）+ `default_capability_types_json`（类型化）+ `default_model_policy_json`（策略化）。
4. **首批 6 个 official 角色**：Tech Lead / Product Manager / Architect / Frontend Engineer / Backend Engineer / QA Engineer。
5. **走独立 catalog**，不扩展 `CAPABILITY_TYPE`，不复用 `official_models`/`tenant_private_capabilities` 表。
6. **三态治理一致**：official / tenant_private / marketplace，与 capability / department_template 模式完全对齐。

### 2. Phase-4 实现边界

- **实现**：S1 只读 official + S2 tenant_private CRUD + S3 Admin 管理 + S4 capability 绑定（metadata only）
- **预留**：`role_profile` / `default_workflow_step_types` / `version` / Employee Instance / AIEmployee 执行
- **永不实现**：直接持有凭证、`backstory` 公开、直接绑定工具对象、触发 prompt 注入

### 3. 一句话总结

**员工模板是 Curis AI 公司的角色定义层，Phase-4 优先实现 S1-S4（metadata CRUD + capability 绑定），ADR-0017 禁止区部分解禁（Template 解禁、Instance/Runtime 仍锁定）；字段设计采纳 CrewAI role/goal/backstory 转化为 role/responsibility/default_instructions，首批 6 个 official 角色基于 MetaGPT 改进；走独立 catalog 不扩展 CAPABILITY_TYPE，三态治理与下层 capability 完全一致。**
