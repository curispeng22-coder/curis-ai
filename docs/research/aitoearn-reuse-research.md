# AiToEarn 复用可行性研究 · 内容营销部门一站式集成

> **研究日期**：2026-07-12
> **研究人**：产品经理 许清楚（software-product-manager）
> **性质**：纯研究 / 复用可行性评估（**零代码、零提交、不 patch 任何契约与资产文件**）
> **研究对象**：https://github.com/yikart/AiToEarn （MIT License）
> **前置关联文档**（同仓既有深度研究，本件在其之上做 PM 视角的路径/风险收敛）：
> - `docs/research/aiearn-content-marketing-reuse-plan.md`（规划总览）
> - `docs/research/aiearn-asset-mapping.md`（精确资产映射）
> - `docs/research/aiearn-content-marketing-final-decision.md`（合规终裁：MIT 代码可自托管白标，Relay 在线服务 ToS §5.1 禁转授权）

---

## 0. 结论摘要（三段式）

**能否复用**：**能**。AiToEarn 四大 Agent（Create / Publish / Engage / Monetize）中，创作/发布/互动三类与我们 `ai_content` 资产包（Skill/Workflow 能力层）高度对齐，可直接映射或经 1 个 MCP Connector 统一吸收执行缺口——约 **85% 功能以最小修正实现一站式复用**；仅 Monetize（变现市场 + CPS/CPE/CPM 结算）约 15% 缺失且触 L2。

**推荐路径**：**路径 A（design-only reservation，ADR-0017 option-a 预授权）** —— 仅加表 / 契约 stub / 只读 facade，零行为变化、不接入凭证、不实例化，把 AiToEarn 能力映射为 `ai_content` 设计态资产或候选/candidate 草稿（同 agency-agents 试点 B 范式）。执行层终态（自建 / 自托管 MIT 代码）作为**路径 B 待 L2 裁定**，不在本研究落地。

**是否触发 L2 Gate**：**本研究（调查与方案设计）本身不触发任何 Gate**；但若建议「实质性导入」（路径 B：将 AiToEarn 转为真实 Department/Employee/Skill/Workflow 资产，或引入外部平台凭据 / Monetize），则命中 **L2 #3 新市场方向 / #6 外部 Agent 生态导入 / #7 新核心资产体系 / #5 权限边界**，须 **总控决策席（用户/CEO）** 拍板。

**文档路径**：`docs/research/aitoearn-reuse-research.md`

---

## 1. 项目概览表（AiToEarn 是什么 / 能力 / 技术栈 / License / 活跃度）

| 维度 | 内容 |
|---|---|
| **是什么** | 一站式 AI 内容营销智能体（slogan：Monetize · Publish · Engage · Create）。帮 OPC（一人公司）/ 创作者 / 品牌在全球主流平台「构建 → 分发 → 变现」内容。官网 aitoearn.ai。 |
| **四大能力 Agent** | 🎨 **Create**（文生视频/图、批量生成、翻译剪辑，调 Grok/Veo/Seedance/Nano Banana 等）<br>📢 **Publish**（14+ 平台一键分发 + 日历排期）<br>💬 **Engage**（浏览器插件点赞/收藏/关注、AI 智能回复、评论挖掘、品牌监测）<br>💰 **Monetize**（商家推广任务市场，CPS/CPE/CPM 结果导向结算） |
| **形态判定** | **多 Agent 编排**（4 个职能 Agent + `aitoearn-ai` 编排 / `aitoearn-server` 服务分离）；对外经 MCP / OpenClaw 被其他 Agent 消费 |
| **技术栈** | Node.js 20.18 + pnpm + Nx monorepo（aitoearn-ai / aitoearn-server / aitoearn-web）+ Electron 桌面端；MongoDB + Redis（Docker Compose 一键起）；Nginx；SSE 长连接 |
| **集成入口（复用关键）** | ① **MCP**：`https://aitoearn.ai/api/unified/mcp`（国际）/ `aitoearn.cn/api/unified/mcp`（国内），Header `x-api-key`<br>② **OpenClaw 插件**：`npx -y @aitoearn/openclaw-plugin-cli`<br>③ **Docker 私有部署**：`docker compose up -d` |
| **License** | **MIT**（GitHub 代码：可商用 / 私有化 / fork / 白标改造，须保留版权声明）。<br>⚠️ 其**在线服务**（Relay / API）受 ToS §5.1 约束（`solely for your` + `non-sublicensable`）→ **禁止转授权给第三方 / 白标转售**（据 aiearn 终裁文档实测）。 |
| **活跃度** | ≈ 2,614 commits；最近 PR #566（2026-06-23）同步开源 v2.5；README 提供简/英/日三语；持续更新（stars 据既有研究 ≈ 18.8k，2026-07-12，以仓库实时页为准）。 |
| **内容营销子能力对照** | 选题（✅ 经 Create 接收需求创意，无独立选题 Agent）/ 写作（✅）/ 配图（✅）/ 视频（✅）/ 多平台分发（✅）/ 排期（✅）/ 互动（✅）/ **SEO（❌ 未提及）/ 独立数据分析（部分：评论挖掘+品牌监测，无专门 Analytics Agent）** |

