# 默认职能人才优先验证 · 2026-08-18

Status: Verification（情报专项主导，CEO 要求优先）  
范围：从 08-18 候选池（~250 候选，`Curis_Talent_Candidate_Package_2026-08-18.md`）核验 Curis 默认职能组织所需人才。  
判据：是否存在「合格外部候选」可经 License/Security 闸门 + Curis 适配 + 能力组合 + 真实任务验证晋级。无则明确报告 **Gap**；Curis 内置职能不得冒充外部市场 Expert。

---

## 0. 结论速览

| 部门 / 角色 | 外部候选结论 | 组件覆盖 | 处置建议 |
|---|---|---|---|
| 空间工程部 · 默认空间工程核心 Employee | **Gap（无外部候选）** | 无 | Curis 内置定义；不得标为外部 Expert |
| 数据分析部 · 默认 Company Analyst / 公司经营分析师 | **Gap（待组合）** | 强（数据分析/SQL/BI/研究组件齐全） | 由 Codex 组合验证，或 Curis 内置定义 |
| 储备 · Data Analyst | 组件级覆盖 | 中 | 组合或内置 |
| 储备 · Business Analyst | 组件级覆盖 | 中 | 组合或内置 |
| 储备 · BI Analyst | 组件级覆盖 | 强 | 组合或内置 |
| 储备 · Analytics Engineer | 组件级覆盖 | 弱 | 优先内置 |
| 储备 · Data Visualization | 组件级覆盖 | 中 | 组合或内置 |
| 储备 · Research Analyst | **最接近外部覆盖** | 强 | gpt-researcher / Market-research-multiagent 可直接组合 |

> 关键事实：候选池在「数据 / BI / 研究」方向**组件（Skill / MCP / Tool）充足**，但**缺少可直接晋级的「完整 Employee 角色」外部 Expert**。这与初轮审计一致——设计/产品/数据/BI 多为 Skill/工具集形态，而非独立可招募 Expert。

---

## 1. 空间工程部 · 默认空间工程核心 Employee —— Gap

**核验结果：候选池无对应外部候选。**

- 该角色本质是为 Curis 创建 / 配置 / 运维「业务空间（Workspace）」的平台工程职能，属 Curis 内部运行架构，不对应任何公开市场 Agent / Expert。
- 候选池中无任何「workspace builder / space engineering / 业务空间搭建」类外部资源。
- **处置**：此岗位必须由 Curis 自行定义内置 Employee（平台/内部职能），**严禁将自定义 Employee 冒充外部市场 Expert**。不进入外部候选库。

---

## 2. 数据分析部 · 默认 Company Analyst / 公司经营分析师 —— Gap（待组合）

**核验结果：无现成外部「公司经营分析师」Expert；但组合所需组件齐全。**

候选池相关组件（均可经 License/Security 闸门，部分需 REVIEW）：

| 组件 | 类型 | 来源 | License | 用途 |
|---|---|---|---|---|
| gpt-researcher | Expert/Tool | assafelovic | Apache-2.0 | 深度资料检索与研究综述 |
| Market-research-multiagent | Expert-Team | kunal-manjunath | MIT | 市场/竞品/财务估算报告 |
| Evidence | Tool/Skill | evidence-dev | MIT | 基于 SQL 的数据分析报告生成 |
| Snowflake / BigQuery / ClickHouse MCP | Connector | 官方/社区 | 各自（REVIEW/商用需核） | 直连数仓取数 |
| Metabase / Tableau MCP | Connector | 社区 | 各自 | BI 看板与查询 |
| 数据分析 / SQL Skill | Skill | anthropics/openai/vercel | source-available / MIT | 取数、清洗、建模 |
| finance_analysis_agent / finrobot | Expert | closure-guo / AI4Finance | MIT / Apache-2.0 | 财务指标与估值 |

**处置**：
- 不强行登记一个「Company Analyst」外部 Expert（不存在）。
- 建议 Codex 能力专项以「组合 Employee 模板」方式，从以上组件装配「公司经营分析师」：取数（SQL/MCP）+ 分析（数据 Skill）+ 研究（gpt-researcher）+ 报告（Evidence / docx Skill）。
- 或 Curis 直接定义内置「公司经营分析师」Employee。两者均不得标为外部市场 Expert。

---

## 3. 储备角色覆盖评估

| 角色 | 可组合组件 | 覆盖度 | 备注 |
|---|---|---|---|
| Data Analyst | 数据 Skill + SQL/MongoDB MCP | 中 | 取数/清洗可组合；缺端到端封装 |
| Business Analyst | Market-research-multiagent + 研究 Skill | 中 | 偏向市场研究，业务需求建模弱 |
| BI Analyst | Evidence + Metabase/Tableau MCP | 强 | 看板/报告链路最接近完整 |
| Analytics Engineer | dbt 类缺失 + SQL MCP + 数据 Skill | 弱 | 建模/血缘无现成外部候选，建议内置 |
| Data Visualization | Evidence + frontend-design Skill + 图表库 MCP | 中 | 静态报告强，交互可视化弱 |
| Research Analyst | gpt-researcher + Market-research-multiagent | 强 | **外部覆盖最佳**，可直接组合晋级 |

---

## 4. 给 Codex 能力专项的交接

1. 空间工程核心 Employee：Curis 内置，不占用外部候选配额。
2. 公司经营分析师：给出组件组合方案（§2 表），请 Codex 在 Runtime 完成绑定 + 真实任务验证 + Evidence。
3. Research Analyst / BI Analyst：外部组件覆盖强，建议优先组合验证，作为数据分析部首批可晋级候选。
4. Analytics Engineer：建议 Curis 内置，外部 Gap 明确。

> 本专项不伪造任何外部 Expert。所有「Gap」角色若由 Curis 内置实现，其来源标记为 `curis-builtin`，不在外部候选库重复登记。

---

## 5. 连续两日扫描（2026-08-18 ~ 08-19）对默认职能的补强

连续自动扫描新增 72 条去重候选（见候选包 `连续两日扫描验证入库` 段），对数据分析部组件覆盖有实质补强，但**不改变 Gap 结论**：

| 默认职能 | 连续扫描新增可用组件 | 对 Gap 影响 |
|---|---|---|
| 空间工程部核心 Employee | 无外部对应 | **Gap 不变**，仍 Curis 内置 |
| 公司经营分析师 / Company Analyst | `data-quality-auditor`（数据质量审计）、`database-lookup`（跨库检索）、`scientific-visualization`（科学可视化） | 组件更充足，但仍**无完整可招募 Employee 角色**，Gap 不变 |
| Data Analyst | `data-quality-auditor` 强化数据清洗/审计 | 覆盖从中→中强 |
| BI Analyst | `scientific-visualization` + 既有 Evidence | 覆盖保持强 |
| Research Analyst | `literature-review`（K-Dense 文献综述） | 覆盖保持强，外部最佳 |
| Analytics Engineer | 仍无 dbt/血缘类外部候选 | **Gap 不变**，建议内置 |

结论：连续扫描提升了数据分析部「组件级」覆盖，但「完整可招募 Employee 角色」仍缺失——与初轮审计一致。空间工程、Company Analyst、Analytics Engineer 必须由 Curis 内置定义，不得冒充外部 Expert。
