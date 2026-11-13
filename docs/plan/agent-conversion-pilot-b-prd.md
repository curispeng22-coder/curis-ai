# Agent 拆解转换引擎 V1 — 受控试点 B 产品需求文档（PRD）

> 版本：Pilot-B PRD v1.0
> 作者：产品经理 许清楚（software-product-manager）
> 阶段：L2 暂停四项 #4 已解冻 → 受控试点 B 进入标准 SOP 第一棒（PRD）
> 衔接文档：`agent-conversion-engine-v1-plan.md`（规划稿）/ `agent-conversion-engine-v1-design.md`（设计稿）/ `agent-conversion-engine-v1-report.md`（汇编）
> 红线声明：所有外部资产以 **candidate/draft 态入库、可回滚**；不接入凭证、不建 marketplace、不 instantiation（ADR-0017 锁 Instance/Runtime）。本 PRD **不写实现代码**，仅定义范围与验收。

---

## 0. 项目信息

| 项 | 内容 |
|----|------|
| Language | 简体中文 |
| Programming Language | Python（backend，对齐 `database.py` / `SourceAdapter` 设计）；本试点**无前端 UI 范围** |
| Project Name | `agent_conversion_pilot_b` |
| 原始需求复述 | 把 L2 暂停四项 #4 解冻后的首刀落在「受控试点 B」——仅以 `agency-agents`（MIT，范式 1）为源，转换 marketing/sales/support/finance/product 5 个商业 division 的外部 Agent 为 Curis 官方员工候选（`et_*`+`pt_*` 先落，`skl_*`/`tl_*` 先出 candidate，`wt_*`/`dt_*` 仅草稿），走标准 SOP，不盲目灌 230+ agent。 |

---

## 1. 产品目标

| # | 目标 | 说明 |
|---|------|------|
| G1 | **验证转换引擎端到端** | 跑通 `SourceAdapter → CanonicalAgentSpec → et_*/pt_* 字段映射 → Admin 写通道 seed（candidate/draft）` 全链路，证明方法论可落地、可回滚。 |
| G2 | **补商业职能员工缺口** | 为 Curis 增补 marketing/sales/support/finance/product 的 AI 员工候选（现有仅 6 个研发官方员工，商业职能为零），与现有资产零冲突。 |
| G3 | **沉淀可复用 SourceAdapter** | 以 agency-agents 为范式 1，把异构源归一为 `CanonicalAgentSpec`，解耦「源解析」与「Curis 映射」，为后续 CrewAI / skill 仓库 / Coze 等多源扩展铺路。 |

> 三目标正交：G1 验证工程链路、G2 产出业务资产、G3 沉淀长期能力。

---

## 2. 用户故事（总控 / Admin 视角）

1. 作为 **Admin**，我希望外部 agent 经标准化流水线转换为 official 员工候选（candidate/draft），以便在不激活的前提下安全扩充 AI 员工库。
2. 作为 **Admin**，我希望所有外部资产以 candidate/draft 态入库且可经 Admin 写通道整批回滚，以便受控评审、随时撤销。
3. 作为 **总控**，我希望转换全程过安全红线扫描（凭证剥离 / prompt 注入 / 越权降级），以便外部内容不污染官方资产、不持久化任何凭证。
4. 作为 **Admin**，我希望抽取的技能/工具候选与现有 115 工具、52 技能比对去重，重叠项标记 enhance_existing，以便零冲突地扩充资产。
5. 作为 **总控**，我希望 SourceAdapter 范式可复制到 CrewAI / skill 仓库等后续源，以便降低未来多源扩展的边际成本。

---

## 3. 需求池（P0 / P1 / P2）

### P0 — 必须，试点核心