---

## 2. 我们内容营销部门现状（资产清点）

> 校验方法：读取 `official-skill-catalog-contract.md` / `tool-catalog-official-plan.md` / `workflow-official-content-plan.md` / `company-package-official-content-plan.md`（设计源），并对运行态 `curis.sqlite` 做只读前缀计数。

### 2.1 `ai_content` 资产包（design-only，官方契约/规划，未实例化）

| 层 | 命名空间 | 数量（据规划文档） | 说明 |
|---|---|---|---|
| Skill（能力 what） | `skl_ai_content_*` | 33 | 选题/内容策划/脚本/视频/分发/运营/SEO/品牌/审核/投放/病毒分析等 |
| Tool（执行 how） | `tl_ai_content_*` | 10+ | web_search / browser_scraper / image_generator / video_generator / text_to_speech / speech_to_text / translation_api / spreadsheet_read / markdown_renderer / youtube_transcript |
| Workflow（编排 order/who） | `wl_ai_content_*` | 12 | content_production / topic_research / script_writing / video_production / seo / editorial_calendar / multichannel_distribution / content_audit / livestream / ugc_campaign / viral_analysis / brand_voice |
| 部门模板 | `dt_content_ops` | design-only 占位 | 尚未填充真实容器 |
| 公司包 | `ccp_ai_content_company` | design-only 占位 | 命名已注册（`ccp_ai_content_*` pattern 合规），内容未填 |

**结构性结论**：catalog 主体是**能力描述层 + 编排层**（Skill/Workflow 饱满），**执行层（Tool）偏抽象**——只有「生成/搜索/爬取」类，缺「真实平台操作」类。与 AiToEarn 形成**能力层 ↔ 执行层互补**。

### 2.2 受控试点 B（agency-agents 外部 Agent 转化）候选态资产

- 来源：`backend/app/agent_conversion/`（agency-agents → Curis `CanonicalAgentSpec` → 候选/draft 资产），独立 CLI `seed_pilot_b.py` 显式 seed 至**独立 DB（curis_pilot_b.sqlite）**，不挂默认 `initialize()`。
- 前缀：`dt_pilot_b_*`（部门）/ `pt_*`（Persona，含内容/商业公司定位）/ `official.employee.*`（员工模板）/ `skl_pilot_b_*`（技能）/ `tl_pilot_b_*`（工具）/ `wt_pilot_b_*`（工作流）。
- 约束：全部 **candidate / draft 态、可回滚**；不接入凭证、不建 Marketplace、不实例化（ADR-0017 锁 Instance/Runtime）。与 AiToEarn 复用同属「外部生态 → Curis 资产」范式，可共用转化 SOP。

### 2.3 运行态 DB 校验结论（2026-07-12，只读）

| 校验项 | 运行态 `curis.sqlite` 结果 |
|---|---|
| `skill_templates` 中 `skl_ai_content_*` | **0 行** |
| `tool_templates` 中 `tl_ai_content_*` | **0 行** |
| `workflow_templates` 中 `wl_ai_content_*` | **0 行** |
| `department_templates` 中 `dt_content_ops` / `dt_ai_content*` / `dt_pilot_b*` | **0 行** |
| `company_packages` 中 `ccp_ai_content*` / `ccp_pilot_b*` | **0 行** |
| `employee_templates` 中 `official.employee.*` | 6 行（基础 6 官方员工，非内容专属） |
| `department_types` 中 `business.*` | 1 行（首个业务型部门类型已注册） |

