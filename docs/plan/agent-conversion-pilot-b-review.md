# Agent 拆解转换引擎 V1 — 受控试点 B：实现评审汇总

> 阶段：代码实现（标准 SOP 第三棒）· 作者：软件工程师（寇豆码）
> 范围：12 个目标 agency-agent → Curis 资产（et_*/pt_*/skl_*/tl_*/wt_*/dt_* + 5 business.* 部门类型），全部 draft/candidate、可回滚、不激活。
> 红线：不接凭证、不建 marketplace、不 instantiation（ADR-0017 仍锁）。

---

## 0. 结论速览

| 项 | 结论 |
|---|---|
| T9 测试 | ✅ **18 passed / 0 failed**（`tests/test_pilot_b_agent_conversion.py`） |
| 全局一致性评审 | ✅ **IS_PASS: YES** |
| 设计 §7.1 映射 | ✅ 12 个 et_* 字段（id/slug/role/department_type/persona_ref/status）逐条对齐 |
| 与既有资产冲突 | ✅ 0 冲突（候选 id 前缀 `pilot_b_`；et_* 用 `official.employee.*` 与既有 `et_%` 无交） |
| 可回滚性 | ✅ `rollback_agent_conversion_pilot_b()` 整批清零，基线 6 et_% / 115 工具 / 55 技能 / 6 persona 不变 |
| 安全三段扫描 | ✅ 全部文本字段 credential / prompt_injection / overclaim 零命中，无控制字符 |
| MIT 合规 | ✅ 12 源均标注 `source='official'` + attribution 文本，未做版权声明篡夺 |

---

## 1. 实现要点（T1–T9）

### T1 解析层契约（`canonical.py`）
`CanonicalAgentSpec` 及 12 个 dataclass（`SourceMeta` / `LicenseInfo` / `DivisionInfo` / `Identity` / `Mission` / `Persona` / `WorkflowStep` / `WorkflowSpec` / `CapabilityCandidate` / `CapabilityCandidates` / `SecurityScan` / `ConversionDisposition`）。`SecurityScan.is_clean` 提供三段零漏报判定。`asset_slug()` 由 `identity.slug` 推导。

### T2 适配器基类（`adapter_base.py`）
`SourceAdapter(ABC)` + `SourceEntry` / `SourceMetadata`。抽象方法 `discover/fetch/parse/extract_capabilities/get_metadata`，为后续范式 2/3 预留扩展点。

### T3 清洗与安全（`sanitize.py` / `security_scan.py`）
- `clean_emoji` / `clean_color`（`#RRGGBB` 严格）/ `strip_invisible` / `clean_text` / `has_control_chars`。
- 三段正则：`CREDENTIAL_PAT` / `PROMPT_INJECTION_PAT` / `OVERCLAIM_PAT`，`scan_all` 聚合，`is_clean` 判定。

### T4 源文件离线抓取（`sources/`）
12 个目标 agent 的 `.md` 离线副本，按 `sources/<division>/<slug>.md` 组织，含 YAML frontmatter + 规范章节。**唯一命名修正**：`product-feedback-synthesizer.md` → `product-feedback-synth.md`（对齐 §7.1 `slug`）。

### T5 agency 适配器（`agency_adapter.py`）
`AgencyMarkdownAdapter`：discover（过滤 5 个 allowed division）→ fetch → parse（frontmatter 优先 pyyaml、回退极简解析器；章节切分；emoji/color 清洗；MIT license；三段安全初扫）→ extract_capabilities（关键词命中 `.md` 正文，产出工具/技能候选）。

> **关键修正**：源文件名与 §7.1 规范 `asset_slug` 并非 kebab 互逆（如 `finance-financial-analyst` → `finance_analyst`、`support-support-responder` → `support_responder`）。适配器以 `PILOT_B_MANIFEST` 构建 `(division, slug) → asset_slug` 映射，归一时以 §7.1 为准，保证 `asset_slug()` 与权威映射一致。

### T6 映射与 seed 编排（`seed.py` + `database.py`）
- `PILOT_B_MANIFEST`（12）、`PILOT_B_SKILLS`（12）、`PILOT_B_TOOLS`（10）、`PILOT_B_DEPARTMENT_TYPES`（5）、`PILOT_B_DEPARTMENTS`（5）。
- `SeedMapper` 纯函数：`map_persona/map_employee/map_skill/map_tool/map_workflow/map_department`，产出 dict/tuple；`build_pilot_b_rows()` 聚合。
- `Database.seed_agent_conversion_pilot_b()`：**opt-in**，先 `initialize()`（幂等、保基线）再 `_seed_agent_conversion_pilot_b()`，按 `department_types → personas → employees → skills → tools → workflows → departments` 顺序 `INSERT OR IGNORE`。
- `Database.rollback_agent_conversion_pilot_b()`：按 id 前缀范围整批 DELETE，保留 6 官方 et_* / 115 工具 / 55 技能 / 6 官方 persona / `business.general` 基线。
- `seed_pilot_b.py`：CLI 触发入口（`--rollback` 支持）。

### T7 评审汇总文档
即本文件。

### T8 `#3` 增强备注
`sprint-prioritizer` 仅产出增强备注（写入 `ConversionDisposition.employee_action='enhance_existing'`、指向 `official.employee.tech_lead`），**不新建 et_***，符合范围限制。`#14`（project-management）/`#15`（security）按裁定**排除**。

