# Curis 外部能力接入盘点（白话版）

> 盘点时间：2026-07-29
> 盘点范围：模型 / Agent / Skill / 连接器 / 能力目录体系 / 产品内用法 / 用户接入方式
> 结论先行：**内核（catalog→registry→resolver→adapter）已经搭好、能跑，但仓库里几乎"没有真数据"——用户从前端目前接不进任何外部能力。**

---

## 一、一句话总览（成熟度判定）

| 能力类别 | 内核是否成型 | 仓库里有没有真数据 | 用户能不能从前端接进来 | 判定 |
|---------|------------|------------------|---------------------|------|
| 模型 Model | ✅ OpenAI 兼容网关可运行 | ⚠️ 仅 1 条种子 | ❌ 无 base_url / api_key 字段 | 半成品 |
| Agent | ✅ 解析层 + 5 个硬编码运行时 | ⚠️ 走 seed 清单 | ❌ 无外部 Agent 入口 | 框架齐、数据空 |
| Skill | ✅ runtime 仅消费 3 类 | ⚠️ 模板表有数据 | ❌ 外部仓库不消费 | 受限 |
| 连接器 Connector | ✅ 2 个 REST + mock/real 双模 | ⚠️ 默认 mock | ❌ 导航里入口被删 | 可跑、未接 |
| 能力目录体系 | ✅ catalog/registry/resolver/adapter 完整 | ⚠️ 表是空的 | ⚠️ 表单只能"登记名片" | 内核成熟 |

**白话翻译**：地基、钢筋、电梯井都盖好了，但楼里还没住户，也没人发门禁卡。

---

## 二、能力类型体系（先认门）

- 内核定义了 **10 类** 能力：`model / agent / tool / connector / skill / mcp / api / cli / webhook / workflow`
  （`backend/app/catalog_constants.py:45-56`）。
- 但**对外暴露时收窄成 6 类**：`model / agent / skill / tool / workflow / connector`
  （`backend/app/capability_registry.py:12` 的 `REGISTRY_TYPES`）。
- 前端"能力中心"正好也是这 6 个 Tab：`模型 / Agent / 技能 / 工具 / 工作流 / 连接器`
  （`frontend/app/ceo-office/capabilities/page.js:27-34`）。

> 注意：mcp / api / cli / webhook 这 4 类在内核里被承认，但**前端界面和对外 registry 都看不到它们**——属于"系统认得，但用户摸不到"。

---

## 三、模型（Model）接入现状

**协议 / 网关**
- 走 `ModelGatewayAdapter`（`backend/app/model_gateway.py:75`），是 **OpenAI 兼容**的 `/v1/chat/completions` 适配层。
- 设计意图：Workspace 执行不直接绑定 OpenAI/Claude/Codex，统一收口到网关后面。

**现状（硬编码）**
- 目前只认 **1 个供应商：newapi**（网关 id `newapi`），默认模型 `gpt-5.4-mini-2026-03-17`
  （`backend/app/model_gateway.py:16-31`）。
- 落库共用一张 `official_models` 表（`backend/app/database.py:591`）。
- 种子数据**只有 1 条**：`official.newapi.default`（`backend/app/database.py:2169-2173`）。
- AI 用量计量是真实的：`ai_usage_records` 账本（`backend/app/ai_usage.py:25`），append-only。

**判定**：网关协议是可运行的"真实现成"，但仓库里**只有 1 个种子模型、没有多供应商/多模型注册入口**。想换模型或私有 base_url，目前没有配置口子。

---

## 四、Agent 接入现状

**两层结构，要分清：**

1. **离线收编层** `backend/app/agent_conversion/`——专门解析外部 Agent 框架文件：
   - `crew_adapter.py`（CrewAI yaml）、`agency_adapter.py`（Agency markdown）、`mcp_adapter.py`（MCP manifest）、`skill_adapter.py`（Skill 仓库）。
   - 这些适配器**目前只被测试引用，生产代码零调用**——属于"能解析，但解析完没人消费"。
   - 安全护栏齐备：`sanitize.py`（清 emoji/颜色/隐形字符）+ `security_scan.py`（正则扫凭证/注入/过度声明，`scan_all:47`）。