> **结论**：`ai_content` 与 `pilot_b_*` 资产**当前均未实例化进运行态 DB**（0 行），均为 **design-only / candidate 态**。它们依赖 **Phase-1 Asset Factory Consolidation Gate（C/D/E/F，`issues/phase1_asset_factory_consolidation_gate.md`）** 将设计态提升为真实可查询 Admin catalog 内容；该 gate 已由总控开 gate（OPEN）、安全边界席 2026-07-11 CLEARED，运行时代码 APPROVED 待实现。
> **待确认**：`ai_content` department_type 在 `department_types` 的注册完成度、以及 `dt_content_ops` / `ccp_ai_content_company` 容器字段填充进度（以 Phase-1 整合 gate 实现状态为准，本研究未读取其实现进度）。

---

## 3. 能力 × 资产映射表（AiToEarn 功能 → Curis 模块 → 判定 → 资产类型）

> 符号：✅ 直接复用 ｜ ⚠️ 概念复用但执行层需修正 ｜ 🔧 经 AiToEarn MCP/执行层统一吸收（推荐）｜ ❌ 缺失需新建 / 走 Gate
> 数据来源：`aiearn-asset-mapping.md` §1–§5（深化自官方 catalog 契约）

| AiToEarn 功能 | 对应 Curis 模块 | 资产类型 | 判定 | 说明 |
|---|---|---|---|---|
| 文案/标题/钩子/缩写扩写/标签 | `skl_ai_content_copywriting` / `hook_writing` / `title_optimization` / `content_repurposing` | Skill | ✅ | 能力层饱满，直接复用 |
| 选题/趋势研究/热点追踪 | `skl_ai_content_topic_planning` / `trend_research` | Skill | ✅ | 直接复用 |
| 案例库/病毒分析/内容性能看板 | `skl_ai_content_viral_analysis` / `content_performance_dashboard` | Skill | ✅ | 直接复用 |
| 视频/图片生成（Grok/Veo/Seedance/Nano Banana） | `tl_ai_content_video_generator` / `image_generator` | Tool | ⚠️ | 仅有抽象 generator，**未绑具体模型供应商** |
| 视频翻译 | `tl_ai_content_translation_api` | Tool | ✅ | 直接复用 |
| 视频剪辑/拼接 | —— | Tool | ❌ | **缺视频剪辑 Tool**（有生成无剪辑） |
| 内容再利用（跨平台再编辑再分发） | `skl_ai_content_content_repurposing` | Skill/Workflow | ✅ | 直接复用 |
| 一键分发 14+ 平台 | `wl_ai_content_multichannel_distribution_sop` + `skl_ai_content_multi_platform_distribution` | Workflow/Skill | ⚠️🔧 | **重大缺口**：仅 `browser_scraper`（读非发），缺真实发布连接器 |
| 日历排期执行 | `skl_ai_content_content_calendar` / `wl_ai_content_editorial_calendar_sop` | Skill/Workflow | ⚠️ | 有规划能力，缺真实调度执行引擎 |
| 平台格式/规则自动适配 | `skl_ai_content_platform_algorithm_research` | Skill | ⚠️ | 有算法研究，缺格式适配执行 Tool |
| 自动点赞/收藏/关注 | —— | Tool | ❌ | **缺互动执行连接器** |
| AI 智能回复评论 | `skl_ai_content_community_management` / `ugc_campaign` | Skill | ⚠️ | 有社区管理 skill，缺自动评论回复执行 Tool |
| 评论挖掘（高转化信号） | —— | Skill | ❌ | **缺评论挖掘 Skill** |
| 品牌声量监测 | `skl_ai_content_competitor_content_watch` | Skill | ⚠️ | 偏竞品，品牌声量监测需补 `brand_monitoring` |
| 变现市场/任务池（淘金广场） | ——（`cmcf_*` 冻结） | 新资产 | ❌ + L2 | 需 Marketplace 资产 + 收费规则解冻 |
| CPS/CPE/CPM 结算 | `cmcf_*`（Commercial Configuration，冻结） | 新资产 | ❌ + L2 | 触 L2 #1/#2 收费/商业模式 |
| 线下商户推广任务 | —— | 新场景 | ❌ + L2 | 新商业闭环，无对应资产 |