### T9 测试（`tests/test_pilot_b_agent_conversion.py`）
18 个用例，覆盖：① 12 et_* 字段对齐 §7.1；② 与既有资产零冲突；③ 可回滚（前向/后向快照）；④ business.* department_type 合法；⑤ emoji/color 清洗 + 安全三段零漏报；⑥ 解析层（adapter + mapper）管线一致性。

---

## 2. 真实 DDL 勘误（必须上报）

实现过程中，真实 `database.py` 与实现设计稿 §0 假设存在 **4 处偏差**，均已对齐处理并建议主理人知悉：

1. **`skill_templates` / `tool_templates` 的 `status` 有 CHECK 约束**
   `status in ('draft','active','disabled','archived')` —— **不含 `'candidate'`**。
   设计 §7.1 原拟 skl_*/tl_* 用 `status='candidate'`，但真实约束会令 `INSERT OR IGNORE` 静默丢弃全部 12 技能 / 10 工具（初版测试即因此 0 插入）。
   **处置**：skl_*/tl_* 统一改用 `'draft'`（与 et_*/pt_*/wt_*/dt_* 一致，全部未激活、可回滚）。语义正确，不违反红线。

2. **基线技能数 = 55，非设计 §0 的 52**
   `initialize()` 当前 seed 55 个 `skill_templates`（含后续补的 3 个）。测试原硬编码 `base==52` 已改为 `base==55`（pilot 后 67）。

3. **基线已含 6 个 `official.employee.*`**
   `tech_lead` / `product_manager` / `architect` / `frontend_engineer` / `backend_engineer` / `qa_engineer`，`department_type='software_rnd'`、`persona_ref=''`。
   因此 `official.employee.%` 在 seed 后为 18（6 基线 + 12 Pilot B），测试改为只校验 §7.1 规定的 12 个 Pilot B id。

4. **基线已含 `business.general` 部门类型**
   Pilot B 另注册 5 个 `business.*`（product/marketing/sales/support/finance）。回滚只删 5 个 Pilot B 类型，保留 `business.general`；测试 `dt_type` 前后快照相应改为 `5 / 0`（排除 `business.general`）。

> 以上 4 项均属「设计稿早于真实 DDL 演进」造成的偏差，未改动真实 schema，仅让种子数据与测试对齐真实约束。

---

## 3. §7.1 映射核验（摘录）

| asset_slug | et id | et slug | persona_id | dept_type |
|---|---|---|---|---|
| product_feedback_synth | official.employee.product_feedback_synth | product-feedback-synth | pt_product_feedback_synth | business.product |
| product_trend_researcher | official.employee.product_trend_researcher | product-trend-researcher | pt_product_trend_researcher | business.product |
| product_nudge_engine | official.employee.product_nudge_engine | product-behavioral-nudge-engine | pt_product_nudge_engine | business.product |
| marketing_growth_hacker | official.employee.marketing_growth_hacker | marketing-growth-hacker | pt_marketing_growth_hacker | business.marketing |
| marketing_content_creator | official.employee.marketing_content_creator | marketing-content-creator | pt_marketing_content_creator | business.marketing |
| marketing_social_strategist | official.employee.marketing_social_strategist | marketing-social-media-strategist | pt_marketing_social_strategist | business.marketing |
| sales_pipeline_analyst | official.employee.sales_pipeline_analyst | sales-pipeline-analyst | pt_sales_pipeline_analyst | business.sales |
| sales_discovery_coach | official.employee.sales_discovery_coach | sales-discovery-coach | pt_sales_discovery_coach | business.sales |
| support_responder | official.employee.support_responder | support-support-responder | pt_support_responder | business.support |
| support_legal_compliance | official.employee.support_legal_compliance | support-legal-compliance-checker | pt_support_legal_compliance | business.support |
| finance_analyst | official.employee.finance_analyst | finance-financial-analyst | pt_finance_analyst | business.finance |
| finance_tax_strategist | official.employee.finance_tax_strategist | finance-tax-strategist | pt_finance_tax_strategist | business.finance |

全部 `pt_*` 的 `image_ref_json` 为真实三键 + `theme_color` 结构；`persona_ref` 100% 可解析。

---

## 4. 安全与合规

- **零凭证**：12 源文本、映射、种子均无 API key / token / 密码；`scan_credential` 全字段零命中。
- **零 prompt-injection / overclaim**：`scan_prompt_injection` / `scan_overclaim` 全字段零命中。
- **MIT 归属**：`source='official'` 且 `attribution` 文本保留原作者版权声明，未篡夺。
- **不激活**：所有 et_*/pt_*/skl_*/tl_*/wt_*/dt_* 为 `draft`/`candidate`（实际落库为 `draft`）态，未挂默认 `initialize()`，未经评审不会进入运行链路。
- **可回滚**：`rollback_agent_conversion_pilot_b()` 已验证整批清零，基线计数不变。

---

## 5. 待主理人决策 / 后续建议

1. **`status` 枚举扩展**（可选）：若希望 pilot candidate 与 draft 区分，建议在 `skill_templates` / `tool_templates` 的 status CHECK 中新增 `'candidate'` 值，届时把种子改回 `'candidate'` 即可（当前用 `draft` 仅为满足真实约束）。
2. **源文件命名**：建议统一以 §7.1 `slug` 作为 `sources/` 文件名（已修正 `product-feedback-synth`），使适配器 discover→parse 链路与权威映射天然一致。
3. **`#3` 增强**：本评审仅产出增强备注，落地增强需另行评审工单。
4. **激活门槛**：任何 et_* 进入激活态前，需经人工评审 + 触发独立实例化流程（非本 seed 职责）。
