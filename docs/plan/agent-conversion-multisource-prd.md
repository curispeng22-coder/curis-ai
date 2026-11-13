# Agent 拆解转换引擎 V1 — 多源扩展 PRD

> **版本**：Multi-Source PRD v1.0
> **作者**：产品经理 许清楚（software-product-manager）
> **阶段**：L2 暂停四项 #4 解冻范围已扩展至多源 → 多源扩展进入标准 SOP 第一棒（PRD）
> **衔接文档**：`agent-conversion-multisource-research.md`（逐源评估）/ 试点 B 三件套（PRD·设计·评审）/ `agent-conversion-engine-v1-design.md`（4.1–4.4）
> **红线声明**：所有外部资产以 **draft 态入库、可回滚**（真实 DDL `status` CHECK 不含 `'candidate'`，统一用 `'draft'`）；不接入凭证、不建 marketplace、不 instantiation（ADR-0017 锁 Instance/Runtime）。本 PRD **不写实现代码**，仅定义范围与验收。

---

## 0. 项目信息

| 项 | 内容 |
|----|------|
| Language | 简体中文 |
| Programming Language | Python（backend，对齐 `database.py` / `SourceAdapter` 设计）；本阶段**无前端 UI 范围** |
| Project Name | `agent_conversion_multisource` |
| 原始需求复述 | 在受控试点 B（仅 agency-agents 单源）方法论验证通过（QA 双轮全绿）的基础上，把 L2 #4 解冻范围扩展到多源，按研究评估选 2–3 个高保真源（CrewAI / curispeng22-coder/skill / MCP Registry），把异构源经统一 `SourceAdapter` 归一为 `CanonicalAgentSpec` 后转换为 Curis 候选资产；**仅新增 Adapter + 扩展 manifest**，复用试点 B 模块。 |

---

## 1. 产品目标

| # | 目标 | 说明 |
|---|------|------|
| G1 | **复用并证明多源范式可扩展** | 在试点 B 的 `SourceAdapter` 范式上新增 2–3 个 Adapter，证明"一次归一、多次复用"——新源仅需新增 Adapter，不改动映射流水线。 |
| G2 | **扩容互补资产（可控、零冲突）** | 为多源补充 `et_*`(CrewAI)/`skl_*`+`tl_*`(skill 仓库)/`tl_*`(MCP) 候选，全部 draft 态、可回滚，与现有 6 官方员工/115 工具/55 技能零冲突。 |
| G3 | **沉淀"增强而非新建"纪律** | 对与既有资产（尤其 Pack F-J 28 条、已 seed MCP 工具）重叠的源，一律判 `enhance_existing`；净新增聚焦 `skl_*` 方法论与未覆盖工具。 |

> 三目标正交：G1 验证工程扩展、G2 产出业务资产、G3 守资产治理。

---

## 2. 用户故事（总控 / Admin 视角）

1. 作为 **Admin**，我希望新源（CrewAI/skill 仓库/MCP）经同一 `SourceAdapter` 流水线转换为候选资产（draft 态），以便安全、可控地扩容 AI 资产库。
2. 作为 **Admin**，我希望所有跨源资产以 draft 态入库且可经独立回滚函数整批回滚（按源 id 前缀），以便受控评审、随时撤销。
3. 作为 **总控**，我希望转换全程过安全红线扫描（凭证剥离 / prompt 注入 / 越权降级）与许可闸门（copyleft/无 LICENSE 拒绝），以便外部内容不污染官方资产。
4. 作为 **总控**，我希望抽取的技能/工具候选与现有 115 工具/55 技能比对去重，重叠项标记 `enhance_existing`，以便零冲突地扩充资产、避免重复。
5. 作为 **架构师**，我希望本阶段仅新增 Adapter 文件 + 扩展 manifest/seed 函数，复用试点 B 的 `canonical/sanitize/security_scan/adapter_base`，以便边际成本最低、不回归试点 B 已验证链路。

---

## 3. 需求池（P0 / P1 / P2）

### P0 — 必须，多源扩展核心