**复用率估算**：✅ 约 40%（能力层 Skill/Workflow）+ ⚠️🔧 约 45%（经 1 个 MCP Connector 吸收执行缺口，catalog 近乎零修正）+ ❌ 约 15%（Monetize 走 L2）= **85% 最小修正一站式复用**。

---

## 4. 复用映射方案：两条路径

### 4.1 路径 A — design-only reservation（推荐，ADR-0017 预授权）

- **做法**：仅做「加表 / 契约 stub / 只读 facade」，零行为变化。把 AiToEarn 四大能力映射为 `ai_content` 设计态资产登记，或按 agency-agents 试点 B 范式落地为 **candidate / draft 态候选资产**（前缀如 `skl_aite_*` / `tl_aite_*` / `wt_aite_*` / `dt_aite_*`，与既有 33 技能 / 10+ 工具 / 12 工作流零命名冲突）。
- **合规锚点**：ADR-0017 option-a「设计预留、预授权」方向——D1 多租户/部门目录通用化、D2 部门 Manifest 缝、D4 类型级扩展走 gate+ADR。design-only reservation 在 ADR-0017 禁止区之外（不实例化、不接凭证、不建 Marketplace）。
- **范围**：不写执行代码、不接 AiToEarn 服务、不引入外部平台凭据、不碰 Monetize。仅产出「能力↔资产」映射契约与候选元数据。
- **触发 Gate**：**否**（研究 + design-only  reservation 不触 L2）。

### 4.2 路径 B — 实质性导入（真实 Department/Employee/Skill/Workflow 资产）

- **做法**：将 AiToEarn 转为**真实可运行资产**——实例化 Department Template（内容营销部）/ Employee Template（内容运营/分发员）/ Persona / Skill Catalog / Tool Catalog（含真实平台发布/互动 Connector 或自托管 MIT 执行引擎）/ Workflow Template；并可选接入外部平台凭据与 Monetize。
- **两种执行层子形态**（据 aiearn 终裁文档）：
  - **B1 接入式**：把 AiToEarn 当外部 Connector（MCP `x-api-key` 进 Credential Vault）——成本低，但触 L2 #5（权限边界/凭据）。
  - **B2 自托管式**：fork/自托管其 **MIT 代码** 为执行引擎底座 + 注册 Curis 自有平台 OAuth App + 自有 AI key——白标 100% 干净、零 aitoearn 服务费（终裁推荐终态），但运维重，且「外部 Agent 生态导入」本身触 L2。
- **触发 Gate**：**是** —— 外部 Agent 生态导入 → L2 #6（及 #3 新市场方向 / #7 新核心资产体系）；若接外部凭据 → L2 #5；若含 Monetize → L2 #1/#2/#4。

### 4.3 路径对比表（A vs B）

| 维度 | 路径 A：design-only reservation | 路径 B：实质性导入 |
|---|---|---|
| **本质** | 加表 / 契约 stub / 只读 facade，零行为变化 | 转为真实 Department/Employee/Skill/Workflow 资产并运行 |
| **改动量** | 极小（仅元数据/契约登记 + 候选草稿，复用试点 B SOP） | 大（实例化 + 执行层 Connector / 自托管引擎 + 凭据体系） |
| **风险** | 低（无运行依赖、无外部凭据、可回滚） | 中–高（外部依赖 / Relay ToS / 平台封号 / 多租户矛盾 / 合规） |
| **可逆性** | 完全可逆（draft/candidate 态，rollback 脚本齐备） | 部分可逆（实例化资产需独立 future gate 撤回；执行引擎运维债） |
| **是否触发 L2 Gate** | **否**（在 ADR-0017 预授权范围内） | **是**（#3 新市场方向 / #6 外部 Agent 生态导入 / #7 新核心资产体系；接凭据 +#5；含 Monetize +#1/#2/#4） |
| **治理要求** | 设计态登记即可，无需总控拍板 | 须 **总控决策席（用户/CEO）** 走 L2 升级链路：`安全边界席` 边界复核 → 飞书升级 → 总控决策 |
| **与现状衔接** | 直接对齐 `ai_content` design-only 资产 + 试点 B candidate 范式 | 依赖 Phase-1 整合 gate 先完成 `ai_content` 实例化，再叠加执行层 |
| **产出价值时点** | 立即可做（方案/契约/映射），但无运行能力 | 需 gate 批准后分阶段落地（阶段1 产出 MVP → 阶段2 执行层） |