2. **运行时真适配器** `backend/app/capability_adapters.py` + `dev_agent.py`：
   - 真实能跑的 Agent 只有硬编码的 5 个（ClaudeCode / OpenAICodex / WorkBuddy 等）。
   - 规范结构 `CanonicalAgentSpec`（`canonical.py:152`）含 identity / mission / persona / workflow / capability_candidates + 治理字段，定义得很完整。

**新增 Agent 怎么进系统？**
- 不走适配器，走 **seed 清单 → `seed_pilot_b.py` CLI**，且是 **opt-in**（没挂到 `initialize()` 自动跑）。

**判定**：解析框架的能力齐备，但"只解析、不消费"；真实运行时只认 5 个硬编码 dev agent；**用户从产品里接外部 Agent 没有入口**。

---

## 五、Skill 接入现状

- 运行时 `SkillRuntime`（`backend/app/skill_runtime.py:25`）默认**只消费 3 类能力**：`model / tool / connector`
  （`skill_runtime.py:13`）。
- 前端能力中心有"技能 Skill"Tab，还有 `migrateHistoricalSkills` 迁移历史技能。
- 落库在 `skill_templates` 表。
- 外部 Skill 仓库接入走 `skill_adapter.py`（离线层，同上——不消费）。

**判定**：Skill 在产品里是"员工被授权调用的能力单元"，但运行时只挂 model/tool/connector 三类；外部 Skill 仓库目前接不进来。

---

## 六、连接器（Connector）/ 外部服务接入现状

**真实连接器只有 2 个**（都是自写 REST）：
- `aitoearn_client.py`：REST `:8080/api/create`（生成类）。
- `social_auto_upload.py`：REST `:8090/api/publish`（发布类，用 cookie 而非 OAuth）。

**双模开关**：
- 基类 `ServiceConnector`（`backend/app/connectors/base.py`）+ `ConnectorMode`（mock / real 双模，`base.py:14-34`）。
- **默认是 mock**（`current_connector_mode` 读 `CURIS_CONNECTOR_MODE`，不设这个变量就是 mock）。
- 要跑真实端点，得自己托管这两个服务，再把环境变量切成 `real`。

**判定**：代码可运行，但默认 mock、真实端点需自托管 + 环境变量；**前端导航里连接器子项被删了**（`TerraNavData.js:40-46`），用户没有配置入口。

---

## 七、能力目录管理体系（catalog / registry / resolver / adapter）

这是整盘最成熟的部分，四件套都齐：

| 组件 | 职责 | 位置 |
|------|------|------|
| `CapabilityCatalog` | 注册 + 校验（model 校验 `gateway_ref` 失败即 fail-closed；`register_external_agent` 仅接受非 model/agent 的外部能力） | `capability_catalog.py:70` / `:255-267` |
| `CapabilityRegistry` | 对外 6 类视图 + 注册接口 | `capability_registry.py:34` |
| `CapabilityResolver` | 解析需求 → 降级链 → 工厂构建 | `capability_resolver.py:140` / `_build_chain:284` |
| `CapabilityAdapterFactory` | 把能力字典变成可执行适配器 | `capability_adapters.py:322` |

**真实适配器 4 个**：`CliAdapter`(:58) / `HttpApiAdapter`(:104) / `WebhookAdapter`(:153) / `McpAdapter`(:191)。
**占位 1 个**：`UnconfiguredAdapter`(:292)——能力没配好时的兜底。
**默认不探活**：`probe_enabled=False`，即不会主动去 ping 外部能力是否在线。

**API 协议**：本会话（A5）已落定统一响应契约 `ApiResponse[T]` 信封 `{code,message,data,trace_id,timestamp}`，`code==0` 成功；能力 registry 路由挂在 `/api/capabilities/*`。

**判定**：管理内核完整、能跑；但表里是空的，且错误路径（探活、外部失败）默认是静默降级（`AUTO_DEGRADE_SILENT = True`，`capability_resolver.py:39`）。