| # | 需求 | 说明 / 验收要点 |
|---|------|------|
| P0-1 | **新增 `CrewYamlAdapter`** | 解析 CrewAI `.yaml`（role/goal/backstory/tools）；结构化直映射 `et_*`/`tl_*`/`wt_*`，跳过 NLP 抽取；复用 `sanitize`/`security_scan`。 |
| P0-2 | **新增 `SkillRepoAdapter`** | 遍历 curispeng22-coder/skill 的 `SKILL.md`；skill→`skl_*`（净新增方法论）、工具引用→命中 `tl_*` 或 candidate；与 Pack F-J 28 条重叠者判 `enhance_existing` 不新建。 |
| P0-3 | **新增 `MCPManifestAdapter`** | 解析 MCP server manifest；`tools→tl_*`（纯工具源）；与已 seed MCP 工具（Pack A/C）重叠者判 `enhance_existing`。 |
| P0-4 | **三源 draft 态入库 + 独立回滚** | 每源独立 opt-in seed 函数（`INSERT OR IGNORE`，幂等）+ 独立回滚函数（按 `crew_`/`skill_`/`mcp_` id 前缀范围 `DELETE`）；**不挂默认 `initialize()`**；`status='draft'`（非 active）。 |
| P0-5 | **跨源零冲突 + 许可闸门** | 入库前与 6 官方员工/115 工具/55 技能做 id/slug 冲突校验；关卡①扫 SPDX，`copyleft`/无 LICENSE 源拒绝（curispeng22 须先确认授权，见待确认 #1）。 |

### P1 — 重要

| # | 需求 | 说明 |
|---|------|------|
| P1-1 | **安全三段扫描全覆盖** | 三源文本字段全经 `security_scan.py`（credential/prompt-injection/overclaim），零漏报；模板永不持久化凭证。 |
| P1-2 | **`skl_*` 方法论抽取（skill 仓库核心净新增）** | 从 curispeng22 抽 `skl_*`（default_capability_types_json=['model'] + additive `category`），与已存 `tl_*` 形成"工具+方法论"配对。 |
| P1-3 | **去重 / 星级 + 汇总评审稿** | 三源候选与现有资产比对，重叠项标 `enhance_existing`；按净新增价值给 ★1~5；输出多源汇总评审稿（安全/许可/去重结论）。 |
| P1-4 | **（可选）`SeedMapper` 通用化** | 若架构师判断，把试点 B 的 manifest 驱动的 `SeedMapper` 重构为消费 `CanonicalAgentSpec` 的通用映射器（源无关）；否则每源沿用 manifest 形状复用 `map_*` 函数。 |

### P2 — 可选 / 后置（本 PRD 不强制）

| # | 需求 | 说明 |
|---|------|------|
| P2-1 | **`PlatformExportAdapter`（Coze/Dify）** | 用户自有 bot 导入试点；需剥离平台私有 schema；marketplace bot 不纳入。 |
| P2-2 | **`AgentConfigAdapter`（AutoGPT）** | 与 CrewAI 范式重叠，待 CrewAI 验证后补刀。 |
| P2-3 | **`wt_*` / `dt_*` 草稿** | CrewAI task / Coze node 可落 `wt_*` 步骤草稿；MCP 为纯工具源不产 `wt_*`/`dt_*`。 |

---

## 4. 范围边界 / 不在范围内

| 维度 | 处理 |
|------|------|
| 资产状态 | ✅ 仅 **draft 态**（`status` CHECK 不含 `'candidate'`，试点 B 评审已勘误）；❌ **不 active 全量、不碰 Instance/Runtime**。 |
| 凭证 | ❌ 不接入、不持久化任何 api_key/secret/token/password。 |
| marketplace | ❌ 不建立、不触发 G3 marketplace gate。 |
| instantiation | ❌ 不创建 Employee Instance / 不触发 Runtime（ADR-0017 仍锁）。 |
| 源范围 | ✅ 首批 CrewAI + curispeng22-coder/skill + MCP Registry；❌ 不纳入 Coze/Dify（P2）、AutoGPT（P2）、GitHub Trending/Awesome（仅索引）。 |
| 改造范围 | ✅ **仅新增 Adapter + 扩展 manifest/seed**（opt-in）；❌ **不改动** 试点 B 已落地代码（`canonical/sanitize/security_scan/adapter_base/agency_adapter/seed` 保持 importable 复用）。 |
| 冲突约束 | ❌ 不与 6 官方员工 / 115 工具 / 55 技能冲突（靠 id 前缀 + 入库前冲突校验）。 |