| # | 需求 | 说明 / 验收要点 |
|---|------|------|
| P0-1 | **解析层基础设施** | 落地 `SourceAdapter` 抽象契约 + `CanonicalAgentSpec` 中间 schema + emoji/color 清洗器（见设计稿 4.1 / 4.2 / 4.4-Q5）。优先实现 `MarkdownFrontmatterAdapter`。 |
| P0-2 | **解析 5 division 真实 agent 文件** | 抓取并解析 5 division 的 agent `.md`，生成合规 `CanonicalAgentSpec` 集合；过 frontmatter/章节完整性校验（类 `lint-agents.sh`），解析失败告警。 |
| P0-3 | **`pt_*` persona 抽取 + `et_*.persona_ref` 关联** | 从 Identity/Style/Communication 抽 persona，落独立 `persona_templates`；`et_*` 经 `persona_ref` 引用；emoji/color 清洗后落 `pt_*.image_ref_json`（**不经 et_***）。 |
| P0-4 | **`et_*` 字段填充** | 填充 `role / responsibility / default_instructions / guardrails_json / department_type / default_capability_types_json`，严格对齐设计稿 4.3.1 映射（含 `persona_overrides_json` delta）。 |
| P0-5 | **经 Admin 写通道 seed 为 candidate/draft 态** | 经 `/api/platform/*` 或 `database.py` seed 函数落 candidate/draft；**不 active 全量、不碰 Instance/Runtime**。 |

### P1 — 重要

| # | 需求 | 说明 |
|---|------|------|
| P1-1 | **`skl_*`/`tl_*` candidate 抽取 + 安全审查** | 从 Deliverables/Advanced Capabilities 抽隐含工具/技能，未命中 Curis 库的出 candidate；过三类安全审查（credential 剥离 / prompt 注入 / 越权降级）。禁止凭空生成工具 id。 |
| P1-2 | **许可合规（MIT 署名保留）** | 登记 SPDX=MIT；`attribution_required=true` → 在 catalog/audit 保留原作者与 MIT 文本；copyleft（GPL/AGPL）源拒绝 harvest。 |
| P1-3 | **去重 / 星级** | 15 条种子与现有 6 官方员工比对，重叠项（`#3 sprint-prioritizer`、`#14 senior-pm`）标 enhance_existing；按净新增价值给 ★1~5。 |

### P2 — 可选 / 后置

| # | 需求 | 说明 |
|---|------|------|
| P2-1 | **`wt_*` 步骤草稿** | schema 已就绪（`workflow_templates`/`workflow_contents` 已落地）；仅补全 `expected_output` + `owner_role`（单 agent 缺省=该 role）。 |
| P2-2 | **`dt_*` division→department 映射稿** | 仅产出 division→`department_types.type_key` / `dt_*` 映射设计稿（反向归集 `default_employee_templates_json`）。 |
| P2-3 | **汇总评审稿** | 输出 pilot B 资产总览 + 安全/许可/去重结论，交 Admin / 安全边界席评审。 |

---

## 4. 范围边界 / 不在范围内

| 维度 | 处理 |
|------|------|
| seed 状态 | ✅ 仅 candidate/draft 态；❌ **不 seed active 全量** |
| 凭证 | ❌ 不接入、不持久化任何 api_key/secret/token/password |
| marketplace | ❌ 不建立、不触发 G3 marketplace gate |
| instantiation | ❌ 不创建 Employee Instance / 不触发 Runtime（ADR-0017 仍锁） |
| 源范围 | 仅 `agency-agents`（范式 1）；❌ 不引入 CrewAI / skill 仓库 / Coze 等后续源 |
| division 范围 | 优先 5 商业 division（marketing/sales/support/finance/product）；❌ 不处理 engineering/design（已覆盖后置） |
| 章节 | ❌ 不处理 `## Learning & Memory`（Phase-4 不支持员工记忆，仅记录不映射） |
| 规模 | ❌ 不盲目灌 230+ agent；仅 15 条种子清单 |

---

## 5. 验收标准

1. **解析完整性**：5 division、15 条种子清单的真实 agent 文件解析无遗漏，每条产出合规 `CanonicalAgentSpec`（required 字段齐全：spec_version/source/license/division/identity/security_scan）。
2. **字段映射正确**：生成的 `et_*`/`pt_*` 候选严格符合设计稿 4.3.1 / 4.3.2 字段映射；emoji/color 经清洗后落 `pt_*.image_ref_json`（不直接落 et_*）。
3. **安全零漏报**：三类风险扫描零漏报——credential 不持久化、prompt_injection 清洗/打回、overclaim 降级为受控 `skl_*` 或剔除。
4. **candidate/draft 态可回滚**：全部资产 `status` 非 active，可经 Admin 写通道整批回滚。
5. **零冲突**：与现有 6 官方员工、115 工具、52 技能零命名/语义冲突；重叠项（#3/#14）仅 enhance_existing，不新建冲突 et_*。