---

## 5. GAP 分析表（复用需补什么 / 可直接用 / 需自建）

| 缺口 | 层 | 类型 | 可直接用（✅） | 需修正/自建（⚠️🔧/❌） | 推荐修正路径 |
|---|---|---|---|---|---|
| 文案/选题/趋势/病毒分析/看板 | Skill | 已有 | ✅ 33 技能覆盖 | — | 直接复用 |
| 内容编排（12 工作流） | Workflow | 已有 | ✅ | — | 直接复用 |
| 视频/图片生成模型绑定 | Tool | ⚠️ 抽象 | 抽象 generator 在 | 未绑 Grok/Veo/Seedance/Nano Banana | 绑定具体供应商，或经执行层吸收 |
| 14+ 平台真实发布 | Tool/Workflow | ❌ 缺失 | — | 仅 `browser_scraper`（读） | 🔧 1 个 Connector 统一吸收（推荐）或逐平台自建 |
| 发布/互动调度引擎 | Workflow/Tool | ⚠️ 执行缺 | 规划能力在 | 缺定时器触发实际发布 | 寄于执行层 Connector |
| 视频剪辑/拼接 | Tool | ❌ 缺失 | — | 有生成无剪辑 | 🔧 经执行层吸收或新增 `video_editor` |
| 互动自动化（点赞/关注/回复） | Tool | ❌ 缺失 | — | 无操作能力 | 🔧 经执行层吸收 |
| 评论挖掘 Skill | Skill | ❌ 缺失 | — | 无对应 skill | 新增 `skl_ai_content_comment_mining` |
| 品牌声量监测 | Skill | ⚠️ 不足 | competitor watch 在 | 偏竞品 | 新增/扩展 `brand_monitoring` |
| Monetize 变现 + 结算 + Marketplace | 新资产 | ❌ + L2 | — | 整体缺失 | 走 L2 #1/#2/#4，未来 gate |

**一句话 GAP**：能力层（Skill/Workflow）我们已基本具备（✅ 40%）；执行层（真实平台操作/剪辑/互动/评论挖掘）是主要缺口（⚠️🔧 45%，经 1 个执行层 Connector 吸收最优）；Monetize 是独立商业闭环（❌ 15%，须 L2）。

---

## 6. L2 Gate 风险清单

### 6.1 运营协定 v2 L2 七项框架（归纳自 `commercial-config-cmcf-proposal.md` / `aiearn-content-marketing-reuse-plan.md` / `agent-conversion-multisource-prd.md`）

| Gate | 名称 | 触发含义 |
|---|---|---|
| **#1** | 商业模式变化 | 定义产品如何赚钱（定价/包装/变现） |
| **#2** | 收费规则变化 | 计费/分账/用量收费逻辑变更 |
| **#3** | 新市场方向 | 内容营销部门作为新业务线纳入产品线 |
| **#4** | Marketplace 开放 | 任务市场 / 淘金广场类资产（红线冻结项；多源扩展曾走 #4 解冻范围） |
| **#5** | 权限边界变化 | 外部平台凭据 / Relay OAuth / Credential Vault 接入 |
| **#6** | 外部 Agent 生态导入 | 外部 Agent 转 Package/Department/Employee/Skill/Workflow |
| **#7** | 新核心资产体系 | 引入超出既有 `cmcf_*`/catalog 范畴的新资产类型 |

### 6.2 本研究触及的 L2 项