---

## 八、产品内如何使用这些能力

- **员工挂钩**：`employee_capabilities` 桥接表（`database.py:807`）+ `EmployeeCapabilityModel`，把员工绑到 `official_models.capability_key`（能力组合）。
- **部门层**：`DepartmentManifest.capability_set` **只声明、不消费**——部门说"我要这些能力"，但运行时并不真的去解析调用。
- **CEO 的一天闭环**（本会话第 2 步落地）：调度走 `runtime_registry` 状态机，但真正"调哪个模型/工具"仍需走 `CapabilityResolver`。

**白话**：能力是"被员工认领"的，但部门那一层还是空契约，没有真正把能力灌进运行链路。

---

## 九、用户如何接入（关键断层）

这是最该让用户知道的：**现在的"能力中心"只能登记名片，接不进来真东西。**

前端表单 `CapabilityFormDrawer.js` 只收集 7 个元数据字段：
`capability_key / type / name / provider_id / model_name / description / version`
（`CapabilityFormDrawer.js:19-27`），并且**明确写明"不填写或保存密钥、Token 与 Authorization"**（`:74`）。

**结论：用户从前端目前接不进来的有——**
1. **MCP**：内核认得，但前端/registry 都看不到，无入口。
2. **外部 Agent**：解析层有、运行时无入口。
3. **私有连接器**：只 2 个内置、默认 mock、导航入口被删。
4. **私有模型 base_url / api_key**：表单只填 `model_name`，没有 base_url / 密钥字段。

**顺带澄清一个误会**：仓库根目录的 `skills-lock.json` 锁的是**开发期 AI 设计技能**（Leonxlnx/taste-skill 等 13 条，给 AI 写代码用的），**跟产品里的 Skill 能力完全不是一回事**，别混了。

凭证 Vault 页面 `control/secret-vault/page.js:13` 写了但**没进导航**；Admin 后台有 `app/platform/CapabilityCatalogPanel.js:10` 但属于另一套管理界面。

---

## 十、建议下一步（按性价比排序）

1. **把"登记"变成"能跑"**：在 `CapabilityFormDrawer` 增加 endpoint / base_url / credential_ref 字段，并打通到 `CapabilityCatalog.register_external_agent`（它已经支持 cli/http/webhook/mcp 外部能力，只是前端没接）。
   - 这一步能一次性解掉 MCP / 私有连接器 / 私有模型 三类断层。
2. **让部门层真正消费能力**：`DepartmentManifest.capability_set` 从"声明"升级为"运行时解析入口"，否则部门能力是摆设。
3. **默认探活 + 显式降级**：把 `probe_enabled` 和 `AUTO_DEGRADE_SILENT` 做成可配置，避免外部能力挂了还静默假装成功。
4. **连接器导航入口恢复**：把 connector 子项加回 `TerraNavData`，并让 `CURIS_CONNECTOR_MODE` 能在界面切换。
5. **多模型种子**：至少把模型网关从"硬编码 1 个"扩展成"可注册 N 个供应商"，否则换模型只能改代码。

---

## 附：关键代码位置速查

- 能力类型定义：`backend/app/catalog_constants.py:45-56`
- 对外 6 类：`backend/app/capability_registry.py:12`
- 模型网关：`backend/app/model_gateway.py:75`（硬编码 newapi：`model_gateway.py:16-31`）
- 模型种子：`backend/app/database.py:2169-2173`
- Agent 解析层：`backend/app/agent_conversion/*.py`（生产零调用）
- Agent 运行时：`backend/app/capability_adapters.py` + `dev_agent.py`
- 连接器：`backend/app/connectors/{aitoearn_client,social_auto_upload,base}.py`（默认 mock：`base.py:14-34`）
- 能力四件套：`capability_catalog.py` / `capability_registry.py` / `capability_resolver.py` / `capability_adapters.py`
- 前端能力中心：`frontend/app/ceo-office/capabilities/{page,CapabilityFormDrawer}.js`
- 前端表单缺口（无 endpoint/凭证）：`CapabilityFormDrawer.js:19-27,74`