---

## 6. 待确认问题（给架构师 / 总控）

1. **写通道方式**：P0-5 的 candidate/draft seed，是允许工程师直接写 `database.py` seed 函数（SQL 直落），还是必须经 `/api/platform/*` 写通道？影响回滚与权限审计实现路径。
2. **security slug 确认**：#15（security-compliance-strategist）真实 slug 待抓取确认（security 共 10 agent），pilot B 是否仍需先补全 slug 再纳入，或允许语义占位待补？
3. **enhance_existing 落库策略**：#3/#14 与 tech_lead 重叠，是写 `et_*` delta 到 `persona_overrides_json`、仅登记 `conversion_disposition=enhance_existing` 不建新 `et_*`、还是并入 tech_lead 的 `default_*`？
4. **division 范围边界**：种子清单含 #14(project-management)、#15(security)，超出 5-division 目标（marketing/sales/support/finance/product）。二者是否纳入 pilot B seed，还是仅作 design 态候选、不落库？
5. **persona 深合并边界**：`et_*.persona_ref → pt_*` 与 `et_*.persona_overrides_json` 的深合并优先级与冲突解决规则，需架构师给出确定契约（避免为微调 fork 整个 persona）。

---

## 附 A：种子清单（15 条，来自规划稿 5.4 候选 harvest）

| # | 源 slug | division | 目标 et_* 草案 | 处置 | ★ |
|---|------|------|------|------|------|
| 1 | product-feedback-synthesizer | product | `et_product_feedback_synth` | create | ★★★★ |
| 2 | product-trend-researcher | product | `et_product_trend_researcher` | create | ★★★ |
| 3 | product-sprint-prioritizer | product | `et_product_sprint_prioritizer` | enhance_existing (tech_lead) | ★★★ |
| 4 | product-behavioral-nudge-engine | product | `et_product_nudge_engine` | create | ★★★ |
| 5 | marketing-growth-hacker | marketing | `et_marketing_growth_hacker` | create | ★★★★★ |
| 6 | marketing-content-creator | marketing | `et_marketing_content_creator` | create | ★★★★★ |
| 7 | marketing-social-media-strategist | marketing | `et_marketing_social_strategist` | create | ★★★★ |
| 8 | sales-pipeline-analyst | sales | `et_sales_pipeline_analyst` | create | ★★★★ |
| 9 | sales-discovery-coach | sales | `et_sales_discovery_coach` | create | ★★★ |
| 10 | support-support-responder | support | `et_support_responder` | create | ★★★★★ |
| 11 | support-legal-compliance-checker | support | `et_support_legal_compliance` | create | ★★★★ |
| 12 | finance-financial-analyst | finance | `et_finance_analyst` | create | ★★★★★ |
| 13 | finance-tax-strategist | finance | `et_finance_tax_strategist` | create | ★★★ |
| 14 | project-management-senior-project-manager | project-management | `et_project_senior_pm` | enhance_existing (tech_lead) | ★★★★ |
| 15 | security-compliance-strategist* | security | `et_security_compliance` | create（slug 待确认） | ★★★★ |

> *division 实际分布：product 4 / marketing 3 / sales 2 / support 2 / finance 2 / project-management 1 / security 1。#14、#15 超出 5-division 目标，见待确认问题 #4。

## 附 B：实现切片参考（架构师 T1–T6，来自设计稿）

- **T1** 解析层基础设施（P0-1）→ **T2** 解析 5 division 生成 spec（P0-2）→ **T3** persona 抽取 + 关联（P0-3）→ **T4** et_* 字段填充（P0-4）→ **T5** skl_*/tl_* candidate + 安全 + 许可（P1）→ **T6** wt_*/dt_* 草稿 + 总评审（P2）。
- 全部为 candidate/草稿；真实 seed 仅在解冻后经 Admin 写通道执行，并过规划稿章节 3 关卡⑦安全评审。

---

*本 PRD 为受控试点 B 的范围与验收定义，不含任何实现代码。后续由架构师据此做实现设计 + 任务分解。*