| 命中 Gate | 为何命中（本研究语境） | 需谁决策 |
|---|---|---|
| **#3 新市场方向** | 若把「内容营销部门一站式复用 AiToEarn」定位为新增业务线 / 产品线扩展 | **总控决策席（用户/CEO）** |
| **#6 外部 Agent 生态导入** | 路径 B 将 AiToEarn（外部开源 Agent 生态）转为 Curis 真实 Department/Employee/Skill/Tool/Workflow 资产 | **总控决策席（用户/CEO）**（参考 agency-agents 多源扩展曾走 #4 解冻） |
| **#7 新核心资产体系** | 路径 B 若引入 Marketplace / 变现类新资产类型，超出既有 catalog/`cmcf_*` 范畴 | **总控决策席（用户/CEO）** |
| **#5 权限边界变化** | 路径 B 接入外部平台 OAuth / AiToEarn `x-api-key` 进 Credential Vault | **安全边界席** 先行边界复核 → 飞书升级 → 总控 |
| **#1 / #2 / #4（Monetize）** | 仅当路径 B 含 Monetize（变现市场 + CPS/CPE/CPM 结算）时命中 | **总控决策席**（#4 Marketplace 冻结项） |

### 6.3 关键区分（务必明确）

- **本研究（调查 + 方案设计 + design-only 映射）本身不触发任何 L2 Gate**——只读分析、零写入、不 patch 契约。
- **仅当建议「实质性导入」（路径 B）时才触发 L2**——尤其 #3/#6/#7（新市场方向 / 外部 Agent 生态导入 / 新核心资产体系）。这需要作为独立升级项提交总控决策席，不在本研究内落地。
- **路径 A（design-only reservation）完全落在 ADR-0017 option-a 预授权范围内，不触发 L2**，是可立即推进的安全动作。

---

## 7. 下一步建议（3–5 条）

1. **立即推进路径 A（design-only reservation）**：把 AiToEarn 四大能力映射为 `ai_content` 设计态资产登记 / candidate 草稿（前缀 `aite_*`，与既有 33 技能 / 10+ 工具 / 12 工作流零冲突），复用 agency-agents 试点 B 的 `CanonicalAgentSpec` → candidate 转化 SOP；零行为变化、不触 L2。
2. **先完成 Phase-1 资产整合 gate（C/D/E/F）**：当前 `ai_content` 资产仍为 design-only（运行态 DB 0 行），须先由该 gate 把 Skill/Tool/Workflow/Department/Company 包实例化为真实 catalog，路径 A/B 才有挂载容器。
3. **阶段1 跑「只产出 MVP」验证价值**：复用既有 `wl_ai_content_*` / `skl_ai_content_*` 做内容工件产出（文案/脚本/分镜/排期/多平台发布草稿），用户自拷贝分发——零外部依赖、零风险，验证编排与产出质量。
4. **执行层终态（路径 B）单独立项走 L2**：若决定自建/自托管 AiToEarn MIT 代码为执行引擎底座（白标、零服务费）或接外部平台凭据，**作为独立 L2 升级项**提交「安全边界席 边界复核 → 飞书升级 → 总控决策席拍板」，不在本研究落地。
5. **Monetize 单列冻结**：变现市场 + CPS/CPE/CPM 结算触 L2 #1/#2/#4 且 `cmcf_*` 当前冻结，建议维持冻结、留作未来 gate，本期不纳入复用范围。

---

## 8. 参考文档索引

- 规划总览：`docs/research/aiearn-content-marketing-reuse-plan.md`
- 精确映射：`docs/research/aiearn-asset-mapping.md`
- 合规终裁：`docs/research/aiearn-content-marketing-final-decision.md`
- 资产契约：`docs/contracts/official-skill-catalog-contract.md`、`docs/plan/tool-catalog-official-plan.md`、`docs/plan/workflow-official-content-plan.md`、`docs/plan/company-package-official-content-plan.md`
- 治理：`docs/decisions/ADR-0017-multitenant-department-catalog.md`、`issues/phase1_asset_factory_consolidation_gate.md`、`docs/plan/commercial-config-cmcf-proposal.md`、`docs/team/gate-decision-seat-role.md`
- 转化 SOP：`backend/app/agent_conversion/README.md`、`docs/plan/agent-conversion-multisource-prd.md`

---

*—— 研究 / 复用可行性评估文档（零代码、零提交、不 patch 任何契约与资产文件）。产品经理 许清楚 · 2026-07-12。*