---

## 5. 验收标准

1. **范式可扩展**：新增 3 个 Adapter 均继承 `SourceAdapter` ABC，输出合规 `CanonicalAgentSpec`（required 字段齐全）；试点 B 链路无回归（其 18 passed 测试仍绿）。
2. **字段映射正确**：三源产出的 `et_*`/`pt_*`/`skl_*`/`tl_*`/`wt_*` 候选严格对齐设计稿 4.3 映射；emoji/color 经清洗后落 `pt_*.image_ref_json`（真实三键 `avatar/nickname/identity` + `theme_color`）。
3. **安全零漏报**：三源全字段 credential/prompt-injection/overclaim 零漏报；无凭证持久化。
4. **draft 态可回滚**：三源资产 `status='draft'`（非 active），各源独立回滚函数按 id 前缀整批清零，基线 6 员工/115 工具/55 技能/6 persona/`business.general` 不变。
5. **零冲突 + 增强纪律**：与 6 官方员工/115 工具/55 技能零命名/语义冲突；Pack F-J 28 条与已 seed MCP 工具均 `enhance_existing`（不新建重复 `tl_*`）；净新增聚焦 `skl_*` 方法论。
6. **许可闸门**：`copyleft`/无 LICENSE 源拒绝 harvest；curispeng22 在授权确认前不落库（见待确认 #1）。

---

## 6. 待确认问题（给总控 / 架构师）

1. **【blocker】curispeng22 许可授权**：该仓库多为个人仓库、无明确 LICENSE。catalog 已部分入库 28 条属历史决策；多源扩展**规模化 harvest 前是否取得明确授权**？未确认前 `SkillRepoAdapter` 仅产设计态、不 seed。
2. **首批源数量**：确认首批为 3 源（CrewAI+skill 仓库+MCP）还是先 2 源（CrewAI+MCP，延迟 skill 仓库至授权确认后）？本研究推荐 3 源但受 #1 制约。
3. **`SeedMapper` 重构 vs 复用**：架构师判断是否把试点 B manifest 驱动的 `SeedMapper` 重构为消费 `CanonicalAgentSpec` 的通用映射器（P1-4）；本研究不强制，倾向"复用 `map_*` 函数 + 每源 manifest 形状"以最低边际成本落地。
4. **`skl_*` 与 `tl_*` 配对粒度**：skill 仓库抽出的方法论 `skl_*` 与已存 `tl_*` 是否强制一一配对，还是允许独立 `skl_*` 存在？影响净新增 `skl_*` 数量。
5. **`enhance_existing` 落库策略**：Pack F-J 28 条 / 已 seed MCP 工具的"增强"是仅补 `description`/`instruction_excerpt`（UPDATE），还是另建 draft 候选待评审覆盖？须明确避免重复行。

---

## 附 A：范围建议（给总控的决策输入）

> 本研究对"首批选哪 2–3 源 / 每源 harvest 多少 / 落哪些资产 / 候选态与回滚"的明确建议。

| 源 | 适配器 | 首批？ | harvest 数量（建议） | 落地资产类型 | 主要处置 |
|------|------|------|------|------|------|
| **CrewAI** | `CrewYamlAdapter` | ✅ 首批 | 15–20 候选 agent，去重后首批 ~10–15 | `et_*` + `tl_*` + `wt_*` | 净新增 `et_*`（研发/通用，补 CrewAI 系角色）、`tools→tl_*` 命中或 candidate |
| **curispeng22-coder/skill** | `SkillRepoAdapter` | ✅ 首批（授权 gate） | 全量 skill 遍历；增强 Pack F-J 28 条 + 抽 `skl_*` ~10–20 + 净新增 `tl_*` 若干 | `skl_*` + `tl_*` | 28 条 `tl_*`→`enhance_existing`；净新增 `skl_*` 方法论；超出 28 条的新工具→`tl_*` candidate |
| **MCP Registry** | `MCPManifestAdapter` | ✅ 首批 | 精选 10–15 高价值 server | `tl_*` | 与 Pack A/C 已 seed MCP 重叠→`enhance_existing`；补全未覆盖 server→`tl_*` candidate |
| Coze/Dify | `PlatformExportAdapter` | ⏸ P1 | 用户自有 bot 试点 ~5–10 | `wt_*` + `tl_*` + `et_*` | ToS/许可 gate；marketplace bot 不纳入 |
| AutoGPT | `AgentConfigAdapter` | ⏸ P2 | 视 CrewAI 验证后补刀 | `et_*` + `tl_*` | 与 CrewAI 重叠 |
| GitHub Trending/Awesome | — | ❌ 不纳入 | — | — | 仅作源发现索引 |

**候选态 + 回滚纪律（沿用试点 B）**：
- `status='draft'`（真实 DDL `status` CHECK 不含 `'candidate'`，试点 B 评审已勘误，全链路统一 `'draft'`）。
- `source='official'`、`tenant_id='platform'`、幂等主键 + `INSERT OR IGNORE`。
- 每源独立 opt-in seed 函数 + 独立回滚函数（按 `crew_` / `skill_` / `mcp_` id 前缀范围 `DELETE`），不挂默认 `initialize()`。
- 每源 id 前缀不同，保证跨源及与试点 B（`pilot_b_` 前缀）零冲突。

---

## 附 B：复用试点 B 模块（架构师实现边界）

**直接复用（importable，不改）**：
- `agent_conversion/canonical.py`（CanonicalAgentSpec 及子 dataclass）
- `agent_conversion/adapter_base.py`（SourceAdapter ABC + SourceEntry + SourceMetadata）
- `agent_conversion/sanitize.py`（clean_emoji / clean_color / strip_invisible / clean_text / has_control_chars）
- `agent_conversion/security_scan.py`（scan_credential / scan_prompt_injection / scan_overclaim / scan_all）
- `agent_conversion/seed.py` 的 `SeedMapper.map_*`（源无关纯函数，新源 manifest 复用其形状）

**新增（本阶段）**：
- `agent_conversion/crew_adapter.py`（`CrewYamlAdapter`）
- `agent_conversion/skill_adapter.py`（`SkillRepoAdapter`）
- `agent_conversion/mcp_adapter.py`（`MCPManifestAdapter`）
- `agent_conversion/seed_multisource.py`（三源 manifest：CREWAI_MANIFEST / SKILL_MANIFEST / MCP_MANIFEST + 各源 build_rows）
- `database.py` 新增 3 个 opt-in seed 函数 + 3 个回滚函数（additive，`INSERT OR IGNORE`，不挂默认 `initialize()`）

**真实 DDL 8 处偏差（沿用须知，避免重蹈试点 B 覆辙）**：
1. `et_*` / `pt_*` **无** `(tenant_id, slug)` 唯一约束 → 幂等靠主键 + `INSERT OR IGNORE`。
2. `pt_*.image_ref_json` 真实三键 = `{avatar, nickname, identity}` + `theme_color`（非 `avatar_emoji/identity_description`）。
3. `decision_style` **无 CHECK** 枚举 → 自由文本。
4. `department_types` 真实仅 4 个（`business.general` / `function.hr` / `function.admin` / `function.bi`）→ 新 `business.*` 须补。
5. `skl`/`tl` `status` CHECK **不含** `'candidate'` → 用 `'draft'`。
6. 基线技能数 = **55**（非 52）。
7. 基线已含 **6 个** `official.employee.*`（tech_lead/product_manager/architect/frontend_engineer/backend_engineer/qa_engineer）。
8. 基线已含 `business.general` 部门类型（回滚仅删本阶段新增的类型）。

---

*本 PRD 为多源扩展的范围与验收定义，不含任何实现代码。后续由架构师据此做实现设计 + 任务分解（建议并行复用试点 B 的 T1–T9 切片结构）。*
